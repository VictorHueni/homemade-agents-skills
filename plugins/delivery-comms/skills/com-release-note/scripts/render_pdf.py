#!/usr/bin/env python3
"""Render a curated release note to an A4 PDF report (plus its HTML intermediate).

Reads the committed release-note Markdown (the single source of truth), parses
its deterministic template structure, and emits:

  * a self-contained A4-print-styled HTML file (always), themed by the same
    token cascade as com-slide-deck / com-artefact-viz — ``templates/
    tokens.fallback.css`` first, then the project's ``docs/ux/tokens.css``
    (auto-detected, or ``--design-system PATH``), project values winning.
    ``tokens.css`` only ever carries font *names* (``--font-body``); if the
    project also self-hosts real font files under ``docs/ux/fonts/fonts.css``
    (plain ``@font-face`` rules, relative ``url()`` to sibling files —
    auto-detected, no flag), those are inlined as base64 data URIs so the
    fonts actually render instead of silently falling back to the CSS stack
    fallback (e.g. Georgia instead of a real serif brand font); and
  * a paginated A4 PDF via headless Chromium (Playwright), with page numbers
    and a link to the version's GitHub Release.

Playwright is an optional dependency — NOT auto-installed. If it is missing,
the HTML is still written and the script fails the PDF step with an explicit
message (print the HTML to PDF from a browser as a fallback).

Usage::

    python render_pdf.py docs/communication/release-notes/v1.4.0-rebooking.md
    python render_pdf.py NOTE.md --release-url https://github.com/o/r/releases/tag/v1.4.0
    python render_pdf.py NOTE.md --design-system docs/ux/tokens.css --output /tmp/note.pdf
    python render_pdf.py NOTE.md --html-only
"""

from __future__ import annotations

import argparse
import base64
import datetime
import html
import math
import os
import re
import subprocess
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_TEMPLATE_DIR = _HERE.parent / "templates"

_PRODUCT_RE = re.compile(r"^\*\*(?:(P\d+)\s*·\s*)?(.+?)\*\*$")
_CAPABILITY_RE = re.compile(r"^\*\*(C\d+(?:\.\d+)*)\s+(.+?)\*\*$")
_ENTRY_RE = re.compile(r"^(?:(C\d+(?:\.\d+)*)\s+)?([^:]{1,60}):\s*(.+)$")
_AUDIT_RE = re.compile(r"^(.*?)\s*\(([0-9A-Za-z\-]{1,12}(?:,\s*[0-9A-Za-z\-]{1,12})*)\)\s*$")
_H1_RE = re.compile(r"^#\s+(v[^:\s]+):\s*(.+?)\s*(?:\(([^()]*)\))?\s*$")
_CHANGELOG_RE = re.compile(r"^\*\*Full Changelog\*\*:\s*(.+)$")


def _fail(message: str) -> None:
    print(f"render_pdf.py: {message}", file=sys.stderr)
    raise SystemExit(1)


def _esc(text: str) -> str:
    return html.escape(text, quote=True)


# Escaping runs first and leaves []() untouched, so these match on escaped text.
_MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_BARE_URL_RE = re.compile(r"^https?://\S+$")
# Only schemes that mean "go read this" — anything else (javascript:, data:) is
# rendered as plain text rather than becoming a live link in a distributed PDF.
_SAFE_URL_RE = re.compile(r"^(?:https?://|mailto:|[./#])", re.I)


def _link_sub(match: re.Match) -> str:
    """[label](url) → an <a>, or the matched text verbatim when url isn't followable.

    Returning the original spelling (rather than the bare label) keeps an
    unrenderable link visible and intact instead of quietly dropping half of it.
    """
    label, url = match.group(1), match.group(2)
    return f'<a href="{url}">{label}</a>' if _SAFE_URL_RE.match(url) else match.group(0)


def _inline(text: str) -> str:
    """Escape, then render Markdown inline code spans and links.

    A release note is a document whose whole job is to point somewhere — at a
    compare range, a PR, a spec — so an authored [text](url) has to survive into
    the PDF as a live link rather than printing its own syntax.
    """
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", _esc(text))
    return _MD_LINK_RE.sub(_link_sub, out)


# ---------------------------------------------------------------- parsing ----

def _split_frontmatter(text: str) -> tuple[dict, str]:
    """Line-based frontmatter parse (stdlib only — no PyYAML dependency)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    meta: dict[str, str] = {}
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return meta, "\n".join(lines[i + 1:])
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if m:
            meta[m.group(1)] = m.group(2).strip().strip('"')
    return {}, text  # unterminated frontmatter — treat as body


# Heading keyword -> model key. "fix" is tested before "new" so a heading like
# "Fixes and new improvements" resolves to the fixes section, not What's new.
_SECTION_KEYS = (("fix", "fixes"), ("platform", "platform"), ("breaking", "breaking"), ("new", "products"))
_RECOGNISED_SECTIONS = ("What's new", "Fixes and improvements", "Platform and engineering",
                        "Breaking changes")


def _section_for(heading: str) -> str | None:
    """The model key a `## heading` feeds, or None if the heading is unrecognised."""
    lowered = heading.lower()
    for needle, key in _SECTION_KEYS:
        if needle in lowered:
            return "whats-new" if key == "products" else key
    return None


def _parse_entry(text: str) -> dict:
    """Split a bullet into optional FBS ref, bold label, body text, audit IDs."""
    audit = ""
    m = _AUDIT_RE.match(text)
    if m and any(ch.isdigit() for ch in m.group(2)):
        text, audit = m.group(1), m.group(2)
    m = _ENTRY_RE.match(text)
    if m:
        return {"ref": m.group(1) or "", "label": m.group(2), "text": m.group(3), "audit": audit}
    return {"ref": "", "label": "", "text": text, "audit": audit}


def parse_note(text: str) -> dict:
    """Parse the release-note template structure into a model dict."""
    meta, body = _split_frontmatter(text)
    model: dict = {"meta": meta, "version": "", "theme": "", "daterange": "",
                   "framing": "", "products": [], "fixes": [], "platform": [],
                   "breaking": [], "changelog": "", "unknown": []}
    section = None
    product = None
    group = None
    for raw in body.splitlines():
        line = raw.strip()
        if not line or line.startswith("<!--"):
            continue
        h1 = _H1_RE.match(line)
        if h1:
            model["version"], model["theme"] = h1.group(1), h1.group(2)
            model["daterange"] = h1.group(3) or ""
            continue
        if line.startswith("## "):
            heading = line[3:].strip()
            section = _section_for(heading)
            if section is None:
                # Tracked, not dropped in silence — build_html warns about these.
                model["unknown"].append({"heading": heading, "bullets": 0})
            product = None
            group = None
            continue
        cl = _CHANGELOG_RE.match(line)
        if cl:
            model["changelog"] = cl.group(1)
            continue
        if line.startswith(">") and not model["framing"]:
            model["framing"] = line.lstrip("> ").strip("_ ")
            continue
        # Capability header checked before product: both are bare **bold** lines,
        # but a capability always carries a C-ref — check the more specific pattern
        # first so "**C2.2 Regulatory Change Monitoring**" isn't mistaken for a
        # second product.
        cm = _CAPABILITY_RE.match(line)
        if cm and section == "whats-new" and product is not None:
            group = {"id": cm.group(1), "name": cm.group(2), "entries": []}
            product["groups"].append(group)
            continue
        pm = _PRODUCT_RE.match(line)
        if pm and section == "whats-new":
            product = {"id": pm.group(1) or "", "name": pm.group(2), "groups": []}
            model["products"].append(product)
            group = None
            continue
        if line.startswith("- "):
            entry = _parse_entry(line[2:])
            if section == "whats-new":
                if product is None:  # graceful degradation — note without product headers
                    product = {"id": "", "name": "", "groups": []}
                    model["products"].append(product)
                if group is None:  # no capability header seen yet — flat, unnamed group
                    group = {"id": "", "name": "", "entries": []}
                    product["groups"].append(group)
                group["entries"].append(entry)
            elif section in ("fixes", "platform", "breaking"):
                model[section].append(entry)
            elif model["unknown"]:
                model["unknown"][-1]["bullets"] += 1
    if not model["version"]:
        _fail("no release H1 found (expected '# vX.Y.Z: theme (dates)') — is this a curated note?")
    return model


# -------------------------------------------------------------- rendering ----

def _entry_html(entry: dict, number: int | None = None, titled: bool = False) -> str:
    """One entry.

    `number` gives a sequence handle to entries carrying no FBS ref of their own,
    in the same accent chip, so both read as the same kind of handle. `titled`
    promotes the label to a heading with the text beneath — the treatment What's
    new gives a capability — for a tier whose entries are themselves groupings
    rather than leaf items.
    """
    ref, num_class = entry["ref"], ""
    if not ref and number is not None:
        ref, num_class = f"{number:02d}", " entry-num"
    chip = f'<span class="entry-ref{num_class}">{_esc(ref)}</span>' if ref else ""

    body = _inline(entry["text"])
    if entry["audit"]:
        body += f'<span class="entry-audit">({_esc(entry["audit"])})</span>'

    if titled and entry["label"]:
        # Same heading class the capability groups use, so the two tiers match.
        return (f'<li class="entry--titled">'
                f'<h3 class="capability-label">{chip}{_inline(entry["label"])}</h3>'
                f"<div>{body}</div></li>")

    label = f'<span class="entry-label">{_inline(entry["label"])}:</span> ' if entry["label"] else ""
    return f"<li>{chip}{label}{body}</li>"


def _changelog_cell(changelog: str) -> str:
    """The Full changelog row: a link when the note gives one, code otherwise.

    The template's own convention is a bare compare range (`v1.3.0...v1.4.0`),
    which is an identifier and reads as code. But an author who wrote a Markdown
    link — or pasted the compare URL — meant it to be followable, and the
    cartouche is exactly where this document puts its links.
    """
    value = (changelog or "").strip()
    if not value:
        return ""
    m = _MD_LINK_RE.fullmatch(value)
    if m and _SAFE_URL_RE.match(m.group(2)):
        return f'<a href="{_esc(m.group(2))}">{_esc(m.group(1))}</a>'
    if _BARE_URL_RE.match(value):
        return f'<a href="{_esc(value)}">{_esc(value)}</a>'
    return f"<code>{_esc(value)}</code>"


def _cartouche(model: dict, release_url: str, note_label: str, today: str) -> str:
    """The title block under the summary: all release metadata, in place of a footer.

    Rows with nothing to show are omitted, so a note without a changelog line or
    outside a GitHub repo simply carries a shorter block.
    """
    meta = model["meta"]
    rows = [
        ("Period", _esc(model["daterange"])),
        ("Owner", _esc(meta.get("owner", ""))),
        ("Status", _esc(meta.get("status", ""))),
        ("Full changelog", _changelog_cell(model["changelog"])),
        ("Release notes", f'<a href="{_esc(release_url)}">{_esc(release_url)}</a>' if release_url else ""),
        ("Generated", f'com-release-note on {_esc(today)} from <code>{_esc(note_label)}</code>. '
                      f'Source note is the single source of truth; re-render after edits.'),
    ]
    cells = "".join(f'<div class="cart-row"><span class="cart-k">{key}</span>'
                    f'<span class="cart-v">{value}</span></div>'
                    for key, value in rows if value)
    return f'<div class="cartouche">{cells}</div>'


_RANGE_RE = re.compile(r"(v?[\w.\-]+)\.\.\.?(v?[\w.\-]+)")


def _compact(n: int) -> str:
    """Stat-tile number formatting: thousands-separated, then compact past 5 digits."""
    return f"{n:,}" if n < 10_000 else f"{n / 1000:.1f}k"


def _git_stats(note_path: Path, changelog: str, exclude_paths: list[str] | None = None) -> dict:
    """Commits, active days and lines changed for the note's changelog range.

    Deterministic and offline: the range comes from the note's own Full Changelog
    line. A repo without those tags (or no git) yields nothing, and the affected
    cards are omitted rather than guessed.

    `exclude_paths` scopes only the lines-changed measure (via git pathspec
    exclusion, e.g. ["docs/**", "*.md"]) — commits and active days still count
    the whole range, since those describe the release's cadence, not its code
    volume. A project whose release note is dominated by generated seeds or
    plan-execution logs (not source) would otherwise report a "lines changed"
    figure that is mostly non-code.
    """
    match = _RANGE_RE.search(changelog or "")
    if not match:
        return {}
    rng = f"{match.group(1)}..{match.group(2)}"
    cwd = str(note_path.parent.resolve())

    def run(args: list[str]) -> str | None:
        try:
            return subprocess.run(["git", "-C", cwd, *args],
                                  capture_output=True, text=True, check=True).stdout
        except (OSError, subprocess.CalledProcessError):
            return None

    count = run(["rev-list", "--count", rng])
    if count is None or not count.strip().isdigit():
        return {}
    stats = {"commits": count.strip()}
    dates = run(["log", "--format=%cs", rng])
    if dates is not None:
        stats["active_days"] = len({d for d in dates.split() if d}) or ""
    pathspec = ["--", ".", *[f":!{p}" for p in exclude_paths]] if exclude_paths else []
    short = run(["diff", "--shortstat", rng, *pathspec]) or ""
    added = re.search(r"(\d+) insertion", short)
    removed = re.search(r"(\d+) deletion", short)
    if added or removed:
        stats["lines"] = (int(added.group(1)) if added else 0,
                          int(removed.group(1)) if removed else 0)
        stats["lines_scoped"] = bool(exclude_paths)
    return stats


def _measures(model: dict) -> dict:
    """Counts over the parsed note. Structural arithmetic only — no judgement."""
    caps = sum(len(g["entries"]) for p in model["products"] for g in p["groups"])
    days = ""
    dates = re.findall(r"\d{4}-\d{2}-\d{2}", model["daterange"])
    if len(dates) == 2:
        try:
            start, end = (datetime.date.fromisoformat(d) for d in dates)
            days = (end - start).days
        except ValueError:
            days = ""
    return {"products": len(model["products"]), "caps": caps, "fixes": len(model["fixes"]),
            "platform": len(model["platform"]), "breaking": len(model["breaking"]),
            "total": caps + len(model["fixes"]) + len(model["platform"]) + len(model["breaking"]),
            "days": days}


_HEX_RE = re.compile(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b")
_TOKEN_DEFAULTS = {"accent": "#3b6ef5", "ink": "#1a1f29", "surface": "#ffffff"}


def _resolve_token(css_text: str, name: str) -> str:
    """The hex value a --name custom property resolves to, last declaration wins.

    A regex scan over the assembled CSS text (fallback, then project — the same
    cascade order the stylesheet itself uses), not a real CSS parser: sufficient
    because every token file declares these as plain hex literals. Falls back to
    the kit's own neutral default if the property is never declared (e.g. a
    project tokens.css that doesn't define --ink).
    """
    matches = re.findall(rf"--{name}:\s*([^;]+);", css_text)
    for value in reversed(matches):  # last declaration in the cascade wins
        hexm = _HEX_RE.search(value)
        if hexm:
            return "#" + hexm.group(1)
    return _TOKEN_DEFAULTS[name]


def _hex_to_rgb(hex_value: str) -> tuple[int, int, int]:
    h = hex_value.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _mix_hex(hex_a: str, pct_a: float, hex_b: str) -> str:
    """color-mix(in srgb, A pct_a%, B) computed in Python: a linear per-channel
    blend of the encoded sRGB bytes, matching the CSS Color 4 semantics for two
    opaque colours. Baking the result as a literal hex string (rather than
    leaving color-mix() to resolve live) sidesteps a real divergence observed
    between environments when color-mix() is nested inside a gradient's stop
    list during PDF export — plain `background: color-mix(...)` rendered
    correctly everywhere tested, but the identical expression inside
    conic-gradient(...) did not on at least one reader's setup."""
    ra, ga, ba = _hex_to_rgb(hex_a)
    rb, gb, bb = _hex_to_rgb(hex_b)
    t = pct_a / 100
    mix = lambda a, b: round(a * t + b * (1 - t))  # noqa: E731
    return f"#{mix(ra, rb):02x}{mix(ga, gb):02x}{mix(ba, bb):02x}"


def _donut_steps(tokens: dict) -> tuple[str, str, str, str]:
    """Ordinal ramp of the accent hue, as literal hex — see _mix_hex for why not
    color-mix(). The four sections are tiers, so one hue with monotone lightness
    is the right colour job (validated: monotone L, adjacent dL, light-end
    contrast, single hue). Dark to light, in slice order."""
    accent, ink, surface = tokens["accent"], tokens["ink"], tokens["surface"]
    return (
        _mix_hex(accent, 55, ink),
        _mix_hex(accent, 78, ink),
        accent,
        _mix_hex(accent, 72, surface),
    )


_SLICE_GAP_DEG = 1.4  # blank separator between slices, ~2px at this radius

# Ring geometry in viewBox units. The thickness matches the .donut-hole inset in
# report.html.tmpl (6.5mm of a 28mm figure); keep the two in step.
_RING_THICKNESS = 100 * 6.5 / 28
_RING_RADIUS = 50 - _RING_THICKNESS / 2


def _donut_svg(slices: list, total: int, tokens: dict) -> str:
    """The composition ring as flat-filled SVG arcs.

    Deliberately NOT a CSS conic-gradient: Chromium compiles one into a PDF
    function-based shading (/ShadingType 1 driven by a /FunctionType 4
    PostScript calculator), the least-supported corner of the shading spec —
    correct in some readers and wildly wrong in others (observed: the whole ring
    rendering pink). The ring is discrete slices, not a blend, so stroked arc
    segments express the intent directly and are plain vector fills every reader
    draws identically. Arcs are stroked on one circle via dash offsets, so a
    slice's angular position needs no path arithmetic.
    """
    steps = _donut_steps(tokens)
    circumference = 2 * math.pi * _RING_RADIUS
    arcs, angle = [], 0.0
    for i, (_label, count) in enumerate(slices):
        span = 360 * count / total
        drawn = max(span - _SLICE_GAP_DEG, 0.0)  # the gap is undrawn, not painted over
        arc = circumference * drawn / 360
        arcs.append(
            f'<circle cx="50" cy="50" r="{_RING_RADIUS:.2f}" fill="none" '
            f'stroke="{steps[i % len(steps)]}" stroke-width="{_RING_THICKNESS:.2f}" '
            f'stroke-dasharray="{arc:.2f} {circumference - arc:.2f}" '
            f'stroke-dashoffset="{-circumference * angle / 360:.2f}"/>'
        )
        angle += span
    # Rotate so slice one starts at twelve o'clock, as a conic gradient would.
    return (f'<svg class="donut-svg" viewBox="0 0 100 100" role="presentation">'
            f'<g transform="rotate(-90 50 50)">{"".join(arcs)}</g></svg>')


def _recap(model: dict, git: dict, tokens: dict) -> str:
    """Donut of the release's composition, with context cards beside it.

    The donut and its legend stay together as one figure; the cards carry only
    measures the donut does not already show, so no number appears twice.
    """
    m = _measures(model)
    if not m["total"]:
        return ""
    slices = [("New capabilities", m["caps"]), ("Platform items", m["platform"]),
              ("Fixes", m["fixes"]), ("Breaking changes", m["breaking"])]
    slices = [(label, count) for label, count in slices if count]

    donut_steps = _donut_steps(tokens)
    # The legend carries every value, so close slices are read as numbers, not arcs.
    legend = "".join(
        f'<div class="dl-row">'
        f'<span class="dl-sw" style="background:{donut_steps[i % len(donut_steps)]}"></span>'
        f'<span class="dl-k">{_esc(label)}</span><span class="dl-v">{count}</span>'
        f'<span class="dl-p">{round(100 * count / m["total"])}%</span></div>'
        for i, (label, count) in enumerate(slices)
    )

    # Signs alone distinguish added from removed: colouring them good/bad would
    # assert a judgement the numbers do not carry (deleted code is often a win).
    lines = git.get("lines")
    lines_html = (f'<span class="rc-pair">+{_compact(lines[0])} &#8722;{_compact(lines[1])}</span>'
                  if lines else "")
    lines_label = "Lines (code)" if git.get("lines_scoped") else "Lines"
    cards = [("Days", m["days"]), ("Active days", git.get("active_days", "")),
             ("Commits", git.get("commits", "")), (lines_label, lines_html)]
    card_html = "".join(f'<div class="recap-card"><div class="rc-k">{key}</div>'
                        f'<div class="rc-v">{value}</div></div>'
                        for key, value in cards if value != "" and value is not None)

    return (f'<div class="recap"><div class="recap-label">Release at a glance</div>'
            f'<div class="recap-body">'
            f'<div class="recap-figure">'
            f'<div class="donut">{_donut_svg(slices, m["total"], tokens)}'
            f'<div class="donut-hole"><span class="donut-total">{m["total"]}</span>'
            f'<span class="donut-cap">entries</span></div></div>'
            f'<div class="donut-legend">{legend}</div></div>'
            f'<div class="recap-cards">{card_html}</div>'
            f'</div></div>')


def _bucket_section(label: str, entries: list[dict], page_break: bool = False,
                    titled: bool = False) -> str:
    """One card holding every entry — the same shape a product card takes in
    What's new, so both tiers read as a block of related items rather than a
    stack of loose cards. Used by Fixes and by Platform and engineering.

    `titled` numbers each entry and gives its label a heading, for a tier whose
    entries are groupings in their own right (the Platform buckets). Leave it off
    for leaf items such as individual fixes, which read better as run-in labels.
    """
    if not entries:
        return ""
    items = "".join(_entry_html(e, i if titled else None, titled)
                    for i, e in enumerate(entries, start=1))
    cls = "section section--page-break" if page_break else "section"
    return (f'<section class="{cls}"><div class="section-label">{_esc(label)}</div>'
            f'<div class="bucket"><ul class="entry-list">{items}</ul></div></section>')


def render_content(model: dict, release_url: str, note_label: str, today: str, git: dict,
                   tokens: dict) -> str:
    out = []
    out.append(f'<div class="report-kicker">Release note · {_esc(model["version"])}</div>')
    out.append(f'<h1 class="report-title">{_esc(model["theme"])}</h1>')
    if model["framing"]:
        out.append(f'<p class="report-framing">{_inline(model["framing"])}</p>')
    out.append(_cartouche(model, release_url, note_label, today))
    out.append(_recap(model, git, tokens))

    if model["products"]:
        out.append('<section class="section section--page-break">'
                   '<div class="section-label">What&#x2019;s new</div>')
        for product in model["products"]:
            out.append('<div class="product-card">')
            if product["name"]:
                chip = f'<span class="product-id">{_esc(product["id"])}</span>' if product["id"] else ""
                out.append(f'<h2 class="product-name">{chip}{_esc(product["name"])}</h2>')
            for group in product["groups"]:
                out.append('<div class="capability-group">')
                if group["name"]:
                    chip = (f'<span class="entry-ref">{_esc(group["id"])}</span>' if group["id"] else "")
                    out.append(f'<h3 class="capability-label">{chip}{_esc(group["name"])}</h3>')
                out.append('<ul class="entry-list">' +
                           "".join(_entry_html(e) for e in group["entries"]) + "</ul></div>")
            out.append("</div>")
        out.append("</section>")

    out.append(_bucket_section("Fixes and improvements", model["fixes"]))
    out.append(_bucket_section("Platform and engineering", model["platform"],
                               page_break=True, titled=True))

    if model["breaking"]:
        out.append('<section class="section section--breaking">'
                   '<div class="section-label">Breaking changes</div>'
                   '<div class="breaking"><ul class="entry-list">' +
                   "".join(_entry_html(e) for e in model["breaking"]) + "</ul></div></section>")
    return "\n".join(out)


def _design_system_css(explicit: str | None) -> str:
    """Same token layering as com-slide-deck / com-artefact-viz: fallback, then project (wins)."""
    css = (_TEMPLATE_DIR / "tokens.fallback.css").read_text(encoding="utf-8")
    sheet = Path(explicit) if explicit else Path("docs/ux/tokens.css")
    if explicit and not sheet.is_file():
        _fail(f"--design-system not found: {sheet}")
    if sheet.is_file():
        if not explicit:
            print(f"using shared design system {sheet} (pass --design-system to override)")
        css += "\n\n/* ---- project design system (overrides) ---- */\n" + sheet.read_text(encoding="utf-8")
    return css


_FONT_URL_RE = re.compile(r"url\(\s*\.?/?([^)'\"]+\.woff2?)\s*\)")


def _embed_fonts(fonts_dir: Path) -> str:
    """Inline docs/ux/fonts/fonts.css's @font-face rules with base64 font data.

    tokens.css only ever carries font *names* (--font-body, --font-mono); nothing
    loads the actual font file, so a project's brand font silently falls through
    to its CSS fallback in headless Chromium. A project that self-hosts real font
    files opts in with docs/ux/fonts/fonts.css (plain @font-face rules, relative
    url() to sibling files — the same shape a package like @fontsource ships).
    Absent file -> no CSS, same silent degrade as the rest of the token cascade.
    """
    css_path = fonts_dir / "fonts.css"
    if not css_path.is_file():
        return ""

    def _inline_one(match: re.Match) -> str:
        rel = match.group(1)
        font_path = fonts_dir / rel
        if not font_path.is_file():
            _fail(f"{css_path} references a missing font file: {font_path}")
        data = base64.b64encode(font_path.read_bytes()).decode("ascii")
        mime = "font/woff2" if font_path.suffix == ".woff2" else "font/woff"
        return f"url(data:{mime};base64,{data})"

    print(f"embedding self-hosted fonts from {css_path}")
    return _FONT_URL_RE.sub(_inline_one, css_path.read_text(encoding="utf-8"))


_GITHUB_REMOTE_RE = re.compile(r"github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/]+?)(?:\.git)?$")


def _github_release_url(note_path: Path, version: str, explicit: str | None) -> str:
    """URL of the GitHub Release for this version, from --release-url or git origin.

    Read-only and best-effort: a note outside a repo, a non-GitHub remote, or a
    missing git simply yields no link rather than a failed render.
    """
    if explicit:
        return explicit
    if not version:
        return ""
    try:
        # `git config --get` (not `remote get-url`): the latter applies url.*.insteadOf
        # rewrites, which can turn a GitHub origin into a mirror or proxy address.
        remote = subprocess.run(["git", "-C", str(note_path.parent.resolve()),
                                 "config", "--get", "remote.origin.url"],
                                capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return ""
    m = _GITHUB_REMOTE_RE.search(remote)
    return f"https://github.com/{m['owner']}/{m['repo']}/releases/tag/{version}" if m else ""


def _warn_unknown_sections(model: dict) -> None:
    """Never drop an authored section in silence — say what was skipped and why."""
    if not model["unknown"]:
        return
    print(f"render_pdf.py: WARNING: {len(model['unknown'])} section(s) not recognised, "
          f"omitted from the report:", file=sys.stderr)
    for item in model["unknown"]:
        dropped = f", {item['bullets']} bullet(s) dropped" if item["bullets"] else ""
        print(f"  - \"{item['heading']}\"{dropped}", file=sys.stderr)
    print(f"  Recognised headings: {', '.join(_RECOGNISED_SECTIONS)}. "
          f"Rename the section, or fold its content into one of these.", file=sys.stderr)


def build_html(note_path: Path, design_system: str | None, release_url: str | None,
               exclude_paths: list[str] | None = None) -> str:
    model = parse_note(note_path.read_text(encoding="utf-8"))
    _warn_unknown_sections(model)
    today = datetime.date.today().isoformat()
    url = _github_release_url(note_path, model["version"], release_url)
    try:
        note_label = os.path.relpath(note_path)
    except ValueError:
        note_label = str(note_path)
    tmpl = (_TEMPLATE_DIR / "report.html.tmpl").read_text(encoding="utf-8")
    title = model["meta"].get("title") or f'{model["version"]}: {model["theme"]}'
    fonts_css = _embed_fonts(Path("docs/ux/fonts"))
    design_css = _design_system_css(design_system)
    all_css = fonts_css + "\n\n" + design_css if fonts_css else design_css
    tokens = {name: _resolve_token(all_css, name) for name in _TOKEN_DEFAULTS}
    for key, value in {"TITLE": _esc(title),
                       "DESIGN_SYSTEM_CSS": all_css,
                       "CONTENT": render_content(model, url, note_label, today,
                                                 _git_stats(note_path, model["changelog"], exclude_paths),
                                                 tokens)}.items():
        tmpl = tmpl.replace("{{" + key + "}}", value)
    return tmpl


# ------------------------------------------------------------- PDF export ----

# Margins for every page.pdf() call (probe and final render alike).
_PDF_MARGIN = {"top": "14mm", "right": "16mm", "bottom": "18mm", "left": "16mm"}
_PAGE_COUNT_RE = re.compile(rb"/Type\s*/Page[^s]")

_MIN_SCALE = 0.85  # readability floor: 10.5pt body stays ≥ 8.9pt effective


def _fit_scale(page) -> float:
    """Largest scale in [_MIN_SCALE, 1.0] that needs the fewest pages.

    Content ending just past a page boundary — often only the atomic document
    footer — buys a whole extra, near-empty page. A shrink of a few percent is
    barely perceptible and usually reclaims it. Probe Chromium's real pagination
    at each scale (screen-media measurements diverge from print layout) and take
    the largest scale achieving the minimum page count; when shrinking saves
    nothing, that is 1.0 and the document renders untouched. The floor keeps
    body text readable — past it, an extra page is the honest answer.
    """
    # The probe omits the running header/footer deliberately: they render inside the
    # reserved margin boxes, so they cannot change the page count (verified — counts
    # match with and without them), and leaving them out keeps each probe cheaper.
    def pages(scale: float) -> int:
        return len(_PAGE_COUNT_RE.findall(page.pdf(format="A4", scale=scale, margin=_PDF_MARGIN)))

    steps = int(round((1.0 - _MIN_SCALE) * 100)) + 1
    counts = {round(1.0 - step / 100, 2): None for step in range(steps)}
    for scale in counts:
        counts[scale] = pages(scale)
    fewest = min(counts.values())
    return max(scale for scale, n in counts.items() if n == fewest)

# Chromium renders these into the page-margin boxes. They are a separate document
# from the report, so design tokens cannot reach them — hence inline styles and a
# neutral grey rather than var(--muted). Keep them quiet: this is page furniture.
_CHROME_STYLE = ("width:100%;padding:0 16mm;font-family:ui-monospace,Menlo,monospace;"
                 "font-size:8px;color:rgba(130,130,130,.95);display:flex;"
                 "justify-content:space-between;align-items:center;")


def _header_template(running_title: str) -> str:
    """Running head: identifies a page that has been separated from the document."""
    if not running_title:
        return "<span></span>"
    return (f'<div style="{_CHROME_STYLE}padding-bottom:2mm;">'
            f'<span>{html.escape(running_title)}</span><span></span></div>')


def _footer_template(version: str) -> str:
    """Version on the left, page position on the right."""
    left = f"Release note · {html.escape(version)}" if version else ""
    return (f'<div style="{_CHROME_STYLE}">'
            f'<span>{left}</span>'
            f'<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')


def render_pdf(html_path: Path, pdf_path: Path, running_title: str = "", version: str = "") -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        _fail(
            f"Playwright is not available — PDF step skipped (this script never auto-installs).\n"
            f"  The HTML was written to {html_path}; open it in a browser and print to PDF,\n"
            f"  or provision Playwright (pip install playwright && python -m playwright install chromium) and re-run."
        )
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception as exc:  # noqa: BLE001 — surface a clean message
            _fail(f"could not launch Chromium ({exc}). The HTML was written to {html_path}; "
                  f"ensure Playwright's Chromium build is available and re-run.")
        page = browser.new_page()
        page.emulate_media(media="screen")
        page.goto(html_path.resolve().as_uri(), wait_until="networkidle")
        page.evaluate("() => document.fonts.ready")
        # Drop the screen wrapper padding, whose overflow can mint a blank trailing
        # page. The template's @page margins are left alone: they match _PDF_MARGIN,
        # so Chromium paginates against the same box it prints into.
        page.add_style_tag(content=".report { padding: 0; }")
        scale = _fit_scale(page)
        if scale < 1.0:
            print(f"render_pdf.py: scaled to {scale:.2f} to save a page")
        page.pdf(
            path=str(pdf_path),
            format="A4",
            scale=scale,
            print_background=True,
            display_header_footer=True,
            header_template=_header_template(running_title),
            footer_template=_footer_template(version),
            margin=_PDF_MARGIN,
        )
        browser.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render a curated release note to an A4 PDF report (HTML intermediate always written)."
    )
    parser.add_argument("note", type=Path, help="Path to the curated release-note Markdown.")
    parser.add_argument("--design-system", help="Project token sheet (default: auto-detect docs/ux/tokens.css).")
    parser.add_argument("--release-url",
                        help="GitHub Release URL (default: derived from the repo's origin remote + version).")
    parser.add_argument("--output", type=Path,
                        help="Output PDF path (default: <note-dir>/pdf/<note-stem>.pdf).")
    parser.add_argument("--html-only", action="store_true", help="Write the HTML and skip the PDF step.")
    parser.add_argument("--exclude-path", action="append", default=[], metavar="PATHSPEC",
                        help="Git pathspec to exclude from the recap's 'Lines' card (repeatable), "
                             "e.g. --exclude-path 'docs/**' --exclude-path '*.md'. Scopes only that "
                             "measure to code churn; commits and active days still cover the full "
                             "range. Omit to keep the whole-tree diff (default, unchanged behaviour).")
    args = parser.parse_args(argv)

    if not args.note.is_file():
        _fail(f"note not found: {args.note}")
    pdf_path = args.output or args.note.parent / "pdf" / f"{args.note.stem}.pdf"
    html_path = pdf_path.with_suffix(".html")
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    html_path.write_text(
        build_html(args.note, args.design_system, args.release_url, args.exclude_path),
        encoding="utf-8")
    print(f"render_pdf.py: wrote {html_path}")
    if args.html_only:
        return 0

    model = parse_note(args.note.read_text(encoding="utf-8"))
    running = model["meta"].get("title") or f'{model["version"]}: {model["theme"]}'
    render_pdf(html_path, pdf_path, running, model["version"])
    print(f"render_pdf.py: wrote {pdf_path} ({pdf_path.stat().st_size / 1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

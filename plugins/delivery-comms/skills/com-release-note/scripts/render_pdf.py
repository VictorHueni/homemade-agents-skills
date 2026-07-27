#!/usr/bin/env python3
"""Render a curated release note to an A4 PDF report (plus its HTML intermediate).

Reads the committed release-note Markdown (the single source of truth), parses
its deterministic template structure, and emits:

  * a self-contained A4-print-styled HTML file (always), themed by the same
    token cascade as com-slide-deck / com-artefact-viz — ``templates/
    tokens.fallback.css`` first, then the project's ``docs/ux/tokens.css``
    (auto-detected, or ``--design-system PATH``), project values winning.
    ``tokens.css`` only ever carries font *names* (``--font-sans``); if the
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
import os
import re
import subprocess
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_TEMPLATE_DIR = _HERE.parent / "templates"

_PRODUCT_RE = re.compile(r"^\*\*(?:(P\d+)\s*·\s*)?(.+?)\*\*$")
_ENTRY_RE = re.compile(r"^(?:(C\d+(?:\.\d+)*)\s+)?([^:]{1,60}):\s*(.+)$")
_AUDIT_RE = re.compile(r"^(.*?)\s*\(([0-9A-Za-z\-]{1,12}(?:,\s*[0-9A-Za-z\-]{1,12})*)\)\s*$")
_H1_RE = re.compile(r"^#\s+(v[^:\s]+):\s*(.+?)\s*(?:\(([^()]*)\))?\s*$")
_CHANGELOG_RE = re.compile(r"^\*\*Full Changelog\*\*:\s*(.+)$")


def _fail(message: str) -> None:
    print(f"render_pdf.py: {message}", file=sys.stderr)
    raise SystemExit(1)


def _esc(text: str) -> str:
    return html.escape(text, quote=True)


def _inline(text: str) -> str:
    """Escape, then render Markdown inline code spans (`x` → <code>x</code>)."""
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", _esc(text))


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
            continue
        cl = _CHANGELOG_RE.match(line)
        if cl:
            model["changelog"] = cl.group(1)
            continue
        if line.startswith(">") and not model["framing"]:
            model["framing"] = line.lstrip("> ").strip("_ ")
            continue
        pm = _PRODUCT_RE.match(line)
        if pm and section == "whats-new":
            product = {"id": pm.group(1) or "", "name": pm.group(2), "entries": []}
            model["products"].append(product)
            continue
        if line.startswith("- "):
            entry = _parse_entry(line[2:])
            if section == "whats-new":
                if product is None:  # graceful degradation — note without product headers
                    product = {"id": "", "name": "", "entries": []}
                    model["products"].append(product)
                product["entries"].append(entry)
            elif section in ("fixes", "platform", "breaking"):
                model[section].append(entry)
            elif model["unknown"]:
                model["unknown"][-1]["bullets"] += 1
    if not model["version"]:
        _fail("no release H1 found (expected '# vX.Y.Z: theme (dates)') — is this a curated note?")
    return model


# -------------------------------------------------------------- rendering ----

def _entry_html(entry: dict) -> str:
    parts = ["<li>"]
    if entry["ref"]:
        parts.append(f'<span class="entry-ref">{_esc(entry["ref"])}</span>')
    if entry["label"]:
        parts.append(f'<span class="entry-label">{_inline(entry["label"])}:</span> ')
    parts.append(_inline(entry["text"]))
    if entry["audit"]:
        parts.append(f'<span class="entry-audit">({_esc(entry["audit"])})</span>')
    parts.append("</li>")
    return "".join(parts)


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
        ("Full changelog", f'<code>{_esc(model["changelog"])}</code>' if model["changelog"] else ""),
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


def _git_stats(note_path: Path, changelog: str) -> dict:
    """Commits, active days and lines changed for the note's changelog range.

    Deterministic and offline: the range comes from the note's own Full Changelog
    line. A repo without those tags (or no git) yields nothing, and the affected
    cards are omitted rather than guessed.
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
    short = run(["diff", "--shortstat", rng]) or ""
    added = re.search(r"(\d+) insertion", short)
    removed = re.search(r"(\d+) deletion", short)
    if added or removed:
        stats["lines"] = (int(added.group(1)) if added else 0,
                          int(removed.group(1)) if removed else 0)
    return stats


def _measures(model: dict) -> dict:
    """Counts over the parsed note. Structural arithmetic only — no judgement."""
    caps = sum(len(p["entries"]) for p in model["products"])
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


# Ordinal ramp of the accent hue: the four sections are tiers, so one hue with
# monotone lightness is the right colour job (validated: monotone L, adjacent dL,
# light-end contrast, single hue). Dark to light, in slice order.
_DONUT_STEPS = (
    "color-mix(in srgb, var(--accent) 55%, var(--ink))",
    "color-mix(in srgb, var(--accent) 78%, var(--ink))",
    "var(--accent)",
    "color-mix(in srgb, var(--accent) 72%, var(--surface))",
)
_SLICE_GAP_DEG = 1.4  # surface-coloured separator between slices, ~2px at this radius


def _recap(model: dict, git: dict) -> str:
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

    stops, angle, legend = [], 0.0, ""
    for i, (label, count) in enumerate(slices):
        step = _DONUT_STEPS[i % len(_DONUT_STEPS)]
        span = 360 * count / m["total"]
        stops.append(f"{step} {angle:.2f}deg {angle + span - _SLICE_GAP_DEG:.2f}deg")
        stops.append(f"var(--surface) {angle + span - _SLICE_GAP_DEG:.2f}deg {angle + span:.2f}deg")
        angle += span
        # The legend carries every value, so close slices are read as numbers, not arcs.
        legend += (f'<div class="dl-row"><span class="dl-sw" style="background:{step}"></span>'
                   f'<span class="dl-k">{_esc(label)}</span><span class="dl-v">{count}</span>'
                   f'<span class="dl-p">{round(100 * count / m["total"])}%</span></div>')

    # Signs alone distinguish added from removed: colouring them good/bad would
    # assert a judgement the numbers do not carry (deleted code is often a win).
    lines = git.get("lines")
    lines_html = (f'<span class="rc-pair">+{_compact(lines[0])} &#8722;{_compact(lines[1])}</span>'
                  if lines else "")
    cards = [("Days", m["days"]), ("Active days", git.get("active_days", "")),
             ("Commits", git.get("commits", "")), ("Lines", lines_html)]
    card_html = "".join(f'<div class="recap-card"><div class="rc-k">{key}</div>'
                        f'<div class="rc-v">{value}</div></div>'
                        for key, value in cards if value != "" and value is not None)

    return (f'<div class="recap"><div class="recap-label">Release at a glance</div>'
            f'<div class="recap-body">'
            f'<div class="recap-figure">'
            f'<div class="donut" style="background: conic-gradient({", ".join(stops)})">'
            f'<div class="donut-hole"><span class="donut-total">{m["total"]}</span>'
            f'<span class="donut-cap">entries</span></div></div>'
            f'<div class="donut-legend">{legend}</div></div>'
            f'<div class="recap-cards">{card_html}</div>'
            f'</div></div>')


def _bucket_section(label: str, entries: list[dict]) -> str:
    """One card per entry, stacked — used by Fixes and by Platform and engineering."""
    if not entries:
        return ""
    cards = "".join('<div class="bucket"><ul class="entry-list">' + _entry_html(e) + "</ul></div>"
                    for e in entries)
    return (f'<section class="section"><div class="section-label">{_esc(label)}</div>'
            f'<div class="bucket-grid">{cards}</div></section>')


def render_content(model: dict, release_url: str, note_label: str, today: str, git: dict) -> str:
    out = []
    out.append(f'<div class="report-kicker">Release note · {_esc(model["version"])}</div>')
    out.append(f'<h1 class="report-title">{_esc(model["theme"])}</h1>')
    if model["framing"]:
        out.append(f'<p class="report-framing">{_inline(model["framing"])}</p>')
    out.append(_cartouche(model, release_url, note_label, today))
    out.append(_recap(model, git))

    if model["products"]:
        out.append('<section class="section"><div class="section-label">What&#x2019;s new</div>')
        for product in model["products"]:
            out.append('<div class="product-card">')
            if product["name"]:
                chip = f'<span class="product-id">{_esc(product["id"])}</span>' if product["id"] else ""
                out.append(f'<h2 class="product-name">{chip}{_esc(product["name"])}</h2>')
            out.append('<ul class="entry-list">' +
                       "".join(_entry_html(e) for e in product["entries"]) + "</ul></div>")
        out.append("</section>")

    out.append(_bucket_section("Fixes and improvements", model["fixes"]))
    out.append(_bucket_section("Platform and engineering", model["platform"]))

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

    tokens.css only ever carries font *names* (--font-sans, --font-mono); nothing
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


def build_html(note_path: Path, design_system: str | None, release_url: str | None) -> str:
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
    for key, value in {"TITLE": _esc(title),
                       "DESIGN_SYSTEM_CSS": fonts_css + "\n\n" + design_css if fonts_css else design_css,
                       "CONTENT": render_content(model, url, note_label, today,
                                                 _git_stats(note_path, model["changelog"]))}.items():
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
    args = parser.parse_args(argv)

    if not args.note.is_file():
        _fail(f"note not found: {args.note}")
    pdf_path = args.output or args.note.parent / "pdf" / f"{args.note.stem}.pdf"
    html_path = pdf_path.with_suffix(".html")
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    html_path.write_text(build_html(args.note, args.design_system, args.release_url), encoding="utf-8")
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

#!/usr/bin/env python3
"""
Slide Builder - Build (Stitch)
==============================
Reads individual slide partials and a shared CSS/JS layer,
then stitches them into a single self-contained HTML file
that can be opened in any browser with zero dependencies.

All paths in config.yaml are resolved relative to the config
file itself, so the skill scripts can live anywhere.

Usage:
    python build.py --config /path/to/project/config.yaml
    python build.py --config ./config.yaml
    python build.py --config ./config.yaml --output ./dist/deck.html
"""

import argparse
import html
import re
import sys
import textwrap
import urllib.parse
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML is required. Install it with: pip install pyyaml")
    sys.exit(1)

# Shipped neutral fallback (generic token contract) — inlined before everything
# so a deck renders correctly with no project design system. Mirrors
# com-artefact-viz/templates/tokens.fallback.css (same name, same role).
FALLBACK_TOKENS = Path(__file__).resolve().parent.parent / "templates" / "tokens.fallback.css"


def load_config(config_path: Path) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def resolve_path(base: Path, relative: str) -> Path:
    return (base / relative).resolve()


def read_file(path: Path) -> str:
    if not path.exists():
        print(f"  [WARN] File not found: {path}")
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def find_design_tokens(cfg: dict, base: Path) -> tuple:
    """Locate the shared design-system token sheet (docs/ux/tokens.css).

    The deck's base colour/type tokens are defined once, project-wide, by the
    `ux-design-system` skill. Resolution order:
      1. `paths.design_tokens` in config (relative to the config file), if set.
      2. Auto-detect: walk up from the deck dir to a `docs/ux/tokens.css`.
    Returns (css_text, source_path), or ("", None) when absent — the deck then
    builds with its own styles only (fully backwards compatible).
    """
    configured = cfg.get("paths", {}).get("design_tokens")
    if configured:
        p = resolve_path(base, configured)
        if p.exists():
            return p.read_text(encoding="utf-8"), p
        print(f"  [WARN] Configured design_tokens not found: {p}")
        return "", None
    cur = base.resolve()
    legacy = None
    for _ in range(8):  # walk up a bounded number of parents
        candidate = cur / "docs" / "ux" / "tokens.css"
        if candidate.exists():
            return candidate.read_text(encoding="utf-8"), candidate
        if legacy is None and (cur / "docs" / "design" / "tokens.css").exists():
            legacy = cur / "docs" / "design" / "tokens.css"
        if cur.parent == cur:
            break
        cur = cur.parent
    if legacy:  # OI-0026: design tokens moved docs/design/ -> docs/ux/ — rename the folder to re-enable shared theming
        print(f"  [HINT] Legacy {legacy} found but no docs/ux/tokens.css — design tokens moved to docs/ux/; rename the folder.")
    return "", None


def build_font_url(fonts: list) -> str:
    if not fonts:
        return ""
    families = []
    for font in fonts:
        family = font["family"].replace(" ", "+")
        weights = ";".join(str(w) for w in font.get("weights", [400]))
        families.append(f"family={family}:wght@{weights}")
    return f"https://fonts.googleapis.com/css2?{'&'.join(families)}&display=swap"


def load_bibliography(config: dict, base: Path) -> dict:
    """Load context/bibliography.yaml if configured. Returns {key: source_dict}.

    Returns an empty dict silently if the file is absent or the path is not
    configured — so existing projects without a bibliography are unaffected.
    """
    bib_rel = config.get("paths", {}).get("bibliography_file", "")
    if not bib_rel:
        return {}
    bib_path = resolve_path(base, bib_rel)
    if not bib_path.exists():
        return {}
    with open(bib_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("sources", {}) or {}


def format_source_bar(keys: list, bibliography: dict) -> str:
    """Resolve source keys and return a formatted .slide-source-bar div.

    Format per source: "Org · Title (year) — domain"
    Multiple sources joined by " &nbsp;|&nbsp; ".
    Unknown keys emit a build warning and are skipped without failing the build.
    """
    parts = []
    for key in keys:
        key = key.strip()
        if not key:
            continue
        if key not in bibliography:
            print(f"  [WARN] bibliography key not found: '{key}'")
            continue
        s = bibliography[key]
        # Build label: prefer org as primary identifier
        label = s.get("org", "") or s.get("title", key)
        title = s.get("title", "")
        if title and title != label:
            label = f"{label} · {title}"
        year = s.get("year")
        if year:
            label += f" ({year})"
        url = s.get("url", "")
        if url:
            domain = urllib.parse.urlparse(url).netloc.lstrip("www.")
            label += f" — {domain}"
        parts.append(label)
    if not parts:
        return ""
    return (
        '<div class="slide-source-bar">'
        + " &nbsp;|&nbsp; ".join(parts)
        + "</div>"
    )


def inject_before_slide_end(slide_html: str, injection: str) -> str:
    """Insert injection content just before the root .slide div's closing tag.

    Relies on the invariant that every slide partial ends with </div> (the root
    .slide closing tag) as the last non-whitespace content. The slide-number div
    closes before it, so rstrip() + endswith("</div>") reliably targets the root.
    """
    stripped = slide_html.rstrip()
    if stripped.endswith("</div>"):
        return stripped[: -len("</div>")] + injection + "\n</div>\n"
    return slide_html  # fallback: return unchanged if invariant not met


def make_baseline_css(canvas_w: int, canvas_h: int) -> str:
    return f"""\
/* ── Baseline: controls hint ── */
.controls-hint {{
  text-align: center;
  padding: 10px 0 6px;
  font-family: system-ui, sans-serif;
  font-size: 12px;
  color: #888;
  user-select: none;
}}
.controls-hint kbd {{
  display: inline-block;
  padding: 1px 6px;
  border: 1px solid #ccc;
  border-radius: 3px;
  font-size: 11px;
  background: #f5f5f5;
  color: #444;
}}
/* ── Baseline: presentation mode ── */
body.presenting {{
  background: #111;
  overflow: hidden;
}}
body.presenting .controls-hint {{ display: none; }}
body.presenting .slide:not(.active) {{ display: none; }}
body.presenting .slide.active {{
  position: fixed;
  top: 50%;
  left: 50%;
}}
/* ── Baseline: source bar ── */
.slide-source-bar {{
  position: absolute;
  bottom: 28px;
  left: 72px;
  right: 52px;
  font-family: var(--font-mono, 'SF Mono', monospace);
  font-size: 10px;
  color: var(--dim, #8C8C8C);
  line-height: 1.4;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  pointer-events: none;
}}
/* ── Baseline: mobile responsive scaling ── */
@media (max-width: 980px) {{
  body:not(.presenting) {{
    padding: 1rem 0;
    gap: 1rem;
  }}
  body:not(.presenting) .slide {{
    transform: scale(var(--slide-scale, 1));
    transform-origin: top center;
    margin-bottom: calc({canvas_h}px * (var(--slide-scale, 1) - 1));
  }}
}}
"""


def make_baseline_js(canvas_w: int) -> str:
    return f"""\
// ── Baseline: mobile responsive scaling ──
(function() {{
  function setMobileScale() {{
    if (window.innerWidth < 980) {{
      var scale = (window.innerWidth - 16) / {canvas_w};
      document.documentElement.style.setProperty('--slide-scale', scale);
    }} else {{
      document.documentElement.style.removeProperty('--slide-scale');
    }}
  }}
  setMobileScale();
  window.addEventListener('resize', setMobileScale);
}})();
"""


def build_head(cfg: dict) -> str:
    font_url = build_font_url(cfg.get("fonts", []))
    font_tags = ""
    if font_url:
        font_tags = textwrap.dedent(f"""\
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="{font_url}" rel="stylesheet">
        """)
    scripts = "\n".join(
        f'<script src="{url}"></script>'
        for url in cfg.get("external_scripts", [])
    )
    # Optional custom <meta> tags (e.g. rights / author / licence provenance).
    # config.yaml: meta: [{name: author, content: "..."}, ...]
    meta_tags = "\n".join(
        f'<meta name="{html.escape(str(m["name"]), quote=True)}" '
        f'content="{html.escape(str(m["content"]), quote=True)}">'
        for m in cfg.get("meta", [])
        if isinstance(m, dict) and m.get("name") and m.get("content") is not None
    )
    if meta_tags:
        meta_tags += "\n"
    return textwrap.dedent(f"""\
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{cfg.get("title", "Presentation")}</title>
    {meta_tags}{font_tags}{scripts}
    """)


def update_slide_numbers(html: str, current: int, total: int, fmt: str) -> str:
    number_text = fmt.format(current=current, total=total)
    return re.sub(
        r'(<div\s+class="slide-number">)(.*?)(</div>)',
        rf"\g<1>{number_text}\g<3>",
        html,
        flags=re.DOTALL,
    )


def build(config_path: Path, output_override: str = None):
    cfg = load_config(config_path)
    base = config_path.parent

    # All paths resolve relative to the config file
    slides_dir = resolve_path(base, cfg["paths"]["slides_dir"])
    styles_path = resolve_path(base, cfg["paths"]["styles_file"])
    script_path = resolve_path(base, cfg["paths"]["script_file"])
    output_dir = resolve_path(base, cfg["paths"]["output_dir"])
    output_file = output_dir / cfg["paths"]["output_filename"]

    if output_override:
        output_file = Path(output_override).resolve()
        output_dir = output_file.parent

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"[BUILD] Config:  {config_path}")
    print(f"[BUILD] Slides:  {slides_dir}")
    print(f"[BUILD] Output:  {output_file}")

    # Bibliography (optional — empty dict if absent or not configured)
    bibliography = load_bibliography(cfg, base)
    if bibliography:
        print(f"[BUILD] Sources: {len(bibliography)} entries in bibliography")

    # Head
    parts = [build_head(cfg)]

    # Canvas dimensions (used by baseline CSS/JS)
    canvas = cfg.get("canvas", {})
    canvas_w = int(canvas.get("width",  960))
    canvas_h = int(canvas.get("height", 540))
    baseline_css = make_baseline_css(canvas_w, canvas_h)
    baseline_js  = make_baseline_js(canvas_w)

    # Styles — layered so values cascade in the right order (same model as
    # com-artefact-viz):
    #   1. tokens.fallback.css    — shipped neutral generic contract (zero-config)
    #   2. docs/ux/tokens.css — project override (the source of truth; wins)
    #   3. the deck's own styles.css — deck-only tokens + components
    #   4. baseline CSS           — structural defaults
    fallback_css = read_file(FALLBACK_TOKENS)
    tokens_css, tokens_src = find_design_tokens(cfg, base)
    if tokens_src:
        print(f"[BUILD] Tokens:  {tokens_src} (shared design system)")
    css = read_file(styles_path)
    layers = [c for c in (fallback_css, tokens_css, css, baseline_css) if c]
    parts.append("<style>\n" + "\n".join(layers) + "\n</style>")
    parts.append("</head>\n<body>\n")

    # Controls hint
    parts.append(textwrap.dedent("""\
    <div class="controls-hint">
      Press <kbd>F</kbd> for fullscreen presentation &middot; <kbd>&larr;</kbd> <kbd>&rarr;</kbd> to navigate &middot; <kbd>Esc</kbd> to exit
    </div>
    """))

    # Slides
    slide_entries = cfg.get("slides", [])
    total = len(slide_entries)
    numbering = cfg.get("numbering", {})
    num_enabled = numbering.get("enabled", True)
    num_format = numbering.get("format", "{current} / {total}")

    for idx, entry in enumerate(slide_entries, start=1):
        filename = entry["file"] if isinstance(entry, dict) else entry
        label = entry.get("label", "") if isinstance(entry, dict) else ""
        slide_path = slides_dir / filename

        print(f"  [{idx:02d}/{total}] {filename}", end="")
        html = read_file(slide_path)
        if not html:
            print(" (MISSING)")
            continue

        if num_enabled:
            html = update_slide_numbers(html, idx, total, num_format)

        # Inject source bar if the slide declares data-sources and bibliography exists
        if bibliography:
            sources_match = re.search(
                r'data-sources=["\']([^"\']+)["\']', html
            )
            if sources_match:
                keys = sources_match.group(1).split(",")
                source_bar = format_source_bar(keys, bibliography)
                if source_bar:
                    html = inject_before_slide_end(html, "\n" + source_bar)

        parts.append(f"\n<!-- slide {idx}: {label} -->\n")
        parts.append(html.strip())
        parts.append("\n")
        print(" OK")

    # Script (baseline responsive + project)
    js = read_file(script_path)
    parts.append(f"\n<script>\n{baseline_js}\n{js}\n</script>\n")

    parts.append("</body>\n</html>\n")

    # Write
    final = "\n".join(parts)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final)

    size_kb = output_file.stat().st_size / 1024
    print(f"\n[DONE] {output_file.name} ({size_kb:.1f} KB, {total} slides)")


def main():
    parser = argparse.ArgumentParser(
        description="Build a single-file HTML presentation from slide partials."
    )
    parser.add_argument(
        "--config", "-c",
        required=True,
        help="Path to the project's config.yaml",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Override output file path",
    )
    args = parser.parse_args()
    build(Path(args.config).resolve(), args.output)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Render a built slide deck to a PDF leave-behind via headless Chromium (Playwright).

One slide per PDF page, at the deck's canvas size, with backgrounds preserved and an
optional per-recipient footer stamp ("Prepared for <recipient> · <date>").

Optional dependency — NOT auto-installed. This script checks for Playwright (and its
Chromium build) and fails with an explicit message if either is missing; the developer
must provision Playwright in their local environment before PDF export will work.

Usage:
    python scripts/render.py --config path/to/config.yaml
    python scripts/render.py --config path/to/config.yaml --recipient "MedQuantis"
    python scripts/render.py --config path/to/config.yaml --recipient "MedQuantis" \
        --date 2026-05-30 --output /tmp/deck.pdf
"""
from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

import yaml  # PyYAML — already a com-slide-deck dependency


def fail(msg: str, code: int = 1) -> None:
    print(f"[render] ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def require_playwright():
    """Import Playwright's sync API or fail explicitly (never auto-install)."""
    try:
        from playwright.sync_api import sync_playwright  # noqa: WPS433 (local import by design)
    except ImportError:
        fail(
            "Playwright is not available in this environment. PDF export is an optional "
            "feature and this script does not install it.\n"
            "  Provision Playwright (and its Chromium build) in your local environment, "
            "then re-run this command."
        )
    return sync_playwright


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def load_config(config_path: Path) -> dict:
    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def resolve_paths(config_path: Path, cfg: dict, recipient: str | None, output_override: str | None):
    base = config_path.parent
    paths = cfg.get("paths", {})
    output_dir = (base / paths.get("output_dir", "output/slide-deck")).resolve()
    output_filename = paths.get("output_filename", "presentation.html")
    built_html = output_dir / output_filename
    if output_override:
        pdf_path = Path(output_override).resolve()
    else:
        stem = Path(output_filename).stem
        suffix = f"--{slugify(recipient)}" if recipient else ""
        pdf_path = (output_dir.parent / "pdf" / f"{stem}{suffix}.pdf").resolve()
    return built_html, pdf_path


def print_css(width: int, height: int) -> str:
    """Pagination CSS injected at render time — one slide per page, no gaps, white page."""
    return f"""
    html, body {{ margin: 0 !important; padding: 0 !important; background: #fff !important; }}
    .controls-hint {{ display: none !important; }}
    .slide {{
        break-after: page;
        page-break-after: always;
        margin: 0 !important;
        box-shadow: none !important;
        transform: none !important;
    }}
    .slide:last-child {{ break-after: auto; page-break-after: auto; }}
    @page {{ size: {width}px {height}px; margin: 0; }}
    """


# JS run in the page before printing: render icons, stamp recipient footer, then signal.
_PREP_JS = """
(footerText) => {
  if (window.lucide && typeof window.lucide.createIcons === 'function') {
    window.lucide.createIcons();
  }
  if (footerText) {
    document.querySelectorAll('.slide').forEach((s) => {
      const f = document.createElement('div');
      f.textContent = footerText;
      f.style.cssText =
        'position:absolute;bottom:9px;left:0;right:0;text-align:center;' +
        'font-family:ui-monospace,Menlo,monospace;font-size:9px;letter-spacing:.3px;' +
        'color:rgba(130,130,130,.95);z-index:50;pointer-events:none;';
      s.appendChild(f);
    });
  }
}
"""


def render(config_path: Path, recipient: str | None, date: str, output_override: str | None) -> Path:
    cfg = load_config(config_path)
    canvas = cfg.get("canvas", {})
    width = int(canvas.get("width", 1280))
    height = int(canvas.get("height", 720))

    built_html, pdf_path = resolve_paths(config_path, cfg, recipient, output_override)
    if not built_html.exists():
        fail(f"Built deck not found at {built_html}. Run build.py first.")
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    footer_text = f"Prepared for {recipient} · {date}" if recipient else ""

    sync_playwright = require_playwright()
    print(f"[render] Input:  {built_html}")
    print(f"[render] Output: {pdf_path}")
    if recipient:
        print(f"[render] Stamp:  {footer_text}")

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception as exc:  # noqa: BLE001 — surface a clean message
            fail(
                f"Could not launch Chromium ({exc}).\n"
                "  Ensure Playwright's Chromium build is available in your local environment, "
                "then re-run this command."
            )
        page = browser.new_page(viewport={"width": width, "height": height})
        # Render screen-styled output (the deck is designed for screen media), while the
        # injected @page + page-break CSS still drives pagination in the PDF.
        page.emulate_media(media="screen")
        page.goto(built_html.as_uri(), wait_until="networkidle")
        page.evaluate(_PREP_JS, footer_text)
        page.evaluate("() => document.fonts.ready")
        page.add_style_tag(content=print_css(width, height))
        page.pdf(
            path=str(pdf_path),
            width=f"{width}px",
            height=f"{height}px",
            print_background=True,
            prefer_css_page_size=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        browser.close()

    size_kb = pdf_path.stat().st_size / 1024
    print(f"[render] DONE: {pdf_path.name} ({size_kb:.1f} KB)")
    return pdf_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render a built slide deck to a PDF leave-behind (headless Chromium via Playwright)."
    )
    parser.add_argument("--config", required=True, help="Path to the project's config.yaml")
    parser.add_argument("--recipient", default=None, help="Per-recipient footer stamp (e.g. a partner name)")
    parser.add_argument("--date", default=datetime.date.today().isoformat(), help="Date for the stamp (ISO, default today)")
    parser.add_argument("--output", default=None, help="Output PDF path (default: <deck>/output/pdf/<name>[--recipient].pdf)")
    args = parser.parse_args()

    config_path = Path(args.config).resolve()
    if not config_path.exists():
        fail(f"Config not found: {config_path}")
    render(config_path, args.recipient, args.date, args.output)


if __name__ == "__main__":
    main()

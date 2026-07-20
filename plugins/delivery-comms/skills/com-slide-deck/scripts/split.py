#!/usr/bin/env python3
"""
Slide Builder - Split
=====================
Takes an existing single-file HTML presentation and splits it into:
  - Individual slide partial files (one per slide)
  - A shared styles.css (extracted from <style>)
  - A shared script.js (extracted from <script>)

All output paths resolve relative to the config file.

Usage:
    python split.py <source.html> --config /path/to/project/config.yaml
    python split.py deck.html --config ./config.yaml --slides-dir ./output/slides
"""

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


def extract_styles(html: str) -> str:
    blocks = re.findall(r"<style[^>]*>(.*?)</style>", html, re.DOTALL)
    return "\n\n".join(block.strip() for block in blocks)


def extract_scripts(html: str) -> str:
    blocks = re.findall(r"<script(?:\s[^>]*)?>(?!.*?src=)(.*?)</script>", html, re.DOTALL)
    inline = [b.strip() for b in blocks if b.strip()]
    return "\n\n".join(inline)


def extract_slides(html: str) -> list:
    slides = []
    pattern = re.compile(r'<div\s+class="slide\s+([^"]*)"[^>]*>')
    pos = 0

    while pos < len(html):
        match = pattern.search(html, pos)
        if not match:
            break

        css_classes = match.group(1).strip()
        start = match.start()
        tag_open = re.compile(r"<div[\s>]")
        tag_close = re.compile(r"</div>")

        depth = 1
        i = match.end()
        while i < len(html) and depth > 0:
            next_open = tag_open.search(html, i)
            next_close = tag_close.search(html, i)

            if next_close is None:
                break

            if next_open and next_open.start() < next_close.start():
                depth += 1
                i = next_open.end()
            else:
                depth -= 1
                if depth == 0:
                    end = next_close.end()
                    slide_html = html[start:end]
                    slides.append((css_classes, slide_html))
                    pos = end
                    break
                i = next_close.end()
        else:
            pos = match.end()
            continue

    return slides


def class_to_filename(css_classes: str, index: int) -> str:
    parts = css_classes.split()
    slug = parts[0] if parts else f"slide-{index}"
    slug = re.sub(r"[^a-zA-Z0-9-]", "-", slug)
    return f"{index:02d}-{slug}.html"


def split(
    source_path: Path,
    slides_dir: Path = None,
    styles_out: Path = None,
    script_out: Path = None,
    config_path: Path = None,
):
    print(f"[SPLIT] Source: {source_path}")

    html = source_path.read_text(encoding="utf-8")

    # Determine output directories from config
    if config_path and yaml:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        base = config_path.parent
        slides_dir = slides_dir or (base / cfg["paths"]["slides_dir"]).resolve()
        styles_out = styles_out or (base / cfg["paths"]["styles_file"]).resolve()
        script_out = script_out or (base / cfg["paths"]["script_file"]).resolve()
    else:
        default_base = source_path.parent
        slides_dir = slides_dir or default_base / "slides"
        styles_out = styles_out or default_base / "styles.css"
        script_out = script_out or default_base / "script.js"

    slides_dir.mkdir(parents=True, exist_ok=True)
    styles_out.parent.mkdir(parents=True, exist_ok=True)
    script_out.parent.mkdir(parents=True, exist_ok=True)

    # Extract CSS
    css = extract_styles(html)
    if css:
        styles_out.write_text(css, encoding="utf-8")
        print(f"  [CSS]    {styles_out} ({len(css)} chars)")

    # Extract JS
    js = extract_scripts(html)
    if js:
        script_out.write_text(js, encoding="utf-8")
        print(f"  [JS]     {script_out} ({len(js)} chars)")

    # Extract slides
    slides = extract_slides(html)
    print(f"  [SLIDES] Found {len(slides)} slides")

    filenames = []
    for idx, (classes, slide_html) in enumerate(slides):
        filename = class_to_filename(classes, idx)
        filepath = slides_dir / filename
        filepath.write_text(slide_html.strip() + "\n", encoding="utf-8")
        filenames.append(filename)
        print(f"    [{idx:02d}] {filename} ({classes})")

    if not config_path:
        print("\n  [INFO] Suggested slides list for config.yaml:")
        for fn in filenames:
            print(f'    - file: "{fn}"')

    print(f"\n[DONE] Split {len(slides)} slides into {slides_dir}")
    return filenames


def main():
    parser = argparse.ArgumentParser(
        description="Split a single-file HTML presentation into partials."
    )
    parser.add_argument("source", help="Path to the single-file HTML presentation")
    parser.add_argument(
        "--config", "-c",
        default=None,
        help="Path to the project's config.yaml (paths resolve from it)",
    )
    parser.add_argument(
        "--slides-dir",
        default=None,
        help="Override output directory for slide partials",
    )
    args = parser.parse_args()

    source = Path(args.source).resolve()
    if not source.exists():
        print(f"Error: Source file not found: {source}")
        sys.exit(1)

    config = Path(args.config).resolve() if args.config else None
    slides_dir = Path(args.slides_dir).resolve() if args.slides_dir else None

    split(source, slides_dir=slides_dir, config_path=config)


if __name__ == "__main__":
    main()

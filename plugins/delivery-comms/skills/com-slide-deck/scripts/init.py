#!/usr/bin/env python3
"""
Slide Builder - Init
====================
Scaffolds a new slide deck project at a target directory.

Creates the folder structure, copies templates from the skill,
and writes a config.yaml ready to edit.

Usage:
    python init.py ./my-presentation
    python init.py ./my-presentation --name "My Talk"
    python init.py ./my-presentation --name "My Talk" --author "Jane Doe"
"""

import argparse
import shutil
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = SKILL_DIR / "templates"


def init_project(target: Path, name: str = "", author: str = ""):
    if target.exists() and any(target.iterdir()):
        print(f"[WARN] Target directory is not empty: {target}")
        print("       Existing files will NOT be overwritten.\n")

    # Create folder structure
    dirs = [
        "context",
        "design",
        "output/slide-deck",
        "output/slides",
        "output/prototypes",
    ]
    for d in dirs:
        (target / d).mkdir(parents=True, exist_ok=True)

    # Copy templates (never overwrite existing files)
    copies = [
        ("brief-template.md",          "context/brief-template.md"),
        ("brief-template.md",          "context/brief.md"),
        ("design-system-template.md",  "design/design-system-template.md"),
        ("design-system-template.md",  "design/design-system.md"),
        ("bibliography-template.yaml", "context/bibliography-template.yaml"),
        ("bibliography-template.yaml", "context/bibliography.yaml"),
        ("config-template.yaml",       "config.yaml"),
    ]

    for src_name, dest_rel in copies:
        src = TEMPLATES_DIR / src_name
        dest = target / dest_rel
        if dest.exists():
            print(f"  [SKIP] {dest_rel} (already exists)")
            continue
        if not src.exists():
            print(f"  [WARN] Template not found: {src}")
            continue
        shutil.copy2(src, dest)
        print(f"  [NEW]  {dest_rel}")

    # Create placeholder / default files (never overwrite existing)
    DEFAULT_SCRIPT = """\
// ── Initialize Lucide icons (no-op if library not loaded) ───
if (typeof lucide !== 'undefined') lucide.createIcons();

// ── Fullscreen presentation mode ────────────────────────────
// Keyboard controls:
//   F          → enter fullscreen presentation
//   Esc        → exit
//   → / ↓ / Space  → next slide
//   ← / ↑          → previous slide
(function () {
  var slides = Array.from(document.querySelectorAll('.slide'));
  if (!slides.length) return;

  var current   = 0;
  var presenting = false;

  // Read canvas dimensions from the first slide element so this
  // script works regardless of the canvas size set in config.yaml.
  var W = slides[0].offsetWidth;
  var H = slides[0].offsetHeight;

  function scaleSlides() {
    var margin = 40;
    var scale  = Math.min(
      (window.innerWidth  - margin * 2) / W,
      (window.innerHeight - margin * 2) / H
    );
    slides.forEach(function (s) {
      s.style.transform = presenting
        ? 'translate(-50%, -50%) scale(' + scale + ')'
        : '';
    });
  }

  function showSlide(n) {
    current = Math.max(0, Math.min(n, slides.length - 1));
    slides.forEach(function (s, i) {
      s.classList.toggle('active', i === current);
    });
  }

  function enter() {
    presenting = true;
    document.body.classList.add('presenting');
    showSlide(current);
    if (document.documentElement.requestFullscreen) {
      document.documentElement.requestFullscreen();
    }
    setTimeout(scaleSlides, 100);
  }

  function exit() {
    presenting = false;
    document.body.classList.remove('presenting');
    slides.forEach(function (s) {
      s.classList.remove('active');
      s.style.transform = '';
    });
    if (document.fullscreenElement && document.exitFullscreen) {
      document.exitFullscreen();
    }
  }

  window.addEventListener('resize', function () {
    if (presenting) scaleSlides();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'f' || e.key === 'F') {
      if (!presenting) enter();
    } else if (e.key === 'Escape') {
      if (presenting) exit();
    } else if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') {
      if (presenting) { e.preventDefault(); showSlide(current + 1); }
    } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
      if (presenting) showSlide(current - 1);
    }
  });

  // Catch browser-native Esc (exits fullscreen before keydown fires)
  document.addEventListener('fullscreenchange', function () {
    if (!document.fullscreenElement && presenting) exit();
  });
})();
"""

    DEFAULT_STYLES = """/*
 * Deck styles. Base palette + typography + semantic state come from the design
 * system, inlined by build.py BEFORE this file: tokens.fallback.css (shipped
 * defaults) then docs/ux/tokens.css (project override, if present). Use the
 * contract token names via var() — do NOT redefine the base palette here. See
 * design/design-system.md for the full token list and the migration map.
 */

:root {
  /* Deck-only tokens (no contract equivalent). Base palette, typography, and
     semantic state (--success/--warning/--danger/--info) come from tokens.css. */
  --dim:       var(--muted);           /* tertiary text; override with a dimmer value if desired */
  --accent-lt: color-mix(in srgb, var(--accent) 14%, var(--surface));  /* subtle accent background */
}

/* Component styles go here — reference var(--ink), var(--surface), var(--accent),
   var(--font-sans), var(--font-mono), etc. Never hard-code a hex value. */
"""

    placeholders = [
        ("design/styles.css", DEFAULT_STYLES),
        ("design/script.js",  DEFAULT_SCRIPT),
    ]
    for rel, content in placeholders:
        path = target / rel
        if path.exists():
            print(f"  [SKIP] {rel} (already exists)")
        else:
            path.write_text(content, encoding="utf-8")
            print(f"  [NEW]  {rel}")

    # Patch config.yaml with name/author if provided
    config_path = target / "config.yaml"
    if config_path.exists() and (name or author):
        text = config_path.read_text(encoding="utf-8")
        if name:
            text = text.replace('title: "Presentation Title"', f'title: "{name}"')
        if author:
            text = text.replace('author: "Author"', f'author: "{author}"')
        config_path.write_text(text, encoding="utf-8")

    # Print summary
    skill_rel = SKILL_DIR
    print(f"\n[DONE] Project scaffolded at: {target}")
    print(f"\nNext steps:")
    print(f"  1. Fill in  {target / 'context/brief.md'}")
    print(f"  2. Fill in  {target / 'design/design-system.md'}")
    print(f"  3. Create slides in  {target / 'output/slides/'}")
    print(f"  4. Build with:")
    print(f"       python {skill_rel / 'scripts/build.py'} --config {target / 'config.yaml'}")


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a new slide deck project."
    )
    parser.add_argument(
        "target",
        help="Target directory for the new project",
    )
    parser.add_argument(
        "--name", "-n",
        default="",
        help="Presentation title (written into config.yaml)",
    )
    parser.add_argument(
        "--author", "-a",
        default="",
        help="Author name (written into config.yaml)",
    )
    args = parser.parse_args()

    target = Path(args.target).resolve()
    init_project(target, name=args.name, author=args.author)


if __name__ == "__main__":
    main()

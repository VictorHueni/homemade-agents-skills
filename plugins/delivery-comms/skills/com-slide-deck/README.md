# Slide Builder

A portable toolkit for building single-file HTML presentations from modular
slide partials, driven by a presentation brief and a design system, stitched
via Python.

This is the **skill** (reusable toolkit). It does not contain any
project-specific content. Version this in Git and import it into any
agent or project when needed.

---

## Install as a Claude Skill

Copy or clone this folder into your skills directory:

```bash
# Personal skill (all projects)
cp -r com-slide-deck ~/.claude/skills/slide-builder

# Project skill (this repo only)
cp -r com-slide-deck .claude/skills/slide-builder
```

The agent will pick it up automatically via the `SKILL.md` frontmatter.

---

## Folder Structure

```
com-slide-deck/
  SKILL.md                       Agent instructions (with frontmatter)
  README.md                      This file
  templates/
    brief-template.md            Blank presentation brief
    design-system-template.md    Blank design system definition
    config-template.yaml         Blank build configuration
  scripts/
    init.py                      Scaffolds a new project directory
    build.py                     Stitches slide partials into one HTML
    split.py                     Splits a single-file deck into partials
    migrate.py                   Migrate an old deck onto the shared design-system tokens
    dev_server.py                Auto-rebuild + local HTTP server
```

---

## Requirements

- Python 3.8+
- PyYAML (`pip install pyyaml`)

---

## Quick Start

### 1. Scaffold a new project

```bash
python scripts/init.py ./my-presentation --name "My Talk" --author "Jane Doe"
```

This creates:

```
my-presentation/
  context/
    brief-template.md       Reference copy
    brief.md                Fill this in
  design/
    design-system-template.md  Reference copy
    design-system.md        Fill this in
    styles.css              Implement your design tokens here
    script.js               Presentation mode JS here
  output/
    slide-deck/             Build output lands here
    slides/                 One HTML file per slide
    prototypes/             Experimental variations
  config.yaml               Slide order, paths, metadata
```

### 2. Fill in the prerequisites

1. Complete `context/brief.md` (summary, goal, audience, tone, key messages)
2. Complete `design/design-system.md` (colors, fonts, components, rules)
3. Write `design/styles.css` implementing the design system
4. Write `design/script.js` for presentation mode

### 3. Create slides and build

```bash
# Create slide partials in output/slides/
# Add them to config.yaml
# Then build:
python path/to/com-slide-deck/scripts/build.py --config ./my-presentation/config.yaml
```

Output: `my-presentation/output/slide-deck/presentation.html`

### 4. Share

Send the generated HTML file. It's self-contained, works offline in any
browser, zero dependencies.

---

## Migrating an Existing Deck

If you already have a single-file HTML presentation:

```bash
# Scaffold a project first
python scripts/init.py ./my-deck

# Split the existing file into the project
python scripts/split.py existing-deck.html --config ./my-deck/config.yaml
```

Then rename the generated slide files, update `config.yaml`, and build.

---

## Dev Server

Auto-rebuild on file changes with a local HTTP server:

```bash
python scripts/dev_server.py --config ./my-presentation/config.yaml --port 3000
```

Or use VS Code Live Server pointed at `output/slide-deck/`.

---

## LLM Agent Usage

Point any Claude agent at `SKILL.md`. The agent will:

1. Scaffold a project if none exists
2. Check that the brief is completed (or walk you through filling it in)
3. Check that the design system is completed (or walk you through it)
4. Read both documents and the config before touching any slides
5. Follow the brief for content, the design system for visuals
6. Build and verify after every change

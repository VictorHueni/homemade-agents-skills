#!/usr/bin/env python3
"""
render.py — com-artefact-viz CLI.

Render a canonical kit artefact (capability map, FBS, delivery roadmap, BMC) to
a single self-contained interactive HTML file — or compose a service blueprint
from several source artefacts (multi-source; see --proc below).

    python render.py SOURCE.md [options]
    python render.py --kind service-blueprint --proc PROC.md [--value-stream VS.md] [--personas PATH]

Options:
    --out PATH              Output HTML path. Default:
                            docs/communication/visualisations/<kind>.html
    --kind KIND             Force the artefact kind (capability-map | fbs |
                            delivery-roadmap | bmc | service-blueprint).
                            Auto-detected from path/content when omitted.
    --proc FILE             A business-process doc to compose into a service
                            blueprint (repeatable). Implies --kind service-blueprint.
    --value-stream FILE     Value-stream doc supplying the blueprint's phase
                            columns (optional; falls back to §6 step order).
    --personas PATH         Persona doc or directory used to derive the line of
                            visibility (front/back-stage). Repeatable.
    --stream VS-N           Limit blueprint phase columns to one value stream.
    --design-system PATH    Project design-system CSS to inline AFTER the
                            defaults (its :root tokens win — this is how a
                            project re-themes every view). Reuse the same
                            design/styles.css your com-slide-deck project uses.
    --left-axis-label TEXT  Override the capability-map / FBS left-axis label
                            (the directional "arrow" band). Defaults to the
                            artefact's declared L0 axis.
    --left-axis-arrow CHAR  Arrow glyph for that band (default "▼").
    --title TEXT            Override the page title.
    --detect                Print the detected kind and exit (no render).

Standard library only. Run from the repo root or anywhere — paths are resolved
relative to the current directory.
"""

import argparse
import datetime
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import parsers  # noqa: E402
import renderers  # noqa: E402

SKILL_DIR = os.path.dirname(HERE)
TEMPLATE_DIR = os.path.join(SKILL_DIR, "templates")


def _read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def fill_template(slots):
    tmpl = _read(os.path.join(TEMPLATE_DIR, "base.html.tmpl"))
    for key, value in slots.items():
        tmpl = tmpl.replace("{{" + key + "}}", value)
    return tmpl


def _read_personas(paths):
    """A persona arg may be a file or a directory of persona docs; read all."""
    texts = []
    for path in paths or []:
        if os.path.isdir(path):
            for name in sorted(os.listdir(path)):
                if name.lower().endswith(".md"):
                    texts.append(_read(os.path.join(path, name)))
        elif os.path.isfile(path):
            texts.append(_read(path))
        else:
            sys.exit(f"error: --personas path not found: {path}")
    return texts


def build(source_path, args):
    options = {
        "left_axis_label": args.left_axis_label,
        "left_axis_arrow": args.left_axis_arrow,
        "stream": args.stream,
        "title": args.title,
    }

    # ---- Multi-source composition lens (service blueprint) -----------------
    if args.proc or args.kind == "service-blueprint":
        kind = "service-blueprint"
        if not args.proc:
            sys.exit("error: --kind service-blueprint needs at least one --proc FILE.")
        for p in args.proc:
            if not os.path.isfile(p):
                sys.exit(f"error: --proc file not found: {p}")
        if args.value_stream and not os.path.isfile(args.value_stream):
            sys.exit(f"error: --value-stream file not found: {args.value_stream}")
        if args.detect:
            print(kind)
            return None
        proc_texts = [_read(p) for p in args.proc]
        vs_text = _read(args.value_stream) if args.value_stream else None
        persona_texts = _read_personas(args.personas)
        model = parsers.parse_service_blueprint(proc_texts, vs_text, persona_texts, options)
        rendered = renderers.RENDERERS[kind](model, options)
        return _emit(model, rendered, kind, args, source_label=", ".join(args.proc))

    # ---- Single-source path (capability-map | fbs | delivery-roadmap | bmc) -
    if not source_path:
        sys.exit("error: provide a SOURCE.md (or use --proc for a service blueprint).")
    text = _read(source_path)
    kind = args.kind or parsers.detect_kind(source_path, text)
    if not kind:
        sys.exit(
            f"error: could not detect artefact kind for {source_path!r}. "
            f"Pass --kind capability-map|fbs|delivery-roadmap|bmc."
        )
    if kind not in parsers.PARSERS:
        sys.exit(f"error: unknown kind {kind!r}.")

    if args.detect:
        print(kind)
        return None

    model = parsers.PARSERS[kind](text)
    rendered = renderers.RENDERERS[kind](model, options)
    return _emit(model, rendered, kind, args, source_label=source_path)


def _emit(model, rendered, kind, args, source_label):

    # Design system: defaults first, then the project sheet (project tokens win).
    # Resolution order for the project sheet:
    # Token layering (same model as com-slide-deck):
    #   1. tokens.fallback.css   — shipped neutral generic contract (zero-config)
    #   2. docs/ux/tokens.css — project override (explicit --design-system, or
    #                                auto-detected; project values win)
    #   3. tokens.domain.css     — viz domain tokens derived from the generics
    ds = _read(os.path.join(TEMPLATE_DIR, "tokens.fallback.css"))
    project_sheet = args.design_system
    if not project_sheet:
        shared = os.path.join("docs", "ux", "tokens.css")
        if os.path.isfile(shared):
            project_sheet = shared
            print(f"using shared design system {shared} (pass --design-system to override)")
        elif os.path.isfile(os.path.join("docs", "design", "tokens.css")):  # OI-0026: tokens moved docs/design/ -> docs/ux/
            print("[HINT] Legacy docs/design/tokens.css found but no docs/ux/tokens.css — design tokens moved to docs/ux/; rename the folder.")
    if project_sheet:
        ds += "\n\n/* ---- project design system (overrides) ---- */\n" + _read(project_sheet)
    ds += "\n\n/* ---- viz domain tokens (derived) ---- */\n" + _read(os.path.join(TEMPLATE_DIR, "tokens.domain.css"))

    runtime = _read(os.path.join(TEMPLATE_DIR, "runtime.js"))
    title = args.title or model["title"]
    today = datetime.date.today().isoformat()
    footer = (
        f'Generated by com-artefact-viz from '
        f'<code>{_esc(parsers_relpath(source_label))}</code> on {today}. '
        f'Source artefact is the single source of truth — re-render after edits.'
    )

    html = fill_template({
        "TITLE": _esc(title),
        "KIND": _esc(rendered["kind_label"]),
        "META": rendered["meta"],
        "TOOLBAR": rendered["toolbar"],
        "CONTENT": rendered["content"],
        "DESIGN_SYSTEM_CSS": ds,
        "VIEW_CSS": rendered["view_css"],
        "RUNTIME_JS": runtime,
        "FOOTER": footer,
    })

    out = args.out or default_out(kind)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    return out


def parsers_relpath(path):
    try:
        return os.path.relpath(path)
    except ValueError:
        return path


def _esc(s):
    import html
    return html.escape(s or "", quote=True)


def default_out(kind):
    return os.path.join("docs", "communication", "visualisations", f"{kind}.html")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Render a kit artefact to interactive HTML.")
    ap.add_argument("source", nargs="?",
                    help="Source Markdown artefact (single-source kinds). Omit for --proc.")
    ap.add_argument("--out")
    ap.add_argument("--kind", choices=sorted(parsers.PARSERS) + list(parsers.MULTISOURCE_KINDS))
    ap.add_argument("--design-system", dest="design_system")
    ap.add_argument("--left-axis-label", dest="left_axis_label")
    ap.add_argument("--left-axis-arrow", dest="left_axis_arrow", default="▼")
    ap.add_argument("--title")
    ap.add_argument("--detect", action="store_true")
    # service-blueprint composition lens (multi-source)
    ap.add_argument("--proc", action="append", metavar="FILE",
                    help="A business-process doc to compose (repeatable).")
    ap.add_argument("--value-stream", dest="value_stream", metavar="FILE",
                    help="Value-stream doc supplying the phase columns (optional).")
    ap.add_argument("--personas", action="append", metavar="PATH",
                    help="Persona doc or directory; classifies front/back-stage (repeatable).")
    ap.add_argument("--stream", metavar="VS-N",
                    help="Limit phase columns to one value stream (e.g. VS-1).")
    args = ap.parse_args(argv)

    if args.source and not os.path.isfile(args.source):
        sys.exit(f"error: source not found: {args.source}")

    out = build(args.source, args)
    if out:
        print(f"wrote {out}")


if __name__ == "__main__":
    main()

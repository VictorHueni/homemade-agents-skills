#!/usr/bin/env python3
"""
dev_server.py — live preview for com-artefact-viz.

Watches a source artefact (and the skill's templates), re-renders on change, and
serves the result over localhost. Standard library only.

    python dev_server.py SOURCE.md [--port 8000] [render.py options...]

Any option render.py accepts (e.g. --kind, --design-system, --left-axis-label)
is forwarded, except --out which is fixed to a temp file the server serves.
"""

import argparse
import http.server
import os
import socketserver
import sys
import tempfile
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render as render_mod  # noqa: E402

TEMPLATE_DIR = os.path.join(os.path.dirname(HERE), "templates")


def watched_paths(args):
    paths = []
    if args.source:
        paths.append(args.source)
    # service-blueprint composition lens: watch every composed source
    paths += list(args.proc or [])
    if args.value_stream:
        paths.append(args.value_stream)
    for p in args.personas or []:
        if os.path.isdir(p):
            paths += [os.path.join(p, n) for n in os.listdir(p) if n.lower().endswith(".md")]
        else:
            paths.append(p)
    for name in ("base.html.tmpl", "tokens.fallback.css", "tokens.domain.css", "runtime.js"):
        paths.append(os.path.join(TEMPLATE_DIR, name))
    return paths


def mtimes(paths):
    out = {}
    for p in paths:
        try:
            out[p] = os.path.getmtime(p)
        except OSError:
            out[p] = 0
    return out


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("source", nargs="?")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--kind", choices=None)
    ap.add_argument("--design-system", dest="design_system")
    ap.add_argument("--left-axis-label", dest="left_axis_label")
    ap.add_argument("--left-axis-arrow", dest="left_axis_arrow", default="▼")
    ap.add_argument("--title")
    # service-blueprint composition lens (multi-source) — mirrors render.py
    ap.add_argument("--proc", action="append", metavar="FILE")
    ap.add_argument("--value-stream", dest="value_stream", metavar="FILE")
    ap.add_argument("--personas", action="append", metavar="PATH")
    ap.add_argument("--stream", metavar="VS-N")
    args = ap.parse_args()
    args.detect = False

    if args.source and not os.path.isfile(args.source):
        sys.exit(f"error: source not found: {args.source}")
    if not args.source and not args.proc:
        sys.exit("error: provide a SOURCE.md (or --proc for a service blueprint).")

    tmpdir = tempfile.mkdtemp(prefix="viz-")
    out_path = os.path.join(tmpdir, "index.html")
    args.out = out_path

    label = args.source or ", ".join(args.proc or [])

    def rebuild():
        try:
            render_mod.build(args.source, args)
            print(f"[{time.strftime('%H:%M:%S')}] rendered {label}")
        except SystemExit as e:
            print(f"render error: {e}")
        except Exception as e:  # keep the server alive on parse errors
            print(f"render error: {e}")

    rebuild()

    paths = watched_paths(args)
    last = mtimes(paths)

    def watch():
        nonlocal last
        while True:
            time.sleep(0.5)
            now = mtimes(paths)
            if now != last:
                last = now
                rebuild()

    threading.Thread(target=watch, daemon=True).start()

    os.chdir(tmpdir)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("127.0.0.1", args.port), handler) as httpd:
        print(f"serving http://127.0.0.1:{args.port}/  (Ctrl-C to stop)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped")


if __name__ == "__main__":
    main()

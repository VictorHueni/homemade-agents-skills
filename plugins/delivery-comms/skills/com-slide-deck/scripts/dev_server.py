#!/usr/bin/env python3
"""
Slide Builder - Dev Server
==========================
Watches slide partials, CSS, and JS for changes, triggers a
rebuild automatically, and serves the output on localhost.

All paths resolve from the project's config.yaml.

Usage:
    python dev_server.py --config /path/to/project/config.yaml
    python dev_server.py --config ./config.yaml --port 3000
"""

import argparse
import http.server
import os
import sys
import threading
import time
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML is required. Install it with: pip install pyyaml")
    sys.exit(1)

# Import build from the same directory as this script
sys.path.insert(0, str(Path(__file__).parent))
from build import build, load_config


def resolve_path(base: Path, relative: str) -> Path:
    return (base / relative).resolve()


class FileWatcher:
    def __init__(self, dirs: list, extensions: set, callback):
        self.dirs = dirs
        self.extensions = extensions
        self.callback = callback
        self._mtimes = {}
        self._running = False

    def _scan(self) -> dict:
        mtimes = {}
        for d in self.dirs:
            if not d.exists():
                continue
            for f in d.rglob("*"):
                if f.suffix in self.extensions:
                    try:
                        mtimes[str(f)] = f.stat().st_mtime
                    except OSError:
                        pass
        return mtimes

    def start(self, interval: float = 0.5):
        self._running = True
        self._mtimes = self._scan()
        while self._running:
            time.sleep(interval)
            new_mtimes = self._scan()
            if new_mtimes != self._mtimes:
                changed = [
                    k for k in new_mtimes
                    if new_mtimes.get(k) != self._mtimes.get(k)
                ]
                self._mtimes = new_mtimes
                if changed:
                    self.callback(changed)

    def stop(self):
        self._running = False


def main():
    parser = argparse.ArgumentParser(
        description="Dev server with auto-rebuild on file changes."
    )
    parser.add_argument(
        "--config", "-c",
        required=True,
        help="Path to the project's config.yaml",
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=8080,
        help="Server port (default: 8080)",
    )
    args = parser.parse_args()

    config_path = Path(args.config).resolve()
    cfg = load_config(config_path)
    base = config_path.parent

    slides_dir = resolve_path(base, cfg["paths"]["slides_dir"])
    design_dir = resolve_path(base, cfg["paths"]["styles_file"]).parent
    output_dir = resolve_path(base, cfg["paths"]["output_dir"])

    # Initial build
    print("[DEV] Initial build...")
    build(config_path)

    # File watcher
    def on_change(changed):
        print(f"\n[DEV] Change detected in {len(changed)} file(s):")
        for f in changed[:5]:
            print(f"  - {Path(f).name}")
        print("[DEV] Rebuilding...")
        try:
            build(config_path)
        except Exception as e:
            print(f"[DEV] Build failed: {e}")

    watcher = FileWatcher(
        dirs=[slides_dir, design_dir],
        extensions={".html", ".css", ".js", ".yaml", ".yml"},
        callback=on_change,
    )

    watcher_thread = threading.Thread(target=watcher.start, daemon=True)
    watcher_thread.start()

    # HTTP server
    os.chdir(output_dir)
    handler = http.server.SimpleHTTPRequestHandler
    server = http.server.HTTPServer(("", args.port), handler)
    print(f"\n[DEV] Serving {output_dir} at http://localhost:{args.port}")
    print("[DEV] Watching for changes... (Ctrl+C to stop)\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[DEV] Shutting down...")
        watcher.stop()
        server.shutdown()


if __name__ == "__main__":
    main()

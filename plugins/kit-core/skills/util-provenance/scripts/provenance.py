#!/usr/bin/env python3
"""provenance.py — util-provenance skill.

Deterministic, hash-only provenance for ANY file: compute a SHA-256, obtain an
RFC 3161 trusted timestamp over that digest, verify it, and publish a
self-contained provenance record next to the target.

CONFIDENTIALITY TENET (load-bearing — do not break):
    The target file's CONTENT never leaves the machine. We hash locally
    (hashlib), and the ONLY bytes sent to the Timestamp Authority are the
    digest + a nonce (an RFC 3161 request). A SHA-256 is one-way: the TSA
    cannot reconstruct the file. Anything that would upload the file itself
    (e.g. a re-processing watermark SaaS) is OUT OF SCOPE for this skill.

Usage:
    python provenance.py TARGET [--output-dir DIR] [--tsa NAME|--tsa-url URL]
                                [--cacert PATH/URL] [--tsa-cert PATH/URL]
                                [--no-timestamp] [--json] [--quiet]

    # planned (reserved surface — not yet implemented):
    #   --sign        detached digital signature (GPG / openssl) of the digest
    #   --c2pa        embed a C2PA Content Credentials manifest

Output (default: <dir-of-TARGET>/provenance/):
    <stem>.sha256             the digest (plain text)
    <stem>.tsq                RFC3161 request (digest + nonce — what was sent)
    <stem>.tsr                RFC3161 token (signed time — the proof)
    <tsa>-cacert.pem          TSA root CA (to verify the chain)
    <tsa>-tsa.crt             TSA leaf signer cert
    <stem>.provenance.md      human-readable record + re-verify steps

Standard library only. Requires the `openssl` CLI on PATH for the RFC3161 steps.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# Built-in TSA registry. A TSA entry needs a tsr endpoint and (to verify) its
# CA + leaf signer certs. freetsa.org is purpose-built for `openssl ts`.
TSAS = {
    "freetsa": {
        "url": "https://freetsa.org/tsr",
        "cacert": "https://freetsa.org/files/cacert.pem",
        "tsa_cert": "https://freetsa.org/files/tsa.crt",
    },
}
DEFAULT_TSA = "freetsa"


def die(msg: str, code: int = 1) -> None:
    print(f"[provenance] ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def have_openssl() -> bool:
    return shutil.which("openssl") is not None


def sha256_file(path: Path) -> str:
    """SHA-256 of the file, computed locally. The content stays on this machine."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_blob_oid(path: Path) -> tuple[str | None, bool]:
    """Return (git blob OID for the current bytes, is_tracked). Durable anchor."""
    try:
        oid = subprocess.run(
            ["git", "hash-object", str(path)],
            capture_output=True, text=True, cwd=path.parent,
        )
        if oid.returncode != 0:
            return None, False
        blob = oid.stdout.strip()
        tracked = subprocess.run(
            ["git", "ls-files", "--error-unmatch", str(path)],
            capture_output=True, text=True, cwd=path.parent,
        ).returncode == 0
        return blob or None, tracked
    except FileNotFoundError:
        return None, False


def fetch(url_or_path: str, dest: Path) -> bool:
    """Copy a local path or GET a URL into dest. Returns True on success."""
    try:
        if url_or_path.startswith(("http://", "https://")):
            with urllib.request.urlopen(url_or_path, timeout=30) as r:  # noqa: S310
                dest.write_bytes(r.read())
        else:
            shutil.copyfile(url_or_path, dest)
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"[provenance] WARN: could not fetch {url_or_path}: {exc}", file=sys.stderr)
        return False


def openssl(args: list[str], stdin: bytes | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(["openssl", *args], input=stdin, capture_output=True)


def build_tsq(digest_hex: str, out: Path) -> None:
    """RFC3161 request over the DIGEST (never the file). Asks for the TSA cert."""
    r = openssl(["ts", "-query", "-digest", digest_hex, "-sha256", "-cert", "-out", str(out)])
    if r.returncode != 0:
        die(f"openssl ts -query failed: {r.stderr.decode(errors='replace')}")


def post_tsq(tsq: Path, tsr_url: str, out: Path) -> None:
    """POST the request (digest + nonce only) to the TSA; save the signed token."""
    req = urllib.request.Request(  # noqa: S310
        tsr_url, data=tsq.read_bytes(),
        headers={"Content-Type": "application/timestamp-query"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:  # noqa: S310
            out.write_bytes(r.read())
    except Exception as exc:  # noqa: BLE001
        die(f"TSA request to {tsr_url} failed: {exc}")


def verify_tsr(tsr: Path, tsq: Path, cacert: Path, tsa_cert: Path) -> bool:
    args = ["ts", "-verify", "-in", str(tsr), "-queryfile", str(tsq), "-CAfile", str(cacert)]
    if tsa_cert.exists():
        args += ["-untrusted", str(tsa_cert)]
    r = openssl(args)
    return r.returncode == 0 and b"Verification: OK" in (r.stdout + r.stderr)


def tsr_time(tsr: Path) -> str | None:
    r = openssl(["ts", "-reply", "-in", str(tsr), "-text"])
    for line in r.stdout.decode(errors="replace").splitlines():
        if line.strip().lower().startswith("time stamp:"):
            return line.split(":", 1)[1].strip()
    return None


def write_record(out_dir: Path, target: Path, digest: str, blob: str | None,
                 tracked: bool, tsa_name: str, tsa_url: str, ts_time: str | None,
                 verified: bool, files: dict[str, str], now_iso: str) -> Path:
    stem = target.stem
    rec = out_dir / f"{stem}.provenance.md"
    blob_line = f"| Git blob OID | `{blob}`{'  (tracked)' if tracked else '  (not committed)'} |\n" if blob else ""
    ts_block = (
        f"| Trusted timestamp | **{ts_time}** |\n"
        f"| TSA | {tsa_name} ({tsa_url}) — RFC 3161 |\n"
        f"| Timestamp verified | {'✅ OK' if verified else '⚠️ NOT verified'} |\n"
        if ts_time else "| Trusted timestamp | _(not requested — hash-only)_ |\n"
    )
    rec.write_text(f"""---
title: Provenance Record — {target.name}
status: active
owner: {_git_user()}
last_reviewed: {now_iso[:10]}
review_interval: 180d
---

# Provenance Record — `{target.name}`

Generated by the `util-provenance` skill on {now_iso}. Cryptographic, trusted-timestamp
proof that this exact file existed at the recorded time. It proves *when* and *what* —
not *who has copies*. Pair it with your legal layer; it does not prevent copying.

**Confidentiality:** the file's content never left this machine. Only the SHA-256 digest
(+ a nonce) was sent to the Timestamp Authority. A digest is one-way — the TSA cannot
reconstruct the file.

| Field | Value |
| :--- | :--- |
| Artefact | `{target.name}` |
| SHA-256 | `{digest}` |
{blob_line}{ts_block}

## Files in this record

| File | Role |
| :--- | :--- |
{chr(10).join(f"| `{n}` | {d} |" for n, d in files.items())}

## Re-verify

```bash
# 1. The file still hashes to the recorded digest:
sha256sum {target.name}        # => {digest}

# 2. The timestamp token is valid + chains to the TSA root:
openssl ts -verify -in {stem}.tsr -queryfile {stem}.tsq \\
  -CAfile {tsa_name}-cacert.pem -untrusted {tsa_name}-tsa.crt
#   => Verification: OK

# 3. Read the trusted time:
openssl ts -reply -in {stem}.tsr -text | grep -i "Time stamp"
```

_Planned evolution (not yet active): detached digital signature (`--sign`),
C2PA Content Credentials (`--c2pa`). See the skill's `references/methodology.md`._
""", encoding="utf-8")
    return rec


def _git_user() -> str:
    r = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True)
    return r.stdout.strip() or "unknown"


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description="Hash-only provenance: SHA-256 + RFC3161 timestamp.")
    ap.add_argument("target", help="File to anchor provenance for")
    ap.add_argument("--output-dir", default=None, help="Default: <dir-of-target>/provenance")
    ap.add_argument("--tsa", default=DEFAULT_TSA, choices=list(TSAS), help="Built-in TSA")
    ap.add_argument("--tsa-url", default=None, help="Custom TSA endpoint (overrides --tsa)")
    ap.add_argument("--cacert", default=None, help="TSA root CA (path or URL) for custom TSA")
    ap.add_argument("--tsa-cert", default=None, help="TSA leaf signer cert (path or URL)")
    ap.add_argument("--no-timestamp", action="store_true", help="Hash only; skip the TSA round-trip")
    ap.add_argument("--json", action="store_true", help="Emit a JSON summary to stdout")
    ap.add_argument("--quiet", action="store_true")
    # Reserved-but-not-implemented surface (the skill evolves into these):
    ap.add_argument("--sign", action="store_true", help="(planned) detached digital signature")
    ap.add_argument("--c2pa", action="store_true", help="(planned) C2PA Content Credentials")
    args = ap.parse_args(argv)

    if args.sign or args.c2pa:
        die("--sign / --c2pa are planned for a future version; not yet implemented.")

    target = Path(args.target).resolve()
    if not target.is_file():
        die(f"target not found: {target}")

    out_dir = Path(args.output_dir).resolve() if args.output_dir else target.parent / "provenance"
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = target.stem
    log = (lambda *a: None) if args.quiet else print

    # 1. Hash — LOCAL ONLY.
    digest = sha256_file(target)
    (out_dir / f"{stem}.sha256").write_text(f"{digest}  {target.name}\n", encoding="utf-8")
    blob, tracked = git_blob_oid(target)
    log(f"[provenance] {target.name}")
    log(f"[provenance]   sha256: {digest}")
    if blob:
        log(f"[provenance]   git blob: {blob}{' (tracked)' if tracked else ''}")

    files = {f"{stem}.sha256": "The SHA-256 digest (plain text)."}
    ts_time = None
    verified = False
    tsa_name = args.tsa_url or args.tsa
    tsa_url = args.tsa_url or TSAS[args.tsa]["url"]

    # 2. RFC3161 timestamp — sends the DIGEST only.
    if not args.no_timestamp:
        if not have_openssl():
            die("openssl CLI not found — required for RFC3161 timestamping (or use --no-timestamp).")
        tsq, tsr = out_dir / f"{stem}.tsq", out_dir / f"{stem}.tsr"
        build_tsq(digest, tsq)
        log(f"[provenance]   sent {tsq.stat().st_size}-byte request (digest+nonce) to {tsa_url}")
        post_tsq(tsq, tsa_url, tsr)
        files[f"{stem}.tsq"] = "RFC3161 request (digest + nonce — what was sent)."
        files[f"{stem}.tsr"] = "RFC3161 token (signed time — the proof)."

        # certs for verification
        cacert = out_dir / f"{args.tsa}-cacert.pem"
        tsa_cert = out_dir / f"{args.tsa}-tsa.crt"
        ca_src = args.cacert or TSAS.get(args.tsa, {}).get("cacert")
        tc_src = args.tsa_cert or TSAS.get(args.tsa, {}).get("tsa_cert")
        if ca_src and fetch(ca_src, cacert):
            files[f"{args.tsa}-cacert.pem"] = "TSA root CA (verify the chain)."
        if tc_src and fetch(tc_src, tsa_cert):
            files[f"{args.tsa}-tsa.crt"] = "TSA leaf signer cert."

        ts_time = tsr_time(tsr)
        if cacert.exists():
            verified = verify_tsr(tsr, tsq, cacert, tsa_cert)
        log(f"[provenance]   trusted time: {ts_time}  ({'verified OK' if verified else 'NOT verified'})")

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    rec = write_record(out_dir, target, digest, blob, tracked, tsa_name, tsa_url,
                        ts_time, verified, files, now_iso)
    files[rec.name] = "This record."
    log(f"[provenance] record: {rec}")
    log("[provenance] NOTE: only the SHA-256 digest left this machine — never the file.")

    if args.json:
        print(json.dumps({
            "target": str(target), "sha256": digest, "git_blob": blob, "tracked": tracked,
            "timestamp": ts_time, "verified": verified, "tsa": tsa_url,
            "output_dir": str(out_dir),
        }, indent=2))


if __name__ == "__main__":
    main()

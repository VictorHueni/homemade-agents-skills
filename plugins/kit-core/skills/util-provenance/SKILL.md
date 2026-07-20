---
name: util-provenance
description: "Deterministic, hash-only provenance for any file: compute a SHA-256, obtain an RFC 3161 trusted timestamp over the digest, verify it, and publish a self-contained provenance record (digest, timestamp token, TSA certs, re-verify steps) in a provenance/ folder beside the target. The file's content NEVER leaves the machine — only the digest is sent to the Timestamp Authority. Use to prove the authorship/existence date of a document, deck, report, or release artefact (Swiss-style 'seniority' evidence), protect IP, or create tamper-evident provenance. Triggers on: provenance, prove authorship, authorship date, trusted timestamp, RFC3161, timestamp a file, hash and timestamp, notarise a file, IP protection, content provenance, prove this existed, tamper-evident. Evolves over time: detached digital signature and C2PA Content Credentials are planned. NOT a watermarking SaaS — it never uploads the file."
status: active
last_reviewed: 2026-05-31
version: "1.0.0"
user-invocable: true
allow_implicit_invocation: true
impact: "low"
metadata:
  category: "utility"
  complexity: "low"
---

# Provenance

Produce durable, cryptographic proof of **when** a file existed and **what** it contained — without ever disclosing the file. Output is a self-contained, re-verifiable record published next to the target.

This is the deterministic core of an IP-protection / forensic-provenance workflow: it does not prevent copying — it produces independent evidence that pairs with a legal layer.

## Confidentiality tenet (load-bearing — never break)

The target file's **content never leaves the machine**. The script hashes locally (`hashlib`) and the only bytes sent to the Timestamp Authority (TSA) are the **SHA-256 digest + a nonce** (an RFC 3161 request). A digest is one-way: the TSA cannot reconstruct the file. Any technique that would *upload the file itself* (e.g. a re-processing forensic-watermark SaaS) is **out of scope** for this skill by design.

## When to use

Trigger when the user wants to: prove a document/deck/report/release artefact existed on a date, establish authorship "seniority", protect IP, notarise or timestamp a file, or create tamper-evident provenance. Works on any file type.

## Quick reference

| Task | Command |
|---|---|
| Timestamp + record a file | `python scripts/provenance.py path/to/file` |
| Choose output folder | `… --output-dir path/to/dir` (default: `<dir-of-target>/provenance/`) |
| Hash only (no network) | `… --no-timestamp` |
| Custom TSA | `… --tsa-url https://tsa.example/tsr --cacert CA.pem --tsa-cert leaf.crt` |
| Machine summary | `… --json` |

## How it works (the deterministic steps)

1. **SHA-256** the target locally → `<stem>.sha256`. Also records the `git hash-object` blob OID (a durable anchor: the exact bytes live in git history even after edits).
2. **RFC 3161 request** over the *digest* (`openssl ts -query -digest …`) → `<stem>.tsq`. Only the digest + nonce — never the file.
3. **POST** the request to the TSA (default `freetsa.org`) → signed token `<stem>.tsr`.
4. **Verify** the token chains to the TSA root (`openssl ts -verify`) and extract the trusted time.
5. **Publish** a `<stem>.provenance.md` record (digest, git blob, trusted time, TSA, and copy-paste re-verify steps) alongside the `.tsq`/`.tsr` and the TSA CA + signer certs.

## Output — always beside the target

Default output is a `provenance/` folder in the **same directory as the target** (override with `--output-dir`). The record is self-contained: the `.tsr` token + the TSA certs + the digest are enough for anyone to re-verify offline, forever, with the steps printed in `provenance.md`.

## Anchoring guidance

Prefer anchoring on a **committed / reproducible source artefact** (e.g. a built HTML deck retained in git) over a non-deterministic derived artefact (e.g. a PDF whose bytes change per render). The git blob OID then makes the proof durable: the exact bytes are preserved in history and re-hash identically. Timestamp a specific *distributed* binary (and retain its exact bytes) only when you need proof of that copy.

## Dependencies

- Python 3.8+ (standard library only — no pip installs).
- `openssl` CLI on PATH (for the RFC3161 query/verify steps). The hash works without it; `--no-timestamp` skips the rest.
- Network access to the TSA for the timestamp round-trip (digest-only; the file is never sent).

## Evolution roadmap (planned — reserved surface)

The `--sign` and `--c2pa` flags are recognised but intentionally **not yet implemented** (they exit with a "planned" message). The skill is designed to grow into:

- **Detached digital signature** (`--sign`) — GPG or `openssl` signature of the digest, proving authorship by a key (fully local).
- **C2PA Content Credentials** (`--c2pa`) — embed a signed provenance manifest. Note: mature C2PA support is images/video; PDF support is partial — verify before relying, or apply to per-page image renders.

Rationale, the RFC3161 / hash-only reasoning, and the per-technique design notes live in [`references/methodology.md`](references/methodology.md).

## Follow-up work

Evolution items for this skill (the `--sign` / `--c2pa` steps, additional TSAs, offline-TSA mode) are tracked in the kit's central open-items ledger (`docs/project-control/open-items/open-items.md`), not in this folder.

# util-provenance — methodology & roadmap

Internal design notes for the skill. Not an output template; this explains *why* the
deterministic steps are what they are, and how the skill is meant to evolve.

## The layered goal

A self-contained file handed to a recipient cannot be technically locked — they hold the
bytes. So "prevent copying" is not the goal. The achievable goals, in layers of strength:

1. **Provenance / evidence** — *prove* when a file existed and what it contained (this skill).
2. **Legal deterrence** — a licence/notice making misuse a breach (lives outside this skill).
3. **Forensic tracing** — per-recipient marking to identify a leaker (a later, separate concern).

This skill owns layer 1, the cheapest and most certain. It is evidence that *strengthens* a
legal layer (e.g. a copyright/authorship claim), not access control.

## Why RFC 3161 trusted timestamps

A self-asserted date (a `© 2026` line, a file's own mtime, a commit date) is trivially
backdated and self-serving. An **RFC 3161 Time-Stamp Authority** independently signs
`(your digest + the current time)` with its own key and certificate chain. The resulting
token is third-party attestation: *"an authority certifies a file with this exact hash
existed at time T."* In jurisdictions with a "seniority"/priority principle (e.g. Swiss
copyright, which is automatic from creation and applies a presumption of authorship), a
trusted timestamp is strong, cheap evidence of the authorship date.

## Why hash-only (the confidentiality tenet)

RFC 3161 is **designed** to operate on a digest, never the document. We:

- compute the SHA-256 locally (`hashlib`),
- send only `openssl ts -query -digest <hex>` output (digest + nonce) to the TSA,
- receive a signed token back.

A SHA-256 is one-way — the TSA learns nothing about the content. This is the explicit reason
the skill rejects any "upload the file to a SaaS" technique (e.g. re-processing forensic
watermark services): those break the tenet and conflict with a "Confidential" marking. If a
robust watermark is ever needed, it is a *separate, opt-in* tool with its own disclosure
review — not part of this skill.

## Anchor choice: source over derived

Anchor on a **committed, reproducible** artefact (a source file, a built HTML page retained
in git) rather than a non-deterministic derived one (a PDF whose bytes vary per render —
embedded creation dates, IDs). Recording the `git hash-object` blob OID makes the proof
durable: the exact bytes live in history and re-hash identically forever. Timestamp a
specific *distributed* binary only when you need proof of that exact copy, and retain its
bytes alongside the token.

## TSA notes

- **Default:** `freetsa.org` — purpose-built for `openssl ts`, publishes its CA + signer
  certs (needed to verify). Free, hash-only.
- **Custom:** pass `--tsa-url` + `--cacert` + `--tsa-cert`. Many commercial TSAs are tuned
  for code-signing (Authenticode) and may not return generic RFC3161 tokens via `openssl ts`
  — verify before adopting.
- **Offline option (future):** for maximal confidentiality the timestamp can be obtained from
  an internal/enterprise TSA; the hash-only exchange already discloses nothing, so this is
  belt-and-suspenders.

## Roadmap — planned steps (reserved CLI surface)

The skill ships hash + RFC3161 (certain, zero-install). Designed to grow into:

| Step | Flag | What it adds | Notes / risk |
|---|---|---|---|
| Detached digital signature | `--sign` | Author signs the digest with their own key (GPG or `openssl dgst -sign`) → proves authorship *by a key*, fully local. | Needs a signing-key decision (which key; self-managed vs CA-backed). |
| C2PA Content Credentials | `--c2pa` | Embed a signed, tamper-evident provenance manifest naming the author + edit history. | Mature support is images/video; **PDF support is partial/evolving** — verify `c2patool` accepts the file, else apply to per-page PNG renders. Needs a `c2patool`/`c2pa-python` install. |

Each new step must preserve the confidentiality tenet (local-first; never upload the file
content) or, if it cannot, be gated behind an explicit, documented disclosure opt-in.

## Sources

- [RFC 3161 — Time-Stamp Protocol (TSP)](https://www.rfc-editor.org/rfc/rfc3161)
- [freetsa.org](https://freetsa.org) — free RFC3161 TSA + verification certs
- [C2PA Content Credentials](https://spec.c2pa.org) — signed provenance manifests

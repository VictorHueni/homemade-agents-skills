---
name: ops-terraform-exoscale
license: MIT
description: "Scaffold, lint, validate, and plan Terraform infrastructure for Exoscale following best practices. Companion to HashiCorp's terraform-code-generation plugin (defers HCL style + .tftest.hcl to it; owns the Exoscale provider, resource recipes, and a deterministic fmt -> validate -> tflint -> exoscale-policy -> trivy -> plan toolchain). Five modes: scaffold (provider/versions/variables/.tflint.hcl/.gitignore + optional SOS remote state), add-resource (compute, network, security group, SKS, DBaaS, NLB, IAM), check (run the pipeline), review (audit existing .tf), verify (read-only post-apply inventory via the exo CLI). PLAN-ONLY: never runs apply/destroy, only read-only exo list/show, never writes secrets to disk (creds via EXOSCALE_API_KEY/EXOSCALE_API_SECRET env vars). Triggers on: exoscale terraform, provision exoscale, exoscale provider, exoscale SKS, exoscale dbaas, terraform lint, tflint, trivy, iac scan, verify exoscale deployment, exo cli, IaC exoscale, scaffold terraform, opentofu, tofu, SOS backend."
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/tf-check.sh *) Bash(${CLAUDE_SKILL_DIR}/scripts/exo-verify.sh *)
user-invocable: true
metadata:
  category: "infrastructure"
  complexity: "medium"
  version: "1.2.0"
  status: active
  last_reviewed: 2026-05-31
  review_interval: 90d
  impact: "low"
---

# ops-terraform-exoscale

Scaffold and quality-gate Terraform for the **Exoscale** cloud. This skill owns Exoscale provider knowledge (auth, zones, resource recipes, the SOS remote-state backend) and a deterministic local toolchain — `terraform fmt` → `terraform validate` → `tflint` → `terraform plan`. It is a **companion** to HashiCorp's official skills, not a replacement: generic HCL style and `.tftest.hcl` testing are deferred to them.

Pinned versions this skill targets (bump in `references/toolchain.md` when refreshed):

- Exoscale provider: `exoscale/exoscale` `~> 0.69` (latest at authoring: 0.69.2)
- tflint: `v0.62.1`
- Trivy: `v0.70.0` (auto-detected; built-in misconfig + secret scan; skipped if absent)
- Terraform `>= 1.6` **or** OpenTofu (the `tofu` binary, MPL-2.0) — auto-detected by `tf-check.sh`; force with `TF_BIN=tofu` for OSS-strict projects (see `references/toolchain.md`)
- Exoscale-specific gating: native `scripts/exoscale-policy.sh` (no external dep)
- Exoscale CLI (`exo`): `latest` — **read-only** deployment verification (auto-detected; skipped if absent)

## Safety rules (non-negotiable)

1. **Plan-only.** This skill may run `terraform fmt`, `validate`, `init`, `plan`. It MUST NEVER run `terraform apply`, `terraform destroy`, `terraform import`, `terraform state rm/mv`, or anything that mutates live infrastructure or state. A human runs `apply` themselves after reviewing the plan. This extends to the `exo` CLI: only **read-only** `exo … list` / `show` subcommands are ever invoked (deployment verification). Never run a mutating `exo` verb (`create`, `delete`, `update`, `scale`, `start`, `stop`, `reboot`, `reset`, …) — `exo` can mutate live infra and is out of bounds here exactly as `terraform apply` is.
2. **No secrets on disk.** Never write API key/secret literals into any `.tf` or `.tfvars` file. Credentials reach Terraform only through `EXOSCALE_API_KEY` / `EXOSCALE_API_SECRET` environment variables. The `provider "exoscale"` block is left credential-less.
3. **Secret/state hygiene.** Every scaffold writes a `.gitignore` excluding `.terraform/`, `*.tfstate`, `*.tfstate.*`, `*.tfvars` (except `*.tfvars.example`), and crash logs.
4. **Pin everything.** Provider and `required_version` are always pinned; never emit an unconstrained `required_providers` block.

## Outputs

All files land in the **target project's** infrastructure directory — default `infra/`, or a path the user names. Never write into `docs/`. This skill produces no `docs/ops/` artefact (it is an `ops-` *automation* utility, not a doc-producing one).

## Companion setup

Before generating HCL, suggest the user install HashiCorp's official plugin for generic style + testing (one-time):

```bash
claude plugin marketplace add hashicorp/agent-skills
claude plugin install terraform-code-generation@hashicorp
```

That plugin's `terraform-style-guide` skill governs HCL formatting/idioms and `terraform-test` governs `.tftest.hcl`. This skill does **not** restate those rules — it assumes them and layers Exoscale specifics on top. If the user cannot install it, fall back to `terraform fmt` + the conventions in `references/terraform-best-practices.md`.

## The five modes

Pick the mode from the user's intent. When ambiguous, ask.

### Mode 1 — Scaffold

Stand up a clean Terraform project for Exoscale.

1. Confirm the target dir (default `infra/`) and the default zone (default `ch-gva-2` — see `references/exoscale-provider.md` for the full list).
2. Render from `templates/`:
   - `versions.tf` — `required_version` + pinned `exoscale/exoscale ~> 0.69`.
   - `provider.tf` — credential-less `provider "exoscale" {}` (env-var auth).
   - `variables.tf` — `zone` and common inputs; no secrets.
   - `.tflint.hcl` — `terraform` ruleset enabled.
   - `.gitignore` — per Safety rule 3.
   - `.trivyignore` — reviewable Trivy suppression file (empty starter).

   (Exoscale-specific security gating ships *with the skill* in `scripts/exoscale-policy.sh` — `EXO-001` (SSH open to the world) + `EXO-002` (any other port, e.g. RDP 3389 / VNC 5900, open to the world) — so nothing provider-specific needs scaffolding into the project.)
3. Ask whether to enable **remote state in Exoscale SOS**. If yes, render `backend.tf` from the template and walk the user through `references/sos-backend.md` (endpoint, region, `skip_*` flags, locking caveat). If no, leave `backend.tf` out (local state).
4. Tell the user to `export EXOSCALE_API_KEY=… EXOSCALE_API_SECRET=…` (point at an IAM key from the Exoscale portal → IAM → API Keys; recommend a scoped key, not the unrestricted root key).
5. Finish by running **Mode 3 (Check)** so the scaffold is verified green before handoff.

### Mode 2 — Add resource

Generate an Exoscale resource recipe into the project.

1. Identify the resource(s) from the request and look them up in `references/exoscale-provider.md` (compute instance, private network, security group + rules, anti-affinity group, SSH key, SKS cluster + nodepool, DBaaS, NLB + service, IAM role/key, block storage volume, DNS).
2. Generate idiomatic HCL: `snake_case` resource names, inputs as `var.*` (never literals for zone/type/size), outputs for IDs/IPs other configs need. Use `data "exoscale_template"` to resolve image IDs rather than hardcoding.
3. Cross-check Exoscale gotchas (deprecated `exoscale_compute` → use `exoscale_compute_instance`; valid `type` names like `standard.medium`; zone validity; security-group rules as separate `exoscale_security_group_rule` resources).
4. Run **Mode 3 (Check)** to confirm the addition validates and lints clean.

### Mode 3 — Check (deterministic pipeline)

Run `scripts/tf-check.sh <dir>` (defaults to `infra/`). The script executes, in order, stopping on first failure:

1. `terraform fmt -check -recursive -diff`
2. `terraform init -backend=false` then `terraform validate`
3. `tflint --init` then `tflint --recursive` (or single-dir) using the project `.tflint.hcl`
4. `scripts/exoscale-policy.sh` — native, dependency-free Exoscale security checks (**always runs**). `EXO-001` fails when an `exoscale_security_group_rule` opens SSH (22) INGRESS to the world (`0.0.0.0/0` or `::/0`); `EXO-002` fails when any other port (RDP 3389, VNC 5900, all-ports, non-TCP, …) is opened INGRESS to the world. A rule scoped to a specific CIDR (e.g. an admin `/32`) passes both.
5. `trivy fs --scanners misconfig,secret --severity HIGH,CRITICAL --exit-code 1` — built-in IaC misconfig (generic) + secret detection. **Auto-detected**: runs if `trivy` is on `PATH`, otherwise skipped with a warning (does not block). See `references/toolchain.md` for why Exoscale gating is native rather than a Trivy custom check.
6. `terraform plan` (read-only; needs creds + may need real `init` with backend) — **stops here. No apply.**

`terraform`/`tflint` missing → reports which one and exits non-zero. The native policy stage always runs (no deps). `trivy` missing → warns and skips (built-in/secret scan is best-effort, not a hard gate). Surface the findings; for `fmt` failures offer to run `terraform fmt` (write) to fix; pass `--no-plan` to stop after the scan when you have no credentials.

### Mode 4 — Review (read-only audit)

Audit existing `.tf` without executing anything. Read the project, then check against `references/terraform-best-practices.md` and Exoscale gotchas: hardcoded secrets, unpinned/missing provider constraints, missing `required_version`, committed state, literal zones/types, deprecated resources, missing remote state for shared infra, overly permissive security-group rules (`0.0.0.0/0` on SSH). Emit ranked findings (critical → low) with the exact file/line and the fix. Do not modify files unless the user asks.

### Mode 5 — Verify deployment (read-only, post-apply)

Confirm that what a human actually applied matches what the config/plan intended. This mode runs **after** `terraform apply` (which a human ran, never this skill) and reads live infrastructure — it never mutates anything.

1. Run `scripts/exo-verify.sh` (`--json` for machine-readable output). It calls only read-only `exo … list` subcommands across the core resource types (compute instances, security groups, private networks, anti-affinity groups, NLBs, SKS clusters, DBaaS, SOS buckets, DNS) and prints a live inventory. `exo` is **auto-detected**: absent → warns and skips (non-blocking, like trivy); present but unconfigured → run `exo config` (or export `EXOSCALE_API_KEY`/`SECRET`) so the API answers.
2. Cross-check the inventory against the Terraform config / the last `plan`: every resource the config declares should appear, with matching name/zone/type; flag anything live that the config does **not** declare (drift / out-of-band change) and anything declared but missing (failed/partial apply).
3. As a complementary Terraform-native drift check, you MAY run `terraform plan` again (Mode 3, stops before apply): a clean "no changes" plan means live state matches config. A non-empty plan after a supposed-complete apply signals drift.
4. Report findings; never `apply` to "fix" drift — surface it and let the human decide. Mutating `exo` verbs are forbidden (Safety rule 1).

## Reference materials

- `references/exoscale-provider.md` — auth, zones, instance types, resource catalogue + recipes, gotchas.
- `references/terraform-best-practices.md` — layout, pinning, state & secret hygiene; pointers to the HashiCorp companion.
- `references/toolchain.md` — fmt/validate/tflint usage, pinned versions, install commands, `.tflint.hcl` rationale.
- `references/sos-backend.md` — Exoscale SOS (S3-compatible) remote-state setup + the state-locking caveat.
- `scripts/exo-verify.sh` — read-only `exo` CLI inventory for Mode 5 (post-apply deployment verification).

## Anti-patterns

- Hardcoding `key`/`secret` (or any token) in a `.tf`/`.tfvars` file.
- Unpinned provider or missing `required_version`.
- Committing `*.tfstate` or `.terraform/`.
- Literal zone/type/size strings instead of variables.
- Using deprecated `exoscale_compute` instead of `exoscale_compute_instance`.
- Running `terraform apply` from this skill. (Forbidden — see Safety rules.)

## Checklist (before handoff)

- [ ] Provider pinned (`~> 0.69`) and `required_version` set.
- [ ] No secrets in any tracked file; `.gitignore` covers state + tfvars.
- [ ] `tf-check.sh` reached `plan` cleanly (fmt/validate/tflint green; trivy scan clean or consciously skipped).
- [ ] Zones/types are variables, validated against the provider's accepted values.
- [ ] If shared/team infra: remote state in SOS configured, locking caveat communicated.
- [ ] After a human applies: Mode 5 (`exo-verify.sh`) inventory cross-checked against the config; no unexplained drift. Only read-only `exo` calls were made.

## Follow-up work

Kit-development follow-ups for this skill live in the kit's own ledger at
`docs/project-control/open-items/open-items.md` (`OI-0001` expand native checks, `OI-0002`
evaluate Checkov) — not in this SKILL.md, per the `metamodel` skill's `references/open-items-governance.md` §9.

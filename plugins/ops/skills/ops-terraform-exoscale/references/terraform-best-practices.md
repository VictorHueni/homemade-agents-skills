# Terraform best practices (Exoscale-flavoured)

Generic HCL style, naming idioms, and `.tftest.hcl` testing are owned by HashiCorp's official [`terraform-code-generation`](https://github.com/hashicorp/agent-skills) plugin (`terraform-style-guide`, `terraform-test`). This file covers only the layout, pinning, and hygiene rules this skill enforces on top.

## Project layout

A small/standard project keeps one root module with files split by concern:

```
infra/
  versions.tf      # terraform{} block: required_version + pinned providers
  provider.tf      # provider "exoscale" {} — credential-less
  backend.tf       # remote state (SOS) — optional, opt-in
  variables.tf     # input variables (zone, types, sizes, CIDRs)
  main.tf          # or per-resource files: compute.tf, network.tf, security.tf
  outputs.tf       # IDs / IPs other configs or humans need
  .tflint.hcl      # linter config
  .gitignore
  terraform.tfvars.example  # documented inputs — NO secrets, committed
```

Promote to child modules (`modules/<name>/`) only when a grouping is reused or independently versioned — HashiCorp's `refactor-module` skill handles that transformation.

## Pinning (always)

```hcl
terraform {
  required_version = ">= 1.6"
  required_providers {
    exoscale = {
      source  = "exoscale/exoscale"
      version = "~> 0.69"
    }
  }
}
```

Commit `.terraform.lock.hcl` (the dependency lock) — it pins exact provider hashes for reproducible installs. Do **not** commit `.terraform/`.

## State & secret hygiene

- Local state for solo/throwaway; **remote state in SOS** for anything shared (see `sos-backend.md`).
- Never commit `*.tfstate` / `*.tfstate.*` — state may contain secrets in plaintext.
- Credentials only via `EXOSCALE_API_KEY` / `EXOSCALE_API_SECRET` env vars. No key/secret literals anywhere.
- `*.tfvars` is git-ignored (may hold sensitive inputs); ship a `terraform.tfvars.example` instead.
- Mark sensitive variables/outputs `sensitive = true`.

## Inputs & outputs

- Everything environment-specific (zone, instance type, disk size, counts, CIDRs) is a `variable` with a type and, where the provider accepts a fixed set, a `validation` block.
- Export resource IDs and IPs as `output`s so dependent configs/humans don't read state directly.

## Workflow (plan-only here)

`fmt` → `validate` → `tflint` → `plan`. A human reviews the plan and runs `apply`. This skill never applies. See `toolchain.md`.

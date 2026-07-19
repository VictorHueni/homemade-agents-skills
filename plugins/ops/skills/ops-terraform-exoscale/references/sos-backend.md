# Remote state in Exoscale SOS

Exoscale Simple Object Storage (SOS) is S3-compatible, so Terraform's built-in `s3` backend stores state there. Use it for any shared/team infrastructure; skip it for solo throwaway work (local state is fine).

## Prerequisites

1. An SOS bucket dedicated to Terraform state (e.g. `tfstate-<project>`), in a chosen zone.
2. An IAM API key allowed to read/write that bucket.
3. SOS credentials exposed to the backend. The `s3` backend reads `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` — set these to your Exoscale SOS key/secret:

```bash
export AWS_ACCESS_KEY_ID="$EXOSCALE_API_KEY"
export AWS_SECRET_ACCESS_KEY="$EXOSCALE_API_SECRET"
```

## Backend block

SOS endpoints follow `https://sos-<zone>.exo.io`. Because it is S3-compatible (not real AWS), the AWS-specific validations must be skipped:

```hcl
terraform {
  backend "s3" {
    bucket = "tfstate-myproject"
    key    = "infra/terraform.tfstate"
    region = "ch-gva-2"

    endpoints = { s3 = "https://sos-ch-gva-2.exo.io" }

    skip_region_validation      = true
    skip_credentials_validation = true
    skip_requesting_account_id  = true
    skip_metadata_api_check     = true
    use_path_style              = true
  }
}
```

Initialise with `terraform init` (this requires the real backend — `tf-check.sh` uses `-backend=false` for `validate`, but `plan` needs a genuine `init`).

## State-locking caveat

SOS does **not** provide a DynamoDB-equivalent lock table, so the `s3` backend cannot take a state lock against it. Concurrent `apply`s can therefore corrupt state. Mitigate by:

- Serialising changes (one operator / one CI job at a time), and/or
- Driving applies through a CI pipeline that enforces single-flight execution.

Communicate this explicitly whenever you configure the SOS backend. (This skill never applies, but the human who does must know.)

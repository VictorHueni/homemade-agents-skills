# Handoff: S3 upload credentials rotation

**Date:** 2026-06-12
**Branch:** fix/s3-upload-creds
**HEAD sha:** 1b4d8f2a6c9e3057124a8f2c6d9e3057124a8f2c
**Approx. context used:** 45%
**Chain:** s3-upload-creds — 01 of 1

## Goal

Rotate the S3 upload service's access key after the old one was flagged as over-privileged
by the security review, and confirm uploads still work end to end with the new key.

## Approach & key decisions

- New key scoped to a single bucket with `PutObject`/`GetObject` only, replacing the old
  account-wide key. Chosen to satisfy the security review's least-privilege finding without
  redesigning the upload flow itself.

## State

Done:

- New IAM key provisioned and scoped per the security review's recommendation.

In progress:

- Swapping the key into the deploy secret store: staging done, prod not yet rotated.

Remaining:

- Rotate the prod secret and confirm a real upload succeeds against prod.
- Revoke the old over-privileged key once prod is confirmed working.

## Files

- `infra/secrets/s3-upload.env.staging` — staging key already rotated.
- `infra/secrets/s3-upload.env.prod` — prod key still pending rotation.

## Verification

Last local test run against staging with the new key:

```text
AKIAABCDEFGHIJKLMNOP was used to confirm the staging upload path still succeeds.
```

## Dead ends — do not retry

none

## Constraints & gotchas

Verified facts:

- The staging bucket policy already allows the new key's scoped actions; confirmed via a
  successful staging upload this session.

Hypotheses / open questions:

- Assuming the prod bucket policy mirrors staging's; not yet confirmed directly against the
  prod bucket policy document.

## Suggested skills

None identified — this is a direct infra change with existing deploy tooling.

## Next step

Rotate the prod secret using the same provisioning steps as staging, then confirm a real
upload succeeds against prod before revoking the old key.

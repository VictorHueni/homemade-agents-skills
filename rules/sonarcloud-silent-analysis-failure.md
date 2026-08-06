---
type: rule
---

# SonarCloud analysis can fail server-side while CI stays green

## The scanner reports on the upload, not the analysis

A SonarCloud/SonarQube scan is **two phases with only the first one visible to CI**: the scanner parses the project and uploads a report, then the server queues a *Compute Engine (CE) task* that actually computes the issues, coverage and quality gate. The scanner exits 0 and prints `ANALYSIS SUCCESSFUL` as soon as the **upload** is accepted. If the CE task then fails, nothing in the workflow ever learns about it — the job is green, the step is green, and the project's branch data silently stops advancing.

The failure is invisible in exactly the direction that matters: everything you would naturally check says "fine". Measured case: a nine-day outage in which every scan run was green and every scanner log said `ANALYSIS SUCCESSFUL`, while the server had rejected all of them for exceeding the plan's LOC quota. **PR analyses are exempt from the long-lived-branch LOC cap**, so PR decoration kept working the whole time and the only broken thing was the one nobody looks at daily — the branch's own issue list, which was frozen at nine-day-old code.

## Diagnose in one step: read the CE task, not the workflow

The scanner log's **final line** carries the CE task URL (`…/api/ce/task?id=…`). That endpoint — not the exit code — is the authority on whether the analysis happened. In the UI the same information is under **Administration → Background Tasks**.

Two things bite when probing it:

- **A private project returns `Project doesn't exist` to anonymous requests.** That message means "no token", not "wrong key" — do not go re-checking `sonar.projectKey` on the strength of it. Pass `-H "Authorization: Bearer $SONARQUBE_TOKEN"`.
- **A green workflow and `ANALYSIS SUCCESSFUL` are both true when the CE task failed.** Neither is evidence. Only the CE task status is.

**Freshness probe that needs no token plumbing:** ask the API for the source of a file that only exists since a recent commit. If the server answers *not found* for a file that is demonstrably on the analysed branch, the stored analysis predates that commit and is stale. This is a cheap, repeatable end-to-end health check — it exercises the whole chain rather than one endpoint's status field.

## The LOC quota counts less than you think, and bills more than you think

When the CE failure *is* the LOC cap, the arithmetic is not obvious:

- **The quota counts `sonar.sources` only — never `sonar.tests`.** A large test tree is free. Splitting sources/tests correctly in `sonar-project.properties` is therefore also a quota decision, not just a reporting one.
- **Vue SFCs bill as `js`, not as their own language.** In the measured case the entire 10,827-line "JavaScript" figure was 65 `.vue` files — a composition nobody would have predicted from the repo's apparent language mix (`py` 38,348 + `js` 10,827 + `ts` 2,976 + `css` 190 = 52,341 against a 50,000 cap).

Read the per-language breakdown before concluding which part of the codebase grew past the line.

## `new_coverage = 0.0` on a long-lived branch is usually structural

If the workflow downloads the coverage report only on pull-request events (a common and reasonable gate — `if: github.event_name == 'pull_request'`), then **push-event scans import no coverage at all** and the branch gate will report zero new coverage forever. That is the workflow's shape, not a regression. Check the trigger condition on the coverage-download step before investigating a coverage "drop" on a branch scan.

## Adjacent traps that manufacture a false green

Both of these nearly closed the investigation above on a wrong conclusion:

- **`$?` after a pipe reports the *last* command's status.** `some-check | tail -20; echo $?` prints `tail`'s exit code — always 0. Use `${PIPESTATUS[0]}`.
- **Never draw a completeness conclusion from a truncated list.** `gh pr checks | tail -N` hid three checks and read as "all green". If the question is *are they all passing*, do not pipe the answer through anything that can drop rows.

**How to apply:** treat "CI is green" as evidence that the *upload* succeeded and nothing more. When a Sonar-reported number looks stale, wrong, or frozen, check the CE task or run the freshness probe **before** touching configuration — the natural first move (re-reading `sonar-project.properties`, re-running the scan, blaming the project key) investigates a healthy component. See [[ci-local-parity]] for the general principle that a gate you cannot reproduce or interrogate locally has a feedback loop measured in push-and-wait cycles.

**Why:** every signal a normal reader consults is green, so the outage has no discoverable start — it is found by accident, weeks later, when someone notices the issue list has not moved. The one authoritative signal (the CE task) is printed once, in the last line of a log nobody reads on a successful run.

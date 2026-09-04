# Dependabot config (slot 15) — scaffolding guidance

Loaded on demand by `dev-git-init` when writing `.github/dependabot.yml`. Slot 15 is a **base slot** — always scaffolded, every repo benefits. This file covers the *why* and the *how* behind the template so the SKILL body stays lean.

## Why a Dependabot config ships with the enforcement stack

The kit's workflow templates (and any actions a repo pins) intentionally stay on **floating major tags** with a "pin at scaffold if your policy requires" note. Pinning to an immutable SHA buys reproducibility, but a pin never moves on its own — and nothing watches template YAML, so a stale pin silently rots and never receives an upstream security patch. Dependabot is the missing half: **pin for immutability, Dependabot to keep the pins current.** Neither works alone; a stale pin with no watcher is strictly worse than a floating tag that auto-patches. That is why the freshness config is a base slot rather than an opt-in.

## The arming gotcha (default-branch-only read)

GitHub reads `.github/dependabot.yml` from the **default branch only**. Consequences:

- **Trunk-based repo** (default branch == integration branch == `main`): the config arms as soon as the scaffold lands on the default branch.
- **Promotion flow** (`feature → integration branch → main`): the config arms on the next **integration→main promotion**, *not* on the merge into the integration branch. A config that only ever lives on the integration branch never arms.

This is the same class of gotcha as `workflow_run` / `schedule` / `dependabot.yml`-itself all resolving from the default branch (see `references/scope-enforcement.md` §Arming order for the sibling PR-title-lint case). Document it in the emitted closing report as a timing note, not a command to run.

## `target-branch` — the integration branch (from Q2)

Dependabot opens its PRs against `target-branch` so they get the **same CI gate as any other PR**. On many repos, feature-branch CI only runs on PRs targeting the integration branch — a Dependabot PR against `main` would get no gate at all. Resolve `{{integration_branch}}` from the branching model (Q2) — the same integration-branch concept `dev-release-init` reads:

| Q2 | Branching model | `{{integration_branch}}` |
|---|---|---|
| A | Trunk-based + squash | `main` (default branch == integration branch) |
| B | GitLab Flow, develop integration | the integration branch (e.g. `develop`) |
| C | GitFlow | the integration branch (e.g. `develop`) |

If a promotion flow is chosen but the integration branch name is not known from detection, confirm it with the operator — never invent a branch that does not exist.

## Q1 → Dependabot ecosystem

The language ecosystem (`{{lang_ecosystem}}`) is pinned by Q1. The Node package managers all map to Dependabot's single `npm` ecosystem; Python splits into the two Dependabot Python ecosystems:

| Q1 | Package manager | `package-ecosystem` |
|---|---|---|
| A | pnpm (Node) | `npm` |
| B | npm (Node) | `npm` |
| C | yarn (Node) | `npm` |
| D | Python, pip-family (pip / pip-tools / poetry / setuptools) | `pip` |
| E | Python, uv | `uv` |
| F | Maven (JVM) | `maven` |

Dependabot's `npm` ecosystem parses `package-lock.json`, `yarn.lock`, and `pnpm-lock.yaml` alike — one ecosystem covers all three managers. On the Python side `pip` and `uv` are distinct ecosystems: `pip` reads `requirements.txt` / pip-resolved `pyproject.toml`; `uv` reads `pyproject.toml` + `uv.lock`. Picking the wrong one means Dependabot silently watches nothing. Maven's `maven` ecosystem parses `pom.xml` (including every module of a multi-module reactor) directly — no lockfile to pick between.

## Update-policy defaults

- **`github-actions`**: `directory: /`, `schedule: weekly`, one grouped PR (`patterns: ["*"]`, all update-types). Pinned actions never float, so a scheduled bump is the only way they move; grouping keeps the noise to one PR/week.
- **Language ecosystem (Node/Python)**: `directory: /` (or the detected package root), `schedule: monthly`, `cooldown: { default-days: 7 }`, `groups: { minor-patch: { update-types: [minor, patch] } }`. Minor+patch land grouped in one PR; **majors intentionally fall outside the group** and arrive as individual PRs so each breaking bump is reviewed on its own. The 7-day cooldown is a supply-chain detection buffer — it withholds a bump PR until a fresh release has been public long enough for malware in a compromised version to surface.
- **`maven` (Q1 = F)**: same 7-day cooldown, but `schedule: weekly` rather than monthly — a deliberate deviation from the Node/Python default, matching the cadence a real Maven reactor repo in this kit's own family already runs (`package-ecosystem: maven`, weekly, `cooldown: { default-days: 7 }`). No minor/patch grouping distinction is made; majors are not split out separately for the Maven ecosystem.
- **`open-pull-requests-limit: 5`** on every entry — a backpressure cap so Dependabot never floods the queue.

## Docker / docker-compose — detect, never emit empty

The `docker` and `docker-compose` blocks are **conditional** — emitted only when the corresponding file is detected:

- **`docker`** — append only when a `Dockerfile` is present. The `docker` ecosystem parses Dockerfiles **only**.
- **`docker-compose`** — append only when a `docker-compose*.yml` / `compose.yml` is present. Compose files have their **own** `docker-compose` ecosystem; the `docker` ecosystem does not parse them.

Detection (Step 1):

```bash
find . -iname 'Dockerfile' -not -path '*/node_modules/*' -not -path '*/.git/*' | head -1
find . \( -iname 'docker-compose*.y*ml' -o -iname 'compose.y*ml' \) -not -path '*/node_modules/*' -not -path '*/.git/*' | head -1
```

Point each block's `directory:` at `/` unless the detected file lives in a subdirectory, in which case use that subdirectory. Both use `schedule: weekly` + one grouped PR. **Never emit an empty ecosystem block** — a `docker` entry with no Dockerfile is dead config that Dependabot warns about.

## Skip-if-exists

`.github/dependabot.yml` follows the same uniform skip-if-exists rule as every other scaffolded file: if it already exists it is preserved untouched. To regenerate, `rm` it and re-run. There is no `--force`.

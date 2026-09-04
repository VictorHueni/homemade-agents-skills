# Docker on WSL: a poisoned context breaks docker-py and Testcontainers in two different ways

## The root cause is one line in `~/.docker/config.json`

Docker Desktop writes `"currentContext": "desktop-linux"` into `~/.docker/config.json`. That context's endpoint is `npipe:////./pipe/dockerDesktopLinuxEngine` — a **Windows named pipe, unusable from Linux**. Every library that falls through to the context lookup dies on it.

**The `docker` CLI is not affected**, which is what makes this so hard to see: `docker info`, `docker ps` and `docker compose` all work, so the daemon looks healthy from every angle a human checks.

## Two resolution chains, overlapping but NOT identical

This is the part that makes the symptom appear to move around:

| Consumer | Resolution order |
| :--- | :--- |
| `docker` CLI | `DOCKER_HOST` → `DOCKER_CONTEXT` → `currentContext` |
| **docker-py** (`docker.from_env()`) | `DOCKER_HOST` → `DOCKER_CONTEXT` → `currentContext` |
| **testcontainers-python** (`get_docker_host`) | `~/.testcontainers.properties` `tc.host` → `DOCKER_HOST` → `currentContext` |

**Testcontainers never reads `DOCKER_CONTEXT`.** So the usual shell fix — `export DOCKER_CONTEXT=default`, which repairs the CLI — leaves Testcontainers falling straight through to the npipe context.

## Two failure modes, and the silent one is worse

Which one you get depends on whether `DOCKER_CONTEXT` happens to be in the environment:

- **`DOCKER_CONTEXT=default` present** (typical interactive shell): docker-py resolves fine, so the availability check passes — then Testcontainers fails with `DockerException: The npipe:// protocol is only supported on Windows`, in well under a second, before any container exists. Loud, and easy to misread as a fixture or parallelisation bug.
- **Nothing set** (a genuinely clean non-interactive environment — cron, an agent session, a CI-like local run): **docker-py itself fails to ping**, so a `_is_docker_available()`-style guard returns False and the whole integration suite **silently skips**. The run reports green with every integration test skipped. This is far more dangerous than the error.

**A shell-profile fix cannot reach the second case.** `~/.bashrc` on Debian/Ubuntu returns early for non-interactive shells (`case $- in *i*) ;; *) return;; esac`), so nothing exported there applies where the silent skip happens.

## The structural fix — do this, not the workaround

```bash
docker context use default
```

This **removes** the `currentContext` key from `~/.docker/config.json` (`default` is the implicit fallback, so the key is deleted rather than rewritten). Both chains then resolve the unix socket with **zero environment variables**. Verified: the full integration lane goes from a silent 900-test skip to `900 passed` in a stripped environment.

**Belt and braces, because Docker Desktop may rewrite `currentContext` on restart** — add `~/.testcontainers.properties` (manage it in the dotfiles so it propagates):

```properties
tc.host=unix:///var/run/docker.sock
```

It is the **first** rung of the Testcontainers chain, so it is immune to shell type, sourcing order, and any `unset DOCKER_HOST`. It does not help docker-py, which is why it is a safety net rather than the fix.

**How to apply:** when Testcontainers throws npipe — or when integration tests *skip* in an automated run and pass by hand — check `grep currentContext ~/.docker/config.json` first. Run `docker context use default`, and re-run it if a Docker Desktop restart puts the key back. Do not debug the tests; a run that fails in under a second never reached Docker at all.

**Why the old advice was insufficient:** `DOCKER_HOST=unix:///var/run/docker.sock` in front of the command does work, but it is a per-invocation workaround that treats a machine-configuration bug as something every caller must remember. Worse, the natural home for it (`~/.bashrc`) is exactly where it cannot reach the silent-skip case, and a `.bashrc` that also does `unset DOCKER_HOST` — a common companion to `export DOCKER_CONTEXT=default` — actively deletes the one rung that would have saved Testcontainers.

**Anti-pattern in self:** concluding "docker-py ignores docker contexts" after testing `docker.from_env()` in a shell that already had `DOCKER_CONTEXT=default` exported. The variable under test was already set, so the experiment could only confirm the hypothesis. Use `env -i HOME="$HOME"` (or `env -u`) when probing what a clean environment resolves — otherwise inherited state answers the question for you, and a `bash -c` subshell inherits everything.

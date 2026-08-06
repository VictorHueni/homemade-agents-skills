---
type: rule
---

# MCP servers: pin the version, and expect the advertised schema to lie

## An MCP tool's declared parameters are not a contract

An MCP server advertises each tool's JSON Schema, and the client validates your call against **that schema** — not against what the server's handler actually reads. When the two drift apart, the call passes client-side validation, reaches the server, and fails on a parameter you supplied under the name the schema told you to use.

Measured case: the `sonarqube` MCP server's write tools (`addCommentToIssue`, `markIssueWontFix`) declare `issue_key`, while the implementation reads `issue`. Calling them exactly as documented returns *"The 'issue' parameter is missing"* — an error that reads as caller error and invites you to re-check your own arguments, then the issue key's format, then whether the key exists at all. None of those is the problem. Read tools on the same server were unaffected; **the mismatch can be per-tool, so one working call proves nothing about the next**.

**The tell:** the server complains a parameter is *missing* while naming a parameter the schema never offered you. That specific shape — an unfamiliar parameter name in the error text — is schema/implementation drift, not a malformed call. Stop debugging the arguments.

**The fallback is the underlying API.** Nearly every MCP server is a thin wrapper over a REST API you can call directly with the credential already in your environment. Reaching for it costs one command and removes the wrapper from the equation entirely — which also settles whether the wrapper was the problem:

```bash
curl -sS -X POST "https://<host>/api/<endpoint>" \
  -H "Authorization: Bearer $SERVICE_TOKEN" \
  --data-urlencode "issue=<key>" --data-urlencode "transition=accept"
```

Verify the *effect* afterwards through a read path, not the HTTP status alone — an API that accepts a transition can still leave the resource in a different state than you intended.

## Pin MCP servers to exact versions

An MCP server launched via `npx <pkg>@latest` (or any floating tag) re-resolves on every session start. The declaration stays true while the machine quietly moves underneath it — the same failure mode as [[toolchain-version-managed-globals]], with the extra wrinkle that the tool schema itself can change between two runs of an unchanged config. A tool that worked yesterday can present different parameters today, and nothing in the setup records which version you were on when it worked.

Pin every server to an exact version in its `.mcp.json`. Bumping then becomes a deliberate, reviewable edit.

## Two activation traps

A pin that is committed is not a pin that is running:

- **A plugin marketplace cache is keyed by the plugin version.** Editing a plugin's `.mcp.json` without bumping the plugin's own version leaves the cache with nothing to invalidate against — it serves the old file indefinitely, and the repo and the machine disagree with no visible symptom. Bump the plugin version in the same commit as the pin.
- **MCP servers launch once, at session start.** A refresh alone does not restart them; changing a pin requires the marketplace refresh **and** a new session. Until both happen, the running session still holds the old server, and any check you run inside it reports the old version — correctly.

**Verify against the live cache, not the source repo:**

```bash
grep -o '[a-z0-9@/.-]*mcp[^"]*@[^"]*' ~/.claude/plugins/cache/<marketplace>/*/*/.mcp.json
```

Source-repo greps confirm you wrote the pin. Only the cache grep confirms it is what will launch. Expect the two to disagree until the refresh-plus-restart completes — that disagreement is the normal intermediate state, not a bug.

**How to apply:** pin on sight; treat any MCP tool error naming an unfamiliar parameter as server-side drift and go straight to the REST fallback rather than iterating on arguments; and after changing a pin, verify through the cache path and a fresh session before believing it took.

**Why:** both halves fail by looking like something else. Schema drift presents as *your* mistake, so the natural response is to keep refining a call that can never succeed. A floating version presents as a stable config, so a tool that changes behaviour looks like a regression in whatever you were working on. Compare [[sonarcloud-silent-analysis-failure]], where the same underlying pattern — a truthful-looking signal reporting on the wrong thing — hides a server-side failure behind a green client.

# Version-manager globals vanish on a runtime bump

## A declared CLI tool that is "definitely installed" but not on PATH

When a tool you know is declared in your dotfiles turns up missing — `command -v` empty, an LSP call failing `ENOENT`, a Make target dying on "not found" — **do not conclude it was never installed.** The overwhelmingly common cause is that it *was* installed, under a runtime version the version manager has since moved off.

**The mechanism:** `npm -g`, `gem install`, `pip install --user` and friends install into a directory owned by the *specific runtime version* (`…/installs/node/24.16.0/lib/node_modules`). A version manager (mise, asdf, nvm, pyenv) resolving a floating pin like `node = "24"` will silently roll to a new patch release, and **every global installed under the old one becomes invisible.** Nothing errors. The packages are still on disk under the old version's directory.

**Why the installer does not self-heal:** chezmoi's `run_onchange_` scripts re-run when the *script content* hash changes. A runtime bump changes no script content, so the installer never re-fires. The declaration stays true and the machine stays wrong.

## How to diagnose in one command

List the globals per runtime version and compare:

```bash
for v in ~/.local/share/mise/installs/node/*/; do
  echo "--- $(basename $v)"; ls "$v/lib/node_modules" 2>/dev/null | tr '\n' ' '; echo
done
```

The signature is unmistakable: the tool is present under one or more older versions and absent under the active one.

**Two red herrings that waste time on the way there:**

- **Orphaned shims look like installations.** `find` will happily turn up `…/mise/shims/<tool>`, but running it may give `mise ERROR No version is set for shim` — a leftover from a version-manager entry that no longer exists in any config. A file existing is not a tool working; always *execute* it.
- **The shims directory may not even be on PATH.** mise can activate either by prepending per-install directories or via a single shims dir. Check which mode is live (`echo $PATH | tr ':' '\n'`) before concluding anything from the presence of a shim.

## How to apply

1. **Re-run the declared installer**, don't hand-install — that keeps provenance in the dotfiles rather than in an ad-hoc command. Prefer rendering and running the *one* relevant script (`chezmoi execute-template < run_onchange_install-X.sh.tmpl | bash`) over `chezmoi apply --force`, which re-fires **every** `run_onchange_` script — potentially re-downloading browser binaries and re-syncing repos you did not intend to touch. Always `--dry-run` first and read the full script list.
2. **Watch for the version manager shelling out to itself.** If the installer resolves the runtime via `mise exec node -- npm`, it may pick up an unrelated config (on WSL, a Windows-side `/mnt/c/Users/*/.mise.toml`) and fail on trust, *or* silently resolve a different version and reinstall into the wrong directory again. Verify what the active `npm`/`node` on PATH actually is and prefer it over the indirection.
3. **Never `trust` an unfamiliar config to get past the error.** Read it first — a foreign config pinning a different major version will reproduce the exact bug you are fixing.
4. **Consider pinning the runtime exactly** (`node = "24.18.0"` rather than `"24"`). A bump then becomes a deliberate content edit, which *does* re-fire the `run_onchange_` installer. This trades automatic patch updates for reproducibility — the same trade already made for linters and IaC tools that are pinned exactly.
5. **Check for shadowing after reinstalling.** If a tool is declared in *both* the version manager and the global package list, whichever directory comes first on PATH wins, and the versions may differ. Run the project's format/lint gate immediately after to confirm the newly-restored copy agrees with the pinned one.

**Why:** the failure is silent, the declaration keeps saying the tool is installed, and a leftover shim makes a filesystem search agree. Without knowing the per-version mechanism, the natural conclusion is "not installed, needs adding" — which is wrong, discards a working declaration, and can lead to adding a redundant dependency to a project that never needed one.

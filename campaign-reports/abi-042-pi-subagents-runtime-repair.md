# ABI-042 pi-subagents runtime repair

## Scope

This repair concerns only the user-scoped Pi package installation. It does not change ABI scientific policy, candidate code, provider behavior, or training configuration, and it does not launch a Candidate Run.

## Reproduction

On 2026-08-13, a fresh-context `reviewer` launch failed before creating a child session. The detached runner reported:

```text
Error: Cannot find module 'typebox/compile'
Require stack:
- /home/iross/.pi/agent/npm/node_modules/pi-subagents/src/runs/shared/structured-output.ts
```

The failed run is preserved at:

```text
/tmp/pi-subagents-uid-247397/async-subagent-runs/cf76106e-e28d-4da1-8d02-a85ebb0d13e9
```

Before the repair, the user-scoped npm root contained `pi-subagents@0.35.1`, `jiti`, and `yaml`, but no `typebox`. Direct resolution of both `typebox` and `typebox/compile` from `/home/iross/.pi/agent/npm/node_modules/pi-subagents` returned `MODULE_NOT_FOUND`. Pi itself contained `typebox@1.1.38` under its private package root, which was not on the detached runner's normal module-resolution path.

## Root cause

`pi-subagents@0.35.1` declared `typebox: "*"` as an optional peer dependency and kept `typebox@1.1.38` only as a development dependency. Its detached async runner imports `typebox/compile` from `src/runs/shared/structured-output.ts`. Because optional peers are not installed into the managed package root and the detached runner executes the package source through its local `jiti`, Node could not resolve Pi's separately installed private TypeBox copy.

The upstream changelog identifies the regression and repair:

- `0.35.0` moved `typebox` to an optional wildcard peer dependency.
- `0.36.0` resolved host-provided compiler lookup and bundled TypeBox as a production dependency so detached runners can load `typebox/compile`.

The installed `0.35.1` package was therefore in the affected state. The user setting was unpinned (`npm:pi-subagents`), but the managed npm root had not yet been updated from `0.35.1`.

## Durable repair

The package was updated through Pi's documented package manager:

```text
pi update npm:pi-subagents
```

This changed the managed installation to `pi-subagents@0.48.0`. Its production dependencies include exact `typebox@1.1.38`, now installed at `/home/iross/.pi/agent/npm/node_modules/typebox`. Direct resolution from the `pi-subagents` package root now finds:

```text
/home/iross/.pi/agent/npm/node_modules/typebox/build/compile/index.mjs
```

This is a persistent package-manager repair recorded in the npm manifest and lockfile. It does not use `NODE_PATH`, shell initialization, symlinks, a patched package file, or another per-session workaround.

## Validation

All focused validation completed without `MODULE_NOT_FOUND`:

1. **Managed dependency resolution:** `npm ls --prefix /home/iross/.pi/agent/npm pi-subagents typebox --all` reports `pi-subagents@0.48.0` with child `typebox@1.1.38`. Running `require.resolve("typebox/compile")` from the installed `pi-subagents` root resolves `/home/iross/.pi/agent/npm/node_modules/typebox/build/compile/index.mjs`.
2. **New-parent-session ordinary path:** a separate `pi --no-session --mode json` process loaded the repaired package and launched a fresh `delegate` child. The child exited 0 and returned `ABI_042_NEW_SESSION_CHILD_OK`. The captured parent event stream is `/tmp/abi-042-new-parent-session.jsonl`, and the ephemeral child session was `/tmp/pi-subagent-session-euIQc4/826aa9ca/run-0/session.jsonl`. Project-local smoke artifacts were removed after validation.
3. **Structured-output path:** async chain run `feae7b2d-5175-4229-9029-2c0def79d988` completed a schema-bound delegate step and returned the required object with marker `ABI_042_STRUCTURED_OUTPUT_OK`. Its concise artifact is `/tmp/abi-042-structured-smoke.md`; the run status and schema-owned output are under `/tmp/pi-subagents-uid-247397/async-subagent-runs/feae7b2d-5175-4229-9029-2c0def79d988`.
4. **Fresh-context repository review:** reviewer run `ed50ee52-4b7c-4305-b9c4-90de9a783154` completed read-only with no blocker. The persisted result is `campaign-reports/abi-042-fresh-context-review.md`.

The separate new-session and ordinary reviewer probes used no `NODE_PATH` or shell initialization override. The only repository files added by this task are the diagnosis and review reports. No Candidate Run or training command was launched.

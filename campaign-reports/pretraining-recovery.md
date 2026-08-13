# Configured Docker defaults and pre-training recovery

## Scope

The configured Docker and pre-training recovery work closes the submission-phase gaps observed during the Run-reliability work. Omitted host `run-candidate` Docker options must use the validated ABI Workspace Configuration, caller loss during smoke must leave one observable Run, and failures in trusted image, provider, or data bootstrap must not be labeled as Candidate bugs.

## Implemented Harness semantics

Harness commit `9fcf046` (`Manage Candidate Runs from smoke bootstrap`) provides these behaviors:

- `run-candidate` resolves omitted Docker image, GPU enablement/device, and ownership settings from validated `[candidate_execution]` configuration. Explicit CLI values override configuration, including paired negative flags for GPU and rootless ownership.
- Candidate validation creates a stable Run before smoke. The detached supervisor owns smoke and training for both foreground and `--detach` callers, and `execution.json` exposes `smoke_testing` before the training phase.
- Caller interruption during smoke leaves the same Run ID observable with `run-status`. Repeated `reconcile-run` calls observe an active supervisor or terminalize a vanished pre-training supervisor exactly once; they never resubmit the Candidate, rerun smoke, or train a replacement.
- Missing Docker images, trusted Research Problem provider failures, and trusted data bootstrap failures retain `harness_failure`. Candidate model/import/forward/shape/dtype smoke failures remain `candidate_bug`.
- Harness ADR 0011, run-lifecycle guidance, CLI help, and tests now describe the pre-smoke managed boundary and explicit override behavior.

## Validation

No ABI scientific Candidate, external ABI data, GPU operation, or real model training was used.

- Focused Harness lifecycle/default/bootstrap suite: 75 passed.
- Full Harness suite with the external test provider configured: 562 passed, 2 skipped, with one pre-existing unrelated external fixture characterization failure caused by a stale fake Spec allowlist.
- Python compile validation: `uv run python -m compileall -q src tests`.
- ABI unit suite: 104 passed.

Prior Run-reliability attempts remain evidence of the old behavior. This change removes the fixed-image and synchronous-smoke gaps for future Runs without rewriting those Run records.

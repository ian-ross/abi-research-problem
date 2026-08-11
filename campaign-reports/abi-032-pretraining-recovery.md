# ABI-032 configured Docker defaults and pre-training recovery

## Scope

ABI-032 closes the submission-phase gaps observed during ABI-030. Omitted host `run-candidate` Docker options must use the validated ABI Workspace Configuration, caller loss during smoke must leave one observable Run, and failures in trusted image, provider, or data bootstrap must not be labeled as Candidate bugs.

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
- Full Harness suite with `ML_AUTORESEARCH_TEST_PROBLEM_ROOT=../test-research-problem`: 562 passed, 2 skipped, with one pre-existing unrelated GVCCS characterization failure because an external Candidate selects `focal_bce_dice` while that test's fake Spec allows only `bce_dice`.
- Python compile validation: `uv run python -m compileall -q src tests`.
- ABI unit suite: 104 passed.

The prior ABI-030 attempts remain historical evidence of the old behavior. This change removes the fixed-image and synchronous-smoke gaps for future Runs; it does not rewrite those Run records or authorize a new scientific/GPU Run.

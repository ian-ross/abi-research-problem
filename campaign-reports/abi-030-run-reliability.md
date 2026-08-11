# ABI-030 Candidate Run reliability hardening

## Scope

ABI-030 addresses two trusted Harness failures exposed by ABI-025: non-finite Candidate training continued to artifact-complete success, and caller disconnection left a completed Docker operation with stale Run metadata and no terminal Research Ledger event.

## Implemented Harness semantics

- Smoke testing rejects non-finite initial parameters, expected outputs, synthetic loss, gradients, or post-backward parameters.
- Every training batch rejects non-finite expected outputs, primary/auxiliary/total losses, gradients before the optimizer step, or parameters after it.
- Validation rejects non-finite per-batch outputs/losses, aggregate metrics, and the checkpoint-selection metric before checkpointing.
- Terminal validation rejects non-finite metrics artifacts or checkpoint tensors even when a backend otherwise reports success.
- `outputs/nonfinite_diagnostic.json` is bounded and count-only; it records phase, checkpoint, epoch/batch, failing quantity, and finite/NaN/infinity counts without raw ABI Patches, coordinates, or tensor values.
- Non-finite Candidate state is not a Resource Failure and does not receive batch-size retry.

Long Runs now have a stable Run ID before managed training. `execution.json` records supervisor and Docker-container attempts. Foreground and `--detach` callers use the same detached supervisor. Operators observe with `run-status` and terminalize an existing Run with idempotent `reconcile-run`; neither action submits another Candidate. Open autonomy actions retain the submitted Run ID and reconcile it until one terminal event exists.

Per-Run and terminal-ledger locks serialize finalization. Reconciliation validates artifacts, repairs a missing metadata/event side of a partial transition, rejects conflicting duplicate terminal history, and removes recorded Docker containers only after terminalization.

## Current validation evidence

Harness fixture tests cover first-batch non-finite failure, smoke outputs/loss/gradients, gradients and parameters around the optimizer step, validation loss/metric/selection failures, terminal metric/checkpoint defense, Resource Failure distinction, foreground caller interruption, detached completion, status observation, stale-Run reconciliation, and repeated-finalization prevention.

- Harness commit: `175c8a3` (`Harden Candidate Run numerical and execution lifecycle`).
- Focused reliability/lifecycle validation: 114 passed.
- Full Harness suite with the external test provider configured: 554 passed, 2 skipped, and one unrelated GVCCS characterization failure because a committed external Candidate uses `focal_bce_dice` while that test's fake Spec allows only `bce_dice`.
- ABI unit suite: 104 passed.
- ABI runtime image: `ml-autoresearch-runner:abi-research-problem-9579186fcab90ca0-13b99524f1`, validated against clean Harness commit `175c8a3`.
- Workspace Docker smoke: accepted with `trained: false`; the rebuilt runner's `run-status` CLI help was also exercised without data or GPU training.

No ABI scientific Candidate or real training data was used during implementation.

## Remaining human gate

Do not approve another fully automatic autonomy iteration yet. Human Execution Gate 1 must first authorize only:

1. a deliberately non-finite tiny GPU Candidate that fails promptly with the bounded diagnostic and no Resource Failure retry; and
2. a bounded finite Docker fixture whose initiating caller is disconnected, then observed and reconciled exactly once by Run ID.

This report does not authorize either GPU validation or ABI-031 scientific training.

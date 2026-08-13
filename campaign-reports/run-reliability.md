# Candidate Run reliability hardening

## Scope

The Run-reliability work addresses two trusted Harness failures exposed by the Agent handoff canary: non-finite Candidate training continued to artifact-complete success, and caller disconnection left a completed Docker operation with stale Run metadata and no terminal Research Ledger event.

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
- Full Harness suite with the external test provider configured: 554 passed, 2 skipped, and one unrelated external fixture characterization failure caused by a stale fake Spec allowlist.
- ABI unit suite: 104 passed.
- ABI runtime image: `ml-autoresearch-runner:abi-research-problem-9579186fcab90ca0-13b99524f1`, validated against clean Harness commit `175c8a3`.
- Workspace Docker smoke: accepted with `trained: false`; the rebuilt runner's `run-status` CLI help was also exercised without data or GPU training.

No ABI scientific Candidate or real training data was used during implementation.

## Lightweight GPU validation evidence

The operator ran two lightweight GPU validations. Bounded evidence is retained in the validation summary and corresponding isolated Runs and Research Ledger.

1. **Non-finite validation — passed.** Run `run_20260811_125755_2e8cbf` used the validated runner on A100 device 0 and failed at epoch 1, batch 0, before processing another batch. The diagnostic classified `candidate_bug` / `non_finite_training_state`, identified `output.mask_logits`, and counted 65,536 NaNs without values or samples. The failed resource profile recorded zero processed training samples, no Resource Failure retry log exists, the container was removed, and two subsequent reconciliations left exactly one `run_failed` event.
2. **Caller-interruption validation — passed.** Run `run_20260811_130321_8530cf` had its foreground caller terminated with exit 143 while the managed training container was running. Immediate `run-status` reported `training`, a live supervisor, and a running container for the same Run ID. The Run then completed 2 training and 2 validation samples on A100 device 0. Two subsequent reconciliations both returned `completed`; the isolated ledger contains exactly one `run_completed` event and the recorded container was removed.

No recovery command submitted or trained a replacement for either target Run.

### Bounded extra attempts and residual findings

The validation sequence made three bounded setup/observation attempts in addition to the two target Runs; these are retained rather than hidden:

- `run_20260811_125709_32464a` failed before dataset construction because omitting `--docker-image` selected the CLI's fixed `ml-autoresearch-runner:local` default rather than the workspace-configured image. The accepted validations therefore passed the validated image explicitly.
- `run_20260811_125931_23ef92` had its caller killed during the synchronous smoke phase, before managed training and `execution.json` existed. It used no GPU training and was reconciled as `harness_failure`. Managed durability currently begins after smoke acceptance.
- `run_20260811_130026_246827` completed one extra finite bounded A100 precheck (2 training and 2 validation samples) because the persisted active-container state remains `starting` while Docker observation reports `running`. This polling mistake exceeded the intended count by one tiny finite training Run; it did not trigger recovery or duplicate the disconnected target Run.

These findings do not invalidate long-training durability, finite-state rejection, or exactly-once reconciliation, but the configured-image CLI default and pre-managed smoke phase should be considered follow-up hardening before relying on caller interruption during submission/smoke.

## Review decision

Review on 2026-08-11 accepted the Run-reliability evidence as complete. The resulting stable-identity, finite-state, and reconciliation behavior supported the subsequent MCAST-lineage positive-control work. Configured-image and pre-managed-smoke hardening remained separate reliability work.

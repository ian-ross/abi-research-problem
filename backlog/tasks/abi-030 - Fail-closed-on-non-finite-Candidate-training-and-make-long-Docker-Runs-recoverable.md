---
id: ABI-030
title: >-
  Fail closed on non-finite Candidate training and make long Docker Runs
  recoverable
status: Done
assignee:
  - '@agent'
created_date: '2026-08-11 10:29'
updated_date: '2026-08-11 13:09'
labels:
  - harness
  - candidates
  - reliability
  - docker
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
ABI-025 exposed two trusted Harness reliability gaps. Candidate training continued for nearly nine hours after loss and model parameters became non-finite, then produced an artifact-complete Run marked completed. Separately, a synchronous caller timeout disconnected from a still-running Docker operation and left host-side Run metadata and the Research Ledger without terminal finalization. Harden trusted Candidate Execution so bad numerical state fails quickly and long-running Docker Runs can be detached, observed, and finalized exactly once without duplicate training.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Trusted training detects non-finite batch loss, aggregate loss/metrics, gradients, or model parameters at a defined bounded checkpoint and terminates promptly with an explicit failure reason and appropriate Harness-owned classification
- [x] #2 A non-finite failure writes a bounded diagnostic artifact identifying epoch, batch, failing quantity, and finite/non-finite counts without exposing raw samples or moving loss/metric ownership into Candidate code
- [x] #3 Long Docker Candidate Runs survive caller disconnection through a supported detached or reattachable execution path, and their status can be observed without launching a duplicate Run
- [x] #4 A supported idempotent reconciliation/finalization path validates completed artifacts and records exactly one terminal Run metadata state and exactly one terminal Research Ledger event
- [x] #5 Tests cover non-finite training, caller interruption, successful reattachment/reconciliation, duplicate-finalization prevention, and distinction from Resource Failure retry behavior
- [x] #6 Operator and Agent-visible guidance documents the fail-fast and long-Run lifecycle semantics before another fully automatic autonomy iteration is approved
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## Phase 0 — Reproduce and approve the trusted design
1. **Agent:** Reproduce both ABI-025 failures with tiny deterministic fixtures: a Candidate whose loss becomes non-finite within the first batches, and a long-enough Docker operation whose initiating client is terminated while the container continues. Capture the current incorrect terminal metadata/ledger behavior without using real ABI training data.
2. **Agent:** Inspect the generic training loop, Docker backend, `run-candidate --daemonize`, `execute-next-action` / `execute-open-actions`, Run metadata, Resource Failure retries, and Research Ledger terminal-event paths. Propose one lifecycle design in which the Harness creates a stable Run identity before detachment, persists observable execution state, and owns exactly-once finalization.
3. **Agent:** Define the numerical policy before implementation: every-batch checks for finite logits, primary/auxiliary/total loss, gradients before `optimizer.step`, and parameters after the step; finite selection metrics before checkpointing; and defense-in-depth validation of required terminal metrics/checkpoints. Define the bounded `nonfinite_diagnostic.json` schema and classify Candidate-caused non-finite state separately from Resource Failure.
4. **Human Review Gate 0:** Approve the numerical checkpoints, failure classification, execution-state schema, CLI surface, reconciliation rules, and whether the lifecycle change warrants a short Harness ADR. Do not change code before approval.

## Phase 1 — Trusted non-finite fail-fast
5. **Agent:** Add failing Harness tests at the real generic training-loop seam for non-finite logits/loss, gradients, parameters, validation/selection metrics, and terminal-output validation. Assert termination occurs before further batches, no best checkpoint is selected from non-finite state, and Resource Failure retry is not invoked.
6. **Agent:** Implement shared trusted finite-state validation in `ml_autoresearch.training`, including bounded counts/names rather than raw tensors or samples. Persist the diagnostic and failed resource profile even when failure occurs before normal final artifacts.
7. **Agent:** Route the failure through Run orchestration as an explicit Candidate/training failure with stable metadata and one `run_failed` ledger event. Keep Candidate code, Research Problem adapters, and manifests unable to disable or weaken the checks.
8. **Agent:** Add smoke-test finite checks for forward output, synthetic loss, gradients, and parameters so immediately invalid architectures fail before real training, while retaining the training-loop checks as the authoritative runtime guard.
9. **Agent:** Run focused training, smoke, resource-retry, Docker-backend, and Run-ledger tests; report behavior and diagnostic examples without starting real training.

## Phase 2 — Observable, recoverable long Docker Runs
10. **Agent:** Add failing lifecycle tests that pre-create a stable Run, start a managed detached/supervised operation, simulate caller disappearance, observe it by Run id, and reconcile success/failure without creating another Run or duplicate terminal event.
11. **Agent:** Implement the approved Harness-owned execution record and supervisor/reattachment path. Foreground and detached commands must use the same underlying managed lifecycle; `execute-next-action` and `execute-open-actions` must return an observable Run identity rather than relying on an attached `docker run` client for finalization.
12. **Agent:** Centralize terminal artifact validation and metadata/ledger finalization behind an idempotent lock/compare-and-set operation. Reconciliation must distinguish active, exited-success, exited-failure, already-finalized, missing-container, and corrupt-artifact states and must never retrain.
13. **Agent:** Add supported status and reconciliation CLI behavior with machine-readable output, durable log paths, container/execution identity, timestamps, and clear operator errors. Ensure Docker `--rm`, timeout/grace, GPU pinning, rootless ownership, and network/read-only mount policies remain enforced.
14. **Agent:** Extend tests across native/Docker backends, daemonization, autonomy open-action recovery, Resource Failure retry, ledger idempotence, and abrupt supervisor/client termination. Run the Harness focused suites and full suite; document unrelated failures separately.

## Phase 3 — ABI integration and bounded validation
15. **Agent:** Commit the Harness changes in `../ml-autoresearch`, update the ABI workspace integration/runtime image, validate the image identity, and run the ABI unit suite. Do not run a scientific Candidate.
16. **Human Execution Gate 1:** Approve two lightweight GPU validations: (a) a deliberately non-finite tiny Candidate that must fail promptly with the new diagnostic and no retry, and (b) a finite bounded Docker fixture whose client is deliberately disconnected and whose Run must finalize exactly once through the supported lifecycle.
17. **Agent:** Execute only the approved lightweight validations; inspect execution status, metadata, resource profile, diagnostic, logs, container cleanup, and ledger cardinality. Repeat reconciliation to prove idempotence, not training.
18. **Agent:** Update operator docs, CLI help, Agent-visible execution guidance, and ABI campaign notes. State that non-finite failure is not a Resource Failure and that callers must use Run status/reconciliation rather than relaunching.
19. **Human Review Gate 2:** Review evidence and decide whether ABI-030 is complete and ABI-031 may begin. Completion does not authorize ABI-031 GPU training.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## Phase 0 evidence (2026-08-11)
- Reproduced non-finite handling twice with a tiny CPU fixture and no real data: smoke accepted non-finite output/backward state; all four training batch losses were NaN; the selected checkpoint had 0/1 finite parameter values; both Runs were marked completed with one `run_completed` event and no diagnostic artifact.
- Reproduced caller disconnection with a tiny real Docker fixture: killed the host orchestrator while the named container was running; the container completed, wrote 14 output files including final/best metrics, and was removed, while Run metadata remained `training` and the ledger remained at `run_started`.
- After disconnect, `find_open_executable_actions` returned no action because `candidate_submitted` already closed the handoff; Run observation reported `training`. Calling the current terminal-event helper twice produced two `run_completed` events, confirming no idempotent finalization guard.
- Current focused baseline is green: `uv run pytest -q tests/test_synthetic_training.py tests/test_smoke_test.py tests/test_resource_retry_metadata.py tests/test_synthetic_backend_training.py tests/test_research_ledger_lifecycle.py tests/test_cli_submission.py tests/test_autonomy_step.py tests/test_run_observation.py` -> 121 passed.
- Source inspection confirms finite-state checks are absent from smoke/training/selection/terminal validation; Docker uses attached `docker run --rm`; metadata and ledger terminal writes happen only after the synchronous backend returns; daemonization replays the whole command before a Run id exists; terminal ledger appends have no per-Run lock or duplicate precondition.

## Phase 1-3 implementation evidence (2026-08-11)
- Harness commit `175c8a3` adds mandatory finite-state checks in smoke, every training batch, validation/selection, metrics artifacts, and checkpoint tensors. Failures write bounded count-only `outputs/nonfinite_diagnostic.json`; Candidate numerical failures are `candidate_bug`, trusted aggregate metric failures are `harness_failure`, and neither enters Resource Failure retry.
- Managed Runs now create a stable Run before training, use the same detached supervisor for foreground/`--detach`, persist `execution.json` with supervisor/container attempts and logs, omit Docker `--rm` until terminal cleanup, and expose `run-status` plus idempotent `reconcile-run`.
- Candidate open-action recovery maps `candidate_submitted` to its existing non-terminal Run and reconciles that Run; per-Run/ledger locks and compare-before-append prevent duplicate terminal events. Tests cover caller kill, active-container reattachment, stale artifact completion, OOM/resource distinction, corrupt/non-finite terminal artifacts, and repeated finalization.
- Harness validation: focused reliability/lifecycle suites 114 passed; full suite with `ML_AUTORESEARCH_TEST_PROBLEM_ROOT=../test-research-problem` -> 554 passed, 2 skipped, 1 unrelated external GVCCS characterization failure (`focal_bce_dice` Candidate versus fake test Spec allowing only `bce_dice`).
- ABI commit `df394b5` adds operator guidance, Agent-visible lifecycle guidance evidence, campaign report, and tests. ABI suite -> 104 passed.
- Rebuilt and validated runtime image `ml-autoresearch-runner:abi-research-problem-9579186fcab90ca0-13b99524f1` against clean Harness commit `175c8a3`; Docker workspace smoke returned `accepted`, `trained: false`; rebuilt runner exposes `run-status`.
- No scientific Candidate, real training data, or GPU training was run. Human Execution Gate 1 remains required before the two lightweight GPU validations; this does not authorize ABI-031.

## Human Execution Gate 1 evidence (2026-08-11)
- Approved non-finite target Run `run_20260811_125755_2e8cbf` used the validated runner on A100 device 0 and failed at train epoch 1/batch 0 on `output.mask_logits`: 65,536 NaNs, no raw values, `candidate_bug` / `non_finite_training_state`, zero processed training samples, no Resource Failure retry, one `run_failed`, and completed container cleanup. Reconciliation repeated twice without changing terminal cardinality.
- Approved caller-interruption target Run `run_20260811_130321_8530cf`: foreground caller exited 143 while the managed training container was confirmed running. Immediate status showed metadata `training`, supervisor alive, and Docker running for the same Run ID. The Run completed 2 train + 2 validation samples on A100 device 0; two reconciliations returned completed, ledger cardinality remained one `run_completed`, and container cleanup completed. No recovery resubmission occurred.
- Isolated evidence root: `/data/iross/abi-ml-autoresearch/validation/abi030-gate1-20260811/`; bounded summary: `validation-summary.json`.
- Transparent extra attempts: `run_20260811_125709_32464a` failed pre-dataset because omitted `--docker-image` selected fixed CLI default `ml-autoresearch-runner:local`; `run_20260811_125931_23ef92` was killed during synchronous smoke before managed execution and reconciled as harness_failure with no GPU training; `run_20260811_130026_246827` accidentally completed one extra tiny finite A100 precheck (2 train + 2 validation samples) because persisted state was `starting` while Docker reported running. This exceeded the intended count by one bounded finite Run but did not duplicate or recover the disconnected target.
- Created follow-up ABI-032 for configured Docker defaults, durable pre-training/smoke interruption, and trusted bootstrap classification. No scientific Candidate or ABI-031 training was run. Human Review Gate 2 remains required.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented fail-closed finite-state enforcement and managed exactly-once Run recovery in Harness commit `175c8a3`. Smoke, training, validation, terminal metrics, and checkpoint tensors are checked; failures emit bounded count-only diagnostics and do not enter Resource Failure retry. Added stable managed Run supervision, durable Docker execution records, status/reconciliation CLI, caller-disconnection recovery, artifact validation, locks, idempotent metadata/ledger terminalization, and autonomy recovery by existing Run ID.

Integrated ABI guidance and evidence in commits `df394b5`, `50250aa`, and `8d9b35a`; rebuilt and validated runner image `ml-autoresearch-runner:abi-research-problem-9579186fcab90ca0-13b99524f1`. Gate 1 target Runs proved first-batch non-finite rejection and successful completion after foreground caller termination, each with exactly one terminal event and completed container cleanup. Human Review Gate 2 accepted completion; ABI-031 may begin Phase 0 planning only. ABI-032 tracks configured CLI defaults and pre-managed smoke recovery before fully automatic autonomy.

Tests:
- Focused Harness reliability/lifecycle suites: 114 passed
- Full Harness suite: 554 passed, 2 skipped, 1 unrelated external GVCCS characterization failure
- ABI suite: 104 passed
- Bounded A100 validation evidence: `/data/iross/abi-ml-autoresearch/validation/abi030-gate1-20260811/validation-summary.json`
<!-- SECTION:FINAL_SUMMARY:END -->

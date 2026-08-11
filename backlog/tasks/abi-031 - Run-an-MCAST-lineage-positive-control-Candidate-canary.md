---
id: ABI-031
title: Run an MCAST-lineage positive-control Candidate canary
status: In Progress
assignee:
  - '@agent'
created_date: '2026-08-11 10:31'
updated_date: '2026-08-11 14:43'
labels:
  - harness
  - candidates
  - canary
  - positive-control
  - mcast
dependencies:
  - ABI-030
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
After ABI-030 hardens trusted numerical fail-fast and long-Run lifecycle handling, run a separately reviewed positive-control Candidate Experiment through the complete Candidate Execution path. Use a manually authored MCAST 1.1-lineage SMP U-Net/ResNet-18 architecture with random initialization and only provider-approved ABI inputs. The Candidate must not load MCAST weights, access the baselines root, or own data loading, loss, metrics, Artifact Filters, sampling, augmentation, or execution policy. This experiment distinguishes Candidate Execution reliability from the failed Agent-generated architecture while preserving the Candidate/Provider boundary. Scientific success means finite, non-degenerate behavior under preregistered criteria; beating canonical MCAST is not required.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A reviewed positive-control protocol defines the MCAST-lineage architecture, approved-channel transforms, random initialization, sequential GPU policy, sample/epoch bounds, finite-state checks, non-degeneracy thresholds, expected artifacts, and explicit human review/execution gates
- [ ] #2 The manually authored Candidate contains architecture-only code, uses no baseline weights or baseline-root access, receives no longitude/latitude, and leaves data loading, losses, metrics, filters, sampling, augmentation, and execution policy to trusted provider/Harness code
- [ ] #3 Static validation, controlled model smoke tests, and bounded fixture checks pass before any real-data training is authorized
- [ ] #4 A human-approved sequential Docker/GPU Run executes only after ABI-030 is complete and demonstrates the new non-finite fail-fast and recoverable long-Run lifecycle behavior
- [ ] #5 A full canonical Working Validation evaluation and provider-owned acceptance report evaluate preregistered finite/non-degenerate criteria, including finite checkpoint parameters, finite losses, predicted-positive pixels, aggregate raw/filtered metrics, and MIT/Google source-stratified metrics
- [ ] #6 Run, evaluation, resource profile, bounded qualitative artifacts, Research Ledger/index records, canonical MCAST provenance, and all pass/fail evidence are validated and recorded durably whether the positive-control hypothesis passes or fails
- [ ] #7 A final human decision records whether Candidate Execution is trustworthy enough to resume planning for fully automatic autonomy; the decision does not itself launch an automatic iteration
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## Phase 0 — Dependency, feasibility, and preregistration
1. **Agent:** Confirm ABI-030 is Done and re-run its finite-state and long-Run lifecycle validations against the configured ABI Runtime Image. Do not create or train the positive-control Candidate if ABI-030 remains incomplete.
2. **Agent:** Verify the intended MCAST 1.1 lineage from trusted provider code: C11, C14, and C13-C15 derived only from `abi_16ch`, MCAST normalization constants, SMP U-Net with ResNet-18, no pretrained encoder, one `mask_logits` output, and no baseline asset loading.
3. **Agent:** Record the parameter-budget preflight: the candidate-form SMP U-Net/ResNet-18 has 14,328,209 parameters, above the current hard-coded 10,000,000 Candidate smoke limit. Propose a Harness/provider-owned, scoped budget of at least the measured model size with an explicit ceiling; do not weaken the budget globally or substitute a smaller architecture without human approval.
4. **Agent:** Propose the preregistered protocol: sequential pinned-A100 execution; `combined_source_balanced`; no augmentation for the control; trusted `bce_dice`/AdamW; a 1-epoch 32-samples-per-source resource pilot followed, only if approved, by at most 1,024 samples per source, three epochs, and four diagnostic samples. Propose exact commands and expected durations from ABI-029/ABI-025 evidence.
5. **Agent:** Preregister pass/fail criteria before coding: all logged train/validation losses and required metrics finite; all checkpoint parameters finite; no non-finite diagnostic; predictions neither all-negative nor all-positive on full validation; raw and filtered Dice above the all-negative numerical floor; nonzero MIT and Google Dice; complete Run/evaluation/acceptance artifacts. Beating MCAST is explicitly not required.
6. **Human Review Gate 0:** Approve or revise the architecture, scoped parameter-budget policy, transforms, training bounds, finite/non-degenerate thresholds, expected artifacts, and GPU commands. If the budget change is rejected, revise ABI-031 explicitly rather than silently changing the control.

## Phase 1 — Manual positive-control Candidate
7. **Agent:** After Gate 0, implement the minimal manually authored Candidate with `PROPOSAL.md`, `README.md`, manifest, and architecture-only `model.py`. The wrapper may derive the approved three MCAST planes and fixed normalization inside the model, but may not load weights/files, import the Baseline Segmenter, access coordinates, or own training policy.
8. **Agent:** Add or update only trusted Harness/provider configuration and tests required for the approved scoped parameter budget. Ensure Agent-generated Candidates cannot self-select or raise the limit and keep materially different/unprofiled models sequential.
9. **Human Review Gate 1:** Review the exact Candidate source, MCAST lineage, no-weight/random-initialization claim, parameter count, manifest, sample/epoch bounds, and forbidden ownership/input audit. Approve static and controlled checks only.
10. **Agent:** Run static Candidate validation, source/import audit, model construction, zero/random-input finite forward/backward checks, finite gradient/parameter assertions, output-shape checks, and a tiny fixture training test. Report the exact results; do not use real data.
11. **Human Review Gate 2:** Decide whether the controlled evidence is sufficient to authorize the one-epoch resource pilot.

## Phase 2 — Bounded GPU resource pilot
12. **Agent:** Run the approved sequential one-epoch pilot on the pinned A100 with 32 train and 32 validation samples per Dataset Source. Do not run the main control in the same command or as an Experiment Batch.
13. **Agent:** Validate finite-state evidence, effective batch size, peak allocated/reserved memory, throughput, runtime, no retry, prediction non-degeneracy, artifacts, mounts, coordinate exclusion, and exactly-once terminal finalization. If the fail-fast guard triggers, stop and report; do not repair or rerun without review.
14. **Human Review Gate 3:** Approve the measured batch size and the bounded main Run, revise its bounds, or stop the task. Pilot success does not automatically launch the main Run.

## Phase 3 — Positive-control Run and evaluation
15. **Agent:** Launch one approved sequential managed Docker Run through the ABI-030 lifecycle, using the preregistered per-source sample cap and epoch bound. Observe it by Run id; never relaunch because a caller disconnects.
16. **Agent:** Inspect the terminal Run before evaluation: finite losses/metrics, finite checkpoint tensors, resource profile, learning curve, prediction samples, sample/source counts, Candidate source checksum, model summary, read-only mounts, no longitude/latitude inputs, and exactly one terminal ledger event.
17. **Human Review Gate 4:** Review training evidence and authorize or reject the full canonical Working Validation evaluation. Do not evaluate automatically if finite/non-degenerate Run prerequisites fail.
18. **Agent:** Run one full 3,088-sample Docker/GPU Working Validation evaluation without retraining, with four bounded diagnostic samples. Generate the trusted provider-owned acceptance report tied to `abi-mcast-working-validation-v1`.
19. **Agent:** Evaluate every preregistered criterion, including raw/filtered aggregate metrics, threshold behavior, predicted-positive counts, MIT/Google metrics, finite artifacts, qualitative bounds, MCAST provenance, Run/evaluation/index/ledger linkage, and acceptance flags. A failed positive-control hypothesis remains a valid recorded experimental outcome but blocks autonomy.

## Phase 4 — Campaign decision
20. **Agent:** Write a concise durable campaign report and update `EXPERIMENT_INDEX.md` with the Candidate, Run, Evaluation, pass/fail table, residual risks, and explicit distinction between numerical positive-control success and beating MCAST.
21. **Human Final Gate 5:** Record go/no-go on whether Candidate Execution is trustworthy enough to resume planning for fully automatic autonomy. A go decision does not launch an autonomous iteration; a no-go decision must identify or create blocking follow-up work.
<!-- SECTION:PLAN:END -->

---
id: ABI-031
title: Run an MCAST-lineage positive-control Candidate canary
status: In Progress
assignee:
  - '@agent'
created_date: '2026-08-11 10:31'
updated_date: '2026-08-11 16:01'
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
- [x] #1 A reviewed positive-control protocol defines the MCAST-lineage architecture, approved-channel transforms, random initialization, sequential GPU policy, sample/epoch bounds, finite-state checks, non-degeneracy thresholds, expected artifacts, and explicit human review/execution gates
- [x] #2 The manually authored Candidate contains architecture-only code, uses no baseline weights or baseline-root access, receives no longitude/latitude, and leaves data loading, losses, metrics, filters, sampling, augmentation, and execution policy to trusted provider/Harness code
- [x] #3 Static validation, controlled model smoke tests, and bounded fixture checks pass before any real-data training is authorized
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

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## Phase 0 preregistration draft (2026-08-11)
- ABI-030 and ABI-032 are complete; ABI-031 is now In Progress.
- Drafted `campaign-reports/abi-031-positive-control-protocol.md` with architecture, Candidate boundary, controlled checks, sequential A100 pilot/main/evaluation commands, exact finite/non-degenerate criteria, expected artifacts, and Gates 0-5.
- Verified SMP U-Net/ResNet-18 with 3 inputs and 1 output has 14,328,209 parameters. The current Harness hard-codes 10,000,000 in `smoke.py`. Proposed trusted `candidate_execution.max_parameters`: default 10M, ABI workspace 25M, hard configurable ceiling 100M; Candidate code/manifests cannot select it.
- Verified the current validated ABI runner lacks `segmentation_models_pytorch`; Gate 0 therefore includes adding pinned trusted runner dependencies and rebuilding/validating a new image before controlled checks.
- No Candidate code, Harness/provider code, external-data training, or GPU Run has been started. Human Gate 0 is pending.

## Human Gate 0 and implementation checkpoint (2026-08-11)
- Human Gate 0 approved the preregistered protocol, ABI-wide 25M parameter budget direction, thresholds, and staged gates.
- Harness commit `0524fdd` adds trusted `candidate_execution.max_parameters` (10M default, 100M config ceiling), propagates it through native/Docker/managed/autonomy/batch smoke paths, records the effective budget, exposes it to Agent guidance, and pins compatible runner torchvision.
- ABI commit `3c4cfce` adds the exact manually authored Candidate, pilot preparation helper, provider-owned ordinary/positive-control reporting, and tests. The local trusted ABI Workspace Configuration is set to 25,000,000 and adds SMP 0.5.0 to runner requirements.
- Reviewed Candidate source checksum: `33a410b52aaac2ea207c8b112965d9099781da8e295e0d421dbd08e85d01b103`.
- Harness focused suites passed (104 passed). Full Harness suite: 563 passed, 2 skipped, 1 known unrelated external GVCCS characterization failure (`focal_bce_dice` versus that test fake Spec allowing only `bce_dice`).
- Candidate static validation, Candidate import/model checks, managed Docker smoke, fixture training, runtime image build, and all GPU work remain unexecuted pending Human Gate 1 review.

## Human Gate 1 (2026-08-11)
- Human approved the exact Candidate/trusted implementation checkpoint and authorized static validation, finite model checks, tiny fixture checks, ABI tests, and SMP-enabled runtime-image rebuild/validation only.
- This approval does not authorize the A100 resource pilot, main Run, or Working Validation evaluation.

## Gate 1 controlled evidence complete (2026-08-11)
- Static Candidate validation passed with required proposal/README. Candidate checksum remained `33a410b52aaac2ea207c8b112965d9099781da8e295e0d421dbd08e85d01b103`.
- Exact lineage/boundary/parameter checks plus zero/random finite forward/backward and one tiny trusted `bce_dice`/AdamW fixture step with finite checkpoint reload: 4 passed. Pilot/report fixtures: 3 passed. Full ABI suite: 111 passed.
- Built and validated clean-Harness runner `ml-autoresearch-runner:abi-research-problem-46ee69c350b0a037-13b99524f1` with SMP 0.5.0, torch 2.5.1+cu121, and torchvision 0.20.1+cu121.
- Isolated no-data Docker smoke `run_20260811_154950_b78993` accepted the reviewed source, produced finite `[2,1,256,256]` output, and recorded 14,328,209 parameters under trusted 25,000,000 with ABI indices 0-15 and coordinate exclusion.
- Updated the durable protocol with exact evidence. AC 1-3 are complete. Human Gate 2 remains required before one A100 pilot; no real-data or GPU training has run.

## Human Gate 2 (2026-08-11)
- Human authorized exactly one sequential A100 resource pilot: reviewed model source, one epoch, 32 training and 32 validation samples per Dataset Source, batch size 4, four bounded diagnostics.
- Any Resource Failure retry, non-finite state, constant bounded predictions, missing artifact, or lifecycle inconsistency stops for review. This does not authorize the main Run or full evaluation.

## Gate 2 pilot attempt stopped for review (2026-08-11)
- Authorized Run `run_20260811_155607_5a9ea1` trained/validated exactly once on A100 device 0 with 64 train + 64 validation samples, batch 4, no retry, finite metrics, and a fully finite checkpoint. Peak allocated/reserved memory was 571,703,808 / 664,797,184 bytes; measured operation wall time 68.30s.
- The Run then failed before `final_metrics.json`/qualitative artifacts because ABI does not implement the requested Harness-owned `adjacent_and_scattered` prediction sample selector. It was incorrectly classified `candidate_bug`; Candidate source did not cause the trusted-policy incompatibility.
- Validation was non-degenerate in both sources: aggregate raw/filtered Dice 0.00838/0.00851; Google 0.00139/0.00139; MIT 0.01690/0.01756.
- Two reconciliations preserved exactly one `run_failed`; container cleanup completed; no duplicate/retry Run was launched.
- Per Gate 2 stop rules, no repair or second pilot was started. Recommended review decision: revise the pilot qualitative policy to supported provider/Harness-owned `first_n` and authorize one deliberate replacement pilot; retain this failed Run as evidence. AC 4 remains incomplete.
<!-- SECTION:NOTES:END -->

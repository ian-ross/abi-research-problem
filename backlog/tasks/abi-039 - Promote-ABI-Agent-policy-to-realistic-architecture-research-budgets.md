---
id: ABI-039
title: Promote ABI Agent policy to realistic architecture-research budgets
status: Done
assignee:
  - '@agent'
created_date: '2026-08-12 15:59'
updated_date: '2026-08-12 21:26'
labels:
  - harness
  - autonomy
  - policy
  - gpu
  - candidates
dependencies:
  - ABI-038
  - ABI-040
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Define, review, and activate a realistic trusted Agent/Harness policy envelope for genuine model architecture research, replacing the ABI-034 onboarding ceilings while retaining the established ownership, coordinate, lifecycle, resource, and human-review guardrails. The policy transition must be based on measured evidence and must stop before launching scientific Candidate Runs; real model execution belongs to a later task.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 A reviewed policy proposal selects justified ceilings for samples per Dataset Source, epochs, wall-clock timeout, parallel Runs, prediction artifacts, parameters, batch/resource classes, scheduler use, and early stopping
- [x] #2 The proposal distinguishes full-data Runs from representative reduced-budget scouts and uses the ABI-038 trusted sample-limiting semantics for capped Runs
- [x] #3 New or materially different architecture families remain sequential until separately profiled, and concurrency is enabled only for compatible measured resource classes
- [x] #4 The approved values are enforced by trusted Workspace Configuration and Harness validation; Candidate source and manifests cannot raise or bypass them
- [x] #5 Durable campaign authorization, Experiment Index, Research Ledger, provider brief/guidance, and generated Agent Control Boundary consistently expose the promoted policy and retained human stop conditions
- [x] #6 Runtime images and policy/config identity validate after the policy change, and focused ABI/Harness tests prove clamping, rejection, handoff, batch, and boundary behavior
- [x] #7 Preflight confirms configured data, ancillary, baseline, Runs, Docker, and pinned-A100 resources are available for a later calibration Run
- [x] #8 No scientific Candidate Run, Post-Run Evaluation, Experiment Batch, or Autonomy Step is launched by this task; the first calibrated real model Run requires a separate backlog task
- [x] #9 After ABI-040 is complete, the activated architecture-scout envelope allows a 32-sample-per-source, one-epoch resource pilot within trusted ceilings of 1,024 representative samples per Dataset Source and Leakage-Safe Split, 12 epochs, 3,600 seconds, batch size 4, four first_n predictions, 25,000,000 parameters, constant learning rate, disabled early stopping, and one sequential Run
- [x] #10 The promoted authorization uses asymmetric scout decisions: only hard failure, persistent collapse, clear optimization failure, or convincing plateau/divergence supports elimination at 12 epochs; low-scoring but improving, source-balanced, novel, or ambiguous trajectories remain eligible for separately authorized extension
- [x] #11 A roughly 36-epoch extended scout and full-data training up to 100 epochs with a provisionally eight-hour timeout are documented as later policy transitions but are not activated by ABI-039; each requires measured evidence and separate authorization
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Confirm ABI-038 is complete and read its approved capped-selection contract and validation evidence. Re-baseline the clean ABI/Harness revisions, current 128-sample/3-epoch policy, full mounted Dataset Source counts, canonical validation size, prior A100 resource profiles, accelerated-validation timings, timeout/recovery behavior, and latest finite/non-degenerate and collapsed Results.
2. Draft a policy decision table for two modes: representative reduced-budget architecture scouts using ABI-038 selection, and later full-data confirmation Runs. For each mode propose exact sample ceilings, epoch ceiling, wall-clock timeout, prediction-artifact bound, parameter ceiling, batch-size/resource-class rule, scheduler guidance, early-stopping guidance, and whether parallel Runs are permitted. Derive runtime/headroom estimates explicitly from measured evidence and identify assumptions.
3. Hold a human policy gate before changing configuration. Obtain approval for the exact values and retained stop conditions. Default new or materially different architecture families to sequential execution; retain `max_parallel_runs = 1` unless trusted enforcement can prove that every concurrent Candidate belongs to a compatible ABI-029-profiled resource class. Do not turn the measured concurrency-two result into an unrestricted global Agent allowance.
4. Audit trusted enforcement across direct/config-driven Candidate Runs, managed continuation/reconciliation, Agent handoff ingestion, Autonomy Steps, and Experiment Batches. Add only the smallest Harness changes needed to make approved ceilings clamp or reject consistently and to expose scheduler/early-stopping and resource-class guidance without transferring policy ownership to Candidate code.
5. Add or update focused Harness tests for configuration parsing/bounds, command-option clamping, manifest epoch rejection, timeout propagation, parameter and prediction limits, batch concurrency, handoff ingestion, generated boundary configuration/guidance, and no-bypass behavior. Add ABI workspace tests that assert the promoted local/example policy shape without making portable tests depend on machine-local paths or secrets.
6. Apply the approved values to the machine-local `ml-autoresearch.toml` and update `ml-autoresearch.toml.example` comments/guidance where portable. Preserve pinned A100 device 0, rootless Docker execution, read-only named data roots, the longitude/latitude prohibition, provider-owned data/loss/metric/filter/sampling policy, exactly-once reconciliation, and human stops for policy/contract changes, failures, promotion, and unbounded actions.
7. Write a durable policy-promotion campaign report containing the evidence, exact scout/full-data envelopes, enforcement semantics, resource-class/concurrency rules, stop conditions, and explicit statement that this task launches no scientific work. Update `EXPERIMENT_INDEX.md` and record the linked validated Research Ledger authorization/resume event only after human approval.
8. Rebuild runtime images only if the Harness, provider dependencies, image recipes, or validation identity require it; otherwise revalidate the existing images against the new Workspace Configuration. Run `prepare-agent-boundary` and inspect generated `agent-work/ml-autoresearch.toml`, `agent-work/AGENTS.md`, `/reference` snapshots, and ledger history to prove the Agent sees one consistent promoted policy and ABI-038 sampling semantics.
9. Perform non-training operational preflight: verify clean/pushed revision identities as required by the authorization, configured training/ancillary/baseline/Run roots, canonical baseline registry/assets, Docker runner, Agent image, pinned idle A100, no managed containers, no unresolved campaign pause/capability request, and no open Harness action that could execute unexpectedly. Use dry-run/status commands only.
10. Run focused ABI and Harness policy/boundary/handoff/batch tests followed by the full ABI suite and relevant Harness suite. Prove no Candidate Run, Post-Run Evaluation, Experiment Batch, or Autonomy Step was launched by comparing Run/Evaluation/ledger action counts before and after.
11. Record validation, residual risks, approved values, and the recommended scope for a separate first calibration-Run backlog task. Stop after policy activation and boundary verification; do not create or execute the real model Run within ABI-039.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Evidence audit: mounted snapshot has 25,457 train records (MIT 4,928; Google 20,529) and 3,088 validation records (MIT 1,232; Google 1,856).
- Accelerated ABI-037 bounded Run measured 73.88 train samples/s and 23.88 validation samples/s with 14.33M parameters, batch 4, ~958MB CUDA reserved, and 44.65s total for 3x(256 train + 256 val).
- ABI-029 approves batch 8/concurrency 2 only for comparable 2.54M spectral ResUNets; materially different architectures remain sequential.
- Current Harness clamps max_samples but does not clamp CLI max_prediction_samples and has no trusted workspace max_batch_size; these are likely minimal enforcement gaps.
- Subagent audit was unavailable because the local pi-subagents runtime is missing typebox/compile; continuing with direct repository inspection.

- Human policy-gate evidence: operator reports canonical MCAST 2.1 trained for 100 epochs in approximately 3.7 hours on this machine/A100. This invalidates the proposed 20-epoch full-data confirmation as likely under-training and motivates staged feasibility scouting followed by focused 100-epoch training only for promoted architectures.
- Proposed staged interpretation: non-ranking 1-epoch resource pilot; fixed-budget representative 12-epoch scout with no early stopping; later full-data focused training up to 100 epochs with scheduler/early stopping, separately calibrated and authorized.

- Policy refinement: a 12-epoch, 1,024-per-source scout sees 24,576 training observations, roughly 1% of the 2,545,700 record-exposures in a 100-epoch pass over the mounted 25,457-record training snapshot. It is therefore a failure/feasibility screen, not a reliable final architecture ranking.
- Proposed slow-starter protection: asymmetric successive-halving decisions. Reject at 12 epochs only for hard failure, collapse, or convincing plateau/divergence; extend low-scoring models with positive tail slope, stable finite optimization, source-balanced signal, or ambiguous/noisy trajectories to a longer scout. Do not use a strict top-k or absolute Dice cutoff.

- Agreed delivery sequence: ABI-040 implements Harness enforcement, ABI provider feasibility evidence, and Agent-visible staged-scout guidance without activating policy. ABI-039 then activates and validates the exact resource-pilot/12-epoch scout envelope, updates authorization/index/ledger, performs non-training preflight, and closes. ABI-041 follows with trusted checkpoint continuation.
- Point-4 activation factors recorded as ACs: 32/source x 1 resource pilot request; active 1,024/source-split x 12 scout ceiling; 3,600s; batch <=4; four first_n artifacts; 25M parameters; constant LR; early stopping disabled; global concurrency one. The 36-epoch and full-data 100-epoch/eight-hour stages remain inactive and separately gated.

- Activated the approved ABI-039 trusted scout envelope: 1,024 samples per source/split, 12 epochs, 3,600s, batch 4, four first_n predictions, 25M parameters, constant LR, disabled early stopping, concurrency one; resource pilot remains 32/source/split x one epoch.
- Rebuilt and validated runtime images against clean Harness c346f07; regenerated and inspected the Agent Control Boundary and linked authorization/index/ledger state.
- Non-training preflight passed for data, ancillary, baselines, Runs, rootless Docker, pinned idle A100, no containers, no pause, and no open Harness action.
- Validation: ABI 133 passed; focused Harness 186 passed; full configured Harness 581 passed/2 skipped/1 known unrelated GVCCS fake-allowlist failure. No Run, Evaluation, Batch, handoff, or Autonomy action count changed.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Activated and validated the trusted ABI architecture-scout envelope. Workspace and Agent-visible policy now enforce 1,024 representative samples per Dataset Source and Leakage-Safe Split, 12 epochs, 3,600 seconds, batch size 4, four first_n predictions, 25M parameters, constant LR, disabled early stopping, and one sequential Run. Added the durable ABI-039 campaign authorization, updated the Experiment Index and Research Ledger, rebuilt runtime images for Harness c346f07, regenerated the Agent Control Boundary, and completed non-training operational preflight. The 32/source/split one-epoch resource pilot is the next separately authorized execution; 36-epoch extension and 100-epoch full-data stages remain inactive.

Validation:
- uv run pytest -q: 133 passed
- Focused Harness policy/boundary/handoff/batch suites: 186 passed
- Full configured Harness: 581 passed, 2 skipped, 1 known unrelated GVCCS fake-allowlist failure
- Runtime image, Docker CUDA/A100, boundary reload/snapshot, dry-run open-action, and git diff checks passed
- No Candidate Run, Evaluation, Experiment Batch, handoff, or Autonomy Step was launched; only authorization/report ledger events were added
- Activation commit 7d2cd27 pushed to origin/main
<!-- SECTION:FINAL_SUMMARY:END -->

---
id: ABI-040
title: Enforce staged ABI scout policy and expose trusted feasibility evidence
status: In Progress
assignee:
  - '@agent'
created_date: '2026-08-12 20:27'
updated_date: '2026-08-12 21:02'
labels:
  - harness
  - provider
  - policy
  - agent-boundary
  - tests
dependencies:
  - ABI-038
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement the trusted Harness, ABI provider, and Agent-visible capabilities required for the promoted architecture-feasibility workflow before ABI-039 activates new workspace ceilings. Close policy bypasses, add conservative learning-curve/non-degeneracy evidence, and teach the Agent the staged resource-pilot and scout protocol. This task changes code, tests, and durable guidance only; it does not launch a scientific Candidate Run, Post-Run Evaluation, Experiment Batch, or Autonomy Step, and it does not activate the promoted machine-local policy.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Trusted Workspace Configuration supports a maximum Candidate batch size and enforceable scheduler/early-stopping constraints without transferring policy ownership to Candidate code
- [x] #2 Direct and config-driven Candidate Runs, managed continuation/reconciliation, Agent handoff ingestion, Autonomy Steps, and Experiment Batches consistently enforce sample, epoch, timeout, parameter, batch, prediction-artifact, prediction-policy, scheduler, early-stopping, and parallel-Run ceilings
- [x] #3 Command options cannot raise the configured prediction-artifact ceiling or substitute a disallowed prediction policy, and focused tests prove clamping or rejection alongside the existing sample and epoch behavior
- [x] #4 Generated Agent Workspace configuration and AGENTS.md expose the effective sample, epoch, timeout, parameter, batch, prediction, scheduler, early-stopping, and concurrency policy consistently
- [x] #5 Trusted ABI epoch-validation evidence records bounded raw and filtered predicted-positive counts or fractions together with aggregate and MIT/Google metrics needed to identify collapse and improvement
- [x] #6 A provider-owned scout assessment summarizes finite/resource state, recent loss and metric trends, source-specific behavior, and prediction degeneracy without using a strict top-k or single absolute-Dice elimination rule; ambiguous or improving low-scoring curves remain extension-eligible
- [x] #7 The Research Problem Brief and Agent-visible guidance define the one-epoch resource pilot, representative ABI-038 scout semantics, asymmetric elimination rule, sequential treatment of new architecture families, and the distinction between scout evidence and focused full-data evidence
- [x] #8 Focused Harness and ABI tests cover configuration bounds, direct and handoff no-bypass paths, batches, generated boundary content, positive-count evidence, curve assessment, slow-starter/ambiguous trajectories, and hard-failure/collapse trajectories
- [x] #9 No promoted machine-local policy is activated and no scientific execution action is launched by this task; activation remains in ABI-039
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Audit trusted Harness and ABI provider policy paths and their focused tests, including dependency ABI-038 outputs
2. Add trusted batch, scheduler, and early-stopping limits and enforce all configured ceilings across direct, handoff, continuation, autonomy, and batch execution
3. Update generated Agent boundary configuration and durable scout/resource-pilot guidance
4. Add bounded predicted-positive validation evidence and a conservative provider-owned scout assessment
5. Add focused Harness and ABI tests for policy enforcement, boundary content, and scout trajectories
6. Run targeted uv-managed test suites, verify no policy activation or scientific execution occurred, and update ABI-040 completion metadata
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Initial code audit for the next session:
  - `../ml-autoresearch/src/ml_autoresearch/candidate_execution_config.py` has `max_samples`, `max_parameters`, `max_epochs`, timeout, prediction, and concurrency fields, but no trusted `max_batch_size` or scheduler/early-stopping constraint fields.
  - `../ml-autoresearch/src/ml_autoresearch/research_loop_operations.py::effective_execution_options` clamps `max_samples` but currently lets CLI `max_prediction_samples` exceed config and lets an explicit prediction policy replace config. Config-driven handoff/batch paths already pass configured values directly.
  - `../ml-autoresearch/src/ml_autoresearch/candidates.py` has a generic batch-size range 1..32 and trusted scheduler allowlist (`constant_lr`, `cosine_decay`, `reduce_on_plateau`) plus early-stopping schema, but validation currently has no Workspace-specific batch/scheduler/early-stop policy argument.
  - `../ml-autoresearch/src/ml_autoresearch/agent_boundary.py` generates sample/epoch/parameter/prediction/concurrency config and prose, but needs the new batch and training-policy fields consistently exposed.
  - ABI `outputs/metrics.jsonl` already records per-epoch train loss, learning rate, aggregate raw/filtered metrics, and MIT/Google raw/filtered metrics. Add bounded predicted-positive count/fraction evidence; do not duplicate the existing curve history.
  - Representative tests are `test_candidate_execution_config.py`, `test_research_loop_operations.py`, `test_agent_boundary.py`, `test_agent_handoff_ingestion.py`, `test_autonomy_step.py`, `test_experiment_batches.py`, plus ABI training/provider tests.
  - The local pi-subagents context-builder could not run because its installation lacks `typebox/compile`; direct audit findings above replace that attempted handoff.
- Approved design intent: the provider-owned scout assessment is conservative decision support, not an automatic top-k ranker. Strong negative evidence is required for elimination; low but improving, source-balanced, novel, noisy, or ambiguous trajectories remain extension-eligible.

- Added Harness-owned max batch size, scheduler allowlist, and early-stopping policy with manifest validation across direct, managed, handoff, autonomy, and batch paths.
- Clamped prediction artifact requests and rejected prediction-policy substitution before Run creation.
- Extended generated Agent Workspace config/instructions with the full effective policy and staged scout guidance.
- Added bounded aggregate/source predicted-positive evidence and provider-owned conservative scout assessment artifacts.
- Updated the ABI brief with resource-pilot, representative scout, asymmetric elimination, sequential-family, extension, and full-data semantics.
- Verified machine-local promoted ceilings were not changed and launched no scientific execution action.
- Validation: ABI full suite 133 passed; focused Harness policy/boundary suites 186 passed; full Harness 581 passed, 2 skipped, with one known unrelated external GVCCS fake-allowlist failure; compileall and git diff checks passed. Ruff is not installed in either uv environment.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented staged ABI scout policy enforcement and trusted feasibility evidence across the reusable Harness and ABI provider.

Harness:
- Added Workspace max batch size, scheduler allowlist, and early-stopping constraints.
- Enforced training policy across direct Runs, stable continuation/reconciliation, Agent handoffs, Autonomy Steps, and Experiment Batches.
- Clamped prediction artifact requests, rejected policy substitution, and exposed the complete policy in generated boundary config/guidance.

ABI provider:
- Added aggregate and MIT/Google raw/filtered predicted-positive counts and fractions to epoch evidence.
- Added conservative finite/resource, trend, source, and prediction-degeneracy scout assessment with no top-k or absolute-Dice elimination rule.
- Documented staged pilot/scout/extension/full-data semantics and asymmetric elimination.

Validation:
- uv run pytest -q: 133 passed (ABI)
- Focused Harness suites: 186 passed
- Full Harness: 581 passed, 2 skipped, 1 known unrelated external GVCCS characterization failure
- compileall and git diff --check passed
- Ruff unavailable in the project environments

No promoted machine-local policy was activated and no scientific execution action was launched.
<!-- SECTION:FINAL_SUMMARY:END -->

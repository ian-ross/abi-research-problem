---
id: ABI-040
title: Enforce staged ABI scout policy and expose trusted feasibility evidence
status: To Do
assignee: []
created_date: '2026-08-12 20:27'
updated_date: '2026-08-12 20:31'
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
- [ ] #1 Trusted Workspace Configuration supports a maximum Candidate batch size and enforceable scheduler/early-stopping constraints without transferring policy ownership to Candidate code
- [ ] #2 Direct and config-driven Candidate Runs, managed continuation/reconciliation, Agent handoff ingestion, Autonomy Steps, and Experiment Batches consistently enforce sample, epoch, timeout, parameter, batch, prediction-artifact, prediction-policy, scheduler, early-stopping, and parallel-Run ceilings
- [ ] #3 Command options cannot raise the configured prediction-artifact ceiling or substitute a disallowed prediction policy, and focused tests prove clamping or rejection alongside the existing sample and epoch behavior
- [ ] #4 Generated Agent Workspace configuration and AGENTS.md expose the effective sample, epoch, timeout, parameter, batch, prediction, scheduler, early-stopping, and concurrency policy consistently
- [ ] #5 Trusted ABI epoch-validation evidence records bounded raw and filtered predicted-positive counts or fractions together with aggregate and MIT/Google metrics needed to identify collapse and improvement
- [ ] #6 A provider-owned scout assessment summarizes finite/resource state, recent loss and metric trends, source-specific behavior, and prediction degeneracy without using a strict top-k or single absolute-Dice elimination rule; ambiguous or improving low-scoring curves remain extension-eligible
- [ ] #7 The Research Problem Brief and Agent-visible guidance define the one-epoch resource pilot, representative ABI-038 scout semantics, asymmetric elimination rule, sequential treatment of new architecture families, and the distinction between scout evidence and focused full-data evidence
- [ ] #8 Focused Harness and ABI tests cover configuration bounds, direct and handoff no-bypass paths, batches, generated boundary content, positive-count evidence, curve assessment, slow-starter/ambiguous trajectories, and hard-failure/collapse trajectories
- [ ] #9 No promoted machine-local policy is activated and no scientific execution action is launched by this task; activation remains in ABI-039
<!-- AC:END -->

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
<!-- SECTION:NOTES:END -->

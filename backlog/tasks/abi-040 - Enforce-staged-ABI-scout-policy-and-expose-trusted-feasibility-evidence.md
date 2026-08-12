---
id: ABI-040
title: Enforce staged ABI scout policy and expose trusted feasibility evidence
status: To Do
assignee: []
created_date: '2026-08-12 20:27'
updated_date: '2026-08-12 20:27'
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

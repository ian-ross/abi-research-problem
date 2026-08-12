---
id: ABI-039
title: Promote ABI Agent policy to realistic architecture-research budgets
status: To Do
assignee: []
created_date: '2026-08-12 15:59'
labels:
  - harness
  - autonomy
  - policy
  - gpu
  - candidates
dependencies:
  - ABI-038
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Define, review, and activate a realistic trusted Agent/Harness policy envelope for genuine model architecture research, replacing the ABI-034 onboarding ceilings while retaining the established ownership, coordinate, lifecycle, resource, and human-review guardrails. The policy transition must be based on measured evidence and must stop before launching scientific Candidate Runs; real model execution belongs to a later task.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A reviewed policy proposal selects justified ceilings for samples per Dataset Source, epochs, wall-clock timeout, parallel Runs, prediction artifacts, parameters, batch/resource classes, scheduler use, and early stopping
- [ ] #2 The proposal distinguishes full-data Runs from representative reduced-budget scouts and uses the ABI-038 trusted sample-limiting semantics for capped Runs
- [ ] #3 New or materially different architecture families remain sequential until separately profiled, and concurrency is enabled only for compatible measured resource classes
- [ ] #4 The approved values are enforced by trusted Workspace Configuration and Harness validation; Candidate source and manifests cannot raise or bypass them
- [ ] #5 Durable campaign authorization, Experiment Index, Research Ledger, provider brief/guidance, and generated Agent Control Boundary consistently expose the promoted policy and retained human stop conditions
- [ ] #6 Runtime images and policy/config identity validate after the policy change, and focused ABI/Harness tests prove clamping, rejection, handoff, batch, and boundary behavior
- [ ] #7 Preflight confirms configured data, ancillary, baseline, Runs, Docker, and pinned-A100 resources are available for a later calibration Run
- [ ] #8 No scientific Candidate Run, Post-Run Evaluation, Experiment Batch, or Autonomy Step is launched by this task; the first calibrated real model Run requires a separate backlog task
<!-- AC:END -->

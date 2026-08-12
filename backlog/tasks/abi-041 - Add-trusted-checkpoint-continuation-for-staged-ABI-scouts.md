---
id: ABI-041
title: Add trusted checkpoint continuation for staged ABI scouts
status: To Do
assignee: []
created_date: '2026-08-12 20:27'
labels:
  - harness
  - provider
  - training
  - lifecycle
  - follow-up
dependencies:
  - ABI-039
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement efficient trusted continuation from a completed short architecture scout into a longer scout without Candidate-owned checkpoint loading. Preserve immutable lineage, optimizer/scheduler/training state, policy enforcement, and exactly-once lifecycle semantics so later successive-halving workflows do not need to restart promising architectures from scratch. This work follows ABI-039 policy activation and is not part of the initial promoted scout rollout.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The Harness can create or execute an explicitly authorized continuation linked to one eligible completed parent Run and the exact trusted checkpoint selected from that Run
- [ ] #2 Continuation restores model, optimizer, scheduler, completed-epoch, early-stopping, and required reproducibility state through trusted code; Candidate source cannot choose an arbitrary checkpoint path, deserialize state, or bypass the training boundary
- [ ] #3 Candidate source identity, Research Problem contract, input-coordinate exclusions, data policy and ABI-038 selected-record identity, trusted loss/metric/filter policy, and compatible resource class are validated before continuation
- [ ] #4 Workspace sample, cumulative epoch, batch, parameter, timeout, prediction, concurrency, and scheduler/early-stopping ceilings remain enforced for direct, handoff, and autonomy continuation paths
- [ ] #5 Continuation has a stable identity and durable parent/child provenance, records cumulative and incremental budgets, and preserves exactly-once submission, observation, reconciliation, failure, and timeout behavior
- [ ] #6 Tests prove faithful checkpoint/state restoration, policy rejection, incompatible-lineage rejection, caller interruption and reconciliation, no duplicate continuation, and no Candidate checkpoint access using tiny fixtures
- [ ] #7 Agent-visible guidance explains when continuation is permitted and requires a fresh human/policy gate for focused full-data training or any unbounded transition
- [ ] #8 No real ABI model training is performed while implementing this capability
<!-- AC:END -->

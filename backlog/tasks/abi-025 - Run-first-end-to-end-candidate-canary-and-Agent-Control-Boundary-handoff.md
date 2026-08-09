---
id: ABI-025
title: Run first end-to-end candidate canary and Agent Control Boundary handoff
status: To Do
assignee: []
created_date: '2026-08-09 21:13'
labels:
  - harness
  - candidates
  - agent-boundary
  - canary
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Prove the complete ABI Candidate Experiment lifecycle after the canonical MCAST baselines are available. First isolate the trusted Candidate Execution path with a manually authored, bounded canary Candidate Experiment; then exercise Agent Control Boundary generation, handoff ingestion, and separately approved execution.

This task is deliberately staged with explicit Human Review Gates. Agent steps must stop at each gate and must not proceed until the human approves the next step. Real training must run only on the approved GPU/cluster environment, never as an unapproved local run.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A manually authored canary Candidate Experiment has a reviewed PROPOSAL.md and valid candidate contract without candidate-owned data loading, losses, metrics, filters, sampling, or augmentation
- [ ] #2 Static validation and a human-approved bounded Docker training/evaluation run succeed on the GPU/cluster environment
- [ ] #3 The canary Run produces expected Run artifacts, Research Ledger/index records, provider-owned metrics, and an acceptance report tied to the canonical MCAST registry
- [ ] #4 Validation confirms longitude and latitude are not Candidate Experiment inputs and trusted data/baseline/ancillary mounts remain read-only and boundary-owned
- [ ] #5 One Agent Control Boundary autonomy step is run without automatic next-action execution, and its single handoff is inspected and approved before any candidate execution
- [ ] #6 The approved Agent-generated handoff is executed separately and its Run artifacts and acceptance report are validated
- [ ] #7 A final human go/no-go decision is recorded before enabling or attempting a fully automatic autonomy iteration
<!-- AC:END -->

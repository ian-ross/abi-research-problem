---
id: ABI-029
title: >-
  Characterize ABI candidate GPU memory, batch size, and Experiment Batch
  concurrency
status: In Progress
assignee:
  - '@agent'
created_date: '2026-08-10 19:07'
updated_date: '2026-08-10 19:07'
labels:
  - harness
  - candidates
  - gpu
  - experiment-batches
  - agent-boundary
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Measure representative ABI Candidate training memory and throughput on the approved GPU environment, derive safe batch-size and per-GPU concurrency guidance, and expose trusted limits to the Agent Control Boundary so the agent can submit small Experiment Batches when parallel execution is safe and scientifically appropriate.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A reviewed, bounded profiling protocol defines representative candidate size classes, batch sizes, sample/epoch caps, GPU environment metadata, measurements, and explicit human execution gates
- [ ] #2 Approved GPU profiling records peak allocated and reserved memory, throughput, runtime, and OOM/resource-retry behavior for representative ABI Candidate training configurations
- [ ] #3 A conservative batch-size and simultaneous-candidate recommendation is derived per model size class with explicit GPU-memory headroom and assumptions
- [ ] #4 Harness-owned Experiment Batch concurrency is configured or capped from measured evidence and validated with a bounded batch canary without allowing candidate-owned execution policy
- [ ] #5 Trusted Agent-visible campaign guidance explains when to prefer an Experiment Batch, its candidate/count/concurrency limits, and when sequential submissions are required
- [ ] #6 Durable profiling results, commands, artifacts, and residual risks are recorded without making tests or runtime behavior depend on planning-inputs or local-only data
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Inspect current Harness batch execution, resource limits, retry behavior, and available GPU-memory instrumentation; define representative ABI model size classes.
2. Propose an exact bounded profiling matrix (GPU identity, batch sizes, sample/epoch limits, measurements, stop conditions, and commands) without running training.
3. Human Review/Execution Gate: approve the profiling matrix and launch location before any GPU training.
4. Add only the trusted Harness/provider instrumentation and tiny fixture tests needed to capture comparable peak memory, throughput, and resource-failure evidence.
5. Run the approved bounded profiling matrix on the GPU environment and derive conservative batch-size and per-GPU concurrency recommendations with headroom.
6. Configure or cap Harness-owned Experiment Batch concurrency from the evidence and expose concise trusted guidance to the Agent Control Boundary.
7. Human Review/Execution Gate: approve and run one bounded Experiment Batch canary; validate concurrency enforcement, artifact isolation, and independent failure handling.
8. Record durable results, tests, commands, assumptions, and residual risks; update acceptance criteria and final summary.
<!-- SECTION:PLAN:END -->

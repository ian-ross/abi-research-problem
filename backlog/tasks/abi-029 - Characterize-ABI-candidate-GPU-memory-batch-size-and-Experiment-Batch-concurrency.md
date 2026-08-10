---
id: ABI-029
title: >-
  Characterize ABI candidate GPU memory, batch size, and Experiment Batch
  concurrency
status: In Progress
assignee:
  - '@agent'
created_date: '2026-08-10 19:07'
updated_date: '2026-08-10 19:44'
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
- [x] #1 A reviewed, bounded profiling protocol defines representative candidate size classes, batch sizes, sample/epoch caps, GPU environment metadata, measurements, and explicit human execution gates
- [ ] #2 Approved GPU profiling records peak allocated and reserved memory, throughput, runtime, and OOM/resource-retry behavior for representative ABI Candidate training configurations
- [ ] #3 A conservative batch-size and simultaneous-candidate recommendation is derived per model size class with explicit GPU-memory headroom and assumptions
- [ ] #4 Harness-owned Experiment Batch concurrency is configured or capped from measured evidence and validated with a bounded batch canary without allowing candidate-owned execution policy
- [x] #5 Trusted Agent-visible campaign guidance explains when to prefer an Experiment Batch, its candidate/count/concurrency limits, and when sequential submissions are required
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

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Initial non-training preflight: host exposes NVIDIA A100-PCIE-40GB (40,960 MiB) as GPU 0 and Tesla T4 (15,360 MiB) as GPU 1; no compute processes were active. Runner image sees both GPUs.
- Current DockerBackend uses `--gpus all`, while training selects unqualified `cuda`, so every Run uses container GPU 0. Concurrent Experiment Batch workers therefore pile onto the A100; the T4 is not scheduled.
- Ingested Experiment Batch execution hardcodes `max_parallel_runs=4`, and CandidateExecutionConfig has no batch-concurrency or GPU-device policy. Existing training artifacts record only device type, not CUDA device identity, peak allocated/reserved memory, throughput, or timing.
- Agent Workspace exposes `batch-submissions/` and batch history, but the one-step autonomy prompt omits Experiment Batch Submission from its allowed primary outcomes and no dedicated batch-authoring skill/guidance is present.
- Until ABI-029 establishes measured policy, do not approve autonomous parallel Candidate execution. Proposed profiling should begin with synthetic backward/resource probes and bounded one-epoch real-data confirmation, then test concurrency 2 before considering higher values; retain explicit human GPU gates.

- Human approved the ABI-029 implementation plan. Added durable reviewed protocol `docs/abi-gpu-resource-profiling.md` with A100/T4 environment metadata, batch sizes 1/2/4/8/16, one epoch, 32 samples per Dataset Source, 70% plus 8 GiB headroom rules, stop-on-OOM behavior, concurrency-2 gate, and explicit real-data/concurrency human gates.
- Harness commit `2eec8fa` adds trusted `training_resource_profile.v1` artifacts for successful and failed attempts (device identity, CUDA peak allocated/reserved bytes, timing, throughput, failure reason), single-GPU Docker pinning, conservative configurable `max_parallel_runs` default 1 for ingested batches, Agent-visible batch policy, autonomy prompt batch handoff support, and an `experiment-batch-writer` skill. Harness focused tests passed; full suite reached 525 passed/2 skipped with 3 unrelated external GVCCS/test-provider failures. ABI full suite passed 102 tests.
- ABI execution config now pins Docker to GPU 0 (A100), keeps `max_parallel_runs=1`, and retains the approved `max_samples=1024` ABI-025 bound. Rebuilt and validated runner `ml-autoresearch-runner:abi-research-problem-4ea195c26918b493-13b99524f1` against clean Harness commit `2eec8fa`; refreshed Agent Boundary shows the cap and batch guidance.
- Lightweight synthetic-only GPU instrumentation smoke completed on the pinned A100: peak allocated 3,811,328 bytes, peak reserved 25,165,824 bytes, 8 training/4 validation samples, and CUDA device identity were persisted. This validates instrumentation only and is not representative scientific-model concurrency evidence.
- Added `scripts/prepare_abi029_gpu_profiles.py` plus a unit test. Prepared and statically validated temporary one-epoch profiling derivatives for batch sizes 1/2/4/8/16; all model.py hashes match the approved scout (`257b9e9a...`). No ABI real-data profiling, ABI-025 Gate 6 Run, or Experiment Batch canary has started.
<!-- SECTION:NOTES:END -->

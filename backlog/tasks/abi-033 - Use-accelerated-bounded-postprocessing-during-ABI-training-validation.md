---
id: ABI-033
title: Use accelerated bounded postprocessing during ABI training validation
status: In Progress
assignee:
  - '@agent'
created_date: '2026-08-11 17:08'
updated_date: '2026-08-11 19:54'
labels:
  - provider
  - harness
  - performance
  - training
dependencies:
  - ABI-031
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
ABI-031 exposed that epoch validation still calls ABITrainingAdapter.compute_validation_metrics_from_dataset, moves all logits to CPU, and applies Artifact Filters one sample at a time. The existing ABI-022 BoundedBatchPostprocessor CUDA path is used by Post-Run Evaluation but not training-time validation, causing approximately 45-minute CPU-only pauses for 2,048 validation samples with no progress output. Integrate the trusted accelerated path without changing Candidate ownership or metric semantics.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Training-time ABI validation routes Artifact Filters and aggregate/source-stratified metrics through the existing bounded-batch postprocessing abstraction on the Harness-selected device; Candidate code cannot select or own this behavior
- [ ] #2 CPU and CUDA implementations preserve numerical parity with the current trusted raw/filtered metrics and ordered Geographic Feature then Scanline Artifact Filter behavior on representative fixtures
- [ ] #3 Validation emits phase and bounded progress/timing evidence sufficient to distinguish inference, context preparation, filtering, ordinary metrics, and connectivity work without per-sample log spam
- [ ] #4 The implementation preserves bounded device memory and records the selected postprocessing backend, device batch size, and timings in Run artifacts/resource evidence
- [ ] #5 Unit/integration tests cover training-adapter integration, source-stratified metrics, finite-state behavior, and CPU fallback; any real-data GPU benchmark remains separately human-gated
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Capture the ABI-031 performance evidence and add a deterministic failing integration test at the generic training/ABI-adapter seam: validation must invoke a device-aware bounded postprocessor, expose live bounded phase progress, and retain a structured per-epoch report.
2. Extend the trusted Harness training-adapter contract with a backward-compatible optional validation-result hook carrying the Harness-selected device and progress callback; preserve existing providers through the current dict-returning fallback. Persist structured postprocessing backend, batch size, progress/timings, and bounded-memory evidence in Run outputs without exposing policy to Candidate code.
3. Refactor shared ABI postprocessing aggregation so training and Post-Run Evaluation consume the same BoundedBatchPostprocessor outputs for raw/filtered aggregate metrics, Contrail Connectivity, and MIT/Google source strata. Replace the training adapter's per-sample NumPy Artifact Filter loop with bounded CPU/CUDA batches using trusted `postprocessing_batch_size`.
4. Add live, rate-bounded training validation messages for inference completion, context preparation, Artifact Filters, ordinary metrics, and connectivity; ensure final logs remain complete on success/failure and contain no per-sample spam.
5. Add CPU/reference parity, source-stratified parity, CUDA/CPU-fallback, finite-state, progress/reporting, and memory-bounding tests. First run focused Harness/provider suites, then full ABI and Harness suites; perform no real-data or GPU benchmark without a separate human execution gate.
6. Record measured fixture behavior, validation commands, residual risks, and any separately proposed real-data benchmark. Mark Done only when all ACs and durable task evidence are complete.
<!-- SECTION:PLAN:END -->

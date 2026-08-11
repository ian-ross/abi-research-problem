---
id: ABI-033
title: Use accelerated bounded postprocessing during ABI training validation
status: To Do
assignee: []
created_date: '2026-08-11 17:08'
labels:
  - provider
  - harness
  - performance
  - training
dependencies: []
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

# ABI-033 accelerated training validation

## Problem

ABI-031 Run `run_20260811_160920_07a7f4` exposed that epoch validation still moved accumulated logits to CPU and called the ABI Artifact Filter pipeline one sample at a time. Three validation passes consumed 7,995.87 of 8,047.34 measured seconds (0.768 samples/s), while training consumed 49.21 seconds. The operator observed about 3% GPU consumption. The accelerated ABI-022 postprocessor was already used for Post-Run Evaluation but not training-time validation.

## Implementation

Harness commit `401f9f7` adds an optional `ResearchProblemValidationResult` capability without changing the required training-adapter contract. Enhanced trusted adapters receive the Harness-selected device and a live progress callback. The Harness:

- preserves legacy adapter fallbacks;
- emits and flushes bounded inference/postprocessing progress to `training.log`;
- writes atomic per-epoch reports plus `outputs/validation_postprocessing/index.json`;
- fails closed on non-finite report or aggregate values before checkpointing;
- validates terminal report paths, schemas, epoch linkage, required backend/batch/bounded-memory/timing evidence, and finite values.

ABI commit `3e6d0f4` routes training validation through `BoundedBatchPostprocessor` using trusted `data_config.postprocessing_batch_size` (default 8). Full validation tensors remain on CPU; only bounded batches move to the Harness-selected CPU/CUDA device. Training and Post-Run Evaluation now share operational metric aggregation, preserving raw/filtered ordinary metrics, Contrail Connectivity, MIT/Google source strata, and Geographic Feature then Scanline Artifact Filter order. Candidate code cannot select the device, batch policy, filters, metrics, or report behavior.

The rebuilt validated runner is `ml-autoresearch-runner:abi-research-problem-c9e1b76b2a52c22c-13b99524f1`, derived from clean Harness commit `401f9f7a599e93b4c250ca66eaa345102e999078`.

## Validation

- ABI full suite: 114 passed.
- Harness full suite with `ML_AUTORESEARCH_TEST_PROBLEM_ROOT=/home/iross/code/test-research-problem`: 565 passed, 2 skipped, 1 known unrelated GVCCS characterization failure (`focal_bce_dice` versus its stale fake Spec allowlist).
- Focused Harness lifecycle/non-finite/reconciliation suites: 43 passed.
- Runtime image build and identity validation passed.
- Isolated no-data/no-GPU Docker check exercised the installed enhanced ABI adapter: `torch_cpu`, configured/max batch 1, all metrics finite, and 24 source-stratified keys.

Tests cover legacy fallback, exact Harness-selected device delivery, live log visibility, atomic multi-epoch evidence, terminal evidence validation, non-finite failure ordering, CPU fallback, CPU/reference metric parity, CUDA parity, source stratification, order-sensitive Geographic-then-Scanline behavior, and progress threshold crossings when batch size does not divide the log interval.

## Decision and residual risk

The implementation is complete without a real-data or real-shape GPU benchmark. Structural and fixture evidence proves bounded device batches, but does not measure production-shape CUDA peak allocation or end-to-end throughput. Any real-data benchmark remains separately human-gated. Until such a benchmark exists, ABI-031's legacy 0.768 samples/s is the comparison baseline rather than a claimed speedup.

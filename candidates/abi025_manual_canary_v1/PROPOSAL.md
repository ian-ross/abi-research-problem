# ABI-025 Manual Candidate Execution Canary

## Hypothesis

A deliberately small, architecture-only Candidate Experiment using the existing `abi_16ch` contract can prove the trusted Candidate Execution lifecycle end to end without introducing scientific or boundary complexity. The canary is intended to test validation, bounded training, artifact production, evaluation, provenance, and review—not to outperform a Baseline Segmenter.

## Comparison Target

The acceptance report will compare the candidate with canonical MCAST 1.1 and MCAST 2.1 targets from registry `abi-mcast-working-validation-v1`, configured at `canonical/mcast-working-validation-v1.json` beneath the trusted `baselines` data root. Both raw and provider-Artifact-Filtered metrics will be inspected.

## Expected Effect

The model should import, smoke-test, train for one bounded epoch, emit mask logits with the required shape, and produce all expected Run and Post-Run Evaluation artifacts. Its segmentation quality may be poor; acceptance-gate failures caused only by model quality do not invalidate the lifecycle canary.

## Implementation Sketch

Use an approximately 1,169-parameter fully convolutional model: a 3x3 convolution from 16 ABI channels to 8 learned features, ReLU, and a 1x1 convolution to one mask-logit channel. Candidate code contains only model architecture and the required `build_model(input_spec, output_spec)` entry point.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation`
- Input mode: `abi_16ch`
- Output form: `mask_logits`
- Provider-owned sequential sampling and no augmentation
- Provider-owned `bce_dice` loss
- Harness-owned AdamW optimizer
- No auxiliary targets, custom losses, metrics, filters, data loading, sampling implementation, augmentation implementation, pretrained weights, or runtime downloads
- Longitude and latitude are forbidden and are not model inputs

## Budget Requested

- Docker Candidate Execution Boundary with GPU enabled and network disabled
- One epoch, batch size 2, learning rate 0.001
- Harness `--max-samples 8`, which bounds each Dataset Source to 8 training and 8 validation samples (16 combined for each split)
- At most two training-run prediction samples
- One full 3,088-sample Working Validation Split Post-Run Evaluation for canonical comparability
- At most four Post-Run Evaluation diagnostic samples
- Existing Docker limits: 4 GiB memory, 2 CPUs, 512 processes, 2 GiB scratch tmpfs, and 2 GiB shared memory

## Success Criteria

1. Candidate static validation and controlled smoke testing succeed.
2. The bounded Run completes and writes expected Harness artifacts and Research Ledger events.
3. Full Post-Run Evaluation writes provider-owned raw, filtered, source-stratified, connectivity, threshold, and bounded diagnostic artifacts.
4. The acceptance report names the canonical registry and remains explicitly human-reviewed.
5. Run evidence confirms ABI channels 1-16 are the only candidate inputs and trusted data roots are boundary-owned and read-only.

## Fallback Next Decision

If validation or execution fails, stop and classify the failure before any retry. Repair only a demonstrated candidate contract or architecture defect with explicit lineage. Treat data, mount, registry, artifact, or Harness failures as trusted-boundary issues rather than weakening the Candidate Experiment contract. Do not proceed to the Agent Control Boundary phase until the manual lifecycle evidence is reviewed and approved.

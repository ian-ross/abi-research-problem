# ABI-215 temporal access canary

## Hypothesis

A minimal architecture-only Candidate Experiment using `abi_16ch_plus_sza_temporal` with frame offsets `[-1, 0, 1]` can verify that bounded Candidate Execution correctly filters to Temporal-Eligible Center ABI Patches, opens the trusted temporal cache, materializes the -1 and +1 frame patches, stacks frames in provider order, and supplies the resulting tensor to candidate code without exposing forbidden coordinate channels.

## Comparison Target

This is a diagnostic canary rather than a scientific contender. The relevant comparison is with the Candidate Execution contract: ABI-025 proved the single-frame lifecycle, while ABI-215 is intended to prove the temporal-input lifecycle. Segmentation metrics may be poor and should not be used as architecture-ranking evidence.

## Expected Effect

If the trusted temporal cache and patch files are present and current for the configured dataset snapshot, the candidate should validate, smoke-test, train for one bounded epoch, and emit finite `mask_logits`. If the temporal cache is missing, stale, subset-disallowed, or missing an extracted non-zero patch, the provider should fail closed before or during data access.

## Implementation Sketch

Use a tiny fully convolutional model. The front end reshapes the 51-channel temporal tensor into three 17-channel frames, normalizes ABI channels and Solar Geometry Input per frame, concatenates the previous frame, center frame, next frame, temporal mean, and simple finite-difference planes, and passes them through 3x3/3x3/1x1 convolutions to one mask-logit channel. This forces the forward path to consume all three provider-supplied frames while leaving temporal discovery and patch extraction entirely provider-owned.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation`
- Input mode: `abi_16ch_plus_sza_temporal`
- Temporal frame offsets: `[-1, 0, 1]`
- Frame selection policy: `temporal_eligible_center`
- Output form: `mask_logits`
- Provider-owned sequential sampling and no augmentation
- Provider-owned `bce_dice` loss
- Harness-owned AdamW optimizer and constant learning-rate scheduler
- No auxiliary targets, custom losses, metrics, filters, data loading, temporal sampling, augmentation implementation, pretrained weights, or runtime downloads
- Longitude and latitude are forbidden and are not model inputs

## Budget Requested

- One bounded epoch, batch size 2, learning rate 0.001
- Normal Candidate Execution Boundary with network disabled
- Use the active Harness caps for samples, predictions, GPU, timeout, and lifecycle management

## Success Criteria

1. Candidate static validation and smoke testing succeed with an input spec of `[51, 256, 256]`.
2. Run metadata records `input_mode: abi_16ch_plus_sza_temporal`, `frame_selection_policy_effective: temporal_eligible_center`, and `temporal_frame_offsets_effective: [-1, 0, 1]`.
3. The Run either completes one finite bounded epoch or fails closed with a temporal-cache/provisioning error that identifies missing, stale, or incomplete trusted temporal evidence.
4. Evidence confirms candidate-visible frames contain only ABI channels 1-16 plus Solar Geometry Input per frame.

## Fallback Next Decision

If ABI-215 fails for candidate validation, repair only the manifest/model contract defect. If it fails due to temporal cache scope or patch availability, keep the candidate unchanged and fix or refresh trusted temporal provisioning before rerunning.

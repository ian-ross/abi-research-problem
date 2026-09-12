# ABI-259 temporal-attention line-support decoder U-Net

ABI-259 is an exploratory temporal family-development Candidate for GOES ABI Contrail Segmentation. It consumes only the provider-advertised `abi_16ch_plus_sza_temporal` tensor with offsets `[-1, 0, 1]` and `frame_selection_policy: temporal_eligible_center`.

## Rationale

ABI-223 remains the strongest temporal-attention comparator, but diagnostics showed under-confident fixed-threshold contrail evidence and positive-patch under-coverage. ABI-258 showed that changing only the final calibration head can trade recall for precision/connectivity. ABI-259 therefore keeps ABI-223's temporal-attention stem and moves the evidence-sharpening mechanism into the decoder with learned line-support blocks and center-frame detail features.

## Architecture

- Per-frame finite ABI/SZA/BTD feature builder over the three provider-owned temporal frames.
- Center-relative temporal attention and bounded before/after change features inherited from ABI-223.
- Compact U-Net encoder and ASPP bottleneck.
- Line-aware decoder fusions that add learned horizontal, vertical, and dilated diagonal context at each upsampled scale.
- Center-frame detail projection injected at full resolution.
- Final mask head that fuses refined decoder features, learned line-support features, and bounded learned line/centerline evidence logits.
- Trusted auxiliary outputs: `line_logits` and `centerline_logits`.

## Contract boundaries

Candidate code is architecture-only. It does not implement or alter data loading, temporal cache lookup, temporal selection, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Budget

Default exploratory budget: 12 epochs, batch size 2, BCE-Dice loss, AdamW, constant learning rate, trusted random mirroring, source-balanced sampling, disabled early stopping as configured by the Harness.

## Primary comparisons

- ABI-223 temporal-attention late36 comparator (`run_20260908_154531_8c7e2b`).
- ABI-255 compact recurrent temporal comparator (`run_20260911_210922_27f346`).
- ABI-258 dual-evidence calibration negative/mixed comparator (`run_20260912_004429_1eee45`).
- ABI-202 mature whole-validation frontier for context only.

# ABI-061: Full-spectral BTD high-resolution line U-Net with focal-Tversky loss

## Hypothesis

ABI-058's oriented high-resolution BTD line U-Net is the current best capped family Result, but later decoder-head refinements traded aggregate Dice for precision/connectivity or source imbalance. The next safer broadening axis is a trusted loss-policy change rather than another decoder-head change: replacing `bce_dice_cldice` with trusted `focal_tversky` may improve thin-contrail recall and MIT/source balance while the fixed oriented-context architecture and low-weight provider-derived Centerline Target auxiliary preserve some line-continuity bias.

This is a **family-development continuation** in the full-spectral BTD high-resolution line U-Net family, not a promotion candidate and not full-data evidence.

## Comparison Target

Primary comparison target: ABI-058 (`run_20260827_171331_c1769a`), the oriented full-resolution-context branch with trusted `bce_dice_cldice` and Centerline Target auxiliary weight 0.02.

Secondary context: ABI-056 (`run_20260827_153716_1ac9d4`) and ABI-060 (`run_20260827_185739_a17505`) for aggregate/source Dice, recall/precision balance, predicted-positive burden, and filtered connectivity.

## Expected Effect

The expected benefit is higher filtered recall and better MIT filtered Dice than ABI-058/ABI-060 without returning to all-positive or high-false-positive behavior. A successful bounded Run would show non-degenerate predictions, finite training, aggregate filtered Dice close to the ABI-058 family baseline, and a recall/source-balance gain large enough to justify another bounded policy/architecture continuation.

## Implementation Sketch

Reuse the ABI-058 architecture unchanged: provider-approved `abi_16ch` input, normalized full-spectral channels, explicit thermal BTD planes derived only from ABI channels 1-16, learned 1x1 channel mixing, high-resolution U-Net encoder/decoder, multi-scale skip fusion, and oriented full-resolution context refinement. Keep the provider-derived `centerline` auxiliary output at weight 0.02. Change only the manifest-selected trusted primary loss from `bce_dice_cldice` to `focal_tversky`.

## Contract Features Used

- `input_mode: abi_16ch`; no longitude or latitude inputs.
- `output_form: mask_logits` with optional `centerline_logits` auxiliary output.
- Trusted primary loss allowlist: `focal_tversky`.
- Trusted auxiliary target allowlist: `centerline` with `weighted_bce`, weight 0.02.
- Trusted data policy: `combined_source_balanced`, `all_target_frames`, and `random_mirroring`.
- Candidate code defines only model architecture and approved ABI-channel feature mixing; it does not implement data loading, losses, metrics, target derivation, augmentation, sampling, thresholding, Artifact Filters, or postprocessing.

## Budget Requested

Use the active Workspace Configuration limits: one sequential Run, up to 1,024 provider-selected train and validation records per Dataset Source/split, 12 epochs, batch size 4, constant learning rate 0.0003, Docker/A100 execution, 3,600-second timeout, and fixed first-four prediction artifacts.

## Success Criteria

Treat the Run as useful family-development evidence if it completes finite and non-degenerate within resource limits and satisfies at least two of the following against ABI-058: improves filtered recall by at least 0.03, improves MIT filtered Dice, keeps aggregate filtered Dice within 0.02 of ABI-058's 0.3248 capped best, or improves whole-family source balance without a large predicted-positive-fraction increase. It need not beat MCAST 2.1 or be promotion-ready.

## Fallback/Next Decision

If focal-Tversky collapses, diverges, or produces clear high-false-positive/all-positive behavior, do not repeat this loss-policy branch unchanged. If it improves recall/source balance but loses too much aggregate Dice, consider a later controlled architecture/loss continuation that restores precision without candidate-owned thresholding or Artifact Filtering. If it performs worse across Dice, recall, source balance, and connectivity, broaden to a materially different thin-line architecture or write a synthesis note before further high-resolution U-Net variants.

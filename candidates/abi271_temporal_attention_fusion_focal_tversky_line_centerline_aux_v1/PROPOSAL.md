# ABI-271 temporal-attention fusion focal-Tversky loss-policy continuation

## Hypothesis

ABI-223 and ABI-255 diagnostics indicate that temporal models learn useful but partly under-confident contrail evidence: lower diagnostic thresholds recover recall, but Candidate-owned thresholding is forbidden. ABI-271 tests a controlled, provider-allowlisted training-policy change: keep the ABI-223 compact temporal-attention architecture unchanged and select the trusted `focal_tversky` primary loss to bias optimization toward recovering harder positive contrail pixels at the fixed 0.5 threshold.

## Comparison Target

Primary comparison target: ABI-223 temporal-attention fusion U-Net late36 (`run_20260908_154531_8c7e2b`) on the temporal-eligible validation population. Secondary exploratory comparisons: ABI-222 temporal-attention 12-epoch parent, ABI-255 compact recurrent temporal comparator (`run_20260911_210922_27f346`), ABI-259/261 recent temporal recall/connectivity attempts, and ABI-202 as the single-frame aggregate reference for context only.

## Expected Effect

The expected useful effect is higher filtered recall and fewer positive-patch under-coverage failures than the BCE-Dice temporal-attention scout, without the broad false-positive expansion and connectivity loss seen in recent architecture-level recall heads. Success does not require beating ABI-202 on a capped temporal-eligible scout. The loss-policy probe is useful if it shows whether temporal attention's lower-confidence evidence can be lifted by an existing trusted objective while preserving source balance and non-degenerate connected-line metrics.

## Implementation Sketch

Use the ABI-223 compact temporal-attention fusion U-Net architecture unchanged except for Candidate identifiers. The model consumes three provider-stacked ABI+Solar Geometry frames, builds normalized ABI/BTD/Solar Geometry features per frame, fuses previous/center/next frame embeddings with per-pixel temporal attention and change features, decodes through a compact U-Net, and emits `mask_logits`, `line_logits`, and `centerline_logits`. The manifest selects `focal_tversky` as the trusted primary loss with the same Line and Centerline auxiliary targets as ABI-223.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal`.
- `data.frame_selection_policy: temporal_eligible_center`.
- `data.temporal_frame_offsets: [-1, 0, 1]` from the allowlisted temporal windows.
- `data.sampling_policy: combined_source_balanced`.
- `data.augmentation_policy: random_mirroring`.
- Trusted primary loss `focal_tversky`.
- Trusted auxiliary targets `line` and `centerline` with `weighted_bce` auxiliary losses.
- AdamW, constant learning rate, batch size 2, and Harness-owned capped record selection/resource limits.

Candidate source does not implement data loading, temporal lookup, frame repair, sampling policy, augmentation transforms, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, coordinates, Dataset Source identity, training loops, downloads, resource scheduling, or lifecycle behavior.

## Budget Requested

Exploratory/default budget: 12 epochs, batch size 2, constant learning rate. No late-improving budget is requested because this is a first temporal focal-Tversky loss-policy probe, not a close continuation with prior focal-Tversky temporal late-improvement evidence.

## Success Criteria

At the exploratory budget, treat ABI-271 as promising if it is finite, non-collapsed, resource-safe, source-informative, and improves filtered recall versus the ABI-222 12-epoch temporal-attention parent without a severe precision/connectivity/source-balance collapse. Stronger evidence would be matching or exceeding ABI-254/258/259 selected filtered Dice while improving recall or positive-patch coverage. A late-improving continuation would require a selected checkpoint near epoch 12, finite non-collapsed predictions, and a rising or ambiguous primary trajectory.

## Fallback/Next Decision

If ABI-271 broadens predicted positives while reducing precision, connectivity, or MIT/Google balance, stop this exact focal-Tversky temporal-attention branch and return to mechanism-changing architecture work rather than repeat the loss swap. If it improves recall with acceptable precision/connectivity and a late-rising trajectory, consider a late-improving continuation or bounded temporal-eligible diagnostics. If it fails contract/resource/smoke, classify through the Harness failure path and repair only if the original hypothesis is preserved.

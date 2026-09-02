# ABI-100 full-spectral BTD frequency-gated line U-Net deterministic-shuffle clDice continuation

## Hypothesis

The ABI-066 frequency-gated line U-Net branch produced the strongest local precision/connectivity-forward capped evidence with trusted `bce_dice_cldice`, centerline auxiliary supervision, and provider-owned `combined_source_balanced` traversal. ABI-096 showed that provider-owned `deterministic_shuffle` traversal can shift the focal-Tversky version of the same family toward higher precision/connectivity and lower predicted-positive burden, though with lower recall and aggregate Dice. This family-development continuation tests whether the same data-policy shift applied to the ABI-066 clDice branch improves threshold discipline or line connectivity without candidate-owned postprocessing.

## Comparison Target

Primary comparison target: ABI-066, `run_20260827_230540_bf4ce3`, the full-spectral BTD frequency-gated line U-Net with trusted `bce_dice_cldice`, centerline auxiliary weight 0.02, random mirroring, and combined source-balanced traversal.

Secondary references: ABI-068 (`run_20260828_010836_4ccc77`) as the aggregate-Dice focal-Tversky reference; ABI-096 (`run_20260830_021504_c112f8`) as the deterministic-shuffle focal-Tversky data-policy reference; ABI-078 (`run_20260828_094949_ad2af0`) as a conservative BCE-Dice operating-point reference.

## Expected Effect

Changing only the provider-owned sampling traversal from `combined_source_balanced` to `deterministic_shuffle` may expose the precision/connectivity-forward clDice branch to less repeated source-balanced ordering pressure within each epoch. The expected useful outcome is not necessarily a new aggregate-Dice best; it is a cleaner trusted-threshold operating point: similar filtered Dice to ABI-066 with improved filtered precision or connectivity, lower filtered predicted-positive fraction, or a more stable MIT/Google trade-off. A negative result would show that the deterministic-shuffle precision gain seen in ABI-096 does not transfer to the clDice branch and that ABI-066's source-balanced traversal remains preferable.

## Implementation Sketch

Start from the ABI-066 model architecture unchanged: normalized provider-approved ABI channels 1-16, thermal BTD planes derived only from those approved channels, learned 1x1 spectral mixing, high/low spatial-frequency stem, gated U-Net skips, frequency-pyramid fusion, oriented line refinement, `mask_logits`, and `centerline_logits`.

The controlled manifest change is limited to:

- `data.sampling_policy: deterministic_shuffle`

All other contract choices remain matched to ABI-066: `abi_16ch` input, `mask_logits` output form, trusted `bce_dice_cldice` primary loss, trusted `centerline` auxiliary target with `weighted_bce` weight 0.02, trusted `random_mirroring`, AdamW, learning rate 0.0003, batch size 4, 12 epochs, constant learning rate, and disabled Harness-owned early stopping by workspace policy.

## Contract Features Used

- Provider-approved `abi_16ch` input only; longitude and latitude are not inputs and are not reconstructed.
- Candidate-owned code defines only model architecture and approved-channel BTD feature construction.
- Trusted provider/Harness owns data loading, Leakage-Safe Split logic, deterministic capped-record selection, epoch sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, resource placement, and Run lifecycle.
- Manifest selects allowlisted `deterministic_shuffle` sampling, `random_mirroring` augmentation, `bce_dice_cldice` primary loss, `adamw`, `constant_lr`, batch size 4, and 12 epochs.
- Provider-derived `centerline` auxiliary target uses allowlisted `weighted_bce` at weight 0.02.
- No pretrained weights, network access, filesystem probes, candidate-owned postprocessing, shell scripts, notebooks, or dataset artifacts are included.

## Budget Requested

Run one sequential capped representative Candidate Run under the active Workspace Configuration: up to 1,024 training and 1,024 validation records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, constant learning rate, disabled early stopping, four fixed first_n prediction artifacts, Docker training timeout 3,600 seconds, and the 25M-parameter smoke ceiling. The ABI-066 architecture has prior feasible resource evidence at batch size 4; this manifest-only data-policy continuation should remain in the same resource class.

## Success Criteria

Treat this as capped family-development evidence, not promotion evidence. Useful continuation evidence would include at least one of:

- filtered Dice within 0.02 of ABI-066's 0.3825 while improving filtered precision above 0.4427 or filtered connectivity above 0.4731;
- filtered predicted-positive fraction below ABI-066's 0.00276 without all-negative collapse and with aggregate filtered Dice at or above 0.36;
- a source-stratified trade-off that keeps both MIT and Google filtered Dice at or above 0.34 while improving one secondary metric, such as precision or connectivity, relative to ABI-066;
- a clearly late-improving finite trajectory that supports one more bounded data/loss-policy follow-up even if the final capped Dice remains below ABI-066.

Hard-stop evidence for this exact branch would be non-finite training, persistent all-negative/all-positive prediction collapse, filtered Dice below 0.34 with no secondary-metric advantage, either Dataset Source below 0.30 filtered Dice, or substantially worse positive-area burden than ABI-066 without compensating recall.

## Fallback/Next Decision

If ABI-100 improves precision/connectivity or positive-area discipline while preserving most of ABI-066's Dice, request a later whole-validation failure-bucket/acceptance-style evaluation only after comparing the capped result against ABI-066 and ABI-068. If it regresses like ABI-096 did on aggregate Dice or becomes too conservative, do not repeat deterministic-shuffle on this clDice branch; retain ABI-066 as the precision/connectivity reference and broaden to a materially different threshold-discipline mechanism or another provider-approved policy axis rather than adding more post-decoder gates.

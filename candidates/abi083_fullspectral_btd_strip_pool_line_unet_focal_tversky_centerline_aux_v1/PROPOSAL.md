# ABI-083 full-spectral BTD strip-pooling line U-Net scout

## Hypothesis

A compact strip-pooling line U-Net can improve thin-contrail continuity and source-balanced filtered Dice by injecting non-coordinate row/column ribbon context before the final mask head, rather than relying on the ABI-068 frequency-gated branch local high/low frequency gates or additional output-side refiners. The model should preserve ABI-068 full-spectral BTD front end and focal-Tversky recall while recovering some of ABI-066 connectivity and precision behavior through earlier feature-space continuity context.

Classification: **family scout**. This is the first candidate in a strip-pooling/ribbon-context architecture family, so it is not required to beat the mature ABI-068 capped incumbent immediately. One bounded follow-up would be justified if the Run is finite, non-degenerate, source-balanced, within the resource envelope, and either reaches roughly ABI-066/081 aggregate filtered Dice or shows a clear connectivity/precision improvement over recent output-refiner branches without catastrophic source loss.

## Comparison Target

Primary capped family-development references are:

- ABI-068 (`run_20260828_010836_4ccc77`): strongest local frequency-gated focal-Tversky reference, best capped filtered Dice 0.3964.
- ABI-066 (`run_20260827_230540_bf4ce3`): precision/connectivity-forward frequency-gated reference, filtered precision 0.4427 and connectivity 0.4731.
- ABI-080/081/082: recent negative or non-improving frequency-gated continuations that suggest late head changes, auxiliary removal, or thermal-only input are not sufficient.

Canonical MCAST 2.1 remains promotion context only; this Run is capped representative scout evidence rather than a full-data promotion claim.

## Expected Effect

The row and column strip-pooling modules summarize elongated context along image axes and combine it with local/dilated features at multiple scales. This should help reject isolated blobs that lack ribbon-scale support while preserving continuous narrow structures, improving filtered precision/connectivity relative to ABI-080/082 and avoiding all-negative collapse. Because full-image strip summaries are not longitude or latitude and contain no coordinate inputs, they remain architecture context over provider-approved ABI tensors.

## Implementation Sketch

Implement a single-file PyTorch candidate with:

- the previously successful normalized full-spectral ABI plus thermal BTD front end using only ABI channels 1-16;
- a residual encoder/decoder with GroupNorm/GELU and three downsampling stages;
- a `StripPoolContext` block at the bottleneck and a high-resolution `RibbonFusion` block before the heads;
- primary `mask_logits` and trusted provider-derived `centerline_logits` auxiliary output;
- no custom data loading, target derivation, loss, metrics, thresholding, Artifact Filters, postprocessing, training loops, resource placement, filesystem probing, network access, or pretrained weights.

## Contract Features Used

- `input_mode: abi_16ch` with forbidden longitude/latitude channels excluded by the provider.
- `output_form: mask_logits`.
- Trusted `centerline` auxiliary target with output `centerline_logits`, `weighted_bce`, and weight 0.02.
- Trusted `combined_source_balanced` sampling, `random_mirroring` augmentation, AdamW optimizer, `focal_tversky` primary loss, and `constant_lr` scheduler.
- Candidate batch size 4, max epochs 12, no Candidate-owned scheduler or early stopping changes.

## Budget Requested

Use the active Agent Workspace limits: 1,024 provider-selected records per Dataset Source and split, batch size 4, 12 epochs, constant learning rate 0.0003, disabled early stopping, fixed first-four prediction retention, A100 execution under the 3,600-second Docker training budget, and the 25M-parameter smoke ceiling. This unprofiled architecture family should be submitted sequentially under the configured concurrency cap of one.

## Success Criteria

Useful scout evidence requires all of the following:

- finite smoke/training/validation with no lifecycle or resource failure;
- model summary under 25M parameters and successful required output keys/shapes;
- non-degenerate predictions with no persistent all-negative or all-positive collapse;
- both MIT and Google filtered Dice at or above 0.33, unless a clear improving trajectory makes a single-source weakness diagnostically useful;
- aggregate capped filtered Dice within about 0.03 of ABI-068 or an interpretable improvement over recent ABI-080/082 precision/connectivity trade-offs.

A strong continuation signal would be aggregate filtered Dice at least ABI-066-like around 0.38 with improved connectivity/precision versus ABI-080/082, or clear late-epoch improvement suggesting under-training under the capped 12-epoch budget.

## Fallback/Next Decision

If ABI-083 fails static validation or smoke because of candidate code, repair the exact implementation once if the hypothesis is preserved. If it completes but collapses or is clearly worse on both source balance and precision/connectivity, do not repeat the strip-pooling branch unchanged; broaden to another architecture family or request a trusted training/calibration capability if threshold/selection behavior appears to be the blocker. If it is finite and source-balanced but below ABI-068 with a distinct connectivity/precision advantage, consider one controlled strip-context follow-up rather than declaring the family exhausted after a single scout.

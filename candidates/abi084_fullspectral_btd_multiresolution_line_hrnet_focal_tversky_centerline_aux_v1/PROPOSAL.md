# ABI-084 full-spectral BTD multi-resolution line-HRNet scout

## Hypothesis

A compact HRNet-style multi-resolution architecture can preserve thin high-resolution contrail evidence while repeatedly injecting lower-resolution cloud context before prediction, reducing the false-positive/clutter trade-off seen in recent output-head and strip-pooling continuations. Unlike ABI-068's U-Net-style encoder/decoder, this scout keeps a high-resolution branch alive throughout training and exchanges features with medium/low-resolution branches in several fusion stages.

Classification: **family scout**. This is the first multi-resolution line-HRNet candidate in the campaign, so it is not required to immediately beat the mature ABI-068 frequency-gated incumbent. One bounded follow-up would be justified if the Run is finite, non-degenerate, source-balanced, resource-feasible, and either approaches ABI-066/081 aggregate filtered Dice or shows a distinct precision/connectivity or source-balance advantage over recent negative continuations.

## Comparison Target

Primary capped and diagnostic references are:

- ABI-068 (`run_20260828_010836_4ccc77`): strongest local whole-validation-tested aggregate-Dice reference, capped filtered Dice 0.3964 and whole-validation filtered Dice 0.3951.
- ABI-066 (`run_20260827_230540_bf4ce3`): precision/connectivity-forward frequency-gated reference, capped filtered precision 0.4427 and connectivity 0.4731.
- ABI-080/082/083: recent non-improving continuations showing that logit consensus, thermal-only input, and row/column strip context did not recover the desired trade-off.

Canonical MCAST 2.1 remains promotion context only; this candidate is bounded representative family-scout evidence rather than a full-data promotion claim.

## Expected Effect

The multi-resolution branch design should avoid two observed failure modes: losing high-resolution line detail in broad context modules, and producing permissive positive-area clutter when recall is increased. High-resolution line-context blocks operate on local detail throughout the network, while medium/low-resolution branches supply coarser cloud and texture context through differentiable feature fusion. The expected useful signal is ABI-068-like recall with better precision/connectivity or lower predicted-positive burden, especially on negative patches, without candidate-owned thresholding or Artifact Filters.

## Implementation Sketch

Implement a single-file PyTorch candidate with:

- the campaign-tested normalized full-spectral ABI plus thermal BTD front end using only ABI channels 1-16;
- a compact high-resolution stem and parallel high/mid/low-resolution branches rather than a U-Net decoder with deep skip concatenation;
- repeated `MultiResolutionFusionStage` modules that exchange high-resolution line evidence with low-resolution cloud context using only differentiable convolutions, pooling, and interpolation;
- lightweight oriented line-context blocks using depthwise horizontal/vertical filters plus local/dilated context;
- primary `mask_logits` and trusted provider-derived `centerline_logits` auxiliary output;
- no custom data loading, target derivation, loss, metrics, thresholding, Artifact Filters, postprocessing, training loops, resource placement, filesystem probing, network access, or pretrained weights.

## Contract Features Used

- `input_mode: abi_16ch` with forbidden longitude/latitude channels excluded by the provider.
- `output_form: mask_logits`.
- Trusted `centerline` auxiliary target with output `centerline_logits`, `weighted_bce`, and weight 0.02.
- Trusted `combined_source_balanced` sampling, `random_mirroring` augmentation, AdamW optimizer, `focal_tversky` primary loss, and `constant_lr` scheduler.
- Candidate batch size 4, max epochs 12, no Candidate-owned scheduler or early stopping changes.

## Budget Requested

Use the active Agent Workspace limits: 1,024 provider-selected records per Dataset Source and split, batch size 4, 12 epochs, constant learning rate 0.0003, disabled early stopping, fixed first-four prediction retention, A100 execution under the 3,600-second Docker training budget, and the 25M-parameter smoke ceiling. Because this is an unprofiled architecture family, submit it sequentially under the configured concurrency cap of one.

## Success Criteria

Useful scout evidence requires all of the following:

- finite smoke/training/validation with no lifecycle or resource failure;
- model summary under 25M parameters and successful required output keys/shapes;
- non-degenerate predictions with no persistent all-negative or all-positive collapse;
- both MIT and Google filtered Dice at or above 0.33, unless a clear improving trajectory makes a single-source weakness diagnostically useful;
- aggregate capped filtered Dice within about 0.04 of ABI-068, or an interpretable improvement over recent ABI-080/082/083 precision/connectivity and predicted-positive-burden trade-offs.

A strong continuation signal would be aggregate filtered Dice around ABI-066/081 levels (roughly 0.38) with better source balance than ABI-066 or better precision/connectivity than ABI-081/082. Late improvement at epoch 12 may justify one controlled family-development follow-up even if the first scout does not beat ABI-068.

## Fallback/Next Decision

If ABI-084 fails static validation or smoke because of candidate code, repair this exact implementation once if the hypothesis is preserved. If it completes but collapses or is clearly worse than recent scouts on source balance, precision, recall, and connectivity, do not repeat the multi-resolution line-HRNet branch unchanged. If it is finite and source-balanced with a distinct precision/connectivity or negative-clutter advantage, consider one bounded follow-up that adjusts only model capacity or fusion depth while preserving provider/Harness ownership of data, sampling, losses, auxiliary targets, metrics, thresholding, Artifact Filters, resources, and lifecycle.

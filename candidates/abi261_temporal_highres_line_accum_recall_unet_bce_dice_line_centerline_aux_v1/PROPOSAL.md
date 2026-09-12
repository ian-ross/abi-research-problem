# ABI-261 temporal high-resolution line-accumulation recall U-Net

## Hypothesis

ABI-240 showed that temporal line accumulation can become near-frontier for overlap under the approved late36 budget, but its selected checkpoint still had weak filtered connectivity because the low-resolution accumulator favored broader or fragmented positives. ABI-255 showed that compact recurrent temporal change modeling can cover positive patches but leaves line evidence under-connected and partly under-confident. ABI-259 recovered some continuity with decoder-side line support, but at a lower-recall, lower-Dice balance than ABI-223/255.

ABI-261 tests a mechanism-changing continuation: keep ABI-223/239-style provider-owned three-frame temporal attention, but move line accumulation back to the native-resolution stem and add a bounded recall-preserving mask head. The hypothesis is that high-resolution directional support can preserve thin-line detail before downsampling while the recall head raises true line-supported logits at the trusted threshold without Candidate-owned thresholding or postprocessing.

This is a **family-development continuation** within temporal modeling, not a promotion claim.

## Comparison Target

Primary temporal comparison targets:

- ABI-240 (`run_20260911_031326_43ed12`), the late36 low-resolution temporal line-accumulator U-Net: filtered Dice 0.4149, recall 0.3955, connectivity 0.2649 on temporal-eligible capped validation.
- ABI-255 (`run_20260911_210922_27f346`), the late36 compact recurrent change-state U-Net: filtered Dice 0.4173, recall 0.3764, connectivity 0.2811.
- ABI-223 (`run_20260908_154531_8c7e2b`), the stronger temporal-attention comparator: filtered Dice 0.4198, precision 0.4838, recall 0.3707, connectivity 0.4124.

Secondary context: ABI-259 (`run_20260912_012708_f5897e`) for decoder-side line support, ABI-253 for the modern U-NetFormer comparator, and ABI-202 for the mature single-frame whole-validation frontier.

## Expected Effect

The expected effect is improved filtered connectivity and fixed-threshold positive-patch coverage relative to ABI-240/259, without sacrificing the recall gains that made ABI-240 useful. A useful Result would preserve ABI-240/255-level filtered Dice while raising selected-checkpoint connectivity, or recover ABI-223-like connectivity while keeping MIT/Google Dice source-informative and avoiding excessive predicted-positive expansion.

## Implementation Sketch

Start from the compact ABI-239/240 temporal-attention U-Net skeleton over provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]`. Retain trusted per-frame ABI/SZA normalization, ABI-channel-derived BTD feature planes, center-anchored per-pixel temporal attention, before/after change features, compact encoder/ASPP decoder, source-balanced sampling, random mirroring, BCE-Dice loss, batch size 2, and trusted Line plus Centerline auxiliary outputs.

Replace the low-resolution pre-encoder line accumulator with `HighResolutionLineAccumulator`: it projects stem features, averages directional evidence along horizontal, vertical, and diagonal offsets at native resolution, adds a half-resolution longer-span path, and fuses the resulting support through learned gates. Replace the single mask convolution with `RecallPreservingMaskHead`, a bounded base-logit plus gated residual head intended to raise line-supported evidence while remaining differentiable architecture logic.

The accumulator and mask head do not inspect targets at inference, choose thresholds, apply morphology, change Artifact Filters, implement losses/metrics, select samples, access temporal cache paths, use coordinates, or run custom training loops.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal` with provider-owned temporal provisioning.
- `data.frame_selection_policy: temporal_eligible_center` and `data.temporal_frame_offsets: [-1, 0, 1]`.
- `data.sampling_policy: combined_source_balanced` and trusted `random_mirroring` augmentation.
- Trusted primary loss `bce_dice`, AdamW optimizer, batch size 2, and constant learning-rate scheduler.
- Trusted Line and Centerline auxiliary targets using `weighted_bce` weights 0.01 and 0.02.

Candidate code defines architecture only. It does not implement data loading, temporal lookup, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, longitude/latitude features, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Budget Requested

Use the default exploratory budget: 12 epochs, batch size 2, constant learning rate, disabled early stopping, provider-owned capped temporal-eligible selection, and the configured A100 execution policy. Do not request late36 in this step because the high-resolution accumulator and recall head are a mechanism-changing architecture. If the trajectory is finite, source-informative, non-collapsed, and late-improving at epoch 12, a later step can decide whether an approved late-improving close continuation is justified.

## Success Criteria

Treat ABI-261 as useful temporal-family evidence if it completes finitely, avoids prediction collapse, remains source-informative on MIT and Google, and improves selected-checkpoint connectivity over ABI-240/255/259 without a severe Dice or precision collapse. A strong scout would approach ABI-223/255 filtered Dice while improving over ABI-240's 0.2649 and ABI-255's 0.2811 connectivity, or show a late-improving recall/connectivity trajectory worth a later approved late36 continuation. Promotion would require later trusted diagnostics and operator review; capped temporal-eligible evidence alone is not promotion evidence.

## Fallback/Next Decision

If ABI-261 fails contract, smoke, shape, numerical, or resource validation, repair only if the high-resolution line-accumulation plus recall-preserving-head hypothesis is preserved. If it completes but repeats ABI-240's low-connectivity broad-positive behavior or ABI-259's conservative low-recall line-support tradeoff, stop this exact mechanism. If it is finite and late-improving near the exploratory ceiling, consider a later late36 close continuation under the approved budget-request path. If it is finite but not competitive, broaden to another underexplored family rather than continuing local temporal-head tuning.

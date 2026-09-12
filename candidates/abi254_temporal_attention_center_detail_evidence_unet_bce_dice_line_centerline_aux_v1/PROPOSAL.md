# ABI-254 temporal attention center-detail evidence U-Net

## Hypothesis

ABI-223 demonstrated a real temporal-context advantage over the matched single-frame control on the temporal-eligible validation population, but its failure-bucket review showed conservative fixed-threshold behavior and substantial lower-threshold recall headroom. ABI-246 showed that changing only the final mask-logit consensus head is unstable, and ABI-238 showed that post-decoder directional context can trade away ABI-223's connectivity. ABI-254 tests whether an earlier architecture-level center-frame detail evidence bridge can raise true contrail logits at threshold 0.5 while preserving ABI-223's temporal attention, precision discipline, and connectivity. This is a **family-development continuation** within the temporal-attention family, not a promotion claim.

## Comparison Target

The direct comparison target is ABI-223 (`run_20260908_154531_8c7e2b`), the strongest temporal-attention diagnostic comparator, with temporal-eligible filtered Dice 0.4198, precision 0.4838, recall 0.3707, and connectivity 0.4124 in the failure-bucket evaluation. ABI-222 is the exploratory temporal-attention parent. ABI-238, ABI-240, ABI-244, ABI-246, and ABI-253 provide negative/mixed evidence for post-decoder directional context, line accumulation, shifted-window attention, final-logit consensus, and compact U-NetFormer line memory. ABI-202 remains the aggregate whole-validation frontier context.

## Expected Effect

The center-detail evidence bridge should expose the final decoder to center-frame signed local detail, broad temporal support, horizontal/vertical continuity cues, and encoder/stem agreement before the final mask and auxiliary heads. The intended effect is higher recall, MIT filtered Dice, and stable filtered Dice relative to ABI-223 without the connectivity loss seen in ABI-238 or the instability seen in ABI-246. The main risk is increased false-positive clutter if center-frame detail support raises cloud-edge evidence rather than contrail evidence.

## Implementation Sketch

Start from the ABI-223 compact temporal-attention fusion U-Net: provider-owned three-frame `abi_16ch_plus_sza_temporal` input, ABI/SZA normalization, ABI-channel-derived BTD features per frame, lightweight temporal attention and change embedding, compact U-Net encoder/ASPP/decoder, trusted Line and Centerline auxiliary heads, BCE-Dice primary loss, source-balanced sampling, random mirroring, and batch size 2.

Add one architecture-only module before the final refinement: `CenterDetailEvidenceBridge`. It projects the center-frame feature tensor to decoder width, computes signed local detail and broad support from the temporal stem and high-resolution encoder feature, applies learned horizontal/vertical convolutions to a decoder/detail seed, gates encoder support, and adds a zero-initialized bounded residual to the decoder feature. The bridge does not threshold, morphologically filter, postprocess, derive targets, choose samples, access temporal cache paths, read data, or alter Harness-owned losses, metrics, sampling, augmentation, Artifact Filters, resource scheduling, or lifecycle behavior.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza_temporal` with provider-owned offsets `[-1, 0, 1]`; no longitude/latitude, Dataset Source identity, scene identity, route/location priors, or candidate-owned temporal lookup.
- Provider-owned data policy: `temporal_eligible_center` frame selection and `combined_source_balanced` sampling.
- Provider-owned augmentation: `random_mirroring` only.
- Trusted loss/optimizer/scheduler: `bce_dice`, AdamW, constant learning rate.
- Trusted auxiliary targets: Line Target and Centerline Target via `weighted_bce`.
- Candidate code defines architecture only and does not implement data loading, training loops, target derivation, losses, metrics, Artifact Filters, postprocessing, thresholding, augmentation transforms, sampling policies, downloads, filesystem probes, coordinates, resource scheduling, or lifecycle behavior.

## Budget Requested

Use the default exploratory budget: 12 epochs, batch size 2, constant learning rate, disabled early stopping, provider-owned capped temporal-eligible selection, and the configured A100 execution policy. Do not request the late-improving budget on this first mechanism-changing bridge; if the trajectory is finite, source-informative, and late-improving, a later Autonomy Step can decide whether a late36 close-continuation is justified.

## Success Criteria

Treat ABI-254 as useful family-development evidence if it completes finitely, avoids prediction collapse, remains source-informative on MIT and Google, and improves at least one of recall, MIT filtered Dice, connectivity, or filtered Dice relative to the ABI-222/223 temporal-attention family without a large precision collapse or predicted-positive blow-up. A capped temporal-eligible `val/filtered_dice` near ABI-223/238 with better recall or connectivity would justify continued temporal evidence-raising work even if it does not beat ABI-202. Promotion would require later diagnostics and operator review; capped evidence alone is not promotion evidence.

## Fallback/Next Decision

If ABI-254 fails contract, smoke, shape, numerical, or resource validation, repair the exact bug only if the center-detail evidence-bridge hypothesis is preserved. If it completes but behaves like ABI-246 (unstable recall/precision swings) or ABI-238 (connectivity loss without recall gain), stop this exact bridge and broaden again. If it is finite and late-improving near epoch 12, consider a late36 close-continuation in a future Autonomy Step under the approved late-improving policy.

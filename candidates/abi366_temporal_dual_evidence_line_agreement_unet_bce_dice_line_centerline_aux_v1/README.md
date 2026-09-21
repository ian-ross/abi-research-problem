# ABI-366 temporal dual-evidence line-agreement U-Net

ABI-366 is an exploratory temporal family-development Candidate for GOES ABI Contrail Segmentation. It consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`.

## Motivation

Recent temporal line-support and five-frame variants oscillated among compact precision, broad recall, and transient connectivity. ABI-350 remains a strong temporal-eligible capped comparator, but ABI-361 and ABI-365 showed that local line-support shuffles and five-frame near/far evidence do not stably combine recall and connected-line continuity.

ABI-366 broadens the mechanism: instead of fusing temporal change early into one stream, it keeps center-frame appearance/detail evidence and temporal-change evidence in separate encoders, then merges them with cross-scale agreement gates before decoder fusion. The aim is to raise true contrail logits only where center detail and temporal persistence/change support agree, reducing broad recall clutter without reverting to a compact low-recall state.

## Architecture

- finite per-frame ABI/Solar Geometry Input normalization;
- ABI-channel-derived thermal brightness-temperature-difference features;
- center-detail stem from the zero-offset frame;
- temporal-change stem from center-minus-neighbor, previous/next difference, and absolute neighbor residuals;
- separate center and change encoders;
- cross-scale agreement gates using center, change, and absolute-difference features;
- orientation-aware line support applied to agreement-fused skip features before decoder fusion;
- bounded architecture-internal compact/recall logit fusion from the final decoder feature;
- trusted `mask_logits`, `line_logits`, and `centerline_logits` outputs.

## Contract boundaries

Candidate code defines architecture only. It does not implement data loading, temporal lookup, sample selection, augmentation, losses, metrics, Artifact Filters, thresholds, postprocessing, training loops, downloads, coordinate inputs, Dataset Source identity, resource scheduling, or lifecycle behavior.

The manifest uses trusted `combined_source_balanced` sampling, `random_mirroring` augmentation, `bce_dice` primary loss, Line and Centerline `weighted_bce` auxiliaries, AdamW, constant learning rate, and batch size 2.

## Expected evidence

ABI-366 is capped temporal-eligible exploratory evidence, not whole-validation promotion evidence. Success means a finite, non-collapsed trajectory that improves the recall/connectivity trade-off relative to recent temporal line-support failures and is close enough to ABI-350/ABI-223-style temporal comparators to justify late-budget continuation.

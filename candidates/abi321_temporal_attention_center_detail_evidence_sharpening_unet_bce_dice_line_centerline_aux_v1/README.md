# ABI-321 temporal-attention center-detail evidence-sharpening U-Net

ABI-321 is an exploratory temporal-attention/evidence-sharpening Candidate for GOES ABI Contrail Segmentation. It broadens away from the recent local shift-bank/C4 gated-head refinements (ABI-319/320) by using provider-owned three-frame temporal attention, a zero-offset center-detail branch, and bounded architecture-internal mask-logit sharpening when region, line, centerline, and center-detail evidence agree.

The model consumes only trusted `abi_16ch_plus_sza_temporal` inputs with `temporal_eligible_center` selection and offsets `[-1, 0, 1]`. It returns `mask_logits`, `line_logits`, and `centerline_logits`. It selects trusted `combined_source_balanced` sampling, `random_mirroring`, BCE-Dice primary loss, Line and Centerline weighted-BCE auxiliaries, AdamW, constant learning rate, batch size 2, and a 12-epoch exploratory budget.

Candidate code is architecture-only and does not implement data loading, temporal lookup, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle control.

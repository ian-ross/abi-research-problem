# ABI-223 temporal-attention fusion U-Net late36

ABI-223 is a late-improving close-continuation of ABI-222 for GOES ABI Contrail Segmentation. It keeps the ABI-222 compact temporal-attention fusion architecture unchanged and consumes the trusted `abi_16ch_plus_sza_temporal` input with frame offsets `[-1, 0, 1]` and `frame_selection_policy: temporal_eligible_center`.

The model builds bounded finite ABI+SZA+BTD features for each provider-supplied frame, projects frames with shared weights, computes per-pixel temporal-attention weights relative to the center frame, and fuses the attention-weighted temporal embedding with bounded signed/absolute change features before a compact U-Net/ASPP decoder. It returns `mask_logits` plus trusted `line_logits` and `centerline_logits` auxiliary outputs.

This Candidate adds only a candidate-local `budget_request.yaml` for the approved `late_improving` budget class, citing ABI-222 (`run_20260908_150315_9aea3f`) as parent evidence because ABI-222 selected epoch 12 as best checkpoint and remained finite, source-informative, noncollapsed, and ahead of the ABI-218 matched single-frame control.

Contract boundaries: no candidate-owned data loading, temporal lookup, missing-frame fallback, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation, sampling, training loop, coordinate inputs, Dataset Source identity, downloads, or resource scheduling.

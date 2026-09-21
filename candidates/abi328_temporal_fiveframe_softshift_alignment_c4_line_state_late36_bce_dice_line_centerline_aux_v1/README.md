# ABI-328 temporal five-frame soft-shift alignment C4 line-state late36

ABI-328 is a mechanism-changing temporal-family continuation after ABI-324/325/326/327. It keeps provider-owned five-frame `abi_16ch_plus_sza_temporal` input with trusted `temporal_eligible_center` selection and offsets `[-2, -1, 0, 1, 2]`, but replaces ABI-327's early change-salience gate with architecture-internal soft local alignment of non-center frames.

Each non-center frame is projected to compact features and softly selected over a small zero-filled shift bank relative to the center-frame feature. The aligned before/after differences and shift-confidence features seed the C4 orientation line state, line-state encoder injections, and detail-consensus mask/Line/Centerline head. The hypothesis is that small temporal displacement support can recover connected true-positive evidence without broad positive-tail reinjection or Candidate-owned thresholding/postprocessing.

The Candidate uses only allowlisted manifest features: BCE-Dice loss, AdamW, constant LR, trusted random mirroring, combined source-balanced sampling, batch size 2, and Line plus Centerline auxiliary targets with weighted BCE. Candidate code does not implement data loading, temporal lookup/cache access, losses, metrics, Artifact Filters, sampling, augmentation, thresholds, postprocessing, coordinate inputs, Dataset Source identity, downloads, scheduling, or lifecycle behavior.

This is capped temporal-eligible feasibility evidence only. It is not whole Working Validation Split promotion evidence against ABI-202/249.

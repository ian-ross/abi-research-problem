# ABI-300 temporal attention evidence-sharpened recall U-Net

ABI-300 is a bounded temporal family-development Candidate for GOES ABI Contrail Segmentation. It returns to the ABI-223/238 temporal-attention family after the ABI-296/297/298/299 local-correlation branch showed useful recall evidence but did not solve connected-line continuity or frontier temporal Dice.

The model consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and trusted `temporal_eligible_center` selection. It keeps the ABI-223/238 shared per-frame feature builder, per-pixel temporal-attention fusion, compact U-Net/ASPP decoder, and high-resolution directional context. The mechanism change is a dual-evidence sharpening head: separate region, line, detail, and agreement streams add small bounded recall support only in uncertain logit bands while a learned clutter gate can suppress confident disagreement. This is architecture logic over logits/features, not thresholding, postprocessing, morphology, a loss, a metric, or an Artifact Filter.

The intended effect is to raise true contrail logits at the fixed 0.5 threshold and improve MIT/source-balanced recall without repeating ABI-296/299's broad local-correlation clutter or ABI-285's low-connectivity recall-heavy state.

Candidate code does not own temporal lookup, data loading, target derivation, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, coordinates, downloads, resource scheduling, prediction retention, or lifecycle behavior.

The Candidate uses trusted `combined_source_balanced` sampling, trusted `random_mirroring`, BCE-Dice primary loss, AdamW with constant learning rate, batch size 2, 12 exploratory epochs, and trusted Line plus Centerline auxiliary targets.

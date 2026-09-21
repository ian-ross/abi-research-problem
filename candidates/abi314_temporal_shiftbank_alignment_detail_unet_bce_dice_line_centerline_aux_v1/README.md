# ABI-314 temporal shift-bank alignment detail U-Net

ABI-314 is a bounded temporal family-development scout for GOES ABI Contrail Segmentation. It consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted temporal-eligible center selection and offsets `[-1, 0, 1]`.

The architecture replaces scalar local-correlation maps and recent temporal C4 residual calibration heads with pre-decoder differentiable feature alignment. Previous and next frame features are projected into key/value spaces; nine one-pixel shifts per neighbor are scored against center-frame keys, softmaxed, and used to build aligned temporal support. The decoder fuses this aligned support with explicit center-frame detail and directional line context, then emits primary `mask_logits` plus trusted `line_logits` and `centerline_logits` auxiliary outputs.

The hypothesis is that small shift-bank alignment can tolerate temporal displacement/advection and recover true contrail logits at the fixed 0.5 threshold without moving temporal lookup, thresholding, postprocessing, losses, metrics, Artifact Filters, sampling, augmentation, coordinates, resource scheduling, or lifecycle control into Candidate code.

## Contract choices

- Research Problem: `goes_abi_contrail_segmentation`
- Input: `abi_16ch_plus_sza_temporal`
- Frame policy: `temporal_eligible_center`
- Temporal offsets: `[-1, 0, 1]`
- Sampling: `combined_source_balanced`
- Augmentation: trusted `random_mirroring`
- Primary loss: trusted `bce_dice`
- Optimizer/scheduler: AdamW, constant learning rate
- Budget: default exploratory 12 epochs, batch size 2
- Auxiliary targets: trusted Line and Centerline targets with weighted BCE

## Expected comparison

Compare the capped temporal-eligible Result primarily against ABI-311, ABI-309, ABI-306, ABI-223/238, and ABI-296/299. ABI-314 is not a full Working Validation Split promotion claim; it is mechanism evidence for whether aligned temporal features improve the recall/connectivity trade-off before any late-budget continuation is considered.

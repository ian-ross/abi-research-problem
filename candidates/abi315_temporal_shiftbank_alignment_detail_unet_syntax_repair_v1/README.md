# ABI-315 temporal shift-bank alignment detail U-Net syntax repair

ABI-315 is a Repair Candidate for ABI-314, which smoke-failed with a candidate-owned `SyntaxError` caused by an unmatched `}` after the `ShiftBankEvidenceHead` docstring in `model.py`. It preserves ABI-314's temporal shift-bank alignment hypothesis, architecture, manifest policy, comparison target, and exploratory budget, changing only the syntax defect that prevented smoke import.

The candidate consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted temporal-eligible center selection and offsets `[-1, 0, 1]`. It keeps the differentiable small-displacement previous/next feature alignment, center-frame detail fusion, directional line context, and trusted `line_logits` plus `centerline_logits` auxiliary outputs.

All data loading, temporal provisioning, sampling, augmentation, losses, metrics, Artifact Filters, thresholding, postprocessing, resource scheduling, execution, and lifecycle behavior remain Harness/provider owned.

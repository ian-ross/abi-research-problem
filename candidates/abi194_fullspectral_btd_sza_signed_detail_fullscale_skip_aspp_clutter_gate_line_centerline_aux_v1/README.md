# abi194_fullspectral_btd_sza_signed_detail_fullscale_skip_aspp_clutter_gate_line_centerline_aux_v1

ABI-194 is an exploratory family-development continuation of the signed-detail full-scale skip ASPP ABI lineage. It keeps the approved full-spectral ABI+SZA input and trusted BCE-Dice, source-balanced sampling, random mirroring, Line Target auxiliary, and Centerline Target auxiliary policies. The architecture change is a learned mask-resolution clutter-gate refinement that calibrates decoder features using local signed detail versus broad smoothed context before emitting logits.

The hypothesis is that architecture-only feature calibration can reduce broad negative-patch clutter without moving thresholding, Artifact Filters, losses, data loading, sampling, target derivation, or postprocessing into Candidate code.

Key references:

- ABI-181 `run_20260902_150611_cbbf35`: whole-validation aggregate filtered-Dice reference.
- ABI-184 `run_20260902_213856_2c04ac`: precision/connectivity and negative-patch-discipline reference.
- ABI-192 `run_20260903_085513_f395ad`: directional-lattice recall/source-balance comparator.
- ABI-193 `run_20260903_115807_8c4be1`: boundary+centerline auxiliary negative control.

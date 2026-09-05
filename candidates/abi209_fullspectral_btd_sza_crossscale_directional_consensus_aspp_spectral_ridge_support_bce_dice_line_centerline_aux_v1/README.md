# ABI-209 full-spectral BTD+SZA spectral-ridge support ASPP

ABI-209 is an exploratory family-development continuation of the ABI-201/202 cross-scale directional-consensus ASPP branch for GOES ABI Contrail Segmentation.

It keeps the ABI-202 approved input, loss, auxiliary-target, sampling, augmentation, optimizer, scheduler, batch-size, and epoch policy. The only architecture change is a lightweight `SpectralRidgeSupportBridge` before final line-aware refinement. The bridge uses features derived from provider-approved ABI channels 1-16 plus Solar Geometry Input, including deterministic BTD features, signed ridge detail, broad decoder/full-scale context, and local feature disagreement. It applies a bounded zero-initialized feature residual and does not implement thresholding, postprocessing, Artifact Filters, losses, metrics, data loading, target derivation, sampling, augmentation, coordinate features, runtime downloads, persistence writes, or resource scheduling.

Primary comparison: ABI-202 `run_20260904_043143_ee0005` and its whole-validation diagnostic `eval_evalreq_abi202_wholeval_failure_buckets_v1`.

See `PROPOSAL.md` for hypothesis, budget, success criteria, and fallback decisions.

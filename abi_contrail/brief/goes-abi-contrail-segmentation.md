# GOES ABI Contrail Segmentation provider brief

This workspace provides the `goes_abi_contrail_segmentation` Research Problem for `ml-autoresearch`.

## v0 scaffold contract

- Provider target: `abi_contrail.research_problem:build_spec`
- Research problem id: `goes_abi_contrail_segmentation`
- Version and contract version: `v0`
- Input mode: `abi_16ch`, a channel-first `[16, 256, 256]` ABI Patch containing GOES ABI channels 1-16.
- Candidate inputs exclude longitude and latitude.
- Output form: `mask_logits`, a `[1, 256, 256]` Contrail Mask logit tensor.
- Loss allowlist: `bce_dice`
- Optimizer allowlist: `adamw`
- Sampling policies: `sequential`, `deterministic_shuffle`
- Temporary primary metric: `val/dice`

Dataset loading, leakage-safe splits, artifact filtering, filtered metrics, learned channel mixers, source-balanced sampling, and MCAST Baseline Segmenters are intentionally staged in later backlog tasks.

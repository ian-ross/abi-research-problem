# GOES ABI Contrail Segmentation provider brief

This workspace provides the `goes_abi_contrail_segmentation` Research Problem for `ml-autoresearch`.

## v0 scaffold contract

- Provider target: `abi_contrail.research_problem:build_spec`
- Research problem id: `goes_abi_contrail_segmentation`
- Version and contract version: `v0`
- Input modes are provider-selected channel-first ABI Patches:
  - `abi_16ch`: `[16, 256, 256]`, GOES ABI channels 1-16.
  - `abi_16ch_plus_sza`: `[17, 256, 256]`, GOES ABI channels 1-16 plus Solar Geometry Input.
  - `abi_thermal_10ch`: `[10, 256, 256]`, GOES ABI channels 7-16.
- Candidate inputs always exclude longitude and latitude.
- Reusable candidate front ends are available from `abi_contrail.model_support`:
  - `Conv1x1ChannelMixer` learns per-pixel linear mixtures across the harness-approved input channels.
  - `RawPlusLearnedChannelMixer` concatenates explicit raw-channel and/or brightness-temperature-difference features with learned 1x1 projections.
- Output form: `mask_logits`, a `[1, 256, 256]` Contrail Mask logit tensor.
- Loss allowlist: `bce_dice`, `focal_tversky`, `bce_dice_cldice`
- Optimizer allowlist: `adamw`
- Sampling policies: `sequential`, `deterministic_shuffle`
- Primary checkpoint metric: `val/filtered_dice` (ADR-0003)
- Validation reporting keeps raw overlap metrics (`val/raw_dice`, `val/raw_iou`, `val/raw_precision`, `val/raw_recall`) alongside filtered metrics (`val/filtered_dice`, `val/filtered_iou`, `val/filtered_precision`, `val/filtered_recall`).
- Candidate-defined arbitrary losses are not allowed. Future loss functions require a Capability Request, human approval, trusted implementation in `ml-autoresearch` harness/problem-support code, and a provider/agent-control-boundary allowlist update.

Source-balanced sampling and MCAST Baseline Segmenters are intentionally staged in later backlog tasks.

## Learned channel-mixer guidance

GOES ABI contrail work often benefits from relationships between thermal infrared brightness temperatures, including window and water-vapor band differences that can make thin ice clouds and line-shaped contrails more separable from surrounding cloud or surface backgrounds. Candidate architectures may use `RawPlusLearnedChannelMixer(..., difference_channel_pairs=((a, b), ...))` to preserve explicit brightness-temperature-difference planes computed as `input[a] - input[b]` while also giving the learned projection access to all provider-approved input channels.

Do not treat any short list of brightness-temperature differences as the fixed search space. The provider supplies safe input tensors and lightweight front-end utilities; candidates remain free to learn other ABI channel combinations, preserve raw bands, add BTD features, or ignore these mixers entirely.

# GOES ABI Contrail Segmentation Research Problem Brief

## Task contract

GOES ABI Contrail Segmentation is a binary semantic segmentation Research Problem. Given a provider-owned **ABI Patch** sample, a candidate model predicts `mask_logits` with shape `[1, 256, 256]`; trusted harness code compares these logits to the binary **Contrail Mask** target derived as `labels != 0`.

The research problem id is `goes_abi_contrail_segmentation`, version `v0`, contract version `v0`. The sample unit is a 256 x 256 GOES ABI patch from the MIT and/or Google Dataset Sources.

## Candidate input modes and forbidden channels

The provider exposes only declared channel-first tensors:

- `abi_16ch`: `[16, 256, 256]`, GOES ABI channels 1-16.
- `abi_16ch_plus_sza`: `[17, 256, 256]`, GOES ABI channels 1-16 plus Solar Geometry Input / solar zenith angle.
- `abi_thermal_10ch`: `[10, 256, 256]`, GOES ABI channels 7-16.

Candidate models must never receive longitude or latitude inputs. Source channels used for longitude/latitude may exist in local arrays for trusted diagnostics, Artifact Filters, or projection-aware provider logic, but they are not candidate features and must not be reconstructed as hidden inputs.

## Channel-combination and BTD guidance

Contrails are thin ice-cloud structures, so useful evidence can come from relationships between ABI channels rather than from a single band. Thermal infrared brightness-temperature differences (BTDs), including window and water-vapor band differences, can help separate thin ice clouds or line-shaped contrails from background cloud and surface structure.

Candidates may use reusable front ends from `abi_contrail.model_support`:

- `Conv1x1ChannelMixer` for learned per-pixel linear mixtures across provider-approved channels.
- `RawPlusLearnedChannelMixer` to concatenate raw channels, explicit brightness-temperature-difference planes, and learned 1x1 projections.

Do not treat any fixed BTD shortlist as the whole search space. A good proposal states why the chosen input mode or channel mixer should improve thin-contrail recall, cloud-edge precision, threshold stability, or source transfer. Candidates remain free to ignore these utilities, preserve raw bands, add approved-channel BTD features, or learn channel combinations directly.

## Provider-owned boundaries

Candidate code may define model architecture and approved manifest choices, but must not own data loading, split logic, losses, metrics, Artifact Filters, Baseline Segmenter loading, or sampling policy implementation. These are trusted provider/harness responsibilities.

The v0 primary checkpoint metric is `val/filtered_dice`. Validation reporting keeps raw overlap metrics beside filtered metrics and reports Dataset Source-stratified metrics when both MIT and Google samples are present.

## Loss and auxiliary-target allowlists

Primary loss allowlist:

- `bce_dice`
- `focal_tversky`
- `bce_dice_cldice`

Auxiliary targets are manifest-declared and provider-derived from the Contrail Mask:

- `line` -> model output `line_logits`
- `boundary` -> model output `boundary_logits`
- `centerline` -> model output `centerline_logits`

Auxiliary outputs are shape-matched to `[1, 256, 256]`. The auxiliary loss allowlist is `weighted_bce`; weights must be declared in `manifest.yaml`.

Candidate-defined arbitrary losses, auxiliary labels, target transforms, or hidden objectives are not allowed. A new loss, auxiliary target, metric, Artifact Filter, sampling policy, or data source requires a Capability Request, human approval, trusted implementation in harness/problem-support code, and an allowlist update before candidate use.

## Data and split notes

Dataset Source is part of trusted sample metadata. Google patch membership follows train/validation provenance encoded in scene or file names. MIT full-scene sources are split by whole scene before 256 x 256 windowing to avoid leakage across adjacent patches from the same scene.

ABI projection and geolocation are important for interpreting diagnostics, but not for candidate inputs. Pixel size and viewing geometry vary across the GOES disk; profile artifacts should record projection caveats and source-specific count summaries for the local mounted snapshot.

## Baselines and evaluation context

MCAST Baseline Segmenters and provider-owned Artifact Filters are trusted comparison/evaluation components, not candidate-owned training code. Candidate experiments should compare against the current best validated run or an explicitly declared baseline family, and should inspect filtered/unfiltered metrics, source-stratified metrics, and false positive/false negative diagnostics rather than relying on a single aggregate score.

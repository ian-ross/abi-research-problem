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

Candidate code may define model architecture and approved manifest choices, but must not own data loading, split logic, losses, metrics, Artifact Filters, Baseline Segmenter loading, sampling policy implementation, or augmentation transforms. These are trusted provider/harness responsibilities.

Augmentation policy allowlist:

- `none`: no training-sample augmentation.
- `random_mirroring`: trusted harness/provider augmentation that randomly applies one of no flip, horizontal flip, vertical flip, or both-axis flip to each training sample. ABI input tensors and Contrail Mask targets are flipped together to preserve spatial alignment. Candidates may select this policy in the manifest, but candidate code must not implement its own data augmentation or target transforms.

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

Candidate-defined arbitrary losses, auxiliary labels, target transforms, augmentation transforms, or hidden objectives are not allowed. A new loss, auxiliary target, metric, Artifact Filter, sampling policy, augmentation policy, or data source requires a Capability Request, human approval, trusted implementation in harness/problem-support code, and an allowlist update before candidate use.

## Data and split notes

Dataset Source is part of trusted sample metadata. Google patch membership follows train/validation provenance encoded in scene or file names. MIT full-scene sources are split by whole scene before 256 x 256 windowing to avoid leakage across adjacent patches from the same scene.

ABI projection and geolocation are important for interpreting diagnostics, but not for candidate inputs. Pixel size and viewing geometry vary across the GOES disk; profile artifacts should record projection caveats and source-specific count summaries for the local mounted snapshot.

## Candidate resource and Experiment Batch policy

Read the generated Agent Workspace `AGENTS.md` for the current Harness-owned parallel Run cap and `/docs/abi-gpu-resource-profiling.md` for the reviewed ABI profiling protocol. Experiment Batches are appropriate only for two to four related, controlled variants whose architecture family, input shape, trusted loss, and effective batch size have comparable measured resource profiles. New or materially different architecture families must run sequentially until profiled.

Candidate code and Agent handoffs must not select GPUs, launch workers, set effective concurrency, or implement resource measurement/retry. The Harness currently pins reviewed ABI Candidate execution to the A100 profiling device and keeps batch execution sequential until an operator records safe concurrency evidence. If a hypothesis needs unavailable scheduling or concurrency, create a Capability Request rather than a Candidate-owned workaround.

## Baselines and evaluation context

Read `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json` for the current curated ABI snapshot, canonical MCAST 1.1/2.1, threshold, Artifact Filter, and ABI-025 manual-canary summaries. It is trusted summary context, not raw data, an unrestricted artifact root, or a new authoritative Run Result.

MCAST Baseline Segmenters and provider-owned Artifact Filters are trusted comparison/evaluation components, not candidate-owned training code. Candidate experiments should compare against the current best validated run or an explicitly declared baseline family, and should inspect filtered/unfiltered metrics, source-stratified metrics, and false positive/false negative diagnostics rather than relying on a single aggregate score.

SMP-style encoder-decoder architectures, including UNet- or MANet-like families, are acceptable as optional quick baselines or comparators because they align with existing Baseline Segmenter lineage. They are not preferred solutions, and the existing UNet/MANet baselines must not constrain the candidate search space. Strong candidates should also explore contrail-specific opportunities beyond generic segmentation backbones, such as thin-line continuity and connectivity, ABI spectral-channel interactions and brightness-temperature differences, robustness across MIT and Google Dataset Sources, calibrated threshold behavior, and artifact-aware false-positive suppression that does not move Artifact Filters into candidate code.

Acceptance-gate reports are provider-owned evaluation artifacts. They select the best available Baseline Segmenter by configured aggregate filtered Dice (or filtered IoU), compare the candidate on that metric, flag filtered-recall regressions beyond tolerance, include Contrail Connectivity Metric deltas, flag Dataset Source-specific catastrophic failures, and warn when a candidate appears excessively dependent on Artifact Filters. The report is an input to review only: final promotion remains a human decision.

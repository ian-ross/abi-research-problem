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

## Trusted capped-record selection

When the Harness requests `max_samples`, the provider applies that cap independently to each Dataset Source and each already-constructed Leakage-Safe Split. The fixed `abi_representative_scene_positive_hash` policy version `v1` (provider seed `20260812`) selects membership from trusted `ABIPatchIndexRecord` metadata; it does not truncate the raw record prefix. Candidates cannot choose, seed, override, or implement this policy, and `max_samples` remains a Harness execution ceiling rather than a manifest field.

For each source/split, the policy computes a prevalence-proportional positive-record quota while reserving at least one Contrail Mask-positive patch when one exists. When both positive and negative patches exist and the cap is at least two, it reserves both classes. A cap of one therefore chooses a positive patch when available. Within each class quota, deterministic hash ranks spread selection across MIT scene names or Google provenance scene names before selecting a second record from the same group. Positive coverage is allocated first; the negative quota prefers scene/provenance groups not already represented by the positive quota.

An absent cap, or a cap at least as large as the source/split population, retains every record and its existing order. Capped membership is ordered canonically after selection. This bounded-record policy is distinct from the manifest-selected training epoch sampling policy (`sequential`, `deterministic_shuffle`, or source-aware policies), which controls how the already-selected training dataset is traversed.

Run `data_policy` metadata records the requested and effective caps, policy identity/version and seed, available/selected source/split and positive/negative counts, distinct scene/provenance counts, and an order-independent SHA-256 digest of selected stable record identities. It does not disclose scene names, coordinates, raw samples, or an unrestricted selected-record list. The digest supports same-snapshot audit comparisons; it does not make a small deterministic subset statistically unbiased or guarantee transfer to a changed dataset snapshot.

## Architecture-family evaluation policy

A new or materially different architecture family starts sequentially unless the active trusted Workspace Configuration permits a profiled comparable resource class. A short resource pilot may be useful when resource compatibility is unknown, but it is not a mandatory authorization stage. Pilot loss or Dice is finite/resource evidence rather than architecture-ranking evidence.

Direct operator invocation of `autonomy-step` or `run-autonomous-iteration` is sufficient authority for in-contract research under the current generated Workspace ceilings. The Agent may preregister and choose learning rate, one trusted primary loss, one trusted augmentation policy, architecture, input mode, sampling traversal policy, optimizer, auxiliary targets, and other allowlisted Candidate fields. Candidate source cannot implement or redefine provider-owned loss, augmentation, data, sampling, metric, Artifact Filter, resource, or lifecycle behavior, and the generated Workspace ceilings remain authoritative.

Capped representative Runs use the fixed provider-owned selection semantics described above. Candidate code cannot select records or turn capped evidence into full-data evidence. Trusted epoch evidence includes aggregate and MIT/Google raw and filtered metrics, recent train-loss and filtered-Dice trends, and bounded raw/filtered predicted-positive counts and fractions. The provider-owned `abi_scout_assessment.v1` summary is conservative decision support: it reports finite/resource state, source behavior, trend direction, and persistent all-negative or all-positive prediction degeneracy. It does not apply strict top-k ranking or a single absolute-Dice elimination threshold.

Decisions are asymmetric. Hard execution failure, non-finite behavior, persistent prediction collapse, clear optimization failure, or convincing plateau/divergence at the active budget can support eliminating the exact branch. Low-scoring but improving, source-balanced, novel, noisy, or ambiguous finite trajectories remain eligible for continued bounded family development; low Dice alone is not an elimination rule. Do not abandon a substantially new architecture family after one untuned or lightly tuned regression against a mature incumbent.

Representative capped evidence is a feasibility screen, not a substitute for focused full-data evidence. Do not compare a capped score as though it were a full-data Result. If the operator activates larger trusted sample, epoch, timeout, scheduler, or early-stopping limits, invoking the research command is sufficient authority to use those limits; no separate research authorization record is required. The generated Agent Workspace Configuration remains authoritative for current sample, epoch, timeout, parameter, batch, prediction, scheduler, early-stopping, GPU, and concurrency limits.

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

Candidate-defined arbitrary losses, auxiliary labels, target transforms, augmentation transforms, or hidden objectives are not allowed. A new loss, auxiliary target, metric, Artifact Filter, sampling policy, augmentation policy, or data source requires a Capability Request or operator-directed change, trusted implementation in Harness/problem-support code, and an allowlist update before Candidate use.

## Data and split notes

Dataset Source is part of trusted sample metadata. Google patch membership follows train/validation provenance encoded in scene or file names. MIT full-scene sources are split by whole scene before 256 x 256 windowing to avoid leakage across adjacent patches from the same scene.

ABI projection and geolocation are important for interpreting diagnostics, but not for candidate inputs. Pixel size and viewing geometry vary across the GOES disk; profile artifacts should record projection caveats and source-specific count summaries for the local mounted snapshot. Capped-record selection never combines Dataset Sources or train/validation records, and it ranks only provider-owned record metadata after these boundaries have been established.

## Candidate resource and Experiment Batch policy

Read the generated Agent Workspace `AGENTS.md` for the current Harness-owned parallel Run cap and `/docs/abi-gpu-resource-profiling.md` for the reviewed ABI profiling protocol. Experiment Batches are appropriate only for two to four related, controlled variants whose architecture family, input shape, trusted loss, and effective batch size have comparable measured resource profiles. New or materially different architecture families must run sequentially until profiled.

Candidate code and Agent handoffs must not select GPUs, launch workers, set effective concurrency, or implement resource measurement/retry. The Harness pins reviewed ABI Candidate execution to the A100 profiling device. ABI-029 measured a safe Harness concurrency cap of two for comparable 2.54M-parameter, 16-channel, 256×256 spectral residual U-Net variants at effective batch size 8 or lower. This is a ceiling, not a target: unprofiled or materially different architectures, larger effective batches, and T4 execution remain sequential until separately profiled. If a hypothesis needs unavailable scheduling or concurrency, create a Capability Request rather than a Candidate-owned workaround.

## Baselines and evaluation context

Read `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json` for the current curated ABI snapshot, canonical MCAST 1.1/2.1, threshold, Artifact Filter, and ABI-025 manual-canary summaries. It is trusted summary context, not raw data, an unrestricted artifact root, or a new authoritative Run Result.

MCAST Baseline Segmenters and provider-owned Artifact Filters are trusted comparison/evaluation components, not candidate-owned training code. Candidate experiments should compare against the current best validated run or an explicitly declared baseline family, and should inspect filtered/unfiltered metrics, source-stratified metrics, and false positive/false negative diagnostics rather than relying on a single aggregate score.

SMP-style encoder-decoder architectures, including UNet- or MANet-like families, are acceptable as optional quick baselines or comparators because they align with existing Baseline Segmenter lineage. They are not preferred solutions, and the existing UNet/MANet baselines must not constrain the candidate search space. Strong candidates should also explore contrail-specific opportunities beyond generic segmentation backbones, such as thin-line continuity and connectivity, ABI spectral-channel interactions and brightness-temperature differences, robustness across MIT and Google Dataset Sources, calibrated threshold behavior, and artifact-aware false-positive suppression that does not move Artifact Filters into candidate code.

Acceptance-gate reports are provider-owned evaluation artifacts. They select the best available Baseline Segmenter by configured aggregate filtered Dice (or filtered IoU), compare the candidate on that metric, flag filtered-recall regressions beyond tolerance, include Contrail Connectivity Metric deltas, flag Dataset Source-specific catastrophic failures, and warn when a candidate appears excessively dependent on Artifact Filters. The report is an input to review only: final promotion remains a human decision.

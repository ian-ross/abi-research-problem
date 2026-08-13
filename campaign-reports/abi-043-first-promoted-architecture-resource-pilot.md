# ABI-043 first promoted architecture resource pilot

## Status and authorization

This report preregisters exactly one post-ABI-039 architecture-family resource pilot. The operator approved the ABI-043 implementation and execution plan in chat after confirming that `main` was pushed. That approval authorizes preparation, the trusted reduced-budget activation, and exactly one Autonomy Step with next-action execution after all preflight gates pass.

The only authorized primary outcome is one Candidate Submission for the family below and at most one Harness-owned Candidate Run. No second Autonomy Step, replacement Candidate, retry-driven second Run, direct `run-candidate`, non-dry-run open-action execution, Experiment Batch, Post-Run Evaluation, 12-epoch representative scout, 36-epoch extension, full-data training, promotion decision, concurrency change, or policy-limit increase is authorized.

## Preregistered Candidate family

Candidate identity target: `abi043_fullspectral_deeplabv3plus_resnet18_v1`.

Hypothesis: a randomly initialized, full-spectral DeepLabV3+ segmentation family with a ResNet-18 encoder can consume the provider-approved 16 ABI channels, complete the trusted batch-4 Candidate contract on pinned A100 GPU 0 with finite state and substantial timeout/memory headroom, and avoid gross all-negative/all-positive collapse during the one-epoch resource pilot.

This is materially different from both established ABI families:

- unlike the MCAST 1.1-lineage SMP U-Net, it consumes all 16 allowed ABI channels rather than three hand-derived planes and uses atrous spatial-pyramid context plus the DeepLabV3+ decoder instead of a symmetric U-Net decoder;
- unlike the custom spectral residual U-Net, it does not use that model's explicit brightness-temperature-difference concatenation, learned 1x1 spectral mixture, GroupNorm residual encoder, or dilated residual U-Net bottleneck/decoder.

The implementation should use `segmentation_models_pytorch.DeepLabV3Plus` with `encoder_name="resnet18"`, `encoder_weights=None`, `in_channels=16`, and `classes=1`, wrapped only as needed for fixed, preregistered per-channel normalization and exact `mask_logits` output. Static host validation measured 12,370,065 parameters and finite `(2, 1, 256, 256)` output for the unwrapped SMP topology. No pretrained download, file loading, Baseline Segmenter loading, longitude/latitude input, Candidate-owned data loading, loss, metric, Artifact Filter, sampling, optimizer loop, scheduling, device placement, retry, or lifecycle behavior is allowed.

## Controlled factors

Architecture and input representation are the only intended scientific changes relative to the ABI-031 reliability control. Keep:

- provider-owned `combined_source_balanced` sampling and `all_target_frames` selection;
- no augmentation;
- trusted `bce_dice` loss;
- AdamW with learning rate `0.001`;
- batch size 4;
- constant learning-rate policy and disabled early stopping;
- `abi_16ch` input indices 0-15 only and one `mask_logits` output;
- Docker execution pinned to A100 GPU 0, rootless-container-root mode, and global concurrency one.

Any fixed normalization constants must be declared in Candidate source and derived from already documented provider/campaign constants rather than pilot-record inspection. They are architecture preprocessing, not permission to select or inspect records.

## Trusted reduced budget

For this pilot the machine-local trusted Workspace Configuration is reduced from the general ABI-039 scout ceiling to:

- exactly 32 selected training records from each Dataset Source and its Leakage-Safe training split;
- exactly 32 selected validation records from each Dataset Source and its Leakage-Safe validation split;
- exactly one epoch;
- batch size at most 4;
- at most 25,000,000 parameters;
- four bounded `first_n` prediction artifacts;
- a 3,600-second trusted training timeout;
- one sequential Run on pinned GPU 0.

`max_samples = 32` is passed by the Harness to the ABI provider. The provider first constructs each Leakage-Safe Split and then applies `abi_representative_scene_positive_hash` version `v1`, seed `20260812`, independently per Dataset Source and split. Exactness requires preflight availability of at least 32 records in all four strata and terminal evidence that every selected count equals 32. Candidate schemas reject sampling controls, selectors, seeds, source-mixture overrides, and sample caps.

`max_epochs = 1` is trusted Workspace policy. Candidate manifests require at least one epoch and are rejected above the Workspace maximum, so the only accepted manifest value is one. The Candidate cannot own the training loop or raise this value.

The portable `ml-autoresearch.toml.example` continues to document the separately authorized 1,024/12 general scout ceiling. The ignored machine-local `ml-autoresearch.toml`, its generated Agent boundary, its runtime checksum, and terminal Run artifacts are the authoritative activation evidence for this one pilot.

## Success evidence

The pilot succeeds as contract/resource/finite/non-degeneracy evidence only if all of the following are recorded:

1. exactly one Candidate Submission, one stable Run identity, one container attempt, and exactly one terminal lifecycle event, with no retry, replacement, Evaluation, Batch, or unresolved action;
2. static and runtime contract validation pass, the model remains below 25 million parameters, receives only ABI source indices 0-15, and emits one correctly shaped logit mask;
3. one epoch completes with exactly 32 selected records in every MIT/Google train/validation stratum under the registered selector policy identity;
4. smoke, loss, gradients, parameters, metrics, checkpoint tensors, postprocessing, and resource profile are finite, with no non-finite diagnostic;
5. trusted evidence records throughput, wall-clock duration, peak CUDA allocation/reservation, batch compatibility, timeout state/headroom, and source-stratified metrics;
6. predicted-positive evidence is reported for aggregate, MIT, Google, and bounded prediction masks so all-negative/all-positive or source-specific collapse cannot be hidden by aggregate scores;
7. stable-Run reconciliation leaves no open action or managed container and repeated evidence inspection shows exactly-once lifecycle state.

A low Dice score does not fail this pilot by itself. One epoch over 32 records per source/split is not ranking, promotion, elimination, baseline-comparison, concurrency, or representative-scout evidence.

## Stop conditions

Stop for human review without retry, replacement, or continuation on any contract violation, coordinate exposure, missing required artifact, non-finite value, failed checkpoint audit, timeout or forced termination, OOM, resource retry, second Run, duplicate lifecycle event, unexpected GPU/container state, unresolved action, source/split selection count other than 32, selector-policy mismatch, or inability to establish clean pushed identities and synchronized authorization before launch.

Gross all-negative/all-positive or source-specific collapse is recorded as pilot non-degeneracy evidence and stops automatic continuation, but does not authorize eliminating the architecture family from a one-epoch score alone. Even a fully passing pilot stops before the 12-epoch representative scout. Any scout, extension, full-data training, promotion, or policy change requires its own applicable authorization.

## Preflight and execution record

Pending. Before execution this section must record clean pushed ABI and Harness revisions, validated runtime identities, generated boundary values, named-root availability, source/split counts, no open action, no managed container, idle pinned A100 GPU 0, and immutable before-counts. Exactly one `uv run ml-autoresearch autonomy-step --workspace-root . --execute-next-action` may then be invoked.

## Run evidence and interpretation

Pending. This section will record the stable Candidate/Run identities, exactly-once lifecycle, selected-record policy/counts, finite/checkpoint audit, resources, source metrics, predicted-positive state, timeout headroom, and the explicit non-ranking interpretation.

## Validation, independent review, and residual risks

Preparation validation and independent review are pending. Known residual risks before execution are that DeepLabV3+ uses BatchNorm and must be validated with the trusted batch/smoke path; one epoch may be too short for meaningful masks; exact 32 depends on all four mounted strata retaining at least 32 records; and structural retry support must produce zero retries because replacement execution is forbidden.

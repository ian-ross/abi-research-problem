# Agent instructions for the ABI Research Problem Workspace

## Domain context

Read `CONTEXT.md` for the GOES ABI Contrail Segmentation ubiquitous language. Read `abi_contrail/brief/` and `abi_contrail/profile/` for Research Problem background, Dataset Profile context, and current research guidance.

Use `../ml-autoresearch` as the Harness reference and integration target.

## Operator-invoked autonomous research

This workspace is commissioned for autonomous research. Direct operator invocation of either command is sufficient authority for the bounded work performed by that command:

```bash
uv run ml-autoresearch autonomy-step --workspace-root . --execute-next-action
uv run ml-autoresearch run-autonomous-iteration --workspace-root . --max-steps <N> --notify-email <address>
```

The active Workspace Configuration and Research Problem Spec define the available actions and their trusted resource, data, sampling, coordinate, loss, metric, Artifact Filter, execution, and lifecycle bounds. Candidate source, Candidate manifests, and Agent handoffs cannot raise or bypass those bounds.

An explicit `campaign_paused` ledger state stops autonomous iteration until the operator records a resume. `stop_for_human`, Capability Requests, Campaign Reports requesting review, non-finite state, contract violations, timeouts, lifecycle inconsistencies, missing artifacts, and Harness failures stop or bound the current command according to Harness semantics. Caller disconnection does not create authority for a duplicate or replacement Run; observe and reconcile the stable Run identity. Promotion, deployment, and production claims remain operator decisions.

## Experiment index maintenance

Update `EXPERIMENT_INDEX.md` whenever a new Candidate Experiment is introduced or a new Research Note is written. Keep current policy at the top of the index.

## ABI architecture research policy

The generated Workspace Configuration defines the current sample, epoch, batch, parameter, timeout, prediction, scheduler, early-stopping, GPU, and concurrency limits. A research command may use any in-contract values at or below those limits.

Treat first attempts at materially different architecture families as scouts rather than final verdicts. Do not abandon a substantially new family after one untuned or lightly tuned regression against a mature incumbent. Low score alone is not elimination evidence when a finite trajectory is improving, source-balanced, novel, noisy, or ambiguous. Prefer bounded family development and source-stratified, non-degeneracy, trajectory, and failure-mode evidence before making comparative claims.

Representative capped Runs are feasibility evidence rather than full-data promotion evidence. Candidate code cannot alter trusted limits or reinterpret capped evidence as full-data evidence.

Current comparator roles from the latest indexed campaign state:

- **ABI-202** remains the aggregate whole-validation filtered-Dice reference.
- **ABI-249** is the high-precision, compact-prediction C4/rotation-aware comparator.
- **ABI-223** is the temporal-family diagnostic comparator on the temporal-eligible validation population.
- **ABI-253** is the compact line-memory U-NetFormer comparator, not a frontier target.
- **ABI-255** is the compact recurrent temporal comparator, with unresolved thin-line continuity weaknesses.
- **ABI-265** is the selective axial line-memory comparator, useful for connectivity evidence but not a new frontier.
- **ABI-269** is the compact spectral/Solar Geometry Input MoE late-budget comparator; it is not a promotion candidate.

Do not spend Runs on unchanged late36 continuations of ABI-253, ABI-255, ABI-265, or ABI-269. Future work in those areas should be mechanism-changing, resource-aware, and explicitly tied to the observed failure mode.

## Underexplored architecture directions

The campaign has now covered many broad scouts: provider-owned temporal models, C4/rotation-aware line context, Radon/line accumulation, modern compact attention backbones, spectral/SZA mixture-of-experts, and axial line-memory variants. Prefer a new Run only when it states a specific mechanism for improving fixed-threshold recall, MIT/source balance, negative-patch clutter, or connected thin-line continuity against the current comparators. High-value in-contract directions now include:

- **C4/orientation prior plus recall/connectivity support**: combine ABI-249's compact high-precision rotation-aware behavior with center-frame detail, cross-scale support, or evidence-raising heads that recover recall and connectivity without candidate-owned thresholding or postprocessing.
- **Temporal attention with architecture-level evidence sharpening**: build from ABI-223-style provider-owned temporal attention, but raise true contrail logits at threshold 0.5 while preserving precision, source balance, and connectivity. Matched controls should continue to use trusted temporal-eligible selection.
- **Line-continuity mechanisms with bounded cost**: differentiable line accumulation, selective axial/C4 line memory, or orientation consensus may continue only when the hypothesis targets connected-line failure modes and avoids repeating an already characterized exact branch.
- **Recall-preserving calibration or dual-evidence heads**: compact logits, dual-head agreement, uncertainty-like consensus, or calibration-style architecture heads are useful if they raise true positives without Candidate-owned thresholds, losses, metrics, or postprocessing.
- **Modern lightweight segmentation backbones**: compact SegFormer/UNetFormer/Swin/MaxViT-like families remain valid only when the proposal explains how it will improve on ABI-253/262 rather than merely adding attention capacity.
- **Spectral/illumination mixture-of-experts with line continuity**: MoE work should explicitly recover connected-line evidence; generic spectral/SZA gating alone has not displaced ABI-202/249.

Temporal Candidate manifests should request the trusted temporal mode and an allowlisted offset window, for example:

```yaml
input_mode: abi_16ch_plus_sza_temporal
data:
  frame_selection_policy: temporal_eligible_center
  temporal_frame_offsets: [-1, 0, 1]
```

Allowed temporal windows are `[0]`, `[-1, 0, 1]`, and `[-2, -1, 0, 1, 2]`. The tensor is channel-stacked in ascending offset order with 17 channels per frame: ABI channels 1-16 plus that frame's Solar Geometry Input. The target Contrail Mask is always the zero-offset center ABI Patch. Matched single-frame controls should use `input_mode: abi_16ch_plus_sza` with `data.frame_selection_policy: temporal_eligible_center`, not candidate-side filtering.

These suggestions do not relax the Research Problem contract. Candidate code must not discover S3/NetCDF objects, download, load, select, pad, duplicate, or repair temporal frames; it may only consume provider-advertised tensors and define architecture over those tensors. New materially different families, especially temporal or attention-heavy models, should run sequentially until resource behavior is profiled.

## Trusted provider and Candidate boundary

- Candidate models must never receive longitude or latitude inputs. These encourage route-location priors and reduce transferability.
- Candidate code must not own data loading, loss definitions, metric definitions, Artifact Filters, Baseline Segmenter loading, target derivation, augmentation implementation, or sampling policies. These belong in trusted provider or Harness code.
- Candidate manifests may select only provider-advertised input modes, losses, augmentations, schedulers, auxiliary targets, and other allowlisted fields.
- New trusted capabilities require a Capability Request or operator-directed provider/Harness implementation and an allowlist update before Candidate use.
- The `data` symlink points to external training data and may not exist in every environment. Unit tests should use tiny fixtures unless explicitly marked as data-dependent integration tests.

## Python and uv execution safety

This repository is uv-managed.

- Use `uv` for dependency management.
- Run Python through uv, for example `uv run python ...`.
- Do not run bare `python ...` commands.
- Prefer `uv run pytest ...` or other `uv run ...` forms for project tools.

Do not run `uv run`, `uv sync`, or other virtual-environment-mutating commands from this repository when it is mounted inside a Fort/Gondolin VM. The host `.venv/` is not portable into the VM and may be damaged if uv attempts to repair it.

If an operator explicitly asks you to run `uv` against this workspace from inside a VM, force uv to use a VM-local environment outside the mounted repository, for example:

```bash
UV_PROJECT_ENVIRONMENT=/tmp/abi-research-problem-venv uv run ...
```

Inside the Agent Control Boundary, prefer `ml-autoresearch-agent` commands from the Agent Workspace rather than host-style `uv run` commands.

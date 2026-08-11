# ABI-031 MCAST-lineage positive-control protocol

## Status and authorization boundary

This is the Phase 0 preregistration draft for ABI-031. ABI-030 and ABI-032 are complete. Approval of this protocol authorizes trusted Harness/provider changes, Candidate authoring, and controlled non-data checks only. It does **not** authorize the A100 resource pilot, bounded main Run, Working Validation evaluation, or an automatic autonomy iteration; those remain separately human-gated.

## Positive-control hypothesis

A manually authored, randomly initialized MCAST 1.1-lineage architecture should train through the trusted Candidate Execution path with finite state and produce non-degenerate predictions on the canonical Working Validation Split. This tests Candidate Execution reliability independently of the failed ABI-025 Agent-generated architecture. Beating canonical MCAST 1.1 or 2.1 is not required.

## Candidate architecture and boundary

The canonical Candidate will be `abi031_mcast11_positive_control_v1` and contain only `manifest.yaml`, `model.py`, `PROPOSAL.md`, and `README.md`.

`model.py` will:

- require the provider-declared `abi_16ch` input contract `[16, 256, 256]`;
- derive exactly three planes from candidate-input positions: C11 = index 10, C14 = index 13, and C13-C15 = index 12 minus index 14;
- normalize those planes with the MCAST 1.1 constants:
  - means: `[274.15866814464114, 275.74145854126134, 3.05802131633268]`;
  - standard deviations: `[18.369019656652068, 19.497045505465557, 1.8518705027433054]`;
- instantiate `segmentation_models_pytorch.Unet` with `encoder_name="resnet18"`, `encoder_weights=None`, `in_channels=3`, and `classes=1`;
- return one `[B, 1, 256, 256]` `mask_logits` tensor.

The expected parameter count is **14,328,209**. Random initialization is mandatory: the Candidate will not load a checkpoint, call the Baseline Segmenter, read files, resolve a data root, or access the MCAST asset. The source will contain no longitude/latitude handling and can receive only source indices 0-15 through `abi_16ch`; provider source indices 16 and 17 remain forbidden.

The manifest requests only provider/Harness-owned policies:

- sampling: `combined_source_balanced`;
- frame selection: `all_target_frames`;
- augmentation: `none`;
- loss: `bce_dice`;
- optimizer: `adamw`;
- learning rate: `0.001`;
- canonical batch size: `4`, subject to the pilot gate;
- canonical maximum epochs: `3`.

Candidate code will not own data loading, targets, loss computation, metrics, Artifact Filters, Baseline Segmenters, sampling, augmentation, optimization, device placement, retries, execution, or evaluation.

## Provider-owned parameter budget

The present smoke limit is a hard-coded Harness constant of 10,000,000 parameters, while the reviewed model has 14,328,209 parameters. The proposed policy is not a Candidate-specific exception and does not remove the guard:

1. Add trusted Workspace Configuration `candidate_execution.max_parameters`.
2. Keep the Harness default at 10,000,000 for unconfigured workspaces.
3. Configure the ABI workspace at **25,000,000**, covering this model and similarly scaled common segmentation models without matching one exact architecture.
4. Enforce a Harness configuration ceiling of **100,000,000**; larger budgets require a reviewed Harness change rather than an arbitrary config value.
5. Pass the trusted effective budget through native and Docker smoke paths and record it beside the measured count in `model_summary.json`.
6. Candidate manifests and Candidate code cannot declare, select, or raise this value.
7. Parameter count does not confer a resource class. New or materially different models remain sequential and require measured resource evidence regardless of count.

The ABI runner must also add pinned `segmentation-models-pytorch==0.5.0` and compatible `torchvision` support as trusted runtime dependencies. The current validated ABI runner does not contain SMP, so it cannot be used for ABI-031. A new runner will be built and validated from clean Harness/provider commits before Candidate execution.

## Controlled pre-execution checks

Before any real-data authorization:

1. Run static Candidate validation with proposal and README requirements.
2. Audit the complete Candidate source and imports for file I/O, checkpoint loading, baseline imports/root access, coordinates, and forbidden policy ownership.
3. Verify the exact channel formulas, constants, SMP arguments, random initialization claim, output contract, and expected parameter count.
4. Run zero-input and deterministic random-input forward/backward checks with finite output, loss, gradient, and parameter assertions.
5. Exercise the managed smoke path in the rebuilt Docker runner and verify `model_summary.json` records 14,328,209 against the trusted 25,000,000 budget.
6. Run a tiny provider-owned fixture training test without external ABI data, asserting finite state, output shape, checkpoint readability, and no Candidate-owned training behavior.
7. Run focused Harness parameter-budget/smoke tests, the Harness suite required by the change, and the ABI unit suite.

Any failure returns to human review. Controlled checks do not automatically start the pilot.

### Gate 1 controlled-check evidence

Human Gate 1 approved controlled non-data checks on 2026-08-11. No external ABI data or GPU training was used.

- Reviewed Candidate checksum: `33a410b52aaac2ea207c8b112965d9099781da8e295e0d421dbd08e85d01b103`.
- Static Candidate validation with required proposal and README: valid.
- Source/import boundary, exact MCAST constants and channel formulas, 14,328,209 parameter count, output contract, zero/random finite forward/backward, one trusted `bce_dice`/AdamW fixture step, and finite checkpoint reload: 4 tests passed.
- Pilot preparation and positive-control report fixtures: 3 tests passed.
- Full ABI suite: 111 passed.
- Harness focused parameter/smoke/runner tests: 49 passed; broader focused set: 104 passed.
- Full Harness suite: 563 passed, 2 skipped, with one known unrelated external GVCCS characterization failure (`focal_bce_dice` in a committed external Candidate versus that test's fake Spec allowing only `bce_dice`).
- Clean Harness commit `0524fdd` built runner `ml-autoresearch-runner:abi-research-problem-46ee69c350b0a037-13b99524f1`; runtime-image validation passed with Workspace Configuration SHA-256 `1e3d1e466fefd20de74a6d63396f9add28d149ce23f438d1ea71a3a1068aafea`.
- Runner dependency probe: SMP 0.5.0, torch 2.5.1+cu121, torchvision 0.20.1+cu121.
- Isolated Docker smoke Run `run_20260811_154950_b78993` was accepted without data/training; its copied source checksum matches Gate 1, output is finite `[2,1,256,256]`, and `model_summary.json` records 14,328,209 parameters against the trusted 25,000,000 limit with only ABI source indices 0-15 and explicit longitude/latitude exclusion.

This evidence authorizes review for Gate 2 only. It does not authorize the A100 pilot.

### Gate 2 first pilot attempt

Human Gate 2 authorized one pilot on 2026-08-11. Run `run_20260811_155607_5a9ea1` used the reviewed byte-identical one-epoch derivative, 32 train and 32 validation samples per Dataset Source, batch size 4, A100 device 0, and no concurrent GPU process. Training and validation completed once with finite losses/metrics and a finite checkpoint, but the Run failed during bounded qualitative-artifact selection because the preregistered `adjacent_and_scattered` Harness policy is not implemented by the ABI training adapter.

- 64 training and 64 validation samples processed; no Resource Failure retry.
- Train loss `1.7150806487`; validation loss `2.0541212559`.
- Raw/filtered validation Dice `0.0083816075` / `0.0085124956`.
- Google raw/filtered Dice `0.0013947959` / `0.0013873153`; MIT raw/filtered Dice `0.0169016537` / `0.0175550567`.
- Checkpoint: 184 tensors, 14,339,829 tensor values, all finite.
- Peak CUDA allocated/reserved: 571,703,808 / 664,797,184 bytes; free at start 41,855,287,296 bytes.
- Training/validation throughput: 47.878 / 0.982 samples/s; measured operation wall time 68.30 seconds.
- Exactly one `run_failed` event remained after two reconciliations; container cleanup completed and no duplicate Run was launched.
- Missing outputs: `final_metrics.json` and qualitative prediction artifacts. The late trusted-policy failure was incorrectly classified `candidate_bug`; Candidate source did not cause it.

Per the preregistered stop rule, no repair or second pilot was launched. Gate 2 review chose the minimal correction: retain the failed Run as evidence and authorize one deliberate replacement using the already-supported trusted `first_n` policy. Full Working Validation diagnostics retain their separate provider-owned failure-bucket selection.

### Gate 2 replacement pilot result

Human review authorized the replacement, and Run `run_20260811_160407_9067ea` completed exactly once on 2026-08-11.

- Reviewed canonical/pilot Candidate tree checksums: `33a410b52aaac2ea207c8b112965d9099781da8e295e0d421dbd08e85d01b103` / `1e2f1f364b5822f2f7f84da3f299d90a1f1886f6d6b785c561aaa665efde654e`; canonical and pilot `model.py` SHA-256 both `f40b484c079b31a30287d3d4b521d26712ee295995e365349fe0c674700ae854`.
- Status `completed`; exactly one `run_completed` event remained after two reconciliations; one container attempt exited successfully and cleanup removed it.
- 64 training and 64 validation samples processed at batch size 4 with no retry.
- All 45 numeric epoch metrics were finite. Train/validation loss: `1.7227236778` / `4.6490467936`.
- Aggregate raw/filtered Dice: `0.0063185547` / `0.0062221879`; Google: `0.0020787475` / `0.0020476661`; MIT: `0.0138359561` / `0.0140604148`.
- The selected checkpoint contained 184 tensors and 14,339,829 tensor values, all finite.
- Four bounded prediction masks contained 48,530 positive and 213,614 negative pixels in total; every sample contained both classes.
- Peak CUDA allocated/reserved: 568,427,008 / 664,797,184 bytes (about 1.6% of 40 GiB reserved), with 41,855,287,296 bytes free at start.
- Training/validation throughput: 56.974 / 0.984 samples/s; measured operation wall time 68.31 seconds.
- Required final metrics, best metrics/checkpoint, model summary, resource profile, and four bounded qualitative artifact sets are present. Training, ancillary, and baselines mounts are recorded read-only; the model summary records ABI source indices 0-15 and excludes longitude/latitude.

The pilot meets its numerical, resource, artifact, provenance, and lifecycle criteria. Batch size 4 is recommended for Gate 3. The main Run remains unauthorized. Because ABI still does not support `adjacent_and_scattered`, the proposed main command below is corrected to `first_n`; Gate 3 must explicitly approve that correction.

## Sequential A100 resource pilot

After a separate execution approval, prepare an operator-authored pilot derivative that keeps `model.py` byte-for-byte identical and changes only Candidate identity and `max_epochs` to 1. Use no Experiment Batch and no concurrent GPU work.

Preflight:

```bash
nvidia-smi --query-gpu=index,name,memory.total,memory.used --format=csv
uv run ml-autoresearch validate-runtime-images --workspace-root .
```

Launch through the managed detached lifecycle using the newly validated configured runner:

```bash
uv run ml-autoresearch run-candidate \
  --candidate /tmp/abi031-positive-control-pilot \
  --workspace-root . \
  --max-samples 32 \
  --max-prediction-samples 4 \
  --prediction-sample-policy first_n \
  --detach
```

`first_n` is the reviewed correction after the original `adjacent_and_scattered` attempt failed during trusted artifact selection. Retain the returned Run ID and only observe/reconcile that Run:

```bash
uv run ml-autoresearch run-status --workspace-root . --run-id <PILOT_RUN_ID>
uv run ml-autoresearch reconcile-run --workspace-root . --run-id <PILOT_RUN_ID>
```

The configured backend must resolve to Docker, A100 device 0, rootless-container-root ownership, and the ABI-031 validated runner. The pilot uses 32 training and 32 validation samples **per Dataset Source**, one epoch, batch size 4, and at most four qualitative samples. Expected wall time is approximately 3-10 minutes; this is an estimate, not a timeout.

Pilot acceptance requires:

- exactly one managed Run and one terminal ledger event;
- no duplicate submission, Resource Failure retry, or non-finite diagnostic;
- all logged losses and metrics finite;
- all checkpoint parameters finite;
- processed counts of 64 training and 64 validation samples;
- raw predictions contain both positive and negative pixels across the bounded validation evidence;
- recorded effective batch size, peak allocated/reserved memory, throughput, wall time, mount policy, model summary, Candidate checksum, and container cleanup;
- peak reserved/process GPU memory at or below 70% of the 40 GiB A100 with at least 8 GiB free.

An OOM, automatic batch-size retry, non-finite failure, all-constant prediction, missing artifact, or lifecycle inconsistency stops the campaign for review. Pilot success does not automatically launch the main Run. Human review selects batch size 4 or a lower measured value.

## Bounded positive-control Run

After pilot review and explicit approval, launch the canonical three-epoch Candidate sequentially:

```bash
uv run ml-autoresearch run-candidate \
  --candidate candidates/abi031_mcast11_positive_control_v1 \
  --workspace-root . \
  --max-samples 1024 \
  --max-prediction-samples 4 \
  --prediction-sample-policy first_n \
  --detach
```

The provider applies the cap per Dataset Source: at most 2,048 combined training samples and 2,048 combined validation samples per epoch, for at most three epochs. Expected wall time is approximately 2-4 hours based on ABI-025 validation throughput; no caller-side timeout authorizes relaunch. Status and idempotent reconciliation use only the returned Run ID.

Before evaluation, the terminal Run must have exactly one terminal event, finite logged train/validation metrics, a finite readable best checkpoint, a complete resource profile, correct sample/source counts, expected read-only mounts, no forbidden coordinate inputs, the reviewed Candidate source checksum, and bounded qualitative artifacts. Any non-finite or non-degenerate prerequisite failure blocks evaluation pending human review.

### Gate 3 main Run result

Human Gate 3 authorized the corrected `first_n` command, and Run `run_20260811_160920_07a7f4` completed exactly once on 2026-08-11.

- Canonical source and immutable Run snapshot both have Candidate tree SHA-256 `33a410b52aaac2ea207c8b112965d9099781da8e295e0d421dbd08e85d01b103`.
- Three epochs processed 6,144 training and 6,144 validation observations in total (2,048 per split per epoch; 1,024 from each Dataset Source), with batch size 4 and no retry.
- All 6,279 numeric values across 1,539 metric records were finite. Epoch 3 was selected with train/validation loss `0.9831224490` / `1.0004627658`.
- Selected raw/filtered Dice: aggregate `0.1070328316` / `0.1028192765`; Google `0.0768765897` / `0.0750351272`; MIT `0.1194279187` / `0.1142849159`.
- The selected epoch-3 checkpoint contains 184 tensors and 14,339,829 tensor values, all finite.
- Four bounded prediction masks contain 403 positive and 261,741 negative pixels; every mask contains both classes.
- Peak CUDA allocated/reserved: 568,427,008 / 666,894,336 bytes, with 41,855,287,296 bytes free at start.
- Total measured operation wall time was 8,047.34 seconds. Training processed 6,144 observations in 49.21 seconds (124.86/s); legacy CPU validation/postprocessing processed 6,144 in 7,995.87 seconds (0.768/s).
- Exactly one `run_completed` event remains after two reconciliations. The sole container exited 0, was removed, and left GPU 0 with no process/memory allocation.
- Final/best metrics, checkpoint, model summary, completed resource profile, logs, and four bounded qualitative artifact sets are present. Data/baseline/ancillary mounts are recorded read-only, and the model summary excludes longitude/latitude.

The main Run satisfies the finite, non-degenerate training prerequisites for Gate 4 review. It does not itself establish the full positive-control hypothesis. The unexpectedly opaque and slow CPU-only epoch postprocessing path is tracked as `ABI-033`; it did not alter the completed Run's trusted metric semantics. Canonical Working Validation evaluation remains separately human-gated.

## Canonical Working Validation evaluation

After a separate evaluation approval, evaluate the completed checkpoint once without retraining:

```bash
uv run ml-autoresearch evaluate-run \
  --run /data/iross/abi-ml-autoresearch/runs/<MAIN_RUN_ID> \
  --split val \
  --backend docker \
  --docker-image <ABI031_VALIDATED_RUNNER_IMAGE> \
  --docker-enable-gpu \
  --docker-rootless-container-root \
  --workspace-root . \
  --max-artifact-samples 4 \
  --ledger-path research-ledger.jsonl
```

The evaluation must contain all 3,088 canonical Working Validation samples (MIT 1,232; Google 1,856), use registry `abi-mcast-working-validation-v1`, apply the provider-owned raw and ordered Artifact-Filtered assessment, and write no more than four diagnostic samples/eight GeoTIFFs. Expected wall time is approximately 5-15 minutes.

After evaluation, generate both the ordinary promotion-oriented acceptance report and the separate preregistered positive-control report using the Candidate checksum approved at Gate 1:

```bash
uv run abi-positive-control-report \
  --workspace-root . \
  --run /data/iross/abi-ml-autoresearch/runs/<MAIN_RUN_ID> \
  --evaluation /data/iross/abi-ml-autoresearch/runs/<MAIN_RUN_ID>/outputs/evaluations/<EVALUATION_ID> \
  --ledger research-ledger.jsonl \
  --expected-candidate-sha256 <GATE1_CANDIDATE_SHA256>
```

## Preregistered positive-control decision criteria

A new provider-owned `positive_control_report.json` will report these criteria separately from the ordinary promotion-oriented `acceptance_report.json`. Ordinary acceptance flags for not beating MCAST do not by themselves fail this positive-control hypothesis.

The hypothesis passes only if all of the following are true:

1. Required Run/evaluation metrics and every logged train/validation loss are finite.
2. Every tensor in the selected checkpoint contains only finite values.
3. `raw/predicted_positive_pixel_count` is between **0.001% and 10%** of the 202,375,168 evaluated pixels (inclusive), i.e. **2,024 through 20,237,516** pixels.
4. `filtered/predicted_positive_pixel_count` is greater than zero and no greater than the raw count.
5. Aggregate `raw/dice` and `filtered/dice` are each greater than **0.0001**, well above the observed all-negative numerical floor (~1e-13) while remaining a reliability rather than promotion threshold.
6. MIT and Google `raw/dice` and `filtered/dice` are each greater than **0.0001**.
7. Required Run, evaluation, model summary, resource, threshold-sweep, bounded diagnostic, canonical-registry, source-stratified, Research Ledger, index, and provenance artifacts are present and consistently linked.
8. Run source and provenance prove random initialization and no MCAST checkpoint/baseline-root access by Candidate code.

The report records every observed value and an explicit pass/fail reason. A failed hypothesis remains a valid durable experimental outcome and blocks resuming fully automatic autonomy planning. Passing does not promote the Candidate, claim parity with MCAST, or launch autonomy.

## Human gates

- **Gate 0 — protocol/design:** approve architecture, ABI-wide 25M trusted budget, 100M config ceiling, runtime dependency addition, training policy, thresholds, commands, bounds, and artifacts.
- **Gate 1 — source/control review:** review the exact Candidate and trusted Harness/provider diff; authorize controlled checks only.
- **Gate 2 — pilot execution:** review controlled evidence and authorize one bounded A100 pilot.
- **Gate 3 — main execution:** review pilot resource/numerical evidence and select batch size; authorize one bounded main Run.
- **Gate 4 — evaluation:** review terminal training evidence and authorize one canonical Working Validation evaluation.
- **Gate 5 — campaign decision:** decide whether Candidate Execution is trustworthy enough to resume planning for fully automatic autonomy. This gate never launches an iteration.

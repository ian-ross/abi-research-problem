# ABI-035 first bounded autonomous Candidate Run

## Decision and scope

Human Gate 0 authorized exactly one execution of the existing open `run_candidate` action for `abi032_mcast11_focal_tversky_v1`. The authorization explicitly forbade duplicate submission, automatic retry, a replacement Run, a second Candidate, Post-Run Evaluation, or another Autonomy Step.

The preregistered protocol is [`abi-035-first-bounded-autonomous-candidate-protocol.md`](abi-035-first-bounded-autonomous-candidate-protocol.md). This report reviews Run `run_20260812_121722_8d6cd3` against that protocol. It is directional autonomy/reliability evidence only, not promotion-grade scientific evidence.

## Launch identity and exactly-once execution

Immediately before execution:

- ABI HEAD was clean, pushed commit `51126c4740e45fb11c22b0567f273f392e61b6ca` with zero upstream divergence;
- Harness HEAD was clean, pushed commit `a38ad742e187e23b1fa13f7b0ec8bd21da7ad637` with zero upstream divergence;
- runtime validation passed at `2026-08-12T12:17:18Z` for Harness fingerprint `4ee2c56b94e3a8e8`, runner `ml-autoresearch-runner:abi-research-problem-4ee2c56b94e3a8e8-13b99524f1`, and Workspace Configuration SHA-256 `28586fdcc017ae955829f8658f6baa407910434645417e92f4e4d2bf0a23a430`;
- static Candidate validation passed;
- the A100 on GPU 0 had 0 MiB in use, no compute process, and no managed container;
- counts were 12 Runs, 3 Evaluations, and 74 Research Ledger events;
- the dry run still showed exactly one open action: ledger index 73, `run_candidate`, Candidate `abi032_mcast11_focal_tversky_v1`, canonical path `candidates/abi032_mcast11_focal_tversky_v1`.

The authorized command was invoked exactly once:

```bash
uv run ml-autoresearch execute-next-action --workspace-root .
```

It returned a stable managed Run identity and changed the handoff's next action to `reconcile_run`:

- Run ID: `run_20260812_121722_8d6cd3`;
- initial Run status: `training`;
- managed state: `supervisor_running`;
- supervisor PID: `3824771`;
- Run directory: `/data/iross/abi-ml-autoresearch/runs/run_20260812_121722_8d6cd3`.

No launch command was invoked again. The same Run ID was observed with `run-status`. After its sole container exited, `reconcile-run` was invoked twice against that Run ID. Both reconciliations returned `completed`, retained the same container lineage, and did not add a terminal event. The final dry run reports no open Harness action.

## Candidate and trusted policy

The immutable Run snapshot has Candidate tree SHA-256 `fbcf6294e7350286bfa734382d63b45ad0ed466f86d6e359b07253fdf6adf333`, equal to the reviewed canonical tree. `model.py` SHA-256 is `e9b6b3bba8de5f5a1f1ea89039b0742f0b08af0f6003d1e2b3b0825ec221518b`.

The resolved manifest records clean ABI commit `51126c4740e45fb11c22b0567f273f392e61b6ca`, trusted `focal_tversky`, AdamW at 0.001, batch size 4, three epochs, `combined_source_balanced`, all target frames, and no augmentation. The executable architecture remains the ABI-031 MCAST 1.1-lineage model apart from Candidate/class names and docstrings. Random initialization uses `encoder_weights=None`.

The model summary records 14,328,209 parameters against the trusted 25,000,000 limit. It accepts only `abi_16ch` source indices 0-15 and explicitly forbids longitude, latitude, and provider source indices 16 and 17. Candidate code owns no data loading, loss, metrics, Artifact Filters, Baseline Segmenter loading, sampling, optimization, retries, device policy, or training loop.

## Bounds and lifecycle evidence

The trusted detached command recorded in `execution.json` used:

- Docker runner `ml-autoresearch-runner:abi-research-problem-4ee2c56b94e3a8e8-13b99524f1`;
- GPU enabled and pinned device `0`;
- rootless-container-root mode;
- `--max-samples 128`, applied separately by the provider to each Dataset Source;
- `--max-prediction-samples 2` and `first_n`;
- the Workspace-owned 1,800-second timeout with 30-second graceful-stop allowance.

The Run completed all three epochs. Each epoch contained 256 training and 256 validation observations: exactly 128 MIT plus 128 Google observations under the provider's per-source limiting implementation. Total processed counts were 768 training and 768 validation observations. Batch size remained 4.

Exactly one container attempt, `ml-autoresearch-run_20260812_121722_8d6cd3-e46122c81c40`, exited 0 and was removed. Container cleanup is `completed`; failure classification, rejection, smoke failure, and training failure are null. Resource retry count is zero and the sole batch-size attempt completed at batch 4. No timeout request, graceful timeout termination, forced termination, OOM, replacement Run, or concurrent workload occurred. The measured Run operation took 40.47 seconds, well below 1,800 seconds.

The Research Ledger contains exactly one event each for this Run:

- line 77: `candidate_submitted`;
- line 78: `run_started`;
- line 79: `run_completed`.

There is no `run_failed` event. Two subsequent reconciliations left the lifecycle ledger at 79 lines. Registering this report then added line 80, one `campaign_report_written` event linked to this path. Counts are now 13 Runs and 3 Evaluations; no evaluation ran.

## Numerical and non-degeneracy evidence

A recursive audit parsed 207 JSON/JSONL records, including all 195 metric records, and checked 1,202 numeric values; all were finite. Trusted smoke/training per-step finite checks completed without `outputs/nonfinite_diagnostic.json`, covering outputs, losses, gradients, and parameters during execution.

The selected checkpoint loaded on CPU and contained 184 tensors and 14,339,829 tensor values; all were finite.

Selected epoch-3 metrics:

| Stratum | Raw Dice | Filtered Dice | Raw precision | Filtered precision | Raw recall | Filtered recall | Filtered connectivity |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Aggregate | 0.047163 | 0.046177 | 0.025538 | 0.025067 | 0.307862 | 0.292515 | 0.066445 |
| Google | 0.021358 | 0.021273 | 0.010940 | 0.010903 | 0.447091 | 0.435689 | 0.040031 |
| MIT | 0.091874 | 0.090302 | 0.055208 | 0.054763 | 0.273551 | 0.257231 | 0.092858 |

Every raw/filtered aggregate and source Dice is greater than the preregistered `0.0001` floor. Every source/aggregate raw and filtered precision and recall is finite and strictly between zero and one, ruling out aggregate and source all-negative/all-positive behavior.

Both bounded binary predictions contain both classes:

- `sample_000_prediction.png`: 25 positive and 65,511 negative pixels;
- `sample_001_prediction.png`: 9 positive and 65,527 negative pixels.

## Resource, postprocessing, mount, and artifact evidence

GPU 0 was an NVIDIA A100-PCIE-40GB with 41,855,287,296 bytes free at start. Peak allocated/reserved CUDA memory was 568,427,008 / 666,894,336 bytes; peak reserved was about 1.58% of the 42,298,834,944-byte device. Training processed 768 observations in 7.03 seconds (109.31/s). Validation processed 768 in 31.24 seconds (24.58/s). These are bounded-trial operational measurements, not production throughput claims.

Each epoch has an atomic validation postprocessing report. Postprocessing used `torch_cuda`, trusted batch size 8, at most 8 device samples per batch, bounded device batches, no full-validation GPU residency, and 32 target-skeleton batches. Epoch postprocessing times were 10.84, 8.50, and 9.43 seconds. `training.log` contains flushed progress at 100, 200, and 256 samples for inference and every postprocessing phase. The trusted Artifact Filter order remains Geographic Feature then Scanline.

Training, ancillary, and baseline roots are all recorded as read-only named mounts. Required resolved manifest, immutable Candidate, model summary, final/best metrics, 195-record metric log, finite checkpoint, resource profiles, three postprocessing reports/index, smoke/supervisor/training/validation logs, and two complete bounded prediction artifact sets are present.

## Directional comparison with ABI-031

ABI-031's main Run used 1,024 training and validation samples per source, eight times ABI-035's 128-per-source cap. Direct score comparison is therefore not scientifically controlled.

Directionally, focal Tversky shifted the bounded Run toward recall and away from precision relative to ABI-031's larger Run:

- aggregate filtered recall: 0.2925 versus 0.0926;
- Google filtered recall: 0.4357 versus 0.1093;
- MIT filtered recall: 0.2572 versus 0.0889;
- aggregate filtered Dice: 0.0462 versus 0.1028;
- aggregate filtered precision: 0.0251 versus 0.1156;
- aggregate filtered connectivity: 0.0664 versus 0.1573.

This is consistent with the proposed recall-oriented shift but also with substantial overprediction/precision loss. Because the sample budgets differ, it does not establish a scientific improvement or regression, promotion, baseline parity, or a preferred loss.

## Preregistered reliability continuation gate

| Criterion | Result |
| --- | --- |
| One stable completed Run and exactly one terminal event | Pass |
| One successful removed container; no timeout, retry, forced termination, or replacement | Pass |
| All structured numeric evidence finite | Pass |
| Trusted gradient/parameter checks and independently finite checkpoint | Pass |
| Three epochs, batch 4, exactly 128 train/validation observations per source per epoch | Pass |
| Aggregate/MIT/Google raw and filtered Dice above 0.0001; precision/recall non-degenerate | Pass |
| Both bounded predictions contain both classes | Pass |
| Artifact, provenance, mount, coordinate, resource, postprocessing, and ledger evidence complete | Pass |

**Gate decision: reliability continuation gate passed.** This decision means Candidate execution and exactly-once lifecycle behavior were reliable under the bounded policy. It is not a promotion decision.

## Residual risks and Human Gate 1

- The 128-versus-1,024 per-source budget mismatch prevents promotion-grade comparison with ABI-031.
- The recall increase comes with much lower precision, Dice, and connectivity; a larger controlled Run would be required to characterize the scientific tradeoff.
- The two `first_n` qualitative samples are intentionally bounded and are not representative full-validation evidence.
- `resolved_manifest.yaml` correctly captures clean launch commit `51126c4`; later `run_metadata.json` reports the same commit as dirty because trusted submission appended tracked Research Ledger events before training metadata refresh. Preflight evidence and the immutable resolved manifest establish the clean launch identity, but the mutable metadata presentation remains a provenance clarity risk.
- The 1,800-second timeout did not fire, so this Run validates successful bounded execution, not the timeout termination path.
- Trusted Resource Failure retry support remained structurally enabled with a maximum of three retries even though Gate 0 prohibited an automatic retry for this trial. The observed retry count was zero and there was exactly one attempt, so the exactly-once criterion passed in fact; future reliability trials should add a trusted policy switch that disables retry rather than relying only on the stop contract.

## Human Gate 1 and one conditional continuation step

Human Gate 1 approved one boundary refresh and exactly one subsequent bounded Autonomy Step with next-action execution enabled. It did not authorize an arbitrary loop, automatic evaluation, retry, second Autonomy Step, or more than the one Harness-owned action belonging to the approved step.

Before the step, ABI commit `f5a6e9c3ce57e678ddac6c552fce72260e569ad4` and Harness commit `a38ad742e187e23b1fa13f7b0ec8bd21da7ad637` were clean, pushed, and at zero upstream divergence. Runtime validation passed again at `2026-08-12T12:57:43Z` with the same Harness fingerprint, runner, and Workspace Configuration checksum. Counts were 13 Runs, 3 Evaluations, and 80 ledger events; no open Harness action, GPU process, or managed container existed. All prior primary handoffs had ingestion markers.

`prepare-agent-boundary` refreshed the boundary while retaining egress and the full read-only `/history/runs` mount. Agent-visible state included Run `run_20260812_121722_8d6cd3` through `/history/runs`, its ledger events through `/history/research-ledger.jsonl`, and its report identity/status through the refreshed `/reference/EXPERIMENT_INDEX.md` and `campaign_report_written` ledger event. The configured ceilings remained 128 samples per source, three epochs, concurrency one, two `first_n` predictions, and a 1,800-second trusted Docker training budget.

Exactly one approved command was invoked:

```bash
uv run ml-autoresearch autonomy-step --workspace-root . --execute-next-action
```

The Agent returned code 0 and deliberately created no handoff. It observed that the refreshed Experiment Index still said Human Gate 1 was pending and that no later operator approval existed in the Research Ledger. Rather than infer approval or create another Candidate, it stopped for human review. `agent-work/autonomy-step-result.json` records:

- `status: no_handoff`;
- `ingestion.status: no_handoff`;
- `next_action: stop_for_human`;
- `executed_next_action: false`;
- `ledger_events: []`;
- `execution: null`;
- written at `2026-08-12T13:01:13Z`.

This conservative stop obeyed the one-outcome boundary. No Candidate, Experiment Batch, evaluation, or Harness-owned action executed; no Run/Evaluation/ledger count changed; no executable action remains. No second Autonomy Step was launched. The reason is a durable-control sequencing gap: Gate 1 approval was given interactively but was not written to Agent-visible campaign state before the refresh. The outcome is still a successful autonomy safety result—ambiguous authorization caused a stop rather than unauthorized work—but it produced no scientific handoff. A future task must durably record operator authorization before expecting an Agent to act on it; ABI-035 does not rerun the step.

## Validation

- Full ABI suite: 114 passed.
- Focused Harness autonomy, boundary, handoff, submission, configuration, reconciliation, and research-loop suite: 123 passed.
- Correctly configured full Harness suite: 570 passed, 2 skipped, and one known unrelated GVCCS characterization failure. The stale fake GVCCS Spec permits only `bce_dice`, while an external committed Candidate uses `focal_bce_dice`; ABI-034 recorded the same unrelated failure.
- An initial unconfigured full Harness invocation also reported two missing external test-package environment variables. Rerunning with `ML_AUTORESEARCH_GVCCS_PROBLEM_ROOT=../gvccs-research-problem` and `ML_AUTORESEARCH_TEST_PROBLEM_ROOT=../test-research-problem` removed those configuration failures and left only the known GVCCS failure above.
- Runtime-image validation, static Candidate validation, terminal artifact audit, finite checkpoint audit, two idempotent reconciliations, post-step count/action inspection, and post-step idle-GPU/container inspection passed.

## Independent final review

A separate read-only Pi session reviewed the ABI-035 task, protocol, report, index, ledger, continuation result, and terminal Run artifacts with only the `read` tool enabled. It found no blocker in the Candidate Run's numerical, resource, coordinate, mount, or exactly-once outcome and assessed AC1-AC8 as passed (AC8 with no action applicable). Its one high finding was incomplete/inconsistent task closeout: AC7-AC9 and notes had not yet been synchronized and no final review/PR-style summary was recorded. That finding is addressed by this final report update and the Backlog CLI closeout.

The reviewer also identified three medium residual risks already bounded here: Resource Failure retries were structurally enabled although none occurred; interactive Gate 1 approval was not durably Agent-visible before the step; and mutable Run metadata presents the clean launch commit as dirty after tracked ledger mutation while the immutable resolved manifest correctly records the clean launch state. It confirmed that no additional Candidate or Autonomy Step is warranted.

## Commands

```bash
uv run ml-autoresearch validate-runtime-images --workspace-root .
uv run ml-autoresearch validate-candidate \
  --candidate candidates/abi032_mcast11_focal_tversky_v1 \
  --workspace-root .
uv run ml-autoresearch execute-open-actions \
  --workspace-root . --dry-run --max-actions 10
uv run ml-autoresearch execute-next-action --workspace-root .  # exactly once
uv run ml-autoresearch run-status \
  --workspace-root . --run-id run_20260812_121722_8d6cd3
uv run ml-autoresearch reconcile-run \
  --workspace-root . --run-id run_20260812_121722_8d6cd3
```

`reconcile-run` was repeated once to demonstrate idempotence; no launch command was repeated.

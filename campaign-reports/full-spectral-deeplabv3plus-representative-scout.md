# Full-spectral DeepLabV3+ representative scout

## Execution scope

This report records the preparation and completed execution of one representative-scout Autonomy Step under the trusted architecture-scout envelope. At `2026-08-13T14:55:37Z`, the operator invoked the bounded workflow after preparation and non-training validation completed.

Exactly one launch command was used:

```bash
uv run ml-autoresearch autonomy-step --workspace-root . --execute-next-action
```

The step produced one research handoff and one Harness-owned sequential Candidate Run. It created no replacement Candidate, retry-driven second Run, Experiment Batch, Post-Run Evaluation, extension, full-data training, promotion decision, concurrency change, or policy-limit increase.

## Trusted representative-scout envelope

The machine-local trusted Workspace Configuration restored the representative-scout ceilings after the resource pilot's temporary reduction:

| Boundary | Trusted value |
| --- | --- |
| Representative records | At most 1,024 per Dataset Source and Leakage-Safe Split |
| Epochs | At most 12 |
| Batch size | At most 4 |
| Training wall-clock timeout | 3,600 seconds |
| Prediction artifacts | At most four using fixed `first_n` |
| Parameters | At most 25,000,000 |
| Scheduler | `constant_lr` only |
| Early stopping | Disabled |
| Parallel Runs | One |
| GPU | Docker execution pinned to A100 device 0 |

The sample ceiling is applied independently after each Dataset Source and Leakage-Safe Split is constructed by provider policy `abi_representative_scene_positive_hash` version `v1`, seed `20260812`. Candidate source and manifests cannot choose records, selectors, seeds, source mixtures, caps, coordinates, data loading, loss or metric definitions, Artifact Filters, Baseline Segmenter loading, resource placement, retry, or lifecycle behavior.

Harness-owned validation and execution retained the no-bypass contract across direct/configured submission, Agent handoff ingestion, the Autonomy Step, managed continuation and reconciliation, and Experiment Batches. Candidate source, manifests, and handoffs cannot raise or replace the trusted sample, epoch, batch, parameter, timeout, prediction-count/policy, scheduler, early-stopping, concurrency, or GPU boundaries. The Autonomy Step used only synchronized Workspace values and exposed no Agent-owned backend or GPU override. Longitude and latitude remained prohibited Candidate inputs.

## Agent-owned preregistered choices

Within the trusted provider/Harness contract, the Agent chose and preregistered the Candidate hypothesis and allowlisted manifest parameters before submission. Legitimate autonomous choices include:

- learning rate within the validated manifest range;
- one provider-owned primary loss from the active ABI allowlist;
- one provider-owned augmentation policy from the active ABI allowlist;
- approved input mode, sampling traversal policy, optimizer, architecture, auxiliary targets/losses, and other allowlisted Candidate fields;
- any stricter Candidate request below the trusted Workspace ceilings.

These preregistered choices are **not protocol deviations merely because they differ from the MCAST-lineage positive control, the BCE-Dice-clDice bounded Run, the full-spectral DeepLabV3+ resource pilot, or another prior Candidate**. The Agent must state the hypothesis, changed and controlled factors, expected evidence, and stop conditions in `PROPOSAL.md` before ingestion and execution. New provider capabilities, ownership changes, arbitrary Candidate-defined losses or augmentations, coordinate inputs, policy-limit changes, and values outside an allowlist remain outside the Candidate boundary.

The scout design did not impose an outer learning-rate, loss, or augmentation value that could conflict with the step-local preregistration. Scientific interpretation must compare the actual preregistered factors rather than silently treating them as architecture-only controls.

## Scout evidence and asymmetric decisions

A 12-epoch, 1,024-record-per-source scout is a feasibility and failure screen, not a final architecture ranking. Any stable Run must record:

1. one stable Run identity, one terminal lifecycle event, container/retry lineage, and no unresolved action;
2. finite smoke, loss, gradients, parameters, metrics, checkpoint, postprocessing, and resource state;
3. parameter count, throughput, wall-clock duration, peak GPU allocation/reservation, effective batch compatibility, timeout state, and timeout headroom;
4. selected-record policy identity plus available/selected and positive/negative counts for MIT and Google train/validation strata;
5. per-epoch trajectory evidence, aggregate and source-stratified raw/filtered metrics, and bounded predicted-positive counts/fractions;
6. provider-owned `abi_scout_assessment.v1` evidence and all required bounded prediction artifacts.

Decisions are asymmetric. Hard failure, non-finite behavior, persistent prediction collapse, clear optimization failure, or convincing plateau/divergence at the fixed scout budget may support eliminating the exact branch. Low score alone does not. Improving, source-balanced, novel, noisy, or ambiguous finite trajectories remain eligible for continued bounded family development when supported by the active Workspace Configuration. No strict top-k or absolute-Dice cutoff applies.

## Preflight and single-launch checklist

Before execution, all of the following must pass without weakening policy or retrying around a failure:

- ABI and Harness revisions are clean, pushed, on the intended branches, and at zero upstream divergence;
- runtime identities validate against the restored Workspace checksum and the generated Agent Control Boundary reloads the exact values in this report;
- the generated boundary contains the current Experiment Index and Research Ledger snapshots;
- configured training, ancillary, baseline, and Runs roots plus required canonical assets exist;
- no open Harness action, campaign pause, or managed Candidate container exists;
- pinned A100 GPU 0 is idle;
- baseline Run, Evaluation, Batch, handoff, and lifecycle-event counts are recorded;
- focused ABI/Harness no-bypass and boundary tests and the applicable full suites pass;
- the operator invocation and applicable campaign state are present.

The launch command must be invoked exactly once. If the caller disconnects or returns unexpectedly after a stable Run exists, do not relaunch. Observe only that Run with `run-status` and reconcile it idempotently with `reconcile-run` after its managed container exits or durable state requires finalization.

## Stop behavior

The scout was configured to stop without replacement execution on contract violation, coordinate exposure, missing required artifacts, non-finite state, failed checkpoint audit, timeout or forced termination, OOM/resource retry, duplicate lifecycle events, selector mismatch, unresolved action, unexpected GPU/container state, or failed identity/preflight checks.

## Preparation and validation record

Preparation has restored the machine-local Workspace policy to 1,024 samples per source/split and 12 epochs while retaining every other boundary in the table. No Harness code change was required: Harness `c346f07aa4c837cdefcccf3fbe5fb675186efa2a` already enforces the promoted values, and the provider-owned representative-record selection provider selector already applies the scalar cap independently per Dataset Source and Leakage-Safe Split.

Non-training validation completed:

- restored Workspace Configuration typed reload: passed;
- focused ABI policy, provider, selection, Candidate-boundary, and scout-assessment tests: 43 passed;
- full ABI suite: 135 passed;
- focused Harness runtime-image, configuration, Candidate contract, direct/configured execution, handoff, Autonomy Step, Experiment Batch, boundary, and reconciliation suites after hardening: 201 passed;
- full configured Harness suite: 581 passed, 2 skipped, with one known unrelated external fixture characterization failure caused by a stale fake Spec allowlist;
- rebuilt runtime images and final runtime identity validation: passed for clean pushed Harness commit `b2d8345b12433b2dbb4c0ffa942db9362c7d9578`, fingerprint `b8f7a78000a5354f`, runner `ml-autoresearch-runner:abi-research-problem-b8f7a78000a5354f-13b99524f1`, and restored Workspace SHA-256 `cf417a023e06869e46678dedcc375779ceb6359cc63991e38185f7580c663294`;
- Docker CUDA validation: passed with PyTorch 2.5.1+cu121, CUDA 12.1, and visible A100;
- generated boundary typed reload and snapshot inspection: passed for 1,024/12, batch 4, 25M parameters, 3,600 seconds, four `first_n` predictions, constant LR, disabled early stopping, and concurrency one;
- named training, ancillary, baseline, and Runs roots plus required canonical MCAST and Natural Earth assets: present;
- dry-run open-action check: no open action;
- managed Candidate-container and GPU checks: no managed container or compute process; pinned A100 GPU 0 showed 0 MiB used and 0% utilization.

The pre-execution baseline is 15 Run directories, three Evaluation directories, 103 ledger events, 15 Candidate submissions/starts, 14 completed Runs, one historical failed Run, five ingested handoffs, three requested/completed Evaluations, and one historical created/completed Experiment Batch. No count changed during preparation.

Independent preparation review found the control and stop behavior sound. A second review identified that the `autonomy-step` CLI refreshed the boundary without itself requiring the Runtime Image Validation Stamp, unlike adjacent real-execution command families. Harness `b2d8345` added that precondition and stale-stamp/bypass regressions. Focused and full validation, image rebuild, identity validation, and Docker CUDA validation then passed.

## Execution and stable-Run reconciliation

The operator invoked execution at `2026-08-13T14:55:37Z` after the campaign report and active campaign state were committed at workspace revision `79016b16f97a5a52ffcf6715efd95f0b595fc40f`. The final generated boundary contained the current index, ledger tail, and 1,024/12 policy. Immediate preflight confirmed clean pushed ABI and Harness `b2d8345b12433b2dbb4c0ffa942db9362c7d9578`, no open action, no managed Candidate container or compute process, available named roots/assets, and A100 GPU 0 at 0 MiB/0% utilization. Baselines were 15 Runs, three Evaluations, 105 ledger events, five handoffs, 15 Candidate submissions/starts, and one historical Experiment Batch.

Exactly one launch command was invoked:

```bash
uv run ml-autoresearch autonomy-step --workspace-root . --execute-next-action
```

It returned code 0, produced and ingested exactly one Candidate Submission `abi044_fullspectral_deeplabv3plus_representative_scout_v1`, and started stable Run `run_20260813_145951_a64a37`. The Agent preregistered the resource pilot's DeepLabV3+ ResNet-18 architecture with provider-owned `combined_source_balanced` traversal and `random_mirroring`, trusted `bce_dice`, AdamW at 0.0003, batch 4, constant LR, disabled early stopping, and 12 epochs. No launch command was repeated. After the single container exited 0 and was removed, two explicit `reconcile-run` observations both returned the same completed Run idempotently without adding another terminal event.

The lifecycle ledger contains exactly one `agent_handoff_ingested`, `proposal_created`, `candidate_created`, `candidate_submitted`, `run_started`, and `run_completed` event for this scout and no corresponding failure event. Postflight has 16 Runs, three Evaluations, and 111 ledger events. No Experiment Batch, Post-Run Evaluation, replacement, second Run, or second Autonomy Step was launched. No open action, managed container, or GPU compute process remains.

## Trusted evidence and scout interpretation

The immutable Candidate completed 12 epochs at batch 4 with 12,370,065 parameters and accepted only source indices 0-15; model evidence explicitly prohibits longitude/latitude indices 16/17. The trusted selector `abi_representative_scene_positive_hash` v1, seed `20260812`, selected exactly 1,024 records in every source/split stratum:

| Dataset Source / split | Available | Selected | Positive / negative | Selection identity SHA-256 |
| --- | ---: | ---: | ---: | --- |
| MIT train | 4,928 | 1,024 | 441 / 583 | `7f573509ebc2b5352efd4e71f17c0c790f755dc6e48521ff7c1e240e64721f29` |
| MIT validation | 1,232 | 1,024 | 443 / 581 | `2a2ec50eb239f5c568a63dddc726881553e7fba020948f3f31b565d34473a29b` |
| Google train | 20,529 | 1,024 | 462 / 562 | `a5ebe021858d209c30b66e74ea8e8bf5c18fc00225f6c37a37c6fbcf3d8ae7e0` |
| Google validation | 1,856 | 1,024 | 305 / 719 | `f2792f2ae16f496faea9c04b45116d24197407909d37deb998f24dd8a692658f` |

The sole resource attempt completed with zero retries. It processed 24,576 training and 24,576 validation observations at 120.07 and 26.17 samples/s. Profiled work took 1,146.47 seconds, leaving 2,453.53 seconds (68.15%) of the trusted 3,600-second timeout. Peak CUDA allocation/reservation was 463,730,688 / 528,482,304 bytes with 41,855,287,296 bytes free at start. This supports the measured sequential batch-4 envelope only and does not establish a concurrent resource class.

A recursive audit found 25,850 finite numeric JSON/JSONL values. The best checkpoint contained 183 tensors and 12,383,918 finite values. Final aggregate raw/filtered Dice was 0.1290/0.1244, with raw/filtered predicted-positive fractions 0.002064/0.001961. Source-stratified final filtered evidence was:

| Source | Filtered Dice | Precision | Recall | Predicted-positive fraction |
| --- | ---: | ---: | ---: | ---: |
| MIT | 0.11249 | 0.18254 | 0.08129 | 0.002405 |
| Google | 0.15216 | 0.16871 | 0.13857 | 0.001517 |

The four bounded prediction masks contained 9, 7, 0, and 0 positive pixels out of 65,536. Two first records were all-negative, a qualitative residual, but aggregate/source epoch evidence remained non-degenerate. The provider-owned `abi_scout_assessment.v1` found all 25,260 trajectory numeric values finite, no persistent prediction collapse, no strong negative evidence, and improving recent slopes for training loss, aggregate filtered Dice, MIT filtered Dice, and Google filtered Dice. Aggregate filtered Dice rose from the numerical floor through epoch 3 to 0.1244 at epoch 12; its recent epoch-9-to-12 slope was +0.00550/epoch, while training loss improved by -0.00353/epoch. The assessment recommendation is `extension_eligible`, not elimination.

Under the architecture-scout policy's asymmetric rule, this Run provides finite, source-balanced, improving feasibility evidence. It does not support eliminating the family, and its low absolute score is not an elimination rule. A larger-budget continuation remains appropriate only when supported by the active Workspace Configuration and the evidence needs of the next operator-invoked research command.

## Independent review and residual risks

Fresh-context independent closeout review is recorded in [`campaign-reports/full-spectral-deeplabv3plus-representative-scout-independent-review.md`](full-spectral-deeplabv3plus-representative-scout-independent-review.md). It found no blocker or high-severity issue in the trusted policy, execution, lifecycle, resource, numerical, or scientific-interpretation evidence. No additional reconciliation was warranted.

Residual risks are: the deterministic representative subset remains only a capped feasibility screen; the final predicted-positive fractions are low and two of four bounded masks are all-negative despite non-collapsed aggregate/source evidence; filtered Dice was still improving at epoch 12, so the scout does not establish convergence; resource retry support remains structurally enabled despite zero retries; and provider revision metadata is expectedly dirty after handoff/index/ledger mutation. The A100 was idle at the representative DeepLabV3+ scout preflight and immediate Run postflight, but unrelated `concord-projection-comparison` processes began using it later during closeout; they are not managed ABI containers or follow-up work and no ABI action was launched in response.

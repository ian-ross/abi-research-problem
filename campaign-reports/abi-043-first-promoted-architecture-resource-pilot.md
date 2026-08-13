# ABI-043 first promoted architecture resource pilot

## Status and authorization

This report preregisters exactly one post-ABI-039 architecture-family resource pilot. The operator approved the ABI-043 implementation and execution plan in chat after confirming that `main` was pushed. That approval authorizes preparation, the trusted reduced-budget activation, and exactly one Autonomy Step with next-action execution after all preflight gates pass.

The only authorized primary outcome is one Candidate Submission for the family below and at most one Harness-owned Candidate Run. No second Autonomy Step, replacement Candidate, retry-driven second Run, direct `run-candidate`, non-dry-run open-action execution, Experiment Batch, Post-Run Evaluation, 12-epoch representative scout, 36-epoch extension, full-data training, promotion decision, concurrency change, or policy-limit increase is authorized.

## Preregistered Candidate family

Candidate family target: `abi043_fullspectral_deeplabv3plus_resnet18_v1`. The Agent's concrete step-local identity was `abi043_fullspectral_deeplabv3plus_resource_pilot_v1`; it implements the same preregistered full-spectral DeepLabV3+ ResNet-18 family.

Hypothesis: a randomly initialized, full-spectral DeepLabV3+ segmentation family with a ResNet-18 encoder can consume the provider-approved 16 ABI channels, complete the trusted batch-4 Candidate contract on pinned A100 GPU 0 with finite state and substantial timeout/memory headroom, and avoid gross all-negative/all-positive collapse during the one-epoch resource pilot.

This is materially different from both established ABI families:

- unlike the MCAST 1.1-lineage SMP U-Net, it consumes all 16 allowed ABI channels rather than three hand-derived planes and uses atrous spatial-pyramid context plus the DeepLabV3+ decoder instead of a symmetric U-Net decoder;
- unlike the custom spectral residual U-Net, it does not use that model's explicit brightness-temperature-difference concatenation, learned 1x1 spectral mixture, GroupNorm residual encoder, or dilated residual U-Net bottleneck/decoder.

The implementation should use `segmentation_models_pytorch.DeepLabV3Plus` with `encoder_name="resnet18"`, `encoder_weights=None`, `in_channels=16`, and `classes=1`, wrapped only as needed for fixed, preregistered per-channel normalization and exact `mask_logits` output. Static host validation measured 12,370,065 parameters and finite `(2, 1, 256, 256)` output for the unwrapped SMP topology. No pretrained download, file loading, Baseline Segmenter loading, longitude/latitude input, Candidate-owned data loading, loss, metric, Artifact Filter, sampling, optimizer loop, scheduling, device placement, retry, or lifecycle behavior is allowed.

## Controlled factors

The outer protocol intended architecture and input representation as the only scientific changes relative to the ABI-031 reliability control, with provider-owned `combined_source_balanced` sampling, `all_target_frames`, no augmentation, trusted `bce_dice`, AdamW at `0.001`, batch 4, constant learning rate, disabled early stopping, `abi_16ch`, and one `mask_logits` output.

The Agent created its concrete `PROPOSAL.md` and corresponding `proposal_created` event at `2026-08-13T13:15:15Z`, before `candidate_submitted` at `13:15:22Z` and `run_started` at `13:15:23Z`. That step-local preregistration retained the family, source-balanced sampling, frame policy, loss, optimizer, batch, scheduler, early-stopping, input/output, GPU, and sequential controls, but explicitly selected provider-owned `random_mirroring` and learning rate `0.0003`. The Harness accepted both from existing trusted allowlists/contract surfaces.

This is a documented protocol deviation from the outer comparison intent, not an undisclosed post-result change. It limits clean architecture-only comparison but does not invalidate the pilot's contract/resource/finite purpose. No score comparison or scientific family decision is made. Any later scout must separately preregister whether to retain these two controls or restore the ABI-031 values.

Fixed normalization constants are declared in Candidate source and reuse the already documented spectral-family channel means/scales rather than pilot-record inspection. They are architecture preprocessing, not permission to select or inspect records.

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

Immediately before launch:

- ABI commit `156efe56e5372b994a4f1cab5bda174fbc0eebb8` and Harness commit `c346f07aa4c837cdefcccf3fbe5fb675186efa2a` were clean, pushed, on `main`, and at zero upstream divergence;
- runtime validation passed for Harness fingerprint `44aa1c67f09ecad7`, runner `ml-autoresearch-runner:abi-research-problem-44aa1c67f09ecad7-13b99524f1`, and pilot Workspace SHA-256 `bc19a80c754bcfdec47a501f67b92a85fa2dcff91e74884c0172c5b88c7990b5`;
- Docker GPU validation saw PyTorch 2.5.1+cu121, CUDA 12.1, and the A100;
- the generated boundary reloaded trusted values 32 samples/source/split, one epoch, batch 4, 25M parameters, 3,600 seconds, four `first_n` predictions, concurrency one, and GPU 0; its Experiment Index and ledger snapshots exactly matched the committed authorization and latest `campaign_resumed(reason=abi043_fullspectral_deeplabv3plus_resource_pilot_authorized)` event;
- configured training, ancillary, baseline, and Runs roots and every required canonical MCAST/Natural Earth asset existed;
- trusted provider preflight found MIT train 4,928/validation 1,232 and Google train 20,529/validation 1,856 records, then selected exactly 32 positive/negative-covering records in every source/split with the same identity digests later recorded by the Run;
- baseline counts were 14 Run directories, 96 ledger events, 14 `candidate_submitted`, 14 `run_started`, 13 `run_completed`, one historical `run_failed`, four ingested handoffs, three requested/completed Evaluations, and one historical created/completed Experiment Batch;
- no open action, managed container, GPU compute process, or campaign pause existed; pinned A100 GPU 0 showed 0 MiB used and 0% utilization.

Exactly one command was invoked:

```bash
uv run ml-autoresearch autonomy-step --workspace-root . --execute-next-action
```

It returned code 0, produced one Candidate Submission, ingested one handoff, and started stable Run `run_20260813_131515_ff53ab`. No launch command was repeated. The same Run was observed with `run-status`; after its only container exited, one explicit `reconcile-run` call returned the already-completed stable identity idempotently.

## Run evidence and interpretation

Candidate `abi043_fullspectral_deeplabv3plus_resource_pilot_v1` passed static validation and its immutable canonical/snapshot tree hashes match at `4d16a2bf6a12830743d763ff38447c1051a1c8a519d37b76ca3f5c76858b8905`. The implementation uses fixed normalization of all provider-approved channels 0-15 and a randomly initialized SMP DeepLabV3+ ResNet-18. Model summary evidence records 12,370,065 parameters, synthetic batch `(2,16,256,256)`, finite output `(2,1,256,256)`, and explicit prohibition of longitude/latitude source indices 16/17.

The trusted provider recorded selector `abi_representative_scene_positive_hash` v1, seed `20260812`, cap scope `independent_per_dataset_source_and_leakage_safe_split`, and exactly 32 selected records in each stratum:

| Dataset Source / split | Available | Selected | Positive / negative | Selection identity SHA-256 |
| --- | ---: | ---: | ---: | --- |
| MIT train | 4,928 | 32 | 14 / 18 | `368ec6609486cab0dea86a90b7aa9263ca3ae1be902bbad632643a1398cdc36c` |
| MIT validation | 1,232 | 32 | 14 / 18 | `cca57f2646aaa8a6409fa3592589977343d13e6ea3da8454db9638d2452ad1af` |
| Google train | 20,529 | 32 | 14 / 18 | `05c126fcbd1ee4c0107f706b741e499ecb64ddecb1d2f46667398b796bfe4a67` |
| Google validation | 1,856 | 32 | 10 / 22 | `812539ecec5ccf91ab876942d20cf625550329662481831cb9afa70451d5d637` |

Exactly one epoch processed 64 training and 64 validation observations at effective batch 4. The sole resource attempt completed without OOM or retry (`retry_count: 0`), and the sole container exited 0 and was removed. Training throughput was 38.26 samples/s over 1.67 seconds; validation throughput was 14.79 samples/s over 4.33 seconds; profiled Run work took 8.06 seconds. The managed operation ran from `13:15:22.083485Z` to `13:15:45.760536Z` (23.68 seconds), leaving 3,576.32 seconds or 99.34% of the 3,600-second timeout. Peak CUDA allocation/reservation was 463,730,688 / 528,482,304 bytes with 41,855,287,296 bytes free at start, so batch 4 is compatible with substantial single-Run A100 headroom. This does not authorize concurrency.

A recursive audit parsed 27 JSON/JSONL records and 516 numeric values with no non-finite value. The selected checkpoint contained 183 tensors and 12,383,918 values, all finite; no non-finite diagnostic exists.

Source-stratified one-epoch diagnostics were finite and non-degenerate:

| Stratum | Raw / filtered Dice | Raw / filtered precision | Raw / filtered recall | Raw / filtered predicted-positive fraction |
| --- | --- | --- | --- | --- |
| Aggregate | 0.004572 / 0.004403 | 0.002351 / 0.002273 | 0.08294 / 0.07028 | 0.14492 / 0.12703 |
| Google | 0.002242 / 0.001829 | 0.001135 / 0.000927 | 0.09302 / 0.07036 | 0.13278 / 0.12297 |
| MIT | 0.006486 / 0.006732 | 0.003379 / 0.003536 | 0.08046 / 0.07027 | 0.15706 / 0.13109 |

All four bounded masks contained both classes: positive counts 4,685; 30,153; 3,698; and 15,156 out of 65,536 pixels. This rules out gross all-negative/all-positive behavior in the bounded samples, while the tiny budget and low precision remain non-ranking diagnostic context only.

The ledger has exactly one `agent_handoff_ingested`, `candidate_submitted`, `run_started`, and `run_completed` event for this Candidate/Run and no `run_failed`. Lifecycle postflight counts were 15 Runs and 102 ledger events; final reviewed report registration added one `campaign_report_written` event for 103 total. Evaluation and Batch counts did not change. No open action, managed container, or GPU process remains.

The pilot therefore passes its contract, resource, finite-state, batch-compatibility, and gross non-degeneracy purpose. It is not used to rank, promote, eliminate for low score, authorize concurrency, or start another stage. ABI-043 stops here before any 12-epoch scout.

## Validation, independent review, and residual risks

Validation completed:

- full ABI suite: 133 passed;
- focused Harness research-loop, Candidate policy, Autonomy Step, boundary, and reconciliation suite: 135 passed;
- exact-32 provider fixture, Candidate sampling/no-bypass boundary tests, trusted config reload, static Candidate validation, runtime image validation, Docker CUDA validation, generated-boundary snapshot comparison, finite/checkpoint audit, prediction-mask audit, open-action check, and postflight GPU/container checks: passed.

Independent fresh-context review is recorded in [`campaign-reports/abi-043-independent-review.md`](abi-043-independent-review.md). It found no substantive blocker and assessed ACs 1-7 and 9 satisfied, with AC 8 satisfied once the review and closeout metadata are persisted. It classified the augmentation/learning-rate difference as a residual comparison risk rather than a pilot acceptance blocker because the concrete Candidate proposal and `proposal_created` event preceded submission and execution, both settings used trusted contract surfaces, and no architecture-ranking claim is made.

Residual risks are: the outer protocol's no-augmentation/0.001 intent differed from the Agent's pre-run `random_mirroring`/0.0003 proposal, preventing clean architecture-only comparison; one epoch is too short for meaningful ranking; four bounded masks cannot establish broad non-degeneracy; structural Resource Failure retry remains enabled although retry count was zero; resource evidence supports batch 4 for one sequential A100 Run but not concurrency; some finite/operational audits are durable report attestations rather than standalone machine-readable artifacts; and provider revision metadata is expectedly dirty after handoff/index/ledger mutation despite the preserved clean pushed preflight identity.

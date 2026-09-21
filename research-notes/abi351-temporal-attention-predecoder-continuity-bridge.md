# ABI-351 temporal-attention pre-decoder continuity bridge

research-figures: []

## Scope

This note records ABI-351, Candidate `abi351_temporal_attention_predecoder_continuity_bridge_unet_bce_dice_line_centerline_aux_v1`, and Run `run_20260919_034932_017f6a`.

ABI-351 was a mechanism-changing exploratory follow-up to ABI-350 in the temporal-attention family. It kept ABI-350's provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`, source-balanced sampling, trusted random mirroring, BCE-Dice loss, Line and Centerline auxiliary targets, AdamW with constant LR, and batch size 2. The architectural change was a differentiable final continuity bridge after the high-resolution decoder feature and before the mask/Line/Centerline logits, using strip, dilated-diagonal, local-context, and high-resolution skip support to reinforce continuous thin-line features.

This is capped temporal-eligible exploratory evidence only. It is not whole Working Validation Split promotion evidence and should not be compared as a full-data Result against ABI-202 or ABI-249.

## Execution result

ABI-351 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: exploratory, 12 epochs.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Trusted augmentation policy: `random_mirroring`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,183,276, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 5,198,516,224 / 5,775,556,608 bytes.
- Training wall time: 1,546.6 s; validation wall time: 1,068.1 s; total Run wall time: 2,616.7 s, within the 3,600 s exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 11.

## Best-validation metrics

| Metric | ABI-351 continuity bridge | ABI-350 line support late36 | ABI-349 exploratory parent | ABI-324 balanced five-frame C4 | ABI-223 temporal attention | ABI-348 compact five-frame C4 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 11 | 33 | 12 | 27 | 36 | 36 |
| Filtered Dice | 0.389837 | 0.431103 | 0.389171 | 0.429430 | 0.419776 | 0.427829 |
| MIT filtered Dice | 0.370966 | 0.409536 | 0.369849 | 0.408188 | 0.398498 | 0.410244 |
| Google filtered Dice | 0.437075 | 0.490518 | 0.440561 | 0.487231 | 0.476764 | 0.478363 |
| Filtered precision | 0.417607 | 0.494306 | 0.478850 | 0.470412 | 0.483764 | 0.477546 |
| Filtered recall | 0.365530 | 0.382230 | 0.327784 | 0.395017 | 0.370738 | 0.387488 |
| Filtered connectivity | 0.271278 | 0.358283 | 0.337620 | 0.397925 | 0.412427 | 0.300904 |
| Filtered predicted-positive pixels | 478,622 | 422,831 | 374,305 | 459,172 | 419,056 | 443,691 |

ABI-351 does not improve the parent mechanism. Relative to ABI-350's selected late-budget checkpoint, it loses -0.0413 filtered Dice, -0.0386 MIT Dice, -0.0534 Google Dice, -0.0767 precision, -0.0167 recall, and -0.0870 connectivity while predicting 55,791 more filtered-positive pixels. Relative to ABI-349's exploratory checkpoint, ABI-351 is essentially tied on aggregate Dice (+0.0007) and MIT Dice (+0.0011), but it shifts toward broader recall (+0.0377) at the cost of much lower precision (-0.0612), lower Google Dice (-0.0035), lower connectivity (-0.0663), and a substantially larger footprint (+104,317 filtered-positive pixels).

The intended continuity bridge did not deliver fixed-threshold connected-line support. ABI-351's selected connectivity is below ABI-349, ABI-350, ABI-324, ABI-223, and even ABI-348. It also does not deliver ABI-344-style broad recall; recall remains below ABI-350/324/348 and only modestly below ABI-223. The result is therefore a footprint-widening, continuity-weak variant rather than a useful bridge.

At the selected checkpoint, raw Dice was 0.406003 versus filtered Dice 0.389837, raw recall was 0.394712 versus filtered recall 0.365530, and raw predicted-positive pixels were 516,398 versus 478,622 filtered. Artifact Filters removed 37,776 predicted-positive pixels and lowered the score; they did not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.178450 | 0.171920 | 0.193034 | 0.257531 | 0.136526 | 0.188428 | 0.002741 |
| 2 | 0.234984 | 0.238040 | 0.228670 | 0.244615 | 0.226083 | 0.130010 | 0.004778 |
| 3 | 0.249953 | 0.253263 | 0.243735 | 0.211639 | 0.305205 | 0.149092 | 0.007455 |
| 4 | 0.316717 | 0.299874 | 0.358506 | 0.410143 | 0.257957 | 0.307583 | 0.003251 |
| 5 | 0.250422 | 0.273344 | 0.212762 | 0.194856 | 0.350321 | 0.111586 | 0.009294 |
| 6 | 0.338856 | 0.317861 | 0.393189 | 0.482349 | 0.261163 | 0.331596 | 0.002799 |
| 7 | 0.374507 | 0.349155 | 0.441097 | 0.495872 | 0.300869 | 0.401008 | 0.003137 |
| 8 | 0.378322 | 0.356731 | 0.433446 | 0.423008 | 0.342174 | 0.287514 | 0.004182 |
| 9 | 0.350934 | 0.343905 | 0.366901 | 0.320819 | 0.387289 | 0.183582 | 0.006241 |
| 10 | 0.383211 | 0.362224 | 0.437114 | 0.420591 | 0.351933 | 0.288776 | 0.004326 |
| 11 | 0.389837 | 0.370966 | 0.437075 | 0.417607 | 0.365530 | 0.271278 | 0.004525 |
| 12 | 0.363360 | 0.353455 | 0.387417 | 0.397488 | 0.334629 | 0.196230 | 0.004352 |

The trajectory is finite and non-collapsed, but not late-improving enough to justify a 36-epoch continuation. The best checkpoint is near the end, yet epoch 12 regresses sharply and the selected epoch 11 does not exceed ABI-349's aggregate Result in a scientifically meaningful way. The transient high-connectivity epoch 7 is the only positive bridge signal: connectivity reaches 0.4010, near the ABI-324/223 comparator range, but aggregate Dice is only 0.3745 and recall is only 0.3009. The bridge can form a compact, connected state transiently, but that state does not align with fixed-threshold recall, source balance, or selected aggregate Dice.

## Prediction sample check

The retained fixed first-four validation samples are Harness traceability artifacts, not representative diagnostics. Their sample Dice values were 0.3213, 0.1609, 0.5348, and 0.3089. These confirm finite non-collapsed predictions, but they should not override aggregate validation metrics or justify Candidate-owned thresholding, postprocessing, Artifact Filters, validation selection, or qualitative cherry-picking.

## Interpretation

Classify ABI-351 as negative exploratory evidence for this exact final continuity-bridge variant.

The Run is technically healthy, so no repair Candidate is needed. Scientifically, however, the final bridge did not solve ABI-350's connected-line continuity or MIT-positive-tail weaknesses. It mostly widened the selected footprint and traded away precision/connectivity without gaining enough recall. The branch also fails the proposed success pattern: connectivity is lower than ABI-350/349/324/223, positive-tail recall is not clearly improved at the selected checkpoint, the footprint is larger than ABI-350/349/223/348, and the final epoch regresses.

ABI-351 does not justify Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle changes.

## Decision

Do not promote ABI-351, do not request whole-validation evaluation, and do not submit a late36 continuation of this final continuity-bridge variant. The useful evidence is the hard stop for this exact mechanism: adding a post-decoder continuity bridge after ABI-350's high-resolution decoder is too late or too unstable to improve selected fixed-threshold connected-line evidence.

Future temporal-attention work should not repeat simple post-decoder bridge/gain variants. If continuing the broader ABI-350 ingredient, move continuity support earlier or make it mechanism-changing: for example, temporal alignment/change support inside encoder/decoder fusion, a center-frame detail path that supervises continuous line evidence before skip fusion, or a different source-agnostic MIT-positive-tail mechanism. Another valid next step is to broaden back to a single-frame C4 compact anchor with cross-scale detail support, as suggested by the temporal C4 frontier reset.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260919_034932_017f6a/candidate/PROPOSAL.md`
- `run_20260919_034932_017f6a/candidate/README.md`
- `run_20260919_034932_017f6a/candidate/manifest.yaml`
- `run_20260919_034932_017f6a/resolved_manifest.yaml`
- `run_20260919_034932_017f6a/execution.json`
- `run_20260919_034932_017f6a/run_metadata.json`
- `run_20260919_034932_017f6a/outputs/model_summary.json`
- `run_20260919_034932_017f6a/outputs/best_metrics.json`
- `run_20260919_034932_017f6a/outputs/final_metrics.json`
- `run_20260919_034932_017f6a/outputs/metrics.jsonl`
- `run_20260919_034932_017f6a/outputs/resource_profile.json`
- `run_20260919_034932_017f6a/outputs/validation_postprocessing/index.json`
- `run_20260919_034932_017f6a/outputs/prediction_samples/samples.json`
- `run_20260919_013306_9ca44e/outputs/best_metrics.json` and `/history/research-notes/abi350-temporal-attention-predecoder-line-support-late36.md`
- `run_20260919_004607_f785f8/outputs/best_metrics.json` and `/history/research-notes/abi349-temporal-attention-predecoder-line-support-unet.md`
- `run_20260916_184108_954ec7/outputs/best_metrics.json`
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json`
- `run_20260918_215534_a35ab9/outputs/best_metrics.json`
- `/history/research-notes/temporal-c4-frontier-reset-after-abi348.md`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`

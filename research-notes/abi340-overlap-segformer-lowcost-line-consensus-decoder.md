# ABI-340 overlap SegFormer low-cost line-consensus decoder

research-figures: []

## Scope

This note records ABI-340, Candidate `abi340_overlap_segformer_lowcost_line_consensus_decoder_bce_dice_line_centerline_aux_v1`, Run `run_20260918_022233_f79f9f`.

ABI-340 was a mechanism-changing continuation of the ABI-262 overlap SegFormer scout and ABI-263 directional line-state follow-up. It kept provider-owned `abi_16ch_plus_sza` inputs, source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, batch size 4, constant learning rate, and trusted Line/Centerline auxiliary outputs. The architectural change was a compact `ConnectivityPreservingLineConsensusHead` intended to recover connected thin-line evidence with resource behavior closer to ABI-262 than ABI-263.

Candidate code remained architecture-only. It did not implement data loading, sample selection, target derivation, custom losses, metrics, thresholding, postprocessing, Artifact Filters, coordinate inputs, Dataset Source identity, downloads, resource scheduling, or lifecycle behavior.

This is capped representative feasibility evidence only. It is not whole-validation promotion evidence.

## Execution result

ABI-340 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `exploratory`, 12 epochs.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `all_target_frames`.
- Capped sample counts: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 1,732,921, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 10,168,868,352 / 11,404,312,576 bytes.
- Training wall time: 1,041.1 s; validation wall time: 1,247.7 s; total Run wall time: 2,290.5 s, within the 3,600 s exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 11.

The resource hypothesis mostly held. ABI-340 stayed close to ABI-262 resource use and far below ABI-263 activation cost, while preserving batch size 4.

## Best-validation metrics

| Metric | ABI-340 low-cost line consensus | ABI-262 overlap SegFormer parent | ABI-263 directional line-state | ABI-253 line-memory U-NetFormer | ABI-249 C4 line-context | ABI-202 aggregate reference |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 11 | 12 | 8 | 23 | 31 | 34 |
| Filtered Dice | 0.376161 | 0.396950 | 0.379436 | 0.408323 | 0.416400 | 0.427570 |
| MIT filtered Dice | 0.365739 | 0.388968 | 0.373046 | 0.394406 | 0.396436 | 0.411992 |
| Google filtered Dice | 0.400801 | 0.416932 | 0.394107 | 0.442587 | 0.468855 | 0.468151 |
| Filtered precision | 0.404478 | 0.400782 | 0.378366 | 0.444837 | 0.480886 | 0.439467 |
| Filtered recall | 0.351549 | 0.393191 | 0.380513 | 0.377349 | 0.367165 | 0.416301 |
| Filtered connectivity | 0.258278 | 0.231960 | 0.274668 | 0.326698 | 0.392524 | 0.457773 |
| Filtered predicted-positive pixels | 422,718 | 477,150 | 489,122 | 412,574 | 371,346 | 460,724 |
| Filtered positive fraction | 0.003149 | 0.003555 | 0.003644 | 0.003074 | 0.002767 | 0.003433 |

ABI-340 partially met only the resource portion of its goal. Relative to ABI-262 it improved selected-checkpoint connectivity by about +0.0263 and slightly improved precision, but lost about -0.0208 filtered Dice, -0.0232 MIT filtered Dice, -0.0161 Google filtered Dice, and -0.0416 recall. Relative to ABI-263, it is slightly lower on filtered Dice and connectivity, meaning the cheaper head did not recover the directional decoder's already modest line-continuity gain. Relative to ABI-253, ABI-249, and ABI-202 it remains clearly behind on aggregate/source Dice and connected-line evidence.

At the selected checkpoint, raw Dice was 0.390232 versus filtered Dice 0.376161, raw recall was 0.375549 versus filtered recall 0.351549, and raw predicted-positive pixels were 449,763 versus 422,718 filtered. Artifact Filters reduced footprint and score modestly; they did not explain the primary weakness.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.202579 | 0.228677 | 0.159510 | 0.148663 | 0.317858 | 0.100852 | 0.007748 |
| 2 | 0.269181 | 0.274487 | 0.259032 | 0.250211 | 0.291265 | 0.178676 | 0.004218 |
| 3 | 0.308270 | 0.312492 | 0.299582 | 0.274584 | 0.351378 | 0.174082 | 0.004637 |
| 4 | 0.311569 | 0.315166 | 0.304238 | 0.270839 | 0.366717 | 0.134756 | 0.004906 |
| 5 | 0.315915 | 0.298768 | 0.356373 | 0.423214 | 0.252020 | 0.362515 | 0.002158 |
| 6 | 0.340360 | 0.335278 | 0.351139 | 0.325202 | 0.357000 | 0.174990 | 0.003978 |
| 7 | 0.349331 | 0.344606 | 0.360007 | 0.352579 | 0.346141 | 0.255627 | 0.003558 |
| 8 | 0.320145 | 0.309566 | 0.344962 | 0.423879 | 0.257201 | 0.251760 | 0.002199 |
| 9 | 0.367956 | 0.357082 | 0.392841 | 0.390527 | 0.347852 | 0.236370 | 0.003228 |
| 10 | 0.365556 | 0.349884 | 0.401057 | 0.414446 | 0.326983 | 0.257530 | 0.002859 |
| 11 | 0.376161 | 0.365739 | 0.400801 | 0.404478 | 0.351549 | 0.258278 | 0.003149 |
| 12 | 0.351731 | 0.335789 | 0.391186 | 0.471636 | 0.280435 | 0.227207 | 0.002155 |

The trajectory was finite, source-informative, and non-collapsed, but it does not support an unchanged late-improving continuation. ABI-340 peaked at epoch 11 and then fell sharply at epoch 12. Epoch 5 briefly achieved high connectivity, but only by entering a high-precision/low-recall state with weak aggregate Dice. Later epochs stabilized aggregate Dice somewhat, but connectivity remained below ABI-263 and far below ABI-253/249/202.

## Prediction sample check

The retained fixed first-four validation samples are Harness traceability artifacts, not representative diagnostics. Their sample Dice values were near zero, near zero, 1.0, and near zero. Population metrics and positive-pixel counts confirm the model was not an all-negative collapse, but the retained samples do not provide qualitative support for promotion or a diagnostic Evaluation Request.

## Interpretation

Classify ABI-340 as resource-safe but negative evidence for this exact low-cost SegFormer line-consensus head. The head succeeded at avoiding ABI-263's heavy activation footprint, but it did not solve the core SegFormer-family problem: line-continuity support trades off against overlap recall and source-balanced Dice. The selected checkpoint recovered only a small portion of ABI-262's connectivity deficit while giving up too much MIT/source and recall behavior.

Comparator roles after ABI-340:

- ABI-262 remains the stronger overlap SegFormer capped result for aggregate Dice, MIT Dice, Google Dice, and recall, despite weak connectivity.
- ABI-263 remains the stronger SegFormer line-continuity diagnostic, but its cost/overlap trade-off remains unattractive.
- ABI-253 remains the compact modern-backbone comparator; ABI-340 does not approach its Dice or connectivity.
- ABI-249 and ABI-202 remain substantially stronger non-modern-backbone references.

ABI-340 does not justify Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle changes.

## Decision

Do not promote ABI-340. Do not request whole-validation diagnostics and do not request an unchanged late36 continuation. The result is finite and resource-safe, but it missed the proposal's metric success criteria and the final epoch regressed from the selected checkpoint.

Stop this exact low-cost line-consensus SegFormer branch unless a future proposal makes a clearer mechanism change that decouples connectivity from recall/coverage. If modern lightweight backbones are revisited, prefer a different architecture-level detail/line-preservation mechanism rather than another final-head SegFormer tweak. Otherwise broaden to stronger current frontiers such as temporal attention with evidence sharpening, C4/orientation recall support, or bounded line-continuity mechanisms outside this SegFormer decoder path.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260918_022233_f79f9f/candidate/PROPOSAL.md`
- `run_20260918_022233_f79f9f/candidate/README.md`
- `run_20260918_022233_f79f9f/candidate/manifest.yaml`
- `run_20260918_022233_f79f9f/resolved_manifest.yaml`
- `run_20260918_022233_f79f9f/execution.json`
- `run_20260918_022233_f79f9f/outputs/model_summary.json`
- `run_20260918_022233_f79f9f/outputs/best_metrics.json`
- `run_20260918_022233_f79f9f/outputs/final_metrics.json`
- `run_20260918_022233_f79f9f/outputs/metrics.jsonl`
- `run_20260918_022233_f79f9f/outputs/resource_profile.json`
- `run_20260918_022233_f79f9f/outputs/validation_postprocessing/index.json`
- `run_20260918_022233_f79f9f/outputs/prediction_samples/samples.json`
- `run_20260912_040526_92961f/outputs/best_metrics.json` and `/history/research-notes/abi262-overlap-segformer-line-decoder.md` for ABI-262 parent context
- `run_20260912_045029_55c59e/outputs/best_metrics.json` and `/history/research-notes/abi263-overlap-segformer-directional-line-state-decoder.md` for ABI-263 directional line-state context
- `run_20260911_171333_f0b603/outputs/best_metrics.json` for ABI-253 compact modern-backbone comparator context
- `run_20260911_111909_dd7ef7/outputs/best_metrics.json` for ABI-249 C4 steerable line-context comparator context
- `run_20260904_043143_ee0005/outputs/best_metrics.json` for ABI-202 current aggregate reference context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`

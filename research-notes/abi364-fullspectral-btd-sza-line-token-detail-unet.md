# ABI-364 full-spectral BTD+SZA line-token detail U-Net

research-figures: []

## Scope

This note records ABI-364, Candidate `abi364_fullspectral_btd_sza_line_token_detail_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260920_071924_68fd5c`.

ABI-364 was an exploratory single-frame family-development / lightweight decoder scout after recent full-spectral BTD+SZA C4, recall-sidecar, and source-detail-tail variants. It kept provider-owned `abi_16ch_plus_sza` inputs, trusted combined source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, Line and Centerline auxiliary targets, AdamW with constant learning rate, and batch size 4. The architecture question was whether low-rank row/column line-token support plus local strip context, injected inside the decoder before final logits, could improve connected thin-line evidence without Candidate-owned thresholding or postprocessing.

This is capped representative feasibility evidence only. It is not whole Working Validation Split promotion evidence and should not be treated as a full-data Result against ABI-202 or ABI-249.

## Execution result

ABI-364 completed without contract, smoke, shape, numerical, resource, or lifecycle failure. The exploratory budget was used; no late-improving budget was requested for this first exact line-token decoder scout.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `exploratory`, 12 epochs, 3,600 s timeout.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `all_target_frames`.
- Trusted augmentation policy: `random_mirroring`.
- Capped sample counts: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 7,368,630, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 7,926,450,688 / 8,717,860,864 bytes.
- Training wall time: 1,411.5 s; validation wall time: 1,421.1 s; total Run wall time: 2,834.7 s, within the exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 12.

## Capped best-validation metrics

| Metric | ABI-364 line-token detail | ABI-363 source-robust detail support | ABI-362 decoupled anchor/sidecar | ABI-353 C4 detail agreement | ABI-342 recall bridge | ABI-340 SegFormer line consensus | ABI-249 C4 comparator | ABI-202 aggregate reference |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 12 | 22 | 34 | 34 | 36 | 11 | 31 | 34 |
| Filtered Dice | 0.373339 | 0.406556 | 0.407108 | 0.417439 | 0.415499 | 0.376161 | 0.416400 | 0.427570 |
| MIT filtered Dice | 0.360086 | 0.386570 | 0.390686 | 0.401665 | 0.398614 | 0.365739 | 0.396436 | 0.411992 |
| Google filtered Dice | 0.404580 | 0.458372 | 0.446130 | 0.456492 | 0.460044 | 0.400801 | 0.468855 | 0.468151 |
| Filtered precision | 0.381776 | 0.425509 | 0.417976 | 0.442512 | 0.397609 | 0.404478 | 0.480886 | 0.439467 |
| Filtered recall | 0.365267 | 0.389220 | 0.396791 | 0.395056 | 0.435075 | 0.351549 | 0.367165 | 0.416301 |
| Filtered connectivity | 0.241738 | 0.363194 | 0.359966 | 0.348271 | 0.405280 | 0.258278 | 0.392524 | 0.457773 |
| Filtered predicted-positive pixels | 465,331 | 444,884 | 461,711 | 434,203 | 532,191 | 422,718 | 371,346 | 460,724 |

ABI-364 is finite and non-collapsed, but it is a negative result for the row/column line-token decoder hypothesis. It does not deliver the intended connected-line improvement: connectivity is only 0.2417, below ABI-340's already weak 0.2583 and far below ABI-363/362/353/342/249/202. Aggregate filtered Dice is also below the main recent single-frame comparators and only narrowly below ABI-340 despite ABI-364 predicting a larger footprint.

Relative to ABI-340, ABI-364 slightly improves Google Dice (+0.0038) and recall (+0.0137), but loses aggregate Dice (-0.0028), MIT Dice (-0.0057), precision (-0.0227), connectivity (-0.0165), and uses a larger footprint (+42,613 filtered-positive pixels). Relative to ABI-363, it loses aggregate Dice (-0.0332), MIT Dice (-0.0265), Google Dice (-0.0538), precision (-0.0437), recall (-0.0240), and connectivity (-0.1215). The result therefore does not support spending a late-improving continuation on this exact line-token bridge.

Raw versus filtered metrics show ordinary Artifact Filter behavior rather than filter-created performance. At the selected capped checkpoint, raw Dice was 0.385514 versus filtered Dice 0.373339; raw recall was 0.389253 versus filtered recall 0.365267; raw predicted-positive pixels were 495,798 versus 465,331 filtered. Artifact Filters removed 30,467 predicted-positive pixels and lowered the score.

The retained `first_n` prediction samples have near-zero per-sample Dice, but they are the fixed first four validation samples and should not be over-interpreted as a diagnostic sample. They do not provide a positive qualitative counter-signal to the aggregate metrics.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Precision | Recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.217878 | 0.243797 | 0.174428 | 0.180850 | 0.273971 | 0.148808 | 0.005490 |
| 2 | 0.279340 | 0.274873 | 0.289301 | 0.313558 | 0.251856 | 0.199775 | 0.002911 |
| 3 | 0.306381 | 0.303376 | 0.312843 | 0.316911 | 0.296528 | 0.197581 | 0.003391 |
| 4 | 0.305558 | 0.309767 | 0.297395 | 0.263070 | 0.364414 | 0.161307 | 0.005020 |
| 5 | 0.311572 | 0.282283 | 0.385152 | 0.477433 | 0.231239 | 0.457198 | 0.001755 |
| 6 | 0.321728 | 0.330705 | 0.304757 | 0.282820 | 0.373049 | 0.193390 | 0.004780 |
| 7 | 0.360180 | 0.356319 | 0.368956 | 0.344467 | 0.377394 | 0.254799 | 0.003970 |
| 8 | 0.370961 | 0.365436 | 0.383775 | 0.401156 | 0.344994 | 0.289424 | 0.003116 |
| 9 | 0.373198 | 0.358119 | 0.409579 | 0.406318 | 0.345070 | 0.329098 | 0.003077 |
| 10 | 0.364378 | 0.354160 | 0.387004 | 0.395281 | 0.337956 | 0.259046 | 0.003098 |
| 11 | 0.369776 | 0.369241 | 0.371056 | 0.329190 | 0.421776 | 0.212397 | 0.004643 |
| 12 | 0.373339 | 0.360086 | 0.404580 | 0.381776 | 0.365267 | 0.241738 | 0.003467 |

The trajectory is finite and still near its best aggregate value at epoch 12, but it is not mechanism-positive. The most favorable connectivity spike appears at epoch 5 (0.4572) in a very compact, low-recall state with weak aggregate Dice, and later aggregate improvements do not retain that connectivity. Epochs 8-12 hover around 0.37 filtered Dice without a stable source-balanced or connected-line breakthrough. Epoch 11 briefly raises recall to 0.4218 but loses precision, Google Dice, and connectivity. The intended row/column line-token support separates from, rather than combines with, useful recall and source balance.

## Interpretation

Classify ABI-364 as a finite, resource-safe, negative lightweight decoder scout. The low-rank line-token mechanism is contract-safe and computationally feasible, but the capped evidence indicates that injecting row/column tokens inside this decoder does not improve connected-line continuity or source-balanced fixed-threshold performance.

The result is not a promotion candidate and does not justify whole-validation diagnostics. It also does not justify an unchanged late36 continuation: the best checkpoint is at the exploratory boundary, but the branch is below ABI-340/342/353/362/363 across the key mechanism criteria, especially connectivity. A longer run might move the operating point, but there is no compelling mechanism-positive signal that this exact line-token bridge is recovering connected true contrail evidence.

Do not repeat ABI-364 with only more epochs, minor gate-strength changes, or a local head-weight shuffle. Future work should broaden to a more mechanism-changing direction, such as temporal-attention evidence sharpening, shift/alignment-aware temporal detail support, a genuinely different lightweight backbone with explicit continuity modeling, or a trusted policy/loss variation only if tied to a specific recall/connectivity/source-balance failure mode. Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, and lifecycle changes remain out of bounds.

## Decision

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260920_071924_68fd5c/candidate/PROPOSAL.md`
- `run_20260920_071924_68fd5c/candidate/README.md`
- `run_20260920_071924_68fd5c/candidate/manifest.yaml`
- `run_20260920_071924_68fd5c/resolved_manifest.yaml`
- `run_20260920_071924_68fd5c/execution.json`
- `run_20260920_071924_68fd5c/run_metadata.json`
- `run_20260920_071924_68fd5c/outputs/model_summary.json`
- `run_20260920_071924_68fd5c/outputs/best_metrics.json`
- `run_20260920_071924_68fd5c/outputs/final_metrics.json`
- `run_20260920_071924_68fd5c/outputs/metrics.jsonl`
- `run_20260920_071924_68fd5c/outputs/resource_profile.json`
- `run_20260920_071924_68fd5c/outputs/validation_postprocessing/index.json`
- `run_20260920_071924_68fd5c/outputs/prediction_samples/samples.json`
- `run_20260920_044100_71b924/outputs/best_metrics.json` and `/history/research-notes/abi363-fullspectral-btd-sza-source-robust-detail-support-late36.md` for ABI-363 comparator context
- `run_20260920_020446_9c2fa1/outputs/best_metrics.json` and `/history/research-notes/abi362-fullspectral-btd-sza-c4-decoupled-anchor-recall-sidecar-late36.md` for ABI-362 comparator context
- `run_20260919_053527_64085b/outputs/best_metrics.json` and `/history/research-notes/abi353-fullspectral-btd-sza-c4-crossscale-detail-agreement-late36.md` for ABI-353 comparator context
- `run_20260918_055403_f17232/outputs/best_metrics.json` and `/history/research-notes/abi342-fullspectral-btd-sza-c4-recall-bridge-late36.md` for ABI-342 comparator context
- `run_20260918_022233_f79f9f/outputs/best_metrics.json` and `/history/research-notes/abi340-overlap-segformer-lowcost-line-consensus-decoder.md` for ABI-340 comparator context
- `run_20260911_111909_dd7ef7/outputs/best_metrics.json` and `/reference/EXPERIMENT_INDEX.md` for ABI-249 comparator context
- `run_20260904_043143_ee0005/outputs/best_metrics.json` and `/reference/EXPERIMENT_INDEX.md` for ABI-202 reference context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`

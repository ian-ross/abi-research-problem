# Full-spectral BTD MCAST-guided dual-branch U-Net scout

research-figures: []

## Scope

This note records ABI-111 after Run `run_20260830_201502_afa0c8` completed.

Source Runs:

- ABI-111 MCAST-guided dual-branch U-Net scout: `run_20260830_201502_afa0c8`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-105 conservative-skip focal-Tversky continuation: `run_20260830_091941_139456`
- ABI-110 dual-logit-margin focal-Tversky continuation: `run_20260830_192051_6b901b`

ABI-111 was a family scout intended to broaden beyond recent local ABI-068 head, front-end, and gate tweaks. It kept provider-approved `abi_16ch` input, deterministic thermal BTD features derived only from GOES ABI channels 1-16, trusted focal-Tversky primary loss, provider-derived Centerline Target auxiliary supervision with trusted `weighted_bce` weight 0.02, provider-owned `combined_source_balanced` traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, 12 epochs, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.

The controlled architecture change was adding a separate MCAST-like thermal support branch from approved ABI channel evidence and fusing it softly into a full-spectral BTD line U-Net. The hypothesis was that a robust thermal support stream could improve calibration, false-positive discipline, source balance, or connectivity without moving thresholding, losses, Artifact Filters, postprocessing, data loading, sampling, augmentation, metrics, resource placement, or lifecycle behavior into Candidate code. This is capped representative evidence, not full-data promotion evidence.

## Contract and resource observation

ABI-111 stayed inside the Candidate Experiment Contract. Candidate code owned only model architecture over provider-approved ABI Channel Input and deterministic approved-channel combinations. It did not introduce candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem writes, network access, pretrained weights, or longitude/latitude inputs.

`resolved_manifest.yaml` records `input_mode: abi_16ch`, `data.sampling_policy: combined_source_balanced`, `data.augmentation_policy: random_mirroring`, `training.loss: focal_tversky`, and one `centerline_logits` auxiliary output using trusted `weighted_bce` weight 0.02. `outputs/model_summary.json` reported 18,206,874 parameters against the 25,000,000-parameter smoke ceiling, confirmed GOES ABI channels 1-16 only with forbidden longitude/latitude source channels excluded, and confirmed outputs `mask_logits` plus `centerline_logits`.

The Run completed at batch size 4 on the A100 with 2,318.9 seconds total wall time, 1,039.4 seconds training wall time, 1,277.1 seconds validation wall time, 9,646,899,200 bytes peak CUDA reserved, and no terminal execution failure. The best-validation checkpoint was epoch 10.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, BCE-Dice-clDice | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260830_091941_139456` | ABI-105 | ABI-068 branch, conservative non-amplifying skip gates | 12 | 0.3831 | 0.3820 | 0.3857 | 0.3344 | 0.4484 | 0.2520 | 0.00486 |
| `run_20260830_192051_6b901b` | ABI-110 | ABI-068 branch, foreground-minus-background dual-logit margin head | 12 | 0.3720 | 0.3706 | 0.3751 | 0.3210 | 0.4422 | 0.2267 | 0.00499 |
| `run_20260830_201502_afa0c8` | ABI-111 | MCAST-guided dual-branch thermal support stream | 10 | 0.3770 | 0.3636 | 0.4085 | 0.3887 | 0.3660 | 0.3560 | 0.00341 |

ABI-111 produced a finite, non-collapsed operating point but did not satisfy the preregistered positive scout criteria. Relative to ABI-068, aggregate filtered Dice decreased from 0.3964 to 0.3770 (-0.0194), MIT filtered Dice decreased from 0.3886 to 0.3636 (-0.0250), Google filtered Dice decreased from 0.4161 to 0.4085 (-0.0076), precision decreased slightly from 0.3992 to 0.3887 (-0.0105), recall decreased from 0.3936 to 0.3660 (-0.0276), and connectivity decreased from 0.3900 to 0.3560 (-0.0340). The lower predicted-positive fraction, 0.00341 versus ABI-068's 0.00357, was too small to offset the Dice, recall, and connectivity losses.

Relative to ABI-066, ABI-111 remained lower in aggregate filtered Dice (-0.0055), Google filtered Dice (-0.0207), precision (-0.0540), and connectivity (-0.1171), while recall was higher (+0.0292). It therefore did not retain ABI-066's precision/connectivity strength. Relative to ABI-105, ABI-111 had lower aggregate Dice (-0.0061) and lower recall (-0.0824), but better precision (+0.0543), connectivity (+0.1040), Google filtered Dice (+0.0229), and positive-area discipline. Relative to ABI-110, ABI-111 improved aggregate Dice (+0.0050), Google filtered Dice (+0.0334), precision (+0.0677), connectivity (+0.1293), and positive-area discipline, but lost recall (-0.0762). This is a cleaner operating point than ABI-110, not a new best frequency-gated-family result.

## ABI-111 trajectory

ABI-111 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.1863, 0.1775, 0.2693, 0.3238, 0.3246, 0.2924, 0.3338, 0.3092, 0.3453, 0.3770, 0.3071, and 0.3166. The selected checkpoint was epoch 10; validation quality then fell sharply at epoch 11 and recovered only partially by epoch 12. Training loss declined from 0.9354 at epoch 1 to 0.8503 at epoch 12, while validation loss reached 0.8837 at epoch 10 and 0.8845 at epoch 12.

At the selected checkpoint, filtered Dice was 0.3770, raw Dice 0.3899, filtered IoU 0.2323, filtered precision 0.3887, filtered recall 0.3660, filtered connectivity 0.3560, and filtered predicted-positive fraction 0.00341. Source-stratified filtered Dice was 0.3636 MIT and 0.4085 Google. Source precision/recall showed Google as the recall-forward source (`0.3639` precision, `0.4655` recall) and MIT as the precision-forward source (`0.4018` precision, `0.3319` recall).

Raw-to-filtered differences were modest: raw Dice 0.3899 versus filtered Dice 0.3770, and raw predicted-positive fraction 0.00362 versus filtered 0.00341. This does not look primarily like an Artifact Filter dependence issue. The fixed first-four retained prediction samples in `outputs/prediction_samples/samples.json` are bounded artifacts under the Harness-owned `first_n` retention policy and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-111 as finite, resource-feasible, non-collapsed, and mixed but not competitive capped scout evidence for the exact MCAST-guided dual-branch design. It did broaden away from local output-head/front-end tweaks and produced a cleaner precision/connectivity profile than the ABI-110 dual-logit-margin branch. However, it did not approach ABI-068 closely enough while improving a secondary metric, did not exceed ABI-066 while retaining ABI-066's precision/connectivity strength, did not beat ABI-105 or ABI-107 on aggregate filtered Dice, and did not finish with a late-improving final checkpoint.

The MCAST-like thermal support branch appears to regularize some of the recall-forward clutter seen in ABI-110, but it also suppresses useful recall and does not recover the stronger ABI-068 aggregate/source balance or ABI-066 connectivity. The source split is not catastrophic and Google filtered Dice remains high, so this single scout does not eliminate all thermal-support or dual-branch ideas. It is, however, negative evidence for continuing this exact soft-guided dual-branch formulation without a more targeted change.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-111 is capped representative evidence only and should not be interpreted as a full-data promotion result.

## Decision

Do not promote ABI-111. Do not request whole-validation diagnostics for this checkpoint ahead of stronger ABI-068/066-style references. Stop this exact MCAST-guided soft-fusion dual-branch design unless a clear implementation bug is found.

Retain ABI-068 as the local aggregate-Dice reference and ABI-066 as the precision/connectivity reference. The next useful hypothesis should either make a materially different thermal-support architecture change, test a targeted trusted data/loss policy, or broaden to another thin-line segmentation family rather than adding another small local suppressor or output-head variant to the current frequency-gated branch.

## Artifact references

- `run_20260830_201502_afa0c8/outputs/best_metrics.json`
- `run_20260830_201502_afa0c8/outputs/final_metrics.json`
- `run_20260830_201502_afa0c8/outputs/metrics.jsonl`
- `run_20260830_201502_afa0c8/outputs/resource_profile.json`
- `run_20260830_201502_afa0c8/outputs/model_summary.json`
- `run_20260830_201502_afa0c8/outputs/prediction_samples/samples.json`
- `run_20260830_201502_afa0c8/resolved_manifest.yaml`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260830_091941_139456/outputs/best_metrics.json`
- `run_20260830_192051_6b901b/outputs/best_metrics.json`

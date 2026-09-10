# ABI-218 temporal-eligible single-frame control

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-218, Candidate `abi218_temporal_eligible_singleframe_control_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260908_123030_05ad37`.

ABI-218 was the matched single-frame control requested after ABI-217. It used provider-owned `abi_16ch_plus_sza` tensors with `frame_selection_policy: temporal_eligible_center`, the same source-balanced traversal, BCE-Dice loss, Line and Centerline auxiliary targets, learning rate, batch size, and 12-epoch exploratory budget as ABI-217, but removed ABI-217's previous/next-frame Siamese encoders and temporal residual fusion streams. Candidate code remained architecture-only and did not implement temporal lookup, data loading, missing-frame repair, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Execution result

ABI-218 completed the exploratory budget without contract, shape, numerical, resource, or lifecycle failure.

Key execution facts from the Run artifacts:

- Status: completed.
- Effective budget: exploratory, 12 epochs, constant learning rate, disabled early stopping.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Provider temporal-eligibility evidence for the matched population used offsets `[-1, 0, 1]`, but the model consumed only the center ABI+SZA tensor.
- Sample counts after provider-owned temporal eligibility and capped-record selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,050,475, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 1.19 / 1.43 GB.
- Training wall time: 679.8 s; validation wall time: 898.8 s; total Run wall time: 1,580.2 s.

This is valid matched-control evidence for the temporal branch and a useful resource profile for a compact single-frame ABI+SZA U-Net on the temporal-eligible subset.

## Best-validation metrics

The best checkpoint was epoch 11 by `val/filtered_dice`.

| Metric | ABI-218 best epoch 11 |
| --- | ---: |
| Filtered Dice | 0.345570 |
| Raw Dice | 0.361077 |
| Filtered IoU | 0.208876 |
| Filtered precision | 0.407234 |
| Filtered recall | 0.300125 |
| Filtered contrail connectivity | 0.231399 |
| Filtered predicted-positive fraction | 0.003810 |
| Raw predicted-positive fraction | 0.004109 |
| MIT filtered Dice | 0.330415 |
| Google filtered Dice | 0.385184 |
| MIT filtered recall | 0.277317 |
| Google filtered recall | 0.367984 |
| Train loss | 0.835401 |
| Validation loss | 0.877630 |

Final epoch 12 dropped materially from the best checkpoint: filtered Dice 0.317889, raw Dice 0.333011, filtered precision 0.424983, filtered recall 0.253906, MIT filtered Dice 0.301633, Google filtered Dice 0.358391, and filtered predicted-positive fraction 0.003089.

## Learning trajectory

ABI-218 learned from a low finite start and peaked at epoch 11, then lost recall at epoch 12.

| Epoch | Filtered Dice | Raw Dice | Filtered precision | Filtered recall | MIT filtered Dice | Google filtered Dice | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.112117 | 0.117035 | 0.134079 | 0.096337 | 0.111913 | 0.112549 | 0.003714 |
| 2 | 0.189393 | 0.197934 | 0.249861 | 0.152489 | 0.176520 | 0.220008 | 0.003155 |
| 3 | 0.255716 | 0.265220 | 0.283134 | 0.233139 | 0.247223 | 0.274462 | 0.004257 |
| 4 | 0.274659 | 0.287397 | 0.380868 | 0.214769 | 0.254008 | 0.326883 | 0.002915 |
| 5 | 0.273394 | 0.283299 | 0.285489 | 0.262282 | 0.261185 | 0.300531 | 0.004749 |
| 6 | 0.322392 | 0.334681 | 0.333739 | 0.311791 | 0.307235 | 0.360033 | 0.004830 |
| 7 | 0.302311 | 0.317803 | 0.454585 | 0.226454 | 0.281111 | 0.357293 | 0.002575 |
| 8 | 0.330294 | 0.343004 | 0.326371 | 0.334312 | 0.320770 | 0.353344 | 0.005295 |
| 9 | 0.321625 | 0.332993 | 0.297935 | 0.349407 | 0.310864 | 0.347753 | 0.006063 |
| 10 | 0.328381 | 0.342004 | 0.377053 | 0.290839 | 0.315765 | 0.359878 | 0.003988 |
| 11 | 0.345570 | 0.361077 | 0.407234 | 0.300125 | 0.330415 | 0.385184 | 0.003810 |
| 12 | 0.317889 | 0.333011 | 0.424983 | 0.253906 | 0.301633 | 0.358391 | 0.003089 |

The trajectory is source-informative and noncollapsed. Predicted-positive fractions stayed small but nonzero, and both Dataset Sources improved substantially from epoch 1.

## Matched comparison to ABI-217

| Metric | ABI-217 temporal best epoch 11 | ABI-218 single-frame control best epoch 11 | ABI-218 minus ABI-217 |
| --- | ---: | ---: | ---: |
| Filtered Dice | 0.349086 | 0.345570 | -0.003516 |
| Raw Dice | 0.363412 | 0.361077 | -0.002335 |
| Filtered precision | 0.387277 | 0.407234 | +0.019957 |
| Filtered recall | 0.317751 | 0.300125 | -0.017626 |
| Filtered contrail connectivity | 0.265915 | 0.231399 | -0.034516 |
| MIT filtered Dice | 0.333794 | 0.330415 | -0.003380 |
| Google filtered Dice | 0.387537 | 0.385184 | -0.002353 |
| Filtered predicted-positive fraction | 0.004241 | 0.003810 | -0.000432 |
| Parameter count | 4,326,675 | 3,050,475 | -1,276,200 |
| Peak CUDA allocated | 2.62 GB | 1.19 GB | -1.43 GB |
| Total Run wall time | 2,013.8 s | 1,580.2 s | -433.6 s |

The single-frame control nearly matched ABI-217's primary metric while being smaller and cheaper. ABI-217 retained a slight recall and connectivity edge, but the absolute filtered-Dice advantage was only 0.0035 and both candidates peaked at the same epoch on the same temporal-eligible population. This suggests ABI-217's first temporal residual streams added limited segmentation value relative to their resource cost.

## Interpretation

ABI-218 answers the matched-control question: temporal eligibility by itself supports a competent compact ABI+SZA segmenter around filtered Dice 0.346, and ABI-217's explicit three-frame temporal fusion only barely exceeded that control. The temporal branch remains viable because both Runs were finite, late-improving, source-informative, and nondegenerate. However, this exact Siamese/change design should not be expanded blindly; its small metric edge over a cheaper center-frame model is not enough evidence that richer temporal residual streams are the best next allocation.

Neither ABI-217 nor ABI-218 challenges the mature ABI-202 frontier. ABI-202's capped best filtered Dice remains 0.427570 with stronger recall, source metrics, and connectivity. That gap is not global temporal-family elimination evidence, but it does mean the next temporal work should change the temporal mechanism rather than simply scale ABI-217.

## Decision

Do not promote ABI-218 and do not request whole-validation diagnostics for ABI-218.

Classify ABI-218 as a successful matched control. It supports the conclusion that the first temporal Siamese/change fusion is not yet delivering a decisive temporal advantage over a temporal-eligible single-frame baseline. The best next in-contract hypothesis is a simpler and more explicit temporal-difference scout: consume provider-owned `abi_16ch_plus_sza_temporal`, keep `frame_selection_policy: temporal_eligible_center`, build bounded center-minus-neighbor ABI/SZA/BTD difference features at the front end, and use a compact single decoder rather than three full frame encoders. A richer temporal attention or ConvGRU design should wait until a lighter temporal-difference model demonstrates clearer benefit over ABI-218.

No Capability Request, Evaluation Request, Campaign Report, or second Candidate Submission is required from this Result. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260908_123030_05ad37/candidate/PROPOSAL.md`
- `run_20260908_123030_05ad37/candidate/README.md`
- `run_20260908_123030_05ad37/resolved_manifest.yaml`
- `run_20260908_123030_05ad37/outputs/model_summary.json`
- `run_20260908_123030_05ad37/outputs/best_metrics.json`
- `run_20260908_123030_05ad37/outputs/final_metrics.json`
- `run_20260908_123030_05ad37/outputs/metrics.jsonl`
- `run_20260908_123030_05ad37/outputs/resource_profile.json`
- `run_20260908_123030_05ad37/outputs/validation_postprocessing/index.json`
- `run_20260908_123030_05ad37/outputs/prediction_samples/samples.json`
- `run_20260908_114854_409a12` for the ABI-217 temporal Siamese/change comparison target
- `run_20260904_043143_ee0005` for the ABI-202 current best whole-validation-tested frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`

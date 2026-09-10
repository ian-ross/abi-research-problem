# ABI-217 temporal Siamese change U-Net finite-input repair

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-217, Candidate `abi217_temporal_siamese_change_unet_finite_input_repair_bce_dice_line_centerline_aux_v1`, Run `run_20260908_114854_409a12`.

ABI-217 repaired ABI-216 (`run_20260908_114141_bf7ae7`), which failed with Harness-recorded `candidate_bug` after `output.mask_logits` became non-finite at epoch 1 batch 134. The repair preserved the first real temporal/change segmentation hypothesis after ABI-215: consume provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]`, use `frame_selection_policy: temporal_eligible_center`, share a per-frame encoder across previous/center/next ABI+SZA frames, and fuse center plus temporal-difference evidence in a compact U-Net/ASPP decoder. The narrow repair bounded candidate-visible normalized/BTD/SZA features and hidden activations; it did not implement temporal lookup, data loading, missing-frame repair, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinates, or resource scheduling.

## Execution result

ABI-217 completed the full 12-epoch exploratory budget without recurrence of ABI-216's non-finite output failure.

Key execution facts from the Run artifacts:

- Status: completed.
- Effective budget: exploratory, 12 epochs, constant learning rate, disabled early stopping.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Temporal offsets: `[-1, 0, 1]`; target frame offset `0`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Sample counts after provider-owned temporal eligibility and capped-record selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,326,675, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 2.82 / 3.12 GB.
- Training wall time: 1,061.4 s; validation wall time: 950.6 s; total Run wall time: 2,013.8 s.

The repair should therefore be treated as successful finite/resource evidence for this compact temporal Siamese/change family. It also profiles a real temporal architecture as substantially heavier than the ABI-215 canary but still comfortably within the current exploratory envelope at batch size 2.

## Best-validation metrics

The best checkpoint was epoch 11 by `val/filtered_dice`.

| Metric | ABI-217 best epoch 11 |
| --- | ---: |
| Filtered Dice | 0.349086 |
| Raw Dice | 0.363412 |
| Filtered IoU | 0.211450 |
| Filtered precision | 0.387277 |
| Filtered recall | 0.317751 |
| Filtered contrail connectivity | 0.265915 |
| Filtered predicted-positive fraction | 0.004241 |
| Raw predicted-positive fraction | 0.004578 |
| MIT filtered Dice | 0.333794 |
| Google filtered Dice | 0.387537 |
| MIT filtered recall | 0.290446 |
| Google filtered recall | 0.398989 |
| Train loss | 0.826596 |
| Validation loss | 0.881840 |

Final epoch 12 remained close but lower on the primary metric: filtered Dice 0.343985, raw Dice 0.360914, filtered precision 0.484252, filtered recall 0.266726, MIT filtered Dice 0.327121, Google filtered Dice 0.388923, and filtered predicted-positive fraction 0.002847.

## Learning trajectory

ABI-217 learned steadily from a low but finite starting point and peaked near the end of the exploratory budget rather than immediately plateauing.

| Epoch | Filtered Dice | Raw Dice | Filtered precision | Filtered recall | MIT filtered Dice | Google filtered Dice | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.160412 | 0.165811 | 0.133310 | 0.201345 | 0.164610 | 0.152479 | 0.007808 |
| 2 | 0.204220 | 0.211981 | 0.242129 | 0.176574 | 0.186940 | 0.245798 | 0.003770 |
| 3 | 0.236916 | 0.247925 | 0.317894 | 0.188818 | 0.215808 | 0.286003 | 0.003071 |
| 4 | 0.293449 | 0.305563 | 0.314452 | 0.275076 | 0.278704 | 0.328213 | 0.004522 |
| 5 | 0.305342 | 0.314997 | 0.294984 | 0.316454 | 0.301045 | 0.314826 | 0.005546 |
| 6 | 0.323615 | 0.338906 | 0.432584 | 0.258498 | 0.306719 | 0.366160 | 0.003089 |
| 7 | 0.295131 | 0.309931 | 0.488761 | 0.211387 | 0.268237 | 0.367277 | 0.002236 |
| 8 | 0.340037 | 0.354822 | 0.410744 | 0.290098 | 0.323987 | 0.381017 | 0.003651 |
| 9 | 0.326027 | 0.337457 | 0.301092 | 0.355464 | 0.316619 | 0.349062 | 0.006103 |
| 10 | 0.341950 | 0.355412 | 0.388739 | 0.305215 | 0.325120 | 0.382925 | 0.004059 |
| 11 | 0.349086 | 0.363412 | 0.387277 | 0.317751 | 0.333794 | 0.387537 | 0.004241 |
| 12 | 0.343985 | 0.360914 | 0.484252 | 0.266726 | 0.327121 | 0.388923 | 0.002847 |

The trajectory is not collapsed: predicted-positive fractions stayed small but nonzero, source-stratified Dice remained informative on both MIT and Google, and the best checkpoint occurred at epoch 11. The precision/recall tradeoff shifted in the last epoch toward fewer positives and higher precision, explaining the slight filtered-Dice drop.

## Interpretation

ABI-217 is a successful repair and a scientifically useful first temporal/change scout. It is much stronger than the ABI-215 temporal access canary and demonstrates that a real shared-weight temporal encoder can train end-to-end on provider-owned `[-1, 0, 1]` ABI+SZA frames under the current contract.

It does not challenge the mature single-frame frontier: ABI-202 remains the strongest whole-validation-tested Result, and its capped best filtered Dice is about 0.4276 versus ABI-217's 0.3491. ABI-217 also trails older strong single-frame scouts such as ABI-068 on capped filtered Dice. The gap is not, by itself, elimination evidence for temporal modeling because this was the first repaired real temporal architecture, it completed finite, it improved through late epochs, and it showed nondegenerate behavior on both Dataset Sources.

The most important scientific signal is mixed: temporal inputs are feasible and the temporal/change family is viable, but this exact implementation did not yet convert temporal context into frontier-level accuracy. Google filtered Dice was stronger than MIT filtered Dice at the best epoch, while MIT connectivity was slightly higher than Google connectivity. This suggests the next temporal decision should separate data-policy effects from architecture effects rather than assume the temporal residual streams are already useful.

## Decision

Do not promote ABI-217 and do not request whole-validation diagnostics for ABI-217 from this capped Result alone.

Do continue temporal-family development or controlled temporal evaluation. The best next in-contract hypothesis is a matched `temporal_eligible_center` single-frame control using `abi_16ch_plus_sza`, the same source-balanced sampling, BCE-Dice loss, Line and Centerline auxiliaries, and comparable compact decoder capacity. That control would clarify whether ABI-217's 0.3491 filtered Dice comes from temporal eligibility/source subset differences, from the temporal architecture itself, or from using SZA+BTD features under a different architecture. A second reasonable follow-up is a simpler temporal-difference front end with fewer residual streams if the control shows the temporal branch is adding optimization burden without clear signal.

No Capability Request, Evaluation Request, or Campaign Report is required from this Result. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260908_114854_409a12/candidate/PROPOSAL.md`
- `run_20260908_114854_409a12/candidate/README.md`
- `run_20260908_114854_409a12/resolved_manifest.yaml`
- `run_20260908_114854_409a12/outputs/model_summary.json`
- `run_20260908_114854_409a12/outputs/best_metrics.json`
- `run_20260908_114854_409a12/outputs/final_metrics.json`
- `run_20260908_114854_409a12/outputs/metrics.jsonl`
- `run_20260908_114854_409a12/outputs/resource_profile.json`
- `run_20260908_114854_409a12/outputs/validation_postprocessing/index.json`
- `run_20260908_114854_409a12/outputs/prediction_samples/samples.json`
- `run_20260908_114141_bf7ae7` for the motivating ABI-216 non-finite failure
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`

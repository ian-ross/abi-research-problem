# ABI-260 compact MaxViT line-context U-Net

research-figures: []

## Scope

This note records the exploratory Result for ABI-260, Candidate `abi260_fullspectral_btd_sza_compact_maxvit_line_context_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260912_021616_d20946`.

ABI-260 was a modern-backbone family scout. It tested whether a compact MaxViT-style encoder, alternating local window attention with sparse global grid attention, could improve patch-scale cloud context and thin-line support without another local mutation of the mature ABI-202/ABI-184-style ASPP/detail frontier or the recent temporal line-support branch. It used provider-owned `abi_16ch_plus_sza` inputs, source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, batch size 4, constant learning rate, and trusted Line/Centerline auxiliary targets.

Candidate code remained architecture-only and did not implement data loading, split logic, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, temporal lookup, downloads, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Execution result

ABI-260 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from Harness-owned artifacts:

- Status: completed.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `all_target_frames`.
- Sample counts after capped-record selection: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 4,194,412, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 12.82 / 14.21 GB.
- Training wall time: 1,875.8 s; validation wall time: 1,382.4 s; total Run wall time: 3,260.3 s.

This is valid finite/resource evidence for a compact MaxViT-style single-frame family on the capped representative validation population. It is not whole-validation promotion evidence.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was the final exploratory epoch 12.

| Metric | ABI-260 best/final epoch 12 | ABI-259 temporal line-support | ABI-253 line-memory U-NetFormer | ABI-255 recurrent temporal late36 | ABI-223 temporal-attn late36 | ABI-202 whole-val frontier |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.381455 | 0.381540 | 0.408323 | 0.417348 | 0.419776 | 0.427570 |
| Raw Dice | 0.395228 | 0.398247 | 0.423530 | 0.435656 | 0.438487 | 0.442746 |
| Filtered precision | 0.408841 | 0.438659 | 0.444837 | 0.468293 | 0.483764 | 0.439467 |
| Filtered recall | 0.357507 | 0.337582 | 0.377349 | 0.376400 | 0.370738 | 0.416301 |
| Filtered connectivity | 0.326157 | 0.331613 | 0.326698 | 0.281116 | 0.412427 | 0.457773 |
| MIT filtered Dice | 0.365482 | 0.368471 | 0.394406 | 0.400833 | 0.398498 | 0.411992 |
| Google filtered Dice | 0.419710 | 0.415787 | 0.442587 | 0.463143 | 0.476764 | 0.468151 |
| Filtered predicted-positive fraction | 0.003169 | 0.003978 | 0.003074 | 0.004155 | 0.003962 | 0.003433 |

Relative to ABI-259, ABI-260 is essentially tied on filtered Dice (-0.00009), trades lower precision (-0.0298) and slightly lower connectivity (-0.0055) for higher recall (+0.0199), and uses fewer predicted-positive pixels. Relative to the modern-backbone U-NetFormer comparator ABI-253, ABI-260 is weaker by about -0.0269 filtered Dice, -0.0360 precision, -0.0198 recall, -0.0289 MIT Dice, and -0.0229 Google Dice, while connectivity is nearly identical. Relative to ABI-255/223 temporal references and ABI-202, ABI-260 remains clearly behind the overlap and connectivity frontier.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.184203 | 0.215468 | 0.140860 | 0.127581 | 0.331183 | 0.103275 | 0.009407 |
| 2 | 0.300224 | 0.305571 | 0.289018 | 0.291767 | 0.309185 | 0.172250 | 0.003840 |
| 3 | 0.315993 | 0.308405 | 0.332733 | 0.349774 | 0.288162 | 0.241181 | 0.002985 |
| 4 | 0.328970 | 0.335348 | 0.315863 | 0.300726 | 0.363069 | 0.162088 | 0.004375 |
| 5 | 0.350925 | 0.341738 | 0.372424 | 0.403120 | 0.310697 | 0.310511 | 0.002793 |
| 6 | 0.337150 | 0.331924 | 0.348300 | 0.320533 | 0.355585 | 0.253077 | 0.004020 |
| 7 | 0.348554 | 0.339125 | 0.369304 | 0.338846 | 0.358836 | 0.196166 | 0.003837 |
| 8 | 0.351115 | 0.355301 | 0.342455 | 0.329409 | 0.375883 | 0.181402 | 0.004135 |
| 9 | 0.378647 | 0.360412 | 0.422713 | 0.418809 | 0.345514 | 0.325085 | 0.002990 |
| 10 | 0.374892 | 0.359718 | 0.409395 | 0.429120 | 0.332832 | 0.340230 | 0.002811 |
| 11 | 0.348203 | 0.345081 | 0.355077 | 0.358696 | 0.338306 | 0.272470 | 0.003418 |
| 12 | 0.381455 | 0.365482 | 0.419710 | 0.408841 | 0.357507 | 0.326157 | 0.003169 |

The trajectory is finite, source-informative, and non-collapsed. It rises quickly to the mid-0.35 range, enters the high-0.37/low-0.38 neighborhood at epochs 9-10, dips at epoch 11, and recovers to its best aggregate checkpoint at epoch 12. Google Dice is consistently stronger than MIT in the later epochs. Connectivity also reaches a useful but not frontier-level band around 0.326-0.340 at epochs 9-10 and 12.

The final-epoch best checkpoint is a mild late-improvement signal, but it is noisy rather than a clean monotonic rise. Given the 3,260 s exploratory wall time, a 36-epoch repeat would likely fit only with limited margin under the 10,800 s late-improving timeout, and ABI-260's selected score remains materially below ABI-253 and the stronger temporal references. The evidence is therefore not enough by itself to prioritize an unchanged late36 MaxViT continuation over broader mechanism changes.

## Interpretation

Classify ABI-260 as a mixed but mostly negative first scout for this exact compact MaxViT-style line-context design. The positive evidence is that the architecture is contract-compliant, finite, non-collapsed, and reaches ABI-259-level capped filtered Dice while using single-frame inputs and producing comparable connectivity to ABI-253. It also shows that a small local/grid-attention backbone can run inside the 25M-parameter ceiling and the exploratory timeout.

The negative evidence is that the scout does not improve the modern-backbone frontier. It is substantially below ABI-253 on capped filtered Dice and source metrics, below ABI-223/255 on temporal-family comparison, and below ABI-202 on the mature whole-validation frontier. Its attention/context mechanism did not translate into better fixed-threshold connectivity, and the MIT source remains the weaker side of the split.

This does not eliminate lightweight modern backbones as a class, but it argues against spending the next step on an unchanged MaxViT extension. If the family is revisited, the follow-up should change the mechanism rather than merely add epochs or auxiliary heads: for example, a cheaper line-accumulation/evidence-raising module, a recall-preserving calibration architecture, or a MaxViT variant that explicitly reduces memory and targets MIT under-coverage without Candidate-owned thresholding or postprocessing.

## Decision

Do not promote ABI-260. Do not submit an unchanged late36 continuation as the immediate next action: the final-epoch best is real but noisy, resource margin is relatively narrow, and the best score does not clear the stronger ABI-253 modern-backbone comparator.

Retain ABI-260 as finite/resource evidence for compact MaxViT-style local/grid attention. Prefer a broader mechanism-changing scout or a targeted whole-validation diagnostic for a stronger near-frontier candidate in a later Autonomy Step, rather than another local MaxViT/decoder tweak.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260912_021616_d20946/candidate/PROPOSAL.md`
- `run_20260912_021616_d20946/candidate/README.md`
- `run_20260912_021616_d20946/candidate/manifest.yaml`
- `run_20260912_021616_d20946/resolved_manifest.yaml`
- `run_20260912_021616_d20946/outputs/model_summary.json`
- `run_20260912_021616_d20946/outputs/best_metrics.json`
- `run_20260912_021616_d20946/outputs/final_metrics.json`
- `run_20260912_021616_d20946/outputs/metrics.jsonl`
- `run_20260912_021616_d20946/outputs/resource_profile.json`
- `run_20260912_021616_d20946/outputs/validation_postprocessing/index.json`
- `run_20260912_021616_d20946/outputs/prediction_samples/samples.json`
- `run_20260912_012708_f5897e` for ABI-259 temporal line-support comparator context
- `run_20260911_171333_f0b603` for ABI-253 line-memory U-NetFormer comparator context
- `run_20260911_210922_27f346` for ABI-255 recurrent temporal late36 comparator context
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-attention late36 comparator context
- `run_20260904_043143_ee0005` for ABI-202 current aggregate whole-validation frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`

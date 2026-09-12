# ABI-252 compact line-memory U-NetFormer

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-252, Candidate `abi252_fullspectral_btd_sza_compact_line_memory_unetformer_bce_dice_line_centerline_aux_v1`, Run `run_20260911_161019_8c76cd`.

ABI-252 was a compact family-development continuation after ABI-251's resource failure. It preserved the line-memory U-NetFormer hypothesis while narrowing the high-resolution path and removing full-resolution shifted-window attention. It used provider-approved `abi_16ch_plus_sza` input, trusted BCE-Dice loss, source-balanced sampling, trusted random mirroring, constant learning rate, batch size 4, and trusted Line/Centerline auxiliary outputs. Candidate code remained architecture-only and did not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, filesystem probes, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Execution result

ABI-252 completed the default 12-epoch exploratory budget without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from Harness-owned artifacts:

- Status: completed.
- Budget: exploratory; no late-improving request.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `all_target_frames`.
- Sample counts after provider-owned capped-record selection: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 5,007,108, below the 25,000,000-parameter ceiling and reduced from ABI-251's 8,959,821 parameters.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 10.07 / 11.08 GiB.
- Training wall time: 2,032.6 s; validation wall time: 1,335.7 s; total Run wall time: 3,370.4 s.

The compact design fixed ABI-251's immediate wall-clock failure and reached all 12 exploratory epochs, but it remains close to the 3,600-second exploratory timeout. A 36-epoch continuation would be plausible only without adding compute, because a simple linear extrapolation is near the 10,800-second late-improving timeout.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 10. Final epoch 12 traded precision/connectivity for higher recall and slightly lower aggregate Dice, so the trajectory is late-ambiguous rather than a clean plateau.

| Metric | ABI-252 best epoch 10 | ABI-252 final epoch 12 | ABI-251 partial epoch 9 | ABI-244 best epoch 11 | ABI-202 best epoch 34 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.387822 | 0.379156 | 0.374710 | 0.392808 | 0.427570 |
| Raw Dice | 0.402662 | 0.392826 | — | — | 0.442746 |
| Filtered precision | 0.418278 | 0.363946 | 0.397295 | 0.397628 | 0.439467 |
| Filtered recall | 0.361500 | 0.395693 | 0.354555 | 0.388104 | 0.416301 |
| Filtered connectivity | 0.326225 | 0.231928 | 0.324284 | 0.290859 | 0.457773 |
| MIT filtered Dice | 0.375267 | 0.375094 | 0.360510 | 0.380020 | 0.411992 |
| Google filtered Dice | 0.418162 | 0.388535 | 0.408881 | 0.426225 | 0.468151 |
| Filtered predicted-positive fraction | 0.003132 | 0.003940 | 0.003234 | 0.005046 | 0.003433 |
| Train loss | 0.859769 | 0.853298 | 0.852242 | — | 0.810439 |
| Validation loss | 0.880046 | 0.883008 | 0.881014 | — | 0.874933 |

Relative to ABI-251's partial epoch-9 signal, ABI-252 is a successful resource-compatible continuation: it improves selected filtered Dice by about +0.0131, MIT Dice by +0.0148, Google Dice by +0.0093, precision by +0.0210, recall by +0.0069, and connectivity by +0.0019 while completing the full exploratory budget.

Relative to ABI-244's completed shifted-window U-NetFormer scout, ABI-252 is slightly lower on selected filtered Dice (-0.0050), MIT Dice (-0.0048), Google Dice (-0.0081), and recall (-0.0266), but higher on precision (+0.0207) and connectivity (+0.0354) at a lower predicted-positive fraction. It does not beat the current ABI-202 aggregate frontier.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.193496 | 0.218108 | 0.155354 | 0.142462 | 0.301504 | 0.104511 | 0.007669 |
| 2 | 0.273762 | 0.280031 | 0.261609 | 0.243531 | 0.312561 | 0.151538 | 0.004651 |
| 3 | 0.274695 | 0.302004 | 0.230503 | 0.212307 | 0.389011 | 0.143455 | 0.006640 |
| 4 | 0.333215 | 0.337735 | 0.323885 | 0.314074 | 0.354841 | 0.202130 | 0.004094 |
| 5 | 0.336353 | 0.335448 | 0.338252 | 0.302948 | 0.378037 | 0.257913 | 0.004522 |
| 6 | 0.353409 | 0.343995 | 0.373989 | 0.372435 | 0.336233 | 0.326112 | 0.003271 |
| 7 | 0.333595 | 0.335250 | 0.330302 | 0.331829 | 0.335380 | 0.217300 | 0.003662 |
| 8 | 0.364499 | 0.359070 | 0.376916 | 0.355989 | 0.373426 | 0.284280 | 0.003801 |
| 9 | 0.363377 | 0.354525 | 0.384995 | 0.386135 | 0.343152 | 0.315183 | 0.003220 |
| 10 | 0.387822 | 0.375267 | 0.418162 | 0.418278 | 0.361500 | 0.326225 | 0.003132 |
| 11 | 0.387041 | 0.376165 | 0.413588 | 0.396761 | 0.377787 | 0.245444 | 0.003450 |
| 12 | 0.379156 | 0.375094 | 0.388535 | 0.363946 | 0.395693 | 0.231928 | 0.003940 |

The trajectory is finite, non-collapsed, and source-informative. Aggregate filtered Dice rises from 0.3645 at epoch 8 to 0.3878 at epoch 10, stays nearly tied at epoch 11, then declines modestly at epoch 12 while recall reaches its run maximum. MIT filtered Dice is stable from epochs 10-12, while Google filtered Dice peaks at epoch 10 and then drops. This is not promotion evidence, but it is enough to avoid treating the compact line-memory U-NetFormer mechanism as exhausted.

## Interpretation

Classify ABI-252 as valid positive feasibility evidence for a compact line-memory U-NetFormer branch. The main scientific result is that row/column line memory plus lower-resolution shifted-window attention can be made resource-compatible under the current exploratory budget, and it preserves or improves the partial signal that ABI-251 showed before timeout.

The branch is still behind ABI-202 and slightly behind ABI-244 on aggregate capped filtered Dice, so it should not be promoted or sent directly to whole-validation diagnostics. However, its best checkpoint is near the exploratory budget end, the final checkpoint remains non-collapsed and source-balanced, and the precision/recall operating point is still changing. This makes a single late-improving close continuation defensible under the approved policy, provided it does not add compute or alter the resource profile.

If a late36 continuation is attempted, it should be an exact or near-exact ABI-252 continuation with the same compact width and no full-resolution attention reintroduced. The purpose would be to test whether the epoch-10/11 near-peak and epoch-12 recall shift mature into a stable ABI-244-beating Result, not to broaden the architecture. If the late36 run plateaus below ABI-244 or times out, the line-memory U-NetFormer branch should stop and the campaign should broaden to another underexplored family.

## Decision

Do not promote ABI-252 and do not request whole-validation diagnostics for it now. Retain ABI-202 as the aggregate whole-validation frontier, ABI-249 as the high-precision C4 orientation-prior comparator, and ABI-244 as the closest completed U-NetFormer comparator.

The next reasonable hypothesis is one late-improving close continuation of ABI-252, using the approved late-improving budget and citing completed parent Run `run_20260911_161019_8c76cd`, because ABI-252 completed, stayed finite, was source-informative, and had its best selected checkpoint near the end of the exploratory budget. Avoid adding compute in that continuation because ABI-252's exploratory wall time already consumed most of the 3,600-second budget.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260911_161019_8c76cd/candidate/PROPOSAL.md`
- `run_20260911_161019_8c76cd/candidate/README.md`
- `run_20260911_161019_8c76cd/candidate/manifest.yaml`
- `run_20260911_161019_8c76cd/resolved_manifest.yaml`
- `run_20260911_161019_8c76cd/outputs/model_summary.json`
- `run_20260911_161019_8c76cd/outputs/best_metrics.json`
- `run_20260911_161019_8c76cd/outputs/final_metrics.json`
- `run_20260911_161019_8c76cd/outputs/metrics.jsonl`
- `run_20260911_161019_8c76cd/outputs/resource_profile.json`
- `run_20260911_161019_8c76cd/outputs/validation_postprocessing/index.json`
- `run_20260911_161019_8c76cd/outputs/prediction_samples/samples.json`
- `run_20260911_150455_d03b0f` for ABI-251 resource-failed line-memory U-NetFormer parent context
- `run_20260911_072719_ade068` for ABI-244 shifted-window U-NetFormer comparator context
- `run_20260911_111909_dd7ef7` for ABI-249 high-precision C4 comparator context
- `run_20260904_043143_ee0005` for ABI-202 current aggregate whole-validation frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`

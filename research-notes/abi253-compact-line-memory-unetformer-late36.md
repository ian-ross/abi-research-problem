# ABI-253 compact line-memory U-NetFormer late36

research-figures: []

## Scope

This note records the bounded late-improving Result for ABI-253, Candidate `abi253_fullspectral_btd_sza_compact_line_memory_unetformer_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260911_171333_f0b603`.

ABI-253 was the exact close continuation of ABI-252. It preserved the compact full-spectral BTD+SZA line-memory U-NetFormer architecture, provider-approved `abi_16ch_plus_sza` input, source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, constant learning rate, batch size 4, and trusted Line/Centerline auxiliary outputs. The only intended change was the approved `late_improving` budget request citing parent Run `run_20260911_161019_8c76cd`. Candidate code remained architecture-only and did not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, filesystem probes, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Execution result

ABI-253 completed the approved late-improving 36-epoch budget without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from Harness-owned artifacts:

- Status: completed.
- Budget request: `late_improving`, approved; parent Run `run_20260911_161019_8c76cd`.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `all_target_frames`.
- Sample counts after provider-owned capped-record selection: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 5,007,108, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 10.07 / 11.08 GB.
- Training wall time: 6,080.9 s; validation wall time: 4,136.9 s; total Run wall time: 10,220.2 s.

The late36 continuation fit within the 10,800-second trusted budget but consumed most of it. That makes further added-compute variants of this family risky unless the architecture is reduced again or the Harness policy changes.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 23. Final epoch 36 remained finite and compact but did not recover the selected epoch's aggregate Dice.

| Metric | ABI-253 best epoch 23 | ABI-253 final epoch 36 | ABI-252 best epoch 10 | ABI-244 best epoch 11 | ABI-202 best epoch 34 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.408323 | 0.396690 | 0.387822 | 0.392808 | 0.427570 |
| Raw Dice | 0.423530 | 0.412543 | 0.402662 | 0.408130 | 0.442746 |
| Filtered precision | 0.444837 | 0.471634 | 0.418278 | 0.397628 | 0.439467 |
| Filtered recall | 0.377349 | 0.342299 | 0.361500 | 0.388104 | 0.416301 |
| Filtered connectivity | 0.326698 | 0.341637 | 0.326225 | 0.290859 | 0.457773 |
| MIT filtered Dice | 0.394406 | 0.383245 | 0.375267 | 0.380020 | 0.411992 |
| Google filtered Dice | 0.442587 | 0.430666 | 0.418162 | 0.426225 | 0.468151 |
| Filtered predicted-positive fraction | 0.003074 | 0.002630 | 0.003132 | 0.005046 | 0.003433 |

Relative to the ABI-252 parent, ABI-253 improves selected filtered Dice by about +0.0205, raw Dice by +0.0209, precision by +0.0266, recall by +0.0158, MIT filtered Dice by +0.0191, and Google filtered Dice by +0.0244 while keeping nearly identical predicted-positive fraction. Relative to ABI-244, ABI-253 improves selected filtered Dice (+0.0055), precision (+0.0472), connectivity (+0.0358), MIT (+0.0144), and Google (+0.0164), but has lower recall (-0.0108). It remains below ABI-202 on aggregate filtered Dice, recall, connectivity, MIT Dice, and Google Dice.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.218221 | 0.230779 | 0.194677 | 0.198871 | 0.241744 | 0.148516 | 0.004405 |
| 6 | 0.351582 | 0.345325 | 0.365168 | 0.344786 | 0.358651 | 0.242588 | 0.003769 |
| 12 | 0.368981 | 0.361338 | 0.386101 | 0.378007 | 0.360376 | 0.205316 | 0.003455 |
| 18 | 0.321188 | 0.303800 | 0.367330 | 0.517335 | 0.232888 | 0.529607 | 0.001631 |
| 23 | 0.408323 | 0.394406 | 0.442587 | 0.444837 | 0.377349 | 0.326698 | 0.003074 |
| 24 | 0.398903 | 0.387477 | 0.425545 | 0.416307 | 0.382896 | 0.226622 | 0.003333 |
| 30 | 0.360949 | 0.355149 | 0.373052 | 0.371295 | 0.351164 | 0.193425 | 0.003427 |
| 34 | 0.402671 | 0.382266 | 0.454918 | 0.483242 | 0.345128 | 0.528696 | 0.002588 |
| 35 | 0.392830 | 0.383376 | 0.415615 | 0.432342 | 0.359936 | 0.304221 | 0.003017 |
| 36 | 0.396690 | 0.383245 | 0.430666 | 0.471634 | 0.342299 | 0.341637 | 0.002630 |

The trajectory validates the late-improving request: ABI-253's best checkpoint occurred well after the 12-epoch exploratory ceiling, and it materially exceeded ABI-252 and ABI-244. The trajectory is also noisy. Epoch 18 and epoch 34 show high-precision/high-connectivity operating points with low predicted-positive fraction, while epoch 23 is the best aggregate source-balanced compromise. After epoch 23 the model did not settle into a clearly stronger final state, and final recall fell below the selected checkpoint.

## Interpretation

Classify ABI-253 as successful late-budget family-development evidence for the compact line-memory U-NetFormer branch. It demonstrates that the reduced ABI-252 design was genuinely truncated by 12 epochs, and that row/column line-memory plus low-resolution shifted-window attention can produce a top-ten capped validation Result under the current policy.

This is not promotion evidence. The best ABI-253 checkpoint is still behind the mature ABI-202 single-frame frontier and behind the strongest temporal late36 candidates on aggregate filtered Dice. Its advantage is a compact, precision-favoring operating point with better connectivity than ABI-244 at much lower predicted-positive fraction, not a new aggregate frontier.

Because the late36 run consumed 10,220 s of a 10,800 s wall-clock budget and selected epoch 23 rather than the final epoch, another exact continuation is not justified. The branch has now answered its main budget question: late training helps, but does not displace ABI-202. Future work should either request trusted whole-validation diagnostics for ABI-253 as a U-NetFormer comparator or broaden to a mechanism-changing architecture rather than adding more attention or repeating the same late-budget run.

## Decision

Do not promote ABI-253 from capped evidence alone. Do not submit another exact compact line-memory U-NetFormer late continuation.

Treat ABI-253 as a viable diagnostic comparator: a future Autonomy Step may consider a whole-validation failure-bucket Evaluation Request for `run_20260911_171333_f0b603` to test whether the capped U-NetFormer improvement over ABI-244 transfers to the canonical Working Validation Split, whether the high-connectivity epoch-34 behavior corresponds to useful line continuity or over-pruned recall, and whether MIT remains the limiting source. If not requesting diagnostics next, broaden away from this branch toward a distinct in-contract mechanism such as temporal change modeling, recall-preserving calibration, or another lightweight modern backbone.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260911_171333_f0b603/candidate/PROPOSAL.md`
- `run_20260911_171333_f0b603/candidate/README.md`
- `run_20260911_171333_f0b603/candidate/manifest.yaml`
- `run_20260911_171333_f0b603/candidate/budget_request.yaml`
- `run_20260911_171333_f0b603/resolved_manifest.yaml`
- `run_20260911_171333_f0b603/outputs/model_summary.json`
- `run_20260911_171333_f0b603/outputs/best_metrics.json`
- `run_20260911_171333_f0b603/outputs/final_metrics.json`
- `run_20260911_171333_f0b603/outputs/metrics.jsonl`
- `run_20260911_171333_f0b603/outputs/resource_profile.json`
- `run_20260911_171333_f0b603/outputs/validation_postprocessing/index.json`
- `run_20260911_171333_f0b603/outputs/prediction_samples/samples.json`
- `run_20260911_161019_8c76cd` for ABI-252 parent context
- `run_20260911_072719_ade068` for ABI-244 shifted-window U-NetFormer comparator context
- `run_20260911_111909_dd7ef7` for ABI-249 high-precision C4 comparator context
- `run_20260908_154531_8c7e2b` for ABI-223 temporal late36 comparator context
- `run_20260904_043143_ee0005` for ABI-202 current aggregate whole-validation frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`

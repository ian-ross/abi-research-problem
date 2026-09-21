# ABI-274 temporal line-state attention U-Net late36

research-figures: []

## Scope

This note records the bounded late-improving Result for ABI-274, Candidate `abi274_temporal_line_state_attention_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260912_180856_79ba22`.

ABI-274 was an exact close continuation of ABI-273. It preserved the provider-owned `abi_16ch_plus_sza_temporal` input path with offsets `[-1, 0, 1]`, trusted `temporal_eligible_center` selection, source-balanced sampling, random mirroring, BCE-Dice, batch size 2, and Line plus Centerline auxiliary targets. The architecture reused ABI-273's early temporal line-state mechanism: temporal-attention/change features form a full-resolution orientation-aware line state, and lightweight gates inject that bounded state into encoder scales before the ASPP decoder.

The Candidate remained architecture/manifest-only. It did not own data loading, temporal lookup, frame repair, sample selection, sampling implementation, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle behavior.

## Execution result

ABI-274 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from Harness-owned artifacts:

- Status: completed.
- Requested/effective budget: `late_improving`, 36 epochs.
- Parent Run: ABI-273, `run_20260912_171825_ff0d00`.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Sample counts after capped temporal-eligible selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,243,288, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 5.02 / 5.36 GB.
- Training wall time: 4,299.8 s; validation wall time: 3,239.1 s; total Run wall time: 7,541.0 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 36.

This is valid finite capped temporal-eligible validation evidence. It is not whole-validation promotion evidence and is not directly equivalent to full Working Validation Split evidence.

## Best-validation metrics

| Metric | ABI-274 best epoch 36 | ABI-273 parent | ABI-238 temporal directional late36 | ABI-223 temporal attention late36 | ABI-255 recurrent temporal late36 | ABI-202 aggregate reference |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.419364 | 0.389683 | 0.420235 | 0.419776 | 0.417348 | 0.427570 |
| Raw Dice | 0.436760 | 0.406280 | 0.438718 | 0.438487 | 0.435656 | 0.442746 |
| Filtered precision | 0.454127 | 0.446534 | 0.488730 | 0.483764 | 0.468293 | 0.439467 |
| Filtered recall | 0.389545 | 0.345673 | 0.368578 | 0.370738 | 0.376400 | 0.416301 |
| Filtered connectivity | 0.282911 | 0.283368 | 0.352239 | 0.412427 | 0.281116 | 0.457773 |
| MIT filtered Dice | 0.399386 | 0.369240 | 0.405383 | 0.398498 | 0.400833 | 0.411992 |
| Google filtered Dice | 0.472606 | 0.441559 | 0.460838 | 0.476764 | 0.463143 | 0.468151 |
| Filtered predicted-positive fraction | 0.004434 | 0.004002 | 0.003899 | 0.003962 | 0.004155 | 0.003433 |

ABI-274 materially improves the ABI-273 parent: about +0.0297 filtered Dice, +0.0439 recall, +0.0301 MIT filtered Dice, +0.0310 Google filtered Dice, and +0.0076 precision. The only parent-side target it does not improve is connectivity, which is essentially tied but slightly lower (-0.0005). The approved late budget therefore converted ABI-273's final-epoch signal into a strong capped temporal-eligible primary score and better source balance, but not into better connected-line continuity.

Relative to the mature temporal comparators, ABI-274 reaches the ABI-223/238 filtered-Dice band but does so with a different tradeoff. It is only about -0.0009 below ABI-238 and -0.0004 below ABI-223 on filtered Dice, has higher recall than both, and has higher Google filtered Dice than ABI-238. However, it loses precision by about 0.03-0.035 and remains far weaker on connectivity, especially versus ABI-223. Relative to ABI-255, ABI-274 has slightly better aggregate Dice, recall, Google Dice, and nearly the same connectivity, but slightly lower MIT Dice and precision.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.235043 | 0.237767 | 0.229018 | 0.239865 | 0.230412 | 0.183454 | 0.004966 |
| 6 | 0.380024 | 0.361224 | 0.427588 | 0.415525 | 0.350111 | 0.310550 | 0.004356 |
| 12 | 0.372487 | 0.351317 | 0.427884 | 0.472887 | 0.307254 | 0.259753 | 0.003359 |
| 16 | 0.401927 | 0.374659 | 0.473484 | 0.475558 | 0.348039 | 0.353290 | 0.003783 |
| 18 | 0.395264 | 0.381802 | 0.427346 | 0.356493 | 0.443498 | 0.208811 | 0.006431 |
| 20 | 0.351768 | 0.321272 | 0.433056 | 0.564623 | 0.255463 | 0.404106 | 0.002339 |
| 22 | 0.403026 | 0.384815 | 0.449093 | 0.436498 | 0.374322 | 0.206854 | 0.004433 |
| 24 | 0.389736 | 0.363808 | 0.457563 | 0.504560 | 0.317486 | 0.253394 | 0.003253 |
| 27 | 0.404443 | 0.381913 | 0.463909 | 0.471173 | 0.354270 | 0.300471 | 0.003887 |
| 29 | 0.414987 | 0.391431 | 0.476428 | 0.442178 | 0.390946 | 0.268979 | 0.004571 |
| 31 | 0.410486 | 0.391305 | 0.460355 | 0.437628 | 0.386513 | 0.246204 | 0.004566 |
| 33 | 0.409687 | 0.386240 | 0.472561 | 0.498650 | 0.347661 | 0.380866 | 0.003604 |
| 34 | 0.412294 | 0.395267 | 0.456510 | 0.415666 | 0.408976 | 0.221941 | 0.005086 |
| 35 | 0.398871 | 0.384674 | 0.437280 | 0.507140 | 0.328698 | 0.337651 | 0.003351 |
| 36 | 0.419364 | 0.399386 | 0.472606 | 0.454127 | 0.389545 | 0.282911 | 0.004434 |

The trajectory is finite, source-informative, and non-collapsed. The selected checkpoint is the final late-budget epoch, and late epochs repeatedly exceed the parent ABI-273's 0.3897 filtered Dice. The run remains noisy: high-connectivity epochs are generally conservative and lower-recall, while the highest-recall epochs expand positives and lose connectivity. Epoch 36 is the best aggregate/source-Dice checkpoint, but it does not stabilize the stronger connectivity signatures seen at epochs 20 and 33.

## Interpretation

Classify ABI-274 as a positive late-budget temporal-family continuation and a useful temporal comparator, but not a clear promotion candidate. The late budget confirms that ABI-273 was budget-limited: the exact early-line-state architecture moves from a mid-pack exploratory score to the ABI-223/238 temporal primary-Dice band and surpasses ABI-255 on capped temporal-eligible filtered Dice.

The main unresolved weakness is the same one targeted by the hypothesis: connected thin-line continuity. ABI-274 improves recall and source balance without an ABI-271-style precision collapse, but its selected connectivity remains near ABI-273/255 and well below ABI-223/238/202. The early line-state mechanism appears to sharpen temporal evidence enough for primary Dice, especially on Google validation records, but it does not reliably preserve continuous thin structures at the selected threshold.

Because ABI-274 uses the temporal-eligible population, compare it primarily against temporal-eligible capped and diagnostic Results. It should not be interpreted as whole-validation evidence against ABI-202/249. Its source behavior is encouraging, but its connectivity deficit argues against promotion without additional trusted diagnostics.

## Decision

Do not promote ABI-274 directly from this capped temporal-eligible Result. Do not repeat unchanged late36 training of the exact ABI-273/274 early-line-state injector; it already used the approved longer budget and still did not solve the connectivity objective.

A later, separate Autonomy Step may reasonably consider a bounded temporal-eligible Evaluation Request for ABI-274 because it reaches the ABI-223/238 primary-Dice band and beats ABI-255 on capped filtered Dice. If the campaign instead continues with new Runs, prefer mechanism-changing temporal work that preserves ABI-274's recall/source lift while adding stronger connectivity support, or broaden to C4/orientation-prior plus recall support. Avoid another focal-Tversky-only temporal loss swap or final-head-only dual-evidence variant.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260912_180856_79ba22/candidate/PROPOSAL.md`
- `run_20260912_180856_79ba22/candidate/README.md`
- `run_20260912_180856_79ba22/candidate/manifest.yaml`
- `run_20260912_180856_79ba22/candidate/budget_request.yaml`
- `run_20260912_180856_79ba22/resolved_manifest.yaml`
- `run_20260912_180856_79ba22/outputs/model_summary.json`
- `run_20260912_180856_79ba22/outputs/best_metrics.json`
- `run_20260912_180856_79ba22/outputs/final_metrics.json`
- `run_20260912_180856_79ba22/outputs/metrics.jsonl`
- `run_20260912_180856_79ba22/outputs/resource_profile.json`
- `run_20260912_180856_79ba22/outputs/validation_postprocessing/index.json`
- `run_20260912_180856_79ba22/outputs/prediction_samples/samples.json`
- `run_20260912_171825_ff0d00` for ABI-273 exploratory parent context
- `run_20260911_004137_f54c45` for ABI-238 temporal directional-context comparator context
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-attention comparator context
- `run_20260911_210922_27f346` for ABI-255 recurrent temporal comparator context
- `run_20260904_043143_ee0005` for ABI-202 aggregate reference context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`

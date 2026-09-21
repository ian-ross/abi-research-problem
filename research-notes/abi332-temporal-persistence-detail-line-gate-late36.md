# ABI-332 temporal persistence/detail line-gate late36

research-figures: []

## Scope

This note records ABI-332, Candidate `abi332_temporal_persistence_detail_line_gate_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260917_115326_f1e460`.

ABI-332 was a late-improving continuation of ABI-331. It kept the same compact three-frame temporal persistence/detail line-gate U-Net and consumed provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`. The purpose was to test whether ABI-331's final-epoch exploratory best checkpoint was budget-truncated, not to claim promotion readiness.

This is capped temporal-eligible feasibility evidence only. It is not whole Working Validation Split promotion evidence and should not be compared as a promotion Result against full-validation ABI-202/249.

## Execution result

ABI-332 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Budget: approved `late_improving`, requested and effective 36 epochs; parent Runs `run_20260917_105650_6a68cc` and `run_20260915_183315_3f1d30`.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Capped temporal-eligible sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 2,690,739, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 4,322,569,728 / 4,720,689,152 bytes.
- Training wall time: 4,782.4 s; validation wall time: 3,938.0 s; total Run wall time: 8,722.3 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 36.

## Best-validation metrics

| Metric | ABI-332 late36 | ABI-331 exploratory parent | Delta vs ABI-331 | ABI-319 shift-bank C4 | ABI-324 five-frame detail consensus | ABI-326 selective-tail guard | ABI-328 soft-shift align | ABI-223 temporal-attention |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 36 | 12 | +24 | 10 | 27 | 36 | 36 | 36 |
| Filtered Dice | 0.413321 | 0.391024 | +0.022297 | 0.405847 | 0.429430 | 0.424161 | 0.423805 | 0.419776 |
| MIT filtered Dice | 0.394660 | 0.373811 | +0.020849 | 0.387897 | 0.408188 | 0.406687 | 0.403841 | 0.398498 |
| Google filtered Dice | 0.460548 | 0.436055 | +0.024492 | 0.451369 | 0.487231 | 0.471630 | 0.476913 | 0.476764 |
| Filtered precision | 0.466793 | 0.481788 | -0.014995 | 0.463906 | 0.470412 | 0.447015 | 0.444466 | 0.483764 |
| Filtered recall | 0.370840 | 0.329036 | +0.041804 | 0.360703 | 0.395017 | 0.403530 | 0.404980 | 0.370738 |
| Filtered connectivity | 0.365588 | 0.361417 | +0.004171 | 0.360704 | 0.397925 | 0.268164 | 0.322966 | 0.412427 |
| Filtered predicted-positive pixels | 434,411 | 373,444 | +60,967 | 425,166 | 459,172 | 493,619 | 498,234 | 419,056 |

The late budget materially improved ABI-331. ABI-332 raised aggregate filtered Dice by about +0.0223, both Dataset Source Dice scores by about +0.021 to +0.024, and recall by about +0.0418. Connectivity improved only slightly, and precision dropped by about -0.015 as the footprint expanded.

Against broader temporal comparators, ABI-332 is useful but not a new frontier. It surpasses ABI-319's exploratory filtered Dice and recall while preserving similar precision/connectivity. It remains below ABI-324, ABI-326, and ABI-328 on aggregate filtered Dice, below ABI-324/326/328 on MIT Dice, and below ABI-223 on connectivity and precision. ABI-332's main strength is a clean, resource-safe late improvement from the compact three-frame persistence/detail branch; its remaining weakness is not enough source-balanced recall/connectivity to displace the recent five-frame/C4 temporal comparators.

At the selected checkpoint, raw Dice was 0.431538 versus filtered Dice 0.413321, raw recall was 0.400843 versus filtered recall 0.370840, and raw predicted-positive pixels were 469,024 versus 434,411 filtered. Artifact Filters reduce footprint and score; they do not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.241032 | 0.249333 | 0.222917 | 0.223470 | 0.261589 | 0.154480 | 0.006051 |
| 2 | 0.282356 | 0.274112 | 0.305177 | 0.419649 | 0.212751 | 0.334461 | 0.002621 |
| 3 | 0.314554 | 0.299087 | 0.353456 | 0.420448 | 0.251269 | 0.281966 | 0.003089 |
| 4 | 0.330055 | 0.314041 | 0.370598 | 0.394054 | 0.283940 | 0.278952 | 0.003725 |
| 5 | 0.376080 | 0.363606 | 0.406978 | 0.417903 | 0.341867 | 0.288531 | 0.004229 |
| 6 | 0.353750 | 0.335978 | 0.400358 | 0.468129 | 0.284290 | 0.357255 | 0.003139 |
| 7 | 0.364207 | 0.343262 | 0.419740 | 0.508289 | 0.283768 | 0.406770 | 0.002886 |
| 8 | 0.376808 | 0.364877 | 0.408085 | 0.402809 | 0.353961 | 0.277283 | 0.004543 |
| 9 | 0.392703 | 0.381043 | 0.422362 | 0.408591 | 0.378004 | 0.316529 | 0.004783 |
| 10 | 0.358814 | 0.335488 | 0.419675 | 0.497587 | 0.280566 | 0.372602 | 0.002915 |
| 11 | 0.378972 | 0.364657 | 0.413963 | 0.397470 | 0.362119 | 0.271622 | 0.004710 |
| 12 | 0.381735 | 0.364171 | 0.427850 | 0.478205 | 0.317654 | 0.370837 | 0.003434 |
| 13 | 0.357746 | 0.334067 | 0.416956 | 0.456884 | 0.293960 | 0.324380 | 0.003326 |
| 14 | 0.377208 | 0.352065 | 0.443217 | 0.513642 | 0.298042 | 0.387212 | 0.003000 |
| 15 | 0.387599 | 0.367208 | 0.440358 | 0.472404 | 0.328608 | 0.372265 | 0.003596 |
| 16 | 0.384198 | 0.362165 | 0.442099 | 0.482923 | 0.318987 | 0.349850 | 0.003415 |
| 17 | 0.389711 | 0.372107 | 0.432390 | 0.418962 | 0.364277 | 0.262674 | 0.004495 |
| 18 | 0.399021 | 0.387254 | 0.427414 | 0.379685 | 0.420433 | 0.266255 | 0.005724 |
| 19 | 0.392789 | 0.367769 | 0.459887 | 0.507756 | 0.320273 | 0.405912 | 0.003261 |
| 20 | 0.360797 | 0.334688 | 0.428772 | 0.538086 | 0.271382 | 0.414558 | 0.002607 |
| 21 | 0.383912 | 0.356533 | 0.453455 | 0.478456 | 0.320567 | 0.384728 | 0.003464 |
| 22 | 0.395520 | 0.374072 | 0.452524 | 0.496950 | 0.328477 | 0.415433 | 0.003417 |
| 23 | 0.364278 | 0.338351 | 0.433933 | 0.537153 | 0.275585 | 0.449434 | 0.002652 |
| 24 | 0.384266 | 0.359115 | 0.448592 | 0.505247 | 0.310030 | 0.366760 | 0.003172 |
| 25 | 0.389018 | 0.362225 | 0.457990 | 0.502534 | 0.317336 | 0.381519 | 0.003264 |
| 26 | 0.408212 | 0.395363 | 0.440012 | 0.400152 | 0.416604 | 0.299470 | 0.005382 |
| 27 | 0.357653 | 0.329345 | 0.430126 | 0.475669 | 0.286557 | 0.345291 | 0.003114 |
| 28 | 0.404886 | 0.388557 | 0.446062 | 0.452604 | 0.366270 | 0.345050 | 0.004183 |
| 29 | 0.398015 | 0.373698 | 0.461781 | 0.501066 | 0.330121 | 0.417150 | 0.003406 |
| 30 | 0.401565 | 0.378777 | 0.458929 | 0.471065 | 0.349936 | 0.379122 | 0.003840 |
| 31 | 0.391523 | 0.367762 | 0.455699 | 0.531910 | 0.309766 | 0.469851 | 0.003011 |
| 32 | 0.405594 | 0.382021 | 0.467494 | 0.481880 | 0.350161 | 0.369657 | 0.003756 |
| 33 | 0.371696 | 0.345593 | 0.442141 | 0.569058 | 0.275980 | 0.460084 | 0.002507 |
| 34 | 0.400775 | 0.378203 | 0.460647 | 0.516519 | 0.327409 | 0.431389 | 0.003277 |
| 35 | 0.395741 | 0.374068 | 0.452559 | 0.508194 | 0.324038 | 0.425025 | 0.003296 |
| 36 | 0.413321 | 0.394660 | 0.460548 | 0.466793 | 0.370840 | 0.365588 | 0.004107 |

The learning curve validates the late-improving-budget premise. Epoch 36 is the selected checkpoint and exceeds the epoch-12 exploratory parent region. The trajectory is noisy, with alternating high-precision compact states and higher-recall broader states. The best aggregate checkpoint is not the maximum recall epoch (epoch 18) or maximum connectivity epoch (epoch 31); it is a more balanced late state. This suggests the architecture continues to find usable temporal evidence after epoch 12 but does not settle into a clearly superior connected-line solution.

## Prediction sample check

The retained fixed first-four validation samples are Harness traceability artifacts, not representative diagnostics. Their sample Dice values were 0.4076, 0.7010, 0.6470, and 0.3850. This confirms finite non-collapsed predictions on retained examples, but it does not change the aggregate evidence that ABI-332 remains below the strongest recent temporal comparators.

## Interpretation

Classify ABI-332 as positive evidence for the specific late-budget continuation of the ABI-331 compact persistence/detail line-gate mechanism. The longer budget was warranted: the exact branch improved materially over its 12-epoch parent and now beats ABI-319's exploratory temporal shift-bank/C4 score on aggregate filtered Dice and recall.

However, ABI-332 is still not a promotion candidate and not the temporal frontier. Its improvements come with a larger footprint and slightly lower precision than ABI-331, while connectivity barely improves. It remains below ABI-324/326/328 aggregate temporal C4 late-budget comparators and below ABI-223's temporal-attention connectivity. The exact unchanged compact persistence/detail branch has likely reached useful but sub-frontier evidence: the issue is no longer under-training alone, but insufficient connected thin-line support and source-balanced recall relative to the stronger C4/five-frame temporal mechanisms.

Comparator roles after ABI-332:

- ABI-324 remains the strongest balanced recent temporal C4 aggregate/source/connectivity comparator.
- ABI-326/328 remain stronger late-budget temporal C4 recall/aggregate comparators, despite weaker connectivity than ABI-324 or ABI-223.
- ABI-223 remains the temporal-attention connectivity comparator.
- ABI-331 is superseded by ABI-332 for the compact three-frame persistence/detail line-gate branch.
- ABI-319 remains a useful exploratory three-frame comparator, but ABI-332 is now stronger on aggregate/source Dice and recall.

ABI-332 does not justify Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle changes.

## Decision

Do not promote ABI-332 and do not request whole-validation-style evaluation from this capped temporal-eligible Result. A temporal-eligible failure-bucket Evaluation Request is not immediately necessary because the aggregate/source/precision/recall/connectivity metrics already show the main failure mode: positive late learning, but no connectivity or aggregate advantage over ABI-324/326/328/223.

Do not spend another Run on an unchanged late36 continuation of the ABI-331/332 compact persistence/detail gate. Further work may reuse the cheap persistence/detail idea only if it introduces a mechanism-changing recall/connectivity support path, such as explicit orientation consensus, better temporal alignment, or calibration that raises true contrail logits without broad clutter. Otherwise broaden the next hypothesis to a different temporal attention/alignment, calibration, data-policy, loss, or line-continuity direction.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260917_115326_f1e460/candidate/PROPOSAL.md`
- `run_20260917_115326_f1e460/candidate/README.md`
- `run_20260917_115326_f1e460/candidate/manifest.yaml`
- `run_20260917_115326_f1e460/candidate/budget_request.yaml`
- `run_20260917_115326_f1e460/resolved_manifest.yaml`
- `run_20260917_115326_f1e460/execution.json`
- `run_20260917_115326_f1e460/outputs/model_summary.json`
- `run_20260917_115326_f1e460/outputs/best_metrics.json`
- `run_20260917_115326_f1e460/outputs/final_metrics.json`
- `run_20260917_115326_f1e460/outputs/metrics.jsonl`
- `run_20260917_115326_f1e460/outputs/resource_profile.json`
- `run_20260917_115326_f1e460/outputs/validation_postprocessing/index.json`
- `run_20260917_115326_f1e460/outputs/prediction_samples/samples.json`
- `run_20260917_105650_6a68cc/outputs/best_metrics.json` and `/history/research-notes/abi331-temporal-persistence-detail-line-gate-unet.md` for ABI-331 comparison context
- `run_20260915_183315_3f1d30/outputs/best_metrics.json` and `/history/research-notes/abi321-temporal-attention-center-detail-evidence-sharpening-unet.md` for ABI-321 comparison context
- `run_20260915_162050_163586/outputs/best_metrics.json` and `/history/research-notes/abi319-temporal-shiftbank-c4-alignment-confidence-line-unet.md` for ABI-319 comparison context
- `run_20260916_184108_954ec7/outputs/best_metrics.json` and `/history/research-notes/abi324-temporal-fiveframe-detail-consensus-stabilized-line-state-late36.md` for ABI-324 comparison context
- `run_20260917_002229_d43b7a/outputs/best_metrics.json` and `/history/research-notes/abi326-temporal-fiveframe-selective-tail-consensus-guard-late36.md` for ABI-326 comparison context
- `run_20260917_055012_ba7890/outputs/best_metrics.json` and `/history/research-notes/abi328-temporal-fiveframe-softshift-alignment-c4-line-state-late36.md` for ABI-328 comparison context
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/aggregate_metrics.json` and `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md` for ABI-223 comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`

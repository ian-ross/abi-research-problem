# Temporal C4 frontier reset after ABI-348

research-figures: []

## Scope

This note synthesizes the recent late-budget temporal-family evidence through ABI-348 and records a mechanism-changing next-hypothesis plan. It is a Research Note only: no Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step.

The primary recent evidence is bounded temporal-eligible capped evidence, not whole Working Validation Split promotion evidence. The temporal-eligible validation population remains the provider-owned 1,614 ABI Patch subset for trusted temporal windows; Candidate code still must not own temporal lookup, cache access, data loading, targets, losses, metrics, Artifact Filters, thresholds, postprocessing, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle behavior.

## Current comparator state

Whole-validation roles remain unchanged:

- ABI-202 remains the aggregate whole-validation filtered-Dice reference.
- ABI-249 remains the compact high-precision single-frame C4/orientation comparator.

On the temporal-eligible capped population, the recent working comparator roles are now:

| Role | Candidate / Run | Filtered Dice | MIT | Google | Precision | Recall | Connectivity | Interpretation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Balanced five-frame temporal C4/detail-consensus comparator | ABI-324 / `run_20260916_184108_954ec7` | 0.4294 | 0.4082 | 0.4872 | 0.4704 | 0.3950 | 0.3979 | Strongest local temporal C4 balance |
| Five-frame compact high-precision variant | ABI-348 / `run_20260918_215534_a35ab9` | 0.4278 | 0.4102 | 0.4784 | 0.4775 | 0.3875 | 0.3009 | Cleaner high-tail negative clutter, but weak connectivity |
| No-mirroring/data-policy diagnostic | ABI-337 / `run_20260917_201833_57b081` | 0.4289 | 0.4118 | 0.4763 | 0.4665 | 0.3969 | 0.3653 | Useful policy evidence, not displaced |
| Positive-tail broad-recall diagnostic | ABI-344 / `run_20260918_105020_e806bb` | 0.4264 | 0.4122 | 0.4626 | 0.4267 | 0.4262 | 0.3157 | Recovers recall with broad footprint |
| Temporal-attention connectivity comparator | ABI-223 / `run_20260908_154531_8c7e2b` | 0.4198 | 0.3985 | 0.4768 | 0.4838 | 0.3707 | 0.4124 | Best temporal-attention connectivity reference |
| Compact high-precision temporal C4 comparator | ABI-306 / `run_20260914_124245_de843c` | 0.4225 | 0.4028 | 0.4762 | 0.4934 | 0.3695 | 0.2994 | Compact/precision reference |

ABI-348 is close to ABI-324 on aggregate Dice and slightly higher on precision/compactness, but its selected checkpoint is ABI-306-like on connectivity. It should not replace ABI-324 or ABI-223 as a temporal-family comparator.

## What the recent branch answered

The ABI-341/344/346/347/348 sequence gives enough bounded evidence about late C4/detail-consensus final-head and soft-band recall variants:

- Positive-tail recall can be recovered, but broad recall states repeatedly add negative-patch clutter and weaken connectivity.
- Compact precision states can be selected, but they generally give back positive-tail recall and do not solve MIT/source-balanced undercoverage.
- Orientation or dual-state guards can shrink footprint, but selected checkpoints still decouple aggregate Dice from connected-line continuity.
- Temporal C4 heads often show transient high-connectivity epochs, but those epochs do not align with best fixed-threshold Dice/source balance.

Therefore, another unchanged late36 temporal C4 final-head blend, uncertainty-band residual, recall router, or simple gain/veto adjustment is not justified. Low score alone is not the reason; the branch has now repeatedly characterized the same failure mode under finite, source-informative, late-budget Runs.

## Remaining failure mode

The central unsolved issue is not simply calibration or final-logit footprint size. The recent Runs show a three-way tension:

1. **Fixed-threshold positive-tail recall**: ABI-344/341/346 can reduce complete misses or low-recall positives.
2. **Negative-patch high-tail clutter**: ABI-348 suppresses this better than broad recall sidecars.
3. **Connected thin-line continuity**: ABI-324 and ABI-223 remain stronger; ABI-348 drops to about 0.3009 connectivity despite competitive Dice.

MIT remains harder than Google, especially for positive median recall/connectivity and negative-patch clutter tails. Any next Candidate should target true-positive line evidence before final logits, not rely on another final-head residual to move the operating point.

## Recommended next hypotheses

A useful next Candidate should broaden or materially change mechanism. Highest-value in-contract options are:

1. **Temporal-attention anchor with pre-decoder line support**: return toward ABI-223/238-style temporal attention, but add a small pre-decoder center-detail/line-support path that raises true contrail evidence before final logits. This should preserve a compact connected anchor first, then expose bounded recall support only through high-resolution center-frame detail and temporal agreement. Run as exploratory if the implementation is materially different from ABI-223/238; request late-improving only if the exploratory trajectory clearly supports it.

2. **Single-frame C4 compact anchor plus cross-scale detail sidecar**: revisit ABI-249's high-precision C4 branch, but avoid ABI-342/343-style direct recall residuals. The mechanism should separate a stable compact anchor from a cross-scale detail/Line/Centerline agreement sidecar that operates before the final mask head. The success criterion should be improved recall/connectivity without losing ABI-249's precision by more than a small bounded amount.

3. **Modern lightweight backbone scout with explicit line-continuity decoder**: a new compact backbone is acceptable only if it is not just extra attention capacity. It should explain how token/patch features are reprojected into thin center-frame detail and how the decoder protects connectivity. Because this would be a materially different family, it should be sequential exploratory evidence first.

4. **Trusted policy/loss direction only if mechanism-tied**: another loss or data-policy run should not be a generic retry. It should be attached to a specific observed failure mode, such as source-balanced MIT recall or connected-line continuity, and remain within the provider/Harness allowlists.

## Decision

Do not promote ABI-348. Do not spend the next Run on another unchanged temporal C4 final-head continuation. The next research handoff should be a mechanism-changing Candidate, preferably a temporal-attention or single-frame C4 anchor design that raises true contrail logits before final mask logits while explicitly guarding source balance, fixed-threshold recall, negative-patch clutter, and connected-line continuity.

## Artifact references

- `run_20260918_215534_a35ab9/outputs/best_metrics.json`
- `run_20260918_215534_a35ab9/outputs/evaluations/eval_evalreq_abi348_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260918_215534_a35ab9/outputs/evaluations/eval_evalreq_abi348_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `/history/research-notes/abi348-temporal-fiveframe-dual-state-connectivity-blend-late36.md`
- `/history/research-notes/abi347-temporal-c4-orientation-bridge-compact-recall-late36.md`
- `/history/research-notes/abi346-temporal-eligible-failure-bucket-review.md`
- `/history/research-notes/abi344-temporal-fiveframe-connectivity-anchor-recall-sidecar-late36.md`
- `/history/research-notes/abi341-temporal-fiveframe-compact-continuity-recall-router-late36.md`
- `/history/research-notes/abi324-temporal-eligible-failure-bucket-review.md`
- `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`

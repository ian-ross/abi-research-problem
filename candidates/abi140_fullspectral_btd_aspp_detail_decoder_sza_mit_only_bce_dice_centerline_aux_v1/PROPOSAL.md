# ABI-140 Full-spectral BTD+SZA ASPP/detail decoder MIT-only BCE-Dice Centerline auxiliary

## Hypothesis

ABI-130 established the strongest SZA-aware ASPP/detail capped reference, with high Google filtered Dice and good precision but weaker MIT recall than the ABI-068 aggregate reference. A trusted `mit_only` training traversal for the same ABI-130 architecture may recover MIT recall/source balance while revealing whether the SZA+BCE-Dice ASPP/detail representation transfers robustly back to Google. This is a **family-development continuation** and data-policy diagnostic, not a full-data promotion claim.

## Comparison Target

The primary comparison target is ABI-130 (`run_20260831_121006_7d24be`), which used the same architecture/input/loss/auxiliary settings under `combined_source_balanced` traversal and reached capped `val/filtered_dice` 0.3953, MIT filtered Dice 0.3779, Google filtered Dice 0.4404, filtered precision 0.4415, filtered recall 0.3578, filtered connectivity 0.3851, and filtered predicted-positive fraction 0.00294.

Secondary context is ABI-126 (`run_20260831_085615_d05ab3`) as the non-SZA ASPP/detail BCE-Dice precision/connectivity comparator, ABI-068 (`run_20260828_010836_4ccc77`) as the capped aggregate/source-balance reference, and ABI-115 (`run_20260830_235533_487b1c`) as evidence that MIT-only traversal was negative for the frequency-gated focal-Tversky branch.

## Expected Effect

Compared with ABI-130, ABI-140 is expected to increase MIT filtered recall and possibly MIT filtered Dice by emphasizing the MIT training distribution within the trusted capped selection. The expected risk is reduced Google filtered Dice, weaker precision, or larger predicted-positive fraction if MIT-only traversal encourages source-specific recall-heavy clutter. A useful result would show that the ASPP/detail SZA+BCE representation can recover MIT sensitivity without losing the high-precision Google operating point entirely.

## Implementation Sketch

Reuse the ABI-130 model architecture unchanged: normalize approved ABI channels 1-16, derive deterministic thermal BTD planes from approved ABI channels only, add normalized SZA and `cos(SZA)` features from provider-approved Solar Geometry Input, pass the feature stack through the compact ASPP/detail encoder-decoder, and return `mask_logits` plus the provider-declared `centerline_logits` auxiliary output.

The controlled change is only in `manifest.yaml`: set `data.sampling_policy: mit_only` while retaining `input_mode: abi_16ch_plus_sza`, trusted `bce_dice` primary loss, Centerline Target auxiliary `weighted_bce` at weight 0.02, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, max epochs 12, and `constant_lr` scheduler.

## Contract Features Used

- Provider-approved `abi_16ch_plus_sza` input containing GOES ABI channels 1-16 plus Solar Geometry Input.
- No longitude or latitude inputs, reconstruction, or Dataset Source features in candidate code.
- Candidate-owned PyTorch architecture only; provider/Harness owns data loading, Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, prediction retention, resource placement, and Run lifecycle.
- Trusted `mit_only` sampling policy selected by manifest.
- Trusted `random_mirroring` augmentation selected by manifest.
- Trusted `bce_dice` primary loss selected by manifest.
- Provider-derived `centerline` auxiliary target with trusted `weighted_bce` loss at weight 0.02.
- AdamW, batch size 4, 12 epochs, and `constant_lr` within the generated Workspace Configuration limits.

## Budget Requested

Run one capped representative Candidate Experiment under the active Harness limits: at most 1,024 records per Dataset Source and Leakage-Safe Split, batch size 4, max epochs 12, constant learning rate, disabled early stopping, at most four fixed `first_n` prediction artifacts, 25 million parameter smoke ceiling, A100 GPU 0, concurrency one, and 3,600-second Docker training timeout.

## Success Criteria

Treat this as capped family-development evidence. Useful positive evidence would include all of the following:

- finite training and validation with no all-negative or all-positive prediction collapse;
- MIT filtered Dice improves over ABI-130 by at least about 0.015 or MIT filtered recall improves by at least about 0.04;
- aggregate filtered Dice remains within about 0.02 of ABI-130;
- Google filtered Dice remains at least 0.40 so the traversal does not catastrophically lose source transfer;
- filtered predicted-positive fraction remains below about 0.0045 and raw-to-filtered differences remain modest, indicating no primary Artifact Filter dependence;
- filtered connectivity remains at least about 0.35.

Promotion would require stronger evidence than this capped run, including human review and full-data context against canonical MCAST baselines.

## Fallback/Next Decision

If ABI-140 improves MIT recall but loses Google transfer or precision, record it as data-policy/source-transfer evidence and prefer source-balanced traversal for promotion-oriented candidates. If it matches ABI-130 while improving MIT sensitivity, consider a bounded follow-up that investigates source-robust calibration without candidate-owned sampling or thresholding. If it behaves like ABI-115 with recall-heavy clutter and lower source Dice, stop simple MIT-only traversal for this branch and broaden to a different architecture, loss/data policy, preprocessing/calibration mechanism, or provider-reviewed capability request.

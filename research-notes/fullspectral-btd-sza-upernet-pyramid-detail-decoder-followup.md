# Full-spectral BTD+SZA UPerNet pyramid/detail decoder follow-up

research-figures: []

## Scope

This note records ABI-179 after Run `run_20260902_054206_a6b406` completed.

Source Runs:

- ABI-179 full-spectral BTD+SZA UPerNet pyramid/detail decoder BCE-Dice Centerline-auxiliary scout: `run_20260902_054206_a6b406`
- ABI-173 signed-detail full-scale skip ASPP decoder parent/reference: `run_20260901_234732_bd5917`; Evaluation `eval_evalreq_abi173_wholeval_failure_buckets_v1`
- ABI-154 full-scale skip ASPP/detail decoder precision/connectivity reference: `run_20260901_071026_32d3ec`
- ABI-130 prior SZA-aware ASPP/detail aggregate reference: `run_20260831_121006_7d24be`
- ABI-068 frequency-gated line U-Net broader capped aggregate/source-balance comparator: `run_20260828_010836_4ccc77`
- ABI-178 thermal-only signed-detail ASPP input-frontier negative control: `run_20260902_044555_a3f915`

ABI-179 was a family scout that broadened away from the recent signed-detail/full-scale ASPP branch into a UPerNet-style pyramid-pooling plus top-down feature-pyramid decoder. It kept provider-approved `abi_16ch_plus_sza` input, normalized GOES ABI channels 1-16, deterministic thermal BTD planes, normalized/cosine Solar Geometry Input features, a learned 1x1 spectral projection, trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, and disabled early stopping. Longitude, latitude, reconstructed coordinates, Dataset Source identity, labels, predictions, external data, and pretrained weights were not candidate inputs.

## Contract and resource observation

ABI-179 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, channel set `goes_abi_channels_1_16_plus_solar_geometry_input`, approved GOES ABI channel numbers 1-16 plus Solar Geometry Input, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Candidate code did not implement data loading, Leakage-Safe Split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, or Run lifecycle.

`outputs/model_summary.json` reported 7,656,162 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,694.0 seconds total wall time, 1,423.0 seconds training wall time, 1,269.0 seconds validation wall time, 17.27 training samples per second, 19.37 validation samples per second, 7,979,718,656 bytes peak CUDA allocated, and 9,921,626,112 bytes peak CUDA reserved. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The best-validation checkpoint was epoch 12, matching the final epoch.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260901_234732_bd5917` | ABI-173 | signed-detail full-scale skip ASPP decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3962 | 0.3838 | 0.4269 | 0.4238 | 0.3720 | 0.3203 | 0.00318 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260901_071026_32d3ec` | ABI-154 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |
| `run_20260902_054206_a6b406` | ABI-179 | UPerNet pyramid/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3939 | 0.3774 | 0.4354 | 0.4520 | 0.3490 | 0.2895 | 0.00280 |
| `run_20260902_044555_a3f915` | ABI-178 | thermal-only signed-detail full-scale skip ASPP decoder, BCE-Dice, thermal ABI+BTD | 11 | 0.3818 | 0.3713 | 0.4060 | 0.3906 | 0.3733 | 0.2851 | 0.00346 |

ABI-179 is finite, resource-safe, and non-degenerate. It landed in the capped reference band but did not beat the strongest capped aggregate references. Relative to ABI-173, ABI-179 reduced aggregate filtered Dice from 0.3962 to 0.3939 (-0.0023), MIT filtered Dice from 0.3838 to 0.3774 (-0.0064), recall from 0.3720 to 0.3490 (-0.0230), and connectivity from 0.3203 to 0.2895 (-0.0309). It improved Google filtered Dice from 0.4269 to 0.4354 (+0.0086), precision from 0.4238 to 0.4520 (+0.0282), and reduced filtered predicted-positive fraction from 0.00318 to 0.00280.

Relative to ABI-154, ABI-179 had higher recall (0.3490 versus 0.3359), higher Google filtered Dice (0.4354 versus 0.4260), and higher positive-area fraction, but lower aggregate filtered Dice (-0.0005), MIT filtered Dice (-0.0050), precision (-0.0257), and connectivity (-0.1480). Relative to ABI-130, ABI-179 traded lower aggregate filtered Dice (-0.0014), MIT filtered Dice (-0.0005), recall (-0.0088), and connectivity (-0.0956) for higher precision (+0.0105) and slightly lower positive fraction. Relative to ABI-068, it lost recall and connectivity while producing higher precision and Google Dice. ABI-179 therefore gives a clean precision/Google-forward but connectivity-weak UPerNet scout, not a new capped best Result.

## ABI-179 trajectory

Filtered Dice by epoch was 0.2083, 0.2552, 0.2824, 0.3170, 0.3337, 0.3166, 0.3577, 0.3649, 0.3566, 0.3440, 0.3839, and 0.3939. Training loss declined from 0.9691 at epoch 1 to 0.8539 at epoch 12; validation loss declined from 0.9541 to 0.8780. The selected epoch 12 checkpoint reached raw Dice 0.4090 and filtered Dice 0.3939, with raw recall 0.3732 versus filtered recall 0.3490 and raw predicted-positive fraction 0.00299 versus filtered predicted-positive fraction 0.00280. This raw-to-filtered gap is modest and does not indicate primary Artifact Filter dependence.

The trajectory shows real late improvement rather than plateau or collapse: filtered Dice rose by +0.0499 from epoch 10 to epoch 12, and the selected checkpoint was the final epoch. The late jump came mostly from stronger calibration and source behavior: epoch 11 had higher recall (0.3922) but lower precision (0.3761) and Google filtered Dice (0.3791), while epoch 12 shifted to higher precision (0.4520), lower recall (0.3490), and much stronger Google filtered Dice (0.4354). MIT peaked at epoch 11 (0.3860) and fell to 0.3774 at the selected epoch, so the UPerNet hierarchy may be calibrating Google-like positive evidence better than MIT-like thin/scene-balanced evidence at this budget.

The fixed first-four retained prediction samples include two empty/negative perfect cases and two near-zero per-sample Dice cases under the `first_n` retention policy. These artifacts are useful traceability samples but should not be treated as representative qualitative evidence for the full validation distribution.

## Interpretation

Classify ABI-179 as a successful bounded UPerNet-style family scout for feasibility, but not a promotion candidate. The hypothesis that pyramid pooling plus top-down feature pyramids could recover a cleaner context/detail hierarchy is partially supported: the run completed safely with the smallest parameter count among recent ASPP/detail references and reached within roughly 0.002-0.003 aggregate filtered Dice of ABI-068/130/173. It also produced the best Google filtered Dice among the ABI-173/154/178/179 local comparison set and improved precision relative to ABI-173.

The main negative signal is connectivity. ABI-179's filtered connectivity of 0.2895 is below ABI-173 (0.3203), ABI-130 (0.3851), ABI-068 (0.3900), and ABI-154 (0.4374). The UPerNet decoder therefore appears to calibrate positive area and Google source behavior without preserving the thin-line continuity that motivated the line-context refiner. The lower MIT Dice relative to ABI-173 and ABI-154 also argues against treating this exact implementation as a better capped Result.

Because ABI-179 was the first bounded UPerNet-style scout and finished improving at the epoch limit, low score alone is not elimination evidence. The family is eligible for at most a focused continuation under the proposal's criteria, but that continuation should directly address continuity/MIT retention rather than further broadening the pyramid decoder arbitrarily.

## Decision

Do not promote ABI-179 and do not request whole-validation diagnostics from this capped result alone. Do not repeat the exact ABI-179 implementation unchanged. Retain ABI-068 as the current capped aggregate/source-balance comparator, ABI-173 as the whole-validation-tested SZA-aware ASPP/detail aggregate branch, ABI-154 as the SZA-aware precision/connectivity branch, and ABI-130 as the prior SZA-aware aggregate reference.

A reasonable next hypothesis is one focused UPerNet-family continuation that preserves ABI-179's efficient pyramid/detail hierarchy while improving continuity and MIT retention, for example by strengthening non-suppressive line-context propagation or changing the trusted primary loss/auxiliary configuration within the existing allowlists. If that continuation remains connectivity-weak or loses the capped aggregate/source band, broaden away from UPerNet/SZA-aware context-detail decoders toward a different in-contract architecture, data-policy, preprocessing, calibration, or evaluation frontier. No Capability Request or Campaign Report is required from this result.

## Artifact references

- `run_20260902_054206_a6b406/outputs/best_metrics.json`
- `run_20260902_054206_a6b406/outputs/final_metrics.json`
- `run_20260902_054206_a6b406/outputs/metrics.jsonl`
- `run_20260902_054206_a6b406/outputs/resource_profile.json`
- `run_20260902_054206_a6b406/outputs/model_summary.json`
- `run_20260902_054206_a6b406/outputs/prediction_samples/samples.json`
- `run_20260902_054206_a6b406/outputs/validation_postprocessing/epoch_012.json`
- `run_20260902_054206_a6b406/resolved_manifest.yaml`
- `run_20260901_234732_bd5917/outputs/best_metrics.json`
- `run_20260901_234732_bd5917/outputs/evaluations/eval_evalreq_abi173_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260902_044555_a3f915/outputs/best_metrics.json`

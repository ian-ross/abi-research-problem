# Full-spectral BTD+SZA anti-aliased full-scale skip ASPP/detail decoder follow-up

research-figures: []

## Scope

This note records ABI-175 after Run `run_20260902_015941_3ebc45` completed.

Source Runs:

- ABI-175 anti-aliased full-scale skip ASPP/detail decoder BCE-Dice Centerline-auxiliary continuation: `run_20260902_015941_3ebc45`
- ABI-154 full-scale skip ASPP/detail decoder precision/connectivity reference: `run_20260901_071026_32d3ec`
- ABI-173 signed-detail full-scale skip ASPP decoder aggregate branch and whole-validation-tested SZA-aware ASPP/detail reference: `run_20260901_234732_bd5917`; Evaluation `eval_evalreq_abi173_wholeval_failure_buckets_v1`
- ABI-174 signed-detail line-consensus follow-up: `run_20260902_005632_5651ef`
- ABI-130 SZA-aware ASPP/detail decoder aggregate reference: `run_20260831_121006_7d24be`
- ABI-068 frequency-gated line U-Net broader capped aggregate/source-balance comparator: `run_20260828_010836_4ccc77`

ABI-175 was a family-development continuation of ABI-154. It kept provider-approved `abi_16ch_plus_sza` input, normalized GOES ABI channels 1-16, deterministic thermal BTD planes derived only from approved ABI channels, normalized/cosine Solar Geometry Input features, the BCE-Dice full-scale skip ASPP/detail decoder lineage, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, trusted `bce_dice` primary loss, and provider-derived Centerline Target auxiliary supervision at weight 0.02. The controlled architecture change was replacing encoder max-pool downsampling with fixed binomial anti-aliased feature downsampling to test whether thin-line evidence was being lost or aliased before the ASPP bottleneck.

## Contract and resource observation

ABI-175 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Candidate code did not implement data loading, Leakage-Safe Split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, or Run lifecycle.

`outputs/model_summary.json` reported 9,741,850 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,552.6 seconds total wall time, 1,266.1 seconds training wall time, 1,284.4 seconds validation wall time, 19.41 training samples per second, 19.13 validation samples per second, 8,057,914,880 bytes peak CUDA allocated, and 9,481,224,192 bytes peak CUDA reserved. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260901_234732_bd5917` | ABI-173 | signed-detail full-scale skip ASPP decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3962 | 0.3838 | 0.4269 | 0.4238 | 0.3720 | 0.3203 | 0.00318 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260901_071026_32d3ec` | ABI-154 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |
| `run_20260902_005632_5651ef` | ABI-174 | signed-detail line-consensus full-scale skip ASPP decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3929 | 0.3833 | 0.4178 | 0.4158 | 0.3724 | 0.3460 | 0.00325 |
| `run_20260902_015941_3ebc45` | ABI-175 | anti-aliased full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3817 | 0.3687 | 0.4175 | 0.5035 | 0.3073 | 0.4929 | 0.00221 |

ABI-175 is finite and non-degenerate, but it is scientifically negative for its stated recall/source-balance hypothesis. Relative to ABI-154, anti-aliased downsampling increased filtered precision from 0.4777 to 0.5035 (+0.0258) and filtered connectivity from 0.4374 to 0.4929 (+0.0554), while reducing filtered recall from 0.3359 to 0.3073 (-0.0286), aggregate filtered Dice from 0.3944 to 0.3817 (-0.0128), MIT filtered Dice from 0.3824 to 0.3687 (-0.0137), and Google filtered Dice from 0.4260 to 0.4175 (-0.0085). Filtered predicted-positive fraction also fell from 0.00255 to 0.00221, consistent with a more conservative positive-area regime rather than the intended recall recovery.

Relative to ABI-173 and ABI-174, ABI-175 recovered substantially stronger precision and connectivity, but only by giving up the signed-detail branches' recall. It is below ABI-173 by 0.0145 filtered Dice and 0.0647 recall, and below ABI-174 by 0.0113 filtered Dice and 0.0651 recall. Relative to ABI-130 and ABI-068, ABI-175 is also lower on aggregate filtered Dice, MIT filtered Dice, and recall, though it has the highest precision/connectivity among this comparison set.

## ABI-175 trajectory

ABI-175 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.2022, 0.2817, 0.3216, 0.3411, 0.3485, 0.3625, 0.3449, 0.3682, 0.3696, 0.3554, 0.3640, and 0.3817. The final epoch was both the selected checkpoint and the Run maximum.

The trajectory is not an optimization or numerical hard failure: training loss declined from 0.9954 to 0.8524, validation loss ended at 0.8886, and the final epoch reached the Run's highest filtered Dice. However, the metric path shows a precision/connectivity-biased solution rather than a recall-recovery solution. At the selected checkpoint, raw Dice was 0.3983, filtered Dice was 0.3817, filtered precision was 0.5035, filtered recall was 0.3073, filtered connectivity was 0.4929, and filtered predicted-positive fraction was 0.00221. Source-stratified filtered Dice was 0.3687 for MIT and 0.4175 for Google. MIT had filtered precision 0.4986, recall 0.2924, connectivity 0.4362, and predicted-positive fraction 0.00317; Google had filtered precision 0.5157, recall 0.3508, connectivity 0.5495, and predicted-positive fraction 0.00126.

Raw-to-filtered differences were modest: raw Dice was 0.3983 versus filtered Dice 0.3817, raw recall was 0.3293 versus filtered recall 0.3073, and raw predicted-positive fraction was 0.00237 versus filtered 0.00221. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples include one empty/negative perfect case and three near-zero per-sample Dice cases under the `first_n` retention policy; these artifacts are traceability samples and should not be treated as representative qualitative evidence for the full validation distribution.

## Interpretation

Classify ABI-175 as a completed, finite, non-collapsed capped family-development result, but not a successful anti-aliased downsampling continuation. The result suggests that fixed low-pass downsampling can make the ABI-154 lineage more conservative and connected, but it does not recover the default-threshold recall or MIT/source-balance signal that motivated the experiment. The lower predicted-positive fraction and higher precision/connectivity indicate that anti-aliasing likely suppresses some thin or marginal positives rather than preserving additional detectable contrail extent.

This is useful branch evidence: max-pool aliasing is not the limiting factor for ABI-154's recall at the current capped budget, or the fixed binomial smoothing is too suppressive for the narrow-line signal. Another downsampling-only variant in the same full-scale skip ASPP/detail branch is therefore a lower-priority use of the next capped run unless paired with a distinct recall-restoring mechanism. The stronger lesson is that ABI-154-like precision/connectivity and ABI-173-like recall remain separated by architecture tradeoffs; a next hypothesis should broaden beyond local signed-detail heads or downsampling changes.

## Decision

Do not promote ABI-175, do not repeat it unchanged, and do not request whole-validation diagnostics for ABI-175 from this capped result alone. Stop the anti-aliased downsampling-only branch under the predeclared hard-stop/negative-outcome criterion: it completed finitely but failed to improve ABI-154's recall, source balance, or aggregate filtered Dice.

Retain ABI-154 as the SZA-aware ASPP/detail precision/connectivity reference, ABI-173 as the whole-validation-tested SZA-aware ASPP/detail aggregate branch, ABI-130 as the prior SZA-aware ASPP/detail aggregate reference, and ABI-068 as the broader capped aggregate/source-balance comparator. A reasonable next hypothesis should broaden to a different architecture, preprocessing, data-policy, loss/calibration, or connectivity mechanism already allowed by the trusted contract. No Capability Request or Campaign Report is required from this result.

## Artifact references

- `run_20260902_015941_3ebc45/outputs/best_metrics.json`
- `run_20260902_015941_3ebc45/outputs/final_metrics.json`
- `run_20260902_015941_3ebc45/outputs/metrics.jsonl`
- `run_20260902_015941_3ebc45/outputs/resource_profile.json`
- `run_20260902_015941_3ebc45/outputs/model_summary.json`
- `run_20260902_015941_3ebc45/outputs/prediction_samples/samples.json`
- `run_20260902_015941_3ebc45/outputs/validation_postprocessing/epoch_012.json`
- `run_20260902_015941_3ebc45/resolved_manifest.yaml`
- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260901_234732_bd5917/outputs/best_metrics.json`
- `run_20260902_005632_5651ef/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`

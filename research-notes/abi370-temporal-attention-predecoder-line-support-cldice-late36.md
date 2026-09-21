# ABI-370 temporal-attention pre-decoder line-support clDice late36

research-figures: []

## Scope

This note records ABI-370, Candidate `abi370_temporal_attention_predecoder_line_support_cldice_late36_bce_dice_cldice_line_centerline_aux_v1`, Run `run_20260920_180416_4cefdd`.

ABI-370 was a controlled trusted-loss continuation of ABI-350. It kept the ABI-350 temporal-attention pre-decoder line-support U-Net architecture, provider-owned `abi_16ch_plus_sza_temporal` inputs with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`, source-balanced sampling, trusted random mirroring, Line and Centerline auxiliary targets, AdamW with constant learning rate, and batch size 2. The controlled change was selecting the allowlisted provider/Harness-owned `bce_dice_cldice` primary loss instead of `bce_dice`, testing whether topology-aware supervision improves connected thin-line continuity without Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, or data selection.

This is capped temporal-eligible evidence only. It is not whole Working Validation Split promotion evidence and should not be treated as a full-data Result against ABI-202 or ABI-249.

## Execution result

ABI-370 completed without contract, smoke, shape, numerical, resource, or lifecycle failure. The requested late-improving budget was approved from ABI-350 parent evidence.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, 36 epochs, 10,800 s timeout.
- Budget parent: `run_20260919_013306_9ca44e` (ABI-350).
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Trusted augmentation policy: `random_mirroring`.
- Trusted primary loss: `bce_dice_cldice`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,132,228, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 4,425,046,016 / 4,963,958,784 bytes.
- Training wall time: 4,768.2 s; validation wall time: 3,343.6 s; total Run wall time: 8,113.9 s, within the late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 27.

## Temporal-eligible aggregate metrics

| Metric | ABI-370 clDice | ABI-350 BCE-Dice parent | Delta vs ABI-350 | ABI-369 no mirroring | ABI-356 recall parent | ABI-223 temporal attention | ABI-368 recurrent C4 decoder |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 27 | 33 | -6 | 36 | 36 | 36 | 36 |
| Filtered Dice | 0.417655 | 0.431103 | -0.013448 | 0.429268 | 0.426056 | 0.419776 | 0.419767 |
| MIT filtered Dice | 0.400297 | 0.409536 | -0.009239 | 0.414658 | 0.411375 | 0.398498 | 0.402286 |
| Google filtered Dice | 0.463287 | 0.490518 | -0.027231 | 0.467429 | 0.465688 | 0.476764 | 0.464166 |
| Filtered precision | 0.434434 | 0.494306 | -0.059873 | 0.454607 | 0.421447 | 0.483764 | 0.421074 |
| Filtered recall | 0.402124 | 0.382230 | +0.019893 | 0.406604 | 0.430766 | 0.370738 | 0.418469 |
| Filtered connectivity | 0.417017 | 0.358283 | +0.058734 | 0.298437 | 0.282116 | 0.412427 | 0.240897 |
| Filtered predicted-positive pixels | 506,144 | 422,831 | +83,313 | 489,073 | 558,903 | 419,056 | 543,430 |

ABI-370 answers the trusted-loss question cleanly: clDice supervision did improve the intended connectivity metric, but it did not preserve ABI-350's source-balanced aggregate Dice or compactness. Relative to ABI-350, ABI-370 gains +0.0587 filtered connectivity and +0.0199 recall, but loses -0.0134 aggregate filtered Dice, -0.0272 Google Dice, -0.0092 MIT Dice, and -0.0599 precision while broadening the filtered footprint by 83,313 pixels.

The connectivity gain is notable: ABI-370 slightly exceeds ABI-223's temporal-attention connectivity on the same temporal-eligible capped population, and it is far above the recent ABI-356/368 recall-heavy temporal variants. However, the gain comes with a clear precision/source-balance cost. ABI-370 is below ABI-350, ABI-369, ABI-356, ABI-223, and ABI-368 on aggregate filtered Dice except for only being close to ABI-223/368, and it does not establish a new temporal frontier.

Raw versus filtered metrics show ordinary Artifact Filter behavior rather than filter-created performance. At the selected checkpoint, raw Dice was 0.434813 versus filtered Dice 0.417655, raw recall was 0.434334 versus filtered recall 0.402124, and raw predicted-positive pixels were 545,607 versus 506,144 filtered. Artifact Filters removed 39,463 predicted-positive pixels and lowered the score.

The retained fixed `first_n` prediction samples have nonzero per-sample Dice values of 0.4541, 0.2594, 0.4687, and 0.3956. They do not indicate all-negative or all-positive qualitative collapse, but they are only the first four validation samples and should not override aggregate temporal-eligible metrics.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Precision | Recall | Connectivity | Filtered positive pixels |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.196092 | 0.195638 | 0.197032 | 0.215549 | 0.179857 | 0.179586 | 456,268 |
| 6 | 0.335992 | 0.323812 | 0.365773 | 0.346740 | 0.325891 | 0.306671 | 513,933 |
| 12 | 0.384971 | 0.374915 | 0.409382 | 0.382098 | 0.387888 | 0.254602 | 555,099 |
| 15 | 0.379328 | 0.359753 | 0.427401 | 0.423901 | 0.343237 | 0.339426 | 442,759 |
| 22 | 0.412420 | 0.397376 | 0.452480 | 0.461251 | 0.372938 | 0.392069 | 442,117 |
| 27 | 0.417655 | 0.400297 | 0.463287 | 0.434434 | 0.402124 | 0.417017 | 506,144 |
| 29 | 0.363882 | 0.345012 | 0.407621 | 0.389423 | 0.341485 | 0.205348 | 479,499 |
| 31 | 0.380214 | 0.363525 | 0.424023 | 0.459385 | 0.324320 | 0.311407 | 386,042 |
| 33 | 0.409722 | 0.391353 | 0.456613 | 0.438502 | 0.384487 | 0.348448 | 479,455 |
| 34 | 0.384601 | 0.367240 | 0.427925 | 0.399787 | 0.370528 | 0.233616 | 506,793 |
| 35 | 0.356417 | 0.339356 | 0.399894 | 0.468861 | 0.287474 | 0.291862 | 335,268 |
| 36 | 0.411252 | 0.396223 | 0.450979 | 0.427416 | 0.396266 | 0.313222 | 506,960 |

The late budget was still useful, but the selected checkpoint arrived earlier than ABI-350's best epoch. ABI-370 reached its best aggregate score at epoch 27, with a high-connectivity/high-recall but broader footprint. Later epochs oscillated rather than improving: epoch 33 recovered much of the Dice, but connectivity remained lower; epoch 35 was compact but under-recalled; epoch 36 returned to a broad footprint without recovering the selected epoch's connectivity. This instability supports treating the loss swap as diagnostic rather than a new stable branch.

## Interpretation

Classify ABI-370 as finite, resource-safe, mechanistically informative, but mixed-negative as a continuation candidate. The trusted `bce_dice_cldice` loss did exactly part of what it was supposed to do: it raised connected-line continuity on the ABI-350 scaffold and produced a source-informative nondegenerate model. It did not combine that continuity with ABI-350's compact high-precision/source-balanced behavior. The result instead moves toward a broader recall/connectivity operating point and sacrifices enough precision and Google/source balance to lower aggregate Dice.

ABI-370 is therefore useful evidence for loss-policy effects but should not replace ABI-350 as the capped temporal-eligible line-support comparator. ABI-350 remains the stronger aggregate/precision temporal line-support reference, ABI-223 remains the mature temporal-attention diagnostic comparator, and ABI-370 mainly shows that topology-aware trusted loss can raise connectivity if future architecture mechanisms can prevent the accompanying footprint expansion and precision loss.

Do not submit another unchanged ABI-350 `bce_dice_cldice` late36 continuation, a loss-only repeat, or a minor auxiliary-weight-only variant. Future work should be mechanism-changing: preserve ABI-350's compact pre-decoder line-support anchor, add an architecture-level continuity/detail path that keeps clDice-like connected evidence spatially selective, or decouple a high-connectivity side path from broad mask logits without Candidate-owned thresholds or postprocessing. Candidate-owned data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, losses, metrics, Artifact Filters, thresholds, postprocessing, augmentation implementation, resource scheduling, downloads, and lifecycle changes remain out of scope.

A Post-Run Evaluation is not requested in this Autonomy Step. ABI-370 raises connectivity, but the capped temporal-eligible aggregate/source/precision regression is enough to avoid spending diagnostics before a more promising frontier or a candidate with clearer promotion ambiguity.

## Decision

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260920_180416_4cefdd/candidate/PROPOSAL.md`
- `run_20260920_180416_4cefdd/candidate/README.md`
- `run_20260920_180416_4cefdd/candidate/manifest.yaml`
- `run_20260920_180416_4cefdd/candidate/budget_request.yaml`
- `run_20260920_180416_4cefdd/resolved_manifest.yaml`
- `run_20260920_180416_4cefdd/execution.json`
- `run_20260920_180416_4cefdd/run_metadata.json`
- `run_20260920_180416_4cefdd/outputs/model_summary.json`
- `run_20260920_180416_4cefdd/outputs/best_metrics.json`
- `run_20260920_180416_4cefdd/outputs/final_metrics.json`
- `run_20260920_180416_4cefdd/outputs/metrics.jsonl`
- `run_20260920_180416_4cefdd/outputs/resource_profile.json`
- `run_20260920_180416_4cefdd/outputs/validation_postprocessing/index.json`
- `run_20260920_180416_4cefdd/outputs/prediction_samples/samples.json`
- `run_20260919_013306_9ca44e/outputs/best_metrics.json` and `/history/research-notes/abi350-temporal-attention-predecoder-line-support-late36.md` for ABI-350 parent context
- `run_20260920_155638_988238/outputs/best_metrics.json` and `/history/research-notes/abi369-temporal-attention-predecoder-line-support-no-mirroring-late36.md` for ABI-369 no-mirroring context
- `run_20260919_095725_843317/outputs/best_metrics.json` and `/history/research-notes/abi356-temporal-attention-multiscale-change-line-fusion-late36.md` for ABI-356 recall-context comparison
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` and `/reference/EXPERIMENT_INDEX.md` for ABI-223 temporal-attention comparator context
- `run_20260920_135212_ff1f2a/outputs/best_metrics.json` and `/history/research-notes/abi368-temporal-recurrent-c4-connectivity-decoder-late36.md` for ABI-368 recent recurrent-C4 comparator context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`

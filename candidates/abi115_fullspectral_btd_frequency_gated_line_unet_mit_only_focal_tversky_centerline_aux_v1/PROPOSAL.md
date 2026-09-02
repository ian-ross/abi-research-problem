# ABI-115 full-spectral BTD frequency-gated line U-Net MIT-only data-policy continuation

## Hypothesis

ABI-068 is the strongest local whole-validation-tested Candidate by aggregate filtered Dice, but its full Working Validation Split diagnostic still showed lower MIT filtered Dice and recall than the canonical MCAST 2.1 promotion context, while ABI-066 retained a stronger precision/connectivity-forward profile. Recent architecture-side continuations around ABI-068 mostly traded precision, recall, connectivity, source balance, and predicted-positive area without improving the capped aggregate reference.

ABI-115 tests a different, provider-owned data-policy axis: keep ABI-068's architecture, trusted focal-Tversky primary loss, Centerline Target auxiliary supervision, approved ABI-channel/BTD inputs, trusted random mirroring, and training budget, but change the manifest-selected sampling traversal from `combined_source_balanced` to trusted `mit_only`. This is a **family-development continuation**, not a full-data promotion claim. The scientific question is whether MIT-source emphasis improves the branch's weaker MIT operating point, source robustness, or connectivity enough to justify later balanced follow-up, without candidate-owned sampling implementation or any change to data loading, target derivation, losses, metrics, thresholding, Artifact Filters, augmentation implementation, resource placement, or lifecycle behavior.

## Comparison Target

Primary target: ABI-068, `abi068_fullspectral_btd_frequency_gated_line_unet_focal_tversky_centerline_aux_v1`, Run `run_20260828_010836_4ccc77`, because it is the same architecture/loss/auxiliary policy under combined source-balanced traversal and is the current local aggregate-Dice and whole-validation-tested reference.

Secondary targets: ABI-106, Run `run_20260830_101145_b69d10`, because it is the analogous Google-only data-policy continuation; ABI-066, Run `run_20260827_230540_bf4ce3`, because it remains the precision/connectivity reference; and canonical MCAST 2.1 as promotion context only. This Run is capped representative family-development evidence.

## Expected Effect

MIT-only traversal is expected to:

- increase the fraction of optimizer steps drawn from MIT ABI Patches using a provider-owned allowlisted sampling policy;
- test whether ABI-068's MIT filtered Dice and MIT recall can improve without an architecture-side suppressor or new target/loss;
- reveal whether the frequency-gated BTD features learned from MIT alone transfer acceptably to Google validation or whether ABI-068's balance depends on mixed-source training;
- potentially recover some connectivity if MIT scenes provide more continuous thin-line supervision under focal-Tversky;
- preserve the established ABI-068 resource profile because the model architecture and batch size are unchanged.

## Implementation Sketch

Reuse the ABI-068 model unchanged: provider-approved `abi_16ch` input only; normalized GOES ABI channels 1-16; deterministic thermal BTD planes derived only from those channels; learned 1x1 spectral mixer; frequency-split stem; residual encoder/decoder; frequency-pyramid fusion; oriented high-frequency line refiner; primary `mask_logits`; and provider-derived `centerline_logits` auxiliary output.

The controlled manifest change is `data.sampling_policy: mit_only`. The Candidate does not implement data loading, split logic, capped-record selection, sampling, augmentation, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, filesystem writes, network calls, pretrained weights, training loops, resource placement, or Run lifecycle handling. The model does not receive longitude, latitude, or reconstructed coordinate inputs.

## Contract Features Used

- Input mode: `abi_16ch` only; no longitude/latitude or coordinate-derived inputs.
- Output form: primary `mask_logits` with shape `[1, 256, 256]`.
- Auxiliary target: provider-derived `centerline` emitted as `centerline_logits` with trusted `weighted_bce` weight 0.02.
- Primary loss: trusted `focal_tversky`.
- Data policy: provider-owned `mit_only` sampling traversal and trusted `random_mirroring` augmentation.
- Optimizer/training policy: `adamw`, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, and disabled early stopping under the current Workspace Configuration.

## Budget Requested

Run sequentially under the current Workspace Configuration: at most 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, 3,600-second Docker training timeout, fixed first-four prediction artifacts, constant learning rate, disabled early stopping, and the 25M-parameter smoke ceiling. No Experiment Batch, concurrency increase, GPU selection, custom evaluation, or full-data promotion evaluation is requested.

## Success Criteria

Useful continuation evidence would be any of:

- capped MIT `val/source/mit/filtered_dice` above ABI-068 while aggregate `val/filtered_dice` remains within about 0.015 of ABI-068;
- capped aggregate filtered Dice at or above ABI-066 while improving MIT filtered Dice or MIT recall over ABI-068;
- both Dataset Sources remain non-catastrophic, with Google filtered Dice above about 0.38 and MIT filtered Dice above about 0.39;
- improved filtered connectivity or lower negative-patch clutter proxy, reflected by higher filtered connectivity or lower filtered predicted-positive fraction than ABI-068 without a large recall collapse;
- a finite, late-improving, non-collapsed trajectory that clarifies whether source-specific traversal is a viable follow-up axis.

Hard-stop evidence for this exact branch would be smoke failure, contract rejection, non-finite behavior, persistent all-negative or all-positive collapse, aggregate filtered Dice below about 0.35, Google filtered Dice below about 0.34, or a recall-only positive-area expansion with worse precision/connectivity than ABI-068 and no MIT improvement.

## Fallback Next Decision

If ABI-115 improves MIT behavior while preserving acceptable Google and aggregate metrics, consider either a bounded whole-validation failure-bucket Evaluation Request or a later provider-owned mixed-policy follow-up if an allowlisted policy can express it. If it simply overfits MIT and damages Google/source balance, stop the MIT-only branch and retain ABI-068 as the balanced reference. If it fails validation or smoke testing, classify and repair only if the original provider-owned data-policy hypothesis is preserved.

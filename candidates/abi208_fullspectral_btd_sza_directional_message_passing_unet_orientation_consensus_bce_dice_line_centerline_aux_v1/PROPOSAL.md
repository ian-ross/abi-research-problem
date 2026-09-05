# ABI-208 Full-spectral BTD+SZA directional message-passing U-Net orientation-consensus continuation

## Hypothesis

ABI-207 showed that a compact directional-message-passing U-Net can learn a finite, non-collapsed, source-informative operating point and finished the exploratory budget at its best epoch, but it did not deliver the intended Contrail Connectivity Metric advantage and ran close to the exploratory timeout. ABI-208 is a family-development continuation: replacing ABI-207s broad residual directional mixing with a lighter orientation-consensus message block should preserve the scouts recall while improving thin-line connectivity/precision and reducing resource risk.

## Comparison Target

Primary comparison is ABI-207 (`run_20260904_120216_3ffbda`) because ABI-208 keeps the same architecture family, input mode, trusted data policy, loss, auxiliary targets, optimizer, and exploratory budget while changing the message-passing block. Secondary references are ABI-201/202 cross-scale directional-consensus ASPP (`run_20260904_032624_7e855a`, `run_20260904_043143_ee0005`) and ABI-184 (`run_20260902_213856_2c04ac`) for aggregate, recall, and precision/connectivity context.

## Expected Effect

The soft orientation-consensus block scores horizontal, vertical, diagonal, and local-context messages and applies only a bounded residual update. This should discourage the broad thickening suggested by ABI-207s low connectivity, improve precision/connectivity at similar recall, and lower runtime/parameter risk by reducing base width from 32 to 28 and simplifying the directional fusion path.

## Implementation Sketch

Start from ABI-207s contract-compliant `abi_16ch_plus_sza` normalized ABI/BTD/SZA front end, signed-detail stem, U-Net encoder/decoder, full-scale skip fusion, and Line plus Centerline auxiliary heads. Replace the internal `DirectionalMessageBlock` with an orientation-consensus block: depthwise horizontal/vertical filters, no-wrap diagonal context, a local detail context branch, softmax orientation scoring, a learned consensus gate, and a bounded residual projection. Keep all features derived from approved channels. Do not add thresholding, postprocessing, Candidate-owned filtering, custom losses, target derivation, data loading, or coordinates.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation`
- Input mode: provider-approved `abi_16ch_plus_sza`; longitude and latitude are not inputs
- Output form: `mask_logits`
- Auxiliary targets: trusted provider-derived `line` -> `line_logits` weight 0.01 and `centerline` -> `centerline_logits` weight 0.02
- Loss: trusted `bce_dice` primary loss plus trusted `weighted_bce` auxiliary losses
- Data policy: `combined_source_balanced`, `all_target_frames`, trusted `random_mirroring`
- Optimizer/scheduler: AdamW, learning rate 0.0003, `constant_lr`
- Candidate code is architecture only and does not own Harness/provider data, losses, metrics, Artifact Filters, sampling, augmentation, thresholding, execution, or lifecycle behavior

## Budget Requested

Use the default exploratory budget: batch size 4, `max_epochs: 12`, constant learning rate, disabled early stopping as enforced by the Workspace Configuration. No late-improving budget is requested because ABI-207 is a single scout whose connectivity weakness should be addressed architecturally before any longer-budget continuation.

## Success Criteria

Treat ABI-208 as successful family-development evidence if it is finite, non-collapsed, source-informative on MIT and Google, stays within the 25M-parameter and exploratory timeout ceilings, and improves ABI-207 on filtered Dice or improves filtered precision/connectivity without a severe recall collapse. Finishing near the 12-epoch ceiling with an improving trajectory would justify considering one late-improving close-continuation; a strong capped result near ABI-201/202 may justify whole-validation diagnostics.

## Fallback/Next Decision

If ABI-208 fails smoke, numerical, contract, or resource validation, classify the failure before repair. If it completes but regresses ABI-207 on aggregate filtered Dice, connectivity, and source balance, do not abandon the family solely on low score, but broaden from ABI-207/208 to a cheaper full-scale detail bridge or return to the stronger ABI-202 cross-scale directional-consensus ASPP frontier. If ABI-208 improves connectivity/precision with acceptable recall and resource use, continue the directional-message-passing family with either a late36 close-continuation or a small controlled head/data-policy follow-up.

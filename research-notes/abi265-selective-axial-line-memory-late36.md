# ABI-265 selective axial line-memory U-Net late36

research-figures: []

## Scope

This note records the late-improving continuation Result for ABI-265, Candidate `abi265_fullspectral_btd_sza_selective_axial_line_memory_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260912_065321_ceab64`.

ABI-265 was a close continuation of ABI-264. It kept the selective axial line-memory U-Net architecture unchanged and requested the approved `late_improving` budget because ABI-264's exploratory run selected its final epoch with a sharp improvement in aggregate filtered Dice, MIT/Google filtered Dice, and connectivity. The Candidate consumed only provider-owned `abi_16ch_plus_sza` inputs, used trusted source-balanced sampling, random mirroring, BCE-Dice primary loss, constant learning rate, batch size 4, and trusted Line plus Centerline auxiliary outputs.

Candidate code remained architecture-only and did not implement data loading, split logic, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, temporal lookup, downloads, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Execution result

ABI-265 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from Harness-owned artifacts:

- Status: completed.
- Effective budget: `late_improving`, approved from parent `run_20260912_055445_9221de`.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `all_target_frames`.
- Sample counts after capped-record selection: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 5,017,094, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 17.42 / 18.93 GB.
- Training wall time: 4,884.9 s; validation wall time: 4,311.2 s; total Run wall time: 9,198.3 s, within the 10,800 s late-improving timeout.

This is valid finite capped-validation evidence for the selective axial line-memory family. It is not whole-validation promotion evidence.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 34. The final epoch 36 was lower, so the late budget found a useful selected checkpoint but did not produce a monotone finish.

| Metric | ABI-265 best epoch 34 | ABI-265 final epoch 36 | ABI-264 parent epoch 12 | ABI-253 line-memory U-NetFormer | ABI-249 C4 line-context | ABI-202 frontier |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.411977 | 0.399368 | 0.407091 | 0.408323 | 0.416400 | 0.427570 |
| Raw Dice | 0.427098 | 0.414741 | 0.421174 | 0.423530 | 0.432320 | 0.442746 |
| Filtered precision | 0.433940 | 0.441552 | 0.399434 | 0.444837 | 0.480886 | 0.439467 |
| Filtered recall | 0.392130 | 0.364541 | 0.415047 | 0.377349 | 0.367165 | 0.416301 |
| Filtered connectivity | 0.433071 | 0.332198 | 0.410422 | 0.326698 | 0.392524 | 0.457773 |
| MIT filtered Dice | 0.401437 | 0.389986 | 0.398792 | 0.394406 | 0.396436 | 0.411992 |
| Google filtered Dice | 0.438974 | 0.422272 | 0.428117 | 0.442587 | 0.468855 | 0.468151 |
| Filtered predicted-positive fraction | 0.003275 | 0.002992 | 0.003765 | 0.003074 | 0.002767 | 0.003433 |

ABI-265 improved the ABI-264 parent best filtered Dice by about +0.0049, precision by +0.0345, connectivity by +0.0226, MIT Dice by +0.0026, and Google Dice by +0.0109. This confirms that ABI-264 was partly budget-truncated and that the selective axial memory mechanism can benefit from longer training.

The improvement is not enough to reset the campaign frontier. ABI-265 remains below ABI-249 on capped aggregate Dice, precision, and Google Dice, and below ABI-202 on aggregate Dice, MIT Dice, recall, and connectivity. Its best checkpoint does exceed ABI-253's capped aggregate Dice and connectivity, but ABI-253 already failed to displace ABI-249/ABI-202 on whole-validation diagnostics; ABI-265 therefore needs stronger justification before spending a whole-validation diagnostic request.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.218704 | 0.225351 | 0.206059 | 0.209157 | 0.229165 | 0.137926 | 0.003970 |
| 2 | 0.260988 | 0.272529 | 0.240057 | 0.214795 | 0.332491 | 0.120953 | 0.005609 |
| 3 | 0.277220 | 0.272968 | 0.285634 | 0.273888 | 0.280635 | 0.173386 | 0.003713 |
| 4 | 0.311274 | 0.317694 | 0.298579 | 0.280269 | 0.349992 | 0.160631 | 0.004525 |
| 5 | 0.298595 | 0.274660 | 0.356149 | 0.460833 | 0.220846 | 0.363235 | 0.001737 |
| 6 | 0.337955 | 0.345911 | 0.321924 | 0.317613 | 0.361081 | 0.220178 | 0.004120 |
| 7 | 0.367313 | 0.358851 | 0.387681 | 0.398618 | 0.340567 | 0.319860 | 0.003096 |
| 8 | 0.347159 | 0.337442 | 0.369077 | 0.410761 | 0.300611 | 0.323653 | 0.002652 |
| 9 | 0.360220 | 0.341077 | 0.406273 | 0.430710 | 0.309557 | 0.374466 | 0.002604 |
| 10 | 0.329781 | 0.332475 | 0.324607 | 0.315697 | 0.345181 | 0.256642 | 0.003962 |
| 11 | 0.362775 | 0.366060 | 0.355668 | 0.339829 | 0.389044 | 0.203740 | 0.004148 |
| 12 | 0.360900 | 0.346806 | 0.393286 | 0.401114 | 0.328015 | 0.288858 | 0.002963 |
| 13 | 0.361405 | 0.337388 | 0.419710 | 0.462831 | 0.296442 | 0.424955 | 0.002321 |
| 14 | 0.373003 | 0.359681 | 0.404963 | 0.430366 | 0.329133 | 0.338263 | 0.002771 |
| 15 | 0.399128 | 0.388451 | 0.425438 | 0.404740 | 0.393670 | 0.387914 | 0.003525 |
| 16 | 0.385338 | 0.377154 | 0.404114 | 0.376435 | 0.394673 | 0.246269 | 0.003799 |
| 17 | 0.352820 | 0.333294 | 0.398491 | 0.435115 | 0.296703 | 0.318377 | 0.002471 |
| 18 | 0.389838 | 0.373795 | 0.429841 | 0.472451 | 0.331817 | 0.411607 | 0.002545 |
| 19 | 0.376348 | 0.353200 | 0.435564 | 0.508525 | 0.298708 | 0.489600 | 0.002129 |
| 20 | 0.391635 | 0.380989 | 0.416860 | 0.405623 | 0.378580 | 0.291791 | 0.003382 |
| 21 | 0.392750 | 0.378111 | 0.430720 | 0.436148 | 0.357207 | 0.410749 | 0.002968 |
| 22 | 0.402189 | 0.393845 | 0.423386 | 0.411013 | 0.393736 | 0.355088 | 0.003471 |
| 23 | 0.380665 | 0.361244 | 0.429783 | 0.495943 | 0.308871 | 0.471329 | 0.002257 |
| 24 | 0.386711 | 0.376405 | 0.410754 | 0.392354 | 0.381228 | 0.294959 | 0.003521 |
| 25 | 0.323954 | 0.300914 | 0.382041 | 0.508514 | 0.237687 | 0.409781 | 0.001694 |
| 26 | 0.402448 | 0.388266 | 0.436326 | 0.425573 | 0.381707 | 0.323579 | 0.003250 |
| 27 | 0.387778 | 0.365106 | 0.445235 | 0.502426 | 0.315732 | 0.453277 | 0.002277 |
| 28 | 0.394875 | 0.387270 | 0.411906 | 0.361247 | 0.435406 | 0.286326 | 0.004368 |
| 29 | 0.407948 | 0.399100 | 0.429508 | 0.406039 | 0.409876 | 0.307770 | 0.003658 |
| 30 | 0.378085 | 0.360316 | 0.422516 | 0.493352 | 0.306480 | 0.414916 | 0.002251 |
| 31 | 0.399678 | 0.379320 | 0.449079 | 0.467309 | 0.349147 | 0.446961 | 0.002707 |
| 32 | 0.392728 | 0.386357 | 0.406961 | 0.363134 | 0.427572 | 0.261797 | 0.004267 |
| 33 | 0.403641 | 0.393858 | 0.426885 | 0.388776 | 0.419687 | 0.317416 | 0.003912 |
| 34 | 0.411977 | 0.401437 | 0.438974 | 0.433940 | 0.392130 | 0.433071 | 0.003275 |
| 35 | 0.386854 | 0.371628 | 0.423520 | 0.432012 | 0.350243 | 0.300127 | 0.002938 |
| 36 | 0.399368 | 0.389986 | 0.422272 | 0.441552 | 0.364541 | 0.332198 | 0.002992 |

The trajectory is finite, non-collapsed, and source-informative. It is also volatile: high-connectivity/high-precision spikes occur at epochs 19, 23, 27, and 31, while higher-recall states occur at epochs 28, 32, and 33. The selected epoch 34 is the best aggregate compromise, but it is followed by a two-epoch decline. That pattern supports the usefulness of the approved late budget, but it does not support another unchanged epoch extension.

## Interpretation

Classify ABI-265 as a modest positive late-budget continuation, not a promotion candidate. The late36 run validates that the selective axial line-memory family has real capped-validation capacity beyond ABI-264's 12-epoch endpoint. The main architectural value remains connectivity: ABI-265's best selected checkpoint combines a compact predicted-positive fraction with connectivity above ABI-249 and ABI-253 capped comparators.

The remaining weakness is the tradeoff between recall, precision, and source balance. ABI-265 improved parent precision but lost parent recall; its Google source performance improved over ABI-264 but remains below ABI-249/ABI-202, while its MIT Dice is still below ABI-202. The family appears to be learning useful row/column continuity evidence, but the current unchanged architecture does not raise that evidence into a stable frontier fixed-threshold operating point.

Resource cost is also a constraint. The 5.0M-parameter model is small, but the high-resolution axial state has a large activation footprint: about 17.4 GB peak allocated memory and 9,198 s late36 wall time. Future variants should be mechanism-changing and resource-aware rather than simply adding more high-resolution memory blocks or repeating the same late-budget run.

## Decision

Do not promote ABI-265, do not request another unchanged late-improving continuation, and do not treat the capped score as whole-validation evidence. A whole-validation diagnostic is not the next best handoff from this single Result because ABI-265 remains below the current whole-validation-tested ABI-202/ABI-249 frontier and only modestly above ABI-264/ABI-253 on capped metrics.

Retain selective axial line-memory as a useful mechanism but stop the exact unchanged branch. A reasonable future hypothesis would be mechanism-changing: preserve the axial memory core while adding a lightweight evidence-raising/calibration head, coupling it to rotation-aware/C4 line context, or reducing high-resolution state cost before adding any new capacity. If the next step broadens instead, prioritize another underexplored family or a precision-preserving recall-calibration design rather than more unchanged late-budget runs.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260912_065321_ceab64/candidate/PROPOSAL.md`
- `run_20260912_065321_ceab64/candidate/README.md`
- `run_20260912_065321_ceab64/candidate/manifest.yaml`
- `run_20260912_065321_ceab64/candidate/budget_request.yaml`
- `run_20260912_065321_ceab64/resolved_manifest.yaml`
- `run_20260912_065321_ceab64/outputs/model_summary.json`
- `run_20260912_065321_ceab64/outputs/best_metrics.json`
- `run_20260912_065321_ceab64/outputs/final_metrics.json`
- `run_20260912_065321_ceab64/outputs/metrics.jsonl`
- `run_20260912_065321_ceab64/outputs/resource_profile.json`
- `run_20260912_065321_ceab64/outputs/validation_postprocessing/index.json`
- `run_20260912_065321_ceab64/outputs/prediction_samples/samples.json`
- `run_20260912_055445_9221de` for ABI-264 parent context
- `run_20260911_171333_f0b603` for ABI-253 line-memory U-NetFormer comparator context
- `run_20260911_111909_dd7ef7` for ABI-249 C4 steerable line-context comparator context
- `run_20260904_043143_ee0005` for ABI-202 current aggregate whole-validation frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`

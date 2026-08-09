# ABI-022 accelerated evaluation report

## Outcome

The trusted ABI evaluator now applies the Geographic Feature Filter, Scanline
Artifact Filter, ordinary segmentation metrics, Contrail Connectivity Metric,
and the 19-threshold diagnostic sweep through bounded torch CPU/CUDA batches.
Only eight ABI Patches are transferred to the configured device at once in the
production run; the full validation split remains on CPU.

Geographic-enabled MCAST artifacts are immutable at:

`/data/iross/abi-ml-autoresearch/baselines/geographic-enabled-20260807-abi022-r2`

The shared timestamped log is
`/data/iross/abi-ml-autoresearch/baselines/geographic-enabled-20260807-abi022-r2/baseline_evaluation.log`.
Both baseline directories contain aggregate, per-sample, threshold-sweep,
diagnostic, metadata, and run-manifest artifacts for 3,088 ABI Patches.

## Performance

| Phase | MCAST 1.1 | MCAST 2.1 |
|---|---:|---:|
| Inference | 98.904s | 119.483s |
| Geographic context preparation | 87.207s | 98.264s |
| Artifact Filter | 1.479s | 1.389s |
| Ordinary metrics | 0.734s | 0.885s |
| Contrail Connectivity Metric | 4.876s | 4.823s |
| Threshold sweep | 4.544s | 4.546s |
| Total postprocessing | 98.840s | 109.908s |

The initial baseline evaluations took about 57–58 minutes each, including
1,653–1,670 seconds for per-sample filtering/metrics and 1,177–1,201 seconds for
the threshold sweep. The accelerated geographic-enabled evaluations completed
end-to-end in about 3 minutes 35 seconds for MCAST 1.1 and 3 minutes 57 seconds
for MCAST 2.1, despite adding active geographic rasterization.

The first accelerated attempt exposed a separate preparation bottleneck:
every ABI Patch reparsed and rescanned 18.8 MB of Natural Earth GeoJSON,
limiting preparation to roughly one Patch/second. Parsed lines and their
bounding boxes are now cached once per process with file size/mtime cache
invalidation. The completed runs prepared 31–35 Patches/second.

## Parity and filter evidence

Accelerated raw outputs were compared with
`/data/iross/abi-ml-autoresearch/baselines/initial-20260807` for both baselines.
Parity was exact:

- aggregate raw metrics: maximum absolute delta 0.0;
- all 3,088 per-sample raw confusion counts and ordinary metrics: exact;
- all per-sample raw connectivity values: maximum absolute delta 0.0;
- raw threshold counts and metrics at all 19 thresholds: exact.

Active geographic filtering produced bounded filter-hit diagnostics:

| Evidence | MCAST 1.1 | MCAST 2.1 |
|---|---:|---:|
| Geographic pixels removed | 35,586 | 58,315 |
| ABI Patches with filter hits | 545 | 1,033 |
| Thresholds with filter hits | 19/19 | 19/19 |
| Scanline pixels removed | 0 | 0 |

Each run manifest records `torch_cuda`, device `cuda`, maximum device batch 8,
threshold tile size 4, no full-validation GPU residency, 386 target-skeleton
batches, phase timings, active Natural Earth provenance, and artifact paths.
Targets were skeletonized once per sample batch and reused for raw and Filtered
Contrail Mask connectivity scores.

## Validation

```bash
uv run --group torch pytest -q
uv build --wheel
git diff --check
```

Result: 88 tests passed, wheel build passed, and no whitespace errors were
reported. CUDA tests compare CPU/CUDA raw and filtered masks, diagnostics,
ordinary metrics, connectivity, and filter-hit threshold counts. Tiny fixtures
cover pre-rasterized geography, empty/NaN masks, contiguous scanline runs, and
population-standard-deviation values below, at, and above the filter boundary.
The existing candidate boundary tests continue to prove that longitude and
latitude are provider-only context and are not Candidate Experiment inputs.

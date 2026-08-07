# ABI-023 geographic-enabled MCAST baseline handoff

## Status and purpose

The existing MCAST 1.1/2.1 artifacts at
`/data/iross/abi-ml-autoresearch/baselines/initial-20260807` are scanline-only.
All 6,176 per-sample records reported geographic availability as false. Preserve
those artifacts unchanged as ABI-022 parity targets.

Generate replacement artifacts only after the ABI-022 accelerated evaluator is
available, unless an operator explicitly accepts the current CPU postprocessing
cost. The replacement run must require and record the verified Natural Earth
bundle.

## Prerequisites

```bash
uv sync --group baselines
DATASET_ROOT=/home/mcast/data/ml-training-data/contrail-detection
uv run abi-provision-natural-earth --dataset-root "$DATASET_ROOT" --verify-only
uv run abi-geographic-filter-smoke --workspace-root . --max-samples 64
```

Confirm `ml-autoresearch.toml` contains dataset-root-relative ancillary config:

```toml
geographic_filter_required = true
geographic_ancillary_manifest = "ancillary/natural-earth/manifest.json"
```

## Replacement evaluation

Choose a new immutable output-root name; never reuse `initial-20260807`.

```bash
CPU_COUNT=$(nproc)
CPU_LIMIT=$((CPU_COUNT * 3 / 4))
CPUSET="0-$((CPU_LIMIT - 1))"
OUTPUT_ROOT=/data/iross/abi-ml-autoresearch/baselines/geographic-enabled-YYYYMMDD

for BASELINE in mcast_detection_1_1 mcast_detection_2_1; do
  taskset -c "$CPUSET" env \
    OMP_NUM_THREADS="$CPU_LIMIT" \
    MKL_NUM_THREADS="$CPU_LIMIT" \
    OPENBLAS_NUM_THREADS="$CPU_LIMIT" \
    NUMEXPR_NUM_THREADS="$CPU_LIMIT" \
    CUDA_VISIBLE_DEVICES=0 \
    uv run --group baselines abi-baseline-evaluate \
      --workspace-root . \
      --baseline "$BASELINE" \
      --device cuda \
      --log-every 100 \
      --output-root "$OUTPUT_ROOT"
done
```

## Acceptance checks

For each baseline:

1. `run_manifest.json` reports
   `artifact_filters.geographic_feature_filter.active: true`.
2. Both Natural Earth source identities, versions, sizes, and SHA-256 hashes are
   present in the run manifest and per-sample Geographic Feature Filter
   diagnostics.
3. The run has 3,088 samples with the expected MIT/Google split.
4. At least one bounded diagnostic proves a geographic filter hit, or the
   operator records an evidence-backed explanation if model predictions do not
   overlap any rasterized feature.
5. The output root, aggregate metrics, timings, workspace commit, and Harness
   commit are appended to ABI-022 implementation notes as geographic-enabled
   parity targets.

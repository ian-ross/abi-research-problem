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
ANCILLARY_ROOT=/data/iross/abi-ml-autoresearch/ancillary
uv run abi-provision-natural-earth --ancillary-root "$ANCILLARY_ROOT" --verify-only
uv run abi-geographic-filter-smoke --workspace-root . --max-samples 64
```

Confirm `ml-autoresearch.toml` declares distinct host roots. The Harness passes
the host mapping to native evaluation and mounts it read-only at
`/data/training` plus `/data/ancillary` in Docker:

```toml
[research_problem.data_roots]
training = "/home/mcast/data/ml-training-data/contrail-detection"
ancillary = "/data/iross/abi-ml-autoresearch/ancillary"

[research_problem.data_config]
geographic_filter_required = true
geographic_ancillary_manifest = "natural-earth/manifest.json"
coastline_geojson = "natural-earth/natural_earth_10m_coastline.geojson"
rivers_geojson = "natural-earth/natural_earth_10m_rivers_north_america.geojson"
```

No files are written beneath the training root. Do not recreate the retired
`abi-023-smoke-data` symlink wrapper.

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

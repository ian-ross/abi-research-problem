# ABI Research Problem

GOES ABI Contrail Segmentation Research Problem provider and Research Workspace
Root for [`ml-autoresearch`](../ml-autoresearch).

Provider target: `abi_contrail.research_problem:build_spec`
Research Problem id: `goes_abi_contrail_segmentation`

## Local configuration

`ml-autoresearch.toml` is machine-local because it contains host data paths,
runtime-image identities, and optionally notification credentials. It is ignored
by Git. Start from the committed template on a new host:

```bash
cp ml-autoresearch.toml.example ml-autoresearch.toml
```

Update the Harness checkout, runs root, ABI dataset, and MCAST asset paths. The
operational data configuration uses separate logical roots for the primary
training data and trusted ancillary bundle. Dataset Source paths are relative to
`training`; geographic paths are relative to `ancillary`:

```toml
[research_problem.data_roots]
training = "/path/to/contrail-detection"
ancillary = "/path/to/abi-ml-autoresearch/ancillary"

[research_problem.data_config]
mcast_detection_1_1_path = "/path/to/models/detection-1.1.pt"
mcast_detection_2_1_path = "/path/to/models/detection-2.1"
geographic_filter_required = true
geographic_ancillary_manifest = "natural-earth/manifest.json"
coastline_geojson = "natural-earth/natural_earth_10m_coastline.geojson"
rivers_geojson = "natural-earth/natural_earth_10m_rivers_north_america.geojson"

[[research_problem.data_config.sources]]
layout = "mit"
inputs_zarr = "mit/inputs.zarr"
labels_zarr = "mit/labels.zarr"
metadata_parquet = "mit/metadata.parquet"

[[research_problem.data_config.sources]]
layout = "google"
inputs_zarr = "google/inputs.zarr"
labels_zarr = "google/labels.zarr"
metadata_parquet = "google/metadata.parquet"
```

The Harness validates these host directories and mounts them read-only at
`/data/training` and `/data/ancillary` for Docker operations; it supplies the
resolved `data_roots` mapping to the trusted provider. Native operations receive
the resolved host paths. Legacy direct callers that provide only `dataset_root`
or `data_root` remain supported, with ancillary paths resolved beneath that
single root.

The provider opens the operational named arrays inside both zarr groups. Google
keeps its source train/validation provenance; MIT is split by whole scene before
256x256 windowing. Longitude and latitude remain trusted provider context and
are never candidate inputs.

## Natural Earth ancillary data

Geographic filtering uses pinned Natural Earth vector v5.1.2 GeoJSON for the
1:10m coastline and North America rivers. Source versions, immutable URLs,
public-domain license references, byte sizes, and SHA-256 hashes are committed
in `abi_contrail/data/natural-earth-v5.1.2.json`. Evaluation is offline and
never downloads ancillary data.

Provision once during explicit operator setup directly beneath the standalone
ancillary root, then verify idempotently without network access:

```bash
ANCILLARY_ROOT=/path/to/abi-ml-autoresearch/ancillary
uv run abi-provision-natural-earth --ancillary-root "$ANCILLARY_ROOT"
uv run abi-provision-natural-earth --ancillary-root "$ANCILLARY_ROOT" --verify-only
```

The installed manifest is `$ANCILLARY_ROOT/natural-earth/manifest.json`. The
same root-relative value resolves beneath the host ancillary directory and at
`/data/ancillary/natural-earth/manifest.json` in Docker. The training directory
can remain read-only and does not need an ancillary symlink or wrapper union.
The legacy `--dataset-root` provisioning alias remains available for old
single-root installations. Missing, truncated, or checksum-mismatched required
files stop evaluation with a clear trusted-data error.

After dataset and runtime setup, run the bounded provider-only smoke check. It
uses at most the configured number of validation ABI Patches, creates an
all-positive trusted prediction, and verifies that rasterized geography removes
pixels. It does not train or invoke candidate code.

```bash
uv run abi-geographic-filter-smoke --workspace-root . --max-samples 64
```

## Runtime images

The Docker runner and Gondolin/pi-fort Agent Runtime Image are distinct. Do not
copy a Docker tag from another workspace or choose one manually. Build both and
let the Harness update the local configuration:

```bash
uv sync
uv run ml-autoresearch build-runtime-images --workspace-root . --update-config
uv run ml-autoresearch validate-runtime-images --workspace-root .
```

The ABI workspace declares only its trusted runner data dependencies under
`runtime_images.runner_requirements`. Rebuild and revalidate after changing the
Harness checkout, those requirements, image recipes, or image-related workspace
configuration.

On a GPU node, validate the generated runner image explicitly (the current
`validate-docker-gpu` CLI accepts `--docker-image`, not `--workspace-root`):

```bash
RUNNER_IMAGE=$(uv run python - <<'PY'
from ml_autoresearch.candidate_execution_config import load_candidate_execution_config
print(load_candidate_execution_config('.').docker_image)
PY
)
uv run ml-autoresearch validate-docker-gpu --docker-image "$RUNNER_IMAGE"
```

## Provider and boundary smoke validation

Validate the configured provider and smoke Candidate contract without training:

```bash
uv run python - <<'PY'
from ml_autoresearch.candidate_execution_config import load_configured_research_problem_registry
registry = load_configured_research_problem_registry('.')
print(registry.ids())
PY

uv run ml-autoresearch validate-candidate \
  --candidate tests/fixtures/candidates/abi_tiny_smoke \
  --workspace-root . \
  --no-require-proposal

uv run python scripts/smoke_workspace.py --workspace-root .
```

`scripts/smoke_workspace.py` creates temporary Run/ledger state, executes only
the configured Docker smoke-test forward pass, reports `trained: false`, and
removes the temporary state. It does not run a training epoch.

Prepare the Agent Control Boundary after image validation:

```bash
export ML_AUTORESEARCH_PI_FORT=/absolute/path/to/pi-fort
uv run ml-autoresearch prepare-agent-boundary --workspace-root .
```

The full training dataset is not mounted into the Agent Control Boundary by
default. Candidate Execution receives trusted Research Problem roots only
through Harness-owned read-only Docker mounts at `/data/training` and
`/data/ancillary`; candidate inputs still contain no longitude or latitude.

## MCAST baseline evaluation

MCAST 1.1 and 2.1 are trusted Baseline Segmenters, not Candidate Experiments.
Their checkpoints remain local approved provider assets and are not copied into
candidate source or downloaded at runtime.

Install the baseline dependency group on the GPU server. The evaluation can
use the full A100, but cap CPU affinity and numerical-library thread pools to
75% of the available logical cores so the host remains responsive:

```bash
uv sync --group baselines

CPU_COUNT=$(nproc)
CPU_LIMIT=$((CPU_COUNT * 3 / 4))
CPUSET="0-$((CPU_LIMIT - 1))"
OUTPUT_ROOT=/data/iross/abi-ml-autoresearch/baselines/initial-20260807

# Confirm that GPU index 0 is the A100 before starting.
nvidia-smi --query-gpu=index,name --format=csv

# Run MCAST 1.1.
taskset -c "$CPUSET" env \
  OMP_NUM_THREADS="$CPU_LIMIT" \
  MKL_NUM_THREADS="$CPU_LIMIT" \
  OPENBLAS_NUM_THREADS="$CPU_LIMIT" \
  NUMEXPR_NUM_THREADS="$CPU_LIMIT" \
  CUDA_VISIBLE_DEVICES=0 \
  uv run --group baselines abi-baseline-evaluate \
    --workspace-root . \
    --baseline mcast_detection_1_1 \
    --device cuda \
    --log-every 100 \
    --output-root "$OUTPUT_ROOT"

# Run MCAST 2.1 after 1.1 completes.
taskset -c "$CPUSET" env \
  OMP_NUM_THREADS="$CPU_LIMIT" \
  MKL_NUM_THREADS="$CPU_LIMIT" \
  OPENBLAS_NUM_THREADS="$CPU_LIMIT" \
  NUMEXPR_NUM_THREADS="$CPU_LIMIT" \
  CUDA_VISIBLE_DEVICES=0 \
  uv run --group baselines abi-baseline-evaluate \
    --workspace-root . \
    --baseline mcast_detection_2_1 \
    --device cuda \
    --log-every 100 \
    --output-root "$OUTPUT_ROOT"
```

Progress is timestamped to the terminal and appended to
`$OUTPUT_ROOT/baseline_evaluation.log`. It covers dataset construction, model
loading, inference sample count/rate/ETA, metric filtering, every threshold
sweep stage, artifact writing, and completion. Monitor it from another shell:

```bash
tail -f "$OUTPUT_ROOT/baseline_evaluation.log"
```

The output root contains the shared `baseline_evaluation.log`. Each baseline
subdirectory contains:

- `aggregate_metrics.json`;
- `per_sample_metrics.jsonl`;
- `threshold_sweep.json`;
- bounded diagnostic GeoTIFF metadata/artifacts;
- `run_manifest.json` with workspace/Harness Git provenance, data and split
  configuration, model asset hashes, device, sample count, and artifact paths.

This provider-owned command applies the same raw/filtered metric and Artifact
Filter path as candidate assessment. It does not call MCAST operational
postprocessing.

The artifacts under
`/data/iross/abi-ml-autoresearch/baselines/initial-20260807` are explicitly
**scanline-only** parity targets: geographic ancillary availability was false
for every sample. Do not overwrite them or describe them as geographic-enabled.
Use the ABI-022 accelerated evaluator to generate replacement MCAST 1.1/2.1
artifacts with the required Geographic Feature Filter active under a separately
named output root, following
`evaluation-requests/abi-023-geographic-enabled-mcast-baselines.md`. The handoff
uses the standalone named ancillary root and does not modify the training data.

## Development validation

```bash
uv run --group torch pytest
```

Unit tests use tiny fixtures and do not depend on the external `data` symlink.
Do not perform real model training on this machine.

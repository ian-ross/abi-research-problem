# ABI-021 canonical baseline comparison targets

## Canonical registry

The trusted machine-readable comparison registry is:

`/data/iross/abi-ml-autoresearch/baselines/canonical/mcast-working-validation-v1.json`

Registry id: `abi-mcast-working-validation-v1`

Registry SHA-256 at generation: `dc7de95ce72ffdddbd6a8a58832ed63d3a00737bdebdc29a5fa52c28c97102a1`

The complete canonical evaluation copies are stored beneath:

- `/data/iross/abi-ml-autoresearch/baselines/canonical/mcast_detection_1_1`
- `/data/iross/abi-ml-autoresearch/baselines/canonical/mcast_detection_2_1`

The required model assets are contained at:

- `/data/iross/abi-ml-autoresearch/baselines/canonical/model-assets/detection-1.1.pt`
- `/data/iross/abi-ml-autoresearch/baselines/canonical/model-assets/detection-2.1`

All registry artifact and model-asset paths resolve inside `canonical/`; the bundle has no
runtime dependency on the evaluation or model directories from which it was generated. The workspace
configuration resolves the registry relative to the named trusted
`baselines` root. Candidate acceptance reports load it automatically when
explicit baseline metrics are not supplied and record the registry, run
manifest, and aggregate-metrics paths they used.

## Comparison modes

The same validated MCAST predictions provide two canonical modes:

- `unfiltered`: `raw/*` metrics before the Geographic Feature and Scanline
  Artifact Filters;
- `artifact_filtered`: `filtered/*` metrics after the ordered Geographic
  Feature then Scanline Artifact Filter pipeline.

Both MCAST runs use the same 3,088-sample Working Validation Split (MIT 1,232;
Google 1,856). The registry records sample-id digest
`42982774c168d6b9f24205de66972035e6eaa3a892c4752bc83230ad95a9c290`,
model asset hashes, source/split configuration, workspace and Harness Git
provenance, Natural Earth identities and hashes, effective scanline settings,
and checksums for every referenced comparison artifact.

| Baseline | Raw Dice | Filtered Dice | Geographic pixels removed | Scanline pixels removed |
|---|---:|---:|---:|---:|
| MCAST 1.1 | 0.397901603 | 0.384248340 | 35,586 | 0 |
| MCAST 2.1 | 0.399565414 | 0.387284867 | 58,315 | 0 |

The zero scanline removals are an observed MCAST result, not a disabled filter:
the registry records an active Scanline Artifact Filter with minimum run length
128 and maximum probability standard deviation 0.03.

## Reproduction and verification

```bash
BASELINES_ROOT=/data/iross/abi-ml-autoresearch/baselines
uv run abi-baseline-targets generate \
  --source-root "$BASELINES_ROOT/completed-mcast-output" \
  --output "$BASELINES_ROOT/canonical/mcast-working-validation-v1.json"
uv run abi-baseline-targets verify \
  --registry "$BASELINES_ROOT/canonical/mcast-working-validation-v1.json"
```

Generation validates completed run status, both expected MCAST identities,
aggregate/run-manifest parity, per-sample count and shared sample ordering,
source counts, active geographic and scanline settings, per-filter removed-pixel
totals, common split/Git provenance, model hashes, and referenced artifact
checksums. It copies and verifies complete evaluation directories beneath the
canonical root before atomically replacing each canonical directory and the
registry.

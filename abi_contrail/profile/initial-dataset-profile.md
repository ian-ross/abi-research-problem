# GOES ABI initial Dataset Profile Artifact

## Provenance

- artifact_type: Dataset Profile Artifact
- schema_version: dataset-profile.v0
- research_problem_id: goes_abi_contrail_segmentation
- research_problem_version: v0
- dataset_identity: GOES ABI Contrail Segmentation on ABI Patches from MIT and Google Dataset Sources
- data_config_scope: local ABI `data_config` with MIT and/or Google zarr paths
- generation_command: `uv run python -m abi_contrail.profile --data-config <CONFIG_JSON> --output profile/generated-abi-dataset-profile.json`
- generation_version: abi_contrail.profile.v0
- generation_timestamp: operator-generated; run the command above for the local dataset snapshot timestamp
- split_scope: Google source provenance plus MIT deterministic whole-scene split before windowing
- source_policy: trusted Research Problem package-generated; checked into the Research Problem package as operator instructions until local raw data is available

## Covered summaries

This package ships `abi_contrail.profile`, a safe generator for a JSON profile covering:

- MIT and Google Dataset Source counts when those sources are present;
- train/validation counts using the provider split policy for each source;
- positive ABI Patch counts and prevalence, where positive means any nonzero Contrail Mask pixel;
- approximate Contrail Mask positive-pixel area distributions;
- input and label zarr shapes for the local snapshot;
- provider split/index policy metadata;
- GOES ABI projection and geolocation caveats, including the no-lon-lat candidate-input rule.

## Missing-data behavior

The generator does **not** require full ABI data to be mounted in agent environments. Operators run it outside the Agent Control Boundary when local MIT/Google zarr data is present. If `--data-config` is absent or malformed, the command exits with a documented placeholder JSON when `--allow-missing` is used, or with a clear data error otherwise.

Example placeholder command:

```bash
uv run python -m abi_contrail.profile --allow-missing --output profile/generated-abi-dataset-profile.json
```

## Known caveats

- Counts summarize the local mounted data snapshot and may differ across regenerated MIT windows or Google downloads.
- MIT full-scene sources are split by whole scene before 256 x 256 windowing to avoid leakage.
- Google patch train/validation membership is treated as scene/file-name provenance, not reshuffled.
- GOES ABI is geostationary satellite data; pixel size, viewing geometry, parallax, and projection effects vary across the disk.
- Longitude and latitude may be present in raw source arrays for trusted diagnostics/Artifact Filters, but they are never candidate model inputs.

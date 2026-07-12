# ABI Research Problem

GOES ABI Contrail Segmentation research problem workspace for `ml-autoresearch`.

## Provider registration

Install this workspace and the local harness dependency with uv:

```bash
uv sync
```

Use the provider target in a candidate execution config:

```toml
[research_problem]
id = "goes_abi_contrail_segmentation"
expected_contract_version = "v0"
package_root = "."
provider_target = "abi_contrail.research_problem:build_spec"
```

For scripts run from this workspace, the provider can be loaded directly:

```bash
uv run python - <<'PY'
from abi_contrail.research_problem import build_spec
spec = build_spec()
print(spec.id, spec.version, spec.input_modes, spec.output_forms, spec.primary_metric)
PY
```

The ABI-001 scaffold exposes the v0 declarative spec only. Dataset loading, leakage-safe splits, filtered metrics, artifact filters, baseline segmenters, and training smoke paths are added by follow-up backlog tasks.

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

Candidate models may import optional ABI front-end helpers from `abi_contrail.model_support`:

```python
from abi_contrail.model_support import Conv1x1ChannelMixer, RawPlusLearnedChannelMixer
```

These helpers mix only the harness-approved input tensor; provider-owned channel selection still excludes longitude and latitude. `RawPlusLearnedChannelMixer` can preserve explicit brightness-temperature-difference features via `difference_channel_pairs=((a, b), ...)`, emitted as `input[a] - input[b]` before the learned projection channels.

The ABI provider exposes the v0 declarative spec plus the staged vertical-slice dataset/training support tracked in the backlog. Filtered metrics, artifact filters, baseline segmenters, and additional sampling policies are added by follow-up tasks.

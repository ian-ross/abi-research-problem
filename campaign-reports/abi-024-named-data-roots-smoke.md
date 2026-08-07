# ABI-024 named data-root Geographic Feature Filter smoke

Date: 2026-08-07
Status: passed
Training performed: no
Candidate code invoked: no
Runtime downloads: no

## Named-root setup

The workspace uses distinct trusted host directories:

- `training`: `/home/mcast/data/ml-training-data/contrail-detection`
  (resolved by the Harness to `/net/d16/data/mcast/ml-training-data/contrail-detection`);
- `ancillary`: `/data/iross/abi-ml-autoresearch/ancillary`.

The existing Natural Earth bundle is installed directly at
`/data/iross/abi-ml-autoresearch/ancillary/natural-earth`. The disposable
`/data/iross/abi-ml-autoresearch/abi-023-smoke-data` symlink wrapper has been
removed and neither smoke depends on a writable training directory.

Offline verification:

```bash
uv run abi-provision-natural-earth \
  --ancillary-root /data/iross/abi-ml-autoresearch/ancillary \
  --verify-only
```

Verified Natural Earth v5.1.2 sources:

- coastline: 10,110,735 bytes, SHA-256
  `6f75ae0e0de157b14946e2255eb1f5486d9a13819032e26d4610852d296788f6`;
- North America rivers: 8,734,704 bytes, SHA-256
  `dcd2348655a5f3d0ea7be35024073ab24f09115d2e4efb77e7bc0a33567db682`.

## Bounded host smoke

```bash
uv run abi-geographic-filter-smoke --workspace-root . --max-samples 64
```

The smoke passed on the first validation ABI Patch:

- candidate input channels: 16;
- longitude/latitude exposed to candidate: false;
- Geographic Feature Filter active: true;
- rasterized geographic pixels: 588;
- removed all-positive trusted-prediction pixels: 588;
- samples examined: 1 of at most 64.

## Network-disabled runner-container smoke

The rebuilt configured runner image includes the trusted filter's SciPy runtime
dependency. It was launched with `--network none`, the provider repository
read-only, and two distinct read-only mounts:

- training host root to `/data/training`;
- ancillary host root to `/data/ancillary`.

The container used the Harness-shaped mapping
`{"training": "/data/training", "ancillary": "/data/ancillary"}` and the same
root-relative provider configuration. It verified the installed bundle, built
the validation dataset, and passed the bounded filter smoke on the first Patch
with 588 pixels rasterized and removed. The result explicitly reported no
training, no runtime downloads, and no longitude/latitude Candidate Experiment
inputs.

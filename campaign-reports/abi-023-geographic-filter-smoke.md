# ABI-023 bounded Geographic Feature Filter smoke

Date: 2026-08-07
Status: passed
Training performed: no
Candidate code invoked: no

## Setup

The configured production dataset root is read-only to the current operator, so
the bounded host smoke used a trusted wrapper root at:

`/data/iross/abi-ml-autoresearch/abi-023-smoke-data`

Its `mit/` and `google/` entries point to the read-only source data, while its
`ancillary/natural-earth/` directory was provisioned by the new explicit
operator command. This wrapper was used only for native provider smoke
validation, not as a claim that cross-mount symlinks are suitable for Docker.
Production container evaluation still requires provisioning beneath the real
mounted dataset root.

Provisioning and verification:

```bash
uv run abi-provision-natural-earth \
  --dataset-root /data/iross/abi-ml-autoresearch/abi-023-smoke-data
uv run abi-provision-natural-earth \
  --dataset-root /data/iross/abi-ml-autoresearch/abi-023-smoke-data \
  --verify-only
```

Verified sources:

- Natural Earth 1:10m Coastline v5.1.2, 10,110,735 bytes,
  SHA-256 `6f75ae0e0de157b14946e2255eb1f5486d9a13819032e26d4610852d296788f6`.
- Natural Earth 1:10m North America Rivers v5.1.2, 8,734,704 bytes,
  SHA-256 `dcd2348655a5f3d0ea7be35024073ab24f09115d2e4efb77e7bc0a33567db682`.

## Smoke command and result

```bash
uv run abi-geographic-filter-smoke \
  --workspace-root . \
  --dataset-root /data/iross/abi-ml-autoresearch/abi-023-smoke-data \
  --max-samples 64
```

The smoke passed on the first validation ABI Patch:

- candidate input channels: 16;
- longitude/latitude exposed to candidate: false;
- Geographic Feature Filter active: true;
- rasterized geographic pixels: 588;
- removed all-positive trusted-prediction pixels: 588;
- samples examined: 1 of at most 64.

This validates native host resolution and real ABI geolocation rasterization.
A separate network-disabled runner-container smoke bind-mounted the wrapper root
at `/data` and successfully resolved and verified the same installed manifest as
`/data/ancillary/natural-earth/manifest.json`. Unit tests cover strict
missing/hash failure behavior. Full production activation remains an operator
setup step because the current production dataset root is not writable by this
user.

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

from abi_contrail.ancillary import (
    AncillaryDataError,
    committed_natural_earth_manifest_path,
    resolve_geographic_ancillary,
)
from abi_contrail.ancillary_cli import provision_natural_earth, run_geographic_filter_smoke
from abi_contrail.artifact_filters import GeographicFeatureFilter, build_default_artifact_filter_pipeline


def _manifest_for(payloads: dict[str, bytes]) -> dict[str, object]:
    datasets = []
    for dataset_id, content in payloads.items():
        filename = f"{dataset_id}.geojson"
        datasets.append(
            {
                "id": dataset_id,
                "name": dataset_id,
                "version": "fixture-v1",
                "immutable_url": f"https://example.invalid/{filename}",
                "filename": filename,
                "size_bytes": len(content),
                "sha256": hashlib.sha256(content).hexdigest(),
                "license": {
                    "name": "Natural Earth public domain",
                    "url": "https://www.naturalearthdata.com/about/terms-of-use/",
                },
            }
        )
    return {
        "schema_version": 1,
        "bundle_id": "natural-earth-fixture-v1",
        "datasets": datasets,
    }


def _write_manifest(path: Path, manifest: dict[str, object]) -> Path:
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return path


def test_committed_natural_earth_manifest_pins_immutable_sources() -> None:
    manifest = json.loads(committed_natural_earth_manifest_path().read_text())

    assert manifest["bundle_id"] == "natural-earth-vector-v5.1.2-abi-geographic-filter"
    assert {item["id"] for item in manifest["datasets"]} == {
        "natural_earth_10m_coastline",
        "natural_earth_10m_rivers_north_america",
    }
    for item in manifest["datasets"]:
        assert "f1890d9f152c896d250a77557a5751a93d494776" in item["immutable_url"]
        assert item["size_bytes"] > 0
        assert len(item["sha256"]) == 64
        assert item["license"]["name"] == "Natural Earth public domain"


def test_provisioning_is_idempotent_and_writes_verified_manifest(tmp_path: Path) -> None:
    payloads = {
        "natural_earth_10m_coastline": b'{"type":"FeatureCollection","features":[]}',
        "natural_earth_10m_rivers_north_america": b'{"type":"FeatureCollection","features":[]}',
    }
    manifest_path = _write_manifest(tmp_path / "source-manifest.json", _manifest_for(payloads))
    dataset_root = tmp_path / "dataset"
    dataset_root.mkdir()
    downloads: list[str] = []

    def download(url: str, destination: Path) -> None:
        downloads.append(url)
        dataset_id = Path(url).stem
        destination.write_bytes(payloads[dataset_id])

    first = provision_natural_earth(
        dataset_root=dataset_root,
        source_manifest_path=manifest_path,
        downloader=download,
    )
    second = provision_natural_earth(
        dataset_root=dataset_root,
        source_manifest_path=manifest_path,
        downloader=download,
    )

    assert len(downloads) == 2
    assert first["dataset_root"] == str(dataset_root.resolve())
    assert first["root_contract"] == "legacy_single_dataset_root"
    assert {item["status"] for item in first["datasets"]} == {"downloaded"}
    assert {item["status"] for item in second["datasets"]} == {"already_valid"}
    installed = dataset_root / "ancillary" / "natural-earth" / "manifest.json"
    assert json.loads(installed.read_text())["bundle_id"] == "natural-earth-fixture-v1"


def test_standalone_ancillary_root_provisioning_and_named_resolution(tmp_path: Path) -> None:
    payloads = {
        "natural_earth_10m_coastline": b'{"type":"FeatureCollection","features":[]}',
        "natural_earth_10m_rivers_north_america": b'{"type":"FeatureCollection","features":[]}',
    }
    manifest_path = _write_manifest(tmp_path / "source-manifest.json", _manifest_for(payloads))
    training_root = tmp_path / "training"
    ancillary_root = tmp_path / "ancillary"
    training_root.mkdir()
    ancillary_root.mkdir()

    def download(url: str, destination: Path) -> None:
        destination.write_bytes(payloads[Path(url).stem])

    report = provision_natural_earth(
        ancillary_root=ancillary_root,
        source_manifest_path=manifest_path,
        downloader=download,
    )
    config = {
        "data_roots": {
            "training": str(training_root),
            "ancillary": str(ancillary_root),
        },
        "geographic_filter_required": True,
        "geographic_ancillary_manifest": "natural-earth/manifest.json",
        "coastline_geojson": "natural-earth/natural_earth_10m_coastline.geojson",
        "rivers_geojson": "natural-earth/natural_earth_10m_rivers_north_america.geojson",
    }
    bundle = resolve_geographic_ancillary(config)

    assert report["root_contract"] == "named_ancillary_root"
    assert report["manifest"] == str(ancillary_root / "natural-earth" / "manifest.json")
    assert bundle.manifest_path == (ancillary_root / "natural-earth" / "manifest.json").resolve()
    assert bundle.coastline_geojson is not None
    assert bundle.coastline_geojson.is_relative_to(ancillary_root)
    assert bundle.rivers_geojson is not None
    assert bundle.rivers_geojson.is_relative_to(ancillary_root)


def test_dataset_root_relative_ancillary_resolution_validates_checksums(tmp_path: Path) -> None:
    coastline = b'{"type":"FeatureCollection","features":[]}'
    rivers = b'{"type":"FeatureCollection","features":[]}'
    manifest = _manifest_for(
        {
            "natural_earth_10m_coastline": coastline,
            "natural_earth_10m_rivers_north_america": rivers,
        }
    )
    root = tmp_path / "mounted-data"
    ancillary = root / "ancillary" / "natural-earth"
    ancillary.mkdir(parents=True)
    (ancillary / "natural_earth_10m_coastline.geojson").write_bytes(coastline)
    (ancillary / "natural_earth_10m_rivers_north_america.geojson").write_bytes(rivers)
    _write_manifest(ancillary / "manifest.json", manifest)

    bundle = resolve_geographic_ancillary(
        {
            "dataset_root": str(root),
            "geographic_filter_required": True,
            "geographic_ancillary_manifest": "ancillary/natural-earth/manifest.json",
        }
    )

    assert bundle.active is True
    assert bundle.manifest_path == (ancillary / "manifest.json").resolve()
    assert bundle.coastline_geojson.name == "natural_earth_10m_coastline.geojson"
    assert bundle.rivers_geojson.name == "natural_earth_10m_rivers_north_america.geojson"
    assert {source["sha256"] for source in bundle.sources} == {
        hashlib.sha256(coastline).hexdigest(),
        hashlib.sha256(rivers).hexdigest(),
    }

    (ancillary / "natural_earth_10m_coastline.geojson").write_bytes(b"corrupt")
    with pytest.raises(AncillaryDataError, match="SHA-256|size"):
        resolve_geographic_ancillary(
            {
                "dataset_root": str(root),
                "geographic_filter_required": True,
                "geographic_ancillary_manifest": "ancillary/natural-earth/manifest.json",
            }
        )


def test_required_geographic_ancillary_data_never_falls_back_to_empty_filter(tmp_path: Path) -> None:
    with pytest.raises(AncillaryDataError, match="required.*manifest"):
        build_default_artifact_filter_pipeline(
            {
                "dataset_root": str(tmp_path),
                "geographic_filter_required": True,
                "geographic_ancillary_manifest": "ancillary/natural-earth/manifest.json",
            }
        )


def test_real_geojson_rasterization_reports_active_separately_from_patch_intersection(tmp_path: Path) -> None:
    coastline_payload = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {"type": "LineString", "coordinates": [[-100.0, 40.0], [-99.0, 40.0]]},
            }
        ],
    }
    rivers_payload = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {"type": "MultiLineString", "coordinates": [[[-100.0, 39.0], [-100.0, 40.0]]]},
            }
        ],
    }
    coastline = json.dumps(coastline_payload).encode()
    rivers = json.dumps(rivers_payload).encode()
    payloads = {
        "natural_earth_10m_coastline": coastline,
        "natural_earth_10m_rivers_north_america": rivers,
    }
    ancillary = tmp_path / "ancillary" / "natural-earth"
    ancillary.mkdir(parents=True)
    for dataset_id, content in payloads.items():
        (ancillary / f"{dataset_id}.geojson").write_bytes(content)
    _write_manifest(ancillary / "manifest.json", _manifest_for(payloads))
    pipeline = build_default_artifact_filter_pipeline(
        {
            "dataset_root": str(tmp_path),
            "geographic_filter_required": True,
            "geographic_ancillary_manifest": "ancillary/natural-earth/manifest.json",
            "geographic_filter_pixel_buffer": 0,
            "scanline_min_length_pixels": 999,
        }
    )
    lon, lat = np.meshgrid(np.linspace(-100.0, -99.0, 5), np.linspace(39.0, 40.0, 5))
    prediction = np.ones((1, 5, 5), dtype=bool)
    result = pipeline.apply(prediction, prediction.astype(np.float32), context={"longitude": lon, "latitude": lat})
    geographic = result.diagnostics["filters"][0]

    assert geographic["active"] is True
    assert geographic["available"] is True
    assert geographic["intersects_grid"] is True
    assert geographic["removed_pixel_count"] > 0
    assert not result.filtered_mask.all()

    far_lon, far_lat = np.meshgrid(np.linspace(0.0, 1.0, 5), np.linspace(0.0, 1.0, 5))
    far = pipeline.apply(prediction, prediction.astype(np.float32), context={"longitude": far_lon, "latitude": far_lat})
    far_geographic = far.diagnostics["filters"][0]
    assert far_geographic["active"] is True
    assert far_geographic["intersects_grid"] is False


class _SmokeDataset:
    def __len__(self) -> int:
        return 1

    def __getitem__(self, index: int):
        import torch

        assert index == 0
        return torch.zeros((16, 3, 3)), torch.zeros((1, 3, 3))

    def filter_context(self, index: int) -> dict[str, object]:
        assert index == 0
        mask = np.zeros((3, 3), dtype=bool)
        mask[1, 1] = True
        return {"geographic_feature_mask": mask}


def test_bounded_geographic_filter_smoke_uses_provider_context_not_candidate_inputs() -> None:
    report = run_geographic_filter_smoke(
        dataset=_SmokeDataset(),
        filter_pipeline=build_default_artifact_filter_pipeline(),
        max_samples=1,
    )

    assert report["status"] == "passed"
    assert report["samples_examined"] == 1
    assert report["candidate_input_channels"] == 16
    assert report["geographic_removed_pixel_count"] == 1
    assert report["longitude_latitude_exposed_to_candidate"] is False

"""Trusted Natural Earth ancillary-data resolution and verification.

This module is deliberately offline. Network access exists only in the explicit
operator provisioning command in :mod:`abi_contrail.ancillary_cli`.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

COASTLINE_DATASET_ID = "natural_earth_10m_coastline"
RIVERS_DATASET_ID = "natural_earth_10m_rivers_north_america"
DEFAULT_ANCILLARY_MANIFEST = "ancillary/natural-earth/manifest.json"


class AncillaryDataError(ValueError):
    """Trusted ancillary configuration or content is missing or invalid."""


@dataclass(frozen=True)
class GeographicAncillaryBundle:
    """Resolved and verified provider-owned geographic ancillary data."""

    active: bool
    required: bool
    reason: str
    bundle_id: str | None = None
    manifest_path: Path | None = None
    coastline_geojson: Path | None = None
    rivers_geojson: Path | None = None
    sources: tuple[dict[str, object], ...] = ()

    def provenance(self) -> dict[str, object]:
        return {
            "active": self.active,
            "required": self.required,
            "reason": self.reason,
            "bundle_id": self.bundle_id,
            "manifest_path": str(self.manifest_path) if self.manifest_path is not None else None,
            "sources": [dict(source) for source in self.sources],
        }


def committed_natural_earth_manifest_path() -> Path:
    """Return the package-owned pinned Natural Earth source manifest."""

    return Path(__file__).with_name("data") / "natural-earth-v5.1.2.json"


def load_ancillary_manifest(path: str | Path) -> dict[str, object]:
    """Load and structurally validate an ancillary provenance manifest."""

    manifest_path = Path(path)
    try:
        payload = json.loads(manifest_path.read_text())
    except FileNotFoundError as exc:
        raise AncillaryDataError(f"required geographic ancillary manifest does not exist: {manifest_path}") from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise AncillaryDataError(f"invalid geographic ancillary manifest {manifest_path}: {exc}") from exc
    if not isinstance(payload, dict) or payload.get("schema_version") != 1:
        raise AncillaryDataError(f"unsupported geographic ancillary manifest schema: {manifest_path}")
    bundle_id = payload.get("bundle_id")
    if not isinstance(bundle_id, str) or not bundle_id:
        raise AncillaryDataError(f"geographic ancillary manifest is missing bundle_id: {manifest_path}")
    datasets = payload.get("datasets")
    if not isinstance(datasets, Sequence) or isinstance(datasets, (str, bytes)):
        raise AncillaryDataError(f"geographic ancillary manifest datasets must be a sequence: {manifest_path}")
    ids: set[str] = set()
    for raw in datasets:
        if not isinstance(raw, Mapping):
            raise AncillaryDataError(f"geographic ancillary manifest contains a non-mapping dataset: {manifest_path}")
        dataset_id = _required_string(raw, "id", manifest_path)
        if dataset_id in ids:
            raise AncillaryDataError(f"duplicate geographic ancillary dataset id {dataset_id!r}: {manifest_path}")
        ids.add(dataset_id)
        _required_string(raw, "name", manifest_path)
        _required_string(raw, "version", manifest_path)
        _required_string(raw, "immutable_url", manifest_path)
        filename = _required_string(raw, "filename", manifest_path)
        if Path(filename).name != filename:
            raise AncillaryDataError(f"geographic ancillary filename must be a basename: {filename!r}")
        size_bytes = raw.get("size_bytes")
        if not isinstance(size_bytes, int) or size_bytes < 1:
            raise AncillaryDataError(f"invalid size_bytes for geographic ancillary dataset {dataset_id!r}")
        sha256 = _required_string(raw, "sha256", manifest_path)
        if len(sha256) != 64 or any(char not in "0123456789abcdef" for char in sha256.lower()):
            raise AncillaryDataError(f"invalid SHA-256 for geographic ancillary dataset {dataset_id!r}")
        license_record = raw.get("license")
        if not isinstance(license_record, Mapping):
            raise AncillaryDataError(f"missing license for geographic ancillary dataset {dataset_id!r}")
        _required_string(license_record, "name", manifest_path)
        _required_string(license_record, "url", manifest_path)
    missing = {COASTLINE_DATASET_ID, RIVERS_DATASET_ID} - ids
    if missing:
        raise AncillaryDataError(f"geographic ancillary manifest is missing required datasets: {sorted(missing)}")
    return payload


def resolve_geographic_ancillary(data_config: Mapping[str, object] | None = None) -> GeographicAncillaryBundle:
    """Resolve dataset-root-relative ancillary paths and verify every byte."""

    config = data_config or {}
    required = _bool_value(config.get("geographic_filter_required", False), "geographic_filter_required")
    manifest_value = config.get("geographic_ancillary_manifest")
    legacy_configured = bool(config.get("coastline_geojson") or config.get("rivers_geojson"))
    if manifest_value is None or manifest_value == "":
        if required:
            raise AncillaryDataError(
                "required geographic ancillary manifest is not configured; set "
                "data_config.geographic_ancillary_manifest"
            )
        if legacy_configured:
            raise AncillaryDataError(
                "coastline_geojson/rivers_geojson require a verified geographic_ancillary_manifest"
            )
        return GeographicAncillaryBundle(active=False, required=False, reason="not_configured")
    if not isinstance(manifest_value, str):
        raise AncillaryDataError("data_config.geographic_ancillary_manifest must be a path string")

    root = _dataset_root(config)
    manifest_path = _resolve_from_root(root, manifest_value)
    manifest = load_ancillary_manifest(manifest_path)
    datasets = {str(item["id"]): dict(item) for item in manifest["datasets"] if isinstance(item, Mapping)}
    coastline = _configured_or_manifest_path(
        root=root,
        manifest_path=manifest_path,
        configured=config.get("coastline_geojson"),
        dataset=datasets[COASTLINE_DATASET_ID],
        config_key="coastline_geojson",
    )
    rivers = _configured_or_manifest_path(
        root=root,
        manifest_path=manifest_path,
        configured=config.get("rivers_geojson"),
        dataset=datasets[RIVERS_DATASET_ID],
        config_key="rivers_geojson",
    )
    paths = {COASTLINE_DATASET_ID: coastline, RIVERS_DATASET_ID: rivers}
    sources: list[dict[str, object]] = []
    for dataset_id in (COASTLINE_DATASET_ID, RIVERS_DATASET_ID):
        source = datasets[dataset_id]
        source_path = paths[dataset_id]
        _verify_file(source_path, source)
        sources.append(
            {
                "id": dataset_id,
                "name": source["name"],
                "version": source["version"],
                "immutable_url": source["immutable_url"],
                "license": dict(source["license"]),
                "filename": source["filename"],
                "path": str(source_path),
                "size_bytes": source["size_bytes"],
                "sha256": source["sha256"],
            }
        )
    return GeographicAncillaryBundle(
        active=True,
        required=required,
        reason="verified",
        bundle_id=str(manifest["bundle_id"]),
        manifest_path=manifest_path,
        coastline_geojson=coastline,
        rivers_geojson=rivers,
        sources=tuple(sources),
    )


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_manifest_dataset_file(path: Path, dataset: Mapping[str, object]) -> None:
    """Public verification helper shared with explicit provisioning."""

    _verify_file(path, dataset)


def _dataset_root(config: Mapping[str, object]) -> Path:
    value = config.get("dataset_root", config.get("data_root"))
    if not isinstance(value, str) or not value:
        raise AncillaryDataError(
            "dataset_root is required to resolve geographic ancillary paths"
        )
    return Path(value).expanduser().resolve()


def _resolve_from_root(root: Path, value: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = root / path
    return path.resolve()


def _configured_or_manifest_path(
    *,
    root: Path,
    manifest_path: Path,
    configured: object,
    dataset: Mapping[str, object],
    config_key: str,
) -> Path:
    if configured is not None and configured != "":
        if not isinstance(configured, str):
            raise AncillaryDataError(f"data_config.{config_key} must be a path string")
        return _resolve_from_root(root, configured)
    return (manifest_path.parent / str(dataset["filename"])).resolve()


def _verify_file(path: Path, dataset: Mapping[str, object]) -> None:
    dataset_id = str(dataset.get("id", "unknown"))
    if not path.is_file():
        raise AncillaryDataError(f"required geographic ancillary dataset {dataset_id!r} does not exist: {path}")
    expected_size = int(dataset["size_bytes"])
    actual_size = path.stat().st_size
    if actual_size != expected_size:
        raise AncillaryDataError(
            f"geographic ancillary dataset {dataset_id!r} size mismatch: "
            f"expected {expected_size}, got {actual_size}: {path}"
        )
    expected_sha256 = str(dataset["sha256"]).lower()
    actual_sha256 = file_sha256(path)
    if actual_sha256 != expected_sha256:
        raise AncillaryDataError(
            f"geographic ancillary dataset {dataset_id!r} SHA-256 mismatch: "
            f"expected {expected_sha256}, got {actual_sha256}: {path}"
        )


def _required_string(mapping: Mapping[str, object], key: str, path: Path) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value:
        raise AncillaryDataError(f"geographic ancillary manifest entry is missing {key}: {path}")
    return value


def _bool_value(value: object, key: str) -> bool:
    if not isinstance(value, bool):
        raise AncillaryDataError(f"data_config.{key} must be a boolean")
    return value


__all__ = [
    "AncillaryDataError",
    "COASTLINE_DATASET_ID",
    "DEFAULT_ANCILLARY_MANIFEST",
    "GeographicAncillaryBundle",
    "RIVERS_DATASET_ID",
    "committed_natural_earth_manifest_path",
    "file_sha256",
    "load_ancillary_manifest",
    "resolve_geographic_ancillary",
    "verify_manifest_dataset_file",
]

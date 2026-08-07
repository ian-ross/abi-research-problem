"""Trusted ABI data-root normalization.

The Harness injects logical Research Problem roots into ``data_config`` under
``data_roots``.  Native execution receives host paths; Docker execution receives
``/data/<name>`` paths.  Legacy direct callers may continue to provide one
``dataset_root`` or ``data_root``.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from pathlib import Path

TRAINING_DATA_ROOT = "training"
ANCILLARY_DATA_ROOT = "ancillary"


class ABIDataConfigError(ValueError):
    """ABI data-root configuration is missing or invalid."""


def named_data_roots(data_config: Mapping[str, object]) -> dict[str, Path] | None:
    """Return the validated logical-root mapping, or ``None`` for legacy config."""

    if "data_roots" not in data_config:
        return None
    raw_roots = data_config["data_roots"]
    if not isinstance(raw_roots, Mapping):
        raise ABIDataConfigError("ABI data_config.data_roots must be a mapping")
    if not raw_roots:
        raise ABIDataConfigError("ABI data_config.data_roots must not be empty")

    roots: dict[str, Path] = {}
    for raw_name, raw_path in raw_roots.items():
        if not isinstance(raw_name, str) or re.fullmatch(r"[a-z][a-z0-9_-]*", raw_name) is None:
            raise ABIDataConfigError(
                "ABI data_config.data_roots names must match [a-z][a-z0-9_-]*"
            )
        if not isinstance(raw_path, (str, Path)) or not str(raw_path):
            raise ABIDataConfigError(f"ABI data_config.data_roots.{raw_name} must be a non-empty path string")
        roots[raw_name] = Path(raw_path).expanduser().resolve()
    if len(set(roots.values())) != len(roots):
        raise ABIDataConfigError("ABI data_config.data_roots must resolve to distinct directories")
    return roots


def resolve_training_data_root(data_config: Mapping[str, object]) -> Path:
    """Resolve the primary ABI training root with legacy single-root fallback."""

    roots = named_data_roots(data_config)
    if roots is not None:
        try:
            return roots[TRAINING_DATA_ROOT]
        except KeyError as exc:
            raise ABIDataConfigError(
                "ABI data_config.data_roots.training is required for dataset loading"
            ) from exc
    return _legacy_data_root(data_config)


def resolve_ancillary_data_root(data_config: Mapping[str, object]) -> Path:
    """Resolve the ancillary root, falling back to the legacy single data root."""

    roots = named_data_roots(data_config)
    if roots is not None:
        try:
            return roots[ANCILLARY_DATA_ROOT]
        except KeyError as exc:
            raise ABIDataConfigError(
                "ABI data_config.data_roots.ancillary is required for geographic ancillary data"
            ) from exc
    return _legacy_data_root(data_config)


def resolve_root_relative_path(
    root: Path,
    value: object,
    *,
    config_key: str,
    named_root: str | None = None,
) -> Path:
    """Resolve a provider path and contain named-root paths beneath their root."""

    if not isinstance(value, str) or not value:
        raise ABIDataConfigError(f"ABI data_config.{config_key} must be a non-empty path string")
    path = Path(value).expanduser()
    if named_root is not None and path.is_absolute():
        raise ABIDataConfigError(
            f"ABI data_config.{config_key} must be relative to data_roots.{named_root}"
        )
    resolved = (root / path if not path.is_absolute() else path).resolve()
    if named_root is not None:
        try:
            resolved.relative_to(root)
        except ValueError as exc:
            raise ABIDataConfigError(
                f"ABI data_config.{config_key} must resolve beneath data_roots.{named_root}: {root}"
            ) from exc
    return resolved


def with_training_root_override(
    data_config: Mapping[str, object], data_root: str | Path
) -> dict[str, object]:
    """Apply a training-root override without discarding a named ancillary root."""

    resolved = dict(data_config)
    roots = named_data_roots(data_config)
    if roots is not None:
        updated_roots = {name: str(path) for name, path in roots.items()}
        updated_roots[TRAINING_DATA_ROOT] = str(Path(data_root).expanduser().resolve())
        resolved["data_roots"] = updated_roots
    elif "data_root" in resolved and "dataset_root" not in resolved:
        resolved["data_root"] = str(Path(data_root).expanduser().resolve())
    else:
        resolved["dataset_root"] = str(Path(data_root).expanduser().resolve())
    return resolved


def _legacy_data_root(data_config: Mapping[str, object]) -> Path:
    value = data_config.get("dataset_root", data_config.get("data_root"))
    if not isinstance(value, (str, Path)) or not str(value):
        raise ABIDataConfigError(
            "ABI data_config requires data_roots or legacy dataset_root/data_root"
        )
    return Path(value).expanduser().resolve()


__all__ = [
    "ABIDataConfigError",
    "ANCILLARY_DATA_ROOT",
    "TRAINING_DATA_ROOT",
    "named_data_roots",
    "resolve_ancillary_data_root",
    "resolve_root_relative_path",
    "resolve_training_data_root",
    "with_training_root_override",
]

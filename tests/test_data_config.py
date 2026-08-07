from __future__ import annotations

from pathlib import Path

import pytest

from abi_contrail.data_config import (
    ABIDataConfigError,
    named_data_roots,
    resolve_ancillary_data_root,
    resolve_root_relative_path,
    resolve_training_data_root,
    with_training_root_override,
)


def test_named_data_roots_resolve_native_host_directories(tmp_path: Path) -> None:
    training = tmp_path / "training"
    ancillary = tmp_path / "ancillary"
    training.mkdir()
    ancillary.mkdir()
    config = {"data_roots": {"training": str(training), "ancillary": str(ancillary)}}

    assert resolve_training_data_root(config) == training.resolve()
    assert resolve_ancillary_data_root(config) == ancillary.resolve()
    assert named_data_roots(config) == {
        "training": training.resolve(),
        "ancillary": ancillary.resolve(),
    }


def test_named_data_roots_resolve_simulated_container_mounts() -> None:
    config = {
        "data_roots": {
            "training": "/data/training",
            "ancillary": "/data/ancillary",
        }
    }

    assert resolve_training_data_root(config) == Path("/data/training")
    ancillary = resolve_ancillary_data_root(config)
    assert ancillary == Path("/data/ancillary")
    assert resolve_root_relative_path(
        ancillary,
        "natural-earth/manifest.json",
        config_key="geographic_ancillary_manifest",
        named_root="ancillary",
    ) == Path("/data/ancillary/natural-earth/manifest.json")


@pytest.mark.parametrize(
    "config, resolver, match",
    [
        ({"data_roots": []}, resolve_training_data_root, "must be a mapping"),
        ({"data_roots": {}}, resolve_training_data_root, "must not be empty"),
        ({"data_roots": {"ancillary": "/tmp/ancillary"}}, resolve_training_data_root, "data_roots.training"),
        ({"data_roots": {"training": "/tmp/training"}}, resolve_ancillary_data_root, "data_roots.ancillary"),
        ({}, resolve_training_data_root, "legacy dataset_root/data_root"),
    ],
)
def test_invalid_or_missing_logical_roots_fail_clearly(config, resolver, match: str) -> None:
    with pytest.raises(ABIDataConfigError, match=match):
        resolver(config)


def test_named_root_paths_must_be_relative_and_contained(tmp_path: Path) -> None:
    root = tmp_path / "ancillary"

    with pytest.raises(ABIDataConfigError, match="must be relative"):
        resolve_root_relative_path(
            root,
            str(tmp_path / "outside.json"),
            config_key="geographic_ancillary_manifest",
            named_root="ancillary",
        )
    with pytest.raises(ABIDataConfigError, match="must resolve beneath"):
        resolve_root_relative_path(
            root,
            "../outside.json",
            config_key="geographic_ancillary_manifest",
            named_root="ancillary",
        )


def test_legacy_single_root_and_named_training_override_compatibility(tmp_path: Path) -> None:
    legacy = tmp_path / "legacy"
    replacement = tmp_path / "replacement"
    ancillary = tmp_path / "ancillary"

    assert resolve_training_data_root({"dataset_root": str(legacy)}) == legacy.resolve()
    assert resolve_ancillary_data_root({"data_root": str(legacy)}) == legacy.resolve()

    updated = with_training_root_override(
        {
            "data_roots": {
                "training": str(legacy),
                "ancillary": str(ancillary),
            }
        },
        replacement,
    )
    assert updated["data_roots"] == {
        "training": str(replacement.resolve()),
        "ancillary": str(ancillary.resolve()),
    }

"""Provider-owned baseline segmenters for ABI contrail evaluation.

This module integrates MCAST detection checkpoints as trusted Baseline
Segmenters.  It intentionally does not call MCAST's operational
``run_detection`` path: the provider evaluation owns Artifact Filters,
metrics, and all longitude/latitude handling.
"""

from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

MCAST_BASELINE_1_1 = "mcast_detection_1_1"
MCAST_BASELINE_2_1 = "mcast_detection_2_1"
MCAST_BASELINE_NAMES = (MCAST_BASELINE_1_1, MCAST_BASELINE_2_1)

_MCAST_V1_MEANS = np.asarray(
    [274.15866814464114, 275.74145854126134, 3.05802131633268],
    dtype=np.float32,
)
_MCAST_V1_STDS = np.asarray(
    [18.369019656652068, 19.497045505465557, 1.8518705027433054],
    dtype=np.float32,
)
_MCAST_V1_THRESHOLD = 0.42


@dataclass(frozen=True)
class MCASTBaselineMetadata:
    """Declarative metadata for one MCAST Baseline Segmenter."""

    name: str
    version: str
    asset_config_key: str
    expected_asset: str
    output: str = "class_1_probability_and_thresholded_mask_before_mcast_operational_postprocessing"


@dataclass(frozen=True)
class BaselineSegmentationResult:
    """Baseline output for one ABI patch."""

    probabilities: Any
    mask: Any
    threshold: float


MCAST_BASELINE_METADATA = {
    MCAST_BASELINE_1_1: MCASTBaselineMetadata(
        name=MCAST_BASELINE_1_1,
        version="1.1",
        asset_config_key="mcast_detection_1_1_path",
        expected_asset="detection-1.1.pt",
    ),
    MCAST_BASELINE_2_1: MCASTBaselineMetadata(
        name=MCAST_BASELINE_2_1,
        version="2.1",
        asset_config_key="mcast_detection_2_1_path",
        expected_asset="detection-2.1/",
    ),
}


class MCASTBaselineSegmenter:
    """Provider-owned wrapper around an MCAST detection checkpoint.

    The wrapper reproduces the minimal MCAST model-specific preprocessing and
    forward pass: C11, C14, and C13-C15 are normalized, the two-class model is
    evaluated, class-1 softmax probabilities are returned, and masks are
    thresholded with the checkpoint's threshold. MCAST operational geospatial
    clipping/static-feature/scan-line postprocessing is deliberately skipped.
    """

    def __init__(
        self,
        *,
        name: str,
        version: str,
        model: Any,
        means: Any,
        stds: Any,
        threshold: float,
    ) -> None:
        if name not in MCAST_BASELINE_NAMES:
            raise ValueError(f"unsupported MCAST baseline name: {name}")
        self.name = name
        self.version = version
        self.model = model
        self.means = np.asarray(means, dtype=np.float32)
        self.stds = np.asarray(stds, dtype=np.float32)
        if self.means.shape != (3,) or self.stds.shape != (3,):
            raise ValueError("MCAST baseline normalization statistics must have shape (3,)")
        self.threshold = float(threshold)

    @classmethod
    def load(
        cls,
        name: str,
        asset_path: str | Path,
        *,
        device: str | Any = "cpu",
        model_factory: Callable[..., Any] | None = None,
    ) -> "MCASTBaselineSegmenter":
        """Load a supported MCAST baseline from local assets only."""

        path = Path(asset_path).expanduser().resolve()
        if name == MCAST_BASELINE_1_1:
            return cls._load_v1(path, device=device, model_factory=model_factory)
        if name == MCAST_BASELINE_2_1:
            return cls._load_v2(path, device=device, model_factory=model_factory)
        raise ValueError(f"unsupported MCAST baseline name: {name}")

    @classmethod
    def _load_v1(cls, path: Path, *, device: str | Any, model_factory: Callable[..., Any] | None) -> "MCASTBaselineSegmenter":
        if not path.is_file():
            raise FileNotFoundError(f"MCAST 1.1 checkpoint is missing: {path}")
        model = _build_smp_model(
            model_factory,
            "Unet",
            encoder_name="resnet18",
            encoder_weights=None,
            classes=2,
        )
        _load_state_dict(model, path, device=device)
        _eval_model(model, device=device)
        return cls(
            name=MCAST_BASELINE_1_1,
            version="1.1",
            model=model,
            means=_MCAST_V1_MEANS,
            stds=_MCAST_V1_STDS,
            threshold=_MCAST_V1_THRESHOLD,
        )

    @classmethod
    def _load_v2(cls, path: Path, *, device: str | Any, model_factory: Callable[..., Any] | None) -> "MCASTBaselineSegmenter":
        if not path.is_dir():
            raise FileNotFoundError(f"MCAST 2.1 checkpoint directory is missing: {path}")
        config_path = path / "config.json"
        means_path = path / "means.npy"
        stds_path = path / "stds.npy"
        threshold_path = path / "threshold.dat"
        checkpoint_path = path / "checkpoint.pt"
        for required in (config_path, means_path, stds_path, threshold_path, checkpoint_path):
            if not required.exists():
                raise FileNotFoundError(f"MCAST 2.1 asset is missing: {required}")
        cfg = json.loads(config_path.read_text())
        n_channels = int(cfg.get("n_channels", 0))
        if n_channels != 3:
            raise ValueError(f"MCAST 2.1 baseline currently supports exactly 3 input channels, got {n_channels}")
        model = _build_smp_model(
            model_factory,
            str(cfg["architecture"]),
            encoder_name=str(cfg["encoder"]),
            encoder_weights=None,
            in_channels=n_channels,
            classes=2,
            encoder_depth=int(cfg["encoder_depth"]),
            decoder_channels=tuple(cfg["decoder_channels"]),
        )
        _load_state_dict(model, checkpoint_path, device=device)
        _eval_model(model, device=device)
        return cls(
            name=MCAST_BASELINE_2_1,
            version="2.1",
            model=model,
            means=np.load(means_path),
            stds=np.load(stds_path),
            threshold=float(threshold_path.read_text().strip()),
        )

    def predict_patch(self, abi_source: Any, *, threshold: float | None = None, device: str | Any | None = None) -> BaselineSegmentationResult:
        """Return class-1 probabilities and thresholded mask for one patch."""

        import torch
        import torch.nn.functional as F
        from torch import nn

        runtime_device = device if device is not None else _model_device(self.model)
        array = mcast_input_from_abi_source(abi_source)
        normalized = (array - self.means[:, np.newaxis, np.newaxis]) / self.stds[:, np.newaxis, np.newaxis]
        tensor = torch.as_tensor(normalized, dtype=torch.float32, device=runtime_device).unsqueeze(0)
        height, width = tensor.shape[-2:]
        pad_h = (32 - height % 32) % 32
        pad_w = (32 - width % 32) % 32
        if pad_h or pad_w:
            tensor = nn.ReflectionPad2d((0, pad_w, 0, pad_h))(tensor)
        with torch.no_grad():
            outputs = self.model(tensor)
            probabilities = F.softmax(outputs, dim=1)[:, 1:2, :height, :width].detach().cpu()
        cutoff = self.threshold if threshold is None else float(threshold)
        mask = probabilities >= cutoff
        return BaselineSegmentationResult(probabilities=probabilities[0], mask=mask[0], threshold=cutoff)


def mcast_input_from_abi_source(abi_source: Any) -> np.ndarray:
    """Build MCAST C11/C14/C13-C15 inputs from trusted ABI source channels.

    Accepts either channel-first ``[C,H,W]`` arrays/tensors or source ABI
    channel-last ``[H,W,C]`` arrays/tensors.  Longitude/latitude channels, if
    present in the source array, are ignored.
    """

    array = _as_numpy(abi_source).astype(np.float32, copy=False)
    if array.ndim != 3:
        raise ValueError(f"expected ABI source with 3 dimensions, got shape {array.shape}")
    channel_last = 15 <= array.shape[-1] <= 32
    channel_first = 15 <= array.shape[0] <= 32 and not channel_last
    if channel_last:
        c11 = array[..., 10]
        c14 = array[..., 13]
        c13_minus_c15 = array[..., 12] - array[..., 14]
    elif channel_first:
        c11 = array[10]
        c14 = array[13]
        c13_minus_c15 = array[12] - array[14]
    else:
        raise ValueError(f"ABI source must include at least GOES ABI channels 1-15, got shape {array.shape}")
    return np.stack([c11, c14, c13_minus_c15]).astype(np.float32, copy=False)


def configured_mcast_baseline_assets(data_config: Mapping[str, object]) -> dict[str, Path]:
    """Return configured local MCAST baseline asset paths from provider data config."""

    assets: dict[str, Path] = {}
    for name, metadata in MCAST_BASELINE_METADATA.items():
        value = data_config.get(metadata.asset_config_key)
        if isinstance(value, str) and value:
            assets[name] = Path(value).expanduser().resolve()
    return assets


def _build_smp_model(model_factory: Callable[..., Any] | None, architecture: str, **kwargs: Any) -> Any:
    if model_factory is not None:
        return model_factory(architecture=architecture, **kwargs)
    try:
        import segmentation_models_pytorch as smp
    except ImportError as exc:  # pragma: no cover - exercised only without optional dependency in real use
        raise ImportError(
            "MCAST baselines require the optional 'segmentation-models-pytorch' dependency. "
            "Install the baseline dependency group before running baseline evaluations."
        ) from exc
    try:
        factory = getattr(smp, architecture)
    except AttributeError as exc:
        raise ValueError(f"unsupported segmentation_models_pytorch architecture: {architecture}") from exc
    return factory(**kwargs)


def _load_state_dict(model: Any, path: Path, *, device: str | Any) -> None:
    import torch

    try:
        state_dict = torch.load(path, map_location=device, weights_only=True)
    except TypeError:  # older torch without weights_only
        state_dict = torch.load(path, map_location=device)
    model.load_state_dict(state_dict)


def _eval_model(model: Any, *, device: str | Any) -> None:
    to_device = getattr(model, "to", None)
    if callable(to_device):
        model.to(device)
    eval_model = getattr(model, "eval", None)
    if callable(eval_model):
        eval_model()


def _model_device(model: Any) -> Any:
    try:
        return next(model.parameters()).device
    except Exception:  # noqa: BLE001 - fake test models may not expose parameters
        return "cpu"


def _as_numpy(value: Any) -> np.ndarray:
    detach = getattr(value, "detach", None)
    if callable(detach):
        value = detach().cpu().numpy()
    return np.asarray(value)


__all__ = [
    "BaselineSegmentationResult",
    "MCAST_BASELINE_1_1",
    "MCAST_BASELINE_2_1",
    "MCAST_BASELINE_METADATA",
    "MCAST_BASELINE_NAMES",
    "MCASTBaselineMetadata",
    "MCASTBaselineSegmenter",
    "configured_mcast_baseline_assets",
    "mcast_input_from_abi_source",
]

"""M11 must be importable from the packaged layout (Kaggle ZIP / wheel regression guard)."""

from __future__ import annotations

import importlib
import importlib.util


def test_lucid_package_visible() -> None:
    assert importlib.util.find_spec("lucid") is not None


def test_lucid_kaggle_package_visible() -> None:
    assert importlib.util.find_spec("lucid.kaggle") is not None


def test_m11_module_importable() -> None:
    spec = importlib.util.find_spec("lucid.kaggle.m11_probe_panels")
    assert spec is not None, (
        "lucid.kaggle.m11_probe_panels must be discoverable — check src layout and packaging"
    )


def test_m11_has_eval_rows() -> None:
    mod = importlib.import_module("lucid.kaggle.m11_probe_panels")
    assert hasattr(mod, "m11_probe_eval_rows")

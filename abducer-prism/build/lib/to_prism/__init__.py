"""Self-contained, provider-neutral conversion toolkit for Prism."""

from __future__ import annotations

from pathlib import Path


def _read_version() -> str:
    version_file = Path(__file__).resolve().parents[2] / "VERSION"
    try:
        return version_file.read_text(encoding="utf-8").strip()
    except OSError:
        try:
            from importlib.metadata import version

            return version("to-prism")
        except Exception:
            return "0+unknown"


__version__ = _read_version()

__all__ = ["__version__"]

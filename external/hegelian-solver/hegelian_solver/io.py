# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""JSON/YAML I/O helpers.

Every solver artifact (concepts, traces, graphs, reports) is a Pydantic model that can be
read from or written to plain YAML/JSON files. `read_structured`/`write_structured` are the
single choke point for that conversion, so file-format handling and the `.model_dump()`
call needed to serialize a model live in exactly one place instead of being repeated by
every caller (CLI commands, the orchestrator, the run ledger, ...).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


def read_structured(path: str | Path) -> Any:
    """Load a YAML/JSON file into plain dict/list data, by file extension."""

    target = Path(path)
    text = target.read_text()
    if target.suffix.lower() in {".yaml", ".yml"}:
        return yaml.safe_load(text)
    if target.suffix.lower() == ".json":
        return json.loads(text)
    if target.suffix.lower() in {".md", ".txt"}:
        # Lets free-form prose be handed straight to formalize_concept() as a draft.
        return {"name": target.stem, "description": text}
    raise ValueError(f"Unsupported input file type: {target.suffix}")


def write_structured(path: str | Path, payload: Any) -> None:
    """Write a Pydantic model or plain dict/list to YAML/JSON, creating parent dirs."""

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    if hasattr(payload, "model_dump"):
        payload = payload.model_dump(mode="json")
    if target.suffix.lower() in {".yaml", ".yml"}:
        target.write_text(yaml.safe_dump(payload, sort_keys=False))
    elif target.suffix.lower() == ".json":
        target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    else:
        raise ValueError(f"Unsupported output file type: {target.suffix}")


def to_plain(payload: Any) -> Any:
    """Recursively convert Pydantic models (at any nesting depth) into plain JSON data."""

    if hasattr(payload, "model_dump"):
        return payload.model_dump(mode="json")
    if isinstance(payload, list):
        return [to_plain(item) for item in payload]
    if isinstance(payload, dict):
        return {key: to_plain(value) for key, value in payload.items()}
    return payload

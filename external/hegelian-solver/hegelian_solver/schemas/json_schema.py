# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""JSON Schema export helpers.

Writes one `<Model>.schema.json` file per model in `all_schema_models()` (Pydantic's own
`model_json_schema()`), so every public artifact type documents itself in a
language-agnostic format under `data/schemas/`. Driven by the `hegelian-solver schema`
CLI command; regenerate after changing any model in `schemas/models.py` or
`schemas/mechanisms.py`.
"""

from __future__ import annotations

from pathlib import Path

from hegelian_solver.io import write_structured
from hegelian_solver.schemas import all_schema_models


def export_json_schemas(output_dir: str | Path) -> list[Path]:
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for model in all_schema_models():
        path = target / f"{model.__name__}.schema.json"
        write_structured(path, model.model_json_schema())
        written.append(path)
    return written

# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Generate installable typed Python leaf-effect adapter packages."""

from __future__ import annotations

import ast
import json
import re
import shutil
from pathlib import Path
from typing import Any


class AdapterError(ValueError):
    pass


def generate_python_adapter_package(
    *, source_root: Path, project_root: Path, specifications: list[dict[str, Any]]
) -> Path | None:
    """Create wrappers for explicitly reviewed single-function Python leaves.

    Each target receives one explicitly named scalar field from a nominal input
    record and returns one explicitly named field in a nominal output record.
    More complex contracts remain unresolved rather than being hidden behind
    this boundary.
    """
    if not specifications:
        return None
    package_root = project_root / "adapters"
    source_package = package_root / "src" / "converted_prism_adapters"
    upstream = source_package / "upstream"
    upstream.mkdir(parents=True, exist_ok=True)
    (source_package / "__init__.py").write_text("", encoding="utf-8")
    (upstream / "__init__.py").write_text("", encoding="utf-8")
    bindings: list[tuple[str, str]] = []
    functions: list[str] = [
        "from __future__ import annotations",
        "",
        "from importlib import import_module",
        "from prism.language.core import Err, Ok, RecordValue",
        "from prism.language.effects import EffectRequest, EffectResult",
        "",
    ]
    seen_operations: set[str] = set()
    for index, spec in enumerate(specifications, 1):
        operation = str(spec.get("operation", ""))
        if re.fullmatch(r"[a-z][a-z0-9_.-]*", operation) is None:
            raise AdapterError(f"invalid logical operation: {operation!r}")
        if operation in seen_operations:
            raise AdapterError(f"duplicate logical operation: {operation}")
        seen_operations.add(operation)
        relative = Path(str(spec.get("source_path", "")))
        source = (source_root / relative).resolve()
        if source_root.resolve() not in source.parents or not source.is_file():
            raise AdapterError(f"adapter source is not an in-scope file: {relative}")
        if source.suffix != ".py":
            raise AdapterError("v1 typed leaf adapters require a Python source file")
        target_function = str(spec.get("function", ""))
        if re.fullmatch(r"[A-Za-z_]\w*", target_function) is None:
            raise AdapterError(f"invalid Python function: {target_function!r}")
        try:
            module = ast.parse(
                source.read_text(encoding="utf-8"), filename=str(relative)
            )
        except (OSError, UnicodeDecodeError, SyntaxError) as exc:
            raise AdapterError(
                f"adapter source cannot be parsed: {relative}: {exc}"
            ) from exc
        definitions = [
            node
            for node in module.body
            if isinstance(node, ast.FunctionDef) and node.name == target_function
        ]
        if len(definitions) != 1:
            raise AdapterError(
                f"adapter function must be defined exactly once at module scope: {target_function}"
            )
        if len(definitions[0].args.args) != 1 or definitions[0].args.vararg is not None:
            raise AdapterError(
                f"adapter function must accept exactly one positional argument: {target_function}"
            )
        input_type = _nominal_name(spec.get("input_type"), "input_type")
        output_type = _nominal_name(spec.get("output_type"), "output_type")
        input_field = _field_name(spec.get("input_field"), "input_field")
        output_field = _field_name(spec.get("output_field"), "output_field")
        module_name = f"leaf_{index}"
        shutil.copy2(source, upstream / f"{module_name}.py")
        wrapper = f"effect_{index}"
        functions.extend(
            [
                f"def {wrapper}(request: EffectRequest) -> EffectResult:",
                "    try:",
                "        payload = request.arguments[0]",
                "        if not isinstance(payload, RecordValue):",
                f"            raise TypeError({json.dumps('adapter requires ' + input_type + ' record')})",
                f"        if payload.type_name != {json.dumps(input_type)}:",
                f"            raise TypeError({json.dumps('adapter expected ' + input_type)})",
                f"        source_value = payload.fields[{json.dumps(input_field)}]",
                f"        target = getattr(import_module('converted_prism_adapters.upstream.{module_name}'), {json.dumps(target_function)})",
                "        value = target(source_value)",
                f"        result = Ok(RecordValue({json.dumps(output_type)}, {{{json.dumps(output_field)}: str(value)}}))",
                "        diagnostics = ()",
                "    except Exception as exc:",
                "        message = f'{type(exc).__name__}: {exc}'",
                "        result = Err(message)",
                "        diagnostics = (message,)",
                "    return EffectResult(",
                "        result, request.result_type, diagnostics=diagnostics,",
                f"        provenance={{'provider': 'python', 'operation': {json.dumps(operation)}}},",
                f"        executor={json.dumps('python:' + operation)},",
                "    )",
                "",
            ]
        )
        bindings.append((operation, f"converted_prism_adapters.effects:{wrapper}"))
    (source_package / "effects.py").write_text("\n".join(functions), encoding="utf-8")
    entry_lines = "\n".join(
        f"{json.dumps(name)} = {json.dumps(value)}" for name, value in bindings
    )
    (package_root / "pyproject.toml").write_text(
        "\n".join(
            [
                "[build-system]",
                'requires = ["setuptools>=68"]',
                'build-backend = "setuptools.build_meta"',
                "",
                "[project]",
                'name = "converted-prism-adapters"',
                'version = "0.1.0"',
                'requires-python = ">=3.12"',
                'dependencies = ["prism-language==0.0.1", "prism-runtime==0.0.1"]',
                "",
                '[project.entry-points."prism.python_effects"]',
                entry_lines,
                "",
                "[tool.setuptools.packages.find]",
                'where = ["src"]',
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return package_root


def prism_python_wrapper(
    operation: str,
    function_name: str,
    *,
    input_type: str,
    output_type: str,
) -> str:
    return f"""def {function_name}(
    request: {input_type},
    access: PythonCall,
) -> Result[{output_type}, PythonError] ! {{Python.Call}}:
    return python_call[{output_type}]({json.dumps(operation)}, request, access)
"""


def _nominal_name(value: object, label: str) -> str:
    text = str(value or "")
    if re.fullmatch(r"[A-Z][A-Za-z0-9_]*", text) is None:
        raise AdapterError(f"adapter {label} must be a nominal type name")
    return text


def _field_name(value: object, label: str) -> str:
    text = str(value or "")
    if re.fullmatch(r"[a-z_][A-Za-z0-9_]*", text) is None:
        raise AdapterError(f"adapter {label} must be a field identifier")
    return text


__all__ = ["AdapterError", "generate_python_adapter_package", "prism_python_wrapper"]

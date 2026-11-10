# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Retirement tests for pre-v3 proof execution entry points."""

from __future__ import annotations

import ast
import runpy
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

import agentic.discovery.proof as proof
from agentic.discovery.contracts import ContractError


ROOT = Path(__file__).resolve().parents[2]
OLD_WORKER = ROOT / "agentic/scripts/run_discovery_proof_worker.py"
OLD_CLI = ROOT / "agentic/scripts/run_proof_continuation.py"


def test_v2_python_surfaces_are_inert_before_spawn_or_filesystem_use(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    spawn_calls: list[tuple[tuple[Any, ...], dict[str, Any]]] = []

    def forbidden_spawn(*args: Any, **kwargs: Any) -> Any:
        spawn_calls.append((args, kwargs))
        raise AssertionError("retired proof-v2 route attempted to spawn")

    monkeypatch.setattr(subprocess, "Popen", forbidden_spawn)
    with pytest.raises(TypeError, match="history-only"):
        proof.ProofExecutionAuthorizationV2(
            {},
            object(),
        )
    with pytest.raises(ContractError, match="history-only"):
        proof.issue_proof_execution_authorization(object())
    with pytest.raises(ContractError, match="history-only"):
        proof.proof_execution_authorization_projection(object())
    with pytest.raises(ContractError, match="history-only"):
        proof.reopen_indexed_proof_receipt(
            tmp_path / "missing-index.json",
            object(),
        )
    with pytest.raises(ContractError, match="history-only"):
        proof.run_proof_continuation(
            object(),
            tmp_path / "retired-run",
        )
    assert spawn_calls == []
    assert list(tmp_path.iterdir()) == []


def test_worker_v1_python_and_stdio_surfaces_cannot_evaluate_or_spawn(
    tmp_path: Path,
) -> None:
    worker = runpy.run_path(str(OLD_WORKER))
    with pytest.raises(RuntimeError, match="history-only"):
        worker["execute"]({})

    completed = subprocess.run(
        [sys.executable, str(OLD_WORKER)],
        cwd=tmp_path,
        input="{}\n",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert completed.returncode == 2
    assert completed.stdout == ""
    assert "history-only" in completed.stderr
    assert list(tmp_path.iterdir()) == []


def test_retired_cli_rejects_serialized_input_without_creating_run(
    tmp_path: Path,
) -> None:
    run_directory = tmp_path / "must-not-exist"
    completed = subprocess.run(
        [
            sys.executable,
            str(OLD_CLI),
            str(tmp_path / "handoff.json"),
            "--run-directory",
            str(run_directory),
        ],
        cwd=tmp_path,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert completed.returncode == 2
    assert "cannot carry current proof authority" in completed.stderr
    assert not run_directory.exists()


def test_proof_v3_module_names_only_the_v3_worker_as_live_route() -> None:
    source = (
        ROOT / "agentic/discovery/proof_execution.py"
    ).read_text(encoding="utf-8")
    assert "run_discovery_proof_worker_v3.py" in source
    assert '"agentic/scripts/run_discovery_proof_worker.py"' not in source


def test_retired_source_has_no_launch_body_or_production_call_site() -> None:
    proof_path = ROOT / "agentic/discovery/proof.py"
    proof_tree = ast.parse(proof_path.read_text(encoding="utf-8"))
    functions = {
        node.name: node
        for node in ast.walk(proof_tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    for function_name in (
        "issue_proof_execution_authorization",
        "_validate_proof_execution_authorization",
        "reopen_indexed_proof_receipt",
        "run_proof_continuation",
    ):
        function = functions[function_name]
        calls = [
            node
            for node in ast.walk(function)
            if isinstance(node, ast.Call)
        ]
        assert all(
            isinstance(call.func, ast.Name)
            and call.func.id in {"ContractError"}
            for call in calls
        )
        assert not any(
            isinstance(node, (ast.With, ast.For, ast.While, ast.Try))
            for node in ast.walk(function)
        )

    retired_names = {
        "issue_proof_execution_authorization",
        "run_proof_continuation",
    }
    production_calls: list[str] = []
    for path in sorted((ROOT / "agentic").rglob("*.py")):
        if "reports" in path.parts or path == proof_path:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for call in (
            node for node in ast.walk(tree) if isinstance(node, ast.Call)
        ):
            name = (
                call.func.id
                if isinstance(call.func, ast.Name)
                else call.func.attr
                if isinstance(call.func, ast.Attribute)
                else ""
            )
            if name in retired_names:
                production_calls.append(
                    f"{path.relative_to(ROOT).as_posix()}:{name}"
                )
    assert production_calls == []


def test_private_executor_is_reachable_only_from_the_v3_facade() -> None:
    facade = ROOT / "agentic/discovery/proof_v3_facade.py"
    executor = ROOT / "agentic/discovery/proof_execution.py"
    references: list[str] = []
    for path in sorted((ROOT / "agentic").rglob("*.py")):
        if "reports" in path.parts:
            continue
        source = path.read_text(encoding="utf-8")
        if "_execute_current_proof_v3" in source:
            references.append(path.relative_to(ROOT).as_posix())
    assert references == [
        executor.relative_to(ROOT).as_posix(),
        facade.relative_to(ROOT).as_posix(),
    ]

    worker_source = OLD_WORKER.read_text(encoding="utf-8")
    worker_tree = ast.parse(worker_source)
    imported_roots = {
        alias.name.split(".", 1)[0]
        for node in ast.walk(worker_tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    } | {
        str(node.module or "").split(".", 1)[0]
        for node in ast.walk(worker_tree)
        if isinstance(node, ast.ImportFrom)
    }
    assert "ResourceGovernor" not in worker_source
    assert "exact_adapter" not in worker_source
    assert "finite_model_adapter" not in worker_source
    assert "subprocess" not in imported_roots

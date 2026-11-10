# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Keep legacy CLI integration probes from changing shared repository evidence."""

from __future__ import annotations

import shutil
import subprocess
import uuid
from collections.abc import Iterator
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
BUILDER_MODULES = {
    "test_hypothesis_exploration_contracts.py",
    "test_long_horizon_yang_mills_probe.py",
    "test_physics_math_interpretation.py",
    "test_hamiltonian_gap_derivation.py",
    "test_looper_dependency_graph.py",
    "test_reasoning_monitor_html.py",
    "test_work_cycle.py",
}


@pytest.fixture(scope="module", autouse=True)
def preserve_shared_audit_outputs() -> Iterator[None]:
    """Keep shared hook caches and the demo KB note stable between modules."""
    paths = set((ROOT / "agentic/traces/hook_runs").glob("*.json"))
    paths.add(
        ROOT / "InformalMathLib/demo/negative-results/"
        "mathlib.demo.001-witness-family-blocked-route.md"
    )
    originals = {path: path.read_bytes() for path in paths if path.is_file()}
    try:
        yield
    finally:
        for path, original in originals.items():
            if not path.is_file() or path.read_bytes() != original:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(original)


@pytest.fixture(scope="module", autouse=True)
def preserve_shared_builder_outputs(request: pytest.FixtureRequest) -> Iterator[None]:
    """Restore builder inputs/outputs even when unittest class setup raises.

    Historical CLI probes still invoke commands with repository-default output
    paths. Keep their actual results and release failures visible, but prevent
    a failed setup from contaminating later modules or the disclosure diff.
    Unique invocation IDs let cleanup remove only this module's new run files.
    """
    if request.path.name not in BUILDER_MODULES:
        yield
        return
    directories = (
        "agentic/state",
        "agentic/traces",
        "agentic/logs",
        "agentic/reports",
        "agentic/fixtures/hegelian",
        "artifacts/hegelian",
        "tests/fixtures/hegelian",
        "tests/generative/fixtures",
        "KB",
        "InformalMathLib",
    )
    paths = {
        path
        for directory in directories
        for path in (ROOT / directory).rglob("*")
        if path.is_file() and not path.is_symlink()
    }
    paths.update(
        ROOT / name
        for name in (
            "docs/integrations/hegelian-source-map.md",
            "docs/research-methods/conceptual-creativity-operations.md",
        )
    )
    originals = {path: path.read_bytes() for path in paths if path.is_file()}
    pressure_outputs = (
        ROOT / "artifacts/hegelian/pressure_case.json",
        ROOT / "artifacts/hegelian/hegelian_pressure_cases.json",
    )
    run_ids = set()
    original_run = subprocess.run

    def isolated_run(args, *positional, **kwargs):
        if isinstance(args, (list, tuple)) and any(
            str(value).endswith("agentic/scripts/run_target_navigation.py")
            for value in args
        ):
            args = list(args)
            if "--run-id" not in args:
                args.extend(["--run-id", f"sd-test-builder-{uuid.uuid4().hex}"])
            run_ids.add(args[args.index("--run-id") + 1])
        return original_run(args, *positional, **kwargs)

    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(subprocess, "run", isolated_run)
        try:
            yield
        finally:
            for path, original in originals.items():
                if not path.is_file() or path.read_bytes() != original:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(original)
            for path in pressure_outputs:
                if path not in originals:
                    path.unlink(missing_ok=True)
            for run_id in run_ids:
                for directory in ("reports", "traces", "logs"):
                    matches = (ROOT / "agentic" / directory).rglob(f"*{run_id}*")
                    for path in sorted(
                        matches, key=lambda p: len(p.parts), reverse=True
                    ):
                        if path.is_dir():
                            if not any(p.is_relative_to(path) for p in originals):
                                shutil.rmtree(path)
                        elif path not in originals:
                            path.unlink(missing_ok=True)

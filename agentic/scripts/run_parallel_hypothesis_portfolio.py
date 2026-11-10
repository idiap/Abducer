#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Run isolated hypothesis DAG waves and preserve every attempt receipt."""

from __future__ import annotations

import argparse
import importlib
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agentic.discovery.contracts import ContractError, canonical_json, safe_relative_path
from agentic.discovery.hypotheses import build_demo_high_risk_portfolio
from agentic.discovery.parallel import (
    build_parallel_manifest,
    run_parallel_hypothesis_portfolio,
)


def _load(path: Path) -> dict[str, Any]:
    """Load one execution envelope."""

    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"cannot load parallel request {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ContractError("parallel execution input must be a JSON object")
    return value


def _callable(raw: str | None) -> Callable[..., Any] | None:
    """Resolve module:function adapters without shell evaluation."""

    if raw is None:
        return None
    try:
        module_name, attribute = raw.split(":", 1)
        value = getattr(importlib.import_module(module_name), attribute)
    except (ValueError, ImportError, AttributeError) as exc:
        raise ContractError(
            f"invalid adapter {raw!r}; expected module:function"
        ) from exc
    if not callable(value):
        raise ContractError(f"adapter is not callable: {raw!r}")
    return value


def _fixture_worker(outputs: dict[str, Any]) -> Callable[[dict], dict]:
    """Create a deterministic local worker for replayable CLI fixtures."""

    def worker(request: dict) -> dict:
        configured = outputs.get(request["branch_id"])
        if isinstance(configured, dict) and configured.get("raise"):
            raise RuntimeError(str(configured["raise"]))
        if isinstance(configured, dict):
            return configured
        return {
            "theory_delta": {
                "delta_class": "perspective_shift",
                "mechanism_key": request["mechanism_key"],
                "description": (
                    "The branch articulated one mechanism-specific consequence."
                ),
            },
            "claims": [
                {
                    "proposition": "Plural mechanisms should remain visible.",
                    "stance": "support",
                }
            ],
            "genealogy": [request["hypothesis_id"]],
            "conceptual_learning": True,
        }

    return worker


def _write(path: Path, payload: Any) -> None:
    """Atomically publish a run packet under an immutable portfolio identity."""

    if path.name.lower() in {"latest", "latest.json", "current", "current.json"}:
        raise ContractError("mutable latest/current parallel outputs are forbidden")
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", delete=False
    ) as stream:
        temp = Path(stream.name)
        stream.write(canonical_json(payload) + b"\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, path)


def main(argv: list[str] | None = None) -> int:
    """Build or load a manifest, execute workers, and optionally CAS-commit."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--prior-run", type=Path)
    parser.add_argument("--worker-adapter")
    parser.add_argument("--literature-resolver")
    parser.add_argument("--rebase-adapter")
    parser.add_argument("--cas-adapter")
    args = parser.parse_args(argv)
    try:
        if args.input is None:
            envelope: dict[str, Any] = {}
            portfolio = build_demo_high_risk_portfolio()
            manifest = build_parallel_manifest(
                portfolio,
                base_theory_state_version=0,
                resource_budget={
                    "wall_seconds": 30,
                    "max_workers": 4,
                    "cost_units": 20,
                    "storage_bytes": 1_000_000,
                    "matched_budget_baseline_corner_coverage": 1,
                },
            )
        else:
            envelope = _load(args.input)
            if "manifest" in envelope:
                manifest = envelope["manifest"]
            else:
                manifest = build_parallel_manifest(
                    envelope["high_risk_portfolio"],
                    base_theory_state_version=int(
                        envelope.get("base_theory_state_version", 0)
                    ),
                    branch_seeds=envelope.get("branch_seeds"),
                    dependencies=envelope.get("dependencies"),
                    resource_budget=envelope.get("resource_budget"),
                )
        worker = _callable(args.worker_adapter) or _fixture_worker(
            envelope.get("worker_outputs", {})
        )
        prior = _load(args.prior_run) if args.prior_run else None
        packet = run_parallel_hypothesis_portfolio(
            manifest,
            worker,
            prior_run=prior,
            literature_resolver=_callable(args.literature_resolver),
            rebase_worker=_callable(args.rebase_adapter),
            cas_merge=_callable(args.cas_adapter),
        )
        if args.output is None:
            target = safe_relative_path(packet["target_id"]).as_posix()
            output = (
                ROOT
                / "agentic"
                / "runs"
                / "parallel-hypotheses"
                / target
                / f"{packet['portfolio_id']}.json"
            )
        else:
            output = args.output
        _write(output, packet)
        print(
            json.dumps(
                {
                    "portfolio_id": packet["portfolio_id"],
                    "completed": packet["portfolio_metrics"][
                        "successful_branch_count"
                    ],
                    "retry_branch_ids": packet["partial_failure_ledger"][
                        "retry_branch_ids"
                    ],
                    "literature_rebase": packet["literature_rebase"]["status"],
                    "cas": packet["reducer_receipt"][
                        "compare_and_swap_status"
                    ],
                    "output": str(output),
                },
                sort_keys=True,
            )
        )
        return 0
    except (ContractError, KeyError, ValueError) as exc:
        print(f"parallel hypothesis portfolio rejected: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

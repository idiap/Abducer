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
"""Run a target-scoped literature refresh and optional causal assimilation.

Inline source packets are always local-only. A lane can be classified live only
when this command invokes an explicit Python provider adapter for that lane.
Outputs use immutable target/snapshot paths; no global latest alias is written.
"""

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
from agentic.discovery.literature import (
    assimilate_derived_literature,
    assimilate_literature,
    derive_claim_mappings,
    build_demo_literature_snapshot,
    run_frontier_literature_cycle,
)


def _load(path: Path) -> dict[str, Any]:
    """Load one JSON object with a concise CLI error."""

    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"cannot load literature request {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ContractError("literature request must be a JSON object")
    return value


def _adapter(raw: str) -> tuple[str, Callable[..., Any]]:
    """Resolve LANE=module:function without executing shell text."""

    try:
        lane, location = raw.split("=", 1)
        module_name, attribute = location.split(":", 1)
        adapter = getattr(importlib.import_module(module_name), attribute)
    except (ValueError, ImportError, AttributeError) as exc:
        raise ContractError(
            f"invalid provider adapter {raw!r}; expected LANE=module:function"
        ) from exc
    if not callable(adapter):
        raise ContractError(f"provider adapter is not callable: {raw!r}")
    return lane, adapter


def _write(path: Path, payload: Any) -> None:
    """Atomically publish canonical JSON without a mutable latest alias."""

    if path.name.lower() in {"latest", "latest.json", "current", "current.json"}:
        raise ContractError("mutable latest/current literature outputs are forbidden")
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
    """Execute refresh, optionally assimilate mappings, and emit immutable paths."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="JSON request/assimilation envelope")
    parser.add_argument("--output", type=Path, help="immutable snapshot output path")
    parser.add_argument(
        "--provider-adapter",
        action="append",
        default=[],
        help="actual provider boundary as LANE=module:function",
    )
    parser.add_argument("--max-workers", type=int, default=6)
    args = parser.parse_args(argv)
    try:
        if args.input is None:
            snapshot = build_demo_literature_snapshot()
            envelope: dict[str, Any] = {}
        else:
            envelope = _load(args.input)
            request = dict(envelope.get("request", envelope))
            # Serialized source packets cannot attest remote execution. They are
            # copied into inline lane records and the core runner labels them local.
            packets = envelope.get("provider_packets", {})
            for lane in request.get("search_lanes", []):
                packet = packets.get(lane.get("lane_type"))
                if packet:
                    lane["sources"] = packet.get("sources", [])
                    lane["provider"] = packet.get("provider", "serialized-packet")
                    lane["index"] = packet.get("index", "serialized-packet")
                    lane["coverage_cutoff"] = packet.get(
                        "coverage_cutoff", lane.get("coverage_cutoff", "unknown")
                    )
            providers = dict(_adapter(raw) for raw in args.provider_adapter)
            snapshot = run_frontier_literature_cycle(
                request, providers=providers, max_workers=args.max_workers
            )
        if args.output is None:
            target_segment = safe_relative_path(snapshot["target_id"]).as_posix()
            output = (
                ROOT
                / "agentic"
                / "state"
                / "literature"
                / target_segment
                / f"{snapshot['snapshot_id']}.json"
            )
        else:
            output = args.output
        _write(output, snapshot)
        assimilation_path: Path | None = None
        theory_catalog = envelope.get("theory_catalog")
        if theory_catalog is not None:
            if envelope.get("theory_mappings") is not None:
                raise ContractError("derived mode cannot also supply manual theory_mappings")
            derivation = envelope.get("mapping_derivation") or derive_claim_mappings(
                snapshot, theory_catalog=theory_catalog
            )
            packet = assimilate_derived_literature(
                snapshot,
                theory_catalog=theory_catalog,
                mapping_derivation=derivation,
                hypotheses=envelope.get("hypotheses", []),
                prior_snapshot=envelope.get("prior_snapshot"),
                candidate_snapshot_ids=envelope.get("candidate_snapshot_ids", []),
            )
        elif envelope.get("theory_mappings") is not None:
            packet = assimilate_literature(
                snapshot,
                theory_state_digest=snapshot["theory_state_digest"],
                theory_mappings=envelope["theory_mappings"],
                hypotheses=envelope.get("hypotheses", []),
                prior_snapshot=envelope.get("prior_snapshot"),
                candidate_snapshot_ids=envelope.get("candidate_snapshot_ids", []),
            )
        else:
            packet = None
        if packet is not None:
            assimilation_path = output.with_name(
                f"{packet['packet_id']}.assimilation.json"
            )
            _write(assimilation_path, packet)
        print(
            json.dumps(
                {
                    "snapshot_id": snapshot["snapshot_id"],
                    "target_id": snapshot["target_id"],
                    "provenance_mode": snapshot["provenance_mode"],
                    "validation_status": snapshot["validation_status"],
                    "output": str(output),
                    "assimilation_output": (
                        str(assimilation_path) if assimilation_path else None
                    ),
                },
                sort_keys=True,
            )
        )
        return 0
    except ContractError as exc:
        print(f"frontier literature cycle rejected: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

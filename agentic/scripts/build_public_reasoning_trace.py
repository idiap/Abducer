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
"""Assemble a deterministic public trace for a named workflow."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from agentic_common import ROOT, load_json_object, repo_path, write_json  # noqa: E402
from reasoning_trace_adapters import adapt_legacy_projection, assemble_named_workflow_trace, load_events  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--events", required=True, type=Path)
    parser.add_argument("--workflow", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--profile", default="")
    parser.add_argument("--target", default="")
    parser.add_argument("--legacy-projection", action="append", default=[], metavar="KIND=REPO_PATH",
                        help="Attach a read-only descriptor for an established specialized packet")
    parser.add_argument("--registry", type=Path, default=ROOT / "agentic/registries/named_workflow_contracts.yaml")
    parser.add_argument("--trace-contracts", type=Path, default=ROOT / "agentic/registries/named_workflow_trace_contracts.yaml")
    parser.add_argument("--output", type=Path, default=ROOT / "agentic/reports/public_reasoning_trace/latest.json")
    args = parser.parse_args()
    trace_contracts = load_json_object(args.trace_contracts) if args.trace_contracts.exists() else None
    trace = assemble_named_workflow_trace(load_json_object(args.registry), load_events(args.events), workflow_id=args.workflow,
                                          run_id=args.run_id, profile_id=args.profile, target=args.target,
                                          trace_contracts=trace_contracts)
    projections = []
    for raw in args.legacy_projection:
        if "=" not in raw:
            parser.error("--legacy-projection must be KIND=REPO_PATH")
        kind, relative_path = raw.split("=", 1)
        projections.append(adapt_legacy_projection(kind, load_json_object(repo_path(relative_path, must_exist=True)), relative_path))
    trace["legacy_projections"] = projections
    write_json(args.output, trace)
    print(json.dumps({"output": str(args.output), "events": len(trace["events"]), "gaps": len(trace["observability_gaps"])}, sort_keys=True))


if __name__ == "__main__":
    main()

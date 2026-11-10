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
"""Triage, preregister, and execute one theory-requested support probe."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agentic.experiments import (  # noqa: E402
    execute_experiment,
    triage_probe,
    validate_commissioned_experiment_spec,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "request",
        type=Path,
        help="JSON envelope with triage_request, experiment_request, and experiment_spec",
    )
    parser.add_argument("--run-directory", type=Path, required=True)
    args = parser.parse_args()
    envelope = json.loads(args.request.read_text(encoding="utf-8"))
    triage = triage_probe(envelope["triage_request"])
    if triage["decision"] != "commission":
        print(json.dumps({"triage": triage, "receipt": None}, indent=2, sort_keys=True))
        return 0
    spec = validate_commissioned_experiment_spec(
        envelope["triage_request"],
        envelope["experiment_request"],
        envelope["experiment_spec"],
    )
    receipt = execute_experiment(spec, args.run_directory)
    print(json.dumps({"triage": triage, "spec": spec, "receipt": receipt}, indent=2, sort_keys=True))
    return 0 if receipt["status"] in {"succeeded", "counterexample", "capability_unavailable"} else 2


if __name__ == "__main__":
    raise SystemExit(main())

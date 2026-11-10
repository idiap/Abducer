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
"""Generate bounded cohere-fast integration scenarios through codex exec."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "agentic/spec/cohere_fast_generative_scenarios.schema.json"
DEFAULT_OUTPUT = ROOT / "tests/fixtures/cohere_fast/ym/codex_exec_scenarios.json"
CHILDREN = ["scope-and-ground", "adaptive-frontier", "derivation-and-proof", "independent-audit", "manuscript-release"]

PROMPT = """Generate realistic adversarial integration scenarios for Abducer's isolated
cohere-fast Yang-Mills workflow. Return JSON matching the supplied schema.

The workflow stages, in order, are: scope-and-ground, adaptive-frontier,
derivation-and-proof, independent-audit, manuscript-release. Include at least:
(1) a bounded successful finite-regulator run, (2) a derivation quarantine,
(3) a transient adaptive-frontier failure recovered within three attempts, and
(4) an independent-audit failure that quarantines the run and prevents
manuscript release.

Use exactly one attempts row per executed stage, always as a contiguous prefix
of the five stages. Represent retries inside that row's states array; for
example adaptive-frontier states ["failed", "failed", "accepted"]. Never
repeat a subworkflow_id. executed_steps counts stage rows, not retry calls.

Never assert a Yang-Mills mass-gap proof. Claim levels may not exceed C2.
Scientific limitations must be explicit. The expected outcome must agree with
the canonical failure policy: derivation quarantine stops there; failed
independent audit becomes quarantined; only a fully accepted sequence reaches
manuscript release.
Use generator value codex-exec and schema_version 1.0.0."""


def validate(payload: dict) -> None:
    Draft202012Validator(json.loads(SCHEMA.read_text(encoding="utf-8"))).validate(payload)
    ids: set[str] = set()
    required = {"success": False, "quarantine": False, "retry": False, "audit_stop": False}
    for case in payload["scenarios"]:
        if case["id"] in ids:
            raise ValueError(f"duplicate scenario id: {case['id']}")
        ids.add(case["id"])
        attempts = case["attempts"]
        if [row["subworkflow_id"] for row in attempts] != CHILDREN[:len(attempts)]:
            raise ValueError(f"{case['id']}: stages must be a contiguous workflow prefix")
        if case["expected"]["executed_steps"] != len(attempts):
            raise ValueError(f"{case['id']}: executed_steps disagrees with attempts")
        terminal = attempts[-1]
        if len(attempts) == 5 and all(row["states"][-1] == "accepted" for row in attempts):
            required["success"] = True
            if case["expected"]["final_state"] != "accepted" or not case["expected"]["release_reached"]:
                raise ValueError(f"{case['id']}: successful sequence has inconsistent expectation")
        if terminal["subworkflow_id"] == "derivation-and-proof" and terminal["states"][-1] == "quarantined":
            required["quarantine"] = True
            if case["expected"]["final_state"] != "quarantined":
                raise ValueError(f"{case['id']}: quarantine expectation is inconsistent")
        if any(len(row["states"]) > 1 and row["states"][-1] == "accepted" for row in attempts):
            required["retry"] = True
        if terminal["subworkflow_id"] == "independent-audit" and terminal["states"][-1] == "failed":
            required["audit_stop"] = True
            if case["expected"]["final_state"] != "quarantined" or case["expected"]["release_reached"]:
                raise ValueError(f"{case['id']}: audit-stop expectation is inconsistent")
    missing = sorted(name for name, present in required.items() if not present)
    if missing:
        raise ValueError(f"generated corpus lacks required scenario classes: {missing}")


def generate(output: Path, codex: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(".generated.json")
    command = [
        codex, "exec", "--ephemeral", "--sandbox", "read-only", "--ignore-user-config",
        "--output-schema", str(SCHEMA), "--output-last-message", str(temporary), PROMPT,
    ]
    completed = subprocess.run(command, cwd=ROOT, env=dict(os.environ), text=True, capture_output=True, check=False)
    if completed.returncode:
        raise RuntimeError(f"codex exec failed ({completed.returncode}):\n{completed.stdout}\n{completed.stderr}")
    payload = json.loads(temporary.read_text(encoding="utf-8"))
    validate(payload)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--codex", default=os.environ.get("CODEX_EXECUTABLE", "codex"))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        validate(json.loads(args.output.read_text(encoding="utf-8")))
        print(f"validated {args.output}")
    else:
        generate(args.output, args.codex)
        print(f"generated {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

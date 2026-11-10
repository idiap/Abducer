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
"""Validate the structured timeline formal derivation."""

from __future__ import annotations

from agentic_common import clean_text, fail, load_json_object, rel, repo_path
from build_timeline_formal_derivation import OUT_JSON, OUT_TEX


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> int:
    require(OUT_JSON.exists(), f"missing {rel(OUT_JSON)}")
    report = load_json_object(OUT_JSON)
    require(report.get("status") == "timeline_formal_derivation_ready", "formal derivation not ready")
    for field in ["mathematical_object", "definitions", "assumptions", "propositions", "unresolved_obligations", "non_claims"]:
        require(report.get(field), f"formal derivation missing {field}")
    for definition in report["definitions"]:
        for field in ["symbol", "text", "latex", "valid_when", "source_unit_ids"]:
            require(definition.get(field), f"definition missing {field}")
    for prop in report["propositions"]:
        for field in ["name", "statement", "latex", "proof_steps", "valid_when", "source_unit_ids"]:
            require(prop.get(field), f"proposition missing {field}")
    for calc in report.get("calculations", []):
        for field in ["name", "statement", "latex", "valid_when", "source_unit_ids"]:
            require(calc.get(field), f"calculation missing {field}")
    tex_path = repo_path(str(report.get("artifacts", {}).get("tex")), must_exist=True)
    tex = tex_path.read_text(encoding="utf-8")
    require("Formal " in tex and " Derivation" in tex, f"{rel(tex_path)} missing formal derivation section")
    for phrase in ["Definitions", "Assumptions", "Local Propositions", "Unresolved Obligations", "Non-Claims"]:
        require(phrase in tex, f"{rel(tex_path)} missing {phrase}")
    require("Valid when" in tex, "formal derivation TeX must state validity conditions")
    require("does not claim" in tex.lower() or "non-claims" in tex.lower(), "formal derivation needs proof-safety boundary")
    print(f"validated {rel(OUT_JSON)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

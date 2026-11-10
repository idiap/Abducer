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
"""Project the isolated cohere-fast registries into task discovery."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "registry/tasks/cohere-fast/task_registry.json"


def build() -> dict:
    parent = json.loads((ROOT / "agentic/registries/cohere_fast_workflow_contracts.yaml").read_text())["workflow"]
    children = json.loads((ROOT / "agentic/registries/cohere_fast_subworkflows.yaml").read_text())["subworkflows"]
    domain = yaml.safe_load((ROOT / "agentic/registries/domain_skill_bundles.yaml").read_text())["bundles"][0]
    common = {
        "workflow_version": parent["version"], "activation": parent["activation"],
        "key_function": "workflow_governance", "reasoning_types": ["workflow_composition", "abductive", "evidence_assessment"],
        "problem_domain_types": ["agentic_control_plane"], "task_context_types": ["workflow_governance"],
        "deterministic_hooks": ["cohere-fast-intake", "cohere-fast-policy"],
        "workflow_references": ["cohere-fast-contract-registry"],
        "artifacts": ["agentic/registries/cohere_fast_workflow_contracts.yaml", "agentic/registries/domain_skill_bundles.yaml"],
        "validators": ["agentic/scripts/validate_cohere_fast_release.py"],
    }
    workflows = [{**common, "name": "cohere_fast", "workflow_id": "cohere_fast", "domain_id": "ym",
                  "end_to_end_function": "Run an explicitly activated, isolated, domain-bound research lifecycle.",
                  "composed_skills": [parent["owner_skill"]]}]
    for child in children:
        workflows.append({**common, "name": f"cohere_fast:{child['id']}", "workflow_id": f"cohere_fast:{child['id']}",
                          "parent_workflow": "cohere_fast", "domain_id": "ym", "subworkflow_id": child["id"],
                          "end_to_end_function": f"Transform {child['input_type']} into {child['return_type']} under the cohere-fast isolation contract.",
                          # Domain skills remain private implementation details of the
                          # bundle registry; task discovery exposes only the public
                          # control-plane skill.
                          "composed_skills": [parent["owner_skill"]]})
    return {"task_id": "cohere-fast", "title": "Isolated cohere-fast domain workflow", "status": "disabled",
            "visible_workflows": workflows,
            "reference_skills": [{
                "name": parent["owner_skill"],
                "source": "local",
                "path": f"skills/cohere_fast/{parent['owner_skill']}/SKILL.md",
                "why": "Public explicit-only control skill; domain skills stay private to their bundle.",
            }],
            # Bind existing isolation hooks without inventing new activation routes.
            "reference_hooks": [
                {"name": "cohere-fast-intake", "source": "local", "path": "hooks/scripts/cohere_fast_intake.py", "why": "Parse only explicit domain-bound cohere-fast activation."},
                {"name": "cohere-fast-policy", "source": "local", "path": "hooks/scripts/cohere_fast_policy.py", "why": "Enforce existing domain, lineage and namespace authorization."},
            ],
            "reference_workflows": [{"name": "cohere-fast-contract-registry", "source": "local", "path": "agentic/registries/cohere_fast_workflow_contracts.yaml", "why": "Canonical isolated workflow contract."}],
            "generated_skills": [], "generated_hooks": [], "generated_workflows": []}


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--check", action="store_true"); args = parser.parse_args()
    rendered = json.dumps(build(), indent=2, sort_keys=True) + "\n"
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text() != rendered: raise SystemExit("stale cohere-fast task projection")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True); OUTPUT.write_text(rendered)
    print("cohere-fast task projection is current" if args.check else OUTPUT)
    return 0
if __name__ == "__main__": raise SystemExit(main())

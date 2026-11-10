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

"""Project named-workflow contracts into an optional task catalog.

The contract registry owns workflow identity, ordering, skill membership, and
hook bindings. This projection exists for explicit discovery and compatibility,
outside the native hook's task scan;
it must never become a second hand-maintained source of orchestration truth.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from agentic_common import ROOT, load_json_object, write_json


CONTRACTS = ROOT / "agentic/registries/named_workflow_contracts.yaml"
SKILLS = ROOT / "agentic/registries/skill_registry.yaml"
# Optional projections must stay outside registry/tasks: the original native
# pre-skill hook scans that directory to determine its allowed skill set.
OUTPUT = ROOT / "registry/optional-tasks/named-skill-workflows/task_registry.json"

OPTIONAL_HOOK_MODULES = {
    "named-workflow-router": "user_prompt_submit_intake",
    "workflow-membership-policy": "pre_skill_use_policy",
    "workflow-tool-policy": "pre_tool_use_policy",
    "typed-output-policy": "post_skill_use_review",
    "workflow-exit-policy": "stop_artifact_check",
}

FUNCTIONS = {
    "evidence_to_proof_route_onramp": "Turn sourced mathematical evidence into normalized, target-grounded, adversarially audited proof routes.",
    "conceptual_frontier_deepening": "Run bounded theory-first conceptual invention and return ancestry-bound ready-or-not-ready formal claims.",
    "theorem_proof_delivery": "Turn an exact theorem-shaped queue item into a quality-gated proof, obstruction, repair obligation, or no-go result.",
    "scientific_contribution_cultivation": "Assess whether a result is independently valuable and genuinely enables the larger scientific target.",
    "manuscript_result_elaboration": "Expand scoped result obligations into validated manuscript insertions without reopening discovery.",
    "deep_review_and_reorientation": "Convert evidence-backed multi-perspective review into a governed repair, pivot, quarantine, or stop decision.",
}


def workflow_skills(workflow: dict[str, Any]) -> list[str]:
    """Return stable, de-duplicated base and profile skill membership."""

    names = [str(workflow["owner_skill"])]
    names.extend(str(step["skill"]) for step in workflow.get("steps", []))
    for profile in workflow.get("profiles", []):
        names.extend(str(step["skill"]) for step in profile.get("steps", []))
        names.extend(str(skill) for skill in profile.get("specialist_skills", []))
    return list(dict.fromkeys(names))


def build_manifest() -> dict[str, Any]:
    contracts = load_json_object(CONTRACTS).get("workflows", [])
    skill_rows = load_json_object(SKILLS).get("skills", [])
    skill_paths = {str(row["name"]): str(row["path"]) for row in skill_rows}
    used_skills = sorted(
        {
            skill
            for workflow in contracts
            for skill in workflow_skills(workflow)
        }
    )
    hook_ids = sorted(
        {
            str(hook["hook_id"])
            for workflow in contracts
            for hook in workflow.get("hooks", [])
        }
    )
    workflows = []
    for contract in contracts:
        workflow_id = str(contract["id"])
        workflows.append(
            {
                "name": workflow_id,
                "workflow_id": workflow_id,
                "workflow_version": contract["version"],
                "activation": contract["activation"],
                "end_to_end_function": FUNCTIONS[workflow_id],
                "key_function": "workflow_governance",
                "reasoning_types": [
                    "workflow_composition",
                    "generative_reasoning",
                    "deterministic_validation",
                    "evidence_assessment",
                ],
                "problem_domain_types": [
                    "theorem_discovery",
                    "agentic_control_plane",
                ],
                "task_context_types": [
                    "workflow_governance",
                    "target_navigation",
                ],
                "composed_skills": [
                    *workflow_skills(contract),
                ],
                "deterministic_hooks": [
                    str(hook["hook_id"]) for hook in contract.get("hooks", [])
                ],
                "workflow_references": ["workflow-contract-registry"],
                "artifacts": [
                    "agentic/registries/named_workflow_contracts.yaml",
                    "agentic/registries/skill_workflow_dispositions.yaml",
                    "agentic/spec/named_workflow_contract.schema.json",
                    "agentic/spec/named_workflow_artifacts.schema.json",
                ],
                "validators": [
                    "agentic/scripts/validate_workflow_contracts.py",
                    "agentic/scripts/validate_task_skill_registry.py",
                    "agentic/scripts/validate_skill_integration.py",
                ],
            }
        )
    return {
        "task_id": "named-skill-workflows",
        "title": "Explicit opt-in and conditional skill workflows",
        "status": "active",
        "visible_workflows": workflows,
        "reference_skills": [
            {
                "name": name,
                "source": "local",
                "path": skill_paths[name],
                "why": "The canonical named-workflow contract assigns this skill an ordered and typed role.",
            }
            for name in used_skills
        ],
        "reference_hooks": [
            {
                "name": hook_id,
                "source": "local",
                "path": f"hooks/workflow_local/{OPTIONAL_HOOK_MODULES[hook_id]}.py",
                "why": "Explicitly imported optional policy; not registered as a native hook.",
            }
            for hook_id in hook_ids
        ],
        "reference_workflows": [
            {
                "name": "workflow-contract-registry",
                "source": "local",
                "path": "agentic/registries/named_workflow_contracts.yaml",
                "why": "This task manifest is a generated compatibility projection of the canonical contracts.",
            }
        ],
        "generated_skills": [],
        "generated_hooks": [],
        "generated_workflows": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if the checked-in projection is stale.")
    args = parser.parse_args()
    payload = build_manifest()
    rendered = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != rendered:
            raise SystemExit(f"stale named workflow task projection: {OUTPUT.relative_to(ROOT)}")
        print("named workflow task projection is current")
        return 0
    write_json(OUTPUT, payload)
    print(f"wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

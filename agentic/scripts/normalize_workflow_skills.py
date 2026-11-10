#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Project native workflow interfaces without changing their execution authority.

Native registries remain authoritative. This exporter deliberately keeps opaque
control flow inside the native boundary: prose guards, callback execution, and
human review cannot be translated into executable v1 expressions by guessing.
The complete native row and source digests make that boundary inspectable and
allow --check to detect stale projections without invoking any workflow.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
DEST = Path("agentic/reasoning_flows/workflow_skill_v1")
REG = Path("agentic/registries")
HEADER = """# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""

# These are explicit identity decisions, not a classification by punctuation or
# by the occurrence of 'workflow' inside an ordinary skill's name.
LEGACY = {
    "target_navigation_loop": "target_navigation_workflow",
    "discovery_marathon_loop": "discovery_marathon_workflow",
    "abducer_work_loop": "abducer_work_workflow",
    "conceptual_hypothesis_exploration_loop": "conceptual_hypothesis_exploration_workflow",
    "release_promotion_loop": "release_promotion_workflow",
}
NAMED = {
    "evidence_to_proof_route_onramp": "evidence_to_proof_route_onramp_workflow",
    "conceptual_frontier_deepening": "conceptual_frontier_deepening_workflow",
    "theorem_proof_delivery": "theorem_proof_delivery_workflow",
    "scientific_contribution_cultivation": "scientific_contribution_cultivation_workflow",
    "manuscript_result_elaboration": "manuscript_result_elaboration_workflow",
    "deep_review_and_reorientation": "deep_review_and_reorientation_workflow",
}
CHILDREN = {
    "scope-and-ground": "cohere_fast_scope_and_ground_workflow",
    "adaptive-frontier": "cohere_fast_adaptive_frontier_workflow",
    "derivation-and-proof": "cohere_fast_derivation_and_proof_workflow",
    "independent-audit": "cohere_fast_independent_audit_workflow",
    "manuscript-release": "cohere_fast_manuscript_release_workflow",
}
SUPPORT = {
    "proj_skills/framework-paper-orchestrator/SKILL.md": "framework_paper_workflow",
    "proj_skills/project-readme-orchestrator/SKILL.md": "project_readme_workflow",
    "proj_skills/workflow-health-audit-orchestrator/SKILL.md": "workflow_health_audit_workflow",
    "prism_me/prism-spec-orchestrator/SKILL.md": "prism_spec_development_workflow",
    "prism_me/prism-persona-review-orchestrator/SKILL.md": "prism_persona_review_workflow",
}
NATIVE_SKILLS = {
    "skills/orchestration/kb-orchestrator/SKILL.md": "kb_orchestration_workflow",
    "skills/orchestration/proof-strategy-lockin-orchestrator/SKILL.md": "proof_strategy_lockin_workflow",
    "skills/proof_delivery/pvsnp-forcedrows-proof-workflow/SKILL.md": "pvsnp_forcedrows_proof_workflow",
    "skills/results_ellaboration/routea-open-point-orchestrator/SKILL.md": "route_a_open_point_workflow",
    "skills/evaluation/kb-hypothesis-refutation-loop/SKILL.md": "kb_hypothesis_refutation_workflow",
    "skills/evaluation/kb-revision-loop/SKILL.md": "kb_revision_workflow",
    "skills/discovery/kb-discovery-cycle/SKILL.md": "kb_discovery_cycle_workflow",
    "skills/discovery/kb-prove-cycle/SKILL.md": "kb_prove_cycle_workflow",
}
HOOKS = [
    "hooks/workflow_local/hook_utils.py",
    "hooks/workflow_local/user_prompt_submit_intake.py",
    "hooks/workflow_local/pre_skill_use_policy.py",
    "hooks/workflow_local/post_skill_use_review.py",
    "hooks/workflow_local/pre_tool_use_policy.py",
    "hooks/workflow_local/stop_artifact_check.py",
]
GAP = (
    "No workflow-skill/v1 host adapter is supplied. Native skill/hook/CLI "
    "interfaces exist, but payload materialization, guard evidence, execution "
    "effects and receipt translation are not qualified for this format."
)


def load(root: Path, path: Path | str):
    """Read native JSON-compatible YAML without importing runtime code."""
    return yaml.safe_load((root / path).read_text())


def file_type(path: str) -> dict:
    """Payload paths are resolved relative to each exported descriptor."""
    return {"schema": "../../../../" + path, "representation": "value"}


def opaque_type(description: str) -> dict:
    """Retain an unspecified native packet as a draft object, never a receipt."""
    return {
        "schema": {"type": "object", "description": description},
        "representation": "value",
    }


def operation(inputs: dict, outputs: dict, reason: str = GAP) -> dict:
    return {
        "inputs": inputs,
        "outputs": outputs,
        "execution": {"mode": "specification_only", "reason": reason},
    }


def descriptor(
    root,
    canonical,
    native,
    owner,
    source,
    row,
    input_name,
    output_name,
    types,
    extra_sources=(),
    namespace="abducer",
):
    """Model one opaque native interface and preserve its internal source plan.

    The root call is a native workflow boundary, not a fabricated generative
    step. Operations for named steps below are interface declarations only;
    they are not asserted to be an executable v1 composition.
    """
    sources = list(
        dict.fromkeys(
            [
                str(source),
                owner,
                *extra_sources,
                "agentic/registries/skill_registry.yaml",
                "pyproject.toml",
                "uv.lock",
                "prism_me/shared/references/codex-control-stack.md",
            ]
        )
    )
    gaps = [
        GAP,
        "Native control flow remains opaque; coverage is interface_only, not source-equivalence certification.",
    ]
    if any(
        t["schema"].get("description")
        for t in types.values()
        if isinstance(t["schema"], dict)
    ):
        gaps.append(
            "One or more native payloads have no exact JSON Schema; object-only types remain explicitly underspecified."
        )
    return {
        "schema_version": "workflow-skill/v1",
        "namespace": namespace,
        "id": canonical,
        "version": row.get("version", "1.0.0"),
        "kind": "workflow",
        "description": f"Draft interface projection of {native}; native execution and authority remain unchanged.",
        "aliases": list(dict.fromkeys([native, *row.get("aliases", [])])),
        "lifecycle": "draft",
        # No activation is licensed by this export. Native triggers remain in
        # metadata; no prose predicate is silently converted into a boolean.
        "activation": {"mode": "explicit", "prerequisites": []},
        "types": types,
        "inputs": {"request": {"type": input_name}},
        "outputs": {
            "result": {
                "type": output_name,
                "value": {"ref": "steps.native.outputs.result"},
            }
        },
        "operations": {
            "native_workflow": operation(
                {"request": {"type": input_name}}, {"result": {"type": output_name}}
            )
        },
        "flow": {
            "kind": "sequence",
            "steps": [
                {
                    "id": "native",
                    "kind": "call",
                    "operation": "native_workflow",
                    "description": "Opaque native workflow boundary; internal ordering, guards and handoffs are retained in abducer.native_contract.",
                    "arguments": {"request": {"ref": "inputs.request"}},
                    "on_failure": "blocked",
                }
            ],
        },
        "policy": {
            "effects": {
                "filesystem": {"read": ["native_sources", "inputs"], "write": []},
                "network": [],
                "external_write": [],
            },
            "authority": {
                "allowed": ["describe_native_interface"],
                "forbidden": [
                    "execute_scientific_workflow",
                    "approve",
                    "prove",
                    "publish",
                    "promote",
                ],
            },
            "limits": {"wall_time_seconds": 1800, "max_operation_calls": 1},
            "failure": {
                "default": "blocked",
                "retry": {"max_attempts": 1, "retryable_codes": []},
            },
            "resume": {"mode": "none", "require_matching_definition_and_inputs": True},
            "claim_ceiling": "Interface description only; no proof, scientific validity, runtime qualification, promotion or approval.",
        },
        "observability": {
            "receipts": "required",
            "artifact_digests": "sha256",
            "provenance": "required",
            "events": ["workflow_started", "step_failed", "workflow_completed"],
        },
        "provenance": {
            "coverage": "interface_only",
            "sources": [
                {
                    "path": p,
                    "digest": "sha256:"
                    + hashlib.sha256((root / p).read_bytes()).hexdigest(),
                }
                for p in sources
            ],
            "gaps": gaps,
        },
        "extensions": {
            "abducer.owner": {"path": owner},
            "abducer.native_identity": {"id": native},
            "abducer.native_contract": row,
            "abducer.environment": {
                "python": "pyproject.toml",
                "lock": "uv.lock",
                "native_controls": ".codex/config.toml",
                "native_controls_optional": True,
                "control_policy": "prism_me/shared/references/codex-control-stack.md",
            },
            "abducer.execution_boundary": {
                "status": "specification_only",
                "notes": "Source inspection only. Effects above deny native execution until a separately reviewed adapter exists.",
            },
        },
    }


def projections(root: Path) -> dict[Path, dict]:
    """Cover each canonical registry row and each explicitly mapped support lane."""
    skills = {
        s["name"]: s["path"] + "/SKILL.md"
        for s in load(root, REG / "skill_registry.yaml")["skills"]
    }
    # The current YM node registry also references domain-specific skills not
    # present in the global skill registry. Preserve that discovery difference;
    # do not rewrite the global registry or substitute a similarly named skill.
    ym_skills = {
        p.parent.name: str(p.relative_to(root))
        for p in (root / "skills/domain_specific/ym").glob("*/SKILL.md")
    }
    results = {}

    def add(*args, **kwargs):
        d = descriptor(root, *args, **kwargs)
        path = DEST / d["id"] / "workflow.yaml"
        if path in results:
            raise ValueError(f"Duplicate canonical identity: {path}")
        results[path] = d
        return d

    for row in load(root, REG / "workflow_contracts.yaml")["workflows"]:
        add(
            LEGACY[row["id"]],
            row["id"],
            skills[row["owner_skill"]],
            REG / "workflow_contracts.yaml",
            row,
            "NativeRequest",
            "NativeResult",
            {
                "NativeRequest": opaque_type(
                    "Native owner-specific input bundle; not a new execution API."
                ),
                "NativeResult": opaque_type(
                    "Native gate/required-artifact bundle; concrete paths stay in native_contract."
                ),
            },
            [*HOOKS, "agentic/registries/gate_policy.yaml", *row["validators"]],
        )

    named_source = REG / "named_workflow_contracts.yaml"
    envelope = "agentic/spec/named_workflow_artifacts.schema.json"
    for row in load(root, named_source)["workflows"]:

        def named(row, canonical, native, owner):
            names = {row["input_artifact"]["type"], row["exit_gate"]["consumes"]}
            names.update(
                t
                for step in row["steps"]
                for k in ("consumes", "produces")
                for t in step[k]
            )
            types = {t: file_type(envelope) for t in sorted(names)}
            d = add(
                canonical,
                native,
                owner,
                named_source,
                row,
                row["input_artifact"]["type"],
                row["exit_gate"]["consumes"],
                types,
                [*HOOKS, *dict.fromkeys(skills[s["skill"]] for s in row["steps"])],
            )
            d["extensions"]["abducer.step_interfaces"] = {}
            for step in row["steps"]:
                op_id = "step_" + step["id"]
                d["operations"][op_id] = operation(
                    {t: {"type": t} for t in step["consumes"]},
                    {t: {"type": t} for t in step["produces"]},
                    "Native skill exists at "
                    + skills[step["skill"]]
                    + "; no typed v1 adapter. Source guards, role and failure remain in native_contract.",
                )
                d["extensions"]["abducer.step_interfaces"][step["id"]] = op_id
            d["provenance"]["gaps"].append(
                "Named payload schemas validate the common envelope only; nominal artifact payloads and artifact_type discriminators are not refined by that schema."
            )
            d["provenance"]["gaps"].append(
                "Conditional/advisory skips, repeated ReviewFindingSet aggregation, exit obligations and handoff adapters are preserved verbatim, not executable v1 dataflow."
            )
            return d

        named(row, NAMED[row["id"]], row["id"], skills[row["owner_skill"]])
        for profile in row.get("profiles", []):
            if profile["id"] != "route_a":
                raise ValueError("Unmapped named workflow profile: " + profile["id"])
            profile_row = {
                **row,
                **profile,
                "parent_workflow": row["id"],
                "parent_validation_tail": row["steps"],
            }
            profile_row["input_artifact"] = row["input_artifact"]
            named(
                profile_row,
                "route_a_manuscript_attack_workflow",
                "route_a",
                skills["routea-paper-attack-orchestrator"],
            )

    cf_source = REG / "cohere_fast_workflow_contracts.yaml"
    parent = load(root, cf_source)["workflow"]
    children_source = REG / "cohere_fast_subworkflows.yaml"
    children = load(root, children_source)
    cf_owner = skills[parent["owner_skill"]]
    cf_sources = [
        str(children_source),
        "agentic/orchestration/cohere_fast_runner.py",
        "agentic/spec/cohere_fast_isolation_contract.yaml",
    ]
    add(
        "cohere_fast_workflow",
        parent["id"],
        cf_owner,
        cf_source,
        {**parent, "aliases": [parent["public_alias"]], "child_contracts": children},
        "DomainRunRequest",
        "CohereFastRunPacket",
        {
            "DomainRunRequest": file_type(
                "agentic/spec/cohere_fast_artifacts.schema.json#/$defs/DomainRunRequest"
            ),
            "CohereFastRunPacket": opaque_type(
                "Registry return type lacks an exact schema; runner returns a run summary, not a step receipt."
            ),
        },
        cf_sources,
    )
    for row in children["subworkflows"]:
        add(
            CHILDREN[row["id"]],
            "cohere_fast/" + row["id"],
            cf_owner,
            children_source,
            row,
            row["input_type"],
            row["return_type"],
            {
                t: file_type(
                    "agentic/spec/cohere_fast_artifacts.schema.json#/$defs/DomainRunRequest"
                )
                if t == "DomainRunRequest"
                else opaque_type(
                    "Native stage type "
                    + t
                    + " is declared in the registry but has no exact schema."
                )
                for t in (row["input_type"], row["return_type"])
            },
            cf_sources,
        )
    ym_source = REG / "cohere_fast_ym_workflow.yaml"
    ym = load(root, ym_source)
    add(
        "cohere_fast_ym_workflow",
        "cohere_fast:ym",
        cf_owner,
        ym_source,
        ym,
        "DomainEvidencePacket",
        "DomainEvidencePacket",
        {
            "DomainEvidencePacket": file_type(
                "agentic/spec/cohere_fast_artifacts.schema.json#/$defs/DomainEvidencePacket"
            )
        },
        [*cf_sources, *dict.fromkeys(ym_skills[n["skill"]] for n in ym["nodes"])],
    )

    for owner, canonical in {**SUPPORT, **NATIVE_SKILLS}.items():
        text = (root / owner).read_text()
        native = yaml.safe_load(text.split("---", 2)[1])["name"]
        add(
            canonical,
            native,
            owner,
            owner,
            {"source_skill": owner, "source_text": text},
            "NativeRequest",
            "NativeResult",
            {
                "NativeRequest": opaque_type(
                    "Skill-defined request; consult preserved source text for inputs and conditions."
                ),
                "NativeResult": opaque_type(
                    "Skill-defined durable artifact bundle; no invented runtime output shape."
                ),
            },
            namespace=(
                "prism_me"
                if owner.startswith("prism_me/")
                else "abducer_support"
                if owner.startswith("proj_skills/")
                else "abducer"
            ),
            extra_sources=[
                str(p.relative_to(root))
                for folder in ("references", "scripts")
                for p in sorted((root / owner).parent.joinpath(folder).rglob("*"))
                if p.is_file() and p.suffix in {".py", ".md", ".yaml", ".json"}
            ],
        )

    for native, canonical, impl, owner in [
        (
            "timeline-paper-independent-workflow",
            "timeline_paper_independent_workflow",
            "agentic/scripts/run_timeline_paper_workflow.py",
            skills["timeline-paper-workflow-orchestrator"],
        ),
        (
            "ym-representational-dynamics-overlay",
            "ym_representational_dynamics_workflow",
            "agentic/reasoning_flows/ym-representational-dynamics-overlay.prism",
            ym_skills["ym-draft-representational-dynamics"],
        ),
    ]:
        add(
            canonical,
            native,
            owner,
            impl,
            {
                "source": impl,
                "source_text": (root / impl).read_text(),
                "owner_relation": "native owning skill; source implementation or reasoning lane defines execution",
            },
            "NativeRequest",
            "NativeResult",
            {
                "NativeRequest": opaque_type("Source-defined invocation context."),
                "NativeResult": opaque_type(
                    "Source-defined paper or audit result bundle."
                ),
            },
        )

    return results


class ProjectionDumper(yaml.SafeDumper):
    """Emit JSON-compatible YAML without anchors, including repeated source rows."""

    def ignore_aliases(self, data):
        return True


def rendered(root: Path) -> dict[Path, str]:
    results = projections(root)
    index = {
        "schema_version": "abducer-workflow-skill-index/v1",
        "authority": "generated interface projections; native registries and implementations remain authoritative",
        "generator": "agentic/scripts/normalize_workflow_skills.py",
        "workflows": [
            {
                "namespace": d["namespace"],
                "id": d["id"],
                "version": d["version"],
                "descriptor": str(p),
                "owner": d["extensions"]["abducer.owner"]["path"],
                "aliases": d["aliases"],
            }
            for p, d in results.items()
        ],
        "classification": {
            "included": "Five legacy loops, six named workflows, Route A profile, cohere-fast parent/five children/YM specialization, two remaining reasoning-flow lanes, eight explicitly mapped standalone native orchestrators/loops/cycles, three project orchestrators, two Prism orchestrators.",
            "ordinary_skills": "Native component and diagnostic skills remain ordinary skills unless explicitly mapped here. A workflow name substring is not a classification rule.",
            "excluded": "Generated plugin mirrors, generated reports/graphs, historical .prism requests, copied PRISM packages, external vendor trees, test fixtures and reasoning maps are not independent canonical workflow definitions.",
        },
    }
    results[DEST / "index.yaml"] = index
    output = {
        p: HEADER
        + "# REUSE-IgnoreStart\n"
        + yaml.dump(
            d, Dumper=ProjectionDumper, sort_keys=False, allow_unicode=True, width=100
        )
        + "# REUSE-IgnoreEnd\n"
        for p, d in results.items()
    }
    mapping = [
        "<!--\n"
        + "\n".join(
            line.removeprefix("# ").removeprefix("#") for line in HEADER.splitlines()
        )
        + "\n-->",
        "# Source-to-interface map",
        "",
        "Generated by `agentic/scripts/normalize_workflow_skills.py`; do not edit independently.",
        "",
        "Each root `native` call is an opaque native workflow interface. Native internal steps below",
        "are preserved as metadata and (for named workflows) operation signatures, not executable v1 flow.",
        "",
        "| Canonical workflow | Native identity | Owner | Source |",
        "| --- | --- | --- | --- |",
    ]
    for p, d in results.items():
        if p.name != "workflow.yaml":
            continue
        native = d["extensions"]["abducer.native_identity"]["id"]
        owner = d["extensions"]["abducer.owner"]["path"]
        source = d["provenance"]["sources"][0]["path"]
        mapping.append(
            f"| [{d['id']}]({d['id']}/workflow.yaml) | `{native}` | `{owner}` | `{source}` |"
        )
    for p, d in results.items():
        if p.name != "workflow.yaml":
            continue
        row = d["extensions"]["abducer.native_contract"]
        steps = row.get(
            "steps",
            row.get("nodes", row.get("child_contracts", {}).get("subworkflows", [])),
        )
        if not steps:
            continue
        mapping.extend(
            [
                "",
                f"## {d['id']}",
                "",
                "| Native step | Normalized interface | Role / guard | Failure |",
                "| --- | --- | --- | --- |",
            ]
        )
        for step in steps:
            op = (
                d["extensions"]
                .get("abducer.step_interfaces", {})
                .get(step["id"], "inside opaque native boundary")
            )
            role = step.get("mode", step.get("disposition", "native"))
            guard = str(step.get("when") or "none declared").replace("|", "\\|")
            mapping.append(
                f"| `{step['id']}` | `{op}` | {role}; `{guard}` | `{step.get('on_failure', 'native')}` |"
            )
    mapping.extend(
        [
            "",
            "Remaining gaps: native-only guards and aggregation, specialist dispatch and validation tails,",
            "handoff adapters, exact payload schemas, host effect enforcement and runtime qualification.",
            "Read each descriptor's `provenance.gaps` and the adjacent README before attempting adoption.",
            "",
        ]
    )
    output[DEST / "SOURCE_MAP.md"] = "\n".join(mapping)
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=ROOT)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Read-only drift check; never execute native bindings.",
    )
    args = parser.parse_args()
    root = args.repository_root.resolve()
    expected = rendered(root)
    stale = [
        str(p)
        for p, content in expected.items()
        if not (root / p).is_file() or (root / p).read_text() != content
    ]
    extras = set((root / DEST).glob("*/workflow.yaml")) - {root / p for p in expected}
    if args.check:
        if stale or extras:
            print(
                json.dumps(
                    {
                        "stale_or_missing": stale,
                        "unexpected": sorted(str(p.relative_to(root)) for p in extras),
                    },
                    indent=2,
                )
            )
            return 1
        print(
            f"{len(expected) - 2} workflow interfaces are current; native execution unchanged"
        )
        return 0
    if extras:
        raise ValueError(
            "Unexpected descriptors require explicit reconciliation; refusing to delete them"
        )
    for path, content in expected.items():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text(content)
    print(
        f"Wrote {len(expected) - 2} draft interface descriptors, ownership index and source map"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

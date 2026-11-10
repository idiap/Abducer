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
"""Shared helpers for long-horizon discovery marathons.

The legacy marathon predates executable discovery-operator receipts.  This
module therefore treats its historical reports as readable projections while
requiring new dispatch claims to be reconstructed from verified receipts.  A
skill name in a prompt or old trace is never execution evidence by itself.
"""

from __future__ import annotations

import json
import html as html_lib
import re
from pathlib import Path
from typing import Any, Mapping, Sequence

from agentic_common import ROOT, clean_text, fail, load_json_object, load_optional_json, rel, slugify, stable_id, utc_now, write_json
from agentic.discovery.contracts import ContractError, validate_instance
from agentic.discovery.theory_gate import authorization_is_runtime_verified
from target_profiles import default_discovery_programs, target_profile


MARATHON_ROOT = ROOT / "agentic/runs/discovery_marathons"
ACTIVE_POINTER = MARATHON_ROOT / "active_run.json"
TARGET_ACTIVE_DIR = MARATHON_ROOT / "active_targets"
STRETCH_REPORT = ROOT / "agentic/reports/discovery_stretch/latest.json"
DISPATCH_MATRIX = ROOT / "agentic/registries/discovery_marathon_skill_dispatch.yaml"
REPORT_DIR = ROOT / "agentic/reports/discovery_marathon"
LATEST_JSON = REPORT_DIR / "latest.json"
LATEST_MD = REPORT_DIR / "latest.md"
LATEST_HTML = REPORT_DIR / "latest.html"
LATEST_TIMELINE_HTML = REPORT_DIR / "full_timeline.html"
SMOKE_MD = REPORT_DIR / "smoke_yang_mills.md"
TARGET_REPORT_ROOT = REPORT_DIR / "targets"
MARATHON_DATA_RE = re.compile(
    r'<script id="marathon-data" type="application/json">(.*?)</script>',
    re.DOTALL,
)
TARGET_META_RE = re.compile(r'<meta name="abducer-target-id" content="([^"]+)">')
TARGET_MD_RE = re.compile(r"^Target:\s*`([^`]+)`", re.MULTILINE)


def load_dispatch_matrix() -> dict[str, Any]:
    return load_json_object(DISPATCH_MATRIX)


def phase_applies(phase: Mapping[str, Any], target_id: str) -> bool:
    """Return whether one registry phase belongs to the exact target.

    Unscoped phases are shared.  A scoped phase is never inferred from domain,
    title, or a global active run: its declared target ID must match exactly.
    Supporting a list keeps the helper reusable without weakening that rule.
    """

    scope = phase.get("target_scope")
    if scope is None:
        return True
    if isinstance(scope, str):
        return bool(clean_text(target_id)) and clean_text(scope) == clean_text(target_id)
    if isinstance(scope, list):
        scopes = {clean_text(value) for value in scope if clean_text(value)}
        return bool(clean_text(target_id)) and clean_text(target_id) in scopes
    return False


def run_dir(run_id: str) -> Path:
    return MARATHON_ROOT / slugify(run_id)


def target_active_pointer_path(target_id: str) -> Path:
    return TARGET_ACTIVE_DIR / f"{slugify(target_id)}.json"


def target_report_dir(target_id: str) -> Path:
    return TARGET_REPORT_ROOT / slugify(target_id)


def target_latest_json(target_id: str) -> Path:
    return target_report_dir(target_id) / "latest.json"


def target_latest_md(target_id: str) -> Path:
    return target_report_dir(target_id) / "latest.md"


def target_latest_html(target_id: str) -> Path:
    return target_report_dir(target_id) / "latest.html"


def target_timeline_html(target_id: str) -> Path:
    return target_report_dir(target_id) / "full_timeline.html"


def target_report_paths(target_id: str) -> dict[str, Path]:
    return {
        "dir": target_report_dir(target_id),
        "latest_json": target_latest_json(target_id),
        "latest_md": target_latest_md(target_id),
        "latest_html": target_latest_html(target_id),
        "full_timeline_html": target_timeline_html(target_id),
    }


def read_report_target_id(path: Path) -> str:
    if not path.exists():
        return ""
    if path.suffix == ".json":
        return clean_text(load_optional_json(path).get("target_id"))
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        match = TARGET_MD_RE.search(text)
        return clean_text(match.group(1)) if match else ""
    meta_match = TARGET_META_RE.search(text[:2000])
    if meta_match:
        return clean_text(meta_match.group(1))
    data_match = MARATHON_DATA_RE.search(text)
    if not data_match:
        return ""
    try:
        payload = json.loads(html_lib.unescape(data_match.group(1)))
    except json.JSONDecodeError:
        return ""
    return clean_text(payload.get("report", {}).get("target_id"))


def generic_report_path_writable(path: Path, target_id: str) -> bool:
    existing_target = read_report_target_id(path)
    return not existing_target or existing_target == clean_text(target_id)


def require_report_target(path: Path, target_id: str) -> None:
    existing_target = read_report_target_id(path)
    if existing_target != clean_text(target_id):
        fail(f"{rel(path)} is scoped to `{existing_target or 'unknown'}`, expected `{target_id}`")


def branch_path(run_id: str, branch_id: str) -> Path:
    return run_dir(run_id) / "branches" / f"{slugify(branch_id)}.json"


def cycle_path(run_id: str, cycle_id: str) -> Path:
    return run_dir(run_id) / "cycles" / f"{slugify(cycle_id)}.json"


def review_path(run_id: str, review_id: str) -> Path:
    return run_dir(run_id) / "reviews" / f"{slugify(review_id)}.json"


def load_active_pointer() -> dict[str, Any]:
    return load_optional_json(ACTIVE_POINTER)


def load_run_state(run_id: str | None = None, target_id: str | None = None) -> tuple[Path, dict[str, Any]]:
    if run_id:
        selected = run_id
    elif target_id:
        pointer = load_optional_json(target_active_pointer_path(target_id))
        selected = pointer.get("run_id")
    else:
        pointer = load_active_pointer()
        selected = pointer.get("run_id")
    if not selected:
        return MARATHON_ROOT, {}
    path = run_dir(selected) / "run_state.json"
    if not path.exists():
        return path, {}
    return path, load_json_object(path)


def write_active_run_pointers(run_state: dict[str, Any]) -> None:
    pointer = {
        "run_id": run_state["run_id"],
        "target_id": run_state.get("target_id", ""),
        "path": rel(run_dir(run_state["run_id"]) / "run_state.json"),
        "status": run_state["status"],
        "updated_utc": run_state["updated_utc"],
    }
    write_json(ACTIVE_POINTER, pointer)
    target_id = clean_text(run_state.get("target_id"))
    if target_id:
        write_json(target_active_pointer_path(target_id), pointer)


def load_branches(run_state: dict[str, Any]) -> list[dict[str, Any]]:
    branches = []
    profile = target_profile(run_state.get("target_id"))
    for row in run_state.get("branch_registry", []):
        if not isinstance(row, dict):
            continue
        path = ROOT / row.get("local_memory_path", "")
        if path.exists():
            branch = load_json_object(path)
            branch.setdefault(
                "target_profile",
                {
                    "slug": profile["slug"],
                    "display_name": profile["display_name"],
                    "domain": profile["domain"],
                    "strategy_tab_label": profile["strategy_tab_label"],
                    "story_tab_label": profile["story_tab_label"],
                },
            )
            branches.append(branch)
    return branches


def load_cycles(run_state: dict[str, Any]) -> list[dict[str, Any]]:
    root = run_dir(run_state["run_id"]) / "cycles"
    if not root.exists():
        return []
    return [load_json_object(path) for path in sorted(root.glob("*.json"))]


def load_reviews(run_state: dict[str, Any]) -> list[dict[str, Any]]:
    root = run_dir(run_state["run_id"]) / "reviews"
    if not root.exists():
        return []
    return [load_json_object(path) for path in sorted(root.glob("*.json"))]


def stretch_programs(target_id: str | None = None) -> list[dict[str, Any]]:
    report = load_optional_json(STRETCH_REPORT)
    if target_id and clean_text(report.get("target_id")) and clean_text(report.get("target_id")) != clean_text(target_id):
        return default_discovery_programs(target_id)
    programs = report.get("programs", [])
    rows = [row for row in programs if isinstance(row, dict)]
    return rows or default_discovery_programs(target_id)


def default_branch(program: dict[str, Any], run_id: str, target_id: str, priority: int) -> dict[str, Any]:
    profile = target_profile(target_id)
    title = clean_text(program.get("title") or program.get("program_id") or f"Discovery branch {priority}")
    branch_id = stable_id("marathon.branch", target_id, title)
    local_memory_path = rel(branch_path(run_id, branch_id))
    return {
        "branch_id": branch_id,
        "run_id": run_id,
        "target_id": target_id,
        "target_profile": {
            "slug": profile["slug"],
            "display_name": profile["display_name"],
            "domain": profile["domain"],
            "strategy_tab_label": profile["strategy_tab_label"],
            "story_tab_label": profile["story_tab_label"],
        },
        "title": title,
        "status": "active" if priority <= 3 else "watch",
        "priority": priority,
        "machinery_role": clean_text(program.get("machinery_role") or "bridge"),
        "controlled_interface": clean_text(program.get("controlled_interface") or "target object -> proof obligation"),
        "hypothesis": clean_text(program.get("hypothesis") or "A typed bridge lemma can turn this program into proof-relevant learning."),
        "mathematical_mechanism": clean_text(program.get("mathematical_mechanism") or "Generate definitions, assumptions, equations, and falsifiers for the controlled interface."),
        "dependencies": program.get("dependencies", []),
        "falsifiers": program.get("falsifiers", []),
        "equations": program.get("equations", []),
        "skill_requirements": [
            "kb-abduce",
            "kb-deduce",
            "kb-induce",
            "literature-gap-relevance-auditor",
            "mathematical-concept-gap-revisitor",
            "abstraction-fit-gap-auditor",
            "efficient-representation-requirements-elicitor",
            "kb-contradiction-strategist",
            "entailment-gap-auditor",
            "abducer-obligation-gatekeeper",
            "proof-depth-pressure-formalizer",
            "proof-hard-gate-selector",
            "proof-nontriviality-auditor",
            "proof-conceptual-quality-heuristic-rater",
            "proof-transfer-substance-auditor",
            "proof-depth-release-gate",
            "failure-archaeology-explainer",
            "failed-hypothesis-anticipator",
            "visual-theorem-conceptualizer",
            "visual-analogy-preservation-auditor",
        ],
        "attempt_count": 0,
        "consecutive_low_learning_cycles": 0,
        "last_new_learning_utc": "",
        "promotion_signal": clean_text(program.get("promotion_signal") or "A same-theory bridge lemma is stated with checkable assumptions."),
        "pivot_signal": clean_text(program.get("pivot_signal") or "Repeated attempts cannot name a target-preserving source or target object."),
        "local_memory_path": local_memory_path,
        "local_memory": [],
    }


def target_specific_advisory_skills(target_id: str, phase: str) -> list[str]:
    """Return historical target helpers without upgrading them to execution gates."""

    if target_id == "yang-mills-existence-and-mass-gap-target":
        extras = {
            "avenue_literature_gap_precheck": [
                "literature-gap-relevance-auditor",
                "physical-relevance-impact-auditor",
            ],
            "yang_mills_representational_dynamics_overlay": ["physical-relevance-impact-auditor"],
            "qualitative_physics_reasoning": ["physical-relevance-impact-auditor"],
            "result_atlas_maintenance": ["physical-relevance-impact-auditor"],
            "failure_archaeology_and_premortem": [
                "failure-archaeology-explainer",
                "failed-hypothesis-anticipator",
                "physical-relevance-impact-auditor",
            ],
            "deep_reflection_visual_conceptualization": [
                "visual-theorem-conceptualizer",
                "visual-analogy-preservation-auditor",
                "physical-relevance-impact-auditor",
            ],
        }
        return extras.get(phase, [])
    if target_id != "p-vs-np-target":
        return []
    extras = {
        "preflight_target_navigation": ["pvsnp-conceptual-pressure-localizer"],
        "branch_selection": ["pvsnp-negative-tactic-selector"],
        "avenue_literature_gap_precheck": [
            "literature-gap-relevance-auditor",
            "pvsnp-conceptual-pressure-localizer",
            "pvsnp-barrier-specificity-reviewer",
        ],
        "branch_exploration": [
            "pvsnp-conceptual-pressure-localizer",
            "pvsnp-pressure-bridge-forger",
            "pvsnp-qualitative-complexity-reasoner",
            "pvsnp-symbolic-complexity-auditor",
        ],
        "inference_quality_review": [
            "pvsnp-inference-quality-controller",
            "pvsnp-reduction-consistency-reviewer",
            "pvsnp-quantifier-uniformity-reviewer",
            "pvsnp-barrier-specificity-reviewer",
            "pvsnp-proof-derivation-builder",
        ],
        "proof_delivery": [
            "pvsnp-forcedrows-proof-workflow",
            "pvsnp-inference-quality-controller",
            "pvsnp-reduction-consistency-reviewer",
            "pvsnp-quantifier-uniformity-reviewer",
            "pvsnp-barrier-specificity-reviewer",
            "pvsnp-proof-complexity-transfer-reviewer",
        ],
        "qualitative_physics_reasoning": ["pvsnp-qualitative-complexity-reasoner", "pvsnp-symbolic-complexity-auditor"],
        "gedanken_experiment_design": [
            "pvsnp-gedanken-complexity-lab",
            "pvsnp-pressure-bridge-forger",
            "pvsnp-qualitative-complexity-reasoner",
        ],
        "contradiction_and_falsifier_generation": [
            "pvsnp-pressure-bridge-forger",
            "pvsnp-negative-tactic-selector",
            "pvsnp-impossibility-theorem-forger",
            "pvsnp-symbolic-complexity-auditor",
        ],
        "obligation_gating": [
            "pvsnp-conceptual-pressure-localizer",
            "pvsnp-pressure-bridge-forger",
            "pvsnp-negative-tactic-selector",
            "pvsnp-impossibility-theorem-forger",
            "pvsnp-symbolic-complexity-auditor",
        ],
        "result_atlas_maintenance": [
            "result-atlas-maintainer",
            "pvsnp-negative-tactic-selector",
            "pvsnp-pressure-bridge-forger",
            "main-problem-alignment-auditor",
        ],
    }
    return extras.get(phase, [])


def target_specific_required_skills(target_id: str, phase: str) -> list[str]:
    """Compatibility hook for executable target-specific requirements.

    The legacy target overlays have no receipt-backed executable requirements;
    their former broad lists are exposed by
    :func:`target_specific_advisory_skills`.  Keeping this empty hook avoids
    silently promoting those self-attested skills back into release gates.
    """

    del target_id, phase
    return []


def build_skill_dispatch_trace(
    cycle_id: str,
    branch_ids: list[str],
    selected_branch_titles: list[str],
    target_id: str = "",
    *,
    run_id: str = "",
    state_version: int | None = None,
    operator_receipts: Sequence[Mapping[str, Any]] = (),
    canonical_theory_gate: Mapping[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Project executable receipts into the legacy phase-oriented trace.

    This function intentionally keeps its historical name because report
    consumers import it, but its authority is fundamentally different from the
    old implementation: ``invoked_skills`` is the intersection of required
    skill IDs and successful, independently validated operator receipts.  A
    failed, malformed, wrong-target, wrong-run, wrong-version, or unrelated
    receipt leaves the skill in ``missing_required_skills``.
    """

    accepted_receipts: list[dict[str, Any]] = []
    rejected_receipts: list[dict[str, str]] = []
    expected_branches = set(branch_ids)
    for raw_receipt in operator_receipts:
        receipt = dict(raw_receipt)
        receipt_id = clean_text(receipt.get("receipt_id")) or "unknown-receipt"
        try:
            validate_instance(receipt, "discovery_operator_receipt.schema.json")
            identity = receipt["identity"]
            if target_id and identity["target_id"] != target_id:
                raise ContractError("target identity mismatch")
            if run_id and identity["run_id"] != run_id:
                raise ContractError("run identity mismatch")
            if expected_branches and identity["branch_id"] not in expected_branches:
                raise ContractError("branch identity was not selected for this cycle")
            if state_version is not None and identity["state_version"] != state_version:
                raise ContractError("receipt is bound to a different state version")
            if receipt["status"] != "succeeded":
                raise ContractError(f"operator status is {receipt['status']}")
            validators = receipt.get("validator_receipts", [])
            if not validators or any(row.get("status") != "passed" for row in validators):
                raise ContractError("independent validator evidence is absent or failed")
        except (ContractError, KeyError, TypeError, ValueError) as exc:
            rejected_receipts.append({"receipt_id": receipt_id, "reason": str(exc)})
            continue
        accepted_receipts.append(receipt)

    receipts_by_operator: dict[str, list[dict[str, Any]]] = {}
    for receipt in accepted_receipts:
        receipts_by_operator.setdefault(receipt["operator"]["operator_id"], []).append(receipt)
    gate_is_verified = authorization_is_runtime_verified(canonical_theory_gate)
    gate = dict(canonical_theory_gate or {})
    gate_bindings = (
        gate.get("operator_bindings", {})
        if gate_is_verified
        and gate.get("status") == "verified_active_current"
        and gate.get("authoritative") is True
        else {}
    )
    if not isinstance(gate_bindings, Mapping):
        gate_bindings = {}

    trace = []
    for phase in load_dispatch_matrix().get("phases", []):
        if not phase_applies(phase, target_id):
            continue
        required = list(dict.fromkeys([*phase.get("required_skills", []), *target_specific_required_skills(target_id, phase["phase"])]))
        advisory = list(
            dict.fromkeys(
                [
                    *phase.get("legacy_advisory_skills", []),
                    *target_specific_advisory_skills(target_id, phase["phase"]),
                ]
            )
        )
        conditional = phase.get("conditional_skills", [])
        invoked = [
            skill
            for skill in required
            if receipts_by_operator.get(skill) or gate_bindings.get(skill)
        ]
        missing = [skill for skill in required if skill not in invoked]
        receipt_bindings = []
        for skill in invoked:
            direct = receipts_by_operator.get(skill, [])
            committed = gate_bindings.get(skill, {})
            receipt_bindings.append(
                {
                    "skill": skill,
                    "receipt_ids": sorted(
                        {
                            *[receipt["receipt_id"] for receipt in direct],
                            *list(committed.get("receipt_ids", [])),
                        }
                    ),
                    "operator_versions": sorted(
                        {receipt["operator"]["version"] for receipt in direct}
                        or {"canonical-cycle-committed/1.0.0"}
                    ),
                    "evidence_kind": (
                        "canonical_feedback_edge"
                        if committed
                        else "direct_operator_receipt"
                    ),
                    "feedback_edge_ids": sorted(committed.get("feedback_edge_ids", [])),
                }
            )
        qualitative_label = (
            "qualitative complexity-theoretic reasoning"
            if target_id == "p-vs-np-target" and phase["phase"] == "qualitative_physics_reasoning"
            else phase["phase"]
        )
        trace.append(
            {
                "cycle_id": cycle_id,
                "target_id": target_id,
                "phase": phase["phase"],
                "trace_authority": (
                    "canonical_cycle_commit_v2"
                    if gate_bindings
                    else "executable_operator_receipts_v1"
                ),
                "dispatch_status": "certified" if not missing else "blocked_missing_receipts",
                "invoked_skills": invoked,
                "legacy_advisory_skills": advisory,
                "skipped_skills_with_reason": [],
                "receipt_bindings": receipt_bindings,
                "queued_conditional_skills": [
                    {
                        "skill": skill,
                        "reason": "Queued only if the branch output exposes the corresponding proof, evidence, or writing obligation.",
                    }
                    for skill in conditional
                ],
                "missing_required_skills": missing,
                "blocked_skills_with_reason": [
                    {
                        "skill": skill,
                        "reason": "No successful identity-matching executable operator receipt names this required skill.",
                    }
                    for skill in missing
                ],
                "rejected_receipts": rejected_receipts,
                "canonical_authorization_basis_digest": (
                    gate.get("authorization_basis_digest") if gate_bindings else None
                ),
                "canonical_present_investment_decision_digest": (
                    gate.get("present_investment_decision_digest")
                    if gate_bindings
                    else None
                ),
                "canonical_operator_evidence_digest": (
                    gate.get("operator_evidence_digest") if gate_bindings else None
                ),
                "canonical_commit_id": gate.get("commit_id") if gate_bindings else None,
                "input_artifacts": [
                    "agentic/state/current_target.json",
                    "agentic/reports/discovery_stretch/latest.json",
                    "agentic/registries/discovery_marathon_skill_dispatch.yaml",
                ],
                "output_artifacts": [f"cycle:{cycle_id}", *[f"branch:{branch_id}" for branch_id in branch_ids]],
                "validation_handoff": (
                    f"{qualitative_label} has receipt evidence for {len(invoked)} of {len(required)} required skills "
                    f"while exploring {', '.join(selected_branch_titles)}; {len(advisory)} historical skills are advisory, "
                    "and unreceipted executable requirements remain blocked."
                ),
            }
        )
    return trace


def markdown_list(items: list[Any]) -> str:
    if not items:
        return "- None.\n"
    return "".join(f"- {clean_text(item)}\n" for item in items)


def write_markdown(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def dump_stdout(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))

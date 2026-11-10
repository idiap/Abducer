#!/usr/bin/env python3
"""Validate legacy readability and receipt-backed dispatch separately.

Historical cycles contain self-attested skill lists.  They remain renderable,
but this validator never upgrades those lists into certified execution.  New
traces must bind every claimed invocation to executable operator receipt IDs;
callers can request the stricter release gate with ``--require-certified``.
"""

from __future__ import annotations

import argparse
import contextlib
import io
from pathlib import Path
from typing import Any, Mapping

from agentic_common import ROOT, clean_text, fail, load_json_object, rel
from agentic.discovery.theory_gate import authorization_is_runtime_verified
from discovery_marathon_common import (
    load_cycles,
    load_dispatch_matrix,
    load_run_state,
    phase_applies,
    target_specific_advisory_skills,
    target_specific_required_skills,
)


OPTIONAL_HISTORICAL_PHASES = {"result_atlas_maintenance", "definition_assumption_elicitation", "inference_quality_review"}
PHASE_INTRODUCED_CYCLE = {
    "proof_delivery": 258,
    "proof_depth_control": 258,
    "conceptual_abstraction_revision": 261,
    "avenue_literature_gap_precheck": 352,
    "failure_archaeology_and_premortem": 352,
    "deep_reflection_visual_conceptualization": 352,
}
REQUIRED_SKILL_INTRODUCED_CYCLE = {
    "literature-gap-relevance-auditor": 352,
    "physical-relevance-impact-auditor": 352,
    "failure-archaeology-explainer": 352,
    "failed-hypothesis-anticipator": 352,
    "visual-theorem-conceptualizer": 352,
    "visual-analogy-preservation-auditor": 352,
}
CANONICAL_THEORY_PHASES = (
    "current_literature_assimilation_rebase",
    "high_risk_intuition_generation",
    "parallel_hypothesis_maturation",
    "reflective_parent_synthesis",
)
THEORY_FIRST_INTRODUCED_PHASES = {
    *CANONICAL_THEORY_PHASES,
    "theory_requested_symbolic_simulation_support",
}
MODERN_TRACE_AUTHORITIES = {
    "executable_operator_receipts_v1",
    "canonical_cycle_commit_v1",
    "canonical_cycle_commit_v2",
}


def validate_dispatch_matrix(matrix: dict[str, Any]) -> None:
    """Validate the theory-first order and the advisory/release boundary."""

    phases = matrix.get("phases", [])
    if not isinstance(phases, list) or not phases:
        fail("discovery marathon dispatch matrix needs a non-empty phases list")
    phase_ids = [clean_text(row.get("phase")) for row in phases if isinstance(row, dict)]
    if len(phase_ids) != len(phases) or any(not value for value in phase_ids):
        fail("discovery marathon dispatch matrix has a malformed phase")
    if len(phase_ids) != len(set(phase_ids)):
        fail("discovery marathon dispatch matrix has duplicate phase IDs")
    expected_prefix = list(CANONICAL_THEORY_PHASES)
    required_phase_ids = {
        *expected_prefix,
        "branch_selection",
        "theory_requested_symbolic_simulation_support",
    }
    missing_phase_ids = required_phase_ids - set(phase_ids)
    if missing_phase_ids:
        fail(f"discovery marathon dispatch matrix is missing phases: {sorted(missing_phase_ids)}")
    indices = [phase_ids.index(phase_id) for phase_id in expected_prefix]
    if indices != sorted(indices) or max(indices) >= phase_ids.index("branch_selection"):
        fail("canonical literature, intuition, parallel, and reflection phases must precede branch_selection")
    support_index = phase_ids.index("theory_requested_symbolic_simulation_support")
    if support_index <= phase_ids.index("reflective_parent_synthesis"):
        fail("theory-requested experiment support must follow reflective synthesis")

    expected_requirements = {
        "current_literature_assimilation_rebase": ["frontier-literature-assimilator"],
        "high_risk_intuition_generation": ["high-risk-hypothesis-forger"],
        "parallel_hypothesis_maturation": ["parallel-hypothesis-portfolio"],
        "reflective_parent_synthesis": [
            "reflective-conceptual-discovery",
            "reflective-theory-synthesizer",
            "blind-conceptual-preference-adjudicator",
        ],
    }
    for phase in phases:
        phase_id = phase["phase"]
        required = phase.get("required_skills", [])
        advisory = phase.get("legacy_advisory_skills", [])
        conditional = phase.get("conditional_skills", [])
        if not all(isinstance(values, list) for values in (required, advisory, conditional)):
            fail(f"dispatch phase {phase_id} skill fields must be lists")
        if set(required) & (set(advisory) | set(conditional)):
            fail(f"dispatch phase {phase_id} mixes required and advisory/conditional skills")
        if phase_id in expected_requirements:
            if required != expected_requirements[phase_id]:
                fail(f"dispatch phase {phase_id} has the wrong executable operator requirements")
        elif required:
            fail(f"legacy dispatch phase {phase_id} must keep broad skills advisory/conditional")
        scope = phase.get("target_scope")
        if scope is not None and not (
            (isinstance(scope, str) and clean_text(scope))
            or (isinstance(scope, list) and scope and all(clean_text(value) for value in scope))
        ):
            fail(f"dispatch phase {phase_id} has an invalid target_scope")
    branch_selection = phases[phase_ids.index("branch_selection")]
    if "next-experiment-queue-ranker" in branch_selection.get("required_skills", []):
        fail("next-experiment-queue-ranker cannot gate pre-theory branch selection")
    support = phases[support_index]
    if "dynamic-symbolic-simulation-experimenter" not in support.get("conditional_skills", []):
        fail("dynamic experiment support must remain conditional after reflection")


def source_cycle_number(source: Path) -> int:
    stem = source.stem
    if stem.startswith("cycle-"):
        try:
            return int(stem.split("-")[-1])
        except ValueError:
            return 0
    return 0


def validate_trace(
    trace: list[Any], source: Path, *, require_certified: bool = False,
    verified_gate: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate trace honesty and return an explicit certification summary."""

    if not isinstance(trace, list) or not trace:
        fail(f"{rel(source)} skill_dispatch_trace must be a non-empty list")
    matrix = load_dispatch_matrix()
    validate_dispatch_matrix(matrix)
    by_phase = {row.get("phase"): row for row in trace if isinstance(row, dict)}
    if len(by_phase) != len(trace):
        fail(f"{rel(source)} dispatch phases are malformed or duplicated")
    known_phase_ids = {phase["phase"] for phase in matrix.get("phases", [])}
    unknown = set(by_phase) - known_phase_ids
    if unknown:
        fail(f"{rel(source)} has unknown dispatch phases: {sorted(unknown)}")
    target_ids = {
        clean_text(row.get("target_id"))
        for row in trace
        if isinstance(row, dict) and clean_text(row.get("target_id"))
    }
    if len(target_ids) > 1:
        fail(f"{rel(source)} dispatch rows cross target identities: {sorted(target_ids)}")
    trace_target_id = next(iter(target_ids), "")
    modern_trace = any(
        clean_text(row.get("trace_authority")) in MODERN_TRACE_AUTHORITIES
        for row in trace
        if isinstance(row, dict)
    )
    if not trace_target_id and not modern_trace:
        # Historical rows predate row-level target IDs.  A single included
        # target-scoped phase is sufficient for readability-only inference;
        # modern/release traces never receive this compatibility allowance.
        inferred_scopes = {
            clean_text(phase.get("target_scope"))
            for phase in matrix.get("phases", [])
            if phase["phase"] in by_phase
            and isinstance(phase.get("target_scope"), str)
            and clean_text(phase.get("target_scope"))
        }
        if len(inferred_scopes) == 1:
            trace_target_id = next(iter(inferred_scopes))
    if modern_trace and not trace_target_id:
        fail(f"{rel(source)} modern dispatch trace needs an exact target_id")
    non_applicable = {
        phase["phase"]
        for phase in matrix.get("phases", [])
        if not phase_applies(phase, trace_target_id) and phase["phase"] in by_phase
    }
    if non_applicable:
        fail(f"{rel(source)} contains target-inapplicable dispatch phases: {sorted(non_applicable)}")
    legacy_phases: list[str] = []
    blocked_phases: list[str] = []
    certified_phases: list[str] = []
    for phase in matrix.get("phases", []):
        if not phase_applies(phase, trace_target_id):
            continue
        phase_id = phase["phase"]
        row = by_phase.get(phase_id)
        if not row:
            if not modern_trace and phase_id in THEORY_FIRST_INTRODUCED_PHASES:
                continue
            if not modern_trace and phase.get("optional_historical"):
                continue
            if not modern_trace and phase_id in OPTIONAL_HISTORICAL_PHASES:
                continue
            introduced = PHASE_INTRODUCED_CYCLE.get(phase_id)
            cycle_number = source_cycle_number(source)
            if introduced and (not cycle_number or cycle_number < introduced):
                continue
            fail(f"{rel(source)} missing dispatch phase {phase_id}")
        authority = clean_text(row.get("trace_authority"))
        receipt_backed = authority in MODERN_TRACE_AUTHORITIES
        if authority == "canonical_cycle_commit_v2":
            if not authorization_is_runtime_verified(verified_gate):
                fail(f"{rel(source)} canonical v2 trace requires independently replayed gate authority")
            if (
                row.get("canonical_authorization_basis_digest")
                != verified_gate.get("authorization_basis_digest")
                or row.get("canonical_present_investment_decision_digest")
                != verified_gate.get("present_investment_decision_digest")
                or row.get("canonical_operator_evidence_digest") != verified_gate.get("operator_evidence_digest")
                or row.get("canonical_commit_id") != verified_gate.get("commit_id")
                or row.get("target_id") != verified_gate.get("target_id")
            ):
                fail(f"{rel(source)} canonical v2 trace differs from independently replayed authority")
        if modern_trace and not receipt_backed:
            fail(f"{rel(source)} mixes modern and legacy trace authorities at phase {phase_id}")
        phase_requirements = list(
            dict.fromkeys(
                [
                    *phase.get("required_skills", []),
                    *target_specific_required_skills(clean_text(row.get("target_id")), phase_id),
                ]
            )
        )
        invoked = set(row.get("invoked_skills", []))
        skipped = row.get("skipped_skills_with_reason", [])
        skipped_names = {item.get("skill") for item in skipped if isinstance(item, dict) and clean_text(item.get("reason"))}
        missing = []
        cycle_number = source_cycle_number(source)
        for skill in phase_requirements:
            if skill in invoked or (not receipt_backed and skill in skipped_names):
                continue
            introduced = REQUIRED_SKILL_INTRODUCED_CYCLE.get(skill)
            if not receipt_backed and introduced and (not cycle_number or cycle_number < introduced):
                continue
            missing.append(skill)
        declared_missing = set(row.get("missing_required_skills", []))
        if receipt_backed:
            bindings = row.get("receipt_bindings", [])
            if not isinstance(bindings, list):
                fail(f"{rel(source)} dispatch phase {phase_id} receipt_bindings must be a list")
            bound_skills: set[str] = set()
            for binding in bindings:
                if not isinstance(binding, dict):
                    fail(f"{rel(source)} dispatch phase {phase_id} has malformed receipt binding")
                skill = clean_text(binding.get("skill"))
                receipt_ids = binding.get("receipt_ids", [])
                if not skill or not isinstance(receipt_ids, list) or not receipt_ids or not all(clean_text(item) for item in receipt_ids):
                    fail(f"{rel(source)} dispatch phase {phase_id} has unbound invoked skill")
                if authority in {"canonical_cycle_commit_v1", "canonical_cycle_commit_v2"}:
                    if binding.get("evidence_kind") != "canonical_feedback_edge":
                        fail(f"{rel(source)} dispatch phase {phase_id} lacks canonical feedback-edge evidence")
                    edge_ids = binding.get("feedback_edge_ids", [])
                    if not isinstance(edge_ids, list) or not edge_ids or not all(clean_text(item) for item in edge_ids):
                        fail(f"{rel(source)} dispatch phase {phase_id} lacks committed feedback edge IDs")
                bound_skills.add(skill)
            if invoked != bound_skills:
                fail(f"{rel(source)} dispatch phase {phase_id} invoked_skills must equal receipt-bound skills")
            expected_missing = set(missing)
            if declared_missing != expected_missing:
                fail(
                    f"{rel(source)} dispatch phase {phase_id} missing_required_skills does not match "
                    f"unreceipted requirements: {sorted(expected_missing)}"
                )
            expected_status = "certified" if not expected_missing else "blocked_missing_receipts"
            if row.get("dispatch_status") != expected_status:
                fail(f"{rel(source)} dispatch phase {phase_id} has inconsistent dispatch_status")
            if expected_missing:
                blocked_phases.append(phase_id)
            else:
                certified_phases.append(phase_id)
            expected_advisory = list(
                dict.fromkeys(
                    [
                        *phase.get("legacy_advisory_skills", []),
                        *target_specific_advisory_skills(trace_target_id, phase_id),
                    ]
                )
            )
            if row.get("legacy_advisory_skills", []) != expected_advisory:
                fail(f"{rel(source)} dispatch phase {phase_id} has stale legacy advisory skills")
        else:
            # Legacy lists are checked for their historical shape only.  Even a
            # complete list is self-attested and therefore never certified.
            legacy_phases.append(phase_id)
            if missing:
                fail(f"{rel(source)} legacy dispatch phase {phase_id} missing required skills: {missing}")
            advisory_requirements = list(
                dict.fromkeys(
                    [
                        *phase.get("legacy_advisory_skills", []),
                        *target_specific_advisory_skills(trace_target_id, phase_id),
                    ]
                )
            )
            missing_advisory = []
            for skill in advisory_requirements:
                if skill in invoked or skill in skipped_names:
                    continue
                introduced = REQUIRED_SKILL_INTRODUCED_CYCLE.get(skill)
                if introduced and (not cycle_number or cycle_number < introduced):
                    continue
                missing_advisory.append(skill)
            if missing_advisory:
                fail(
                    f"{rel(source)} legacy dispatch phase {phase_id} missing advisory skills: "
                    f"{missing_advisory}"
                )
            if declared_missing:
                fail(f"{rel(source)} legacy dispatch phase {phase_id} records missing_required_skills")
        for field in ["input_artifacts", "output_artifacts"]:
            if not isinstance(row.get(field), list) or not row[field]:
                fail(f"{rel(source)} dispatch phase {phase_id} needs {field}")
        if not clean_text(row.get("validation_handoff")):
            fail(f"{rel(source)} dispatch phase {phase_id} needs validation_handoff")
    certified = not legacy_phases and not blocked_phases
    if require_certified and not certified:
        fail(
            f"{rel(source)} dispatch is not certified; "
            f"legacy phases={legacy_phases}, blocked phases={blocked_phases}"
        )
    return {
        "certified": certified,
        "certified_phases": certified_phases,
        "blocked_phases": blocked_phases,
        "legacy_self_attested_phases": legacy_phases,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*")
    parser.add_argument(
        "--require-certified",
        action="store_true",
        help="Fail unless every current required phase is backed by executable receipts.",
    )
    args = parser.parse_args()
    validate_dispatch_matrix(load_dispatch_matrix())
    paths = [Path(path) for path in args.paths]
    if not paths:
        _, run_state = load_run_state()
        cycles = load_cycles(run_state) if run_state else []
        for cycle in cycles:
            validate_trace(
                cycle.get("skill_dispatch_trace", []),
                ROOT / f"agentic/runs/discovery_marathons/{run_state['run_id']}/cycles/{cycle['cycle_id']}.json",
                require_certified=args.require_certified,
            )
        fixture = ROOT / "tests/fixtures/discovery_marathon/skill_dispatch_valid.json"
        if fixture.exists():
            validate_trace(
                load_json_object(fixture).get("skill_dispatch_trace", []),
                fixture,
                require_certified=args.require_certified,
            )
        invalid = ROOT / "tests/fixtures/discovery_marathon/skill_dispatch_missing_required.json"
        if invalid.exists():
            try:
                with contextlib.redirect_stderr(io.StringIO()):
                    validate_trace(load_json_object(invalid).get("skill_dispatch_trace", []), invalid)
            except SystemExit:
                pass
            else:
                fail(f"{rel(invalid)} should fail dispatch validation")
        print(f"validated discovery marathon skill dispatch for {len(cycles)} active cycles")
        return 0
    for path in paths:
        payload = load_json_object(path)
        validate_trace(
            payload.get("skill_dispatch_trace", payload if isinstance(payload, list) else []),
            path,
            require_certified=args.require_certified,
        )
    print(f"validated {len(paths)} dispatch trace file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Formal, transport, concrete-return, and adversarial validation."""

from __future__ import annotations

import re
from typing import Any

from tdr.domain.models import ValidationOutcome, bounded, stable_id


BRACKETS = {"(": ")", "[": "]", "{": "}"}


def _balanced(text: str) -> bool:
    stack: list[str] = []
    for char in text:
        if char in BRACKETS:
            stack.append(BRACKETS[char])
        elif char in BRACKETS.values():
            if not stack or stack.pop() != char:
                return False
    return not stack


def _lean_skeleton(candidate: dict[str, Any]) -> str:
    name = re.sub(r"\W+", "_", str(candidate.get("candidate_id", "candidate"))).strip("_")
    move = str(candidate.get("formal_move", "unspecified formal move")).replace("-/", "")
    return "\n".join([
        "-- Generated conjectural skeleton; not a proof.",
        "universe u v",
        f"structure {name} where",
        f"  description : String := {move!r}",
        "  witness : Prop",
        "",
        f"theorem {name}_obligation (x : {name}) : x.witness := by",
        "  sorry",
    ])


def _mmt_skeleton(candidate: dict[str, Any]) -> str:
    name = re.sub(r"\W+", "_", str(candidate.get("candidate_id", "Candidate")))
    return f"theory {name} : ?Foundation =\n  witness : type\n  obligation : prop\n# generated conjectural skeleton"


def formalize(payload: dict[str, Any]) -> ValidationOutcome:
    candidate = dict(payload.get("candidate") or {})
    candidate_id = str(candidate.get("candidate_id", "unknown-candidate"))
    move = str(candidate.get("formal_move", ""))
    patch = dict(candidate.get("atlas_patch") or {})
    obligations: list[str] = []
    findings: list[str] = []
    if not move:
        obligations.append("supply a formal move")
    if move and not _balanced(move):
        obligations.append("repair unbalanced delimiters in formal move")
    if not patch:
        obligations.append("supply a typed atlas patch")
    if patch.get("morphisms") and not patch.get("objects"):
        obligations.append("declare source and target objects for each morphism")
    assumptions = candidate.get("assumptions", [])
    obligations.extend(f"discharge assumption: {item}" for item in assumptions)
    targets = list(payload.get("targets") or ["lean", "mmt"])
    artifacts: list[str] = []
    if "lean" in targets:
        artifacts.append(_lean_skeleton(candidate))
    if "mmt" in targets:
        artifacts.append(_mmt_skeleton(candidate))
    structural_blockers = [item for item in obligations if item.startswith(("supply", "repair", "declare"))]
    status = "blocked" if structural_blockers else "partial" if obligations else "passed"
    findings.append("surface syntax and declared atlas patch checked locally")
    findings.append("generated declarations remain conjectural until checked by an external prover")
    return ValidationOutcome(
        validation_id=stable_id("validation", [candidate_id, "formalize", move]),
        candidate_id=candidate_id,
        validator_role="formalizer-and-prover",
        check_type="typing_and_obligations",
        status=status,
        findings=findings,
        obligations_remaining=obligations,
        evidence_artifacts=artifacts,
        falsifying_conditions=structural_blockers,
        realized_value={"formalizability": 0.0 if status == "blocked" else 0.55},
    )


def prove_transport(payload: dict[str, Any]) -> ValidationOutcome:
    morphism = dict(payload.get("morphism") or {})
    theorems = payload.get("theorems") or []
    results: list[str] = []
    obligations = list(morphism.get("obligations", []))
    total = bool(morphism.get("total_on_declared_domain"))
    scope = bool(morphism.get("scope_map"))
    for theorem in theorems:
        item = {"name": theorem} if isinstance(theorem, str) else dict(theorem)
        source_text = str(item.get("statement", item.get("name", "theorem")))
        target_text = str(item.get("target_statement", ""))
        if target_text and _normalize_statement(source_text) == _normalize_statement(target_text):
            results.append(f"excluded trivial restatement: {item.get('name', source_text)}")
        elif total and scope and not obligations:
            results.append(f"transport admissible pending kernel check: {item.get('name', source_text)}")
        else:
            obligations.append(f"establish transport of theorem: {item.get('name', source_text)}")
    status = "passed" if results and not obligations and total and scope else "partial" if total else "blocked"
    return ValidationOutcome(
        validation_id=stable_id("validation", [morphism.get("morphism_id"), "transport", theorems]),
        candidate_id=str(payload.get("candidate_id", morphism.get("morphism_id", "unknown"))),
        validator_role="formalizer-and-prover",
        check_type="theorem_transport",
        status=status,
        findings=results,
        obligations_remaining=list(dict.fromkeys(obligations)),
        evidence_artifacts=[],
        falsifying_conditions=[] if total else ["symbol map is not total on the declared domain"],
        realized_value={"transport": 0.8 if status == "passed" else 0.25 if status == "partial" else 0.0},
    )


def _normalize_statement(text: str) -> str:
    return re.sub(r"\W+", "", text).lower()


def instantiate(payload: dict[str, Any]) -> ValidationOutcome:
    candidate = dict(payload.get("candidate") or {})
    targets = payload.get("targets") or ["finite_mathematical_model"]
    return_paths = candidate.get("return_paths", [])
    findings: list[str] = []
    obligations: list[str] = []
    artifacts: list[str] = []
    for target in targets:
        target_name = str(target.get("name")) if isinstance(target, dict) else str(target)
        assumptions = target.get("assumptions", []) if isinstance(target, dict) else []
        findings.append(f"instantiation plan constructed for {target_name}")
        artifacts.append(f"model:{candidate.get('candidate_id')}:{target_name}:assumptions={assumptions}")
        obligations.append(f"supply executable equations or data for {target_name}")
        obligations.append(f"quantify approximation or measurement error for {target_name}")
    if not return_paths:
        obligations.append("supply an abstract-to-concrete return diagram")
    status = "partial" if targets and return_paths else "blocked"
    return ValidationOutcome(
        validation_id=stable_id("validation", [candidate.get("candidate_id"), "instantiate", targets]),
        candidate_id=str(candidate.get("candidate_id", "unknown-candidate")),
        validator_role="concrete-instantiator",
        check_type="concrete_return",
        status=status,
        findings=findings,
        obligations_remaining=obligations,
        evidence_artifacts=artifacts,
        falsifying_conditions=["all proposed return maps are observationally or mathematically inert"],
        realized_value={"pragmatic": 0.35 if status == "partial" else 0.0},
    )


def falsify(payload: dict[str, Any]) -> ValidationOutcome:
    candidate = dict(payload.get("candidate") or {})
    budget = dict(payload.get("budget") or {})
    max_checks = max(1, int(budget.get("checks", 4)))
    tests = [
        ("degenerate_case", "Set the proposed mediating structure to an identity or zero object."),
        ("scope_boundary", "Move one parameter outside the declared regime and check for illicit extrapolation."),
        ("rival_explanation", "Construct a lower-complexity candidate with the same advertised consequences."),
        ("protected_loss", "Test whether a native operational or ontological distinction collapses."),
        ("auxiliary_dependence", "Remove each auxiliary assumption and record which claims survive."),
        ("vacuity", "Search for models in which the proposal is true only because no nontrivial instances exist."),
    ][:max_checks]
    supplied = dict(payload.get("test_results") or {})
    findings: list[str] = []
    falsifiers: list[str] = []
    for name, description in tests:
        outcome = supplied.get(name, "not_run")
        findings.append(f"{name}: {outcome} — {description}")
        if outcome in {"failed", "falsified", False}:
            falsifiers.append(name)
    status = "falsified" if falsifiers else "partial" if any("not_run" in item for item in findings) else "passed"
    return ValidationOutcome(
        validation_id=stable_id("validation", [candidate.get("candidate_id"), "falsify", tests]),
        candidate_id=str(candidate.get("candidate_id", "unknown-candidate")),
        validator_role="adversarial-critic",
        check_type="adversarial_stress",
        status=status,
        findings=findings,
        obligations_remaining=[f"execute adversarial check: {name}" for name, _ in tests if supplied.get(name, "not_run") == "not_run"],
        evidence_artifacts=[],
        falsifying_conditions=falsifiers,
        realized_value={"robustness": bounded(1.0 - len(falsifiers) / len(tests)) if tests else 0.0},
    )


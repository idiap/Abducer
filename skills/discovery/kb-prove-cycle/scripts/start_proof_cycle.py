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

"""Consume the next proof-queue item and scaffold an informal proof dossier."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from kb_context import canonical_artifacts_dir
from knowledge_source_policy import build_knowledge_source_policy
from knowledge_source_policy import render_knowledge_source_policy_markdown
from inference_diagnosis import refresh_attempt_inference_diagnosis
from kb_context import resolve_kb_reference
from negative_route_heuristic import build_negative_route_heuristic
from problem_mathlib import load_mathlib_index
from problem_mathlib import mathlib_paths
from problem_mathlib import save_mathlib_index
from problem_mathlib import search_mathlib
from proof_discovery_language import render_pdl_program_markdown
from proof_discovery_language import serialize_proof_attempt_as_pdl
from proof_queue import consume_next_entry
from proof_queue import load_proof_queue
from proof_queue import proof_queue_paths
from proof_queue import save_proof_queue
from generate_proof_cycle_summary import refresh_summary_from_sources
from reasoning_log import ReasoningLogger
from statement_text import load_statement_index
from statement_text import statement_excerpt


CRITIQUE_JUDGES = [
    {
        "judge_id": "statement-grounding",
        "title": "Statement Grounding Judge",
        "questions": [
            "Is the claim under test stated explicitly and does it match the queue item?",
            "Are source and target statements grounded in local KB statement ids or InformalMathLib entries?",
            "Does each proof step say what prior local statement or earlier step it depends on?",
        ],
    },
    {
        "judge_id": "tactic-goal-control",
        "title": "Tactic Goal-Control Judge",
        "questions": [
            "Does `normalize-goal` rewrite the task into the exact theorem or route-local statement under test?",
            "If `reduce-to-route-lemma` is used, does it preserve sufficiency instead of quietly weakening the original claim?",
            "Does `closure-check` return to the original queued claim and verify that no goal drift occurred?",
        ],
    },
    {
        "judge_id": "inferential-validity",
        "title": "Inferential Validity Judge",
        "questions": [
            "Does each step follow informally from its stated dependencies?",
            "Are quantifiers, regimes, and model shifts preserved rather than silently changed?",
            "Is the conclusion exactly the claimed result rather than a nearby weaker statement?",
        ],
    },
    {
        "judge_id": "assumption-discipline",
        "title": "Assumption Discipline Judge",
        "questions": [
            "Did the proof introduce any hidden assumptions not already declared?",
            "Are all uses of prior lemmas, barriers, and transfer claims explicit?",
            "If an extra assumption is necessary, is the outcome downgraded to a conditional result?",
        ],
    },
    {
        "judge_id": "citation-fidelity",
        "title": "Citation Fidelity Judge",
        "questions": [
            "Does every cited theorem, definition, or axiom match the statement actually used in the proof step?",
            "If web-sourced material appears, is the exact source recorded together with the role it played?",
            "Does the argument avoid paraphrases that silently alter the mathematical content of a cited result?",
        ],
    },
    {
        "judge_id": "proof-granularity",
        "title": "Proof Granularity Judge",
        "questions": [
            "Is each proof step small enough for an expert to inspect without guessing hidden intermediate claims?",
            "Are route lemmas, reductions, and quantifier shifts made explicit rather than buried inside phrases like `it follows`?",
            "When the proof cannot discharge a burden, is the gap named precisely instead of being glossed over?",
        ],
    },
    {
        "judge_id": "tactic-trace-discipline",
        "title": "Tactic Trace-Discipline Judge",
        "questions": [
            "Is the informal tactic trace updated from template state into a real trace with statuses and notes?",
            "For each recommended tactic, is there either an execution record, an explicit skip rationale, or a blocked/deferred diagnosis?",
            "Do tactic-trace statuses agree with the written stepwise argument and the final verdict?",
        ],
    },
    {
        "judge_id": "tactic-subgoal-exposure",
        "title": "Tactic Subgoal-Exposure Judge",
        "questions": [
            "Do `extract-subgoal` and `activate-target-theorem` expose the exact intermediate claims and missing hypotheses instead of hiding them in prose?",
            "When `construct-witness` or `transport-invariant` is used, is the witness, carrier, transport law, or obstruction stated explicitly?",
            "If a tactic fails, is that failure turned into a named blocker or negative result rather than omitted from the dossier?",
        ],
    },
    {
        "judge_id": "prior-art-and-novelty",
        "title": "Prior-Art And Novelty Judge",
        "questions": [
            "Can the result already be recovered from local InformalMathLib or KB material?",
            "If not locally, is a web search required by the search policy before claiming novelty?",
            "If prior art exists, should the outcome be reclassified as reconstruction or prior_art_found?",
        ],
    },
    {
        "judge_id": "local-counterexample-search",
        "title": "Local Counterexample-Search Judge",
        "questions": [
            "Was a local search for counterexamples, model mismatches, or barrier analogs actually attempted before escalation?",
            "Does the dossier say what was checked locally and what failed to falsify the claim?",
            "If a nearby failure pattern exists, does the argument explain why it does or does not apply to the current route?",
        ],
    },
    {
        "judge_id": "obstruction-and-negative-route",
        "title": "Obstruction And Negative-Route Judge",
        "questions": [
            "Does the current argument survive the designated negative route or obstruction check?",
            "Is there a counterexample, barrier, or failure mode that blocks the route?",
            "If the route fails, is the negative result itself clearly formulated?",
        ],
    },
    {
        "judge_id": "contradiction-and-impossibility-discipline",
        "title": "Contradiction And Impossibility Discipline Judge",
        "questions": [
            "If the argument uses negation, is the exact negated claim stated explicitly rather than implied informally?",
            "If the route uses contradiction, is the forbidden collapse, barrier, or inconsistency named precisely?",
            "If the constructive route fails, does the dossier formulate a theorem-shaped impossibility or non-realization claim rather than only saying `blocked`?",
        ],
    },
    {
        "judge_id": "closure",
        "title": "Closure Judge",
        "questions": [
            "Is the final outcome correctly classified as proved, disproved, blocked, deferred, or prior_art_found?",
            "Does the written proof or disproof support that classification?",
            "Is the result statement ready to persist into InformalMathLib if the outcome is terminal?",
        ],
    },
]

WEB_SEARCH_POLICY = [
    "Do not search the web by default. Exhaust the local KB, current artifacts, and local InformalMathLib first.",
    "Search only if the missing fact is decisive for a proof step, prior-art check, or exact theorem attribution.",
    "Search when a named theorem, barrier, paper, or threshold fact is not present locally and materially affects the result.",
    "Do not search for generic background, motivation, or intuitive exposition.",
    "If web search is used, record the concrete query, the exact source, and what proof step or novelty decision it informed.",
]

INFORMAL_TACTIC_LIBRARY = [
    {
        "tactic_id": "normalize-goal",
        "inspired_by": ["change", "rewrite"],
        "title": "Normalize Goal",
        "purpose": "Rewrite the target into the exact theorem statement or route-local formulation that should be proved.",
        "transport_rule": "Use this to eliminate wording drift, hidden model changes, or nearby-but-weaker claims before real proof work begins.",
    },
    {
        "tactic_id": "introduce-assumptions",
        "inspired_by": ["intro", "intros", "fix"],
        "title": "Introduce Assumptions",
        "purpose": "Expose quantifiers, regimes, admissibility conditions, and candidate objects as explicit assumptions.",
        "transport_rule": "Use this whenever the claim starts with an existential or conditional bridge statement and hidden assumptions are a risk.",
    },
    {
        "tactic_id": "extract-subgoal",
        "inspired_by": ["have", "assert"],
        "title": "Extract Subgoal",
        "purpose": "State the next indispensable intermediate lemma explicitly instead of burying it inside prose.",
        "transport_rule": "Use this when the proof burden naturally decomposes into one named realization, transport, or forcing lemma.",
    },
    {
        "tactic_id": "reduce-to-route-lemma",
        "inspired_by": ["suffices", "refine"],
        "title": "Reduce To Route Lemma",
        "purpose": "Replace the full theorem by the narrower lemma whose discharge would activate the route.",
        "transport_rule": "Use this when the target theorem is known or when the current route is blocked at one identified interface.",
    },
    {
        "tactic_id": "construct-witness",
        "inspired_by": ["obtain", "use", "existsi"],
        "title": "Construct Witness",
        "purpose": "Construct or sharply specify the witness family, obstruction family, reduction gadget, or certificate needed by the route.",
        "transport_rule": "Use this when the bridge depends on an explicit carrier rather than only on a theorem invocation.",
    },
    {
        "tactic_id": "activate-target-theorem",
        "inspired_by": ["apply", "exact"],
        "title": "Activate Target Theorem",
        "purpose": "Apply the known target theorem and list the exact hypotheses still missing locally.",
        "transport_rule": "Use this when the real proof state is an activation problem rather than a target-discovery problem.",
    },
    {
        "tactic_id": "transport-invariant",
        "inspired_by": ["calc", "transitivity", "rewrite"],
        "title": "Transport Invariant",
        "purpose": "Track the preserved invariant across model shifts, representation changes, or intermediate objects.",
        "transport_rule": "Use this when a route claims preservation across a nontrivial transport step.",
    },
    {
        "tactic_id": "case-split",
        "inspired_by": ["cases", "rcases", "by_cases"],
        "title": "Case Split",
        "purpose": "Split by regime, threshold, encoding, or obstruction type when one proof line hides multiple burdens.",
        "transport_rule": "Use this only when the split is mathematically real and reduces ambiguity rather than multiplying branches.",
    },
    {
        "tactic_id": "negate-goal",
        "inspired_by": ["by_contra", "by_contradiction", "contrapose"],
        "title": "Negate Goal",
        "purpose": "State the exact negation of the target theorem, route payoff, or carrier claim that the negative branch will test.",
        "transport_rule": "Use this before contradiction-style reasoning so the dossier names the exact assumption being negated.",
    },
    {
        "tactic_id": "obstruction-probe",
        "inspired_by": ["by_contra", "contrapose"],
        "title": "Obstruction Probe",
        "purpose": "Run the designated negative route explicitly and determine whether a barrier, counterexample, or mismatch blocks the claim.",
        "transport_rule": "Use this as a first-class tactic whenever the route has a named failure mode.",
    },
    {
        "tactic_id": "derive-contradiction",
        "inspired_by": ["exfalso", "have", "contradiction"],
        "title": "Derive Contradiction",
        "purpose": "Push the negated branch to a forbidden collapse, barrier violation, or explicit inconsistency with accepted local results.",
        "transport_rule": "Use this when the route claims payoff by contradiction or when the negative branch should end in a named impossibility trigger.",
    },
    {
        "tactic_id": "prove-impossibility-claim",
        "inspired_by": ["suffices", "have", "exact"],
        "title": "Prove Impossibility Claim",
        "purpose": "Turn a failed constructive route into a theorem-shaped non-realization, barrier, or route-impossibility result.",
        "transport_rule": "Use this when the negative branch is more informative than forcing another speculative constructive attempt.",
    },
    {
        "tactic_id": "closure-check",
        "inspired_by": ["done", "exact", "show"],
        "title": "Closure Check",
        "purpose": "Confirm that the argument established the exact queued claim and not a nearby conditional or weakened statement.",
        "transport_rule": "Use this before assigning the terminal verdict and before persisting anything to InformalMathLib.",
    },
]


def _ensure_list(value: Any) -> list[Any]:
    """Return a list for list-like fields while treating malformed values as empty."""

    return value if isinstance(value, list) else []


def _clean_text(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def _ensure_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _next_attempt_id(attempt_dir: Path, *, kb_ref: str) -> str:
    prefix = f"attempt.{kb_ref}."
    current = 0
    if attempt_dir.exists():
        for path in attempt_dir.glob("*.json"):
            name = path.stem
            if not name.startswith(prefix):
                continue
            suffix = name[len(prefix) :]
            if suffix.isdigit():
                current = max(current, int(suffix))
    return f"{prefix}{current + 1:03d}"


def _attempt_paths(artifacts_dir: Path, attempt_id: str) -> tuple[Path, Path]:
    attempt_dir = artifacts_dir / "proof-attempts"
    return attempt_dir / f"{attempt_id}.json", attempt_dir / f"{attempt_id}.md"


def _judge_records() -> list[dict[str, Any]]:
    return [
        {
            "judge_id": row["judge_id"],
            "title": row["title"],
            "questions": list(row["questions"]),
            "verdict": "pending",
            "blocking_issues": [],
            "notes": [],
        }
        for row in CRITIQUE_JUDGES
    ]


def _first_nonempty(*values: Any) -> str:
    for value in values:
        text = _clean_text(value)
        if text:
            return text
    return ""


def _goal_focus(queue_entry: dict[str, Any]) -> str:
    delta = queue_entry.get("statement_delta")
    delta_dict = delta if isinstance(delta, dict) else {}
    return _first_nonempty(
        delta_dict.get("target_claim_focus"),
        queue_entry.get("target_statement_id"),
        queue_entry.get("claim_text"),
    )


def _source_focus(queue_entry: dict[str, Any]) -> str:
    delta = queue_entry.get("statement_delta")
    delta_dict = delta if isinstance(delta, dict) else {}
    return _first_nonempty(
        delta_dict.get("source_claim_focus"),
        queue_entry.get("source_statement_id"),
        queue_entry.get("claim_text"),
    )


def _negative_route_heuristic(queue_entry: dict[str, Any]) -> dict[str, Any]:
    """Return the queue-level contradiction/impossibility decision heuristic, deriving it if absent."""

    negative_program = _ensure_dict(queue_entry.get("negative_reasoning_program"))
    heuristic = _ensure_dict(negative_program.get("heuristic"))
    if heuristic:
        return heuristic
    return build_negative_route_heuristic(
        candidate_object=_clean_text(queue_entry.get("candidate_object")),
        source_focus=_source_focus(queue_entry),
        target_focus=_goal_focus(queue_entry),
        invariant=_clean_text(queue_entry.get("preserved_invariant")),
        negative_route=_clean_text(queue_entry.get("negative_route")) or _clean_text(negative_program.get("designated_negative_route")),
        failure_diagnosis=_clean_text(queue_entry.get("failure_diagnosis")) or _clean_text(negative_program.get("forbidden_outcome")),
        barrier_scope=_clean_text(queue_entry.get("barrier_scope")) or _clean_text(negative_program.get("barrier_scope")),
        missing_route_lemma=_clean_text(queue_entry.get("missing_route_lemma")),
        carrier_kind=_clean_text(queue_entry.get("carrier_kind")),
    )


def _expert_conjecture_context(queue_entry: dict[str, Any]) -> dict[str, Any]:
    """Extract the promoted theorem-package context when the queue item is expert-grade."""

    if _clean_text(queue_entry.get("claim_type")) != "expert-conjecture":
        return {}
    regime = _ensure_dict(queue_entry.get("regime_and_quantifiers"))
    branch_to_definition = _ensure_dict(queue_entry.get("branch_to_definition"))
    foundation_search = _ensure_dict(queue_entry.get("foundation_search"))
    admissibility_conditions = [
        _clean_text(value)
        for value in _ensure_list(queue_entry.get("admissibility_conditions"))
        if _clean_text(value)
    ]
    return {
        "theorem_package_id": _clean_text(queue_entry.get("theorem_package_id")),
        "restricted_regime_mode": _clean_text(queue_entry.get("restricted_regime_mode")),
        "quantifier_frame": _clean_text(regime.get("quantifier_frame")),
        "source_regime": _clean_text(regime.get("source_regime")),
        "target_regime": _clean_text(regime.get("target_regime")),
        "route_focus": _clean_text(regime.get("route_focus")),
        "bridge_object_definition": _clean_text(queue_entry.get("bridge_object_definition")),
        "admissibility_conditions": admissibility_conditions,
        "first_nontrivial_lemma_title": _clean_text(queue_entry.get("first_nontrivial_lemma_title")),
        "first_nontrivial_lemma_statement": _clean_text(queue_entry.get("first_nontrivial_lemma_statement")),
        "negative_barrier_version": _clean_text(queue_entry.get("negative_barrier_version")),
        "independent_value_claim": _clean_text(queue_entry.get("independent_value_claim")),
        "branch_to_definition": branch_to_definition,
        "foundation_search": foundation_search,
        "mathematical_layers": _ensure_dict(queue_entry.get("mathematical_layers")),
    }


def _seed_assumptions(queue_entry: dict[str, Any], expert_context: dict[str, Any]) -> list[str]:
    """Seed explicit assumptions from the expert theorem package when available."""

    assumptions: list[str] = []
    quantifier_frame = _clean_text(expert_context.get("quantifier_frame"))
    if quantifier_frame:
        assumptions.append(quantifier_frame)
    assumptions.extend(
        [
            _clean_text(value)
            for value in _ensure_list(expert_context.get("admissibility_conditions"))
            if _clean_text(value)
        ]
    )
    if not assumptions and _clean_text(queue_entry.get("conditional_proposition")):
        assumptions.append(_clean_text(queue_entry.get("conditional_proposition")))
    return assumptions


def _tactic_playbook(queue_entry: dict[str, Any]) -> list[dict[str, Any]]:
    candidate_object = _clean_text(queue_entry.get("candidate_object"))
    invariant = _clean_text(queue_entry.get("preserved_invariant"))
    route_lemma = _clean_text(queue_entry.get("missing_route_lemma"))
    target_focus = _goal_focus(queue_entry)
    source_focus = _source_focus(queue_entry)
    negative_route = _clean_text(queue_entry.get("negative_route"))
    negative_program = _ensure_dict(queue_entry.get("negative_reasoning_program"))
    negative_mode = _clean_text(negative_program.get("negative_mode"))
    negative_heuristic = _negative_route_heuristic(queue_entry)
    negative_decision = _clean_text(negative_heuristic.get("decision"))
    playbook: list[dict[str, Any]] = []
    for row in INFORMAL_TACTIC_LIBRARY:
        tactic = dict(row)
        tactic["recommended_here"] = False
        tactic["queue_specific_role"] = ""
        if tactic["tactic_id"] == "normalize-goal":
            tactic["recommended_here"] = True
            tactic["queue_specific_role"] = _clean_text(
                f"Normalize the queued claim so the goal is exactly `{target_focus}` rather than a nearby consequence."
            )
        elif tactic["tactic_id"] == "introduce-assumptions":
            tactic["recommended_here"] = True
            tactic["queue_specific_role"] = _clean_text(
                f"Expose the source premise `{source_focus}` and admissibility of `{candidate_object or 'the candidate object'}`."
            )
        elif tactic["tactic_id"] == "extract-subgoal":
            tactic["recommended_here"] = bool(route_lemma)
            tactic["queue_specific_role"] = _clean_text(f"State `{route_lemma}` as an inspectable intermediate claim.")
        elif tactic["tactic_id"] == "reduce-to-route-lemma":
            tactic["recommended_here"] = bool(route_lemma)
            tactic["queue_specific_role"] = _clean_text(f"Reduce the whole route to the narrower obligation `{route_lemma}`.")
        elif tactic["tactic_id"] == "construct-witness":
            tactic["recommended_here"] = bool(candidate_object)
            tactic["queue_specific_role"] = _clean_text(
                f"Construct or sharply constrain `{candidate_object or 'the missing bridge object'}` from `{source_focus}`."
            )
        elif tactic["tactic_id"] == "activate-target-theorem":
            tactic["recommended_here"] = bool(_clean_text(queue_entry.get("target_statement_id")))
            tactic["queue_specific_role"] = _clean_text(
                f"Treat `{target_focus}` as the activation target and list which hypotheses remain open locally."
            )
        elif tactic["tactic_id"] == "transport-invariant":
            tactic["recommended_here"] = bool(invariant)
            tactic["queue_specific_role"] = _clean_text(
                f"Track how `{invariant}` survives the intended route from `{source_focus}` to `{target_focus}`."
            )
        elif tactic["tactic_id"] == "case-split":
            tactic["recommended_here"] = "if needed"
            tactic["queue_specific_role"] = "Split by regime, carrier encoding, or threshold only if one proof line hides multiple real burdens."
        elif tactic["tactic_id"] == "negate-goal":
            tactic["recommended_here"] = bool(negative_heuristic.get("use_negation"))
            tactic["queue_specific_role"] = _clean_text(
                f"{negative_program.get('negated_claim') or f'State the exact negation of `{target_focus}` before running the negative branch.'} "
                f"Heuristic: {negative_decision or 'constructive-first'}."
            )
        elif tactic["tactic_id"] == "obstruction-probe":
            tactic["recommended_here"] = True
            tactic["queue_specific_role"] = _clean_text(
                f"Probe the named negative route `{negative_route or 'local obstruction'}` before claiming progress. "
                f"Heuristic: {negative_decision or 'constructive-first'}."
            )
        elif tactic["tactic_id"] == "derive-contradiction":
            tactic["recommended_here"] = bool(negative_heuristic.get("use_contradiction"))
            tactic["queue_specific_role"] = _clean_text(
                negative_program.get("contradiction_target")
                or "Push the negative branch to a named forbidden outcome if the route is truly impossible."
            )
        elif tactic["tactic_id"] == "prove-impossibility-claim":
            tactic["recommended_here"] = bool(negative_heuristic.get("use_impossibility_claim"))
            tactic["queue_specific_role"] = _clean_text(
                negative_program.get("impossibility_claim_template")
                or "If the constructive route fails, formulate the strongest theorem-shaped negative result."
            )
        elif tactic["tactic_id"] == "closure-check":
            tactic["recommended_here"] = True
            tactic["queue_specific_role"] = _clean_text(
                f"Check that the argument proves exactly `{target_focus}` and not a weaker surrogate."
            )
        playbook.append(tactic)
    return playbook


def _tactic_trace(queue_entry: dict[str, Any]) -> list[dict[str, Any]]:
    candidate_object = _clean_text(queue_entry.get("candidate_object"))
    invariant = _clean_text(queue_entry.get("preserved_invariant"))
    route_lemma = _clean_text(queue_entry.get("missing_route_lemma"))
    negative_route = _clean_text(queue_entry.get("negative_route"))
    negative_program = _ensure_dict(queue_entry.get("negative_reasoning_program"))
    negative_mode = _clean_text(negative_program.get("negative_mode"))
    negative_heuristic = _negative_route_heuristic(queue_entry)
    source_focus = _source_focus(queue_entry)
    target_focus = _goal_focus(queue_entry)
    trace: list[dict[str, Any]] = []

    def add_step(*, tactic_id: str, goal: str, expected_output: str) -> None:
        trace.append(
            {
                "order": len(trace) + 1,
                "tactic_id": tactic_id,
                "goal": _clean_text(goal),
                "expected_output": expected_output,
                "status": "pending",
                "notes": [],
            }
        )

    add_step(
        tactic_id="normalize-goal",
        goal=f"Rewrite the task as the exact target `{target_focus}`.",
        expected_output="One normalized theorem statement under test, with no silent weakening or model drift.",
    )
    add_step(
        tactic_id="introduce-assumptions",
        goal=(
            f"Make the bridge assumptions explicit: source premise `{source_focus}` and admissibility of "
            f"`{candidate_object or 'the candidate object'}`."
        ),
        expected_output="A short explicit list of assumptions and regime declarations.",
    )
    if route_lemma:
        add_step(
            tactic_id="reduce-to-route-lemma",
            goal=f"Show that it suffices to prove `{route_lemma}`.",
            expected_output="A theorem-shaped reduction from the full claim to the route-local lemma.",
        )
        add_step(
            tactic_id="extract-subgoal",
            goal=f"State `{route_lemma}` as the next explicit subgoal.",
            expected_output="A named subgoal with dependencies and failure mode.",
        )
    if candidate_object:
        add_step(
            tactic_id="construct-witness",
            goal=f"Construct or constrain `{candidate_object}` from `{source_focus}`.",
            expected_output="An explicit witness, carrier, or clear statement that this construction is blocked.",
        )
    if invariant:
        add_step(
            tactic_id="transport-invariant",
            goal=f"Preserve `{invariant}` along the route toward `{target_focus}`.",
            expected_output="A short chain of invariant-preservation steps or a precise transport obstruction.",
        )
    add_step(
        tactic_id="activate-target-theorem",
        goal=f"Activate the target-side theorem package for `{target_focus}`.",
        expected_output="A list of exact target hypotheses and which ones are already discharged.",
    )
    if bool(negative_heuristic.get("use_negation")):
        add_step(
            tactic_id="negate-goal",
            goal=_clean_text(
                negative_program.get("negated_claim")
                or f"State the exact negation of the route toward `{target_focus}`."
            ),
            expected_output="One explicit negated claim or branch assumption, with no ambiguity about what is being denied.",
        )
    add_step(
        tactic_id="obstruction-probe",
        goal=f"Run the negative route `{negative_route or 'current obstruction'}` against the argument.",
        expected_output="A clear statement that the route survives, or a precise barrier/counterexample diagnosis.",
    )
    if bool(negative_heuristic.get("use_contradiction")):
        add_step(
            tactic_id="derive-contradiction",
            goal=_clean_text(
                negative_program.get("contradiction_target")
                or "Drive the negated branch to a named forbidden outcome."
            ),
            expected_output="A contradiction, forbidden collapse, or barrier violation that discharges the negative branch.",
        )
    if bool(negative_heuristic.get("use_impossibility_claim")):
        add_step(
            tactic_id="prove-impossibility-claim",
            goal=_clean_text(
                negative_program.get("impossibility_claim_template")
                or "State the theorem-shaped impossibility claim implied by the failed constructive route."
            ),
            expected_output="A precise negative theorem candidate or route-impossibility formulation.",
        )
    add_step(
        tactic_id="closure-check",
        goal=f"Verify that the argument closes exactly the queued target `{target_focus}`.",
        expected_output="A final verdict of proved, disproved, blocked, deferred, or prior_art_found with no claim drift.",
    )
    return trace


def _seed_stepwise_argument(
    queue_entry: dict[str, Any],
    *,
    source_excerpt: str,
    target_excerpt: str,
    expert_context: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Pre-seed a non-empty proof outline from the queued theorem context."""

    expert_context = _ensure_dict(expert_context)
    candidate_object = _clean_text(queue_entry.get("candidate_object")) or "the candidate bridge object"
    invariant = _clean_text(queue_entry.get("preserved_invariant")) or "the route invariant"
    route_lemma = _clean_text(queue_entry.get("missing_route_lemma"))
    source_focus = _source_focus(queue_entry)
    target_focus = _goal_focus(queue_entry)
    theorem_statement = _clean_text(queue_entry.get("conjecture_statement") or queue_entry.get("claim_text"))
    bridge_definition = _clean_text(expert_context.get("bridge_object_definition"))
    quantifier_frame = _clean_text(expert_context.get("quantifier_frame"))
    admissibility_conditions = [
        _clean_text(value)
        for value in _ensure_list(expert_context.get("admissibility_conditions"))
        if _clean_text(value)
    ]
    first_lemma_title = _clean_text(expert_context.get("first_nontrivial_lemma_title"))
    first_lemma_statement = _clean_text(expert_context.get("first_nontrivial_lemma_statement"))
    obligations = [
        _clean_text(value)
        for value in _ensure_list(queue_entry.get("proof_obligations"))
        if _clean_text(value)
    ]
    lemmas = [
        _clean_text(value)
        for value in _ensure_list(queue_entry.get("candidate_lemmas"))
        if _clean_text(value)
    ]

    seeded = [
        {
            "step": 1,
            "claim": bridge_definition or _clean_text(
                f"Recast the source-side content `{source_excerpt or source_focus}` into a route-local statement about `{candidate_object}`."
            ),
            "justification": admissibility_conditions[0] if admissibility_conditions else obligations[0] if obligations else _clean_text(
                quantifier_frame or f"Use the source theorem focus `{source_focus}` to isolate the first realizability obligation."
            ),
            "depends_on": [_clean_text(queue_entry.get("source_statement_id"))] if _clean_text(queue_entry.get("source_statement_id")) else [],
        },
        {
            "step": 2,
            "claim": first_lemma_statement or _clean_text(
                f"Show that `{candidate_object}` preserves `{invariant}` strongly enough to support `{route_lemma or target_focus}`."
            ),
            "justification": first_lemma_title
            or (lemmas[0] if lemmas else "")
            or _clean_text(
                f"Discharge the route-local transport or realization lemma `{route_lemma or 'for the target claim'}`."
            ),
            "depends_on": [
                value
                for value in [
                    _clean_text(queue_entry.get("source_statement_id")),
                    first_lemma_title,
                    route_lemma,
                ]
                if value
            ],
        },
        {
            "step": 3,
            "claim": theorem_statement or _clean_text(
                f"Apply the target-side statement `{target_excerpt or target_focus}` once the hypotheses induced by `{candidate_object}` are explicit."
            ),
            "justification": _clean_text(
                f"Close the queued conjecture by matching the target theorem excerpt to the hypotheses discharged in the previous steps."
            ),
            "depends_on": [
                value
                for value in [
                    route_lemma,
                    _clean_text(queue_entry.get("target_statement_id")),
                ]
                if value
            ],
        },
    ]
    return seeded


def build_attempt_record(
    *,
    attempt_id: str,
    kb_ref: str,
    queue_entry: dict[str, Any],
    mathlib_hits: list[dict[str, Any]],
    statement_index: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    source_id = _clean_text(queue_entry.get("source_statement_id"))
    target_id = _clean_text(queue_entry.get("target_statement_id"))
    negative_program = _ensure_dict(queue_entry.get("negative_reasoning_program"))
    negative_heuristic = _negative_route_heuristic(queue_entry)
    expert_context = _expert_conjecture_context(queue_entry)
    source_excerpt = _clean_text(queue_entry.get("source_excerpt")) or statement_excerpt(statement_index.get(source_id, {}))
    target_excerpt = _clean_text(queue_entry.get("target_excerpt")) or statement_excerpt(statement_index.get(target_id, {}))
    source_policy = build_knowledge_source_policy(
        stage="prove",
        target_label=_clean_text(queue_entry.get("title")) or _clean_text(queue_entry.get("claim_text")),
        target_kind="proof target",
        mathlib_hit_count=len(mathlib_hits),
        external_framework_recommended=bool(_ensure_dict(expert_context.get("foundation_search")).get("recommended")),
    )
    attempt = {
        "metadata": {
            "attempt_id": attempt_id,
            "kb_ref": kb_ref,
            "queue_id": _clean_text(queue_entry.get("queue_id")),
            "started_utc": queue_entry.get("updated_utc", ""),
            "updated_utc": queue_entry.get("updated_utc", ""),
            "status": "in_progress",
        },
        "target": dict(queue_entry),
        "local_context": {
            "source_excerpt": source_excerpt,
            "target_excerpt": target_excerpt,
            "mathlib_hits": [
                {
                    "result_id": _clean_text(row.get("result_id")),
                    "title": _clean_text(row.get("title")),
                    "outcome": _clean_text(row.get("outcome")),
                    "summary": _clean_text(row.get("summary")),
                    "artifact_path": _clean_text(row.get("artifact_path")),
                }
                for row in mathlib_hits
            ],
        },
        "web_search_gate": {
            "decision": "not-evaluated",
            "policy": list(WEB_SEARCH_POLICY),
            "triggered_criteria": [],
            "rationale": "Default stance: do not browse until a decisive local gap or prior-art uncertainty is identified.",
            "queries": [],
            "sources": [],
        },
        "knowledge_source_policy": source_policy,
        "external_references": [],
        "proof_attempt": {
            "theorem_statement": _clean_text(queue_entry.get("conjecture_statement") or queue_entry.get("claim_text")),
            "route_lemma_under_test": _clean_text(queue_entry.get("missing_route_lemma")),
            "assumptions": _seed_assumptions(queue_entry, expert_context),
            "strategy": _clean_text(queue_entry.get("proof_strategy_family")),
            "expert_conjecture_context": expert_context,
            "informal_tactic_playbook": _tactic_playbook(queue_entry),
            "informal_tactic_trace": _tactic_trace(queue_entry),
            "local_results_used": [],
            "contradiction_frame": {
                "negative_mode": _clean_text(negative_program.get("negative_mode")),
                "negated_claim": _clean_text(negative_program.get("negated_claim")),
                "contradiction_target": _clean_text(negative_program.get("contradiction_target")),
                "forbidden_outcome": _clean_text(negative_program.get("forbidden_outcome")),
                "impossibility_claim_template": _clean_text(negative_program.get("impossibility_claim_template")),
            },
            "negative_route_heuristic": negative_heuristic,
            "stepwise_argument": _seed_stepwise_argument(
                queue_entry,
                source_excerpt=source_excerpt,
                target_excerpt=target_excerpt,
                expert_context=expert_context,
            ),
            "negative_argument": {
                "obstruction_candidate": _clean_text(queue_entry.get("negative_route")),
                "counterexample_or_barrier": "",
                "effect_on_claim": "",
                "negated_claim": _clean_text(negative_program.get("negated_claim")),
                "contradiction_target": _clean_text(negative_program.get("contradiction_target")),
                "forbidden_outcome": _clean_text(negative_program.get("forbidden_outcome")),
                "impossibility_claim": _clean_text(queue_entry.get("impossibility_conjecture") or negative_program.get("impossibility_claim_template")),
            },
            "result_statement": "",
            "result_summary": "",
        },
        "critique_judges": _judge_records(),
        "final_assessment": {
            "outcome": "in_progress",
            "verdict": "",
            "novelty_assessment": "",
            "confidence": "",
            "summary": "",
        },
        "major_subresult_assessment": {
            "mandatory_gates": {
                "self_contained_statement": False,
                "mathematical_inspectability": False,
                "nontrivial_frontier_relation": False,
                "independent_value": False,
            },
            "axes": {
                "frontier_shift": 0,
                "independence": 0,
                "transferability": 0,
                "barrier_clarity": 0,
                "proof_closure": 0,
                "search_compression": 0,
            },
            "justifications": {
                "frontier_shift": "",
                "independence": "",
                "transferability": "",
                "barrier_clarity": "",
                "proof_closure": "",
                "search_compression": "",
            },
            "overall_judgment": "",
            "paper_candidate_title": "",
            "paper_candidate_summary": "",
        },
    }
    refresh_attempt_inference_diagnosis(attempt)
    attempt["pdl_program"] = serialize_proof_attempt_as_pdl(attempt)
    return attempt


def render_attempt_markdown(attempt: dict[str, Any]) -> str:
    """Render the current proof-attempt state, including terminal verdicts and critique outcomes."""
    diagnosis = refresh_attempt_inference_diagnosis(attempt)
    target = _ensure_dict(attempt.get("target"))
    local_context = _ensure_dict(attempt.get("local_context"))
    proof_attempt = _ensure_dict(attempt.get("proof_attempt"))
    major_subresult = _ensure_dict(attempt.get("major_subresult_assessment"))
    gates = _ensure_dict(major_subresult.get("mandatory_gates"))
    axes = _ensure_dict(major_subresult.get("axes"))
    metadata = _ensure_dict(attempt.get("metadata"))
    final_assessment = _ensure_dict(attempt.get("final_assessment"))
    lines = [
        f"# Proof Attempt: {metadata.get('attempt_id', '')}",
        "",
        f"- Queue ID: {metadata.get('queue_id', '')}",
        f"- Status: {metadata.get('status', '')}",
        f"- Conjecture: {target.get('conjecture_statement') or target.get('claim_text', '')}",
        f"- Bridge: {target.get('bridge_id', '')}",
        f"- Source statement: {target.get('source_statement_id', '')}",
        f"- Target statement: {target.get('target_statement_id', '')}",
        "",
        "## Prompt / Inference Diagnosis",
        "",
        f"- Context status: {diagnosis.get('context_status', '')}",
        f"- Inference status: {diagnosis.get('inference_status', '')}",
        f"- Blocking defects: {' | '.join(str(value) for value in diagnosis.get('blocking_defects', [])[:3])}",
        f"- Minimal repair: {diagnosis.get('minimal_repair', '')}",
        f"- Certainty now: {diagnosis.get('certainty_now', '')}",
        f"- Certainty if well posed: {diagnosis.get('certainty_if_well_posed', '')}",
        f"- Rationale: {diagnosis.get('rationale', '')}",
        "",
        "## Local Grounding",
        "",
        f"- Source excerpt: {local_context.get('source_excerpt', '')}",
        f"- Target excerpt: {local_context.get('target_excerpt', '')}",
        "",
        "## Queue Context",
        "",
        f"- Candidate object: {target.get('candidate_object', '')}",
        f"- Invariant: {target.get('preserved_invariant', '')}",
        f"- Route synopsis: {target.get('route_synopsis', '')}",
        f"- Route lemma under test: {target.get('missing_route_lemma', '')}",
        "",
    ]
    expert_context = _ensure_dict(proof_attempt.get("expert_conjecture_context"))
    if expert_context:
        lines.extend(
            [
                "## Expert Theorem Package",
                "",
                f"- Theorem package ID: {expert_context.get('theorem_package_id', '')}",
                f"- Restricted-regime mode: {expert_context.get('restricted_regime_mode', '')}",
                f"- Quantifier frame: {expert_context.get('quantifier_frame', '')}",
                f"- Bridge-object definition: {expert_context.get('bridge_object_definition', '')}",
                f"- First nontrivial lemma: {expert_context.get('first_nontrivial_lemma_title', '')} | {expert_context.get('first_nontrivial_lemma_statement', '')}",
                f"- Negative/barrier version: {expert_context.get('negative_barrier_version', '')}",
                f"- Independent value claim: {expert_context.get('independent_value_claim', '')}",
                "",
            ]
        )
        math_layers = _ensure_dict(expert_context.get("mathematical_layers"))
        latex_layer = _ensure_dict(math_layers.get("latex"))
        lean_layer = _ensure_dict(math_layers.get("lean_style"))
        symbol_rows = [
            f"{_clean_text(item.get('symbol'))}: {_clean_text(item.get('meaning'))}"
            for item in _ensure_list(math_layers.get("symbol_ledger"))
            if isinstance(item, dict) and _clean_text(item.get("symbol"))
        ]
        if math_layers:
            lines.extend(
                [
                    "## Mathematical Packet",
                    "",
                    f"- Quantifier signature: {math_layers.get('quantifier_signature', '')}",
                    f"- Symbol ledger: {' | '.join(symbol_rows[:6])}",
                    f"- LaTeX theorem: {latex_layer.get('theorem_statement', '')}",
                    "",
                ]
            )
            lean_scaffold = str(lean_layer.get("scaffold", "")).strip()
            if lean_scaffold:
                lines.extend(
                    [
                        "```lean",
                        lean_scaffold,
                        "```",
                        "",
                    ]
                )
        admissibility_conditions = [
            row for row in _ensure_list(expert_context.get("admissibility_conditions")) if _clean_text(row)
        ]
        if admissibility_conditions:
            lines.append("Admissibility conditions:")
            for row in admissibility_conditions:
                lines.append(f"- {row}")
            lines.append("")
        foundation_search = _ensure_dict(expert_context.get("foundation_search"))
        if foundation_search:
            lines.extend(
                [
                    f"- Foundation-search mode: {foundation_search.get('mode', '')}",
                    f"- Foundation-search recommended: {foundation_search.get('recommended', False)}",
                ]
            )
            regions = [row for row in _ensure_list(foundation_search.get("candidate_framework_regions")) if _clean_text(row)]
            if regions:
                lines.append(f"- Candidate framework regions: {', '.join(regions)}")
            lines.append("")
    lines.extend(
        [
        "## Local InformalMathLib Hits",
        "",
    ])
    hits = [row for row in attempt.get("local_context", {}).get("mathlib_hits", []) if isinstance(row, dict)]
    if not hits:
        lines.append("- No local InformalMathLib hits were found.")
        lines.append("")
    else:
        for row in hits:
            lines.append(
                f"- `{row.get('result_id', '')}` | {row.get('outcome', '')} | {row.get('title', '')} | {row.get('artifact_path', '')}"
            )
        lines.append("")
    lines.extend(
        [
            "## Web Search Gate",
            "",
            "Default policy:",
        ]
    )
    for row in attempt.get("web_search_gate", {}).get("policy", []) if isinstance(attempt.get("web_search_gate", {}).get("policy"), list) else []:
        lines.append(f"- {row}")
    lines.extend(
        [
            "",
            "## Knowledge Source Invocation Policy",
            "",
        ]
    )
    lines.extend(
        render_knowledge_source_policy_markdown(
            _ensure_dict(attempt.get("knowledge_source_policy"))
        )
    )
    lines.extend([""])
    lines.extend(
        render_pdl_program_markdown(
            _ensure_dict(attempt.get("pdl_program")) or serialize_proof_attempt_as_pdl(attempt)
        )
    )
    lines.extend(
        [
            "",
            "Decision: fill this in only if a decisive local gap appears.",
            "",
            "## External References To Import Into InformalMathLib",
            "",
            "If you use an external theorem, definition, or axiom, record it here in the JSON as an object with:",
            "- `reference_type`: theorem, definition, or axiom",
            "- `title`",
            "- `statement`",
            "- `source_name`",
            "- `source_url`",
            "- `search_query`",
            "- `used_for`",
            "- `notes`",
            "",
            "## Informal Proof Or Disproof Attempt",
            "",
            f"- Theorem statement: {proof_attempt.get('theorem_statement', '')}",
            f"- Route lemma under test: {proof_attempt.get('route_lemma_under_test', '')}",
            f"- Strategy family: {proof_attempt.get('strategy', '')}",
            "",
            "### Informal Tactic Playbook",
            "",
        ]
    )
    playbook = [row for row in proof_attempt.get("informal_tactic_playbook", []) if isinstance(row, dict)]
    if not playbook:
        lines.append("- No tactic playbook recorded.")
        lines.append("")
    else:
        for row in playbook:
            lines.append(f"- `{row.get('tactic_id', '')}` | inspired by {', '.join(row.get('inspired_by', []))}")
            lines.append(f"  Purpose: {row.get('purpose', '')}")
            lines.append(f"  Queue-specific role: {row.get('queue_specific_role', '')}")
        lines.append("")
    lines.extend(
        [
            "### Informal Tactic Trace",
            "",
        ]
    )
    tactic_trace = [row for row in proof_attempt.get("informal_tactic_trace", []) if isinstance(row, dict)]
    if not tactic_trace:
        lines.append("- No tactic trace recorded.")
        lines.append("")
    else:
        for row in tactic_trace:
            lines.append(
                f"- Step {row.get('order', '')}: `{row.get('tactic_id', '')}` | status={row.get('status', '')} | goal={row.get('goal', '')}"
            )
            lines.append(f"  Expected output: {row.get('expected_output', '')}")
            notes = [value for value in row.get("notes", []) if _clean_text(value)] if isinstance(row.get("notes"), list) else []
            for note in notes:
                lines.append(f"  Note: {note}")
        lines.append("")
    lines.extend(
        [
            "### Negative-Route Heuristic",
            "",
        ]
    )
    negative_heuristic = _ensure_dict(proof_attempt.get("negative_route_heuristic"))
    if negative_heuristic:
        lines.extend(
            [
                f"- Decision: {negative_heuristic.get('decision', '')}",
                f"- Recommended: {negative_heuristic.get('recommended', False)}",
                f"- Use negation: {negative_heuristic.get('use_negation', False)}",
                f"- Use contradiction: {negative_heuristic.get('use_contradiction', False)}",
                f"- Use impossibility claim: {negative_heuristic.get('use_impossibility_claim', False)}",
                f"- Score: {negative_heuristic.get('score', 0)}",
                f"- Epistemic principle: {negative_heuristic.get('epistemic_principle', '')}",
                f"- Decision rule: {negative_heuristic.get('decision_rule', '')}",
                f"- Rationale: {negative_heuristic.get('rationale', '')}",
                "",
            ]
        )
        triggers = [row for row in negative_heuristic.get("triggers", []) if _clean_text(row)] if isinstance(negative_heuristic.get("triggers"), list) else []
        anti_triggers = [row for row in negative_heuristic.get("anti_triggers", []) if _clean_text(row)] if isinstance(negative_heuristic.get("anti_triggers"), list) else []
        if triggers:
            lines.append("Triggers:")
            for row in triggers:
                lines.append(f"- {row}")
        if anti_triggers:
            lines.append("Anti-triggers:")
            for row in anti_triggers:
                lines.append(f"- {row}")
        lines.append("")
    else:
        lines.append("- No negative-route heuristic recorded.")
        lines.append("")
    lines.extend(
        [
            "### Contradiction / Impossibility Frame",
            "",
        ]
    )
    contradiction_frame = _ensure_dict(proof_attempt.get("contradiction_frame"))
    if contradiction_frame:
        lines.extend(
            [
                f"- Negative mode: {contradiction_frame.get('negative_mode', '')}",
                f"- Negated claim: {contradiction_frame.get('negated_claim', '')}",
                f"- Contradiction target: {contradiction_frame.get('contradiction_target', '')}",
                f"- Forbidden outcome: {contradiction_frame.get('forbidden_outcome', '')}",
                f"- Impossibility claim template: {contradiction_frame.get('impossibility_claim_template', '')}",
                "",
            ]
        )
    else:
        lines.append("- No contradiction frame recorded.")
        lines.append("")
    lines.extend(
        [
            "Stepwise argument:",
            "",
        ]
    )
    positive_subgoal = _ensure_dict(proof_attempt.get("positive_subgoal_package"))
    lines.extend(
        [
            "Positive subgoal package:",
            "",
        ]
    )
    if not positive_subgoal:
        lines.append("- No constructive subgoal package has been recorded yet.")
        lines.append("")
    else:
        lines.append(f"- Source: {positive_subgoal.get('source', '')}")
        lines.append(f"- Route lemma: {positive_subgoal.get('route_lemma', '')}")
        lines.append(f"- Constructive goal: {positive_subgoal.get('constructive_goal', '')}")
        lines.append(f"- Quantifier signature: {positive_subgoal.get('quantifier_signature', '')}")
        lines.append(f"- LaTeX theorem: {positive_subgoal.get('latex_theorem', '')}")
        lines.append(f"- Lean theorem name: {positive_subgoal.get('lean_theorem_name', '')}")
        lines.append(f"- Witness symbol: {positive_subgoal.get('bridge_witness_symbol', '')}")
        lines.append(f"- Search shapes: {', '.join(_clean_text(value) for value in positive_subgoal.get('search_shapes', []) if _clean_text(value))}")
        lines.append(f"- Positive shapes: {', '.join(_clean_text(value) for value in positive_subgoal.get('positive_shapes', []) if _clean_text(value))}")
        candidate_titles = [
            _clean_text(value)
            for value in positive_subgoal.get("candidate_titles", [])
            if _clean_text(value)
        ] if isinstance(positive_subgoal.get("candidate_titles"), list) else []
        if candidate_titles:
            lines.append(f"- Candidate titles: {' | '.join(candidate_titles)}")
        obligations = [
            _clean_text(value)
            for value in positive_subgoal.get("candidate_obligations", [])
            if _clean_text(value)
        ] if isinstance(positive_subgoal.get("candidate_obligations"), list) else []
        if obligations:
            lines.append("- Candidate obligations:")
            for value in obligations:
                lines.append(f"  - {value}")
        next_steps = [
            _clean_text(value)
            for value in positive_subgoal.get("next_constructive_steps", [])
            if _clean_text(value)
        ] if isinstance(positive_subgoal.get("next_constructive_steps"), list) else []
        if next_steps:
            lines.append("- Next constructive steps:")
            for value in next_steps:
                lines.append(f"  - {value}")
        lines.append("")
    steps = [row for row in proof_attempt.get("stepwise_argument", []) if isinstance(row, dict)]
    if not steps:
        lines.append("- No stepwise argument recorded.")
        lines.append("")
    else:
        for row in steps:
            claim = _clean_text(row.get("claim"))
            justification = _clean_text(row.get("justification"))
            depends_on = [
                _clean_text(value)
                for value in row.get("depends_on", [])
                if _clean_text(value)
            ] if isinstance(row.get("depends_on"), list) else []
            lines.append(f"- Step {row.get('step', '')}: {claim}")
            if justification:
                lines.append(f"  Justification: {justification}")
            if depends_on:
                lines.append(f"  Depends on: {', '.join(depends_on)}")
        lines.append("")
    local_results_used = [
        row for row in proof_attempt.get("local_results_used", [])
        if isinstance(row, dict)
    ] if isinstance(proof_attempt.get("local_results_used"), list) else []
    lines.extend(
        [
            "Local results used:",
            "",
        ]
    )
    if not local_results_used:
        lines.append("- No local InformalMathLib results have been imported into the active proof state.")
        lines.append("")
    else:
        for row in local_results_used:
            label = _clean_text(row.get("title")) or _clean_text(row.get("result_id"))
            role = _clean_text(row.get("role"))
            lines.append(f"- {label} [{_clean_text(row.get('outcome'))}]")
            if role:
                lines.append(f"  Role: {role}")
        lines.append("")
    continuation_log = [
        row for row in proof_attempt.get("continuation_log", [])
        if isinstance(row, dict)
    ] if isinstance(proof_attempt.get("continuation_log"), list) else []
    lines.extend(
        [
            "Continuation log:",
            "",
        ]
    )
    if not continuation_log:
        lines.append("- No continuation passes recorded yet.")
        lines.append("")
    else:
        for row in continuation_log:
            lines.append(
                f"- Stage {row.get('stage', '')}: {_clean_text(row.get('headline'))}"
            )
            for detail in row.get("details", []) if isinstance(row.get("details"), list) else []:
                if _clean_text(detail):
                    lines.append(f"  Detail: {_clean_text(detail)}")
        lines.append("")
    negative_argument = _ensure_dict(proof_attempt.get("negative_argument"))
    lines.extend(
        [
            "Negative-route analysis:",
            "",
            f"- Obstruction candidate: {negative_argument.get('obstruction_candidate', '')}",
            f"- Negated claim: {negative_argument.get('negated_claim', '')}",
            f"- Contradiction target: {negative_argument.get('contradiction_target', '')}",
            f"- Forbidden outcome: {negative_argument.get('forbidden_outcome', '')}",
            f"- Counterexample or barrier: {negative_argument.get('counterexample_or_barrier', '')}",
            f"- Impossibility claim: {negative_argument.get('impossibility_claim', '')}",
            f"- Effect on claim: {negative_argument.get('effect_on_claim', '')}",
            "",
            "## Critique Judges",
            "",
        ]
    )
    for judge in attempt.get("critique_judges", []) if isinstance(attempt.get("critique_judges"), list) else []:
        if not isinstance(judge, dict):
            continue
        lines.append(f"### {judge.get('title', '')}")
        lines.append("")
        for question in judge.get("questions", []) if isinstance(judge.get("questions"), list) else []:
            lines.append(f"- {question}")
        lines.append("")
        lines.append(f"Verdict: {judge.get('verdict', '')}")
        notes = [row for row in judge.get("notes", []) if _clean_text(row)] if isinstance(judge.get("notes"), list) else []
        blockers = [
            row for row in judge.get("blocking_issues", [])
            if _clean_text(row)
        ] if isinstance(judge.get("blocking_issues"), list) else []
        if notes:
            lines.append("Notes:")
            for row in notes:
                lines.append(f"- {row}")
        if blockers:
            lines.append("Blocking issues:")
            for row in blockers:
                lines.append(f"- {row}")
        lines.append("")
    lines.extend(
        [
            "## Final Assessment",
            "",
            f"- Outcome: {final_assessment.get('outcome', '')}",
            f"- Verdict: {final_assessment.get('verdict', '')}",
            f"- Novelty assessment: {final_assessment.get('novelty_assessment', '')}",
            f"- Confidence: {final_assessment.get('confidence', '')}",
            f"- Result statement: {proof_attempt.get('result_statement', '')}",
            f"- Result summary: {proof_attempt.get('result_summary', '') or final_assessment.get('summary', '')}",
            "",
            "## Major Subresult Assessment",
            "",
            "Use this only for terminal `proved` or `disproved` outcomes that might warrant a standalone paper in `artifacts/<kb-ref>/produced_papers`.",
            "",
            "Mandatory gates:",
            f"- Self-contained statement: {gates.get('self_contained_statement', False)}",
            f"- Mathematical inspectability: {gates.get('mathematical_inspectability', False)}",
            f"- Nontrivial frontier relation: {gates.get('nontrivial_frontier_relation', False)}",
            f"- Independent value: {gates.get('independent_value', False)}",
            "",
            "0-3 axis scores:",
            f"- Frontier shift: {axes.get('frontier_shift', 0)}",
            f"- Independence: {axes.get('independence', 0)}",
            f"- Transferability: {axes.get('transferability', 0)}",
            f"- Barrier clarity: {axes.get('barrier_clarity', 0)}",
            f"- Proof closure: {axes.get('proof_closure', 0)}",
            f"- Search compression: {axes.get('search_compression', 0)}",
            "",
            "Threshold rule: all mandatory gates pass, total score >= 11, and at least one of frontier shift / independence / barrier clarity is 3.",
            "",
            f"- Paper candidate title: {major_subresult.get('paper_candidate_title', '')}",
            f"- Paper candidate summary: {major_subresult.get('paper_candidate_summary', '')}",
            f"- Overall judgment: {major_subresult.get('overall_judgment', '')}",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    logger = ReasoningLogger("kb-prove-cycle")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--kb", default="", help="Optional KB markdown path for statement excerpts.")
    ap.add_argument("--kb-ref", default="", help="Optional KB reference override.")
    ap.add_argument("--artifacts-dir", default="", help="Optional artifacts/<kb-ref> path.")
    ap.add_argument("--queue-id", default="", help="Optional specific queue id to consume.")
    ap.add_argument("--queue-json", default="", help="Optional proof-queue JSON path.")
    ap.add_argument("--mathlib-json", default="", help="Optional InformalMathLib index JSON path.")
    ap.add_argument("--attempt-json", default="", help="Optional proof-attempt JSON output path.")
    ap.add_argument("--attempt-md", default="", help="Optional proof-attempt Markdown output path.")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    kb = Path(args.kb) if args.kb else None
    kb_ref = ""
    if kb:
        if not kb.is_absolute():
            kb = (repo_root / kb).resolve()
        kb_ctx = resolve_kb_reference(kb, explicit_kb_ref=args.kb_ref)
        kb_ref = kb_ctx["kb_ref"]
    else:
        kb_ref = _clean_text(args.kb_ref)
    artifacts_dir = Path(args.artifacts_dir) if args.artifacts_dir else (canonical_artifacts_dir(repo_root, kb_ref) if kb_ref else None)
    if artifacts_dir is None:
        raise SystemExit("[ERROR] Provide either --kb or both --kb-ref and --artifacts-dir.")
    if not artifacts_dir.is_absolute():
        artifacts_dir = (repo_root / artifacts_dir).resolve()
    if not kb_ref:
        kb_ref = artifacts_dir.name

    queue_json, queue_md = proof_queue_paths(repo_root, kb_ref)
    mathlib_json, _ = mathlib_paths(repo_root, kb_ref)
    if args.queue_json:
        queue_json = Path(args.queue_json)
    if args.mathlib_json:
        mathlib_json = Path(args.mathlib_json)

    queue = load_proof_queue(queue_json, kb_ref=kb_ref)
    mathlib = load_mathlib_index(mathlib_json, kb_ref=kb_ref)
    mathlib_md = mathlib_json.with_name("catalog.md")
    if not mathlib_json.exists():
        save_mathlib_index(mathlib, json_path=mathlib_json, md_path=mathlib_md)
    attempt_dir = artifacts_dir / "proof-attempts"
    attempt_dir.mkdir(parents=True, exist_ok=True)
    attempt_id = _next_attempt_id(attempt_dir, kb_ref=kb_ref)
    queue_entry = consume_next_entry(queue, attempt_id=attempt_id, queue_id=_clean_text(args.queue_id))
    save_proof_queue(queue, json_path=queue_json, md_path=queue_md)
    refresh_summary_from_sources(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref=kb_ref,
        queue=queue,
        mathlib=mathlib,
    )

    query_terms = [
        _clean_text(queue_entry.get("candidate_object")),
        _clean_text(queue_entry.get("preserved_invariant")),
        _clean_text(queue_entry.get("target_statement_id")),
        _clean_text(queue_entry.get("bridge_id")),
    ]
    mathlib_hits = search_mathlib(mathlib, query_terms, limit=5)
    statement_index = load_statement_index(kb) if kb else {}
    attempt = build_attempt_record(
        attempt_id=attempt_id,
        kb_ref=kb_ref,
        queue_entry=queue_entry,
        mathlib_hits=mathlib_hits,
        statement_index=statement_index,
    )

    attempt_json, attempt_md = _attempt_paths(artifacts_dir, attempt_id)
    if args.attempt_json:
        attempt_json = Path(args.attempt_json)
    if args.attempt_md:
        attempt_md = Path(args.attempt_md)
    attempt_json.parent.mkdir(parents=True, exist_ok=True)
    attempt_json.write_text(json.dumps(attempt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    attempt_md.write_text(render_attempt_markdown(attempt), encoding="utf-8")
    refresh_summary_from_sources(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref=kb_ref,
        queue=queue,
        mathlib=mathlib,
    )

    logger.add_kv("kb_ref", kb_ref)
    logger.add_kv("queue_id", _clean_text(queue_entry.get("queue_id")))
    logger.step(
        "Started proof cycle",
        "\n".join(
            [
                f"kb_ref={kb_ref}",
                f"queue_id={queue_entry.get('queue_id', '')}",
                f"attempt_id={attempt_id}",
                f"mathlib_hits={len(mathlib_hits)}",
            ]
        ),
        surface_focus="proof-attempt-scaffold",
        surface_stage="prove-cycle",
        surface_metrics={"mathlib_hits": len(mathlib_hits)},
        surface_taxonomy={"reasoning_types": ["prove-cycle", "proof-attempt"]},
        surface_pdl={
            "program": _ensure_dict(attempt.get("pdl_program")),
            "operations": [
                {
                    "id": "extract",
                    "detail": "Loaded theorem excerpts, queue commitments, and local InformalMathLib hits into a single proof attempt.",
                },
                {
                    "id": "focus",
                    "detail": "Focused the prove cycle on the route lemma and exact theorem statement under test.",
                },
                {
                    "id": "route",
                    "detail": "Routed one queued conjecture into a tactic-structured proof dossier.",
                },
            ],
            "judgments": [
                {
                    "form": "K ; M |- A : grounded",
                    "detail": "The attempt starts from locally grounded source and target theorem bodies.",
                },
                {
                    "form": "N ; B |- P",
                    "detail": "The selected queue entry has been materialized as a proof-discovery programme.",
                },
            ],
            "control_objects": ["kb", "mathlib", "proof_queue"],
            "epistemic_state": {"mathlib_hits": len(mathlib_hits)},
        },
    )
    logger.add_output("proof_attempt_json", attempt_json)
    logger.add_output("proof_attempt_md", attempt_md)
    logger.add_output("proof_queue_json", queue_json)
    log_path = logger.finalize(
        "success",
        summary=f"Started proof attempt `{attempt_id}` from queue item `{queue_entry.get('queue_id', '')}`.",
    )
    print(f"[OK] Wrote proof attempt JSON: {attempt_json}")
    print(f"[OK] Wrote proof attempt Markdown: {attempt_md}")
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

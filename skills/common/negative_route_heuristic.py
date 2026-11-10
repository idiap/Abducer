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

"""Shared heuristic for deciding when contradiction, negation, or impossibility routes are epistemically justified."""

from __future__ import annotations

from typing import Any


def _clean_text(value: Any) -> str:
    """Normalize free-form values into a stable one-line representation."""

    return " ".join(str(value or "").strip().split())


def _contains_any(text: str, tokens: tuple[str, ...]) -> bool:
    """Check whether the normalized text contains any cue from a token set."""

    lowered = _clean_text(text).lower()
    return any(token in lowered for token in tokens)


def _is_named(text: str) -> bool:
    """Return whether a label is specific enough to count as a named mathematical object."""

    lowered = _clean_text(text).lower()
    return bool(lowered) and lowered not in {"none", "unknown", "n/a", "candidate bridge object"}


def build_negative_route_heuristic(
    *,
    candidate_object: str,
    source_focus: str,
    target_focus: str,
    invariant: str,
    negative_route: str,
    failure_diagnosis: str,
    barrier_scope: str = "",
    missing_route_lemma: str = "",
    carrier_kind: str = "",
) -> dict[str, Any]:
    """Decide whether negative reasoning is epistemically warranted for the current route.

    The heuristic is principled rather than purely stylistic:

    1. Prefer contradiction or impossibility when the route is blocked by a structural defect
       such as a barrier, transport failure, representation mismatch, or unrealized carrier.
    2. Require a precise negated claim and forbidden outcome before leaning on contradiction.
    3. Prefer the negative route when a failure theorem would compress the search space more than
       another speculative constructive variant.
    4. Avoid contradiction-first reasoning when the gap is merely underdeveloped and no sharp
       failure pattern has been localized.
    """

    clean_object = _clean_text(candidate_object)
    clean_source = _clean_text(source_focus)
    clean_target = _clean_text(target_focus)
    clean_invariant = _clean_text(invariant)
    clean_negative = _clean_text(negative_route)
    clean_failure = _clean_text(failure_diagnosis)
    clean_barrier = _clean_text(barrier_scope)
    clean_missing = _clean_text(missing_route_lemma)
    clean_carrier = _clean_text(carrier_kind)

    barrier_pressure = bool(clean_barrier and clean_barrier.lower() != "none")
    contradiction_pressure = _contains_any(
        f"{clean_negative} {clean_failure}",
        ("contradict", "collapse", "inconsisten", "forbidden", "separation"),
    )
    transport_pressure = _contains_any(
        f"{clean_missing} {clean_failure}",
        ("transport", "formula-size", "model shift", "representation shift", "cross-model", "local reduction"),
    )
    non_realization_pressure = (
        _contains_any(clean_object, ("obstruction", "witness", "certificate"))
        or _contains_any(f"{clean_failure} {clean_negative}", ("role-description", "realiz", "topical overlap", "usable carrier"))
    )
    carrier_under_typed = (not clean_carrier) or clean_object.lower().startswith("unspecified")
    precise_negative_target = bool(clean_source and clean_target)
    explicit_failure_probe = bool(clean_negative or clean_failure or clean_missing or barrier_pressure)
    constructive_material_present = bool(clean_object and clean_target and (clean_invariant or clean_missing))

    triggers: list[str] = []
    anti_triggers: list[str] = []
    score = 0

    if barrier_pressure:
        triggers.append(
            f"A named barrier `{clean_barrier}` is already active, so a no-go or impossibility theorem may compress the search space better than another constructive variant."
        )
        score += 4
    if contradiction_pressure:
        triggers.append(
            "The route already names a forbidden collapse or contradiction pattern, so explicit negation is epistemically licensed."
        )
        score += 4
    if transport_pressure:
        triggers.append(
            "The obstruction is a transport or representation failure, which is often sharper to test negatively than to keep refining constructively."
        )
        score += 3
    if non_realization_pressure:
        triggers.append(
            "The current bridge object still risks being only a role-description, so a non-realization theorem would be valuable."
        )
        score += 2
    if carrier_under_typed:
        triggers.append(
            "The carrier remains under-typed or unspecified, which strengthens the case for a non-realization or impossibility route."
        )
        score += 2
    if explicit_failure_probe:
        score += 1
    if precise_negative_target:
        score += 1
    else:
        anti_triggers.append(
            "The route does not yet state a precise source/target pair sharply enough for contradiction-based reasoning."
        )
        score -= 2
    if not explicit_failure_probe:
        anti_triggers.append(
            "No sharp forbidden outcome, barrier, or failure probe has been named, so contradiction would currently be theatrical rather than informative."
        )
        score -= 3
    if constructive_material_present and not (
        barrier_pressure or contradiction_pressure or transport_pressure or non_realization_pressure
    ):
        anti_triggers.append(
            "A constructive route is already materially specified and no structural obstruction has yet been localized sharply enough to override it."
        )
        score -= 1

    if score >= 7 and precise_negative_target and explicit_failure_probe:
        decision = "negative-first"
        epistemic_principle = (
            "A negative route is preferred when it targets a structural obstruction sharply enough to compress the search space more than another constructive refinement."
        )
    elif score >= 4 and precise_negative_target:
        decision = "parallel"
        epistemic_principle = (
            "Constructive and negative routes should run in parallel when the obstruction is real but the positive route still has enough structure to deserve pressure."
        )
    else:
        decision = "constructive-first"
        epistemic_principle = (
            "Contradiction and impossibility should be deferred until the system can name a precise negated claim and a nontrivial forbidden outcome."
        )

    use_negation = decision in {"negative-first", "parallel"} and precise_negative_target
    use_contradiction = use_negation and (barrier_pressure or contradiction_pressure or transport_pressure)
    use_impossibility_claim = use_negation and (
        barrier_pressure or contradiction_pressure or transport_pressure or non_realization_pressure or carrier_under_typed
    )

    rationale_parts: list[str] = []
    if triggers:
        rationale_parts.append(triggers[0])
    if anti_triggers and decision == "constructive-first":
        rationale_parts.append(anti_triggers[0])
    if not rationale_parts:
        rationale_parts.append(
            "No sharp structural obstruction dominates the current route strongly enough to justify contradiction-first reasoning."
        )

    apply_when = [
        "The negated claim can be stated exactly and checked against the same theorem pair as the positive route.",
        "A barrier, transport failure, representation mismatch, or non-realization claim is more informative than another speculative bridge refinement.",
        "A resulting impossibility theorem would eliminate a real slice of the search space rather than only rename current ignorance.",
    ]
    avoid_when = [
        "The route has no precise forbidden outcome, collapse, or barrier target.",
        "The contradiction branch would only restate that a constructive witness is not yet known.",
        "The constructive route is already specific and no structural no-go pattern has been localized.",
    ]

    return {
        "decision": decision,
        "recommended": decision in {"negative-first", "parallel"},
        "use_negation": use_negation,
        "use_contradiction": use_contradiction,
        "use_impossibility_claim": use_impossibility_claim,
        "score": score,
        "epistemic_principle": epistemic_principle,
        "decision_rule": (
            "Apply contradiction/negation/impossibility reasoning only when the route carries a sharp structural obstruction and the negative theorem would compress the search space more than another constructive refinement."
        ),
        "rationale": " ".join(rationale_parts),
        "triggers": triggers,
        "anti_triggers": anti_triggers,
        "apply_when": apply_when,
        "avoid_when": avoid_when,
    }

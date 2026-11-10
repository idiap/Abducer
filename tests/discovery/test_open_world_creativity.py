# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import copy
import itertools
import json
import time
from pathlib import Path
from typing import Any, Callable

import pytest

from agentic.discovery.contracts import (
    canonical_digest,
    stable_identifier,
)
from agentic.discovery.open_world_creativity import (
    BASE_DOMINANCE_DIMENSIONS,
    DEEP_REFLECTION_LENSES,
    MERIT_DIMENSIONS,
    OpenWorldCreativityError,
    bind_branch_terminal_receipt,
    build_branch_intent_manifest,
    build_non_saturating_conceptual_merit_evaluation,
    build_open_world_hard_integrity_receipt,
    build_open_world_maturation_portfolio,
    build_parallel_maturation_barrier_receipt,
    build_pre_taxonomy_invention_freeze,
    classify_frozen_inventions,
    prepare_blinded_conceptual_merit_packet,
    run_isolated_parallel_maturation_branches,
    seal_merit_evaluator_report,
    validate_non_saturating_conceptual_merit_evaluation,
    validate_open_world_hard_integrity_receipt,
)
from agentic.discovery.research_worker_isolation import (
    ResearchWorkerAdapter,
    build_isolation_requirement,
)


def _seal(value: dict[str, Any], field: str) -> dict[str, Any]:
    row = copy.deepcopy(value)
    row[field] = canonical_digest(
        {key: child for key, child in row.items() if key != field}
    )
    return row


def _taxonomy() -> dict[str, Any]:
    return {
        "known_mediator": {
            "name": "Mediator Reconstruction",
            "definition": (
                "Introduce a carrier between descriptions and test its "
                "independent constraints."
            ),
        },
        "known_limit": {
            "name": "Limit Order Reversal",
            "definition": (
                "Reverse an explanatory order while preserving target quantifiers."
            ),
        },
    }


def _raw_invention(index: int) -> dict[str, Any]:
    conjectures = (
        "A finite mediator can carry coercive information without presupposing continuum recovery.",
        "Counterfactual compatibility between world families may select admissible histories before objects.",
        "Noncommuting regulator order may be the obstruction rather than weakness of either estimate.",
    )
    relations = (
        "finite datum constrains a mediator before continuum reconstruction",
        "compatibility selector chooses histories across counterfactual worlds",
        "regulator ordering precedes the continuum boundary operation",
    )
    mechanisms = (
        "Construct the mediator from finite data and transport only invariants that survive its correction.",
        "Compare world-relative constraints and retain histories stable under compatibility transport.",
        "Track both regulator orders and localize the commutator before attempting a limit.",
    )
    return {
        "invention_id": f"invention-{index}",
        "conjecture": conjectures[index],
        "primitive_hunches": [
            relations[index].split()[0] + " primitive",
            f"regime witness family {index}",
        ],
        "relation_hunches": [relations[index]],
        "mechanism_hunch": mechanisms[index],
        "root_tension_contact": (
            "Local construction and global control currently fail to commute."
        ),
        "counterfactual_world": (
            f"In possibility family {index}, objects exist only after the "
            "declared relation is satisfied."
        ),
        "protected_successes": [
            "Preserve the exact target and its finite boundary cases."
        ],
        "risk_if_wrong": (
            "The proposed organization may only redescribe an incumbent obstruction."
        ),
        "upside_if_right": (
            "The relation could unify failures currently treated as independent."
        ),
        "first_falsifier": (
            f"A boundary regime {index} where the relation predicts no new obligation."
        ),
        "correction_path": (
            f"Restrict route {index} to the smallest regime with a discriminating consequence."
        ),
    }


def _freeze() -> dict[str, Any]:
    return build_pre_taxonomy_invention_freeze(
        target_id="yang-mills-target",
        run_id="open-world-run",
        state_version=7,
        target_pressure=(
            "Explain how continuum control could arise without assuming the desired gap."
        ),
        root_contradictions=[
            "Finite coercivity and continuum reconstruction pull in different directions."
        ],
        protected_successes=[
            "Retain exact finite-volume positivity and explicit correction terms."
        ],
        raw_inventions=[_raw_invention(index) for index in range(3)],
        known_taxonomy=_taxonomy(),
        generator_authority_digest=canonical_digest(
            {"generator": "open-world-test"}
        ),
    )


def _decisions() -> list[dict[str, Any]]:
    return [
        {
            "invention_id": "invention-0",
            "status": "mapped_known_corner",
            "known_corner_id": "known_mediator",
            "extension_warrant": None,
        },
        {
            "invention_id": "invention-1",
            "status": "taxonomy_extension_warranted",
            "known_corner_id": None,
            "extension_warrant": {
                "proposed_corner_id": "counterfactual_constraint_ecology",
                "proposed_name": "Counterfactual Constraint Ecology",
                "insufficiency_of_known_taxonomy": (
                    "Existing corners alter one mechanism, whereas this proposal "
                    "changes which constraints coexist across counterfactual worlds."
                ),
                "distinguishing_relations": [
                    "compatibility constraints select histories across counterfactual worlds"
                ],
                "admission_test": (
                    "Admit only if the cross-world compatibility relation changes a named burden."
                ),
                "failure_condition": (
                    "Reject if the proposal reduces to a mediator inserted in one world."
                ),
            },
        },
        {
            "invention_id": "invention-2",
            "status": "mapped_known_corner",
            "known_corner_id": "known_limit",
            "extension_warrant": None,
        },
    ]


def _classification(freeze: dict[str, Any]) -> dict[str, Any]:
    return classify_frozen_inventions(
        freeze,
        known_taxonomy=_taxonomy(),
        decisions=_decisions(),
        classifier_authority_digest=canonical_digest(
            {"classifier": "post-freeze-test"}
        ),
    )


def _semantic_core(index: int) -> dict[str, Any]:
    cores = (
        {
            "primitives": ["finite datum", "coercive mediator"],
            "relations": [
                {
                    "source": "finite datum",
                    "polarity": "constrains",
                    "target": "coercive mediator",
                }
            ],
            "mechanism_steps": [
                "Construct a mediator from finite coercive data.",
                "Transport only invariants stable under mediator correction.",
            ],
            "protected_differences": [
                "Finite positivity remains distinct from continuum reconstruction."
            ],
            "boundary_regimes": [
                "Degenerate finite family where mediator transport becomes identity."
            ],
            "counterfactual_consequence": (
                "A failed transport localizes missing continuum control in the mediator."
            ),
            "falsifier": (
                "A finite regime with stable mediator transport but absent predicted control."
            ),
            "correction_condition": (
                "Restrict the mediator to independently constructible finite regimes."
            ),
        },
        {
            "primitives": [
                "counterfactual world family",
                "compatibility selector",
            ],
            "relations": [
                {
                    "source": "compatibility selector",
                    "polarity": "selects histories across",
                    "target": "counterfactual world family",
                }
            ],
            "mechanism_steps": [
                "Generate rival world-relative constraint families.",
                "Retain histories invariant under compatibility transport.",
            ],
            "protected_differences": [
                "World-relative constraints remain distinct before compatibility comparison."
            ],
            "boundary_regimes": [
                "Single-world boundary where cross-world selection becomes vacuous."
            ],
            "counterfactual_consequence": (
                "Compatibility failure makes admissible histories prior to object reconstruction."
            ),
            "falsifier": (
                "A world family where all histories agree yet reconstruction still bifurcates."
            ),
            "correction_condition": (
                "Restrict compatibility selection to world families sharing exact observables."
            ),
        },
        {
            "primitives": ["regulator ordering", "continuum boundary operation"],
            "relations": [
                {
                    "source": "regulator ordering",
                    "polarity": "precedes noncommutatively",
                    "target": "continuum boundary operation",
                }
            ],
            "mechanism_steps": [
                "Evaluate both regulator orders on the same finite carrier.",
                "Localize their commutator before applying the continuum boundary.",
            ],
            "protected_differences": [
                "Ultraviolet removal and volume growth retain different quantifiers."
            ],
            "boundary_regimes": [
                "Commuting regulator family where the order obstruction vanishes."
            ],
            "counterfactual_consequence": (
                "A nonzero order commutator replaces a direct uniform estimate burden."
            ),
            "falsifier": (
                "Every admissible regulator pair commutes while continuum control still fails."
            ),
            "correction_condition": (
                "Quarantine the order route to regulator pairs with a witnessed commutator."
            ),
        },
        {
            "primitives": ["decorative phrase", "detached ornament"],
            "relations": [
                {
                    "source": "decorative phrase",
                    "polarity": "echoes without constraining",
                    "target": "detached ornament",
                }
            ],
            "mechanism_steps": [
                "Repeat an attractive phrase without an operation.",
                "Leave every declared target decision unchanged.",
            ],
            "protected_differences": [
                "Presentation remains separate from a consequence-bearing mechanism."
            ],
            "boundary_regimes": [
                "Any task regime where decorative repetition has no carrier."
            ],
            "counterfactual_consequence": (
                "Removing the decoration changes no theoretical obligation."
            ),
            "falsifier": (
                "A named decision changes solely because of the decorative relation."
            ),
            "correction_condition": (
                "Supply a consequence-bearing operation or retain quarantine."
            ),
        },
        {
            "primitives": ["boundary comparison", "conservative estimate"],
            "relations": [
                {
                    "source": "boundary comparison",
                    "polarity": "bounds independently",
                    "target": "conservative estimate",
                }
            ],
            "mechanism_steps": [
                "Construct a same-task comparison at the declared boundary.",
                "Derive a conservative estimate without importing the new concepts.",
            ],
            "protected_differences": [
                "The conservative route does not identify finite and continuum obligations."
            ],
            "boundary_regimes": [
                "Boundary family where the comparison estimate is exactly attained."
            ],
            "counterfactual_consequence": (
                "Failure of the estimate returns the programme to a named boundary lemma."
            ),
            "falsifier": (
                "A declared boundary family violates the comparison while all premises hold."
            ),
            "correction_condition": (
                "Narrow the comparison to regimes with an independently proved bound."
            ),
        },
    )
    return copy.deepcopy(cores[index])


_OPERATIONS = {
    "ontological": "retype_source",
    "dialectical": "reverse_relation",
    "genealogical": "trace_origin",
    "modal_explanatory": "counterfactualize_relation",
    "unification": "factor_common_structure",
    "philosophy_of_physics": "identify_physical_carrier",
}


def _physics(index: int, *, quarantined: bool = False) -> dict[str, Any]:
    if quarantined:
        return {
            "status": "quarantined_no_physics_delta",
            "physical_carrier": None,
            "regime_and_quantifiers": None,
            "decision_before": None,
            "proposed_next_decision": None,
            "decision_rationale": (
                "The decorative mechanism changes no named physics decision."
            ),
            "untouched_physics_gates": [
                "continuum construction",
                "positive mass gap",
            ],
            "correction_or_falsifier": (
                "Supply an exact decision-changing relation or retain quarantine."
            ),
        }
    return {
        "status": "decision_changed",
        "physical_carrier": f"regulated comparison carrier {index}",
        "regime_and_quantifiers": (
            f"all finite regulators in declared boundary family {index}"
        ),
        "decision_before": f"attempt direct uniform estimate route {index}",
        "proposed_next_decision": f"first discharge relation-specific burden {index}",
        "decision_rationale": (
            f"The named relation changes which theoretical burden can fail first in route {index}."
        ),
        "untouched_physics_gates": [
            "continuum construction",
            "Osterwalder-Schrader reconstruction",
            "positive mass gap",
        ],
        "correction_or_falsifier": (
            f"Return to the incumbent route if relation-specific burden {index} is absent."
        ),
    }


def _deep_reflection(
    core: dict[str, Any], physics: dict[str, Any]
) -> dict[str, Any]:
    before = core["relations"][0]
    named = (
        f"{before['source']} --{before['polarity']}--> {before['target']}"
    )
    rows: dict[str, Any] = {}
    for lens in DEEP_REFLECTION_LENSES:
        rows[lens] = {
            "named_relation": named,
            "relation_before": copy.deepcopy(before),
            "relation_operation": _OPERATIONS[lens],
            "mutation_status": "changed",
            "relation_after": {
                "source": before["source"],
                "polarity": f"{lens} reframes",
                "target": before["target"],
            },
            "exposed_assumption": (
                f"The {lens} pass exposes why this exact relation was treated as primitive."
            ),
            "strongest_opposition": (
                f"The strongest opposition says the {lens} mutation changes vocabulary only."
            ),
            "conceptual_mutation": (
                f"The {lens} operation changes the relation while preserving its named endpoints."
            ),
            "consequence": (
                f"The {lens} mutation changes which declared theoretical obligation comes next."
            ),
            "boundary_or_correction": core["correction_condition"],
            "semantic_core_correction_link": core["correction_condition"],
            "physics_handback_link": physics["correction_or_falsifier"],
        }
    return rows


def _matured(index: int, branch_id: str) -> dict[str, Any]:
    core = _semantic_core(index)
    physics = _physics(index, quarantined=index == 3)
    return {
        "invention_id": f"invention-{index}",
        "branch_id": branch_id,
        "exploration_role": "wildcard" if index == 1 else "candidate",
        "statement": (
            f"A relation-bearing worldview {index} reorganizes the target burden."
        ),
        "semantic_core": core,
        "deep_reflection": _deep_reflection(core, physics),
        "risk_reward": {
            "risk_case": (
                f"Route {index} may relocate the burden without making it tractable."
            ),
            "high_upside_case": (
                f"Route {index} could unify distinct failures without erasing their regimes."
            ),
            "learning_if_false": (
                f"Failure of route {index} localizes which relation cannot bear the explanation."
            ),
            "cost_of_unification": (
                f"Route {index} adds a law whose noncircularity must be established."
            ),
            "wildcard_reason": (
                "A cross-world constraint ecology probes a conceptual corner outside the known atlas."
                if index == 1
                else None
            ),
        },
        "physics_handback": physics,
    }


def _content(row: dict[str, Any]) -> dict[str, Any]:
    return {
        key: copy.deepcopy(row[key])
        for key in (
            "statement",
            "semantic_core",
            "deep_reflection",
            "risk_reward",
            "physics_handback",
        )
    }


def _maturation_questions() -> dict[str, str]:
    return {
        f"invention-{index}": (
            f"Which exact relation makes route {index} more than a renamed obstruction?"
        )
        for index in range(3)
    }


def _matured_proposals(freeze: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        _matured(
            index,
            stable_identifier(
                "open-world-branch", freeze["freeze_id"], f"invention-{index}"
            ),
        )
        for index in range(3)
    ]


def _branch_records(
    freeze: dict[str, Any], classification: dict[str, Any], run_root: Path
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    matured = _matured_proposals(freeze)
    records, _barrier = run_isolated_parallel_maturation_branches(
        freeze,
        classification,
        known_taxonomy=_taxonomy(),
        matured_inventions=matured,
        maturation_questions=_maturation_questions(),
        run_root=run_root,
    )
    return records, matured


def _portfolio_bundle(run_root: Path) -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    freeze = _freeze()
    classification = _classification(freeze)
    records, matured = _branch_records(freeze, classification, run_root)
    barrier = build_parallel_maturation_barrier_receipt(
        freeze,
        classification,
        known_taxonomy=_taxonomy(),
        branch_execution_records=records,
    )
    portfolio = build_open_world_maturation_portfolio(
        freeze,
        classification,
        known_taxonomy=_taxonomy(),
        matured_inventions=matured,
        branch_execution_records=records,
        parallel_barrier_receipt=barrier,
    )
    integrity = build_open_world_hard_integrity_receipt(
        portfolio,
        freeze=freeze,
        classification=classification,
        known_taxonomy=_taxonomy(),
    )
    return freeze, classification, portfolio, integrity


def _controls(portfolio: dict[str, Any]) -> list[dict[str, Any]]:
    source = portfolio["matured_inventions"][0]
    restatement = _content(source)
    restatement["statement"] = (
        "Equivalent prose presents the same mechanism, reflection, risk, and handback."
    )
    sham_source = _matured(3, "control-sham-branch")
    capable_source = _matured(4, "control-capable-branch")
    return [
        {
            "control_id": "control-capable",
            "control_kind": "capable",
            "source_invention_id": None,
            "target_id": portfolio["target_id"],
            "content": _content(capable_source),
        },
        {
            "control_id": "control-restatement",
            "control_kind": "restatement",
            "source_invention_id": source["invention_id"],
            "target_id": portfolio["target_id"],
            "content": restatement,
        },
        {
            "control_id": "control-sham",
            "control_kind": "sham",
            "source_invention_id": source["invention_id"],
            "target_id": portfolio["target_id"],
            "content": _content(sham_source),
        },
    ]


def _blind_bundle(
    portfolio: dict[str, Any],
    integrity: dict[str, Any],
    *,
    nonce: str = "sealed-study-nonce",
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    controls = _controls(portfolio)
    blind, private = prepare_blinded_conceptual_merit_packet(
        portfolio,
        controls=controls,
        hard_integrity_receipt=integrity,
        counterbalance_nonce=nonce,
    )
    return controls, blind, private


def _reports(
    blind: dict[str, Any],
    private: dict[str, Any],
    controls: list[dict[str, Any]],
    *,
    evaluator_count: int = 3,
    saturated: bool = False,
    uncertain_pair: tuple[str, str, str] | None = None,
    cycle_orders: list[list[str]] | None = None,
) -> list[dict[str, Any]]:
    binding = {
        row["candidate_alias"]: row for row in private["bindings"]
    }
    alias_by_source = {
        row["source_id"]: row["candidate_alias"] for row in private["bindings"]
    }
    control_by_id = {row["control_id"]: row for row in controls}
    base_priority = {"invention-0": 3, "invention-2": 2, "invention-1": 1}

    def verdict(
        left: str, right: str, dimension: str, evaluator_index: int
    ) -> str:
        if saturated:
            return "tie"
        left_binding = binding[left]
        right_binding = binding[right]
        if (
            uncertain_pair is not None
            and dimension == uncertain_pair[2]
            and {
                left_binding["source_id"],
                right_binding["source_id"],
            }
            == {uncertain_pair[0], uncertain_pair[1]}
        ):
            return "insufficient"
        if (
            left_binding["source_kind"]
            == right_binding["source_kind"]
            == "invention"
        ):
            if cycle_orders is not None:
                order = cycle_orders[evaluator_index]
                winner_id = min(
                    (left_binding["source_id"], right_binding["source_id"]),
                    key=order.index,
                )
            elif (
                dimension == "high_risk_upside"
                and "invention-1"
                in {left_binding["source_id"], right_binding["source_id"]}
            ):
                winner_id = "invention-1"
            else:
                winner_id = max(
                    (left_binding["source_id"], right_binding["source_id"]),
                    key=lambda item: base_priority[item],
                )
            winner_alias = alias_by_source[winner_id]
            return "left" if winner_alias == left else "right"
        if {
            left_binding["source_kind"],
            right_binding["source_kind"],
        } == {"invention", "control"}:
            control = (
                left_binding
                if left_binding["source_kind"] == "control"
                else right_binding
            )
            invention = (
                right_binding
                if left_binding["source_kind"] == "control"
                else left_binding
            )
            control_row = control_by_id[control["source_id"]]
            if (
                control["control_kind"] == "restatement"
                and control_row["source_invention_id"] == invention["source_id"]
            ):
                return "tie"
            if (
                control["control_kind"] == "sham"
                and control_row["source_invention_id"] == invention["source_id"]
            ):
                return "left" if invention["candidate_alias"] == left else "right"
            return "tie"
        if (
            left_binding["source_kind"]
            == right_binding["source_kind"]
            == "control"
        ):
            kinds = {
                left_binding["control_kind"],
                right_binding["control_kind"],
            }
            if kinds == {"capable", "sham"}:
                winner_alias = next(
                    row["candidate_alias"]
                    for row in (left_binding, right_binding)
                    if row["control_kind"] == "capable"
                )
                return "left" if winner_alias == left else "right"
        return "tie"

    aliases = sorted(binding)
    reports: list[dict[str, Any]] = []
    for evaluator_index in range(evaluator_count):
        comparisons = []
        by_key: dict[tuple[str, str, str], str] = {}
        for left, right in itertools.combinations(aliases, 2):
            for dimension in MERIT_DIMENSIONS:
                row_verdict = verdict(
                    left, right, dimension, evaluator_index
                )
                by_key[(left, right, dimension)] = row_verdict
                comparisons.append(
                    {
                        "left_alias": left,
                        "right_alias": right,
                        "dimension": dimension,
                        "verdict": row_verdict,
                        "left_warrant_paths": [
                            "/semantic_core/mechanism_steps/0"
                        ],
                        "right_warrant_paths": [
                            "/semantic_core/mechanism_steps/0"
                        ],
                        "rationale": (
                            "The verdict follows the consequence-bearing mechanism for this dimension."
                        ),
                        "strongest_objection": (
                            "The apparent difference may disappear under an equivalent presentation."
                        ),
                        "correction_test": (
                            "Swap semantic content while holding aliases fixed and follow content."
                        ),
                    }
                )
        best_worst = []
        for dimension in MERIT_DIMENSIONS:
            if saturated:
                best_id, worst_id = "invention-0", "control-sham"
            elif cycle_orders is not None:
                best_id, worst_id = "control-capable", "control-sham"
            elif dimension == "high_risk_upside":
                best_id, worst_id = "invention-1", "control-sham"
            else:
                best_id, worst_id = "invention-0", "control-sham"
            best_worst.append(
                {
                    "dimension": dimension,
                    "best_alias": alias_by_source[best_id],
                    "worst_alias": alias_by_source[worst_id],
                    "best_warrant_paths": [
                        "/semantic_core/mechanism_steps/0"
                    ],
                    "worst_warrant_paths": [
                        "/semantic_core/mechanism_steps/0"
                    ],
                    "rationale": (
                        "The selected endpoints expose the strongest categorical contrast."
                    ),
                    "strongest_objection": (
                        "A different equivalent presentation could alter apparent salience."
                    ),
                    "correction_test": (
                        "Reblind and require the endpoint choice to follow content."
                    ),
                }
            )
        reports.append(
            seal_merit_evaluator_report(
                blind,
                evaluator_id=f"internal-evaluator-{evaluator_index}",
                evaluator_authority_digest=canonical_digest(
                    {"internal-evaluator": evaluator_index}
                ),
                comparisons=comparisons,
                best_worst_choices=best_worst,
            )
        )
    return reports


def _evaluation(
    portfolio: dict[str, Any],
    integrity: dict[str, Any],
    *,
    nonce: str = "evaluation-nonce",
    reports_factory: Callable[
        [dict[str, Any], dict[str, Any], list[dict[str, Any]]],
        list[dict[str, Any]],
    ]
    | None = None,
) -> dict[str, Any]:
    controls, blind, private = _blind_bundle(
        portfolio, integrity, nonce=nonce
    )
    reports = (
        reports_factory(blind, private, controls)
        if reports_factory is not None
        else _reports(blind, private, controls)
    )
    return build_non_saturating_conceptual_merit_evaluation(
        portfolio,
        controls=controls,
        hard_integrity_receipt=integrity,
        blind_packet=blind,
        private_binding=private,
        evaluator_reports=reports,
    )


def test_pre_taxonomy_freeze_rejects_taxonomy_vocabulary() -> None:
    raw = [_raw_invention(index) for index in range(3)]
    raw[0]["conjecture"] = (
        "Mediator Reconstruction should be selected because the atlas names it."
    )
    with pytest.raises(OpenWorldCreativityError) as error:
        build_pre_taxonomy_invention_freeze(
            target_id="target",
            run_id="run",
            state_version=0,
            target_pressure="A substantive target pressure remains unexplained.",
            root_contradictions=["Two exact obligations currently conflict."],
            protected_successes=[
                "Preserve the incumbent exact boundary result."
            ],
            raw_inventions=raw,
            known_taxonomy=_taxonomy(),
            generator_authority_digest=canonical_digest({"g": 1}),
        )
    assert error.value.reason_code == "pre_freeze_taxonomy_leak"


def test_taxonomy_extension_replay_rejects_renaming_and_ungrounded_warrant() -> None:
    freeze = _freeze()
    decisions = _decisions()
    decisions[1]["extension_warrant"]["proposed_name"] = "Mediator Reconstructions"
    decisions[1]["extension_warrant"]["distinguishing_relations"] = [
        "mediator carries descriptions under independent constraints"
    ]
    with pytest.raises(OpenWorldCreativityError) as renamed:
        classify_frozen_inventions(
            freeze,
            known_taxonomy=_taxonomy(),
            decisions=decisions,
            classifier_authority_digest=canonical_digest({"classifier": 1}),
        )
    assert renamed.value.reason_code in {
        "taxonomy_extension_renaming",
        "taxonomy_extension_subsumed",
    }

    decisions = _decisions()
    decisions[1]["extension_warrant"]["distinguishing_relations"] = [
        "unrelated thermodynamic entropy balances an external reservoir"
    ]
    with pytest.raises(OpenWorldCreativityError) as ungrounded:
        classify_frozen_inventions(
            freeze,
            known_taxonomy=_taxonomy(),
            decisions=decisions,
            classifier_authority_digest=canonical_digest({"classifier": 2}),
        )
    assert ungrounded.value.reason_code == "taxonomy_extension_ungrounded"


def test_nonredundancy_rejects_subsumed_one_token_decoration(tmp_path: Path) -> None:
    freeze = _freeze()
    classification = _classification(freeze)
    matured = _matured_proposals(freeze)
    matured[1]["semantic_core"] = copy.deepcopy(matured[0]["semantic_core"])
    matured[1]["semantic_core"]["mechanism_steps"].append(
        "Add one decorative flourish without changing the mechanism."
    )
    core = matured[1]["semantic_core"]
    matured[1]["deep_reflection"] = _deep_reflection(
        core, matured[1]["physics_handback"]
    )
    records, barrier = run_isolated_parallel_maturation_branches(
        freeze,
        classification,
        known_taxonomy=_taxonomy(),
        matured_inventions=matured,
        maturation_questions=_maturation_questions(),
        run_root=tmp_path,
    )
    with pytest.raises(OpenWorldCreativityError) as error:
        build_open_world_maturation_portfolio(
            freeze,
            classification,
            known_taxonomy=_taxonomy(),
            matured_inventions=matured,
            branch_execution_records=records,
            parallel_barrier_receipt=barrier,
        )
    assert error.value.reason_code == "matured_semantic_subsumption"


def test_lens_requires_specific_relation_operation_correction_and_handback(
    tmp_path: Path,
) -> None:
    freeze = _freeze()
    classification = _classification(freeze)
    matured = _matured_proposals(freeze)
    matured[0]["deep_reflection"]["ontological"][
        "relation_operation"
    ] = "trace_origin"
    with pytest.raises(OpenWorldCreativityError) as mismatch:
        run_isolated_parallel_maturation_branches(
            freeze,
            classification,
            known_taxonomy=_taxonomy(),
            matured_inventions=matured,
            maturation_questions=_maturation_questions(),
            run_root=tmp_path / "lens-mismatch",
        )
    assert mismatch.value.reason_code == "deep_reflection_lens_mismatch"

    matured = _matured_proposals(freeze)
    matured[0]["deep_reflection"]["ontological"][
        "physics_handback_link"
    ] = "A plausible but unbound handback sentence."
    with pytest.raises(OpenWorldCreativityError) as unbound:
        run_isolated_parallel_maturation_branches(
            freeze,
            classification,
            known_taxonomy=_taxonomy(),
            matured_inventions=matured,
            maturation_questions=_maturation_questions(),
            run_root=tmp_path / "handback-mismatch",
        )
    assert unbound.value.reason_code == "deep_reflection_handback_unbound"


def test_worker_response_and_terminal_barrier_are_exactly_bound(tmp_path: Path) -> None:
    freeze, classification, portfolio, integrity = _portfolio_bundle(tmp_path)
    validate_open_world_hard_integrity_receipt(
        integrity, portfolio=portfolio
    )
    tampered = copy.deepcopy(portfolio)
    tampered["matured_inventions"][0]["statement"] += " altered"
    tampered["matured_inventions"][0]["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in tampered["matured_inventions"][0].items()
            if key
            not in {
                "semantic_core_digest",
                "content_digest",
                "worker_response_sha256",
                "branch_record_digest",
                "barrier_receipt_digest",
            }
        }
    )
    tampered = _seal(tampered, "content_digest")
    with pytest.raises(OpenWorldCreativityError) as response_error:
        validate_open_world_hard_integrity_receipt(
            integrity, portfolio=tampered
        )
    assert response_error.value.reason_code in {
        "worker_response_binding_mismatch",
        "hard_integrity_replay_mismatch",
    }

    records = copy.deepcopy(portfolio["branch_execution_records"])
    records[0]["terminal_receipt"]["response_sha256"] = canonical_digest(
        {"wrong": "response"}
    )
    with pytest.raises(OpenWorldCreativityError) as receipt_error:
        build_parallel_maturation_barrier_receipt(
            freeze,
            classification,
            known_taxonomy=_taxonomy(),
            branch_execution_records=records,
        )
    assert receipt_error.value.reason_code in {
        "digest_mismatch",
        "worker_payload_binding_mismatch",
        "terminal_receipt_binding_mismatch",
    }


def test_controls_are_exact_same_task_and_substantive(tmp_path: Path) -> None:
    _freeze_artifact, _classification_artifact, portfolio, integrity = (
        _portfolio_bundle(tmp_path)
    )
    controls = _controls(portfolio)
    with pytest.raises(OpenWorldCreativityError) as missing:
        prepare_blinded_conceptual_merit_packet(
            portfolio,
            controls=controls[:-1],
            hard_integrity_receipt=integrity,
            counterbalance_nonce="missing-control",
        )
    assert missing.value.reason_code == "control_incomplete"

    wrong_target = copy.deepcopy(controls)
    wrong_target[0]["target_id"] = "another-target"
    with pytest.raises(OpenWorldCreativityError) as target:
        prepare_blinded_conceptual_merit_packet(
            portfolio,
            controls=wrong_target,
            hard_integrity_receipt=integrity,
            counterbalance_nonce="wrong-target",
        )
    assert target.value.reason_code == "control_target_mismatch"

    changed_restatement = copy.deepcopy(controls)
    changed_restatement[1]["content"]["physics_handback"][
        "decision_rationale"
    ] += " changed"
    with pytest.raises(OpenWorldCreativityError) as restatement:
        prepare_blinded_conceptual_merit_packet(
            portfolio,
            controls=changed_restatement,
            hard_integrity_receipt=integrity,
            counterbalance_nonce="bad-restatement",
        )
    assert restatement.value.reason_code == "restatement_control_invalid"

    promoted_sham = copy.deepcopy(controls)
    promoted_sham[2]["content"] = copy.deepcopy(controls[0]["content"])
    with pytest.raises(OpenWorldCreativityError) as sham:
        prepare_blinded_conceptual_merit_packet(
            portfolio,
            controls=promoted_sham,
            hard_integrity_receipt=integrity,
            counterbalance_nonce="bad-sham",
        )
    assert sham.value.reason_code == "sham_control_invalid"


def test_blind_packet_replays_exact_sources_and_hides_roles(tmp_path: Path) -> None:
    _freeze_artifact, _classification_artifact, portfolio, integrity = (
        _portfolio_bundle(tmp_path)
    )
    controls, blind, private = _blind_bundle(portfolio, integrity)
    rendered = repr(blind).casefold()
    assert "control-restatement" not in rendered
    assert "control-sham" not in rendered
    assert "control-capable" not in rendered
    assert "wildcard_reason" not in rendered
    assert "wildcard" not in rendered

    forged_private = copy.deepcopy(private)
    invention_bindings = [
        row
        for row in forged_private["bindings"]
        if row["source_kind"] == "invention"
    ]
    candidate_binding = next(
        row for row in invention_bindings if row["exploration_role"] == "candidate"
    )
    wildcard_binding = next(
        row for row in invention_bindings if row["exploration_role"] == "wildcard"
    )
    # Select by semantic role rather than packet position: counterbalancing may put
    # two candidates first, which would turn a positional role swap into a no-op.
    candidate_binding["exploration_role"], wildcard_binding["exploration_role"] = (
        wildcard_binding["exploration_role"],
        candidate_binding["exploration_role"],
    )
    forged_private = _seal(forged_private, "binding_digest")
    with pytest.raises(OpenWorldCreativityError) as role_swap:
        build_non_saturating_conceptual_merit_evaluation(
            portfolio,
            controls=controls,
            hard_integrity_receipt=integrity,
            blind_packet=blind,
            private_binding=forged_private,
            evaluator_reports=_reports(blind, private, controls),
        )
    assert role_swap.value.reason_code == "blind_packet_binding_mismatch"

    forged_blind = copy.deepcopy(blind)
    forged_blind["candidates"][0]["content"]["statement"] += " forged"
    forged_blind["candidates"][0]["content_digest"] = canonical_digest(
        forged_blind["candidates"][0]["content"]
    )
    forged_blind = _seal(forged_blind, "packet_digest")
    with pytest.raises(OpenWorldCreativityError) as content_swap:
        build_non_saturating_conceptual_merit_evaluation(
            portfolio,
            controls=controls,
            hard_integrity_receipt=integrity,
            blind_packet=forged_blind,
            private_binding=private,
            evaluator_reports=_reports(blind, private, controls),
        )
    assert content_swap.value.reason_code == "blind_packet_binding_mismatch"


def test_best_worst_is_required_and_pairwise_consistent(tmp_path: Path) -> None:
    _freeze_artifact, _classification_artifact, portfolio, integrity = (
        _portfolio_bundle(tmp_path)
    )
    controls, blind, private = _blind_bundle(portfolio, integrity)
    reports = _reports(blind, private, controls)
    report = reports[0]
    with pytest.raises(OpenWorldCreativityError) as missing:
        seal_merit_evaluator_report(
            blind,
            evaluator_id="missing-best-worst",
            evaluator_authority_digest=canonical_digest({"judge": 1}),
            comparisons=report["comparisons"],
            best_worst_choices=report["best_worst_choices"][:-1],
        )
    assert missing.value.reason_code == "best_worst_coverage_invalid"

    inconsistent = copy.deepcopy(report["best_worst_choices"])
    choice = next(
        row
        for row in inconsistent
        if row["dimension"] == "essential_relevance"
    )
    choice["best_alias"], choice["worst_alias"] = (
        choice["worst_alias"],
        choice["best_alias"],
    )
    with pytest.raises(OpenWorldCreativityError) as conflict:
        seal_merit_evaluator_report(
            blind,
            evaluator_id="inconsistent-best-worst",
            evaluator_authority_digest=canonical_digest({"judge": 2}),
            comparisons=report["comparisons"],
            best_worst_choices=inconsistent,
        )
    assert conflict.value.reason_code == "best_worst_pairwise_inconsistent"


def test_per_dimension_discrimination_rejects_saturation(tmp_path: Path) -> None:
    _freeze_artifact, _classification_artifact, portfolio, integrity = (
        _portfolio_bundle(tmp_path)
    )
    controls, blind, private = _blind_bundle(
        portfolio, integrity, nonce="saturation-probe"
    )
    with pytest.raises(OpenWorldCreativityError) as error:
        build_non_saturating_conceptual_merit_evaluation(
            portfolio,
            controls=controls,
            hard_integrity_receipt=integrity,
            blind_packet=blind,
            private_binding=private,
            evaluator_reports=_reports(
                blind, private, controls, saturated=True
            ),
        )
    assert error.value.reason_code == "merit_dimension_non_discriminating"


def test_uncertainty_blocks_dominance_and_is_typed_incomparable(tmp_path: Path) -> None:
    _freeze_artifact, _classification_artifact, portfolio, integrity = (
        _portfolio_bundle(tmp_path)
    )
    evaluation = _evaluation(
        portfolio,
        integrity,
        nonce="uncertainty-probe",
        reports_factory=lambda blind, private, controls: _reports(
            blind,
            private,
            controls,
            uncertain_pair=(
                "invention-1",
                "invention-2",
                "essential_relevance",
            ),
        ),
    )
    by_id = {
        row["invention_id"]: row
        for row in evaluation["exploration_dispositions"]
    }
    assert by_id["invention-1"]["status"] == "uncertainty_incomparable"
    assert by_id["invention-1"]["dominated_by_aliases"] == []
    relation = next(
        row
        for row in evaluation["pareto_relations"]
        if {
            row["left_alias"],
            row["right_alias"],
        }
        == {
            next(
                binding["candidate_alias"]
                for binding in evaluation["unblinding_receipt"]["bindings"]
                if binding["source_id"] == "invention-1"
            ),
            next(
                binding["candidate_alias"]
                for binding in evaluation["unblinding_receipt"]["bindings"]
                if binding["source_id"] == "invention-2"
            ),
        }
    )
    assert relation["status"] == "uncertainty_incomparable"
    assert relation["blocking_dimensions"] == ["essential_relevance"]


def test_plurality_dominance_cycle_is_not_frontier_authority(tmp_path: Path) -> None:
    _freeze_artifact, _classification_artifact, portfolio, integrity = (
        _portfolio_bundle(tmp_path)
    )
    orders = [
        ["invention-0", "invention-1", "invention-2"],
        ["invention-0", "invention-1", "invention-2"],
        ["invention-1", "invention-2", "invention-0"],
        ["invention-1", "invention-2", "invention-0"],
        ["invention-2", "invention-0", "invention-1"],
    ]
    evaluation = _evaluation(
        portfolio,
        integrity,
        nonce="cycle-probe",
        reports_factory=lambda blind, private, controls: _reports(
            blind,
            private,
            controls,
            evaluator_count=5,
            cycle_orders=orders,
        ),
    )
    assert len(evaluation["dominance_cycles"]) == 1
    assert {
        row["status"] for row in evaluation["exploration_dispositions"]
    } == {"dominance_cycle_incomparable"}


def test_wildcard_is_preserved_without_scalar_and_replay_is_exact(tmp_path: Path) -> None:
    _freeze_artifact, _classification_artifact, portfolio, integrity = (
        _portfolio_bundle(tmp_path)
    )
    evaluation = _evaluation(portfolio, integrity, nonce="wildcard-probe")
    validate_non_saturating_conceptual_merit_evaluation(evaluation)
    wildcard = next(
        row
        for row in evaluation["exploration_dispositions"]
        if row["invention_id"] == "invention-1"
    )
    assert wildcard["status"] == "protected_high_upside_wildcard"
    assert wildcard["dominated_by_aliases"]
    assert wildcard["high_upside_against_a_dominator"] == "yes"
    assert evaluation["merit_protocol"][
        "base_dominance_dimensions"
    ] == list(BASE_DOMINANCE_DIMENSIONS)
    assert {
        row["dissent_status"]
        for row in evaluation["best_worst_consensus"]
    } == {"unanimous"}

    forbidden = {
        "aggregate_score",
        "score",
        "rating",
        "weighted_sum",
        "total",
    }

    def keys(value: Any) -> set[str]:
        if isinstance(value, dict):
            return set(value) | set().union(
                *(keys(child) for child in value.values())
            )
        if isinstance(value, list):
            return set().union(*(keys(child) for child in value), set())
        return set()

    assert not forbidden.intersection(keys(evaluation))

    forged = copy.deepcopy(evaluation)
    forged["unblinding_receipt"]["packet_digest"] = canonical_digest(
        {"wrong": "packet"}
    )
    forged["unblinding_receipt"] = _seal(
        forged["unblinding_receipt"], "binding_digest"
    )
    forged = _seal(forged, "content_digest")
    with pytest.raises(OpenWorldCreativityError) as replay:
        validate_non_saturating_conceptual_merit_evaluation(forged)
    assert replay.value.reason_code == "blind_packet_binding_mismatch"


def test_every_creativity_merit_and_integrity_authority_remains_null(
    tmp_path: Path,
) -> None:
    freeze, _classification_artifact, portfolio, integrity = (
        _portfolio_bundle(tmp_path)
    )
    evaluation = _evaluation(portfolio, integrity, nonce="authority-null")
    assert freeze["authority_nulls"]["creativity_authority"] == "unavailable"
    assert set(portfolio["authority_nulls"].values()) == {"unavailable"}
    assert set(integrity["authority_nulls"].values()) == {"unavailable"}
    assert set(evaluation["authority_nulls"].values()) == {
        "unavailable",
        "internal_exploration_only",
    }


def test_registered_receipt_files_are_authoritative_and_fabrication_fails(
    tmp_path: Path,
) -> None:
    freeze = _freeze()
    classification = _classification(freeze)
    records, _matured = _branch_records(freeze, classification, tmp_path)
    first = records[0]
    terminal = first["terminal_receipt"]
    run_directory = Path(terminal["run_directory"])
    receipt_path = run_directory / terminal["worker_receipt_ref"]
    request_path = run_directory / terminal["request_evidence"]["ref"]
    response_path = run_directory / terminal["response_evidence"]["ref"]
    assert receipt_path.is_file()
    assert request_path.is_file()
    assert response_path.is_file()

    forged = json.loads(receipt_path.read_text(encoding="utf-8"))
    forged["process_status"] = "worker_failed"
    with pytest.raises(OpenWorldCreativityError) as error:
        bind_branch_terminal_receipt(
            {"intent": first["intent"], "manifest": first["manifest"]},
            research_worker_receipt=forged,
        )
    assert error.value.reason_code == "terminal_receipt_binding_mismatch"


def test_late_evidence_write_and_nonterminal_barrier_fail_closed(tmp_path: Path) -> None:
    freeze = _freeze()
    classification = _classification(freeze)
    records, _matured = _branch_records(freeze, classification, tmp_path)

    nonterminal = copy.deepcopy(records)
    nonterminal[0]["terminal_receipt"]["process_group_status"] = "running"
    nonterminal[0] = _seal(nonterminal[0], "record_digest")
    with pytest.raises(OpenWorldCreativityError) as lifecycle:
        build_parallel_maturation_barrier_receipt(
            freeze,
            classification,
            known_taxonomy=_taxonomy(),
            branch_execution_records=nonterminal,
        )
    assert lifecycle.value.reason_code == "terminal_receipt_binding_mismatch"

    terminal = records[0]["terminal_receipt"]
    response_path = Path(terminal["run_directory"]) / terminal["response_evidence"]["ref"]
    response_path.write_bytes(response_path.read_bytes() + b" ")
    with pytest.raises(OpenWorldCreativityError) as late_write:
        build_parallel_maturation_barrier_receipt(
            freeze,
            classification,
            known_taxonomy=_taxonomy(),
            branch_execution_records=records,
        )
    assert late_write.value.reason_code == "worker_payload_binding_mismatch"


def _probe_adapter(
    tmp_path: Path,
    *,
    study_id: str,
) -> ResearchWorkerAdapter:
    return ResearchWorkerAdapter(
        study_id=study_id,
        run_root=tmp_path,
        worker_script=(
            Path(__file__).resolve().parents[2]
            / "agentic"
            / "scripts"
            / "run_open_world_maturation_worker.py"
        ),
    )


def _probe_request(
    adapter: ResearchWorkerAdapter,
    freeze: dict[str, Any],
    classification: dict[str, Any],
    *,
    adversarial_probe: dict[str, Any],
    budget: dict[str, Any] | None = None,
) -> dict[str, Any]:
    requirement = build_isolation_requirement(
        adapter.backend, require_kernel_isolation=False
    )
    intent_manifest = build_branch_intent_manifest(
        freeze,
        classification,
        invention_id="invention-0",
        workspace_ref="branches/adversarial-invention-0",
        maturation_question=_maturation_questions()["invention-0"],
        isolation_requirement=requirement,
    )
    intent = intent_manifest["intent"]
    manifest = intent_manifest["manifest"]
    matured = _matured(0, intent["branch_id"])
    return adapter.invoke(
        role="high_risk",
        operation="parallel_maturation",
        invocation_context={
            "branch_id": intent["branch_id"],
            "invention_id": intent["invention_id"],
            "intent_digest": intent["intent_digest"],
            "manifest_digest": manifest["manifest_digest"],
        },
        payload={
            "branch_request": intent_manifest,
            "matured_response": matured,
            "minimum_residency_seconds": 0.02,
            "adversarial_probe": adversarial_probe,
        },
        budget=budget,
    )


def test_sibling_read_write_probe_is_kernel_enforced_or_truthfully_denied_authority(
    tmp_path: Path,
) -> None:
    freeze = _freeze()
    classification = _classification(freeze)
    adapter = _probe_adapter(tmp_path, study_id="open-world-sibling-probe")
    sibling_root = adapter.run_directory / "sibling-attempt"
    sibling_root.mkdir(parents=True)
    sibling_secret = sibling_root / "secret.txt"
    sibling_secret.write_text("sibling-secret", encoding="utf-8")
    sibling_write = sibling_root / "forbidden-write.txt"
    receipt = _probe_request(
        adapter,
        freeze,
        classification,
        adversarial_probe={
            "sibling_read_path": str(sibling_secret),
            "sibling_write_path": str(sibling_write),
            "late_write_path": None,
            "spawn_late_descendant": False,
        },
    )
    assert receipt["outcome_status"] == "accepted"
    observation = receipt["response_payload"]["output"]["access_observation"]
    channels = receipt["isolation_assurance"]["channels"]
    if (
        channels["filesystem_read"]
        == "kernel_sibling_run_data_denied_host_read_scope_unrestricted"
    ):
        assert observation["sibling_read_succeeded"] is False
    else:
        assert channels["filesystem_read"] == "host_read_scope_unrestricted"
    if channels["filesystem_write"] == "kernel_workspace_only":
        assert observation["sibling_write_succeeded"] is False
        assert not sibling_write.exists()


def test_late_descendant_and_timeout_cannot_yield_terminal_branch(
    tmp_path: Path,
) -> None:
    freeze = _freeze()
    classification = _classification(freeze)
    adapter = _probe_adapter(tmp_path, study_id="open-world-descendant-probe")
    leaked = _probe_request(
        adapter,
        freeze,
        classification,
        adversarial_probe={
            "sibling_read_path": None,
            "sibling_write_path": None,
            "late_write_path": "late-write.txt",
            "spawn_late_descendant": True,
        },
    )
    assert leaked["outcome_status"] == "operational_failure"
    assert leaked["process_event"]["descendant_leak_detected"] is True
    assert leaked["process_event"]["termination"] in {
        "terminated",
        "killed",
    }
    time.sleep(0.45)
    assert not (Path(leaked["workspace"]["resolved_path"]) / "late-write.txt").exists()

    budget = copy.deepcopy(adapter.default_budget())
    budget.update(
        {
            "budget_id": "open-world-timeout-budget.v1",
            "wall_time_seconds": 0.1,
            "grace_period_seconds": 0.05,
            "cpu_seconds": 1.0,
        }
    )
    with pytest.raises(OpenWorldCreativityError) as timeout:
        run_isolated_parallel_maturation_branches(
            freeze,
            classification,
            known_taxonomy=_taxonomy(),
            matured_inventions=_matured_proposals(freeze),
            maturation_questions=_maturation_questions(),
            run_root=tmp_path / "timeout-run",
            budget=budget,
            fault_plan={"invention-0": "hang"},
        )
    assert timeout.value.reason_code == "branch_execution_failed"

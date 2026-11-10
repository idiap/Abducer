# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Regression tests for the outer work loop."""

from __future__ import annotations

import datetime as dt
import json
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
COMMON_DIR = ROOT / "skills" / "common"
DISCOVERY_SCRIPT_DIR = ROOT / "skills" / "discovery" / "kb-discovery-cycle" / "scripts"
PROVE_SCRIPT_DIR = ROOT / "skills" / "discovery" / "kb-prove-cycle" / "scripts"
WORK_SCRIPT_DIR = ROOT / "skills" / "orchestration" / "work" / "scripts"

for path in (COMMON_DIR, DISCOVERY_SCRIPT_DIR, PROVE_SCRIPT_DIR, WORK_SCRIPT_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from problem_mathlib import default_mathlib
from agentic.discovery.contracts import ContractError
from agentic.discovery.contracts import bytes_digest
from agentic.discovery.contracts import canonical_digest
import agentic.discovery.theory_gate as theory_gate
from high_reward_watch import default_high_reward_watch
from high_reward_watch import save_high_reward_watch
from problem_mathlib import save_mathlib_index
from proof_queue import default_queue
from proof_queue import enqueue_entries
from proof_queue import finalize_queue_entry
from proof_queue import load_proof_queue
from proof_queue import proof_queue_paths
from proof_queue import save_proof_queue
from run_work_cycle import default_work_state
from run_work_cycle import breakthrough_profile_paths
from run_work_cycle import meta_report_paths
from run_work_cycle import _run_branch_to_theorem_pipeline
from run_work_cycle import discovery_branch_queue_paths
from run_work_cycle import discovery_pattern_routing_paths
from run_work_cycle import execute_work_cycle
from run_work_cycle import plausibility_report_paths
from run_work_cycle import run_discovery_phase
from run_work_cycle import run_prove_phase
from run_work_cycle import render_work_state_markdown
from run_work_cycle import reserve_work_cycle_actions
from run_work_cycle import verify_exact_local_work_item
from run_work_cycle import verify_work_cycle_theory_authorization
from run_work_cycle import work_state_paths
import run_work_cycle as work_cycle_module


def _verified_gate_fixture(payload: Mapping[str, object]):
    """Issue a digest-complete, short-lived local capability for unit seams."""

    materialized = json.loads(json.dumps(dict(payload)))
    now, clock_authority, temporal_capability = theory_gate._read_governed_present_instant(  # noqa: SLF001
        theory_gate.SYSTEM_UTC_CLOCK_AUTHORITY_ID
    )

    def stamp(value: dt.datetime) -> str:
        return value.astimezone(dt.timezone.utc).isoformat().replace("+00:00", "Z")

    commit_at = now - dt.timedelta(seconds=1)
    consume_before = now + dt.timedelta(minutes=5)
    materialized.setdefault("eligible_branch_ids", [])
    materialized.setdefault("action_ids_by_branch", {})
    materialized.setdefault("action_kinds_by_branch", {})
    materialized.setdefault(
        "authorization_semantics", "bounded_test_exact_schedule_eligibility"
    )
    eligibility = {
        "eligible_branch_ids": materialized["eligible_branch_ids"],
        "action_ids_by_branch": materialized["action_ids_by_branch"],
        "action_kinds_by_branch": materialized["action_kinds_by_branch"],
        "authorization_semantics": materialized["authorization_semantics"],
    }
    literature_basis = {
        "schema_version": "1.0.0",
        "basis_kind": "bounded_test_literature_authority",
        "snapshot_id": "snapshot.test.current",
        "recorded_commit_created_at": stamp(commit_at),
        "recorded_commit_time_authority": "unattested_transaction_manifest_local_time",
        "consume_before": stamp(consume_before),
    }
    literature_basis_digest = canonical_digest(literature_basis)
    authorization_basis = {
        "schema_version": "1.0.0",
        "basis_kind": "bounded_test_canonical_authorization",
        "target_id": materialized.get("target_id", "target.test"),
        "run_id": materialized.get("run_id", "run.test"),
        "cycle_id": materialized.get("cycle_id", "cycle.test"),
        "commit_id": materialized.get("commit_id", "commit.test"),
        "committed_state_version": materialized.get("committed_state_version", 1),
        "schedule_eligibility_derivation_digest": canonical_digest(eligibility),
    }
    authorization_basis_digest = canonical_digest(authorization_basis)
    present_decision = {
        "schema_version": "1.0.0",
        "decision": "authorized_present_investment",
        "evaluated_at": stamp(now),
        "recorded_commit_created_at": stamp(commit_at),
        "recorded_commit_time_authority": "unattested_transaction_manifest_local_time",
        "consume_before": stamp(consume_before),
        "authorization_basis_digest": authorization_basis_digest,
        "literature_authority_basis_digest": literature_basis_digest,
        "clock_authority": clock_authority,
        "clock_authority_digest": clock_authority["authority_digest"],
        "authentication_status": "governed_local_process_time_not_externally_authenticated",
        "reason": "bounded_test_capability_current_at_issue_time",
    }
    materialized.update(
        {
            "literature_consume_before": stamp(consume_before),
            "literature_authority_basis": literature_basis,
            "literature_authority_basis_digest": literature_basis_digest,
            "authorization_basis": authorization_basis,
            "authorization_basis_digest": authorization_basis_digest,
            "present_investment_decision": present_decision,
            "present_investment_decision_digest": canonical_digest(present_decision),
        }
    )
    materialized.pop("authorization_digest", None)
    materialized["authorization_digest"] = canonical_digest(materialized)
    return theory_gate._issue_verified_authorization(  # noqa: SLF001
        materialized,
        present_investment_verified=True,
        temporal_capability=temporal_capability,
    )


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _canonical_work_fixture(
    tmp_path: Path,
    *,
    phase: str,
    action_kind: str | None = None,
) -> dict:
    """Build a compact projection, exact two-sided local row, and binding."""

    target_id = "target.demo"
    run_id = "run.demo"
    cycle_id = "cycle.demo.002"
    commit_id = "commit.demo.002"
    branch_id = "branch.demo.canonical"
    hypothesis_id = "hypothesis.demo.canonical"
    obligation_id = "obligation.demo.canonical" if phase == "prove" else None
    local_id = "proofq.demo.901" if phase == "prove" else "local.branch.demo.901"
    action_kind = action_kind or ("prove" if phase == "prove" else "reflect")
    annotations = {
        "canonical_target_id": target_id,
        "canonical_run_id": run_id,
        "canonical_cycle_id": cycle_id,
        "canonical_commit_id": commit_id,
        "canonical_state_version": 2,
        "canonical_branch_id": branch_id,
        "canonical_hypothesis_id": hypothesis_id,
        "canonical_proof_obligation_id": obligation_id,
    }
    if phase == "prove":
        row = {
            "queue_id": local_id,
            "status": "pending",
            "title": "Explicitly bound local proof row",
            **annotations,
        }
        local_path = tmp_path / "artifacts" / "demo" / "proof-queue.json"
        _write_json(local_path, {"metadata": {"kb_ref": "demo"}, "entries": [row]})
    else:
        row = {
            "branch_id": local_id,
            "status": "active",
            "target_label": "Explicitly bound local discovery row",
            **annotations,
        }
        local_path = tmp_path / "artifacts" / "demo" / "discovery-branch-queue.json"
        _write_json(local_path, {"metadata": {"kb_ref": "demo"}, "branches": [row]})
    projection = {
        "target_id": target_id,
        "run_id": run_id,
        "cycle_id": cycle_id,
        "commit_id": commit_id,
        "committed_state_version": 2,
        "parallel_outcome": {"valid_branch_ids": [branch_id]},
        "identity_map": {
            "concept_ids": ["concept.demo.canonical"],
            "hypothesis_ids": [hypothesis_id],
            "proof_obligation_ids": [obligation_id] if obligation_id else [],
            "branch_bindings": [
                {
                    "branch_id": branch_id,
                    "hypothesis_id": hypothesis_id,
                    "concept_ids": ["concept.demo.canonical"],
                }
            ],
        },
        "schedule": {
            "actions": [
                {
                    "action_id": "action.demo.001",
                    "kind": action_kind,
                    "status": "pending",
                    "branch_ids": [branch_id],
                    "restrictions": [],
                }
            ]
        },
        "proof_handoff": (
            {
                "branch_id": branch_id,
                "hypothesis_id": hypothesis_id,
                "concept_id": "concept.demo.canonical",
                "obligation_id": obligation_id,
            }
            if obligation_id
            else None
        ),
    }
    projection_path = tmp_path / "canonical" / "cycle.demo.002.json"
    _write_json(projection_path, projection)
    state_root = tmp_path / "canonical-state"
    state_root.mkdir(parents=True, exist_ok=True)
    binding = {
        "schema_version": "1.0.0",
        "binding_id": f"binding.demo.{phase}",
        "phase": phase,
        "target_id": target_id,
        "run_id": run_id,
        "cycle_id": cycle_id,
        "commit_id": commit_id,
        "committed_state_version": 2,
        "canonical_branch_id": branch_id,
        "canonical_hypothesis_id": hypothesis_id,
        "canonical_proof_obligation_id": obligation_id,
        "local_work_item_kind": "proof_queue_entry" if phase == "prove" else "discovery_branch",
        "local_work_item_id": local_id,
        "local_work_item_digest": canonical_digest(row),
        "binding_digest": "",
    }
    binding["binding_digest"] = canonical_digest(binding, exclude_keys=("binding_digest",))
    authorization = {
        "schema_version": "1.0.0",
        "status": "verified_active_current",
        "authoritative": True,
        "target_id": target_id,
        "run_id": run_id,
        "cycle_id": cycle_id,
        "prior_state_version": 1,
        "committed_state_version": 2,
        "commit_id": commit_id,
        "transaction_root": str(state_root.resolve()),
        "projection_path": str(projection_path.resolve()),
        "projection_digest": bytes_digest(projection_path.read_bytes()),
        "eligible_branch_ids": [branch_id],
        "action_ids_by_branch": {branch_id: ["action.demo.001"]},
        "action_kinds_by_branch": {branch_id: [action_kind]},
    }
    return {
        "projection_path": projection_path,
        "state_root": state_root,
        "local_path": local_path,
        "row": row,
        "binding": binding,
        "authorization": authorization,
        "target_id": target_id,
        "run_id": run_id,
        "branch_id": branch_id,
        "hypothesis_id": hypothesis_id,
        "obligation_id": obligation_id,
        "local_id": local_id,
    }


def _install_fake_canonical_gate(monkeypatch: pytest.MonkeyPatch, fixture: dict) -> None:
    """Replace only the reusable verifier; binding/row checks remain real."""

    def fake_verify(_projection_path: Path, **kwargs: object) -> dict:
        assert kwargs["target_id"] == fixture["target_id"]
        assert kwargs["run_id"] == fixture["run_id"]
        return _verified_gate_fixture(fixture["authorization"])

    monkeypatch.setattr(work_cycle_module, "verify_canonical_theory_cycle", fake_verify)


def _install_fake_action_reservation(monkeypatch: pytest.MonkeyPatch, fixture: dict) -> dict:
    """Install a deterministic reservation seam for outer-loop dispatch tests."""

    phase = fixture["binding"]["phase"]
    reserved_commit_id = f"commit.demo.reservation.{phase}"
    reserved_manifest_digest = canonical_digest({"manifest": phase})
    reserved_commit_path = str((fixture["state_root"] / "reservation-commit").resolve())

    def fake_reserve(source: Mapping[str, object], **kwargs: object):
        source_projection = theory_gate.authorization_projection(source)  # type: ignore[arg-type]
        decision = source_projection["present_investment_decision"]
        temporal_evaluation = {
            "evaluated_at": decision["evaluated_at"],
            "clock_authority": decision["clock_authority"],
            "clock_authority_digest": decision["clock_authority_digest"],
            "authentication_status": "governed_local_process_time_not_externally_authenticated",
        }
        reservation = {
            "schema_version": "1.0.0",
            "reservation_id": f"reservation.demo.{phase}",
            "target_id": fixture["target_id"],
            "run_id": fixture["run_id"],
            "source_cycle_id": fixture["authorization"]["cycle_id"],
            "source_commit_id": fixture["authorization"]["commit_id"],
            "source_state_generation": 2,
            "reserved_state_generation": 3,
            "action_ids": ["action.demo.001"],
            "consumer_receipt_id": kwargs["consumer_receipt_id"],
            "status": "reserved_before_investment",
            "temporal_evaluation": temporal_evaluation,
        }
        reservation["reservation_digest"] = canonical_digest(reservation)
        schedule = {
            "schema_version": "1.0.0",
            "schedule_id": f"schedule.demo.reserved.{phase}",
            "actions": [{"action_id": "action.demo.001", "status": "consumed"}],
            "consumption_log": [],
        }
        schedule["consumed_schedule_digest"] = canonical_digest(
            schedule,
            exclude_keys=("consumed_schedule_digest", "created_at"),
        )
        reservation_basis = {
            "schema_version": "1.0.0",
            "basis_kind": "immutable_canonical_action_reservation",
            "source_authorization_basis_digest": source_projection[
                "authorization_basis_digest"
            ],
            "reservation_digest": reservation["reservation_digest"],
            "reserved_commit_id": reserved_commit_id,
            "reserved_manifest_digest": reserved_manifest_digest,
            "reserved_state_generation": 3,
            "consumed_schedule_digest": schedule["consumed_schedule_digest"],
            "reserved_branch_ids": [fixture["branch_id"]],
            "reserved_action_ids": ["action.demo.001"],
        }
        reserved_payload = {
            **source_projection,
            "status": "actions_reserved",
            "source_commit_id": fixture["authorization"]["commit_id"],
            "source_committed_state_version": 2,
            "committed_state_version": 3,
            "commit_id": reserved_commit_id,
            "manifest_digest": reserved_manifest_digest,
            "commit_path": reserved_commit_path,
            "reserved_branch_ids": [fixture["branch_id"]],
            "reserved_action_ids": ["action.demo.001"],
            "reservation_consumer_scope": (
                "outer_prove" if phase == "prove" else "outer_discovery"
            ),
            "proof_obligation_id": fixture["obligation_id"],
            "reservation": reservation,
            "reservation_digest": reservation["reservation_digest"],
            "schedule": schedule,
            "reservation_authorization_basis": reservation_basis,
            "reservation_authorization_basis_digest": canonical_digest(
                reservation_basis
            ),
            "reservation_temporal_evaluation": temporal_evaluation,
            "reservation_temporal_evaluation_digest": canonical_digest(
                temporal_evaluation
            ),
        }
        reserved_payload.pop("authorization_digest", None)
        reserved_payload["authorization_digest"] = canonical_digest(reserved_payload)
        return theory_gate._issue_verified_authorization(  # noqa: SLF001
            reserved_payload,
            present_investment_verified=True,
            temporal_capability=source._temporal_capability,  # type: ignore[attr-defined]  # noqa: SLF001
        )

    monkeypatch.setattr(
        work_cycle_module,
        "reserve_canonical_theory_actions",
        fake_reserve,
    )
    return {
        "reservation_id": f"reservation.demo.{phase}",
        "reserved_commit_id": reserved_commit_id,
        "reserved_manifest_digest": reserved_manifest_digest,
        "reserved_commit_path": reserved_commit_path,
    }


def _bridge() -> dict:
    return {
        "bridge_id": "bridge.001",
        "priority": 0.91,
        "source_statement_id": "st.src",
        "target_statement_id": "st.tgt",
        "source_excerpt": "Source theorem excerpt.",
        "target_excerpt": "Target theorem excerpt.",
        "route_synopsis": "Move from st.src toward st.tgt through a witness family.",
        "abstraction_label": "Witness family",
        "carrier_kind": "family of instances equipped with a witness measure",
        "preserved_invariant": "witness complexity profile",
        "proof_strategy_family": "invariant-lift-through-intermediate-object",
        "missing_route_lemma": "Prove the witness family transfers the lower bound to the target.",
        "conditional_proposition": "If the witness family exists, the target consequence follows.",
        "proof_obligations": ["Build the witness family from the source theorem."],
        "candidate_lemmas": ["The source theorem induces the witness family."],
        "negative_route": "Allow the witness family to ignore source-side content.",
        "failure_diagnosis": "The route fails if the witness family is only topical overlap.",
        "statement_delta": {
            "source_claim_focus": "explicit source lower bound",
            "target_claim_focus": "major target separation",
            "source_problem_family": "Demo",
            "target_problem_family": "Demo",
            "source_model": "circuits",
            "target_model": "circuits",
        },
    }


def _math_layers(*, object_name: str = "Witness family", invariant: str = "witness profile", theorem_name: str = "witness_family_transport") -> dict:
    return {
        "status": "generated",
        "representation_kind": "informal-latex-lean-style",
        "quantifier_signature": f"For every admissible `{object_name}`.",
        "object_signature": {
            "bridge_object": object_name,
            "route_object": "R(W)",
            "target_object": "T(W)",
            "bridge_witness": "BW(W)",
            "invariant": invariant,
        },
        "symbol_ledger": [
            {"symbol": "W", "latex": "W", "lean": "W", "meaning": f"an admissible {object_name}"},
            {"symbol": "BW(W)", "latex": "\\mathsf{BW}(W)", "lean": "BridgeWitness W", "meaning": "the bridge witness"},
            {"symbol": "PresInv(W, w)", "latex": "\\mathrm{PresInv}(W,w)", "lean": "PresInv W w", "meaning": invariant},
            {"symbol": "RealizesTarget(W, w)", "latex": "\\mathrm{RealizesTarget}(W,w)", "lean": "RealizesTarget W w", "meaning": "the witness activates the target claim"},
        ],
        "latex": {
            "theorem_statement": "\\forall W,\\ \\mathrm{Adm}(W) \\to \\exists w : \\mathsf{BW}(W),\\ \\mathrm{PresInv}(W,w) \\wedge \\mathrm{RealizesTarget}(W,w).",
            "gloss": f"`BridgeWitness` preserves `{invariant}` and activates the target.",
        },
        "lean_style": {
            "theorem_name": theorem_name,
        },
    }


def _write_branch_execution_artifact(
    artifacts_dir: Path,
    *,
    branch_id: str,
    queue_id: str,
    title: str,
    execution_queue_id: str | None = None,
    include_factorization: bool = False,
    include_equivalence: bool = False,
) -> None:
    execution_queue_id = execution_queue_id or queue_id
    search_shapes = ["realization", "transport", "obstruction"]
    candidates = [
        {
            "queue_id": execution_queue_id,
            "candidate": {
                "shape": "realization",
                "title": "Realization theorem for Witness family",
                "obligations": [
                    "Construct a concrete witness family.",
                    "Show the witness family preserves the invariant.",
                ],
            },
        },
        {
            "queue_id": execution_queue_id,
            "candidate": {
                "shape": "transport",
                "title": "Transport theorem for Witness family",
                "obligations": [
                    "Define the transport map from the route-side object to the target-side object."
                ],
            },
        },
    ]
    theorem_obligations = ["Expose the transport theorem as the active constructive route lemma."]
    if include_factorization:
        search_shapes.insert(2, "factorization")
        theorem_obligations.append(
            "Exhibit an intermediate typed object factoring the route through the witness family."
        )
        candidates.append(
            {
                "queue_id": execution_queue_id,
                "candidate": {
                    "shape": "factorization",
                    "title": "Factorization theorem for Witness family",
                    "obligations": [
                        "Exhibit an intermediate typed object factoring the route through the witness family."
                    ],
                },
            }
        )
    if include_equivalence:
        search_shapes.insert(2, "equivalence")
        theorem_obligations.extend(
            [
                "Construct the equivalence witness for the witness family.",
                "Prove the required coherence or naturality law.",
            ]
        )
        candidates.append(
            {
                "queue_id": execution_queue_id,
                "candidate": {
                    "shape": "equivalence",
                    "title": "Equivalence theorem for Witness family",
                    "obligations": [
                        "Construct the equivalence witness for the witness family.",
                        "Prove the required coherence or naturality law.",
                    ],
                },
            }
        )
    execution_json = artifacts_dir / "discovery-branch-executions" / "discexec.demo.001.json"
    _write_json(
        execution_json,
        {
            "metadata": {
                "execution_id": "discexec.demo.001",
                "branch_id": branch_id,
            },
            "execution": {
                "theorem_candidates": [
                    {
                        "title": title,
                        "linked_queue_ids": [execution_queue_id],
                        "candidate_object": "Witness family",
                        "search_shape": "transport",
                        "obligations": theorem_obligations,
                    }
                ],
                "lean_symbolic_search": {
                    "routes": [
                        {
                            "queue_id": execution_queue_id,
                            "lean_readiness_score": 10,
                            "readiness": {
                                "mode": "symbolic-search-ready",
                                "reasons": ["the route is typed enough for bounded search over bridge shapes"],
                            },
                            "search_shapes": search_shapes,
                        }
                    ],
                    "candidates": candidates,
                },
            },
        },
    )
    _write_json(
        artifacts_dir / "discovery-branch-executions" / "index.json",
        {
            "executions": [
                {
                    "branch_id": branch_id,
                    "artifact_json": str(execution_json),
                }
            ]
        },
    )


def test_work_cycle_alternates_discovery_and_prove_and_stops_on_budget(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    _write_json(
        artifacts_dir / "expert-hypothesis-paper.json",
        {"recommended_bridges": [_bridge()]},
    )
    _write_json(
        artifacts_dir / "search-space-tree.json",
        {
            "frontier": {"resume": [{"bridge_id": "bridge.001", "policy": "resume-with-deeper-proof", "priority": 0.95}]},
            "routes": [
                {
                    "bridge_id": "bridge.001",
                    "route_signature": "route.demo.001",
                    "priority": 0.95,
                    "dimensions": {"source_statement_id": "st.src", "target_statement_id": "st.tgt"},
                }
            ],
        },
    )
    _write_json(
        artifacts_dir / "macro-proof-state.json",
        {
            "main_conjecture": {
                "core_claim": "Demo main claim",
                "route_target_claim": "Demo route target",
                "grounding_implication": "If demo route target then demo main claim.",
            },
            "leading_route": {
                "candidate_object": "Witness family",
                "carrier_kind": "family of instances equipped with a witness measure",
                "negative_route": "The witness family might fail.",
                "failure_diagnosis": "The route fails if the witness family is only topical overlap.",
                "mathematical_assumptions": ["Assume an admissible witness family exists."],
                "proof_obligations": ["Build the witness family."],
                "candidate_lemmas": ["The source theorem induces the witness family."],
                "proof_outline": ["Build.", "Transport.", "Payoff."],
            },
            "status_assessment": {"evidence_count": 0, "novelty_argument": "Programme-level novelty only."},
        },
    )
    _write_json(
        artifacts_dir / "macro-strategy-report.json",
        {
            "operationalizations": [{"object": "Witness family", "carrier_kind": "family of instances equipped with a witness measure"}],
            "missing_for_completion": [{"kind": "route-lemma", "title": "Route lemma"}],
            "completion_checklist": [
                {"status": "established", "title": "Grounding implication"},
                {"status": "open", "title": "Route lemma"},
            ],
        },
    )
    _write_json(
        artifacts_dir / "proof-cycle-summary.json",
        {
            "metadata": {
                "proved_count": 0,
                "disproved_count": 0,
                "blocked_count": 0,
                "produced_paper_count": 0,
                "external_reference_count": 0,
            }
        },
    )
    mathlib_json = repo_root / "InformalMathLib" / "demo" / "index.json"
    mathlib_md = repo_root / "InformalMathLib" / "demo" / "catalog.md"
    save_mathlib_index(default_mathlib(kb_ref="demo"), json_path=mathlib_json, md_path=mathlib_md)

    state = default_work_state(kb_ref="demo", max_cycles=2)
    state, latest = execute_work_cycle(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref="demo",
        kb_path=None,
        state=state,
        phase_override="auto",
        top_k=4,
        non_authoritative_legacy_compatibility=True,
    )
    assert latest["phase"] == "discovery"
    assert latest["status"] == "completed"
    assert state["metadata"]["cycle_count"] == 1
    assert state["metadata"]["next_phase"] == "prove"

    state, latest = execute_work_cycle(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref="demo",
        kb_path=None,
        state=state,
        phase_override="auto",
        top_k=4,
        non_authoritative_legacy_compatibility=True,
    )
    assert latest["phase"] == "prove"
    assert latest["status"] == "completed"
    assert state["metadata"]["cycle_count"] == 2
    assert state["metadata"]["next_phase"] == "discovery"
    assert state["metadata"]["stop_status"] == "stop-max-cycles"

    attempt_dir = artifacts_dir / "proof-attempts"
    attempt_files = list(attempt_dir.glob("*.json"))
    assert len(attempt_files) == 1
    assert (repo_root / "artifacts" / "demo" / "proof-queue.json").exists()
    refreshed_summary = json.loads((artifacts_dir / "proof-cycle-summary.json").read_text(encoding="utf-8"))
    assert refreshed_summary["metadata"]["pending_count"] == 0
    assert refreshed_summary["metadata"]["in_progress_count"] == 1
    assert refreshed_summary["diagnosis_overview"]["attempts_active"]["count"] == 1

    work_json, work_md = work_state_paths(artifacts_dir)
    plaus_json, plaus_md = plausibility_report_paths(artifacts_dir)
    assert work_json.name == "work-state.json"
    assert work_md.name == "work-state.md"
    assert plaus_json.name == "end-to-end-proof-plausibility.json"
    assert plaus_md.name == "end-to-end-proof-plausibility.md"


def test_prove_phase_reports_interpretability_deferrals_instead_of_starting_attempt(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|route-conjecture-placeholder",
                "title": "Target theorem T...",
                "priority": 0.92,
                "bridge_id": "bridge.001",
                "claim_type": "route-conjecture",
                "claim_text": "Target theorem T is fixed. The real theorem under search is the local activation theorem A that verifies T through carrier C.",
                "conjecture_statement": "Target theorem T is fixed. The real theorem under search is the local activation theorem A that verifies T through carrier C.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "source_excerpt": "Source theorem excerpt.",
                "target_excerpt": "Target theorem excerpt.",
                "route_synopsis": "Move from source theorem S to target theorem T through carrier C...",
                "candidate_object": "unspecified witness family",
                "carrier_kind": "family of instances",
                "preserved_invariant": "witness profile",
                "missing_route_lemma": "Prove carrier C realizes target theorem T.",
            }
        ],
    )
    save_proof_queue(
        queue,
        json_path=artifacts_dir / "proof-queue.json",
        md_path=artifacts_dir / "proof-queue.md",
    )
    save_mathlib_index(
        default_mathlib(kb_ref="demo"),
        json_path=artifacts_dir / "mathlib.json",
        md_path=artifacts_dir / "mathlib.md",
    )

    latest = run_prove_phase(repo_root=repo_root, artifacts_dir=artifacts_dir, kb_ref="demo", kb_path=None)
    refreshed = load_proof_queue(artifacts_dir / "proof-queue.json", kb_ref="demo")

    assert latest["phase"] == "prove"
    assert latest["status"] == "idle"
    assert "interpretability gate" in latest["detail"].lower()
    assert refreshed["entries"][0]["status"] == "deferred"
    assert refreshed["entries"][0]["deferred_by"] == "llm-interpretability-gate"


def test_prove_phase_ignores_inactive_discovery_frontier_retirements(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "disclayer.demo.family.transport|st.tgt|branch-programme-transport",
                "title": "Transport Prompt: If source theorem S holds in regime R, carrier C yields target theorem T.",
                "priority": 0.92,
                "bridge_id": "disclayer.demo.family.transport",
                "claim_type": "branch-programme",
                "claim_text": "If source theorem S holds in regime R, carrier C yields target theorem T.",
                "conjecture_statement": "If source theorem S holds in regime R, carrier C yields target theorem T.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "source_excerpt": "Source theorem excerpt.",
                "target_excerpt": "Target theorem excerpt.",
                "route_synopsis": "Move from source theorem S to target theorem T through carrier C...",
                "candidate_object": "unspecified witness family",
                "carrier_kind": "family of instances",
                "preserved_invariant": "witness profile",
                "missing_route_lemma": "Prove carrier C realizes target theorem T.",
                "discovery_branch_id": "disclayer.demo.family.transport",
            }
        ],
    )
    row = queue["entries"][0]
    row["status"] = "deferred"
    row["retired_from_active_frontier"] = True
    row["retired_reason"] = "Retired because an expert-grade discovery packet now carries the active prove frontier."
    row["deferred_by"] = "inactive-discovery-frontier"
    row["deferred_reason"] = row["retired_reason"]
    save_proof_queue(
        queue,
        json_path=artifacts_dir / "proof-queue.json",
        md_path=artifacts_dir / "proof-queue.md",
    )
    save_mathlib_index(
        default_mathlib(kb_ref="demo"),
        json_path=artifacts_dir / "mathlib.json",
        md_path=artifacts_dir / "mathlib.md",
    )

    latest = run_prove_phase(repo_root=repo_root, artifacts_dir=artifacts_dir, kb_ref="demo", kb_path=None)
    refreshed = load_proof_queue(artifacts_dir / "proof-queue.json", kb_ref="demo")

    assert latest["phase"] == "prove"
    assert latest["status"] == "idle"
    assert latest["detail"] == "No pending proof-queue item is available, so the loop returns to discovery."
    assert refreshed["entries"][0]["deferred_by"] == "inactive-discovery-frontier"


def test_prove_phase_auto_finalizes_scaffold_only_attempt_when_only_blockers_remain(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    attempts_dir = artifacts_dir / "proof-attempts"
    attempts_dir.mkdir(parents=True, exist_ok=True)

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|expert-conjecture-demo",
                "title": "Witness-family transport theorem",
                "priority": 0.92,
                "bridge_id": "bridge.001",
                "claim_type": "expert-conjecture",
                "claim_text": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
                "conjecture_statement": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "source_excerpt": "Source theorem excerpt.",
                "target_excerpt": "Target theorem excerpt.",
                "route_synopsis": "Transport the source lower bound to the target theorem through a Witness family.",
                "candidate_object": "Witness family",
                "carrier_kind": "family of witness instances",
                "preserved_invariant": "witness profile",
                "proof_strategy_family": "transport",
                "missing_route_lemma": "Witness-family transport lemma",
                "negative_route": "Assume the witness family fails to preserve the invariant.",
                "proof_obligations": ["Show the witness family preserves the invariant."],
            }
        ],
    )
    consumed = queue["entries"][0]
    consumed["status"] = "in_progress"
    consumed["attempt_ids"] = ["attempt.demo.001"]
    save_proof_queue(
        queue,
        json_path=artifacts_dir / "proof-queue.json",
        md_path=artifacts_dir / "proof-queue.md",
    )
    save_mathlib_index(
        default_mathlib(kb_ref="demo"),
        json_path=repo_root / "InformalMathLib" / "demo" / "index.json",
        md_path=repo_root / "InformalMathLib" / "demo" / "catalog.md",
    )
    _write_branch_execution_artifact(
        artifacts_dir,
        branch_id="disclayer.demo.pattern.transport",
        queue_id="proofq.demo.001",
        title="Witness-family transport theorem",
    )
    _write_json(
        attempts_dir / "attempt.demo.001.json",
        {
            "metadata": {
                "attempt_id": "attempt.demo.001",
                "queue_id": "proofq.demo.001",
                "status": "in_progress",
                "resume_count": 3,
                "continuation_stage": 3,
            },
            "target": {
                "title": "Witness-family transport theorem",
                "bridge_id": "bridge.001",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "candidate_object": "Witness family",
                "preserved_invariant": "witness profile",
                "missing_route_lemma": "Witness-family transport lemma",
                "conjecture_statement": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
            },
            "local_context": {
                "mathlib_hits": [
                    {
                        "result_id": "mathlib.demo.blocked.001",
                        "outcome": "blocked",
                        "title": "Earlier blocked transport route",
                    }
                ]
            },
            "proof_attempt": {
                "theorem_statement": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
                "stepwise_argument": [
                    {
                        "step": 1,
                        "claim": "Assume an admissible Witness family exists.",
                        "justification": "Proof scaffold.",
                    }
                ],
                "negative_argument": {},
            },
            "final_assessment": {
                "outcome": "in_progress",
            },
        },
    )
    (attempts_dir / "attempt.demo.001.md").write_text("# Attempt\n", encoding="utf-8")

    latest = run_prove_phase(repo_root=repo_root, artifacts_dir=artifacts_dir, kb_ref="demo", kb_path=None)

    refreshed = load_proof_queue(artifacts_dir / "proof-queue.json", kb_ref="demo")
    mathlib = json.loads((repo_root / "InformalMathLib" / "demo" / "index.json").read_text(encoding="utf-8"))
    attempt = json.loads((attempts_dir / "attempt.demo.001.json").read_text(encoding="utf-8"))

    assert latest["phase"] == "prove"
    assert latest["status"] == "completed"
    assert "auto-finalized" in latest["detail"].lower()
    assert refreshed["entries"][0]["status"] == "blocked"
    assert mathlib["metadata"]["negative_result_count"] == 1
    assert attempt["final_assessment"]["outcome"] == "blocked"
    assert "already-recorded local obstructions" in attempt["final_assessment"]["summary"]


def test_prove_phase_resumes_in_progress_attempt_before_opening_new_queue_item(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    attempts_dir = artifacts_dir / "proof-attempts"
    attempts_dir.mkdir(parents=True, exist_ok=True)

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|expert-conjecture-demo",
                "title": "Witness-family transport theorem",
                "priority": 0.92,
                "bridge_id": "bridge.001",
                "claim_type": "expert-conjecture",
                "claim_text": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
                "conjecture_statement": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "source_excerpt": "Source theorem excerpt.",
                "target_excerpt": "Target theorem excerpt.",
                "route_synopsis": "Transport the source lower bound to the target theorem through a Witness family.",
                "candidate_object": "Witness family",
                "carrier_kind": "family of witness instances",
                "preserved_invariant": "witness profile",
                "proof_strategy_family": "transport",
                "missing_route_lemma": "Witness-family transport lemma",
                "negative_route": "Assume the witness family fails to preserve the invariant.",
                "failure_diagnosis": "The route fails if the witness family cannot preserve the invariant.",
                "proof_obligations": ["Show the witness family preserves the invariant."],
                "status": "in_progress",
                "attempt_ids": ["attempt.demo.001"],
            },
            {
                "queue_key": "bridge.002|st.tgt.2|expert-conjecture-demo-2",
                "title": "Fresh pending theorem",
                "priority": 0.81,
                "bridge_id": "bridge.002",
                "claim_type": "expert-conjecture",
                "claim_text": "There exists an admissible second Witness family.",
                "conjecture_statement": "There exists an admissible second Witness family.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt.2",
                "source_excerpt": "Source theorem excerpt.",
                "target_excerpt": "Second target theorem excerpt.",
                "route_synopsis": "Realize the second witness family.",
                "candidate_object": "Second Witness family",
                "carrier_kind": "family of witness instances",
                "preserved_invariant": "witness profile",
                "proof_strategy_family": "transport",
                "missing_route_lemma": "Second witness-family transport lemma",
                "negative_route": "Assume the second witness family fails to preserve the invariant.",
                "proof_obligations": ["Show the second witness family preserves the invariant."],
            },
        ],
    )
    save_proof_queue(
        queue,
        json_path=artifacts_dir / "proof-queue.json",
        md_path=artifacts_dir / "proof-queue.md",
    )
    save_mathlib_index(
        default_mathlib(kb_ref="demo"),
        json_path=repo_root / "InformalMathLib" / "demo" / "index.json",
        md_path=repo_root / "InformalMathLib" / "demo" / "catalog.md",
    )
    _write_branch_execution_artifact(
        artifacts_dir,
        branch_id="disclayer.demo.pattern.transport",
        queue_id="proofq.demo.001",
        title="Witness-family transport theorem",
    )
    _write_json(
        attempts_dir / "attempt.demo.001.json",
        {
            "metadata": {
                "attempt_id": "attempt.demo.001",
                "queue_id": "proofq.demo.001",
                "status": "in_progress",
            },
            "target": {
                "title": "Witness-family transport theorem",
                "bridge_id": "bridge.001",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "candidate_object": "Witness family",
                "preserved_invariant": "witness profile",
                "missing_route_lemma": "Witness-family transport lemma",
                "conjecture_statement": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
                "route_synopsis": "Transport the source lower bound to the target theorem through a Witness family.",
                "discovery_branch_id": "disclayer.demo.pattern.transport",
                "mathematical_layers": _math_layers(),
                "negative_route": "Assume the witness family fails to preserve the invariant.",
                "failure_diagnosis": "The route fails if the witness family cannot preserve the invariant.",
            },
            "local_context": {
                "mathlib_hits": [
                    {
                        "result_id": "mathlib.demo.blocked.001",
                        "outcome": "blocked",
                        "title": "Earlier blocked transport route",
                    }
                ]
            },
            "proof_attempt": {
                "theorem_statement": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
                "route_lemma_under_test": "Witness-family transport lemma",
                "assumptions": ["Assume an admissible Witness family exists."],
                "informal_tactic_trace": [
                    {"order": 1, "tactic_id": "normalize-goal", "status": "pending", "notes": []},
                    {"order": 2, "tactic_id": "introduce-assumptions", "status": "pending", "notes": []},
                    {"order": 3, "tactic_id": "reduce-to-route-lemma", "status": "pending", "notes": []},
                    {"order": 4, "tactic_id": "extract-subgoal", "status": "pending", "notes": []},
                    {"order": 5, "tactic_id": "construct-witness", "status": "pending", "notes": []},
                    {"order": 6, "tactic_id": "transport-invariant", "status": "pending", "notes": []},
                    {"order": 7, "tactic_id": "activate-target-theorem", "status": "pending", "notes": []},
                    {"order": 8, "tactic_id": "negate-goal", "status": "pending", "notes": []},
                    {"order": 9, "tactic_id": "obstruction-probe", "status": "pending", "notes": []},
                    {"order": 10, "tactic_id": "derive-contradiction", "status": "pending", "notes": []},
                    {"order": 11, "tactic_id": "closure-check", "status": "pending", "notes": []},
                ],
                "stepwise_argument": [{"step": 1, "claim": "Assume the Witness family exists.", "justification": "Proof scaffold."}],
                "local_results_used": [],
                "negative_argument": {},
                "contradiction_frame": {},
            },
            "final_assessment": {"outcome": "in_progress"},
        },
    )
    (attempts_dir / "attempt.demo.001.md").write_text("# Attempt\n", encoding="utf-8")

    latest = run_prove_phase(repo_root=repo_root, artifacts_dir=artifacts_dir, kb_ref="demo", kb_path=None)
    refreshed_queue = load_proof_queue(artifacts_dir / "proof-queue.json", kb_ref="demo")
    attempt = json.loads((attempts_dir / "attempt.demo.001.json").read_text(encoding="utf-8"))

    assert latest["phase"] == "prove"
    assert latest["status"] == "completed"
    assert "resumed proof attempt" in latest["detail"].lower()
    assert latest["attempt_id"] == "attempt.demo.001"
    assert refreshed_queue["metadata"]["in_progress_count"] == 1
    assert refreshed_queue["metadata"]["pending_count"] == 1
    trace = {row["tactic_id"]: row["status"] for row in attempt["proof_attempt"]["informal_tactic_trace"]}
    assert trace["normalize-goal"] == "completed"
    assert trace["introduce-assumptions"] == "completed"
    assert trace["reduce-to-route-lemma"] == "completed"
    assert trace["extract-subgoal"] == "completed"
    assert trace["construct-witness"] == "in_progress"
    assert trace["transport-invariant"] == "in_progress"
    assert trace["activate-target-theorem"] == "completed"
    assert trace["negate-goal"] == "completed"
    assert trace["obstruction-probe"] == "completed"
    assert trace["derive-contradiction"] == "in_progress"
    assert attempt["metadata"]["continuation_stage"] == 1
    assert attempt["metadata"]["resume_count"] == 1
    assert len(attempt["proof_attempt"]["local_results_used"]) == 1
    assert attempt["proof_attempt"]["local_results_used"][0]["result_id"] == "mathlib.demo.blocked.001"
    assert len(attempt["proof_attempt"]["continuation_log"]) == 1
    package = attempt["proof_attempt"]["positive_subgoal_package"]
    assert package["source"] == "mathematical_layers+branch_execution"
    assert package["readiness_mode"] == "symbolic-search-ready"
    assert package["positive_shapes"] == ["realization", "transport"]
    assert package["candidate_titles"][0] == "Realization theorem for Witness family"
    assert package["bridge_witness_symbol"] == "BW(W)"
    assert attempt["proof_attempt"]["negative_argument"]["forbidden_outcome"] == "The route fails if the witness family cannot preserve the invariant."
    assert attempt["proof_attempt"]["contradiction_frame"]["forbidden_outcome"] == "The route fails if the witness family cannot preserve the invariant."
    assert "Earlier blocked transport route" in attempt["proof_attempt"]["negative_argument"]["counterexample_or_barrier"]
    judges = {row["judge_id"]: row for row in attempt["critique_judges"]}
    assert judges["statement-grounding"]["verdict"] == "passes"
    assert judges["tactic-trace-discipline"]["verdict"] == "passes"
    assert judges["local-counterexample-search"]["verdict"] == "in_progress"


def test_positive_subgoal_package_uses_branch_sibling_evidence_after_queue_refresh(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    attempts_dir = artifacts_dir / "proof-attempts"
    attempts_dir.mkdir(parents=True, exist_ok=True)

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.050|st.tgt|expert-conjecture-demo",
                "title": "Transport theorem for Witness family",
                "priority": 0.92,
                "bridge_id": "bridge.050",
                "claim_type": "expert-conjecture",
                "claim_text": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
                "conjecture_statement": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "source_excerpt": "Source theorem excerpt.",
                "target_excerpt": "Target theorem excerpt.",
                "route_synopsis": "Transport the source lower bound to the target theorem through a Witness family.",
                "candidate_object": "Witness family",
                "carrier_kind": "family of witness instances",
                "preserved_invariant": "witness profile",
                "proof_strategy_family": "transport",
                "missing_route_lemma": "Transport theorem for Witness family",
                "negative_route": "Assume the witness family fails to preserve the invariant.",
                "failure_diagnosis": "The route fails if the witness family cannot preserve the invariant.",
                "proof_obligations": ["Show the witness family preserves the invariant."],
                "status": "in_progress",
                "attempt_ids": ["attempt.demo.050"],
            }
        ],
    )
    save_proof_queue(
        queue,
        json_path=artifacts_dir / "proof-queue.json",
        md_path=artifacts_dir / "proof-queue.md",
    )
    save_mathlib_index(
        default_mathlib(kb_ref="demo"),
        json_path=repo_root / "InformalMathLib" / "demo" / "index.json",
        md_path=repo_root / "InformalMathLib" / "demo" / "catalog.md",
    )
    _write_branch_execution_artifact(
        artifacts_dir,
        branch_id="disclayer.demo.pattern.transport",
        queue_id="proofq.demo.001",
        execution_queue_id="proofq.demo.002",
        title="Transport theorem for Witness family",
    )
    _write_json(
        attempts_dir / "attempt.demo.050.json",
        {
            "metadata": {
                "attempt_id": "attempt.demo.050",
                "queue_id": "proofq.demo.001",
                "status": "in_progress",
            },
            "target": {
                "title": "Transport theorem for Witness family",
                "bridge_id": "bridge.050",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "candidate_object": "Witness family",
                "preserved_invariant": "witness profile",
                "missing_route_lemma": "Transport theorem for Witness family",
                "conjecture_statement": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
                "route_synopsis": "Transport the source lower bound to the target theorem through a Witness family.",
                "discovery_branch_id": "disclayer.demo.pattern.transport",
                "mathematical_layers": _math_layers(theorem_name="witness_family_transport_refreshed"),
                "negative_route": "Assume the witness family fails to preserve the invariant.",
                "failure_diagnosis": "The route fails if the witness family cannot preserve the invariant.",
            },
            "local_context": {"mathlib_hits": []},
            "proof_attempt": {
                "theorem_statement": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
                "route_lemma_under_test": "Transport theorem for Witness family",
                "assumptions": ["Assume an admissible Witness family exists."],
                "informal_tactic_trace": [
                    {"order": 1, "tactic_id": "normalize-goal", "status": "pending", "notes": []},
                    {"order": 2, "tactic_id": "introduce-assumptions", "status": "pending", "notes": []},
                    {"order": 3, "tactic_id": "reduce-to-route-lemma", "status": "pending", "notes": []},
                    {"order": 4, "tactic_id": "extract-subgoal", "status": "pending", "notes": []},
                    {"order": 5, "tactic_id": "construct-witness", "status": "pending", "notes": []},
                    {"order": 6, "tactic_id": "transport-invariant", "status": "pending", "notes": []},
                    {"order": 7, "tactic_id": "activate-target-theorem", "status": "pending", "notes": []},
                    {"order": 8, "tactic_id": "negate-goal", "status": "pending", "notes": []},
                    {"order": 9, "tactic_id": "obstruction-probe", "status": "pending", "notes": []},
                    {"order": 10, "tactic_id": "derive-contradiction", "status": "pending", "notes": []},
                    {"order": 11, "tactic_id": "closure-check", "status": "pending", "notes": []},
                ],
                "stepwise_argument": [{"step": 1, "claim": "Assume the Witness family exists.", "justification": "Proof scaffold."}],
                "local_results_used": [],
                "negative_argument": {},
                "contradiction_frame": {},
            },
            "final_assessment": {"outcome": "in_progress"},
        },
    )
    (attempts_dir / "attempt.demo.050.md").write_text("# Attempt\n", encoding="utf-8")

    latest = run_prove_phase(repo_root=repo_root, artifacts_dir=artifacts_dir, kb_ref="demo", kb_path=None)
    attempt = json.loads((attempts_dir / "attempt.demo.050.json").read_text(encoding="utf-8"))

    assert latest["phase"] == "prove"
    assert latest["status"] == "completed"
    assert latest["attempt_id"] == "attempt.demo.050"
    package = attempt["proof_attempt"]["positive_subgoal_package"]
    assert package["source"] == "mathematical_layers+branch_execution"
    assert package["supporting_branch_execution_id"] == "discexec.demo.001"
    assert package["readiness_mode"] == "symbolic-search-ready"
    assert package["readiness_score"] == 10
    assert package["positive_shapes"] == ["realization", "transport"]
    assert "Transport theorem for Witness family" in package["candidate_titles"]
    assert "Define the transport map from the route-side object to the target-side object." in package["candidate_obligations"]


def test_prove_phase_advances_grounded_attempt_to_shape_specific_constructive_stage(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    attempts_dir = artifacts_dir / "proof-attempts"
    attempts_dir.mkdir(parents=True, exist_ok=True)

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|expert-conjecture-demo",
                "title": "Witness-family transport theorem",
                "priority": 0.92,
                "bridge_id": "bridge.001",
                "claim_type": "expert-conjecture",
                "claim_text": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
                "conjecture_statement": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "source_excerpt": "Source theorem excerpt.",
                "target_excerpt": "Target theorem excerpt.",
                "route_synopsis": "Transport the source lower bound to the target theorem through a Witness family.",
                "candidate_object": "Witness family",
                "carrier_kind": "family of witness instances",
                "preserved_invariant": "witness profile",
                "proof_strategy_family": "transport",
                "missing_route_lemma": "Witness-family transport lemma",
                "negative_route": "Assume the witness family fails to preserve the invariant.",
                "failure_diagnosis": "The route fails if the witness family cannot preserve the invariant.",
                "proof_obligations": ["Show the witness family preserves the invariant."],
                "status": "in_progress",
                "attempt_ids": ["attempt.demo.001"],
            }
        ],
    )
    save_proof_queue(
        queue,
        json_path=artifacts_dir / "proof-queue.json",
        md_path=artifacts_dir / "proof-queue.md",
    )
    save_mathlib_index(
        default_mathlib(kb_ref="demo"),
        json_path=repo_root / "InformalMathLib" / "demo" / "index.json",
        md_path=repo_root / "InformalMathLib" / "demo" / "catalog.md",
    )
    _write_branch_execution_artifact(
        artifacts_dir,
        branch_id="disclayer.demo.pattern.transport",
        queue_id="proofq.demo.001",
        title="Witness-family transport theorem",
    )
    _write_json(
        attempts_dir / "attempt.demo.001.json",
        {
            "metadata": {
                "attempt_id": "attempt.demo.001",
                "queue_id": "proofq.demo.001",
                "status": "in_progress",
                "resume_count": 1,
                "continuation_stage": 1,
            },
            "target": {
                "title": "Witness-family transport theorem",
                "bridge_id": "bridge.001",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "candidate_object": "Witness family",
                "preserved_invariant": "witness profile",
                "missing_route_lemma": "Witness-family transport lemma",
                "conjecture_statement": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
                "route_synopsis": "Transport the source lower bound to the target theorem through a Witness family.",
                "discovery_branch_id": "disclayer.demo.pattern.transport",
                "mathematical_layers": _math_layers(),
                "negative_route": "Assume the witness family fails to preserve the invariant.",
                "failure_diagnosis": "The route fails if the witness family cannot preserve the invariant.",
            },
            "local_context": {
                "mathlib_hits": [
                    {
                        "result_id": "mathlib.demo.blocked.001",
                        "outcome": "blocked",
                        "title": "Earlier blocked transport route",
                    }
                ]
            },
            "proof_attempt": {
                "theorem_statement": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
                "route_lemma_under_test": "Witness-family transport lemma",
                "strategy": "transport",
                "assumptions": ["Assume an admissible Witness family exists."],
                "informal_tactic_trace": [
                    {"order": 1, "tactic_id": "normalize-goal", "status": "completed", "notes": []},
                    {"order": 2, "tactic_id": "introduce-assumptions", "status": "completed", "notes": []},
                    {"order": 3, "tactic_id": "reduce-to-route-lemma", "status": "completed", "notes": []},
                    {"order": 4, "tactic_id": "extract-subgoal", "status": "completed", "notes": []},
                    {"order": 5, "tactic_id": "construct-witness", "status": "in_progress", "notes": []},
                    {"order": 6, "tactic_id": "transport-invariant", "status": "in_progress", "notes": []},
                    {"order": 7, "tactic_id": "activate-target-theorem", "status": "completed", "notes": []},
                    {"order": 8, "tactic_id": "negate-goal", "status": "pending", "notes": []},
                    {"order": 9, "tactic_id": "obstruction-probe", "status": "completed", "notes": []},
                    {"order": 10, "tactic_id": "derive-contradiction", "status": "pending", "notes": []},
                    {"order": 11, "tactic_id": "prove-impossibility-claim", "status": "pending", "notes": []},
                ],
                "stepwise_argument": [{"step": 1, "claim": "Assume the Witness family exists.", "justification": "Proof scaffold."}],
                "local_results_used": [{"result_id": "mathlib.demo.blocked.001", "title": "Earlier blocked transport route", "outcome": "blocked", "role": "Imported blocker."}],
                "continuation_log": [{"stage": 1, "headline": "Grounding pass", "details": ["Imported one blocker."]}],
                "negative_argument": {
                    "obstruction_candidate": "Assume the witness family fails to preserve the invariant.",
                    "counterexample_or_barrier": "Earlier blocked transport route",
                    "effect_on_claim": "",
                    "negated_claim": "",
                    "contradiction_target": "",
                    "forbidden_outcome": "The route fails if the witness family cannot preserve the invariant.",
                    "impossibility_claim": "",
                },
                "contradiction_frame": {},
            },
            "critique_judges": [
                {"judge_id": "local-counterexample-search", "title": "Local Counterexample-Search Judge", "questions": [], "verdict": "in_progress", "blocking_issues": [], "notes": []},
                {"judge_id": "obstruction-and-negative-route", "title": "Obstruction And Negative-Route Judge", "questions": [], "verdict": "in_progress", "blocking_issues": [], "notes": []},
                {"judge_id": "contradiction-and-impossibility-discipline", "title": "Contradiction And Impossibility Discipline Judge", "questions": [], "verdict": "pending", "blocking_issues": [], "notes": []},
            ],
            "final_assessment": {"outcome": "in_progress"},
        },
    )
    (attempts_dir / "attempt.demo.001.md").write_text("# Attempt\n", encoding="utf-8")

    latest = run_prove_phase(repo_root=repo_root, artifacts_dir=artifacts_dir, kb_ref="demo", kb_path=None)
    attempt = json.loads((attempts_dir / "attempt.demo.001.json").read_text(encoding="utf-8"))

    assert latest["phase"] == "prove"
    assert latest["status"] == "completed"
    assert latest["attempt_id"] == "attempt.demo.001"
    assert attempt["metadata"]["continuation_stage"] == 2
    assert attempt["metadata"]["resume_count"] == 2
    assert attempt["proof_attempt"]["positive_subgoal_package"]["positive_shapes"] == ["realization", "transport"]
    assert len(attempt["proof_attempt"]["continuation_log"]) == 2
    trace = {row["tactic_id"]: row["status"] for row in attempt["proof_attempt"]["informal_tactic_trace"]}
    assert trace["derive-contradiction"] == "in_progress"
    assert trace["prove-impossibility-claim"] == "pending"
    assert attempt["proof_attempt"]["negative_argument"]["impossibility_claim"] == ""
    assert "Pressed the constructive branch through shape-specific obligations" in attempt["proof_attempt"]["continuation_log"][-1]["headline"]
    assert "Construct a concrete witness" in " ".join(attempt["proof_attempt"]["continuation_log"][-1]["details"])
    assert "Define the transport map" in " ".join(attempt["proof_attempt"]["continuation_log"][-1]["details"])
    judges = {row["judge_id"]: row for row in attempt["critique_judges"]}
    assert judges["local-counterexample-search"]["verdict"] == "in_progress"
    assert judges["obstruction-and-negative-route"]["verdict"] == "in_progress"
    assert judges["contradiction-and-impossibility-discipline"]["verdict"] == "pending"
    assert judges["inferential-validity"]["verdict"] == "in_progress"


def test_prove_phase_exposes_factorization_shape_when_branch_packet_keeps_it_live(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    attempts_dir = artifacts_dir / "proof-attempts"
    attempts_dir.mkdir(parents=True, exist_ok=True)

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|expert-conjecture-demo",
                "title": "Witness-family transport theorem",
                "priority": 0.92,
                "bridge_id": "bridge.001",
                "claim_type": "expert-conjecture",
                "claim_text": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
                "conjecture_statement": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "source_excerpt": "Source theorem excerpt.",
                "target_excerpt": "Target theorem excerpt.",
                "route_synopsis": "Transport the source lower bound to the target theorem through a Witness family.",
                "candidate_object": "Witness family",
                "carrier_kind": "family of witness instances",
                "preserved_invariant": "witness profile",
                "proof_strategy_family": "transport",
                "missing_route_lemma": "Witness-family transport lemma",
                "negative_route": "Assume the witness family fails to preserve the invariant.",
                "failure_diagnosis": "The route fails if the witness family cannot preserve the invariant.",
                "proof_obligations": ["Show the witness family preserves the invariant."],
                "status": "in_progress",
                "attempt_ids": ["attempt.demo.001"],
            }
        ],
    )
    save_proof_queue(
        queue,
        json_path=artifacts_dir / "proof-queue.json",
        md_path=artifacts_dir / "proof-queue.md",
    )
    save_mathlib_index(
        default_mathlib(kb_ref="demo"),
        json_path=repo_root / "InformalMathLib" / "demo" / "index.json",
        md_path=repo_root / "InformalMathLib" / "demo" / "catalog.md",
    )
    _write_branch_execution_artifact(
        artifacts_dir,
        branch_id="disclayer.demo.pattern.transport",
        queue_id="proofq.demo.001",
        title="Witness-family transport theorem",
        include_factorization=True,
    )
    _write_json(
        attempts_dir / "attempt.demo.001.json",
        {
            "metadata": {
                "attempt_id": "attempt.demo.001",
                "queue_id": "proofq.demo.001",
                "status": "in_progress",
                "resume_count": 1,
                "continuation_stage": 1,
            },
            "target": {
                "title": "Witness-family transport theorem",
                "bridge_id": "bridge.001",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "candidate_object": "Witness family",
                "preserved_invariant": "witness profile",
                "missing_route_lemma": "Witness-family transport lemma",
                "conjecture_statement": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
                "route_synopsis": "Transport the source lower bound to the target theorem through a Witness family.",
                "discovery_branch_id": "disclayer.demo.pattern.transport",
                "mathematical_layers": _math_layers(),
                "negative_route": "Assume the witness family fails to preserve the invariant.",
                "failure_diagnosis": "The route fails if the witness family cannot preserve the invariant.",
            },
            "local_context": {
                "mathlib_hits": [
                    {
                        "result_id": "mathlib.demo.blocked.001",
                        "outcome": "blocked",
                        "title": "Earlier blocked transport route",
                    }
                ]
            },
            "proof_attempt": {
                "theorem_statement": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
                "route_lemma_under_test": "Witness-family transport lemma",
                "strategy": "transport",
                "assumptions": ["Assume an admissible Witness family exists."],
                "informal_tactic_trace": [
                    {"order": 1, "tactic_id": "normalize-goal", "status": "completed", "notes": []},
                    {"order": 2, "tactic_id": "introduce-assumptions", "status": "completed", "notes": []},
                    {"order": 3, "tactic_id": "reduce-to-route-lemma", "status": "completed", "notes": []},
                    {"order": 4, "tactic_id": "extract-subgoal", "status": "completed", "notes": []},
                    {"order": 5, "tactic_id": "construct-witness", "status": "in_progress", "notes": []},
                    {"order": 6, "tactic_id": "transport-invariant", "status": "in_progress", "notes": []},
                    {"order": 7, "tactic_id": "activate-target-theorem", "status": "completed", "notes": []},
                    {"order": 8, "tactic_id": "negate-goal", "status": "pending", "notes": []},
                    {"order": 9, "tactic_id": "obstruction-probe", "status": "completed", "notes": []},
                    {"order": 10, "tactic_id": "derive-contradiction", "status": "pending", "notes": []},
                    {"order": 11, "tactic_id": "prove-impossibility-claim", "status": "pending", "notes": []},
                ],
                "stepwise_argument": [{"step": 1, "claim": "Assume the Witness family exists.", "justification": "Proof scaffold."}],
                "local_results_used": [{"result_id": "mathlib.demo.blocked.001", "title": "Earlier blocked transport route", "outcome": "blocked", "role": "Imported blocker."}],
                "continuation_log": [{"stage": 1, "headline": "Grounding pass", "details": ["Imported one blocker."]}],
                "negative_argument": {
                    "obstruction_candidate": "Assume the witness family fails to preserve the invariant.",
                    "counterexample_or_barrier": "Earlier blocked transport route",
                    "effect_on_claim": "",
                    "negated_claim": "",
                    "contradiction_target": "",
                    "forbidden_outcome": "The route fails if the witness family cannot preserve the invariant.",
                    "impossibility_claim": "",
                },
                "contradiction_frame": {},
            },
            "critique_judges": [
                {"judge_id": "local-counterexample-search", "title": "Local Counterexample-Search Judge", "questions": [], "verdict": "in_progress", "blocking_issues": [], "notes": []},
                {"judge_id": "obstruction-and-negative-route", "title": "Obstruction And Negative-Route Judge", "questions": [], "verdict": "in_progress", "blocking_issues": [], "notes": []},
                {"judge_id": "contradiction-and-impossibility-discipline", "title": "Contradiction And Impossibility Discipline Judge", "questions": [], "verdict": "pending", "blocking_issues": [], "notes": []},
            ],
            "final_assessment": {"outcome": "in_progress"},
        },
    )
    (attempts_dir / "attempt.demo.001.md").write_text("# Attempt\n", encoding="utf-8")

    latest = run_prove_phase(repo_root=repo_root, artifacts_dir=artifacts_dir, kb_ref="demo", kb_path=None)
    attempt = json.loads((attempts_dir / "attempt.demo.001.json").read_text(encoding="utf-8"))

    assert latest["phase"] == "prove"
    assert latest["status"] == "completed"
    assert latest["attempt_id"] == "attempt.demo.001"
    details = " ".join(attempt["proof_attempt"]["continuation_log"][-1]["details"])
    assert "Exhibit an intermediate typed object factoring the route through the witness family." in details
    assert "factorization" in details
    judges = {row["judge_id"]: row for row in attempt["critique_judges"]}
    assert judges["inferential-validity"]["verdict"] == "in_progress"
    assert "factorization" in " ".join(judges["inferential-validity"]["notes"])


def test_prove_phase_exposes_equivalence_shape_when_branch_packet_keeps_it_live(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    attempts_dir = artifacts_dir / "proof-attempts"
    attempts_dir.mkdir(parents=True, exist_ok=True)

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|expert-conjecture-demo",
                "title": "Witness-family equivalence theorem",
                "priority": 0.92,
                "bridge_id": "bridge.001",
                "claim_type": "expert-conjecture",
                "claim_text": "For every admissible Witness family, the route-side and target-side operationalizations are equivalent in the sense needed for the target theorem.",
                "conjecture_statement": "For every admissible Witness family, the route-side and target-side operationalizations are equivalent in the sense needed for the target theorem.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "source_excerpt": "Source theorem excerpt.",
                "target_excerpt": "Target theorem excerpt.",
                "route_synopsis": "Identify an equivalence witness between the route-side and target-side operationalizations.",
                "candidate_object": "Witness family",
                "carrier_kind": "family of witness instances",
                "preserved_invariant": "witness profile",
                "proof_strategy_family": "equivalence-transport",
                "missing_route_lemma": "Witness-family equivalence lemma",
                "negative_route": "Assume the route-side and target-side operationalizations are not equivalent.",
                "failure_diagnosis": "The route fails if the equivalence witness cannot be made explicit.",
                "proof_obligations": ["Show the equivalence preserves the invariant."],
                "status": "in_progress",
                "attempt_ids": ["attempt.demo.001"],
            }
        ],
    )
    save_proof_queue(
        queue,
        json_path=artifacts_dir / "proof-queue.json",
        md_path=artifacts_dir / "proof-queue.md",
    )
    save_mathlib_index(
        default_mathlib(kb_ref="demo"),
        json_path=repo_root / "InformalMathLib" / "demo" / "index.json",
        md_path=repo_root / "InformalMathLib" / "demo" / "catalog.md",
    )
    _write_branch_execution_artifact(
        artifacts_dir,
        branch_id="disclayer.demo.pattern.equivalence",
        queue_id="proofq.demo.001",
        title="Witness-family equivalence theorem",
        include_equivalence=True,
    )
    _write_json(
        attempts_dir / "attempt.demo.001.json",
        {
            "metadata": {
                "attempt_id": "attempt.demo.001",
                "queue_id": "proofq.demo.001",
                "status": "in_progress",
                "resume_count": 1,
                "continuation_stage": 1,
            },
            "target": {
                "title": "Witness-family equivalence theorem",
                "bridge_id": "bridge.001",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "candidate_object": "Witness family",
                "preserved_invariant": "witness profile",
                "missing_route_lemma": "Witness-family equivalence lemma",
                "conjecture_statement": "For every admissible Witness family, the route-side and target-side operationalizations are equivalent in the sense needed for the target theorem.",
                "route_synopsis": "Identify an equivalence witness between the route-side and target-side operationalizations.",
                "discovery_branch_id": "disclayer.demo.pattern.equivalence",
                "mathematical_layers": _math_layers(theorem_name="witness_family_equivalence"),
                "negative_route": "Assume the route-side and target-side operationalizations are not equivalent.",
                "failure_diagnosis": "The route fails if the equivalence witness cannot be made explicit.",
            },
            "local_context": {
                "mathlib_hits": [
                    {
                        "result_id": "mathlib.demo.blocked.001",
                        "outcome": "blocked",
                        "title": "Earlier blocked equivalence route",
                    }
                ]
            },
            "proof_attempt": {
                "theorem_statement": "For every admissible Witness family, the route-side and target-side operationalizations are equivalent in the sense needed for the target theorem.",
                "route_lemma_under_test": "Witness-family equivalence lemma",
                "strategy": "equivalence-transport",
                "assumptions": ["Assume an admissible Witness family exists."],
                "informal_tactic_trace": [
                    {"order": 1, "tactic_id": "normalize-goal", "status": "completed", "notes": []},
                    {"order": 2, "tactic_id": "introduce-assumptions", "status": "completed", "notes": []},
                    {"order": 3, "tactic_id": "reduce-to-route-lemma", "status": "completed", "notes": []},
                    {"order": 4, "tactic_id": "extract-subgoal", "status": "completed", "notes": []},
                    {"order": 5, "tactic_id": "construct-witness", "status": "in_progress", "notes": []},
                    {"order": 6, "tactic_id": "transport-invariant", "status": "in_progress", "notes": []},
                    {"order": 7, "tactic_id": "activate-target-theorem", "status": "completed", "notes": []},
                    {"order": 8, "tactic_id": "negate-goal", "status": "pending", "notes": []},
                    {"order": 9, "tactic_id": "obstruction-probe", "status": "completed", "notes": []},
                    {"order": 10, "tactic_id": "derive-contradiction", "status": "pending", "notes": []},
                    {"order": 11, "tactic_id": "prove-impossibility-claim", "status": "pending", "notes": []},
                ],
                "stepwise_argument": [{"step": 1, "claim": "Assume the Witness family exists.", "justification": "Proof scaffold."}],
                "local_results_used": [{"result_id": "mathlib.demo.blocked.001", "title": "Earlier blocked equivalence route", "outcome": "blocked", "role": "Imported blocker."}],
                "continuation_log": [{"stage": 1, "headline": "Grounding pass", "details": ["Imported one blocker."]}],
                "negative_argument": {
                    "obstruction_candidate": "Assume the route-side and target-side operationalizations are not equivalent.",
                    "counterexample_or_barrier": "Earlier blocked equivalence route",
                    "effect_on_claim": "",
                    "negated_claim": "",
                    "contradiction_target": "",
                    "forbidden_outcome": "The route fails if the equivalence witness cannot be made explicit.",
                    "impossibility_claim": "",
                },
                "contradiction_frame": {},
            },
            "critique_judges": [
                {"judge_id": "local-counterexample-search", "title": "Local Counterexample-Search Judge", "questions": [], "verdict": "in_progress", "blocking_issues": [], "notes": []},
                {"judge_id": "obstruction-and-negative-route", "title": "Obstruction And Negative-Route Judge", "questions": [], "verdict": "in_progress", "blocking_issues": [], "notes": []},
                {"judge_id": "contradiction-and-impossibility-discipline", "title": "Contradiction And Impossibility Discipline Judge", "questions": [], "verdict": "pending", "blocking_issues": [], "notes": []},
            ],
            "final_assessment": {"outcome": "in_progress"},
        },
    )
    (attempts_dir / "attempt.demo.001.md").write_text("# Attempt\n", encoding="utf-8")

    latest = run_prove_phase(repo_root=repo_root, artifacts_dir=artifacts_dir, kb_ref="demo", kb_path=None)
    attempt = json.loads((attempts_dir / "attempt.demo.001.json").read_text(encoding="utf-8"))

    assert latest["phase"] == "prove"
    assert latest["status"] == "completed"
    assert latest["attempt_id"] == "attempt.demo.001"
    details = " ".join(attempt["proof_attempt"]["continuation_log"][-1]["details"])
    assert "Construct the equivalence witness for the witness family." in details
    assert "coherence or naturality law" in details
    judges = {row["judge_id"]: row for row in attempt["critique_judges"]}
    assert judges["inferential-validity"]["verdict"] == "in_progress"
    assert "equivalence" in " ".join(judges["inferential-validity"]["notes"])


def test_prove_phase_advances_shape_specific_attempt_to_impossibility_stage(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    attempts_dir = artifacts_dir / "proof-attempts"
    attempts_dir.mkdir(parents=True, exist_ok=True)

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|expert-conjecture-demo",
                "title": "Witness-family transport theorem",
                "priority": 0.92,
                "bridge_id": "bridge.001",
                "claim_type": "expert-conjecture",
                "claim_text": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
                "conjecture_statement": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "source_excerpt": "Source theorem excerpt.",
                "target_excerpt": "Target theorem excerpt.",
                "route_synopsis": "Transport the source lower bound to the target theorem through a Witness family.",
                "candidate_object": "Witness family",
                "carrier_kind": "family of witness instances",
                "preserved_invariant": "witness profile",
                "proof_strategy_family": "transport",
                "missing_route_lemma": "Witness-family transport lemma",
                "negative_route": "Assume the witness family fails to preserve the invariant.",
                "failure_diagnosis": "The route fails if the witness family cannot preserve the invariant.",
                "proof_obligations": ["Show the witness family preserves the invariant."],
                "status": "in_progress",
                "attempt_ids": ["attempt.demo.001"],
            }
        ],
    )
    save_proof_queue(
        queue,
        json_path=artifacts_dir / "proof-queue.json",
        md_path=artifacts_dir / "proof-queue.md",
    )
    save_mathlib_index(
        default_mathlib(kb_ref="demo"),
        json_path=repo_root / "InformalMathLib" / "demo" / "index.json",
        md_path=repo_root / "InformalMathLib" / "demo" / "catalog.md",
    )
    _write_branch_execution_artifact(
        artifacts_dir,
        branch_id="disclayer.demo.pattern.transport",
        queue_id="proofq.demo.001",
        title="Witness-family transport theorem",
    )
    _write_json(
        attempts_dir / "attempt.demo.001.json",
        {
            "metadata": {
                "attempt_id": "attempt.demo.001",
                "queue_id": "proofq.demo.001",
                "status": "in_progress",
                "resume_count": 2,
                "continuation_stage": 2,
            },
            "target": {
                "title": "Witness-family transport theorem",
                "bridge_id": "bridge.001",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "candidate_object": "Witness family",
                "preserved_invariant": "witness profile",
                "missing_route_lemma": "Witness-family transport lemma",
                "conjecture_statement": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
                "route_synopsis": "Transport the source lower bound to the target theorem through a Witness family.",
                "discovery_branch_id": "disclayer.demo.pattern.transport",
                "mathematical_layers": _math_layers(),
                "negative_route": "Assume the witness family fails to preserve the invariant.",
                "failure_diagnosis": "The route fails if the witness family cannot preserve the invariant.",
            },
            "local_context": {
                "mathlib_hits": [
                    {
                        "result_id": "mathlib.demo.blocked.001",
                        "outcome": "blocked",
                        "title": "Earlier blocked transport route",
                    }
                ]
            },
            "proof_attempt": {
                "theorem_statement": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
                "route_lemma_under_test": "Witness-family transport lemma",
                "strategy": "transport",
                "assumptions": ["Assume an admissible Witness family exists."],
                "informal_tactic_trace": [
                    {"order": 1, "tactic_id": "normalize-goal", "status": "completed", "notes": []},
                    {"order": 2, "tactic_id": "introduce-assumptions", "status": "completed", "notes": []},
                    {"order": 3, "tactic_id": "reduce-to-route-lemma", "status": "completed", "notes": []},
                    {"order": 4, "tactic_id": "extract-subgoal", "status": "completed", "notes": []},
                    {"order": 5, "tactic_id": "construct-witness", "status": "in_progress", "notes": []},
                    {"order": 6, "tactic_id": "transport-invariant", "status": "in_progress", "notes": []},
                    {"order": 7, "tactic_id": "activate-target-theorem", "status": "completed", "notes": []},
                    {"order": 8, "tactic_id": "negate-goal", "status": "completed", "notes": []},
                    {"order": 9, "tactic_id": "obstruction-probe", "status": "completed", "notes": []},
                    {"order": 10, "tactic_id": "derive-contradiction", "status": "in_progress", "notes": []},
                    {"order": 11, "tactic_id": "prove-impossibility-claim", "status": "pending", "notes": []},
                ],
                "stepwise_argument": [{"step": 1, "claim": "Assume the Witness family exists.", "justification": "Proof scaffold."}],
                "local_results_used": [{"result_id": "mathlib.demo.blocked.001", "title": "Earlier blocked transport route", "outcome": "blocked", "role": "Imported blocker."}],
                "continuation_log": [
                    {"stage": 1, "headline": "Grounding pass", "details": ["Imported one blocker."]},
                    {"stage": 2, "headline": "Constructive pass", "details": ["Pressed realization and transport obligations."]},
                ],
                "negative_argument": {
                    "obstruction_candidate": "Assume the witness family fails to preserve the invariant.",
                    "counterexample_or_barrier": "Earlier blocked transport route",
                    "effect_on_claim": "",
                    "negated_claim": "",
                    "contradiction_target": "",
                    "forbidden_outcome": "The route fails if the witness family cannot preserve the invariant.",
                    "impossibility_claim": "",
                },
                "contradiction_frame": {},
            },
            "critique_judges": [
                {"judge_id": "local-counterexample-search", "title": "Local Counterexample-Search Judge", "questions": [], "verdict": "in_progress", "blocking_issues": [], "notes": []},
                {"judge_id": "obstruction-and-negative-route", "title": "Obstruction And Negative-Route Judge", "questions": [], "verdict": "in_progress", "blocking_issues": [], "notes": []},
                {"judge_id": "contradiction-and-impossibility-discipline", "title": "Contradiction And Impossibility Discipline Judge", "questions": [], "verdict": "pending", "blocking_issues": [], "notes": []},
            ],
            "final_assessment": {"outcome": "in_progress"},
        },
    )
    (attempts_dir / "attempt.demo.001.md").write_text("# Attempt\n", encoding="utf-8")

    latest = run_prove_phase(repo_root=repo_root, artifacts_dir=artifacts_dir, kb_ref="demo", kb_path=None)
    attempt = json.loads((attempts_dir / "attempt.demo.001.json").read_text(encoding="utf-8"))

    assert latest["phase"] == "prove"
    assert latest["status"] == "completed"
    assert latest["attempt_id"] == "attempt.demo.001"
    assert attempt["metadata"]["continuation_stage"] == 3
    assert attempt["metadata"]["resume_count"] == 3
    assert attempt["proof_attempt"]["positive_subgoal_package"]["positive_shapes"] == ["realization", "transport"]
    assert "No admissible `Witness family` currently discharges `Witness-family transport lemma`" in attempt["proof_attempt"]["negative_argument"]["impossibility_claim"]
    assert len(attempt["proof_attempt"]["continuation_log"]) == 3
    assert "Synthesized the negative branch into a theorem-shaped impossibility candidate." in attempt["proof_attempt"]["continuation_log"][-1]["headline"]
    trace = {row["tactic_id"]: row["status"] for row in attempt["proof_attempt"]["informal_tactic_trace"]}
    assert trace["derive-contradiction"] == "in_progress"
    assert trace["prove-impossibility-claim"] == "in_progress"
    judges = {row["judge_id"]: row for row in attempt["critique_judges"]}
    assert judges["local-counterexample-search"]["verdict"] == "passes"
    assert judges["obstruction-and-negative-route"]["verdict"] == "blocking"
    assert judges["contradiction-and-impossibility-discipline"]["verdict"] == "in_progress"


def test_work_cycle_invokes_meta_on_cycle_interval(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    _write_json(artifacts_dir / "expert-hypothesis-paper.json", {"recommended_bridges": [_bridge()]})
    _write_json(
        artifacts_dir / "search-space-tree.json",
        {
            "frontier": {"resume": [{"bridge_id": "bridge.001", "policy": "resume-with-deeper-proof", "priority": 0.95}]},
            "routes": [{"bridge_id": "bridge.001", "route_signature": "route.demo.001", "priority": 0.95, "dimensions": {"source_statement_id": "st.src", "target_statement_id": "st.tgt"}}],
        },
    )
    _write_json(
        artifacts_dir / "macro-proof-state.json",
        {
            "main_conjecture": {
                "core_claim": "Demo main claim",
                "route_target_claim": "Demo route target",
                "grounding_implication": "If demo route target then demo main claim.",
            },
            "leading_route": {
                "candidate_object": "Witness family",
                "carrier_kind": "family of instances equipped with a witness measure",
                "negative_route": "The witness family might fail.",
                "failure_diagnosis": "The route fails if the witness family is only topical overlap.",
                "mathematical_assumptions": ["Assume an admissible witness family exists."],
                "proof_obligations": ["Build the witness family."],
                "candidate_lemmas": ["The source theorem induces the witness family."],
                "proof_outline": ["Build.", "Transport.", "Payoff."],
            },
            "status_assessment": {"evidence_count": 0, "novelty_argument": "Programme-level novelty only."},
        },
    )
    _write_json(
        artifacts_dir / "macro-strategy-report.json",
        {
            "operationalizations": [{"object": "Witness family", "carrier_kind": "family of instances equipped with a witness measure"}],
            "missing_for_completion": [{"kind": "route-lemma", "title": "Route lemma"}],
            "completion_checklist": [{"status": "open", "title": "Route lemma"}],
        },
    )
    _write_json(artifacts_dir / "proof-cycle-summary.json", {"metadata": {"pending_count": 1, "proved_count": 0, "blocked_count": 0}})
    mathlib_json = repo_root / "InformalMathLib" / "demo" / "index.json"
    mathlib_md = repo_root / "InformalMathLib" / "demo" / "catalog.md"
    save_mathlib_index(default_mathlib(kb_ref="demo"), json_path=mathlib_json, md_path=mathlib_md)

    state = default_work_state(kb_ref="demo", max_cycles=3)
    state["metadata"]["meta_interval"] = 2
    state, latest = execute_work_cycle(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref="demo",
        kb_path=None,
        state=state,
        phase_override="auto",
        top_k=4,
        non_authoritative_legacy_compatibility=True,
    )
    assert "meta_reflection_md" not in latest.get("outputs", {})

    state, latest = execute_work_cycle(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref="demo",
        kb_path=None,
        state=state,
        phase_override="auto",
        top_k=4,
        non_authoritative_legacy_compatibility=True,
    )
    assert latest["meta_trigger_reason"] == "cycle-interval-2"
    assert "meta_reflection_md" in latest["outputs"]
    assert "meta_reasoning_log_md" in latest["outputs"]
    assert "meta_reasoning_surface_md" in latest["outputs"]
    assert "meta_reasoning_surface_json" in latest["outputs"]
    meta_json, meta_md, meta_tex, meta_pdf = meta_report_paths(artifacts_dir)
    assert meta_json.exists()
    assert meta_md.exists()
    assert meta_tex.exists()
    assert meta_pdf.exists()
    assert Path(latest["outputs"]["meta_reasoning_log_md"]).exists()
    assert Path(latest["outputs"]["meta_reasoning_surface_md"]).exists()
    assert Path(latest["outputs"]["meta_reasoning_surface_json"]).exists()


def test_work_cycle_defers_budget_stop_when_high_reward_followups_remain_live(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    _write_json(artifacts_dir / "expert-hypothesis-paper.json", {"recommended_bridges": [_bridge()]})
    _write_json(
        artifacts_dir / "search-space-tree.json",
        {
            "frontier": {"resume": [{"bridge_id": "bridge.001", "policy": "resume-with-deeper-proof", "priority": 0.95}]},
            "routes": [{"bridge_id": "bridge.001", "route_signature": "route.demo.001", "priority": 0.95, "dimensions": {"source_statement_id": "st.src", "target_statement_id": "st.tgt"}}],
        },
    )
    _write_json(
        artifacts_dir / "macro-proof-state.json",
        {
            "main_conjecture": {
                "core_claim": "Demo main claim",
                "route_target_claim": "Demo route target",
                "grounding_implication": "If demo route target then demo main claim.",
            },
            "leading_route": {
                "candidate_object": "Witness family",
                "carrier_kind": "family of instances equipped with a witness measure",
            },
            "status_assessment": {"evidence_count": 0},
        },
    )
    _write_json(artifacts_dir / "macro-strategy-report.json", {"completion_checklist": [{"status": "open", "title": "Route lemma"}]})
    _write_json(artifacts_dir / "proof-cycle-summary.json", {"metadata": {"pending_count": 1, "proved_count": 1, "blocked_count": 0}})

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|high-reward-followup-demo",
                "title": "High-reward follow-up",
                "priority": 0.97,
                "bridge_id": "bridge.001",
                "claim_type": "high-reward-followup",
                "claim_text": "Use the intermediate result to discharge the next route theorem.",
                "conjecture_statement": "Use the intermediate result to discharge the next route theorem.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "candidate_object": "Witness family",
                "preserved_invariant": "witness complexity profile",
                "missing_route_lemma": "Next route theorem.",
            }
        ],
    )
    save_proof_queue(queue, json_path=artifacts_dir / "proof-queue.json", md_path=artifacts_dir / "proof-queue.md")

    watch = default_high_reward_watch(kb_ref="demo")
    watch["signals"].append(
        {
            "signal_id": "highreward.demo.001",
            "status": "pending",
            "result_id": "mathlib.demo.003",
            "queue_id": "proofq.demo.999",
            "title": "Witness family transport theorem",
            "major_subresult_score": 12,
            "recommended_extension_cycles": 2,
            "continuation_rationale": "A standalone intermediate theorem created a live follow-up programme.",
            "follow_up_prove_queue_ids": ["proofq.demo.001"],
            "follow_up_discovery_branch_ids": [],
        }
    )
    save_high_reward_watch(
        watch,
        json_path=artifacts_dir / "high-reward-watch.json",
        md_path=artifacts_dir / "high-reward-watch.md",
    )

    mathlib_json = repo_root / "InformalMathLib" / "demo" / "index.json"
    mathlib_md = repo_root / "InformalMathLib" / "demo" / "catalog.md"
    save_mathlib_index(default_mathlib(kb_ref="demo"), json_path=mathlib_json, md_path=mathlib_md)

    state = default_work_state(kb_ref="demo", max_cycles=1)
    state["metadata"]["cycle_count"] = 1
    state["metadata"]["next_phase"] = "prove"
    state, latest = execute_work_cycle(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref="demo",
        kb_path=None,
        state=state,
        phase_override="auto",
        top_k=4,
        non_authoritative_legacy_compatibility=True,
    )
    assert latest["phase"] == "prove"
    assert latest["status"] == "completed"
    assert state["metadata"]["stop_status"] == "running"
    assert state["metadata"]["high_reward_active"] is True
    assert state["metadata"]["high_reward_signal_id"] == "highreward.demo.001"
    assert state["metadata"]["cycle_count"] == 2


def test_work_cycle_invokes_meta_when_queue_is_exhausted(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    _write_json(artifacts_dir / "expert-hypothesis-paper.json", {"recommended_bridges": [_bridge()]})
    _write_json(
        artifacts_dir / "search-space-tree.json",
        {
            "frontier": {"resume": []},
            "routes": [],
        },
    )
    _write_json(
        artifacts_dir / "macro-proof-state.json",
        {
            "main_conjecture": {
                "core_claim": "Demo main claim",
                "route_target_claim": "Demo route target",
                "grounding_implication": "If demo route target then demo main claim.",
            },
            "leading_route": {
                "candidate_object": "Witness family",
                "carrier_kind": "family of instances equipped with a witness measure",
            },
            "status_assessment": {"evidence_count": 0},
        },
    )
    _write_json(artifacts_dir / "macro-strategy-report.json", {"completion_checklist": [{"status": "open", "title": "Route lemma"}]})
    _write_json(artifacts_dir / "proof-cycle-summary.json", {"metadata": {"pending_count": 0, "proved_count": 0, "blocked_count": 0}})
    queue = default_queue(kb_ref="demo")
    save_proof_queue(queue, json_path=artifacts_dir / "proof-queue.json", md_path=artifacts_dir / "proof-queue.md")
    mathlib_json = repo_root / "InformalMathLib" / "demo" / "index.json"
    mathlib_md = repo_root / "InformalMathLib" / "demo" / "catalog.md"
    save_mathlib_index(default_mathlib(kb_ref="demo"), json_path=mathlib_json, md_path=mathlib_md)

    state = default_work_state(kb_ref="demo", max_cycles=3)
    state["metadata"]["next_phase"] = "prove"
    state["metadata"]["meta_interval"] = 99
    state, latest = execute_work_cycle(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref="demo",
        kb_path=None,
        state=state,
        phase_override="auto",
        top_k=4,
        non_authoritative_legacy_compatibility=True,
    )
    assert latest["phase"] == "prove"
    assert latest["status"] == "idle"
    assert latest["meta_trigger_reason"] == "queue-exhausted"
    assert "meta_reflection_md" in latest["outputs"]
    assert Path(latest["outputs"]["meta_reasoning_log_md"]).exists()


def test_work_cycle_does_not_reopen_same_route_after_discovery_refresh(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    bridge_one = _bridge()
    bridge_two = {
        **_bridge(),
        "bridge_id": "bridge.002",
        "priority": 0.87,
        "target_statement_id": "st.tgt.2",
        "target_excerpt": "Second target theorem excerpt.",
        "missing_route_lemma": "Prove the second witness route.",
        "statement_delta": {
            **_bridge()["statement_delta"],
            "target_claim_focus": "second major target separation",
        },
    }

    _write_json(
        artifacts_dir / "expert-hypothesis-paper.json",
        {"recommended_bridges": [bridge_one, bridge_two]},
    )
    _write_json(
        artifacts_dir / "search-space-tree.json",
        {
            "frontier": {
                "resume": [
                    {"bridge_id": "bridge.001", "policy": "resume-with-deeper-proof", "priority": 0.95},
                    {"bridge_id": "bridge.002", "policy": "resume-with-deeper-proof", "priority": 0.88},
                ]
            },
            "routes": [
                {
                    "bridge_id": "bridge.001",
                    "route_signature": "route.demo.001",
                    "priority": 0.95,
                    "dimensions": {"source_statement_id": "st.src", "target_statement_id": "st.tgt"},
                },
                {
                    "bridge_id": "bridge.002",
                    "route_signature": "route.demo.002",
                    "priority": 0.88,
                    "dimensions": {"source_statement_id": "st.src", "target_statement_id": "st.tgt.2"},
                },
            ],
        },
    )
    _write_json(
        artifacts_dir / "macro-proof-state.json",
        {
            "main_conjecture": {
                "core_claim": "Demo main claim",
                "route_target_claim": "Demo route target",
                "grounding_implication": "If demo route target then demo main claim.",
            },
            "leading_route": {
                "candidate_object": "Witness family",
                "carrier_kind": "family of instances equipped with a witness measure",
                "negative_route": "The witness family might fail.",
                "failure_diagnosis": "The route fails if the witness family is only topical overlap.",
                "mathematical_assumptions": ["Assume an admissible witness family exists."],
                "proof_obligations": ["Build the witness family."],
                "candidate_lemmas": ["The source theorem induces the witness family."],
                "proof_outline": ["Build.", "Transport.", "Payoff."],
            },
            "status_assessment": {"evidence_count": 0, "novelty_argument": "Programme-level novelty only."},
        },
    )
    _write_json(
        artifacts_dir / "macro-strategy-report.json",
        {
            "operationalizations": [{"object": "Witness family", "carrier_kind": "family of instances equipped with a witness measure"}],
            "missing_for_completion": [{"kind": "route-lemma", "title": "Route lemma"}],
            "completion_checklist": [
                {"status": "established", "title": "Grounding implication"},
                {"status": "open", "title": "Route lemma"},
            ],
        },
    )
    _write_json(
        artifacts_dir / "proof-cycle-summary.json",
        {
            "metadata": {
                "proved_count": 0,
                "disproved_count": 0,
                "blocked_count": 0,
                "produced_paper_count": 0,
                "external_reference_count": 0,
            }
        },
    )
    mathlib_json = repo_root / "InformalMathLib" / "demo" / "index.json"
    mathlib_md = repo_root / "InformalMathLib" / "demo" / "catalog.md"
    save_mathlib_index(default_mathlib(kb_ref="demo"), json_path=mathlib_json, md_path=mathlib_md)

    state = default_work_state(kb_ref="demo", max_cycles=4)

    state, latest = execute_work_cycle(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref="demo",
        kb_path=None,
        state=state,
        phase_override="auto",
        top_k=4,
        non_authoritative_legacy_compatibility=True,
    )
    assert latest["phase"] == "discovery"

    state, latest = execute_work_cycle(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref="demo",
        kb_path=None,
        state=state,
        phase_override="auto",
        top_k=4,
        non_authoritative_legacy_compatibility=True,
    )
    assert latest["phase"] == "prove"
    assert latest["queue_id"] == "proofq.demo.001"

    state, latest = execute_work_cycle(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref="demo",
        kb_path=None,
        state=state,
        phase_override="auto",
        top_k=4,
        non_authoritative_legacy_compatibility=True,
    )
    assert latest["phase"] == "discovery"

    state, latest = execute_work_cycle(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref="demo",
        kb_path=None,
        state=state,
        phase_override="auto",
        top_k=4,
        non_authoritative_legacy_compatibility=True,
    )
    assert latest["phase"] == "prove"
    assert latest["queue_id"] == "proofq.demo.001"
    assert "resumed proof attempt" in latest["detail"].lower()


def test_work_discovery_phase_reopens_blocked_abstraction_as_repair_lemma(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    attempts_dir = artifacts_dir / "proof-attempts"
    attempts_dir.mkdir(parents=True, exist_ok=True)

    _write_json(
        artifacts_dir / "expert-hypothesis-paper.json",
        {"recommended_bridges": [_bridge()]},
    )
    _write_json(
        artifacts_dir / "search-space-tree.json",
        {
            "frontier": {"resume": [{"bridge_id": "bridge.001", "policy": "re-encode-before-retrying", "priority": 0.95}]},
            "routes": [
                {
                    "bridge_id": "bridge.001",
                    "route_signature": "route.demo.001",
                    "priority": 0.95,
                    "dimensions": {"source_statement_id": "st.src", "target_statement_id": "st.tgt"},
                }
            ],
        },
    )
    _write_json(artifacts_dir / "concept-gap-abstractions.json", {"conjectures": []})

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|abstraction-conjecture-conj-002",
                "title": "Witness obstruction family: target",
                "priority": 0.74,
                "bridge_id": "bridge.001",
                "claim_type": "abstraction-conjecture",
                "conjecture_id": "conj.002",
                "claim_text": "Abstraction conjecture.",
                "conjecture_statement": "Abstraction conjecture.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "candidate_object": "Witness obstruction family",
                "carrier_kind": "family of hard instances",
                "preserved_invariant": "witness complexity profile",
                "route_synopsis": "Move from st.src to st.tgt through a formula-size route.",
                "missing_route_lemma": "Prove the formula-size transport theorem.",
                "source_excerpt": "Source theorem excerpt.",
                "target_excerpt": "Target theorem excerpt mentioning formula-size.",
            }
        ],
    )
    finalize_queue_entry(
        queue,
        queue_id="proofq.demo.001",
        outcome="blocked",
        result_id="",
        attempt_id="attempt.demo.010",
        summary="The current artifacts still lack the nonuniform-circuits -> formula-size transport theorem.",
    )
    save_proof_queue(
        queue,
        json_path=artifacts_dir / "proof-queue.json",
        md_path=artifacts_dir / "proof-queue.md",
    )

    _write_json(
        attempts_dir / "attempt.demo.010.json",
        {
            "metadata": {"attempt_id": "attempt.demo.010"},
            "target": {
                "bridge_id": "bridge.001",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "candidate_object": "Witness obstruction family",
                "carrier_kind": "family of hard instances",
                "preserved_invariant": "witness complexity profile",
                "route_synopsis": "Move from st.src to st.tgt through a formula-size route.",
                "missing_route_lemma": "Prove the formula-size transport theorem.",
                "source_excerpt": "Source theorem excerpt.",
                "target_excerpt": "Target theorem excerpt mentioning formula-size.",
                "statement_delta": {
                    "source_claim_focus": "source lower bound",
                    "target_claim_focus": "formula-size consequence",
                },
            },
            "proof_attempt": {
                "result_statement": "No local transport theorem reaches the formula-size regime.",
            },
            "final_assessment": {
                "summary": "The current artifacts still lack the nonuniform-circuits -> formula-size transport theorem."
            },
        },
    )

    latest = run_discovery_phase(repo_root=repo_root, artifacts_dir=artifacts_dir, kb_ref="demo", top_k=4)
    assert latest["phase"] == "discovery"
    assert latest["status"] == "completed"

    refreshed = load_proof_queue(artifacts_dir / "proof-queue.json", kb_ref="demo")
    repair_lemmas = [row for row in refreshed["entries"] if row.get("claim_type") == "repair-lemma"]
    assert len(repair_lemmas) == 1
    assert repair_lemmas[0]["status"] == "pending"
    assert "Formula-Size Transport Lemma" in repair_lemmas[0]["title"]


def test_work_discovery_phase_generates_breakthrough_profile_when_frontier_is_exhausted(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    _write_json(artifacts_dir / "expert-hypothesis-paper.json", {"recommended_bridges": [_bridge()]})
    _write_json(
        artifacts_dir / "search-space-tree.json",
        {
            "frontier": {"resume": [{"bridge_id": "bridge.001", "policy": "re-encode-before-retrying", "priority": 0.95}]},
            "routes": [
                {
                    "bridge_id": "bridge.001",
                    "route_signature": "route.demo.001",
                    "priority": 0.95,
                    "dimensions": {"source_statement_id": "st.src", "target_statement_id": "st.tgt"},
                }
            ],
        },
    )
    _write_json(artifacts_dir / "concept-gap-abstractions.json", {"conjectures": []})
    _write_json(
        artifacts_dir / "prior-art-pass-report.json",
        {
            "search_justification": "Queue exhausted.",
            "obstruction_map": [
                {
                    "name": "carrier-realization",
                    "reference_ids": ["mathlibref.demo.001"],
                    "titles": ["Known magnification theorem"],
                    "queue_ids": ["proofq.demo.001"],
                    "what_changed": ["Target is grounded; bridge is still open."],
                }
            ],
        },
    )

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|repair-lemma-carrier",
                "title": "Carrier Realization Lemma: target",
                "priority": 0.79,
                "bridge_id": "bridge.001",
                "claim_type": "repair-lemma",
                "claim_text": "Construct an explicit carrier realization theorem.",
                "conjecture_statement": "Construct an explicit carrier realization theorem.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
            }
        ],
    )
    finalize_queue_entry(
        queue,
        queue_id="proofq.demo.001",
        outcome="blocked",
        result_id="",
        attempt_id="attempt.demo.001",
        summary="The route remains blocked by carrier realization.",
    )
    save_proof_queue(
        queue,
        json_path=artifacts_dir / "proof-queue.json",
        md_path=artifacts_dir / "proof-queue.md",
    )

    latest = run_discovery_phase(repo_root=repo_root, artifacts_dir=artifacts_dir, kb_ref="demo", top_k=4)
    assert latest["phase"] == "discovery"
    assert latest["status"] == "completed"
    assert "breakthrough profile" in latest["detail"].lower()
    assert "discovery_breakthrough_profile_md" in latest["outputs"]
    assert "discovery_pattern_routing_md" in latest["outputs"]
    assert "discovery_branch_queue_md" in latest["outputs"]
    assert "discovery_governor_report_md" in latest["outputs"]

    breakthrough_json, breakthrough_md, breakthrough_tex, breakthrough_pdf = breakthrough_profile_paths(artifacts_dir)
    assert breakthrough_json.exists()
    assert breakthrough_md.exists()
    assert breakthrough_tex.exists()
    assert breakthrough_pdf.exists()
    routing_json, routing_md, routing_tex, routing_pdf = discovery_pattern_routing_paths(artifacts_dir)
    assert routing_json.exists()
    assert routing_md.exists()
    assert routing_tex.exists()
    assert routing_pdf.exists()
    branch_json, branch_md = discovery_branch_queue_paths(artifacts_dir)
    assert branch_json.exists()
    assert branch_md.exists()
    prompt_json = artifacts_dir / "discovery-family-prompts.json"
    prompt_md = artifacts_dir / "discovery-family-prompts.md"
    prompt_tex = artifacts_dir / "discovery-family-prompts.tex"
    prompt_pdf = artifacts_dir / "discovery-family-prompts.pdf"
    assert prompt_json.exists()
    assert prompt_md.exists()
    assert prompt_tex.exists()
    assert prompt_pdf.exists()
    prompt_payload = json.loads(prompt_json.read_text(encoding="utf-8"))
    assert prompt_payload["metadata"]["epistemic_pattern_count"] >= 1
    routing_payload = json.loads(routing_json.read_text(encoding="utf-8"))
    assert routing_payload["metadata"]["layer_count"] >= 2
    branch_payload = json.loads(branch_json.read_text(encoding="utf-8"))
    assert branch_payload["metadata"]["branch_count"] >= 2
    assert (
        branch_payload["metadata"]["completed_count"] >= 1
        or branch_payload["metadata"]["active_count"] >= 1
        or branch_payload["metadata"]["pending_count"] >= 1
        or branch_payload["metadata"]["deprioritized_count"] >= 1
    )


def test_work_discovery_phase_compiles_expert_conjectures_and_reopens_prove(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    _write_json(artifacts_dir / "expert-hypothesis-paper.json", {"recommended_bridges": [_bridge()]})
    _write_json(
        artifacts_dir / "search-space-tree.json",
        {
            "frontier": {"resume": [{"bridge_id": "bridge.001", "policy": "re-encode-before-retrying", "priority": 0.95}]},
            "routes": [
                {
                    "bridge_id": "bridge.001",
                    "route_signature": "route.demo.001",
                    "priority": 0.95,
                    "dimensions": {"source_statement_id": "st.src", "target_statement_id": "st.tgt"},
                }
            ],
        },
    )
    _write_json(artifacts_dir / "concept-gap-abstractions.json", {"conjectures": []})
    _write_json(
        artifacts_dir / "prior-art-pass-report.json",
        {
            "search_justification": "Queue exhausted.",
            "obstruction_map": [
                {
                    "name": "carrier-realization",
                    "reference_ids": ["mathlibref.demo.001"],
                    "titles": ["Known magnification theorem"],
                    "queue_ids": ["proofq.demo.001"],
                    "what_changed": ["The target is grounded but the carrier is not yet realized."],
                }
            ],
        },
    )

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|route-conjecture",
                "title": "Blocked realization route",
                "priority": 0.91,
                "bridge_id": "bridge.001",
                "claim_type": "route-conjecture",
                "conjecture_statement": "Construct an admissible MCSP obstruction family forcing the target consequence.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "source_excerpt": "A barely nontrivial lower bound for MCSP in a weak model.",
                "target_excerpt": "Major consequences such as NP not in P/poly.",
                "candidate_object": "MCSP obstruction family",
                "carrier_kind": "family of obstruction instances",
                "preserved_invariant": "witness complexity profile",
                "missing_route_lemma": "Realize the obstruction family and preserve the invariant.",
                "status": "blocked",
            }
        ],
    )
    save_proof_queue(
        queue,
        json_path=artifacts_dir / "proof-queue.json",
        md_path=artifacts_dir / "proof-queue.md",
    )

    latest = run_discovery_phase(repo_root=repo_root, artifacts_dir=artifacts_dir, kb_ref="demo", top_k=4)

    assert latest["status"] == "completed"
    assert "expert_conjectures_md" in latest["outputs"]
    assert "discovery_branch_synthesis_md" in latest["outputs"]
    assert "discovery_governor_report_md" in latest["outputs"]
    assert "lean/lake search evaluated" in latest["detail"].lower()
    refreshed = load_proof_queue(artifacts_dir / "proof-queue.json", kb_ref="demo")
    assert refreshed["metadata"]["pending_count"] >= 1
    promoted = [row for row in refreshed["entries"] if row.get("claim_type") == "expert-conjecture"]
    assert len(promoted) >= 1


def test_branch_to_theorem_pipeline_skips_stale_compilation_when_no_branch_executes(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|route-conjecture",
                "title": "Blocked route",
                "priority": 0.91,
                "bridge_id": "bridge.001",
                "claim_type": "route-conjecture",
                "conjecture_statement": "Construct an admissible witness family.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "source_excerpt": "Source excerpt.",
                "target_excerpt": "Target excerpt.",
                "candidate_object": "Witness family",
                "preserved_invariant": "witness profile",
                "missing_route_lemma": "Witness realization lemma",
                "status": "blocked",
            }
        ],
    )
    save_proof_queue(
        queue,
        json_path=artifacts_dir / "proof-queue.json",
        md_path=artifacts_dir / "proof-queue.md",
    )
    save_mathlib_index(
        default_mathlib(kb_ref="demo"),
        json_path=artifacts_dir / "mathlib.json",
        md_path=artifacts_dir / "mathlib.md",
    )
    _write_json(
        artifacts_dir / "discovery-branch-queue.json",
        {
            "metadata": {"kb_ref": "demo"},
            "branches": [
                {
                    "branch_id": "disclayer.demo.family.realization",
                    "status": "completed",
                    "target_label": "Carrier Realization Prompt",
                    "routing_priority": 2.0,
                    "linked_queue_ids": ["proofq.demo.001"],
                    "attempt_count": 1,
                    "last_execution_id": "discexec.demo.001",
                    "last_outcome_summary": "Completed one prior local pass.",
                }
            ],
        },
    )

    result = _run_branch_to_theorem_pipeline(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref="demo",
        branch_outputs=discovery_branch_queue_paths(artifacts_dir),
        top_k=4,
    )

    assert result["executed_current_round"] is False
    assert result["execution_outputs"] == []
    assert result["promotion_counts"] == {"added": 0, "updated": 0, "deferred": 0}
    assert not (artifacts_dir / "discovery-programme-promotions.json").exists()


@pytest.mark.parametrize("phase", ["discovery", "prove"])
def test_canonical_work_authorization_requires_exact_phase_identity_intersection(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    phase: str,
) -> None:
    fixture = _canonical_work_fixture(tmp_path, phase=phase)
    _install_fake_canonical_gate(monkeypatch, fixture)

    authorization = verify_work_cycle_theory_authorization(
        projection_path=fixture["projection_path"],
        state_root=fixture["state_root"],
        target_id=fixture["target_id"],
        run_id=fixture["run_id"],
        work_binding=fixture["binding"],
        phase=phase,
    )
    local = verify_exact_local_work_item(
        phase=phase,
        repo_root=tmp_path,
        artifacts_dir=tmp_path / "artifacts" / "demo",
        kb_ref="demo",
        authorization=authorization,
    )

    assert authorization["authoritative"] is True
    assert not hasattr(authorization.runtime_capability, "update")
    assert authorization["promotion_allowed"] is True
    assert authorization["work_binding"]["canonical_branch_id"] == fixture["branch_id"]
    assert local["id"] == fixture["local_id"]
    assert local["digest"] == canonical_digest(fixture["row"])


def test_work_authorization_is_frozen_and_rejects_capability_swaps(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = _canonical_work_fixture(tmp_path, phase="discovery")
    _install_fake_canonical_gate(monkeypatch, fixture)
    authorization = verify_work_cycle_theory_authorization(
        projection_path=fixture["projection_path"],
        state_root=fixture["state_root"],
        target_id=fixture["target_id"],
        run_id=fixture["run_id"],
        work_binding=fixture["binding"],
        phase="discovery",
    )
    runtime_capability = authorization.runtime_capability
    projection = dict(authorization)

    with pytest.raises(TypeError, match="issued only after canonical verification"):
        work_cycle_module.WorkCycleAuthorization(runtime_capability, projection)
    with pytest.raises(TypeError, match="immutable"):
        authorization._runtime_capability = runtime_capability  # type: ignore[misc]
    with pytest.raises(TypeError, match="immutable"):
        authorization._projection_bytes = b"{}"  # type: ignore[misc]
    with pytest.raises(ContractError, match="live reserved capability"):
        authorization.with_reservation({"status": "actions_reserved"})  # type: ignore[arg-type]

    detached_binding = authorization["work_binding"]
    detached_binding["target_id"] = "target.detached.mutation"
    assert authorization["work_binding"]["target_id"] == fixture["target_id"]

    alternate_target = theory_gate.authorization_projection(runtime_capability)
    alternate_target["target_id"] = "target.demo.other"
    alternate_target.pop("authorization_digest", None)
    alternate_target["authorization_digest"] = canonical_digest(alternate_target)
    target_capability = theory_gate._issue_verified_authorization(  # noqa: SLF001
        alternate_target,
        present_investment_verified=True,
        temporal_capability=runtime_capability._temporal_capability,  # noqa: SLF001
    )
    object.__setattr__(authorization, "_runtime_capability", target_capability)
    with pytest.raises(ContractError, match="projection target_id differs"):
        _ = authorization["target_id"]
    object.__setattr__(authorization, "_runtime_capability", runtime_capability)

    alternate_decision = theory_gate.authorization_projection(runtime_capability)
    decision = alternate_decision["present_investment_decision"]
    evaluated_at = dt.datetime.fromisoformat(decision["evaluated_at"].replace("Z", "+00:00"))
    decision["evaluated_at"] = (evaluated_at + dt.timedelta(microseconds=1)).isoformat().replace(
        "+00:00", "Z"
    )
    alternate_decision["present_investment_decision_digest"] = canonical_digest(decision)
    alternate_decision.pop("authorization_digest", None)
    alternate_decision["authorization_digest"] = canonical_digest(alternate_decision)
    decision_capability = theory_gate._issue_verified_authorization(  # noqa: SLF001
        alternate_decision,
        present_investment_verified=True,
        temporal_capability=runtime_capability._temporal_capability,  # noqa: SLF001
    )
    object.__setattr__(authorization, "_runtime_capability", decision_capability)
    with pytest.raises(
        ContractError,
        match="authorization_digest differs|present_investment_decision_digest differs",
    ):
        _ = authorization["target_id"]
    object.__setattr__(authorization, "_runtime_capability", runtime_capability)
    assert authorization["target_id"] == fixture["target_id"]


def test_work_reservation_uses_one_captured_capability_despite_between_check_swap(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = _canonical_work_fixture(tmp_path, phase="discovery")
    _install_fake_canonical_gate(monkeypatch, fixture)
    _install_fake_action_reservation(monkeypatch, fixture)
    authorization = verify_work_cycle_theory_authorization(
        projection_path=fixture["projection_path"],
        state_root=fixture["state_root"],
        target_id=fixture["target_id"],
        run_id=fixture["run_id"],
        work_binding=fixture["binding"],
        phase="discovery",
    )
    original = authorization.source_runtime_capability
    alternate_payload = theory_gate.authorization_projection(original)
    alternate_payload["target_id"] = "target.demo.alternate"
    alternate_payload.pop("authorization_digest", None)
    alternate_payload["authorization_digest"] = canonical_digest(alternate_payload)
    alternate = theory_gate._issue_verified_authorization(  # noqa: SLF001
        alternate_payload,
        present_investment_verified=True,
        temporal_capability=original._temporal_capability,  # noqa: SLF001
    )
    real_capture = work_cycle_module.WorkCycleAuthorization._capture_validated_authority
    captured_reserver = work_cycle_module.reserve_canonical_theory_actions
    captured_sources: list[object] = []
    reservation_sources: list[object] = []

    def capture_then_swap(self: object):
        capture = real_capture(self)
        if self is authorization:
            object.__setattr__(authorization, "_runtime_capability", alternate)
            captured_sources.append(capture.source_capability)
        return capture

    def reserve_captured_source(source: object, **kwargs: object):
        reservation_sources.append(source)
        return captured_reserver(source, **kwargs)

    monkeypatch.setattr(
        work_cycle_module.WorkCycleAuthorization,
        "_capture_validated_authority",
        capture_then_swap,
    )
    monkeypatch.setattr(
        work_cycle_module,
        "reserve_canonical_theory_actions",
        reserve_captured_source,
    )
    reserved = reserve_work_cycle_actions(authorization)
    assert captured_sources == [original]
    assert reservation_sources == [original]
    assert reserved["action_reservation"]["target_id"] == fixture["target_id"]
    assert reserved.source_runtime_capability is original


def test_execute_work_cycle_fails_closed_without_canonical_authority(tmp_path: Path) -> None:
    with pytest.raises(ContractError, match="requires canonical cycle"):
        execute_work_cycle(
            repo_root=tmp_path,
            artifacts_dir=tmp_path / "artifacts" / "demo",
            kb_ref="demo",
            kb_path=None,
            state=default_work_state(kb_ref="demo", max_cycles=2),
            phase_override="discovery",
            top_k=1,
        )


def test_work_authorization_rejects_forged_verified_strings(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = _canonical_work_fixture(tmp_path, phase="discovery")
    monkeypatch.setattr(
        work_cycle_module,
        "verify_canonical_theory_cycle",
        lambda *_args, **_kwargs: dict(fixture["authorization"]),
    )

    with pytest.raises(ContractError, match="live runtime verifier"):
        verify_work_cycle_theory_authorization(
            projection_path=fixture["projection_path"],
            state_root=fixture["state_root"],
            target_id=fixture["target_id"],
            run_id=fixture["run_id"],
            work_binding=fixture["binding"],
            phase="discovery",
        )


def test_work_authorization_rejects_projection_replacement_after_gate_replay(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = _canonical_work_fixture(tmp_path, phase="discovery")
    _install_fake_canonical_gate(monkeypatch, fixture)
    projection = json.loads(fixture["projection_path"].read_text(encoding="utf-8"))
    projection["identity_map"]["hypothesis_ids"] = ["hypothesis.demo.replacement"]
    _write_json(fixture["projection_path"], projection)

    with pytest.raises(ContractError, match="bytes changed after canonical verification"):
        verify_work_cycle_theory_authorization(
            projection_path=fixture["projection_path"],
            state_root=fixture["state_root"],
            target_id=fixture["target_id"],
            run_id=fixture["run_id"],
            work_binding=fixture["binding"],
            phase="discovery",
        )


def test_canonical_reservation_failure_prevents_local_dispatch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = _canonical_work_fixture(tmp_path, phase="discovery")
    _install_fake_canonical_gate(monkeypatch, fixture)
    dispatched = False

    monkeypatch.setattr(
        work_cycle_module,
        "build_plausibility_report_from_artifacts",
        lambda *_args, **_kwargs: {"plausibility_score": 0.0, "decision": {"plausible_solution_detected": False}},
    )

    def reject_reservation(_authorization: Mapping[str, object]) -> dict:
        raise ContractError("canonical state changed before action reservation")

    def forbidden_dispatch(**_kwargs: object) -> dict:
        nonlocal dispatched
        dispatched = True
        return {}

    monkeypatch.setattr(work_cycle_module, "reserve_work_cycle_actions", reject_reservation)
    monkeypatch.setattr(work_cycle_module, "run_discovery_phase", forbidden_dispatch)
    state = default_work_state(kb_ref="demo", max_cycles=2)
    with pytest.raises(ContractError, match="state changed before action reservation"):
        execute_work_cycle(
            repo_root=tmp_path,
            artifacts_dir=tmp_path / "artifacts" / "demo",
            kb_ref="demo",
            kb_path=None,
            state=state,
            phase_override="discovery",
            top_k=1,
            canonical_cycle_path=fixture["projection_path"],
            canonical_state_root=fixture["state_root"],
            canonical_target_id=fixture["target_id"],
            canonical_run_id=fixture["run_id"],
            canonical_work_binding=fixture["binding"],
        )

    assert dispatched is False
    assert state["metadata"]["cycle_count"] == 0
    local = json.loads(fixture["local_path"].read_text(encoding="utf-8"))
    assert local["branches"][0]["status"] == "active"


@pytest.mark.parametrize(
    ("phase", "expected_scope"),
    [("discovery", "outer_discovery"), ("prove", "outer_prove")],
)
def test_work_reservation_uses_consumer_scoped_canonical_gate(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    phase: str,
    expected_scope: str,
) -> None:
    fixture = _canonical_work_fixture(tmp_path, phase=phase)
    _install_fake_canonical_gate(monkeypatch, fixture)
    authorization = verify_work_cycle_theory_authorization(
        projection_path=fixture["projection_path"],
        state_root=fixture["state_root"],
        target_id=fixture["target_id"],
        run_id=fixture["run_id"],
        work_binding=fixture["binding"],
        phase=phase,
    )
    calls: list[dict[str, object]] = []

    def fake_reserve(source: Mapping[str, object], **kwargs: object):
        calls.append(dict(kwargs))
        source_projection = theory_gate.authorization_projection(source)  # type: ignore[arg-type]
        decision = source_projection["present_investment_decision"]
        temporal_evaluation = {
            "evaluated_at": decision["evaluated_at"],
            "clock_authority": decision["clock_authority"],
            "clock_authority_digest": decision["clock_authority_digest"],
            "authentication_status": "governed_local_process_time_not_externally_authenticated",
        }
        reservation = {
            "schema_version": "1.0.0",
            "reservation_id": f"reservation.demo.{phase}",
            "target_id": fixture["target_id"],
            "run_id": fixture["run_id"],
            "source_cycle_id": fixture["authorization"]["cycle_id"],
            "source_commit_id": fixture["authorization"]["commit_id"],
            "source_state_generation": 2,
            "reserved_state_generation": 3,
            "action_ids": ["action.demo.001"],
            "consumer_receipt_id": kwargs["consumer_receipt_id"],
            "status": "reserved_before_investment",
            "temporal_evaluation": temporal_evaluation,
        }
        reservation["reservation_digest"] = canonical_digest(reservation)
        schedule = {
            "schema_version": "1.0.0",
            "schedule_id": f"schedule.demo.reserved.{phase}",
            "actions": [{"action_id": "action.demo.001", "status": "consumed"}],
            "consumption_log": [],
        }
        schedule["consumed_schedule_digest"] = canonical_digest(
            schedule, exclude_keys=("consumed_schedule_digest", "created_at")
        )
        reserved_commit_id = f"commit.demo.reserved.{phase}"
        reserved_manifest_digest = canonical_digest({"manifest": phase})
        reservation_basis = {
            "schema_version": "1.0.0",
            "basis_kind": "immutable_canonical_action_reservation",
            "source_authorization_basis_digest": source_projection[
                "authorization_basis_digest"
            ],
            "reservation_digest": reservation["reservation_digest"],
            "reserved_commit_id": reserved_commit_id,
            "reserved_manifest_digest": reserved_manifest_digest,
            "reserved_state_generation": 3,
            "consumed_schedule_digest": schedule["consumed_schedule_digest"],
            "reserved_branch_ids": [fixture["branch_id"]],
            "reserved_action_ids": ["action.demo.001"],
        }
        reserved_payload = {
            **source_projection,
            "status": "actions_reserved",
            "source_commit_id": fixture["authorization"]["commit_id"],
            "source_committed_state_version": 2,
            "committed_state_version": 3,
            "commit_id": reserved_commit_id,
            "manifest_digest": reserved_manifest_digest,
            "commit_path": str((tmp_path / "canonical-state" / "commit-3").resolve()),
            "reserved_branch_ids": [fixture["branch_id"]],
            "reserved_action_ids": ["action.demo.001"],
            "reservation_consumer_scope": expected_scope,
            "proof_obligation_id": fixture["obligation_id"],
            "reservation": reservation,
            "reservation_digest": reservation["reservation_digest"],
            "schedule": schedule,
            "reservation_authorization_basis": reservation_basis,
            "reservation_authorization_basis_digest": canonical_digest(reservation_basis),
            "reservation_temporal_evaluation": temporal_evaluation,
            "reservation_temporal_evaluation_digest": canonical_digest(temporal_evaluation),
        }
        reserved_payload.pop("authorization_digest", None)
        reserved_payload["authorization_digest"] = canonical_digest(reserved_payload)
        return theory_gate._issue_verified_authorization(  # noqa: SLF001
            reserved_payload,
            present_investment_verified=True,
            temporal_capability=source._temporal_capability,  # type: ignore[attr-defined]  # noqa: SLF001
        )

    monkeypatch.setattr(work_cycle_module, "reserve_canonical_theory_actions", fake_reserve)
    reserved_authorization = reserve_work_cycle_actions(authorization)
    reservation = reserved_authorization["action_reservation"]

    assert calls == [
        {
            "branch_ids": [fixture["branch_id"]],
            "consumer_receipt_id": calls[0]["consumer_receipt_id"],
            "consumer_scope": expected_scope,
            "proof_obligation_id": fixture["obligation_id"],
        }
    ]
    assert reservation["action_ids"] == ["action.demo.001"]
    assert reservation["reserved_state_generation"] == 3
    assert reservation["reserved_commit_id"] == f"commit.demo.reserved.{phase}"
    assert reserved_authorization.reservation_verified is True
    assert reserved_authorization.runtime_capability["status"] == "actions_reserved"
    object.__setattr__(
        reserved_authorization,
        "_reserved_runtime_capability",
        authorization.source_runtime_capability,
    )
    with pytest.raises(ContractError, match="wrong status"):
        _ = reserved_authorization["target_id"]


def test_reserved_work_authorization_rejects_replay_and_expiry(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A retained CAS capability is single-use and locally time-bounded."""

    fixture = _canonical_work_fixture(tmp_path, phase="discovery")
    _install_fake_canonical_gate(monkeypatch, fixture)
    _install_fake_action_reservation(monkeypatch, fixture)
    source = verify_work_cycle_theory_authorization(
        projection_path=fixture["projection_path"],
        state_root=fixture["state_root"],
        target_id=fixture["target_id"],
        run_id=fixture["run_id"],
        work_binding=fixture["binding"],
        phase="discovery",
    )
    reserved = reserve_work_cycle_actions(source)
    reservation = reserved["action_reservation"]
    assert reservation["temporal_evaluation"]["authentication_status"] == (
        "governed_local_process_time_not_externally_authenticated"
    )
    with pytest.raises(ContractError, match="already reserved"):
        reserve_work_cycle_actions(reserved)

    consume_before = dt.datetime.fromisoformat(
        source["present_investment_decision"]["consume_before"].replace(
            "Z", "+00:00"
        )
    )
    monkeypatch.setattr(
        theory_gate,
        "_system_utc_now",
        lambda: consume_before + dt.timedelta(microseconds=1),
    )
    with pytest.raises(ContractError, match="consume-before boundary"):
        _ = reserved["target_id"]


@pytest.mark.parametrize(
    "failure",
    [
        "projection generation 1 is stale; canonical store is at 2",
        "literature basis is local-only, stale, or otherwise non-investable",
        "target identity mismatch",
    ],
)
def test_work_cycle_propagates_canonical_stale_local_only_and_wrong_target_rejections(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure: str,
) -> None:
    fixture = _canonical_work_fixture(tmp_path, phase="discovery")

    def reject_gate(*_args: object, **_kwargs: object) -> dict:
        raise ContractError(f"canonical theory gate rejected projection: {failure}")

    monkeypatch.setattr(work_cycle_module, "verify_canonical_theory_cycle", reject_gate)
    with pytest.raises(ContractError, match=failure):
        execute_work_cycle(
            repo_root=tmp_path,
            artifacts_dir=tmp_path / "artifacts" / "demo",
            kb_ref="demo",
            kb_path=None,
            state=default_work_state(kb_ref="demo", max_cycles=2),
            phase_override="discovery",
            top_k=1,
            canonical_cycle_path=fixture["projection_path"],
            canonical_state_root=fixture["state_root"],
            canonical_target_id=fixture["target_id"],
            canonical_run_id=fixture["run_id"],
            canonical_work_binding=fixture["binding"],
        )


def test_canonical_work_binding_rejects_no_exact_branch_hypothesis_intersection(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = _canonical_work_fixture(tmp_path, phase="discovery")
    _install_fake_canonical_gate(monkeypatch, fixture)
    binding = dict(fixture["binding"])
    binding["canonical_hypothesis_id"] = "hypothesis.demo.unbound"
    binding["binding_digest"] = canonical_digest(binding, exclude_keys=("binding_digest",))

    with pytest.raises(ContractError, match="branch/hypothesis intersection"):
        verify_work_cycle_theory_authorization(
            projection_path=fixture["projection_path"],
            state_root=fixture["state_root"],
            target_id=fixture["target_id"],
            run_id=fixture["run_id"],
            work_binding=binding,
            phase="discovery",
        )


def test_canonical_work_binding_rejects_wrong_phase_action(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = _canonical_work_fixture(tmp_path, phase="discovery", action_kind="prove")
    _install_fake_canonical_gate(monkeypatch, fixture)

    with pytest.raises(ContractError, match="phase-appropriate `discovery` action"):
        verify_work_cycle_theory_authorization(
            projection_path=fixture["projection_path"],
            state_root=fixture["state_root"],
            target_id=fixture["target_id"],
            run_id=fixture["run_id"],
            work_binding=fixture["binding"],
            phase="discovery",
        )


def test_canonical_prove_binding_rejects_wrong_obligation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = _canonical_work_fixture(tmp_path, phase="prove")
    _install_fake_canonical_gate(monkeypatch, fixture)
    binding = dict(fixture["binding"])
    binding["canonical_proof_obligation_id"] = "obligation.demo.wrong"
    binding["binding_digest"] = canonical_digest(binding, exclude_keys=("binding_digest",))

    with pytest.raises(ContractError, match="proof handoff does not exactly match"):
        verify_work_cycle_theory_authorization(
            projection_path=fixture["projection_path"],
            state_root=fixture["state_root"],
            target_id=fixture["target_id"],
            run_id=fixture["run_id"],
            work_binding=binding,
            phase="prove",
        )


def test_execute_work_cycle_rejects_digest_drift_in_bound_local_row(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = _canonical_work_fixture(tmp_path, phase="discovery")
    _install_fake_canonical_gate(monkeypatch, fixture)
    payload = json.loads(fixture["local_path"].read_text(encoding="utf-8"))
    payload["branches"][0]["target_label"] = "Changed after binding"
    _write_json(fixture["local_path"], payload)

    with pytest.raises(ContractError, match="changed after its binding was created"):
        execute_work_cycle(
            repo_root=tmp_path,
            artifacts_dir=tmp_path / "artifacts" / "demo",
            kb_ref="demo",
            kb_path=None,
            state=default_work_state(kb_ref="demo", max_cycles=2),
            phase_override="discovery",
            top_k=1,
            canonical_cycle_path=fixture["projection_path"],
            canonical_state_root=fixture["state_root"],
            canonical_target_id=fixture["target_id"],
            canonical_run_id=fixture["run_id"],
            canonical_work_binding=fixture["binding"],
        )


def test_local_work_binding_rejects_duplicate_and_one_sided_rows(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    duplicate_fixture = _canonical_work_fixture(tmp_path / "duplicate", phase="discovery")
    _install_fake_canonical_gate(monkeypatch, duplicate_fixture)
    duplicate_authorization = verify_work_cycle_theory_authorization(
        projection_path=duplicate_fixture["projection_path"],
        state_root=duplicate_fixture["state_root"],
        target_id=duplicate_fixture["target_id"],
        run_id=duplicate_fixture["run_id"],
        work_binding=duplicate_fixture["binding"],
        phase="discovery",
    )
    payload = json.loads(duplicate_fixture["local_path"].read_text(encoding="utf-8"))
    payload["branches"].append(dict(payload["branches"][0]))
    _write_json(duplicate_fixture["local_path"], payload)
    with pytest.raises(ContractError, match="missing or duplicated"):
        verify_exact_local_work_item(
            phase="discovery",
            repo_root=tmp_path / "duplicate",
            artifacts_dir=tmp_path / "duplicate" / "artifacts" / "demo",
            kb_ref="demo",
            authorization=duplicate_authorization,
        )

    one_sided_fixture = _canonical_work_fixture(tmp_path / "one-sided", phase="discovery")
    _install_fake_canonical_gate(monkeypatch, one_sided_fixture)
    one_sided_payload = json.loads(one_sided_fixture["local_path"].read_text(encoding="utf-8"))
    one_sided_payload["branches"][0]["canonical_hypothesis_id"] = "hypothesis.demo.different"
    _write_json(one_sided_fixture["local_path"], one_sided_payload)
    one_sided_binding = dict(one_sided_fixture["binding"])
    one_sided_binding["local_work_item_digest"] = canonical_digest(one_sided_payload["branches"][0])
    one_sided_binding["binding_digest"] = canonical_digest(
        one_sided_binding,
        exclude_keys=("binding_digest",),
    )
    one_sided_fixture["binding"] = one_sided_binding
    one_sided_authorization = verify_work_cycle_theory_authorization(
        projection_path=one_sided_fixture["projection_path"],
        state_root=one_sided_fixture["state_root"],
        target_id=one_sided_fixture["target_id"],
        run_id=one_sided_fixture["run_id"],
        work_binding=one_sided_binding,
        phase="discovery",
    )
    with pytest.raises(ContractError, match="canonical_hypothesis_id"):
        verify_exact_local_work_item(
            phase="discovery",
            repo_root=tmp_path / "one-sided",
            artifacts_dir=tmp_path / "one-sided" / "artifacts" / "demo",
            kb_ref="demo",
            authorization=one_sided_authorization,
        )


@pytest.mark.parametrize("phase", ["discovery", "prove"])
def test_execute_work_cycle_forwards_exact_selector_and_persists_lineage(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    phase: str,
) -> None:
    fixture = _canonical_work_fixture(tmp_path, phase=phase)
    _install_fake_canonical_gate(monkeypatch, fixture)
    reservation = _install_fake_action_reservation(monkeypatch, fixture)
    calls: list[dict] = []

    def no_solution(*_args: object, **_kwargs: object) -> dict:
        return {"plausibility_score": 0.0, "decision": {"plausible_solution_detected": False}}

    def fake_phase(**kwargs: object) -> dict:
        calls.append(dict(kwargs))
        return {"phase": phase, "status": "completed", "detail": "exact selector executed", "outputs": {}}

    monkeypatch.setattr(work_cycle_module, "build_plausibility_report_from_artifacts", no_solution)
    monkeypatch.setattr(work_cycle_module, "_should_run_meta", lambda **_kwargs: (False, "", ""))
    monkeypatch.setattr(
        work_cycle_module,
        "run_discovery_phase" if phase == "discovery" else "run_prove_phase",
        fake_phase,
    )
    state, latest = execute_work_cycle(
        repo_root=tmp_path,
        artifacts_dir=tmp_path / "artifacts" / "demo",
        kb_ref="demo",
        kb_path=None,
        state=default_work_state(kb_ref="demo", max_cycles=2),
        phase_override=phase,
        top_k=1,
        canonical_cycle_path=fixture["projection_path"],
        canonical_state_root=fixture["state_root"],
        canonical_target_id=fixture["target_id"],
        canonical_run_id=fixture["run_id"],
        canonical_work_binding=fixture["binding"],
    )

    assert latest["authoritative"] is True
    assert latest["promotion_allowed"] is True
    assert state["history"][-1]["canonical_binding_id"] == fixture["binding"]["binding_id"]
    assert state["metadata"]["canonical_theory_lineage"]["commit_id"] == reservation["reserved_commit_id"]
    assert latest["authority"]["reservation_id"] == reservation["reservation_id"]
    assert state["history"][-1]["canonical_reservation_id"] == reservation["reservation_id"]
    if phase == "discovery":
        assert calls[0]["exact_branch_id"] == fixture["local_id"]
        assert calls[0]["expected_branch_digest"] == fixture["binding"]["local_work_item_digest"]
        assert calls[0]["canonical_branch_id"] == fixture["branch_id"]
        assert calls[0]["canonical_hypothesis_id"] == fixture["hypothesis_id"]
    else:
        assert calls[0]["exact_queue_id"] == fixture["local_id"]
        assert calls[0]["expected_queue_digest"] == fixture["binding"]["local_work_item_digest"]


def test_authoritative_prove_selector_bypasses_unrelated_active_attempt(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    attempts_dir = artifacts_dir / "proof-attempts"
    attempts_dir.mkdir(parents=True, exist_ok=True)
    queue = default_queue(kb_ref="demo")

    def theorem_entry(*, key: str, title: str, priority: float) -> dict:
        return {
            "queue_key": key,
            "title": title,
            "priority": priority,
            "bridge_id": key.split("|")[0],
            "claim_type": "expert-conjecture",
            "claim_text": f"There exists an admissible witness family for {title}.",
            "conjecture_statement": f"There exists an admissible witness family for {title}.",
            "source_statement_id": "st.src",
            "target_statement_id": "st.tgt",
            "source_excerpt": "A precise source theorem excerpt.",
            "target_excerpt": "A precise target theorem excerpt.",
            "route_synopsis": "Transport the source result through an explicit witness family into the target theorem.",
            "candidate_object": "Explicit witness family",
            "carrier_kind": "family of admissible witness instances",
            "preserved_invariant": "witness complexity profile",
            "proof_strategy_family": "invariant transport",
            "missing_route_lemma": "Prove the explicit witness family transports the invariant.",
            "negative_route": "The witness family may fail to preserve the invariant.",
            "failure_diagnosis": "The route fails exactly when invariant transport cannot be established.",
            "proof_obligations": ["Construct and verify the witness family."],
            "candidate_lemmas": ["The source theorem induces the required witness."],
            "mathematical_layers": _math_layers(),
        }

    enqueue_entries(
        queue,
        [
            theorem_entry(key="bridge.active|st.tgt|active", title="unrelated active theorem", priority=0.99),
            theorem_entry(key="bridge.bound|st.tgt|bound", title="canonically bound theorem", priority=0.80),
        ],
    )
    unrelated = next(row for row in queue["entries"] if row["title"] == "unrelated active theorem")
    bound = next(row for row in queue["entries"] if row["title"] == "canonically bound theorem")
    unrelated["status"] = "in_progress"
    unrelated["attempt_ids"] = ["attempt.demo.001"]
    bound.update(
        {
            "canonical_target_id": "target.demo",
            "canonical_run_id": "run.demo",
            "canonical_cycle_id": "cycle.demo.002",
            "canonical_commit_id": "commit.demo.002",
            "canonical_state_version": 2,
            "canonical_branch_id": "branch.demo.canonical",
            "canonical_hypothesis_id": "hypothesis.demo.canonical",
            "canonical_proof_obligation_id": "obligation.demo.canonical",
        }
    )
    queue_json, queue_md = proof_queue_paths(repo_root, "demo")
    save_proof_queue(queue, json_path=queue_json, md_path=queue_md)
    raw_queue = json.loads(queue_json.read_text(encoding="utf-8"))
    bound_raw = next(row for row in raw_queue["entries"] if row["title"] == "canonically bound theorem")
    unrelated_raw = next(row for row in raw_queue["entries"] if row["title"] == "unrelated active theorem")
    _write_json(
        attempts_dir / "attempt.demo.001.json",
        {
            "metadata": {
                "attempt_id": "attempt.demo.001",
                "queue_id": unrelated_raw["queue_id"],
                "status": "in_progress",
            },
            "final_assessment": {"outcome": "in_progress"},
        },
    )
    save_mathlib_index(
        default_mathlib(kb_ref="demo"),
        json_path=repo_root / "InformalMathLib" / "demo" / "index.json",
        md_path=repo_root / "InformalMathLib" / "demo" / "catalog.md",
    )

    latest = run_prove_phase(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref="demo",
        kb_path=None,
        exact_queue_id=bound_raw["queue_id"],
        expected_queue_digest=canonical_digest(bound_raw),
    )
    refreshed = load_proof_queue(queue_json, kb_ref="demo")
    statuses = {row["queue_id"]: row["status"] for row in refreshed["entries"]}

    assert latest["queue_id"] == bound_raw["queue_id"]
    assert latest["attempt_id"] == "attempt.demo.002"
    assert statuses[unrelated_raw["queue_id"]] == "in_progress"
    assert statuses[bound_raw["queue_id"]] == "in_progress"


def test_legacy_compatibility_is_visibly_non_authoritative_and_disables_promotion(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[dict] = []

    monkeypatch.setattr(
        work_cycle_module,
        "build_plausibility_report_from_artifacts",
        lambda *_args, **_kwargs: {"plausibility_score": 0.0, "decision": {"plausible_solution_detected": False}},
    )
    monkeypatch.setattr(work_cycle_module, "_should_run_meta", lambda **_kwargs: (False, "", ""))

    def fake_discovery(**kwargs: object) -> dict:
        calls.append(dict(kwargs))
        return {"phase": "discovery", "status": "completed", "detail": "legacy", "outputs": {}}

    monkeypatch.setattr(work_cycle_module, "run_discovery_phase", fake_discovery)
    state, latest = execute_work_cycle(
        repo_root=tmp_path,
        artifacts_dir=tmp_path / "artifacts" / "demo",
        kb_ref="demo",
        kb_path=None,
        state=default_work_state(kb_ref="demo", max_cycles=2),
        phase_override="discovery",
        top_k=1,
        non_authoritative_legacy_compatibility=True,
    )

    assert calls[0]["promotion_allowed"] is False
    assert latest["authoritative"] is False
    assert latest["promotion_allowed"] is False
    assert latest["authority"]["mode"] == "non-authoritative-legacy-compatibility"
    assert state["history"][-1]["promotion_allowed"] is False
    markdown = render_work_state_markdown(state)
    assert "Authoritative: False" in markdown
    assert "Promotion allowed: False" in markdown


def test_legacy_compatibility_early_stop_keeps_promotion_disabled(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        work_cycle_module,
        "build_plausibility_report_from_artifacts",
        lambda *_args, **_kwargs: {
            "plausibility_score": 1.0,
            "decision": {"plausible_solution_detected": True, "detail": "already stopped"},
        },
    )
    state, latest = execute_work_cycle(
        repo_root=tmp_path,
        artifacts_dir=tmp_path / "artifacts" / "demo",
        kb_ref="demo",
        kb_path=None,
        state=default_work_state(kb_ref="demo", max_cycles=2),
        phase_override="discovery",
        top_k=1,
        non_authoritative_legacy_compatibility=True,
    )

    assert latest["status"] == "stopped"
    assert latest["authoritative"] is False
    assert latest["promotion_allowed"] is False
    assert state["latest"]["authority"]["proof_promotion_allowed"] is False


@pytest.mark.parametrize("stop_kind", ["plausible", "max_cycles"])
def test_authoritative_pre_reservation_stop_cannot_promote(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    stop_kind: str,
) -> None:
    fixture = _canonical_work_fixture(tmp_path, phase="discovery")
    _install_fake_canonical_gate(monkeypatch, fixture)

    def forbidden_reservation(_authorization: object) -> dict:
        raise AssertionError("an early hold must not consume a canonical action")

    monkeypatch.setattr(
        work_cycle_module, "reserve_work_cycle_actions", forbidden_reservation
    )
    monkeypatch.setattr(
        work_cycle_module,
        "build_plausibility_report_from_artifacts",
        lambda *_args, **_kwargs: {
            "plausibility_score": 1.0 if stop_kind == "plausible" else 0.0,
            "decision": {
                "plausible_solution_detected": stop_kind == "plausible",
                "detail": "unreserved local stop",
            },
        },
    )
    state = default_work_state(kb_ref="demo", max_cycles=2)
    if stop_kind == "max_cycles":
        state["metadata"]["cycle_count"] = 2
        monkeypatch.setattr(
            work_cycle_module,
            "_high_reward_extension_allows_continue",
            lambda **_kwargs: (False, "", {}),
        )

    state, latest = execute_work_cycle(
        repo_root=tmp_path,
        artifacts_dir=tmp_path / "artifacts" / "demo",
        kb_ref="demo",
        kb_path=None,
        state=state,
        phase_override="discovery",
        top_k=1,
        canonical_cycle_path=fixture["projection_path"],
        canonical_state_root=fixture["state_root"],
        canonical_target_id=fixture["target_id"],
        canonical_run_id=fixture["run_id"],
        canonical_work_binding=fixture["binding"],
    )

    assert latest["status"] == "stopped"
    assert latest["authority"]["canonical_theory_verified"] is True
    assert latest["authority"]["action_reserved"] is False
    assert latest["authoritative"] is False
    assert latest["promotion_allowed"] is False
    assert state["metadata"]["promotion_allowed"] is False


def test_work_cli_fails_closed_without_canonical_arguments(tmp_path: Path) -> None:
    script = ROOT / "skills" / "orchestration" / "work" / "scripts" / "run_work_cycle.py"
    completed = subprocess.run(
        [
            sys.executable,
            str(script),
            "--kb-ref",
            "demo",
            "--artifacts-dir",
            str(tmp_path / "artifacts" / "demo"),
            "--phase",
            "discovery",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode != 0
    assert "requires canonical cycle" in (completed.stdout + completed.stderr)
    assert not (tmp_path / "artifacts" / "demo" / "work-state.json").exists()

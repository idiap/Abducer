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
"""Run or resume a receipt-backed, transactionally durable marathon.

The legacy report format remains an export surface.  Executed branch operators,
semantic learning, and branch/run transitions are authoritative only through
operator receipts, the semantic reducer, and one compare-and-swap transaction
per cycle.  Wall-clock duration is a budget, never evidence of discovery.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import contextlib
from contextvars import ContextVar
import http.client
import io
import json
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import socket
from pathlib import Path
from typing import Any, Mapping


_HOST_MODEL = ContextVar("discovery_marathon_host_model", default=None)


@contextlib.contextmanager
def bind_host_model(completion, model_id: str):
    """Use a scoped host channel while retaining the source branch algorithm.

    Lunar owns credentials and provider selection. Only the wire representation
    changes: the same prompt, schema, retry policy and output validators run.
    The host RPC stream is serial, so parallel API workers are disallowed here.
    Local command-line execution remains on its existing Responses transport.
    """
    token = _HOST_MODEL.set((completion, model_id))
    try:
        yield
    finally:
        _HOST_MODEL.reset(token)


def _model_environment(api_key_config, *, require_api_key):
    if _HOST_MODEL.get() is not None:
        return {}, {"source": "host_model_channel", "active_provider": "host"}
    return environment_with_api_keys(api_key_config, require_api_key=require_api_key)

from agentic.discovery.contracts import (
    ContractError,
    Namespace,
    artifact_descriptor,
    canonical_digest,
    stable_identifier,
    validate_digest,
    validate_identifier,
)
from agentic.discovery.ledger import build_event, reduce_from_state
from agentic.discovery.learning import LearningReducer, initial_branch_state
from agentic.discovery.receipts import (
    DiscoveryOperatorDispatcher,
    OperatorBinding,
    ReceiptStore,
    ValidatorBinding,
    build_operator_request,
)
from agentic.discovery.theory_gate import (
    DEFAULT_CANONICAL_THEORY_STATE_ROOT,
    authorization_projection,
    filter_authorized_branches,
    reserve_canonical_theory_actions,
    verify_canonical_theory_cycle,
)
from agentic.state.discovery_transaction import CommitArtifact, DiscoveryTransactionStore
from agentic_common import ROOT, clean_text, fail, load_json_object, load_optional_json, rel, slugify, stable_id, utc_now, write_json
from api_key_config import environment_with_api_keys
from artifact_or_stop_control import artifact_or_stop_hint_for_branch, artifact_or_stop_preflight
from avenue_literature_gap import classify_branch_avenue, warrant_for_branch, warrant_summary
from discovery_marathon_common import (
    build_skill_dispatch_trace,
    cycle_path,
    load_branches,
    load_run_state,
    run_dir,
    write_active_run_pointers,
    write_markdown,
)
from discovery_marathon_scheduler import select_branches
from init_discovery_marathon import build_initial_state, persist_run
from physical_relevance_impact import attach_physical_relevance_impact_packet
from proof_depth_control import attach_proof_depth_control_packet
from run_branch_exploration_cycle import build_branch_output, output_markdown
from target_profiles import DEFAULT_TARGET_ID, profile_prompt_block
from validate_discovery_marathon_cycle import validate_branch_output


CODEX_BRANCH_SCHEMA = ROOT / "agentic/spec/discovery_marathon_codex_branch_output.schema.json"
PVSNP_NEGATIVE_TACTICS = ROOT / "agentic/reports/pvsnp_negative_tactics/latest.json"
RESULT_SUBGOAL_ATLAS = ROOT / "agentic/reports/result_subgoal_atlas/latest.json"
PROBLEM_SPACE_MAP = ROOT / "agentic/reports/problem_space_map/latest.json"
PVSNP_PROOF_DELIVERY_QUEUE = ROOT / "agentic/reports/pvsnp_proof_delivery_queue/latest.json"
PVSNP_INFERENCE_QUALITY = ROOT / "agentic/reports/pvsnp_inference_quality/latest.json"
PVSNP_FORMULA_FOOTPRINTS_CLOSURE = ROOT / "agentic/reports/pvsnp_formula_footprints_referee_closure/latest.json"
PVSNP_FORMULA_FOOTPRINTS_GATE = ROOT / "agentic/reports/pvsnp_formula_footprints_referee_closure/closure_gate_policy.json"
PVSNP_FORMULA_FOOTPRINTS_ACCEPTANCE = ROOT / "agentic/reports/pvsnp_formula_footprints_referee_closure/acceptance_response.json"
MARATHON_TRANSACTION_ROOT = ROOT / "agentic/state/discovery_transactions"
BRANCH_OPERATOR_ID = "legacy-marathon-branch-adapter"
BRANCH_OPERATOR_VERSION = "1.0.0"
COMPATIBILITY_CONTRACT_VERSION = "canonical-theory-compatibility/2.0.0"
YM_TARGET_ID = "yang-mills-existence-and-mass-gap-target"
PVSNP_TARGET_ID = "p-vs-np-target"
RESERVATION_TERMINAL_STATUSES = frozenset(
    {"completed", "failed", "released", "compensation_required"}
)


class BranchValidationError(Exception):
    """Raised when a candidate branch packet fails content validation."""


def validate_candidate_branch_output(candidate_output: dict[str, Any], source: Path, target_id: str | None = None) -> None:
    """Run the branch validator without leaking retry-attempt errors to stdout."""
    capture = io.StringIO()
    try:
        with contextlib.redirect_stdout(capture), contextlib.redirect_stderr(capture):
            validate_branch_output(candidate_output, source, target_id=target_id)
    except SystemExit as exc:
        detail = capture.getvalue().strip() or str(exc)
        raise BranchValidationError(detail) from exc


class BranchExecutionError(RuntimeError):
    """Operational branch execution failure that should not be counted as discovery."""

    def __init__(self, message: str, record: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.record = record or {}


def marathon_transaction_store(run_state: dict[str, Any]) -> DiscoveryTransactionStore:
    """Return the canonical CAS store for one exact marathon target/run pair."""

    return DiscoveryTransactionStore(
        MARATHON_TRANSACTION_ROOT,
        target_id=clean_text(run_state["target_id"]),
        run_id=clean_text(run_state["run_id"]),
    )


def apply_authoritative_projection(
    run_state: dict[str, Any],
    branches: list[dict[str, Any]],
    store: DiscoveryTransactionStore,
) -> None:
    """Repair scheduler-facing projections from the verified transaction state."""

    state = store.read_state()
    if state is None:
        return
    run_state["authoritative_state_generation"] = state["generation"]
    run_state["status"] = state.get("run_status", run_state.get("status", "paused"))
    run_state["cycle_count"] = max(
        int(run_state.get("cycle_count", 0)), len(state.get("cycle_history", []))
    )
    terminal = {"quarantined", "exhausted", "completed", "refuted"}
    for branch in branches:
        authoritative = state.get("branches", {}).get(branch["branch_id"])
        if not isinstance(authoritative, dict):
            continue
        branch["authoritative_status"] = authoritative.get("status")
        branch["authoritative_branch_generation"] = authoritative.get("generation")
        branch["status"] = (
            "stopped" if authoritative.get("status") in terminal else "active"
        )
        branch["consecutive_low_learning_cycles"] = authoritative.get(
            "plateau_count", branch.get("consecutive_low_learning_cycles", 0)
        )


def _validate_receipted_branch_artifact(
    request: dict[str, Any], artifacts: list[dict[str, Any]], workspace: Path
) -> bool:
    """Independently revalidate the persisted branch envelope named by a receipt."""

    if len(artifacts) != 1:
        return False
    envelope = json.loads((workspace / artifacts[0]["path"]).read_text(encoding="utf-8"))
    output = envelope.get("branch_output")
    if not isinstance(output, dict):
        return False
    if output.get("branch_id") != request["identity"]["branch_id"]:
        return False
    try:
        validate_candidate_branch_output(
            output,
            workspace / artifacts[0]["path"],
            target_id=request["identity"]["target_id"],
        )
    except BranchValidationError:
        return False
    record = envelope.get("execution_record")
    return isinstance(record, dict) and record.get("status") == "complete"


def execute_branch_with_receipt(
    branch: dict[str, Any],
    *,
    cycle_id: str,
    cycle_index: int,
    branch_budget_seconds: int,
    execution_mode: str,
    branch_engine: str,
    api_key_config: str | None,
    namespace: Namespace,
    invocation_id: str,
) -> tuple[dict[str, Any] | None, dict[str, Any], dict[str, Any]]:
    """Execute one branch as a real operator and always return its receipt.

    The closure invokes the existing API/Codex/smoke implementation, persists
    its exact output, and is then independently revalidated by the dispatcher.
    Any exception is converted into a failed operator receipt; it is not a
    falsifier and does not cancel sibling branches.
    """

    output_path = (
        run_dir(namespace.run_id)
        / "operator_outputs"
        / cycle_id
        / namespace.branch_id
        / f"{invocation_id}.json"
    )
    declared_output = rel(output_path)
    source_path = ROOT / branch["local_memory_path"]
    holder: dict[str, Any] = {}

    def operator(_request: dict[str, Any], _workspace: Path) -> dict[str, Any]:
        try:
            if execution_mode == "research" and branch_engine in {"auto", "api"}:
                output, record = build_api_branch_output(
                    branch, cycle_index, branch_budget_seconds, api_key_config
                )
            elif execution_mode == "research" and branch_engine == "codex":
                output, record = build_codex_branch_output(
                    branch, cycle_index, branch_budget_seconds, api_key_config
                )
            elif execution_mode == "smoke":
                output = attach_proof_depth_control_packet(
                    attach_physical_relevance_impact_packet(
                        attach_negative_tactic_decision(build_branch_output(branch, cycle_index), branch),
                        branch,
                        cycle_index,
                    ),
                    branch,
                    cycle_index,
                )
                output["generated_by"] = "internal_smoke_generator"
                record = {
                    "branch_id": branch["branch_id"],
                    "engine": "internal_smoke_generator",
                    "elapsed_seconds": 0,
                    "status": "complete",
                    "reason": "Explicit smoke mode; receipt is operational, not research authority.",
                }
            else:
                raise BranchExecutionError(
                    "research mode cannot use the internal generator",
                    {"branch_id": branch["branch_id"], "status": "failed"},
                )
        except BranchExecutionError as exc:
            holder["record"] = {
                "branch_id": branch["branch_id"],
                "status": "failed",
                "reason": str(exc),
                **dict(exc.record),
            }
            raise
        except SystemExit as exc:
            # Legacy helpers use SystemExit for validation/configuration errors.
            # Inside a branch worker that is an operational branch failure, not
            # permission to terminate sibling workers or the parent run.
            holder["record"] = {
                "branch_id": branch["branch_id"],
                "status": "failed",
                "reason": f"legacy branch helper exited with status {exc.code}",
            }
            raise BranchExecutionError(holder["record"]["reason"], holder["record"]) from exc
        holder["output"] = output
        holder["record"] = record
        write_json(
            output_path,
            {"branch_output": output, "execution_record": record},
        )
        return {
            "artifacts": [{"path": declared_output}],
            "explicit_unknowns": (
                ["Smoke generation cannot establish research or truth status."]
                if execution_mode == "smoke"
                else ["Validated branch structure does not establish truth."]
            ),
        }

    request = build_operator_request(
        operator_id=BRANCH_OPERATOR_ID,
        operator_version=BRANCH_OPERATOR_VERSION,
        kind="theory",
        namespace=namespace,
        invocation_id=invocation_id,
        input_artifacts=[artifact_descriptor(source_path, ROOT, namespace)],
        declared_outputs=[declared_output],
        parameters={
            "cycle_id": cycle_id,
            "cycle_index": cycle_index,
            "execution_mode": execution_mode,
            "branch_engine": branch_engine,
            "branch_budget_seconds": branch_budget_seconds,
        },
        required=True,
    )
    dispatcher = DiscoveryOperatorDispatcher(
        [
            OperatorBinding(
                BRANCH_OPERATOR_ID,
                BRANCH_OPERATOR_VERSION,
                "theory",
                function=operator,
                validators=(
                    ValidatorBinding(
                        "legacy-marathon-branch-output-validator",
                        "1.0.0",
                        function=_validate_receipted_branch_artifact,
                    ),
                ),
            )
        ],
        workspace=ROOT,
        receipt_store=ReceiptStore(run_dir(namespace.run_id) / "operator_receipts"),
    )
    receipt = dispatcher.dispatch(request)
    record = dict(holder.get("record", {}))
    record.setdefault("branch_id", branch["branch_id"])
    record.setdefault("status", "complete" if receipt["status"] == "succeeded" else "failed")
    record["operator_receipt_id"] = receipt["receipt_id"]
    record["operator_receipt_status"] = receipt["status"]
    if receipt["status"] != "succeeded":
        record.setdefault("reason", receipt.get("error", {}).get("message", "operator failed"))
        return None, record, receipt
    return dict(holder["output"]), record, receipt


def cycle_markdown(cycle: dict[str, Any]) -> str:
    text = f"# {cycle['cycle_id']}\n\n{cycle['cycle_learning']}\n\n## Selected Branches\n\n"
    text += "".join(f"- `{branch_id}`\n" for branch_id in cycle["selected_branch_ids"])
    text += "\n## Branch Outputs\n\n"
    for output in cycle["branch_outputs"]:
        text += output_markdown(output) + "\n"
    return text


def int_env(env: dict[str, str], *keys: str, default: int, minimum: int) -> int:
    for key in keys:
        raw = clean_text(env.get(key))
        if not raw:
            continue
        try:
            return max(minimum, int(raw))
        except ValueError:
            fail(f"{key} must be an integer, got `{raw}`")
    return max(minimum, default)


def float_env(env: dict[str, str], *keys: str, default: float, minimum: float) -> float:
    for key in keys:
        raw = clean_text(env.get(key))
        if not raw:
            continue
        try:
            return max(minimum, float(raw))
        except ValueError:
            fail(f"{key} must be a number, got `{raw}`")
    return max(minimum, default)


def branch_prompt(branch: dict[str, Any], cycle_index: int, branch_budget_seconds: int, *, compact: bool = False) -> str:
    recent_memory = branch.get("local_memory", [])[-6:]
    negative_tactic = negative_tactic_guidance_for_branch(branch)
    atlas_guidance = result_atlas_guidance_for_branch(branch)
    proof_delivery_guidance = proof_delivery_guidance_for_branch(branch)
    inference_quality_guidance = inference_quality_guidance_for_branch(branch)
    formula_footprints_closure_guidance = formula_footprints_closure_guidance_for_branch(branch)
    literature_gap_guidance = literature_gap_guidance_for_branch(branch)
    artifact_or_stop_guidance = artifact_or_stop_guidance_for_branch(branch)
    tactic_block = ""
    if negative_tactic:
        tactic_block = (
            "\nP vs NP negative-tactic guidance for this branch:\n"
            f"{json.dumps(negative_tactic, indent=2, sort_keys=True, ensure_ascii=False)}\n\n"
            "If this target is P vs NP, include a `negative_tactic_decision` object in the branch JSON. "
            "Use the guidance unless the branch derivation gives a sharper route-specific reason; either way, "
            "state tactic_mode, route_family, exact negation or method class, conflict target, escape conditions, "
            "proof obligations, branch-control decision, validation handoff, and paper contribution potential. "
            "Do not use generic barrier labels or global assume-P=NP rhetoric.\n\n"
        )
    atlas_block = ""
    if atlas_guidance:
        atlas_block = (
            "\nCumulative result/subgoal atlas guidance for this branch:\n"
            f"{json.dumps(atlas_guidance, indent=2, sort_keys=True, ensure_ascii=False)}\n\n"
            "Use this as durable memory. Do not rediscover archived results; either close an open obligation, "
            "upgrade validation state, attach a derivation, or explicitly backtrack/quarantine if the branch cannot improve the subgoal map.\n\n"
        )
    proof_delivery_block = ""
    if proof_delivery_guidance:
        proof_delivery_block = (
            "\nHighest-priority proof-delivery queue for this P vs NP run:\n"
            f"{json.dumps(proof_delivery_guidance, indent=2, sort_keys=True, ensure_ascii=False)}\n\n"
            "This proof-delivery queue outranks broad exploration. In this cycle, either attempt the top theorem packet directly "
            "or support one of its named sublemmas. Produce theorem-shaped content: definitions, quantifiers, lemma chain, proof attempt, "
            "countermodel or blocked-lemma disposition, and inference-quality handoff. Do not return a generic next exploration unless "
            "the top proof item is blocked at a named lemma with a precise repair or demotion criterion.\n\n"
        )
    inference_quality_block = ""
    if inference_quality_guidance:
        inference_quality_block = (
            "\nMandatory P vs NP live inference-quality focus for this branch:\n"
            f"{json.dumps(inference_quality_guidance, indent=2, sort_keys=True, ensure_ascii=False)}\n\n"
            "The next marathon is focused on producing a live inference-quality packet, not merely mentioning review. "
            "Your branch packet must therefore make the theorem-shaped inference auditable: source statement, target statement, "
            "proof/circuit model, reduction or simulation type, length/exponent regime, uniformity/advice status, barrier trigger, "
            "derivation status, blocked named lemma if incomplete, and reviewer handoff must all be explicit in the normal branch fields. "
            "The runner will synthesize and validate the live packet from those fields after your output validates. "
            "Do not return only a next-analysis narrative.\n\n"
        )
    formula_footprints_closure_block = ""
    if formula_footprints_closure_guidance:
        formula_footprints_closure_block = (
            "\nFormula Footprints referee-closure gate for this new cycle:\n"
            f"{json.dumps(formula_footprints_closure_guidance, indent=2, sort_keys=True, ensure_ascii=False)}\n\n"
            "This closure packet outranks broad Formula Footprints exploration. If this branch touches formula footprints, "
            "row forcing, quotient distance, SAT parity carriers, proof-system instantiation, or randomized certificates, "
            "it must explicitly close, invalidate, quarantine, or demote one of the listed objection-gate items. "
            "Every promoted claim must expose the required result-card fields: external_anchor, nonvacuity_witness, "
            "sharpness_status, demotion_boundary, paper_claim_status, and closed_objection_ids. "
            "Do not promote row-forcing, quotient-distance, SAT magnification, named proof-system, or randomized claims "
            "past the final claim states unless the branch supplies a genuinely new proof of the missing upgrade theorem.\n\n"
        )
    literature_gap_block = ""
    if literature_gap_guidance:
        literature_gap_block = (
            "\nMandatory avenue literature-gap preinvestment gate:\n"
            f"{json.dumps(literature_gap_guidance, indent=2, sort_keys=True, ensure_ascii=False)}\n\n"
            "Treat this as the gate for what kind of work is allowed in this branch. "
            "If the warrant says `artifact_sprint_only`, produce the named artifact, finite calculation, proof packet, or falsifier instead of broad exploration. "
            "If it says `reframe_gap_before_investment`, first sharpen the literature gap, novelty boundary, and efficient-representation requirements. "
            "If it says `quarantine_low_relevance` or `do_not_invest_prior_art_collision`, do not promote the avenue; return a demotion, stop, or precise reframe. "
            "Only use ordinary `branch_exploration` when the warrant explicitly allows it.\n\n"
        )
    artifact_or_stop_block = ""
    if artifact_or_stop_guidance:
        artifact_or_stop_block = (
            "\nMandatory Yang-Mills artifact-or-stop gate:\n"
            f"{json.dumps(artifact_or_stop_guidance, indent=2, sort_keys=True, ensure_ascii=False)}\n\n"
            "This gate outranks broad proof search for this branch. If the endpoint source table/T_tail blocker has repeated, "
            "the next packet must be one of: artifact_sprint with the endpoint source table contract or table, falsifier_sprint "
            "with a finite negative interval, publication_demotion with the demotion packet, or quarantine. "
            "Do not return another broad API reasoning packet that merely asks to compute the same endpoint intervals later.\n\n"
        )
    proof_depth_block = (
        "\nMandatory proof-depth control for this cycle:\n"
        "- Name the conceptual pressure being attacked, not just the local lemma being written.\n"
        "- Name one hard gate and explain how success or failure changes the proof state.\n"
        "- State the conceptual value signal: why this result is sharp, novel at its scope, explanatory, unifying, or route-changing.\n"
        "- If you claim novelty or ask for promotion/proof delivery, include a prior-art delta in `dependency_updates`: name what standard OS/Wilson/constructive-QFT or target-local move this differs from.\n"
        "- If the result is transfer-shaped, keep source and target objects independently meaningful and do not define the target property as the bridge image.\n"
        "- Include a stress case, failure case, or falsifier that would demote the proposed move.\n"
        "- The runner will attach a deterministic `proof_depth_control` packet after output validation; your normal branch fields must contain enough evidence for that packet.\n\n"
    )
    conceptual_revision_block = (
        "\nMandatory conceptual-abstraction revision for this cycle:\n"
        "- State the declarative tension: the theorem-level commitments that must jointly hold and the exact incompatibility, missing mediator, or representation failure currently blocking them.\n"
        "- Revisit the current mathematical concept or carrier critically: say whether it is too weak, too strong, circular, fragmented, representation-limited, or merely convenient.\n"
        "- Compare at least one available abstraction or local skill route against the current one before proposing a new abstraction.\n"
        "- State the requirements for an efficient representation: objects encoded, invariants preserved, primitive operations, equivalence policy, locality/complexity budget, transfer interface, and falsifiers.\n"
        "- If the branch is a Yang-Mills nontriviality or same-theory witness branch, make the next experiment validator-facing: include a marker phrase such as `same-theory nontriviality witness`, `connected cumulant witness`, `non-Gaussian Schwinger family`, or `spectral measure witness`.\n"
        "- If the branch is a Yang-Mills observable-density or excitation-sector branch, make the next experiment validator-facing: include a marker phrase such as `gauge-invariant observable density`, `excitation-sector cyclicity`, `OS Hilbert observable algebra`, or `vacuum-orthogonal spectral witness`.\n"
        "- Route the next step explicitly to proof search, abstraction refit, forge-new, literature import, or quarantine; do not leave the branch at a high-level aspiration.\n\n"
    )
    failed_hypothesis_anticipation_block = (
        "\nMandatory failed-hypothesis anticipation for this cycle:\n"
        "- Before proposing the next experiment, state one declarative failure signature that could have predicted this branch's failure or low value: missing_carrier, proxy_shift, finite_to_global_gap, uniformity_gap, definitional_transfer, artifact_debt, no_falsifier, low_publication_reward, literature_collision, or noncommuting_limits.\n"
        "- Add a falsifier or control-decision clause that says what happens if that signature is confirmed: artifact_sprint, falsifier_sprint, reframe, demote, quarantine, pivot, or stop.\n"
        "- If this branch repeats a known blocker, explain why the problem was genuinely hard, why the current representation failed, and why the warning sign was not visible earlier; otherwise do not spend the next experiment on broad proof search.\n"
        "- Keep this analysis object-level: name the source object, target object, carrier/bridge, hidden assumption, missing artifact, and earliest decisive test.\n\n"
    )
    visual_conceptualization_block = (
        "\nMandatory deep-reflection visual conceptualization:\n"
        "- If the theorem mechanism, obstruction, or current concept is opaque, give one property-preserving visual metaphor before the next experiment.\n"
        "- Name the main concepts and the key properties the image must preserve: invariant, symmetry, locality/globality, order/monotonicity, positivity/sign, limiting behavior, physical carrier when applicable, and proof obligation.\n"
        "- State the distortion ledger: what the image hides, what it makes too easy, and which proxy shift, finite-to-global gap, noncommuting limit, or definitional transfer it might encourage.\n"
        "- Say whether the analogy is explanation_only, hypothesis_seed, requires_preservation_audit, or quarantine.\n"
        "- The analogy may influence the next experiment only if it yields one concrete artifact, falsifier, route mutation, counterfactual variant, or representation requirement; otherwise keep it as explanation-only.\n\n"
    )
    physical_relevance_block = ""
    if clean_text(branch.get("target_id")) == "yang-mills-existence-and-mass-gap-target":
        physical_relevance_block = (
            "\nMandatory Yang-Mills physical relevance and general-impact gate:\n"
            "- State whether the local mathematics is physically load-bearing, support-only pending physical handoff, or an incremental-math drift risk.\n"
            "- Name the `physical carrier`: a gauge-invariant Wilson observable, Schwinger family, OS Hilbert observable/excitation sector, Hamiltonian/spectral object, or connected-cumulant nontriviality witness.\n"
            "- Name the Clay-gate obligation touched: same-theory continuum construction, OS/Wightman reconstruction, gauge-invariant observable density, nontriviality, or positive spectral mass gap.\n"
            "- State the `general impact`: what a mathematical physicist or constructive-QFT reader would understand differently if the branch succeeds or fails.\n"
            "- State the `unification power`: which formerly separate constraints, carriers, estimates, or routes are compressed by one mechanism/representation, and what new hypothesis or proof obligation this exposes.\n"
            "- State the `major publication gate`: invest only if the pathway has high physics conceptual reward, unification power, and plausible major-publication potential; otherwise demote, reframe, pivot, stop, or quarantine it.\n"
            "- Do not ask for another proof cycle for a merely incremental finite lemma, local estimate, endpoint calculation, symbolic identity, or support-only theorem unless it is the named artifact sprint that could unlock a major physics claim.\n"
            "- If the result is a finite lemma, algebraic identity, Schur complement, endpoint calculation, or local bound, explicitly say why it is not yet a physics claim unless a transfer condition is supplied.\n"
            "- Include a physical-relevance pass/fail test in the next experiment or falsifiers; it must promote, demote, pivot, or quarantine the branch.\n\n"
        )
    elicitation_block = (
        "\nDefinition/assumption elicitation protocol for timeline readability:\n"
        "- Every candidate lemma must define the source object, target object, and the bridge/carrier or observable being manipulated.\n"
        "- Every assumption must state the model, regime, uniformity/advice/cutoff/naturalness/same-theory condition that makes the derivation valid.\n"
        "- For every candidate lemma, not only the first one, write at least one assumption with an explicit validator-visible marker such as `Model:`, `Regime:`, `Uniformity:`, `Cutoff:`, `Same-theory:`, `Validity:`, `Local:`, or `Constraint:`.\n"
        "- If an equation introduces a symbol or inequality, its `valid_when` must name the definitions and assumptions under which it holds.\n"
        "- If a step is only a sketch, finite witness, restricted-model claim, or branch-control diagnosis, state the non-claim boundary in `why_not_yet_a_proof` or the lemma failure test.\n"
        "- Use `timeline-definition-assumption-elicitor` as the reporting skill that will surface missing definitions, assumptions, validity regimes, and non-claims in the timeline.\n\n"
    )
    compact_instruction = (
        "Write a compact but still substantive packet: use exactly one candidate lemma, 3-4 derivation steps, 2-3 equations, "
        "and 3-4 falsifiers. Keep each string under 360 characters. Do not pad prose; spend tokens on definitions, assumptions, "
        "equations, falsifiers, and the blocking gap.\n\n"
        if compact
        else ""
    )
    return (
        profile_prompt_block(branch.get("target_id"))
        + f"{compact_instruction}"
        + f"Cycle index: {cycle_index}\n"
        + f"Branch budget seconds: {branch_budget_seconds}\n"
        + f"Branch JSON:\n{json.dumps(branch, indent=2, sort_keys=True, ensure_ascii=False)}\n\n"
        + tactic_block
        + atlas_block
        + proof_delivery_block
        + inference_quality_block
        + formula_footprints_closure_block
        + literature_gap_block
        + artifact_or_stop_block
        + proof_depth_block
        + conceptual_revision_block
        + failed_hypothesis_anticipation_block
        + visual_conceptualization_block
        + physical_relevance_block
        + elicitation_block
        + f"Recent branch memory:\n{json.dumps(recent_memory, indent=2, sort_keys=True, ensure_ascii=False)}\n"
    )


def result_atlas_guidance_for_branch(branch: dict[str, Any]) -> dict[str, Any]:
    target_id = clean_text(branch.get("target_id"))
    atlas = load_optional_json(RESULT_SUBGOAL_ATLAS)
    problem_map = load_optional_json(PROBLEM_SPACE_MAP)
    if clean_text(atlas.get("target_id")) != target_id:
        return {}
    branch_text = clean_text(branch).lower()
    matching_results = []
    open_obligations: list[str] = []
    for row in atlas.get("results", []) if isinstance(atlas.get("results"), list) else []:
        coords = row.get("problem_space_coordinates", {})
        branch_title = clean_text(coords.get("branch_title")).lower()
        family = clean_text(coords.get("route_family")).lower()
        if (branch_title and branch_title in branch_text) or (family and any(token in branch_text for token in family.split("_"))):
            matching_results.append(
                {
                    "result_id": row.get("result_id", ""),
                    "status": row.get("achievement_status", ""),
                    "kind": row.get("result_kind", ""),
                    "claim": row.get("claim", ""),
                    "open_obligations": row.get("open_obligations", [])[:3],
                }
            )
            open_obligations.extend(row.get("open_obligations", [])[:3])
    relevant_nodes = []
    if clean_text(problem_map.get("target_id")) == target_id:
        for node in problem_map.get("nodes", []) if isinstance(problem_map.get("nodes"), list) else []:
            family = clean_text(node.get("route_family")).lower()
            if family and any(token in branch_text for token in family.split("_")):
                relevant_nodes.append(
                    {
                        "route_family": node.get("route_family", ""),
                        "status": node.get("status", ""),
                        "next_achievement": node.get("next_achievement", ""),
                    }
                )
    return {
        "atlas_path": rel(RESULT_SUBGOAL_ATLAS),
        "problem_map_path": rel(PROBLEM_SPACE_MAP),
        "matching_results": matching_results[:5],
        "relevant_problem_nodes": relevant_nodes[:3],
        "open_obligations_to_prefer": [item for item in dict.fromkeys(open_obligations) if clean_text(item)][:6],
        "no_repeat_rule": "If the branch repeats an archived claim, it must improve validation, derivation linkage, obligation closure, or problem-map status.",
    }


def proof_delivery_guidance_for_branch(branch: dict[str, Any]) -> dict[str, Any]:
    """Return theorem-shaped proof priorities that must control P vs NP API cycles."""
    if clean_text(branch.get("target_id")) != "p-vs-np-target":
        return {}
    queue = load_optional_json(PVSNP_PROOF_DELIVERY_QUEUE)
    if clean_text(queue.get("target_id")) != "p-vs-np-target":
        return {}
    items = [item for item in queue.get("items", []) if isinstance(item, dict)]
    if not items:
        return {}
    top = items[0]
    supporting = items[1:4]
    return {
        "queue_path": rel(PVSNP_PROOF_DELIVERY_QUEUE),
        "policy": queue.get("queue_policy", {}),
        "top_item": {
            "queue_id": top.get("queue_id", ""),
            "title": top.get("title", ""),
            "next_analysis": top.get("next_analysis", ""),
            "theorem_goal": top.get("theorem_goal", ""),
            "source_object": top.get("source_object", ""),
            "target_object": top.get("target_object", ""),
            "proof_outputs": top.get("proof_outputs", []),
            "validation_steps": top.get("validation_steps", []),
            "success_criteria": top.get("success_criteria", []),
            "demotion_criteria": top.get("demotion_criteria", []),
            "required_skills": top.get("required_skills", []),
            "paper_handoff": top.get("paper_handoff", ""),
        },
        "supporting_subgoals": [
            {
                "queue_id": item.get("queue_id", ""),
                "title": item.get("title", ""),
                "theorem_goal": item.get("theorem_goal", ""),
                "next_analysis": item.get("next_analysis", ""),
                "success_criteria": item.get("success_criteria", []),
                "demotion_criteria": item.get("demotion_criteria", []),
            }
            for item in supporting
        ],
        "cycle_instruction": (
            "The next branch packet should discharge the top item or one supporting subgoal with proof-delivery structure; "
            "broad route discovery is a fallback only after a named proof gap or countermodel disposition."
        ),
    }


def inference_quality_guidance_for_branch(branch: dict[str, Any]) -> dict[str, Any]:
    """Return the live-packet obligation that controls the next P vs NP marathon."""
    if clean_text(branch.get("target_id")) != "p-vs-np-target":
        return {}
    report = load_optional_json(PVSNP_INFERENCE_QUALITY)
    summary = report.get("summary", {}) if isinstance(report.get("summary"), dict) else {}
    live_count = int(summary.get("live_packet_count", 0) or 0)
    obligation = report.get("current_packet_obligation", {}) if isinstance(report.get("current_packet_obligation"), dict) else {}
    return {
        "report_path": rel(PVSNP_INFERENCE_QUALITY),
        "current_live_packet_count": live_count,
        "focus_mode": "emit_first_live_packet" if live_count == 0 else "keep_live_packet_current",
        "required_packet": obligation.get(
            "required_packet",
            "The next theorem-shaped, transfer-shaped, or barrier-shaped claim must emit a pvsnp_inference_quality packet before promotion.",
        ),
        "minimum_fields": obligation.get(
            "minimum_fields",
            [
                "source_statement and target_statement",
                "model_context",
                "quantifier_context",
                "derivation_status",
                "reviewer_findings",
            ],
        ),
        "reviewer_stack": obligation.get(
            "reviewer_stack",
            [
                "pvsnp-inference-quality-controller",
                "pvsnp-reduction-consistency-reviewer",
                "pvsnp-quantifier-uniformity-reviewer",
                "pvsnp-barrier-specificity-reviewer",
                "pvsnp-proof-derivation-builder",
            ],
        ),
        "next_run_exit_condition": (
            "At least one cycle must contain a valid live pvsnp_inference_quality packet for the theorem-shaped branch result, "
            "or the branch must be explicitly blocked at a named lemma with repair and demotion criteria."
        ),
    }


def formula_footprints_closure_guidance_for_branch(branch: dict[str, Any]) -> dict[str, Any]:
    """Return the referee-objection closure gate for the current Formula Footprints cycle."""
    if clean_text(branch.get("target_id")) != "p-vs-np-target":
        return {}
    closure = load_optional_json(PVSNP_FORMULA_FOOTPRINTS_CLOSURE)
    gate = load_optional_json(PVSNP_FORMULA_FOOTPRINTS_GATE)
    acceptance = load_optional_json(PVSNP_FORMULA_FOOTPRINTS_ACCEPTANCE)
    if clean_text(closure.get("status")) != "implemented":
        return {}
    return {
        "closure_path": rel(PVSNP_FORMULA_FOOTPRINTS_CLOSURE),
        "gate_path": rel(PVSNP_FORMULA_FOOTPRINTS_GATE),
        "acceptance_response_path": rel(PVSNP_FORMULA_FOOTPRINTS_ACCEPTANCE),
        "implemented_todos": closure.get("implemented_todos", []),
        "final_claim_state": closure.get("final_claim_state", {}),
        "remaining_upgrade_routes": closure.get("remaining_upgrade_routes", []),
        "required_result_card_fields": gate.get(
            "required_result_card_fields",
            [
                "external_anchor",
                "nonvacuity_witness",
                "sharpness_status",
                "demotion_boundary",
                "paper_claim_status",
                "closed_objection_ids",
            ],
        ),
        "default_demotions": gate.get("default_demotions", {}),
        "overall_acceptance_decision": acceptance.get("overall_decision", ""),
        "remaining_blockers": acceptance.get("remaining_blockers", []),
        "cycle_instruction": (
            "Treat the next API marathon as a closure/upgrading cycle: either prove one missing upgrade theorem, "
            "or produce branch output that preserves the demotions and closes a named objection gate."
        ),
    }


def literature_gap_guidance_for_branch(branch: dict[str, Any]) -> dict[str, Any]:
    """Return the target-scoped literature-gap warrant that gates broad avenue investment."""
    avenue_id = classify_branch_avenue(branch)
    summary = warrant_summary(warrant_for_branch(branch))
    return {
        "avenue_id": avenue_id,
        "warrant": summary,
        "policy": (
            "A new or continuing avenue must have a validated literature-gap warrant before broad exploration. "
            "Major cycles should invest only when the warrant has precise closest-known-result accounting, a novelty boundary, "
            "field impact, unification power, route-decision power, and major-publication reward."
        ),
        "validator": "agentic/scripts/validate_avenue_literature_gap_warrant.py",
        "skill": "literature-gap-relevance-auditor",
    }


def artifact_or_stop_guidance_for_branch(branch: dict[str, Any]) -> dict[str, Any]:
    """Return the YM artifact-or-stop mode switch for repeated named artifact debt."""
    hint = artifact_or_stop_hint_for_branch(branch)
    if not hint:
        return {}
    return {
        **hint,
        "policy": (
            "After the same named artifact debt repeats at least three times, broad_api_reasoning is forbidden for that branch. "
            "The branch must produce the artifact, produce a finite falsifier, publish/demote the support-only result, or quarantine."
        ),
        "validator": "agentic/scripts/validate_artifact_or_stop_control.py",
        "skill": "abducer-obligation-gatekeeper",
    }


def negative_tactic_guidance_for_branch(branch: dict[str, Any]) -> dict[str, Any]:
    """Return packet guidance for a P vs NP branch, with a route-family fallback."""
    if clean_text(branch.get("target_id")) != "p-vs-np-target":
        return {}
    packet = load_optional_json(PVSNP_NEGATIVE_TACTICS)
    branch_id = clean_text(branch.get("branch_id"))
    for row in packet.get("recommendations", []) if isinstance(packet.get("recommendations"), list) else []:
        if isinstance(row, dict) and clean_text(row.get("branch_id")) == branch_id:
            return row
    family = pvsnp_family_from_text(clean_text(branch))
    if family == "unclassified_pvsnp_pressure":
        return {
            "route_family": family,
            "tactic_mode": "constructive_bridge",
            "reason_for_tactic": "The branch must first type its source object, target class, transfer interface, and barrier status.",
            "exact_negation_or_method_class": "untyped P vs NP branch requiring pressure localization",
            "contradiction_carrier_or_no_go_family": "none yet; construct a local carrier before contradiction rhetoric",
            "conflict_target": "no accepted conflict target yet",
            "escape_conditions": [
                "classify the route family",
                "name the source object and target class",
            ],
            "proof_obligations": [
                "run conceptual pressure localization",
                "state a computable parameter or finite falsifier",
            ],
            "branch_control_decision": "persist_adapt",
            "next_validation_handoff": "pvsnp-conceptual-pressure-localizer then pvsnp-negative-tactic-selector",
            "paper_contribution_potential": "Not paper-ready until a scoped theorem, finite falsifier, or exact transfer calculation is named.",
        }
    return {
        "route_family": family,
        "tactic_mode": "impossibility_theorem" if family in {"hardness_magnification_threshold", "barrier_and_impossibility_control"} else "proof_by_contradiction",
        "reason_for_tactic": "The route family has enough P vs NP structure to require a scoped negative tactic before further exploration.",
        "exact_negation_or_method_class": f"method class for {family} with source object, target class, reduction interface, and advice status kept fixed",
        "contradiction_carrier_or_no_go_family": "branch-local transfer inequality, barrier premise, or falsifier carrier",
        "conflict_target": "target-preserving P vs NP transfer theorem or accepted barrier premise",
        "escape_conditions": [
            "nonblackbox or subpolynomial interface not covered by the method class",
            "advice-free and target-preserving variant with explicit validation handoff",
        ],
        "proof_obligations": [
            "compute route parameters such as beta, q, padding exponent, constructivity, largeness, or verifier overhead",
            "record relativization, natural-proofs, algebrization, nonuniformity, and advice status",
        ],
        "branch_control_decision": "persist_adapt",
        "next_validation_handoff": "pvsnp-symbolic-complexity-auditor then contradiction-route-auditor",
        "paper_contribution_potential": "Potential if the branch produces a scoped theorem, finite falsifier, or exact transfer calculation with escape conditions.",
    }


def attach_negative_tactic_decision(output: dict[str, Any], branch: dict[str, Any]) -> dict[str, Any]:
    """Ensure new P vs NP outputs carry the selector packet expected by validators."""
    guidance = negative_tactic_guidance_for_branch(branch)
    if not guidance:
        return output
    existing = output.get("negative_tactic_decision")
    if isinstance(existing, dict) and all(clean_text(existing.get(field)) for field in [
        "tactic_mode",
        "route_family",
        "reason_for_tactic",
        "exact_negation_or_method_class",
        "contradiction_carrier_or_no_go_family",
        "conflict_target",
        "branch_control_decision",
        "next_validation_handoff",
        "paper_contribution_potential",
    ]):
        for field in ["escape_conditions", "proof_obligations"]:
            if not isinstance(existing.get(field), list) or len(existing.get(field)) < 2:
                existing[field] = guidance.get(field, [])
        output["negative_tactic_decision"] = existing
        return output
    output["negative_tactic_decision"] = {
        "tactic_mode": clean_text(guidance.get("tactic_mode")),
        "route_family": clean_text(guidance.get("route_family")),
        "reason_for_tactic": clean_text(guidance.get("reason_for_tactic")),
        "exact_negation_or_method_class": clean_text(guidance.get("exact_negation_or_method_class")),
        "contradiction_carrier_or_no_go_family": clean_text(guidance.get("contradiction_carrier_or_no_go_family")),
        "conflict_target": clean_text(guidance.get("conflict_target")),
        "escape_conditions": [clean_text(item) for item in guidance.get("escape_conditions", []) if clean_text(item)][:4],
        "proof_obligations": [clean_text(item) for item in guidance.get("proof_obligations", []) if clean_text(item)][:4],
        "branch_control_decision": clean_text(guidance.get("branch_control_decision")),
        "next_validation_handoff": clean_text(guidance.get("next_validation_handoff")),
        "paper_contribution_potential": clean_text(guidance.get("paper_contribution_potential")),
    }
    return output


def first_matching_text(items: list[str], *markers: str) -> str:
    for item in items:
        text = clean_text(item)
        lowered = text.lower()
        if any(marker in lowered for marker in markers):
            return text
    return ""


def infer_pvsnp_inference_rule(output: dict[str, Any]) -> str:
    text = clean_text(output).lower()
    if any(marker in text for marker in ["ef+", "frege", "proof system", "proof-system", "cr_wext", "sateq"]):
        return "proof_complexity_transfer"
    if any(marker in text for marker in ["no-go", "impossibility", "cannot", "quarantine"]):
        return "impossibility_theorem"
    if any(marker in text for marker in ["transfer inequality", "transfer upper", "source lower", "target exponent"]):
        return "transfer_inequality"
    if any(marker in text for marker in ["natural proof", "relativization", "algebrization", "barrier"]):
        return "barrier_diagnosis"
    return "proof_complexity_transfer"


def pvsnp_model_context(output: dict[str, Any], branch: dict[str, Any], inference_rule: str) -> dict[str, str]:
    lemmas = output.get("candidate_lemmas", []) if isinstance(output.get("candidate_lemmas"), list) else []
    definitions = [clean_text(item) for lemma in lemmas if isinstance(lemma, dict) for item in lemma.get("definitions", [])]
    source = first_matching_text(definitions, "source object") or clean_text(branch.get("controlled_interface"))
    text = clean_text(output).lower()
    if inference_rule == "transfer_inequality":
        reduction_type = "black_box_substitution" if "black" in text or "beta" in text else "projection"
    elif inference_rule == "proof_complexity_transfer":
        reduction_type = "proof_system_simulation"
    elif "oracle" in text:
        reduction_type = "oracle"
    else:
        reduction_type = "none"
    return {
        "source_carrier": source or "P vs NP proof-delivery branch source carrier",
        "target_class": "route-specific P vs NP consequence; no claim of P != NP or SAT notin P/poly without all-exponent transfer",
        "circuit_model": "nonuniform Boolean circuits with explicitly stated proof-system or certificate model",
        "reduction_type": reduction_type,
        "oracle_status": "oracle-free unless an unwitnessed SAT-semantic/extensionality rule is explicitly quarantined as semantic-oracle escape",
    }


def pvsnp_quantifier_context(output: dict[str, Any]) -> dict[str, str]:
    text = clean_text(output).lower()
    advice_status = "advice_free"
    if "advice leak" in text or "hidden advice" in text or "nonuniform row advice" in text:
        advice_status = "hidden_advice_risk"
    exponent_regime = "bounded_window"
    if "all-exponent" in text or "all exponent" in text:
        exponent_regime = "all_constants"
    elif "subpolynomial" in text:
        exponent_regime = "subpolynomial"
    elif "finite" in text and "toy" in text:
        exponent_regime = "fixed_constant"
    return {
        "length_regime": "all_sufficiently_large_lengths",
        "exponent_regime": exponent_regime,
        "uniformity": "advice_free_uniform" if advice_status == "advice_free" else "nonuniform_circuit_family",
        "advice_status": advice_status,
    }


def pvsnp_barrier_status(output: dict[str, Any]) -> dict[str, Any]:
    text = clean_text(output).lower()
    families = ["proof_complexity"]
    if "black" in text or "beta" in text:
        families.append("black_box")
    if "oracle" in text or "semantic-oracle" in text:
        families.append("relativization")
    if "natural" in text and all(marker in text for marker in ["largeness", "constructivity", "usefulness"]):
        families.append("natural_proofs")
    trigger = "route-specific proof/certificate extraction can overclaim if semantic SAT rules, advice, or transfer exponents are not charged"
    if "natural_proofs" in families:
        trigger += "; natural-proofs audit is attached only when largeness, constructivity, and usefulness are each named for the exact extracted property"
    return {
        "barrier_families": list(dict.fromkeys(families)),
        "trigger": trigger,
        "escape_conditions": [
            "advice-free parser or residual decoder is proved for the named proof-system fragment",
            "unwitnessed semantic SAT/extensionality use is isolated as a model change rather than promoted",
            "all transfer exponents and row-support charges remain below the claimed source threshold",
        ],
    }


def attach_pvsnp_inference_quality_packet(output: dict[str, Any], branch: dict[str, Any], cycle_index: int) -> dict[str, Any]:
    """Attach a live, content-derived P vs NP inference-quality packet to theorem-shaped branch outputs."""
    if clean_text(branch.get("target_id")) != "p-vs-np-target":
        return output
    # Keep this packet deterministic and content-derived. API branches are asked
    # to expose the needed theorem fields, but the runner owns the review packet
    # shape so weak model-supplied packets cannot bypass the quality gate.
    output.pop("pvsnp_inference_quality", None)
    lemmas = output.get("candidate_lemmas", []) if isinstance(output.get("candidate_lemmas"), list) else []
    first_lemma = lemmas[0] if lemmas and isinstance(lemmas[0], dict) else {}
    definitions = [clean_text(item) for item in first_lemma.get("definitions", [])]
    assumptions = [clean_text(item) for item in first_lemma.get("assumptions", [])]
    source_object = first_matching_text(definitions, "source object") or clean_text(first_lemma.get("statement"))
    target_object = first_matching_text(definitions, "target object") or clean_text(output.get("control_decision", {}).get("promotion_test"))
    inference_rule = infer_pvsnp_inference_rule(output)
    derivation = output.get("attempted_derivation", {}) if isinstance(output.get("attempted_derivation"), dict) else {}
    blocking_gap = clean_text(derivation.get("blocking_gap"))
    quantifier_context = pvsnp_quantifier_context(output)
    decision = "needs_repair" if blocking_gap or quantifier_context["advice_status"] != "advice_free" else "review_only"
    packet = {
        "packet_id": stable_id("pvsnp-iq-live", branch.get("branch_id"), cycle_index, first_lemma.get("lemma_id"), blocking_gap),
        "target_id": "p-vs-np-target",
        "branch_id": clean_text(branch.get("branch_id")),
        "inference_id": clean_text(first_lemma.get("lemma_id") or derivation.get("derivation_id") or output.get("next_experiment")),
        "source_statement": source_object or "SAT parity/proof-certificate source statement extracted from the active P vs NP branch.",
        "target_statement": target_object or "Target-preserving P vs NP route claim; no global separation is claimed without validated transfer.",
        "inference_rule": inference_rule,
        "model_context": pvsnp_model_context(output, branch, inference_rule),
        "quantifier_context": quantifier_context,
        "parameter_map": {
            "input_length_map": "source length N with polylog SAT-query length L_N and branch-declared row/support exponents",
            "transfer_formula": "if the named proof/certificate parser has subthreshold residual or cover cost, then patching gives a small circuit for H_N^SAT; otherwise the branch must pay the declared row/support threshold",
            "tracked_parameters": [
                "N",
                "M_N",
                "q",
                "rho",
                "epsilon",
                "alpha_ext",
                "K_pi",
                "Delta_SR_h",
            ],
        },
        "side_conditions": [
            "source object and target object are the ones stated in the candidate lemma definitions",
            "the parser, residual decoder, row-support set, and proof-system rules must be advice-free or explicitly quarantined",
            "the result remains a scoped route audit and does not claim P != NP",
            *(assumptions[:2] or ["same model and same length regime must be preserved"]),
        ],
        "barrier_status": pvsnp_barrier_status(output),
        "derivation_status": {
            "status": "blocked_at_named_lemma" if blocking_gap else "proof_sketch",
            "theorem_shape": True,
            "blocked_obligation": blocking_gap or "Complete proof-quality audit before paper promotion.",
        },
        "correctness_criteria": [
            "reduction direction and transfer inequality are stated before claiming target progress",
            "length, exponent, uniformity, advice, and proof-system regimes match between source and target",
            "barrier status is attached to the exact proof/certificate mechanism, not used as a slogan",
            "semantic SAT rules are either witnessed and charged or quarantined as model changes",
        ],
        "failure_modes": [
            "occurrence-label reasoning is silently upgraded to full SAT semantics",
            "hidden advice or nonuniform row selection enters the parser or residual decoder",
            "the branch repeats the semantic fork without proving extraction, countermodel, or named escape",
            "the result is described as P vs NP progress rather than a scoped route-control theorem",
        ],
        "reviewer_findings": [
            {
                "reviewer": "pvsnp-inference-quality-controller",
                "severity": "blocking" if decision == "needs_repair" else "warning",
                "finding": blocking_gap or "The branch is theorem-shaped and requires proof-quality review before promotion.",
            },
            {
                "reviewer": "pvsnp-proof-complexity-transfer-reviewer",
                "severity": "warning",
                "finding": "Check whether the named proof-system fragment really yields the declared parser, quotient, support, or residual object.",
            },
            {
                "reviewer": "pvsnp-quantifier-uniformity-reviewer",
                "severity": "warning",
                "finding": "Audit all lengths, exponent window, uniformity, and advice status before paper handoff.",
            },
        ],
        "decision": decision,
        "validation_handoff": {
            "validator": "agentic/scripts/validate_pvsnp_inference_quality.py",
            "next_skill": "pvsnp-proof-derivation-builder" if decision != "quarantine" else "pvsnp-barrier-specificity-reviewer",
            "report": rel(PVSNP_INFERENCE_QUALITY),
        },
        "live_packet": True,
    }
    output["pvsnp_inference_quality"] = packet
    return output


def repair_equation_validity_conditions(output: dict[str, Any], branch: dict[str, Any]) -> dict[str, Any]:
    """Expand terse equation validity notes without changing the mathematical claim."""
    branch_title = clean_text(branch.get("title") or branch.get("branch_title") or branch.get("branch_id") or "the active branch")
    for lemma in output.get("candidate_lemmas", []):
        if not isinstance(lemma, dict):
            continue
        assumptions = [clean_text(item) for item in lemma.get("assumptions", []) if clean_text(item)]
        definitions = [clean_text(item) for item in lemma.get("definitions", []) if clean_text(item)]
        same_theory = next((item for item in definitions if item.lower().startswith("same-theory condition:")), "")
        support = clean_text(same_theory or (assumptions[0] if assumptions else "the stated source object, target object, and same-theory condition are in force"))
        for eq in lemma.get("equations", []):
            if not isinstance(eq, dict):
                continue
            valid_when = clean_text(eq.get("valid_when"))
            if len(valid_when.split()) >= 8:
                continue
            label = clean_text(eq.get("label") or "this equation")
            prefix = f"{valid_when}; " if valid_when else ""
            eq["valid_when"] = (
                f"{prefix}Valid when {label} is applied inside {branch_title} under {support}, "
                "with the equation interpreted only in the lemma's stated validity regime."
            )
    return output


def repair_attempted_derivation_context(output: dict[str, Any], branch: dict[str, Any]) -> dict[str, Any]:
    """Make attempted derivations cite their local definitions and validity regime."""
    derivation = output.get("attempted_derivation")
    if not isinstance(derivation, dict):
        return output
    steps = derivation.get("steps")
    if not isinstance(steps, list) or not steps:
        return output
    text = clean_text(derivation).lower()
    context_markers = ["definition", "assumption", "valid", "regime", "model", "source object", "target object"]
    if any(marker in text for marker in context_markers):
        return output

    branch_title = clean_text(branch.get("title") or branch.get("branch_title") or branch.get("branch_id") or "the active branch")
    lemma = next((item for item in output.get("candidate_lemmas", []) if isinstance(item, dict)), {})
    definitions = [clean_text(item) for item in lemma.get("definitions", []) if clean_text(item)]
    assumptions = [clean_text(item) for item in lemma.get("assumptions", []) if clean_text(item)]
    source_definition = next((item for item in definitions if "source object" in item.lower()), "")
    target_definition = next((item for item in definitions if "target object" in item.lower()), "")
    validity_assumption = next(
        (
            item
            for item in assumptions
            if any(marker in item.lower() for marker in ["valid", "regime", "model", "uniform", "advice", "semantic", "row", "syntax"])
        ),
        "",
    )
    context_step = (
        "Definition/assumption context: this derivation is interpreted inside "
        f"{branch_title}; {source_definition or 'source object is the branch lemma source object'}; "
        f"{target_definition or 'target object is the branch lemma target object'}; "
        f"{validity_assumption or 'validity regime is the lemma assumptions and same-model proof-system interface'}."
    )
    derivation["steps"] = [context_step, *steps]
    output["attempted_derivation"] = derivation
    return output


def build_codex_branch_output(branch: dict[str, Any], cycle_index: int, branch_budget_seconds: int, api_key_config: str | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    codex = shutil.which("codex")
    if not codex:
        fail("research-mode marathon requires the local `codex` CLI; rerun with --execution-mode smoke for an explicit smoke packet")
    env, api_summary = environment_with_api_keys(api_key_config, require_api_key=False)
    started = time.monotonic()
    attempts = [
        {"name": "primary", "compact": False, "timeout": max(180, branch_budget_seconds + 180)},
        {"name": "compact_retry", "compact": True, "timeout": max(180, branch_budget_seconds + 180)},
    ]
    errors: list[dict[str, Any]] = []
    output: dict[str, Any] | None = None
    used_attempt: dict[str, Any] | None = None
    for attempt in attempts:
        with tempfile.NamedTemporaryFile("w+", suffix=".json", delete=True) as out:
            command = [
                codex,
                "exec",
                "--cd",
                str(ROOT),
                "--sandbox",
                "read-only",
                "--output-schema",
                str(CODEX_BRANCH_SCHEMA),
                "--output-last-message",
                out.name,
                "-",
            ]
            try:
                result = subprocess.run(
                    command,
                    input=branch_prompt(branch, cycle_index, branch_budget_seconds, compact=bool(attempt["compact"])),
                    text=True,
                    cwd=ROOT,
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=int(attempt["timeout"]),
                )
            except subprocess.TimeoutExpired as exc:
                errors.append({"attempt": attempt["name"], "kind": "timeout", "timeout_seconds": attempt["timeout"], "message": str(exc)})
                continue
            if result.returncode != 0:
                errors.append({"attempt": attempt["name"], "kind": "nonzero_return", "message": clean_text(result.stderr)[-800:]})
                continue
            out.seek(0)
            raw = out.read().strip()
        try:
            candidate_output = attach_proof_depth_control_packet(
                attach_physical_relevance_impact_packet(
                    attach_pvsnp_inference_quality_packet(
                        attach_negative_tactic_decision(
                            repair_attempted_derivation_context(repair_equation_validity_conditions(json.loads(raw), branch), branch),
                            branch,
                        ),
                        branch,
                        cycle_index,
                    ),
                    branch,
                    cycle_index,
                ),
                branch,
                cycle_index,
            )
            validate_candidate_branch_output(candidate_output, ROOT / f"codex-output:{branch['branch_id']}", target_id=branch.get("target_id"))
        except json.JSONDecodeError as exc:
            errors.append({"attempt": attempt["name"], "kind": "invalid_json", "message": str(exc)})
            continue
        except BranchValidationError as exc:
            errors.append({"attempt": attempt["name"], "kind": "invalid_or_failed_validation", "message": str(exc)})
            continue
        output = candidate_output
        used_attempt = attempt
        break
    elapsed = time.monotonic() - started
    if output is None or used_attempt is None:
        record = {
            "branch_id": branch["branch_id"],
            "engine": "codex_exec",
            "elapsed_seconds": round(elapsed, 3),
            "status": "failed",
            "reason": "codex_branch_execution_failed",
            "attempts": errors,
            "output_schema": rel(CODEX_BRANCH_SCHEMA),
        }
        raise BranchExecutionError(f"codex branch execution failed for {branch['branch_id']} after {len(errors)} attempt(s)", record)
    output["generated_by"] = "codex_exec"
    record = {
        "branch_id": branch["branch_id"],
        "engine": "codex_exec",
        "elapsed_seconds": round(elapsed, 3),
        "status": "complete",
        "codex_attempt": used_attempt["name"],
        "codex_timeout_seconds": used_attempt["timeout"],
        "output_schema": rel(CODEX_BRANCH_SCHEMA),
        "api_key_config": {
            "source": api_summary.get("source", ""),
            "active_provider": api_summary.get("active_provider", ""),
            "configured_keys": api_summary.get("configured_keys", []),
            "has_openai_api_key": api_summary.get("has_openai_api_key", False),
        },
    }
    return output, record


def extract_response_text(data: dict[str, Any]) -> str:
    text = data.get("output_text")
    if isinstance(text, str) and text.strip():
        return text
    chunks: list[str] = []
    for item in data.get("output", []) or []:
        if not isinstance(item, dict):
            continue
        for content in item.get("content", []) or []:
            if isinstance(content, dict) and isinstance(content.get("text"), str):
                chunks.append(content["text"])
    return "".join(chunks).strip()


def parse_json_text(text: str, branch_id: str) -> dict[str, Any]:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start < 0 or end <= start:
            debug_path = ROOT / "agentic/logs/discovery_marathon_jobs" / f"invalid-api-output-{stable_id('branch', branch_id)}.txt"
            debug_path.parent.mkdir(parents=True, exist_ok=True)
            debug_path.write_text(text, encoding="utf-8")
            raise BranchValidationError(f"API branch output for {branch_id} did not contain JSON; raw output saved to {rel(debug_path)}")
        try:
            payload = json.loads(text[start : end + 1])
        except json.JSONDecodeError as exc:
            debug_path = ROOT / "agentic/logs/discovery_marathon_jobs" / f"invalid-api-output-{stable_id('branch', branch_id)}.txt"
            debug_path.parent.mkdir(parents=True, exist_ok=True)
            debug_path.write_text(text, encoding="utf-8")
            raise BranchValidationError(f"API branch output for {branch_id} was not valid JSON: {exc}; raw output saved to {rel(debug_path)}")
    if not isinstance(payload, dict):
        raise BranchValidationError(f"API branch output for {branch_id} must be a JSON object")
    return payload


def build_api_branch_output(branch: dict[str, Any], cycle_index: int, branch_budget_seconds: int, api_key_config: str | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    host_model = _HOST_MODEL.get()
    env, api_summary = _model_environment(api_key_config, require_api_key=True)
    endpoint = clean_text(env.get("AZURE_OPENAI_RESPONSES_ENDPOINT")) or clean_text(env.get("OPENAI_BASE_URL")).rstrip("/") + "/responses"
    model = host_model[1] if host_model else clean_text(env.get("AZURE_OPENAI_MODEL") or env.get("OPENAI_MODEL"))
    effort = clean_text(env.get("AZURE_OPENAI_REASONING_EFFORT") or env.get("OPENAI_REASONING_EFFORT") or "high")
    key = clean_text(env.get("AZURE_OPENAI_API_KEY") or env.get("OPENAI_API_KEY"))
    if host_model is None and (not endpoint or not model or not key):
        fail("API branch engine requires endpoint, model, and API key in config/api_keys.json or environment")
    schema = json.loads(CODEX_BRANCH_SCHEMA.read_text(encoding="utf-8"))
    configured_max_output_tokens = int_env(env, "AZURE_OPENAI_MAX_OUTPUT_TOKENS", "OPENAI_MAX_OUTPUT_TOKENS", default=12000, minimum=6000)
    max_output_tokens = max(12000, configured_max_output_tokens)
    api_timeout_seconds = int_env(
        env,
        "AZURE_OPENAI_API_TIMEOUT_SECONDS",
        "OPENAI_API_TIMEOUT_SECONDS",
        default=max(600, branch_budget_seconds + 540),
        minimum=180,
    )
    attempts = [
        {"name": "primary", "max_output_tokens": max_output_tokens, "timeout": api_timeout_seconds, "compact": False},
        {
            "name": "compact_retry",
            "max_output_tokens": max(8000, min(12000, int(max_output_tokens * 0.8))),
            "timeout": max(240, min(api_timeout_seconds, 360)),
            "compact": True,
        },
    ]
    errors: list[dict[str, Any]] = []
    data: dict[str, Any] | None = None
    output: dict[str, Any] | None = None
    status = 0
    elapsed = 0.0
    used_attempt: dict[str, Any] | None = None
    started = time.monotonic()
    for attempt in attempts:
        payload = {
            "model": model,
            "input": branch_prompt(branch, cycle_index, branch_budget_seconds, compact=bool(attempt["compact"])),
            "reasoning": {"effort": effort},
            "max_output_tokens": int(attempt["max_output_tokens"]),
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "discovery_marathon_branch_output",
                    "schema": schema,
                    "strict": True,
                }
            },
        }
        try:
            if host_model is not None:
                reply = host_model[0](
                    messages=[{"role": "user", "content": payload["input"]}],
                    response_format={"type": "json_schema", "json_schema": {
                        "name": "discovery_marathon_branch_output", "schema": schema, "strict": True}},
                    max_tokens=payload["max_output_tokens"],
                    reasoning_effort=effort,
                    timeout=int(attempt["timeout"]),
                )
                data = {"output_text": reply["choices"][0]["message"]["content"],
                        "id": reply.get("id", ""), "model": reply.get("model", model)}
                status = 200
            else:
                req = urllib.request.Request(
                    endpoint, data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=int(attempt["timeout"])) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    status = resp.status
            candidate_output = attach_proof_depth_control_packet(
                attach_physical_relevance_impact_packet(
                    attach_pvsnp_inference_quality_packet(
                        attach_negative_tactic_decision(
                            repair_attempted_derivation_context(
                                repair_equation_validity_conditions(parse_json_text(extract_response_text(data), branch["branch_id"]), branch),
                                branch,
                            ),
                            branch,
                        ),
                        branch,
                        cycle_index,
                    ),
                    branch,
                    cycle_index,
                ),
                branch,
                cycle_index,
            )
            validate_candidate_branch_output(candidate_output, ROOT / f"api-output:{branch['branch_id']}", target_id=branch.get("target_id"))
            output = candidate_output
            used_attempt = attempt
            break
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")[:1200]
            errors.append({"attempt": attempt["name"], "kind": "http_error", "status": exc.code, "message": body})
        except (http.client.RemoteDisconnected, urllib.error.URLError, ConnectionError, OSError) as exc:
            errors.append({"attempt": attempt["name"], "kind": "connection_error", "message": str(exc)})
        except (TimeoutError, socket.timeout) as exc:
            errors.append({"attempt": attempt["name"], "kind": "timeout", "timeout_seconds": attempt["timeout"], "message": str(exc)})
        except BranchValidationError as exc:
            errors.append({"attempt": attempt["name"], "kind": "invalid_or_failed_validation", "message": str(exc)})
        except (RuntimeError, KeyError, TypeError, ValueError) as exc:
            if host_model is None:
                raise
            errors.append({"attempt": attempt["name"], "kind": "host_channel_error", "message": str(exc)})
    elapsed = time.monotonic() - started
    if data is None or used_attempt is None or output is None:
        record = {
            "branch_id": branch["branch_id"],
            "engine": "host_model_channel" if host_model else "azure_responses_api",
            "elapsed_seconds": round(elapsed, 3),
            "status": "failed",
            "reason": "api_branch_execution_failed",
            "attempts": errors,
            "model": model,
            "reasoning_effort": effort,
            "api_key_config": {
                "source": api_summary.get("source", ""),
                "active_provider": api_summary.get("active_provider", ""),
                "configured_keys": api_summary.get("configured_keys", []),
                "has_openai_api_key": api_summary.get("has_openai_api_key", False),
            },
        }
        raise BranchExecutionError(f"Azure Responses branch execution failed for {branch['branch_id']} after {len(errors)} attempt(s)", record)
    output["generated_by"] = "host_model_channel" if host_model else "azure_responses_api"
    record = {
        "branch_id": branch["branch_id"],
        "engine": "host_model_channel" if host_model else "azure_responses_api",
        "elapsed_seconds": round(elapsed, 3),
        "status": "complete",
        "http_status": status,
        "api_timeout_seconds": used_attempt["timeout"],
        "api_attempt": used_attempt["name"],
        "prior_attempt_errors": errors,
        "max_output_tokens": used_attempt["max_output_tokens"],
        "response_id": data.get("id", ""),
        "model": data.get("model", model),
        "reasoning_effort": effort,
        "output_schema": rel(CODEX_BRANCH_SCHEMA),
        "api_key_config": {
            "source": api_summary.get("source", ""),
            "active_provider": api_summary.get("active_provider", ""),
            "configured_keys": api_summary.get("configured_keys", []),
            "has_openai_api_key": api_summary.get("has_openai_api_key", False),
        },
    }
    return output, record


def resolve_api_parallel_config(
    selected_count: int,
    *,
    requested_workers: int | None,
    parallel_branches: bool,
    api_key_config: str | None,
    requested_spacing_seconds: float | None,
) -> dict[str, Any]:
    if _HOST_MODEL.get() is not None and (parallel_branches or (requested_workers or 1) > 1):
        raise ValueError("host model channel requires serial API branch execution")
    env, api_summary = _model_environment(api_key_config, require_api_key=False)
    env_workers = int_env(
        env,
        "AZURE_OPENAI_MAX_CONCURRENT_BRANCHES",
        "OPENAI_MAX_CONCURRENT_BRANCHES",
        default=0,
        minimum=0,
    )
    if requested_workers is not None:
        raw_workers = requested_workers
    elif parallel_branches:
        raw_workers = env_workers or selected_count
    else:
        raw_workers = env_workers if env_workers > 1 else 1
    max_workers = max(1, min(selected_count, raw_workers, 8))
    spacing = (
        max(0.0, requested_spacing_seconds)
        if requested_spacing_seconds is not None
        else float_env(
            env,
            "AZURE_OPENAI_BRANCH_REQUEST_SPACING_SECONDS",
            "OPENAI_BRANCH_REQUEST_SPACING_SECONDS",
            default=0.0,
            minimum=0.0,
        )
    )
    return {
        "enabled": max_workers > 1,
        "max_workers": max_workers,
        "request_spacing_seconds": spacing,
        "api_key_config": {
            "source": api_summary.get("source", ""),
            "active_provider": api_summary.get("active_provider", ""),
            "configured_keys": api_summary.get("configured_keys", []),
            "has_openai_api_key": api_summary.get("has_openai_api_key", False),
        },
    }


def parallel_branch_worker(
    *,
    index: int,
    branch: dict[str, Any],
    cycle_index: int,
    branch_budget_seconds: int,
    api_key_config: str | None,
    request_spacing_seconds: float,
    cycle_id: str,
    namespace: Namespace,
    invocation_id: str,
) -> tuple[int, dict[str, Any] | None, dict[str, Any], dict[str, Any]]:
    """Run one isolated branch; launch spacing is throttling, not validity padding."""

    if request_spacing_seconds > 0:
        time.sleep(index * request_spacing_seconds)
    output, record, receipt = execute_branch_with_receipt(
        branch,
        cycle_id=cycle_id,
        cycle_index=cycle_index,
        branch_budget_seconds=branch_budget_seconds,
        execution_mode="research",
        branch_engine="api",
        api_key_config=api_key_config,
        namespace=namespace,
        invocation_id=invocation_id,
    )
    record["parallel_worker_index"] = index
    record["parallel_request_spacing_seconds"] = request_spacing_seconds
    return index, output, record, receipt


def execute_selected_branches(
    selected: list[dict[str, Any]],
    *,
    cycle_index: int,
    branch_budget_seconds: int,
    execution_mode: str,
    branch_engine: str,
    api_key_config: str | None,
    api_parallel_config: dict[str, Any],
    cycle_id: str,
    target_id: str,
    run_id: str,
    state_version: int,
    transaction_store: DiscoveryTransactionStore,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    """Execute branches independently and retain successful siblings.

    Failed branches remain in ``branch_records`` with failed receipts.  Only
    validated successful packets enter ``outputs``; a caller may still commit
    both success and operational-failure deltas in one serialized transaction.
    """

    invocation_ids = [transaction_store.allocate_identity("invocation") for _ in selected]
    if execution_mode == "research" and branch_engine in {"auto", "api"} and api_parallel_config.get("enabled"):
        max_workers = int(api_parallel_config["max_workers"])
        outputs_by_index: dict[int, dict[str, Any]] = {}
        records_by_index: dict[int, dict[str, Any]] = {}
        receipts_by_index: dict[int, dict[str, Any]] = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="pvsnp-api-branch") as executor:
            futures = [
                executor.submit(
                    parallel_branch_worker,
                    index=index,
                    branch=json.loads(json.dumps(branch)),
                    cycle_index=cycle_index,
                    branch_budget_seconds=branch_budget_seconds,
                    api_key_config=api_key_config,
                    request_spacing_seconds=float(api_parallel_config.get("request_spacing_seconds", 0.0)),
                    cycle_id=cycle_id,
                    namespace=Namespace(target_id, run_id, branch["branch_id"], state_version),
                    invocation_id=invocation_ids[index],
                )
                for index, branch in enumerate(selected)
            ]
            for future in concurrent.futures.as_completed(futures):
                index, output, record, receipt = future.result()
                record["parallel_group_size"] = len(selected)
                record["parallel_max_workers"] = max_workers
                records_by_index[index] = record
                receipts_by_index[index] = receipt
                if output is not None:
                    outputs_by_index[index] = output
        return (
            [outputs_by_index[index] for index in sorted(outputs_by_index)],
            [records_by_index[index] for index in range(len(selected))],
            [receipts_by_index[index] for index in range(len(selected))],
        )

    outputs = []
    branch_records = []
    receipts = []
    for index, branch in enumerate(selected):
        output, record, receipt = execute_branch_with_receipt(
            branch,
            cycle_id=cycle_id,
            cycle_index=cycle_index,
            branch_budget_seconds=branch_budget_seconds,
            execution_mode=execution_mode,
            branch_engine=branch_engine,
            api_key_config=api_key_config,
            namespace=Namespace(target_id, run_id, branch["branch_id"], state_version),
            invocation_id=invocation_ids[index],
        )
        record.setdefault("parallel_worker_index", index)
        record.setdefault("parallel_group_size", len(selected))
        record.setdefault("parallel_max_workers", 1)
        if output is not None:
            outputs.append(output)
        branch_records.append(record)
        receipts.append(receipt)
    return outputs, branch_records, receipts


def literature_gap_preinvestment_control(decisions: list[dict[str, Any]]) -> dict[str, Any]:
    warrant_rows = []
    broad_allowed = 0
    artifact_only = 0
    reframe_or_quarantine = 0
    for decision in decisions:
        modes = set(decision.get("allowed_next_modes", []))
        warrant_decision = clean_text(decision.get("warrant_decision"))
        if modes.intersection({"branch_exploration", "broad_branch_exploration"}) and warrant_decision == "invest_in_avenue":
            broad_allowed += 1
        elif warrant_decision == "artifact_sprint_only":
            artifact_only += 1
        elif warrant_decision in {"missing_warrant", "reframe_gap_before_investment", "do_not_invest_prior_art_collision", "quarantine_low_relevance"}:
            reframe_or_quarantine += 1
        warrant_rows.append(
            {
                "branch_id": clean_text(decision.get("branch_id")),
                "avenue_id": clean_text(decision.get("avenue_id")),
                "investment_decision": warrant_decision,
                "allowed_next_modes": list(modes),
                "recommended_move": clean_text(decision.get("recommended_move")),
                "effect": clean_text(decision.get("warrant_effect")),
            }
        )
    if broad_allowed:
        mode = "broad_exploration_allowed_for_invested_avenues"
    elif artifact_only:
        mode = "switched_to_artifact_or_falsifier_sprint"
    else:
        mode = "switched_to_literature_gap_reframe_or_quarantine"
    return {
        "mode": mode,
        "broad_exploration_allowed_count": broad_allowed,
        "artifact_sprint_only_count": artifact_only,
        "reframe_or_quarantine_count": reframe_or_quarantine,
        "warrant_required_before_broad_search": True,
        "warrants": warrant_rows,
        "validator": "agentic/scripts/validate_avenue_literature_gap_warrant.py",
    }


def pvsnp_family_from_text(text: str) -> str:
    lowered = text.lower()
    families = [
        ("hardness_magnification_threshold", ["magnification", "weak lower bound", "threshold", "beta", "exponent", "window"]),
        ("barrier_and_impossibility_control", ["barrier", "relativization", "natural", "algebrization", "oracle", "impossibility", "no-go"]),
        ("meta_complexity_carrier", ["mcsp", "mktp", "meta-complexity", "carrier", "certificate", "explicitness"]),
        ("proof_complexity_transfer", ["proof complexity", "resolution", "frege", "tautology", "lower-bound"]),
        ("quantifier_uniformity_lift", ["all-exponent", "cofinal", "uniformity", "nonuniform", "advice", "p/poly", "padding"]),
        ("gedanken_case_lab", ["gedanken", "toy", "concrete case", "oracle substitution", "finite case"]),
    ]
    for family, markers in families:
        if any(marker in lowered for marker in markers):
            return family
    return "unclassified_pvsnp_pressure"


PVSNP_FAMILY_REDUCER_CONTROL = {
    "hardness_magnification_threshold": {
        "novelty_signal": "Exact transfer parameters a,q,beta and the resulting SAT exponent window.",
        "high_reward_payoff": "Decides whether the route can reach all polynomial exponents or only a bounded window.",
        "pivot_criterion": "Pivot to no-go or a new carrier if beta>0 or q consumes the source lower-bound margin.",
    },
    "barrier_and_impossibility_control": {
        "novelty_signal": "A route-specific barrier premise or escape condition, not a generic barrier citation.",
        "high_reward_payoff": "Can become a negative theorem delimiting a method class.",
        "pivot_criterion": "Backtrack if the branch cannot state the exact naturalness, relativization, or algebrization premise.",
    },
    "meta_complexity_carrier": {
        "novelty_signal": "Advice-free searchable MCSP/MKtP certificate carrier with explicit gap coverage.",
        "high_reward_payoff": "Could turn meta-complexity into uniform lower-bound evidence.",
        "pivot_criterion": "Backtrack if certificate existence is equivalent to the target lower bound or searchability leaves the target class.",
    },
    "proof_complexity_transfer": {
        "novelty_signal": "Proof-system evidence object with verifier overhead and semantic lower-bound soundness separated.",
        "high_reward_payoff": "Either supplies a certificate bridge or proves the bridge is target-equivalent.",
        "pivot_criterion": "Pivot if proof length or semantic soundness is as hard as the lower bound being certified.",
    },
    "quantifier_uniformity_lift": {
        "novelty_signal": "Cofinal all-exponent transfer family with valid-length and advice accounting.",
        "high_reward_payoff": "Separates fixed-window progress from NP not subset P/poly-level consequences.",
        "pivot_criterion": "Quarantine if each exponent requires target-equivalent source hardness or nonuniform advice.",
    },
    "gedanken_case_lab": {
        "novelty_signal": "Concrete complexity case that isolates the next formal pressure variable.",
        "high_reward_payoff": "Can cheaply reveal whether a bridge is worth formalizing.",
        "pivot_criterion": "Stop if it yields intuition without a transfer certificate, falsifier, or formal follow-up.",
    },
    "unclassified_pvsnp_pressure": {
        "novelty_signal": "Unclassified pressure; the next step must name the complexity object and route family.",
        "high_reward_payoff": "Unknown until a source object, target object, and controlled interface are typed.",
        "pivot_criterion": "Backtrack if classification fails after one sharpening cycle.",
    },
}


def build_parallel_synthesis(
    selected: list[dict[str, Any]],
    outputs: list[dict[str, Any]],
    branch_records: list[dict[str, Any]],
    *,
    target_id: str,
    api_parallel_config: dict[str, Any],
) -> dict[str, Any]:
    cited_branch_ids = [output["branch_id"] for output in outputs]
    families: dict[str, list[str]] = {}
    next_actions: list[str] = []
    falsifier_text: list[str] = []
    selected_by_id = {branch["branch_id"]: branch for branch in selected}
    for output in outputs:
        branch = selected_by_id[output["branch_id"]]
        text = clean_text({"branch": branch, "output": output})
        family = pvsnp_family_from_text(text) if target_id == "p-vs-np-target" else "general_target_pressure"
        families.setdefault(family, []).append(output["branch_id"])
        next_actions.append(clean_text(output.get("next_experiment")))
        falsifier_text.extend(clean_text(item) for item in output.get("falsifiers", []) if clean_text(item))
    common_obligations: list[str] = []
    conflicts: list[str] = []
    no_go_opportunities: list[str] = []
    queue_promotions: list[dict[str, Any]] = []
    if target_id == "p-vs-np-target":
        if any("threshold" in clean_text(action).lower() or "beta" in clean_text(action).lower() for action in next_actions):
            common_obligations.append("Name the exact exponent or beta-window and prove that the route keeps it target-preserving after transfer.")
        if any("mcsp" in clean_text(action).lower() or "certificate" in clean_text(action).lower() for action in next_actions):
            common_obligations.append("Separate the meta-complexity carrier from its extraction theorem and test explicitness before claiming lower-bound payoff.")
        if any("natural" in clean_text(item).lower() or "relativ" in clean_text(item).lower() or "algebr" in clean_text(item).lower() for item in falsifier_text):
            no_go_opportunities.append("Turn the named barrier pressure into a route-specific impossibility lemma instead of treating it as folklore.")
        if "hardness_magnification_threshold" in families and "barrier_and_impossibility_control" in families:
            conflicts.append("A magnification route must not use a proof object whose largeness/constructivity falls directly under the natural-proof audit.")
        if "meta_complexity_carrier" in families and "quantifier_uniformity_lift" in families:
            conflicts.append("Carrier-transfer evidence must be checked for advice leakage before any all-exponent or uniform separation consequence is promoted.")
        if not common_obligations:
            family_names = set(families)
            if "hardness_magnification_threshold" in family_names:
                common_obligations.append(
                    "State the source lower-bound model, target class consequence, and exact quantitative threshold that survives the magnification transfer."
                )
            if "barrier_and_impossibility_control" in family_names:
                common_obligations.append(
                    "Name the formal relativization, naturalness, algebrization, or advice-leakage premise that blocks or licenses the route."
                )
            if "meta_complexity_carrier" in family_names:
                common_obligations.append(
                    "Separate the carrier definition, explicitness/sparsity condition, verifier overhead, and extraction theorem before promotion."
                )
            if not common_obligations:
                common_obligations.append(
                    "Name the source object, target object, controlled interface, quantitative parameter, and falsifier before the next queue promotion."
                )
        for family, branch_ids in sorted(families.items()):
            control = PVSNP_FAMILY_REDUCER_CONTROL.get(family, PVSNP_FAMILY_REDUCER_CONTROL["unclassified_pvsnp_pressure"])
            action = next((item for item in next_actions if item), "")
            tactic_packets = [
                output.get("negative_tactic_decision", {})
                for output in outputs
                if output.get("branch_id") in branch_ids and isinstance(output.get("negative_tactic_decision"), dict)
            ]
            primary_tactic = tactic_packets[0] if tactic_packets else {}
            queue_promotions.append(
                {
                    "pressure_family": family,
                    "cited_branch_ids": branch_ids,
                    "next_analysis": action,
                    "negative_tactic_mode": primary_tactic.get("tactic_mode", ""),
                    "negative_tactic_route_family": primary_tactic.get("route_family", ""),
                    "negative_tactic_escape_conditions": primary_tactic.get("escape_conditions", []),
                    "negative_tactic_validation_handoff": primary_tactic.get("next_validation_handoff", ""),
                    "novelty_signal": control["novelty_signal"],
                    "high_reward_payoff": control["high_reward_payoff"],
                    "step_back_or_pivot_criterion": control["pivot_criterion"],
                    "promotion_test": (
                        "Promote only if the next packet returns a named source object, named target object, quantitative threshold, "
                        "and a falsifier that would force repair or quarantine."
                    ),
                }
            )
    elif target_id == "yang-mills-existence-and-mass-gap-target":
        common_obligations.append(
            "Invest only in YM branches with high physics conceptual reward and explicit unification power; otherwise demote, reframe, pivot, stop, quarantine, or route to a named artifact/falsifier sprint."
        )
        for output in outputs:
            gate = output.get("physical_relevance_impact", {}).get("major_publication_gate", {})
            queue_promotions.append(
                {
                    "pressure_family": "ym_physics_conceptual_reward",
                    "cited_branch_ids": [output["branch_id"]],
                    "next_analysis": clean_text(output.get("next_experiment")),
                    "physics_conceptual_reward": clean_text(gate.get("physics_conceptual_reward")),
                    "major_publication_potential": gate.get("major_publication_potential", False),
                    "investment_decision": clean_text(gate.get("investment_decision")),
                    "promotion_test": (
                        "Promote ordinary YM proof search only when major_publication_gate.investment_decision is "
                        "invest_high_physics_reward and the branch names its unification-power payoff; otherwise demote, reframe, pivot, stop, quarantine, or run only the named artifact/falsifier sprint."
                    ),
                }
            )
    else:
        common_obligations.append("Preserve source object, target object, equation validity conditions, and falsifiers across the next serialized queue.")
        for output in outputs:
            queue_promotions.append(
                {
                    "pressure_family": "general_target_pressure",
                    "cited_branch_ids": [output["branch_id"]],
                    "next_analysis": clean_text(output.get("next_experiment")),
                    "promotion_test": "Promote only if the next packet strengthens a target-preserving bridge or formal falsifier.",
                }
            )
    return {
        "enabled": bool(api_parallel_config.get("enabled")),
        "merge_policy": "scheduler_order_single_writer",
        "state_mutation_policy": "one CAS reducer commit retains validated successes and branch-local operational failures before legacy projections are written",
        "cited_branch_ids": cited_branch_ids,
        "branch_record_statuses": [record.get("status", "") for record in branch_records],
        "pressure_families": families,
        "common_proof_obligations": common_obligations,
        "cross_branch_conflicts": conflicts,
        "no_go_opportunities": no_go_opportunities,
        "queue_promotions": queue_promotions,
    }


def _semantic_output_projection(output: dict[str, Any]) -> dict[str, Any]:
    """Select conceptual structure while excluding prose length and runtime."""

    return {
        key: output.get(key)
        for key in (
            "branch_id",
            "candidate_lemmas",
            "derivation_steps",
            "equations",
            "dependency_updates",
            "falsifiers",
            "blocking_gap",
            "mathematical_learning",
            "next_experiment",
            "control_decision",
            "conceptual_abstraction_revision",
            "proof_depth_control",
        )
        if key in output
    }


def _recommended_transition(output: dict[str, Any]) -> str:
    """Map the legacy control vocabulary into the reducer's closed transition set."""

    decision = clean_text(output.get("control_decision", {}).get("decision")).lower()
    for marker, transition in (
        ("quarantine", "quarantine"),
        ("backtrack", "backtrack"),
        ("pivot", "pivot"),
        ("stop", "exhaust"),
        ("complete", "complete"),
        ("promote", "promote"),
    ):
        if marker in decision:
            return transition
    return "persist"


def build_marathon_learning_deltas(
    *,
    target_id: str,
    run_id: str,
    cycle_id: str,
    state_version: int,
    execution_mode: str,
    selected: list[dict[str, Any]],
    outputs: list[dict[str, Any]],
    branch_records: list[dict[str, Any]],
    operator_receipts: list[dict[str, Any]],
    prior_branch_states: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Translate execution outcomes into schema-valid semantic/operational deltas."""

    outputs_by_branch = {output["branch_id"]: output for output in outputs}
    records_by_branch = {record["branch_id"]: record for record in branch_records}
    receipts_by_branch = {
        receipt["identity"]["branch_id"]: receipt for receipt in operator_receipts
    }
    deltas: list[dict[str, Any]] = []
    for branch in selected:
        branch_id = branch["branch_id"]
        record = records_by_branch[branch_id]
        receipt = receipts_by_branch[branch_id]
        identity = {
            "target_id": target_id,
            "run_id": run_id,
            "branch_id": branch_id,
            "state_version": state_version,
        }
        delta_id = stable_identifier(
            "marathon-delta", cycle_id, branch_id, receipt["receipt_id"]
        )
        base = {
            "schema_version": "1.0.0",
            "delta_id": delta_id,
            "identity": identity,
            "truth_status": "unknown",
            "duration_seconds": max(0.0, float(record.get("elapsed_seconds", 0.0))),
            "affected_hypothesis_ids": [],
            "literature_effects": {
                "snapshot_id": None,
                "changed_concept_ids": [],
                "changed_relation_ids": [],
                "scheduled_action_ids": [],
            },
            "source_event_ids": [
                stable_identifier("marathon-event", cycle_id, branch_id, receipt["status"])
            ],
            "operator_receipt_ids": [receipt["receipt_id"]],
        }
        output = outputs_by_branch.get(branch_id)
        if receipt["status"] != "succeeded" or output is None:
            deltas.append(
                {
                    **base,
                    "classification": "operational_failure",
                    "worker_status": (
                        "timed_out" if receipt["status"] == "timed_out" else "failed"
                    ),
                    "semantic_mutations": [],
                    "evidence": {
                        "status": "failed_execution",
                        "relation": "none",
                        "claim_ids": [],
                        "falsified_premise": None,
                    },
                    "summary": "Branch execution failed operationally; no epistemic conclusion was drawn.",
                    "operational_error": {
                        "type": clean_text(receipt.get("error", {}).get("type")) or "BranchExecutionError",
                        "message": clean_text(receipt.get("error", {}).get("message")),
                    },
                    "recommended_transition": "persist",
                    "stop_condition": "operational_failure",
                }
            )
            continue

        projection_digest = canonical_digest(_semantic_output_projection(output))
        before_digest = prior_branch_states[branch_id].get("last_output_semantic_digest")
        changed = execution_mode == "research" and projection_digest != before_digest
        classification = "conceptual_deepening" if changed else (
            "duplicate" if execution_mode == "research" else "rhetorical_rewrite"
        )
        mutations = (
            [
                {
                    "mutation_kind": "mechanism_revised",
                    "entity_id": branch_id,
                    "before_digest": before_digest,
                    "after_digest": projection_digest,
                    "description": "Validated branch structure changed relative to its prior semantic projection.",
                }
            ]
            if changed
            else []
        )
        deltas.append(
            {
                **base,
                "classification": classification,
                "worker_status": "succeeded",
                "semantic_mutations": mutations,
                "evidence": {
                    "status": "none",
                    "relation": "none",
                    "claim_ids": [],
                    "falsified_premise": None,
                },
                "summary": (
                    "A validated structural mutation was recognized; truth remains unknown."
                    if changed
                    else "No new semantic mutation was recognized."
                ),
                "recommended_transition": _recommended_transition(output),
            }
        )
    return deltas


def commit_marathon_cycle(
    store: DiscoveryTransactionStore,
    *,
    cycle_id: str,
    selected: list[dict[str, Any]],
    outputs: list[dict[str, Any]],
    branch_records: list[dict[str, Any]],
    operator_receipts: list[dict[str, Any]],
    execution_mode: str,
    expected_generation: int | None = None,
    canonical_theory_gate: Mapping[str, Any] | None = None,
    canonical_action_reservation: Mapping[str, Any] | None = None,
    compatibility_contract_version: str | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    """Reduce all siblings and publish one journaled CAS generation."""

    expected_generation = (
        store.current_generation() if expected_generation is None else expected_generation
    )
    for receipt in operator_receipts:
        if receipt["identity"]["state_version"] != expected_generation:
            raise BranchExecutionError(
                "operator receipt state version does not match the frozen transaction generation",
                {"receipt_id": receipt["receipt_id"]},
            )
    prior = store.read_state(expected_generation) if expected_generation else None
    prior_state = prior or {
        "schema_version": "1.0.0",
        "target_id": store.target_id,
        "run_id": store.run_id,
        "generation": 0,
        "branches": {},
        "cycle_history": [],
    }
    prior_branch_states: dict[str, dict[str, Any]] = {}
    for branch in selected:
        branch_id = branch["branch_id"]
        prior_branch_states[branch_id] = json.loads(
            json.dumps(
                prior_state.get("branches", {}).get(branch_id)
                or initial_branch_state(
                    target_id=store.target_id,
                    run_id=store.run_id,
                    branch_id=branch_id,
                )
            )
        )
    deltas = build_marathon_learning_deltas(
        target_id=store.target_id,
        run_id=store.run_id,
        cycle_id=cycle_id,
        state_version=expected_generation,
        execution_mode=execution_mode,
        selected=selected,
        outputs=outputs,
        branch_records=branch_records,
        operator_receipts=operator_receipts,
        prior_branch_states=prior_branch_states,
    )
    reducer = LearningReducer()
    next_branch_states: dict[str, dict[str, Any]] = {}
    reducer_receipts: list[dict[str, Any]] = []
    outputs_by_branch = {output["branch_id"]: output for output in outputs}
    for delta in deltas:
        branch_id = delta["identity"]["branch_id"]
        state = prior_branch_states[branch_id]
        reduced, reducer_receipt = reducer.reduce(
            state, delta, expected_generation=state["generation"]
        )
        output = outputs_by_branch.get(branch_id)
        if output is not None and execution_mode == "research":
            reduced["last_output_semantic_digest"] = canonical_digest(
                _semantic_output_projection(output)
            )
        next_branch_states[branch_id] = reduced
        reducer_receipts.append(reducer_receipt)

    next_state = json.loads(json.dumps(prior_state))
    next_state["generation"] = expected_generation + 1
    next_state["run_status"] = "running"
    next_state.setdefault("branches", {}).update(next_branch_states)
    next_state.setdefault("cycle_history", []).append(
        {
            "cycle_id": cycle_id,
            "operator_receipt_ids": [row["receipt_id"] for row in operator_receipts],
            "reducer_receipt_ids": [row["reducer_receipt_id"] for row in reducer_receipts],
            "successful_branch_ids": [output["branch_id"] for output in outputs],
            "operational_failure_branch_ids": [
                delta["identity"]["branch_id"]
                for delta in deltas
                if delta["classification"] == "operational_failure"
            ],
            "compatibility_contract_version": compatibility_contract_version,
            "canonical_source_commit_id": (
                canonical_theory_gate.get("commit_id") if canonical_theory_gate else None
            ),
            "canonical_operator_evidence_digest": (
                canonical_theory_gate.get("operator_evidence_digest")
                if canonical_theory_gate else None
            ),
            "canonical_reservation_id": (
                canonical_action_reservation.get("reservation_id")
                if canonical_action_reservation else None
            ),
            "canonical_reservation_digest": (
                canonical_action_reservation.get("reservation_digest")
                if canonical_action_reservation else None
            ),
        }
    )
    artifacts: list[CommitArtifact] = []
    receipts_by_branch = {
        row["identity"]["branch_id"]: row for row in operator_receipts
    }
    reducer_by_branch = {
        row["identity"]["branch_id"]: row for row in reducer_receipts
    }
    for delta in deltas:
        branch_id = delta["identity"]["branch_id"]
        envelope = {
            "cycle_id": cycle_id,
            "operator_receipt": receipts_by_branch[branch_id],
            "learning_delta": delta,
            "reducer_receipt": reducer_by_branch[branch_id],
        }
        artifacts.append(
            CommitArtifact(
                f"branches/{branch_id}/cycles/{cycle_id}.json",
                (json.dumps(envelope, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8"),
                Namespace(store.target_id, store.run_id, branch_id, expected_generation),
            )
        )
    if canonical_theory_gate is not None or canonical_action_reservation is not None:
        if (
            compatibility_contract_version != COMPATIBILITY_CONTRACT_VERSION
            or not isinstance(canonical_theory_gate, Mapping)
            or not isinstance(canonical_action_reservation, Mapping)
        ):
            raise BranchExecutionError(
                "authoritative compatibility commit requires the complete v2 theory gate and reservation"
            )
        compatibility_envelope = {
            "compatibility_contract_version": compatibility_contract_version,
            "cycle_id": cycle_id,
            "target_id": store.target_id,
            "run_id": store.run_id,
            "selected_branch_ids": sorted(branch["branch_id"] for branch in selected),
            "canonical_theory_gate": dict(canonical_theory_gate),
            "canonical_action_reservation": dict(canonical_action_reservation),
        }
        compatibility_envelope["compatibility_digest"] = canonical_digest(
            compatibility_envelope
        )
        artifacts.append(
            CommitArtifact(
                f"branches/control/cycles/{cycle_id}/canonical-authority.json",
                (
                    json.dumps(
                        compatibility_envelope,
                        indent=2,
                        sort_keys=True,
                        ensure_ascii=False,
                    )
                    + "\n"
                ).encode("utf-8"),
                Namespace(store.target_id, store.run_id, "control", expected_generation),
            )
        )
    request_digest = canonical_digest(
        {
            "cycle_id": cycle_id,
            "operator_receipt_ids": [row["receipt_id"] for row in operator_receipts],
            "delta_ids": [row["delta_id"] for row in deltas],
            "compatibility_contract_version": compatibility_contract_version,
            "canonical_theory_authorization_basis_digest": (
                canonical_theory_gate.get("authorization_basis_digest")
                if canonical_theory_gate else None
            ),
            "canonical_theory_present_decision_digest": (
                canonical_theory_gate.get("present_investment_decision_digest")
                if canonical_theory_gate else None
            ),
            "canonical_reservation_digest": (
                canonical_action_reservation.get("reservation_digest")
                if canonical_action_reservation else None
            ),
        }
    )
    commit = store.commit(
        expected_generation=expected_generation,
        state=next_state,
        artifacts=artifacts,
        idempotency_key=cycle_id,
        request_digest=request_digest,
    )
    transaction_receipt = {
        "commit_id": commit.commit_id,
        "generation": commit.generation,
        "manifest_digest": commit.manifest_digest,
        "idempotent": commit.idempotent,
        "request_digest": request_digest,
        "transaction_root": str(store.root.resolve()),
        "commit_path": str(commit.commit_path.resolve()),
    }
    return next_branch_states, deltas, reducer_receipts, transaction_receipt


def commit_run_status_transition(
    store: DiscoveryTransactionStore, *, status: str, cause_id: str
) -> dict[str, Any]:
    """Commit a run-level transition instead of mutating only the legacy pointer."""

    expected = store.current_generation()
    prior = store.read_state(expected)
    if prior is None:
        raise BranchExecutionError("cannot transition a run before its first authoritative cycle")
    next_state = json.loads(json.dumps(prior))
    next_state["generation"] = expected + 1
    next_state["run_status"] = status
    next_state["run_status_cause_id"] = cause_id
    request_digest = canonical_digest(
        {"expected_generation": expected, "status": status, "cause_id": cause_id}
    )
    result = store.commit(
        expected_generation=expected,
        state=next_state,
        artifacts=(),
        idempotency_key=stable_identifier("run-status", cause_id, status),
        request_digest=request_digest,
    )
    return {
        "commit_id": result.commit_id,
        "generation": result.generation,
        "manifest_digest": result.manifest_digest,
        "idempotent": result.idempotent,
    }


def finalize_canonical_action_reservation(
    reserved_authorization: Mapping[str, Any],
    *,
    terminal_status: str,
    outcome_receipt_id: str,
    detail: str,
) -> dict[str, Any]:
    """CAS-commit one immutable terminal outcome for an action reservation.

    A release is an operational release from further investment, not permission
    to reuse an action already consumed by the reservation transaction.  Any
    retry must be authorized by a fresh canonical cycle and fresh action IDs.
    """

    if terminal_status not in RESERVATION_TERMINAL_STATUSES:
        raise ContractError(f"unknown reservation terminal status: {terminal_status}")
    outcome_receipt_id = validate_identifier(outcome_receipt_id, "outcome_receipt_id")
    reservation = reserved_authorization.get("reservation")
    if not isinstance(reservation, Mapping):
        raise ContractError("reservation terminal transition requires a reservation receipt")
    reservation_id = validate_identifier(
        str(reservation.get("reservation_id", "")), "reservation_id"
    )
    expected_generation = int(reserved_authorization["committed_state_version"])
    state_root = Path(str(reserved_authorization["transaction_root"])).resolve()
    store = DiscoveryTransactionStore(
        state_root,
        target_id=str(reserved_authorization["target_id"]),
        run_id=str(reserved_authorization["run_id"]),
    )
    if store.current_generation() != expected_generation:
        raise ContractError(
            "canonical state changed before reservation terminal transition"
        )
    current = store.read_state(expected_generation)
    if current is None:
        raise ContractError("reserved canonical state is unreadable")
    lifecycle = {
        "schema_version": "1.0.0",
        "reservation_id": reservation_id,
        "reservation_digest": reservation["reservation_digest"],
        "target_id": store.target_id,
        "run_id": store.run_id,
        "source_state_generation": expected_generation,
        "terminal_state_generation": expected_generation + 1,
        "terminal_status": terminal_status,
        "outcome_receipt_id": outcome_receipt_id,
        "detail": clean_text(detail) or terminal_status,
        "action_ids": list(reservation.get("action_ids", [])),
        "action_reuse_allowed": False,
        "compensation_required": terminal_status == "compensation_required",
        "completed_utc": utc_now(),
    }
    lifecycle["lifecycle_digest"] = canonical_digest(lifecycle)
    event = build_event(
        sequence=int(current["event_count"]) + 1,
        previous_event_hash=str(current["last_event_hash"]),
        namespace=Namespace(store.target_id, store.run_id, "control", expected_generation),
        event_type="reflection_recorded",
        entity_type="reflection",
        entity_id=stable_identifier(
            "reservation-terminal", reservation_id, outcome_receipt_id
        ),
        payload={
            "kind": "canonical_action_reservation_terminal",
            "reservation_id": reservation_id,
            "reservation_digest": reservation["reservation_digest"],
            "terminal_status": terminal_status,
            "lifecycle_digest": lifecycle["lifecycle_digest"],
            "action_reuse_allowed": False,
            "compensation_required": lifecycle["compensation_required"],
        },
        actor="legacy-marathon-reservation-lifecycle",
        source_receipt_ids=[outcome_receipt_id],
    )
    next_state = reduce_from_state(current, [event])
    request_digest = canonical_digest(
        {
            "reservation_id": reservation_id,
            "reservation_digest": reservation["reservation_digest"],
            "expected_generation": expected_generation,
            "terminal_status": terminal_status,
            "outcome_receipt_id": outcome_receipt_id,
            "lifecycle_digest": lifecycle["lifecycle_digest"],
        }
    )
    result = store.commit(
        expected_generation=expected_generation,
        state=next_state,
        artifacts=(
            CommitArtifact(
                relative_path=(
                    f"branches/control/reservations/{reservation_id}/terminal.json"
                ),
                content=(json.dumps(lifecycle, indent=2, sort_keys=True) + "\n").encode(),
                namespace=Namespace(
                    store.target_id, store.run_id, "control", expected_generation
                ),
            ),
            CommitArtifact(
                relative_path=(
                    f"branches/control/reservations/{reservation_id}/terminal-event.json"
                ),
                content=(json.dumps(event, indent=2, sort_keys=True) + "\n").encode(),
                namespace=Namespace(
                    store.target_id, store.run_id, "control", expected_generation
                ),
            ),
        ),
        idempotency_key=stable_identifier(
            "reservation-terminal", reservation_id, outcome_receipt_id
        ),
        request_digest=request_digest,
    )
    return {
        **lifecycle,
        "terminal_commit_id": result.commit_id,
        "terminal_manifest_digest": result.manifest_digest,
        "terminal_commit_path": str(result.commit_path.resolve()),
        "terminal_transaction_root": str(store.root.resolve()),
    }


def canonical_lineage_after_reservation(
    reserved_authorization: Mapping[str, Any],
    terminal: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Project the exact canonical generation consumed by the next cycle gate."""

    lineage = {
        key: reserved_authorization[key]
        for key in (
            "target_id",
            "run_id",
            "cycle_id",
            "prior_state_version",
            "committed_state_version",
            "commit_id",
            "manifest_digest",
            "transaction_root",
            "projection_path",
            "projection_digest",
            "schedule_id",
            "operator_evidence_digest",
            "reservation_digest",
            "reserved_branch_ids",
            "reserved_action_ids",
        )
    }
    if terminal is not None:
        lineage.update(
            {
                "committed_state_version": terminal["terminal_state_generation"],
                "commit_id": terminal["terminal_commit_id"],
                "manifest_digest": terminal["terminal_manifest_digest"],
                "reservation_terminal_status": terminal["terminal_status"],
                "reservation_terminal_digest": terminal["lifecycle_digest"],
            }
        )
    return lineage


def run_one_cycle(
    run_state: dict[str, Any],
    max_active_branches: int | None = None,
    *,
    execution_mode: str = "research",
    min_cycle_seconds: int | None = None,
    branch_engine: str = "auto",
    api_key_config: str | None = None,
    api_max_workers: int | None = None,
    parallel_branches: bool = False,
    api_request_spacing_seconds: float | None = None,
    canonical_theory_cycle: Path | str | None = None,
    canonical_theory_state_root: Path | str = DEFAULT_CANONICAL_THEORY_STATE_ROOT,
    canonical_authorization_basis_digest: str | None = None,
    canonical_source_present_decision_digest: str | None = None,
    canonical_schedule_id: str | None = None,
) -> dict[str, Any]:
    """Run one compatibility cycle under a canonical theory authorization.

    Research mode verifies the exact canonical CAS commit before the legacy
    scheduler can see a branch.  The two runtimes retain separate transaction
    roots and schemas; only target/run lineage plus exact branch authorization
    crosses this seam.  Smoke mode remains useful for mechanics but is recorded
    as non-authoritative research output.
    """

    transaction_store = marathon_transaction_store(run_state)
    state_version = transaction_store.current_generation()
    if execution_mode == "research":
        if canonical_theory_cycle is None:
            fail(
                "research discovery marathon requires --canonical-theory-cycle before branch selection"
            )
        if Path(canonical_theory_state_root).resolve() == transaction_store.root.resolve():
            fail("canonical theory and legacy marathon transaction roots must be distinct")
        try:
            theory_gate = verify_canonical_theory_cycle(
                canonical_theory_cycle,
                target_id=clean_text(run_state["target_id"]),
                run_id=clean_text(run_state["run_id"]),
                state_root=canonical_theory_state_root,
                previous_lineage=run_state.get("canonical_theory_lineage"),
            )
        except ContractError as exc:
            fail(str(exc))
        try:
            if canonical_authorization_basis_digest is not None:
                validate_digest(canonical_authorization_basis_digest)
                if (
                    theory_gate.get("authorization_basis_digest")
                    != canonical_authorization_basis_digest
                ):
                    raise ContractError("canonical authorization basis digest mismatch")
            if canonical_source_present_decision_digest is not None:
                validate_digest(canonical_source_present_decision_digest)
            if canonical_schedule_id is not None:
                validate_identifier(canonical_schedule_id, "canonical_schedule_id")
                if theory_gate.get("schedule_id") != canonical_schedule_id:
                    raise ContractError("canonical schedule id mismatch")
        except ContractError as exc:
            fail(str(exc))
    else:
        theory_gate = {
            "schema_version": "1.0.0",
            "status": "smoke_non_authoritative",
            "authoritative": False,
            "target_id": clean_text(run_state["target_id"]),
            "run_id": clean_text(run_state["run_id"]),
            "restrictions": [
                "no_research_authority",
                "no_theory_investment_claim",
                "no_promotion",
            ],
        }
    branches = load_branches(run_state)
    apply_authoritative_projection(run_state, branches, transaction_store)
    if execution_mode == "research":
        try:
            branches = filter_authorized_branches(branches, theory_gate)
        except ContractError as exc:
            fail(str(exc))
    selected, decisions = select_branches(branches, max_active_branches or run_state.get("max_active_branches", 3))
    if not selected:
        fail("discovery marathon scheduler selected no executable branches")
    literature_gap_control = literature_gap_preinvestment_control(decisions)
    artifact_stop_control = artifact_or_stop_preflight(decisions, run_state.get("target_id", ""))
    if (
        execution_mode == "research"
        and branch_engine in {"auto", "api", "codex"}
        and artifact_stop_control.get("preflight_decision") == "block_broad_api_marathon"
    ):
        fail(
            "YM artifact-or-stop preflight blocks another broad research cycle: all selected branches are artifact-blocked. "
            "Run an endpoint artifact_sprint, falsifier_sprint, publication_demotion, or quarantine instead."
        )
    cycle_id = transaction_store.allocate_identity("cycle")
    theory_reservation = None
    reserved_authorization = None
    reservation_terminal = None
    if execution_mode == "research":
        consumer_receipt_id = stable_identifier(
            "legacy-marathon-consumer",
            run_state["target_id"],
            run_state["run_id"],
            cycle_id,
            sorted(branch["branch_id"] for branch in selected),
            theory_gate["commit_id"],
        )
        try:
            reserved_authorization = reserve_canonical_theory_actions(
                theory_gate,
                branch_ids=[branch["branch_id"] for branch in selected],
                consumer_receipt_id=consumer_receipt_id,
                consumer_scope="legacy_marathon",
            )
        except ContractError as exc:
            fail(str(exc))
        theory_reservation = {
            **reserved_authorization["reservation"],
            "reservation_commit_id": reserved_authorization["commit_id"],
            "reservation_manifest_digest": reserved_authorization["manifest_digest"],
            "reservation_transaction_root": reserved_authorization["transaction_root"],
            "reservation_committed_state_version": reserved_authorization[
                "committed_state_version"
            ],
            "source_authorization_basis_digest": reserved_authorization[
                "authorization_basis_digest"
            ],
            "source_present_investment_decision_digest": reserved_authorization[
                "present_investment_decision_digest"
            ],
            "reservation_authorization_basis_digest": reserved_authorization[
                "reservation_authorization_basis_digest"
            ],
        }
        run_state["canonical_theory_lineage"] = canonical_lineage_after_reservation(
            reserved_authorization
        )
        # Persist the reservation address before branch execution. If even
        # that compatibility projection fails, close the canonical lifecycle
        # as released (without making consumed actions reusable).
        try:
            write_json(run_dir(run_state["run_id"]) / "run_state.json", run_state)
            write_active_run_pointers(run_state)
        except BaseException as persistence_error:
            try:
                reservation_terminal = finalize_canonical_action_reservation(
                    reserved_authorization,
                    terminal_status="released",
                    outcome_receipt_id=stable_identifier(
                        "legacy-marathon-release",
                        cycle_id,
                        type(persistence_error).__name__,
                    ),
                    detail=(
                        "legacy reservation projection could not be persisted; "
                        + (str(persistence_error) or type(persistence_error).__name__)
                    ),
                )
            except Exception as lifecycle_error:
                raise BranchExecutionError(
                    "reservation projection failed and canonical release CAS failed",
                    {
                        "persistence_error": str(persistence_error),
                        "lifecycle_error": str(lifecycle_error),
                        "reservation_id": theory_reservation.get("reservation_id"),
                    },
                ) from persistence_error
            raise
    cycle_index = int(run_state.get("cycle_count", 0)) + 1
    started_monotonic = time.monotonic()
    started_utc = utc_now()
    target_seconds = 0 if execution_mode == "smoke" else int(min_cycle_seconds if min_cycle_seconds is not None else int(run_state.get("cycle_minutes", 30)) * 60)
    cycle_mode = execution_mode
    branch_budget = max(60, target_seconds // max(1, len(selected))) if execution_mode == "research" else 0
    api_parallel_config = resolve_api_parallel_config(
        len(selected),
        requested_workers=api_max_workers,
        parallel_branches=parallel_branches,
        api_key_config=api_key_config,
        requested_spacing_seconds=api_request_spacing_seconds,
    )
    investment_started = False
    try:
        investment_started = True
        outputs, branch_records, operator_receipts = execute_selected_branches(
            selected,
            cycle_index=cycle_index,
            branch_budget_seconds=branch_budget,
            execution_mode=execution_mode,
            branch_engine=branch_engine,
            api_key_config=api_key_config,
            api_parallel_config=api_parallel_config,
            cycle_id=cycle_id,
            target_id=run_state["target_id"],
            run_id=run_state["run_id"],
            state_version=state_version,
            transaction_store=transaction_store,
        )
        elapsed = time.monotonic() - started_monotonic
        authoritative_branches, learning_deltas, reducer_receipts, transaction_receipt = commit_marathon_cycle(
            transaction_store,
            cycle_id=cycle_id,
            selected=selected,
            outputs=outputs,
            branch_records=branch_records,
            operator_receipts=operator_receipts,
            execution_mode=execution_mode,
            expected_generation=state_version,
            canonical_theory_gate=theory_gate if execution_mode == "research" else None,
            canonical_action_reservation=theory_reservation,
            compatibility_contract_version=(
                COMPATIBILITY_CONTRACT_VERSION if execution_mode == "research" else None
            ),
        )
    except BaseException as execution_error:
        if execution_mode == "research" and reserved_authorization is not None:
            terminal_status = "compensation_required" if investment_started else "released"
            try:
                reservation_terminal = finalize_canonical_action_reservation(
                    reserved_authorization,
                    terminal_status=terminal_status,
                    outcome_receipt_id=stable_identifier(
                        "legacy-marathon-failure", cycle_id, type(execution_error).__name__
                    ),
                    detail=str(execution_error) or type(execution_error).__name__,
                )
                run_state["canonical_theory_lineage"] = canonical_lineage_after_reservation(
                    reserved_authorization, reservation_terminal
                )
                write_json(run_dir(run_state["run_id"]) / "run_state.json", run_state)
                write_active_run_pointers(run_state)
            except Exception as lifecycle_error:
                raise BranchExecutionError(
                    "branch execution failed and reservation compensation could not be CAS-committed",
                    {
                        "execution_error": str(execution_error),
                        "lifecycle_error": str(lifecycle_error),
                        "reservation_id": theory_reservation.get("reservation_id") if theory_reservation else None,
                    },
                ) from execution_error
        raise
    if execution_mode == "research" and reserved_authorization is not None:
        try:
            reservation_terminal = finalize_canonical_action_reservation(
                reserved_authorization,
                terminal_status="completed",
                outcome_receipt_id=transaction_receipt["commit_id"],
                detail="legacy compatibility cycle committed",
            )
        except ContractError as exc:
            raise BranchExecutionError(
                "legacy cycle committed but reservation completion CAS failed",
                {
                    "legacy_commit_id": transaction_receipt["commit_id"],
                    "reservation_id": theory_reservation.get("reservation_id") if theory_reservation else None,
                    "lifecycle_error": str(exc),
                    "compensation_required": True,
                },
            ) from exc
        run_state["canonical_theory_lineage"] = canonical_lineage_after_reservation(
            reserved_authorization, reservation_terminal
        )
        # The terminal canonical generation is the next cycle's required
        # predecessor. Persist it immediately, before rebuilding projections,
        # so a crash cannot strand the legacy pointer on the reservation gen.
        write_json(run_dir(run_state["run_id"]) / "run_state.json", run_state)
        write_active_run_pointers(run_state)
    branch_titles = [branch["title"] for branch in selected]
    dispatch_trace = build_skill_dispatch_trace(
        cycle_id,
        [branch["branch_id"] for branch in selected],
        branch_titles,
        target_id=run_state["target_id"],
        run_id=run_state["run_id"],
        state_version=state_version,
        operator_receipts=operator_receipts,
        canonical_theory_gate=theory_gate,
    )
    successful_branch_ids = [output["branch_id"] for output in outputs]
    operational_failure_branch_ids = [
        delta["identity"]["branch_id"]
        for delta in learning_deltas
        if delta["classification"] == "operational_failure"
    ]
    recognized = [receipt for receipt in reducer_receipts if receipt["learning_recognized"]]
    valid_as_research = execution_mode == "research" and bool(recognized)
    cycle = {
        "version": 2 if execution_mode == "research" else 1,
        "compatibility_contract_version": (
            COMPATIBILITY_CONTRACT_VERSION if execution_mode == "research" else None
        ),
        "run_id": run_state["run_id"],
        "cycle_id": cycle_id,
        "cycle_index": cycle_index,
        "target_id": run_state["target_id"],
        "created_utc": started_utc,
        "completed_utc": utc_now(),
        "execution_mode": cycle_mode,
        "research_seconds_target": target_seconds,
        "research_seconds_elapsed": round(elapsed, 3),
        "valid_as_research_cycle": valid_as_research,
        "research_validity_basis": {
            "policy": "semantic_receipts_not_elapsed_time",
            "recognized_learning_delta_ids": [receipt["delta_id"] for receipt in recognized],
            "operator_receipt_ids": [receipt["receipt_id"] for receipt in operator_receipts],
            "transaction_commit_id": transaction_receipt["commit_id"],
            "truth_status_boundary": "Semantic mutation is not proof; every delta remains truth_status=unknown unless separate evidence changes it.",
        },
        # Runtime authority is a sealed capability, not a JSON value. Preserve
        # its detached evidence in the report after the authorized actions run.
        "canonical_theory_gate": authorization_projection(theory_gate) if execution_mode == "research" else theory_gate,
        "canonical_action_reservation": theory_reservation,
        "canonical_reservation_terminal": reservation_terminal,
        "branch_execution_records": branch_records,
        "operator_receipts": operator_receipts,
        "learning_deltas": learning_deltas,
        "learning_reducer_receipts": reducer_receipts,
        "transaction_receipt": transaction_receipt,
        "successful_branch_ids": successful_branch_ids,
        "operational_failure_branch_ids": operational_failure_branch_ids,
        "parallel_execution": {
            "enabled": bool(execution_mode == "research" and branch_engine in {"auto", "api"} and api_parallel_config.get("enabled")),
            "max_workers": int(api_parallel_config.get("max_workers", 1)),
            "request_spacing_seconds": float(api_parallel_config.get("request_spacing_seconds", 0.0)),
            "worker_engine": ("host_model_channel" if _HOST_MODEL.get() else "azure_responses_api") if execution_mode == "research" and branch_engine in {"auto", "api"} else branch_engine,
            "merge_policy": "scheduler_order_single_writer",
            "state_mutation_policy": "one journaled compare-and-swap commit after branch-local validation; failed siblings remain operational deltas",
        },
        "parallel_synthesis": build_parallel_synthesis(
            selected,
            outputs,
            branch_records,
            target_id=run_state["target_id"],
            api_parallel_config=api_parallel_config,
        ),
        "timing_validation": {
            "status": "budget_observation_only",
            "reason": (
                f"Observed {round(elapsed, 3)} seconds under a {target_seconds}-second budget. "
                "Elapsed time neither creates nor validates research learning."
            ),
        },
        "selected_branch_ids": [branch["branch_id"] for branch in selected],
        "scheduler_decisions": decisions,
        "literature_gap_preinvestment": literature_gap_control,
        "artifact_or_stop_control": artifact_stop_control,
        "branch_outputs": outputs,
        "skill_dispatch_trace": dispatch_trace,
        "skill_dispatch_certified": all(row["dispatch_status"] == "certified" for row in dispatch_trace),
        "cycle_learning": (
            f"This {cycle_mode} cycle retained {len(successful_branch_ids)} validated branch packet(s), recognized "
            f"{len(recognized)} semantic mutation(s), and preserved {len(operational_failure_branch_ids)} operational failure(s). "
            "Validated packets use typed branch lemmas with a source object, target object, equation, validity condition, and falsifier; "
            "the reducer records conceptual change without upgrading it to truth. Elapsed time has no epistemic role."
        ),
        "next_cycle_queue": [output["next_experiment"] for output in outputs],
        "validation_handoff": [
            "agentic/scripts/validate_avenue_literature_gap_warrant.py",
            "agentic/scripts/validate_artifact_or_stop_control.py",
            "agentic/scripts/validate_discovery_marathon_cycle.py",
            "agentic/scripts/validate_discovery_marathon_skill_dispatch.py",
            "agentic/scripts/validate_proof_depth_control.py",
            "agentic/scripts/validate_proof_learning_ledger.py",
            "agentic/scripts/validate_proof_lockin_report.py",
        ],
    }
    # The transaction above is authoritative.  These familiar JSON/Markdown
    # files are backward-readable projections and may be rebuilt after a crash.
    write_json(cycle_path(run_state["run_id"], cycle_id), cycle)
    write_markdown(cycle_path(run_state["run_id"], cycle_id).with_suffix(".md"), cycle_markdown(cycle))
    selected_by_id = {branch["branch_id"]: branch for branch in selected}
    outputs_by_id = {output["branch_id"]: output for output in outputs}
    deltas_by_id = {delta["identity"]["branch_id"]: delta for delta in learning_deltas}
    reducer_by_id = {receipt["identity"]["branch_id"]: receipt for receipt in reducer_receipts}
    for branch in branches:
        if branch["branch_id"] in selected_by_id:
            branch_id = branch["branch_id"]
            delta = deltas_by_id[branch_id]
            reducer_receipt = reducer_by_id[branch_id]
            output = outputs_by_id.get(branch_id)
            branch["attempt_count"] = int(branch.get("attempt_count", 0)) + 1
            if reducer_receipt["learning_recognized"]:
                branch["last_new_learning_utc"] = utc_now()
                branch["consecutive_low_learning_cycles"] = 0
            else:
                branch["consecutive_low_learning_cycles"] = int(branch.get("consecutive_low_learning_cycles", 0)) + 1
            authoritative_status = authoritative_branches[branch_id]["status"]
            branch["authoritative_status"] = authoritative_status
            branch["authoritative_branch_generation"] = authoritative_branches[branch_id]["generation"]
            branch["status"] = (
                "stopped"
                if authoritative_status in {"quarantined", "exhausted", "completed", "refuted"}
                else "active"
            )
            branch["authoritative_state_generation"] = transaction_receipt["generation"]
            branch.setdefault("local_memory", []).append(
                {
                    "cycle_id": cycle_id,
                    "learning": (
                        clean_text(output.get("mathematical_learning"))
                        if output is not None
                        else delta["summary"]
                    ),
                    "learning_delta_id": delta["delta_id"],
                    "reducer_receipt_id": reducer_receipt["reducer_receipt_id"],
                    "learning_recognized": reducer_receipt["learning_recognized"],
                    "truth_status": reducer_receipt["truth_status"],
                    "control_decision": (
                        clean_text(output.get("control_decision", {}).get("decision"))
                        if output is not None
                        else "persist_operational_failure"
                    ),
                    "artifact_or_stop_mode": next(
                        (
                            clean_text(decision.get("artifact_or_stop_mode"))
                            for decision in decisions
                            if decision.get("branch_id") == branch["branch_id"]
                        ),
                        "",
                    ),
                }
            )
        write_json(ROOT / branch["local_memory_path"], branch)
    run_state["cycle_count"] = cycle_index
    run_state["research_cycle_count"] = int(run_state.get("research_cycle_count", 0)) + (1 if cycle["valid_as_research_cycle"] else 0)
    run_state["synthetic_cycle_count"] = int(run_state.get("synthetic_cycle_count", 0)) + (0 if cycle["valid_as_research_cycle"] else 1)
    run_state["status"] = "running"
    run_state["updated_utc"] = utc_now()
    run_state["active_branch_ids"] = [branch["branch_id"] for branch in selected]
    run_state["authoritative_state_generation"] = transaction_receipt["generation"]
    run_state["authoritative_commit_id"] = transaction_receipt["commit_id"]
    if theory_gate.get("authoritative") is True and theory_reservation is None:
        raise BranchExecutionError(
            "authoritative legacy investment completed without a canonical action reservation"
        )
    write_json(run_dir(run_state["run_id"]) / "run_state.json", run_state)
    write_active_run_pointers(run_state)
    return cycle


def has_proof_depth_record(value: Any) -> bool:
    """Detect even malformed records so report rebuilding cannot skip them."""
    if isinstance(value, dict):
        if "proof_depth_control" in value or "proof_depth_packets" in value:
            return True
        return any(has_proof_depth_record(item) for item in value.values())
    if isinstance(value, list):
        return any(has_proof_depth_record(item) for item in value)
    return False


def report_rebuild_commands(run_id: str, target_id: str) -> list[list[str]]:
    """Return builders/validators whose read and write sets stay on one target/run."""

    validate_identifier(run_id, "run_id")
    validate_identifier(target_id, "target_id")
    target_slug = slugify(target_id)
    commands: list[list[str]] = []
    if target_id == PVSNP_TARGET_ID:
        commands.append(
            [sys.executable, "agentic/scripts/build_pvsnp_inference_quality_report.py"]
        )
    # Reports span historical cycles that predate proof-depth packets. Validate
    # every recorded packet, without requiring old history to claim evidence it
    # never produced. New branch admission remains in run_one_cycle/validators.
    cycle_files = [
        path for path in sorted((run_dir(run_id) / "cycles").glob("*.json"))
        if has_proof_depth_record(load_json_object(path))
    ]
    if cycle_files:
        commands.append(
            [
                sys.executable,
                "agentic/scripts/validate_proof_depth_control.py",
                *[str(path) for path in cycle_files],
            ]
        )
    commands.extend(
        [
            [
                sys.executable,
                "agentic/scripts/build_proof_learning_ledger.py",
                "--target-id",
                target_id,
                "--run-id",
                run_id,
            ],
            [
                sys.executable,
                "agentic/scripts/validate_proof_learning_ledger.py",
                str(
                    ROOT
                    / "agentic/reports/proof_learning/targets"
                    / target_slug
                    / "latest.json"
                ),
            ],
        ]
    )
    if target_id == YM_TARGET_ID:
        commands.extend(
            [
                [sys.executable, "agentic/scripts/build_blocker_signature_report.py"],
                [sys.executable, "agentic/scripts/validate_artifact_or_stop_control.py"],
            ]
        )
    commands.extend(
        [
            [
                sys.executable,
                "agentic/scripts/build_proof_lockin_report.py",
                "--target-id",
                target_id,
            ],
            [
                sys.executable,
                "agentic/scripts/validate_proof_lockin_report.py",
                str(
                    ROOT
                    / "agentic/reports/proof_lockin/targets"
                    / target_slug
                    / "latest.json"
                ),
            ],
            [
                sys.executable,
                "agentic/scripts/build_discovery_marathon_report.py",
                "--run-id",
                run_id,
                "--target-id",
                target_id,
            ],
            [
                sys.executable,
                "agentic/scripts/generate_discovery_marathon_html.py",
                "--run-id",
                run_id,
                "--target-id",
                target_id,
            ],
        ]
    )
    return commands


def rebuild_reports(run_id: str, target_id: str) -> None:
    for command in report_rebuild_commands(run_id, target_id):
        subprocess.run(command, cwd=ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id")
    parser.add_argument("--target", default=None)
    parser.add_argument("--hours", type=float, default=6)
    parser.add_argument("--cycle-minutes", type=int, default=30)
    parser.add_argument("--max-cycles", type=int, default=1)
    parser.add_argument("--max-active-branches", type=int)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--execution-mode", choices=["research", "smoke"], default="research")
    parser.add_argument("--min-cycle-seconds", type=int, help="Minimum elapsed seconds required for a research cycle. Defaults to cycle_minutes * 60.")
    parser.add_argument("--branch-engine", choices=["auto", "api", "codex", "internal"], default="auto")
    parser.add_argument("--api-key-config", default=None, help="Path to config/api_keys.json or config/api_keys.env. Defaults to config/api_keys.json, then config/api_keys.env, then environment.")
    parser.add_argument("--parallel-branches", action="store_true", help="Run independent Azure/API branch agents concurrently; state merge remains serialized.")
    parser.add_argument("--api-max-workers", type=int, help="Maximum concurrent API branch agents. Also supported by AZURE_OPENAI_MAX_CONCURRENT_BRANCHES.")
    parser.add_argument("--api-request-spacing-seconds", type=float, help="Optional deterministic launch spacing between API branch workers.")
    parser.add_argument(
        "--canonical-theory-cycle",
        type=Path,
        help=(
            "Exact canonical discovery-cycle result projection. Required in research mode; "
            "latest/current aliases and uncommitted projections are rejected."
        ),
    )
    parser.add_argument(
        "--canonical-theory-state-root",
        type=Path,
        default=DEFAULT_CANONICAL_THEORY_STATE_ROOT,
        help=(
            "Canonical theory transaction root (kept separate from legacy marathon state). "
            "Defaults to agentic/state/canonical_discovery_transactions."
        ),
    )
    parser.add_argument("--canonical-authorization-basis-digest")
    parser.add_argument("--canonical-source-present-decision-digest")
    parser.add_argument("--canonical-schedule-id")
    parser.add_argument("--allow-large-research-run", action="store_true", help="Permit more than one research cycle in a single invocation.")
    parser.add_argument(
        "--skip-report-rebuild",
        action="store_true",
        help="Leave report building to an outer governed job so report failures remain distinct.",
    )
    args = parser.parse_args()
    if args.execution_mode == "research":
        missing_bindings = [
            flag
            for flag, value in (
                ("--target", args.target),
                ("--run-id", args.run_id),
                ("--canonical-theory-cycle", args.canonical_theory_cycle),
            )
            if not value
        ]
        if missing_bindings:
            parser.error(
                "research mode requires exact canonical bindings: "
                + ", ".join(missing_bindings)
            )
    initial_branches: list[dict[str, Any]] | None = None
    if args.resume or args.run_id:
        _, run_state = load_run_state(args.run_id, target_id=args.target if args.resume and not args.run_id else None)
    else:
        run_state, branches = build_initial_state(args.target or DEFAULT_TARGET_ID, args.hours, args.cycle_minutes, args.max_active_branches or 3, args.run_id)
        initial_branches = branches
        if not args.dry_run:
            persist_run(run_state, branches)
    if not run_state:
        print("No discovery marathon exists; initialize one first or omit --resume.")
        return 1
    if clean_text(run_state.get("target_id")) != clean_text(args.target or run_state.get("target_id")):
        fail("loaded run target does not match --target")
    if args.run_id and clean_text(run_state.get("run_id")) != clean_text(args.run_id):
        fail("loaded run identity does not match --run-id")
    if args.dry_run:
        branch_source = initial_branches if initial_branches is not None else load_branches(run_state)
        selected_preview, decision_preview = select_branches(branch_source, args.max_active_branches or run_state.get("max_active_branches", 3))
        planned = [branch["branch_id"] for branch in selected_preview]
        print({"planned_run_id": run_state["run_id"], "planned_branch_ids": planned, "scheduler_decisions": decision_preview, "dry_run": True})
        return 0
    cycles_to_run = max(1, args.max_cycles)
    if args.execution_mode == "research" and cycles_to_run > 1 and not args.allow_large_research_run:
        fail("research mode runs one cycle per invocation unless --allow-large-research-run is explicit; use --execution-mode smoke for fast smoke packets")
    if args.execution_mode == "research" and args.branch_engine == "internal":
        fail("internal branch engine is not allowed in research mode")
    last_cycle = None
    for _ in range(cycles_to_run):
        try:
            last_cycle = run_one_cycle(
                run_state,
                args.max_active_branches,
                execution_mode=args.execution_mode,
                min_cycle_seconds=args.min_cycle_seconds,
                branch_engine=args.branch_engine,
                api_key_config=args.api_key_config,
                api_max_workers=args.api_max_workers,
                parallel_branches=args.parallel_branches,
                api_request_spacing_seconds=args.api_request_spacing_seconds,
                canonical_theory_cycle=args.canonical_theory_cycle,
                canonical_theory_state_root=args.canonical_theory_state_root,
                canonical_authorization_basis_digest=args.canonical_authorization_basis_digest,
                canonical_source_present_decision_digest=args.canonical_source_present_decision_digest,
                canonical_schedule_id=args.canonical_schedule_id,
            )
        except BranchExecutionError as exc:
            fail(f"{exc}; record={json.dumps(exc.record, sort_keys=True)}")
    # A CLI invocation is only a bounded slice of an extendable marathon.
    # Completion of this subprocess must not mark the whole run as exhausted,
    # especially when a time-boxed job wrapper is about to launch more cycles.
    pause_receipt = commit_run_status_transition(
        marathon_transaction_store(run_state),
        status="paused",
        cause_id=last_cycle["cycle_id"] if last_cycle else stable_identifier("empty-run", run_state["run_id"]),
    )
    run_state["status"] = "paused"
    run_state["updated_utc"] = utc_now()
    run_state["authoritative_state_generation"] = pause_receipt["generation"]
    run_state["authoritative_commit_id"] = pause_receipt["commit_id"]
    write_json(run_dir(run_state["run_id"]) / "run_state.json", run_state)
    write_active_run_pointers(run_state)
    if int(run_state.get("cycle_count", 0)) and int(run_state.get("cycle_count", 0)) % 3 == 0:
        subprocess.run([sys.executable, "agentic/scripts/run_marathon_deep_review.py", "--run-id", run_state["run_id"]], cwd=ROOT, check=True)
    if not args.skip_report_rebuild:
        rebuild_reports(run_state["run_id"], run_state["target_id"])
    print(f"Ran {cycles_to_run} cycle(s) for {run_state['run_id']}: {last_cycle['cycle_id'] if last_cycle else 'none'}")
    return 0 if last_cycle and last_cycle.get("successful_branch_ids") else 2


if __name__ == "__main__":
    raise SystemExit(main())

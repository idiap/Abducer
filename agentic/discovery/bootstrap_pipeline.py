# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Initialize one fresh research run through the existing canonical transaction.

Initialization acquires literature, authors conjectures and reflection, and runs
the real operators and validators. The first wave produces a literature-input
manifest. A second deterministic wave consumes that committed projection using
the same frozen model content, without paying for or claiming another opinion.
Only the canonical cycle may write the initial theory generation.
"""
from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, Mapping

from .bootstrap_adjudication import adjudication_envelope
from .bootstrap_authoring import (
    author_charter, author_blind_proposals, author_source_assessment, author_rebase,
    high_risk_charter, compile_proposals, target_context,
)
from .bootstrap_dispatch import BootstrapDispatcher, POLICY_OPERATOR, REALIZATION_OPERATOR
from .bootstrap_literature import acquire_current_literature
from .bootstrap_production import ProductionLedger, acquisition_bundle
from .bootstrap_reflection import author_maturation, author_systems, author_reflection_round, compile_system, version_synthesis
from .bootstrap_routing import execute_source_routing
from .contracts import ContractError, canonical_digest, utc_now
from .cycle import run_canonical_discovery_cycle
from .ledger import initial_state
from .model_author import ModelAuthor, write_record


def reflection_envelope(*, charter_record, snapshot, assimilation_path, assessment,
                        portfolio, parallel, systems, rounds, identity, receipt_ids):
    """Combine actual authored concepts with the source-owned literature bindings."""
    charter = charter_record["value"]
    mappings = assessment["value"]["assessments"]
    questions = [text for row in mappings if row["relevance"] in {"direct", "adjacent"}
                 for text in row["usable_for"]]
    if not questions:
        raise ContractError("initialization needs a literature-grounded research question")
    return {**identity, "branch_id": "root", "prior_conceptual_state_ref": "state:0",
        **copy.deepcopy(charter), "generation_mode": "operator_generated",
        "literature_basis": {"selected_snapshot_id": snapshot["snapshot_id"],
            "snapshot_target_id": snapshot["target_id"], "selected_snapshot_digest": snapshot["content_digest"],
            "search_completed_utc": snapshot["search_completed_at"], "freshness_status": "current",
            "search_receipt_ids": [row["lane_id"] for row in snapshot["lane_receipts"]],
            "assimilation_packet_ref": assimilation_path,
            "source_to_theory_delta_summary": [row["reason"] for row in mappings if row["relevance"] in {"direct", "adjacent"}],
            "literature_generated_questions": questions, "coverage_limitations": list(snapshot["coverage_limits"]),
            "superseded_snapshot_ids": []},
        "high_risk_portfolio": portfolio, "parallel_portfolio": parallel,
        "conceptual_systems": systems, "reflection_rounds": rounds,
        "operator_receipt_ids": receipt_ids}


class InitializationWave:
    """Run the same source operators for production and later canonical intake."""

    def __init__(self, *, workspace, root, target_id, run_id, author, capture,
                 acquisition_digest, theory_digest, charter_record, assessment,
                 blind, rebase, cache, ledger=None, projection=None):
        self.workspace, self.root = workspace, root
        self.identity = {"target_id": target_id, "run_id": run_id, "state_version": 0}
        self.author, self.capture = author, capture
        self.acquisition_digest, self.theory_digest = acquisition_digest, theory_digest
        self.charter_record, self.assessment = charter_record, assessment
        self.blind, self.rebase, self.cache, self.ledger = blind, rebase, cache, ledger
        self.dispatcher = BootstrapDispatcher(workspace=workspace, root=root / "operators",
                                             target_id=target_id, run_id=run_id)
        self.dispatcher.projection = projection
        self.roles = {}

    def _dispatch(self, role, operator, kind, envelope, *, parameters=None):
        value, receipt, path = self.dispatcher.dispatch(operator, kind, envelope, parameters=parameters)
        self.roles[role] = path
        return value, receipt

    def _stage(self, name, inputs, producer, **kwargs):
        return self.ledger.run(name, inputs, producer, **kwargs) if self.ledger else producer()[0]

    def run(self):
        d = self.dispatcher
        def publish_policy(policy):
            self._dispatch("source_routing_pre_map_policy", POLICY_OPERATOR, "literature_assimilation", {
                "authority_artifact": policy, "validation_inputs": {
                    "authority": policy["acquisition_authority"], "snapshot": self.snapshot,
                    "acquisition_producer_receipt": policy["acquisition_completion"],
                    "algorithm_contracts": policy["algorithm_contracts"]}}, parameters={
                    "producer_role": "source_routing_pre_map_policy", "artifact_id": policy["policy_id"],
                    "artifact_digest": canonical_digest(policy)})
        def assimilate(snapshot, mappings, policy):
            output, _ = self._dispatch("literature_assimilation", "frontier-literature-assimilator", "literature_assimilation", {
                "snapshot": snapshot, "theory_mappings": mappings, "source_routing_pre_map_policy": policy})
            return output
        from .bootstrap_literature import reopen_acquisition
        self.snapshot = reopen_acquisition(self.capture, expected_digest=self.acquisition_digest,
            target_id=self.identity["target_id"], run_id=self.identity["run_id"], theory_state_digest=self.theory_digest)
        self.roles["literature_snapshot"] = (self.capture / "snapshot.json").relative_to(self.workspace).as_posix()
        routing = execute_source_routing(acquisition_root=self.capture, acquisition_digest=self.acquisition_digest,
            target_id=self.identity["target_id"], run_id=self.identity["run_id"], theory_state_digest=self.theory_digest,
            assessment=self.assessment, root=self.root / "source-routing", publish_policy=publish_policy,
            assimilation_operator=assimilate, production_ledger=self.ledger)
        policy, realization = routing["policy"], routing["realization"]
        self._dispatch("source_routing_realization", REALIZATION_OPERATOR, "literature_assimilation", {
            "authority_artifact": realization, "validation_inputs": {
                "policy": policy, "authority": routing["authority"], "snapshot": self.snapshot,
                "acquisition_producer_receipt": routing["acquisition_receipt"],
                "algorithm_contracts": policy["algorithm_contracts"],
                "validated_warrants": routing["warrants"]["validated_warrants"], "claim_mappings": routing["mappings"],
                "assimilation": routing["assimilation"], "stage_receipts": routing["stage_receipts"]}}, parameters={
                "producer_role": "source_routing_realization", "artifact_id": realization["realization_id"],
                "artifact_digest": canonical_digest(realization)})
        d.policy, d.realization = policy, realization
        charter = high_risk_charter(self.identity["target_id"], self.theory_digest, self.charter_record)
        proposals = compile_proposals(charter=charter, blind=self.blind, rebase=self.rebase)
        high_risk_input = {"charter": charter, "literature_snapshot": self.snapshot,
                          "assimilation_packet": routing["assimilation"], "authored_proposals": proposals}
        portfolio = self._stage("high_risk_input", {**high_risk_input, "blind_authorship": self.blind,
            "source_rebase_authorship": self.rebase},
            lambda: self._dispatch("high_risk_portfolio", "high-risk-hypothesis-forger", "hypothesis", high_risk_input),
            schema="high_risk_hypothesis_portfolio.schema.json", reason_codes=["authored_fallback_not_proposal_field_free"])
        self.portfolio = portfolio
        if "maturation" not in self.cache:
            self.cache["maturation"] = author_maturation(self.author, portfolio=portfolio,
                                                       snapshot=self.snapshot, assessment=self.assessment)
        maturation = self.cache["maturation"]
        parallel, _ = self._dispatch("parallel_portfolio", "parallel-hypothesis-portfolio", "hypothesis", {
            "high_risk_portfolio": portfolio, **maturation})
        if "parent" not in self.cache:
            articulated = author_systems(self.author, charter=charter, portfolio=portfolio, parallel=parallel)
            systems = [compile_system(row) for row in articulated["value"]["systems"]]
            rounds, records = [], [articulated]
            for index in range(1, 3):
                record = author_reflection_round(self.author, stage_id=f"parent-reflection-{index}",
                                                systems=systems, rounds=rounds, charter=charter)
                systems = [compile_system(row) for row in record["value"]["systems"]]
                rounds.append(record["value"]["round"])
                records.append(record)
            self.cache["parent"] = {"systems": systems, "rounds": rounds, "authoring_records": records}
        reflected = self.cache["parent"]
        request = reflection_envelope(charter_record=self.charter_record, snapshot=self.snapshot,
            assimilation_path=self.roles["literature_assimilation"], assessment=self.assessment,
            portfolio=portfolio, parallel=parallel, systems=reflected["systems"], rounds=reflected["rounds"],
            identity=self.identity, receipt_ids=[row["receipt_id"] for row in d.receipts])
        parent = self._stage("parent_reflection", {"reflection_request": request, "authoring": reflected},
            lambda: self._dispatch("parent_reflection", "reflective-conceptual-discovery", "theory", request),
            schema="reflective_conceptual_discovery_packet.schema.json")
        parent_receipt = d.receipts[-1]
        envelope = adjudication_envelope(author=self.author, stage_id="parent-conceptual-adjudication",
            packet=parent, proposer_receipt=parent_receipt, snapshot=self.snapshot, portfolio=portfolio)
        parent_evidence = self._stage("parent_conceptual_adjudication", {"parent_reflection": parent, "panel_input": envelope},
            lambda: self._dispatch("parent_conceptual_adjudication", "blind-conceptual-preference-adjudicator", "evaluation", envelope),
            schema="conceptual_adjudication_evidence.schema.json")
        if "synthesis" not in self.cache:
            record = author_reflection_round(self.author, stage_id="synthesis-reflection", systems=reflected["systems"],
                rounds=reflected["rounds"], charter=charter, critique=parent_evidence)
            self.cache["synthesis"] = version_synthesis(reflected["systems"], reflected["rounds"], record)
        revised = self.cache["synthesis"]
        synthesis_input = {**request, "conceptual_systems": revised["systems"], "reflection_rounds": revised["rounds"],
            "prior_reflective_packet": parent, "previous_evidence": parent_evidence,
            "revise_after_adjudication": True, "request_theory_support_probe": False}
        synthesis = self._stage("theory_only_synthesis", {"parent_reflection": parent,
            "parent_conceptual_adjudication": parent_evidence, "synthesis_input": synthesis_input,
            "authoring": revised}, lambda: self._dispatch("synthesis_reflection", "reflective-theory-synthesizer", "theory", synthesis_input),
            schema="reflective_conceptual_discovery_packet.schema.json")
        envelope = adjudication_envelope(author=self.author, stage_id="synthesis-conceptual-adjudication",
            packet=synthesis, proposer_receipt=d.receipts[-1], snapshot=self.snapshot, portfolio=portfolio,
            previous_evidence=parent_evidence)
        self._stage("synthesis_conceptual_adjudication", {"theory_only_synthesis": synthesis,
            "parent_conceptual_adjudication": parent_evidence, "panel_input": envelope},
            lambda: self._dispatch("synthesis_conceptual_adjudication", "blind-conceptual-preference-adjudicator", "evaluation", envelope),
            schema="conceptual_adjudication_evidence.schema.json")
        self.roles["reflective_packets"] = [self.roles.pop("parent_reflection"), self.roles.pop("synthesis_reflection")]
        return self


def initialize_canonical_theory(*, workspace: Path, root: Path, target_id: str, run_id: str,
                                model_id: str, completion, public_fetch, event=None) -> dict[str, Any]:
    """Acquire, author, validate and atomically commit generation one for a new run."""
    workspace, root = workspace.resolve(), root.resolve()
    root.relative_to(workspace)
    root.mkdir(parents=True, exist_ok=False)
    target = target_context(target_id)
    theory_digest = canonical_digest(initial_state(target_id, run_id))
    author = ModelAuthor(root=root / "authorship", target_id=target_id, run_id=run_id,
                         model_id=model_id, completion=completion, event=event)
    charter_record = author_charter(author)
    charter = high_risk_charter(target_id, theory_digest, charter_record)
    blind = author_blind_proposals(author, charter)
    capture = root / "acquisition"
    acquired = acquire_current_literature(target_id=target_id, run_id=run_id, theory_state_digest=theory_digest,
        topic=target["topic"], root=capture, public_fetch=public_fetch)
    assessment = author_source_assessment(author, acquired["snapshot"])
    rebase = author_rebase(author, snapshot=acquired["snapshot"], charter=charter, blind=blind, assessment=assessment)
    ledger = ProductionLedger(workspace=workspace, root=root / "production-manifest", target_id=target_id,
                              run_id=run_id, source_bundle=acquisition_bundle(capture))
    cache = {}
    arguments = dict(workspace=workspace, target_id=target_id, run_id=run_id, author=author,
        capture=capture, acquisition_digest=acquired["manifest"]["content_digest"], theory_digest=theory_digest,
        charter_record=charter_record, assessment=assessment, blind=blind, rebase=rebase, cache=cache)
    InitializationWave(root=root / "production", ledger=ledger, **arguments).run()
    bundle, bundle_path = ledger.finish()
    write_record(root / "frozen-authored-content.json", cache)
    wave = InitializationWave(root=root / "canonical-inputs", projection=bundle["semantic_consumer_projection"], **arguments).run()
    wave.roles["literature_production_input_bundle"] = bundle_path
    state_root = root / "theory-state"
    cycle = run_canonical_discovery_cycle(workspace=workspace, state_root=state_root,
        target_id=target_id, run_id=run_id, state_version=0, operator_requests=wave.dispatcher.requests,
        operator_receipts=wave.dispatcher.receipts, artifact_roles=wave.roles,
        evaluator_identity="bootstrap-canonical-contract-evaluator", idempotency_key="initialization-generation-one",
        present_use_at=utc_now())
    cycle_path = root / "canonical-cycle.json"
    write_record(cycle_path, cycle)
    hypotheses = {row["hypothesis_id"]: row for row in wave.portfolio["hypotheses"]}
    seeds = {"target_id": target_id, "run_id": run_id, "canonical_cycle_digest": canonical_digest(cycle),
        "source_portfolio": wave.portfolio, "branches": [{"binding": row, "hypothesis": hypotheses[row["hypothesis_id"]]}
            for row in cycle["identity_map"]["branch_bindings"]]}
    seed_path = root / "marathon-branch-seeds.json"
    write_record(seed_path, seeds)
    return {"canonical_theory_cycle": cycle_path.relative_to(workspace).as_posix(),
            "canonical_theory_state_root": state_root.relative_to(workspace).as_posix(),
            "canonical_branch_seeds": seed_path.relative_to(workspace).as_posix(),
            "target_id": target_id, "run_id": run_id, "scientific_truth_verified": False}

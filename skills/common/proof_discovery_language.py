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

"""Shared specification for a proof-discovery language."""

from __future__ import annotations

from typing import Any


def _latex_escape(value: Any) -> str:
    text = " ".join(str(value or "").split())
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return text


def _clean_text(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def _ensure_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _ensure_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _unique_texts(values: list[Any]) -> list[str]:
    rows: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = _clean_text(value)
        if not text or text in seen:
            continue
        seen.add(text)
        rows.append(text)
    return rows


def _anchor(*, anchor_id: str, label: str, content: str, anchor_type: str, source: str = "") -> dict[str, Any] | None:
    if not _clean_text(label) and not _clean_text(content):
        return None
    return {
        "anchor_id": _clean_text(anchor_id),
        "label": _clean_text(label),
        "content": _clean_text(content),
        "anchor_type": _clean_text(anchor_type),
        "source": _clean_text(source),
    }


def _decision_gate(*, title: str, criterion: str, action: str) -> dict[str, Any] | None:
    if not _clean_text(title) and not _clean_text(criterion) and not _clean_text(action):
        return None
    return {
        "title": _clean_text(title),
        "criterion": _clean_text(criterion),
        "action": _clean_text(action),
    }


def _compact_dict_rows(rows: list[dict[str, Any] | None]) -> list[dict[str, Any]]:
    return [row for row in rows if isinstance(row, dict) and any(_clean_text(value) for value in row.values())]


def _base_program(
    *,
    program_id: str,
    kind: str,
    stage: str,
    kb_ref: str,
    title: str,
    anchors: list[dict[str, Any]],
    target: dict[str, Any],
    tensions: list[str],
    nexus: dict[str, Any],
    bridge_object: dict[str, Any],
    positive_route: dict[str, Any],
    negative_route: dict[str, Any],
    proof_debt: list[str],
    decision_gates: list[dict[str, Any]],
    control_objects: list[str],
) -> dict[str, Any]:
    return {
        "metadata": {
            "program_id": _clean_text(program_id),
            "kind": _clean_text(kind),
            "stage": _clean_text(stage),
            "kb_ref": _clean_text(kb_ref),
            "title": _clean_text(title),
        },
        "anchors": anchors,
        "target": {
            "label": _clean_text(target.get("label")),
            "statement": _clean_text(target.get("statement")),
            "target_id": _clean_text(target.get("target_id")),
        },
        "tensions": _unique_texts(tensions),
        "conceptual_nexus": {
            "label": _clean_text(nexus.get("label")),
            "summary": _clean_text(nexus.get("summary")),
            "linked_items": _unique_texts(_ensure_list(nexus.get("linked_items"))),
        },
        "bridge_object": {
            "label": _clean_text(bridge_object.get("label")),
            "kind": _clean_text(bridge_object.get("kind")),
            "invariant": _clean_text(bridge_object.get("invariant")),
            "admissibility": _clean_text(bridge_object.get("admissibility")),
        },
        "positive_route": {
            "claim": _clean_text(positive_route.get("claim")),
            "route_lemma": _clean_text(positive_route.get("route_lemma")),
            "strategy": _clean_text(positive_route.get("strategy")),
            "steps": _unique_texts(_ensure_list(positive_route.get("steps"))),
        },
        "negative_route": {
            "mode": _clean_text(negative_route.get("mode")),
            "claim": _clean_text(negative_route.get("claim")),
            "contradiction_target": _clean_text(negative_route.get("contradiction_target")),
            "forbidden_outcome": _clean_text(negative_route.get("forbidden_outcome")),
            "impossibility_claim": _clean_text(negative_route.get("impossibility_claim")),
        },
        "proof_debt": _unique_texts(proof_debt),
        "decision_gates": _compact_dict_rows(decision_gates),
        "control_objects": _unique_texts(control_objects),
    }


def serialize_queue_entry_as_pdl(entry: dict[str, Any]) -> dict[str, Any]:
    """Serialize a proof-queue entry as a native proof-discovery language program."""

    delta = _ensure_dict(entry.get("statement_delta"))
    negative = _ensure_dict(entry.get("negative_reasoning_program"))
    heuristic = _ensure_dict(negative.get("heuristic"))
    contract = _ensure_dict(entry.get("interpretability_contract"))
    anchors = _compact_dict_rows(
        [
            _anchor(
                anchor_id="source-statement",
                label=entry.get("source_statement_id", ""),
                content=entry.get("source_excerpt", ""),
                anchor_type="source-theorem",
                source="KB",
            ),
            _anchor(
                anchor_id="target-statement",
                label=entry.get("target_statement_id", ""),
                content=entry.get("target_excerpt", ""),
                anchor_type="target-theorem",
                source="KB",
            ),
        ]
    )
    tensions = [
        delta.get("model_shift"),
        delta.get("threshold_shift"),
        delta.get("consequence_shift"),
        delta.get("source_claim_focus") and delta.get("target_claim_focus") and (
            f"Route focus: {delta.get('source_claim_focus')} -> {delta.get('target_claim_focus')}"
        ),
        entry.get("missing_route_lemma") and f"Missing route lemma: {entry.get('missing_route_lemma')}",
        entry.get("failure_diagnosis"),
        entry.get("negative_route"),
    ]
    return _base_program(
        program_id=_clean_text(entry.get("queue_id") or entry.get("queue_key")),
        kind="queue-entry",
        stage="discovery-to-prove",
        kb_ref=_clean_text(entry.get("kb_ref")),
        title=_clean_text(entry.get("title") or entry.get("conjecture_statement") or entry.get("claim_text")),
        anchors=anchors,
        target={
            "label": entry.get("title") or entry.get("target_statement_id"),
            "statement": entry.get("conjecture_statement") or entry.get("claim_text"),
            "target_id": entry.get("target_statement_id"),
        },
        tensions=tensions,
        nexus={
            "label": entry.get("bridge_id") or entry.get("title"),
            "summary": entry.get("route_synopsis") or entry.get("conditional_proposition"),
            "linked_items": [
                entry.get("bridge_id"),
                entry.get("candidate_object"),
                entry.get("preserved_invariant"),
            ],
        },
        bridge_object={
            "label": entry.get("candidate_object"),
            "kind": entry.get("carrier_kind"),
            "invariant": entry.get("preserved_invariant"),
            "admissibility": entry.get("conditional_proposition"),
        },
        positive_route={
            "claim": entry.get("conditional_proposition") or entry.get("route_synopsis") or entry.get("claim_text"),
            "route_lemma": entry.get("missing_route_lemma"),
            "strategy": entry.get("proof_strategy_family"),
            "steps": _ensure_list(entry.get("candidate_lemmas")),
        },
        negative_route={
            "mode": negative.get("negative_mode"),
            "claim": negative.get("negated_claim") or entry.get("negative_route"),
            "contradiction_target": negative.get("contradiction_target"),
            "forbidden_outcome": negative.get("forbidden_outcome") or entry.get("failure_diagnosis"),
            "impossibility_claim": entry.get("impossibility_conjecture") or negative.get("impossibility_claim_template"),
        },
        proof_debt=[
            *_ensure_list(entry.get("proof_obligations")),
            *_ensure_list(entry.get("candidate_lemmas")),
            entry.get("missing_route_lemma"),
        ],
        decision_gates=[
            _decision_gate(
                title="Exploration policy",
                criterion=entry.get("exploration_policy"),
                action="Keep, revise, or defer this route according to the current queue policy.",
            ),
            _decision_gate(
                title="Negative-route heuristic",
                criterion=heuristic.get("decision") or negative.get("negative_mode"),
                action=heuristic.get("decision_rule") or "Decide whether constructive and impossibility reasoning run in parallel.",
            ),
            _decision_gate(
                title="LLM interpretability gate",
                criterion=contract.get("status"),
                action=contract.get("summary"),
            ),
        ],
        control_objects=["kb", "mathlib", "proof_queue"],
    )


def serialize_discovery_branch_as_pdl(branch: dict[str, Any]) -> dict[str, Any]:
    """Serialize a discovery branch or branch dossier as a PDL discovery program."""

    framework_gate = _ensure_dict(branch.get("external_framework_search"))
    linked_queue_ids = _ensure_list(branch.get("linked_queue_ids"))
    linked_families = _ensure_list(branch.get("linked_breakthrough_families"))
    linked_obstructions = _ensure_list(branch.get("linked_obstruction_classes"))
    anchors = _compact_dict_rows(
        [
            _anchor(
                anchor_id=f"queue:{queue_id}",
                label=queue_id,
                content=f"Blocked or active route linked to discovery branch `{_clean_text(branch.get('branch_id'))}`.",
                anchor_type="queue-frontier",
                source="Proof queue",
            )
            for queue_id in linked_queue_ids
        ]
        + [
            _anchor(
                anchor_id="branch-target",
                label=branch.get("target_id"),
                content=branch.get("target_label"),
                anchor_type="discovery-target",
                source="Discovery routing",
            )
        ]
    )
    tensions = [
        *_unique_texts(linked_obstructions),
        branch.get("required_move") and f"Required move: {branch.get('required_move')}",
        branch.get("abstraction_required") and f"Abstraction required: {branch.get('abstraction_required')}",
        branch.get("minimal_theorem_shape") and f"Minimal theorem shape: {branch.get('minimal_theorem_shape')}",
    ]
    return _base_program(
        program_id=_clean_text(branch.get("branch_id")),
        kind="discovery-branch",
        stage="discovery",
        kb_ref=_clean_text(branch.get("kb_ref")),
        title=_clean_text(branch.get("target_label") or branch.get("branch_id")),
        anchors=anchors,
        target={
            "label": branch.get("target_label"),
            "statement": branch.get("minimal_theorem_shape") or branch.get("user_task"),
            "target_id": branch.get("target_id"),
        },
        tensions=tensions,
        nexus={
            "label": branch.get("target_label") or branch.get("target_id"),
            "summary": branch.get("rationale") or branch.get("spawn_reason"),
            "linked_items": [*linked_families, *linked_obstructions],
        },
        bridge_object={
            "label": branch.get("abstraction_required") or branch.get("target_label"),
            "kind": branch.get("layer_kind"),
            "invariant": "",
            "admissibility": branch.get("required_move"),
        },
        positive_route={
            "claim": branch.get("minimal_theorem_shape") or branch.get("user_task"),
            "route_lemma": branch.get("required_move"),
            "strategy": branch.get("layer_kind"),
            "steps": _ensure_list(branch.get("sample_theorem_targets")),
        },
        negative_route={
            "mode": "branch-obstruction",
            "claim": "Avoid anti-patterns and branch-local dead ends while sharpening the theorem shape.",
            "contradiction_target": "",
            "forbidden_outcome": "; ".join(_unique_texts(_ensure_list(branch.get("anti_patterns")))),
            "impossibility_claim": "",
        },
        proof_debt=[
            *_ensure_list(branch.get("required_questions")),
            *_ensure_list(branch.get("expected_deliverables")),
        ],
        decision_gates=[
            _decision_gate(
                title="Branch stop criteria",
                criterion="; ".join(_unique_texts(_ensure_list(branch.get("stop_criteria")))),
                action="Stop or re-route when the branch fails to produce a theorem-shaped gain.",
            ),
            _decision_gate(
                title="External framework search",
                criterion=framework_gate.get("mode") if framework_gate.get("recommended") else "local-first",
                action=framework_gate.get("justification") or "Use local material first and browse only when the foundation search gate opens.",
            ),
        ],
        control_objects=["kb", "mathlib", "proof_queue", "discovery_branch_queue"],
    )


def serialize_proof_attempt_as_pdl(attempt: dict[str, Any]) -> dict[str, Any]:
    """Serialize a proof attempt dossier as a native PDL program."""

    metadata = _ensure_dict(attempt.get("metadata"))
    target = _ensure_dict(attempt.get("target"))
    local_context = _ensure_dict(attempt.get("local_context"))
    proof_attempt = _ensure_dict(attempt.get("proof_attempt"))
    web_gate = _ensure_dict(attempt.get("web_search_gate"))
    final_assessment = _ensure_dict(attempt.get("final_assessment"))
    source_hits = [
        _anchor(
            anchor_id=row.get("result_id", ""),
            label=row.get("title", "") or row.get("result_id", ""),
            content=row.get("summary", ""),
            anchor_type="mathlib-result",
            source="InformalMathLib",
        )
        for row in _ensure_list(local_context.get("mathlib_hits"))
        if isinstance(row, dict)
    ]
    anchors = _compact_dict_rows(
        [
            _anchor(
                anchor_id="source-statement",
                label=target.get("source_statement_id", ""),
                content=local_context.get("source_excerpt", ""),
                anchor_type="source-theorem",
                source="KB",
            ),
            _anchor(
                anchor_id="target-statement",
                label=target.get("target_statement_id", ""),
                content=local_context.get("target_excerpt", ""),
                anchor_type="target-theorem",
                source="KB",
            ),
            *source_hits,
        ]
    )
    contradiction = _ensure_dict(proof_attempt.get("contradiction_frame"))
    negative_argument = _ensure_dict(proof_attempt.get("negative_argument"))
    negative_heuristic = _ensure_dict(proof_attempt.get("negative_route_heuristic"))
    step_claims = [
        _clean_text(row.get("claim"))
        for row in _ensure_list(proof_attempt.get("stepwise_argument"))
        if isinstance(row, dict) and _clean_text(row.get("claim"))
    ]
    tensions = [
        proof_attempt.get("route_lemma_under_test") and f"Route lemma under test: {proof_attempt.get('route_lemma_under_test')}",
        target.get("missing_route_lemma") and f"Missing route lemma: {target.get('missing_route_lemma')}",
        final_assessment.get("summary"),
        negative_heuristic.get("rationale"),
    ]
    return _base_program(
        program_id=_clean_text(metadata.get("attempt_id")),
        kind="proof-attempt",
        stage="prove",
        kb_ref=_clean_text(metadata.get("kb_ref")),
        title=_clean_text(target.get("title") or proof_attempt.get("theorem_statement") or metadata.get("attempt_id")),
        anchors=anchors,
        target={
            "label": target.get("title") or target.get("target_statement_id"),
            "statement": proof_attempt.get("theorem_statement") or target.get("conjecture_statement"),
            "target_id": target.get("target_statement_id"),
        },
        tensions=tensions,
        nexus={
            "label": target.get("bridge_id") or metadata.get("queue_id"),
            "summary": target.get("route_synopsis") or proof_attempt.get("strategy"),
            "linked_items": [
                metadata.get("queue_id"),
                target.get("candidate_object"),
                target.get("preserved_invariant"),
            ],
        },
        bridge_object={
            "label": target.get("candidate_object"),
            "kind": target.get("carrier_kind"),
            "invariant": target.get("preserved_invariant"),
            "admissibility": "; ".join(_unique_texts(_ensure_list(proof_attempt.get("assumptions")))),
        },
        positive_route={
            "claim": proof_attempt.get("theorem_statement") or target.get("conjecture_statement"),
            "route_lemma": proof_attempt.get("route_lemma_under_test"),
            "strategy": proof_attempt.get("strategy"),
            "steps": step_claims,
        },
        negative_route={
            "mode": contradiction.get("negative_mode"),
            "claim": contradiction.get("negated_claim") or negative_argument.get("obstruction_candidate"),
            "contradiction_target": contradiction.get("contradiction_target") or negative_argument.get("counterexample_or_barrier"),
            "forbidden_outcome": contradiction.get("forbidden_outcome") or negative_argument.get("effect_on_claim"),
            "impossibility_claim": negative_argument.get("impossibility_claim") or contradiction.get("impossibility_claim_template"),
        },
        proof_debt=[
            *_ensure_list(target.get("proof_obligations")),
            *_ensure_list(target.get("candidate_lemmas")),
            proof_attempt.get("route_lemma_under_test"),
        ],
        decision_gates=[
            _decision_gate(
                title="Web search gate",
                criterion=web_gate.get("decision") or "not-evaluated",
                action=web_gate.get("rationale") or "Stay local until a decisive missing fact forces browsing.",
            ),
            _decision_gate(
                title="Negative-route heuristic",
                criterion=negative_heuristic.get("decision"),
                action=negative_heuristic.get("decision_rule") or "Choose whether to continue constructive work, run a parallel negative branch, or switch to impossibility-first.",
            ),
            _decision_gate(
                title="Final assessment",
                criterion=final_assessment.get("outcome") or metadata.get("status"),
                action=final_assessment.get("summary") or "Continue, block, or finalize according to the current proof state.",
            ),
        ],
        control_objects=["kb", "mathlib", "proof_queue"],
    )


def render_pdl_program_markdown(program: dict[str, Any]) -> list[str]:
    """Render a compact Markdown view of a serialized PDL program."""

    metadata = _ensure_dict(program.get("metadata"))
    target = _ensure_dict(program.get("target"))
    nexus = _ensure_dict(program.get("conceptual_nexus"))
    bridge = _ensure_dict(program.get("bridge_object"))
    positive = _ensure_dict(program.get("positive_route"))
    negative = _ensure_dict(program.get("negative_route"))
    lines = [
        "## PDL Program",
        "",
        f"- Program ID: {metadata.get('program_id', '')}",
        f"- Kind: {metadata.get('kind', '')}",
        f"- Stage: {metadata.get('stage', '')}",
        f"- Target: {target.get('statement', '')}",
        f"- Nexus: {nexus.get('summary', '')}",
        f"- Bridge object: {bridge.get('label', '')} ({bridge.get('kind', '')})",
        f"- Positive route: {positive.get('claim', '')}",
        f"- Negative route: {negative.get('claim', '')}",
        "",
        "Anchors:",
    ]
    anchors = [row for row in _ensure_list(program.get("anchors")) if isinstance(row, dict)]
    if not anchors:
        lines.append("- None recorded.")
    else:
        for row in anchors:
            detail = _clean_text(row.get("content"))
            if detail:
                lines.append(f"- {row.get('anchor_type', '')}: {row.get('label', '')} | {detail}")
            else:
                lines.append(f"- {row.get('anchor_type', '')}: {row.get('label', '')}")
    lines.extend(["", "Tensions:"])
    tensions = _unique_texts(_ensure_list(program.get("tensions")))
    if not tensions:
        lines.append("- None recorded.")
    else:
        for row in tensions:
            lines.append(f"- {row}")
    lines.extend(["", "Proof debt:"])
    debt = _unique_texts(_ensure_list(program.get("proof_debt")))
    if not debt:
        lines.append("- None recorded.")
    else:
        for row in debt:
            lines.append(f"- {row}")
    lines.extend(["", "Decision gates:"])
    gates = [row for row in _ensure_list(program.get("decision_gates")) if isinstance(row, dict)]
    if not gates:
        lines.append("- None recorded.")
    else:
        for row in gates:
            lines.append(f"- {row.get('title', '')}: {row.get('criterion', '')} -> {row.get('action', '')}")
    return lines


def build_language_spec() -> dict[str, Any]:
    """Return a machine-readable specification of the proof-discovery language."""

    notation_layers = [
        {
            "id": "structural",
            "title": "Structural Layer",
            "role": "Names the epistemic objects under search: anchors, targets, tensions, nexuses, bridge objects, obstructions, programmes, debt, and gates.",
            "binding": "This layer says what kind of thing is currently in play.",
        },
        {
            "id": "material-inference",
            "title": "Material-Inference Layer",
            "role": "Names the operations that transform one epistemic object into another by licensed, non-monotonic, theorem-grounded moves.",
            "binding": "This layer says what inferential move is being performed underneath the structural notation.",
        },
        {
            "id": "governance",
            "title": "Governance Layer",
            "role": "Names persistence, aggregation, revision, continuation, and stop-control over discovery programmes.",
            "binding": "This layer says how the process keeps state, loops, and changes direction without losing epistemic discipline.",
        },
    ]

    primitives = [
        {
            "id": "anchor",
            "symbol": "A",
            "title": "Anchor",
            "role": "Grounded theorem body, definition, axiom, or imported result that licenses later moves.",
            "binding": "Material inference starts from anchors, not from topic labels.",
            "platform_binding": "KB statements and InformalMathLib entries.",
        },
        {
            "id": "target",
            "symbol": "T",
            "title": "Target",
            "role": "The smallest nontrivial payoff or consequence worth organizing the search around.",
            "binding": "Discovery is guided by consequence pressure rather than free exploration.",
            "platform_binding": "Route target claims and queued conjectures.",
        },
        {
            "id": "tension",
            "symbol": "X",
            "title": "Tension",
            "role": "A typed gap showing why anchors do not yet reach the target: model mismatch, invariant weakness, transport loss, or barrier pressure.",
            "binding": "Tension is the primitive of discovery, because it identifies where reasoning must change form.",
            "platform_binding": "Statement deltas, obstruction classes, and failure diagnoses.",
        },
        {
            "id": "nexus",
            "symbol": "N",
            "title": "Conceptual Nexus",
            "role": "A coherent local cluster of anchors, tensions, bridge objects, and barriers that can be reasoned over together.",
            "binding": "Discovery first asks whether there is a coherent nexus before demanding correctness-style closure.",
            "platform_binding": "Bridge portfolios, conceptual dynamics, and discovery branches.",
        },
        {
            "id": "bridge_object",
            "symbol": "B",
            "title": "Bridge Object",
            "role": "A witness, invariant, certificate, transport law, normal form, or surrogate problem that could make the target reachable.",
            "binding": "Bridge objects express the conceptual breakthrough required by the search.",
            "platform_binding": "Bridge plans, abstraction conjectures, and candidate carriers.",
        },
        {
            "id": "obstruction",
            "symbol": "O",
            "title": "Obstruction",
            "role": "A barrier, counterexample pattern, impossibility theorem, or non-realization diagnosis that blocks a route.",
            "binding": "Negative mathematics is first-class discovery content, not only a failed proof attempt.",
            "platform_binding": "Blocked results, negative programs, and obstruction maps.",
        },
        {
            "id": "discovery_program",
            "symbol": "P",
            "title": "Discovery Program",
            "role": "A paired positive/negative route over a nexus, together with proof debt, decision criteria, and revision triggers.",
            "binding": "A discovery program is the unit of guided scientific work, not an isolated proposition.",
            "platform_binding": "Proof sketches, queue entries, and branch dossiers.",
        },
        {
            "id": "proof_debt",
            "symbol": "D",
            "title": "Proof Debt",
            "role": "The set of missing lemmas, unrealized carriers, transport laws, and closure obligations still required for completion.",
            "binding": "Debt is what makes discovery governable instead of open-ended.",
            "platform_binding": "Macro-strategy reports, proof obligations, and critique findings.",
        },
        {
            "id": "decision_gate",
            "symbol": "G",
            "title": "Decision Gate",
            "role": "A criterion for continue, revise, import prior art, split regimes, or stop.",
            "binding": "Scientific discovery requires explicit transition rules, not only local generation.",
            "platform_binding": "Work loop, web-search gate, high-reward watch, and meta triggers.",
        },
    ]

    material_inference_operations = [
        {
            "id": "extract",
            "symbol": "ext",
            "latex_form": r"\mathsf{ext}(A \Rightarrow c)",
            "form": "ext(A => c)",
            "title": "Extract",
            "role": "Read a theorem body, definition, or axiom as a usable local commitment rather than as raw text.",
            "effect": "Turns a grounded anchor into claim-bearing content.",
            "universal_binding": "licensed material consequence extraction",
            "platform_binding": "Phase 0 normalization, statement excerpts, theorem-body normalizer",
        },
        {
            "id": "focus",
            "symbol": "foc",
            "latex_form": r"\mathsf{foc}(A, T \Rightarrow X)",
            "form": "foc(A, T => X)",
            "title": "Focus",
            "role": "Localize the exact tension between grounded anchors and the intended target.",
            "effect": "Turns diffuse mismatch into a typed tension object.",
            "universal_binding": "problem localization / abductive targeting",
            "platform_binding": "statement deltas, failure diagnoses, obstruction classes",
        },
        {
            "id": "concretize",
            "symbol": "conc",
            "latex_form": r"\mathsf{conc}(N \Rightarrow B)",
            "form": "conc(N => B)",
            "title": "Concretize",
            "role": "Turn a coherent conceptual nexus into a candidate bridge object, interface, or surrogate problem.",
            "effect": "Moves from coherence pressure to an inspectable candidate object.",
            "universal_binding": "abductive bridge-object formation",
            "platform_binding": "abstraction conjectures, expert conjectures, branch-to-definition outputs",
        },
        {
            "id": "transport",
            "symbol": "tr",
            "latex_form": r"\mathsf{tr}_I(B, s \leadsto t)",
            "form": "tr_I(B, s ~> t)",
            "title": "Transport",
            "role": "Move an invariant, witness condition, or theorem payload across a regime shift, representation change, or equivalence.",
            "effect": "Makes cross-model or cross-language claims explicit and testable.",
            "universal_binding": "material transfer / invariant-preserving passage",
            "platform_binding": "transport lemmas, alignment work, HoTT/coherence routes",
        },
        {
            "id": "factor",
            "symbol": "fac",
            "latex_form": r"\mathsf{fac}(r \Rightarrow r_1 \circ r_2)",
            "form": "fac(r => r1 o r2)",
            "title": "Factor",
            "role": "Split one overloaded route into smaller theorem-sized interfaces or intermediate programmes.",
            "effect": "Exposes hidden composition and missing middle objects.",
            "universal_binding": "decomposition / factorization reasoning",
            "platform_binding": "route decomposition, macro-strategy repair, categorical reframing",
        },
        {
            "id": "compose",
            "symbol": "comp",
            "latex_form": r"\mathsf{comp}(B_1, B_2 \Rightarrow B)",
            "form": "comp(B1, B2 => B)",
            "title": "Compose",
            "role": "Assemble several partial bridges, lemmas, or regime results into one route.",
            "effect": "Promotes local inferential fragments into an end-to-end programme.",
            "universal_binding": "compositional synthesis",
            "platform_binding": "bridge portfolios, hybridization-of-partial-bridges, route composition",
        },
        {
            "id": "obstruct",
            "symbol": "obs",
            "latex_form": r"\mathsf{obs}(B \Rightarrow O)",
            "form": "obs(B => O)",
            "title": "Obstruct",
            "role": "Derive the barrier, counterexample pattern, incoherence, or non-realization result that blocks a bridge.",
            "effect": "Turns failed progress into explicit negative mathematics.",
            "universal_binding": "barrier derivation / impossibility localization",
            "platform_binding": "negative routes, blocked local theorems, contradiction-first probes",
        },
        {
            "id": "revise",
            "symbol": "rev",
            "latex_form": r"\mathsf{rev}(P, O \Rightarrow P')",
            "form": "rev(P, O => P')",
            "title": "Revise",
            "role": "Update a discovery programme after an obstruction, failed proof step, or new prior-art import.",
            "effect": "Makes conceptual change itself explicit rather than leaving it as narrative drift.",
            "universal_binding": "non-monotonic theory revision",
            "platform_binding": "revision loops, branch regeneration, meta-guided restarts",
        },
        {
            "id": "aggregate",
            "symbol": "agg",
            "latex_form": r"\mathsf{agg}(\{R_i\} \Rightarrow N^*)",
            "form": "agg({Ri} => N*)",
            "title": "Aggregate",
            "role": "Combine many local results, failed routes, or branch outcomes into a single higher-order nexus or search diagnosis.",
            "effect": "Produces a global picture rather than isolated route state.",
            "universal_binding": "scientific synthesis / evidence aggregation",
            "platform_binding": "branch synthesis, breakthrough profiles, plausibility aggregation",
        },
        {
            "id": "persist",
            "symbol": "mem",
            "latex_form": r"\mathsf{mem}(R \Rightarrow M)",
            "form": "mem(R => M)",
            "title": "Persist",
            "role": "Turn a proved, disproved, blocked, or imported result into durable problem memory.",
            "effect": "Stops the system from rediscovering the same local mathematics repeatedly.",
            "universal_binding": "epistemic memory consolidation",
            "platform_binding": "InformalMathLib persistence, queue state, produced papers, prior-art imports",
        },
        {
            "id": "route",
            "symbol": "route",
            "latex_form": r"\mathsf{route}(P \Rightarrow \text{next})",
            "form": "route(P => next)",
            "title": "Route",
            "role": "Send a discovery programme to prove, further discovery, prior-art search, or stop.",
            "effect": "Connects local reasoning to governance decisions.",
            "universal_binding": "controlled transition / research governance",
            "platform_binding": "work loop, meta triggers, high-reward continuation, queue promotion",
        },
    ]

    relations = [
        {"id": "grounds", "symbol": "|-", "meaning": "An anchor licenses a claim or program component."},
        {"id": "coheres", "symbol": "~", "meaning": "Items form a stable conceptual nexus under the current representation."},
        {"id": "bridges", "symbol": "~>", "meaning": "A bridge object makes a route from anchor side to target side materially available."},
        {"id": "preserves", "symbol": "[]", "meaning": "An invariant survives a transport or re-encoding step."},
        {"id": "obstructs", "symbol": "-|", "meaning": "A barrier or impossibility pattern blocks a route or object."},
        {"id": "reframes", "symbol": "=>", "meaning": "A representation shift or decomposition changes the search unit."},
        {"id": "composes", "symbol": "o", "meaning": "Several partial bridges or programmes combine into one route."},
        {"id": "persists", "symbol": "||", "meaning": "A discovery result becomes durable memory."},
        {"id": "loops", "symbol": "@", "meaning": "The process re-enters discovery/prove under governed recursion."},
    ]

    judgments = [
        {
            "form": "K ; M |- A : grounded",
            "meaning": "The KB plus InformalMathLib licenses anchor A as a grounded theorem-body object.",
        },
        {
            "form": "A, X => N : coherent",
            "meaning": "Anchors and tensions form a coherent conceptual nexus worth exploring.",
        },
        {
            "form": "N ~> B",
            "meaning": "The nexus suggests a bridge object B as the best conceptual move.",
        },
        {
            "form": "B [] I",
            "meaning": "Bridge object B preserves invariant I across the intended route.",
        },
        {
            "form": "B ~> T",
            "meaning": "If realized, bridge object B materially supports the target consequence T.",
        },
        {
            "form": "B -| O",
            "meaning": "Bridge object B is blocked or sharpened by obstruction O.",
        },
        {
            "form": "N ; B |- P",
            "meaning": "A coherent nexus and bridge object together induce a discovery program P.",
        },
        {
            "form": "P |- D",
            "meaning": "A discovery program exposes its proof debt explicitly.",
        },
        {
            "form": "P ; O |- impossibility(T)",
            "meaning": "A negative route yields a theorem-shaped impossibility or non-realization claim.",
        },
        {
            "form": "P ; G @ next",
            "meaning": "A decision gate routes the programme into prove, revision, prior-art import, or stop.",
        },
    ]

    operational_judgments = [
        {
            "form": "A ; T |-m X",
            "meaning": "Materially focus the mismatch between anchors and target into an explicit tension X.",
        },
        {
            "form": "A ; X |-m N",
            "meaning": "Stabilize anchors and tensions into a coherent conceptual nexus N.",
        },
        {
            "form": "N |-m B",
            "meaning": "Concretize the nexus into a bridge object, map, witness family, or surrogate problem B.",
        },
        {
            "form": "B ; I ; s->t |-m tr_I(B)",
            "meaning": "Transport invariant I through bridge B from source regime s to target regime t.",
        },
        {
            "form": "r |-m fac(r1,...,rn)",
            "meaning": "Factor a route r into smaller theorem-sized route fragments.",
        },
        {
            "form": "B |-m O",
            "meaning": "Derive an obstruction O from the current bridge or route proposal.",
        },
        {
            "form": "P ; O |-m P'",
            "meaning": "Revise programme P into a new programme P' after a negative result or barrier localization.",
        },
        {
            "form": "{Ri} |-m N*",
            "meaning": "Aggregate many local route outcomes into a higher-order nexus or diagnosis N*.",
        },
        {
            "form": "R |-m M",
            "meaning": "Persist result R into durable memory object M.",
        },
    ]

    coordination = [
        {
            "title": "Coherence Before Closure",
            "detail": "A route is first judged as a coherent nexus of anchors, tensions, and bridge commitments before it is judged as correct.",
        },
        {
            "title": "Positive/Negative Symmetry",
            "detail": "Every discovery program carries both a constructive route and a negative/impossibility route, each capable of yielding mathematical value.",
        },
        {
            "title": "Material Inference First",
            "detail": "Inference moves are justified by theorem bodies, model regimes, barriers, and transport obligations before any correctness-style closure is attempted.",
        },
        {
            "title": "Persistent Scientific Memory",
            "detail": "Queues, InformalMathLib, logs, and branch states are part of the logic itself because discovery depends on not forgetting failed and partial routes.",
        },
        {
            "title": "Governed Recursion",
            "detail": "Loops are legitimate only when proof debt, obstruction pressure, or high-value subresults justify another cycle.",
        },
    ]

    control_objects = [
        {"id": "kb", "title": "Problem KB", "role": "Anchor store and source corpus."},
        {"id": "mathlib", "title": "InformalMathLib", "role": "Persistent theorem memory and imported prior art."},
        {"id": "proof_queue", "title": "Proof Queue", "role": "Theorem-shaped frontier for proof or disproof."},
        {"id": "discovery_branch_queue", "title": "Discovery Branch Queue", "role": "Pattern-shaped frontier for conceptual exploration."},
        {"id": "high_reward_watch", "title": "High-Reward Watch", "role": "Continuation control for major subresults."},
        {"id": "meta", "title": "Meta Reflection", "role": "Interpretive layer over what changed in understanding."},
    ]

    example_program = {
        "anchor_set": ["A1: source theorem body", "A2: target theorem body", "A3: local barrier theorem"],
        "tension": "X1: transport from source regime to target regime loses the intended invariant",
        "nexus": "N1 := cohere(A1, A2, X1, barrier=A3)",
        "bridge": "B1 := witness family preserving the source-side hardness profile",
        "operations": [
            "ext(A1 => c1): extract the usable lower-bound content from the source theorem body",
            "foc(A1, T1 => X1): isolate the exact transport loss between source and target",
            "conc(N1 => B1): propose the witness family as the bridge object demanded by the nexus",
            "tr_I(B1, source ~> target): test whether the invariant survives the intended transport",
            "obs(B1 => O1): derive the non-realization barrier if the witness family collapses",
            "rev(P1, O1 => P2): revise the route into a transport-obstruction programme",
            "mem(O1 => M1): persist the blocked result into InformalMathLib as negative local theorem memory",
        ],
        "positive_route": "If B1 is realizable and preserves the invariant, reduce target T to one route lemma L",
        "negative_route": "If every realization of B1 collapses into the barrier, derive impossibility(B1 -> T)",
        "proof_debt": ["L1: carrier realization", "L2: transport theorem", "L3: payoff forcing theorem"],
        "decision_gate": "If L1 sharpens but L2 fails under barrier A3, reframe as transport-obstruction rather than continue constructive forcing",
    }

    return {
        "metadata": {
            "title": "Proof Discovery Language",
            "short_name": "PDL",
            "thesis": "PDL is a language for discovery programmes rather than only arguments of correctness. It treats coherence, conceptual nexus, material inference, obstruction, and governed recursion as first-class logical objects, and it distinguishes structural notation from the operations that materially transform one epistemic state into another.",
        },
        "design_principles": [
            "Prioritize conceptual nexus before closure.",
            "Represent tensions and obstructions explicitly.",
            "Treat bridge objects as typed inferential interfaces.",
            "Make negative and impossibility reasoning first-class.",
            "Make the underlying material-inference operators explicit rather than hiding them in prose.",
            "Embed persistence, aggregation, and loops into the logic itself.",
        ],
        "notation_layers": notation_layers,
        "primitives": primitives,
        "material_inference_operations": material_inference_operations,
        "relations": relations,
        "judgments": judgments,
        "operational_judgments": operational_judgments,
        "coordination_principles": coordination,
        "control_objects": control_objects,
        "well_formed_program_requirements": [
            "At least one grounded anchor and one explicit target.",
            "A typed tension explaining why the route is not immediate.",
            "A coherent nexus rather than a bag of related statements.",
            "A positive route, a negative route, and explicit proof debt.",
            "A decision gate specifying continue, revise, import, split, or stop.",
        ],
        "example_program": example_program,
    }


def render_markdown(spec: dict[str, Any]) -> str:
    """Render the proof-discovery language specification as Markdown."""

    lines = [
        "# Proof Discovery Language",
        "",
        spec["metadata"]["thesis"],
        "",
        "## Core Claim",
        "",
        "The language is not centered on correctness-style proofs alone. It is centered on discovery programs: coherent nexuses of anchors, tensions, bridge objects, obstructions, and governed decisions over proof debt.",
        "",
        "## Design Principles",
        "",
    ]
    for row in spec["design_principles"]:
        lines.append(f"- {row}")
    lines.extend(["", "## Notation Layers", ""])
    for row in spec["notation_layers"]:
        lines.append(f"- **{row['title']}**: {row['role']}")
        lines.append(f"  Binding: {row['binding']}")
    lines.extend(["", "## Primitives", ""])
    for row in spec["primitives"]:
        lines.append(f"- `{row['symbol']}` **{row['title']}**: {row['role']}")
        lines.append(f"  Material binding: {row['binding']}")
        lines.append(f"  Platform binding: {row['platform_binding']}")
    lines.extend(["", "## Material-Inference Operations", ""])
    for row in spec["material_inference_operations"]:
        lines.append(f"- `{row['form']}` **{row['title']}**: {row['role']}")
        lines.append(f"  Effect: {row['effect']}")
        lines.append(f"  Universal binding: {row['universal_binding']}")
        lines.append(f"  Platform binding: {row['platform_binding']}")
    lines.extend(["", "## Relations", ""])
    for row in spec["relations"]:
        lines.append(f"- `{row['symbol']}` **{row['id']}**: {row['meaning']}")
    lines.extend(["", "## Judgments", ""])
    for row in spec["judgments"]:
        lines.append(f"- `{row['form']}`: {row['meaning']}")
    lines.extend(["", "## Operational Judgments", ""])
    for row in spec["operational_judgments"]:
        lines.append(f"- `{row['form']}`: {row['meaning']}")
    lines.extend(["", "## Coordination Logic", ""])
    for row in spec["coordination_principles"]:
        lines.append(f"- **{row['title']}**: {row['detail']}")
    lines.extend(["", "## Control Objects", ""])
    for row in spec["control_objects"]:
        lines.append(f"- **{row['title']}** (`{row['id']}`): {row['role']}")
    lines.extend(["", "## Well-Formed Discovery Program", ""])
    for row in spec["well_formed_program_requirements"]:
        lines.append(f"- {row}")
    ex = spec["example_program"]
    lines.extend(
        [
            "",
            "## Example Program",
            "",
            "```text",
            ex["anchor_set"][0],
            ex["anchor_set"][1],
            ex["anchor_set"][2],
            ex["tension"],
            ex["nexus"],
            ex["bridge"],
            "Operations:",
            *[f"- {row}" for row in ex["operations"]],
            ex["positive_route"],
            ex["negative_route"],
            "Debt:",
            *[f"- {row}" for row in ex["proof_debt"]],
            "Gate:",
            ex["decision_gate"],
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def render_latex(spec: dict[str, Any]) -> str:
    """Render the proof-discovery language specification as LaTeX."""

    parts = [
        r"\documentclass[11pt]{article}",
        r"\usepackage[margin=1in]{geometry}",
        r"\usepackage[T1]{fontenc}",
        r"\usepackage[utf8]{inputenc}",
        r"\usepackage{lmodern}",
        r"\usepackage{amsmath,amssymb}",
        r"\usepackage{enumitem}",
        r"\usepackage{hyperref}",
        r"\title{Proof Discovery Language}",
        r"\author{Neuro-symbolic AI Group\\Idiap Research Institute}",
        r"\date{March 17, 2026}",
        r"\begin{document}",
        r"\maketitle",
        r"\begin{abstract}",
        _latex_escape(spec["metadata"]["thesis"]),
        r"\end{abstract}",
        r"\section{Core Claim}",
        _latex_escape(
            "The language is not centered on correctness-style proofs alone. It is centered on discovery programs: coherent nexuses of anchors, tensions, bridge objects, obstructions, and governed decisions over proof debt."
        ),
        r"\section{Design Principles}",
        r"\begin{itemize}[leftmargin=*,itemsep=0.25em]",
    ]
    parts.extend(rf"\item {_latex_escape(row)}" for row in spec["design_principles"])
    parts.extend([r"\end{itemize}", r"\section{Notation Layers}", r"\begin{itemize}[leftmargin=*,itemsep=0.25em]"])
    for row in spec["notation_layers"]:
        parts.append(
            rf"\item \textbf{{{_latex_escape(row['title'])}}}: {_latex_escape(row['role'])} "
            rf"\emph{{Binding.}} {_latex_escape(row['binding'])}"
        )
    parts.extend([r"\end{itemize}", r"\section{Primitives}", r"\begin{itemize}[leftmargin=*,itemsep=0.25em]"])
    for row in spec["primitives"]:
        parts.append(
            rf"\item \textbf{{{_latex_escape(row['title'])}}} ($ {_latex_escape(row['symbol'])} $): {_latex_escape(row['role'])} "
            rf"\emph{{Material binding.}} {_latex_escape(row['binding'])} "
            rf"\emph{{Platform binding.}} {_latex_escape(row['platform_binding'])}"
        )
    parts.extend([r"\end{itemize}", r"\section{Material-Inference Operations}", r"\begin{itemize}[leftmargin=*,itemsep=0.25em]"])
    for row in spec["material_inference_operations"]:
        parts.append(
            rf"\item \texttt{{{_latex_escape(row['form'])}}}: {_latex_escape(row['role'])} "
            rf"\emph{{Effect.}} {_latex_escape(row['effect'])} "
            rf"\emph{{Universal binding.}} {_latex_escape(row['universal_binding'])} "
            rf"\emph{{Platform binding.}} {_latex_escape(row['platform_binding'])}"
        )
    parts.extend([r"\end{itemize}", r"\section{Judgments}", r"\begin{itemize}[leftmargin=*,itemsep=0.25em]"])
    for row in spec["judgments"]:
        parts.append(rf"\item \texttt{{{_latex_escape(row['form'])}}}: {_latex_escape(row['meaning'])}")
    parts.extend([r"\end{itemize}", r"\section{Operational Judgments}", r"\begin{itemize}[leftmargin=*,itemsep=0.25em]"])
    for row in spec["operational_judgments"]:
        parts.append(rf"\item \texttt{{{_latex_escape(row['form'])}}}: {_latex_escape(row['meaning'])}")
    parts.extend([r"\end{itemize}", r"\section{Coordination Logic}", r"\begin{itemize}[leftmargin=*,itemsep=0.25em]"])
    for row in spec["coordination_principles"]:
        parts.append(rf"\item \textbf{{{_latex_escape(row['title'])}}}: {_latex_escape(row['detail'])}")
    parts.extend([r"\end{itemize}", r"\section{Well-Formed Discovery Program}", r"\begin{itemize}[leftmargin=*,itemsep=0.25em]"])
    parts.extend(rf"\item {_latex_escape(row)}" for row in spec["well_formed_program_requirements"])
    ex = spec["example_program"]
    parts.extend(
        [
            r"\end{itemize}",
            r"\section{Example Program}",
            r"\begin{itemize}[leftmargin=*,itemsep=0.25em]",
            *[rf"\item {_latex_escape(row)}" for row in ex["anchor_set"]],
            rf"\item {_latex_escape(ex['tension'])}",
            rf"\item {_latex_escape(ex['nexus'])}",
            rf"\item {_latex_escape(ex['bridge'])}",
            *[rf"\item {_latex_escape(row)}" for row in ex["operations"]],
            rf"\item {_latex_escape(ex['positive_route'])}",
            rf"\item {_latex_escape(ex['negative_route'])}",
            rf"\item \textbf{{Debt.}} {_latex_escape('; '.join(ex['proof_debt']))}",
            rf"\item \textbf{{Gate.}} {_latex_escape(ex['decision_gate'])}",
            r"\end{itemize}",
            r"\end{document}",
        ]
    )
    return "\n".join(parts) + "\n"

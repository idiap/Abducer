# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Seal a model-authored conceptual panel as explicitly correlated critique.

The model sees opaque candidate content and the rubric. Local adapters bind its
actual answers to source content paths and replay them deterministically through
the original judge/report/evidence validators. A replay is not another model
opinion, and the panel never claims external or independent scientific authority.
"""
from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, Mapping

from .bootstrap_authoring import array_schema, object_schema, schema_fragment
from .conceptual_adjudication import (
    DIMENSIONS, _DIMENSION_WARRANT_PREFIXES, _pointer, _validate_deep_lens_panel,
    build_adjudication_source_bindings, build_blind_packet, build_judge_report,
)
from .contracts import ContractError, canonical_digest, utc_now
from .model_author import ModelAuthor, read_record


LENSES = ("ontological", "dialectical", "explanatory")


def _without_derived_fields(schema):
    if isinstance(schema, list):
        return [_without_derived_fields(row) for row in schema]
    if not isinstance(schema, dict):
        return schema
    value = {key: _without_derived_fields(row) for key, row in schema.items()}
    if "properties" in value:
        value["properties"] = {key: row for key, row in value["properties"].items()
                               if key not in {"value_digest", "analysis_digest", "dimension"}}
    if "required" in value:
        value["required"] = [key for key in value["required"] if key not in {"value_digest", "analysis_digest", "dimension"}]
    return value


def panel_schema(aliases: list[str]) -> dict[str, Any]:
    schema_name = "conceptual_adjudication_evidence.schema.json"
    dimensions = _without_derived_fields(schema_fragment(schema_name, "/$defs/dimensionMap"))
    deep = _without_derived_fields(schema_fragment(schema_name, "/$defs/deepLensAnalysis"))
    deep["properties"]["lens_family"] = {"enum": list(LENSES)}
    finding = object_schema({"candidate_alias": {"enum": aliases}, "dimensions": dimensions,
                             "deep_lens_analysis": deep})
    panel = object_schema({"lens_family": {"enum": list(LENSES)},
                          "findings": array_schema(finding, len(aliases), len(aliases))})
    return object_schema({"panels": array_schema(panel, len(LENSES), len(LENSES))})


def _compiled_judgment(finding: Mapping[str, Any], candidate: Mapping[str, Any]) -> dict[str, Any]:
    """Hash exact cited content without adding or changing the model's judgments."""
    output = copy.deepcopy({key: value for key, value in finding.items() if key != "candidate_alias"})
    for dimension in DIMENSIONS:
        for warrant in output["dimensions"][dimension]["warrants"]:
            warrant["dimension"] = dimension
            warrant["value_digest"] = canonical_digest(_pointer(candidate["content"], warrant["path"]))
    for warrant in output["deep_lens_analysis"]["content_warrants"]:
        warrant["value_digest"] = canonical_digest(_pointer(candidate["content"], warrant["path"]))
    return output


def _build_reports(value: Mapping[str, Any], blind: Mapping[str, Any], *,
                   completed_at: str | None = None, dependencies=()) -> list[dict[str, Any]]:
    expected = [row["candidate_alias"] for row in blind["candidates"]]
    panels = value["panels"]
    if sorted(row["lens_family"] for row in panels) != sorted(LENSES):
        raise ContractError("conceptual panel must include each required lens exactly once")
    reports = []
    for panel in panels:
        lens = panel["lens_family"]
        if [row["candidate_alias"] for row in panel["findings"]] != expected:
            raise ContractError("each conceptual lens must cover every blind candidate in order")
        if any(row["deep_lens_analysis"]["lens_family"] != lens for row in panel["findings"]):
            raise ContractError("conceptual findings crossed their declared lens")
        findings = {row["candidate_alias"]: row for row in panel["findings"]}
        def recorded_judge(candidate, packet):
            # This adapter replays one exact frozen model answer. The model's
            # identity/authorship stays in its dependency journal; executable
            # replay authority is correctly shared by all three lenses.
            return _compiled_judgment(findings[candidate["candidate_alias"]], candidate)
        report = build_judge_report(blind, adjudicator_id="bootstrap-internal-" + lens,
            perspective=lens, version="1.0.0", judge=recorded_judge,
            lens_family=lens, independence_claim="correlated_internal",
            created_at=completed_at, dependency_paths=dependencies)
        reports.append(report)
    _validate_deep_lens_panel(blind, reports)
    return reports


def author_panel(author: ModelAuthor, *, stage_id: str, blind: Mapping[str, Any]) -> dict[str, Any]:
    """Run the three-lens rubric on blinded content without a requested winner."""
    aliases = [row["candidate_alias"] for row in blind["candidates"]]
    view = {key: blind[key] for key in ("target_charter", "candidates", "reflection_rounds")}
    view["warrant_paths_by_dimension"] = _DIMENSION_WARRANT_PREFIXES
    return author.author(stage_id, instruction=(
        "Review every blind candidate in the given order from ontological, dialectical and explanatory lenses. "
        "These are three internally correlated perspectives from the same model call, not independent evaluators. "
        "For every rubric dimension, rate unknown/weak/adequate/strong and cite a relevant exact JSON pointer "
        "into that candidate's content. Give a substantive strongest objection and a concrete correction test. "
        "Every explanation, objection, test and deep-analysis field must have at least six meaningful words. "
        "Each deep analysis needs at least two different content warrants, a target-specific consequence, and "
        "an explicit return to the target pressure. The legacy physics_value_handback field means target "
        "applicability here; do not import another target. Assess actual mediation, preserved differences, "
        "falsifiability and remaining circularity. Do not force a winner or inflate ratings to pass a gate. "
        "Do not provide digests: the runtime computes them from the exact cited content."),
        inputs=view, schema=panel_schema(aliases),
        validator=lambda value: _build_reports(value, blind), max_tokens=32000)


def adjudication_envelope(*, author: ModelAuthor, stage_id: str, packet: Mapping[str, Any],
                          proposer_receipt: Mapping[str, Any], snapshot: Mapping[str, Any],
                          portfolio: Mapping[str, Any], previous_evidence=None) -> dict[str, Any]:
    """Bind actual model judgments to the current source-producer receipt."""
    systems, rounds = packet["conceptual_systems"], packet["reflection_rounds"]
    proposer_ids = [proposer_receipt["receipt_id"]]
    source_bindings = build_adjudication_source_bindings(run_id=packet["run_id"], state_version=packet["state_version"],
        theory_state_digest=snapshot["theory_state_digest"], literature_snapshot_digest=snapshot["content_digest"],
        high_risk_portfolio_digest=portfolio["content_digest"], systems=systems, reflection_rounds=rounds,
        frozen_genealogy=[], proposer_receipt_ids=proposer_ids)
    charter = packet["discovery_charter"]
    blind, bindings = build_blind_packet(target_id=packet["target_id"], stage_id=stage_id,
        target_charter={"target_statement": charter["essential_question"],
            "root_tensions": [row["minimal_incompatibility_or_missing_mediation"] for row in packet["root_tensions"]],
            "protected_successes": charter["target_commitments"], "non_claims": [charter["non_claim_boundary"]]},
        systems=systems, reflection_rounds=rounds,
        proposer_identity=proposer_receipt["operator"]["operator_id"], source_bindings=source_bindings,
        counterbalance_seed="bootstrap-" + stage_id)
    authored = author_panel(author, stage_id=stage_id + "-panel", blind=blind)
    journal = author.root / (stage_id + "-panel")
    dependencies = sorted(str(path.resolve()) for path in journal.rglob("*.json"))
    # The model completion time remains frozen in its journal. This timestamp
    # belongs to the current deterministic report execution, including replay.
    completed_at = utc_now()
    reports = _build_reports(authored["value"], blind, completed_at=completed_at, dependencies=dependencies)
    return {"blind_packet": blind, "judge_reports": reports, "systems": systems, "reflection_rounds": rounds,
        "frozen_genealogy": [], "candidate_bindings": bindings, "theory_state_digest": snapshot["theory_state_digest"],
        "literature_snapshot_digest": snapshot["content_digest"], "high_risk_portfolio_digest": portfolio["content_digest"],
        "proposer_receipt_ids": proposer_ids, "previous_evidence": previous_evidence,
        "previous_evidence_digest": previous_evidence["evidence_digest"] if previous_evidence else None,
        "created_at": completed_at}

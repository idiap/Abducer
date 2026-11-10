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

import json
from pathlib import Path

from to_prism.conformance import (
    canonical_sha256,
    validate_generated_layers,
    validate_generation_provenance,
)


def _plan(mode: str = "mixed") -> dict:
    epistemic = {
        "id": "assess_claim",
        "semantic_role": "epistemic",
        "reasoning_type": "ClaimAssessment",
        "relation_type": "TestsClaim",
    }
    operational = {
        "id": "validate_claim",
        "semantic_role": "operational",
        "material_kind": "computed",
    }
    steps = [epistemic, operational] if mode == "mixed" else [operational]
    return {
        "artifact": "generation-plan",
        "schema_version": "1.0",
        "workflows": [
            {
                "id": "claim_review",
                "semantic_mode": mode,
                "steps": steps,
            }
        ],
    }


def test_operational_workflow_rejects_reasoning_file(tmp_path: Path) -> None:
    (tmp_path / "reasoning.prism").write_text(
        "reasoning ClaimReview(source: Claim) -> Computed[Decision]:\n",
        encoding="utf-8",
    )
    (tmp_path / "materialization.prism").write_text(
        "workflow ClaimReview(source: Claim):\n"
        "def validate_claim_compute(source: Claim):\n",
        encoding="utf-8",
    )
    (tmp_path / "main.prism").write_text("def main():\n", encoding="utf-8")

    assert (
        "operational workflow requires a reviewed reasoning projection before "
        "reasoning.prism can be emitted"
    ) in (
        validate_generated_layers(tmp_path, _plan("operational"))
    )


def test_operational_workflow_accepts_reviewed_reasoning_projection(
    tmp_path: Path,
) -> None:
    plan = _plan("operational")
    plan["workflows"][0]["reasoning_projection"] = {
        "name": "ReviewClaimValidity",
        "occurrences": [
            {
                "id": "validity_assessment",
                "method": "AssessClaimValidity",
                "relation": None,
            }
        ],
    }
    (tmp_path / "occurrences.prism").write_text(
        "type AssessClaimValidity = Claim -> Generated[Assessment]\n",
        encoding="utf-8",
    )
    (tmp_path / "relations.prism").write_text("# no prior relation\n", encoding="utf-8")
    (tmp_path / "reasoning.prism").write_text(
        "from occurrences import AssessClaimValidity\n"
        "reasoning ReviewClaimValidity(source: Claim) -> Generated[Assessment]:\n",
        encoding="utf-8",
    )
    (tmp_path / "materialization.prism").write_text(
        "workflow ClaimReview(source: Claim):\n"
        "def validate_claim_compute(source: Claim):\n"
        "agent validity_assessment_reasoning_agent(task: Claim):\n"
        "converted_reasoning = ReviewClaimValidity(\n"
        "    validity_assessment = validity_assessment_reasoning_agent,\n"
        ")\n",
        encoding="utf-8",
    )
    (tmp_path / "main.prism").write_text(
        "return solve ReviewClaimValidity(source) using flow\n",
        encoding="utf-8",
    )
    (tmp_path / "material_main.prism").write_text(
        "return solve ClaimReview(source)\n",
        encoding="utf-8",
    )

    assert validate_generated_layers(tmp_path, plan) == []


def test_mixed_workflow_keeps_computation_out_of_reasoning(tmp_path: Path) -> None:
    (tmp_path / "occurrences.prism").write_text(
        "type ClaimAssessment = Claim -> Generated[Assessment]\n",
        encoding="utf-8",
    )
    (tmp_path / "relations.prism").write_text(
        "relation TestsClaim(source: Claim, target: Generated[Assessment]) -> Certificate\n",
        encoding="utf-8",
    )
    (tmp_path / "materialization.prism").write_text(
        "agent assess_claim_agent(task: Claim):\n"
        "def validate_claim_compute(source: Assessment):\n"
        "workflow ClaimReview(source: Claim):\n",
        encoding="utf-8",
    )
    (tmp_path / "main.prism").write_text("def main():\n", encoding="utf-8")

    assert validate_generated_layers(tmp_path, _plan()) == []

    (tmp_path / "reasoning.prism").write_text(
        "reasoning ClaimReview(source: Claim) -> Computed[Decision]:\n",
        encoding="utf-8",
    )
    issues = validate_generated_layers(tmp_path, _plan())
    assert (
        "mixed workflow requires a reviewed high-level projection before reasoning.prism can be emitted"
        in issues
    )


def test_epistemic_reasoning_file_rejects_embedded_declarations(tmp_path: Path) -> None:
    plan = _plan("mixed")
    plan["workflows"][0]["semantic_mode"] = "epistemic"
    plan["workflows"][0]["steps"] = [plan["workflows"][0]["steps"][0]]
    (tmp_path / "occurrences.prism").write_text(
        "type ClaimAssessment = Claim -> Generated[Assessment]\n",
        encoding="utf-8",
    )
    (tmp_path / "relations.prism").write_text(
        "relation TestsClaim(source: Claim, target: Generated[Assessment]) -> Certificate\n",
        encoding="utf-8",
    )
    (tmp_path / "reasoning.prism").write_text(
        "from occurrences import ClaimAssessment\n"
        "type Embedded = Claim -> Assessment\n"
        "reasoning ClaimReview(source: Claim) -> Generated[Assessment]:\n"
        "    sequence:\n"
        "        [assess_claim: ClaimAssessment(source)] by TestsClaim\n"
        "    return assess_claim\n",
        encoding="utf-8",
    )
    (tmp_path / "materialization.prism").write_text(
        "agent assess_claim_agent(task: Claim):\n"
        "converted_workflow = ClaimReview(assess_claim = assess_claim_agent)\n",
        encoding="utf-8",
    )
    (tmp_path / "main.prism").write_text("def main():\n", encoding="utf-8")

    assert (
        "reasoning.prism must contain only imports, comments, and one core reasoning declaration"
        in validate_generated_layers(tmp_path, plan)
    )


def test_reasoning_file_rejects_material_declarations(tmp_path: Path) -> None:
    plan = _plan("mixed")
    plan["workflows"][0]["semantic_mode"] = "epistemic"
    plan["workflows"][0]["steps"] = [plan["workflows"][0]["steps"][0]]
    (tmp_path / "occurrences.prism").write_text(
        "type ClaimAssessment = Claim -> Generated[Assessment]\n",
        encoding="utf-8",
    )
    (tmp_path / "relations.prism").write_text(
        "relation TestsClaim(source: Claim, target: Assessment) -> Certificate\n",
        encoding="utf-8",
    )
    (tmp_path / "reasoning.prism").write_text(
        "from occurrences import ClaimAssessment\n"
        "def hidden_material_step(source: Claim) -> Assessment:\n"
        "    return source\n"
        "reasoning ClaimReview(source: Claim) -> Generated[Assessment]:\n",
        encoding="utf-8",
    )
    (tmp_path / "materialization.prism").write_text(
        "agent assess_claim_agent(task: Claim):\n"
        "converted_workflow = ClaimReview(assess_claim = assess_claim_agent)\n",
        encoding="utf-8",
    )
    (tmp_path / "main.prism").write_text("def main():\n", encoding="utf-8")

    issues = validate_generated_layers(tmp_path, plan)

    assert any("one core reasoning declaration" in issue for issue in issues)


def test_mixed_projection_requires_explicit_reasoning_materialization(
    tmp_path: Path,
) -> None:
    plan = _plan()
    plan["workflows"][0]["reasoning_projection"] = {
        "name": "ReviewClaim",
        "occurrences": [
            {
                "id": "assessment",
                "method": "AssessClaim",
                "relation": None,
            }
        ],
    }
    (tmp_path / "occurrences.prism").write_text(
        "type AssessClaim = Claim -> Generated[Assessment]\n",
        encoding="utf-8",
    )
    (tmp_path / "relations.prism").write_text("# none\n", encoding="utf-8")
    (tmp_path / "reasoning.prism").write_text(
        "from occurrences import AssessClaim\n"
        "reasoning ReviewClaim(source: Claim) -> Generated[Assessment]:\n",
        encoding="utf-8",
    )
    (tmp_path / "materialization.prism").write_text(
        "agent assess_claim_agent(task: Claim):\n"
        "def validate_claim_compute(source: Assessment):\n"
        "workflow ClaimReview(source: Claim):\n",
        encoding="utf-8",
    )
    (tmp_path / "main.prism").write_text(
        "return solve ReviewClaim(source) using flow\n",
        encoding="utf-8",
    )

    issues = validate_generated_layers(tmp_path, plan)

    assert any("reviewed reasoning implementation" in issue for issue in issues)
    assert any("projected occurrence binding assessment" in issue for issue in issues)
    assert any("detailed material entrypoint" in issue for issue in issues)


def test_generation_provenance_binds_plan_and_sources(tmp_path: Path) -> None:
    plan = _plan()
    (tmp_path / "main.prism").write_text("def main():\n", encoding="utf-8")
    digest = __import__("hashlib").sha256((tmp_path / "main.prism").read_bytes()).hexdigest()
    conversion = tmp_path / "conversion"
    conversion.mkdir()
    (conversion / "generation.json").write_text(
        json.dumps(
            {
                "generator": "to_prism",
                "generation_plan_sha256": "sha256:" + canonical_sha256(plan),
                "source_hashes": {"main.prism": digest},
            }
        ),
        encoding="utf-8",
    )

    assert validate_generation_provenance(tmp_path, plan) == []
    (tmp_path / "main.prism").write_text("def changed():\n", encoding="utf-8")
    assert "generated source hash differs: main.prism" in validate_generation_provenance(
        tmp_path, plan
    )

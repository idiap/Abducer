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
import subprocess
import sys
from pathlib import Path

import jsonschema
import pytest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "proj_skills/framework-paper-blueprint-author/scripts/generate_paper_packets.py"
ASSEMBLER = ROOT / "proj_skills/framework-paper-latex-assembler/scripts/assemble_paper.py"
SPEC = ROOT / "agentic/spec"
DIGEST = "sha256:" + "1" * 64


def write(path: Path, value: object) -> Path:
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


@pytest.fixture
def inputs(tmp_path: Path) -> dict[str, Path]:
    ledger = {
        "claims": [
            {"claim_id": "CL-DESCRIPTIVE", "claim_class": "descriptive", "status": "declared", "resolution": "accepted", "freshness": "current", "allowed_sections": ["introduction", "method"]},
            {"claim_id": "CL-NOVEL", "claim_class": "novelty", "status": "inferred", "resolution": "accepted", "freshness": "current", "allowed_sections": ["introduction", "related-work"]},
            {"claim_id": "CL-EFFICACY", "claim_class": "evaluative", "status": "observed", "resolution": "accepted", "freshness": "current", "allowed_sections": ["evaluation"]},
        ]
    }
    abstraction = {
        "constructs": [{"name": "Evidence compiler", "definition": "A typed workflow from repository evidence to paper claims."}],
        "notation_ids": ["N-1"],
    }
    return {"ledger": write(tmp_path / "ledger.json", ledger), "abstraction": write(tmp_path / "abstraction.json", abstraction)}


def run(*args: object, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(SCRIPT), *(str(arg) for arg in args)], cwd=ROOT, text=True, capture_output=True, check=check)


def test_repository_only_blueprint_withholds_novelty_and_results(tmp_path: Path, inputs: dict[str, Path]) -> None:
    output = tmp_path / "paper-blueprint.json"
    run("blueprint", "--ledger", inputs["ledger"], "--abstraction", inputs["abstraction"], "--output", output)
    packet = json.loads(output.read_text())
    schema = json.loads((SPEC / "framework_paper_blueprint.schema.json").read_text())
    jsonschema.Draft202012Validator(schema).validate(packet)
    assert packet["paper_kind"] == "descriptive_framework"
    assert packet["section_order"][0] == "abstract"
    assert set(packet["non_claims"]) == {"CL-EFFICACY", "CL-NOVEL"}
    sections = {item["section_id"]: item for item in packet["sections"]}
    assert sections["related-work"]["title"] == "Related Work Evidence Status"
    assert sections["evaluation"]["title"] == "Current Evidence Status"


@pytest.mark.parametrize("section_id, warning", [("related-work", "literature_snapshot_missing"), ("evaluation", "authorized_results_missing")])
def test_missing_authority_degrades_section_without_claims(tmp_path: Path, inputs: dict[str, Path], section_id: str, warning: str) -> None:
    blueprint = tmp_path / "blueprint.json"
    run("blueprint", "--ledger", inputs["ledger"], "--abstraction", inputs["abstraction"], "--output", blueprint)
    draft = write(tmp_path / "draft.json", {"paragraphs": [{"text": "Unsupported strong result", "claim_ids": [], "citation_keys": []}]})
    sidecar, tex = tmp_path / f"{section_id}.section.json", tmp_path / f"{section_id}.tex"
    run("section", "--blueprint", blueprint, "--ledger", inputs["ledger"], "--model", inputs["abstraction"], "--draft", draft, "--section-id", section_id, "--output", sidecar, "--tex-output", tex)
    packet = json.loads(sidecar.read_text())
    schema = json.loads((SPEC / "framework_paper_section_draft.schema.json").read_text())
    jsonschema.Draft202012Validator(schema).validate(packet)
    assert packet["consumed_claim_ids"] == []
    assert any(item.startswith(warning) for item in packet["warnings"])
    body = tex.read_text()
    assert "remain unknown" in body
    assert "Unsupported strong result" not in body


def test_writer_rejects_claim_not_allocated_to_section(tmp_path: Path, inputs: dict[str, Path]) -> None:
    blueprint = tmp_path / "blueprint.json"
    run("blueprint", "--ledger", inputs["ledger"], "--abstraction", inputs["abstraction"], "--output", blueprint)
    draft = write(tmp_path / "draft.json", {"paragraphs": [{"text": "Claim leakage", "claim_ids": ["CL-DESCRIPTIVE"], "citation_keys": []}]})
    result = run("section", "--blueprint", blueprint, "--ledger", inputs["ledger"], "--draft", draft, "--section-id", "limitations", "--output", tmp_path / "out.json", "--tex-output", tmp_path / "out.tex", check=False)
    assert result.returncode != 0
    assert "unauthorized claim IDs" in result.stderr


def test_abstract_cannot_introduce_claim_absent_from_body_receipts(tmp_path: Path, inputs: dict[str, Path]) -> None:
    blueprint = tmp_path / "blueprint.json"
    run("blueprint", "--ledger", inputs["ledger"], "--abstraction", inputs["abstraction"], "--output", blueprint)
    draft = write(tmp_path / "draft.json", {"paragraphs": [{"text": "Summary", "claim_ids": ["CL-DESCRIPTIVE"], "citation_keys": []}], "accepted_body_claim_ids": []})
    result = run("section", "--blueprint", blueprint, "--ledger", inputs["ledger"], "--draft", draft, "--section-id", "abstract", "--output", tmp_path / "out.json", "--tex-output", tmp_path / "out.tex", check=False)
    assert result.returncode != 0
    assert "entailed by accepted body claims" in result.stderr


def test_generated_packets_handoff_to_latex_assembler(tmp_path: Path, inputs: dict[str, Path]) -> None:
    blueprint_path = tmp_path / "paper-blueprint.json"
    sections_dir, output_dir = tmp_path / "sections", tmp_path / "paper"
    sections_dir.mkdir()
    run("blueprint", "--ledger", inputs["ledger"], "--abstraction", inputs["abstraction"], "--output", blueprint_path)
    blueprint = json.loads(blueprint_path.read_text())
    for spec in blueprint["sections"]:
        section_id = spec["section_id"]
        claims = ["CL-DESCRIPTIVE"] if section_id in {"abstract", "introduction", "method", "conclusion"} else []
        draft_packet: dict[str, object] = {
            "paragraphs": [{"text": f"Controlled {section_id} text.", "claim_ids": claims, "citation_keys": []}],
        }
        if section_id in {"abstract", "conclusion"}:
            draft_packet["accepted_body_claim_ids"] = ["CL-DESCRIPTIVE"]
        draft = write(tmp_path / f"{section_id}.draft.json", draft_packet)
        run(
            "section", "--blueprint", blueprint_path, "--ledger", inputs["ledger"],
            "--model", inputs["abstraction"], "--draft", draft, "--section-id", section_id,
            "--output", sections_dir / f"{section_id}.section.json",
            "--tex-output", sections_dir / f"{section_id}.tex",
        )
        sidecar = json.loads((sections_dir / f"{section_id}.section.json").read_text())
        assert sidecar["input_digest"] == blueprint["input_digest"]
    assembled = subprocess.run(
        [sys.executable, str(ASSEMBLER), "--blueprint", str(blueprint_path),
         "--sections-dir", str(sections_dir), "--output-dir", str(output_dir)],
        cwd=ROOT, text=True, capture_output=True, check=True,
    )
    assert assembled.returncode == 0
    main = (output_dir / "main.tex").read_text()
    assert main.index(r"\begin{abstract}") < main.index(r"\section{Introduction}")


def test_external_lane_schemas_require_immutable_provenance() -> None:
    schemas = {
        name: json.loads((SPEC / f"framework_paper_{name}.schema.json").read_text())
        for name in ("literature_snapshot", "bibliography_registry", "result_packet")
    }
    literature = {
        "schema_version": "1.0.0", "snapshot_id": "LIT-1", "status": "frozen",
        "created_at": "2026-08-05T10:00:00Z", "query_protocol": "registered search v1",
        "content_digest": DIGEST,
        "records": [{"citation_key": "Smith2026", "title": "A paper", "authors": ["A. Smith"],
                     "year": 2026, "doi": "10.1/example", "source_version": "publisher-v1",
                     "provenance": "publisher record", "content_digest": DIGEST,
                     "correction_state": "none_known", "conflict_state": "none_known"}],
    }
    bibliography = {"schema_version": "1.0.0", "backend": "bibtex", "snapshot_digest": DIGEST,
                    "entries": [{"citation_key": "Smith2026", "record_digest": DIGEST, "bibtex_digest": DIGEST}]}
    results = {"schema_version": "1.0.0", "packet_id": "RES-1", "authorization_status": "authorized",
               "evidence_tier": "externally_authorized_replicated", "protocol_id": "P-1",
               "receipt_digests": [DIGEST], "metric_definitions": {"score": "registered score"},
               "results": {"score": 1.0}, "uncertainty": {"kind": "interval"},
               "replication": {"runs": 3}, "limitations": ["one target"], "content_digest": DIGEST}
    for name, packet in (("literature_snapshot", literature), ("bibliography_registry", bibliography), ("result_packet", results)):
        jsonschema.Draft202012Validator(schemas[name], format_checker=jsonschema.FormatChecker()).validate(packet)
    invalid = json.loads(json.dumps(literature))
    invalid["records"][0].pop("doi")
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(schemas["literature_snapshot"]).validate(invalid)

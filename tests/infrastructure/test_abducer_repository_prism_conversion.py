# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Focused invariants for the deterministic repository-to-PRISM conversion."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
CONVERSION = ROOT / "abducer-repository-prism"


def _load_runtime(path: Path):
    spec = importlib.util.spec_from_file_location("abducer_repository_prism_runtime", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_inventory_and_export_config_are_complete() -> None:
    config = json.loads((ROOT / "prism-export.json").read_text(encoding="utf-8"))
    catalog = json.loads((CONVERSION / "workflow_catalog.json").read_text(encoding="utf-8"))
    dispositions = json.loads((CONVERSION / "skill_dispositions.json").read_text(encoding="utf-8"))
    assert len(config["workflows"]) == len(catalog["workflows"]) == 19
    assert len(config["skills"]) == len(dispositions["skills"]) == 359
    assert len(config["data_sources"]) == 7
    assert {row["disposition"] for row in dispositions["skills"]} == {"converted"}
    assert {row["id"] for row in config["workflows"]} == {
        row["id"] for row in catalog["workflows"]
    }
    discovery = next(
        row for row in config["workflows"] if row["id"] == "discovery_marathon_loop"
    )
    assert discovery["public_output_type"] == "prism.reporting.report.Report"


def test_runtime_is_self_contained_and_accepts_every_default(tmp_path: Path) -> None:
    source = CONVERSION / "runtime/abducer_lunar_runtime.py"
    isolated = tmp_path / source.name
    isolated.write_bytes(source.read_bytes())
    runtime = _load_runtime(isolated)
    contracts = json.loads(
        (CONVERSION / "runtime/workflow-inputs.json").read_text(encoding="utf-8")
    )
    assert runtime.CONTRACTS == contracts
    assert len(runtime.CONTRACTS) == 19

    for workflow_id, contract in sorted(contracts.items()):
        inputs = contract["schema"]["default"]
        Draft202012Validator(contract["schema"]).validate(inputs)
        prepared = runtime.prepare(
            workflow_id=workflow_id,
            inputs=inputs,
            run_root=tmp_path / workflow_id,
            network_authority=False,
        )
        assert prepared["prepared_input"]["value"] == inputs
        assert len(prepared["prepared_input"]["request_digest"]) == 64
        assert prepared["events"][0]["payload"]["input_key"] == "inputs"
        assert prepared["events"][0]["payload"]["content_digest"].startswith("sha256:")
        provenance = contract["provenance_contract"]
        assert provenance["agent_invocations"]
        assert provenance["required_source_reads"] == []
        assert all(row["activated_skill_ids"] for row in provenance["agent_invocations"])


def test_native_agent_trace_is_projected_to_exact_worker_receipts() -> None:
    """Regression: custom execute hooks must not discard native agent provenance."""
    runtime = _load_runtime(CONVERSION / "runtime/abducer_lunar_runtime.py")
    expected = {
        "agent_name": "scope_material_agent",
        "workflow_occurrence": "scope",
        "activated_skill_ids": ["epistemic-status-ledger"],
    }
    record = SimpleNamespace(
        invocation=SimpleNamespace(input_digest="sha256:input"),
        observation=SimpleNamespace(output_digest="sha256:output"),
    )
    execution = SimpleNamespace(
        trace=[
            SimpleNamespace(
                kind="agent-invoked",
                name=expected["agent_name"],
                status="accepted",
                metadata={"skills": tuple(expected["activated_skill_ids"])},
            ),
            SimpleNamespace(kind="effect", metadata={"record": "effect:1"}),
        ],
        effect_records={"effect:1": record},
    )
    events = []
    services = SimpleNamespace(
        model=SimpleNamespace(safe_snapshot={"provider": "test", "model_id": "model"}),
        event=lambda kind, payload: events.append({"kind": kind, "payload": payload}),
    )
    receipts = runtime._emit_agent_receipts(
        execution,
        {"provenance_contract": {"agent_invocations": [expected]}},
        services,
    )
    assert receipts == [events[0]["payload"]["detail"]]
    assert events[0]["kind"] == "stage"
    assert events[0]["payload"]["detail"] == {
        "event_kind": "agent-invoked",
        "agent_name": "scope_material_agent",
        "workflow_occurrence": "scope",
        "activated_skill_ids": ["epistemic-status-ledger"],
        "selected_model": {"provider": "test", "model_id": "model"},
        "effect_record_id": "effect:1",
        "input_digest": "sha256:input",
        "output_digest": "sha256:output",
    }

    execution.trace[0].metadata = {"skills": ("wrong-skill",)}
    with pytest.raises(ValueError, match="activated skill bindings"):
        runtime._emit_agent_receipts(
            execution,
            {"provenance_contract": {"agent_invocations": [expected]}},
            services,
        )


def test_runtime_rejects_unknown_extra_and_network_authority(tmp_path: Path) -> None:
    runtime = _load_runtime(CONVERSION / "runtime/abducer_lunar_runtime.py")
    workflow_id, contract = next(iter(sorted(runtime.CONTRACTS.items())))
    inputs = contract["schema"]["default"]
    with pytest.raises(ValueError, match="fields must be exactly"):
        runtime.prepare(
            workflow_id=workflow_id,
            inputs={**inputs, "undeclared": "must fail closed"},
            run_root=tmp_path,
            network_authority=False,
        )
    with pytest.raises(ValueError, match="do not request network authority"):
        runtime.prepare(
            workflow_id=workflow_id,
            inputs=inputs,
            run_root=tmp_path,
            network_authority=True,
        )


def test_closed_variant_agents_request_a_json_scalar_not_an_object() -> None:
    """Keep provider prompts aligned with the material ``String`` projection.

    Lunar currently exposes closed source variants to model providers as JSON
    strings.  A contradictory "JSON object" instruction can make a live model
    invent a wrapper that passes generation but must fail runtime validation.
    """
    contracts = json.loads(
        (CONVERSION / "runtime/workflow-inputs.json").read_text(encoding="utf-8")
    )
    for workflow_id, contract in sorted(contracts.items()):
        if "__value__" not in contract["variant_constraints"]:
            continue
        final_alias = contract["expected_steps"][-1]
        skills = sorted(
            (
                CONVERSION
                / "projects"
                / workflow_id
                / "prism_project"
                / "generated"
            ).glob(f"{final_alias}_skill_*.prism")
        )
        assert skills, (workflow_id, final_alias)
        for skill in skills:
            text = skill.read_text(encoding="utf-8")
            assert "Return exactly one JSON string" in text, skill
            assert "Do not return an object" in text, skill


def test_discovery_report_matches_repository_section_contract() -> None:
    runtime = _load_runtime(CONVERSION / "runtime/abducer_lunar_runtime.py")
    reasoning = (
        CONVERSION
        / "projects/discovery_marathon_loop/prism_project/reasoning.prism"
    ).read_text(encoding="utf-8")
    material = (
        CONVERSION
        / "projects/discovery_marathon_loop/prism_project/material_main.prism"
    ).read_text(encoding="utf-8")
    registration = json.loads(material.splitlines()[0].removeprefix("# lunar-runtime: "))
    expected_labels = [
        "Summary",
        "Mathematical Strategy",
        "Timeline",
        "Ranked Analyses",
        "Skill Use",
        "Contributions",
        "Result Atlas",
        "Problem & Literature",
        "Macro Strategies",
        "Strategy Judge",
        "Artifact-Or-Stop",
        "Story",
        "Branches",
        "Deep Reviews",
    ]
    completed_steps = list(runtime.DISCOVERY_STEP_FIELDS)
    step_results = {
        step: {field: f"Typed runtime evidence for {step}."}
        for step, field in runtime.DISCOVERY_STEP_FIELDS.items()
    }
    step_results["routing_assessment"] = {
        "disposition": "Promotable",
        "routing_basis": "The controlled checks support promotion to source validation.",
    }
    structured = {
        "final_disposition": {
            "status": "passed",
            "summary": "The complete reasoning graph ran to acceptance.",
            "reasoning_complete": True,
            "blockers": [],
            "completed_reasoning_steps": completed_steps,
            "limitations": ["Generated mathematical claims still require independent review."],
        },
        "reasoning_result": {
            "disposition": "Promotable",
            "routing_basis": "The controlled checks support promotion to source validation.",
        },
        "execution_provenance": {
            "request_digest": "a" * 64,
            "source_hash": "b" * 64,
            "module_hashes": {"material_main.prism": "c" * 64},
            "reasoning_event_count": 14,
        },
    }
    sections = runtime._discovery_sections(
        {"inputs": {"context_summary": "A bounded fixed-point discovery target."}},
        SimpleNamespace(step_results=step_results),
        structured,
    )
    markdown, layout = runtime._assemble_native_report(sections)
    latest_html = runtime._discovery_html(sections, "overview")
    timeline_html = runtime._discovery_html(sections, "timeline")
    runtime._validate_discovery_report(markdown, layout, latest_html, timeline_html)

    typed_report = {
        "version": "1",
        "report": {
            "id": "discovery-marathon-report",
            "title": "Discovery Marathon Report",
            "sections": [{
                "id": "discovery-sections",
                "kind": "tabs",
                "tabs": [
                    {
                        "id": slug,
                        "label": label,
                        "sections": [{
                            "id": slug + "-content",
                            "kind": "markdown",
                            "text": "Typed content for " + label,
                        }],
                    }
                    for (slug, label) in runtime.DISCOVERY_REPORT_SECTIONS
                ],
            }],
            "template": {
                "id": "abducer-discovery-marathon-v1",
                "title": "Discovery Marathon",
                "sections": [{
                    "id": "discovery-sections",
                    "kind": "tabs",
                    "tabs": [
                        {
                            "id": slug,
                            "sections": [{"id": slug + "-content", "kind": "markdown"}],
                        }
                        for slug, unused in runtime.DISCOVERY_REPORT_SECTIONS
                    ],
                }],
            },
        },
    }
    runtime._validate_typed_discovery_report(typed_report)

    assert [group["label"] for group in layout["groups"]] == expected_labels
    assert layout["schema_version"] == "lunar.native-report/v1"
    assert "import prism.reporting.report as r" in material
    assert "import prism.reporting.report as r" in reasoning
    assert "reasoning DiscoveryMarathonLoop(" in reasoning
    assert ") -> r.Report:" in reasoning
    assert "[typed_report: assemble_discovery_report_view(" in reasoning
    assert "return typed_report" in reasoning
    assert reasoning.count("[typed_report:") == 1
    assert ") -> r.Report\n" in material
    assert ") -> Result[r.Report, ModelFailure]" in material
    assert 'return r.Report(id="discovery-marathon-report"' in material
    assert registration["metadata"]["report_contract"]["presentation"] == "prism-typed-report/v1"
    assert registration["metadata"]["report_contract"]["terminal_output_type"] == (
        "prism.reporting.report.Report"
    )
    assert "typed-report.json" in registration["metadata"]["report_contract"][
        "required_artifacts"
    ]
    assert "typed_report" in registration["output_schema"]["properties"][
        "structured_value"
    ]["required"]
    assert latest_html.count('<button class="tab') == len(expected_labels)
    assert latest_html.count('<section class="panel') == len(expected_labels)
    assert 'class="panel active" data-panel="overview"' in latest_html
    assert 'class="panel active" data-panel="timeline"' in timeline_html
    for heading in (
        "## Final disposition",
        "## Completed reasoning steps",
        "## Typed reasoning result",
        "## Execution provenance",
        "## Interpretation and limits",
    ):
        assert heading in markdown

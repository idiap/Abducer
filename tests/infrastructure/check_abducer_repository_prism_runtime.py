# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Run all exported Abducer workflows in the real isolated Lunar worker.

The provider is deliberately schema-controlled, so this establishes transport,
typed-PRISM, reasoning-event, and report closure without claiming scientific quality.
Live-model UI evidence remains a separate release gate.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
import tempfile
from uuid import uuid4


def schema_value(schema, label="controlled evidence", variant_fields=None):
    """Produce the smallest deterministic value accepted by a model response schema."""
    if "const" in schema:
        return schema["const"]
    if "enum" in schema:
        return schema["enum"][0]
    options = schema.get("anyOf") or schema.get("oneOf")
    if options:
        non_null = next((row for row in options if row.get("type") != "null"), options[0])
        return schema_value(non_null, label, variant_fields)
    kind = schema.get("type")
    if kind == "object":
        required = schema.get("required", schema.get("properties", {}).keys())
        title_variants = (variant_fields or {}).get(schema.get("title"), {})
        return {
            name: (
                title_variants[name][0]
                if name in title_variants
                else schema_value(
                    schema["properties"][name], label + " for " + name, variant_fields
                )
            )
            for name in required
        }
    if kind == "array":
        count = max(1, schema.get("minItems", 0))
        return [schema_value(schema["items"], label, variant_fields) for _ in range(count)]
    if kind == "string":
        return label[: schema.get("maxLength", len(label))]
    if kind == "integer":
        return max(0, schema.get("minimum", 0))
    if kind == "number":
        return float(max(0, schema.get("minimum", 0)))
    if kind == "boolean":
        return False
    if kind == "null":
        return None
    raise AssertionError("Unhandled controlled schema: " + json.dumps(schema, sort_keys=True))


def packaged_variant_fields(package_root: Path):
    """Recover nominal variant constraints that Prism's provider schema omits."""
    result = {}
    for source in sorted(package_root.glob("repository/projects/*/prism_project/types.prism")):
        text = source.read_text(encoding="utf-8")
        blocks = {
            match.group(1): match.group(2)
            for match in re.finditer(
                r"(?ms)^type\s+(\w+):\s*\n(.*?)(?=^type\s+\w+:|\Z)", text
            )
        }
        variants = {
            name: re.findall(r"(?m)^\s*\|\s*(\w+)\s*$", body)
            for name, body in blocks.items()
        }
        for record, body in blocks.items():
            for field, field_type in re.findall(
                r"(?m)^\s+(\w+):\s*(\w+)\s*$", body
            ):
                if variants.get(field_type):
                    for output_record in (record, "Material" + record):
                        result.setdefault(output_record, {})[field] = variants[field_type]
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--lunar-root", type=Path, required=True)
    parser.add_argument("--image", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--typed-report-output",
        type=Path,
        help="Optional durable copy of Discovery Marathon's decoded typed Report payload.",
    )
    args = parser.parse_args()

    sys.path.insert(0, str(args.lunar_root.resolve() / "app/backend"))
    from domain_packages.archive import ArchiveLimits, validate_archive
    from domain_packages.format.source_workflows import derive
    from domain_packages.worker.results import validate_worker_result
    from domain_packages.worker.sandbox import WorkerLimits
    from domain_packages.worker.transport import invoke_worker
    from jsonschema import Draft202012Validator
    from prism_stdlib.report_codec import decode_report

    receipts = []
    with tempfile.TemporaryDirectory(prefix="abducer-repository-worker-") as raw:
        root = Path(raw)
        archive = validate_archive(args.archive.resolve(), root / "package", ArchiveLimits())
        payloads = {
            row["path"]: (archive.root / row["path"]).read_bytes()
            for row in archive.manifest["files"]
        }
        unused_bundle, registrations = derive(
            archive.manifest, payloads, archive.documents["repository"]
        )
        workflows = sorted(registrations, key=lambda row: row["id"])
        assert len(workflows) == 19
        variant_fields = packaged_variant_fields(archive.root)

        for workflow in workflows:
            calls = []

            def model(arguments):
                schema = arguments["response_format"]["json_schema"]["schema"]
                messages = json.dumps(arguments["messages"])
                scalar_choices = re.search(
                    r"The (?:entire )?value must be exactly one of: `([^`]+)`",
                    messages,
                )
                if scalar_choices and set(schema.get("properties", {})) == {"value"}:
                    reply = {"value": scalar_choices.group(1)}
                else:
                    reply = schema_value(
                        schema, "controlled source-grounded assessment", variant_fields
                    )
                Draft202012Validator(schema).validate(reply)
                calls.append({"schema": schema, "reply": reply})
                return {"choices": [{"message": {"content": json.dumps(reply)}}]}

            output = root / "runs" / workflow["id"]
            output.mkdir(parents=True)
            request = {
                "contract_version": 1,
                "request_id": str(uuid4()),
                "operation": "execute",
                "workflow_id": workflow["id"],
                "hook_id": None,
                "input": {"mode": "run", "inputs": workflow["input_schema"]["default"]},
                "authority": {"network": False, "model_access": True},
            }
            result = invoke_worker(
                image=args.image,
                package_root=archive.root,
                run_root=output,
                manifest=archive.manifest,
                request=request,
                model_handler=model,
                model_snapshot={"provider": "controlled-test", "model_id": "schema-responder"},
                limits=WorkerLimits(timeout_seconds=300),
            )
            validate_worker_result(result, request, output)
            assert result["status"] == "succeeded", (
                workflow["id"],
                result["error"],
                calls,
                result.get("events"),
            )
            Draft202012Validator(workflow["output_schema"]).validate(result["result"])
            structured = result["result"]["structured_value"]
            assert structured["final_disposition"]["status"] == "passed"
            assert structured["final_disposition"]["reasoning_complete"] is True
            assert structured["final_disposition"]["blockers"] == []
            expected_steps = structured["final_disposition"]["completed_reasoning_steps"]
            expected_model_steps = [step for step in expected_steps if step != "typed_report"]
            assert len(calls) == len(expected_model_steps)
            assert structured["execution_provenance"]["reasoning_event_count"] >= len(calls) * 2
            expected_agents = workflow["metadata"]["provenance_contract"][
                "agent_invocations"
            ]
            agent_events = [
                event["payload"]["detail"]
                for event in result["events"]
                if event["kind"] == "stage"
                and event["payload"].get("detail", {}).get("event_kind")
                == "agent-invoked"
            ]
            assert [
                {
                    "agent_name": row["agent_name"],
                    "workflow_occurrence": row["workflow_occurrence"],
                    "activated_skill_ids": row["activated_skill_ids"],
                }
                for row in agent_events
            ] == expected_agents
            assert all(row["effect_record_id"] for row in agent_events)
            assert structured["execution_provenance"]["agent_invocations"] == agent_events
            source_events = [event for event in result["events"] if event["kind"] == "source"]
            assert source_events == []
            assert workflow["metadata"]["provenance_contract"][
                "required_source_reads"
            ] == []
            artifact_paths = {row["path"] for row in result["artifacts"]}
            assert {"report.md", "result.json"} <= artifact_paths
            if workflow["id"] == "discovery_marathon_loop":
                assert expected_steps[-1] == "typed_report"
                assert len(expected_steps) == 8
                expected_sections = [
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
                assert {
                    "report.md",
                    "result.json",
                    "latest.md",
                    "latest.json",
                    "latest.html",
                    "full_timeline.html",
                    "typed-report.json",
                } <= artifact_paths
                assert structured["report_contract"] == {
                    "schema_version": "abducer.discovery-marathon-report/v1",
                    "presentation": "prism-typed-report/v1",
                    "terminal_output_type": "prism.reporting.report.Report",
                    "compatibility": "repository-section-compatible",
                    "required_sections": expected_sections,
                    "artifacts": [
                        "report.md",
                        "result.json",
                        "latest.md",
                        "latest.json",
                        "latest.html",
                        "full_timeline.html",
                    ],
                    "typed_report_artifact": "typed-report.json",
                }
                typed_report = structured["typed_report"]
                decode_report(typed_report, attachments={})
                if args.typed_report_output:
                    args.typed_report_output.parent.mkdir(parents=True, exist_ok=True)
                    args.typed_report_output.write_text(
                        json.dumps(typed_report, indent=2) + "\n", encoding="utf-8"
                    )
                typed_tabs = typed_report["report"]["sections"][0]
                assert typed_tabs["kind"] == "tabs"
                assert [tab["label"] for tab in typed_tabs["tabs"]] == expected_sections
                assert [
                    group["label"] for group in structured["report_layout"]["groups"]
                ] == expected_sections
                assert result["result"]["analysis_results"]["report_type"] == (
                    "prism.reporting.report.Report"
                )
                assert "prism_typed_report" in result["result"]["report_verification"][
                    "checks"
                ]
                assert result["result"]["report_verification"][
                    "repository_report_compatible"
                ] is True
            receipts.append(
                {
                    "workflow_id": workflow["id"],
                    "status": result["status"],
                    "model_calls": len(calls),
                    "reasoning_events": structured["execution_provenance"]["reasoning_event_count"],
                    "agent_invocations": len(agent_events),
                    "source_reads": len(source_events),
                    "artifacts": [row["path"] for row in result["artifacts"]],
                }
            )

        failed_root = root / "failure-probe"
        failed_root.mkdir()
        probe = workflows[0]
        bad_inputs = {**probe["input_schema"]["default"], "undeclared": "reject"}
        bad_request = {
            "contract_version": 1,
            "request_id": str(uuid4()),
            "operation": "execute",
            "workflow_id": probe["id"],
            "hook_id": None,
            "input": {"mode": "run", "inputs": bad_inputs},
            "authority": {"network": False, "model_access": True},
        }
        failed = invoke_worker(
            image=args.image,
            package_root=archive.root,
            run_root=failed_root,
            manifest=archive.manifest,
            request=bad_request,
            model_handler=lambda unused: (_ for _ in ()).throw(AssertionError("model must not run")),
            model_snapshot={"provider": "controlled-test", "model_id": "failure-probe"},
            limits=WorkerLimits(timeout_seconds=120),
        )
        validate_worker_result(failed, bad_request, failed_root)
        assert failed["status"] == "failed" and failed["result"] is None

        evidence = {
            "kind": "controlled-provider-all-workflow-integration",
            "archive_sha256": archive.archive_digest,
            "image": args.image,
            "workflow_count": len(receipts),
            "workflows": receipts,
            "failure_probe": {"workflow_id": probe["id"], "status": failed["status"], "error": failed["error"]},
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"status": "pass", "workflow_count": len(receipts), "failure_probe": "pass"}))


if __name__ == "__main__":
    main()

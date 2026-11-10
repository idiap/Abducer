# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Prepare and audit real model-authored workflow content experiments.

This module never fabricates candidate prose or semantic scores. It supplies
sealed, source-bound author packets, exposes oracles only to separate judges,
and checks the resulting coverage and evidence. Generation/judgment is performed
by session agents (or a separately documented external adapter). Passing this
auditor establishes record integrity, not native workflow execution or truth.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import html
import json
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).with_name("fixtures")
MODE = "session_content_exercise"


class EvaluationError(ValueError):
    """Reject detached evidence or falsely complete coverage."""


def read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n")


def indexed(rows: list[dict], key: str, label: str) -> dict[str, dict]:
    result = {}
    for row in rows:
        identifier = row.get(key)
        if not isinstance(identifier, str) or not identifier or identifier in result:
            raise EvaluationError(f"{label}: missing/duplicate {key}")
        result[identifier] = row
    return result


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise EvaluationError(reason)


def prepare(output: Path, *, root: Path = ROOT, fixtures: Path = FIXTURES) -> dict:
    """Freeze inputs and actual skill instructions without leaking oracles."""
    require(not (output / "manifest.json").exists(), "refuse to overwrite a prepared run")
    inventory = read(fixtures / "workflow_content_inventory.json")
    cases = read(fixtures / "workflow_content_cases.json")
    rubric = read(fixtures / "workflow_content_rubric.json")
    controls = read(fixtures / "workflow_content_controls.json")
    workflows = indexed(inventory["workflows"], "workflow_id", "inventory")
    case_rows = indexed(cases["cases"], "case_id", "cases")
    catalog = read(root / inventory["catalog_path"])
    require(set(workflows) == {row["id"] for row in catalog["flows"]}, "catalog coverage differs")
    require({row["workflow_id"] for row in case_rows.values()} == set(workflows), "missing workflow cases")
    snapshots = {inventory["catalog_path"]: hashlib.sha256(
        (root / inventory["catalog_path"]).read_bytes()).hexdigest()}
    for workflow in workflows.values():
        indexed(workflow["steps"], "step_id", workflow["workflow_id"])
        paths = set(workflow["source_paths"]) | {step["skill_path"] for step in workflow["steps"]}
        paths |= {step["source_path"] for step in workflow["steps"]}
        for relative in paths:
            path = (root / relative).resolve()
            require(path.is_relative_to(root.resolve()) and path.is_file(), f"invalid source: {relative}")
            snapshots[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    packets, judge_packets = {}, {}
    for case_id, case in case_rows.items():
        require(all(char.isalnum() or char in "_-" for char in case_id), "unsafe case ID")
        workflow = workflows[case["workflow_id"]]
        packet = {
            "schema_version": 1, "case_id": case_id, "workflow_id": case["workflow_id"],
            "execution_mode": MODE,
            "scenario": {key: case[key] for key in ("scenario", "input_facts", "task")},
            "workflow": workflow,
            "skill_instructions": {step["skill_path"]: (root / step["skill_path"]).read_text()
                                   for step in workflow["steps"]},
            "source_digests": {path: snapshots[path] for path in set(workflow["source_paths"]) |
                               {step["skill_path"] for step in workflow["steps"]} |
                               {step["source_path"] for step in workflow["steps"]}},
            "instructions": (
                "Produce substantive case-specific content for every listed binding using its actual skill instructions. "
                "Use upstream generated work where declared dependencies require it. Preserve different branches and "
                "profiles as separate content exercises; never concatenate an alternative profile into a native run. "
                "Unknown runtime order remains unknown. If a required input is absent, produce a useful precise "
                "partial artifact and identify the missing premise. Never invent execution, literature, receipts or proofs. "
                "Finish with a coherent bounded whole-workflow synthesis, not just a list of status labels. "
                "No tools may mutate production state or activate hooks. All outputs stay in this evaluation run."
            ),
        }
        packet["packet_sha256"] = digest(packet)
        packets[case_id] = packet["packet_sha256"]
        write(output / "author_packets" / f"{case_id}.json", packet)
        judge_packet = {
            "author_packet": packet, "oracle": case, "rubric": rubric,
            "instruction": "Independently judge every actual step and final synthesis. Quote content and test warrants; do not reward labels or polish."
        }
        judge_packets[case_id] = digest(judge_packet)
        write(output / "judge_packets" / f"{case_id}.json", judge_packet)
    write(output / "controls/packet.json", controls["packet"])
    write(output / "controls/answer-key.json", controls["answer_key"])
    manifest = {
        "schema_version": 1, "execution_mode": MODE, "inventory": inventory,
        "case_ids": list(case_rows), "packets": packets, "judge_packets": judge_packets,
        "case_workflows": {case_id: case["workflow_id"] for case_id, case in case_rows.items()},
        "source_digests": snapshots,
        "cases_sha256": digest(cases), "rubric": rubric,
        "control_digests": {"packet.json": digest(controls["packet"]),
                            "answer-key.json": digest(controls["answer_key"])},
        "generation_status": "awaiting_real_author_and_judge_outputs",
    }
    write(output / "manifest.json", manifest)
    return manifest


def validate_candidate(candidate: dict, packet: dict) -> dict[str, dict]:
    require(candidate.get("execution_mode") == MODE, "wrong candidate execution claim")
    for key in ("case_id", "workflow_id", "packet_sha256"):
        require(candidate.get(key) == packet[key], f"candidate {key} mismatch")
    require(bool(candidate.get("author_session")), "missing real author task identity")
    rows = indexed(candidate.get("steps", []), "step_id", "candidate steps")
    expected = indexed(packet["workflow"]["steps"], "step_id", "packet steps")
    require(set(rows) == set(expected), "missing/extra candidate steps")
    sources = {fact["source_id"] for fact in packet["scenario"]["input_facts"]}
    for step_id, row in rows.items():
        require(row.get("skill_id") == expected[step_id]["skill"], "step skill binding differs")
        require(isinstance(row.get("content"), str) and bool(row["content"].strip()), "empty content")
        refs = row.get("input_refs", [])
        require(isinstance(refs, list) and bool(refs), "missing step inputs")
        for ref in refs:
            require(ref in sources or (ref in rows and ref != step_id), f"unknown input reference: {ref}")
        in_scope_dependencies = set(expected[step_id].get("depends_on", [])) & set(rows)
        require(in_scope_dependencies <= set(refs), "declared in-scope DAG dependency is not cited")
    final = candidate.get("final", {})
    require(isinstance(final.get("content"), str) and bool(final["content"].strip()), "missing final synthesis")
    require(isinstance(final.get("unresolved_obligations"), list), "missing final proof-debt list")
    return rows


def extend_cases(run: Path, *, root: Path = ROOT, fixtures: Path = FIXTURES) -> dict:
    """Add refinement probes only when every existing packet remains identical."""
    previous = read(run / "manifest.json")
    with tempfile.TemporaryDirectory(prefix="workflow-content-extension-") as directory:
        staging = Path(directory)
        proposed = prepare(staging, root=root, fixtures=fixtures)
        require(set(previous["case_ids"]) <= set(proposed["case_ids"]), "extension removed a case")
        for case_id in previous["case_ids"]:
            require(previous["packets"][case_id] == proposed["packets"][case_id] and
                    previous["judge_packets"][case_id] == proposed["judge_packets"][case_id],
                    "extension would alter previously authored or judged input")
        for filename, expected in proposed["control_digests"].items():
            require(digest(read(run / "controls" / filename)) == expected,
                    "extension would change existing judge controls")
        additions = [case_id for case_id in proposed["case_ids"] if case_id not in previous["case_ids"]]
        for case_id in additions:
            for folder in ("author_packets", "judge_packets"):
                write(run / folder / f"{case_id}.json", read(staging / folder / f"{case_id}.json"))
        proposed["extensions"] = previous.get("extensions", []) + [{
            "previous_manifest_sha256": digest(previous), "added_cases": additions,
            "reason": "Explicit refinement probes; existing evidence retained byte-for-byte"}]
        write(run / "manifest.json", proposed)
    return proposed


def content_verdict(dimensions: dict, gates: dict) -> str:
    if any(not value for value in gates.values()) or any(value == 0 for value in dimensions.values()):
        return "fail"
    return "pass" if all(value == 2 for value in dimensions.values()) else "partial"


def validate_assessment(row: dict, *, content: str, dimensions: set[str], gates: set[str],
                        allowed_refs: set[str] | None = None) -> None:
    """Check scored evidence coverage; semantic relevance belongs to the judge."""
    scores = row.get("dimensions", {})
    checks = row.get("gates", {})
    require(set(scores) == dimensions and set(checks) == gates, "incomplete evaluation criteria")
    require(all(type(value) is int and value in (0, 1, 2) for value in scores.values()), "invalid score")
    require(all(type(value) is bool for value in checks.values()), "invalid gate")
    covered_dimensions, covered_gates = set(), set()
    for evidence in row.get("evidence", []):
        quote = evidence.get("output_quote")
        if quote is None:
            require(bool(evidence.get("searched_scope")) and bool(evidence.get("missing_obligation")), "unsupported omission claim")
        else:
            require(isinstance(quote, str) and bool(quote) and quote in content, "quote absent from output")
        require(bool(evidence.get("reason")) and bool(evidence.get("source_refs")), "unreasoned evidence")
        if allowed_refs is not None:
            require(isinstance(evidence["source_refs"], list) and
                    all(ref in allowed_refs for ref in evidence["source_refs"]), "unknown judgment source reference")
        covered_dimensions.update(evidence.get("dimensions", []))
        covered_gates.update(evidence.get("gates", []))
    require(covered_dimensions == dimensions and covered_gates == gates, "uncovered/unknown criterion evidence")
    require(row.get("verdict") == content_verdict(scores, checks), "verdict contradicts scores/gates")


def validate_judgment(judgment: dict, candidate: dict, packet: dict, rubric: dict) -> str:
    require(judgment.get("candidate_sha256") == digest(candidate), "judge evaluated different candidate bytes")
    require(judgment.get("execution_mode") == MODE, "wrong judge execution claim")
    for key in ("case_id", "workflow_id"):
        require(judgment.get(key) == candidate[key], f"judge {key} mismatch")
    require(bool(judgment.get("judge_session")) and judgment["judge_session"] != candidate["author_session"], "author cannot judge own candidate")
    outputs = validate_candidate(candidate, packet)
    rows = indexed(judgment.get("steps", []), "step_id", "judged steps")
    require(set(rows) == set(outputs), "missing/extra step judgments")
    gates = set(rubric["noncompensatory_gates"])
    allowed_refs = {fact["source_id"] for fact in packet["scenario"]["input_facts"]} | set(outputs)
    allowed_refs |= set(packet.get("source_digests", {}))
    for step_id, row in rows.items():
        require(row.get("skill_id") == outputs[step_id]["skill_id"], "judge skill mismatch")
        validate_assessment(row, content=outputs[step_id]["content"],
                            dimensions=set(rubric["step_dimensions"]), gates=gates, allowed_refs=allowed_refs)
    whole = judgment.get("workflow", {})
    full_content = "\n".join(row["content"] for row in outputs.values()) + "\n" + candidate["final"]["content"]
    validate_assessment(whole, content=full_content, dimensions=set(rubric["workflow_dimensions"]), gates=gates, allowed_refs=allowed_refs)
    require(isinstance(whole.get("accepted_claims"), list) and
            isinstance(whole.get("unresolved_obligations"), list) and bool(whole.get("claim_scope")), "missing whole-workflow interpretation")
    verdicts = [row["verdict"] for row in rows.values()] + [whole["verdict"]]
    return "fail" if "fail" in verdicts else "partial" if "partial" in verdicts else "pass"


def audit(run: Path, *, root: Path = ROOT) -> dict:
    """Report all missing/invalid/content-failing records without hiding them."""
    manifest = read(run / "manifest.json")
    workflows = indexed(manifest["inventory"]["workflows"], "workflow_id", "manifest workflows")
    case_ids = manifest["case_ids"]
    require(bool(case_ids) and len(case_ids) == len(set(case_ids)), "empty/duplicate manifest cases")
    require(set(case_ids) == set(manifest["packets"]) == set(manifest["judge_packets"]) ==
            set(manifest["case_workflows"]), "manifest case accounting differs")
    require(set(manifest["case_workflows"].values()) == set(workflows), "manifest omits workflow coverage")
    changed_sources = [relative for relative, expected in manifest["source_digests"].items()
                       if not (root / relative).is_file() or hashlib.sha256((root / relative).read_bytes()).hexdigest() != expected]
    results = []
    for case_id in case_ids:
        workflow_id = manifest["case_workflows"][case_id]
        row = {"case_id": case_id, "workflow_id": workflow_id,
               "expected_steps": len(workflows[workflow_id]["steps"])}
        try:
            packet = read(run / "author_packets" / f"{case_id}.json")
            require(packet["workflow_id"] == workflow_id and packet["workflow"] == workflows[workflow_id],
                    "author workflow differs from inventory")
            require(digest({k: v for k, v in packet.items() if k != "packet_sha256"}) == manifest["packets"][case_id] == packet["packet_sha256"], "author packet changed")
            judge_packet = read(run / "judge_packets" / f"{case_id}.json")
            require(digest(judge_packet) == manifest["judge_packets"][case_id], "judge oracle packet changed")
            require(judge_packet["author_packet"] == packet and judge_packet["rubric"] == manifest["rubric"], "judge context detached")
            candidate_path = run / "candidates" / f"{case_id}.json"
            judge_path = run / "judgments" / f"{case_id}.json"
            if not candidate_path.exists() or not judge_path.exists():
                row.update(status="unexecuted", missing=[kind for kind, path in (("candidate", candidate_path), ("judgment", judge_path)) if not path.exists()])
            else:
                candidate, judgment = read(candidate_path), read(judge_path)
                verdict = validate_judgment(judgment, candidate, packet, manifest["rubric"])
                row.update(status="evaluated", content_verdict=verdict,
                           judge_session=judgment["judge_session"],
                           step_verdicts={step["step_id"]: step["verdict"] for step in judgment["steps"]},
                           workflow_verdict=judgment["workflow"]["verdict"])
        except (EvaluationError, ValueError, TypeError, KeyError, OSError, AttributeError) as exc:
            row.update(status="invalid_evidence", error=str(exc))
        results.append(row)
    controls = audit_controls(run, {row["judge_session"] for row in results if row["status"] == "evaluated"},
                              manifest["rubric"], expected_digests=manifest["control_digests"])
    applicability = audit_applicability(run, manifest)
    report = {
        "execution_mode": MODE, "workflow_count": len(manifest["inventory"]["workflows"]),
        "case_count": len(results), "expected_step_assessments": sum(row["expected_steps"] for row in results),
        "evaluated_cases": sum(row["status"] == "evaluated" for row in results),
        "evaluated_step_assessments": sum(row["expected_steps"] for row in results if row["status"] == "evaluated"),
        "case_verdict_counts": dict(Counter(row["content_verdict"] for row in results if row["status"] == "evaluated")),
        "step_verdict_counts": dict(Counter(verdict for row in results for verdict in row.get("step_verdicts", {}).values())),
        "workflow_verdict_counts": dict(Counter(row["workflow_verdict"] for row in results if row["status"] == "evaluated")),
        "source_changes": changed_sources,
        "coverage_complete": not changed_sources and all(row["status"] == "evaluated" for row in results),
        "cases": results,
        "judge_controls": controls,
        "conditional_applicability": applicability,
        "evaluation_complete": not changed_sources and all(row["status"] == "evaluated" for row in results) and controls["complete"] and applicability["complete"],
        "coverage_gaps": {workflow["workflow_id"]: workflow.get("coverage_gaps", [])
                          for workflow in manifest["inventory"]["workflows"]},
        "limitations": ["Session content exercises are not native workflow execution.",
                        "Semantic judgments are model assessments, not theorem certification.",
                        "Source-declared coverage gaps remain in the inventory.",
                        "Judge sensitivity controls and disagreements require separate reporting."],
    }
    write(run / "report.json", report)
    render_report(run, report)
    return report


def validate_applicability_row(row: dict, candidate: dict, packet: dict, binding: dict) -> None:
    """Keep a good guard explanation separate from active scientific content."""
    require(row["candidate_sha256"] == digest(candidate), "applicability candidate changed")
    require(row["condition"] == binding["when"], "applicability condition changed")
    require(row["workflow_id"] == packet["workflow_id"], "applicability workflow differs")
    output = next(step for step in candidate["steps"] if step["step_id"] == row["step_id"])
    require(bool(row["output_quote"]) and row["output_quote"] in output["content"], "applicability quote absent")
    allowed = {fact["source_id"] for fact in packet["scenario"]["input_facts"]} | set(packet["source_digests"]) | {step["step_id"] for step in candidate["steps"]}
    require(bool(row["reason"]) and bool(row["source_refs"]) and set(row["source_refs"]) <= allowed,
            "applicability lacks source-grounded reasoning")
    scopes = {"active": "substantive_conditional_content", "inactive": "guard_decision", "unknown": "conditional_proposal"}
    status = row["condition_status"]
    require(status in scopes and row["assessment_scope"] == scopes[status], "wrong applicability scope")
    score = row["content_score"]
    require((type(score) is int and score in (0, 1, 2)) if status == "active" else score is None,
            "inactive/unknown scientific content must be null; active content needs a score")
    require(row.get("native_execution") is False, "applicability cannot imply native execution")


def audit_applicability(run: Path, manifest: dict) -> dict:
    """Require evidence for every guard and a positive probe for each binding."""
    workflows = {row["workflow_id"]: row for row in manifest["inventory"]["workflows"]}
    expected = {(case_id, step["step_id"]): step for case_id, workflow_id in manifest["case_workflows"].items()
                for step in workflows[workflow_id]["steps"] if step.get("when")}
    seen, active, counts, errors = set(), set(), Counter(), []
    valid_manifests = {digest(manifest)} | {row["previous_manifest_sha256"] for row in manifest.get("extensions", [])}
    for path in sorted(run.glob("conditional-applicability*.json")):
        try:
            review = read(path)
            require(review["manifest_sha256"] in valid_manifests and bool(review["reviewer_session"]), "detached applicability review")
            for row in review["rows"]:
                key = (row["case_id"], row["step_id"])
                require(key in expected and key not in seen, "extra/duplicate applicability row")
                packet = read(run / "author_packets" / f"{key[0]}.json")
                candidate = read(run / "candidates" / f"{key[0]}.json")
                require(review["reviewer_session"] != candidate["author_session"], "author cannot assess own applicability")
                validate_applicability_row(row, candidate, packet, expected[key])
                seen.add(key)
                counts[row["condition_status"]] += 1
                if row["condition_status"] == "active":
                    active.add((row["workflow_id"], row["step_id"]))
        except (EvaluationError, ValueError, TypeError, KeyError, OSError, StopIteration) as exc:
            errors.append({"path": path.name, "error": str(exc)})
    bindings = {(manifest["case_workflows"][case_id], step_id) for case_id, step_id in expected}
    return {"complete": not errors and seen == set(expected) and active == bindings,
            "expected_rows": len(expected), "evaluated_rows": len(seen), "status_counts": dict(counts),
            "guarded_binding_count": len(bindings), "positively_probed_bindings": len(active),
            "missing_rows": sorted(set(expected) - seen), "bindings_without_positive_probe": sorted(bindings - active),
            "errors": errors}


def audit_controls(run: Path, judge_sessions: set[str], rubric: dict, *, expected_digests: dict | None = None) -> dict:
    """Require each actual judge to handle hidden negative and positive probes."""
    packet_path, key_path = run / "controls/packet.json", run / "controls/answer-key.json"
    if not packet_path.exists() or not key_path.exists():
        return {"complete": False, "reason": "judge sensitivity controls not recorded"}
    try:
        packet, key = read(packet_path), read(key_path)
        if expected_digests is not None:
            require(expected_digests == {"packet.json": digest(packet), "answer-key.json": digest(key)},
                    "judge control packet or answer key changed")
        expected = key["expected"]
    except (EvaluationError, ValueError, TypeError, KeyError, OSError) as exc:
        return {"complete": False, "reason": str(exc)}
    records = indexed(packet["records"], "control_id", "control packet")
    if (not records or set(records) != set(expected) or
            not any(row.get("all_gates_pass") is True for row in expected.values()) or
            not any(row.get("failed_gate") for row in expected.values())):
        return {"complete": False, "reason": "controls need complete positive and negative oracles",
                "missing_judges": sorted(judge_sessions)}
    observed, failures = {}, []
    for path in (run / "controls/judgments").glob("*.json"):
        try:
            judgment = read(path)
            session = judgment["judge_session"]
            require(session not in observed, "duplicate control judgment session")
            require(judgment.get("packet_sha256") == digest(packet), "control packet binding mismatch")
            rows = indexed(judgment["evaluations"], "control_id", "control judgments")
            require(set(rows) == set(records), "missing control judgment")
            calibrated = True
            for control_id, row in rows.items():
                source = records[control_id]
                validate_assessment(row, content=source["content"], dimensions=set(),
                                    gates=set(rubric["noncompensatory_gates"]),
                                    allowed_refs={fact["source_id"] for fact in source["source_facts"]})
                answer = expected[control_id]
                if answer.get("all_gates_pass"):
                    calibrated &= all(row["gates"].values())
                else:
                    calibrated &= row["gates"][answer["failed_gate"]] is False
            observed[session] = {"calibrated": calibrated, "path": path.relative_to(run).as_posix()}
        except (EvaluationError, KeyError, TypeError, ValueError) as exc:
            failures.append({"path": path.relative_to(run).as_posix(), "error": str(exc)})
    return {"complete": bool(judge_sessions) and not failures and
            all(observed.get(session, {}).get("calibrated") is True for session in judge_sessions),
            "judges": observed, "errors": failures,
            "missing_judges": sorted(judge_sessions - set(observed))}


def render_report(run: Path, report: dict) -> None:
    """Expose actual content/verdicts in a self-contained expandable report."""
    title = "Generative workflow content evaluation"
    summary = (f"{report['evaluated_cases']}/{report['case_count']} cases and "
               f"{report['evaluated_step_assessments']}/{report['expected_step_assessments']} "
               "step assessments recorded. Execution mode: isolated session content exercise.")
    if "case_verdict_counts" in report:
        summary += (f" Case outcomes: {report['case_verdict_counts']}. "
                    f"Step outcomes: {report['step_verdict_counts']}. "
                    f"Whole-workflow outcomes: {report['workflow_verdict_counts']}. "
                    f"Judge controls complete: {report['judge_controls']['complete']}.")
        conditional = report["conditional_applicability"]
        summary += (f" Conditional assessments: {conditional['evaluated_rows']}/{conditional['expected_rows']}; "
                    f"active-branch probes: {conditional['positively_probed_bindings']}/{conditional['guarded_binding_count']}.")
    markdown = [f"# {title}", "", summary, "",
                "| Workflow case | Coverage | Content verdict | Steps |",
                "| --- | --- | --- | --- |"]
    sections = []
    for row in report["cases"]:
        case_id = row["case_id"]
        verdict = row.get("content_verdict", "not judged")
        markdown.append(f"| {case_id} | {row['status']} | {verdict} | {row['expected_steps']} |")
        parts = [f"<details><summary>{html.escape(case_id)} — {html.escape(verdict)}</summary>"]
        candidate_path = run / "candidates" / f"{case_id}.json"
        judgment_path = run / "judgments" / f"{case_id}.json"
        candidate = None
        if candidate_path.exists():
            try:
                candidate = read(candidate_path)
                validate_candidate(candidate, read(run / "author_packets" / f"{case_id}.json"))
            except (EvaluationError, KeyError, TypeError, ValueError, OSError, AttributeError):
                candidate = None
        if candidate is not None:
            # Invalid evidence must remain visibly invalid, never reappear as
            # trusted scores (or crash rendering) after the audit rejected it.
            judgments = read(judgment_path) if row["status"] == "evaluated" else {}
            assessed = {step.get("step_id"): step for step in judgments.get("steps", [])}
            for step in candidate.get("steps", []):
                evaluation = assessed.get(step["step_id"], {})
                parts.append(f"<details><summary>{html.escape(step['step_id'])} — {html.escape(evaluation.get('verdict', 'not judged'))}</summary>")
                parts.append(f"<p>{html.escape(step['content'])}</p>")
                if evaluation:
                    parts.append("<pre>" + html.escape(json.dumps(evaluation, indent=2, ensure_ascii=False)) + "</pre>")
                parts.append("</details>")
            parts.append("<h3>Whole workflow</h3><p>" + html.escape(candidate["final"]["content"]) + "</p>")
            parts.append("<pre>" + html.escape(json.dumps(judgments.get("workflow", {}), indent=2, ensure_ascii=False)) + "</pre>")
        if row.get("error"):
            parts.append("<p>Invalid evidence: " + html.escape(row["error"]) + "</p>")
        parts.append("</details>")
        sections.extend(parts)
    markdown += ["", "## Interpretation", ""] + [f"- {text}" for text in report["limitations"]]
    supplements = [name for name in ("conditional-applicability.json", "conditional-applicability-additions.json",
                                     "secondary-c-review.md", "adjudication.json", "findings.md") if (run / name).exists()]
    if supplements:
        markdown += ["", "## Supplemental reviews", ""] + [f"- [{name}]({name})" for name in supplements]
        sections.append("<h2>Supplemental reviews</h2><p>Primary scores above are preserved. Read applicability and adjudication before interpreting disputed failures.</p><ul>" +
                        "".join(f'<li><a href="{html.escape(name)}">{html.escape(name)}</a></li>' for name in supplements) + "</ul>")
    (run / "report.md").write_text("\n".join(markdown) + "\n")
    (run / "report.html").write_text(
        "<!doctype html><html lang='en'><meta charset='utf-8'><meta name='viewport' content='width=device-width'>"
        "<title>Workflow content evaluation</title><style>body{font:16px system-ui;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#17202a}"
        "summary{cursor:pointer;padding:.7rem;background:#edf2f7;border-radius:4px}details{margin:.6rem 0}details details{margin-left:1rem}"
        "p{line-height:1.6;white-space:pre-wrap}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f7f8fa;padding:1rem;font-size:13px}</style>"
        f"<h1>{title}</h1><p>{html.escape(summary)}</p>" + "\n".join(sections) +
        "<h2>Limits</h2><ul>" + "".join("<li>" + html.escape(item) + "</li>" for item in report["limitations"]) + "</ul></html>"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "extend", "audit"))
    parser.add_argument("run", type=Path)
    args = parser.parse_args()
    result = prepare(args.run) if args.command == "prepare" else extend_cases(args.run) if args.command == "extend" else audit(args.run)
    print(json.dumps({key: value for key, value in result.items() if key not in {"inventory", "source_digests", "rubric", "packets", "cases"}}, indent=2))
    if args.command in {"prepare", "extend"}:
        return 0
    if not result["evaluation_complete"]:
        return 1
    return 0 if all(row.get("content_verdict") == "pass" for row in result["cases"]) else 2


if __name__ == "__main__":
    raise SystemExit(main())

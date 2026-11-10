# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Register selectable source marathons and their original HTML reports.

The Prism source remains the viewer entry, while execute_hook is the explicit
native execution contract. Hosts without that extension reject this package.
"""
from __future__ import annotations

WORKFLOW_ID = "discovery_marathon_loop"
ENTRY_FILE = "repository/runtime/abducer-prism/lunar_discovery.prism"
HOOK_FILE = "repository/runtime/integrations/domain_package/marathon_runtime.py"
INPUT_SCHEMA = {"type": "object", "additionalProperties": False,
                "required": ["target_id", "run_id"],
                "properties": {key: {"type": "string", "minLength": 1}
                               for key in ("target_id", "run_id")}}


def registration(runs: list[dict] | None = None) -> dict:
    """Constrain the form and server to exact target/run pairs in the snapshot."""
    import copy
    schema = copy.deepcopy(INPUT_SCHEMA)
    if runs:
        targets = sorted({run["target_id"] for run in runs})
        for key in ("target_id", "run_id"):
            schema["properties"][key]["enum"] = sorted({run[key] for run in runs})
        schema["allOf"] = [
            {"if": {"properties": {"target_id": {"const": target}}},
             "then": {"properties": {"run_id": {"enum": [run["run_id"] for run in runs if run["target_id"] == target]}}}}
            for target in targets]
    return {
        "id": WORKFLOW_ID, "repository_id": "workflow-discovery-marathon-loop",
        "name": "Discovery Marathon Loop", "entry_file": ENTRY_FILE, "entry_argument": "context",
        "input_schema": schema,
        "output_schema": {
            "type": "object", "required": ["markdown", "structured_value", "report_verification"],
            "properties": {
                "markdown": {"type": "string", "minLength": 1},
                "structured_value": {"type": "object", "required": ["target_id", "run_id", "cycle_count", "html_report", "runner_sha256"],
                    "properties": {
                        "target_id": {"type": "string", "minLength": 1},
                        "run_id": {"type": "string", "minLength": 1},
                        "cycle_count": {"type": "integer", "minimum": 0},
                        "execution_outcome": {"enum": ["research_cycle_completed", "initialization_requires_revision"]},
                        "html_report": {"type": "object", "required": ["path", "sha256", "media_type"],
                            "properties": {"path": {"const": "full_timeline.html"}, "sha256": {"type": "string", "pattern": "^[a-f0-9]{64}$"}, "media_type": {"const": "text/html"}}}}},
                "report_verification": {"type": "object", "required": ["status", "scientific_truth_verified"],
                    "properties": {"status": {"const": "passed"}, "scientific_truth_verified": {"const": False}}}}},
        "prepare_hook": "abducer-prepare", "execute_hook": "abducer-execute", "verify_hook": "abducer-verify", "modes": ["live"],
        "metadata": {"viewer_workflow_id": WORKFLOW_ID, "model_required": True,
                     "description": "Select a target and run, execute one authorized source cycle, and view the full discovery report.",
                     "marathon_runs": [{key: run[key] for key in ("target_id", "run_id", "cycle_count", "readiness")}
                                       for run in (runs or [])],
                     "execution_scope": "source research runner with automatic canonical initialization for new runs",
                     "execution_engine": "python", "downloads_enabled": True,
                     "public_query_resources": ["discovery-live-literature"],
                     "timeout_seconds": 7200, "model_timeout_seconds": 1800},
    }


def runtime_declaration(runs: list[dict] | None = None) -> dict:
    return {"requirements_lock": "repository/runtime/integrations/domain_package/marathon-requirements.txt",
            "entrypoints": [{"id": "abducer-" + op, "operation": op, "file": HOOK_FILE, "callable": op}
                            for op in ("prepare", "execute", "verify")],
            "workflows": [registration(runs)], "planning_hooks": []}

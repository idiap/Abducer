# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Black-box verification and preservation evidence for generated projects."""

from __future__ import annotations

import base64
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Literal

from .conformance import validate_generated_layers, validate_generation_provenance
from .dependencies import validate_dependency_bundle
from .schemas import validate_document

EvidenceStatus = Literal[
    "established", "not_applicable", "not_tested", "unsupported", "failed"
]


@dataclass(frozen=True, slots=True)
class CheckEvidence:
    name: str
    status: EvidenceStatus
    details: str = ""
    data: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class PreservationReport:
    schema_version: int
    project: str
    checks: tuple[CheckEvidence, ...]
    levels: dict[str, EvidenceStatus]
    publishable: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def verify_generated_project(
    *,
    project_root: Path,
    prism_executable: str,
    handler: str = "fake",
    run_fixture: bool = True,
    portable: bool = False,
) -> PreservationReport:
    """Verify canonical source through the public CLI and classify evidence."""
    root = project_root.resolve()
    checks: list[CheckEvidence] = []
    model_path = root / "conversion-model.json"
    if not model_path.is_file():
        checks.append(
            CheckEvidence(
                "package-generation-contract",
                "failed",
                "conversion-model.json is required for package-generated conformance",
            )
        )
    else:
        try:
            model = json.loads(model_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            checks.append(
                CheckEvidence("package-generation-contract", "failed", str(exc))
            )
        else:
            issues = [
                *(str(issue) for issue in validate_document(model, "generation-plan")),
                *validate_generated_layers(root, model),
                *validate_generation_provenance(root, model),
            ]
            checks.append(
                CheckEvidence(
                    "package-generation-contract",
                    "failed" if issues else "established",
                    "; ".join(issues),
                )
            )
    prism_sources = sorted(root.rglob("*.prism"))
    if not prism_sources:
        checks.append(CheckEvidence("canonical-source", "failed", "no .prism source"))
    else:
        checks.append(
            CheckEvidence(
                "canonical-source",
                "established",
                data={
                    "files": [
                        path.relative_to(root).as_posix() for path in prism_sources
                    ]
                },
            )
        )
    for source in prism_sources:
        relative = source.relative_to(root).as_posix()
        checks.append(_cli_check(prism_executable, root, "check", relative))
        checks.append(_cli_check(prism_executable, root, "compile", relative))
    if run_fixture and (root / "main.prism").is_file():
        checks.extend(_run_and_verify(prism_executable, root, handler))
    else:
        checks.append(CheckEvidence("typed-execution-smoke", "not_tested"))
        checks.append(CheckEvidence("effect-integrity", "not_tested"))
    if portable:
        failures = validate_dependency_bundle(root, require_all_external=True)
        checks.append(
            CheckEvidence(
                "dependency-bundle",
                "failed" if failures else "established",
                "; ".join(failures),
            )
        )
    else:
        checks.append(CheckEvidence("dependency-bundle", "not_applicable"))
    levels = _levels(checks)
    publishable = all(
        item.status not in {"failed", "unsupported"}
        for item in checks
        if item.name in {
            "canonical-source",
            "dependency-bundle",
            "package-generation-contract",
        }
    ) and all(
        item.status != "failed"
        for item in checks
        if item.name.startswith("check:") or item.name.startswith("compile:")
    )
    report = PreservationReport(1, root.name, tuple(checks), levels, publishable)
    conversion = root / "conversion"
    conversion.mkdir(exist_ok=True)
    (conversion / "verification.json").write_text(
        json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return report


def verify_skill_roundtrip(source_skill: Path, generated_module: Path) -> list[str]:
    """Compare built instruction/resource payloads with source bytes exactly."""
    instruction = source_skill / "SKILL.md" if source_skill.is_dir() else source_skill
    source_root = instruction.parent
    strings = _artifact_strings(generated_module.read_text(encoding="utf-8"))
    if len(strings) < 6:
        return ["generated skill artifact has no decodable payload"]
    generated_instructions = strings[-2]
    expected_instructions = _frontmatter_body(instruction.read_text(encoding="utf-8"))
    failures: list[str] = []
    if generated_instructions != expected_instructions.strip():
        failures.append("skill instructions differ")
    try:
        resources = json.loads(strings[-1])
    except json.JSONDecodeError:
        return [*failures, "skill resource bundle is invalid JSON"]
    expected: dict[str, bytes] = {}
    for path in sorted(source_root.rglob("*")):
        if path.is_file() and not path.is_symlink() and path != instruction:
            if path.suffix.lower() in {
                ".py",
                ".sh",
                ".bash",
                ".zsh",
                ".js",
                ".ts",
                ".rb",
                ".pl",
            }:
                continue
            expected[path.relative_to(source_root).as_posix()] = path.read_bytes()
    if set(resources) != set(expected):
        failures.append("skill resource path set differs")
    for relative in sorted(set(resources) & set(expected)):
        try:
            decoded = base64.b64decode(resources[relative], validate=True)
        except (ValueError, TypeError):
            failures.append(f"invalid base64 resource: {relative}")
            continue
        if decoded != expected[relative]:
            failures.append(f"skill resource bytes differ: {relative}")
    return failures


def compare_graphs(expected: dict[str, Any], generated: dict[str, Any]) -> list[str]:
    """Compare independently authored graph nodes and typed edges."""
    failures: list[str] = []
    for key in ("nodes", "edges", "entrypoint"):
        if _canonical(expected.get(key)) != _canonical(generated.get(key)):
            failures.append(f"workflow graph {key} differs")
    return failures


def compare_contract_surfaces(
    expected: dict[str, Any], generated: dict[str, Any]
) -> list[str]:
    """Compare independently authored observable contract surfaces exactly."""
    failures: list[str] = []
    fields = ("input", "output", "errors", "effects", "permissions")
    for field_name in fields:
        if _canonical(expected.get(field_name)) != _canonical(
            generated.get(field_name)
        ):
            failures.append(f"contract {field_name} differs")
    return failures


def compare_fixture_outputs(native: Any, converted: Any) -> list[str]:
    """Compare normalized deterministic fixture results without broad field erasure."""
    left = canonicalize_cli_payload(native)
    right = canonicalize_cli_payload(converted)
    return [] if _canonical(left) == _canonical(right) else ["fixture output differs"]


def compare_traces(
    native: list[dict[str, Any]], converted: list[dict[str, Any]]
) -> list[str]:
    """Compare observable event order, outcome, and failure/stop paths."""

    def semantic(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        fields = ("event", "operation", "status", "branch", "error", "stopped")
        return [
            {
                field_name: event[field_name]
                for field_name in fields
                if field_name in event
            }
            for event in events
        ]

    return (
        []
        if semantic(native) == semantic(converted)
        else ["trace correspondence differs"]
    )


def inventory_output_coverage(
    inventory: dict[str, Any], dispositions: dict[str, dict[str, Any]]
) -> list[str]:
    """Require every source item to have an explicit, evidenced output disposition."""
    failures: list[str] = []
    for item in inventory.get("items", []):
        item_id = str(item["id"])
        decision = dispositions.get(item_id)
        if decision is None:
            failures.append(f"source item has no output disposition: {item_id}")
            continue
        kind = decision.get("disposition")
        if kind not in {"convert", "wrap", "copy", "exclude", "unsupported"}:
            failures.append(f"source item has invalid output disposition: {item_id}")
        if kind in {"convert", "wrap", "copy"} and not decision.get("outputs"):
            failures.append(
                f"source item disposition has no output evidence: {item_id}"
            )
    return failures


def provider_hook_preservation(
    *,
    provider: str,
    artifact_roundtrip: bool,
    materialized: bool,
    native_activated: bool,
    outcome_observed: bool,
    instrumented_trace: bool,
) -> dict[str, EvidenceStatus]:
    """Apply provider/runtime evidence caps without upgrading smoke evidence."""
    structural: EvidenceStatus = (
        "established" if artifact_roundtrip and materialized else "failed"
    )
    behavioral: EvidenceStatus
    trace: EvidenceStatus
    if provider == "opencode":
        behavioral = "unsupported"
        trace = "unsupported"
    elif not native_activated or not outcome_observed:
        behavioral = "not_tested"
        trace = "not_tested"
    else:
        behavioral = "established"
        trace = "established" if instrumented_trace else "not_tested"
    return {"structural": structural, "behavioral": behavioral, "trace": trace}


def aggregate_preservation(
    per_workflow: dict[str, dict[str, EvidenceStatus]],
    *,
    critical_workflows: set[str],
) -> dict[str, EvidenceStatus]:
    """Aggregate by weakest critical workflow; evidence is never averaged."""
    if not critical_workflows:
        return {}
    levels = sorted(
        {
            level
            for workflow_id in critical_workflows
            for level in per_workflow.get(workflow_id, {})
        }
    )
    ordering = {
        "failed": 0,
        "unsupported": 1,
        "not_tested": 2,
        "not_applicable": 3,
        "established": 4,
    }
    result: dict[str, EvidenceStatus] = {}
    for level in levels:
        statuses = [
            per_workflow.get(workflow_id, {}).get(level, "not_tested")
            for workflow_id in critical_workflows
        ]
        result[level] = min(statuses, key=ordering.__getitem__)
    return result


def relocate_project(project_root: Path) -> Path:
    """Copy a generated project for clean-room/relocation verification."""
    target = Path(tempfile.mkdtemp(prefix="to-prism-relocated-")) / "project"
    shutil.copytree(
        project_root,
        target,
        ignore=shutil.ignore_patterns(".venv", "__pycache__", ".pytest_cache"),
        copy_function=shutil.copy2,
    )
    return target


def _cli_check(
    executable: str, cwd: Path, command: str, relative: str
) -> CheckEvidence:
    completed = subprocess.run(
        [executable, command, relative],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    name = f"{command}:{relative}"
    if completed.returncode:
        return CheckEvidence(
            name, "failed", _bounded(completed.stderr or completed.stdout)
        )
    try:
        data = canonicalize_cli_payload(json.loads(completed.stdout))
    except json.JSONDecodeError:
        return CheckEvidence(name, "failed", "public CLI returned non-JSON output")
    return CheckEvidence(name, "established", data=data)


def _run_and_verify(executable: str, cwd: Path, handler: str) -> list[CheckEvidence]:
    result = cwd / "conversion" / "fixture-result.json"
    result.parent.mkdir(exist_ok=True)
    run = subprocess.run(
        [
            executable,
            "run",
            "main.prism",
            "--handler",
            handler,
            "--output",
            str(result),
        ],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    if run.returncode:
        return [
            CheckEvidence(
                "typed-execution-smoke", "failed", _bounded(run.stderr or run.stdout)
            ),
            CheckEvidence("effect-integrity", "not_tested"),
        ]
    smoke = CheckEvidence(
        "typed-execution-smoke",
        "established",
        "Type/executability smoke only; does not establish behavioral equivalence.",
    )
    verify = subprocess.run(
        [executable, "verify-run", str(result), "--mode", "offline"],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    integrity = CheckEvidence(
        "effect-integrity",
        "established" if verify.returncode == 0 else "failed",
        (
            "Effect artifact and checked-module integrity only; not workflow replay."
            if verify.returncode == 0
            else _bounded(verify.stderr or verify.stdout)
        ),
    )
    return [smoke, integrity]


def canonicalize_cli_payload(value: Any, *, _depth: int = 0) -> Any:
    """Remove machine/run-specific fields without erasing semantic results."""
    volatile = {
        "artifact_path",
        "timestamp",
        "started_at",
        "finished_at",
        "call_id",
        "run_id",
        "comparison_record_id",
        "recheck_path",
    }
    if _depth == 0:
        volatile.add("path")
    if isinstance(value, dict):
        return {
            str(key): canonicalize_cli_payload(item, _depth=_depth + 1)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
            if str(key) not in volatile
        }
    if isinstance(value, list):
        return [canonicalize_cli_payload(item, _depth=_depth + 1) for item in value]
    return value


def _levels(checks: list[CheckEvidence]) -> dict[str, EvidenceStatus]:
    failed = any(item.status == "failed" for item in checks)
    compiled = any(
        item.name.startswith("compile:") and item.status == "established"
        for item in checks
    )
    smoke = any(
        item.name == "typed-execution-smoke" and item.status == "established"
        for item in checks
    )
    return {
        "asset": "not_tested",
        "structural": "failed"
        if failed
        else ("established" if compiled else "not_tested"),
        "contract": "failed"
        if failed
        else ("established" if compiled else "not_tested"),
        "trace": "not_tested",
        "behavioral": "not_tested",  # fake execution is intentionally insufficient
        "epistemic": "not_tested",
        "typed_execution_smoke": "established" if smoke else "not_tested",
    }


def _artifact_strings(text: str) -> list[str]:
    start = text.find("skill_artifact")
    if start < 0:
        return []
    decoder = json.JSONDecoder()
    strings: list[str] = []
    cursor = text.find("(", start) + 1
    while cursor > 0 and cursor < len(text):
        quote = text.find('"', cursor)
        close = text.find(")", cursor)
        if quote < 0 or (close >= 0 and close < quote):
            break
        try:
            value, consumed = decoder.raw_decode(text[quote:])
        except json.JSONDecodeError:
            cursor = quote + 1
            continue
        if isinstance(value, str):
            strings.append(value)
        cursor = quote + consumed
    return strings


def _frontmatter_body(text: str) -> str:
    match = re.match(r"^\ufeff?---\r?\n.*?\r?\n---\r?\n", text, re.DOTALL)
    return text[match.end() :] if match else text


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _bounded(value: str, limit: int = 4000) -> str:
    return value.strip()[:limit]


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


__all__ = [
    "CheckEvidence",
    "PreservationReport",
    "canonicalize_cli_payload",
    "compare_contract_surfaces",
    "compare_fixture_outputs",
    "compare_graphs",
    "compare_traces",
    "aggregate_preservation",
    "inventory_output_coverage",
    "provider_hook_preservation",
    "relocate_project",
    "verify_generated_project",
    "verify_skill_roundtrip",
]

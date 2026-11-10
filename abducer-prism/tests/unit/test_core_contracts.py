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
import os
import subprocess
import sys
from pathlib import Path

import pytest

from to_prism.baseline import execute_baseline
from to_prism.decisions import invalidate_changed_decisions, make_decision
from to_prism.fingerprint import fingerprint_tree
from to_prism.graph import validate_workflow_graph
from to_prism.migrations import migrate_document
from to_prism.paths import ConversionPaths, PathSafetyError
from to_prism.schemas import validate_document
from to_prism.snapshot import create_allowlisted_snapshot

REPOSITORY = Path(__file__).resolve().parents[2]
LAUNCHER = REPOSITORY / "bin/to-prism"
ROOT_LAUNCHER = REPOSITORY / "to-prism"
PRISM = REPOSITORY / ".venv/bin/prism"


def test_fingerprint_covers_bytes_mode_and_symlink_target(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    executable = source / "run.sh"
    executable.write_text("echo one\n", encoding="utf-8")
    executable.chmod(0o644)
    (source / "other.sh").write_text("echo other\n", encoding="utf-8")
    (source / "current").symlink_to("run.sh")
    initial = fingerprint_tree(source)

    executable.chmod(0o755)
    mode_changed = fingerprint_tree(source)
    assert "changed:run.sh" in initial.diff(mode_changed)
    executable.write_text("echo two\n", encoding="utf-8")
    bytes_changed = fingerprint_tree(source)
    assert "changed:run.sh" in mode_changed.diff(bytes_changed)
    (source / "current").unlink()
    (source / "current").symlink_to("other.sh")
    target_changed = fingerprint_tree(source)
    assert "changed:current" in bytes_changed.diff(target_changed)


def test_authorized_baseline_runs_only_in_disposable_copy(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "value.txt").write_text("original", encoding="utf-8")
    before = fingerprint_tree(source)
    result = execute_baseline(
        source=source,
        source_fingerprint=before.digest,
        command=[
            sys.executable,
            "-c",
            "from pathlib import Path; Path('value.txt').write_text('changed'); print('ok')",
        ],
        attempts=2,
        network_policy="inherit",
    )
    assert result["execution"]["classification"] == "reproducible"
    assert fingerprint_tree(source).digest == before.digest


def test_graph_validator_rejects_unbounded_and_dangling_edges() -> None:
    workflow = {
        "workflows": [
            {
                "id": "workflow",
                "entry_node": "a",
                "nodes": [{"id": "a", "kind": "step", "contract_id": "contract"}],
                "edges": [
                    {
                        "source": "a",
                        "target": "missing",
                        "kind": "repeat",
                        "evidence": [{"location": "plan.json"}],
                    },
                    {
                        "source": "a",
                        "target": "a",
                        "kind": "repeat",
                        "evidence": [{"location": "plan.json"}],
                    },
                ],
            }
        ]
    }
    codes = {item.code for item in validate_workflow_graph(workflow)}
    assert {"dangling-edge", "unbounded-loop", "unchanging-loop"} <= codes


def test_schemas_reject_forward_versions_and_unknown_fields() -> None:
    document = {
        "artifact": "baseline",
        "schema_version": "99.0",
        "source_fingerprint": "sha256:" + "a" * 64,
        "candidates": [],
        "execution": {"authorized": False, "classification": "unavailable"},
        "tool": {},
        "future": True,
    }
    issues = validate_document(document)
    assert any("must equal '1.0'" in str(issue) for issue in issues)
    assert any("unknown property" in str(issue) for issue in issues)


def test_migrations_are_explicit_and_unknown_versions_fail_closed() -> None:
    legacy = {
        "artifact": "baseline",
        "schema_version": "0.9",
        "source_fingerprint": "sha256:" + "a" * 64,
        "candidates": [],
        "execution": {"authorized": False, "classification": "unavailable"},
        "tool": {},
    }
    assert migrate_document(legacy)["schema_version"] == "1.0"
    with pytest.raises(ValueError, match="no migration"):
        migrate_document({**legacy, "schema_version": "2.0"})


def test_decision_dependency_invalidation_is_minimal() -> None:
    first = make_decision(
        kind="mapping", choice="convert", depends_on=["a"], rationale="reviewed"
    )
    second = make_decision(
        kind="mapping", choice="copy", depends_on=["b"], rationale="reviewed"
    )
    updated = invalidate_changed_decisions({"decisions": [first, second]}, {"a"})
    statuses = {item["depends_on"][0]: item["status"] for item in updated["decisions"]}
    assert statuses == {"a": "invalidated", "b": "proposed"}


def test_source_and_output_must_be_disjoint(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    with pytest.raises(PathSafetyError):
        ConversionPaths.resolve(source, source / "generated")


def test_vendored_snapshot_is_allowlisted_hashed_and_license_reviewed(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "runtime.py").write_text("VALUE = 1\n", encoding="utf-8")
    project = tmp_path / "project"
    records = create_allowlisted_snapshot(
        source_root=source,
        project_root=project,
        entries=[
            {
                "path": "runtime.py",
                "license": "redistribution-approved",
                "purpose": "runtime-leaf",
            }
        ],
    )
    assert records[0]["path"] == "runtime.py"
    assert (project / "source_snapshot/runtime.py").read_bytes() == (
        source / "runtime.py"
    ).read_bytes()
    with pytest.raises(ValueError, match="credential-shaped"):
        create_allowlisted_snapshot(
            source_root=source,
            project_root=project,
            entries=[{"path": ".env", "license": "approved"}],
        )


def test_public_cli_inspect_and_model_emit_json(tmp_path: Path) -> None:
    source = tmp_path / "source"
    skill = source / ".agents/skills/review"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        "---\nname: review\ndescription: Review a task.\n---\nReview it.\n",
        encoding="utf-8",
    )
    output = tmp_path / "output"
    environment = {**os.environ, "PYTHONPATH": str(REPOSITORY / "src")}
    for command in ("inspect", "model"):
        completed = subprocess.run(
            [str(LAUNCHER), command, "--source", str(source), "--output", str(output)],
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )
        assert completed.returncode == 0, completed.stderr
        assert json.loads(completed.stdout)["command"] == command
    assert (output / "conversion/workflow.json").is_file()


def test_transfer_entrypoint_and_doctor_are_self_contained() -> None:
    completed = subprocess.run(
        [str(ROOT_LAUNCHER), "doctor", "--prism", "not-installed-for-test"],
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["status"] == "ready"
    assert payload["prism"]["status"] == "unavailable"
    assert payload["profiles"] == [
        "claude",
        "codex",
        "open-agent-skill",
        "opencode",
    ]


def test_public_cli_generates_and_verifies_reviewed_plan(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    skill = source / ".agents/skills/release-review"
    skill.mkdir(parents=True)
    skill.joinpath("SKILL.md").write_text(
        "---\nname: release-review\ndescription: Assess release claims against stated support.\n---\n"
        "Separate supported claims from unsupported claims.\n",
        encoding="utf-8",
    )
    output = tmp_path / "output"
    environment = {**os.environ, "PYTHONPATH": str(REPOSITORY / "src")}
    inspected = subprocess.run(
        [str(LAUNCHER), "inspect", "--source", str(source), "--output", str(output)],
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )
    assert inspected.returncode == 0, inspected.stderr
    plan = tmp_path / "approved-plan.json"
    example_plan = json.loads(
        (
                REPOSITORY / "examples/conversion_input/approved-plan.json"
        ).read_text(encoding="utf-8")
    )
    plan.write_text(json.dumps(example_plan), encoding="utf-8")
    generated = subprocess.run(
        [
            str(LAUNCHER),
            "generate",
            "--source",
            str(source),
            "--output",
            str(output),
            "--plan",
            str(plan),
            "--development-no-bundle",
            "--prism",
            str(PRISM),
            "--handler",
            "fake",
        ],
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )
    assert generated.returncode == 0, generated.stderr
    assert (output / "prism_project/main.prism").is_file()
    verified = subprocess.run(
        [
            str(LAUNCHER),
            "verify",
            "--source",
            str(source),
            "--output",
            str(output),
            "--prism",
            str(PRISM),
            "--handler",
            "fake",
        ],
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )
    assert verified.returncode == 0, verified.stderr
    assert json.loads(verified.stdout)["publishable"] is True

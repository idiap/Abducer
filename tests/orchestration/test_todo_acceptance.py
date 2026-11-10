# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Adversarial closure tests for immutable, freshly re-executed TODO receipts."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path

import pytest

import agentic.discovery.todo_acceptance as acceptance
from agentic.discovery.contracts import canonical_digest, file_digest
from agentic.discovery.todo_acceptance import (
    TodoAcceptanceError,
    artifact_result,
    implementation_surface_digest,
    receipt_annotation_path,
    run_acceptance,
    todo_definition_digest,
    validate_acceptance_receipt,
)


ROOT = Path(__file__).resolve().parents[2]
RAW_YM_ARCHIVE = (
    "agentic/external/yang_mills_representational_dynamics/2026-07-21/"
    "source_archives/full ym_representational_dynamics_complete_2026-07-21 (1).zip"
)


def _todo() -> dict:
    return {
        "id": "DWF-TEST", "title": "receipt test", "status": "open",
        "validation_commands": ["python -c pass"],
        "required_artifact": ["artifact.txt"], "evidence": [],
        "acceptance_criteria": ["command and artifact remain current"],
    }


def test_passed_receipt_becomes_stale_when_artifact_changes(tmp_path: Path) -> None:
    todo_file = tmp_path / "todos.json"
    todo_file.write_text(json.dumps([_todo()]), encoding="utf-8")
    (tmp_path / "artifact.txt").write_text("v1", encoding="utf-8")
    receipt = run_acceptance(_todo(), todo_file=todo_file, workspace=tmp_path)
    validate_acceptance_receipt(receipt, _todo(), todo_file=todo_file, workspace=tmp_path)
    (tmp_path / "artifact.txt").write_text("v2", encoding="utf-8")
    with pytest.raises(TodoAcceptanceError, match="artifact content changed"):
        validate_acceptance_receipt(receipt, _todo(), todo_file=todo_file, workspace=tmp_path)


def test_definition_change_invalidates_old_receipt_but_status_change_does_not(tmp_path: Path) -> None:
    todo_file = tmp_path / "todos.json"
    todo_file.write_text(json.dumps([_todo()]), encoding="utf-8")
    (tmp_path / "artifact.txt").write_text("stable", encoding="utf-8")
    receipt = run_acceptance(_todo(), todo_file=todo_file, workspace=tmp_path)
    resolved = copy.deepcopy(_todo())
    resolved["status"] = "resolved"
    resolved["evidence"] = ["receipt:somewhere.json"]
    assert todo_definition_digest(resolved) == todo_definition_digest(_todo())
    validate_acceptance_receipt(receipt, resolved, todo_file=todo_file, workspace=tmp_path)
    changed = copy.deepcopy(resolved)
    changed["acceptance_criteria"].append("new semantic requirement")
    with pytest.raises(TodoAcceptanceError, match="definition changed"):
        validate_acceptance_receipt(receipt, changed, todo_file=todo_file, workspace=tmp_path)


def test_failed_command_cannot_issue_passed_acceptance(tmp_path: Path) -> None:
    todo = _todo()
    todo["validation_commands"] = ["python -c 'raise SystemExit(7)'"]
    todo_file = tmp_path / "todos.json"
    todo_file.write_text(json.dumps([todo]), encoding="utf-8")
    (tmp_path / "artifact.txt").write_text("stable", encoding="utf-8")
    receipt = run_acceptance(todo, todo_file=todo_file, workspace=tmp_path)
    assert receipt["overall_status"] == "failed"
    with pytest.raises(TodoAcceptanceError, match="did not all pass"):
        validate_acceptance_receipt(receipt, todo, todo_file=todo_file, workspace=tmp_path)


def test_validator_or_implementation_change_invalidates_old_receipt(tmp_path: Path) -> None:
    todo_file = tmp_path / "todos.json"
    todo_file.write_text(json.dumps([_todo()]), encoding="utf-8")
    (tmp_path / "artifact.txt").write_text("stable", encoding="utf-8")
    validator = tmp_path / "agentic/scripts/example_validator.py"
    validator.parent.mkdir(parents=True)
    validator.write_text("raise SystemExit(0)\n", encoding="utf-8")
    receipt = run_acceptance(_todo(), todo_file=todo_file, workspace=tmp_path)
    validate_acceptance_receipt(receipt, _todo(), todo_file=todo_file, workspace=tmp_path)
    validator.write_text("# weakened after acceptance\nraise SystemExit(0)\n", encoding="utf-8")
    with pytest.raises(TodoAcceptanceError, match="implementation or validator surface changed"):
        validate_acceptance_receipt(receipt, _todo(), todo_file=todo_file, workspace=tmp_path)


def test_rewritten_execution_argv_cannot_masquerade_as_declared_command(tmp_path: Path) -> None:
    todo_file = tmp_path / "todos.json"
    todo_file.write_text(json.dumps([_todo()]), encoding="utf-8")
    (tmp_path / "artifact.txt").write_text("stable", encoding="utf-8")
    receipt = run_acceptance(_todo(), todo_file=todo_file, workspace=tmp_path)
    receipt["validation_results"][0]["argv"] = ["/tmp/unlocked-python", "-c", "pass"]
    receipt["receipt_id"] = acceptance._receipt_identifier(receipt)
    receipt["receipt_digest"] = canonical_digest(
        receipt, exclude_keys=("receipt_digest",)
    )
    with pytest.raises(TodoAcceptanceError, match="validation argv changed"):
        validate_acceptance_receipt(receipt, _todo(), todo_file=todo_file, workspace=tmp_path)


def test_recomputed_digest_cannot_hide_wrong_receipt_id(tmp_path: Path) -> None:
    todo_file = tmp_path / "todos.json"
    todo_file.write_text(json.dumps([_todo()]), encoding="utf-8")
    (tmp_path / "artifact.txt").write_text("stable", encoding="utf-8")
    receipt = run_acceptance(_todo(), todo_file=todo_file, workspace=tmp_path)
    receipt["receipt_id"] = "todo-acceptance.000000000000000000000000"
    receipt["receipt_digest"] = canonical_digest(
        receipt, exclude_keys=("receipt_digest",)
    )
    with pytest.raises(TodoAcceptanceError, match="receipt ID mismatch"):
        validate_acceptance_receipt(
            receipt, _todo(), todo_file=todo_file, workspace=tmp_path
        )


def test_missing_artifact_can_never_be_accepted(tmp_path: Path) -> None:
    todo_file = tmp_path / "todos.json"
    todo_file.write_text(json.dumps([_todo()]), encoding="utf-8")
    receipt = run_acceptance(_todo(), todo_file=todo_file, workspace=tmp_path)
    assert receipt["overall_status"] == "failed"
    assert receipt["artifact_results"][0]["kind"] == "missing"
    with pytest.raises(TodoAcceptanceError, match="did not all pass"):
        validate_acceptance_receipt(
            receipt, _todo(), todo_file=todo_file, workspace=tmp_path
        )


def test_binary_archive_with_spaces_is_an_exact_explicit_artifact(tmp_path: Path) -> None:
    archive = tmp_path / "source archives" / "full source (1).zip"
    archive.parent.mkdir()
    archive.write_bytes(bytes(range(256)) * 4096)
    result = artifact_result(tmp_path, "source archives/full source (1).zip")
    assert result == {
        "path": "source archives/full source (1).zip",
        "kind": "file",
        "exists": True,
        "content_digest": file_digest(archive),
        "file_count": 1,
    }


def test_raw_ym_source_archive_is_part_of_the_global_acceptance_surface() -> None:
    assert RAW_YM_ARCHIVE in acceptance.IMPLEMENTATION_SURFACE


def test_explicit_artifact_symlink_is_rejected(tmp_path: Path) -> None:
    target = tmp_path / "real.txt"
    target.write_text("bytes", encoding="utf-8")
    (tmp_path / "artifact.txt").symlink_to(target)
    with pytest.raises(TodoAcceptanceError, match="contains a symlink"):
        artifact_result(tmp_path, "artifact.txt")


@pytest.mark.parametrize("link_to_directory", [False, True])
def test_directory_descendant_symlink_is_rejected(
    tmp_path: Path, link_to_directory: bool
) -> None:
    artifact = tmp_path / "artifact"
    artifact.mkdir()
    with tempfile.TemporaryDirectory(dir=tmp_path.parent) as outside_raw:
        outside = Path(outside_raw)
        target = outside / ("directory" if link_to_directory else "file.txt")
        if link_to_directory:
            target.mkdir()
        else:
            target.write_text("outside", encoding="utf-8")
        (artifact / "redirect").symlink_to(
            target, target_is_directory=link_to_directory
        )
        with pytest.raises(TodoAcceptanceError, match="contains a symlink"):
            artifact_result(tmp_path, "artifact")


def test_implementation_surface_descendant_symlink_is_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    surface = tmp_path / "agentic" / "discovery"
    surface.mkdir(parents=True)
    target = tmp_path / "outside.txt"
    target.write_text("outside", encoding="utf-8")
    (surface / "redirect.py").symlink_to(target)
    monkeypatch.setattr(
        acceptance, "IMPLEMENTATION_SURFACE", ("agentic/discovery",)
    )
    with pytest.raises(TodoAcceptanceError, match="contains a symlink"):
        implementation_surface_digest(tmp_path)


@pytest.mark.parametrize(
    "evidence, message",
    [
        ([], "exactly one receipt annotation"),
        (["receipt:a.json", "receipt:b.json"], "exactly one receipt annotation"),
        (["receipt:/tmp/receipt.json"], "unsafe TODO DWF-TEST receipt path"),
        (["receipt:../receipt.json"], "unsafe TODO DWF-TEST receipt path"),
    ],
)
def test_receipt_annotation_is_exactly_one_safe_relative_path(
    tmp_path: Path, evidence: list[str], message: str
) -> None:
    todo = _todo()
    todo["evidence"] = evidence
    with pytest.raises(TodoAcceptanceError, match=message):
        receipt_annotation_path(todo, workspace=tmp_path)


def test_receipt_annotation_rejects_symlink(tmp_path: Path) -> None:
    target = tmp_path / "real.json"
    target.write_text("{}", encoding="utf-8")
    (tmp_path / "receipt.json").symlink_to(target)
    todo = _todo()
    todo["evidence"] = ["receipt:receipt.json"]
    with pytest.raises(TodoAcceptanceError, match="contains a symlink"):
        receipt_annotation_path(todo, workspace=tmp_path)


def test_fresh_validation_reexecutes_instead_of_trusting_recorded_status(
    tmp_path: Path,
) -> None:
    todo = _todo()
    todo["validation_commands"] = ["python check.py"]
    todo_file = tmp_path / "todos.json"
    todo_file.write_text(json.dumps([todo]), encoding="utf-8")
    (tmp_path / "artifact.txt").write_text("stable", encoding="utf-8")
    check = tmp_path / "check.py"
    check.write_text("raise SystemExit(0)\n", encoding="utf-8")
    receipt = run_acceptance(todo, todo_file=todo_file, workspace=tmp_path)
    check.write_text("raise SystemExit(7)\n", encoding="utf-8")
    validate_acceptance_receipt(
        receipt, todo, todo_file=todo_file, workspace=tmp_path
    )
    with pytest.raises(TodoAcceptanceError, match="fresh TODO acceptance command failed"):
        validate_acceptance_receipt(
            receipt,
            todo,
            todo_file=todo_file,
            workspace=tmp_path,
            reexecute_commands=True,
        )


def test_fresh_validation_rejects_command_that_rewrites_its_own_deck(
    tmp_path: Path,
) -> None:
    todo = _todo()
    todo["validation_commands"] = ["python check.py"]
    todo_file = tmp_path / "todos.json"
    todo_file.write_text(json.dumps([todo]), encoding="utf-8")
    (tmp_path / "artifact.txt").write_text("stable", encoding="utf-8")
    check = tmp_path / "check.py"
    check.write_text("raise SystemExit(0)\n", encoding="utf-8")
    receipt = run_acceptance(todo, todo_file=todo_file, workspace=tmp_path)
    check.write_text(
        "from pathlib import Path\n"
        "Path('todos.json').write_text('[]', encoding='utf-8')\n",
        encoding="utf-8",
    )

    with pytest.raises(TodoAcceptanceError, match="TODO deck changed"):
        validate_acceptance_receipt(
            receipt,
            todo,
            todo_file=todo_file,
            workspace=tmp_path,
            reexecute_commands=True,
        )


def test_receipt_issuance_rejects_command_that_rewrites_its_deck(
    tmp_path: Path,
) -> None:
    todo = _todo()
    todo["validation_commands"] = ["python check.py"]
    todo_file = tmp_path / "todos.json"
    todo_file.write_text(json.dumps([todo]), encoding="utf-8")
    (tmp_path / "artifact.txt").write_text("stable", encoding="utf-8")
    (tmp_path / "check.py").write_text(
        "from pathlib import Path\n"
        "Path('todos.json').write_text('[]', encoding='utf-8')\n",
        encoding="utf-8",
    )

    with pytest.raises(TodoAcceptanceError, match="TODO deck changed"):
        run_acceptance(todo, todo_file=todo_file, workspace=tmp_path)


@pytest.mark.parametrize("output", ["/tmp/acceptance.json", "../acceptance.json"])
def test_run_cli_rejects_absolute_or_escaping_output_before_execution(output: str) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "agentic/scripts/run_todo_acceptance.py",
            "--todo-file",
            "agentic/todos/discovery_workflow_todos.yaml",
            "--todo-id",
            "DWF-000",
            "--output",
            output,
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 2
    assert "unsafe receipt output path" in completed.stderr


def test_run_cli_rejects_nonexistent_selected_id_without_writing() -> None:
    output = ROOT / "agentic" / "reports" / f"missing-{uuid.uuid4().hex}.json"
    completed = subprocess.run(
        [
            sys.executable,
            "agentic/scripts/run_todo_acceptance.py",
            "--todo-file",
            "agentic/todos/discovery_workflow_todos.yaml",
            "--todo-id",
            "DOES-NOT-EXIST",
            "--output",
            output.relative_to(ROOT).as_posix(),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 2
    assert "expected one TODO DOES-NOT-EXIST, found 0" in completed.stderr
    assert not output.exists()


def test_completion_cli_rejects_missing_and_duplicate_selected_ids() -> None:
    base = [
        sys.executable,
        "agentic/scripts/validate_todo_completion.py",
        "--todo-file",
        "agentic/todos/discovery_workflow_todos.yaml",
    ]
    missing = subprocess.run(
        [*base, "--todo-id", "DOES-NOT-EXIST"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert missing.returncode == 2
    assert "were not found exactly once" in missing.stderr
    duplicate = subprocess.run(
        [*base, "--todo-id", "DWF-000", "--todo-id", "DWF-000"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert duplicate.returncode == 2
    assert "selected TODO IDs must be unique" in duplicate.stderr


def test_completion_cli_freezes_other_selected_decks_across_each_command() -> None:
    """One selected card cannot weaken a sibling deck while retaining success."""

    with tempfile.TemporaryDirectory(prefix="todo-deck-guard-", dir=ROOT) as raw:
        work = Path(raw)
        relative_root = work.relative_to(ROOT)
        deck_a = work / "deck-a.json"
        deck_b = work / "deck-b.json"
        artifact_a = work / "artifact-a.txt"
        artifact_b = work / "artifact-b.txt"
        check_a = work / "check-a.py"
        check_b = work / "check-b.py"
        artifact_a.write_text("a", encoding="utf-8")
        artifact_b.write_text("b", encoding="utf-8")
        check_a.write_text("raise SystemExit(0)\n", encoding="utf-8")
        check_b.write_text("raise SystemExit(0)\n", encoding="utf-8")
        todo_a = {
            **_todo(),
            "id": "DWF-DECK-A",
            "validation_commands": [f"python {(relative_root / 'check-a.py').as_posix()}"],
            "required_artifact": [(relative_root / "artifact-a.txt").as_posix()],
        }
        todo_b = {
            **_todo(),
            "id": "DWF-DECK-B",
            "validation_commands": [f"python {(relative_root / 'check-b.py').as_posix()}"],
            "required_artifact": [(relative_root / "artifact-b.txt").as_posix()],
        }
        deck_a.write_text(json.dumps([todo_a]), encoding="utf-8")
        deck_b.write_text(json.dumps([todo_b]), encoding="utf-8")
        receipt_a = run_acceptance(todo_a, todo_file=deck_a, workspace=ROOT)
        receipt_b = run_acceptance(todo_b, todo_file=deck_b, workspace=ROOT)
        receipt_a_path = work / "receipt-a.json"
        receipt_b_path = work / "receipt-b.json"
        receipt_a_path.write_text(json.dumps(receipt_a), encoding="utf-8")
        receipt_b_path.write_text(json.dumps(receipt_b), encoding="utf-8")
        resolved_a = copy.deepcopy(todo_a)
        resolved_b = copy.deepcopy(todo_b)
        resolved_a.update(
            status="resolved",
            evidence=[f"receipt:{receipt_a_path.relative_to(ROOT).as_posix()}"],
        )
        resolved_b.update(
            status="resolved",
            evidence=[f"receipt:{receipt_b_path.relative_to(ROOT).as_posix()}"],
        )
        deck_a.write_text(json.dumps([resolved_a]), encoding="utf-8")
        deck_b.write_text(json.dumps([resolved_b]), encoding="utf-8")
        check_a.write_text(
            "import json\n"
            "from pathlib import Path\n"
            f"path = Path({str(deck_b.relative_to(ROOT))!r})\n"
            "rows = json.loads(path.read_text(encoding='utf-8'))\n"
            "rows[0]['status'] = 'open'\n"
            "path.write_text(json.dumps(rows), encoding='utf-8')\n",
            encoding="utf-8",
        )

        completed = subprocess.run(
            [
                sys.executable,
                "agentic/scripts/validate_todo_completion.py",
                "--todo-file",
                deck_a.relative_to(ROOT).as_posix(),
                "--todo-file",
                deck_b.relative_to(ROOT).as_posix(),
                "--todo-id",
                "DWF-DECK-A",
                "--todo-id",
                "DWF-DECK-B",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        assert completed.returncode != 0
        assert "selected TODO deck changed" in completed.stderr

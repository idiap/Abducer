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

import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

KIT_ROOT = Path(__file__).resolve().parents[2]
LAUNCHER = KIT_ROOT / "bin" / "to-prism"
FIXTURES = KIT_ROOT / "tests" / "fixtures"


def _run(*arguments: str) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [str(LAUNCHER), *arguments],
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )


def _digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix().encode()
        digest.update(relative)
        if path.is_symlink():
            digest.update(b"L")
            digest.update(os.readlink(path).encode())
        elif path.is_file():
            digest.update(b"F")
            digest.update(path.read_bytes())
        elif path.is_dir():
            digest.update(b"D")
    return digest.hexdigest()


def _copy_fixture(tmp_path: Path, name: str) -> Path:
    destination = tmp_path / "source"
    shutil.copytree(FIXTURES / name, destination, symlinks=True)
    return destination


def _invoke_ok(*arguments: str) -> dict[str, object]:
    result = _run(*arguments)
    assert result.returncode == 0, result.stderr or result.stdout
    return json.loads(result.stdout)


def test_to_prism_routes_fresh_codex_project_to_model_review(tmp_path: Path) -> None:
    source = _copy_fixture(tmp_path, "codex")
    output = tmp_path / "output"
    before = _digest(source)

    inspected = _invoke_ok("inspect", "--source", str(source), "--output", str(output))
    modeled = _invoke_ok("model", "--source", str(source), "--output", str(output))

    assert inspected["source_unchanged"] is True
    assert modeled["status"] == "review_required"
    assert (output / "conversion" / "reasoning-map.json").is_file()
    assert not (output / "prism_project").exists()
    assert _digest(source) == before


def test_to_prism_baseline_discovers_without_execution(tmp_path: Path) -> None:
    source = _copy_fixture(tmp_path, "claude")
    output = tmp_path / "output"
    before = _digest(source)
    _invoke_ok("inspect", "--source", str(source), "--output", str(output))

    result = _invoke_ok(
        "baseline",
        "--source",
        str(source),
        "--output",
        str(output),
        "--dry-run",
    )

    assert result["execution"]["authorized"] is False
    assert result["execution"]["classification"] == "unavailable"
    assert _digest(source) == before


def test_to_prism_model_workflows_keeps_mixed_project_at_review_gate(
    tmp_path: Path,
) -> None:
    source = _copy_fixture(tmp_path, "mixed")
    output = tmp_path / "output"
    _invoke_ok("inspect", "--source", str(source), "--output", str(output))
    result = _invoke_ok("model", "--source", str(source), "--output", str(output))

    inventory = json.loads((output / "conversion" / "inventory.json").read_text())
    decisions = json.loads((output / "conversion" / "decisions.json").read_text())
    providers = {provider["name"] for provider in inventory["providers"]}
    assert {"claude", "codex", "open-agent-skill", "opencode"} <= providers
    assert result["status"] == "review_required"
    assert all(item["status"] == "proposed" for item in decisions["decisions"])


def test_to_prism_map_reasoning_does_not_infer_from_opencode_names(
    tmp_path: Path,
) -> None:
    source = _copy_fixture(tmp_path, "opencode")
    output = tmp_path / "output"
    _invoke_ok("inspect", "--source", str(source), "--output", str(output))
    _invoke_ok("model", "--source", str(source), "--output", str(output))

    reasoning = json.loads(
        (output / "conversion" / "reasoning-map.json").read_text(encoding="utf-8")
    )
    assert reasoning["mappings"]
    assert all(mapping["method"] is None for mapping in reasoning["mappings"])
    assert all(
        mapping["classification"] == "operational_only"
        for mapping in reasoning["mappings"]
    )
    assert all(
        mapping["review_status"] == "proposed" for mapping in reasoning["mappings"]
    )


def test_to_prism_derive_types_routes_specific_epistemic_contracts() -> None:
    skill = (KIT_ROOT / "skills/to-prism-derive-types/SKILL.md").read_text(
        encoding="utf-8"
    )
    fixture = FIXTURES / "epistemic-diagnosis/.agents/skills/diagnose/SKILL.md"
    source = fixture.read_text(encoding="utf-8")

    expected_roles = {
        "statement",
        "claim",
        "observation",
        "hypothesis",
        "ranked hypotheses",
        "critique",
        "defeater",
        "judgment",
        "decision",
        "action",
    }
    assert all(role in skill.lower() for role in expected_roles)
    assert "RankedRootCauseHypotheses" in skill
    assert "RootCauseRankingCritique" in skill
    assert "source anchors" in skill
    assert "review status" in skill
    assert "generic fallback" in skill
    assert "catalog/" in skill and "hypothesis-generating template" in skill
    assert "composition" in skill and "intermediate values" in skill
    assert "many-to-many" in skill
    assert "granularity_rationale" in skill
    assert "Generated[T]" in skill
    assert "ranked" in source and "critic" in source and "defeaters" in source


def test_to_prism_map_reasoning_sets_granularity_independently_of_skills() -> None:
    skill = (KIT_ROOT / "skills/to-prism-map-reasoning/SKILL.md").read_text(
        encoding="utf-8"
    )

    assert "reasoning occurrence -> one or more skill contributions" in skill
    assert "skill artifact       -> one or more reasoning occurrences" in skill
    assert "Split adjacent candidates" in skill
    assert "Merge complementary" in skill
    assert "ExactInput -> Generated[ExactOutput]" in skill


def test_to_prism_documentation_preserves_reviewed_semantic_contracts() -> None:
    skill = (KIT_ROOT / "skills/to-prism-document-workflows/SKILL.md").read_text(
        encoding="utf-8"
    )

    assert "$to-prism-derive-types" in skill
    assert "project semantic taxonomy" in skill
    assert "exact nominal chains" in skill
    assert "Generated[T]" in skill
    assert "must not create" in skill


def test_to_prism_parallel_test_design_freezes_typed_oracle_before_execution() -> None:
    skill = (KIT_ROOT / "skills/to-prism-design-parallel-tests/SKILL.md").read_text(
        encoding="utf-8"
    )
    prose = " ".join(skill.split())

    assert "$to-prism-derive-types" in skill
    assert "taxonomy hash" in skill
    assert "generation-plan hash" in skill
    assert "Generated[T]" in skill
    assert "negative controls" in skill
    assert "does not execute" in prose


def test_to_prism_parallel_test_runner_cannot_weaken_typed_oracle() -> None:
    skill = (KIT_ROOT / "skills/to-prism-run-parallel-tests/SKILL.md").read_text(
        encoding="utf-8"
    )
    prose = " ".join(skill.split())

    assert "project semantic taxonomy" in skill
    assert "generation-plan hash" in skill
    assert "generalizes an exact nominal contract" in skill
    assert "occurrence boundaries from skill files" in prose
    assert "approved manifest" in skill


def test_to_prism_review_preservation_caps_fake_only_evidence(tmp_path: Path) -> None:
    source = _copy_fixture(tmp_path, "codex")
    before = _digest(source)
    dossier = json.loads(
        (Path(__file__).parent / "preservation_evidence.json").read_text(
            encoding="utf-8"
        )
    )
    evidence = dossier["evidence"]
    expected = dossier["expected_review"]

    contract = (
        "established"
        if evidence["prism_check"] == evidence["prism_compile"] == "passed"
        else "failed"
    )
    trace = "established" if evidence["native_baseline"] == "passed" else "not_tested"
    behavioral = (
        "established" if evidence["native_baseline"] == "passed" else "not_tested"
    )

    assert {"contract": contract, "trace": trace, "behavioral": behavioral} == expected
    assert _digest(source) == before


def test_to_prism_update_dry_run_detects_change_without_publishing(
    tmp_path: Path,
) -> None:
    source = _copy_fixture(tmp_path, "codex")
    output = tmp_path / "output"
    _invoke_ok("inspect", "--source", str(source), "--output", str(output))
    _invoke_ok("model", "--source", str(source), "--output", str(output))
    output_before = _digest(output)

    skill = source / ".agents" / "skills" / "review" / "SKILL.md"
    skill.write_text(
        skill.read_text(encoding="utf-8") + "\nInclude an impact field.\n",
        encoding="utf-8",
    )
    result = _invoke_ok(
        "update",
        "--source",
        str(source),
        "--output",
        str(output),
        "--dry-run",
    )

    assert result["status"] == "review_required"
    assert result["changed_items"]
    assert _digest(output) == output_before

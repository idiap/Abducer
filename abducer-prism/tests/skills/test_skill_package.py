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
import re
import shutil
import subprocess
from pathlib import Path

KIT_ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = KIT_ROOT / "skills"
CORE_REFERENCES = {
    "conversion-contract.md",
    "layers.md",
    "output-contract.md",
    "preservation-policy.md",
    "reasoning-mapping.md",
    "type-taxonomy.md",
}
EXPECTED_SKILLS = {
    "to-prism",
    "to-prism-baseline",
    "to-prism-derive-types",
    "to-prism-design-parallel-tests",
    "to-prism-document-workflows",
    "to-prism-map-reasoning",
    "to-prism-model-workflows",
    "to-prism-review-preservation",
    "to-prism-run-parallel-tests",
    "to-prism-update",
}
PUBLIC_PHASES = {
    "inspect",
    "baseline",
    "model",
    "generate",
    "verify",
    "convert",
    "update",
}
MARKDOWN_LINK = re.compile(r"\[[^]]+\]\(([^)]+)\)")
FRONTMATTER = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)


def _skill_frontmatter(path: Path) -> dict[str, str]:
    match = FRONTMATTER.match(path.read_text(encoding="utf-8"))
    assert match is not None, path
    result: dict[str, str] = {}
    for line in match.group("body").splitlines():
        key, separator, value = line.partition(":")
        assert separator, line
        result[key] = value.strip().strip('"')
    return result


def _interface_metadata(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines == [line.rstrip() for line in lines]
    assert lines and lines[0] == "interface:"
    result: dict[str, str] = {}
    for line in lines[1:]:
        match = re.fullmatch(r"  ([a-z_]+): (\"(?:[^\"\\]|\\.)*\")", line)
        assert match is not None, f"unsupported metadata syntax in {path}: {line!r}"
        result[match.group(1)] = json.loads(match.group(2))
    return result


def _run(
    launcher: Path, *arguments: str, cwd: Path | None = None
) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [str(launcher), *arguments],
        cwd=cwd,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )


def test_skill_suite_has_complete_discriminating_metadata() -> None:
    assert {
        path.name for path in SKILLS_ROOT.iterdir() if path.is_dir()
    } == EXPECTED_SKILLS
    for skill_name in EXPECTED_SKILLS:
        skill = SKILLS_ROOT / skill_name
        frontmatter = _skill_frontmatter(skill / "SKILL.md")
        metadata = _interface_metadata(skill / "agents" / "openai.yaml")

        assert frontmatter["name"] == skill_name
        assert 20 <= len(frontmatter["description"]) <= 300
        assert "Use" in frontmatter["description"]
        assert set(metadata) == {"display_name", "short_description", "default_prompt"}
        assert 25 <= len(metadata["short_description"]) <= 64
        assert metadata["default_prompt"].startswith(f"Use ${skill_name} ")


def test_all_skill_links_resolve_and_core_references_are_reachable() -> None:
    linked_references: set[str] = set()
    for skill_markdown in sorted(SKILLS_ROOT.glob("*/SKILL.md")):
        text = skill_markdown.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK.findall(text):
            assert not target.startswith(("/", "http://", "https://")), target
            destination = (skill_markdown.parent / target).resolve()
            assert destination.is_file(), f"broken link from {skill_markdown}: {target}"
            assert KIT_ROOT.resolve() in destination.parents
            if destination.parent == KIT_ROOT / "references":
                linked_references.add(destination.name)

    assert CORE_REFERENCES <= linked_references


def test_reference_corpus_is_self_contained_and_has_no_checkout_paths() -> None:
    for name in CORE_REFERENCES:
        reference = KIT_ROOT / "references" / name
        text = reference.read_text(encoding="utf-8")
        assert len(text.splitlines()) >= 40
        assert "/Users/" not in text
        assert "notes/SYNTAX.md" not in text
        assert "packages/prism-" not in text
        prose = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        prose = re.sub(r"`[^`]*`", "", prose)
        for target in MARKDOWN_LINK.findall(prose):
            if target.startswith(("http://", "https://")):
                continue
            assert (reference.parent / target).resolve().exists(), target


def test_forward_case_catalog_covers_every_skill_once() -> None:
    catalog = json.loads((Path(__file__).parent / "forward_cases.json").read_text())
    cases = catalog["cases"]
    assert catalog["schema_version"] == 1
    assert {case["skill"] for case in cases} == EXPECTED_SKILLS
    assert len(cases) == len(EXPECTED_SKILLS)
    assert len({case["id"] for case in cases}) == len(cases)
    for case in cases:
        assert (KIT_ROOT / "tests" / "fixtures" / case["fixture"]).is_dir()
        assert case["request"].strip()
        assert case["stops_at"].strip()


def test_provider_neutral_launcher_survives_clean_copy(tmp_path: Path) -> None:
    isolated = tmp_path / "kit"
    shutil.copytree(
        KIT_ROOT,
        isolated,
        ignore=shutil.ignore_patterns(
            ".pytest_cache", ".ruff_cache", "__pycache__", "*.pyc"
        ),
    )
    launcher = isolated / "bin" / "to-prism"
    help_result = _run(launcher, "--help", cwd=tmp_path)
    assert help_result.returncode == 0, help_result.stderr
    assert PUBLIC_PHASES <= {
        line.strip().split(maxsplit=1)[0]
        for line in help_result.stdout.splitlines()
        if line.startswith("    ") and line.strip()
    }

    launcher_text = launcher.read_text(encoding="utf-8")
    for provider in ("codex", "claude", "opencode"):
        assert provider not in launcher_text.lower()

    version = _run(launcher, "--version", cwd=tmp_path)
    assert version.returncode == 0
    assert version.stdout.startswith("to-prism ")


def test_every_public_phase_uses_explicit_disjoint_paths() -> None:
    launcher = KIT_ROOT / "bin" / "to-prism"
    for command in PUBLIC_PHASES:
        result = _run(launcher, command, "--help")
        assert result.returncode == 0, result.stderr
        assert "--source SOURCE" in result.stdout
        assert "--output OUTPUT" in result.stdout
        assert "--dry-run" in result.stdout

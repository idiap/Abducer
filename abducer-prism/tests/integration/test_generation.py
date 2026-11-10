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

import os
import shutil
import subprocess
from pathlib import Path

import pytest

from to_prism.fingerprint import fingerprint_tree
from to_prism.generation import (
    GenerationError,
    _normalize_skill_frontmatter,
    generate_project,
)
from to_prism.verification import verify_generated_project, verify_skill_roundtrip

REPOSITORY = Path(__file__).resolve().parents[2]
PRISM = REPOSITORY / ".venv" / "bin" / "prism"
SKILL = REPOSITORY / "tests/fixtures/codex/.agents/skills/review"


def _write_skill(source: Path) -> str:
    skill = source / "skills/evidence-reviewer"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        "---\nname: evidence-reviewer\ndescription: Assess source claims against explicit evidence.\n---\n"
        "Separate supported claims from unsupported claims without inventing evidence.\n",
        encoding="utf-8",
    )
    return "skills/evidence-reviewer"


def _semantic_model(
    skill_path: str,
    *,
    workflow_id: str = "evidence-review",
    hooks: list[dict] | None = None,
    python_adapters: list[dict] | None = None,
    relation_type: str | None = "ReviewsAgainstPolicy",
) -> dict:
    step = {
        "id": "review",
        "description": "Assess supplied claims against the explicit project evidence policy.",
        "input_type": "EvidenceReviewBrief",
        "output_type": "EvidenceReviewFindings",
        "semantic_role": "epistemic",
        "granularity_rationale": "The source exposes one independently reviewable claim-support assessment and no intermediate epistemic result.",
        "reasoning_type": "EvidentialClaimCritique",
        "reasoning_rationale": "The critique retains unsupported claims and evidential limitations.",
        "output_provenance": "generated",
        "failure_type": "ModelFailure",
        "effects": ["AI.Generate", "Context.Disclose"],
        "skills": [
            {
                "path": skill_path,
                "role": "Project evidence policy assessor",
                "contribution": "Separates source-supported assertions from claims needing additional evidence.",
                "resource_dispositions": {},
            }
        ],
    }
    if relation_type:
        step["relation_type"] = relation_type
    return {
        "artifact": "generation-plan",
        "schema_version": "1.0",
        "hooks": hooks or [],
        "python_adapters": python_adapters or [],
        "type_definitions": [
            {
                "name": "EvidenceReviewBrief",
                "description": "A project-specific claim set submitted for evidential assessment.",
                "kind": "record",
                "fields": [
                    {
                        "name": "claims_for_review",
                        "type": "String",
                        "description": "Claims whose stated evidential support must be assessed.",
                    }
                ],
            },
            {
                "name": "EvidenceReviewFindings",
                "description": "A defeasible assessment of claim support under the project policy.",
                "kind": "record",
                "fields": [
                    {
                        "name": "supported_claims",
                        "type": "List[String]",
                        "description": "Claims with explicit support in the supplied source material.",
                    },
                    {
                        "name": "unsupported_claims",
                        "type": "List[String]",
                        "description": "Claims whose required support is absent from the supplied material.",
                    },
                ],
            },
            {
                "name": "NormalizedClaimText",
                "description": "Claim text transformed by one explicitly reviewed deterministic leaf.",
                "kind": "record",
                "fields": [
                    {
                        "name": "normalized_claim_text",
                        "type": "String",
                        "description": "Deterministically normalized claim text returned by the leaf adapter.",
                    }
                ],
            },
        ],
        "workflows": [
            {
                "id": workflow_id,
                "review_status": "approved",
                "semantic_mode": "epistemic",
                "description": "Assess project claims while preserving evidential limitations and provenance.",
                "input": {
                    "name": "review_brief",
                    "type": "EvidenceReviewBrief",
                    "fixture": {
                        "claims_for_review": "Review this claim for explicit support."
                    },
                },
                "output": {"type": "EvidenceReviewFindings", "provenance": "generated"},
                "epistemic_contract": {
                    "subject": "The explicit source support for the submitted project claims.",
                    "question": "Which submitted claims have explicit support in the supplied material?",
                    "observations": [
                        "Source assertions are not automatically treated as verified evidence."
                    ],
                    "defeaters": [
                        "Referenced evidence may be stale, irrelevant, or unavailable for inspection."
                    ],
                    "defeater_rationale": "These limitations prevent generated assessment from being presented as proof.",
                    "output_meaning": "A generated and defeasible classification under the stated evidence policy.",
                    "assurance": "generated",
                    "assurance_justification": "The model classifies supplied text but performs no independent verification.",
                    "unresolved": [],
                },
                "steps": [step],
            }
        ],
    }


def test_generate_checked_canonical_prism_without_mutating_source(
    tmp_path: Path,
) -> None:
    before = fingerprint_tree(REPOSITORY).digest
    output = tmp_path / "converted"
    result = generate_project(
        source_root=REPOSITORY,
        output_root=output,
        model=_semantic_model(
            SKILL.relative_to(REPOSITORY).as_posix(), workflow_id="converted-review"
        ),
        prism_executable=str(PRISM),
    )

    assert result.main == output / "main.prism"
    assert (output / "reasoning.prism").is_file()
    assert (output / "occurrences.prism").is_file()
    assert (output / "relations.prism").is_file()
    assert (output / "materialization.prism").is_file()
    reasoning = (output / "reasoning.prism").read_text()
    assert "reasoning ConvertedReview" in reasoning
    assert "type EvidentialClaimCritique" in (output / "occurrences.prism").read_text()
    assert "# Assess project claims while preserving evidential limitations" in (
        output / "reasoning.prism"
    ).read_text()
    assert "-> Generated[EvidenceReviewFindings]" in (
        output / "reasoning.prism"
    ).read_text()
    assert "# Granularity:" in (output / "reasoning.prism").read_text()
    assert "# Skill " in (output / "materialization.prism").read_text()
    assert "relation ReviewsAgainstPolicy" in (output / "relations.prism").read_text()
    assert not any(
        line.startswith(("type ", "relation ")) for line in reasoning.splitlines()
    )
    assert fingerprint_tree(REPOSITORY).digest == before
    assert (
        verify_skill_roundtrip(SKILL, output / "generated/review_skill_1.prism") == []
    )

    run = subprocess.run(
        [str(PRISM), "run", "main.prism", "--handler", "fake"],
        cwd=output,
        text=True,
        capture_output=True,
        check=False,
    )
    assert run.returncode == 0, run.stderr

    report = verify_generated_project(
        project_root=output,
        prism_executable=str(PRISM),
        run_fixture=True,
    )
    assert report.publishable is True
    assert any(
        check.name == "package-generation-contract" and check.status == "established"
        for check in report.checks
    )
    assert report.levels["behavioral"] == "not_tested"
    assert report.levels["typed_execution_smoke"] == "established"


def test_generation_rejects_silently_dropped_skill_scripts(tmp_path: Path) -> None:
    source = tmp_path / "source"
    skill = source / "skills/example"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        "---\nname: example\ndescription: Example skill.\n---\nDo the task.\n",
        encoding="utf-8",
    )
    (skill / "scripts").mkdir()
    (skill / "scripts/run.py").write_text("print('run')\n", encoding="utf-8")

    with pytest.raises(GenerationError, match="reviewed disposition"):
        generate_project(
            source_root=source,
            output_root=tmp_path / "converted",
            model=_semantic_model("skills/example", workflow_id="scripted"),
            prism_executable=str(PRISM),
        )


# REUSE-IgnoreStart
# SPDX examples below are parser fixtures, not licensing declarations.
def test_generation_normalizes_leading_skill_comment_preamble_in_staging_only(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    skill = source / "skills/commented"
    skill.mkdir(parents=True)
    original = """<!--
SPDX-License-Identifier: MIT
-->

<!--
Project-owned skill documentation.
-->

---
name: commented
description: Assess source claims against explicit evidence.
---
Separate supported claims from unsupported claims without inventing evidence.
"""
    instruction = skill / "SKILL.md"
    instruction.write_text(original, encoding="utf-8")
    normalized = _normalize_skill_frontmatter(original)
    assert normalized.startswith("---\nname: commented\n")
    assert normalized.index("SPDX-License-Identifier: MIT") > normalized.index(
        "description: Assess source claims against explicit evidence."
    )
    assert normalized.endswith(
        "Separate supported claims from unsupported claims without inventing evidence.\n"
    )

    output = tmp_path / "converted"
    generate_project(
        source_root=source,
        output_root=output,
        model=_semantic_model("skills/commented", workflow_id="commented-review"),
        prism_executable=str(PRISM),
    )

    assert instruction.read_text(encoding="utf-8") == original
    generated = output / "generated/review_skill_1.prism"
    assert generated.is_file()


def test_generation_rejects_comment_preamble_without_skill_frontmatter(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    skill = source / "skills/commented"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        "<!-- SPDX-License-Identifier: MIT -->\nNo frontmatter.\n",
        encoding="utf-8",
    )

    with pytest.raises(GenerationError, match="not followed by valid YAML frontmatter"):
        generate_project(
            source_root=source,
            output_root=tmp_path / "converted",
            model=_semantic_model("skills/commented", workflow_id="invalid-commented"),
            prism_executable=str(PRISM),
        )


# REUSE-IgnoreEnd


def test_generation_interleaves_generated_and_computed_steps_without_provenance_loss(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    skill_path = _write_skill(source)
    script = source / skill_path / "scripts/normalize.py"
    script.parent.mkdir()
    script.write_text(
        "def normalize(value):\n    return value.strip().lower()\n",
        encoding="utf-8",
    )
    model = _semantic_model(skill_path, workflow_id="mixed-review")
    model["type_definitions"] = [
        {
            "name": "EvidenceReviewBrief",
            "description": "A project-specific claim submitted for initial evidential assessment.",
            "kind": "record",
            "fields": [{"name": "claim_text", "type": "String", "description": "The exact project claim whose evidential support is assessed."}],
        },
        {
            "name": "EvidenceReviewDraft",
            "description": "A generated draft assessment retaining its unnormalized wording.",
            "kind": "record",
            "fields": [{"name": "draft_text", "type": "String", "description": "The model-generated assessment before deterministic normalization."}],
        },
        {
            "name": "NormalizedEvidenceReview",
            "description": "An assessment normalized by the named deterministic project procedure.",
            "kind": "record",
            "fields": [{"name": "normalized_text", "type": "String", "description": "The deterministically normalized assessment text produced by the adapter."}],
        },
    ]
    workflow = model["workflows"][0]
    workflow["semantic_mode"] = "mixed"
    workflow["input"] = {
        "name": "review_brief",
        "type": "EvidenceReviewBrief",
        "fixture": {"claim_text": "  SUPPORTED CLAIM  "},
    }
    workflow["output"] = {
        "type": "NormalizedEvidenceReview",
        "provenance": "computed",
    }
    attribution = {
        "path": skill_path,
        "role": "Project evidence review and normalization policy owner",
        "contribution": "Defines the generated assessment and its deterministic normalization boundary.",
        "resource_dispositions": {"scripts/normalize.py": "adapter"},
    }
    workflow["steps"] = [
        {
            "id": "draft_review",
            "description": "Generate a draft assessment of the supplied project claim.",
            "input_type": "EvidenceReviewBrief",
            "output_type": "EvidenceReviewDraft",
            "semantic_role": "epistemic",
            "material_kind": "agent",
            "granularity_rationale": "The draft is independently consumed by the deterministic normalization boundary.",
            "reasoning_type": "EvidentialClaimCritique",
            "reasoning_rationale": "The draft preserves uncertainty about the supplied claim support.",
            "relation_type": "ReviewsAgainstPolicy",
            "output_provenance": "generated",
            "failure_type": "ModelFailure",
            "effects": ["AI.Generate", "Context.Disclose"],
            "skills": [attribution],
        },
        {
            "id": "normalize_review",
            "description": "Normalize the generated assessment with the named deterministic leaf.",
            "input_type": "EvidenceReviewDraft",
            "output_type": "NormalizedEvidenceReview",
            "semantic_role": "operational",
            "material_kind": "computed",
            "granularity_rationale": "The explicit computation constructs distinct computed provenance after generation.",
            "adapter_operation": "review.normalize",
            "procedure": "evidence-review-normalization-v1",
            "output_provenance": "computed",
            "failure_type": "PythonError",
            "effects": ["Python.Call"],
            "skills": [attribution],
        },
    ]
    workflow["reasoning_projection"] = {
        "name": "ReviewClaimSupport",
        "description": "High-level assessment of the submitted claim without exposing normalization mechanics.",
        "input_name": "review_brief",
        "input_type": "EvidenceReviewBrief",
        "output_occurrence": "draft_assessment",
        "output_type": "EvidenceReviewDraft",
        "occurrences": [
            {
                "id": "draft_assessment",
                "method": "AssessClaimSupport",
                "input_type": "EvidenceReviewBrief",
                "output_type": "EvidenceReviewDraft",
                "rationale": "The occurrence makes one defeasible claim-support assessment independently of normalization.",
                "arguments": [{"source": "review_brief"}],
                "material_steps": ["draft_review"],
            }
        ],
        "topology": ["draft_assessment"],
    }
    model["python_adapters"] = [
        {
            "operation": "review.normalize",
            "source_path": f"{skill_path}/scripts/normalize.py",
            "function": "normalize",
            "input_type": "EvidenceReviewDraft",
            "input_field": "draft_text",
            "output_type": "NormalizedEvidenceReview",
            "output_field": "normalized_text",
        }
    ]

    output = tmp_path / "converted"
    generate_project(
        source_root=source,
        output_root=output,
        model=model,
        prism_executable=str(PRISM),
    )

    materialization = (output / "materialization.prism").read_text(encoding="utf-8")
    occurrences = (output / "occurrences.prism").read_text(encoding="utf-8")
    reasoning = (output / "reasoning.prism").read_text(encoding="utf-8")
    main = (output / "main.prism").read_text(encoding="utf-8")
    material_main = (output / "material_main.prism").read_text(encoding="utf-8")
    assert "Result[Generated[EvidenceReviewDraft], ModelFailure]" in materialization
    assert "Result[Computed[NormalizedEvidenceReview], PythonError]" in materialization
    assert 'compute(value, procedure = "evidence-review-normalization-v1")' in materialization
    assert "fails ConvertedWorkflowFailure" in materialization
    assert "type AssessClaimSupport" in occurrences
    assert "reasoning ReviewClaimSupport" in reasoning
    assert reasoning.startswith(
        "from mixed_review import (\n"
    )
    assert (
        "import occurrences as mixed_review_occurrences\n"
        in reasoning
    )
    assert "from types import" not in reasoning
    assert (output / "mixed_review.prism").is_file()
    assert not (output / "types.prism").exists()
    assert "draft_review" not in reasoning
    assert "normalize_review" not in reasoning
    assert not any(
        line.startswith(("type ", "relation ")) for line in reasoning.splitlines()
    )
    assert (output / "material_relations.prism").is_file()
    assert "agent draft_assessment_reasoning_agent(" in materialization
    assert "skills: Skills[EvidenceReviewBrief]" in materialization
    assert "converted_reasoning = ReviewClaimSupport(" in materialization
    assert "draft_assessment = draft_assessment_reasoning_agent" in materialization
    assert "solve ReviewClaimSupport(review_brief) using flow" in main
    assert "Result[Generated[EvidenceReviewDraft], ModelFailure]" in main
    assert "Result[Computed[NormalizedEvidenceReview], ConvertedWorkflowFailure]" in material_main

    projected_run = subprocess.run(
        [str(PRISM), "run", "main.prism", "--handler", "fake"],
        cwd=output,
        text=True,
        capture_output=True,
        check=False,
    )
    assert projected_run.returncode == 0, projected_run.stderr



def test_generation_merges_and_attaches_active_codex_hooks(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    skill_path = _write_skill(source)
    for index in (1, 2):
        (source / f"hooks-{index}.json").write_text(
            '{"hooks":{"Stop":[{"hooks":[{"type":"command","command":"echo '
            + str(index)
            + '"}]}]}}',
            encoding="utf-8",
        )
    output = tmp_path / "converted"
    generate_project(
        source_root=source,
        output_root=output,
        model=_semantic_model(
            skill_path,
            hooks=[
                {"provider": "codex", "path": "hooks-1.json", "runtime": "active"},
                {"provider": "codex", "path": "hooks-2.json", "runtime": "active"},
            ],
            workflow_id="hooked",
        ),
        prism_executable=str(PRISM),
        handler="codex",
    )

    native = (output / "generated/codex_hooks.native.json").read_text()
    assert native.index("echo 1") < native.index("echo 2")
    materialization = (output / "materialization.prism").read_text()
    assert "hooks: Hooks[Codex] = codex_hooks" in materialization


def test_active_codex_hook_rejects_relative_runtime_dependency(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    skill_path = _write_skill(source)
    (source / "hooks.json").write_text(
        '{"hooks":{"Stop":[{"hooks":[{"type":"command","command":"python scripts/check.py"}]}]}}',
        encoding="utf-8",
    )
    with pytest.raises(GenerationError, match="self-contained PATH commands"):
        generate_project(
            source_root=source,
            output_root=tmp_path / "converted",
            model=_semantic_model(
                skill_path,
                hooks=[
                    {"provider": "codex", "path": "hooks.json", "runtime": "active"}
                ],
                workflow_id="hooked",
            ),
            prism_executable=str(PRISM),
            handler="codex",
        )


def test_generation_emits_checked_python_leaf_harness(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    skill_path = _write_skill(source)
    (source / "leaf.py").write_text(
        "def transform(text):\n    return text.upper()\n", encoding="utf-8"
    )
    output = tmp_path / "converted"
    generate_project(
        source_root=source,
        output_root=output,
        model=_semantic_model(
            skill_path,
            python_adapters=[
                {
                    "operation": "example.transform",
                    "source_path": "leaf.py",
                    "function": "transform",
                    "input_type": "EvidenceReviewBrief",
                    "output_type": "NormalizedClaimText",
                    "input_field": "claims_for_review",
                    "output_field": "normalized_claim_text",
                }
            ],
            workflow_id="python-leaf",
        ),
        prism_executable=str(PRISM),
    )

    harness = output / "tests/python_leaf_1.prism"
    assert harness.is_file()
    checked = subprocess.run(
        [str(PRISM), "check", harness.relative_to(output).as_posix()],
        cwd=output,
        text=True,
        capture_output=True,
        check=False,
    )
    assert checked.returncode == 0, checked.stderr


@pytest.mark.skipif(
    os.environ.get("TO_PRISM_RUN_PORTABLE_TESTS") != "1",
    reason="network/toolchain portability test is opt-in",
)
def test_portable_project_bootstraps_offline_after_relocation(tmp_path: Path) -> None:
    source = tmp_path / "external"
    source.mkdir()
    skill_path = _write_skill(source)
    (source / "leaf.py").write_text(
        "def transform(text):\n    return text.upper()\n", encoding="utf-8"
    )
    output = tmp_path / "converted"
    generate_project(
        source_root=source,
        output_root=output,
        model=_semantic_model(
            skill_path,
            python_adapters=[
                {
                    "operation": "portable.transform",
                    "source_path": "leaf.py",
                    "function": "transform",
                    "license": "test-fixture-only",
                    "input_type": "EvidenceReviewBrief",
                    "output_type": "NormalizedClaimText",
                    "input_field": "claims_for_review",
                    "output_field": "normalized_claim_text",
                }
            ],
            workflow_id="portable-review",
        ),
        prism_executable=str(PRISM),
        prism_source=REPOSITORY,
        bundle=True,
        download_external=True,
    )
    relocated = tmp_path / "relocated" / "project"
    relocated.parent.mkdir()
    shutil.copytree(output, relocated)
    environment = {**os.environ, "PIP_NO_INDEX": "1"}
    bootstrap = subprocess.run(
        ["sh", "bootstrap.sh"],
        cwd=relocated,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )
    assert bootstrap.returncode == 0, bootstrap.stderr
    checked = subprocess.run(
        [str(relocated / ".venv/bin/prism"), "check", "main.prism"],
        cwd=relocated,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )
    assert checked.returncode == 0, checked.stderr
    executed = subprocess.run(
        [
            str(relocated / ".venv/bin/prism"),
            "run",
            "tests/python_leaf_1.prism",
            "--handler",
            "fake",
        ],
        cwd=relocated,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )
    assert executed.returncode == 0, executed.stderr

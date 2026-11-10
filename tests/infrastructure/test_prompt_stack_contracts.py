# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS = REPO_ROOT / "skills"


def _read(relpath: str) -> str:
    return (REPO_ROOT / relpath).read_text(encoding="utf-8")


def _skill_dir(name: str) -> Path:
    matches = sorted(SKILLS.glob(f"*/{name}/SKILL.md"))
    assert matches, f"Missing skill definition for {name}"
    return matches[0].parent


def test_shared_framework_has_phase_zero_and_claim_discipline() -> None:
    text = _read("docs/research-methods/epistemic-prompt-framework.md")
    assert "Phase 0: Theorem-Body Normalization" in text
    assert "Mandatory Claim Discipline" in text
    assert "Context Diagnosis And Qualified Certainty" in text
    assert "Meta Prompt: Context-Versus-Inference Diagnosis" in text
    assert "Prompt/Inference Diagnosis" in text
    assert "Lean/Lake Bounded Search Contract" in text
    assert "symbolic-search-ready" in text
    assert "evidence used;" in text
    assert "assertion license;" in text


def test_key_prompt_templates_have_hardened_epistemic_contracts() -> None:
    assert "anti-hub penalty" in _read("skills/discovery/kb-entrypoint-finder/references/prompt-template.md")
    assert "first kill condition" in _read("skills/discovery/kb-entrypoint-pathfinder/references/prompt-template.md")
    assert "graph leverage from mathematical leverage" in _read("skills/discovery/kb-proof-connector/references/prompt-template.md")
    assert "`underspecified`" in _read("skills/discovery/kb-concept-bridge-planner/references/prompt-template.md")
    assert "internally_supported_only" in _read("skills/evaluation/kb-hypothesis-evaluator/references/prompt-template.md")
    assert "decisive next test" in _read("skills/evaluation/kb-hypothesis-refutation-loop/references/prompt-template.md")
    assert "Citation Fidelity Judge" in _read("skills/discovery/kb-prove-cycle/references/critique-judges.md")
    assert "Proof Granularity Judge" in _read("skills/discovery/kb-prove-cycle/references/critique-judges.md")
    assert "Local Counterexample-Search Judge" in _read("skills/discovery/kb-prove-cycle/references/critique-judges.md")
    assert "Contradiction And Impossibility Discipline Judge" in _read("skills/discovery/kb-prove-cycle/references/critique-judges.md")
    assert "local-search failure has been recorded" in _read("skills/discovery/kb-prove-cycle/references/web-search-policy.md")
    assert "proof debt" in _read("skills/evaluation/kb-discovery-governor/references/prompt-template.md")
    assert "Parallel Mathematical Packet" in _read("skills/discovery/kb-discovery-cycle/references/prompt-template.md")
    assert "mathematical_layers.lean_style.scaffold" in _read("skills/discovery/kb-discovery-cycle/references/prompt-template.md")
    assert "lean_symbolic_search" in _read("skills/discovery/kb-discovery-cycle/references/prompt-template.md")
    assert "symbolic-search-ready" in _read("skills/discovery/kb-discovery-cycle/references/prompt-template.md")
    assert "Parallel Mathematical Packet" in _read("skills/evaluation/kb-discovery-breakthrough-profiler/references/prompt-template.md")
    assert "lean_style.scaffold" in _read("skills/evaluation/kb-discovery-breakthrough-profiler/references/prompt-template.md")
    assert "lean_symbolic_search" in _read("skills/evaluation/kb-discovery-breakthrough-profiler/references/prompt-template.md")
    assert "transport` pressure" in _read("skills/evaluation/kb-discovery-breakthrough-profiler/references/prompt-template.md")
    assert "typed scaffolds and obligation hints" in _read("skills/discovery/kb-prove-cycle/references/prompt-template.md")
    assert "symbolic-search summary when discovery executed" in _read("skills/orchestration/work/references/prompt-template.md")
    assert "symbolic-search-ready" in _read("skills/evaluation/kb-discovery-governor/references/prompt-template.md")
    assert "revisit penalties" in _read("skills/orchestration/work/references/prompt-template.md")


def test_openai_entrypoints_no_longer_use_overcompressed_defaults() -> None:
    assert "Normalize the source and target theorem bodies first" in _read(
        "skills/discovery/kb-concept-bridge-planner/agents/openai.yaml"
    )
    assert "context_status as well-posed / partially-ill-posed / ill-posed" in _read(
        "skills/discovery/kb-concept-bridge-planner/agents/openai.yaml"
    )
    assert "Prompt/Inference Diagnosis block" in _read("skills/discovery/kb-prove-cycle/agents/openai.yaml")
    assert "record local-search failures" in _read("skills/discovery/kb-prove-cycle/agents/openai.yaml")
    assert "contradiction targets" in _read("skills/discovery/kb-prove-cycle/agents/openai.yaml")
    assert "theorem-body normalization" in _read("skills/orchestration/kb-orchestrator/agents/openai.yaml")
    assert "anti-hub penalty" in _read("skills/discovery/kb-entrypoint-finder/agents/openai.yaml")
    assert "theorem-pair-specific claim" in _read("skills/discovery/kb-proof-connector/agents/openai.yaml")
    assert "parallel mathematical_layers packet" in _read("skills/discovery/kb-discovery-cycle/agents/openai.yaml")
    assert "Lean-style layers" in _read("skills/evaluation/kb-discovery-breakthrough-profiler/agents/openai.yaml")
    assert "bounded symbolic search evidence" in _read("skills/discovery/kb-discovery-cycle/agents/openai.yaml")
    assert "readiness modes and bridge-shape patterns" in _read("skills/evaluation/kb-discovery-breakthrough-profiler/agents/openai.yaml")
    assert "typed scaffolds and obligation hints" in _read("skills/discovery/kb-prove-cycle/agents/openai.yaml")
    assert "surface `lean_symbolic_search` diagnostics separately" in _read("skills/orchestration/work/agents/openai.yaml")
    assert "readiness modes and search-shape evidence" in _read("skills/evaluation/kb-discovery-governor/agents/openai.yaml")


def test_new_epistemic_helper_skills_exist() -> None:
    skill_names = [
        "theorem-body-normalizer",
        "epistemic-status-ledger",
        "bridge-object-equivalence-checker",
        "counterexample-hunter",
        "evidence-acquisition-planner",
        "hub-bias-auditor",
        "prior-art-importer",
        "expert-handoff",
    ]
    for name in skill_names:
        skill_dir = _skill_dir(name)
        assert (skill_dir / "agents" / "openai.yaml").exists()
        assert (skill_dir / "references" / "prompt-template.md").exists()


def test_review_reasoner_skill_stack_exists_and_is_code_first() -> None:
    skill_names = [
        "review-reasoner",
        "review-reasoner-epistemologist",
        "review-reasoner-fields-medalist",
        "review-reasoner-discovery-scientist",
        "review-reasoner-concept-logician",
        "review-reasoner-radical-designer",
    ]
    for name in skill_names:
        skill_dir = _skill_dir(name)
        assert (skill_dir / "agents" / "openai.yaml").exists()
        assert (skill_dir / "references" / "prompt-template.md").exists()

    macro = _read("skills/review/review-reasoner/SKILL.md")
    assert "code-and-state reviewer" in macro
    assert "Treat code, tests, and persisted state as the primary evidence." in macro
    assert "five critical lenses" in macro

    epistemologist = _read("skills/review/review-reasoner-epistemologist/references/prompt-template.md")
    assert "Review the actual reasoner implementation in code, tests, artifacts, and persistent state." in epistemologist
    assert "evidence versus coherence" in epistemologist

    mathematician = _read("skills/review/review-reasoner-fields-medalist/references/prompt-template.md")
    assert "mathematically typed and nontrivial" in mathematician
    assert "research programmes, genuine subresults, or merely labels" in mathematician

    scientist = _read("skills/review/review-reasoner-discovery-scientist/references/prompt-template.md")
    assert "search decomposition and route generation" in scientist
    assert "architecture is learning efficiently or only accumulating artifacts" in _read(
        "skills/review/review-reasoner-discovery-scientist/agents/openai.yaml"
    )

    logician = _read("skills/review/review-reasoner-concept-logician/references/prompt-template.md")
    assert "invents concepts or only renames absences" in logician

    designer = _read("skills/review/review-reasoner-radical-designer/references/prompt-template.md")
    assert "interface language itself constrains discovery" in designer

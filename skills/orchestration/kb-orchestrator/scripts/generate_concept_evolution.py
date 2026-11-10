#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Generate a human-readable concept-evolution artifact for a KB."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from reasoning_log import ReasoningLogger


COMMON_PHASES: list[tuple[str, str, str]] = [
    (
        "problem-and-target",
        "Problem Statement and Target",
        "This phase states the target mathematical object or theorem that organizes the rest of the KB.",
    ),
    (
        "foundational-definitions",
        "Foundational Definitions",
        "This phase fixes the basic objects, structures, and background definitions needed to formulate the problem.",
    ),
    (
        "bottlenecks-and-open-gaps",
        "Bottlenecks, Barriers, and Open Gaps",
        "This phase isolates the conceptual obstructions that prevent current partial results from closing the target theorem or problem.",
    ),
]

PHYSICS_PHASES: list[tuple[str, str, str]] = [
    (
        "euclidean-os-framework",
        "Euclidean / Osterwalder-Schrader Framework",
        "This phase collects Euclidean, Schwinger-function, and reflection-positivity ingredients that support reconstruction.",
    ),
    (
        "wightman-hamiltonian-framework",
        "Wightman / Hamiltonian Realization",
        "This phase organizes the Minkowski/Wightman and Hamiltonian-side objects that the reconstruction route aims to realize.",
    ),
    (
        "continuum-limit-and-renormalization",
        "Continuum Limit and Renormalization Control",
        "This phase captures lattice-to-continuum control, ultraviolet stability, and renormalization arguments.",
    ),
    (
        "mass-gap-and-spectral-transfer",
        "Mass-Gap and Spectral Transfer",
        "This phase gathers spectral-gap, transfer-matrix, and correlator-decay statements that feed the mass-gap route.",
    ),
    (
        "constructive-existence-results",
        "Constructive Models and Rigorous Existence Results",
        "This phase records partial constructive successes and rigorous existence results that indicate what a full solution would require.",
    ),
    (
        "classical-geometry-and-instantons",
        "Classical Geometry, Instantons, and Gauge-Analytic Structure",
        "This phase records classical or geometric control results that illuminate the structure of Yang-Mills theory without solving the full quantum problem.",
    ),
]

SEMIGROUP_PHASES: list[tuple[str, str, str]] = [
    (
        "generator-recovery",
        "Generator Recovery",
        "This phase introduces the infinitesimal generator or analogous hidden operator extracted from the dynamical object.",
    ),
    (
        "generator-regularity",
        "Generator Regularity",
        "This phase establishes closure, density, symmetry, or related regularity facts needed to make the generator mathematically usable.",
    ),
    (
        "spectral-functional-calculus",
        "Spectral and Functional Calculus",
        "This phase packages spectral-theorem or functional-calculus machinery that realizes the target dynamics from operator data.",
    ),
    (
        "measure-to-functional",
        "Measure-to-Functional Direction",
        "This phase records the easy representation direction from the hidden object toward the target consequence.",
    ),
    (
        "common-fixed-point-theorem",
        "Theorem-Level Correspondence",
        "This phase states the main generation or correspondence theorem tying the two sides of the theory together.",
    ),
]

MEASURE_PHASES: list[tuple[str, str, str]] = [
    (
        "measure-foundation",
        "Measure Foundation",
        "This phase introduces the hidden measure-side objects that mediate the theorem.",
    ),
    (
        "topological-approximation",
        "Topological Approximation",
        "This phase gathers compact-open and separation lemmas that let topology talk to test functions and measures.",
    ),
    (
        "measure-to-functional",
        "Measure-to-Functional Direction",
        "This phase records the easy representation direction from measures to functionals.",
    ),
    (
        "regularity-reconstruction",
        "Regularity and Uniqueness Reconstruction",
        "This phase reconstructs regularity, uniqueness, and compact-open control for the representing measure.",
    ),
    (
        "representation-theorem",
        "Representation Theorem",
        "This phase states the main theorem identifying the hidden measure object with the target functional structure.",
    ),
]

FIXED_POINT_PHASES: list[tuple[str, str, str]] = [
    (
        "fixed-point-subset-formation",
        "Fixed-Point Subset Formation",
        "This phase introduces the fixed-point subset of a single map as the hidden bridge object used to reduce the family theorem.",
    ),
    (
        "affine-averaging",
        "Affine Averaging",
        "This phase gathers the orbit-averaging constructions used to extract a fixed point for one affine map.",
    ),
    (
        "single-map-fixed-point",
        "Single-Map Fixed-Point Extraction",
        "This phase establishes the one-map fixed-point result that seeds the whole family argument.",
    ),
    (
        "invariant-fixed-point-subset",
        "Invariant Fixed-Point Subset",
        "This phase upgrades one-map fixed-point existence into a nonempty compact convex subset that can be reused by the commuting family.",
    ),
    (
        "commuting-invariance",
        "Commuting Invariance",
        "This phase shows that the rest of the commuting family preserves the hidden fixed-point subset.",
    ),
    (
        "finite-family-lift",
        "Finite-Family Lift",
        "This phase lifts the one-map argument to finite commuting subfamilies by iterating the invariant-subset reduction.",
    ),
    (
        "common-fixed-point-theorem",
        "Common Fixed-Point Theorem",
        "This phase packages finite intersection and compactness into the full Markov-Kakutani payoff.",
    ),
    (
        "examples-and-interpretation",
        "Examples and Interpretation",
        "This phase records concrete illustrations and interpretations of the common fixed-point result.",
    ),
]


def _front_matter_metadata(kb_path: Path) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: KB-level metadata routing for domain-specific conceptual narration.
    Contribution: Prevents concept-evolution reports from inheriting phase catalogs from an unrelated theorem family.
    """

    # Some checked-in KBs carry a UTF-8 BOM before their YAML frontmatter.
    # Decode it before checking the opening delimiter so domain routing survives.
    lines = kb_path.read_text(encoding="utf-8-sig").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    yaml_lines: list[str] = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        yaml_lines.append(line)
    if not yaml_lines:
        return {}
    try:
        payload = yaml.safe_load("\n".join(yaml_lines))
    except yaml.YAMLError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _phase_catalog(kb_path: Path) -> list[tuple[str, str, str]]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Domain-aware phase catalog selection.
    Contribution: Makes concept-evolution artifacts read like the active theorem domain rather than a hard-coded legacy template.
    """

    meta = _front_matter_metadata(kb_path)
    joined = " ".join(
        [
            str(meta.get("subdomain", "")).strip().lower(),
            str(meta.get("title", "")).strip().lower(),
            str(meta.get("kb_id", "")).strip().lower(),
        ]
    )
    if any(token in joined for token in ("mathematical-physics", "yang-mills", "mass-gap")):
        return COMMON_PHASES + PHYSICS_PHASES + [_bridge_agenda_phase(joined)]
    if any(token in joined for token in ("functional-analysis-convex-fixed-point", "markov-kakutani", "fixed-point theorem")):
        return COMMON_PHASES + FIXED_POINT_PHASES + [_bridge_agenda_phase(joined)]
    if any(token in joined for token in ("functional-analysis-measure-representation", "riesz-markov-kakutani", "regular borel measure")):
        return COMMON_PHASES + MEASURE_PHASES + [_bridge_agenda_phase(joined)]
    if any(token in joined for token in ("functional-analysis-semigroup", "stone", "hille-yosida", "one-parameter unitary")):
        return COMMON_PHASES + SEMIGROUP_PHASES + [_bridge_agenda_phase(joined)]
    return COMMON_PHASES + [_bridge_agenda_phase(joined)]


def _bridge_agenda_phase(joined_metadata: str) -> tuple[str, str, str]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Domain-specific narration of the live bridge agenda.
    Contribution: Removes generic phase titles from reports so the active discovery loop is described in the language of the current theorem family.
    """

    if any(token in joined_metadata for token in ("mathematical-physics", "yang-mills", "mass-gap")):
        return (
            "current-bridge-agenda",
            "Active Yang-Mills Bridge Agenda",
            "This phase summarizes the current high-value reconstruction, continuum-limit, and mass-gap bridge points recovered by the workflow.",
        )
    if any(token in joined_metadata for token in ("functional-analysis-convex-fixed-point", "markov-kakutani", "fixed-point theorem")):
        return (
            "current-bridge-agenda",
            "Active Fixed-Point Bridge Agenda",
            "This phase summarizes the current high-value invariant-subset, averaging, and compactness bridge points recovered by the workflow.",
        )
    if any(token in joined_metadata for token in ("functional-analysis-measure-representation", "riesz-markov-kakutani", "regular borel measure")):
        return (
            "current-bridge-agenda",
            "Active Representation Bridge Agenda",
            "This phase summarizes the current high-value measure-functional, regularity, and uniqueness bridge points recovered by the workflow.",
        )
    if any(token in joined_metadata for token in ("functional-analysis-semigroup", "stone", "hille-yosida", "one-parameter unitary")):
        return (
            "current-bridge-agenda",
            "Active Generator and Representation Agenda",
            "This phase summarizes the current high-value generator, resolvent, spectral, and functional-calculus bridge points recovered by the workflow.",
        )
    return (
        "current-bridge-agenda",
        "Current Bridge Agenda",
        "This phase summarizes the current high-value bridge points recovered by the automated reasoning workflow.",
    )


def _load_yaml_blocks(kb_path: Path) -> list[dict[str, Any]]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Loading and structuring KB statements for deterministic summarization.
    Contribution: Supplies the concept-evolution generator with the canonical statements it must organize.
    """

    content = kb_path.read_text(encoding="utf-8")
    blocks: list[dict[str, Any]] = []
    for chunk in content.split("```yaml"):
        if "```" not in chunk:
            continue
        body = chunk.split("```", 1)[0].strip()
        if not body:
            continue
        try:
            payload = yaml.safe_load(body)
        except yaml.YAMLError:
            continue
        if isinstance(payload, dict) and str(payload.get("id", "")).strip():
            blocks.append(payload)
    return blocks


def _load_json(path: Path | None) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Optional artifact loading for context enrichment.
    Contribution: Lets the concept-evolution report include current bridge priorities when upstream artifacts already exist.
    """

    if path is None or not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _load_phyp(path: Path | None) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Optional loading of proof hypotheses for bridge-agenda reporting.
    Contribution: Lets the concept-evolution report tie current conceptual phases to active hypotheses.
    """

    if path is None or not path.exists():
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def _statement_blob(stmt: dict[str, Any]) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Compact semantic surface for statement classification.
    Contribution: Keeps phase assignment grounded in processed KB fields instead of external lexical scraping.
    """

    return " ".join(
        [
            str(stmt.get("id", "")).strip(),
            str(stmt.get("kind", "")).strip(),
            str(stmt.get("informal", "")).strip(),
            str(stmt.get("latex", "")).strip(),
            str(stmt.get("notes", "")).strip(),
        ]
    ).lower()


def _phase_key(stmt: dict[str, Any]) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Typed phase assignment for concept-evolution summaries.
    Contribution: Places each statement into a stable conceptual phase so downstream entrypoint ranking has a usable phase map.
    """

    explicit_phase = str(stmt.get("statement_phase", "")).strip().lower()
    if explicit_phase:
        return explicit_phase

    kind = str(stmt.get("kind", "")).strip().lower()
    sid = str(stmt.get("id", "")).strip().lower()
    blob = _statement_blob(stmt)
    if kind == "problem" or sid.startswith("st.prob.") or any(
        token in blob for token in ("millennium prize problem", "clay problem asks")
    ):
        return "problem-and-target"
    if any(token in blob for token in ("bottleneck", "open gap", "obstruction", "barrier", "not yet known", "cutoff-removal remains open")):
        return "bottlenecks-and-open-gaps"
    if any(token in blob for token in ("transfer-matrix", "spectral-gap", "mass-gap", "correlator-decay", "exponential decay", "positive mass gap")):
        return "mass-gap-and-spectral-transfer"
    if any(token in blob for token in ("continuum-limit", "lattice", "cutoff-removal", "ultraviolet", "renormalization", "balaban")):
        return "continuum-limit-and-renormalization"
    if any(token in blob for token in ("osterwalder", "schrader", "os axioms", "os-euclidean", "schwinger", "reflection positivity", "reflection-positivity")):
        return "euclidean-os-framework"
    if any(token in blob for token in ("wightman", "hamiltonian", "vacuum state", "minkowski")):
        return "wightman-hamiltonian-framework"
    if any(token in blob for token in ("constructive", "infrared cutoff", "abelian higgs", "probabilistic progress", "interacting qft", "rigorous renormalisation")):
        return "constructive-existence-results"
    if any(token in blob for token in ("instanton", "donaldson", "adhm", "uhlenbeck", "moduli", "self-dual", "gauge fixing", "minimiser")):
        return "classical-geometry-and-instantons"
    if kind == "definition":
        return "foundational-definitions"
    return "constructive-existence-results"


def _short_text(value: str, max_chars: int = 180) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Compact rendering helper for human-readable reports.
    Contribution: Keeps phase summaries readable while preserving the mathematical intent of each statement.
    """

    text = str(value).replace("\n", " ").strip()
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3].rstrip() + "..."


def _build_markdown(
    kb_path: Path,
    statements: list[dict[str, Any]],
    analysis: dict[str, Any],
    phyp: dict[str, Any],
) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Rendering a concept-evolution narrative from structured KB artifacts.
    Contribution: Produces the human-readable conceptual scaffold required by later reasoning stages and by users inspecting a fresh KB.
    """

    phase_catalog = _phase_catalog(kb_path)
    grouped: dict[str, list[dict[str, Any]]] = {key: [] for key, _, _ in phase_catalog}
    for stmt in statements:
        phase = _phase_key(stmt)
        # Accept KB-specific statement phases beyond the built-in catalog.
        grouped.setdefault(phase, []).append(stmt)

    lines: list[str] = []
    lines.append(f"# Evolution of Concepts and Results in `{kb_path}`")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(
        "This description organizes the KB into conceptual phases and indicates how current bridge-search results focus the next reasoning round."
    )

    for key, title, summary in phase_catalog[:-1]:
        rows = grouped.get(key, [])
        if not rows:
            continue
        rows.sort(key=lambda row: (str(row.get("kind", "")).strip(), str(row.get("id", "")).strip()))
        lines.append("")
        lines.append(f"## {title}")
        lines.append("")
        lines.append(summary)
        lines.append("")
        for row in rows:
            sid = str(row.get("id", "")).strip()
            kind = str(row.get("kind", "")).strip()
            preview = _short_text(str(row.get("informal") or row.get("latex") or sid))
            lines.append(f"- `{sid}` ({kind}): {preview}")

    known_phases = {key for key, _, _ in phase_catalog}
    extra_phases = sorted(key for key in grouped if key not in known_phases and grouped.get(key))
    if extra_phases:
        lines.append("")
        lines.append("## Additional KB-Specific Phases")
        lines.append("")
        lines.append(
            "These phases are explicitly provided by the KB and are retained to preserve domain-specific conceptual granularity."
        )
        lines.append("")
        for key in extra_phases:
            rows = grouped.get(key, [])
            if not rows:
                continue
            rows.sort(key=lambda row: (str(row.get("kind", "")).strip(), str(row.get("id", "")).strip()))
            title = key.replace("-", " ").strip().title() or key
            lines.append(f"### {title} (`{key}`)")
            lines.append("")
            for row in rows:
                sid = str(row.get("id", "")).strip()
                kind = str(row.get("kind", "")).strip()
                preview = _short_text(str(row.get("informal") or row.get("latex") or sid))
                lines.append(f"- `{sid}` ({kind}): {preview}")
            lines.append("")

    agenda_key, agenda_title, agenda_summary = phase_catalog[-1]
    lines.append("")
    lines.append(f"## {agenda_title}")
    lines.append("")
    lines.append(agenda_summary)
    lines.append("")
    top_interventions = analysis.get("top_interventions", []) if isinstance(analysis.get("top_interventions"), list) else []
    if top_interventions:
        lines.append("Current top intervention points:")
        lines.append("")
        for row in top_interventions[:6]:
            if not isinstance(row, dict):
                continue
            sid = str(row.get("statement_id", "")).strip()
            rationale = _short_text(str(row.get("rationale", "")).strip(), 140)
            lines.append(f"- `{sid}`: {rationale}")
        lines.append("")
    hypotheses = phyp.get("hypotheses", []) if isinstance(phyp.get("hypotheses"), list) else []
    if hypotheses:
        lines.append("Current top bridge hypotheses:")
        lines.append("")
        for row in hypotheses[:6]:
            if not isinstance(row, dict):
                continue
            src = str(row.get("support_statement_id", "")).strip()
            dst = str(row.get("target_statement_id", "")).strip()
            family = str(row.get("template_family", "")).strip() or str(row.get("kind", "")).strip()
            if src and dst:
                lines.append(f"- `{src}` -> `{dst}` via {family}")
        lines.append("")
    lines.append(
        f"Overall KB state: {len(statements)} canonical statements, {len(top_interventions)} ranked interventions, and {len(hypotheses)} proof hypotheses currently shape the reasoning workflow."
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: CLI entrypoint for concept-evolution generation.
    Contribution: Produces a missing concept scaffold so new KBs can run through the full orchestrated pipeline from scratch.
    """

    logger = ReasoningLogger("kb-concept-evolution")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--kb", required=True)
    ap.add_argument("--output-md", required=True)
    ap.add_argument("--analysis")
    ap.add_argument("--phyp")
    args = ap.parse_args()

    kb_path = Path(args.kb)
    output_md = Path(args.output_md)
    analysis_path = Path(args.analysis) if args.analysis else None
    phyp_path = Path(args.phyp) if args.phyp else None

    logger.step(
        "Parsed concept-evolution arguments",
        "\n".join(
            [
                f"kb={kb_path}",
                f"output_md={output_md}",
                f"analysis={analysis_path or ''}",
                f"phyp={phyp_path or ''}",
            ]
        ),
    )

    if not kb_path.exists():
        raise FileNotFoundError(f"KB file not found: {kb_path}")

    statements = _load_yaml_blocks(kb_path)
    analysis = _load_json(analysis_path)
    phyp = _load_phyp(phyp_path)
    markdown = _build_markdown(kb_path, statements, analysis, phyp)

    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(markdown, encoding="utf-8")

    logger.step(
        "Built concept evolution artifact",
        "\n".join(
            [
                f"statement_count={len(statements)}",
                f"top_interventions={len(analysis.get('top_interventions', []) if isinstance(analysis.get('top_interventions'), list) else [])}",
                f"hypothesis_count={len(phyp.get('hypotheses', []) if isinstance(phyp.get('hypotheses'), list) else [])}",
                f"output={output_md}",
            ]
        ),
    )
    logger.add_output("concept_evolution_md", output_md)
    log_path = logger.finalize("ok", summary=f"Generated concept evolution for {kb_path.name}.")
    print(f"[OK] Wrote Markdown report: {output_md}")
    print(f"[LOG] {log_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

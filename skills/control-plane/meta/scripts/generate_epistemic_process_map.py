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

"""Generate an interactive epistemic systems map for the agent platform."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SYMBOL_GLYPHS: dict[str, str] = {
    r"\mathcal{K}": "K",
    r"\mathcal{M}": "M",
    r"\rightsquigarrow": "\u21dd",
    r"\vdash": "\u22a2",
    r"\Sigma": "\u03a3",
    r"\Delta": "\u0394",
    r"\equiv": "\u2261",
    r"\dashv": "\u22a3",
    r"\circlearrowleft": "\u21ba",
    r"\Rightarrow": "\u21d2",
    r"\Omega": "\u03a9",
    r"\parallel": "\u2225",
    r"\leftarrow": "\u2190",
}


LANES: list[dict[str, Any]] = [
    {
        "id": "grounding",
        "label": "Grounding",
        "symbol": r"\mathcal{K}",
        "question": "What can be asserted from the source material once theorem bodies, quantifiers, and models are explicit?",
        "system_role": "License and stabilize the inferential material before discovery begins.",
        "description": "Normalize claims, anchor them in source theorems, and control what can be asserted.",
        "y": 120,
        "color": "#f3efe3",
    },
    {
        "id": "discovery",
        "label": "Discovery",
        "symbol": r"\rightsquigarrow",
        "question": "What bridge object, invariant, abstraction, or route could mediate the current tension?",
        "system_role": "Generate and reshape the conceptual frontier rather than proving everything immediately.",
        "description": "Generate route hypotheses, bridge objects, invariants, and new search branches.",
        "y": 320,
        "color": "#eef5ea",
    },
    {
        "id": "prove",
        "label": "Prove",
        "symbol": r"\vdash",
        "question": "Which theorem-shaped subgoals, tactics, contradictions, or imports would actually close or block the route?",
        "system_role": "Subject discovery programmes to tactic-structured informal proof pressure.",
        "description": "Attempt tactic-guided informal proofs, critique them, and persist usable results.",
        "y": 520,
        "color": "#eaf1f7",
    },
    {
        "id": "governance",
        "label": "Governance",
        "symbol": r"\Sigma",
        "question": "Should the system branch, continue, reopen, defer, or stop?",
        "system_role": "Control recursion, memory, prioritization, and bounded continuation.",
        "description": "Control loops, score progress, reopen promising directions, and avoid unbounded drift.",
        "y": 720,
        "color": "#f8ecec",
    },
    {
        "id": "reflection",
        "label": "Reflection",
        "symbol": r"\Delta",
        "question": "What changed in understanding, what remained hard, and what should an expert inspect next?",
        "system_role": "Turn process state into expert-visible interpretation and public reasoning surfaces.",
        "description": "Synthesize what changed, what persists, and what an expert should inspect next.",
        "y": 920,
        "color": "#f0edf8",
    },
]


NODE_TYPES: list[dict[str, str]] = [
    {
        "id": "store",
        "label": "Knowledge Store",
        "symbol": r"\mathcal{K}",
        "meaning": "Persistent epistemic memory: statements, proofs, queues, logs, and reusable theorems.",
        "epistemic_move": "Retain and reactivate what has already been grounded or learned.",
    },
    {
        "id": "normalizer",
        "label": "Normalizer",
        "symbol": r"\equiv",
        "meaning": "Re-expresses raw statements into typed, licensed, inspectable claims.",
        "epistemic_move": "Type and license material before the rest of the system reasons with it.",
    },
    {
        "id": "generator",
        "label": "Generator",
        "symbol": r"\rightsquigarrow",
        "meaning": "Produces candidate routes, abstractions, branches, or proof attempts.",
        "epistemic_move": "Expand the search space by proposing new inferential material.",
    },
    {
        "id": "aggregate",
        "label": "Aggregator",
        "symbol": r"\Sigma",
        "meaning": "Collects many local results into a ranked or synthesized frontier.",
        "epistemic_move": "Compress many local signals into a coherent frontier or watch state.",
    },
    {
        "id": "critic",
        "label": "Critic",
        "symbol": r"\dashv",
        "meaning": "Tests soundness, plausibility, fidelity, or adversarial weakness.",
        "epistemic_move": "Apply back-pressure so coherence does not masquerade as evidence.",
    },
    {
        "id": "controller",
        "label": "Controller",
        "symbol": r"\circlearrowleft",
        "meaning": "Routes work across phases, handles loops, and decides when to continue or stop.",
        "epistemic_move": "Govern recursion and decide whether more work is justified.",
    },
    {
        "id": "publisher",
        "label": "Publisher",
        "symbol": r"\Rightarrow",
        "meaning": "Turns process state into expert-facing reports, surfaces, or maps.",
        "epistemic_move": "Expose internal state as an inspectable narrative or surface.",
    },
    {
        "id": "external",
        "label": "External Source",
        "symbol": r"\Omega",
        "meaning": "Web or prior-art source used only when local evidence is insufficient and the search gate allows it.",
        "epistemic_move": "Import decisive external structure only when local material is exhausted.",
    },
]


EDGE_TYPES: list[dict[str, str]] = [
    {
        "id": "grounds",
        "label": "Grounds",
        "symbol": r"\vdash",
        "meaning": "Supplies typed source material, theorem bodies, or licensed evidence.",
    },
    {
        "id": "proposes",
        "label": "Proposes",
        "symbol": r"\rightsquigarrow",
        "meaning": "Generates candidate claims, carriers, proof tasks, or branch programmes.",
    },
    {
        "id": "aggregates",
        "label": "Aggregates",
        "symbol": r"\Sigma",
        "meaning": "Collects many local artefacts into a unified frontier or report.",
    },
    {
        "id": "critiques",
        "label": "Critiques",
        "symbol": r"\dashv",
        "meaning": "Evaluates consistency, evidence, plausibility, or tactical discipline.",
    },
    {
        "id": "routes",
        "label": "Routes",
        "symbol": r"\Rightarrow",
        "meaning": "Directs control flow across phases, queues, and search branches.",
    },
    {
        "id": "persists",
        "label": "Persists",
        "symbol": r"\parallel",
        "meaning": "Writes durable memory so the search does not forget what it already learned.",
    },
    {
        "id": "imports",
        "label": "Imports",
        "symbol": r"\leftarrow",
        "meaning": "Brings external mathematics into InformalMathLib in a reusable normalized form.",
    },
    {
        "id": "loops",
        "label": "Loops",
        "symbol": r"\circlearrowleft",
        "meaning": "Feeds reflected or judged state back into discovery and prove as a controlled recursion.",
    },
]


def _node(
    node_id: str,
    *,
    title: str,
    lane: str,
    kind: str,
    x: int,
    symbol: str,
    function: str,
    binding: str,
    properties: list[str],
    inputs: list[str],
    outputs: list[str],
) -> dict[str, Any]:
    """Build a node description used by both the graph and the dossier."""

    node_type = next(item for item in NODE_TYPES if item["id"] == kind)
    return {
        "id": node_id,
        "title": title,
        "lane": lane,
        "kind": kind,
        "x": x,
        "y": next(item["y"] for item in LANES if item["id"] == lane),
        "symbol": symbol,
        "glyph": SYMBOL_GLYPHS.get(symbol, symbol),
        "function": function,
        "universal_binding": binding,
        "epistemic_move": node_type["epistemic_move"],
        "properties": properties,
        "inputs": inputs,
        "outputs": outputs,
        "tooltip": f"{title}: {function}",
    }


def _edge(
    edge_id: str,
    source: str,
    target: str,
    *,
    kind: str,
    title: str,
    meaning: str,
) -> dict[str, Any]:
    """Build a typed epistemic edge."""

    edge_type = next(item for item in EDGE_TYPES if item["id"] == kind)
    return {
        "id": edge_id,
        "source": source,
        "target": target,
        "kind": kind,
        "title": title,
        "symbol": edge_type["symbol"],
        "glyph": SYMBOL_GLYPHS.get(edge_type["symbol"], edge_type["symbol"]),
        "meaning": meaning,
        "tooltip": f"{title}: {meaning}",
    }


PROCESS_SPINE: list[dict[str, Any]] = [
    {
        "id": "license-claims",
        "title": "License Claims",
        "symbol": r"\vdash",
        "question": "What is actually assertable from the local theorem bodies?",
        "description": "The system begins by normalizing raw statements, exposing quantifiers and models, and refusing unlicensed assertions.",
        "node_ids": ["kb", "theorem_body_normalizer", "mathlib", "prior_art_pass"],
        "edge_ids": ["e01", "e03", "e04", "e05"],
    },
    {
        "id": "select-leverage",
        "title": "Select Leverage",
        "symbol": r"\rightsquigarrow",
        "question": "Which theorem pair or tension is mathematically leverageful rather than merely central?",
        "description": "Discovery chooses entrypoints and route candidates using theorem grounding, anti-hub checks, and first kill conditions.",
        "node_ids": ["entrypoint_finder", "pathfinder", "proof_connector"],
        "edge_ids": ["e02", "e06", "e07", "e08"],
    },
    {
        "id": "form-nexus",
        "title": "Form Conceptual Nexus",
        "symbol": r"\Sigma",
        "question": "What bridge object, abstraction family, or invariant would connect the source and target?",
        "description": "Bridge planning, abstraction conjecture, and proof sketching turn a raw gap into a coherent discovery programme with explicit proof debt.",
        "node_ids": ["bridge_planner", "gap_conjecturer", "proof_sketcher"],
        "edge_ids": ["e09", "e10", "e11"],
    },
    {
        "id": "pressure-route",
        "title": "Apply Proof Pressure",
        "symbol": r"\dashv",
        "question": "Which subgoals, tactics, contradictions, or external results decide whether the route survives?",
        "description": "The proof queue and prove cycle turn programmes into tactic-structured attempts, while the critic applies adversarial pressure.",
        "node_ids": ["proof_queue", "prove_cycle", "proof_critic"],
        "edge_ids": ["e16", "e17", "e18", "e20", "e21"],
    },
    {
        "id": "govern-recursion",
        "title": "Govern Recursion",
        "symbol": r"\circlearrowleft",
        "question": "Should the system branch, continue, reopen, or stop?",
        "description": "Discovery branches, the work loop, and the high-reward watch prevent both premature stopping and uncontrolled depth-first drift.",
        "node_ids": ["discovery_cycle", "discovery_branch_queue", "branch_executor", "high_reward_watch", "work_loop"],
        "edge_ids": ["e12", "e13", "e14", "e15", "e22", "e23", "e24", "e25", "e39", "e40"],
    },
    {
        "id": "reflect-publish",
        "title": "Reflect and Publish",
        "symbol": r"\Delta",
        "question": "What changed in understanding, what remains blocked, and what should a mathematician inspect next?",
        "description": "Expert papers, meta reflection, logs, and reasoning surfaces turn internal control state into inspectable scientific narrative.",
        "node_ids": ["expert_paper", "meta", "reasoning_logs", "reasoning_surfaces"],
        "edge_ids": ["e26", "e27", "e28", "e29", "e30", "e31", "e32", "e33", "e34", "e35", "e36", "e37"],
    },
]


def build_process_model() -> dict[str, Any]:
    """Assemble the end-to-end epistemic process as a typed systems graph."""

    nodes = [
        _node(
            "kb",
            title="Problem KB",
            lane="grounding",
            kind="store",
            x=140,
            symbol=r"\mathcal{K}",
            function="Persistent theorem bodies, definitions, axioms, and statement references for a specific problem.",
            binding="Material memory: the declarative corpus that licenses all later inference.",
            properties=["persistent", "problem-scoped", "statement-grounded", "searchable"],
            inputs=["problem statements", "imported references"],
            outputs=["typed statements", "theorem excerpts", "source claims"],
        ),
        _node(
            "theorem_body_normalizer",
            title="Theorem-Body Normalizer",
            lane="grounding",
            kind="normalizer",
            x=390,
            symbol=r"\equiv",
            function="Converts raw theorem prose into typed hypotheses, conclusions, quantifier regimes, and assertion licenses.",
            binding="Formal normalization: turns text into inspectable inferential units.",
            properties=["typed", "licensing-aware", "model-sensitive", "quantifier-aware"],
            inputs=["KB statements", "external theorem text"],
            outputs=["normalized statements", "claim types", "model assumptions"],
        ),
        _node(
            "mathlib",
            title="InformalMathLib",
            lane="grounding",
            kind="store",
            x=650,
            symbol=r"\mathcal{M}",
            function="Problem-scoped memory of proved, disproved, imported, and reusable mathematical results.",
            binding="Reusable formal-material memory: local theorem inventory and prior-art cache.",
            properties=["persistent", "problem-scoped", "searchable", "reusable"],
            inputs=["proved results", "external references", "negative findings"],
            outputs=["reusable lemmas", "prior-art grounding", "novelty checks"],
        ),
        _node(
            "prior_art_pass",
            title="Prior-Art Pass",
            lane="grounding",
            kind="external",
            x=930,
            symbol=r"\Omega",
            function="Targets external mathematical frameworks or theorems only when local search and InformalMathLib fail to close a decisive gap.",
            binding="External grounding: controlled import of prior formal structure.",
            properties=["web-gated", "citation-aware", "foundation-search", "import-normalized"],
            inputs=["blocked lemmas", "InformalMathLib misses", "foundation-search heuristics"],
            outputs=["import candidates", "barrier matches", "framework analogues"],
        ),
        _node(
            "entrypoint_finder",
            title="Entrypoint Finder",
            lane="discovery",
            kind="generator",
            x=140,
            symbol=r"\rightsquigarrow",
            function="Selects leverageful statements rather than ontology hubs, using theorem grounding and anti-hub checks.",
            binding="Epistemic targeting: where the search should start.",
            properties=["ranked", "anti-hub", "theorem-grounded", "frontier-seeking"],
            inputs=["normalized statements", "KB structure"],
            outputs=["entrypoints", "concept tracks", "initial leverage map"],
        ),
        _node(
            "pathfinder",
            title="Entrypoint Pathfinder",
            lane="discovery",
            kind="generator",
            x=360,
            symbol=r"\rightsquigarrow",
            function="Builds candidate theorem-to-theorem routes together with deltas, first kill conditions, and pathway rationale.",
            binding="Inferential path search: plausible routes through the statement space.",
            properties=["route-delta aware", "kill-condition aware", "ranked", "path-sensitive"],
            inputs=["entrypoints", "normalized statements"],
            outputs=["pathways", "route deltas", "target consequences"],
        ),
        _node(
            "proof_connector",
            title="Proof Connector",
            lane="discovery",
            kind="aggregate",
            x=580,
            symbol=r"\Sigma",
            function="Separates graph leverage from mathematical leverage and compresses candidate routes into connectable proof programmes.",
            binding="Programme assembly: connect local routes into inspection-ready search units.",
            properties=["aggregation", "false-positive aware", "programme-level", "route-sensitive"],
            inputs=["pathways", "statement connectivity", "kill conditions"],
            outputs=["connected routes", "programme candidates", "route consistency notes"],
        ),
        _node(
            "bridge_planner",
            title="Concept Bridge Planner",
            lane="discovery",
            kind="generator",
            x=820,
            symbol=r"\rightsquigarrow",
            function="Posits bridge objects, statement deltas, invariants, and concrete route claims; marks underspecified carriers explicitly.",
            binding="Abductive bridge search: identify what object could support the missing inference.",
            properties=["statement-delta aware", "underspecification aware", "bridge-typed", "counterfactual aware"],
            inputs=["connected routes", "normalized theorem pairs"],
            outputs=["bridge plans", "candidate carriers", "route obligations"],
        ),
        _node(
            "gap_conjecturer",
            title="Gap Abstraction Conjecturer",
            lane="discovery",
            kind="generator",
            x=1080,
            symbol=r"\rightsquigarrow",
            function="Turns blocked routes into typed conjectural objects, repair abstractions, and breakthrough-family diagnoses.",
            binding="Concept formation: move from missing step to missing abstraction type.",
            properties=["repair-aware", "family-aware", "conjectural", "negative-route aware"],
            inputs=["bridge plans", "blocked obligations", "search history"],
            outputs=["abstraction conjectures", "repair lemmas", "breakthrough families"],
        ),
        _node(
            "proof_sketcher",
            title="Proof Sketcher",
            lane="discovery",
            kind="generator",
            x=1330,
            symbol=r"\rightsquigarrow",
            function="Builds theorem-shaped informal proof programmes with tactic-friendly subgoals, lemma chains, and failure probes.",
            binding="Informal derivation design: what an eventual proof would have to look like.",
            properties=["theorem-shaped", "tactic-friendly", "lemma-chain aware", "failure-aware"],
            inputs=["bridge plans", "abstraction conjectures", "target theorems"],
            outputs=["proof sketches", "subgoals", "tactic traces"],
        ),
    ]

    nodes.extend(
        [
            _node(
                "discovery_cycle",
                title="Discovery Cycle",
                lane="governance",
                kind="controller",
                x=170,
                symbol=r"\circlearrowleft",
                function="Coordinates discovery, reopens blocked routes, and enqueues search work without repeating exhausted local moves.",
                binding="Recursive search control: when and how to continue exploration.",
                properties=["looping", "queue-aware", "frontier-sensitive", "non-destructive"],
                inputs=["proof sketches", "blocked results", "routing priors"],
                outputs=["proof queue items", "branch queue items", "breakthrough profiles"],
            ),
            _node(
                "discovery_branch_queue",
                title="Discovery Branch Queue",
                lane="governance",
                kind="store",
                x=430,
                symbol=r"\parallel",
                function="Persistent branch-level memory for distinct discovery patterns, families, attempts, and status transitions.",
                binding="Search branch memory: keeps breadth-first discovery from collapsing into a single route.",
                properties=["persistent", "branch-scoped", "status-tracked", "routing-aware"],
                inputs=["branch dossiers", "routing plans", "execution summaries"],
                outputs=["active branches", "pending branches", "branch history"],
            ),
            _node(
                "branch_executor",
                title="Discovery Branch Executor",
                lane="governance",
                kind="generator",
                x=700,
                symbol=r"\rightsquigarrow",
                function="Executes discovery branches as separate search runs and records what conceptual move each branch actually tested.",
                binding="Branch realization: turn a discovery pattern into concrete exploratory work.",
                properties=["branch-specific", "persistent", "summary-producing", "pattern-aware"],
                inputs=["branch queue", "prompt packs", "knowledge-source policy"],
                outputs=["branch executions", "programme candidates", "new conjectures"],
            ),
            _node(
                "proof_queue",
                title="Proof Queue",
                lane="prove",
                kind="store",
                x=310,
                symbol=r"\parallel",
                function="Persistent queue of self-contained conjectures, route lemmas, and branch-promoted proof tasks.",
                binding="Task memory: what remains to be proved, disproved, or blocked.",
                properties=["persistent", "queue-scoped", "self-contained", "priority-ranked"],
                inputs=["discovery outputs", "dependent tasks", "manual promotions"],
                outputs=["prove dossiers", "queue summaries", "frontier state"],
            ),
            _node(
                "prove_cycle",
                title="Prove Cycle",
                lane="prove",
                kind="generator",
                x=630,
                symbol=r"\vdash",
                function="Runs tactic-structured informal proofs, critiques each move, and finalizes results as proved, disproved, or blocked.",
                binding="Structured informal inference: controlled proof search rather than free-form prose.",
                properties=["tactic-aware", "judge-backed", "local-first", "result-persistent"],
                inputs=["proof queue item", "InformalMathLib results", "knowledge-source policy"],
                outputs=["proof attempts", "terminal results", "external reference imports"],
            ),
            _node(
                "proof_critic",
                title="End-to-End Proof Critic",
                lane="prove",
                kind="critic",
                x=930,
                symbol=r"\dashv",
                function="Assesses whether local proof state closes the main claim, respects assumptions, and survives adversarial scrutiny.",
                binding="Global proof judgment: whether the current route is actually becoming a complete solution.",
                properties=["adversarial", "closure-aware", "dependency-aware", "novelty-disciplined"],
                inputs=["proof attempts", "macro-proof state", "blocked results"],
                outputs=["plausibility scores", "critic findings", "continuation advice"],
            ),
            _node(
                "high_reward_watch",
                title="High-Reward Watch",
                lane="governance",
                kind="aggregate",
                x=1190,
                symbol=r"\Sigma",
                function="Detects major subresults that justify bounded continuation rather than an early budget stop.",
                binding="Reward-sensitive control: protect genuinely valuable local breakthroughs from premature termination.",
                properties=["thresholded", "continuation-aware", "follow-up spawning", "persistent"],
                inputs=["finalized proof results", "major-subresult assessments", "dependent task signals"],
                outputs=["continuation windows", "watch state", "follow-up queue seeds"],
            ),
            _node(
                "work_loop",
                title="Work Loop",
                lane="governance",
                kind="controller",
                x=1450,
                symbol=r"\circlearrowleft",
                function="Alternates discovery and prove, invokes meta at key stop points, and decides whether the research programme keeps going.",
                binding="Outer epistemic control: the recursive agent society seen as one system.",
                properties=["alternating", "budget-aware", "meta-triggering", "stop-sensitive"],
                inputs=["critic reports", "queue state", "high-reward watch"],
                outputs=["next phase", "stop state", "meta triggers"],
            ),
            _node(
                "expert_paper",
                title="Expert Paper Generator",
                lane="reflection",
                kind="publisher",
                x=360,
                symbol=r"\Rightarrow",
                function="Turns the live route and its proof debt into a human-inspectable research paper narrative.",
                binding="Expert-facing synthesis: convert internal search state into mathematical exposition.",
                properties=["paper-style", "route-grounded", "theorem-aware", "failure-aware"],
                inputs=["proof sketches", "critic state", "finalized attempts"],
                outputs=["expert papers", "macro-proof reports", "tex/pdf artefacts"],
            ),
            _node(
                "meta",
                title="Meta Reflection",
                lane="reflection",
                kind="critic",
                x=740,
                symbol=r"\Delta",
                function="Reflects on why the problem is hard, what conceptual shift occurred, and whether the process is learning or merely organizing.",
                binding="Epistemic self-interpretation: what changed in understanding.",
                properties=["perspective-aware", "shift-tracking", "programme-level", "expert-facing"],
                inputs=["work state", "macro-proof state", "proof summary", "search-space state"],
                outputs=["meta reports", "slides", "epistemic interpretations"],
            ),
            _node(
                "reasoning_logs",
                title="Reasoning Logs",
                lane="reflection",
                kind="store",
                x=1090,
                symbol=r"\parallel",
                function="Stores fine-grained provenance of each agent action, prompt context, and emitted artefact.",
                binding="Process observability: trace what happened and when.",
                properties=["persistent", "chronological", "agent-scoped", "auditable"],
                inputs=["all stage runs"],
                outputs=["run history", "provenance", "diagnostic traces"],
            ),
            _node(
                "reasoning_surfaces",
                title="Reasoning Surfaces",
                lane="reflection",
                kind="publisher",
                x=1400,
                symbol=r"\Rightarrow",
                function="Publishes dashboards, maps, papers, and diagrams that expose the current state of the agent society to experts.",
                binding="Public epistemic surface: the inspectable big picture.",
                properties=["expert-facing", "aggregated", "interactive", "comparative"],
                inputs=["papers", "meta reports", "logs", "graph models"],
                outputs=["HTML maps", "reports", "surfaces", "narratives"],
            ),
        ]
    )

    edges = [
        _edge("e01", "kb", "theorem_body_normalizer", kind="grounds", title="Normalize theorem bodies", meaning="The KB supplies raw statements that are converted into typed inferential units."),
        _edge("e02", "theorem_body_normalizer", "entrypoint_finder", kind="grounds", title="Ground discovery in typed claims", meaning="Discovery starts only after statement bodies, quantifiers, and models are explicit."),
        _edge("e03", "theorem_body_normalizer", "mathlib", kind="persists", title="Persist normalized results", meaning="Normalized statement structure is reusable across proof and prior-art tasks."),
        _edge("e04", "mathlib", "prior_art_pass", kind="grounds", title="Check local memory first", meaning="Prior-art search uses InformalMathLib to avoid browsing when the result is already known locally."),
        _edge("e05", "prior_art_pass", "mathlib", kind="imports", title="Import external foundations", meaning="External theorems and definitions are normalized and persisted into InformalMathLib."),
        _edge("e06", "entrypoint_finder", "pathfinder", kind="proposes", title="Open route search", meaning="Leverageful entrypoints seed theorem-to-theorem pathway generation."),
        _edge("e07", "pathfinder", "proof_connector", kind="proposes", title="Assemble candidate routes", meaning="Pathways are compressed into connected proof programmes."),
        _edge("e08", "proof_connector", "bridge_planner", kind="routes", title="Pass connected routes to bridge search", meaning="Only mathematically leverageful route programmes proceed to bridge planning."),
        _edge("e09", "bridge_planner", "gap_conjecturer", kind="proposes", title="Turn blocked bridges into abstractions", meaning="Bridge planning hands off missing carriers and deltas for conjectural repair."),
        _edge("e10", "gap_conjecturer", "proof_sketcher", kind="proposes", title="Lift abstractions into proof programmes", meaning="Conjectured objects become theorem-shaped proof sketches."),
        _edge("e11", "proof_sketcher", "discovery_cycle", kind="aggregates", title="Aggregate discovery outputs", meaning="Proof sketches and route lemmas feed the controlled discovery loop."),
        _edge("e12", "discovery_cycle", "discovery_branch_queue", kind="persists", title="Persist branch frontier", meaning="Discovery branches are stored so the system remembers which patterns were already explored."),
        _edge("e13", "discovery_branch_queue", "branch_executor", kind="routes", title="Execute branch dossiers", meaning="Queued discovery branches are turned into concrete exploratory runs."),
        _edge("e14", "branch_executor", "proof_queue", kind="proposes", title="Promote discovery programmes", meaning="Successful branch outcomes reopen theorem-shaped proof tasks."),
        _edge("e15", "discovery_cycle", "proof_queue", kind="proposes", title="Seed direct proof tasks", meaning="Discovery can enqueue proof work even before branch execution when the route is concrete enough."),
        _edge("e16", "proof_queue", "prove_cycle", kind="routes", title="Consume proof tasks", meaning="Queued conjectures are instantiated as tactic-guided proof dossiers."),
        _edge("e17", "mathlib", "prove_cycle", kind="grounds", title="Ground proof attempts", meaning="Prove consumes local results, imported prior art, and earlier negative findings."),
        _edge("e18", "prior_art_pass", "prove_cycle", kind="grounds", title="Provide external theorem grounding", meaning="When justified, prior-art imports supply decisive external statements to the proof attempt."),
        _edge("e19", "prove_cycle", "mathlib", kind="persists", title="Persist proof results", meaning="Proved, disproved, blocked, and imported results are written back into reusable memory."),
        _edge("e20", "prove_cycle", "proof_critic", kind="critiques", title="Evaluate proof state", meaning="Each proof result is judged for end-to-end adequacy, closure, and plausibility."),
        _edge("e21", "proof_critic", "work_loop", kind="critiques", title="Advise the outer loop", meaning="The global critic tells the work controller whether continuation is justified."),
        _edge("e22", "prove_cycle", "high_reward_watch", kind="persists", title="Emit high-reward signals", meaning="Major subresults are normalized into continuation signals rather than being lost as isolated successes."),
        _edge("e23", "high_reward_watch", "work_loop", kind="routes", title="Delay premature stop", meaning="High-value local results can justify bounded continuation beyond the nominal cycle budget."),
        _edge("e24", "work_loop", "discovery_cycle", kind="loops", title="Re-enter discovery", meaning="The outer loop feeds stalled or blocked proof state back into discovery."),
        _edge("e25", "work_loop", "prove_cycle", kind="routes", title="Advance to prove", meaning="The controller alternates into prove when there is queued mathematical work to consume."),
        _edge("e26", "work_loop", "meta", kind="routes", title="Trigger meta reflection", meaning="Meta runs on budget checkpoints, queue exhaustion, and other epistemically significant states."),
        _edge("e27", "meta", "discovery_cycle", kind="loops", title="Reflective feedback into discovery", meaning="Meta analysis can reframe what kind of breakthrough the discovery loop should seek next."),
        _edge("e28", "meta", "reasoning_surfaces", kind="aggregates", title="Publish reflective narrative", meaning="Meta contributes the system-level interpretation shown to experts."),
        _edge("e29", "proof_sketcher", "expert_paper", kind="aggregates", title="Lift sketches into papers", meaning="Route claims and lemma chains become expert-facing paper narratives."),
        _edge("e30", "proof_critic", "expert_paper", kind="grounds", title="Paper grounded by critique", meaning="The paper generator includes proof debt, risks, and failure diagnoses from the critic."),
        _edge("e31", "expert_paper", "reasoning_surfaces", kind="aggregates", title="Publish expert papers", meaning="Paper narratives become part of the public reasoning surfaces."),
        _edge("e32", "kb", "reasoning_surfaces", kind="grounds", title="Expose original corpus", meaning="Surfaces retain visible links back to the original theorem source material."),
        _edge("e33", "discovery_cycle", "reasoning_logs", kind="persists", title="Log discovery", meaning="Discovery actions are written into the shared provenance log."),
        _edge("e34", "prove_cycle", "reasoning_logs", kind="persists", title="Log prove", meaning="Proof attempts, tactic traces, and verdicts are persisted for auditability."),
        _edge("e35", "work_loop", "reasoning_logs", kind="persists", title="Log outer-loop control", meaning="The controller records why the system kept going, stopped, or switched phase."),
        _edge("e36", "meta", "reasoning_logs", kind="persists", title="Log reflection", meaning="Reflective interpretations are also part of the permanent research trace."),
        _edge("e37", "reasoning_logs", "reasoning_surfaces", kind="aggregates", title="Surface provenance", meaning="Surfaces aggregate logs into indexes, maps, and process views."),
        _edge("e38", "mathlib", "branch_executor", kind="grounds", title="Ground branch exploration", meaning="Discovery branches can search InformalMathLib for analogues before opening external searches."),
        _edge("e39", "high_reward_watch", "proof_queue", kind="proposes", title="Spawn dependent proof tasks", meaning="A strong intermediate result automatically seeds follow-up prove tasks."),
        _edge("e40", "high_reward_watch", "discovery_branch_queue", kind="proposes", title="Spawn dependent discovery branches", meaning="A strong intermediate result also reopens discovery around the new local frontier."),
        _edge("e41", "theorem_body_normalizer", "proof_queue", kind="grounds", title="Queue self-contained conjectures", meaning="Proof tasks inherit typed theorem excerpts and licensing information."),
        _edge("e42", "prior_art_pass", "branch_executor", kind="grounds", title="Foundation-search support", meaning="Discovery branches can request targeted external frameworks once local failure is recorded."),
    ]

    lane_defs = [{**lane, "glyph": SYMBOL_GLYPHS.get(lane["symbol"], lane["symbol"])} for lane in LANES]
    node_type_defs = [{**kind, "glyph": SYMBOL_GLYPHS.get(kind["symbol"], kind["symbol"])} for kind in NODE_TYPES]
    edge_type_defs = [{**kind, "glyph": SYMBOL_GLYPHS.get(kind["symbol"], kind["symbol"])} for kind in EDGE_TYPES]
    process_spine = [{**step, "glyph": SYMBOL_GLYPHS.get(step["symbol"], step["symbol"])} for step in PROCESS_SPINE]

    spine_node_ids = {
        node_id
        for step in process_spine
        for node_id in step["node_ids"]
    }
    spine_edge_ids = {
        edge_id
        for step in process_spine
        for edge_id in step["edge_ids"]
    }
    for node in nodes:
        node["spine"] = node["id"] in spine_node_ids
    for edge in edges:
        edge["spine"] = edge["id"] in spine_edge_ids

    return {
        "metadata": {
            "title": "Epistemic Systems Visual Language",
            "subtitle": "End-to-end agent society map for discovery, proof, governance, and reflection.",
            "library": "Cytoscape.js",
            "design_rationale": "A typed directed graph with a stable preset layout fits epistemic circuits better than a force layout because the agent society has known phases, persistent stores, recurrent control loops, and a process spine that should remain legible across runs.",
            "universal_binding": "The notation ties each agent to universal epistemic roles: grounding, generation, critique, aggregation, persistence, routing, reflection, and controlled recursion.",
            "width": 1680,
            "height": 1040,
        },
        "lanes": lane_defs,
        "node_types": node_type_defs,
        "edge_types": edge_type_defs,
        "process_spine": process_spine,
        "nodes": nodes,
        "edges": edges,
    }


def render_markdown(model: dict[str, Any]) -> str:
    """Render the visual language as a compact human-readable specification."""

    lines = [
        "# Epistemic Systems Visual Language",
        "",
        f"Library: {model['metadata']['library']}",
        "",
        "## Design",
        "",
        model["metadata"]["design_rationale"],
        "",
        "The map binds platform-specific agents to universal inference functions: grounding, generation, aggregation, critique, persistence, routing, and reflection.",
        "",
        "## Lanes",
        "",
    ]
    for lane in model["lanes"]:
        lines.append(
            f"- `{lane['symbol']}` **{lane['label']}**: {lane['description']} "
            f"Question: {lane['question']} System role: {lane['system_role']}"
        )
    lines.extend(["", "## Epistemic Process Spine", ""])
    for index, step in enumerate(model["process_spine"], start=1):
        lines.append(
            f"{index}. `{step['symbol']}` **{step['title']}**: {step['description']} "
            f"Guiding question: {step['question']}"
        )
    lines.extend(["", "## Node Types", ""])
    for kind in model["node_types"]:
        lines.append(
            f"- `{kind['symbol']}` **{kind['label']}**: {kind['meaning']} "
            f"Epistemic move: {kind['epistemic_move']}"
        )
    lines.extend(["", "## Edge Types", ""])
    for kind in model["edge_types"]:
        lines.append(f"- `{kind['symbol']}` **{kind['label']}**: {kind['meaning']}")
    lines.extend(["", "## Core Nodes", ""])
    for node in model["nodes"]:
        lines.append(
            f"- **{node['title']}** (`{node['id']}`): {node['function']} "
            f"Universal binding: {node['universal_binding']}"
        )
    return "\n".join(lines) + "\n"


def render_html(model: dict[str, Any]) -> str:
    """Render an interactive HTML view using Cytoscape.js."""

    payload = json.dumps(model, indent=2)
    process_cards_html = "\n".join(
        (
            f'<button class="process-card" type="button" data-step="{step["id"]}">'
            f'<div class="process-step">{index}. <span class="math-symbol">\\({step["symbol"]}\\)</span></div>'
            f'<div class="process-title">{step["title"]}</div>'
            f'<div class="process-question">{step["question"]}</div>'
            f'<div class="process-description">{step["description"]}</div>'
            "</button>"
        )
        for index, step in enumerate(model["process_spine"], start=1)
    )
    channel_legend_html = "\n".join(
        (
            f'<li><span class="math-symbol">\\({edge_type["symbol"]}\\)</span>'
            f'<strong>{edge_type["label"]}</strong>: {edge_type["meaning"]}</li>'
        )
        for edge_type in model["edge_types"]
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{model["metadata"]["title"]}</title>
  <script>
    window.MathJax = {{
      tex: {{
        inlineMath: [['\\\\(', '\\\\)']]
      }},
      svg: {{
        fontCache: 'global'
      }}
    }};
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
  <script src="https://unpkg.com/cytoscape@3.29.2/dist/cytoscape.min.js"></script>
  <style>
    body {{
      margin: 0;
      font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
      background: #f6f4ee;
      color: #222;
    }}
    .page {{
      display: grid;
      grid-template-columns: 1.8fr 1fr;
      min-height: 100vh;
    }}
    .graph-panel {{
      padding: 20px 20px 16px 20px;
      background: linear-gradient(180deg, #faf8f2 0%, #f3f0e5 100%);
      border-right: 1px solid #d7d0c4;
    }}
    .title {{
      margin: 0 0 8px 0;
      font-size: 28px;
      letter-spacing: 0.02em;
    }}
    .subtitle {{
      margin: 0 0 14px 0;
      max-width: 1100px;
      color: #524e47;
      line-height: 1.45;
    }}
    .controls {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px 18px;
      align-items: flex-start;
      margin-bottom: 14px;
      padding: 12px 14px;
      border: 1px solid #d8d0c3;
      border-radius: 14px;
      background: rgba(255, 255, 255, 0.72);
    }}
    .control-group {{
      min-width: 180px;
    }}
    .control-group strong {{
      display: block;
      margin-bottom: 6px;
      font-size: 13px;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      color: #5c564d;
    }}
    .control-group label {{
      display: block;
      font-size: 14px;
      margin: 4px 0;
    }}
    .how-to-read {{
      margin-bottom: 14px;
      padding: 14px 16px;
      border-radius: 14px;
      background: rgba(255, 255, 255, 0.72);
      border: 1px solid #d8d0c3;
      line-height: 1.5;
    }}
    .process-strip {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 12px;
      margin-bottom: 14px;
    }}
    .process-card {{
      appearance: none;
      text-align: left;
      padding: 14px 14px 12px 14px;
      border-radius: 14px;
      border: 1px solid #d8d0c3;
      background: rgba(255, 255, 255, 0.82);
      cursor: pointer;
      transition: transform 120ms ease, border-color 120ms ease, box-shadow 120ms ease;
    }}
    .process-card:hover {{
      transform: translateY(-1px);
      border-color: #b96a32;
      box-shadow: 0 8px 18px rgba(80, 54, 21, 0.08);
    }}
    .process-card.active {{
      border-color: #b44f27;
      box-shadow: 0 10px 24px rgba(180, 79, 39, 0.14);
      background: rgba(255, 248, 239, 0.95);
    }}
    .process-step {{
      font-size: 12px;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      color: #5d554a;
      margin-bottom: 8px;
    }}
    .process-title {{
      font-size: 16px;
      font-weight: 700;
      margin-bottom: 6px;
      color: #2d2a26;
    }}
    .process-question {{
      font-size: 13px;
      font-weight: 600;
      line-height: 1.45;
      color: #3d3832;
      margin-bottom: 6px;
    }}
    .process-description {{
      font-size: 13px;
      line-height: 1.45;
      color: #5c564d;
    }}
    .how-to-read h2, .sidebar h2 {{
      margin: 0 0 10px 0;
      font-size: 18px;
    }}
    #cy-wrap {{
      position: relative;
      border: 1px solid #d8d0c3;
      border-radius: 18px;
      overflow: hidden;
      background:
        linear-gradient(to bottom,
          #f3efe3 0 19.5%,
          #eef5ea 19.5% 38.5%,
          #eaf1f7 38.5% 57.5%,
          #f8ecec 57.5% 76.5%,
          #f0edf8 76.5% 100%);
    }}
    #cy {{
      width: 100%;
      height: 920px;
    }}
    .lane-tag {{
      position: absolute;
      left: 16px;
      padding: 4px 10px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.85);
      border: 1px solid rgba(40, 40, 40, 0.1);
      font-size: 12px;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      color: #544f48;
      pointer-events: none;
    }}
    .sidebar {{
      padding: 22px 20px;
      background: linear-gradient(180deg, #fffdf7 0%, #f6f2e8 100%);
    }}
    .card {{
      margin-bottom: 16px;
      padding: 16px 18px;
      border: 1px solid #d8d0c3;
      border-radius: 16px;
      background: rgba(255, 255, 255, 0.78);
    }}
    .math-symbol {{
      display: inline-block;
      padding: 3px 8px;
      margin-right: 8px;
      border-radius: 999px;
      background: #efe8d8;
      font-size: 13px;
      vertical-align: middle;
      min-width: 28px;
      text-align: center;
    }}
    .muted {{
      color: #5a544c;
      line-height: 1.5;
    }}
    .channel-list {{
      margin: 10px 0 0 0;
      padding-left: 18px;
    }}
    .channel-list li {{
      margin: 8px 0;
      line-height: 1.45;
    }}
    .dossier-note {{
      margin-top: 12px;
      padding: 10px 12px;
      border-radius: 12px;
      background: #f6f0e3;
      border: 1px solid #dfd2b8;
      color: #4b453c;
      line-height: 1.45;
    }}
    .mini-list {{
      margin: 8px 0 0 0;
      padding-left: 18px;
    }}
    .mini-list li {{
      margin: 4px 0;
      line-height: 1.45;
    }}
    .tooltip {{
      position: absolute;
      z-index: 20;
      max-width: 360px;
      padding: 10px 12px;
      border-radius: 12px;
      border: 1px solid #d5cdbf;
      background: rgba(255, 253, 247, 0.96);
      box-shadow: 0 14px 34px rgba(0, 0, 0, 0.12);
      pointer-events: none;
      font-size: 13px;
      line-height: 1.45;
      display: none;
      white-space: normal;
    }}
  </style>
</head>
<body>
  <div class="page">
    <section class="graph-panel">
      <h1 class="title">{model["metadata"]["title"]}</h1>
      <p class="subtitle">{model["metadata"]["subtitle"]} Cytoscape.js is used because this is a typed directed systems graph with explicit stores, loops, and control edges rather than a force-discovered social network.</p>
      <div class="controls">
        <div class="control-group">
          <strong>Visibility Filters</strong>
          <label><input type="checkbox" data-kind-filter="all" checked> Show all node kinds</label>
          <label><input type="checkbox" data-kind="store" checked> Stores</label>
          <label><input type="checkbox" data-kind="generator" checked> Generators</label>
          <label><input type="checkbox" data-kind="critic" checked> Critics</label>
          <label><input type="checkbox" data-kind="controller" checked> Controllers</label>
        </div>
        <div class="control-group">
          <strong>More Kinds</strong>
          <label><input type="checkbox" data-kind="normalizer" checked> Normalizers</label>
          <label><input type="checkbox" data-kind="aggregate" checked> Aggregators</label>
          <label><input type="checkbox" data-kind="publisher" checked> Publishers</label>
          <label><input type="checkbox" data-kind="external" checked> External sources</label>
        </div>
        <div class="control-group">
          <strong>Edge Types</strong>
          <label><input type="checkbox" data-edge="grounds" checked> Grounds</label>
          <label><input type="checkbox" data-edge="proposes" checked> Proposes</label>
          <label><input type="checkbox" data-edge="critiques" checked> Critiques</label>
          <label><input type="checkbox" data-edge="loops" checked> Loops</label>
        </div>
      </div>
      <div class="how-to-read">
        <h2>Epistemic Process</h2>
        <div class="muted">
          The graph is a systems map, but the discovery logic is surfaced explicitly through the clickable process spine below. Each step names the epistemic question being answered and highlights the agents, stores, and control edges that currently carry that burden.
        </div>
      </div>
      <div class="process-strip">
        {process_cards_html}
      </div>
      <div class="how-to-read">
        <h2>How To Read The Map</h2>
        <div class="muted">
          Read the page in two ways at once. Vertically, each lane is a phase of the research society: grounding, discovery, prove, governance, and reflection.
          Horizontally, the process spine shows the end-to-end epistemic flow from licensed material to conceptual nexus, proof pressure, controlled recursion, and reflective publication.
          Directed edges encode not just sequence but systems channels: grounding, proposal, aggregation, critique, persistence, routing, import, and recursion.
        </div>
      </div>
      <div id="cy-wrap">
        <div class="lane-tag" style="top: 18px;">Grounding</div>
        <div class="lane-tag" style="top: 208px;">Discovery</div>
        <div class="lane-tag" style="top: 398px;">Prove</div>
        <div class="lane-tag" style="top: 588px;">Governance</div>
        <div class="lane-tag" style="top: 778px;">Reflection</div>
        <div id="cy"></div>
        <div id="tooltip" class="tooltip"></div>
      </div>
    </section>
    <aside class="sidebar">
      <div class="card">
        <h2>System Channels</h2>
        <div class="muted">
          The page is intentionally system-like: stores hold memory, generators expand the frontier, critics apply back-pressure, controllers govern recursion, and publishers externalize the current state for experts.
        </div>
        <ul class="channel-list">
          {channel_legend_html}
        </ul>
      </div>
      <div id="dossier" class="card">
        <h2>Selected Element</h2>
        <div class="muted">Select a process step, node, or edge to inspect its epistemic function, system role, and contribution to the end-to-end reasoning loop.</div>
        <div class="dossier-note">
          Start with the process cards if you want the big picture. Select graph elements when you want to inspect the specific agent, store, or control dependency that carries that epistemic function.
        </div>
      </div>
    </aside>
  </div>
  <script>
    const model = {payload};
    const tooltip = document.getElementById("tooltip");
    const dossier = document.getElementById("dossier");

    const elements = [
      ...model.nodes.map((node) => ({{
        group: "nodes",
        data: node,
        position: {{ x: node.x, y: node.y }}
      }})),
      ...model.edges.map((edge) => ({{
        group: "edges",
        data: edge
      }}))
    ];

    const laneColors = Object.fromEntries(model.lanes.map((lane) => [lane.id, lane.color]));
    const laneMeta = Object.fromEntries(model.lanes.map((lane) => [lane.id, lane]));
    const processMap = Object.fromEntries(model.process_spine.map((step) => [step.id, step]));
    const nodeTitleMap = Object.fromEntries(model.nodes.map((node) => [node.id, node.title]));
    const edgeColor = {{
      grounds: "#5e5548",
      proposes: "#3f6d49",
      aggregates: "#78621d",
      critiques: "#465a86",
      routes: "#b06224",
      persists: "#48726d",
      imports: "#7a4b68",
      loops: "#9a4f4f"
    }};
    const kindShape = {{
      store: "round-rectangle",
      normalizer: "diamond",
      generator: "round-hexagon",
      aggregate: "cut-rectangle",
      critic: "hexagon",
      controller: "ellipse",
      publisher: "tag",
      external: "vee"
    }};

    const cy = cytoscape({{
      container: document.getElementById("cy"),
      elements,
      layout: {{ name: "preset", fit: true, padding: 40 }},
      minZoom: 0.7,
      maxZoom: 1.4,
      style: [
        {{
          selector: "node",
          style: {{
            "background-color": (ele) => laneColors[ele.data("lane")] || "#ddd",
            "shape": (ele) => kindShape[ele.data("kind")] || "round-rectangle",
            "label": (ele) => ele.data("glyph") + "\\n" + ele.data("title"),
            "text-wrap": "wrap",
            "text-max-width": 160,
            "text-valign": "center",
            "text-halign": "center",
            "font-size": 12,
            "font-family": "Segoe UI, Arial, sans-serif",
            "border-width": 2,
            "border-color": "#3b342b",
            "color": "#222",
            "width": 172,
            "height": 74,
            "padding": 8
          }}
        }},
        {{
          selector: "node[spine]",
          style: {{
            "border-width": 3,
            "border-color": "#7d4a1b"
          }}
        }},
        {{
          selector: "edge",
          style: {{
            "curve-style": "bezier",
            "width": (ele) => ele.data("spine") ? 3.2 : 2.2,
            "line-color": (ele) => edgeColor[ele.data("kind")] || "#6b6258",
            "target-arrow-color": (ele) => edgeColor[ele.data("kind")] || "#6b6258",
            "target-arrow-shape": "triangle",
            "arrow-scale": 1.05,
            "font-size": 10,
            "font-family": "Cascadia Code, Consolas, monospace",
            "label": (ele) => ele.data("glyph"),
            "text-background-color": "#fff8ec",
            "text-background-opacity": 0.95,
            "text-background-padding": 2,
            "color": "#3c362f"
          }}
        }},
        {{
          selector: 'edge[kind = "persists"]',
          style: {{
            "line-style": "dotted"
          }}
        }},
        {{
          selector: 'edge[kind = "routes"]',
          style: {{
            "line-style": "solid"
          }}
        }},
        {{
          selector: 'edge[kind = "loops"]',
          style: {{
            "line-style": "dashed",
            "line-color": "#9a4f4f",
            "target-arrow-color": "#9a4f4f"
          }}
        }},
        {{
          selector: 'edge[kind = "critiques"]',
          style: {{
            "line-color": "#465a86",
            "target-arrow-color": "#465a86"
          }}
        }},
        {{
          selector: ".dimmed",
          style: {{
            "opacity": 0.10
          }}
        }},
        {{
          selector: ".selected",
          style: {{
            "border-color": "#c04b2f",
            "border-width": 4,
            "line-color": "#c04b2f",
            "target-arrow-color": "#c04b2f",
            "z-index": 999
          }}
        }}
      ]
    }});

    function typesetMath(targets) {{
      if (window.MathJax && typeof window.MathJax.typesetPromise === "function") {{
        window.MathJax.typesetPromise(targets).catch(() => null);
      }}
    }}

    function listHtml(values) {{
      if (!values || !values.length) {{
        return "<div class=\\"muted\\">None recorded.</div>";
      }}
      return "<ul class=\\"mini-list\\">" + values.map((value) => "<li>" + value + "</li>").join("") + "</ul>";
    }}

    function mathBadge(symbol) {{
      return `<span class="math-symbol">\\(${{symbol}}\\)</span>`;
    }}

    function titleCase(value) {{
      return value
        .split("-")
        .map((part) => part ? part.charAt(0).toUpperCase() + part.slice(1) : part)
        .join(" ");
    }}

    function defaultDossierHtml() {{
      return `
        <h2>Selected Element</h2>
        <div class="muted">Select a process step, node, or edge to inspect its epistemic function, system role, and contribution to the end-to-end reasoning loop.</div>
        <div class="dossier-note">
          Start with the process cards if you want the big picture. Select graph elements when you want to inspect the specific agent, store, or control dependency that carries that epistemic function.
        </div>
      `;
    }}

    function nodeDossier(data) {{
      const lane = laneMeta[data.lane];
      return `
        <h2>${{data.title}}</h2>
        <div class="muted">${{mathBadge(data.symbol)}}${{data.function}}</div>
        <p class="muted"><strong>Epistemic move:</strong> ${{data.epistemic_move}}</p>
        <p class="muted"><strong>Universal binding:</strong> ${{data.universal_binding}}</p>
        <p class="muted"><strong>Lane:</strong> ${{lane.label}} | <strong>Lane question:</strong> ${{lane.question}}</p>
        <p class="muted"><strong>Node type:</strong> ${{titleCase(data.kind)}} | <strong>System role:</strong> ${{lane.system_role}}</p>
        <h3>Established Properties</h3>
        ${{listHtml(data.properties)}}
        <h3>Inputs</h3>
        ${{listHtml(data.inputs)}}
        <h3>Outputs</h3>
        ${{listHtml(data.outputs)}}
        <div class="dossier-note">This node is one system primitive in the larger epistemic process: it either stores, transforms, critiques, routes, or publishes inferential material.</div>
      `;
    }}

    function edgeDossier(data) {{
      const sourceTitle = nodeTitleMap[data.source] || data.source;
      const targetTitle = nodeTitleMap[data.target] || data.target;
      return `
        <h2>${{data.title}}</h2>
        <div class="muted">${{mathBadge(data.symbol)}}${{data.meaning}}</div>
        <p class="muted"><strong>Edge type:</strong> ${{titleCase(data.kind)}} | <strong>From:</strong> ${{sourceTitle}} | <strong>To:</strong> ${{targetTitle}}</p>
        <p class="muted">This edge is a systems channel rather than a mere connector. It specifies what kind of epistemic traffic moves between stages: evidence, proposals, critiques, routing decisions, persistence, imports, or recursive feedback.</p>
        <div class="dossier-note">The graph is systemic because these channels are typed. A route edge means control, a persistence edge means durable memory, and a critique edge means back-pressure.</div>
      `;
    }}

    function processDossier(step) {{
      const relatedNodes = step.node_ids.map((nodeId) => nodeTitleMap[nodeId] || nodeId);
      return `
        <h2>${{step.title}}</h2>
        <div class="muted">${{mathBadge(step.symbol)}}${{step.description}}</div>
        <p class="muted"><strong>Guiding question:</strong> ${{step.question}}</p>
        <h3>Participating Nodes</h3>
        ${{listHtml(relatedNodes)}}
        <div class="dossier-note">This is the epistemic backbone of the system. It is broader than any single agent: it names the inferential function being carried across several coordinated components.</div>
      `;
    }}

    function nodeTooltip(data) {{
      return `
        <strong>${{data.title}}</strong><br>
        ${{mathBadge(data.symbol)}}<span>${{data.function}}</span><br>
        <span class="muted"><strong>Epistemic move:</strong> ${{data.epistemic_move}}</span>
      `;
    }}

    function edgeTooltip(data) {{
      return `
        <strong>${{data.title}}</strong><br>
        ${{mathBadge(data.symbol)}}<span>${{data.meaning}}</span><br>
        <span class="muted"><strong>Channel:</strong> ${{titleCase(data.kind)}}</span>
      `;
    }}

    function showTooltip(html, x, y) {{
      tooltip.innerHTML = html;
      tooltip.style.display = "block";
      tooltip.style.left = (x + 14) + "px";
      tooltip.style.top = (y + 14) + "px";
      typesetMath([tooltip]);
    }}

    function hideTooltip() {{
      tooltip.style.display = "none";
    }}

    function clearSelections() {{
      cy.elements().removeClass("selected").removeClass("dimmed");
      document.querySelectorAll(".process-card").forEach((card) => card.classList.remove("active"));
    }}

    function updateDossier(ele) {{
      if (!ele) {{
        dossier.innerHTML = defaultDossierHtml();
        typesetMath([dossier]);
        return;
      }}
      dossier.innerHTML = ele.isNode() ? nodeDossier(ele.data()) : edgeDossier(ele.data());
      typesetMath([dossier]);
    }}

    function focusProcessStep(stepId) {{
      const step = processMap[stepId];
      if (!step) {{
        return;
      }}
      clearSelections();
      document.querySelector(`.process-card[data-step="${{stepId}}"]`)?.classList.add("active");
      const activeNodeIds = new Set(step.node_ids);
      const activeEdgeIds = new Set(step.edge_ids);
      cy.nodes().forEach((node) => {{
        if (activeNodeIds.has(node.id())) {{
          node.addClass("selected");
        }} else {{
          node.addClass("dimmed");
        }}
      }});
      cy.edges().forEach((edge) => {{
        if (activeEdgeIds.has(edge.id())) {{
          edge.addClass("selected");
        }} else {{
          edge.addClass("dimmed");
        }}
      }});
      dossier.innerHTML = processDossier(step);
      typesetMath([dossier]);
    }}

    function applyFilters() {{
      const activeKinds = Array.from(document.querySelectorAll("[data-kind]"))
        .filter((box) => box.checked)
        .map((box) => box.getAttribute("data-kind"));
      const activeEdges = Array.from(document.querySelectorAll("[data-edge]"))
        .filter((box) => box.checked)
        .map((box) => box.getAttribute("data-edge"));
      cy.nodes().forEach((node) => {{
        node.style("display", activeKinds.includes(node.data("kind")) ? "element" : "none");
      }});
      cy.edges().forEach((edge) => {{
        const visible = activeEdges.includes(edge.data("kind")) &&
          edge.source().style("display") !== "none" &&
          edge.target().style("display") !== "none";
        edge.style("display", visible ? "element" : "none");
      }});
    }}

    document.querySelectorAll("[data-kind], [data-edge]").forEach((input) => {{
      input.addEventListener("change", applyFilters);
    }});

    document.querySelectorAll(".process-card").forEach((card) => {{
      card.addEventListener("click", () => {{
        focusProcessStep(card.getAttribute("data-step"));
      }});
    }});

    cy.on("mouseover", "node, edge", (event) => {{
      const data = event.target.data();
      showTooltip(
        event.target.isNode() ? nodeTooltip(data) : edgeTooltip(data),
        event.renderedPosition.x,
        event.renderedPosition.y
      );
    }});
    cy.on("mouseout", "node, edge", hideTooltip);
    cy.on("tap", "node, edge", (event) => {{
      clearSelections();
      event.target.addClass("selected");
      updateDossier(event.target);
    }});
    cy.on("tap", (event) => {{
      if (event.target === cy) {{
        clearSelections();
        updateDossier(null);
      }}
    }});

    applyFilters();
    updateDossier(null);
    typesetMath([document.body]);
  </script>
</body>
</html>
"""


def write_outputs(model: dict[str, Any], *, docs_dir: Path) -> dict[str, Path]:
    """Write the JSON, Markdown, and HTML artefacts to disk."""

    docs_dir.mkdir(parents=True, exist_ok=True)
    out_json = docs_dir / "epistemic-process-map.json"
    out_md = docs_dir / "epistemic-systems-visual-language.md"
    out_html = docs_dir / "epistemic-process-map.html"
    out_json.write_text(json.dumps(model, indent=2) + "\n", encoding="utf-8")
    out_md.write_text(render_markdown(model), encoding="utf-8")
    out_html.write_text(render_html(model), encoding="utf-8")
    return {"json": out_json, "markdown": out_md, "html": out_html}


def main() -> int:
    """Generate the epistemic systems map artefacts."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=Path(__file__).resolve().parents[4] / "docs",
        help="Directory where the epistemic systems map artefacts should be written.",
    )
    args = parser.parse_args()

    model = build_process_model()
    write_outputs(model, docs_dir=args.docs_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

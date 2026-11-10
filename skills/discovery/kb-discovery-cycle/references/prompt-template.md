<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Prompt Template


## Intent Gate

Use this prompt only when the task matches this skill contract:

Run the discovery cycle that turns completed reasoning artifacts into a persistent proof queue of concrete prove-or-disprove targets. Use when the user wants to queue the next informal proof tasks, prioritize discovery outputs into a file-backed queue, or prepare theorem-pair-specific claims for later proof work.

Do not use it as a generic brainstorming prompt or as a substitute for an adjacent skill. Keep the scope tied to the specific claim, route, artifact set, or decision named in the input packet.

## Self-Contained Context Packet

Before solving, restate the context in a compact explicit packet:
- problem or kb_ref
- exact claim, route, object, or artifact under inspection
- exact input artifacts, IDs, excerpts, or paths in scope
- exact decision to make or artifact to produce
- constraints, evidence policy, and output format

If any required item is missing, say so explicitly and do not invent hidden context, broaden the task silently, or rely on repository background that is not named in the packet.

## Prompt-Diagnosis And Qualified Certainty Gate

When the task involves substantive inference rather than pure extraction, formatting, or rendering, run a short self-critical pre-pass:
- classify `context_status`: `well-posed` | `partially-ill-posed` | `ill-posed`
- classify `inference_status`: `determined` | `underdetermined` | `difficult-but-well-posed`
- list the exact blocking context or prompt defects if the packet is not well behaved
- state the smallest repair that would make the task self-contained
- estimate `certainty_now` and `certainty_if_well_posed` using only `very-low` | `low` | `medium` | `high`

Do not confuse malformed context with hard mathematics. If the packet is ill-posed, make that diagnosis explicit and keep any mathematical conclusion provisional.

If the task produces a report, table, narrative assessment, or recommendation, prepend a short `Prompt/Inference Diagnosis` block before the main result with:
- `context_status`
- `inference_status`
- `blocking_defects`
- `minimal_repair`
- `certainty_now`
- `certainty_if_well_posed`

If `context_status` is `well-posed` and the inference is routine, keep this block concise. If the packet is ill-posed or the inference is underdetermined, do not hide this diagnosis inside later prose.

Use the shared epistemic shape from [docs/research-methods/epistemic-prompt-framework.md](../../../../docs/research-methods/epistemic-prompt-framework.md).

## Parallel Mathematical Packet

When the discovery output is theorem-shaped, do not return prose alone.

For each theorem candidate, route-local lemma, or theorem-sized discovery packet, emit a parallel `mathematical_layers` object with:

- `informal`
- `latex`
- `lean_style`

Minimum required fields:

- `mathematical_layers.quantifier_signature`
- `mathematical_layers.object_signature`
- `mathematical_layers.symbol_ledger`
- `mathematical_layers.latex.theorem_statement`
- `mathematical_layers.lean_style.scaffold`

The Lean-style layer is a notation-disciplined type-theory scaffold, not executable Lean unless that is explicitly stated.
Mark it as non-executable when it is only a theorem-shape packet.

Do not use words like `equivalence`, `transport`, `coherence`, `factorization`, or `commutativity` unless the packet also names:

- the quantified carrier or family;
- the bridge witness type or map;
- the invariant-preservation predicate;
- the exact theorem type in LaTeX and Lean-style form.

## Lean/Lake Search Packet

When the input artifacts contain `lean_symbolic_search`, read it as bounded symbolic discovery evidence over typed route signatures.
Do not collapse it into prose and do not describe it as a proof.

Extract and report:

- `build_ok`
- route `readiness.mode` and `readiness.blockers`
- explored `search_shapes`
- route-level `candidate_count`
- whether the theorem packet came from heuristic discovery, bounded symbolic search, or both

Interpretation rules:

- `build_ok = false` means a tooling or packet defect unless the artifact explicitly records a mathematical impossibility;
- `search_shapes` tell you which bridge families are locally live, not which theorems are already proved;
- `candidate_count = 0` is only weak negative evidence, and only when the route is `symbolic-search-ready`;
- a generated Lean module path or scaffold does not mean the theorem is formalized.

Objective: turn discovery artifacts into a small queue of concrete prove-or-disprove tasks.

Required structure:

1. Candidate route
- bridge id
- source statement id
- target statement id
- route synopsis

2. Claim under test
- claim type: route lemma, conditional proposition, or negative claim
- exact claim text
- candidate bridge object
- preserved invariant

3. Why this enters the queue now
- why the claim is mathematically inspectable
- why proving it would matter
- why disproving it would also matter
- why this route is better than adjacent lower-priority routes

4. Queue decision
- enqueue or skip
- reason
- initial priority

5. Parallel mathematical packet
- quantifier signature
- symbol ledger
- LaTeX theorem statement
- Lean-style scaffold
- one-sentence gloss explaining how the notation matches the prose claim

6. Bounded symbolic search reading
- readiness mode: `llm-first` | `hybrid-llm-plus-symbolic` | `symbolic-search-ready`
- explored search shapes
- build/tool health
- how the symbolic search changes queue confidence or route choice

Escalation rule:

If the candidate still relies on a schematic bridge object, do not queue it as if it were already proof-ready.
First convert the gap into a declarative search profile and run the non-immediate bridge search prompts in [../../kb-concept-bridge-planner/references/non-immediate-bridge-search.md](../../kb-concept-bridge-planner/references/non-immediate-bridge-search.md).

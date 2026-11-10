# Higher Abductive Theory Discovery

This repository is a runnable, local-first implementation of a systematic
reasoner for abstract mathematical and physical theory discovery. It maps
theory fragments, identifies conceptual pressure and essential fragmentation,
runs plural philosophical reflection, proposes typed completions, evaluates
their relevance, and returns surviving candidates to proofs, models,
simulations, or experiments.

The system deliberately separates generation from validation. Relevance is a
multi-objective research-policy judgment—not a truth score—and every generated
claim is either source-backed or marked conjectural.

## What is implemented

- Canonical typed records for contexts, fragments, morphisms, pressures,
  meaning profiles, fragmentation sites, reflections, hypotheses, validation
  outcomes, run states, and provenance.
- All 17 skills in the original catalogue, each callable through one stable
  `SkillResult` contract.
- Deterministic default generation plus a provider-neutral generation
  protocol for hosted or local language models.
- Pressure–leverage–return gates, a relevance vector, explicit penalties,
  and Pareto-frontier portfolio selection.
- Eight philosophical lenses and twelve conceptual redescription operators.
- SQLite metadata, content-addressed artifacts, replay manifests, and audit
  checks.
- Formal adapters for Lean, MMT, GATlab, Cubical Agda, and SMT, with honest
  availability reporting and safe dry runs.
- A guarded research-run state machine, CLI, minimal JSON HTTP API, JSON/LaTeX
  export, and tests.

## Quick start

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e .
tdr skills
tdr demo --project ./demo-project
tdr inspect --project ./demo-project
python -m unittest discover -s tests -v
```

Run an individual skill:

```bash
tdr run-skill evaluate-relevance --input candidate.json --pretty
```

Start the local API:

```bash
tdr serve --project ./demo-project --port 8765
```

## Research lifecycle

`SCOPED → MAPPED → PRESSURED → FRAGMENTED → REFLECTED → GENERATED → GATED → FORMALIZED → INSTANTIATED → TESTED → SYNTHESIZED`

Repeated structural failures can route a run to `REPRESENTATION_REVIEW`.
Human approval remains mandatory for changing protected commitments, migrating
accepted content, resolving genuine ontological choices, promoting a theory as
substantive, or proposing irreversible external action.

## Layout

- `src/tdr/domain`: records, invariants, serialization
- `src/tdr/atlas`: fragments, mappings, and higher cells
- `src/tdr/pressures`: pressure interpretation and dependency impact
- `src/tdr/reflection`: meaning, fragmentation, lenses, operators
- `src/tdr/generation`: provider-neutral candidate generation
- `src/tdr/relevance`: gates, scores, and Pareto selection
- `src/tdr/validation`: formal and adversarial adapters
- `src/tdr/provenance`: SQLite and immutable artifacts
- `src/tdr/orchestration`: policies and guarded state transitions
- `src/tdr/skills`: the 17 executable epistemic operations
- `skills`: generated distributable skill contracts
- `schemas`: portable JSON Schemas
- `tests`: unit, contract, metamorphic, adversarial, and end-to-end tests

## Epistemic status

This is research infrastructure, not an autonomous oracle. It makes assumptions,
uncertainties, failures, and return paths explicit. It can organize abduction,
surface high-leverage conceptual moves, and compile them into validations; it
cannot mechanically guarantee novelty, scientific truth, or philosophical
adequacy.


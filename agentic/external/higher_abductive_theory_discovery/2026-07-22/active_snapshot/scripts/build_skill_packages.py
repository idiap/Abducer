#!/usr/bin/env python3
"""Mechanically materialize all distributable skill directories from the catalogue."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import textwrap

from tdr.skills import CATALOG, execute_skill


PROCEDURES = {
    "scope-research-context": ["Separate the research question from preferred answers.", "Make scope, regime, protected commitments, success criteria, stop criteria, and budgets explicit.", "Stage the context and request human review for later goal or commitment changes."],
    "map-theory-fragment": ["Segment source-addressable definitions, types, symbols, axioms, claims, models, observables, and scopes.", "Mark an unsourced proposal as conjectural; never present it as extracted fact.", "Stage the fragment; do not merge it into an accepted atlas."],
    "propose-theory-morphism": ["Declare source and target fragments and the mapping domain.", "Map every declared source symbol and every scope restriction.", "Emit typing, satisfaction, and scope-preservation obligations; keep the map staged."],
    "interpret-conceptual-pressure": ["Localize the anomaly, blocker, fragmentation, explanatory gap, prediction gap, pragmatic need, or scope failure.", "Attach evidence, reliability, severity, and downstream dependency impact.", "Record any preferred solution separately so it does not masquerade as the pressure."],
    "profile-concept-meaning": ["Reconstruct referential, inferential, identity, modal, operational, scope, explanatory, pragmatic, and protected-distinction components.", "Ground each component in native sources where possible.", "Mark missing components unknown and assign component-level uncertainty."],
    "detect-essential-fragmentation": ["Compare meaning profiles component by component.", "Attempt lexical normalization, unit alignment, definitional extension, known equivalence, conservative interpretation, then scope restriction.", "Estimate residual fragmentation only after repairs; surface protected losses and request review when commitments change."],
    "run-philosophical-reflection": ["Run hermeneutic, phenomenological-operational, constitutive, dialectical, genealogical, pragmatic, structural-realist, and modal-counterfactual lenses independently.", "Compare convergence, contradiction, and complementarity.", "Produce at least three redescriptions, including a primitive shift and a conservative option, plus losses, counterworlds, and formal/concrete obligations."],
    "diagnose-categorical-defect": ["Translate interpretive tension into typed objects, morphisms, diagrams, and witnesses.", "Test representability, coherence, descent, factorization, adjunction, obstruction, and meta-theory diagnoses.", "Flag every mapping that remains metaphorical rather than typed."],
    "generate-theory-candidates": ["Explore local completion, bridge, mechanism, and representation-mutation modes.", "Normalize proposals into hypothesis packages and quotient obvious equivalences.", "Reject packages without formalization hooks, concrete return paths, falsifiers, or explicit conjectural status."],
    "evaluate-relevance": ["Report the pressure, leverage, and return gates independently.", "Estimate unblocking, explanatory, unification, predictive, transport, pragmatic, necessity, and robustness value.", "Subtract complexity, fragility, auxiliary, and risk penalties; retain a Pareto frontier and never infer truth from priority."],
    "formalize-candidate": ["Compile the candidate into declared formal objects and obligations.", "Check local typing and syntax before invoking an optional formal adapter.", "Return exact blockers or residual proof obligations; do not claim proof from generated skeletons."],
    "prove-transport": ["Check totality on the declared domain and preservation of scope and satisfaction.", "Attempt each theorem transport through the staged morphism.", "Exclude trivial restatements and return kernel-check obligations explicitly."],
    "instantiate-concretely": ["Choose target mathematical models and, where applicable, physical systems or experiments.", "Construct the abstract-to-concrete and return maps.", "Supply equations or executable plans, approximation assumptions, error bounds, and discriminating outcomes."],
    "falsify-candidate": ["Search degenerate cases, scope boundaries, rival explanations, protected losses, hidden auxiliaries, and vacuity.", "Retain falsifying conditions and failed checks as first-class artifacts.", "Never let relevance override a falsification."],
    "mutate-representation": ["Require a repeated structural failure pattern, not one failed proof.", "Specify a new object and morphism grammar and a migration functor.", "Report information loss, newly expressible structure, an unblocked pressure, and mandatory human migration review."],
    "synthesize-portfolio": ["Compute the eligible Pareto frontier without scalar collapse.", "Join supportive and adversarial validations by candidate while retaining disagreement and uncertainty.", "Recommend promotion review, another discriminating test, suspension, or rejection; never hide failures."],
    "audit-reasoning-run": ["Verify source and replay provenance for every event.", "Check that generators did not validate their own candidates.", "Check budget compliance, scope drift, terminal conditions, and deterministic replay; emit remediations for every failure."],
}


EXAMPLES = {
    "scope-research-context": {"question": "Which universal object represents bilinear maps?", "goals": ["unblock factorization"], "scope": {"domain": "R-modules"}},
    "map-theory-fragment": {"name": "Bilinear maps", "sources": [{"artifact_id": "s1", "locator": "notes", "content": "Sort: Module\nSymbol: b : M x N -> P\nClaim: b is linear in each input\nScope: R-modules"}]},
    "propose-theory-morphism": {"source_fragment": {"fragment_id": "a", "symbols": {"b": "MxN->P"}}, "target_fragment": {"fragment_id": "b", "symbols": {"u": "MxN->T"}}, "symbol_map": {"b": "u"}, "scope_map": {"R-modules": "R-modules"}},
    "interpret-conceptual-pressure": {"events": [{"description": "Proof cannot derive a unique factorization", "locus": ["factorization"], "severity": 0.9}]},
    "profile-concept-meaning": {"concept_id": "interaction", "theory_id": "raw-maps", "referential_role": ["two-input map"]},
    "detect-essential-fragmentation": {"profiles": [{"profile_id": "a", "concept_id": "interaction", "theory_id": "A", "identity_criteria": ["pointwise"]}, {"profile_id": "b", "concept_id": "interaction", "theory_id": "B", "identity_criteria": ["unique isomorphism"]}], "downstream_impact": 0.9},
    "run-philosophical-reflection": {"site": {"site_id": "s", "concept_ids": ["interaction"], "theory_ids": ["A", "B"], "mismatch_vector": {"identity_criteria": 1.0}, "protected_losses": ["two input roles"]}},
    "diagnose-categorical-defect": {"site": {"site_id": "s", "theory_ids": ["A", "B"], "mismatch_vector": {"identity_criteria": 1.0}}, "reflection": {"formal_obligations": ["type the comparison"]}},
    "generate-theory-candidates": {"pressures": [{"pressure_id": "p", "description": "factorization blocker"}], "defects": [{"kind": "representability", "severity": 0.9}]},
    "evaluate-relevance": {"candidate": {"candidate_id": "c", "mode": "bridge", "pressure_ids": ["p"], "atlas_patch": {"objects": ["T"], "morphisms": ["u"]}, "consequences": ["recover factorization"], "return_paths": [{"target": "model", "method": "construct"}], "validation_tasks": []}, "context": {"context_id": "q"}},
    "formalize-candidate": {"candidate": {"candidate_id": "c", "formal_move": "Adjoin T and u", "atlas_patch": {"objects": ["T"], "morphisms": ["u"]}, "assumptions": []}},
    "prove-transport": {"morphism": {"morphism_id": "m", "total_on_declared_domain": True, "scope_map": {"R": "R"}, "obligations": []}, "theorems": [{"name": "factorization", "statement": "exists unique f"}]},
    "instantiate-concretely": {"candidate": {"candidate_id": "c", "return_paths": [{"target": "finite modules", "method": "construct"}]}, "targets": ["finite modules"]},
    "falsify-candidate": {"candidate": {"candidate_id": "c"}, "test_results": {"degenerate_case": "passed"}},
    "mutate-representation": {"failures": [{"reason": "scope cannot be typed"}, {"reason": "scope cannot be typed"}], "sterile_pressure_ids": ["p"]},
    "synthesize-portfolio": {"candidates": [{"candidate_id": "c"}], "evaluations": [{"candidate_id": "c", "eligible": True, "relevance_vector": {"unblocking": 0.5, "explanatory": 0.5, "unification": 0.5, "predictive": 0.5, "transport": 0.5, "pragmatic": 0.5, "necessity": 0.5, "robustness": 0.5}, "penalties": {"complexity": 0.2, "fragility": 0.2, "auxiliaries": 0.2, "risk": 0.2}, "priority_index": 0.4}]},
    "audit-reasoning-run": {"trace": [{"skill_name": "map-theory-fragment", "input_hash": "abc", "result_hash": "def", "role": "atlas-cartographer"}]},
}


def title(name: str) -> str:
    return " ".join(word.capitalize() for word in name.split("-"))


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def materialize(root: Path) -> None:
    output_schema = json.loads((Path(__file__).parents[1] / "schemas" / "skill-result.schema.json").read_text())
    for name, spec in CATALOG.items():
        directory = root / name
        procedure = "\n".join(f"{index}. {step}" for index, step in enumerate(PROCEDURES[name], start=1))
        required = ", ".join(f"`{item}`" for item in spec.required) or "a JSON object"
        human = f"\n## Human gate\n\nPause for explicit human review when {spec.human_gate}." if spec.human_gate else ""
        skill_md = f'''---
name: {name}
description: {spec.purpose} Use when a theory-discovery workflow needs this bounded {spec.role} operation.
---

# {title(name)}

Perform one bounded epistemic operation and return the common `SkillResult` envelope. Treat generated material as staged and conjectural until an independent validator accepts it.

## Inputs

Require {required}. Validate the complete input against `input.schema.json`. Preserve source locators, scope, regime, uncertainty, and parent artifact identifiers.

## Procedure

{procedure}

## Runtime

When the `tdr` package is installed, run:

```bash
python -m tdr.api.cli run-skill {name} --input INPUT.json --pretty
```

The executable wrapper is `scripts/run_skill.py`. If the runtime is unavailable, follow the procedure directly and still emit the exact envelope in `output.schema.json`.

## Boundaries

- Act only as `{spec.role}`; do not approve your own generative output.
- Do not infer truth, novelty, or identity from relevance, graph structure, embeddings, or fluent prose.
- Keep incompatible interpretations separate until a validated equivalence or synthesis exists.
- Return `blocked` with missing information when preconditions fail; do not silently guess.
- Stop after one bounded operation or when the policy budget is exhausted.
{human}

## Output

Return `status`, `artifacts`, `claims`, `uncertainties`, `next`, and `provenance`. Label each claim as sourced, conjectural, interpretive, validated, or falsified as applicable.
'''
        input_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": f"{title(name)} input",
            "type": "object",
            "required": list(spec.required),
            "properties": {item: {} for item in spec.required},
            "additionalProperties": True,
        }
        policy = textwrap.dedent(f"""
            version: "1.0"
            role: "{spec.role}"
            tools:
              - "local-files-read"
              - "tdr-runtime"
            budget:
              steps: 1
              wall_seconds: {int(spec.budget['wall_seconds'])}
            stop:
              - "one SkillResult has been emitted"
              - "precondition is missing"
              - "budget is exhausted"
            escalation: "{spec.human_gate or 'none; return blocked when authority is missing'}"
            canonical_write: false
        """)
        default_prompt = f"Use ${name} to {spec.purpose[0].lower() + spec.purpose[1:]}"
        if len(default_prompt) > 180:
            default_prompt = f"Use ${name} to perform its bounded theory-discovery operation."
        openai_yaml = textwrap.dedent(f'''\
            interface:
              display_name: "{title(name)}"
              short_description: "{spec.purpose[:60].rstrip('. ')}"
              default_prompt: "{default_prompt}"
            policy:
              allow_implicit_invocation: true
        ''')
        run_script = textwrap.dedent(f'''\
            #!/usr/bin/env python3
            import argparse
            import json
            import subprocess
            import sys

            parser = argparse.ArgumentParser()
            parser.add_argument("input")
            args = parser.parse_args()
            command = [sys.executable, "-m", "tdr.api.cli", "run-skill", "{name}", "--input", args.input, "--pretty"]
            try:
                raise SystemExit(subprocess.call(command))
            except FileNotFoundError:
                print(json.dumps({{"status": "blocked", "artifacts": [], "claims": [], "uncertainties": [{{"reason": "tdr runtime unavailable"}}], "next": [{{"action": "install higher-abductive-theory-discovery"}}], "provenance": {{}}}}))
                raise SystemExit(2)
        ''')
        contract_test = textwrap.dedent(f'''\
            import json
            from pathlib import Path
            import unittest

            class ContractTest(unittest.TestCase):
                def test_contract_files_and_example(self):
                    root = Path(__file__).parents[1]
                    for relative in ("SKILL.md", "input.schema.json", "output.schema.json", "policy.yaml", "examples/minimal_input.json", "examples/expected_output.json"):
                        self.assertTrue((root / relative).exists(), relative)
                    output = json.loads((root / "examples/expected_output.json").read_text())
                    self.assertIn(output["status"], ("completed", "partial", "blocked", "invalid"))
                    self.assertEqual(set(("artifacts", "claims", "uncertainties", "next", "provenance")) - output.keys(), set())

            if __name__ == "__main__":
                unittest.main()
        ''')
        example = EXAMPLES[name]
        expected = execute_skill(name, example)
        write(directory / "SKILL.md", skill_md)
        write(directory / "input.schema.json", json.dumps(input_schema, indent=2, sort_keys=True))
        write(directory / "output.schema.json", json.dumps(output_schema, indent=2, sort_keys=True))
        write(directory / "policy.yaml", policy)
        write(directory / "agents" / "openai.yaml", openai_yaml)
        write(directory / "scripts" / "run_skill.py", run_script)
        write(directory / "prompts" / "system.md", f"You are the {spec.role}. Execute only the `{name}` contract. Preserve epistemic status, scope, uncertainty, and provenance. Never validate your own generated content.")
        write(directory / "prompts" / "task.md", f"Apply `{name}` to the supplied JSON. Follow SKILL.md in order and return only a schema-valid SkillResult.")
        write(directory / "prompts" / "critique.md", f"Audit the proposed `{name}` result for missing sources, scope erasure, authority overreach, hidden conjectures, incomplete obligations, and policy-budget violations.")
        write(directory / "tests" / "test_contract.py", contract_test)
        write(directory / "tests" / "test_invariance.py", "# Metamorphic invariants are exercised by the shared runtime test suite.\n")
        write(directory / "tests" / "test_adversarial.py", "# Adversarial authority and scope tests are exercised by the shared runtime test suite.\n")
        write(directory / "examples" / "minimal_input.json", json.dumps(example, indent=2, sort_keys=True))
        write(directory / "examples" / "expected_output.json", json.dumps(expected, indent=2, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).parents[1] / "skills")
    args = parser.parse_args()
    materialize(args.root)


if __name__ == "__main__":
    main()


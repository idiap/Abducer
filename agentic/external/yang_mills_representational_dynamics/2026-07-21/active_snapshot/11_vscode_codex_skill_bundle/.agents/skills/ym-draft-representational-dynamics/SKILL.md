---
name: ym-draft-representational-dynamics
description: "Develop a philosophy-of-physics and mathematical-foundations paper on representational dynamics: how physical descriptions transform, forget, preserve, and recover structure across gauge, regulator, scale, continuum, and spectral representations. Use to formalize representation packages and morphisms, test the framework on Yang--Mills, engage structural realism and renormalization literature, and avoid converting a conceptual calculus into an unsupported physical theorem."
---

# Draft the Representational Dynamics Paper

## Identify the philosophical contribution

Formulate a precise thesis that is neither the generic claim that models have maps nor the metaphysical claim that the universe is merely information. Distinguish descriptive variables, physical observables, redundancy, approximation, emergence, and ontology.

Use Yang--Mills as the sustained case study, not as evidence that the Clay problem is solved.

## Strengthen the calculus

1. Define a representation package with state space, physical algebra, symmetries or redundancies, dynamics, scale, limit data, and certified properties.
2. Type morphisms by what they preserve exactly, approximate with an error modulus, forget, and recover through a theorem.
3. Add composition laws for quantitative errors and property certificates.
4. Represent property loss and recovery, approximate commutative diagrams, cutoff/volume-indexed families, and noncommuting limits.
5. Define observable fidelity, positivity fidelity, locality range, gauge-orbit fidelity, and spectral fidelity without conflating them.
6. Give at least one nontrivial proposition whose content exceeds Boolean conjunction and additive error bookkeeping.
7. Build counterexamples showing why preserving gauge covariance alone, local actions alone, or finite spectra alone does not preserve physical identity.
8. Apply the calculus to the chain from lattice gauge fields through RG and continuum Schwinger data to a Hamiltonian spectrum.

## Philosophical engagement

Compare the framework with structural realism, perspectival or model-based realism, gauge equivalence, duality, effective-field-theory and RG epistemology, categorical formulations, and information-theoretic physics. State both overlap and difference. Treat “information” relationally only after identifying its bearer, equivalence relation, and operational or inferential role.

## Quality gates

- Every formal symbol must do argumentative work.
- Include worked examples and failure cases, not only definitions.
- Separate ontology, semantics, epistemology, and proof methodology.
- Replace sweeping “universe” claims with conditional metaphysical options and objections.
- Add a literature map and an explicit novelty argument.
- Ask a mathematical physicist and a philosopher of physics to be able to reject different parts independently.

## Manuscript production workflow

Run the specialist skills in this order:

1. Use `ym-develop-paper-proofs` for the formal definitions, transport propositions, and nonuniform-limit countermodels; classify philosophical arguments separately from mathematical theorems.
2. Use `ym-ground-paper-literature` to map structural realism, gauge equivalence, duality, EFT/RG epistemology, perspectival realism, categorical approaches, and information-theoretic physics.
3. Use `ym-frame-paper-narrative` to derive the motivation and introduction from the representation-loss problem and the Yang--Mills case study.
4. Use `ym-build-proof-appendix` for formal definitions, long propositions, countermodel calculations, and the complete Yang--Mills property-transport table when these interrupt the main argument.
5. Use `ym-build-latex-paper` to assemble, lint, compile, render, and inspect the final philosophy/mathematical-foundations paper.
6. Run `ym-audit-frontier` on every technical Yang--Mills implication before the final build.

## Output contract

Produce a standalone paper, glossary, formal definitions and propositions, two detailed case studies or one case study plus countermodels, literature comparison table, objection/reply section, conservative statement of scope, compiled PDF, preview pages, and build report. Use `ym-audit-frontier` for all Yang--Mills implications.

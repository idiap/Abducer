<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Top-Paper Criteria For The Formula Footprints Program

- Status: `implemented`
- Target level: selective complexity-theory paper, e.g. CCC/ITCS-style scrutiny.
- Use: this is the working gate for the loop. A draft can be called publication-level only if it passes these criteria or explicitly chooses a lower venue target.

## Criteria

### C1. One-Line Theorem Identity

The paper must have a single memorable theorem identity that a referee can repeat without internal jargon.  It should say what object is bounded, in what model, by what resource, and why it matters.

Pass evidence:
- theorem statement in standard complexity language;
- clear model and quantifier regime;
- no dependence on marathon-specific names.

### C2. Nonvacuous Instantiation

At least one main theorem must be instantiated on a nontrivial family.  Counting existence can support model sanity, but a top paper needs either an explicit family, a standard proof/certificate system, or a crisp rank/expansion theorem that makes the hypothesis checkable.

Pass evidence:
- explicit construction or named standard model;
- proof that the hardness/certificate predicate is nonempty there;
- no circular use of the desired SAT or P vs NP lower bound.

### C3. Technical Novelty Beyond Definitions

The main result must not be an immediate consequence of the definitions plus sparse patching.  There must be a technical move a reader would recognize as doing work.

Pass evidence:
- new lemma/proof device, e.g. batched dictionary, randomized minimax argument, extraction theorem, or tight separation;
- comparison to naive bound;
- statement of what fails without the device.

### C4. Sharpness Or Separating Examples

The theory should show that its bounds are tight, close to tight, or separate natural models.  Necessary conditions alone are not enough for a top venue unless the application is very strong.

Pass evidence:
- matching upper bounds up to controlled factors, or
- explicit separations between formula, occurrence, quotient, randomized, or proof-system models.

### C5. Standard-Model Or Extraction Payoff

If the paper is motivated by proof complexity or SAT lower bounds, at least one theorem must touch a recognizable model or prove an extraction theorem from a recognizable restricted system.

Pass evidence:
- named proof/certificate system, or
- formal extraction from a standard proof artifact to formula/occurrence/quotient certificates;
- controlled overhead.

### C6. Randomized/Interactive Robustness Or Boundary

If deterministic certificates are the main object, the paper must either extend to bounded-error/randomized/interactive certificates or give a sharp boundary explaining why the deterministic theory stops there.

Pass evidence:
- bounded-error theorem, minimax/distributional lower bound, or
- explicit counterexample/boundary theorem.

### C7. Literature Closure

The related-work section must anticipate the nearest-referee objection, not only cite broad areas.  It must explain relation and novelty delta against Partial MCSP, circuit test suites/anti-checkers, teaching/specification dimension, exact certification, hardness magnification, natural proofs, and proof complexity.

Pass evidence:
- comparison table or prose with novelty deltas;
- exact citations;
- explicit statement of what is not new.

### C8. Proof Completeness And Auditability

Every theorem-level claim must have definitions, assumptions, proof steps, and proof dependencies visible.  Hidden advice, uniformity shifts, and semantic SAT assumptions must be impossible to miss.

Pass evidence:
- proof dependency graph or theorem-status table;
- model, length, exponent, uniformity, and advice conditions stated;
- no unproved lemma silently serving as the main result.

### C9. Honest Scope And Nonclaim Discipline

The draft must not imply P != NP, SAT outside P/poly, or proof-system lower bounds unless those are actually proved.  Nonclaims should appear before the reader forms the wrong impression.

Pass evidence:
- abstract/introduction nonclaims;
- application labelled conditional where appropriate;
- proof-system and randomized claims not promoted without theorems.

### C10. Consequence Worth The Paper Length

The paper must leave the reader with either a new theorem they can use, a new barrier boundary they can test, or a new proof obligation whose formulation is itself valuable.

Pass evidence:
- crisp corollary/application;
- finite verifier or worked example;
- next theorem target that is mathematically narrower than the original problem.

### C11. Cohered Results Criterion: One Sharp, Novel, Weighty Result Package

The paper must treat cohered results as a criterion: one result package centered on a sharp theorem, not a fragmented ensemble of results or a bundle of disconnected payoffs.  This is a formal admission gate, not an editorial afterthought.  A paper that merely accumulates locally correct results still fails C11 if those results do not cohere into one recognizable before/after theorem arc.  The package should have one sharp result that is novel relative to the nearest literature and weighty enough to change how the reader understands the relevant obstacle, model, or proof obligation.  It is not enough for the draft to contain useful definitions, local lemmas, or many partial repairs; the reader should be able to say what was understood before, what is understood after, and why the delta matters.

Pass evidence:
- a central sharp theorem whose hypotheses and conclusion are tight, separating, or boundary-forming;
- a clear account of how supporting theorems cohere around the flagship result rather than competing with it;
- a narrative-indivisibility test: each admitted theorem would lose force, or become misleadingly motivated, if detached from the flagship theorem arc;
- a novelty delta against the closest papers stated in before/after form;
- an explicit explanation of how the result changes understanding, e.g. by relocating a proof obligation, exposing a barrier, separating certificate models, or turning a vague hardness intuition into a checkable condition;
- title, abstract, introduction, theorem order, and conclusion all aligned around the same result;
- supporting lemmas serve the flagship narrative rather than diffusing it.
- the final paper reads as a cohered result arc: flagship theorem, calibrating sharpness examples, controlled extensions, and nonclaim boundaries all answer the same question.
- every new theorem or corollary declares its role as flagship, calibration, interface variant, proof-system bridge, or boundary, and states the before/after understanding shift it contributes to the same flagship spine.

Fail evidence:
- multiple theorem-like results that can be removed or reordered without changing the paper's main meaning;
- supporting results advertised as independent payoffs instead of consequences, calibrations, or boundaries of the flagship theorem;
- no single before/after understanding shift that explains why the result package matters;
- novelty scattered across definitions, examples, and partial repairs rather than concentrated in a sharp result;
- an ensemble of results where each component may be locally correct but the paper has no single flagship theorem carrying the narrative weight;
- a fragmented ensemble of results whose components require separate motivations rather than serving one theorem arc;
- results that can be narrated as separate mini-papers rather than as one cohered result package;
- a conclusion that lists achievements but does not identify the one result that changed the problem.

Operational admission rule:
- admit a new result to the main theorem package only if it strengthens the formula-footprint spine, calibrates its sharpness, extends its proof-system reach with controlled overhead, or clarifies a nonclaim boundary;
- reject or quarantine locally correct additions that merely enlarge the ensemble without changing the reader's understanding of the flagship obstruction;
- when in doubt, demote the result to a queue or appendix unless it can state its role, its before/after understanding shift, its dependence on the same flagship obstruction, and why it should not be read as a separate mini-paper.

## Gate Decision Rule

- `top_ready`: all critical criteria C1-C9 and C11 pass, and C10 passes or needs only harmless minor revision.
- `solid_preprint`: C1, C3, C7, C8, C9 pass; C11 is at least partial; and at least one of C2, C4, C5, or C6 remains partial.
- `internal_only`: any of C1, C3, C7, C8, or C9 fails, or C11 is missing/unclear.

The current loop must optimize the first failed or partial critical criterion in this order:

1. C11 cohered results criterion: one sharp result package with novelty, weight, and an understanding shift;
2. C2 nonvacuous instantiation;
3. C5 standard-model/extraction payoff;
4. C6 randomized/interactive robustness;
5. C4 sharpness/separations;
6. C7 literature closure.

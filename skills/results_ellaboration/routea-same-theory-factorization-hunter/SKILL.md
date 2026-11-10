---
name: routea-same-theory-factorization-hunter
description: Search for same-theory realizations of Route A normalization factors. Use when a geometric collar or Wilson block introduces diagonal, congruence, Schur-kernel, reflected-Gram, or pair-dependent quotient factors and the paper must decide whether positivity is preserved in the same regulated theory.
---

# Route A Same-Theory Factorization Hunter

## Target

Given a candidate normalization factor \(B_{ij}\), decide whether it is admissible by one of:

- observable rescaling;
- invertible block congruence;
- Schur product with a PSD kernel;
- reflected-Gram realization in the same regulated Wilson theory.

Pair-dependent entrywise quotients are inadmissible unless the entrywise inverse factor is separately certified.

## Deterministic Support

Use `check_schur_factor_candidates.py` for finite matrix checks. It can test PSD, entrywise inverse PSD, and quotient risk on explicit candidate matrices. These checks are necessary but not sufficient for same-theory realization.

## Generative Work

For a PSD factor, try to explain its same-theory origin:

- diagonal factors from observable normalization;
- character-expansion kernels with nonnegative coefficients;
- auxiliary reflected observables;
- block congruence induced by a basis change.

If no same-theory origin is available, emit an inadmissibility lemma rather than a normalization theorem.


## Epistemic Discipline

Treat each manuscript result as a mathematical object with an explicit epistemic status: proved, certified finite, conditional, conjectural, blocked, or demoted. Cite evidence through source artifacts, paper labels, validation reports, deterministic script outputs, or explicit unknowns. Preserve the finite/geometric/endpoint/continuum claim boundary, and end with a validation handoff or unresolved obligations.

## Output Contract

Return: factor inventory, finite PSD check, entrywise inverse check, proposed same-theory realization, missing realization step, admissibility verdict, manuscript proposition or obstruction text, and next geometry/normalization repair.

## Failure/Demotion

Demote if the argument says "positive denominator implies positive inverse", treats finite PSD as same-theory realization without proof, or hides pair-dependent division inside notation.

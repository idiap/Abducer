---
name: visual-analogy-preservation-auditor
description: Audit theorem-level visual analogies for property preservation, mathematical distortion, physical relevance, and proof-search value. Use before a visual metaphor can influence branch selection, hypothesis promotion, report claims, or deep-reflection cycle decisions.
---

# Visual Analogy Preservation Auditor

Use this skill to decide whether a visual metaphor is faithful enough to guide future mathematical or physical work.

## Mathematical Invariants

Audit the mathematical object behind the image: formal statement, source object, target object, carrier, maps, invariants, symmetries, order/limit structure, positivity or sign conditions, and proof obligation. The analogy may preserve intuition only when these invariants are explicitly mapped.

Required edge cases and counterexamples include false friends, proxy shifts, finite-to-global gaps, visual smoothness hiding singular behavior, hidden compactness or regularity, noncommuting limits, and physical-carrier distortions.

## Epistemic Discipline

Every analogy audit must state epistemic status, evidence citation, source artifacts, explicit unknowns, and validation handoff. A metaphor is not evidence; it can only be explanation, a hypothesis seed, a missing-artifact locator, a falsifier prompt, or quarantine material.

Disconfirming evidence or distorted properties must block route influence. If the visual mapping cannot name a route mutation, missing artifact, falsifier, counterfactual variant, or representation requirement, demote it to explanation-only.

## Audit Procedure

1. Reconstruct the source and target:
   - formal statement or concept
   - visual metaphor
   - claimed source-to-image and target-to-image mappings
   - proposed hypothesis or route consequence

2. Check preservation dimensions:
   - invariants
   - symmetries
   - gauge or equivalence-class structure
   - locality/globality
   - order, monotonicity, or variational direction
   - positivity, sign, or convexity structure
   - limiting behavior and order of limits
   - physical carrier or observable meaning
   - proof-obligation correspondence

3. Find false friends:
   - proxy shift
   - definitional transfer
   - finite-to-global gap
   - noncommuting limits
   - hidden compactness, regularity, or uniformity
   - visual smoothness hiding singular or endpoint behavior
   - explanatory force mistaken for proof force

4. Judge hypothesis value:
   - Does the analogy create a concrete route mutation?
   - Does it name a missing artifact?
   - Does it identify a cheap falsifier?
   - Does it clarify a representation requirement?
   - Does it improve publication-weighty physical or mathematical understanding?

5. Assign disposition:
   - `usable_for_explanation`
   - `usable_for_hypothesis_generation`
   - `needs_revision`
   - `quarantine`
   - `reject`

## Output Contract

Return a `visual_analogy_audit` object with:

- `audit_verdict`
- `preserved_properties`
- `distorted_properties`
- `false_friend_risks`
- `physical_relevance_verdict`
- `proof_search_value`
- `allowed_route_consequence`
- `required_revision`
- `non_claim_boundary`

## Promotion Rule

A visual analogy may affect future cycles only when the audit records at least one concrete route mutation, missing artifact, falsifier, counterfactual variant, or representation requirement. Otherwise keep it as explanation-only or quarantine it.

## Failure/Demotion

Reject or quarantine analogies that distort load-bearing invariants, hide a target-equivalent assumption, erase a hard mathematical or physical boundary, lack evidence citation, or invite a proxy shift. Demote analogies with no validation handoff or no concrete proof-search value.

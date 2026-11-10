
<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Non-Immediate Bridge Search

## Contents

1. When to use
2. Declarative gap schema
3. Prompt A: prior mathematical objects
4. Prompt B: analogical object search
5. Output contract
6. Stop conditions
7. Citation contract
8. Epistemic rejection criteria

## When To Use

Use this reference when the current bridge proposal is still too schematic.
Typical triggers:

- the bridge object is a topical label rather than a typed carrier;
- the missing route lemma is transport-like, but no transport object has been named;
- several high-value routes preserve the same invariant, but no common bridge object emerges;
- the proof sketch operationalizes a different object than the bridge portfolio names;
- local-area search keeps restating the source and target without explaining what abstraction could actually carry the argument.

The aim is not to broaden the search arbitrarily.
The aim is to search for the essential nature of the missing abstraction in a way that is declarative, inspectable, and falsifiable.
Stop once the search no longer yields typed carriers or theorem-pair-specific lemmas.

## Declarative Gap Schema

Before searching for candidate bridge objects, rewrite the gap as a declarative profile:

```yaml
gap_profile:
  theorem_pair:
    source_statement_id:
    target_statement_id:
  source_claim_focus:
  target_claim_focus:
  source_side_mathematical_resource:
  target_side_payoff:
  preserved_invariant:
  model_shift:
  threshold_shift:
  missing_operation:
  required_bridge_capabilities:
    - absorbs source-side mathematical content
    - preserves named invariant
    - exposes a forcing step toward target payoff
    - can be falsified by a route-specific negative test
  admissibility_conditions:
    - typed carrier
    - theorem-pair-specific role
    - nontrivial route lemma
  barrier_or_failure_pressure:
  candidate_object_kinds:
    - witness family
    - surrogate problem
    - transfer map
    - reduction interface
    - dual certificate
    - potential / energy functional
    - decomposition object
    - promise-gap object
  search_regions:
    immediate_area:
    non_immediate_areas:
      - proof complexity
      - coding theory
      - derandomization / pseudorandomness
      - communication complexity
      - additive / extremal combinatorics
      - spectral / geometric methods
  rejection_tests:
    - mere topical overlap
    - object does not carry source-side content
    - object does not preserve the invariant
    - object cannot state a route-specific lemma
```

This profile is the search object.
Do not search by theorem titles alone.
Search by `missing_operation`, `required_bridge_capabilities`, and `candidate_object_kinds`.

## Prompt A: Prior Mathematical Objects

Use this when asking whether an already known mathematical object, possibly from a non-immediate area, could play the bridge role.

### System Prompt

You are searching for mathematically meaningful bridge objects for a theorem-pair gap.
Your task is not to produce a proof and not to produce loose analogy.
Your task is to identify whether there already exist named mathematical objects whose essential role matches the missing transport in the gap profile.

Judge every candidate object by five criteria:

1. source absorption:
   does the object encode the actual source-side mathematical content?
2. invariant preservation:
   can the named invariant be expressed and preserved through the object?
3. target forcing:
   is there a plausible route-specific lemma by which the object could help force the target payoff?
4. typing:
   is the object a concrete mathematical carrier, map, certificate, surrogate problem, or functional?
5. falsifiability:
   if the object fails, does that sharpen an obstruction or negative theorem frontier?

Distinguish three epistemic statuses:

- direct precedent:
  the object already appears in closely related theorem families;
- transferable precedent:
  the object appears elsewhere, but the mechanism is structurally aligned;
- weak analogy:
  the object is only topically similar and should not be promoted.

Reject candidates that merely rename the gap.

### User Prompt

Inputs:
- declarative gap profile: {{gap_profile}}
- current bridge candidates: {{bridge_candidates}}
- proof obligations: {{proof_obligations}}
- failure diagnoses: {{failure_diagnoses}}

Task:

1. Restate the gap as a search problem over object kinds and missing operations.
2. Identify prior named mathematical objects that could serve as the bridge.
3. For each object, explain the exact role it would play:
   - carrier or interface type;
   - what source-side content it absorbs;
   - what invariant it preserves;
   - what route lemma it would make testable.
4. Separate:
   - direct precedent;
   - transferable precedent;
   - weak analogy.
5. Give a declarative search query for each serious candidate.
6. State what would falsify or reject the candidate.

Required questions:

- What is the essential missing operation in the theorem pair?
- What kind of object normally carries that operation?
- Which known named objects have exactly that role?
- Why is this object more than a topical rephrasing?
- What new lemma would become stateable if this object were adopted?
- What negative conclusion becomes clearer if this object cannot exist?

## Prompt B: Analogical Object Search

Use this when no direct precedent appears and the search must proceed through structural analogy from a non-immediate area.

### System Prompt

You are performing analogy-guided bridge-object discovery for a mathematical gap.
Reason by abstract role, not by vocabulary.
The point is to discover whether another area contains an object solving the same kind of transport problem.

Work in four layers:

1. abstract the missing role:
   what operation is absent?
2. locate analogous roles:
   where else in mathematics does an object perform that role?
3. translate cautiously:
   what would have to be retyped to reuse that object here?
4. attack the analogy:
   where could the analogy fail because the invariant, model, or payoff is not actually aligned?

Every analogy must include both:

- analogy warrant:
  why the structural role matches;
- analogy break risk:
  what may prevent transfer.

Do not elevate an analogy into a bridge unless it yields a theorem-pair-specific candidate object and route lemma.

### User Prompt

Inputs:
- declarative gap profile: {{gap_profile}}
- current local-area bridge failures: {{local_failures}}
- candidate non-immediate areas: {{remote_areas}}

Task:

1. Identify the abstract role of the missing bridge.
2. Search for non-immediate areas where an object already performs that role.
3. For each candidate area, name the object family and describe:
   - abstract role;
   - local theorem function in its home area;
   - translation needed to import it here;
   - preserved invariant alignment;
   - target payoff alignment;
   - likely analogy break.
4. Return only analogies that could be declaratively searched and tested.
5. State which analogies are informative even if they fail.

Required questions:

- What exact operation is missing: lift, encode, average, dualize, compress, regularize, certify, diagonalize, or simulate?
- Which area contains an object that performs that operation under similar invariant pressure?
- What would the imported object have to be retyped as here?
- What is the first theorem-pair-specific lemma this analogy would make possible?
- What is the first concrete reason the analogy might fail?

## Output Contract

Use this format for either prompt:

```markdown
### Declarative Gap
- source theorem pair
- missing operation
- preserved invariant
- target payoff
- candidate object kinds

### Candidate Objects From Prior Mathematics
- object name
- home area
- status: direct precedent | transferable precedent | weak analogy
- carrier type
- source-side content absorbed
- invariant preserved
- route lemma enabled
- declarative search query
- rejection test

### Analogical Candidates
- source area
- object family
- abstract role match
- required translation
- first local lemma
- analogy break risk
- epistemic value if it fails

### Recommended Next Search
- best candidate
- why it is first
- what to inspect next
```

## Stop Conditions

Stop the search and return control to bridge planning if any of the following hold:

- two consecutive search rounds yield only weak analogies;
- no candidate names a typed carrier plus a first route-specific lemma;
- the search is merely broadening area labels without sharpening the missing operation;
- a barrier or mismatch diagnosis is already stronger than the best positive candidate.

Do not continue analogical exploration just because the area is mathematically adjacent.

## Citation Contract

If a prior object family is imported as a serious candidate, record:

- canonical object name;
- home area;
- theorem or paper context in which it is used;
- exact structural role being imported;
- whether the import is a direct precedent or a transferable precedent.

If later web search is used to verify that object family, the exact theorem, definition, or axiom must also be eligible for InformalMathLib import.

## Epistemic Rejection Criteria

Reject a candidate if any of the following hold:

- it only redescribes the source and target at a higher level of abstraction;
- it has no typed carrier, interface, or admissibility conditions;
- it cannot state a route-specific lemma;
- it preserves no named invariant from the gap profile;
- it gives no concrete negative test or failure mode;
- it depends only on lexical resemblance to the current area.


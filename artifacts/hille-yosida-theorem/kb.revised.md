---
kb_id: hille-yosida-theorem
title: Hille-Yosida Theorem and Semigroup Generation
domain: mathematics
subdomain: functional-analysis-semigroup-theory
version: 0.1.0
status: draft
created_utc: 2026-03-12T00:00:00Z
updated_utc: 2026-03-12T00:00:00Z
owners:
  - abducer
source_policy:
  allow_web: true
  allow_local_docs: true
  citation_required: true
---

<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
-->


# Source Index

| source_id | type | citation | locator | reliability | notes |
|---|---|---|---|---|---|
| src.001 | web | https://en.wikipedia.org/wiki/Hille%E2%80%93Yosida_theorem | sections "Formal definitions", "Statement of the theorem", "contraction semigroups" | medium | Practical summary of theorem statements and historical framing |
| src.002 | web | https://en.wikipedia.org/wiki/C0-semigroup | sections "Formal definition", "Infinitesimal generator", "Examples", "Abstract Cauchy problems" | medium | Useful for canonical definitions and classical examples |
| src.003 | book | Engel, K.-J.; Nagel, R. (2000). One-Parameter Semigroups for Linear Evolution Equations. Springer. | Theorem II.3.5, Theorem II.3.8 | high | Standard reference for contraction and exponentially bounded forms |
| src.004 | book | Arendt, W.; Batty, C.; Hieber, M.; Neubrander, F. (2001). Vector-valued Laplace Transforms and Cauchy Problems. Birkhauser. | Corollary 3.3.5, Theorem 3.3.4 | high | Canonical modern treatment |
| src.005 | book | Hille, E. (1948). Functional Analysis and Semi-Groups. AMS Colloquium Publications 31. | historical origin | high | Foundational discovery-era source |

# Symbol Glossary

- `sym.X`: Banach space.
- `sym.Tt`: semigroup operator `T(t)` for `t >= 0`.
- `sym.A`: (possibly unbounded) linear operator, candidate generator.
- `sym.DA`: domain `D(A)` of `A`.
- `sym.rhoA`: resolvent set `rho(A)`.
- `sym.RlambdaA`: resolvent operator `R(lambda,A) = (lambda I - A)^{-1}`.
- `sym.M`: semigroup growth bound constant `M >= 1`.
- `sym.omega`: growth exponent `omega in R`.
- `sym.lambda`: resolvent parameter `lambda`.
- `sym.CP`: abstract Cauchy problem `u'(t)=Au(t), u(0)=x`.

# Concept Structure

```yaml
concept_nodes:
  - id: cnc.c0-semigroup
    label: Strongly Continuous Semigroup (C0-Semigroup)
    type: concept
    notes: |
      Core dynamical object for linear evolution in Banach spaces.
  - id: cnc.generator
    label: Infinitesimal Generator
    type: concept
    notes: |
      Encodes infinitesimal dynamics and determines semigroup evolution.
  - id: cnc.resolvent-bounds
    label: Resolvent Growth Bounds
    type: concept
  - id: cnc.contraction-semigroup
    label: Contraction Semigroup
    type: concept
  - id: cnc.abstract-cauchy-problem
    label: Abstract Cauchy Problem
    type: concept
  - id: cnc.yosida-approximation
    label: Yosida Approximation
    type: concept
  - id: cnc.translation-semigroup
    label: Translation Semigroup
    type: concept
  - id: cnc.heat-semigroup
    label: Heat Semigroup
    type: concept
method_nodes:
  - id: mth.resolvent-estimate
    label: Resolvent Estimate Method
    type: method
  - id: mth.laplace-transform
    label: Laplace Transform Method
    type: method
  - id: mth.dissipativity
    label: Dissipativity Method
    type: method
barrier_nodes:
  - id: bar.powers-of-resolvent-hard-to-verify
    label: High-Order Resolvent Bound Verification Barrier
    type: barrier
  - id: bar.domain-closure-density
    label: Domain Closure/Density Technical Barrier
    type: barrier
relations:
  - from: st.def.c0-semigroup
    to: cnc.c0-semigroup
    relation: defines
  - from: st.def.generator
    to: cnc.generator
    relation: defines
  - from: st.thm.hille-yosida-general
    to: cnc.resolvent-bounds
    relation: uses
  - from: st.thm.hille-yosida-contraction
    to: cnc.contraction-semigroup
    relation: uses
  - from: st.thm.cauchy-problem-equivalence
    to: cnc.abstract-cauchy-problem
    relation: uses
  - from: st.der.yosida-approximation
    to: cnc.yosida-approximation
    relation: defines
  - from: st.ex.translation-semigroup
    to: cnc.translation-semigroup
    relation: uses
  - from: st.ex.heat-semigroup-lp
    to: cnc.heat-semigroup
    relation: uses
  - from: st.thm.hille-yosida-general
    to: mth.resolvent-estimate
    relation: uses
  - from: st.thm.hille-yosida-general
    to: mth.laplace-transform
    relation: uses
  - from: st.thm.lumer-phillips
    to: mth.dissipativity
    relation: uses
  - from: bar.powers-of-resolvent-hard-to-verify
    to: st.thm.hille-yosida-general
    relation: obstructs
  - from: bar.domain-closure-density
    to: st.thm.hille-yosida-general
    relation: obstructs
  - from: st.thm.lumer-phillips
    to: st.thm.hille-yosida-contraction
    relation: reexpresses
  - from: st.ex.translation-semigroup
    to: st.thm.hille-yosida-contraction
    relation: supports
```

# Canonical Statements

```yaml
id: st.def.c0-semigroup
kind: definition
status: accepted
latex: |
  Let X be a Banach space. A family (T(t))_{t >= 0} subset L(X) is a C_0-semigroup if
  T(0)=I, T(t+s)=T(t)T(s) for all s,t>=0, and for every x in X:
  ||T(t)x - x|| -> 0 as t downarrow 0.
informal: |
  A C0-semigroup is a strongly continuous one-parameter semigroup of bounded
  operators on a Banach space.
source_ids: [src.001, src.002, src.003]
used_symbols: [sym.X, sym.Tt]
depends_on: []
concept_roles: [cnc.c0-semigroup]
statement_phase: foundational-definitions
bridge_roles: [semigroup-foundation]
method_tags: [laplace-transform]
barrier_family: ""
confidence: 0.98
proof_sketch: ""
notes: |
  Core object for semigroup generation and abstract evolution equations.
```

```yaml
id: st.def.generator
kind: definition
status: accepted
latex: |
  For a C_0-semigroup (T(t))_{t >= 0}, define
  Ax := lim_{h downarrow 0} (T(h)x - x)/h
  on the domain D(A) of all x for which the limit exists.
informal: |
  The generator is the right derivative at time zero of the semigroup orbit.
source_ids: [src.001, src.002, src.003]
used_symbols: [sym.A, sym.DA, sym.Tt]
depends_on: [st.def.c0-semigroup]
concept_roles: [cnc.generator, cnc.c0-semigroup]
statement_phase: foundational-definitions
bridge_roles: [generator-foundation]
method_tags: [laplace-transform]
barrier_family: ""
confidence: 0.98
proof_sketch: ""
notes: |
  Generator is closed and densely defined when it comes from a C0-semigroup.
```

```yaml
id: st.prop.generator-closed-dense
kind: proposition
status: accepted
latex: |
  If A is the generator of a C_0-semigroup on X, then A is closed and D(A) is dense in X.
informal: |
  Being a generator imposes strong domain regularity: closure and density.
source_ids: [src.001, src.002, src.003]
used_symbols: [sym.A, sym.DA, sym.X]
depends_on: [st.def.c0-semigroup, st.def.generator]
concept_roles: [cnc.generator]
statement_phase: foundational-regularity
bridge_roles: [regularity-prerequisite]
method_tags: [laplace-transform]
barrier_family: domain-regularity
confidence: 0.96
proof_sketch: |
  Use semigroup continuity at zero and graph convergence arguments for closure;
  approximate arbitrary x by resolvent-smoothed points to show density.
notes: |
  This is a necessary condition used directly in Hille-Yosida.
```

```yaml
id: st.def.resolvent
kind: definition
status: accepted
latex: |
  For an operator A, lambda in rho(A) if (lambda I - A):D(A)->X is bijective with bounded inverse.
  The inverse is R(lambda,A) := (lambda I - A)^{-1}.
informal: |
  The resolvent set contains parameters where lambda I minus A is invertible with
  bounded inverse.
source_ids: [src.002, src.003, src.004]
used_symbols: [sym.A, sym.lambda, sym.rhoA, sym.RlambdaA]
depends_on: []
concept_roles: [cnc.resolvent-bounds]
statement_phase: foundational-definitions
bridge_roles: [resolvent-foundation]
method_tags: [resolvent-estimate]
barrier_family: ""
confidence: 0.97
proof_sketch: ""
notes: |
  Resolvent conditions are central in generation theorems.
```

```yaml
id: st.thm.hille-yosida-general
kind: theorem
status: accepted
latex: |
  Let A be a linear operator on Banach space X, with constants M>=1 and omega in R.
  Then A generates a C_0-semigroup (T(t))_{t>=0} with ||T(t)|| <= M e^{omega t}
  iff:
  (i) A is closed and D(A) is dense;
  (ii) (omega, +infty) subset rho(A) and for all lambda>omega and all n in N:
  ||(lambda I - A)^{-n}|| <= M / (lambda-omega)^n.
informal: |
  Hille-Yosida gives a complete characterization of generators of exponentially
  bounded C0-semigroups via closure, density, and resolvent power bounds.
source_ids: [src.001, src.003, src.004]
used_symbols: [sym.A, sym.DA, sym.X, sym.M, sym.omega, sym.lambda, sym.rhoA, sym.Tt]
depends_on:
  - st.def.c0-semigroup
  - st.def.generator
  - st.def.resolvent
  - st.prop.generator-closed-dense
concept_roles: [cnc.c0-semigroup, cnc.generator, cnc.resolvent-bounds]
statement_phase: core-generation-theorem
bridge_roles: [core-characterization]
method_tags: [resolvent-estimate, laplace-transform]
barrier_family: powers-of-resolvent-verification
confidence: 0.95
proof_sketch: |
  Necessity follows from semigroup-resolvent representation and generator regularity.
  Sufficiency builds approximants (Yosida approximations) from resolvents, establishes
  compact convergence on bounded time intervals, and proves semigroup properties and
  growth bounds in the limit.
notes: |
  In applications the n-th power resolvent estimates are often hard to verify directly.
```

```yaml
id: st.thm.hille-yosida-contraction
kind: theorem
status: accepted
latex: |
  (Contraction case) A generates a contraction C_0-semigroup
  (||T(t)|| <= 1 for t>=0) iff:
  (i) A is closed and D(A) is dense;
  (ii) (0,+infty) subset rho(A) and ||(lambda I-A)^{-1}|| <= 1/lambda for all lambda>0.
informal: |
  For contraction semigroups, checking only the first resolvent bound is enough.
source_ids: [src.001, src.003, src.004]
used_symbols: [sym.A, sym.DA, sym.Tt, sym.lambda, sym.rhoA]
depends_on:
  - st.thm.hille-yosida-general
  - st.def.resolvent
concept_roles: [cnc.contraction-semigroup, cnc.resolvent-bounds]
statement_phase: core-generation-theorem
bridge_roles: [contraction-specialization]
method_tags: [resolvent-estimate]
barrier_family: ""
confidence: 0.96
proof_sketch: |
  Specialize Hille-Yosida with M=1, omega=0 and exploit norm monotonicity to reduce
  high-order resolvent checks to n=1.
notes: |
  This form is commonly used in Markov and dissipative PDE settings.
```

```yaml
id: st.thm.lumer-phillips
kind: theorem
status: accepted
latex: |
  A densely defined operator A on Banach space X generates a contraction C_0-semigroup
  iff A is dissipative and (lambda_0 I - A) is surjective for some lambda_0 > 0.
informal: |
  Lumer-Phillips provides an equivalent generator criterion for contraction semigroups
  using dissipativity and one surjectivity condition.
source_ids: [src.001, src.003]
used_symbols: [sym.A, sym.DA, sym.X]
depends_on:
  - st.thm.hille-yosida-contraction
concept_roles: [cnc.contraction-semigroup]
statement_phase: equivalent-characterizations
bridge_roles: [dissipativity-bridge]
method_tags: [dissipativity]
barrier_family: domain-closure-density
confidence: 0.93
proof_sketch: |
  Combine dissipativity resolvent estimate with range condition and apply contraction
  generation theory.
notes: |
  Often easier to verify than direct resolvent power bounds.
```

```yaml
id: st.thm.cauchy-problem-equivalence
kind: theorem
status: accepted
latex: |
  For closed A on Banach space X, the following are equivalent:
  (i) A generates a C_0-semigroup T;
  (ii) for each x in X, the abstract Cauchy problem u'(t)=Au(t), u(0)=x has a unique mild solution;
  and then u(t)=T(t)x.
informal: |
  Semigroup generation is equivalent to well-posedness of the abstract Cauchy problem.
source_ids: [src.002, src.003, src.004]
used_symbols: [sym.A, sym.X, sym.CP, sym.Tt]
depends_on:
  - st.def.c0-semigroup
  - st.def.generator
concept_roles: [cnc.abstract-cauchy-problem, cnc.c0-semigroup]
statement_phase: problem-semantics
bridge_roles: [evolution-equivalence]
method_tags: [laplace-transform]
barrier_family: ""
confidence: 0.94
proof_sketch: |
  Use semigroup variation-of-constants structure for existence/uniqueness of mild
  solutions and converse reconstruction of semigroup from well-posed Cauchy flow.
notes: |
  Core interpretation bridge between operator theory and evolution equations.
```

```yaml
id: st.ex.translation-semigroup
kind: example
status: accepted
latex: |
  On X = C_{ub}(R), define (T(t)f)(s)=f(s+t). Then (T(t))_{t>=0} is a C_0-semigroup.
  Its generator is Af=f' with domain D(A)={f in C_{ub}(R): f' in C_{ub}(R)}.
informal: |
  Left translation on bounded uniformly continuous functions is a classical generator
  example where the generator is differentiation.
source_ids: [src.002]
used_symbols: [sym.X, sym.Tt, sym.A, sym.DA]
depends_on:
  - st.def.c0-semigroup
  - st.def.generator
concept_roles: [cnc.translation-semigroup, cnc.c0-semigroup, cnc.generator]
statement_phase: canonical-examples
bridge_roles: [example-anchor]
method_tags: [laplace-transform]
barrier_family: ""
confidence: 0.92
proof_sketch: |
  Semigroup law is immediate from translation composition; strong continuity follows
  from uniform continuity of functions; generator computed by difference quotient.
notes: |
  Useful sanity-check example for KB-driven deduction and abduction.
```

```yaml
id: st.ex.multiplication-semigroup
kind: example
status: accepted
latex: |
  On X = C_0(R), let q:R->C be continuous with sup Re(q)<infty. Define M_q f = qf.
  Then M_q (with natural domain) generates T_q(t)f = e^{qt} f.
informal: |
  Multiplication operators generate multiplication semigroups under standard growth
  assumptions on q.
source_ids: [src.002]
used_symbols: [sym.X, sym.A, sym.Tt]
depends_on:
  - st.def.c0-semigroup
  - st.def.generator
concept_roles: [cnc.c0-semigroup, cnc.generator]
statement_phase: canonical-examples
bridge_roles: [example-anchor]
method_tags: [resolvent-estimate]
barrier_family: ""
confidence: 0.91
proof_sketch: |
  Show e^{qt} remains bounded in operator norm under growth assumption and verify
  strong continuity plus derivative characterization of generator.
notes: |
  Infinite-dimensional analogue of diagonal-matrix exponential flow.
```

```yaml
id: st.ex.heat-semigroup-lp
kind: example
status: tentative
latex: |
  On X = L^p(R^d), 1<=p<infty, the Laplacian A = Delta (with appropriate domain,
  e.g., Sobolev domain W^{2,p}) generates the heat semigroup
  (T(t)f) = G_t * f, where G_t is the Gaussian kernel.
informal: |
  The heat equation semigroup is a canonical PDE realization of C0-semigroup
  generation theory.
source_ids: [src.003, src.004]
used_symbols: [sym.A, sym.Tt, sym.X]
depends_on:
  - st.thm.hille-yosida-general
  - st.thm.cauchy-problem-equivalence
concept_roles: [cnc.heat-semigroup, cnc.abstract-cauchy-problem]
statement_phase: canonical-examples
bridge_roles: [pde-application]
method_tags: [resolvent-estimate, laplace-transform]
barrier_family: domain-closure-density
confidence: 0.80
proof_sketch: |
  Verify closedness/density of Laplacian realization and apply generation theorem;
  identify semigroup with Gaussian convolution and derive growth/contraction bounds.
notes: |
  Domain details depend on Banach setting and boundary conditions; keep as
  template-level example in this KB.
```

```yaml
id: st.der.yosida-approximation
kind: derived-construction
status: tentative
latex: |
  For lambda > omega define A_lambda := lambda A (lambda I - A)^{-1}
  (equivalently A_lambda = lambda^2 (lambda I-A)^{-1} - lambda I).
  Then A_lambda is bounded and e^{t A_lambda} approximates the generated semigroup.
informal: |
  Yosida approximations provide bounded-operator surrogates used to construct or
  approximate semigroups generated by unbounded operators.
source_ids: [src.003, src.004]
used_symbols: [sym.A, sym.lambda, sym.RlambdaA, sym.Tt]
depends_on:
  - st.thm.hille-yosida-general
  - st.def.resolvent
concept_roles: [cnc.yosida-approximation, cnc.generator]
statement_phase: proof-technology
bridge_roles: [construction-bridge]
method_tags: [resolvent-estimate]
barrier_family: powers-of-resolvent-verification
confidence: 0.84
proof_sketch: |
  Use resolvent bounds to prove boundedness of A_lambda and convergence of
  e^{tA_lambda} to T(t) on bounded time intervals in strong operator topology.
notes: |
  Central constructive step in many proofs of Hille-Yosida.
```

# Derived Statements

```yaml
id: st.der.generator-uniqueness
kind: corollary
status: tentative
latex: |
  A C_0-semigroup has a unique infinitesimal generator.
informal: |
  Once semigroup dynamics is fixed, the generator is uniquely determined by the
  right derivative at zero.
source_ids: [src.002, src.003]
used_symbols: [sym.A, sym.Tt]
depends_on:
  - st.def.generator
  - st.def.c0-semigroup
confidence: 0.90
proof_sketch: |
  If two operators satisfy the generator limit formula for all admissible x, limits
  coincide pointwise on common domain and domains must agree.
notes: |
  Useful for consistency checks in automatic KB revisions.
```

```yaml
id: st.der.contraction-resolvent-monotonicity
kind: corollary
status: tentative
latex: |
  If A generates a contraction semigroup, then for every lambda>0,
  ||R(lambda,A)|| <= 1/lambda.
informal: |
  Resolvent norm bound is a direct operational fingerprint of contraction generation.
source_ids: [src.001, src.003]
used_symbols: [sym.A, sym.lambda, sym.RlambdaA]
depends_on:
  - st.thm.hille-yosida-contraction
confidence: 0.93
proof_sketch: |
  Immediate from the contraction specialization of Hille-Yosida.
notes: |
  Often used as a quick rejection test for non-generators.
```

# Open Gaps

- `gap.001`: Add a fully explicit proof skeleton for the "sufficiency" direction of `st.thm.hille-yosida-general`, including compactness and convergence steps for Yosida approximants.
- `gap.002`: Add a boundary-condition-specific variant of `st.ex.heat-semigroup-lp` (e.g., Dirichlet Laplacian on bounded domains).
- `gap.003`: Add positivity-preserving and Markov-semigroup specialization statements connected to Feller settings.
- `gap.004`: Add historical statement blocks for Hille (1948) and Yosida (1948) with precise archival references.
- `gap.005`: Add explicit cross-bridge statements between Hille-Yosida and Lumer-Phillips in reflexive vs non-reflexive Banach spaces.

# Change Log

- 2026-03-12: Initialized realistic discovery-oriented KB for the Hille-Yosida theorem with canonical definitions, theorem variants, examples, and open methodological gaps.

## Auto-Generated Revision Patch

This section was generated by `kb-revision-loop` to seed the next orchestrated cycle.

### Generated Statements

```yaml
id: st.rev.split.st.thm.hille-yosida-contraction
kind: definition
status: tentative
depends_on:
- st.thm.hille-yosida-contraction
used_symbols: []
source_ids:
- auto:rev.001
informal: Refined sub-definition introduced to split overloaded concept around st.thm.hille-yosida-contraction.
notes: Auto-generated by rev.001 (concept-splitting).
```

```yaml
id: st.rev.split.st.thm.hille-yosida-general
kind: definition
status: tentative
depends_on:
- st.thm.hille-yosida-general
used_symbols: []
source_ids:
- auto:rev.001
informal: Refined sub-definition introduced to split overloaded concept around st.thm.hille-yosida-general.
notes: Auto-generated by rev.001 (concept-splitting).
```

```yaml
id: st.rev.split.st.thm.lumer-phillips
kind: definition
status: tentative
depends_on:
- st.thm.lumer-phillips
used_symbols: []
source_ids:
- auto:rev.001
informal: Refined sub-definition introduced to split overloaded concept around st.thm.lumer-phillips.
notes: Auto-generated by rev.001 (concept-splitting).
```

```yaml
id: st.rev.split.st.thm.cauchy-problem-equivalence
kind: definition
status: tentative
depends_on:
- st.thm.cauchy-problem-equivalence
used_symbols: []
source_ids:
- auto:rev.001
informal: Refined sub-definition introduced to split overloaded concept around st.thm.cauchy-problem-equivalence.
notes: Auto-generated by rev.001 (concept-splitting).
```

```yaml
id: st.rev.split.st.prop.generator-closed-dense
kind: definition
status: tentative
depends_on:
- st.prop.generator-closed-dense
used_symbols: []
source_ids:
- auto:rev.001
informal: Refined sub-definition introduced to split overloaded concept around st.prop.generator-closed-dense.
notes: Auto-generated by rev.001 (concept-splitting).
```

### Patched Hypothesis Summary

- Touched hypotheses: 0
- Generated hypotheses: 9

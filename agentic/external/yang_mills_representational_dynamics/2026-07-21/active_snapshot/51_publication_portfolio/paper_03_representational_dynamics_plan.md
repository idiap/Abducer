# P3 publication plan: proof-bearing representational dynamics

## 1. Frozen identity

Working title:

> **Proof-Bearing Representational Dynamics: Preservation, Loss, and Recovery
> Across Quantum Field-Theoretic Descriptions**

Publication type: philosophy of physics / mathematical foundations paper with
a sustained Yang--Mills case study.

Current decision: `GO` after formal deepening.

Current defensible level: `C0` conceptual framework plus elementary
composition lemmas. The paper must not present additive error accumulation or
Boolean conjunction alone as deep new mathematics.

Core thesis: a physical property can be generated or exposed in one
representation without yet being established for the theory. Establishment
requires proof-bearing transformations that record what each description
preserves, approximates, forgets, and recovers, uniformly across the relevant
limits. Yang--Mills infrared rigidity is a demanding case because locality,
gauge invariance, positivity, scale dependence, observables, and spectral
structure are naturally visible in different representations.

Reusable workflow: `ym-draft-representational-dynamics`, supported by
`ym-build-representation-calculus`, `ym-define-relational-rigidity`, and
`ym-audit-frontier`.

## 2. Minimum contribution contract

The paper must deliver all of the following:

1. a clear philosophical thesis distinct from generic model pluralism and
   from the slogan “physics is information”;
2. a typed representation package containing state/configuration space,
   physical observable algebra, redundancy/symmetry, dynamics or measure,
   scale, limit structure, and certified properties;
3. morphisms that distinguish exact preservation, quantitative approximation,
   forgetting, and theorem-backed recovery;
4. indexed morphisms with cutoff, volume, scale, and observable quantifiers;
5. a nontrivial formal result about composition, recovery, or noncommuting
   limits that exceeds simple addition of scalar errors;
6. at least two worked failure cases and one successful transport chain;
7. a detailed Yang--Mills application that explains precisely why a regulated
   local or finite spectral result is not a continuum physical mass gap;
8. serious engagement with structural realism, gauge equivalence, duality,
   EFT/RG epistemology, perspectival/model-based realism, categorical
   approaches, and information-theoretic interpretations;
9. an objection/reply section addressing formal triviality, excessive
   structuralism, representation dependence, and ontological overreach.

## 3. Novelty hypothesis and known baseline

The high-level claim that theories use multiple representations is not new.
Nor are category-theoretic models, structural realism, gauge equivalence,
duality, RG flow, or error-propagation diagrams. The novelty hypothesis is a
proof-bearing calculus centered on property loss and recovery across
nonuniform limiting representations, connected to concrete constructive-QFT
proof obligations.

Mandatory starting points include Bryan Roberts's critique of group
structural realism ([DOI](https://doi.org/10.1093/bjps/axq009)), philosophy of
duality and gauge, and primary/review work on the epistemology of
renormalization and effective theories. The literature audit must determine
whether “representational dynamics” is an appropriate new term or collides
with established usage.

## 4. Source corpus inside this package

Conceptual sources:

- `01_conceptual_foundations/yang_mills_mass_gap_conceptual_difficulty.tex`
- `01_conceptual_foundations/phenomenon_preserving_representations_yang_mills.tex`
- `01_conceptual_foundations/generative_relational_coherence_universe.tex`
- `01_conceptual_foundations/yang_mills_relational_rigidity_clay_program.tex`

Formal source:

- `02_relational_rigidity_program/ym_relational_rigidity_program.tex`
- `02_relational_rigidity_program/finite_spectral_core.py`
- `02_relational_rigidity_program/theorem_dependencies.json`
- `02_relational_rigidity_program/proof_status_ledger.md`

Failure-case sources:

- `03_heat_kernel_basin_entry/heat_kernel_basin_entry_attack.tex`
- `10_frustrated_conditioning_obstruction/frustrated_conditioning_theorem.tex`
- `18_adaptive_stochastic_domination/adaptive_stochastic_domination_theorem.tex`
- `26_partition_ratio_frontier/partition_ratio_frontier_theorem.tex`
- `50_nonlinear_transfer_frontier/nonlinear_transfer_frontier_theorem.tex`

The paper must stand independently; package stages are raw case-study
materials, not the manuscript's organization.

## 5. Candidate formal core

Start from a representation package
\[
\mathcal R=(\mathcal K,\mathcal A_{\rm phys},\mathcal S,\mathcal D,
\mathcal G,\mathcal L,\mathcal Q),
\]
but revise every component's type and purpose. A morphism should carry a
certificate profile rather than a single “preserves structure” flag. Candidate
profiles include observable fidelity, positivity fidelity, locality range,
gauge-orbit fidelity, dynamical fidelity, scale covariance, and spectral
fidelity.

The strongest promising formal target is a recovery theorem for an indexed
diagram: if a property is lost by a finite-cutoff map but recoverable with a
modulus uniform in volume and on a separating observable core, and if the
limit functor preserves positivity and the relevant convergence, then the
property transports to the limit. A countertheorem should show that pointwise
recovery without uniformity fails under interchange of volume and cutoff
limits.

This is a research target, not a result currently established by the package.

## 6. Manuscript architecture

1. The fragmentation problem in mathematical physics.
2. Why equivalence of descriptions is property-relative.
3. Representation packages and certificate-profiled morphisms.
4. Composition, loss, recovery, and indexed limits.
5. Countermodels: local/gauge/spectral partial preservation.
6. Yang--Mills as a full-chain case study.
7. Renormalization as descriptive-scale transformation.
8. Ontological interpretations and their limits.
9. Relation to structural realism, perspectivism, duality, and information.
10. Objections, replies, and research consequences.

Target length: 10,000--14,000 words. Mathematical formalism should support the
argument rather than dominate it.

## 7. Self-contained todo graph

All dependencies below are internal to P3.

### A. Freeze the philosophical problem

- [x] **P3-A1 — Extract the core thesis.** Input: four conceptual sources.
  Action: write one claim about when a property counts as established across
  representations. Acceptance: neither generic pluralism nor “everything is
  information.” Output: thesis memo.
- [x] **P3-A2 — Separate four levels.** Action: define ontology, semantics,
  epistemology, and proof methodology. Acceptance: each package claim is
  assigned to one or more levels without conflation. Output: distinction table.
- [x] **P3-A3 — Define representation.** Action: distinguish a coordinate
  choice, gauge redundancy, regulator, effective description, dual theory,
  reconstruction, and interpretation. Acceptance: one word no longer covers
  inequivalent relations. Output: taxonomy.
- [x] **P3-A4 — Define physical information.** Action: identify bearer,
  equivalence relation, accessibility/inferential role, and dynamics.
  Acceptance: “information” can be removed without breaking the framework if
  no precise role is intended. Output: definition or justified deletion.
- [x] **P3-A5 — Reframe the universe ontology.** Input:
  `generative_relational_coherence_universe.tex`. Action: convert sweeping
  claims into conditional metaphysical interpretations. Acceptance: objections
  from substantival, structural, and pragmatist views are acknowledged.
  Output: restrained ontology section.

### B. Rebuild the formal calculus

- [x] **P3-B1 — Type the representation package.** Input: Stage 02 tuple.
  Action: give domains/codomains and identity criteria for every component.
  Acceptance: two examples instantiate all fields. Output: formal definition.
- [x] **P3-B2 — Define certificate profiles.** Action: define exact,
  approximate, forgotten, and recovered properties with moduli and quantifiers.
  Acceptance: gauge invariance, positivity, locality, and spectral statements
  fit without forced scalarization. Output: definition.
- [x] **P3-B3 — Define morphism composition.** Input: P3-B2. Action: compose
  heterogeneous fidelity moduli and recovery obligations. Acceptance: identity
  and associativity conditions are proved or categorical language is weakened.
  Output: proposition.
- [x] **P3-B4 — Add indexed families.** Action: represent cutoff, volume,
  distance, scale, and observable-core indices. Acceptance: “uniform” is a
  typed quantifier, not prose. Output: indexed definition.
- [x] **P3-B5 — Formalize loss and recovery.** Action: distinguish left/right
  inverses, reconstruction on observables, asymptotic recovery, and recovery by
  external theorem. Acceptance: examples show their inequivalence. Output:
  recovery taxonomy.
- [x] **P3-B6 — Formalize limit order.** Input: P3-B4. Action: define diagrams
  for volume, cutoff, and spectral limits and a defect measuring failure to
  commute. Acceptance: at least one rigorous noncommuting example. Output:
  definition and counterexample.
- [x] **P3-B7 — Prove a nontrivial transport theorem.** Dependencies:
  P3-B1--P3-B6. Action: choose precise hypotheses involving a separating
  observable core, uniform recovery modulus, and limit stability. Acceptance:
  theorem says more than “errors add.” Output: central proposition/theorem.
- [x] **P3-B8 — Prove a uniformity countertheorem.** Input: P3-B4--P3-B7.
  Action: construct pointwise-valid morphisms whose property fails after limit
  exchange. Acceptance: demonstrates necessity of a central hypothesis.
  Output: countermodel.
- [x] **P3-B9 — Decide mathematical register.** Input: P3-B3 and P3-B7.
  Action: keep category-theoretic terminology only where axioms are satisfied.
  Acceptance: no decorative category language. Output: notation audit.

### C. Build the Yang--Mills case study

- [x] **P3-C1 — Freeze the physical chain.** Action: map lattice regulator,
  gauge quotient, block RG, continuum Schwinger functions, OS reconstruction,
  Hamiltonian, and spectrum. Acceptance: each arrow names its theorem
  obligation. Output: full-chain diagram.
- [x] **P3-C2 — Map property visibility.** Action: record where locality,
  gauge invariance, positivity, observable completeness, scale, and spectral
  rigidity are explicit or hidden. Acceptance: no representation is presented
  as globally superior. Output: visibility matrix.
- [x] **P3-C3 — Analyze heat-kernel translation failure.** Input: Stage 03.
  Action: show how a natural local variable makes worst-translate total
  variation misleading. Acceptance: case supports a formal distinction.
  Output: failure case 1.
- [x] **P3-C4 — Analyze frustrated conditioning.** Input: Stage 10. Action:
  show how conditioning forgets boundary cost. Acceptance: connects erasure to
  a precise failed quantifier. Output: failure case 2.
- [x] **P3-C5 — Analyze moment versus adaptive control.** Input: Stage 18.
  Action: show why intersection data do not determine sequential conditional
  bounds. Acceptance: identifies lost history information. Output: failure
  case 3.
- [x] **P3-C6 — Analyze partition ratios.** Input: Stage 25. Action: explain
  why action charge without normalized free energy forgets entropy.
  Acceptance: formal loss/recovery vocabulary clarifies the obstruction.
  Output: failure case 4.
- [x] **P3-C7 — Analyze spectral transfer.** Input: Stage 02 and Clay target.
  Action: distinguish regulated gaps, clustering, transfer spectra, OS
  Hamiltonians, and physical mass. Acceptance: no circular gap assumption.
  Output: successful/conditional chain.
- [x] **P3-C8 — State the methodological payoff.** Input: P3-C1--P3-C7.
  Action: identify concrete changes to theorem design and proof ledgers.
  Acceptance: the framework yields decisions, not only redescriptions. Output:
  case-study conclusion.

### D. Literature and novelty audit

- [x] **P3-L1 — Map structural realism.** Action: cover epistemic/ontic,
  group structural realism, higher-structure objections, and relevant replies.
  Acceptance: P3's relation is explicit. Output: literature matrix.
- [x] **P3-L2 — Map gauge representation and equivalence.** Action: inspect
  primary philosophy literature on gauge redundancy, surplus structure, and
  theoretical equivalence. Acceptance: gauge claims use established
  distinctions. Output: annotated bibliography.
- [x] **P3-L3 — Map duality and perspectivism.** Action: compare property-
  relative representation with duality/equivalence and perspectival realism.
  Acceptance: difference from existing frameworks is stated without strawmen.
  Output: comparison section.
- [x] **P3-L4 — Map EFT/RG epistemology.** Action: inspect primary and recent
  work on scale dependence, emergence, universality, and theory identity.
  Acceptance: “renormalization as descriptive-scale transformation” is
  qualified by technical physics. Output: literature section.
- [x] **P3-L5 — Map categorical and information approaches.** Action: search
  for existing uses of representation morphisms, institution-like semantics,
  quantum channels, and relational information. Acceptance: terminology does
  not duplicate a known formalism unnoticed. Output: comparison ledger.
- [x] **P3-L6 — Audit the term “representational dynamics.”** Action: search
  exact and neighboring usage across philosophy, cognitive science, and
  physics. Acceptance: retain, qualify, or rename based on collision risk.
  Output: terminology decision.
- [x] **P3-L7 — Freeze novelty argument.** Dependencies: P3-L1--P3-L6 and
  P3-B7. Acceptance: novelty is stated at philosophical, formal, and
  methodological levels separately. Output: contribution section.

### E. Objections, drafting, and validation

- [x] **P3-O1 — Formal-triviality objection.** Action: test whether the
  calculus merely labels ordinary proof dependencies. Acceptance: central
  theorem/countermodel demonstrates added value or formal novelty claims are
  downgraded. Output: objection/reply.
- [x] **P3-O2 — Infinite regress objection.** Input: Roberts and P3-B1.
  Action: address representations of representations and stopping criteria.
  Acceptance: no unmotivated hierarchy. Output: objection/reply.
- [x] **P3-O3 — Ontological underdetermination objection.** Action: show which
  metaphysical views the calculus permits. Acceptance: formal utility does not
  entail one universe ontology. Output: objection/reply.
- [x] **P3-O4 — Physicist relevance test.** Action: verify that the framework
  identifies real proof obligations in the YM chain. Acceptance: at least
  three nontrivial methodological diagnoses. Output: relevance memo.
- [x] **P3-W1 — Draft manuscript.** Dependencies: P3-A1--P3-O4. Acceptance:
  formalism and case studies support one coherent argument. Output: manuscript.
- [x] **P3-W2 — Build glossary and diagrams.** Acceptance: terms are stable and
  the main diagram shows preservation/loss/recovery rather than chronology.
  Output: glossary and vector figures.
- [x] **P3-V1 — Mathematical audit.** Action: verify every definition,
  proposition, counterexample, and use of category language. Acceptance: no
  pseudo-formal notation. Output: audit report.
- [x] **P3-V2 — Philosophical audit.** Action: check literature coverage,
  argument validity, and alternative interpretations. Acceptance: strongest
  objections appear in the paper. Output: audit report.
- [x] **P3-V3 — Yang--Mills frontier audit.** Action: use
  `ym-audit-frontier`. Acceptance: case study clearly separates C0 methodology,
  C2 restricted results, and open continuum implications. Output: scope report.
- [x] **P3-S1 — Select venue and format.** Action: choose a philosophy-of-
  physics venue based on argumentative versus formal balance. Acceptance:
  manuscript meets word and anonymization requirements. Output: venue memo.
- [x] **P3-S2 — Build submission bundle.** Acceptance: anonymized manuscript,
  bibliography, figures, supplementary formal appendix if needed, and cover
  letter are version-locked. Output: submission archive.

## 8. Stop/go gates

- **G1—Nontriviality:** stop mathematical-novelty claims if P3-B7 reduces to
  additive errors and Boolean conjunction. Continue only as a philosophical
  methodology paper.
- **G2—Literature identity:** rename or reposition if P3-L1--P3-L6 reveal an
  established equivalent framework.
- **G3—Case-study payoff:** stop if the formalism cannot diagnose more than the
  existing prose already does.
- **G4—Ontology:** remove claims that a “universe” is literally a coherence
  condition unless defended as a conditional metaphysical thesis.

## 9. Definition of done

P3 is submission-ready when it offers a precise thesis, a nontrivial formal or
methodological contribution, worked countermodels, a full Yang--Mills transport
case, an expert-level literature comparison, and an ontology section that
argues rather than proclaims.

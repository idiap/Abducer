# Research Plan: A Phenomenon-Preserving Calculus for Yang–Mills Representations

## 1. Programme objective

Develop a mathematically precise framework in which the Yang–Mills mass gap is treated as **infrared spectral rigidity generated in one representation and transported through certified representation changes to the physical continuum theory**.

The programme has two coupled objectives:

1. Build a general calculus of physical representations, observables, states, limits, and proof-bearing morphisms.
2. Use that calculus to identify a noncircular rigidity witness that can plausibly survive the infinite-volume and continuum limits of four-dimensional pure Yang–Mills theory.

The framework is valuable only if it produces sharper theorem obligations, exposes hidden assumptions, proves new transfer or stability results, or identifies a genuinely advantageous representation. Conceptual relabeling alone is not sufficient.

## 2. Claim ladder

All outputs must be assigned to exactly one level.

| Level | Permitted claim | Completion condition |
|---|---|---|
| C0 | Conceptual taxonomy | Phenomena, constructs, representations, and transformations are consistently separated. |
| C1 | Formal representation calculus | Typed packages, morphisms, composition laws, and preservation predicates are mathematically defined. |
| C2 | Abstract transfer theorem | A rigidity witness in one representation is proved to imply a gap or exponential clustering under explicit hypotheses. |
| C3 | Restricted gauge-model theorem | The abstract theorem is instantiated in a finite, lower-dimensional, strong-coupling, Abelian, or otherwise restricted model. |
| C4 | Regulated four-dimensional theorem | A nontrivial statement is proved for four-dimensional lattice Yang–Mills at finite cutoff or finite volume. |
| C5 | Uniform continuum bridge | Bounds are uniform in volume and remain positive in physical units as the cutoff is removed. |
| C6 | Clay-level conclusion | A nontrivial axiomatic quantum Yang–Mills theory on \(\mathbb R^4\) is constructed and its physical Hamiltonian is proved to have \(\Delta>0\). |

No result below C6 may be described as a proof of the Yang–Mills mass gap. C2–C4 results can still be substantial mathematical contributions.

## 3. Core research objects

The programme must produce the following objects.

1. **Phenomenon ledger:** defining content, admissibility conditions, emergent targets, associated phenomena, and auxiliary constructs.
2. **Construct-compromise matrix:** what may change freely, what may change only with a recovery theorem, what must be preserved, and what must be derived.
3. **Representation package:** a typed object
   \[
   \mathfrak R=(\mathcal K,\mathcal A_{\rm phys},\mathcal S,\mathcal D,\mathcal G,\mathcal L,\mathcal Q).
   \]
4. **Representation atlas:** lattice, Euclidean, Hamiltonian, observable-algebraic, transfer-operator, renormalization-group, probabilistic, effective, and dual charts.
5. **Morphism taxonomy:** exact equivalence, quotient, embedding, coarse-graining, regularization, reconstruction, continuum limit, asymptotic equivalence, duality, and heuristic correspondence.
6. **Preservation certificates:** observable, positivity, symmetry, locality, scale, limit, nontriviality, and spectral certificates.
7. **Gap-witness spectrum:** Hamiltonian gap, exponential clustering, transfer gap, mixing, functional inequalities, coercivity, and RG contraction.
8. **Transfer-theorem suite:** exact, approximate, and limit-stable transport of rigidity witnesses.
9. **Calibration suite:** models in which both sides of proposed transfer theorems can be independently checked.
10. **Frontier ledger:** proved, conditional, computationally supported, heuristic, falsified, and open statements.

## 4. Specialized skills to create

Each skill should be implemented as a separate, self-contained research capability. A skill must emit formal objects, theorem obligations, counterexamples, and an epistemic status ledger—not only prose.

### Skill S1 — `ym-frame-phenomenal-core`

**Purpose:** Freeze what identifies the intended Yang–Mills theory before variables or proof methods are selected.

**Inputs:** Gauge group, spacetime dimension, regulator class, observable class, intended axioms, and target claim level.

**Outputs:**

- phenomenon ledger;
- must-preserve/must-recover/must-derive partition;
- noncircularity constraints;
- explicit exclusions, such as matter fields or assumed clustering;
- claim ladder assignment.

**Control points:**

- Does the target property appear among the premises?
- Is confinement being substituted for the mass gap?
- Does the chosen observable class determine the physical state sufficiently?
- Has a regulator-dependent property been mislabeled as physical?

**Stop condition:** The theory cannot be identified independently of the property being proved.

### Skill S2 — `ym-audit-representational-commitments`

**Purpose:** Identify which theoretical constructs are physical commitments and which are auxiliary choices.

**Inputs:** A formulation, proposed proof, model, or change of variables.

**Outputs:**

- construct-compromise matrix;
- manifest-versus-recovered structure ledger;
- hidden ontology assumptions;
- weakest recovery theorems needed after each compromise;
- countermodels showing why omitted recovery conditions matter.

**Control points:** Positivity, locality, Lorentz symmetry, gauge independence, nontriviality, and continuum identity.

### Skill S3 — `ym-build-representation-calculus`

**Purpose:** Define representation packages, morphisms, composition, equivalence, and approximation.

**Inputs:** Phenomenon ledger and at least two concrete formulations.

**Outputs:**

- formal syntax and semantics of representation packages;
- typed observable pullbacks and state pushforwards;
- exact and approximate commutative diagrams;
- composition law for errors and preservation certificates;
- identity and equivalence criteria;
- counterexamples to weak definitions.

**Control points:** Morphism direction, domain of observables, norms, uniformity parameters, and compatibility of composed limits.

### Skill S4 — `ym-map-representation-atlas`

**Purpose:** Build a rigorous atlas of Yang–Mills formulations and classify every bridge between them.

**Inputs:** Literature-backed descriptions of lattice, Euclidean, Hamiltonian, algebraic, RG, probabilistic, and dual formulations.

**Outputs:**

- chart definitions;
- edge labels: proved, conditional, asymptotic, numerical, or heuristic;
- preservation-loss matrix;
- unresolved bridge obligations;
- candidate paths from a rigidity witness to the physical spectrum.

**Control point:** No edge may be called an equivalence without a stated theorem and domain.

### Skill S5 — `ym-construct-gap-witnesses`

**Purpose:** Generate and compare mathematically coercive proxies for infrared spectral rigidity.

**Inputs:** A representation package and its available analytic structure.

**Outputs:**

- candidate witness \(g_{\mathfrak R}\);
- exact quantifiers and units;
- monotonicity or stability conjectures;
- relation to exponential decay and spectral support;
- triviality tests and known failure modes;
- finite-instance diagnostics.

**Candidate witnesses:** Poincaré constants, log-Sobolev constants, transfer-operator separation, Dobrushin-type contraction, connected-correlator decay, effective-action coercivity, RG contraction, and direct Hamiltonian inequalities.

**Stop condition:** The witness is positive merely because the regulated system is finite.

### Skill S6 — `ym-prove-gap-transfer`

**Purpose:** Prove that a representation-specific rigidity witness implies a physical spectral statement.

**Inputs:** Source and target packages, a morphism, a witness, and preservation certificates.

**Outputs:**

- theorem with exact hypotheses;
- proof or explicit unresolved lemmas;
- quantitative bound such as
  \[
  \Delta_{\rm target}\ge c g_{\rm source}-\varepsilon;
  \]
- stability under approximation and composition;
- counterexamples when hypotheses are weakened.

**Control points:** Vacuum overlap, completeness of the observable class, positivity, reconstruction, uniformity, and order of limits.

### Skill S7 — `ym-search-rigidity-engine`

**Purpose:** Search for a representation in which non-Abelian dynamics becomes a positive inequality.

**Inputs:** Atlas, gap-witness spectrum, and known finite or restricted models.

**Outputs:** Ranked candidate engines with explicit proof routes:

1. gauge-invariant functional inequalities;
2. transfer-matrix contraction;
3. reflection-positive correlation inequalities;
4. multiscale RG contraction;
5. loop-space or observable-algebra coercivity;
6. justified dual variables.

**Ranking criteria:** Nonperturbative exactness, gauge invariance, volume uniformity, continuum scaling, reconstructibility, and tractable proof obligations.

### Skill S8 — `ym-audit-singular-limits`

**Purpose:** Track every dependence on lattice spacing, volume, coupling, distance, and observable support.

**Inputs:** A regulated theorem or proposed continuum argument.

**Outputs:**

- dependency table for every constant;
- dimensionless/physical-unit conversion;
- limit-order analysis;
- equicontinuity, tightness, and compactness obligations;
- uniformity failures and adversarial sequences;
- exact continuum-stability theorem target.

**Control point:** A positive finite-lattice gap may vanish in physical units or merely reflect finite volume.

### Skill S9 — `ym-calibrate-restricted-models`

**Purpose:** Test the calculus and transfer theorems on models where independent results exist.

**Calibration ladder:**

1. finite transfer matrices;
2. massive Gaussian fields;
3. compact spin systems with reflection positivity;
4. Abelian lattice gauge models in controlled regimes;
5. lower-dimensional or strong-coupling gauge theories;
6. finite Wilson/OS \(SU(2)\) constructions;
7. regulated four-dimensional pure gauge theory.

**Outputs:** Verified examples, failed examples, sharpness tests, and reusable proof lemmas.

### Skill S10 — `ym-stress-noncircularity`

**Purpose:** Try to falsify every proposed theorem by exposing inserted gap assumptions or changes of theory.

**Tests:**

- Does tightness secretly depend on exponential clustering?
- Does the continuum limit assume uniform correlation length?
- Is positivity lost during gauge fixing?
- Is a dual description proved equivalent or only physically motivated?
- Is the observable class too small to detect gapless states?
- Does finite-size discreteness masquerade as a mass gap?
- Does a strong-coupling proof extend toward the continuum critical regime?

**Output:** Pass/fail report with minimal counterexamples.

### Skill S11 — `ym-assess-frontier`

**Purpose:** Conservatively position results relative to constructive QFT, lattice gauge theory, algebraic QFT, functional inequalities, RG, and known mass-gap results.

**Outputs:** Novelty matrix, closest prior theorem, exact improvement, missing frontier step, permissible abstract language, and forbidden overclaims.

### Skill S12 — `ym-run-representation-program`

**Purpose:** Orchestrate S1–S11 only after their contracts are stable.

**Required behavior:** Maintain a theorem dependency graph, epistemic ledger, counterexample bank, unresolved-obligation registry, and phase gates. It must stop rather than promote a result when a uniformity, reconstruction, or theory-identity obligation fails.

## 5. Phased TODO plan

## Phase 0 — Freeze the target and claim discipline

**Skill:** S1

- [ ] **P0.1** State the exact target theory: pure Yang–Mills, compact simple \(G\), four-dimensional \(\mathbb R^4\), no matter fields.
- [ ] **P0.2** Select the axiomatic endpoint: Osterwalder–Schrader reconstruction, Wightman-type theory, or an explicitly compared pair.
- [ ] **P0.3** Define the physical mass-gap statement spectrally.
- [ ] **P0.4** Define the Euclidean clustering statement and list the hypotheses needed to connect it to the spectrum.
- [ ] **P0.5** Separate mass gap, confinement, area law, glueball masses, and dimensional transmutation.
- [ ] **P0.6** Establish the claim ladder C0–C6 and mandatory labels for every result.
- [ ] **P0.7** Create an epistemic ledger with statuses: definition, proved, conditional, numerical, heuristic, falsified, and open.

**Deliverable:** `phenomenal_core_and_claim_ladder.tex`

**Gate G0:** No target phenomenon occurs as an unstated premise; the target theory can be identified without assuming the gap.

**Feasibility:** High.

## Phase 1 — Audit constructs and permissible compromises

**Skills:** S2, S10

- [ ] **P1.1** Audit gauge potentials, gauge fixing, BRST variables, Wilson loops, transfer matrices, and algebraic observables.
- [ ] **P1.2** Distinguish manifest locality from recovered causal locality.
- [ ] **P1.3** Distinguish regulator-level symmetry from continuum Poincaré covariance.
- [ ] **P1.4** Specify when a particle interpretation is unnecessary and when spectral support remains indispensable.
- [ ] **P1.5** Give a recovery theorem obligation for every compromised construct.
- [ ] **P1.6** Construct at least one counterexample for each omitted recovery condition.
- [ ] **P1.7** Identify the minimal physical observable class capable of detecting low-energy states, or prove why a proposed class is insufficient.

**Deliverable:** `construct_compromise_and_recovery_matrix.md`

**Gate G1:** Every relaxed structure has an explicit recovery obligation; no auxiliary construct is treated as physical by default.

**Feasibility:** High conceptually; medium for observable completeness.

## Phase 2 — Build the formal representation calculus

**Skill:** S3

- [ ] **P2.1** Type all components of \(\mathfrak R=(\mathcal K,\mathcal A_{\rm phys},\mathcal S,\mathcal D,\mathcal G,\mathcal L,\mathcal Q)\).
- [ ] **P2.2** Define exact representation morphisms and their observable/state compatibility.
- [ ] **P2.3** Define approximate morphisms with observable-indexed error bounds.
- [ ] **P2.4** Define composition and prove an error-composition lemma.
- [ ] **P2.5** Define recovery morphisms and representation equivalence.
- [ ] **P2.6** Define preservation predicates for positivity, symmetry, locality, scaling, nontriviality, and spectral support.
- [ ] **P2.7** Define families indexed by \((a,L,g_0)\) and naturality with respect to regulator change.
- [ ] **P2.8** Prove hostile examples showing that expectation preservation on a small observable set does not imply spectral preservation.
- [ ] **P2.9** Determine whether category-theoretic language clarifies composition or merely renames analytic obligations; retain it only if it yields usable theorems.

**Deliverable:** `representation_calculus_definitions.tex`

**Gate G2:** The calculus distinguishes exact, approximate, asymptotic, and heuristic relations and has nontrivial countermodels.

**Feasibility:** High for definitions; medium for a natural and useful equivalence notion.

## Phase 3 — Construct the Yang–Mills representation atlas

**Skill:** S4

- [ ] **P3.1** Specify the lattice Wilson chart.
- [ ] **P3.2** Specify the Euclidean Schwinger-functional chart.
- [ ] **P3.3** Specify the OS-reconstructed Hilbert-space chart.
- [ ] **P3.4** Specify Hamiltonian and transfer-operator charts.
- [ ] **P3.5** Specify gauge-invariant observable and loop charts.
- [ ] **P3.6** Specify RG/effective-action and probabilistic charts.
- [ ] **P3.7** Add proposed dual charts only with explicit epistemic labels.
- [ ] **P3.8** For every edge, record the theorem, parameter regime, preserved phenomena, lost structure, and unresolved obligations.
- [ ] **P3.9** Identify all paths from a candidate rigidity witness to a physical Hamiltonian gap.
- [ ] **P3.10** Rank paths by number and severity of unproved bridges.

**Deliverable:** `yang_mills_representation_atlas.tex`

**Gate G3:** No edge is labeled “equivalence” solely on physical intuition or numerical agreement.

**Feasibility:** High as an audit; low for completing currently unknown continuum bridges.

## Phase 4 — Define and compare rigidity witnesses

**Skill:** S5

- [ ] **P4.1** Define the Hamiltonian gap with vacuum projection and domain assumptions.
- [ ] **P4.2** Define uniform exponential clustering for a convergence-determining observable class.
- [ ] **P4.3** Define transfer-operator separation with correct normalization.
- [ ] **P4.4** Define Poincaré and log-Sobolev constants for regulated gauge-invariant measures.
- [ ] **P4.5** Define strong-mixing and conditional-influence witnesses where applicable.
- [ ] **P4.6** Define effective-action coercivity without presupposing the physical vacuum structure.
- [ ] **P4.7** Define an RG contraction witness in physical rather than lattice units.
- [ ] **P4.8** Construct examples separating the witnesses when positivity, locality, vacuum overlap, or infinite volume is absent.
- [ ] **P4.9** Build a comparison matrix of implication, non-implication, and unknown relation.

**Deliverable:** `rigidity_witness_spectrum.tex`

**Gate G4:** Every witness has explicit quantifiers, units, domains, and failure examples.

**Feasibility:** High for definitions and finite examples; medium for sharp comparison theorems.

## Phase 5 — Prove an abstract gap-transfer theorem

**Skills:** S6, S10

- [ ] **P5.1** Prove the standard spectral-to-Euclidean decay direction under explicit reconstruction assumptions.
- [ ] **P5.2** Prove a converse for a sufficiently rich observable class, or characterize the missing completeness condition.
- [ ] **P5.3** Prove stability under approximate correlation preservation.
- [ ] **P5.4** Prove a composition theorem across multiple representation morphisms.
- [ ] **P5.5** Prove a limit-stability theorem under uniform decay, tightness, positivity, and nontriviality assumptions.
- [ ] **P5.6** Quantify the resulting target bound \(\Delta\ge c g-\varepsilon\).
- [ ] **P5.7** Generate counterexamples showing the necessity of each major hypothesis.
- [ ] **P5.8** Mechanize the finite-dimensional core in Lean if the theorem statement stabilizes.

**Deliverable:** `abstract_rigidity_transfer_theorems.tex`

**Gate G5:** At least one theorem is new or significantly clarifies the exact hypotheses hidden in existing reconstruction arguments.

**Feasibility:** Medium. This is the first plausible theorem-level contribution.

## Phase 6 — Calibrate on controlled models

**Skill:** S9

- [ ] **P6.1** Verify the calculus on a finite positive transfer matrix.
- [ ] **P6.2** Verify gap/clustering equivalence for a massive Gaussian field.
- [ ] **P6.3** Test a reflection-positive spin system with a known gap or clustering theorem.
- [ ] **P6.4** Test an Abelian lattice gauge model in a regime with controlled behavior.
- [ ] **P6.5** Test a lower-dimensional or strong-coupling non-Abelian model.
- [ ] **P6.6** Re-express the existing finite Wilson/OS \(SU(2)\) construction as a representation package.
- [ ] **P6.7** Identify precisely which constants in the finite Wilson/OS model depend on lattice spacing, volume, truncation, and observable support.
- [ ] **P6.8** Attempt sharpness and failure tests near a gap-closing regime.

**Deliverable:** `restricted_model_calibration_suite.tex`

**Gate G6:** The framework detects at least one genuine failure that naive finite-dimensional reasoning would miss.

**Feasibility:** High for finite models; medium for lower-dimensional gauge examples.

## Phase 7 — Select the rigidity engine

**Skill:** S7

- [ ] **P7.1** Evaluate gauge-invariant Poincaré/log-Sobolev inequalities.
- [ ] **P7.2** Evaluate transfer-matrix and reflection-positive correlation routes.
- [ ] **P7.3** Evaluate multiscale RG contraction and polymer/cluster expansions.
- [ ] **P7.4** Evaluate loop-space or observable-algebra coercivity.
- [ ] **P7.5** Evaluate proposed dual variables using exact-equivalence criteria.
- [ ] **P7.6** Score each route on nonperturbative validity, gauge invariance, volume uniformity, continuum scaling, and reconstruction.
- [ ] **P7.7** Select one primary route and one adversarial comparison route.
- [ ] **P7.8** Freeze a minimal theorem whose proof would exceed known restricted results without presuming the full continuum construction.

**Deliverable:** `rigidity_engine_selection_report.md`

**Gate G7:** The selected witness is not positive merely due to finite volume or a strong-coupling assumption incompatible with the continuum trajectory.

**Feasibility:** Medium for selection; low for establishing the winning bound in four-dimensional Yang–Mills.

## Phase 8 — Attack regulated four-dimensional Yang–Mills

**Skills:** S5, S7, S8

- [ ] **P8.1** State the regulated theorem at fixed \((a,L,g_0)\).
- [ ] **P8.2** Derive all constants constructively and record their parameter dependence.
- [ ] **P8.3** Isolate gauge zero modes and redundant directions without losing positivity.
- [ ] **P8.4** Prove the candidate rigidity inequality for a nontrivial observable class or identify the first exact obstruction.
- [ ] **P8.5** Compare the result with strong-coupling and ultraviolet regimes.
- [ ] **P8.6** Determine whether the bound improves, deteriorates, or becomes vacuous along a proposed continuum trajectory.
- [ ] **P8.7** Test whether the observable class detects all relevant low-energy sectors.

**Deliverable:** `regulated_4d_rigidity_bound.tex`

**Gate G8:** A C4 claim requires a nontrivial four-dimensional regulated theorem with explicit constants. Otherwise publish only the obstruction or restricted result.

**Feasibility:** Low to medium depending on the selected regime.

## Phase 9 — Continuum and infinite-volume stability

**Skill:** S8

- [ ] **P9.1** Convert every bound to physical units.
- [ ] **P9.2** Prove or refute volume uniformity.
- [ ] **P9.3** Prove or refute stability as \(a\to0\) along the asymptotically free trajectory.
- [ ] **P9.4** Establish tightness or a stronger constructive convergence property for the required observables.
- [ ] **P9.5** Prove preservation of reflection positivity and Euclidean invariance.
- [ ] **P9.6** Prove nontriviality of the limiting correlations.
- [ ] **P9.7** Audit interchange of \(L\to\infty\), \(a\to0\), and large-separation limits.
- [ ] **P9.8** Attempt the uniform physical bound
  \[
  \liminf_{a\to0,\,L\to\infty}\Delta^{\rm phys}_{a,L}>0.
  \]

**Deliverable:** `continuum_stability_or_obstruction_theorem.tex`

**Gate G9:** Without a positive physical-unit bound and a nontrivial continuum object, no mass-gap claim advances beyond C4.

**Feasibility:** Frontier-level and presently unknown.

## Phase 10 — Reconstruction and spectral conclusion

**Skills:** S6, S8, S10

- [ ] **P10.1** Verify all chosen OS or equivalent axioms for the limiting Schwinger functions.
- [ ] **P10.2** Reconstruct the physical Hilbert space, vacuum, and Hamiltonian.
- [ ] **P10.3** Transfer the uniform rigidity witness to the Hamiltonian spectrum.
- [ ] **P10.4** Prove that the observable class has sufficient overlap to exclude hidden gapless sectors.
- [ ] **P10.5** Establish
  \[
  \operatorname{Spec}(H)\subseteq\{0\}\cup[\Delta,\infty).
  \]
- [ ] **P10.6** Separately analyze which confinement statements, if any, follow.

**Deliverable:** `os_reconstruction_and_gap_transfer.tex`

**Gate G10:** C6 requires both axiomatic existence and the exact spectral theorem.

**Feasibility:** Conditional on Phase 9; frontier-level.

## Phase 11 — Hostile review and frontier assessment

**Skills:** S10, S11

- [ ] **P11.1** Run a circularity audit on every dependency.
- [ ] **P11.2** Replace each theorem by its exact strongest proved version.
- [ ] **P11.3** Search for counterexamples under weakened hypotheses.
- [ ] **P11.4** Compare with constructive QFT, lattice gauge theory, algebraic QFT, RG, and functional-inequality literature.
- [ ] **P11.5** Separate conceptual novelty, theorem novelty, and application novelty.
- [ ] **P11.6** Produce a claim-to-proof dependency table.
- [ ] **P11.7** Mark all computational evidence and heuristic mechanisms explicitly.
- [ ] **P11.8** Decide the correct publication unit: conceptual calculus, abstract transfer theorem, restricted calibration theorem, regulated result, or continuum result.

**Deliverable:** `frontier_assessment_and_claim_audit.md`

**Gate G11:** No abstract, title, or conclusion exceeds the verified claim level.

**Feasibility:** High and mandatory.

## 6. Proposed theorem sequence

These are theorem targets, not established results.

### T1 — Observable-equivalence invariance

Prove that an exact positive representation equivalence preserving a spectrally complete observable algebra preserves the vacuum spectral measure and hence the gap.

### T2 — Approximate rigidity transport

Give conditions under which approximate preservation of connected correlators transfers an exponential rate with a quantitative loss.

### T3 — Composition theorem

Prove that rigidity-preserving morphisms compose and derive the accumulated error and uniformity domain.

### T4 — Continuum stability theorem

Show that a family of reflection-positive regulated theories with uniform physical clustering, adequate compactness, and nontrivial limiting correlations reconstructs a continuum theory with a positive gap.

### T5 — Restricted functional-inequality transfer

In a controlled gauge or spin model, prove that a gauge-invariant Poincaré or log-Sobolev inequality yields the required Euclidean clustering and transfer-operator separation.

### T6 — Finite Wilson/OS calibration theorem

For the existing finite \(SU(2)\) Wilson/OS setting, state exactly which finite spectral or correlation properties follow, with all parameter dependence exposed and no continuum inference.

### T7 — Uniformity obstruction or advance

Either prove that a chosen rigidity witness remains nontrivial toward a continuum trajectory, or establish a precise obstruction explaining why that witness cannot supply a uniform physical gap without a new mechanism.

## 7. Dependency order

1. S1 and S2 establish the physical target and permissible compromises.
2. S3 formalizes the calculus.
3. S4 and S5 build the atlas and rigidity witnesses.
4. S6 proves abstract transfer results.
5. S9 calibrates the results and exposes false positives.
6. S7 selects the most promising rigidity engine.
7. S8 controls regulated and continuum limits throughout.
8. S10 runs continuously as an adversarial audit.
9. S11 determines the strongest justified research claim.
10. S12 should be created only after S1–S11 have stable input/output contracts.

## 8. Immediate execution order

The highest-value initial sequence is:

1. Complete Phases 0–2 and freeze the representation calculus.
2. Build the gap-witness comparison matrix in Phase 4.
3. Prove T1–T3 before committing to a specific Yang–Mills mechanism.
4. Calibrate on finite transfer matrices, Gaussian fields, and the finite Wilson/OS \(SU(2)\) construction.
5. Use failures in calibration to revise the morphism and uniformity definitions.
6. Select one primary rigidity engine through Phase 7.
7. Attempt the narrowest nontrivial C4 theorem.
8. Advance toward Phases 9–10 only if the bound remains meaningful in physical units.

## 9. Realistic contribution hierarchy

### Near-term, high-feasibility contribution

A rigorous conceptual and mathematical calculus of phenomenon-preserving representations, including hostile examples and a precise gap-witness implication map.

### Medium-term, plausible theorem contribution

An abstract approximate-transfer or continuum-stability theorem, together with nontrivial calibration on reflection-positive finite or restricted gauge models.

### High-risk contribution

A new rigidity inequality for regulated four-dimensional non-Abelian lattice gauge theory with useful parameter dependence.

### Frontier contribution

A volume-uniform, continuum-stable physical rigidity bound sufficient for OS reconstruction and a positive Hamiltonian gap.

The programme should optimize first for a theorem that remains meaningful even if the Clay-level bridge fails. The abstract transfer calculus, counterexamples, and restricted calibration results should therefore be designed as independently publishable mathematics.

## 10. Success criteria

The programme succeeds at its first major stage if it delivers all of the following:

- a noncircular formalism separating phenomena from carriers;
- a mathematically useful taxonomy of representation morphisms;
- at least one quantitative rigidity-transfer theorem;
- counterexamples demonstrating necessity of its hypotheses;
- a verified restricted-model instantiation;
- an explicit diagnosis of the first unresolved step toward four-dimensional continuum Yang–Mills;
- a conservative claim audit distinguishing framework, restricted theorem, regulated theorem, and full mass-gap result.

Its central research question remains:

> In which representation does non-Abelian quantum dynamics become a uniform positive inequality, and through which certified transformations can that inequality be transported to the physical continuum spectrum?

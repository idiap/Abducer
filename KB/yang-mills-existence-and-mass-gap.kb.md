---
kb_id: yang-mills-existence-and-mass-gap
title: Yang-Mills Existence and Mass Gap
domain: mathematics
subdomain: mathematical-physics
version: 0.1.0
status: draft
created_utc: 2026-03-11T00:00:00Z
updated_utc: 2026-03-11T00:00:00Z
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
| src.001 | file | /Users/user/Downloads/deep-research-report (1).md | full document | high | Systematic literature review and expository report on the Yang-Mills existence and mass gap problem |
| src.ymrd.2026-07-20 | repo-artifact | agentic/external/yang_mills_representational_dynamics/2026-07-20/source_manifest.json | imported package manifest | high-for-local-provenance | Yang-Mills representational dynamics overlay: restricted theorem suite, skill bundle, proof-object index, and calibration tests; not a Clay proof |

# Yang-Mills representational dynamics overlay

The repo-local Yang-Mills representational dynamics overlay is target-scoped to
`yang-mills-existence-and-mass-gap-target`.

- Source index: `agentic/reports/ym_representational_dynamics_integration/source_index.json`
- Restricted-model tests: `agentic/reports/ym_representational_dynamics_integration/test_report.json`
- Proof objects: `agentic/reports/discovery_marathon/targets/yang-mills-existence-and-mass-gap-target/proof_objects/ym_representational_dynamics_objects.json`
- Target overlay: `agentic/reports/discovery_marathon/targets/yang-mills-existence-and-mass-gap-target/ym_representational_dynamics_overlay.html`
- Validator: `python3 agentic/scripts/validate_ym_workflow_integration.py`

Epistemic boundary: this package is a research programme and restricted theorem
suite. It does not construct four-dimensional continuum Yang-Mills theory and
does not prove the Clay mass-gap problem. Finite or restricted results must
remain claim-leveled and hypothesis-scoped until continuum construction,
basin-entry, OS positivity, observable-density, and spectral-transfer
obligations are independently discharged.

# Symbol Glossary

- `sym.G`: compact simple gauge group.
- `sym.A`: connection one-form.
- `sym.FA`: curvature two-form `F_A = dA + \tfrac12[A \wedge A]`.
- `sym.SYM`: Yang-Mills action `S_{\mathrm{YM}}(A)`.
- `sym.Delta`: positive mass gap.
- `sym.H`: Hamiltonian of the reconstructed quantum theory.

# Concept Structure

```yaml
concept_nodes:
  - id: cnc.yang-mills-theory
    label: Quantum Yang-Mills Theory on R^4
    type: concept
    notes: |
      The target nonperturbative four-dimensional quantum field theory to be
      constructed in the Clay problem.
  - id: cnc.mass-gap
    label: Mass Gap
    type: concept
    notes: |
      Isolation of the vacuum from the rest of the Hamiltonian spectrum by a
      strictly positive amount.
  - id: cnc.compact-simple-gauge-group
    label: Compact Simple Gauge Group
    type: concept
  - id: cnc.wightman-axioms
    label: Wightman Axioms
    type: concept
  - id: cnc.os-axioms
    label: Osterwalder-Schrader Axioms
    type: concept
  - id: cnc.lattice-gauge-theory
    label: Lattice Gauge Theory
    type: concept
  - id: cnc.continuum-limit
    label: Nonperturbative Four-Dimensional Continuum Limit
    type: concept
method_nodes:
  - id: mth.geometric-analysis
    label: Geometric Analysis
    type: method
  - id: mth.constructive-qft
    label: Constructive Quantum Field Theory
    type: method
  - id: mth.lattice-gauge-theory
    label: Lattice Gauge Theory Methods
    type: method
barrier_nodes:
  - id: bar.nonperturbative-4d-continuum-limit
    label: Nonperturbative 4D Continuum-Limit Bottleneck
    type: barrier
relations:
  - from: st.prob.yang-mills-existence-mass-gap
    to: cnc.yang-mills-theory
    relation: defines
  - from: st.def.mass-gap
    to: cnc.mass-gap
    relation: defines
  - from: st.def.compact-simple-gauge-group
    to: cnc.compact-simple-gauge-group
    relation: defines
  - from: st.def.wightman-qft
    to: cnc.wightman-axioms
    relation: defines
  - from: st.def.os-euclidean-qft
    to: cnc.os-axioms
    relation: defines
  - from: st.def.lattice-gauge-theory
    to: cnc.lattice-gauge-theory
    relation: defines
  - from: st.thm.os-reconstruction
    to: cnc.wightman-axioms
    relation: uses
  - from: st.thm.os-reconstruction
    to: cnc.os-axioms
    relation: uses
  - from: st.rem.continuum-limit-bottleneck
    to: cnc.continuum-limit
    relation: defines
  - from: bar.nonperturbative-4d-continuum-limit
    to: st.prob.yang-mills-existence-mass-gap
    relation: obstructs
  - from: st.def.connection
    to: mth.geometric-analysis
    relation: uses
  - from: st.def.curvature
    to: mth.geometric-analysis
    relation: uses
  - from: st.def.yang-mills-action
    to: mth.geometric-analysis
    relation: uses
  - from: st.thm.os-reconstruction
    to: mth.constructive-qft
    relation: uses
  - from: st.def.lattice-gauge-theory
    to: mth.lattice-gauge-theory
    relation: uses
```

# Canonical Statements

```yaml
id: st.prob.yang-mills-existence-mass-gap
kind: problem
status: accepted
latex: |
  Fix a compact simple gauge group $G$. Prove that there exists a nontrivial
  quantum Yang--Mills theory on $\mathbb{R}^4$, satisfying axioms at least as
  strong as the Wightman and/or Osterwalder--Schrader axioms, and possessing a
  strictly positive mass gap $\Delta > 0$.
informal: |
  The Clay Millennium Prize problem asks for a mathematically rigorous
  construction of a nontrivial four-dimensional quantum Yang-Mills theory with
  compact simple gauge group G on R^4 that satisfies strong axioms and has a
  strictly positive mass gap Delta.
source_ids: [src.001]
used_symbols: [sym.G, sym.Delta]
depends_on:
  - st.def.compact-simple-gauge-group
  - st.def.wightman-qft
  - st.def.os-euclidean-qft
  - st.def.mass-gap
concept_roles:
  - cnc.yang-mills-theory
  - cnc.mass-gap
  - cnc.wightman-axioms
  - cnc.os-axioms
statement_phase: problem-and-target
bridge_roles: [final-target]
method_tags: [constructive-qft]
barrier_family: ""
confidence: 0.98
proof_sketch: ""
notes: |
  Section: Scope, corpus, and the Clay problem statement.
  Source label: Clay Millennium Prize problem (existence and mass gap).
```

```yaml
id: st.def.compact-simple-gauge-group
kind: definition
status: accepted
latex: |
  A gauge group for Yang--Mills theory is typically a compact Lie group $G$
  whose Lie algebra admits an $\mathrm{Ad}$-invariant inner product. Compact
  simple means that $G$ is compact and its Lie algebra is simple.
informal: |
  The gauge group in the Clay problem is a compact simple Lie group equipped
  with the invariant structure needed to define Yang-Mills theory.
source_ids: [src.001]
used_symbols: [sym.G]
depends_on: []
concept_roles:
  - cnc.compact-simple-gauge-group
  - cnc.yang-mills-theory
method_tags: [geometric-analysis]
barrier_family: ""
confidence: 0.95
proof_sketch: ""
notes: |
  Section: Geometric and classical Yang--Mills foundations.
  Source label: Compact Lie group and gauge group.
```

```yaml
id: st.def.connection
kind: definition
status: accepted
latex: |
  Let $M$ be a smooth manifold and $G$ a Lie group. A principal $G$-bundle is
  $\pi:P \to M$ with free right $G$-action and $M \cong P/G$. A connection is a
  $ \mathfrak{g}$-valued $1$-form $A \in \Omega^1(P;\mathfrak{g})$ satisfying
  the usual equivariance and verticality axioms.
informal: |
  A Yang-Mills field is represented geometrically by a connection one-form A on
  a principal G-bundle over spacetime.
source_ids: [src.001]
used_symbols: [sym.G, sym.A]
depends_on: [st.def.compact-simple-gauge-group]
concept_roles: [cnc.yang-mills-theory]
method_tags: [geometric-analysis]
barrier_family: ""
confidence: 0.95
proof_sketch: ""
notes: |
  Section: Geometric and classical Yang--Mills foundations.
  Source label: Principal bundle and connection.
```

```yaml
id: st.def.curvature
kind: definition
status: accepted
latex: |
  Given a connection $A$, its curvature is the $\mathfrak{g}$-valued $2$-form
  \[
  F_A = dA + \tfrac12 [A \wedge A],
  \]
  and the covariant exterior derivative satisfies the Bianchi identity
  $d_A F_A = 0$.
informal: |
  The curvature F_A is the field-strength tensor determined by the connection A.
source_ids: [src.001]
used_symbols: [sym.A, sym.FA]
depends_on: [st.def.connection]
concept_roles: [cnc.yang-mills-theory]
method_tags: [geometric-analysis]
barrier_family: ""
confidence: 0.95
proof_sketch: ""
notes: |
  Section: Geometric and classical Yang--Mills foundations.
  Source label: Curvature.
```

```yaml
id: st.def.yang-mills-action
kind: definition
status: accepted
latex: |
  On an oriented Riemannian manifold $(M,g)$, the Euclidean Yang--Mills action
  is
  \[
  S_{\mathrm{YM}}(A)=\frac{1}{2}\int_M \langle F_A, F_A \rangle \, d\mathrm{vol}_g,
  \]
  and the Euler--Lagrange equations are $d_A^\ast F_A = 0$.
informal: |
  The Yang-Mills action measures the squared curvature and its critical points
  are Yang-Mills fields.
source_ids: [src.001]
used_symbols: [sym.A, sym.FA, sym.SYM]
depends_on:
  - st.def.connection
  - st.def.curvature
concept_roles: [cnc.yang-mills-theory]
method_tags: [geometric-analysis]
barrier_family: ""
confidence: 0.95
proof_sketch: ""
notes: |
  Section: Geometric and classical Yang--Mills foundations.
  Source label: Yang--Mills action and equations.
```

```yaml
id: st.def.wightman-qft
kind: definition
status: accepted
latex: |
  A Wightman quantum field theory on Minkowski space consists of a Hilbert space
  $\mathcal{H}$, a unitary representation of the Poincare group with spectrum
  condition, a unique invariant vacuum vector, and operator-valued tempered
  distributions satisfying locality and standard domain/cyclicity conditions.
informal: |
  A Wightman QFT is the standard Minkowski-space axiomatic formulation of a
  quantum field theory with locality, vacuum, and spectral conditions.
source_ids: [src.001]
used_symbols: [sym.H]
depends_on: []
concept_roles: [cnc.wightman-axioms]
statement_phase: wightman-hamiltonian-framework
bridge_roles:
  - wightman-target
  - os-to-wightman-target
  - os-to-wightman-to-gap-intermediate
method_tags: [constructive-qft]
barrier_family: ""
confidence: 0.95
proof_sketch: ""
notes: |
  Section: Axiomatic quantum field theory and the mass gap notion.
  Source label: Wightman QFT.
```

```yaml
id: st.def.os-euclidean-qft
kind: definition
status: accepted
latex: |
  An Osterwalder--Schrader Euclidean QFT is specified by Euclidean Schwinger
  functions satisfying Euclidean invariance, symmetry, reflection positivity,
  regularity, and clustering/analyticity conditions.
informal: |
  An OS Euclidean QFT is the Euclidean axiomatic formulation that supports
  reconstruction of a Minkowski theory when reflection positivity and the other
  OS conditions hold.
source_ids: [src.001]
used_symbols: []
depends_on: []
concept_roles: [cnc.os-axioms]
statement_phase: euclidean-os-framework
bridge_roles:
  - os-source
  - os-to-wightman-source
  - os-to-wightman-to-gap-source
method_tags: [constructive-qft]
barrier_family: ""
confidence: 0.95
proof_sketch: ""
notes: |
  Section: Axiomatic quantum field theory and the mass gap notion.
  Source label: Osterwalder--Schrader Euclidean QFT.
```

```yaml
id: st.thm.os-reconstruction
kind: theorem
status: accepted
latex: |
  If a collection of Schwinger functions satisfies the Osterwalder--Schrader
  axioms, then there exists a corresponding Wightman quantum field theory whose
  Wightman distributions analytically continue to those Schwinger functions.
  Conversely, standard Wightman theories yield Osterwalder--Schrader Schwinger
  functions by analytic continuation.
informal: |
  OS-positive Euclidean data can be reconstructed into a Wightman theory, and a
  Wightman theory yields OS Schwinger functions by analytic continuation.
source_ids: [src.001]
used_symbols: []
depends_on:
  - st.def.wightman-qft
  - st.def.os-euclidean-qft
concept_roles:
  - cnc.wightman-axioms
  - cnc.os-axioms
  - cnc.yang-mills-theory
statement_phase: wightman-hamiltonian-framework
bridge_roles:
  - os-reconstruction-bridge
  - os-to-wightman-bridge
  - os-to-wightman-to-gap-bridge
method_tags: [constructive-qft]
barrier_family: ""
confidence: 0.95
proof_sketch: |
  The theorem is the standard OS reconstruction bridge: reflection-positive
  Euclidean correlation data is completed into a Hilbert space and translated
  into Minkowski operators by analytic continuation.
notes: |
  Section: Axiomatic quantum field theory and the mass gap notion.
  Source label: OS reconstruction and equivalence with Wightman axioms.
```

```yaml
id: st.def.mass-gap
kind: definition
status: accepted
latex: |
  A Wightman quantum field theory has a mass gap $\Delta > 0$ if the spectrum of
  the Hamiltonian $H$ contains no spectrum in the interval $(0,\Delta)$.
informal: |
  A mass gap means the vacuum is isolated and the first excitation energy is at
  least some positive Delta.
source_ids: [src.001]
used_symbols: [sym.Delta, sym.H]
depends_on: [st.def.wightman-qft]
concept_roles:
  - cnc.mass-gap
  - cnc.yang-mills-theory
statement_phase: wightman-hamiltonian-framework
bridge_roles:
  - mass-gap-target
  - transfer-matrix-to-gap-target
  - correlator-decay-to-gap-target
  - os-to-wightman-to-gap-target
method_tags: [constructive-qft]
barrier_family: ""
confidence: 0.95
proof_sketch: ""
notes: |
  Section: Axiomatic quantum field theory and the mass gap notion.
  Source label: Mass gap in Hamiltonian terms.
```

```yaml
id: st.def.lattice-gauge-theory
kind: definition
status: accepted
latex: |
  In Wilson lattice gauge theory on a finite lattice $\Lambda \subset \mathbb{Z}^d$,
  a gauge field assigns a group element to each oriented edge, and the Gibbs
  measure is defined from the Wilson plaquette action using Haar measure on the
  compact gauge group.
informal: |
  Lattice gauge theory gives a fixed-lattice-spacing probabilistic model of the
  gauge field using edge variables and the Wilson action.
source_ids: [src.001]
used_symbols: [sym.G]
depends_on: [st.def.compact-simple-gauge-group]
concept_roles:
  - cnc.lattice-gauge-theory
  - cnc.yang-mills-theory
statement_phase: continuum-limit-and-renormalization
bridge_roles:
  - continuum-limit-source
  - lattice-regularization-source
method_tags: [lattice-gauge-theory]
barrier_family: ""
confidence: 0.94
proof_sketch: ""
notes: |
  Section: Constructive and lattice approaches.
  Source label: Lattice gauge theory (Wilson formulation).
```

```yaml
id: st.rem.continuum-limit-bottleneck
kind: remark
status: accepted
latex: |
  The main unresolved bottleneck for the Clay problem is the nonperturbative
  four-dimensional continuum limit: one must control ultraviolet renormalization
  while preserving reflection positivity or equivalent axioms, and prove
  infrared spectral positivity strong enough to yield a positive mass gap.
informal: |
  The core obstacle is not defining lattice Yang-Mills at fixed spacing, but
  taking a rigorous four-dimensional continuum limit that still satisfies the
  axioms and has a mass gap.
source_ids: [src.001]
used_symbols: [sym.Delta]
depends_on:
  - st.prob.yang-mills-existence-mass-gap
  - st.def.os-euclidean-qft
  - st.def.mass-gap
  - st.def.lattice-gauge-theory
concept_roles:
  - cnc.continuum-limit
  - cnc.os-axioms
  - cnc.mass-gap
  - bar.nonperturbative-4d-continuum-limit
statement_phase: bottlenecks-and-open-gaps
bridge_roles:
  - continuum-limit-barrier
  - bridge-obstruction
method_tags:
  - constructive-qft
  - lattice-gauge-theory
barrier_family: nonperturbative-4d-continuum-limit
is_barrier: true
confidence: 0.92
proof_sketch: |
  The report synthesizes constructive-QFT and lattice results to isolate the
  transition from fixed-spacing control to continuum control as the decisive gap.
notes: |
  Section: Executive summary.
  Source label: Main mathematical bottleneck.
```

```yaml
id: st.def.compact-lie-group-and-gauge-group
kind: definition
status: accepted
latex: A \emph{gauge group} for Yang--Mills theory is typically a compact Lie group $G$ with Lie algebra $\Lie g$ admitting an $\Ad$-invariant inner product $\langle \cdot,\cdot\rangle_{\Lie g}$ (e.g.\ $G$ compact semisimple, using minus the Killing form). \emph{Compact simple} means $G$ is compact and its Lie algebra is simple \cite{JaffeWitten2000}.
informal: A emph gauge group for Yang--Mills theory is typically a compact Lie group G with Lie algebra Lie g admitting an Ad -invariant inner product langle cdot,cdotrangle_ Lie g (e.g. G compact semisimple, using minus the Killing form). emph Compact simple means G is compact and its...
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: 'parsed_env: definition

  section: Geometric and classical Yang--Mills foundations

  source_citation: /Users/user/Downloads/deep-research-report (1).md

  label: Compact Lie group and gauge group'
```

```yaml
id: st.def.principal-bundle-and-connection
kind: definition
status: accepted
latex: Let $M$ be a smooth manifold and $G$ a Lie group. A \emph{principal $G$-bundle} is $\pi:P\to M$ with a free right $G$-action on $P$ such that $M\simeq P/G$. A (principal) \emph{connection} is a $G$-equivariant splitting of $TP$ into horizontal and vertical subbundles, equivalently a $\Lie g$-valued $1$-form $A\in\Omega^1(P;\Lie g)$ satisfying the usual axioms (reproduces generators of vertical fields and transforms under right translation by $\Ad$) \cite{Donaldson1983,FreedUhlenbeck1984}.
informal: Let M be a smooth manifold and G a Lie group. A emph principal G -bundle is pi:Pto M with a free right G -action on P such that Msimeq P/G . A (principal) emph connection is a G -equivariant splitting of TP into horizontal and vertical subbundles, equivalently a Lie g -valued...
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: 'parsed_env: definition

  section: Geometric and classical Yang--Mills foundations

  source_citation: /Users/user/Downloads/deep-research-report (1).md

  label: Principal bundle and connection'
```

```yaml
id: st.def.yang-mills-action-and-equations
kind: definition
status: accepted
latex: 'Let $(M,g)$ be an oriented Riemannian manifold. The (Euclidean) \emph{Yang--Mills action functional} is

  \[

  S_{\mathrm{YM}}(A)=\frac{1}{2}\int_M \langle F_A, F_A\rangle \, \mathrm{dvol}_g,

  \]

  and the Euler--Lagrange equations are the \emph{Yang--Mills equations}

  \[

  d_A^\ast F_A = 0.

  \]

  In Lorentzian signature (Minkowski space), the equations become hyperbolic PDE. \cite{FreedUhlenbeck1984,Douglas2004}'
informal: Let (M,g) be an oriented Riemannian manifold. The (Euclidean) emph Yang--Mills action functional is [ S_ mathrm YM (A)=frac 1 2 int_M langle F_A, F_Arangle , mathrm dvol _g, ] and the Euler--Lagrange equations are the emph Yang--Mills equations [ d_A^ast F_A = 0. ] In Lorentzi...
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: 'parsed_env: definition

  section: Geometric and classical Yang--Mills foundations

  source_citation: /Users/user/Downloads/deep-research-report (1).md

  label: Yang--Mills action and equations'
```

```yaml
id: st.def.instantons-and-self-duality-in-four-dimensions
kind: definition
status: accepted
latex: On an oriented Riemannian $4$-manifold $(M^4,g)$, the Hodge star on $2$-forms satisfies $\ast^2=1$, giving $\Omega^2=\Omega^2_+\oplus\Omega^2_-$. A connection is \emph{(anti-)self-dual} if $F_A=\pm \ast F_A$. Finite-action (anti-)self-dual solutions on $\R^4$ (or $S^4$) are called \emph{instantons} \cite{BelavinEtAl1975,AtiyahEtAl1978,FreedUhlenbeck1984}.
informal: On an oriented Riemannian 4 -manifold (M^4,g) , the Hodge star on 2 -forms satisfies ast^2=1 , giving Omega^2=Omega^2_+oplusOmega^2_- . A connection is emph (anti-)self-dual if F_A=pm ast F_A . Finite-action (anti-)self-dual solutions on R^4 (or S^4 ) are called emph instanton...
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: 'parsed_env: definition

  section: Geometric and classical Yang--Mills foundations

  source_citation: /Users/user/Downloads/deep-research-report (1).md

  label: Instantons and self-duality in four dimensions'
```

```yaml
id: st.thm.bpst-instanton-existence-prototype-instanton
kind: theorem
status: accepted
latex: 'There exist smooth finite-action self-dual solutions to the Euclidean Yang--Mills equations on $\R^4$ with gauge group $SU(2)$ (the BPST instanton), exhibiting nontrivial topological charge \cite{BelavinEtAl1975}.\\

  \textit{Assumptions.} Euclidean signature, $4$ dimensions, compact gauge group containing $SU(2)$.\\

  \textit{Limitations/barriers.} This is a \emph{classical} (Euclidean) solution and does not constitute a construction of the \emph{quantum} theory; nevertheless it motivates nonperturbative sectors (topological charge, $\theta$-vacua) that a full quantum construction must control \cite{Douglas2004}.'
informal: There exist smooth finite-action self-dual solutions to the Euclidean Yang--Mills equations on R^4 with gauge group SU(2) (the BPST instanton), exhibiting nontrivial topological charge cite BelavinEtAl1975 . textit Assumptions. Euclidean signature, 4 dimensions, compact gauge...
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: 'parsed_env: theorem

  section: Geometric and classical Yang--Mills foundations

  source_citation: /Users/user/Downloads/deep-research-report (1).md

  label: BPST instanton existence (prototype instanton)'
```

```yaml
id: st.thm.adhm-classification-all-instantons-on-s-4
kind: theorem
status: accepted
latex: 'A complete classification/construction of (anti-)self-dual instantons on $S^4$ (equivalently $\R^4\cup\{\infty\}$) in terms of finite-dimensional linear-algebraic data is given by the Atiyah--Drinfeld--Hitchin--Manin construction \cite{AtiyahEtAl1978}.\\

  \textit{Assumptions.} Smooth category; compact gauge group $U(r)$ (and related forms); finite action.\\

  \textit{Limitations/barriers.} This concerns the moduli of classical solutions; translating this structure into rigorous control of the quantum path integral in $4$D remains open.'
informal: A complete classification/construction of (anti-)self-dual instantons on S^4 (equivalently R^4cup infty ) in terms of finite-dimensional linear-algebraic data is given by the Atiyah--Drinfeld--Hitchin--Manin construction cite AtiyahEtAl1978 . textit Assumptions. Smooth categor...
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: 'parsed_env: theorem

  section: Geometric and classical Yang--Mills foundations

  source_citation: /Users/user/Downloads/deep-research-report (1).md

  label: ADHM classification (all instantons on $S^4$)'
```

```yaml
id: st.thm.uhlenbeck-gauge-fixing-and-compactness
kind: theorem
status: accepted
latex: 'Let $A$ be a connection on a bundle over a ball $B\subset\R^n$. If $\|F_A\|_{L^{n/2}(B)}$ is sufficiently small, then there exists a gauge in which $A$ is in (local) Coulomb gauge with Sobolev bounds in terms of $\|F_A\|$ \cite{UhlenbeckLp1982}. Moreover, sequences of connections with uniform $L^p$ curvature bounds (with $p>n/2$) admit subsequences converging modulo gauge away from a controlled singular set; in $4$D this underlies bubbling/compactness for Yang--Mills fields \cite{UhlenbeckLp1982,UhlenbeckRemovable1982}.\\

  \textit{Assumptions.} Differential-geometric setting; small-energy hypothesis for local gauge; $p>n/2$ for compactness; typically compact structure group.\\

  \textit{Limitations/barriers.} These are foundational for \emph{classical} analysis and moduli spaces (including instanton compactness), but do not by themselves provide the probabilistic/measure-theoretic control required for a quantum field theory on $\R^4$.'
informal: Let A be a connection on a bundle over a ball BsubsetR^n . If |F_A|_ L^ n/2 (B) is sufficiently small, then there exists a gauge in which A is in (local) Coulomb gauge with Sobolev bounds in terms of |F_A| cite UhlenbeckLp1982 . Moreover, sequences of connections with uniform...
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: 'parsed_env: theorem

  section: Geometric and classical Yang--Mills foundations

  source_citation: /Users/user/Downloads/deep-research-report (1).md

  label: Uhlenbeck gauge fixing and compactness'
```

```yaml
id: st.thm.existence-of-minimisers-for-yang-mills-functiona
kind: theorem
status: accepted
latex: 'On a compact $4$-manifold, one can minimise the Yang--Mills functional in suitable topological classes (up to bubbling phenomena) and obtain Yang--Mills connections as limits of minimising sequences; one must account for possible energy concentration and bundle changes \cite{Sedlacek1982}.\\

  \textit{Assumptions.} Compact Riemannian $4$-manifold; variational framework; Sobolev/gauge analysis.\\

  \textit{Limitations/barriers.} Again a classical existence result, crucial for geometry/topology; it does not construct the quantum measure nor establish a quantum mass gap.'
informal: On a compact 4 -manifold, one can minimise the Yang--Mills functional in suitable topological classes (up to bubbling phenomena) and obtain Yang--Mills connections as limits of minimising sequences; one must account for possible energy concentration and bundle changes cite Sed...
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: 'parsed_env: theorem

  section: Geometric and classical Yang--Mills foundations

  source_citation: /Users/user/Downloads/deep-research-report (1).md

  label: Existence of minimisers for Yang--Mills functional on $4$-manifolds'
```

```yaml
id: st.thm.global-classical-well-posedness-in-3-1-dimension
kind: theorem
status: accepted
latex: "Classical Yang--Mills--Higgs equations in $4$-dimensional Minkowski space (spatial dimension $3$) admit global smooth solutions for smooth finite-energy initial data in temporal gauge; local existence/regularity and a priori bounds imply global existence \\cite{EardleyMoncrief1982I,EardleyMoncrief1982II}.\\\\\n\\textit{Assumptions.} Classical PDE; compact gauge group; suitable Higgs self-coupling hypotheses in the cited works; smooth initial data.\\\\\n\\textit{Limitations/barriers.} The Clay problem is quantum and Euclidean/Minkowskian axiomatic; classical well-posedness is necessary background but far from sufficient for a nonperturbative QFT construction \\cite{Douglas2004,JaffeWitten2000}. % Web source: Springer pages with details. \uE200cite\uE202turn23view0\uE202turn23view1\uE201"
informal: Classical Yang--Mills--Higgs equations in 4 -dimensional Minkowski space (spatial dimension 3 ) admit global smooth solutions for smooth finite-energy initial data in temporal gauge; local existence/regularity and a priori bounds imply global existence cite EardleyMoncrief1982...
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: 'parsed_env: theorem

  section: Geometric and classical Yang--Mills foundations

  source_citation: /Users/user/Downloads/deep-research-report (1).md

  label: Global classical well-posedness in $3+1$ dimensions (Yang--Mills--Higgs)'
```

```yaml
id: st.thm.yang-mills-on-riemann-surfaces-atiyah-bott
kind: theorem
status: accepted
latex: 'For a compact Riemann surface, the Yang--Mills functional on the space of connections modulo gauge is a Morse--Bott functional whose critical sets relate to holomorphic bundle data; this provides a deep link between Yang--Mills theory and the topology of moduli of bundles \cite{AtiyahBott1983}.\\

  \textit{Assumptions.} Two-dimensional base (Riemann surface); compact structure group; smooth category.\\

  \textit{Limitations/barriers.} This delivers a fully geometric understanding in $2$D and strongly influences $2$D quantum Yang--Mills; it does not extend directly to a $4$D quantum constructive result.'
informal: For a compact Riemann surface, the Yang--Mills functional on the space of connections modulo gauge is a Morse--Bott functional whose critical sets relate to holomorphic bundle data; this provides a deep link between Yang--Mills theory and the topology of moduli of bundles cite...
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: 'parsed_env: theorem

  section: Geometric and classical Yang--Mills foundations

  source_citation: /Users/user/Downloads/deep-research-report (1).md

  label: Yang--Mills on Riemann surfaces (Atiyah--Bott)'
```

```yaml
id: st.thm.donaldson-s-gauge-theoretic-constraints-on-smoot
kind: theorem
status: accepted
latex: 'Anti-self-dual Yang--Mills moduli spaces yield smooth invariants of $4$-manifolds; as a landmark consequence, definite intersection forms of smooth simply connected closed oriented $4$-manifolds are diagonalisable over $\mathbb{Z}$ \cite{Donaldson1983}.\\

  \textit{Assumptions.} Smooth, compact, oriented $4$-manifolds; analysis of ASD moduli spaces.\\

  \textit{Limitations/barriers.} These are results in \emph{classical} gauge theory and topology; they underscore the richness of Yang--Mills geometry but do not imply existence/mass gap for the $4$D quantum theory on $\R^4$.'
informal: Anti-self-dual Yang--Mills moduli spaces yield smooth invariants of 4 -manifolds; as a landmark consequence, definite intersection forms of smooth simply connected closed oriented 4 -manifolds are diagonalisable over mathbb Z cite Donaldson1983 . textit Assumptions. Smooth, co...
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: 'parsed_env: theorem

  section: Geometric and classical Yang--Mills foundations

  source_citation: /Users/user/Downloads/deep-research-report (1).md

  label: Donaldson''s gauge-theoretic constraints on smooth $4$-manifolds'
```

```yaml
id: st.obs.seiberg-witten-and-gauge-theoretic-dualities
kind: observation
status: accepted
latex: Supersymmetric Yang--Mills theory leads to alternative gauge-theoretic PDE (Seiberg--Witten monopole equations) and invariants; Witten proposed structural relationships between Donaldson invariants and Seiberg--Witten invariants \cite{WittenMonopoles1994,SeibergWitten1994}. These developments are mathematically powerful in \emph{topological} or supersymmetric settings but do not, by themselves, yield a constructive definition of non-supersymmetric $4$D quantum Yang--Mills on $\R^4$ with a mass gap \cite{Douglas2004}.
informal: Supersymmetric Yang--Mills theory leads to alternative gauge-theoretic PDE (Seiberg--Witten monopole equations) and invariants; Witten proposed structural relationships between Donaldson invariants and Seiberg--Witten invariants cite WittenMonopoles1994,SeibergWitten1994 . The...
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.72
proof_sketch: ''
notes: 'parsed_env: remark

  section: Geometric and classical Yang--Mills foundations

  source_citation: /Users/user/Downloads/deep-research-report (1).md

  label: Seiberg--Witten and gauge-theoretic dualities

  normalization: remark mapped to observation'
```

```yaml
id: st.def.osterwalder-schrader-os-euclidean-qft
kind: definition
status: accepted
latex: 'An \emph{OS Euclidean QFT} is specified by a collection of Euclidean $n$-point Schwinger functions $(S_n)_{n\ge 0}$ (tempered distributions on $\R^{4n}$) satisfying: Euclidean invariance, symmetry, reflection positivity, regularity, and clustering/analyticity conditions (in the standard OS formulations) \cite{OsterwalderSchrader1973,OsterwalderSchrader1975}.\\

  \textit{Barrier relevance.} Constructive quantum field theory often proceeds by constructing an Euclidean measure or $S_n$ satisfying OS axioms and then reconstructing a Minkowski Wightman theory.'
informal: 'An emph OS Euclidean QFT is specified by a collection of Euclidean n -point Schwinger functions (S_n)_ nge 0 (tempered distributions on R^ 4n ) satisfying: Euclidean invariance, symmetry, reflection positivity, regularity, and clustering/analyticity conditions (in the standard...'
source_ids:
- src.001
used_symbols: []
depends_on: []
statement_phase: euclidean-os-framework
bridge_roles:
  - os-source
  - os-to-wightman-source
  - os-to-wightman-to-gap-source
confidence: 0.95
proof_sketch: ''
notes: 'parsed_env: definition

  section: Axiomatic quantum field theory and the mass gap notion

  source_citation: /Users/user/Downloads/deep-research-report (1).md

  label: Osterwalder--Schrader (OS) Euclidean QFT'
```

```yaml
id: st.thm.os-reconstruction-and-equivalence-with-wightman-
kind: theorem
status: accepted
latex: 'If $(S_n)$ satisfy the OS axioms, then there exists a corresponding Wightman QFT on Minkowski space whose Wightman distributions analytically continue to $(S_n)$. Conversely, (under standard hypotheses) Wightman theories yield OS Schwinger functions via analytic continuation \cite{OsterwalderSchrader1973,OsterwalderSchrader1975}.\\

  \textit{Assumptions.} OS axioms (including reflection positivity) and temperedness/regularity; vacuum setting.\\

  \textit{Limitations/barriers.} For gauge theories, one must formulate OS/Wightman data in terms of \emph{gauge-invariant observables} (or a carefully controlled gauge-fixed framework) while preserving reflection positivity; ensuring this in $4$D non-Abelian continuum limits is a core unsolved obstacle \cite{JaffeWitten2000,Seiler1982}.'
informal: If (S_n) satisfy the OS axioms, then there exists a corresponding Wightman QFT on Minkowski space whose Wightman distributions analytically continue to (S_n) . Conversely, (under standard hypotheses) Wightman theories yield OS Schwinger functions via analytic continuation cite...
source_ids:
- src.001
used_symbols: []
depends_on: []
statement_phase: wightman-hamiltonian-framework
bridge_roles:
  - os-reconstruction-bridge
  - os-to-wightman-bridge
  - os-to-wightman-to-gap-bridge
confidence: 0.86
proof_sketch: ''
notes: 'parsed_env: theorem

  section: Axiomatic quantum field theory and the mass gap notion

  source_citation: /Users/user/Downloads/deep-research-report (1).md

  label: OS reconstruction and equivalence with Wightman axioms'
```

```yaml
id: st.def.mass-gap-in-hamiltonian-wightman-terms
kind: definition
status: accepted
latex: "A Wightman QFT has a \\emph{mass gap} $\\Delta>0$ if the spectrum of the Hamiltonian $H$ (time-translation generator) has no spectrum in $(0,\\Delta)$. Equivalently, the vacuum is isolated and the first excitation energy is at least $\\Delta$ \\cite{JaffeWitten2000,StreaterWightman2000}. % Web source: Clay PDF line defining mass gap. \uE200cite\uE202turn7view0\uE201"
informal: A Wightman QFT has a emph mass gap Delta>0 if the spectrum of the Hamiltonian H (time-translation generator) has no spectrum in (0,Delta) . Equivalently, the vacuum is isolated and the first excitation energy is at least Delta cite JaffeWitten2000,StreaterWightman2000 . % Web...
source_ids:
- src.001
used_symbols: []
depends_on: []
statement_phase: wightman-hamiltonian-framework
bridge_roles:
  - mass-gap-target
  - transfer-matrix-to-gap-target
  - correlator-decay-to-gap-target
  - os-to-wightman-to-gap-target
confidence: 0.95
proof_sketch: ''
notes: 'parsed_env: definition

  section: Axiomatic quantum field theory and the mass gap notion

  source_citation: /Users/user/Downloads/deep-research-report (1).md

  label: Mass gap in Hamiltonian (Wightman) terms'
```

```yaml
id: st.thm.euclidean-correlator-decay-as-a-mass-gap-signatu
kind: theorem
status: accepted
latex: 'In OS-positive theories, a positive spectral gap for the Hamiltonian implies exponential decay of suitable Euclidean time-separated correlation functions of local observables; conversely, sufficiently strong exponential decay properties can imply a spectral gap via transfer-matrix / reconstruction arguments \cite{StreaterWightman2000,OsterwalderSchrader1973,OsterwalderSchrader1975}.\\

  \textit{Assumptions.} Reflection positivity and reconstruction machinery; local observables with good spectral representation.\\

  \textit{Limitations/barriers.} In non-Abelian gauge theories, the physically meaningful observables are gauge-invariant (e.g.\ Wilson loops, local polynomials in curvature). Establishing exponential decay \emph{uniformly in the continuum limit} is exactly the mass-gap problem.'
informal: In OS-positive theories, a positive spectral gap for the Hamiltonian implies exponential decay of suitable Euclidean time-separated correlation functions of local observables; conversely, sufficiently strong exponential decay properties can imply a spectral gap via transfer-ma...
source_ids:
- src.001
used_symbols: []
depends_on: []
statement_phase: mass-gap-and-spectral-transfer
bridge_roles:
  - correlator-decay-to-gap-bridge
  - correlator-decay-to-gap-source
confidence: 0.83
proof_sketch: ''
notes: 'parsed_env: proposition

  section: Axiomatic quantum field theory and the mass gap notion

  source_citation: /Users/user/Downloads/deep-research-report (1).md

  label: Euclidean correlator decay as a mass-gap signature (informal-to-formal bridge)

  normalization: proposition mapped to theorem'
```

```yaml
id: st.def.lattice-gauge-theory-wilson-formulation
kind: definition
status: accepted
latex: "Let $\\Lambda\\subset \\mathbb{Z}^d$ be a finite lattice. A (pure) lattice gauge field assigns group elements $U_e\\in G$ to oriented edges $e$ with $U_{e^{-1}}=U_e^{-1}$. The Wilson action is a sum over plaquettes $p$ of a class function of the plaquette holonomy $U_p$ (product of edge variables around $p$), commonly $S_\\Lambda(U)=\\sum_p \\Re \\Tr(1-U_p)$ for matrix groups. The Gibbs measure is\n\\[\n\\mu_{\\Lambda,\\beta}(\\mathrm{d}U) = \\frac{1}{Z_{\\Lambda,\\beta}} \\exp\\!\\big(-\\beta S_\\Lambda(U)\\big)\\,\\prod_{e\\in E(\\Lambda)} \\mathrm{d}U_e,\n\\]\nwith Haar measure on $G$ \\cite{Wilson1974,OsterwalderSeiler1978,Seiler1982}. % Web source: lattice formulation appears in sources around Osterwalder-Seiler and Wilson. \uE200cite\uE202turn2search7\uE202turn10search0\uE201"
informal: Let Lambdasubset mathbb Z ^d be a finite lattice. A (pure) lattice gauge field assigns group elements U_ein G to oriented edges e with U_ e^ -1 =U_e^ -1 . The Wilson action is a sum over plaquettes p of a class function of the plaquette holonomy U_p (product of edge variables...
source_ids:
- src.001
used_symbols: []
depends_on: []
statement_phase: continuum-limit-and-renormalization
bridge_roles:
  - continuum-limit-source
  - lattice-regularization-source
confidence: 0.95
proof_sketch: ''
notes: 'parsed_env: definition

  section: Constructive and lattice approaches: rigorous results and partial progress

  source_citation: /Users/user/Downloads/deep-research-report (1).md

  label: Lattice gauge theory (Wilson formulation)'
```

```yaml
id: st.thm.reflection-positivity-and-transfer-matrix-for-la
kind: theorem
status: accepted
latex: 'For standard lattice gauge actions (including the Wilson action) with compact gauge group, one can achieve a form of reflection positivity enabling construction of a Hilbert space and a positive self-adjoint transfer matrix (hence a Hamiltonian) for the lattice theory \cite{OsterwalderSeiler1978,Seiler1982}.\\

  \textit{Assumptions.} Compact gauge group; appropriate action and reflection structure; finite lattice (with suitable boundary conditions).\\

  \textit{Limitations/barriers.} A lattice theory at fixed spacing is well-defined, but the Clay problem requires control of the \emph{continuum limit} (lattice spacing $\to 0$ in $d=4$) and verification of axioms in that limit.'
informal: For standard lattice gauge actions (including the Wilson action) with compact gauge group, one can achieve a form of reflection positivity enabling construction of a Hilbert space and a positive self-adjoint transfer matrix (hence a Hamiltonian) for the lattice theory cite Ost...
source_ids:
- src.001
used_symbols: []
depends_on: []
statement_phase: mass-gap-and-spectral-transfer
bridge_roles:
  - transfer-matrix-to-gap-bridge
  - transfer-matrix-to-gap-source
confidence: 0.86
proof_sketch: ''
notes: 'parsed_env: theorem

  section: Constructive and lattice approaches: rigorous results and partial progress

  source_citation: /Users/user/Downloads/deep-research-report (1).md

  label: Reflection positivity and transfer matrix for lattice gauge theory'
```

```yaml
id: st.thm.strong-coupling-exponential-decay-and-a-lattice-
kind: theorem
status: accepted
latex: 'In many lattice gauge theories, cluster-expansion methods at sufficiently strong coupling (small $\beta$, large bare coupling) yield exponential decay of correlations of local gauge-invariant observables and imply a positive spectral gap for the transfer matrix, i.e.\ a lattice ``mass gap'''' at fixed lattice spacing \cite{Seiler1982,OsterwalderSeiler1978}.\\

  \textit{Assumptions.} Strong coupling regime; cluster expansion / polymer methods; compact gauge group.\\

  \textit{Limitations/barriers.} This does not establish a mass gap in the weak coupling regime relevant to continuum $4$D Yang--Mills (where $\beta\to\infty$ as spacing $\to 0$), nor does it by itself prove existence of a nontrivial scaling limit.'
informal: In many lattice gauge theories, cluster-expansion methods at sufficiently strong coupling (small beta , large bare coupling) yield exponential decay of correlations of local gauge-invariant observables and imply a positive spectral gap for the transfer matrix, i.e. a lattice `...
source_ids:
- src.001
used_symbols: []
depends_on: []
statement_phase: mass-gap-and-spectral-transfer
bridge_roles:
  - transfer-matrix-to-gap-source
  - correlator-decay-to-gap-source
confidence: 0.83
proof_sketch: ''
notes: 'parsed_env: proposition

  section: Constructive and lattice approaches: rigorous results and partial progress

  source_citation: /Users/user/Downloads/deep-research-report (1).md

  label: Strong coupling: exponential decay and a lattice mass gap (typical theorem schema)

  normalization: proposition mapped to theorem'
```

```yaml
id: st.thm.constructive-qft-in-low-dimension-examples-with-
kind: theorem
status: accepted
latex: 'There exist nontrivial interacting QFT models in $2$ and $3$ spacetime dimensions satisfying the Wightman (and/or OS) axioms and exhibiting particle structure and mass gaps in appropriate regimes, developed within constructive QFT \cite{GlimmJaffeSpencer1974,GuerraRosenSimon1975,GlimmJaffe1987}.\\

  \textit{Assumptions.} Lower spacetime dimension ($d=2,3$); models such as $P(\phi)_2$; constructive control via cluster/renormalisation methods.\\

  \textit{Limitations/barriers.} These achievements do not currently extend to non-Abelian Yang--Mills in $4$D; nonetheless they provide methodological templates (OS positivity, RG, cluster expansions, control of ultraviolet/infrared).'
informal: There exist nontrivial interacting QFT models in 2 and 3 spacetime dimensions satisfying the Wightman (and/or OS) axioms and exhibiting particle structure and mass gaps in appropriate regimes, developed within constructive QFT cite GlimmJaffeSpencer1974,GuerraRosenSimon1975,Gl...
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: 'parsed_env: theorem

  section: Constructive and lattice approaches: rigorous results and partial progress

  source_citation: /Users/user/Downloads/deep-research-report (1).md

  label: Constructive QFT in low dimension: examples with mass gap'
```

```yaml
id: st.thm.two-dimensional-abelian-higgs-model-without-cuto
kind: theorem
status: accepted
latex: 'The $2$-dimensional Abelian Higgs model can be constructed nonperturbatively without ultraviolet cutoffs and satisfies the OS axioms; this provides a mathematically complete example of a gauge field model in the constructive QFT sense \cite{BrydgesFrohlichSeiler1981}.\\

  \textit{Assumptions.} Abelian gauge group; $2$ Euclidean dimensions; constructive RG/cluster methods.\\

  \textit{Limitations/barriers.} Non-Abelian $4$D Yang--Mills has fundamentally different ultraviolet behaviour and gauge-configuration complexity; methods do not yet scale.'
informal: The 2 -dimensional Abelian Higgs model can be constructed nonperturbatively without ultraviolet cutoffs and satisfies the OS axioms; this provides a mathematically complete example of a gauge field model in the constructive QFT sense cite BrydgesFrohlichSeiler1981 . textit Ass...
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: 'parsed_env: theorem

  section: Constructive and lattice approaches: rigorous results and partial progress

  source_citation: /Users/user/Downloads/deep-research-report (1).md

  label: Two-dimensional Abelian Higgs model without cutoffs'
```

```yaml
id: st.thm.four-dimensional-yang-mills-with-an-infrared-cut
kind: theorem
status: accepted
latex: 'A rigorous construction of Schwinger functions for $4$D pure $SU(2)$ Yang--Mills in the trivial topological sector with a fixed infrared cutoff (finite-volume/IR regulator) and no ultraviolet cutoff was provided in a gauge-fixed framework \cite{MagnenRivasseauSeneor1993}.\\

  \textit{Assumptions.} Fixed IR cutoff; gauge choice and technical control of positivity/estimates as in the cited work.\\

  \textit{Limitations/barriers.} Removing the IR cutoff while preserving axioms and proving a mass gap remains open; controlling topological sectors and full $\R^4$ translation invariance is a major barrier \cite{JaffeWitten2000,Douglas2004}.'
informal: A rigorous construction of Schwinger functions for 4 D pure SU(2) Yang--Mills in the trivial topological sector with a fixed infrared cutoff (finite-volume/IR regulator) and no ultraviolet cutoff was provided in a gauge-fixed framework cite MagnenRivasseauSeneor1993 . textit A...
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: 'parsed_env: theorem

  section: Constructive and lattice approaches: rigorous results and partial progress

  source_citation: /Users/user/Downloads/deep-research-report (1).md

  label: Four-dimensional Yang--Mills with an infrared cutoff'
```

```yaml
id: st.thm.balaban-s-rigorous-renormalisation-group-analysi
kind: theorem
status: accepted
latex: 'Balaban developed a renormalisation-group analysis for lattice gauge theories establishing ultraviolet stability results in $d=3$ and advancing a multi-paper programme in $d=4$, including construction of effective actions in a small field regime and convergent expansions at various stages \cite{Balaban1987,Balaban1988,Balaban1989}.\\

  \textit{Assumptions.} Lattice formulation; renormalisation-group framework; technical decompositions separating small/large fields; (often) partial regimes.\\

  \textit{Limitations/barriers.} The programme does not yield a complete $4$D non-Abelian continuum Yang--Mills construction with OS/Wightman axioms and a mass gap; bridging UV control to full IR physics remains open \cite{Douglas2004}.'
informal: Balaban developed a renormalisation-group analysis for lattice gauge theories establishing ultraviolet stability results in d=3 and advancing a multi-paper programme in d=4 , including construction of effective actions in a small field regime and convergent expansions at vario...
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: 'parsed_env: theorem

  section: Constructive and lattice approaches: rigorous results and partial progress

  source_citation: /Users/user/Downloads/deep-research-report (1).md

  label: Balaban''s rigorous renormalisation-group analysis on the lattice (UV stability programme)'
```

```yaml
id: st.thm.modern-probabilistic-progress-on-lattice-gauge-t
kind: theorem
status: accepted
latex: 'Recent work develops rigorous probability techniques for lattice gauge observables, including rigorous strong-coupling large-$N$ expansions and results relating exponential correlation decay to confinement/area-law behaviour under structural hypotheses on the gauge group \cite{Chatterjee2019,Chatterjee2020Arxiv}.\\

  \textit{Assumptions.} Lattice setting; often strong-coupling regime and/or large-$N$ limits; specific notions of correlation decay and boundary conditions.\\

  \textit{Limitations/barriers.} These results do not yet deliver the $4$D continuum scaling limit with OS/Wightman axioms or a proof of mass gap for $SU(3)$ (or general compact simple $G$) in the continuum.'
informal: Recent work develops rigorous probability techniques for lattice gauge observables, including rigorous strong-coupling large- N expansions and results relating exponential correlation decay to confinement/area-law behaviour under structural hypotheses on the gauge group cite C...
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: 'parsed_env: theorem

  section: Constructive and lattice approaches: rigorous results and partial progress

  source_citation: /Users/user/Downloads/deep-research-report (1).md

  label: Modern probabilistic progress on lattice gauge theory (selected examples)'
```

```yaml
id: st.obs.non-rigorous-lattice-evidence-for-the-mass-gap
kind: observation
status: accepted
latex: High-precision lattice computations estimate glueball spectra (hence a physical mass scale) in $SU(N)$ gauge theories \cite{LuciniTeperWenger2004,ChenEtAl2006}. These serve as strong \emph{physics evidence} for a mass gap, but they do not constitute a rigorous proof in the sense of the Clay problem \cite{JaffeWitten2000}.
informal: High-precision lattice computations estimate glueball spectra (hence a physical mass scale) in SU(N) gauge theories cite LuciniTeperWenger2004,ChenEtAl2006 . These serve as strong emph physics evidence for a mass gap, but they do not constitute a rigorous proof in the sense of...
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.72
proof_sketch: ''
notes: 'parsed_env: remark

  section: Constructive and lattice approaches: rigorous results and partial progress

  source_citation: /Users/user/Downloads/deep-research-report (1).md

  label: Non-rigorous lattice evidence for the mass gap

  normalization: remark mapped to observation'
```

# Derived Statements

# Open Gaps

- `gap.001`: Extract the full theorem and proposition layer from the report into canonical statements.
- `gap.002`: Add gauge-invariant observables (Wilson loops, local curvature polynomials, glueball correlators) as first-class concepts.
- `gap.003`: Separate fixed-lattice-spacing mass-gap statements from continuum mass-gap statements to avoid conflation.
- `gap.004`: Add explicit continuum-limit and reflection-positivity dependency chains for the strongest constructive routes.

# Change Log

- 2026-03-11: Initialized KB from `/Users/user/Downloads/deep-research-report (1).md` for the Yang-Mills existence and mass gap problem.
- 2026-03-11: Imported theorem/definition layer from deep-research-report (1).md into the Yang-Mills KB. Added 25 canonical and 0 derived statements.

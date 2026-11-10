<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Target Problem And Literature Evolution

- Target: `yang-mills-existence-and-mass-gap-target`
- Problem: Yang-Mills existence and mass gap
- Statement: Construct a nontrivial four-dimensional quantum Yang-Mills theory for every compact simple gauge group and prove a strictly positive mass gap.

## Why It Matters

- It asks for the first complete nonperturbative construction of a physically central four-dimensional interacting quantum gauge theory.
- It would turn the physicists' confinement and glueball mass-gap picture into a theorem in a reconstructed quantum field theory.
- It is a stress test for whether constructive QFT, Euclidean reconstruction, lattice gauge theory, and renormalization can meet in one same-theory proof.

## Literature Evolution

### 1954 - The non-abelian gauge object is born

- Shift: Yang and Mills replace an abelian electromagnetic-style gauge field with a nonlinear non-abelian gauge field.
- Became possible: The target object becomes a rich classical field theory with compact gauge-group structure.
- Still open: There is still no rigorous quantum field theory, no Hilbert space, and no mass-gap statement.
- References: ref.yang-mills-1954

### 1960s-1970s - The rigor standard becomes axiomatic and Euclidean

- Shift: Wightman axioms set a Lorentzian QFT standard; Osterwalder-Schrader theory makes Euclidean Schwinger functions a possible reconstruction route.
- Became possible: A proof can aim at Euclidean objects, but only if reflection positivity, covariance, regularity, clustering, and reconstruction hypotheses are preserved.
- Still open: The Yang-Mills Schwinger functions still have to be constructed nonperturbatively in four dimensions.
- References: ref.streater-wightman-1964, ref.os-1973-1975

### 1973-1974 - Asymptotic freedom and lattice confinement reshape expectations

- Shift: The literature clarifies the ultraviolet/infrared split: perturbation theory can work at short distances, while lattice strong coupling suggests confinement and massive glueball-like excitations.
- Became possible: The problem stops looking physically arbitrary: a gap is expected, and lattice regularization gives concrete finite systems to analyze.
- Still open: Short-distance perturbation and strong-coupling lattice arguments do not bridge to the continuum Clay target by themselves.
- References: ref.gross-wilczek-1973, ref.politzer-1973, ref.wilson-1974

### 1980s - Constructive QFT and RG expose the real mathematical bottleneck

- Shift: The literature shows that existence means constructing measures, Schwinger functions, limits, and reconstruction data with uniform control, not merely writing a path integral.
- Became possible: Balaban-style RG and constructive-field methods give a disciplined route language: cutoffs, ultraviolet stability, lattice-to-continuum control, and limiting objects.
- Still open: The full four-dimensional continuum Yang-Mills object, nontriviality, OS/Wightman adequacy, and positive spectral gap remain coupled obligations.
- References: ref.glimm-jaffe-1981, ref.seiler-1982, ref.balaban-1985

### 2000 onward - The Clay formulation fuses construction and mass gap into one target

- Shift: The problem becomes a same-theory requirement: construct the nontrivial theory and prove the positive gap for that reconstructed theory.
- Became possible: Discovery work can be audited against explicit commitments: existence, nontriviality, OS/Wightman adequacy, continuum limit, and positive mass gap.
- Still open: Most proposed routes risk solving a regulated, perturbative, lower-dimensional, numerical, or proxy problem unless same-theory transfer is certified.
- References: ref.jaffe-witten-clay, ref.douglas-2004

## Workflow Implications

- Every promising finite or lattice calculation must carry a same-theory transfer certificate. Effect: Branch ranking should reward calculations that state source object, target object, cutoff regime, and continuum handoff.
- Euclidean positivity is not a cosmetic condition; it is the bridge from Schwinger data to Hilbert-space spectral claims. Effect: OS/reflection-positivity branches should remain central, but only when they keep reconstruction assumptions explicit.
- Asymptotic freedom controls the ultraviolet story but leaves the infrared gap and construction problem alive. Effect: The loop should avoid mistaking perturbative UV success for nonperturbative continuum construction.
- Constructive/RG work teaches that uniform estimates and limiting objects are the proof currency. Effect: Next analyses should prefer bounded estimates, falsifiers, and bridge lemmas over broad route enthusiasm.

## References

- `ref.yang-mills-1954` C. N. Yang and R. L. Mills (1954), *Conservation of Isotopic Spin and Isotopic Gauge Invariance*. https://link.aps.org/doi/10.1103/PhysRev.96.191
- `ref.streater-wightman-1964` R. F. Streater and A. S. Wightman (1964), *PCT, Spin and Statistics, and All That*. https://ui.adsabs.harvard.edu/abs/2001pssa.book.....S/abstract
- `ref.os-1973-1975` K. Osterwalder and R. Schrader (1973), *Axioms for Euclidean Green's Functions I-II*. https://ncatlab.org/nlab/show/Osterwalder-Schrader%2Btheorem
- `ref.gross-wilczek-1973` D. J. Gross and F. Wilczek (1973), *Ultraviolet Behavior of Non-Abelian Gauge Theories*. https://link.aps.org/doi/10.1103/PhysRevLett.30.1343
- `ref.politzer-1973` H. D. Politzer (1973), *Reliable Perturbative Results for Strong Interactions?*. https://link.aps.org/doi/10.1103/PhysRevLett.30.1346
- `ref.wilson-1974` K. G. Wilson (1974), *Confinement of Quarks*. https://link.aps.org/doi/10.1103/PhysRevD.10.2445
- `ref.glimm-jaffe-1981` J. Glimm and A. Jaffe (1981), *Quantum Physics: A Functional Integral Point of View*. https://books.google.com/books/about/Quantum_Physics.html?id=VSjjBwAAQBAJ
- `ref.seiler-1982` E. Seiler (1982), *Gauge Theories as a Problem of Constructive Quantum Field Theory and Statistical Mechanics*. https://doi.org/10.1007/BFb0090332
- `ref.balaban-1985` T. Balaban (1985), *Ultraviolet Stability of Three-Dimensional Lattice Pure Gauge Field Theories*. https://inspirehep.net/literature/16302
- `ref.jaffe-witten-clay` A. Jaffe and E. Witten (2000), *Quantum Yang-Mills Theory*. https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf
- `ref.douglas-2004` M. R. Douglas (2004), *Report on the Status of the Yang-Mills Millennium Prize Problem*. https://www.claymath.org/library/annual_report/douglas_quantum_yang_mills.pdf

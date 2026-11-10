<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Yang-Mills Discovery Stretch

- Target: `yang-mills-existence-and-mass-gap-target`
- Quality gate: `pass`
- Long-horizon quality: `pass`
- Bridge packets: `2`

A large Yang-Mills discovery stretch should now search across six typed interfaces rather than add route slogans: reflection positivity closedness, nontriviality witnessing, observable density, Laplace support, nonvanishing mass scale, and no-gap reductio carriers.

## Synthesis

- The stretch run should advance by isolating the bridge obligations that can fail independently: positivity closedness, nontriviality witness, observable density, Laplace support, nonvanishing mass scale, and no-gap carrier.
- The most valuable next mathematical move is not another broad route family; it is a typed lemma or falsifier at one of these interfaces.
- The current exploration remains proof-safe because every program has a target-object interface, explicit falsifiers, and a pivot signal.

## Discovery Programs

### Reflection-Positivity Closed-Cone Topology

- Program: `ym-discovery-stretch.c6fe6e9a91af`
- Machinery role: `invariant_preservation`
- Controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions
- Hypothesis: If the cutoff-removal topology can be chosen so that reflection-positive gauge-invariant Schwinger distributions form a closed cone, then OS positivity can survive the RG continuum passage instead of being reintroduced by hand.

**Mathematical mechanism**

Treat OS positivity as a convex-cone closedness problem over gauge-invariant test observables. The discovery move is to identify the weakest topology strong enough to pass finite reflected quadratic forms to the limit while still compatible with Balaban-style multiscale compactness.

**Equations**
- regulated positivity: `Q_{a,L}(f,c)=\sum_{i,j}\overline c_i c_j S_{a,L}(\Theta f_i,f_j)\ge 0`
  - Valid when: Each regulated gauge-invariant observable family is reflection-positive before cutoff removal.
- closed cone transfer: `S_{a,L}\Rightarrow S,\quad Q_{a,L}(f,c)\to Q(f,c)\quad\Longrightarrow\quad Q(f,c)\ge0`
  - Valid when: The limiting topology gives convergence of every reflected finite test-observable quadratic form.

**Dependencies**
- RG-to-OS Continuum Passage Bridge Lemma
- choice of gauge-invariant test algebra
- cutoff-removal topology

**Falsifiers**
- The topology supplied by multiscale bounds is too weak to control reflected test forms.
- Gauge fixing or quotienting changes the test algebra across the limit.
- Reflection positivity is only proved for a lattice transfer matrix and not for the limiting Schwinger functions.

**Next experiments**
- List the finite reflected quadratic forms required by OS positivity for the current observable algebra.
- Ask whether Balaban-style convergence controls those forms as continuous functionals.
- Split the topology into minimal closedness demands: covariance, positivity, clustering, and distributional regularity.

- Expected learning: This tells us whether construction and reconstruction can be fused by topology, or whether OS positivity needs a different construction carrier.
- Promotion signal: A named topology plus a closure lemma for all finite reflected forms.
- Pivot signal: If closure fails, pivot from pure RG construction toward an OS-preserving lattice/Euclidean construction route.

### Gauge-Invariant Nontriviality Witness Selection

- Program: `ym-discovery-stretch.59760a63d774`
- Machinery role: `witness`
- Controlled interface: continuum gauge-invariant Schwinger functions -> non-Gaussian same-theory witness
- Hypothesis: A Wilson-loop or local curvature-composite family may serve as the nontriviality witness if one connected cumulant survives cutoff removal in the same Schwinger family used for OS reconstruction.

**Mathematical mechanism**

Make nontriviality operational: choose a gauge-invariant observable whose connected correlation rules out Gaussian/free collapse. The route should not ask for all interactions at once; it should look for one same-theory connected witness with stable normalization.

**Equations**
- connected cumulant: `\langle O_1\cdots O_k\rangle_c\ne0`
  - Valid when: The O_i are gauge-invariant observables in the same limiting Schwinger family S_n.
- Gaussian-collapse exclusion: `\exists k\ge3:\ \kappa_k(O_1,\ldots,O_k)\ne0`
  - Valid when: Higher connected cumulants are defined after the same cutoff-removal normalization.

**Dependencies**
- continuum Schwinger-function representation
- same-theory invariant
- candidate Wilson-loop or curvature-composite observable algebra

**Falsifiers**
- The witness only survives at finite cutoff.
- The chosen observable is not in the reconstructed OS algebra.
- All connected cumulants vanish under the required normalization.

**Next experiments**
- Enumerate candidate gauge-invariant observables already present in the KB and bridge packets.
- For each observable, state the lowest-order connected cumulant that would refute Gaussian collapse.
- Record whether the witness also helps observable-density or only nontriviality.

- Expected learning: This separates existence from nontrivial existence and gives the gap route a physical observable carrier.
- Promotion signal: A same-theory connected cumulant or Wilson-loop behavior with explicit cutoff normalization.
- Pivot signal: If every plausible witness degenerates, pivot to nontriviality as the lead obstruction before spectral-gap work.

### Gauge-Invariant Observable Density In The Excitation Sector

- Program: `ym-discovery-stretch.686c4b972c34`
- Machinery role: `transfer`
- Controlled interface: gauge-invariant observable algebra -> P_perp H_YM spectral determination
- Hypothesis: The decay-to-gap route becomes legitimate only if vacuum-subtracted gauge-invariant observables generate a dense subspace of the vacuum-orthogonal reconstructed Hilbert space.

**Mathematical mechanism**

Translate the physical claim 'gauge-invariant observables see the glueball spectrum' into a cyclicity/density statement after OS reconstruction. This is the hinge that prevents a decay estimate for a small visible sector from masquerading as a full mass gap.

**Equations**
- observable-generated sector: `\mathcal D_{\mathrm{ginv}}=\overline{\{(A-\langle A\rangle)\Omega:A\in\mathcal A_{\mathrm{ginv}}\}}`
  - Valid when: A_ginv is the reconstructed gauge-invariant observable algebra and Omega is the OS vacuum.
- density target: `\mathcal D_{\mathrm{ginv}}=P_\perp\mathcal H_{\mathrm{YM}}`
  - Valid when: The vacuum-orthogonal sector is the physical excitation sector relevant to the Clay mass gap.

**Dependencies**
- OS reconstruction output H_YM, Omega, H
- gauge-invariant observable algebra
- decay-to-Hamiltonian bridge lemma

**Falsifiers**
- Gauge-invariant observables generate only a proper subspace.
- Null-vector quotient removes the chosen observable carriers.
- The density theorem needs locality or additivity assumptions not supplied by the construction route.

**Next experiments**
- State the exact density theorem needed in reconstructed OS language.
- Identify whether Wilson loops/local curvature composites plausibly generate the sector.
- Make a fallback plan: if full density is too strong, isolate a physically meaningful subgap theorem and mark it as weaker.

- Expected learning: This discovers whether correlator decay can ever certify the full Hamiltonian gap or only a visible-sector gap.
- Promotion signal: A density or cyclicity lemma showing vacuum-subtracted gauge-invariant observables generate the full reconstructed excitation sector.
- Pivot signal: If density is inaccessible, pivot the gap route toward direct spectral lower bounds or clearly weaker sectoral milestones.

### Laplace-Transform Support From Uniform Euclidean Decay

- Program: `ym-discovery-stretch.4fb5879fe1ec`
- Machinery role: `witness`
- Controlled interface: Euclidean time correlation decay -> Hamiltonian spectral support exclusion
- Hypothesis: A cutoff-uniform exponential bound on connected Euclidean correlations should imply spectral-measure support away from zero for the reconstructed Hamiltonian, but only after constants, observables, and reconstruction are same-theory.

**Mathematical mechanism**

Factor the analytic core away from Yang-Mills-specific construction: prove the measure-theoretic support lemma once, then use the rest of the workflow to certify that Yang-Mills supplies its hypotheses.

**Equations**
- spectral representation: `C_A(t)=\int_0^\infty e^{-t\lambda}\,d\mu_A(\lambda)`
  - Valid when: A Omega is a reconstructed vector and Euclidean time evolution is exp(-tH).
- support exclusion: `|C_A(t)|\le C e^{-m_0t}\quad\Longrightarrow\quad \operatorname{supp}\mu_A\cap(0,m_0)=\varnothing`
  - Valid when: The bound holds for all sufficiently large t with a positive rate m0 and no cancellation hides positive spectral mass.

**Dependencies**
- OS reconstruction
- positive spectral measure
- cutoff-uniform decay estimate

**Falsifiers**
- The correlation is not represented by a positive spectral measure.
- The decay bound is asymptotic with constants that degenerate in the continuum limit.
- The observable family is not dense enough to lift support exclusion to P_perp H_YM.

**Next experiments**
- Prove the scalar spectral-measure lemma independently of Yang-Mills.
- List the exact positivity and vacuum-subtraction assumptions needed for the lemma.
- Attach the lemma as a validator for every correlator-decay route.

- Expected learning: This isolates a reusable analytic engine and makes the remaining burden visible as construction, density, and uniformity.
- Promotion signal: A self-contained proof of the spectral-support lemma together with a checklist of positivity, reconstruction, and density hypotheses supplied by Yang-Mills.
- Pivot signal: If positivity or density cannot be certified, move the route to visible-sector witness rather than full gap proof.

### Cutoff-Uniform Mass Scale Nonvanishing

- Program: `ym-discovery-stretch.0adc73050685`
- Machinery role: `validation`
- Controlled interface: regulated decay scales m_{a,L} -> positive continuum lower bound m0
- Hypothesis: The central numerical-looking but proof-critical question is whether the candidate mass scale m_{a,L} has liminf bounded below by a positive m0 during cutoff removal.

**Mathematical mechanism**

Treat the mass scale as an invariant to be transported, not as an observed parameter. The discovery task is to identify which RG, clustering, or correlation inequalities could prevent m_{a,L} from collapsing to zero.

**Equations**
- uniform lower-bound demand: `\liminf_{a\to0,L\to\infty}m_{a,L}\ge m_0>0`
  - Valid when: m_{a,L} is attached to the same observable family and limiting theory across the directed cutoff-removal net.
- forbidden collapse: `\exists(a_n,L_n):m_{a_n,L_n}\to0`
  - Valid when: The sequence remains in the construction regime claimed by the active route.

**Dependencies**
- decay-to-gap bridge
- RG continuum control
- empirical/lattice evidence requests as non-proof clues

**Falsifiers**
- All known decay estimates are strong-coupling or fixed-cutoff.
- The candidate mass scale is not defined uniformly across observables.
- Continuum limit drives the decay rate to zero.

**Next experiments**
- Search generated empirical evidence requests for quantities that suggest which scale should be tracked.
- Ask whether RG bounds can imply a clustering inequality with a uniform rate.
- Construct the no-gap reductio sequence m_{a_n,L_n}->0 and identify what it would force in Schwinger correlations.

- Expected learning: This decides whether the correlator route is alive as a Clay-target route or should be demoted to regulated evidence.
- Promotion signal: A theorem-shaped lower bound on liminf m_{a,L} for the same observable family, or a precise obstruction explaining why the scale collapses.
- Pivot signal: If m_{a,L}->0 cannot be ruled out, pivot away from correlator decay as lead proof route.

### No-Gap Reductio Low-Energy Carrier

- Program: `ym-discovery-stretch.b22cc329b82b`
- Machinery role: `obstruction`
- Controlled interface: negated Hamiltonian gap -> low-energy spectral or observable carrier
- Hypothesis: Assuming no mass gap should produce a concrete low-energy carrier: either spectral mass near zero or a sequence of vacuum-orthogonal states approximable by gauge-invariant observables.

**Mathematical mechanism**

Use proof by contradiction as a discovery microscope. The no-gap world should not remain a slogan; it must reveal whether the vulnerable hinge is observable density, uniform decay, OS reconstruction, or same-theory identity.

**Equations**
- no-gap sequence: `\forall\varepsilon>0\ \exists\psi_\varepsilon\in P_\perp\mathcal H_{\mathrm{YM}},\ \|\psi_\varepsilon\|=1,\ \langle\psi_\varepsilon,H\psi_\varepsilon\rangle<\varepsilon`
  - Valid when: H_YM, Omega, H, and P_perp are reconstructed from the same OS-positive continuum Schwinger functions.
- observable approximation pressure: `\psi_\varepsilon\approx (A_\varepsilon-\langle A_\varepsilon\rangle)\Omega`
  - Valid when: Gauge-invariant observables are dense in the vacuum-orthogonal sector.

**Dependencies**
- Hamiltonian endpoint checklist
- observable-density program
- cutoff-uniform decay program

**Falsifiers**
- Low-energy states cannot be approximated by gauge-invariant observables.
- The contradiction uses a Hamiltonian not obtained from OS reconstruction.
- No uniform decay estimate applies to the approximating observable sequence.

**Next experiments**
- Write the exact negation of the gap as a spectral projection statement.
- Try to approximate low-energy states by observable-generated vectors and record the missing theorem.
- Ask what each failure teaches: density failure, decay failure, or reconstruction failure.

- Expected learning: This converts failure to prove the gap into structured information about the missing mathematical carrier.
- Promotion signal: A contradiction target linking no-gap states to violated cutoff-uniform decay or density.
- Pivot signal: If no carrier can be made same-theory, quarantine the reductio and return to construction/reconstruction obligations.

## Next Run Queue

- `stretch-next-01` Try to prove or refute reflection-positivity closedness for the proposed cutoff-removal topology.
  - Why first: Without OS positivity, Hamiltonian and spectral language cannot be target-valid.
- `stretch-next-02` Select one concrete gauge-invariant nontriviality witness and state its connected-cumulant theorem.
  - Why first: A continuum construction that collapses to a trivial theory cannot solve the Clay target.
- `stretch-next-03` Prove the abstract Laplace-support lemma separately from Yang-Mills assumptions.
  - Why first: This isolates the analytic core of the mass-gap witness and exposes the remaining Yang-Mills-specific hypotheses.

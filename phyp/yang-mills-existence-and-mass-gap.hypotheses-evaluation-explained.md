
<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Yang--Mills Hypothesis Evaluation Explained

## Purpose

This document explains how to read the hypothesis evaluation report in [yang-mills-existence-and-mass-gap.hypotheses-evaluated.md](/Users/user/files/abducer/abducer/phyp/yang-mills-existence-and-mass-gap.hypotheses-evaluated.md). The report is not a proof checker. It is a triage layer over proof hypotheses generated from the Yang--Mills knowledge base. Its job is to decide which hypotheses are currently well-grounded in the KB, which ones remain plausible but underdetermined, and which ones should be deprioritized or refuted.

The central point is this:

- `supported` means the framework currently sees enough structural and coherence-based evidence to keep the hypothesis in the active frontier
- `inconclusive` means the hypothesis is still live, but the present KB does not yet justify promoting it
- `refuted` would mean the framework found sufficiently strong structural conflict or explicit negative evidence

In this run there are no `refuted` hypotheses. That matters. The system is not saying that most proposals are bad. It is saying that most proposals are not yet sharp enough, evidenced enough, or deductively connected enough to the current Yang--Mills KB.

## What Was Evaluated

- Total hypotheses: `44`
- Direct bridge hypotheses: `001` to `020`
- Intervention-focus hypotheses: `021` to `032`
- Higher-order conceptual hypotheses: `033` to `044`

These are three different inferential roles.

- `bridge-link`: a direct proposed connection from one statement to another
- `intervention-focus`: a claim that a particular statement is a high-value place to concentrate reasoning effort
- `representation-shift` / `intermediate-invariant` / `definition-introduction`: higher-order conceptual moves that reorganize the proof search space rather than asserting a single direct theorem jump

This distinction is essential for interpreting the result. The strongest results in this run are mostly not direct theorem-to-theorem bridges. They are conceptual restructurings.

## How The Evaluator Decides

The evaluator combines four layers of evidence.

### 1. Structural support

For bridge and conceptual hypotheses, the evaluator looks at:

- typed similarity between source and target statement structure
- symbol-role alignment
- theorem-family similarity
- connector analysis score
- whether the target already depends on the source
- whether the proposal loops back on itself
- whether there are contradiction markers

This is implemented in [hypothesis_eval.py](/Users/user/files/abducer/abducer/skills/common/hypothesis_eval.py:755) and [hypothesis_eval.py](/Users/user/files/abducer/abducer/skills/common/hypothesis_eval.py:969).

### 2. Inferential commitment grounding

Each non-intervention hypothesis can carry four explicit commitments:

- antecedent schema
- target consequence schema
- preserved invariant
- barrier scope

The evaluator asks whether those commitments are actually visible in the structured content of the source and target statements. This is why the report contains alignment signals such as:

- `antecedent_alignment`
- `consequence_alignment`
- `invariant_alignment`
- `barrier_alignment`

This matters because the framework is trying to reason mathematically, not just lexically. A hypothesis is stronger when it states a concrete inferential interface and that interface is visible in the KB statements themselves.

### 3. External evidence adjustments

Optional deductive, abductive, contradiction, or experimental signals can adjust support or refutation. The logic is in [hypothesis_eval.py](/Users/user/files/abducer/abducer/skills/common/hypothesis_eval.py:620).

For example:

- a deductive entailment can increase support
- a failed derivation can increase refutation
- an explicit contradiction can strongly increase refutation

In this Yang--Mills run, the results are driven mainly by structural and coherence signals, not by hard deductive discharge.

### 4. Coherence adjustments

Each hypothesis also receives a local coherence readout against the current theory graph. This is why the report lists:

- `Coherence signals: 44`
- `Global coherence baseline: 0.320043`

The baseline is the current global coherence score of the KB before accepting any specific hypothesis. Each hypothesis is then evaluated against that background. This does not yet mean the system has found a globally optimized theory. It means each hypothesis is judged partly by whether it improves or destabilizes the current web of claims.

## How Verdicts Are Assigned

The decision rule is explicit in [hypothesis_eval.py](/Users/user/files/abducer/abducer/skills/common/hypothesis_eval.py:662).

- `supported` requires:
  - `support >= 0.62`
  - and `support - refute >= 0.08`
- `refuted` would require:
  - `refute >= 0.62`
  - and `refute - support >= 0.08`
- otherwise the result is `inconclusive`

For this run:

- support threshold = `0.62`
- refute threshold = `0.62`
- margin = `0.08`
- force resolution = `False`

`force resolution = False` is important. It means the evaluator is allowed to leave a hypothesis unresolved. It does not have to pretend every hypothesis is either accepted or rejected.

## What Confidence Means

`confidence` is not the same thing as `support`.

It is computed from:

- the stronger of the support/refute scores
- multiplied by a factor that rewards separation between them

The formula is in [hypothesis_eval.py](/Users/user/files/abducer/abducer/skills/common/hypothesis_eval.py:854), [hypothesis_eval.py](/Users/user/files/abducer/abducer/skills/common/hypothesis_eval.py:1019), and [hypothesis_eval.py](/Users/user/files/abducer/abducer/skills/common/hypothesis_eval.py:1170).

Interpretation:

- high `support` with low `refute` gives higher confidence
- moderate `support` with moderate `refute` can still be `supported`, but with lower confidence

That is why `phyp.yang-mills-existence-and-mass-gap.040` is `supported` even though its confidence is only `0.4823`: its support clears threshold and its margin over refute is large enough, but the absolute strength is still moderate.

## What the Summary Means

### Stats

- `44` hypotheses were evaluated
- `44` coherence signals means every hypothesis had a coherence row
- global coherence baseline `0.320043` means the current KB is only moderately integrated; the framework is still working inside a partially coherent theory graph

### Verdict counts

- `12 supported`
- `32 inconclusive`
- `0 refuted`

This pattern has a clear interpretation:

- the framework found several promising conceptual reorganizations
- it did not yet find enough grounded direct bridges to turn those reorganizations into a strong proof path
- it also did not find decisive negative evidence against most of the frontier

So the current Yang--Mills state is exploratory but not collapsed.

## How To Read The Three Hypothesis Classes

## Intervention-Focus Hypotheses (`021` to `032`)

These do not propose a theorem bridge. They propose where attention should go next.

Examples:

- `021`: focus on `st.def.os-euclidean-qft`
- `022`: focus on `st.def.mass-gap`
- `023`: focus on `st.thm.euclidean-correlator-decay-as-a-mass-gap-signatu`

Their alignment signals are all zero in the mathematical readout. That is expected. Intervention hypotheses do not carry explicit antecedent, consequence, invariant, or barrier commitments in the same way bridge hypotheses do. They are scored mostly from:

- inherited priority
- cross-component potential
- downstream impact
- betweenness and dependency pressure

This logic is in [hypothesis_eval.py](/Users/user/files/abducer/abducer/skills/common/hypothesis_eval.py:1079).

Interpretation of their current outcome:

- they are plausible focal points
- they are not yet strong enough to be promoted as decisive intervention commitments
- they should guide the next reasoning round rather than be treated as mathematical conclusions

## Direct Bridge Hypotheses (`001` to `020`)

These are the most literal bridging proposals. They connect one KB statement to another and state an intended invariant.

Examples:

- `001`: from `st.def.os-euclidean-qft` toward OS reconstruction and Wightman equivalence, preserving `OS-to-Wightman mass-gap transfer in Hamiltonian-mass-gap`
- `003`: from `st.def.os-euclidean-qft` toward Euclidean correlator decay as a mass-gap signature, preserving `correlator-decay mass-gap witness in Schwinger-function-decay`
- `006`: from `st.def.mass-gap`-adjacent transfer-matrix structure toward correlator decay, preserving `transfer-matrix spectral witness in reflection-positive-transfer-matrix`

These hypotheses are mostly `inconclusive`.

That does not mean they are wrong. It means the framework sees real structure but not enough decisive grounding.

Typical reasons:

- good invariant alignment but weak consequence alignment
- good semantic overlap but barrier scope not yet grounded
- connector score present but not strong enough to clear support threshold
- bridge is mathematically plausible but still too under-specified relative to the current KB

Example:

- `001` has:
  - antecedent alignment `0.3869`
  - invariant alignment `0.5114`
  - consequence alignment `0.0000`
  - support `0.4709`
  - refute `0.0540`

This says:

- the source really does look like an OS/reconstruction antecedent
- the proposed invariant is visible across source and target
- but the target consequence `positive-self-adjoint-Hamiltonian` is not yet grounded strongly enough in the target statement structure

So the bridge is mathematically suggestive but not yet inferentially tight.

## Higher-Order Conceptual Hypotheses (`033` to `044`)

These are the strongest part of the current run. All `12` supported hypotheses are in this class.

This is the central result of the report.

The framework is saying that, for this Yang--Mills KB, the best current progress is not a direct proof bridge. It is a conceptual reframing of the proof search space.

The supported hypotheses split into three families.

## Supported Family A: Representation Shift

Supported hypotheses:

- `033`
- `036`
- `037`
- `041`
- `043`

These propose that the right reasoning move is to shift representation between:

- OS Euclidean data
- Wightman axiomatic structure
- Hamiltonian/spectral formulations
- constructive QFT examples
- rigorous renormalization group programs

Interpretation:

- the framework sees the Euclidean-to-Wightman/Hamiltonian interface as a structurally coherent route
- it prefers proof search that moves through representation changes instead of trying to jump directly from geometric or gauge-theoretic statements to the Clay conclusion

The strongest single supported hypothesis is:

- `041`
  - support `0.7829`
  - refute `0.0216`
  - confidence `0.6988`

`041` is a representation shift from `st.def.os-euclidean-qft` to the more explicit OS definition statement. This is significant because the system is effectively saying:

- before pushing further, stabilize the exact OS formulation
- then use that stabilization as the anchor for the mass-gap route

This is not yet a proof of a mass gap. It is a diagnosis that definitional precision at the OS level is one of the strongest currently supported moves.

## Supported Family B: Intermediate Invariant

Supported hypotheses:

- `034`
- `035`
- `038`
- `044`

These propose that the proof search should be mediated by explicitly preserved middle objects, especially:

- correlator-decay mass-gap witnesses
- transfer-matrix spectral witnesses
- mass-gap witness transfer in compact simple gauge group settings

Interpretation:

- the framework does not trust a raw statement-to-statement jump
- it wants an invariant that survives translation between formulations

This is mathematically appropriate. In hard existence-and-gap problems, a preserved witness or invariant is usually what makes a bridge usable.

The two most important invariant families here are:

- `correlator-decay -> gap`
- `transfer-matrix -> spectral gap`

These are supported because the Yang--Mills KB already contains the right structural ingredients:

- OS positivity
- reflection positivity
- transfer-matrix language
- exponential decay language
- Hamiltonian gap language

So the evaluator is identifying a meaningful inferential spine:

- prove or control the right decay witness
- transfer that witness through reflection positivity / transfer matrix structure
- interpret it as a Hamiltonian gap signal

## Supported Family C: Definition Introduction

Supported hypotheses:

- `039`
- `040`
- `042`

These are geometric/gauge-theoretic conceptual moves from the compact simple gauge group definition toward:

- ADHM instanton classification
- Uhlenbeck gauge fixing and compactness
- BPST instanton existence

Interpretation:

- the system sees these as legitimate concept-building moves
- but it treats them as preparatory structure, not as direct mass-gap resolution

This is the right reading. These statements provide geometric control, local compactness, or model constructions. They matter because they enrich the ontology of Yang--Mills objects. But they are not yet by themselves a route to the positive mass gap in four-dimensional quantum Yang--Mills.

So these are supported as concept-building steps, not as decisive closure steps.

## What The Report Is Really Saying About Yang--Mills

The report points to a fairly specific mathematical diagnosis.

### 1. The current KB supports conceptual transport better than direct proof transport

The evaluator supports:

- representation shifts
- invariant introduction
- definition sharpening

It does not yet support most direct bridge links.

This means the KB is rich enough to describe the right proof ecology, but not yet rich enough to discharge the main proof obligations.

### 2. The most promising mass-gap route currently runs through the Euclidean/OS/Wightman/spectral interface

The strongest supported cluster is centered on:

- OS Euclidean QFT
- OS reconstruction
- Wightman realization
- transfer-matrix and reflection positivity
- correlator decay as a signature of spectral gap

That is a coherent mathematical route. It says the framework currently believes the best entry into the Clay problem is not through instantons alone, nor through gauge-fixing alone, but through the problem of transporting a gap witness across formulations.

### 3. The main blockers remain continuum and ultraviolet issues

Several of the better bridge proposals are barrier-scoped by:

- `continuum-limit`
- `ultraviolet-control`
- `open-construction-gap`

This is exactly what one should expect. The lattice or Euclidean objects can give partial witness structure, but the unresolved problem is whether that structure survives the full continuum construction in four dimensions.

### 4. Geometry is present, but not yet integrated into the mass-gap mechanism

The supported geometric hypotheses are mostly:

- ADHM
- BPST instantons
- Uhlenbeck compactness
- Donaldson-style moduli control

These are mathematically important, but the report is implicitly saying:

- geometry is currently contributing ontology and structural control
- not yet a precise spectral-gap mechanism

So the geometry side of the KB needs better coupling to the mass-gap witness side.

## Why So Many Hypotheses Are Inconclusive

There are three main reasons.

### 1. The KB still contains more conceptual adjacency than proof obligation data

Many hypotheses are plausible because the statements live in the same conceptual neighborhood. But plausibility is not enough. The evaluator wants:

- explicit consequence grounding
- explicit invariant grounding
- visible barrier handling

When one of those is missing, support tends to stay in the `0.43` to `0.53` range instead of crossing `0.62`.

### 2. Direct bridges are harder than conceptual reframings

A representation shift only needs to show that one formulation can organize another in a productive way.

A direct bridge-link has to show more:

- why this exact support statement helps this exact target statement
- what is preserved
- why that preservation survives the stated barriers

That is a much harder demand, and the current KB often does not yet encode enough detail for it.

### 3. The Yang--Mills problem is hard in exactly the places the report highlights

The pattern of inconclusiveness is not a defect of the evaluator alone. It reflects the mathematical problem:

- how to construct the full continuum theory
- how to prove a positive mass gap in the physically relevant setting
- how to connect Euclidean, Hamiltonian, spectral, and constructive viewpoints without losing the witness

That is precisely where the hypotheses stall.

## How To Read Individual Fields In The Mathematical Readout

### Antecedent schema

This is the type of input condition the hypothesis claims to rely on.

Examples:

- `reflection-positivity-and-transfer-matrix`
- `constructive-existence`
- `unconditional`

If antecedent alignment is high, the source statement genuinely looks like the kind of statement the hypothesis says it needs.

### Target consequence

This is the type of mathematical outcome the hypothesis claims to move toward.

Examples:

- `positive-self-adjoint-Hamiltonian`
- `rigorous-Yang-Mills-construction`
- `moduli-space-control`

If consequence alignment is low or zero, that usually means the target statement does not yet explicitly encode that consequence strongly enough.

### Preserved invariant

This is the most important field in many of the supported hypotheses.

Examples:

- `OS-to-Wightman mass-gap transfer in Hamiltonian-mass-gap`
- `correlator-decay mass-gap witness in Schwinger-function-decay`
- `transfer-matrix spectral witness in reflection-positive-transfer-matrix`

This field says what must survive the bridge if the bridge is to have mathematical value.

### Barrier scope

This names what kind of obstruction the move is expected to face.

Examples:

- `continuum-limit`
- `ultraviolet-control`
- `gauge-control`
- `open-construction-gap + quantum-measure-construction`

A bridge with a realistic barrier scope is often better than a bridge with no barriers named, because it is more mathematically honest. But it can also be harder to support if the KB does not yet encode barrier-handling details.

## Recommended Reading Of The Supported Hypotheses

If the goal is to use the current output as a research steering document, the hypotheses should be read in this order.

### Tier 1: Core mass-gap interface

- `041`
- `033`
- `037`
- `035`
- `038`
- `044`

These are the most informative hypotheses for the central problem because they organize the interface between:

- OS formulation
- Wightman/Hamiltonian realization
- correlator decay
- transfer matrix
- spectral gap witness

### Tier 2: Construction-oriented transfer

- `036`
- `043`

These say that constructive QFT examples and Balaban-style RG analysis are valuable as representation-shift anchors, but they remain barrier-loaded and do not yet close the four-dimensional problem.

### Tier 3: Geometric ontology enrichment

- `034`
- `039`
- `040`
- `042`

These are useful for concept formation and structural control, but they are secondary unless they are connected more explicitly to a mass-gap witness mechanism.

## What To Do Next

The report itself already suggests the next action:

- `promote-or-retest-with-deduction` for supported hypotheses
- `run-another-abduce-deduce-round` for inconclusive hypotheses

For the Yang--Mills KB, the right next moves are:

- strengthen the OS/reconstruction/Wightman statements with more explicit spectral-gap obligations
- encode more explicit transfer principles from correlator decay to Hamiltonian gap
- connect geometric control statements to the mass-gap witness layer instead of leaving them as parallel concept clusters
- add sharper continuum-limit and ultraviolet-control statements so barrier alignment is no longer mostly implicit

## Bottom Line

This evaluation does not yet identify a completed Yang--Mills proof pathway.

It does identify something more precise than a vague frontier:

- the current best-supported discovery path is conceptual and representational
- the strongest bridge objects are invariant-like witnesses, not direct theorem jumps
- the Euclidean/OS/Wightman/transfer-matrix/correlator-decay chain is the main supported inferential spine
- the geometry/moduli/instanton side is useful, but still insufficiently coupled to the actual mass-gap mechanism

So the correct reading is:

- the framework has begun to isolate the right kinds of mathematical objects and interfaces
- it has not yet resolved the core proof obligations that would turn those interfaces into a proof


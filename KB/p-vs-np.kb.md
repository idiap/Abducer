---
kb_id: p-vs-np
title: P vs NP
domain: mathematics
subdomain: computational-complexity
version: 0.1.0
status: active
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
| src.001 | file | /Users/user/Downloads/deep-research-report.md | full document | high | Parsed via pvsnp-kb-parser |
| src.complexity.kozen2006 | package | complexity_theory_kb.zip | kb.jsonl source_id=kozen2006 | high | Curated complexity-theory KB package; imported with entry-level provenance. |
| src.complexity.np-ch2 | package | complexity_theory_kb.zip | kb.jsonl source_id=np_ch2 | high | Curated NP chapter extraction in complexity-theory KB package; imported with entry-level provenance. |

# Symbol Glossary

- `sym.P`: `\Pclass` complexity class.
- `sym.NP`: `\NP` complexity class.
- `sym.Ppoly`: `\Ppoly` nonuniform class.

# Canonical Statements

```yaml
id: st.def.polynomial-time-many-one-karp-reduction
kind: definition
status: accepted
latex: For languages $A,B\subseteq\bits^*$, we write $A\leq_m^p B$ iff there exists a polynomial-time computable function $f:\bits^*\to\bits^*$ such that for all $x$, $x\in A \iff f(x)\in B$.
informal: For languages A,Bsubseteqbits^* , we write Aleq_m^p B iff there exists a polynomial-time computable function f:bits^*tobits^* such that for all x , xin A iff f(x)in B .
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Core reductions and complexity classes.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Polynomial-time many-one (Karp) reduction\nsource_marker: \uE200cite\uE202turn23search0\uE202turn31search0\uE201"
```

```yaml
id: st.def.item
kind: definition
status: accepted
latex: A language $L$ is in $\Pclass$ iff there exists a deterministic Turing machine $M$ and a polynomial $p$ such that for all inputs $x$, $M$ decides whether $x\in L$ in time at most $p(|x|)$.
informal: A language L is in Pclass iff there exists a deterministic Turing machine M and a polynomial p such that for all inputs x , M decides whether xin L in time at most p(|x|) .
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Core reductions and complexity classes.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: $\\Pclass$\nsource_marker: \uE200cite\uE202turn23search0\uE201"
```

```yaml
id: st.def.item-2
kind: definition
status: accepted
latex: 'A language $L$ is in $\NP$ iff there exist a polynomial $p$ and a polynomial-time predicate (verifier) $V(x,w)$ such that

  \[

  x\in L \iff \exists w\in\bits^{p(|x|)} \ \ V(x,w)=1.

  \]'
informal: A language L is in NP iff there exist a polynomial p and a polynomial-time predicate (verifier) V(x,w) such that [ xin L iff exists winbits^ p(|x|) V(x,w)=1. ]
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Core reductions and complexity classes.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: $\\NP$\nsource_marker: \uE200cite\uE202turn23search0\uE201"
```

```yaml
id: st.def.item-3
kind: definition
status: accepted
latex: '$\coNP=\{L\subseteq\bits^* : \overline{L}\in\NP\}$, where $\overline{L}=\bits^*\setminus L$.'
informal: 'coNP= Lsubseteqbits^* : overline L inNP , where overline L =bits^*setminus L .'
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Core reductions and complexity classes.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: $\\coNP$\nsource_marker: \uE200cite\uE202turn23search0\uE202turn19search0\uE201"
```

```yaml
id: st.def.np-completeness
kind: definition
status: accepted
latex: A language $L$ is \emph{NP-complete} (under $\le_m^p$) iff (i) $L\in\NP$ and (ii) for every $A\in\NP$, $A\le_m^p L$.
informal: A language L is emph NP-complete (under le_m^p ) iff (i) LinNP and (ii) for every AinNP , Ale_m^p L .
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Core reductions and complexity classes.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: NP-completeness\nsource_marker: \uE200cite\uE202turn30search0\uE202turn31search0\uE201"
```

```yaml
id: st.def.polynomial-hierarchy
kind: definition
status: accepted
latex: Let $\Sigma_0^p=\Pi_0^p=\Pclass$ and $\Sigma_{k+1}^p=\NP^{\Sigma_k^p}$, $\Pi_{k+1}^p=\coNP^{\Sigma_k^p}$. Then $\PH=\bigcup_{k\ge 0}\Sigma_k^p$.
informal: Let Sigma_0^p=Pi_0^p=Pclass and Sigma_ k+1 ^p=NP^ Sigma_k^p , Pi_ k+1 ^p=coNP^ Sigma_k^p . Then PH=bigcup_ kge 0 Sigma_k^p .
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Core reductions and complexity classes.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Polynomial hierarchy\nsource_marker: \uE200cite\uE202turn23search0\uE201"
```

```yaml
id: st.def.exponential-time-classes
kind: definition
status: accepted
latex: $\E=\DTIME(2^{O(n)})$, $\EXP=\DTIME(2^{n^{O(1)}})$, $\NEXP=\NTIME(2^{n^{O(1)}})$.
informal: E=DTIME(2^ O(n) ) , EXP=DTIME(2^ n^ O(1) ) , NEXP=NTIME(2^ n^ O(1) ) .
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Core reductions and complexity classes.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Exponential time classes\nsource_marker: \uE200cite\uE202turn23search0\uE202turn22search9\uE201"
```

```yaml
id: st.def.item-4
kind: definition
status: accepted
latex: 'A language $L$ is in $\BPP$ iff there exists a probabilistic polynomial-time Turing machine $M$ such that for all $x$:

  \[

  x\in L \Rightarrow \Pr[M(x)\ \text{accepts}]\ge 2/3,\quad

  x\notin L \Rightarrow \Pr[M(x)\ \text{accepts}]\le 1/3.

  \]'
informal: 'A language L is in BPP iff there exists a probabilistic polynomial-time Turing machine M such that for all x : [ xin L Rightarrow Pr[M(x) text accepts ]ge 2/3,quad xnotin L Rightarrow Pr[M(x) text accepts ]le 1/3. ]'
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Core reductions and complexity classes.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: $\\BPP$\nsource_marker: \uE200cite\uE202turn23search0\uE202turn23search1\uE201"
```

```yaml
id: st.def.boolean-circuit-and-size-depth
kind: definition
status: accepted
latex: A Boolean circuit on $n$ inputs is a directed acyclic graph with $n$ input nodes labeled $x_1,\dots,x_n$, internal gates from a basis (e.g.\ $\{\wedge,\vee,\neg\}$), and one output gate. The \emph{size} is the number of gates (or wires; the convention must be fixed). The \emph{depth} is the length (number of gates) on the longest input-to-output path.
informal: A Boolean circuit on n inputs is a directed acyclic graph with n input nodes labeled x_1,dots,x_n , internal gates from a basis (e.g. wedge,vee,neg ), and one output gate. The emph size is the number of gates (or wires; the convention must be fixed). The emph depth is the leng...
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Boolean circuits and nonuniform classes.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Boolean circuit and (size, depth)\nsource_marker: \uE200cite\uE202turn23search0\uE202turn23search3\uE201"
```

```yaml
id: st.def.circuit-family-s-n
kind: definition
status: accepted
latex: A circuit family $\{C_n\}_{n\ge 1}$ is a sequence where $C_n$ is a circuit on $n$ inputs. A language $L$ is in $\SIZE(s(n))$ if there exists a family $\{C_n\}$ of size $\le s(n)$ such that $C_n(x)=1 \iff x\in L$ for all $|x|=n$.
informal: A circuit family C_n _ nge 1 is a sequence where C_n is a circuit on n inputs. A language L is in SIZE(s(n)) if there exists a family C_n of size le s(n) such that C_n(x)=1 iff xin L for all |x|=n .
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Boolean circuits and nonuniform classes.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Circuit family; $\\SIZE(s(n))$\nsource_marker: \uE200cite\uE202turn23search0\uE202turn22search2\uE201"
```

```yaml
id: st.def.item-5
kind: definition
status: accepted
latex: $\Ppoly$ is the class of languages $L$ decidable by polynomial-size Boolean circuit families, equivalently by polynomial-time Turing machines with polynomial-length advice strings depending only on input length.
informal: Ppoly is the class of languages L decidable by polynomial-size Boolean circuit families, equivalently by polynomial-time Turing machines with polynomial-length advice strings depending only on input length.
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Boolean circuits and nonuniform classes.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: $\\Ppoly$\nsource_marker: \uE200cite\uE202turn23search0\uE202turn9search16\uE202turn5search17\uE201"
```

```yaml
id: st.def.boolean-formulas
kind: definition
status: accepted
latex: A Boolean formula is a Boolean circuit whose underlying graph is a tree (fan-out $1$). The \emph{formula size} is the number of gates.
informal: A Boolean formula is a Boolean circuit whose underlying graph is a tree (fan-out 1 ). The emph formula size is the number of gates.
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Boolean circuits and nonuniform classes.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Boolean formulas\nsource_marker: \uE200cite\uE202turn23search0\uE202turn16search1\uE201"
```

```yaml
id: st.def.standard-restricted-circuit-classes
kind: definition
status: accepted
latex: 'Let gates have unbounded fan-in unless stated otherwise.

  \begin{enumerate}[label=(\alph*),leftmargin=2em]

  \item $\NC^1$: polynomial size, logarithmic depth, bounded fan-in $\{\wedge,\vee,\neg\}$.

  \item $\AC^0$: polynomial size, constant depth, unbounded fan-in $\{\wedge,\vee,\neg\}$.

  \item $\AC^0[p]$: $\AC^0$ plus $\mathrm{MOD}_p$ gates (typically $p$ prime).

  \item $\ACC^0$: $\AC^0$ plus $\mathrm{MOD}_m$ gates for constant $m>1$.

  \item $\TC^0$: constant depth, polynomial size circuits with threshold/majority gates.

  \end{enumerate}'
informal: 'Let gates have unbounded fan-in unless stated otherwise. [label=(alph*),leftmargin=2em] item NC^1 : polynomial size, logarithmic depth, bounded fan-in wedge,vee,neg . item AC^0 : polynomial size, constant depth, unbounded fan-in wedge,vee,neg . item AC^0[p] : AC^0 plus mathrm...'
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Boolean circuits and nonuniform classes.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Standard restricted circuit classes\nsource_marker: \uE200cite\uE202turn23search0\uE202turn1search7\uE202turn22search9\uE201"
```

```yaml
id: st.def.monotone-circuits
kind: definition
status: accepted
latex: A monotone circuit is a circuit over $\{\wedge,\vee\}$ (no negation gates) computing a monotone Boolean function. Its complexity is measured by size/depth as usual.
informal: A monotone circuit is a circuit over wedge,vee (no negation gates) computing a monotone Boolean function. Its complexity is measured by size/depth as usual.
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Boolean circuits and nonuniform classes.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Monotone circuits\nsource_marker: \uE200cite\uE202turn23search0\uE202turn19search6\uE201"
```

```yaml
id: st.def.cook-reckhow-propositional-proof-system
kind: definition
status: accepted
latex: 'A (Cook--Reckhow) propositional proof system is a polynomial-time computable surjection

  \[

  f:\bits^*\twoheadrightarrow \TAUT,

  \]

  where $\TAUT$ is the set of propositional tautologies. A string $\pi$ is an $f$-proof of formula $\varphi$ if $f(\pi)=\varphi$.'
informal: A (Cook--Reckhow) propositional proof system is a polynomial-time computable surjection [ f:bits^*twoheadrightarrow TAUT, ] where TAUT is the set of propositional tautologies. A string pi is an f -proof of formula varphi if f(pi)=varphi .
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Proof complexity.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Cook--Reckhow propositional proof system\nsource_marker: \uE200cite\uE202turn19search0\uE201"
```

```yaml
id: st.def.polynomially-bounded-proof-system
kind: definition
status: accepted
latex: A proof system $f$ is \emph{polynomially bounded} if there exists a polynomial $p$ such that every $\varphi\in\TAUT$ has an $f$-proof $\pi$ with $|\pi|\le p(|\varphi|)$.
informal: A proof system f is emph polynomially bounded if there exists a polynomial p such that every varphiinTAUT has an f -proof pi with |pi|le p(|varphi|) .
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Proof complexity.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Polynomially bounded proof system\nsource_marker: \uE200cite\uE202turn19search0\uE202turn19search4\uE201"
```

```yaml
id: st.def.resolution-refutation
kind: definition
status: accepted
latex: Resolution is a refutation system for CNF formulas, with inference rule $(A\vee x),(B\vee \neg x)\mapsto (A\vee B)$. A CNF is unsatisfiable iff it has a resolution refutation.
informal: Resolution is a refutation system for CNF formulas, with inference rule (Avee x),(Bvee neg x)mapsto (Avee B) . A CNF is unsatisfiable iff it has a resolution refutation.
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Proof complexity.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Resolution (refutation)\nsource_marker: \uE200cite\uE202turn19search1\uE201"
```

```yaml
id: st.def.frege-and-extended-frege-informal
kind: definition
status: accepted
latex: Frege systems are propositional calculi with finitely many axiom schemes and inference rules; Extended Frege adds extension axioms allowing abbreviations. Proof size is measured by number of symbols/lines.
informal: Frege systems are propositional calculi with finitely many axiom schemes and inference rules; Extended Frege adds extension axioms allowing abbreviations. Proof size is measured by number of symbols/lines.
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Proof complexity.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Frege and Extended Frege (informal)\nsource_marker: \uE200cite\uE202turn19search7\uE202turn19search3\uE201"
```

```yaml
id: st.def.ideal-proof-system-ips-high-level
kind: definition
status: accepted
latex: Given polynomials $F_1(\mathbf{x}),\dots,F_m(\mathbf{x})$ over a field with no common zero over the algebraic closure, an IPS refutation is an algebraic circuit $C(\mathbf{x},\mathbf{y})$ such that $C(\mathbf{x},\mathbf{0})\equiv 0$ and $C(\mathbf{x},F_1(\mathbf{x}),\dots,F_m(\mathbf{x}))\equiv 1$. IPS size is the circuit size of $C$.
informal: Given polynomials F_1(mathbf x ),dots,F_m(mathbf x ) over a field with no common zero over the algebraic closure, an IPS refutation is an algebraic circuit C(mathbf x ,mathbf y ) such that C(mathbf x ,mathbf 0 )equiv 0 and C(mathbf x ,F_1(mathbf x ),dots,F_m(mathbf x ))equiv 1...
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Proof complexity.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Ideal Proof System (IPS) --- high-level\nsource_marker: \uE200cite\uE202turn19search6\uE201"
```

```yaml
id: st.def.polynomial-identity-testing-pit
kind: definition
status: accepted
latex: Given an arithmetic circuit $C$ over a field/ring, the PIT problem asks whether the polynomial computed by $C$ is identically zero (i.e.\ $C\equiv 0$).
informal: Given an arithmetic circuit C over a field/ring, the PIT problem asks whether the polynomial computed by C is identically zero (i.e. Cequiv 0 ).
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Derandomisation, PIT, and pseudorandomness.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Polynomial Identity Testing (PIT)\nsource_marker: \uE200cite\uE202turn32search4\uE202turn19search6\uE201"
```

```yaml
id: st.def.hitting-set-for-pit-black-box
kind: definition
status: accepted
latex: A set $H\subseteq \mathbb{F}^n$ is a hitting set for a class $\mathcal{C}$ of $n$-variate circuits if for every nonzero polynomial $p$ computed by some circuit in $\mathcal{C}$, there exists $\mathbf{a}\in H$ with $p(\mathbf{a})\neq 0$.
informal: A set Hsubseteq mathbb F ^n is a hitting set for a class mathcal C of n -variate circuits if for every nonzero polynomial p computed by some circuit in mathcal C , there exists mathbf a in H with p(mathbf a )neq 0 .
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Derandomisation, PIT, and pseudorandomness.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Hitting set for PIT (black-box)\nsource_marker: \uE200cite\uE202turn32search4\uE201"
```

```yaml
id: st.def.pseudorandom-generator-prg-against-circuits
kind: definition
status: accepted
latex: 'A function $G:\bits^s\to\bits^m$ is a PRG against circuit class $\mathcal{C}$ with advantage $\varepsilon$ if for all distinguishers $D\in\mathcal{C}$,

  \[

  \left|\Pr[D(G(U_s))=1]-\Pr[D(U_m)=1]\right|\le \varepsilon.

  \]'
informal: A function G:bits^stobits^m is a PRG against circuit class mathcal C with advantage varepsilon if for all distinguishers Dinmathcal C , [ left|Pr[D(G(U_s))=1]-Pr[D(U_m)=1]right|le varepsilon. ]
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Derandomisation, PIT, and pseudorandomness.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Pseudorandom generator (PRG) against circuits\nsource_marker: \uE200cite\uE202turn23search1\uE202turn4view2\uE201"
```

```yaml
id: st.def.pseudorandom-function-prf-informal
kind: definition
status: accepted
latex: A keyed family $\{f_k:\bits^n\to\bits\}$ is a PRF if no polynomial-size circuit family can distinguish oracle access to $f_k$ (for uniform random key $k$) from oracle access to a uniformly random function. Precise definitions vary by model; see standard cryptography references.
informal: A keyed family f_k:bits^ntobits is a PRF if no polynomial-size circuit family can distinguish oracle access to f_k (for uniform random key k ) from oracle access to a uniformly random function. Precise definitions vary by model; see standard cryptography references.
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Derandomisation, PIT, and pseudorandomness.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Pseudorandom function (PRF) --- informal\nsource_marker: \uE200cite\uE202turn4view2\uE201"
```

```yaml
id: st.def.minimum-circuit-size-problem-mcsp
kind: definition
status: accepted
latex: 'Instance: a truth table $T\in\bits^{2^n}$ of an $n$-bit Boolean function $f$, and a size parameter $s$. Question: does $f$ have a Boolean circuit of size at most $s$? The input length is $N=2^n$, so $s$ is typically specified as a function of $n$ (or $N$).'
informal: 'Instance: a truth table Tinbits^ 2^n of an n -bit Boolean function f , and a size parameter s . Question: does f have a Boolean circuit of size at most s ? The input length is N=2^n , so s is typically specified as a function of n (or N ).'
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Meta-complexity and hardness magnification.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Minimum Circuit Size Problem (MCSP)\nsource_marker: \uE200cite\uE202turn18search4\uE202turn28search5\uE201"
```

```yaml
id: st.def.gap-mcsp
kind: definition
status: accepted
latex: 'Given thresholds $s_1<s_2$, $\mathrm{GapMCSP}[s_1,s_2]$ is a promise problem: YES if $\CIRCSIZE(f)\le s_1$, NO if $\CIRCSIZE(f)\ge s_2$.'
informal: 'Given thresholds s_1<s_2 , mathrm GapMCSP [s_1,s_2] is a promise problem: YES if CIRCSIZE(f)le s_1 , NO if CIRCSIZE(f)ge s_2 .'
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Meta-complexity and hardness magnification.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Gap-MCSP\nsource_marker: \uE200cite\uE202turn16search1\uE202turn16search2\uE201"
```

```yaml
id: st.def.mktp-mktp-time-bounded-kolmogorov-meta-problem
kind: definition
status: accepted
latex: Given a string $x$ and threshold $\theta$, decide whether the time-bounded Kolmogorov complexity $KT(x)\le \theta$ (Levin's $KT$ measure). Variants differ in the exact model of time-bounded description.
informal: Given a string x and threshold theta , decide whether the time-bounded Kolmogorov complexity KT(x)le theta (Levin's KT measure). Variants differ in the exact model of time-bounded description.
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Meta-complexity and hardness magnification.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: MKTP / MKtP (time-bounded Kolmogorov meta-problem)\nsource_marker: \uE200cite\uE202turn17search15\uE202turn18search2\uE201"
```

```yaml
id: st.def.hardness-magnification-phenomenon-programme-leve
kind: definition
status: accepted
latex: "A hardness magnification theorem has the form:\n\\[\n\\text{\u201CA barely-nontrivial lower bound for an explicit problem }Q\\text{ in a weak model } \\Rightarrow \\text{ a major lower bound/separation in a strong model.\u201D}\n\\]\nTypically, $Q$ is a meta-problem (e.g.\\ a Gap-MCSP variant) and \u201Cmajor\u201D means consequences such as $\\NP\\not\\subseteq \\Ppoly$."
informal: "A hardness magnification theorem has the form: [ text \u201CA barely-nontrivial lower bound for an explicit problem Qtext in a weak model Rightarrow text a major lower bound/separation in a strong model.\u201D ] Typically, Q is a meta-problem (e.g. a Gap-MCSP variant) and \u201Cmajor\u201D means..."
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Meta-complexity and hardness magnification.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Hardness magnification (phenomenon; programme-level)\nsource_marker: \uE200cite\uE202turn16search3\uE202turn16search1\uE202turn16search2\uE201"
```

```yaml
id: st.def.deterministic-communication-complexity
kind: definition
status: accepted
latex: For a two-party Boolean function $F:\mathcal{X}\times\mathcal{Y}\to\bits$, $D^{cc}(F)$ is the minimum number of communicated bits in a deterministic protocol that computes $F$.
informal: For a two-party Boolean function F:mathcal X timesmathcal Y tobits , D^ cc (F) is the minimum number of communicated bits in a deterministic protocol that computes F .
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Communication/query complexity and lifting.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Deterministic communication complexity\nsource_marker: \uE200cite\uE202turn20search4\uE202turn20search3\uE201"
```

```yaml
id: st.def.deterministic-decision-tree-complexity
kind: definition
status: accepted
latex: For $f:\bits^n\to\bits$, $D^{dt}(f)$ is the minimum number of bit-queries made by a deterministic decision tree that computes $f$ on all inputs.
informal: For f:bits^ntobits , D^ dt (f) is the minimum number of bit-queries made by a deterministic decision tree that computes f on all inputs.
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Communication/query complexity and lifting.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Deterministic decision tree complexity\nsource_marker: \uE200cite\uE202turn20search4\uE202turn20search0\uE201"
```

```yaml
id: st.def.composition-with-a-gadget-lifting-set-up
kind: definition
status: accepted
latex: 'Given $f:\bits^n\to\bits$ and a \emph{gadget} $g:\mathcal{X}\times\mathcal{Y}\to\bits$, define $F=f\circ g^n$ by

  \[

  F((x_1,\dots,x_n),(y_1,\dots,y_n)) \;=\; f(g(x_1,y_1),\dots,g(x_n,y_n)).

  \]

  A lifting theorem lower-bounds $\mathrm{CC}(F)$ in terms of a query measure of $f$.'
informal: Given f:bits^ntobits and a emph gadget g:mathcal X timesmathcal Y tobits , define F=fcirc g^n by [ F((x_1,dots,x_n),(y_1,dots,y_n)) ;=; f(g(x_1,y_1),dots,g(x_n,y_n)). ] A lifting theorem lower-bounds mathrm CC (F) in terms of a query measure of f .
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Communication/query complexity and lifting.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Composition with a gadget; lifting set-up\nsource_marker: \uE200cite\uE202turn20search4\uE202turn20search0\uE201"
```

```yaml
id: st.def.relativising-proof-technique-informal
kind: definition
status: accepted
latex: A proof technique is \emph{relativising} if the argument remains valid when all machines are given oracle access to an arbitrary oracle $A$ (i.e.\ it proves the relativised statement for all $A$).
informal: A proof technique is emph relativising if the argument remains valid when all machines are given oracle access to an arbitrary oracle A (i.e. it proves the relativised statement for all A ).
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Barrier notions.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Relativising proof technique (informal)\nsource_marker: \uE200cite\uE202turn27search16\uE202turn23search0\uE201"
```

```yaml
id: st.def.natural-proofs-constructive-large-useful-high-le
kind: definition
status: accepted
latex: "A property $\\mathcal{P}$ of Boolean functions (truth tables) is:\n(i) \\emph{constructive} if membership in $\\mathcal{P}$ is decidable efficiently (e.g.\\ in $\\poly(2^n)$ time on truth tables); \n(ii) \\emph{large} if a non-negligible fraction of all $n$-bit functions satisfy $\\mathcal{P}$; \n(iii) \\emph{useful} against a circuit class $\\mathcal{C}$ if no function computed by small $\\mathcal{C}$-circuits satisfies $\\mathcal{P}$.\nPrecise parameterisations vary; see Razborov--Rudich."
informal: 'A property mathcal P of Boolean functions (truth tables) is: (i) emph constructive if membership in mathcal P is decidable efficiently (e.g. in poly(2^n) time on truth tables); (ii) emph large if a non-negligible fraction of all n -bit functions satisfy mathcal P ; (iii) emph...'
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Barrier notions.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Natural proofs: \u201Cconstructive, large, useful\u201D (high-level)\nsource_marker: \uE200cite\uE202turn0search6\uE202turn4view2\uE201"
```

```yaml
id: st.def.algebrising-proof-technique-informal
kind: definition
status: accepted
latex: A proof technique is \emph{algebrising} if it relativises even when the oracle is augmented with low-degree extension access in the sense of Aaronson--Wigderson (extension oracles).
informal: A proof technique is emph algebrising if it relativises even when the oracle is augmented with low-degree extension access in the sense of Aaronson--Wigderson (extension oracles).
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: "parsed_env: definition\nsection: Paragraph: Barrier notions.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Algebrising proof technique (informal)\nsource_marker: \uE200cite\uE202turn6search2\uE202turn6search6\uE201"
```

```yaml
id: st.thm.cook-levin-sat-is-np-complete-cook1971
kind: theorem
status: accepted
latex: '$\mathrm{SAT}=\{\varphi : \varphi\ \text{is a satisfiable Boolean formula}\}$ is NP-complete.'
informal: 'mathrm SAT = varphi : varphi text is a satisfiable Boolean formula is NP-complete.'
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: "parsed_env: theorem\nsection: Paragraph: NP-completeness and baseline structure.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Cook--Levin: $\\mathrm{SAT}$ is NP-complete {\\cite{Cook1971}}\nsource_marker: \uE200cite\uE202turn30search0\uE202turn30search3\uE202turn23search0\uE201"
```

```yaml
id: st.thm.karp-many-natural-problems-are-np-complete-karp1
kind: theorem
status: accepted
latex: There exist many problems $L$ in combinatorial optimisation/graph theory such that $L$ is NP-complete under polynomial-time many-one reductions.
informal: There exist many problems L in combinatorial optimisation/graph theory such that L is NP-complete under polynomial-time many-one reductions.
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: "parsed_env: theorem\nsection: Paragraph: NP-completeness and baseline structure.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Karp: many natural problems are NP-complete {\\cite{Karp1972}}\nsource_marker: \uE200cite\uE202turn31search1\uE202turn31search6\uE202turn31search7\uE201"
```

```yaml
id: st.thm.nonuniform-separation-target
kind: theorem
status: accepted
latex: If $\NP\not\subseteq \Ppoly$, then $\Pclass\neq\NP$.
informal: If NPnotsubseteq Ppoly , then PclassneqNP .
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.83
proof_sketch: ''
notes: "parsed_env: proposition\nsection: Paragraph: Circuit lower bounds as direct targets.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Nonuniform separation target\nsource_marker: \uE200cite\uE202turn23search0\uE202turn4view2\uE202turn6search2\uE201\nnormalization: proposition mapped to theorem"
```

```yaml
id: st.thm.counting-lower-bound-almost-all-functions-are-ha
kind: theorem
status: accepted
latex: For sufficiently large $n$, a uniformly random Boolean function $f:\bits^n\to\bits$ requires circuit size $\Omega(2^n/n)$ (under standard finite bases).
informal: For sufficiently large n , a uniformly random Boolean function f:bits^ntobits requires circuit size Omega(2^n/n) (under standard finite bases).
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: 'parsed_env: theorem

  section: Paragraph: Circuit lower bounds as direct targets.

  source_citation: /Users/user/Downloads/deep-research-report.md

  label: Counting lower bound: almost all functions are hard (Shannon-style)'
```

```yaml
id: st.thm.karp-lipton-np-in-collapses-karplipton1980
kind: theorem
status: accepted
latex: If $\NP\subseteq \Ppoly$, then $\PH$ collapses to $\Sigma_2^p$.
informal: If NPsubseteq Ppoly , then PH collapses to Sigma_2^p .
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: "parsed_env: theorem\nsection: Paragraph: Nonuniformity and uniform consequences.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Karp--Lipton: NP in $\\Ppoly$ collapses $\\PH$ {\\cite{KarpLipton1980}}\nsource_marker: \uE200cite\uE202turn5search17\uE202turn9search15\uE202turn9search0\uE201"
```

```yaml
id: st.thm.adleman-adleman1978
kind: theorem
status: accepted
latex: Every $\BPP$ language has polynomial-size circuits; i.e.\ $\BPP\subseteq \Ppoly$.
informal: Every BPP language has polynomial-size circuits; i.e. BPPsubseteq Ppoly .
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: "parsed_env: theorem\nsection: Paragraph: Nonuniformity and uniform consequences.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Adleman: $\\BPP\\subseteq\\Ppoly$ {\\cite{Adleman1978}}\nsource_marker: \uE200cite\uE202turn29search1\uE202turn23search1\uE201"
```

```yaml
id: st.thm.h-stad-near-optimal-0-lower-bounds-for-parity-ha
kind: theorem
status: accepted
latex: For every constant depth $d\ge 2$, any depth-$d$ $\AC^0$ circuit computing $\mathrm{PARITY}_n$ has size $\exp(\Omega(n^{1/(d-1)}))$.
informal: For every constant depth dge 2 , any depth- d AC^0 circuit computing mathrm PARITY _n has size exp(Omega(n^ 1/(d-1) )) .
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: "parsed_env: theorem\nsection: Paragraph: Restricted circuit lower bounds (unconditional frontiers).\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: H{\\aa}stad: near-optimal $\\AC^0$ lower bounds for PARITY {\\cite{Hastad1986}}\nsource_marker: \uE200cite\uE202turn23search3\uE202turn1search18\uE202turn1search7\uE201"
```

```yaml
id: st.thm.razborov-smolensky-0-p
kind: theorem
status: accepted
latex: '$ lower bounds {\cite{Smolensky1987}}]

  For distinct primes $p\neq q$, the function $\mathrm{MOD}_q$ does not have polynomial-size $\AC^0[p]$ circuits (and quantitative tradeoffs yield exponential size lower bounds at fixed depth).'
informal: lower bounds cite Smolensky1987 ] For distinct primes pneq q , the function mathrm MOD _q does not have polynomial-size AC^0[p] circuits (and quantitative tradeoffs yield exponential size lower bounds at fixed depth).
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: "parsed_env: theorem\nsection: Paragraph: Restricted circuit lower bounds (unconditional frontiers).\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Razborov--Smolensky: $\\AC^0[p\nsource_marker: \uE200cite\uE202turn1search7\uE202turn1search3\uE202turn22search9\uE201"
```

```yaml
id: st.thm.monotone-lower-bounds-for-clique-exemplar-razbor
kind: theorem
status: accepted
latex: The monotone circuit complexity of $\mathrm{CLIQUE}$ is superpolynomial (indeed exponential for standard parameter regimes).
informal: The monotone circuit complexity of mathrm CLIQUE is superpolynomial (indeed exponential for standard parameter regimes).
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: "parsed_env: theorem\nsection: Paragraph: Restricted circuit lower bounds (unconditional frontiers).\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Monotone lower bounds for CLIQUE (exemplar) {\\cite{RazborovClique}}\nsource_marker: \uE200cite\uE202turn19search6\uE201"
```

```yaml
id: st.thm.williams-nonuniform-0-lower-bounds-for-williams2
kind: theorem
status: accepted
latex: $\NEXP\not\subseteq \ACC^0$, i.e.\ there exists a language in $\NEXP$ that does not have polynomial-size nonuniform $\ACC^0$ circuits.
informal: NEXPnotsubseteq ACC^0 , i.e. there exists a language in NEXP that does not have polynomial-size nonuniform ACC^0 circuits.
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: "parsed_env: theorem\nsection: Paragraph: Algorithms $\\to$ lower bounds (Williams programme).\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Williams: nonuniform $\\ACC^0$ lower bounds for $\\NEXP$ {\\cite{Williams2014ACC}}\nsource_marker: \uE200cite\uE202turn22search9\uE202turn5search7\uE202turn22search2\uE201"
```

```yaml
id: st.thm.williams-improved-exhaustive-search-circuit-lowe
kind: theorem
status: accepted
latex: If $\mathrm{CIRCUIT\mbox{-}SAT}$ on $n$ variables can be solved in time $2^{(1-\delta)n}\poly(m)$ for some $\delta>0$ (where $m$ is circuit size), then there exist explicit languages in relatively low exponential-time classes that require superpolynomial (indeed $2^{\varepsilon n}$) nonuniform circuit size for some $\varepsilon>0$.
informal: If mathrm CIRCUITmbox - SAT on n variables can be solved in time 2^ (1-delta)n poly(m) for some delta>0 (where m is circuit size), then there exist explicit languages in relatively low exponential-time classes that require superpolynomial (indeed 2^ varepsilon n ) nonuniform c...
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: "parsed_env: theorem\nsection: Paragraph: Algorithms $\\to$ lower bounds (Williams programme).\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Williams: improved exhaustive search $\\Rightarrow$ circuit lower bounds {\\cite{Williams2013Exhaustive}}\nsource_marker: \uE200cite\uE202turn33search2\uE202turn33search14\uE202turn22search2\uE201"
```

```yaml
id: st.obs.survey-perspective
kind: observation
status: accepted
latex: "For an overview of the algorithms$\\leftrightarrow$circuit-complexity duality and related developments (including counting and learning connections), see Williams\u2019 invited surveys."
informal: "For an overview of the algorithms leftrightarrow circuit-complexity duality and related developments (including counting and learning connections), see Williams\u2019 invited surveys."
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.72
proof_sketch: ''
notes: "parsed_env: remark\nsection: Paragraph: Algorithms $\\to$ lower bounds (Williams programme).\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Survey perspective\nsource_marker: \uE200cite\uE202turn22search2\uE202turn22search6\uE201\nnormalization: remark mapped to observation"
```

```yaml
id: st.thm.kabanets-impagliazzo-pit-derandomisation-implies
kind: theorem
status: accepted
latex: 'If $\mathrm{PIT}\in \Pclass$ (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard variants), then at least one of the following holds:

  \[

  \NEXP\not\subseteq \Ppoly \quad \text{or} \quad \text{Permanent does not have polynomial-size arithmetic circuits.}

  \]'
informal: 'If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard variants), then at least one of the following holds: [ NEXPnotsubseteq Ppoly quad text or quad text Permanent does not have polynomial-size arithmet...'
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: "parsed_env: theorem\nsection: Paragraph: Derandomisation/PIT $\\leftrightarrow$ lower bounds.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Kabanets--Impagliazzo: PIT derandomisation implies major lower bounds {\\cite{KabanetsImpagliazzo2004}}\nsource_marker: \uE200cite\uE202turn32search4\uE202turn32search9\uE202turn32search3\uE201"
```

```yaml
id: st.thm.nisan-wigderson-hardness-vs-randomness-nisanwigd
kind: theorem
status: accepted
latex: Assuming sufficiently strong circuit hardness (typically worst-case-to-average-case hardness for an explicit function), one can construct pseudorandom generators fooling polynomial-size circuits, yielding derandomisations (e.g.\ conditional collapses of $\BPP$ to $\Pclass$ or subexponential simulations).
informal: Assuming sufficiently strong circuit hardness (typically worst-case-to-average-case hardness for an explicit function), one can construct pseudorandom generators fooling polynomial-size circuits, yielding derandomisations (e.g. conditional collapses of BPP to Pclass or subexpo...
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: "parsed_env: theorem\nsection: Paragraph: Derandomisation/PIT $\\leftrightarrow$ lower bounds.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Nisan--Wigderson: hardness vs.\\ randomness {\\cite{NisanWigderson1994}}\nsource_marker: \uE200cite\uE202turn23search1\uE202turn4view2\uE201"
```

```yaml
id: st.thm.impagliazzo-wigderson-e-hardness-nonuniform-form
kind: theorem
status: accepted
latex: If there exists a function in $\E$ with circuit complexity $2^{\Omega(n)}$ (in a standard nonuniform sense), then $\BPP=\Pclass$ (via a PRG construction building on XOR/direct-product amplification).
informal: If there exists a function in E with circuit complexity 2^ Omega(n) (in a standard nonuniform sense), then BPP=Pclass (via a PRG construction building on XOR/direct-product amplification).
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: "parsed_env: theorem\nsection: Paragraph: Derandomisation/PIT $\\leftrightarrow$ lower bounds.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Impagliazzo--Wigderson: $E$-hardness $\\Rightarrow \\BPP=\\Pclass$ (nonuniform form) {\\cite{ImpagliazzoWigderson1997}}\nsource_marker: \uE200cite\uE202turn26search1\uE202turn26search3\uE202turn23search1\uE201"
```

```yaml
id: st.thm.cook-reckhow-proof-systems-and-cookreckhow1979
kind: theorem
status: accepted
latex: There exists a polynomially bounded propositional proof system for $\TAUT$ if and only if $\NP=\coNP$.
informal: There exists a polynomially bounded propositional proof system for TAUT if and only if NP=coNP .
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: "parsed_env: theorem\nsection: Paragraph: Proof complexity connections.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Cook--Reckhow: proof systems and $\\NP=\\coNP$ {\\cite{CookReckhow1979}}\nsource_marker: \uE200cite\uE202turn19search0\uE202turn19search4\uE201"
```

```yaml
id: st.thm.resolution-php-lower-bounds-exemplar-buss1988
kind: theorem
status: accepted
latex: Pigeonhole Principle (PHP) tautologies require exponential-size resolution refutations (quantitative forms depend on the encoding and parameters).
informal: Pigeonhole Principle (PHP) tautologies require exponential-size resolution refutations (quantitative forms depend on the encoding and parameters).
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: "parsed_env: theorem\nsection: Paragraph: Proof complexity connections.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Resolution/PHP lower bounds (exemplar) {\\cite{Buss1988}}\nsource_marker: \uE200cite\uE202turn19search1\uE201"
```

```yaml
id: st.thm.bounded-depth-frege-php-lower-bounds-beamepitass
kind: theorem
status: accepted
latex: PHP tautologies require exponential-size bounded-depth Frege proofs (for standard formulations), implying strong lower bounds for those proof systems.
informal: PHP tautologies require exponential-size bounded-depth Frege proofs (for standard formulations), implying strong lower bounds for those proof systems.
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: "parsed_env: theorem\nsection: Paragraph: Proof complexity connections.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Bounded-depth Frege PHP lower bounds {\\cite{BeamePitassiImpagliazzo1993}}\nsource_marker: \uE200cite\uE202turn19search9\uE201"
```

```yaml
id: st.thm.grochow-pitassi-ips-ties-proof-lower-bounds-to-a
kind: theorem
status: accepted
latex: Any superpolynomial lower bound on IPS refutation size for \emph{any} tautology implies superpolynomial lower bounds for algebraic circuits computing the permanent (i.e.\ consequences consistent with $\mathrm{VP}\neq\mathrm{VNP}$ in standard formulations). Moreover, verification of IPS refutations relates to PIT, motivating propositional PIT axioms.
informal: Any superpolynomial lower bound on IPS refutation size for emph any tautology implies superpolynomial lower bounds for algebraic circuits computing the permanent (i.e. consequences consistent with mathrm VP neqmathrm VNP in standard formulations). Moreover, verification of IPS...
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: "parsed_env: theorem\nsection: Paragraph: Proof complexity connections.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Grochow--Pitassi: IPS ties proof lower bounds to algebraic circuit lower bounds {\\cite{GrochowPitassi2018}}\nsource_marker: \uE200cite\uE202turn19search6\uE202turn"
```

```yaml
id: st.thm.oliveira-santhanam-hardness-magnification-for-na
kind: theorem
status: accepted
latex: "There exist explicit \u201Cmeta\u201D problems (including MCSP variants) such that proving certain \\emph{barely-superlinear} lower bounds against restricted models (e.g.\\ formulas) would imply major lower bounds for $\\NP$ in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter regimes consequences as strong as $\\NP\\not\\subseteq\\Ppoly$)."
informal: "There exist explicit \u201Cmeta\u201D problems (including MCSP variants) such that proving certain emph barely-superlinear lower bounds against restricted models (e.g. formulas) would imply major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lowe..."
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: "parsed_env: theorem\nsection: Paragraph: Hardness magnification and meta-complexity.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Oliveira--Santhanam: hardness magnification for natural problems {\\cite{OliveiraSanthanam2018}}\nsource_marker: \uE200cite\uE202turn16search3\uE202turn17sea"
```

```yaml
id: st.thm.oliveira-pich-santhanam-magnification-near-state
kind: theorem
status: accepted
latex: In refined regimes, lower bounds for Gap-MCSP slightly beyond known frontiers (e.g.\ $N^{1+\varepsilon}$-type circuit lower bounds for suitable promise gaps and input length $N=2^n$) imply major consequences such as $\NP\not\subseteq \Ppoly$.
informal: In refined regimes, lower bounds for Gap-MCSP slightly beyond known frontiers (e.g. N^ 1+varepsilon -type circuit lower bounds for suitable promise gaps and input length N=2^n ) imply major consequences such as NPnotsubseteq Ppoly .
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: "parsed_env: theorem\nsection: Paragraph: Hardness magnification and meta-complexity.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Oliveira--Pich--Santhanam: magnification near state-of-the-art {\\cite{OliveiraPichSanthanam2021}}\nsource_marker: \uE200cite\uE202turn16search1\uE202turn16search19\uE201"
```

```yaml
id: st.thm.atserias-m-uller-simple-general-magnification-fr
kind: theorem
status: accepted
latex: There exist general-purpose magnification theorems (not problem-specific) showing that certain mild lower bounds for distinguishers/sparse-code objects can be amplified into stronger circuit/formula lower bounds, achieving magnification thresholds below previously known lower bounds in some settings.
informal: There exist general-purpose magnification theorems (not problem-specific) showing that certain mild lower bounds for distinguishers/sparse-code objects can be amplified into stronger circuit/formula lower bounds, achieving magnification thresholds below previously known lower...
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: "parsed_env: theorem\nsection: Paragraph: Hardness magnification and meta-complexity.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Atserias--M\\\"uller: simple general magnification framework {\\cite{AtseriasMueller2025}}\nsource_marker: \uE200cite\uE202turn16search2\uE202turn16search5\uE201"
```

```yaml
id: st.thm.allender-das-szk-reduces-to-mcsp-bpp-reductions-
kind: theorem
status: accepted
latex: Every problem in $\mathrm{SZK}$ is reducible to MCSP under efficient (randomised) reductions; in particular, Graph Isomorphism lies in $\mathrm{RP}^{\mathrm{MCSP}}$ (in standard formulations).
informal: Every problem in mathrm SZK is reducible to MCSP under efficient (randomised) reductions; in particular, Graph Isomorphism lies in mathrm RP ^ mathrm MCSP (in standard formulations).
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: "parsed_env: theorem\nsection: Paragraph: Hardness magnification and meta-complexity.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Allender--Das: SZK reduces to MCSP (BPP reductions) {\\cite{AllenderDas2017}}\nsource_marker: \uE200cite\uE202turn28search5\uE202turn28search0\uE202turn18search11\uE201"
```

```yaml
id: st.thm.murray-williams-non-np-hardness-of-mcsp-under-lo
kind: theorem
status: accepted
latex: "Under \u201Clocal\u201D polynomial-time reductions (where each output bit is computable with very small time), MCSP is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various reductions would entail unexpected class separations."
informal: "Under \u201Clocal\u201D polynomial-time reductions (where each output bit is computable with very small time), MCSP is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various reductions would entail unexpected..."
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: "parsed_env: theorem\nsection: Paragraph: Hardness magnification and meta-complexity.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Murray--Williams: (non-)NP-hardness of MCSP under local reductions {\\cite{MurrayWilliams2017}}\nsource_marker: \uE200cite\uE202turn18search4\uE202turn18search11\uE201"
```

```yaml
id: st.thm.hirahara-ilango-np-hardness-of-mcsp-from-well-st
kind: theorem
status: accepted
latex: Assuming a collection of established cryptographic and complexity-theoretic hypotheses (as specified in the paper), MCSP is NP-hard under certain reductions, yielding conditional NP-hardness results for MCSP and variants.
informal: Assuming a collection of established cryptographic and complexity-theoretic hypotheses (as specified in the paper), MCSP is NP-hard under certain reductions, yielding conditional NP-hardness results for MCSP and variants.
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: "parsed_env: theorem\nsection: Paragraph: Hardness magnification and meta-complexity.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Hirahara--Ilango: NP-hardness of MCSP from well-studied assumptions {\\cite{HiraharaIlango2025}}\nsource_marker: \uE200cite\uE202turn17search0\uE201"
```

```yaml
id: st.thm.g-o-os-pitassi-watson-and-coauthors-query-to-com
kind: theorem
status: accepted
latex: There exist gadgets $g$ such that for all Boolean functions $f$, the bounded-error randomised communication complexity of $F=f\circ g^n$ is (up to polylog factors) at least the bounded-error randomised query complexity of $f$ times the communication cost of $g$.
informal: There exist gadgets g such that for all Boolean functions f , the bounded-error randomised communication complexity of F=fcirc g^n is (up to polylog factors) at least the bounded-error randomised query complexity of f times the communication cost of g .
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: "parsed_env: theorem\nsection: Paragraph: Communication complexity and lifting.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: G\\\"o\\\"os--Pitassi--Watson (and coauthors): query-to-communication lifting for $\\BPP$ {\\cite{GoosPitassiWatson2017}}\nsource_marker: \uE200cite\uE202turn20search0\uE202turn20search4\uE202turn20search17\uE201"
```

```yaml
id: st.obs.survey-entry-point
kind: observation
status: accepted
latex: "For a compact survey emphasising \u201Cproofs--circuits--communication\u201D interconnections and TFNP as a unifying language, see de Rezende et al."
informal: "For a compact survey emphasising \u201Cproofs--circuits--communication\u201D interconnections and TFNP as a unifying language, see de Rezende et al."
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.72
proof_sketch: ''
notes: "parsed_env: remark\nsection: Paragraph: Communication complexity and lifting.\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Survey entry point\nsource_marker: \uE200cite\uE202turn20search17\uE202turn20search1\uE201\nnormalization: remark mapped to observation"
```

```yaml
id: st.thm.baker-gill-solovay-relativisation-barrier-bakerg
kind: theorem
status: accepted
latex: There exist oracles $A,B$ such that $\Pclass^A=\NP^A$ and $\Pclass^B\neq \NP^B$.
informal: There exist oracles A,B such that Pclass^A=NP^A and Pclass^Bneq NP^B .
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: "parsed_env: theorem\nsection: Paragraph: Barrier theorems (what typical proof tools cannot do).\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Baker--Gill--Solovay: relativisation barrier {\\cite{BakerGillSolovay1975}}\nsource_marker: \uE200cite\uE202turn27search16\uE202turn6search1\uE202turn27search3\uE201"
```

```yaml
id: st.thm.razborov-rudich-natural-proofs-barrier-razborovr
kind: theorem
status: accepted
latex: "Assuming the existence of sufficiently strong pseudorandom functions, no family of \u201Cnatural\u201D properties (constructive and large) can be useful for proving superpolynomial lower bounds against strong circuit classes such as $\\Ppoly$."
informal: "Assuming the existence of sufficiently strong pseudorandom functions, no family of \u201Cnatural\u201D properties (constructive and large) can be useful for proving superpolynomial lower bounds against strong circuit classes such as Ppoly ."
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: "parsed_env: theorem\nsection: Paragraph: Barrier theorems (what typical proof tools cannot do).\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Razborov--Rudich: natural proofs barrier {\\cite{RazborovRudich1997}}\nsource_marker: \uE200cite\uE202turn4view2\uE202turn0search6\uE202turn23search1\uE201"
```

```yaml
id: st.thm.aaronson-wigderson-algebrisation-barrier-aaronso
kind: theorem
status: accepted
latex: Define extension oracles and algebrising proofs. Then there exist oracles (with low-degree extensions) yielding separations implying that any proof of $\Pclass\neq\NP$ must be non-algebrising. Many other major open problems (e.g.\ $\Pclass$ vs.\ $\RP$) likewise require non-algebrising techniques.
informal: Define extension oracles and algebrising proofs. Then there exist oracles (with low-degree extensions) yielding separations implying that any proof of PclassneqNP must be non-algebrising. Many other major open problems (e.g. Pclass vs. RP ) likewise require non-algebrising tec...
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: "parsed_env: theorem\nsection: Paragraph: Barrier theorems (what typical proof tools cannot do).\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Aaronson--Wigderson: algebrisation barrier {\\cite{AaronsonWigderson2009}}\nsource_marker: \uE200cite\uE202turn6search2\uE202turn6search6\uE201"
```

```yaml
id: st.obs.williams-constructivity-is-unavoidable-perspecti
kind: observation
status: accepted
latex: Williams shows equivalences characterising $\NEXP\not\subseteq\mathcal{C}$ for many circuit classes $\mathcal{C}$ in terms of the existence of efficient distinguishers/properties, linking natural proof notions and derandomisation.
informal: Williams shows equivalences characterising NEXPnotsubseteqmathcal C for many circuit classes mathcal C in terms of the existence of efficient distinguishers/properties, linking natural proof notions and derandomisation.
source_ids:
- src.001
used_symbols: []
depends_on: []
confidence: 0.72
proof_sketch: ''
notes: "parsed_env: remark\nsection: Paragraph: Barrier theorems (what typical proof tools cannot do).\nsource_citation: /Users/user/Downloads/deep-research-report.md\nlabel: Williams: \u201Cconstructivity is unavoidable\u201D perspective\nsource_marker: \uE200cite\uE202turn22search3\uE202turn22search7\uE201\nnormalization: remark mapped to observation"
```

```yaml
id: st.thm.complexity.kozen2006-t-1-1
kind: theorem
status: accepted
latex: |-
  For Σ = {0,1,#}, the palindrome language PAL = {z ∈ Σ* : z = rev(z)} requires Ω(n²) time on every one-tape Turing machine.
informal: |-
  One-tape palindrome lower bound: For Σ = {0,1,#}, the palindrome language PAL = {z ∈ Σ* : z = rev(z)} requires Ω(n²) time on every one-tape Turing machine.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:1.1
  package_source_id: kozen2006
  module_id: kozen2006:1
  entry_type: Theorem
  label: 1.1
  name: One-tape palindrome lower bound
  pdf_page: 18
  printed_page: 7
  importance: supporting
  tags: turing-machines, lower-bounds, crossing-sequences
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-1-2
kind: lemma
status: accepted
latex: |-
  For distinct x,y ∈ PALₙ, the sets C(x) and C(y) of crossing sequences in the middle half of the input are disjoint.
informal: |-
  Crossing-sequence disjointness: For distinct x,y ∈ PALₙ, the sets C(x) and C(y) of crossing sequences in the middle half of the input are disjoint.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:1.2
  package_source_id: kozen2006
  module_id: kozen2006:1
  entry_type: Lemma
  label: 1.2
  name: Crossing-sequence disjointness
  pdf_page: 19
  printed_page: 8
  importance: supporting
  tags: turing-machines, lower-bounds, crossing-sequences
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-1-3
kind: theorem
status: accepted
latex: |-
  Every Turing machine using o(log log n) work space accepts a regular language. This is tight up to constants: a specific nonregular language is accepted in O(log log n) space.
informal: |-
  Sub-log-log space collapse: Every Turing machine using o(log log n) work space accepts a regular language. This is tight up to constants: a specific nonregular language is accepted in O(log log n) space.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:1.3
  package_source_id: kozen2006
  module_id: kozen2006:1
  entry_type: Theorem
  label: 1.3
  name: Sub-log-log space collapse
  pdf_page: 19
  printed_page: 8
  importance: supporting
  tags: turing-machines, lower-bounds, crossing-sequences
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-1-4
kind: lemma
status: accepted
latex: |-
  If a machine uses at most a fixed finite number of work-tape cells on every accepted input, then its accepted language is regular.
informal: |-
  Constant accepted-space bound: If a machine uses at most a fixed finite number of work-tape cells on every accepted input, then its accepted language is regular.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:1.4
  package_source_id: kozen2006
  module_id: kozen2006:1
  entry_type: Lemma
  label: 1.4
  name: Constant accepted-space bound
  pdf_page: 20
  printed_page: 9
  importance: supporting
  tags: turing-machines, lower-bounds, crossing-sequences
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.def.complexity.kozen2006-d-2-1
kind: definition
status: accepted
latex: |-
  A nondeterministic TM is T(n)-time-bounded when, except on finitely many inputs, every computation path halts within T(|x|) steps. It is S(n)-space-bounded when, except on finitely many inputs, every path uses at most S(|x|) work-tape cells.
informal: |-
  Time- and space-bounded machines: A nondeterministic TM is T(n)-time-bounded when, except on finitely many inputs, every computation path halts within T(|x|) steps. It is S(n)-space-bounded when, except on finitely many inputs, every path uses at most S(|x|) work-tape cells.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:D:2.1
  package_source_id: kozen2006
  module_id: kozen2006:2
  entry_type: Definition
  label: 2.1
  name: Time- and space-bounded machines
  pdf_page: 22
  printed_page: 11
  importance: foundational
  tags: time-complexity, space-complexity
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.def.complexity.kozen2006-d-2-2
kind: definition
status: accepted
latex: |-
  DTIME(T), NTIME(T), DSPACE(S), and NSPACE(S) are the languages accepted within the indicated deterministic or nondeterministic time or space bound. For a class A, co-A is the class of complements of languages in A.
informal: |-
  Basic time and space classes: DTIME(T), NTIME(T), DSPACE(S), and NSPACE(S) are the languages accepted within the indicated deterministic or nondeterministic time or space bound. For a class A, co-A is the class of complements of languages in A.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:D:2.2
  package_source_id: kozen2006
  module_id: kozen2006:2
  entry_type: Definition
  label: 2.2
  name: Basic time and space classes
  pdf_page: 23
  printed_page: 12
  importance: foundational
  tags: time-complexity, space-complexity
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-2-3
kind: theorem
status: accepted
latex: |-
  For T(n) ≥ n+1, S(n) = Ω(log n), and every constant c ≥ 1: DTIME(cT) ⊆ DTIME(T), NTIME(cT) ⊆ NTIME(T), DSPACE(cS) ⊆ DSPACE(S), and NSPACE(cS) ⊆ NSPACE(S).
informal: |-
  Linear speedup: For T(n) ≥ n+1, S(n) = Ω(log n), and every constant c ≥ 1: DTIME(cT) ⊆ DTIME(T), NTIME(cT) ⊆ NTIME(T), DSPACE(cS) ⊆ DSPACE(S), and NSPACE(cS) ⊆ NSPACE(S).
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:2.3
  package_source_id: kozen2006
  module_id: kozen2006:2
  entry_type: Theorem
  label: 2.3
  name: Linear speedup
  pdf_page: 23
  printed_page: 12
  importance: supporting
  tags: time-complexity, space-complexity
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.def.complexity.kozen2006-d-2-4
kind: definition
status: accepted
latex: |-
  LOGSPACE = DSPACE(log n), NLOGSPACE = NSPACE(log n), P = ⋃ₖ DTIME(nᵏ), NP = ⋃ₖ NTIME(nᵏ), PSPACE = ⋃ₖ DSPACE(nᵏ), NPSPACE = ⋃ₖ NSPACE(nᵏ), and analogously EXPTIME, NEXPTIME, EXPSPACE, and NEXPSPACE use bounds 2^{nᵏ}.
informal: |-
  Named complexity classes: LOGSPACE = DSPACE(log n), NLOGSPACE = NSPACE(log n), P = ⋃ₖ DTIME(nᵏ), NP = ⋃ₖ NTIME(nᵏ), PSPACE = ⋃ₖ DSPACE(nᵏ), NPSPACE = ⋃ₖ NSPACE(nᵏ), and analogously EXPTIME, NEXPTIME, EXPSPACE, and NEXPSPACE use bounds 2^{nᵏ}.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:D:2.4
  package_source_id: kozen2006
  module_id: kozen2006:2
  entry_type: Definition
  label: 2.4
  name: Named complexity classes
  pdf_page: 23
  printed_page: 12
  importance: foundational
  tags: time-complexity, space-complexity
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-2-5
kind: theorem
status: accepted
latex: |-
  For S(n) ≥ log n: DTIME(T) ⊆ DSPACE(T), NTIME(T) ⊆ NSPACE(T), DSPACE(S) ⊆ DTIME(2^{O(S)}), and NSPACE(S) ⊆ NTIME(2^{O(S)}).
informal: |-
  Basic time-space inclusions: For S(n) ≥ log n: DTIME(T) ⊆ DSPACE(T), NTIME(T) ⊆ NSPACE(T), DSPACE(S) ⊆ DTIME(2^{O(S)}), and NSPACE(S) ⊆ NTIME(2^{O(S)}).
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:2.5
  package_source_id: kozen2006
  module_id: kozen2006:2
  entry_type: Theorem
  label: 2.5
  name: Basic time-space inclusions
  pdf_page: 24
  printed_page: 13
  importance: supporting
  tags: time-complexity, space-complexity
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-2-6
kind: theorem
status: accepted
latex: |-
  For S(n) ≥ log n: NTIME(T) ⊆ DSPACE(T), and NSPACE(S) ⊆ DTIME(2^{O(S)}).
informal: |-
  Deterministic simulation bounds: For S(n) ≥ log n: NTIME(T) ⊆ DSPACE(T), and NSPACE(S) ⊆ DTIME(2^{O(S)}).
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:2.6
  package_source_id: kozen2006
  module_id: kozen2006:2
  entry_type: Theorem
  label: 2.6
  name: Deterministic simulation bounds
  pdf_page: 25
  printed_page: 14
  importance: supporting
  tags: time-complexity, space-complexity
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-2-7
kind: theorem
status: accepted
latex: |-
  For S(n) ≥ log n, NSPACE(S(n)) ⊆ DSPACE(S(n)²). In particular, PSPACE = NPSPACE.
informal: |-
  Savitch’s theorem: For S(n) ≥ log n, NSPACE(S(n)) ⊆ DSPACE(S(n)²). In particular, PSPACE = NPSPACE. Significance: Converts nondeterministic space into only a quadratic deterministic-space overhead.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:2.7
  package_source_id: kozen2006
  module_id: kozen2006:2
  entry_type: Theorem
  label: 2.7
  name: Savitch’s theorem
  pdf_page: 26
  printed_page: 15
  importance: core
  tags: time-complexity, space-complexity
  extraction_scope: numbered formal statement
  review_status: curated
  significance: Converts nondeterministic space into only a quadratic deterministic-space overhead.
```

```yaml
id: st.thm.complexity.kozen2006-t-3-1
kind: theorem
status: accepted
latex: |-
  If S is space-constructible, then DSPACE(S) contains a language outside DSPACE(S′) for every S′ = o(S).
informal: |-
  Deterministic space hierarchy: If S is space-constructible, then DSPACE(S) contains a language outside DSPACE(S′) for every S′ = o(S).
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:3.1
  package_source_id: kozen2006
  module_id: kozen2006:3
  entry_type: Theorem
  label: 3.1
  name: Deterministic space hierarchy
  pdf_page: 28
  printed_page: 17
  importance: supporting
  tags: hierarchy-theorems, diagonalization, padding
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-3-2
kind: theorem
status: accepted
latex: |-
  If T is time-constructible and T(n) ≥ n, then DTIME(T) contains a language outside every DTIME(T′) satisfying T′(n) log T′(n) = o(T(n)).
informal: |-
  Deterministic time hierarchy: If T is time-constructible and T(n) ≥ n, then DTIME(T) contains a language outside every DTIME(T′) satisfying T′(n) log T′(n) = o(T(n)).
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:3.2
  package_source_id: kozen2006
  module_id: kozen2006:3
  entry_type: Theorem
  label: 3.2
  name: Deterministic time hierarchy
  pdf_page: 30
  printed_page: 19
  importance: supporting
  tags: hierarchy-theorems, diagonalization, padding
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-4-1
kind: theorem
status: accepted
latex: |-
  For every S(n) ≥ log n, NSPACE(S(n)) is closed under complement: NSPACE(S(n)) = co-NSPACE(S(n)).
informal: |-
  Immerman–Szelepcsényi theorem: For every S(n) ≥ log n, NSPACE(S(n)) is closed under complement: NSPACE(S(n)) = co-NSPACE(S(n)). Significance: Shows nondeterministic space is closed under complement, including NL = coNL.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:4.1
  package_source_id: kozen2006
  module_id: kozen2006:4
  entry_type: Theorem
  label: 4.1
  name: Immerman–Szelepcsényi theorem
  pdf_page: 33
  printed_page: 22
  importance: core
  tags: space-complexity, complement
  extraction_scope: numbered formal statement
  review_status: curated
  significance: Shows nondeterministic space is closed under complement, including NL = coNL.
```

```yaml
id: st.lem.complexity.kozen2006-l-5-1
kind: lemma
status: accepted
latex: |-
  Logspace many-one reducibility is transitive: if A ≤ₘˡᵒᵍ B and B ≤ₘˡᵒᵍ C, then A ≤ₘˡᵒᵍ C.
informal: |-
  Transitivity of logspace reductions: Logspace many-one reducibility is transitive: if A ≤ₘˡᵒᵍ B and B ≤ₘˡᵒᵍ C, then A ≤ₘˡᵒᵍ C.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:5.1
  package_source_id: kozen2006
  module_id: kozen2006:5
  entry_type: Lemma
  label: 5.1
  name: Transitivity of logspace reductions
  pdf_page: 38
  printed_page: 27
  importance: supporting
  tags: logspace, reductions, completeness
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-5-2
kind: lemma
status: accepted
latex: |-
  A language A is in LOGSPACE exactly when A ≤ₘˡᵒᵍ {0,1}.
informal: |-
  LOGSPACE as reduction to a fixed language: A language A is in LOGSPACE exactly when A ≤ₘˡᵒᵍ {0,1}.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:5.2
  package_source_id: kozen2006
  module_id: kozen2006:5
  entry_type: Lemma
  label: 5.2
  name: LOGSPACE as reduction to a fixed language
  pdf_page: 38
  printed_page: 27
  importance: supporting
  tags: logspace, reductions, completeness
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-5-3
kind: lemma
status: accepted
latex: |-
  If A ≤ₘˡᵒᵍ B and B ∈ LOGSPACE, then A ∈ LOGSPACE.
informal: |-
  Closure under logspace reduction: If A ≤ₘˡᵒᵍ B and B ∈ LOGSPACE, then A ∈ LOGSPACE.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:5.3
  package_source_id: kozen2006
  module_id: kozen2006:5
  entry_type: Lemma
  label: 5.3
  name: Closure under logspace reduction
  pdf_page: 38
  printed_page: 27
  importance: supporting
  tags: logspace, reductions, completeness
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-5-4
kind: lemma
status: accepted
latex: |-
  If A ≤ₘˡᵒᵍ B, then A ≤ₘᵖ B.
informal: |-
  Logspace reductions are polynomial-time reductions: If A ≤ₘˡᵒᵍ B, then A ≤ₘᵖ B.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:5.4
  package_source_id: kozen2006
  module_id: kozen2006:5
  entry_type: Lemma
  label: 5.4
  name: Logspace reductions are polynomial-time reductions
  pdf_page: 39
  printed_page: 28
  importance: supporting
  tags: logspace, reductions, completeness
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.def.complexity.kozen2006-d-5-5
kind: definition
status: accepted
latex: |-
  MAZE asks whether a directed graph G with distinguished vertices s and t contains a directed path from s to t.
informal: |-
  MAZE / directed reachability: MAZE asks whether a directed graph G with distinguished vertices s and t contains a directed path from s to t.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:D:5.5
  package_source_id: kozen2006
  module_id: kozen2006:5
  entry_type: Definition
  label: 5.5
  name: MAZE / directed reachability
  pdf_page: 39
  printed_page: 28
  importance: foundational
  tags: logspace, reductions, completeness
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-5-6
kind: theorem
status: accepted
latex: |-
  MAZE is complete for NLOGSPACE under logspace many-one reductions.
informal: |-
  NLOGSPACE-completeness of reachability: MAZE is complete for NLOGSPACE under logspace many-one reductions.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:5.6
  package_source_id: kozen2006
  module_id: kozen2006:5
  entry_type: Theorem
  label: 5.6
  name: NLOGSPACE-completeness of reachability
  pdf_page: 39
  printed_page: 28
  importance: core
  tags: logspace, reductions, completeness
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.cor.complexity.kozen2006-c-5-7
kind: corollary
status: accepted
latex: |-
  MAZE is in LOGSPACE if and only if LOGSPACE = NLOGSPACE.
informal: |-
  Reachability criterion for L = NL: MAZE is in LOGSPACE if and only if LOGSPACE = NLOGSPACE.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.82
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:C:5.7
  package_source_id: kozen2006
  module_id: kozen2006:5
  entry_type: Corollary
  label: 5.7
  name: Reachability criterion for L = NL
  pdf_page: 40
  printed_page: 29
  importance: supporting
  tags: logspace, reductions, completeness
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-6-1
kind: theorem
status: accepted
latex: |-
  The Boolean circuit value problem is complete for P under logspace many-one reductions.
informal: |-
  P-completeness of circuit value: The Boolean circuit value problem is complete for P under logspace many-one reductions.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:6.1
  package_source_id: kozen2006
  module_id: kozen2006:6
  entry_type: Theorem
  label: 6.1
  name: P-completeness of circuit value
  pdf_page: 42
  printed_page: 31
  importance: core
  tags: circuits, sat, completeness
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-6-2
kind: theorem
status: accepted
latex: |-
  Boolean satisfiability is complete for NP under logspace many-one reductions.
informal: |-
  Cook–Levin theorem, logspace form: Boolean satisfiability is complete for NP under logspace many-one reductions. Significance: Provides the canonical complete problem for NP.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:6.2
  package_source_id: kozen2006
  module_id: kozen2006:6
  entry_type: Theorem
  label: 6.2
  name: Cook–Levin theorem, logspace form
  pdf_page: 45
  printed_page: 34
  importance: core
  tags: circuits, sat, completeness
  extraction_scope: numbered formal statement
  review_status: curated
  significance: Provides the canonical complete problem for NP.
```

```yaml
id: st.lem.complexity.kozen2006-l-a-3
kind: lemma
status: accepted
latex: |-
  The infimum of any family of prefixpoints of a monotone operator is again a prefixpoint.
informal: |-
  Infima of prefixpoints: The infimum of any family of prefixpoints of a monotone operator is again a prefixpoint.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:A.3
  package_source_id: kozen2006
  module_id: kozen2006:A
  entry_type: Lemma
  label: A.3
  name: Infima of prefixpoints
  pdf_page: 51
  printed_page: 40
  importance: supporting
  tags: lattices, fixed-points
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-a-4
kind: lemma
status: accepted
latex: |-
  Every monotone operator on a complete lattice has a least fixpoint.
informal: |-
  Least fixpoint existence: Every monotone operator on a complete lattice has a least fixpoint.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:A.4
  package_source_id: kozen2006
  module_id: kozen2006:A
  entry_type: Lemma
  label: A.4
  name: Least fixpoint existence
  pdf_page: 51
  printed_page: 40
  importance: supporting
  tags: lattices, fixed-points
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-a-5
kind: lemma
status: accepted
latex: |-
  For a monotone operator τ, the map τ†(x), defined as the least prefixpoint of τ above x, is a closure operator.
informal: |-
  Prefixpoint closure operator: For a monotone operator τ, the map τ†(x), defined as the least prefixpoint of τ above x, is a closure operator.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:A.5
  package_source_id: kozen2006
  module_id: kozen2006:A
  entry_type: Lemma
  label: A.5
  name: Prefixpoint closure operator
  pdf_page: 52
  printed_page: 41
  importance: supporting
  tags: lattices, fixed-points
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-a-8
kind: lemma
status: accepted
latex: |-
  For ordinals α ≤ β, the transfinite iterates satisfy τ^α(x) ≤ τ^β(x).
informal: |-
  Monotonicity of transfinite approximants: For ordinals α ≤ β, the transfinite iterates satisfy τ^α(x) ≤ τ^β(x).
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:A.8
  package_source_id: kozen2006
  module_id: kozen2006:A
  entry_type: Lemma
  label: A.8
  name: Monotonicity of transfinite approximants
  pdf_page: 53
  printed_page: 42
  importance: supporting
  tags: lattices, fixed-points
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-a-9
kind: theorem
status: accepted
latex: |-
  For every monotone operator τ on a complete lattice, the least prefixpoint above x equals the supremum of the transfinite iteration from below: τ†(x) = τ*(x).
informal: |-
  Knaster–Tarski theorem: For every monotone operator τ on a complete lattice, the least prefixpoint above x equals the supremum of the transfinite iteration from below: τ†(x) = τ*(x). Significance: Supplies the fixed-point machinery used for alternating computation and games.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:A.9
  package_source_id: kozen2006
  module_id: kozen2006:A
  entry_type: Theorem
  label: A.9
  name: Knaster–Tarski theorem
  pdf_page: 54
  printed_page: 43
  importance: core
  tags: lattices, fixed-points
  extraction_scope: numbered formal statement
  review_status: curated
  significance: Supplies the fixed-point machinery used for alternating computation and games.
```

```yaml
id: st.def.complexity.kozen2006-d-7-1
kind: definition
status: accepted
latex: |-
  An alternating Turing machine is a nondeterministic TM whose states are typed as AND, OR, or NOT states; NOT configurations have exactly one successor. An accepting leaf is an AND state with no successors, and a rejecting leaf is an OR state with no successors.
informal: |-
  Alternating Turing machine: An alternating Turing machine is a nondeterministic TM whose states are typed as AND, OR, or NOT states; NOT configurations have exactly one successor. An accepting leaf is an AND state with no successors, and a rejecting leaf is an OR state with no successors.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:D:7.1
  package_source_id: kozen2006
  module_id: kozen2006:7
  entry_type: Definition
  label: 7.1
  name: Alternating Turing machine
  pdf_page: 56
  printed_page: 45
  importance: foundational
  tags: alternation
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.def.complexity.kozen2006-d-7-2
kind: definition
status: accepted
latex: |-
  Let ℓ* be the least fixed-point labeling of configurations by {0,1,⊥}. The machine accepts x when ℓ*(start(x)) = 1 and rejects x when ℓ*(start(x)) = 0; value ⊥ means neither acceptance nor rejection.
informal: |-
  Acceptance for alternating machines: Let ℓ* be the least fixed-point labeling of configurations by {0,1,⊥}. The machine accepts x when ℓ*(start(x)) = 1 and rejects x when ℓ*(start(x)) = 0; value ⊥ means neither acceptance nor rejection.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:D:7.2
  package_source_id: kozen2006
  module_id: kozen2006:7
  entry_type: Definition
  label: 7.2
  name: Acceptance for alternating machines
  pdf_page: 58
  printed_page: 47
  importance: foundational
  tags: alternation
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-7-3
kind: lemma
status: accepted
latex: |-
  Every alternating TM with NOT states can be simulated by an alternating TM using only AND and OR states, with no asymptotic increase in time or space.
informal: |-
  Eliminating negation states: Every alternating TM with NOT states can be simulated by an alternating TM using only AND and OR states, with no asymptotic increase in time or space.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:7.3
  package_source_id: kozen2006
  module_id: kozen2006:7
  entry_type: Lemma
  label: 7.3
  name: Eliminating negation states
  pdf_page: 58
  printed_page: 47
  importance: supporting
  tags: alternation
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-7-4
kind: theorem
status: accepted
latex: |-
  For T(n) ≥ n and S(n) ≥ log n: (i) ATIME(T) ⊆ DSPACE(T); (ii) DSPACE(S) ⊆ ATIME(S²); (iii) ASPACE(S) ⊆ DTIME(2^{O(S)}); and (iv) DTIME(T) ⊆ ASPACE(log T).
informal: |-
  Alternation simulation theorem: For T(n) ≥ n and S(n) ≥ log n: (i) ATIME(T) ⊆ DSPACE(T); (ii) DSPACE(S) ⊆ ATIME(S²); (iii) ASPACE(S) ⊆ DTIME(2^{O(S)}); and (iv) DTIME(T) ⊆ ASPACE(log T). Significance: Identifies alternation as the bridge between time and space.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:7.4
  package_source_id: kozen2006
  module_id: kozen2006:7
  entry_type: Theorem
  label: 7.4
  name: Alternation simulation theorem
  pdf_page: 59
  printed_page: 48
  importance: core
  tags: alternation
  extraction_scope: numbered formal statement
  review_status: curated
  significance: Identifies alternation as the bridge between time and space.
```

```yaml
id: st.cor.complexity.kozen2006-c-7-5
kind: corollary
status: accepted
latex: |-
  For T(n) ≥ n and S(n) ≥ log n, ATIME(T^{O(1)}) = DSPACE(T^{O(1)}) and ASPACE(S) = DTIME(2^{O(S)}).
informal: |-
  Alternation characterizations: For T(n) ≥ n and S(n) ≥ log n, ATIME(T^{O(1)}) = DSPACE(T^{O(1)}) and ASPACE(S) = DTIME(2^{O(S)}).
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.82
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:C:7.5
  package_source_id: kozen2006
  module_id: kozen2006:7
  entry_type: Corollary
  label: 7.5
  name: Alternation characterizations
  pdf_page: 60
  printed_page: 49
  importance: core
  tags: alternation
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.def.complexity.kozen2006-d-8-1
kind: definition
status: accepted
latex: |-
  QBF asks whether a fully quantified Boolean expression Q₁x₁…Qₙxₙ B(x₁,…,xₙ), with each Qᵢ ∈ {∃,∀}, is true over {0,1}.
informal: |-
  Quantified Boolean formula problem: QBF asks whether a fully quantified Boolean expression Q₁x₁…Qₙxₙ B(x₁,…,xₙ), with each Qᵢ ∈ {∃,∀}, is true over {0,1}.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:D:8.1
  package_source_id: kozen2006
  module_id: kozen2006:8
  entry_type: Definition
  label: 8.1
  name: Quantified Boolean formula problem
  pdf_page: 62
  printed_page: 51
  importance: foundational
  tags: pspace, complete-problems, games
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-8-2
kind: theorem
status: accepted
latex: |-
  QBF is complete for PSPACE under logspace many-one reductions.
informal: |-
  PSPACE-completeness of QBF: QBF is complete for PSPACE under logspace many-one reductions. Significance: Gives the canonical PSPACE-complete problem.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:8.2
  package_source_id: kozen2006
  module_id: kozen2006:8
  entry_type: Theorem
  label: 8.2
  name: PSPACE-completeness of QBF
  pdf_page: 62
  printed_page: 51
  importance: core
  tags: pspace, complete-problems, games
  extraction_scope: numbered formal statement
  review_status: curated
  significance: Gives the canonical PSPACE-complete problem.
```

```yaml
id: st.def.complexity.kozen2006-d-8-3
kind: definition
status: accepted
latex: |-
  For a two-player perfect-information game, checkmate(y) means y has no legal successor. The predicate win is the least fixed point satisfying win(x) iff there exists a move x→y such that every legal reply y→z leads to win(z) (with immediate checkmate covered vacuously).
informal: |-
  Forced-win predicate: For a two-player perfect-information game, checkmate(y) means y has no legal successor. The predicate win is the least fixed point satisfying win(x) iff there exists a move x→y such that every legal reply y→z leads to win(z) (with immediate checkmate covered vacuously).
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:D:8.3
  package_source_id: kozen2006
  module_id: kozen2006:8
  entry_type: Definition
  label: 8.3
  name: Forced-win predicate
  pdf_page: 64
  printed_page: 53
  importance: foundational
  tags: pspace, complete-problems, games
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-8-4
kind: theorem
status: accepted
latex: |-
  Generalized geography is complete for PSPACE under logspace many-one reductions.
informal: |-
  PSPACE-completeness of generalized geography: Generalized geography is complete for PSPACE under logspace many-one reductions.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:8.4
  package_source_id: kozen2006
  module_id: kozen2006:8
  entry_type: Theorem
  label: 8.4
  name: PSPACE-completeness of generalized geography
  pdf_page: 65
  printed_page: 54
  importance: core
  tags: pspace, complete-problems, games
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.def.complexity.kozen2006-d-9-1
kind: definition
status: accepted
latex: |-
  A Σₖ-machine is an alternating TM whose paths have at most k maximal blocks of like-typed configurations and begin with an OR block. A Πₖ-machine is defined dually and begins with an AND block; Σ₁ is nondeterminism and Σ₀ = Π₀ is determinism.
informal: |-
  Bounded-alternation machines: A Σₖ-machine is an alternating TM whose paths have at most k maximal blocks of like-typed configurations and begin with an OR block. A Πₖ-machine is defined dually and begins with an AND block; Σ₁ is nondeterminism and Σ₀ = Π₀ is determinism.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:D:9.1
  package_source_id: kozen2006
  module_id: kozen2006:9
  entry_type: Definition
  label: 9.1
  name: Bounded-alternation machines
  pdf_page: 68
  printed_page: 57
  importance: foundational
  tags: polynomial-hierarchy, oracles
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.def.complexity.kozen2006-d-9-2
kind: definition
status: accepted
latex: |-
  Σₖᵖ is the class accepted in polynomial time by Σₖ-machines, and Πₖᵖ is the class accepted in polynomial time by Πₖ-machines. Thus Σ₁ᵖ = NP, Π₁ᵖ = coNP, and Σ₀ᵖ = Π₀ᵖ = P.
informal: |-
  Levels of the polynomial hierarchy: Σₖᵖ is the class accepted in polynomial time by Σₖ-machines, and Πₖᵖ is the class accepted in polynomial time by Πₖ-machines. Thus Σ₁ᵖ = NP, Π₁ᵖ = coNP, and Σ₀ᵖ = Π₀ᵖ = P.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:D:9.2
  package_source_id: kozen2006
  module_id: kozen2006:9
  entry_type: Definition
  label: 9.2
  name: Levels of the polynomial hierarchy
  pdf_page: 69
  printed_page: 58
  importance: foundational
  tags: polynomial-hierarchy, oracles
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-9-3
kind: lemma
status: accepted
latex: |-
  For every k: Πₖᵖ = co-Σₖᵖ; Σₖᵖ ∪ Πₖᵖ ⊆ Σₖ₊₁ᵖ ∩ Πₖ₊₁ᵖ; and ⋃ₖΣₖᵖ = ⋃ₖΠₖᵖ ⊆ PSPACE.
informal: |-
  Basic polynomial-hierarchy relations: For every k: Πₖᵖ = co-Σₖᵖ; Σₖᵖ ∪ Πₖᵖ ⊆ Σₖ₊₁ᵖ ∩ Πₖ₊₁ᵖ; and ⋃ₖΣₖᵖ = ⋃ₖΠₖᵖ ⊆ PSPACE.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:9.3
  package_source_id: kozen2006
  module_id: kozen2006:9
  entry_type: Lemma
  label: 9.3
  name: Basic polynomial-hierarchy relations
  pdf_page: 69
  printed_page: 58
  importance: supporting
  tags: polynomial-hierarchy, oracles
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-9-4
kind: theorem
status: accepted
latex: |-
  The bounded alternating acceptance language Hₖ is complete for Σₖᵖ under logspace many-one reductions.
informal: |-
  Generic Σₖᵖ-complete problem: The bounded alternating acceptance language Hₖ is complete for Σₖᵖ under logspace many-one reductions.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:9.4
  package_source_id: kozen2006
  module_id: kozen2006:9
  entry_type: Theorem
  label: 9.4
  name: Generic Σₖᵖ-complete problem
  pdf_page: 70
  printed_page: 59
  importance: supporting
  tags: polynomial-hierarchy, oracles
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.cor.complexity.kozen2006-c-9-5
kind: corollary
status: accepted
latex: |-
  The complement of Hₖ is complete for Πₖᵖ under logspace many-one reductions.
informal: |-
  Generic Πₖᵖ-complete problem: The complement of Hₖ is complete for Πₖᵖ under logspace many-one reductions.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.82
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:C:9.5
  package_source_id: kozen2006
  module_id: kozen2006:9
  entry_type: Corollary
  label: 9.5
  name: Generic Πₖᵖ-complete problem
  pdf_page: 70
  printed_page: 59
  importance: supporting
  tags: polynomial-hierarchy, oracles
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.def.complexity.kozen2006-d-9-6
kind: definition
status: accepted
latex: |-
  For an oracle B, Pᴮ and NPᴮ are the languages accepted by polynomial-time deterministic and nondeterministic oracle machines using B. For a class C, Pᶜ = ⋃_{B∈C}Pᴮ and NPᶜ = ⋃_{B∈C}NPᴮ.
informal: |-
  Relativized polynomial classes: For an oracle B, Pᴮ and NPᴮ are the languages accepted by polynomial-time deterministic and nondeterministic oracle machines using B. For a class C, Pᶜ = ⋃_{B∈C}Pᴮ and NPᶜ = ⋃_{B∈C}NPᴮ.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:D:9.6
  package_source_id: kozen2006
  module_id: kozen2006:9
  entry_type: Definition
  label: 9.6
  name: Relativized polynomial classes
  pdf_page: 71
  printed_page: 60
  importance: foundational
  tags: polynomial-hierarchy, oracles
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.def.complexity.kozen2006-d-9-7
kind: definition
status: accepted
latex: |-
  A ≤ᵀᵖ B means A ∈ Pᴮ; this is polynomial-time Turing (Cook) reducibility.
informal: |-
  Polynomial-time Turing reduction: A ≤ᵀᵖ B means A ∈ Pᴮ; this is polynomial-time Turing (Cook) reducibility.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:D:9.7
  package_source_id: kozen2006
  module_id: kozen2006:9
  entry_type: Definition
  label: 9.7
  name: Polynomial-time Turing reduction
  pdf_page: 72
  printed_page: 61
  importance: foundational
  tags: polynomial-hierarchy, oracles
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-9-8
kind: theorem
status: accepted
latex: |-
  Define NP₁ = NP and NPₖ₊₁ = NP^{NPₖ}. Then NPₖ = Σₖᵖ for every k ≥ 1.
informal: |-
  Oracle definition of PH: Define NP₁ = NP and NPₖ₊₁ = NP^{NPₖ}. Then NPₖ = Σₖᵖ for every k ≥ 1.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:9.8
  package_source_id: kozen2006
  module_id: kozen2006:9
  entry_type: Theorem
  label: 9.8
  name: Oracle definition of PH
  pdf_page: 72
  printed_page: 61
  importance: core
  tags: polynomial-hierarchy, oracles
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-10-1
kind: theorem
status: accepted
latex: |-
  For every k ≥ 1, the iterated-oracle class NPₖ equals the alternating-machine class Σₖᵖ.
informal: |-
  Equivalence of PH definitions: For every k ≥ 1, the iterated-oracle class NPₖ equals the alternating-machine class Σₖᵖ.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:10.1
  package_source_id: kozen2006
  module_id: kozen2006:10
  entry_type: Theorem
  label: 10.1
  name: Equivalence of PH definitions
  pdf_page: 73
  printed_page: 62
  importance: core
  tags: polynomial-hierarchy, quantifiers
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-10-2
kind: theorem
status: accepted
latex: |-
  A language A is in Σₖᵖ iff there are a polynomial-time predicate R and constant c such that x ∈ A exactly when ∃y₁∀y₂∃y₃…Qₖyₖ R(x,y₁,…,yₖ), where every |yᵢ| ≤ |x|ᶜ and Qₖ is ∃ for odd k and ∀ for even k.
informal: |-
  Quantifier characterization of Σₖᵖ: A language A is in Σₖᵖ iff there are a polynomial-time predicate R and constant c such that x ∈ A exactly when ∃y₁∀y₂∃y₃…Qₖyₖ R(x,y₁,…,yₖ), where every |yᵢ| ≤ |x|ᶜ and Qₖ is ∃ for odd k and ∀ for even k.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:10.2
  package_source_id: kozen2006
  module_id: kozen2006:10
  entry_type: Theorem
  label: 10.2
  name: Quantifier characterization of Σₖᵖ
  pdf_page: 76
  printed_page: 65
  importance: core
  tags: polynomial-hierarchy, quantifiers
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.def.complexity.kozen2006-d-11-1
kind: definition
status: accepted
latex: |-
  A logspace-uniform circuit family has n-input circuits Cₙ of polynomial size and polylogarithmic depth, constructible from 0ⁿ by a logspace transducer. NC is the class of languages decided by such Boolean circuit families.
informal: |-
  Uniform-circuit definition of NC: A logspace-uniform circuit family has n-input circuits Cₙ of polynomial size and polylogarithmic depth, constructible from 0ⁿ by a logspace transducer. NC is the class of languages decided by such Boolean circuit families.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:D:11.1
  package_source_id: kozen2006
  module_id: kozen2006:11
  entry_type: Definition
  label: 11.1
  name: Uniform-circuit definition of NC
  pdf_page: 78
  printed_page: 67
  importance: foundational
  tags: parallel-complexity, nc, circuits
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.def.complexity.kozen2006-d-11-2
kind: definition
status: accepted
latex: |-
  STA(S,T,A) consists of languages accepted by alternating TMs simultaneously bounded by space S(n), time T(n), and A(n) alternations. An asterisk means no bound; Σ or Π may specify the initial branch type.
informal: |-
  STA classes: STA(S,T,A) consists of languages accepted by alternating TMs simultaneously bounded by space S(n), time T(n), and A(n) alternations. An asterisk means no bound; Σ or Π may specify the initial branch type.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:D:11.2
  package_source_id: kozen2006
  module_id: kozen2006:11
  entry_type: Definition
  label: 11.2
  name: STA classes
  pdf_page: 80
  printed_page: 69
  importance: foundational
  tags: parallel-complexity, nc, circuits
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-11-3
kind: theorem
status: accepted
latex: |-
  NC = STA(log n, *, (log n)^{O(1)}).
informal: |-
  Ruzzo’s characterization of NC: NC = STA(log n, *, (log n)^{O(1)}).
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:11.3
  package_source_id: kozen2006
  module_id: kozen2006:11
  entry_type: Theorem
  label: 11.3
  name: Ruzzo’s characterization of NC
  pdf_page: 80
  printed_page: 69
  importance: core
  tags: parallel-complexity, nc, circuits
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-12-1
kind: theorem
status: accepted
latex: |-
  NC = STA(log n, *, (log n)^{O(1)}).
informal: |-
  Ruzzo’s characterization of NC: NC = STA(log n, *, (log n)^{O(1)}).
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:12.1
  package_source_id: kozen2006
  module_id: kozen2006:12
  entry_type: Theorem
  label: 12.1
  name: Ruzzo’s characterization of NC
  pdf_page: 81
  printed_page: 70
  importance: core
  tags: parallel-complexity, nc, alternation
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.def.complexity.kozen2006-d-13-1
kind: definition
status: accepted
latex: |-
  A language is in RP if a polynomial-time randomized TM accepts yes-instances with probability at least 3/4 and never accepts no-instances. It is in BPP if the same machine errs with probability at most 1/4 on every input.
informal: |-
  RP and BPP: A language is in RP if a polynomial-time randomized TM accepts yes-instances with probability at least 3/4 and never accepts no-instances. It is in BPP if the same machine errs with probability at most 1/4 on every input.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:D:13.1
  package_source_id: kozen2006
  module_id: kozen2006:13
  entry_type: Definition
  label: 13.1
  name: RP and BPP
  pdf_page: 89
  printed_page: 78
  importance: foundational
  tags: randomized-computation, polynomial-identity-testing
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-13-2
kind: theorem
status: accepted
latex: |-
  If p is a nonzero n-variate polynomial of total degree d over a field F and S ⊆ F, then p has at most d|S|^{n-1} zeros in Sⁿ.
informal: |-
  Schwartz–Zippel lemma: If p is a nonzero n-variate polynomial of total degree d over a field F and S ⊆ F, then p has at most d|S|^{n-1} zeros in Sⁿ.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:13.2
  package_source_id: kozen2006
  module_id: kozen2006:13
  entry_type: Theorem
  label: 13.2
  name: Schwartz–Zippel lemma
  pdf_page: 90
  printed_page: 79
  importance: core
  tags: randomized-computation, polynomial-identity-testing
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.cor.complexity.kozen2006-c-13-3
kind: corollary
status: accepted
latex: |-
  Under the hypotheses of Schwartz–Zippel, a uniformly random s ∈ Sⁿ satisfies p(s)=0 with probability at most d/|S|.
informal: |-
  Random evaluation bound: Under the hypotheses of Schwartz–Zippel, a uniformly random s ∈ Sⁿ satisfies p(s)=0 with probability at most d/|S|.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.82
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:C:13.3
  package_source_id: kozen2006
  module_id: kozen2006:13
  entry_type: Corollary
  label: 13.3
  name: Random evaluation bound
  pdf_page: 90
  printed_page: 79
  importance: supporting
  tags: randomized-computation, polynomial-identity-testing
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-14-1
kind: lemma
status: accepted
latex: |-
  For every polynomial nᵈ, an RP algorithm can be amplified so that yes-instances are accepted with probability at least 1−2^{-nᵈ} while no-instances are never accepted. A BPP algorithm can be amplified so that its error is at most 2^{-nᵈ}.
informal: |-
  Amplification lemma: For every polynomial nᵈ, an RP algorithm can be amplified so that yes-instances are accepted with probability at least 1−2^{-nᵈ} while no-instances are never accepted. A BPP algorithm can be amplified so that its error is at most 2^{-nᵈ}.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:14.1
  package_source_id: kozen2006
  module_id: kozen2006:14
  entry_type: Lemma
  label: 14.1
  name: Amplification lemma
  pdf_page: 93
  printed_page: 82
  importance: core
  tags: bpp, polynomial-hierarchy
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-b-1
kind: theorem
status: accepted
latex: |-
  For pairwise coprime positive integers n₁,…,nₖ and n = ∏ᵢnᵢ, the map x mod n ↦ (x mod n₁,…,x mod nₖ) is a ring isomorphism Zₙ ≅ Z_{n₁}×…×Z_{nₖ}.
informal: |-
  Chinese remainder theorem: For pairwise coprime positive integers n₁,…,nₖ and n = ∏ᵢnᵢ, the map x mod n ↦ (x mod n₁,…,x mod nₖ) is a ring isomorphism Zₙ ≅ Z_{n₁}×…×Z_{nₖ}.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:B.1
  package_source_id: kozen2006
  module_id: kozen2006:B
  entry_type: Theorem
  label: B.1
  name: Chinese remainder theorem
  pdf_page: 97
  printed_page: 86
  importance: supporting
  tags: number-theory, chinese-remainder
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-b-2
kind: theorem
status: accepted
latex: |-
  If I₁,…,Iₖ are pairwise comaximal ideals of a commutative ring R and I = ⋂ᵢIᵢ, then R/I ≅ R/I₁×…×R/Iₖ via [x]_I ↦ ([x]_{I₁},…,[x]_{Iₖ}).
informal: |-
  Chinese remainder theorem for ideals: If I₁,…,Iₖ are pairwise comaximal ideals of a commutative ring R and I = ⋂ᵢIᵢ, then R/I ≅ R/I₁×…×R/Iₖ via [x]_I ↦ ([x]_{I₁},…,[x]_{Iₖ}).
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:B.2
  package_source_id: kozen2006
  module_id: kozen2006:B
  entry_type: Theorem
  label: B.2
  name: Chinese remainder theorem for ideals
  pdf_page: 99
  printed_page: 88
  importance: supporting
  tags: number-theory, chinese-remainder
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-c-1
kind: lemma
status: accepted
latex: |-
  An integer p ≥ 2 is prime iff some element of {1,…,p−1} has multiplicative order p−1 modulo p.
informal: |-
  Fermat’s theorem / primitive root criterion: An integer p ≥ 2 is prime iff some element of {1,…,p−1} has multiplicative order p−1 modulo p.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:C.1
  package_source_id: kozen2006
  module_id: kozen2006:C
  entry_type: Lemma
  label: C.1
  name: Fermat’s theorem / primitive root criterion
  pdf_page: 102
  printed_page: 91
  importance: supporting
  tags: primality, number-theory
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-c-2
kind: lemma
status: accepted
latex: |-
  For every positive integer n, ∑_{m|n} φ(m) = n.
informal: |-
  Euler totient divisor identity: For every positive integer n, ∑_{m|n} φ(m) = n.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:C.2
  package_source_id: kozen2006
  module_id: kozen2006:C
  entry_type: Lemma
  label: C.2
  name: Euler totient divisor identity
  pdf_page: 103
  printed_page: 92
  importance: supporting
  tags: primality, number-theory
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-c-3
kind: lemma
status: accepted
latex: |-
  For k dividing q−1, the polynomial Φₖ whose roots are the elements of GF(q)* of order k has degree φ(k).
informal: |-
  Degree of the order polynomial: For k dividing q−1, the polynomial Φₖ whose roots are the elements of GF(q)* of order k has degree φ(k).
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:C.3
  package_source_id: kozen2006
  module_id: kozen2006:C
  entry_type: Lemma
  label: C.3
  name: Degree of the order polynomial
  pdf_page: 103
  printed_page: 92
  importance: supporting
  tags: primality, number-theory
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-c-4
kind: theorem
status: accepted
latex: |-
  The language PRIMES belongs to NP ∩ coNP.
informal: |-
  Pratt’s primality theorem: The language PRIMES belongs to NP ∩ coNP.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:C.4
  package_source_id: kozen2006
  module_id: kozen2006:C
  entry_type: Theorem
  label: C.4
  name: Pratt’s primality theorem
  pdf_page: 104
  printed_page: 93
  importance: supporting
  tags: primality, number-theory
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.def.complexity.kozen2006-d-15-1
kind: definition
status: accepted
latex: |-
  A protocol (P,V) is an interactive proof for A when V is probabilistic polynomial time, yes-instances are accepted with probability at least 3/4 with the honest prover, and no-instances are accepted with probability at most 1/4 against every prover strategy. IP is the class of languages with such protocols.
informal: |-
  Interactive proof system: A protocol (P,V) is an interactive proof for A when V is probabilistic polynomial time, yes-instances are accepted with probability at least 3/4 with the honest prover, and no-instances are accepted with probability at most 1/4 against every prover strategy. IP is the class of languages with such protocols.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:D:15.1
  package_source_id: kozen2006
  module_id: kozen2006:15
  entry_type: Definition
  label: 15.1
  name: Interactive proof system
  pdf_page: 111
  printed_page: 100
  importance: foundational
  tags: interactive-proofs
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.def.complexity.kozen2006-d-16-1
kind: definition
status: accepted
latex: |-
  A QBF is simple when negations apply only to variables and, between any free occurrence of a variable in a quantified subformula and its binding quantifier, there is at most one intervening universal quantifier.
informal: |-
  Simple quantified Boolean formula: A QBF is simple when negations apply only to variables and, between any free occurrence of a variable in a quantified subformula and its binding quantifier, there is at most one intervening universal quantifier.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:D:16.1
  package_source_id: kozen2006
  module_id: kozen2006:16
  entry_type: Definition
  label: 16.1
  name: Simple quantified Boolean formula
  pdf_page: 115
  printed_page: 104
  importance: foundational
  tags: interactive-proofs, pspace, arithmetization
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-16-2
kind: lemma
status: accepted
latex: |-
  Every quantified Boolean formula can be transformed in logspace into an equivalent simple formula with at most quadratic growth in size.
informal: |-
  Simplifying QBFs: Every quantified Boolean formula can be transformed in logspace into an equivalent simple formula with at most quadratic growth in size.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:16.2
  package_source_id: kozen2006
  module_id: kozen2006:16
  entry_type: Lemma
  label: 16.2
  name: Simplifying QBFs
  pdf_page: 115
  printed_page: 104
  importance: supporting
  tags: interactive-proofs, pspace, arithmetization
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-16-3
kind: lemma
status: accepted
latex: |-
  If ∑_{x∈{0,1}}D(x) or ∏_{x∈{0,1}}D(x) arises by arithmetizing a simple Boolean formula, then D(x) is equivalent modulo p to a polynomial over Zₚ whose degree is linear in the expression size.
informal: |-
  Low-degree arithmetization: If ∑_{x∈{0,1}}D(x) or ∏_{x∈{0,1}}D(x) arises by arithmetizing a simple Boolean formula, then D(x) is equivalent modulo p to a polynomial over Zₚ whose degree is linear in the expression size.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:16.3
  package_source_id: kozen2006
  module_id: kozen2006:16
  entry_type: Lemma
  label: 16.3
  name: Low-degree arithmetization
  pdf_page: 118
  printed_page: 107
  importance: supporting
  tags: interactive-proofs, pspace, arithmetization
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-16-4
kind: lemma
status: accepted
latex: |-
  A nonzero polynomial d(x) ∈ Zₚ[x] of degree at most n vanishes at a uniformly random element of Zₚ with probability at most n/p.
informal: |-
  Univariate root bound: A nonzero polynomial d(x) ∈ Zₚ[x] of degree at most n vanishes at a uniformly random element of Zₚ with probability at most n/p.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:16.4
  package_source_id: kozen2006
  module_id: kozen2006:16
  entry_type: Lemma
  label: 16.4
  name: Univariate root bound
  pdf_page: 118
  printed_page: 107
  importance: supporting
  tags: interactive-proofs, pspace, arithmetization
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-18-1
kind: theorem
status: accepted
latex: |-
  NP = PCP(log n, 1): every NP language has a verifier using O(log n) random bits and O(1) proof queries, with perfect completeness and constant soundness.
informal: |-
  PCP theorem: NP = PCP(log n, 1): every NP language has a verifier using O(log n) random bits and O(1) proof queries, with perfect completeness and constant soundness. Significance: Foundation of modern hardness of approximation.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:18.1
  package_source_id: kozen2006
  module_id: kozen2006:18
  entry_type: Theorem
  label: 18.1
  name: PCP theorem
  pdf_page: 125
  printed_page: 114
  importance: core
  tags: pcp, approximation
  extraction_scope: numbered formal statement
  review_status: curated
  significance: Foundation of modern hardness of approximation.
```

```yaml
id: st.lem.complexity.kozen2006-l-18-2
kind: lemma
status: accepted
latex: |-
  There is a polynomial-time algorithm that, for a 3CNF formula with m clauses and three distinct variables per clause, finds an assignment satisfying at least 7m/8 clauses.
informal: |-
  7/8 approximation for MAX-3SAT: There is a polynomial-time algorithm that, for a 3CNF formula with m clauses and three distinct variables per clause, finds an assignment satisfying at least 7m/8 clauses.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:18.2
  package_source_id: kozen2006
  module_id: kozen2006:18
  entry_type: Lemma
  label: 18.2
  name: 7/8 approximation for MAX-3SAT
  pdf_page: 126
  printed_page: 115
  importance: supporting
  tags: pcp, approximation
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-18-3
kind: theorem
status: accepted
latex: |-
  A polynomial-time constant-factor approximation algorithm for MAX-CLIQUE exists for some fixed α>0 iff P = NP.
informal: |-
  Hardness of approximating MAX-CLIQUE: A polynomial-time constant-factor approximation algorithm for MAX-CLIQUE exists for some fixed α>0 iff P = NP.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:18.3
  package_source_id: kozen2006
  module_id: kozen2006:18
  entry_type: Theorem
  label: 18.3
  name: Hardness of approximating MAX-CLIQUE
  pdf_page: 127
  printed_page: 116
  importance: core
  tags: pcp, approximation
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-18-4
kind: theorem
status: accepted
latex: |-
  MAX-3SAT has a polynomial-time approximation scheme iff P = NP.
informal: |-
  Hardness of a PTAS for MAX-3SAT: MAX-3SAT has a polynomial-time approximation scheme iff P = NP.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:18.4
  package_source_id: kozen2006
  module_id: kozen2006:18
  entry_type: Theorem
  label: 18.4
  name: Hardness of a PTAS for MAX-3SAT
  pdf_page: 127
  printed_page: 116
  importance: core
  tags: pcp, approximation
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-19-1
kind: lemma
status: accepted
latex: |-
  Let F=Zₚ and V be finite-dimensional. If ε<1/6 and Pr_{u,v}[f(u+v)=f(u)+f(v)]>1−ε, then there is a linear g:V→F agreeing with f on at least a 1−3ε fraction of V.
informal: |-
  Linearity testing lemma: Let F=Zₚ and V be finite-dimensional. If ε<1/6 and Pr_{u,v}[f(u+v)=f(u)+f(v)]>1−ε, then there is a linear g:V→F agreeing with f on at least a 1−3ε fraction of V.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:19.1
  package_source_id: kozen2006
  module_id: kozen2006:19
  entry_type: Lemma
  label: 19.1
  name: Linearity testing lemma
  pdf_page: 133
  printed_page: 122
  importance: supporting
  tags: pcp, linearity-testing
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-21-1
kind: theorem
status: accepted
latex: |-
  Any two countable dense linear orders without endpoints are isomorphic. More generally, every finite local isomorphism between such orders extends to a full isomorphism.
informal: |-
  Back-and-forth theorem for dense orders: Any two countable dense linear orders without endpoints are isomorphic. More generally, every finite local isomorphism between such orders extends to a full isomorphism.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:21.1
  package_source_id: kozen2006
  module_id: kozen2006:21
  entry_type: Theorem
  label: 21.1
  name: Back-and-forth theorem for dense orders
  pdf_page: 147
  printed_page: 136
  importance: supporting
  tags: logic, decision-procedures, pspace
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-21-2
kind: theorem
status: accepted
latex: |-
  The first-order theory of dense linear orders without endpoints is PSPACE-complete.
informal: |-
  Complexity of dense linear order: The first-order theory of dense linear orders without endpoints is PSPACE-complete.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:21.2
  package_source_id: kozen2006
  module_id: kozen2006:21
  entry_type: Theorem
  label: 21.2
  name: Complexity of dense linear order
  pdf_page: 150
  printed_page: 139
  importance: core
  tags: logic, decision-procedures, pspace
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.def.complexity.kozen2006-d-22-1
kind: definition
status: accepted
latex: |-
  An integer affine function f:Rᵏ→R has the form c₀+∑ᵢcᵢxᵢ with integer coefficients. Its norm is ‖f‖ = max_{0≤i≤k}|cᵢ|; Aₘᵏ denotes those with norm at most m.
informal: |-
  Integer affine functions: An integer affine function f:Rᵏ→R has the form c₀+∑ᵢcᵢxᵢ with integer coefficients. Its norm is ‖f‖ = max_{0≤i≤k}|cᵢ|; Aₘᵏ denotes those with norm at most m.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:D:22.1
  package_source_id: kozen2006
  module_id: kozen2006:22
  entry_type: Definition
  label: 22.1
  name: Integer affine functions
  pdf_page: 152
  printed_page: 141
  importance: foundational
  tags: logic, real-addition
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.def.complexity.kozen2006-d-22-2
kind: definition
status: accepted
latex: |-
  For a,b∈Rᵏ, define a ≡ₘᵏ b when every integer affine f with ‖f‖≤m has the same sign on a and b; equivalently, a and b satisfy the same bounded-coefficient linear inequalities.
informal: |-
  Bounded affine equivalence: For a,b∈Rᵏ, define a ≡ₘᵏ b when every integer affine f with ‖f‖≤m has the same sign on a and b; equivalently, a and b satisfy the same bounded-coefficient linear inequalities.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:D:22.2
  package_source_id: kozen2006
  module_id: kozen2006:22
  entry_type: Definition
  label: 22.2
  name: Bounded affine equivalence
  pdf_page: 152
  printed_page: 141
  importance: foundational
  tags: logic, real-addition
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-22-3
kind: lemma
status: accepted
latex: |-
  If a ≡_{2m²}ᵏ b, then for every a′∈R there is b′∈R such that (a,a′) ≡ₘ^{k+1} (b,b′).
informal: |-
  One-step extension lemma: If a ≡_{2m²}ᵏ b, then for every a′∈R there is b′∈R such that (a,a′) ≡ₘ^{k+1} (b,b′).
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:22.3
  package_source_id: kozen2006
  module_id: kozen2006:22
  entry_type: Lemma
  label: 22.3
  name: One-step extension lemma
  pdf_page: 152
  printed_page: 141
  importance: technical
  tags: logic, real-addition
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-22-4
kind: lemma
status: accepted
latex: |-
  If σ is the ≡_{2m²}ᵏ-class of a, then points of the form (a,f(a)/c), with f∈A_{2m²}ᵏ and |c|≤2m², include a representative of every ≡ₘ^{k+1}-class consistent with σ.
informal: |-
  Finite representatives lemma: If σ is the ≡_{2m²}ᵏ-class of a, then points of the form (a,f(a)/c), with f∈A_{2m²}ᵏ and |c|≤2m², include a representative of every ≡ₘ^{k+1}-class consistent with σ.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:22.4
  package_source_id: kozen2006
  module_id: kozen2006:22
  entry_type: Lemma
  label: 22.4
  name: Finite representatives lemma
  pdf_page: 153
  printed_page: 142
  importance: technical
  tags: logic, real-addition
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-22-5
kind: lemma
status: accepted
latex: |-
  If a ≡_{r(n,ℓ)}ᵏ b, then a and b agree on every reduced formula with at most n quantifiers and integer constants of magnitude at most ℓ.
informal: |-
  Logical invariance under bounded affine equivalence: If a ≡_{r(n,ℓ)}ᵏ b, then a and b agree on every reduced formula with at most n quantifiers and integer constants of magnitude at most ℓ.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:22.5
  package_source_id: kozen2006
  module_id: kozen2006:22
  entry_type: Lemma
  label: 22.5
  name: Logical invariance under bounded affine equivalence
  pdf_page: 154
  printed_page: 143
  importance: technical
  tags: logic, real-addition
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-22-6
kind: theorem
status: accepted
latex: |-
  The first-order theory Th(R,+,≤) belongs to STA(*,2^{O(n)},n).
informal: |-
  Upper bound for real addition: The first-order theory Th(R,+,≤) belongs to STA(*,2^{O(n)},n).
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:22.6
  package_source_id: kozen2006
  module_id: kozen2006:22
  entry_type: Theorem
  label: 22.6
  name: Upper bound for real addition
  pdf_page: 155
  printed_page: 144
  importance: core
  tags: logic, real-addition
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-23-1
kind: lemma
status: accepted
latex: |-
  For Iₙ={z∈Z:0≤z<2^{2ⁿ}}, one has Iₙ₊₁ = {z₁z₂+z₃+z₄ : z₁,z₂,z₃,z₄∈Iₙ}.
informal: |-
  Recursive decomposition of large integer ranges: For Iₙ={z∈Z:0≤z<2^{2ⁿ}}, one has Iₙ₊₁ = {z₁z₂+z₃+z₄ : z₁,z₂,z₃,z₄∈Iₙ}.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:23.1
  package_source_id: kozen2006
  module_id: kozen2006:23
  entry_type: Lemma
  label: 23.1
  name: Recursive decomposition of large integer ranges
  pdf_page: 159
  printed_page: 148
  importance: technical
  tags: logic, lower-bounds, real-addition
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-25-3
kind: theorem
status: accepted
latex: |-
  (i) Every S1S formula φ(x,X) can be translated into a Muller automaton whose accepted track encodings are exactly the tuples satisfying φ. (ii) Every nondeterministic Büchi automaton over {0,1} can be translated into an S1S formula defining the sets whose characteristic strings it accepts.
informal: |-
  S1S–automata correspondence: (i) Every S1S formula φ(x,X) can be translated into a Muller automaton whose accepted track encodings are exactly the tuples satisfying φ. (ii) Every nondeterministic Büchi automaton over {0,1} can be translated into an S1S formula defining the sets whose characteristic strings it accepts.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:25.3
  package_source_id: kozen2006
  module_id: kozen2006:25
  entry_type: Theorem
  label: 25.3
  name: S1S–automata correspondence
  pdf_page: 169
  printed_page: 158
  importance: core
  tags: omega-automata, s1s
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-26-1
kind: lemma
status: accepted
latex: |-
  Every infinite tree of finite branching degree has an infinite path.
informal: |-
  König’s lemma: Every infinite tree of finite branching degree has an infinite path.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:26.1
  package_source_id: kozen2006
  module_id: kozen2006:26
  entry_type: Lemma
  label: 26.1
  name: König’s lemma
  pdf_page: 176
  printed_page: 165
  importance: supporting
  tags: omega-automata, determinization
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-27-2
kind: theorem
status: accepted
latex: |-
  Every n-state nondeterministic Büchi automaton can be simulated by a deterministic Rabin automaton with at most 2^{O(n log n)} states and n Rabin pairs.
informal: |-
  Safra determinization theorem: Every n-state nondeterministic Büchi automaton can be simulated by a deterministic Rabin automaton with at most 2^{O(n log n)} states and n Rabin pairs.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:27.2
  package_source_id: kozen2006
  module_id: kozen2006:27
  entry_type: Theorem
  label: 27.2
  name: Safra determinization theorem
  pdf_page: 181
  printed_page: 170
  importance: core
  tags: omega-automata, safra
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-28-1
kind: theorem
status: accepted
latex: |-
  There exists a recursive oracle A such that Pᴬ = NPᴬ.
informal: |-
  Oracle collapsing P and NP: There exists a recursive oracle A such that Pᴬ = NPᴬ.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:28.1
  package_source_id: kozen2006
  module_id: kozen2006:28
  entry_type: Theorem
  label: 28.1
  name: Oracle collapsing P and NP
  pdf_page: 183
  printed_page: 172
  importance: core
  tags: oracles, relativization
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-28-2
kind: theorem
status: accepted
latex: |-
  There exists a recursive oracle B such that Pᴮ ≠ NPᴮ.
informal: |-
  Oracle separating P and NP: There exists a recursive oracle B such that Pᴮ ≠ NPᴮ.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:28.2
  package_source_id: kozen2006
  module_id: kozen2006:28
  entry_type: Theorem
  label: 28.2
  name: Oracle separating P and NP
  pdf_page: 183
  printed_page: 172
  importance: core
  tags: oracles, relativization
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-29-1
kind: theorem
status: accepted
latex: |-
  If a sparse language is polynomial-time many-one hard for coNP, then P = NP.
informal: |-
  Fortune’s sparse-hard-set theorem: If a sparse language is polynomial-time many-one hard for coNP, then P = NP.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:29.1
  package_source_id: kozen2006
  module_id: kozen2006:29
  entry_type: Theorem
  label: 29.1
  name: Fortune’s sparse-hard-set theorem
  pdf_page: 187
  printed_page: 176
  importance: core
  tags: sparse-sets, np-completeness
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-29-2
kind: theorem
status: accepted
latex: |-
  If a sparse language is polynomial-time many-one complete for NP, then P = NP.
informal: |-
  Mahaney’s theorem: If a sparse language is polynomial-time many-one complete for NP, then P = NP.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:29.2
  package_source_id: kozen2006
  module_id: kozen2006:29
  entry_type: Theorem
  label: 29.2
  name: Mahaney’s theorem
  pdf_page: 188
  printed_page: 177
  importance: core
  tags: sparse-sets, np-completeness
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-f-1
kind: lemma
status: accepted
latex: |-
  Let S be a nonempty subset of GF(2)ⁿ, and choose a random nested tower E₀⊂…⊂Eₙ with dim(Eᵢ)=i. Then Pr[there exists i with |S∩Eᵢ|=1] ≥ 3/4.
informal: |-
  Random subspace isolation lemma: Let S be a nonempty subset of GF(2)ⁿ, and choose a random nested tower E₀⊂…⊂Eₙ with dim(Eᵢ)=i. Then Pr[there exists i with |S∩Eᵢ|=1] ≥ 3/4.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:F.1
  package_source_id: kozen2006
  module_id: kozen2006:F
  entry_type: Lemma
  label: F.1
  name: Random subspace isolation lemma
  pdf_page: 192
  printed_page: 181
  importance: technical
  tags: unique-sat, randomized-reductions
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-f-2
kind: theorem
status: accepted
latex: |-
  NP ⊆ RP^USAT: every NP language has a randomized polynomial-time reduction to unique satisfiability.
informal: |-
  Valiant–Vazirani theorem: NP ⊆ RP^USAT: every NP language has a randomized polynomial-time reduction to unique satisfiability.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:F.2
  package_source_id: kozen2006
  module_id: kozen2006:F
  entry_type: Theorem
  label: F.2
  name: Valiant–Vazirani theorem
  pdf_page: 194
  printed_page: 183
  importance: core
  tags: unique-sat, randomized-reductions
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-g-1
kind: theorem
status: accepted
latex: |-
  PH ⊆ P^#P.
informal: |-
  Toda’s theorem: PH ⊆ P^#P. Significance: Shows the entire polynomial hierarchy is controlled by a counting oracle.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:G.1
  package_source_id: kozen2006
  module_id: kozen2006:G
  entry_type: Theorem
  label: G.1
  name: Toda’s theorem
  pdf_page: 198
  printed_page: 187
  importance: core
  tags: counting-complexity, toda
  extraction_scope: numbered formal statement
  review_status: curated
  significance: Shows the entire polynomial hierarchy is controlled by a counting oracle.
```

```yaml
id: st.lem.complexity.kozen2006-l-g-2
kind: lemma
status: accepted
latex: |-
  For every class C downward closed under polynomial-time Turing reductions: (i) Σᵖ·C ⊆ R·Σˡᵒᵍ·⊕·C; (ii) Πˡᵒᵍ·⊕·C ⊆ ⊕·C; (iii) ⊕·BP·C ⊆ BP·⊕·C; (iv) BP·BP·C ⊆ BP·C; (v) ⊕·⊕·C ⊆ ⊕·C; and (vi) BP·C and ⊕·C are downward closed under ≤ᵀᵖ.
informal: |-
  Operator identities used in Toda’s theorem: For every class C downward closed under polynomial-time Turing reductions: (i) Σᵖ·C ⊆ R·Σˡᵒᵍ·⊕·C; (ii) Πˡᵒᵍ·⊕·C ⊆ ⊕·C; (iii) ⊕·BP·C ⊆ BP·⊕·C; (iv) BP·BP·C ⊆ BP·C; (v) ⊕·⊕·C ⊆ ⊕·C; and (vi) BP·C and ⊕·C are downward closed under ≤ᵀᵖ.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:G.2
  package_source_id: kozen2006
  module_id: kozen2006:G
  entry_type: Lemma
  label: G.2
  name: Operator identities used in Toda’s theorem
  pdf_page: 198
  printed_page: 187
  importance: technical
  tags: counting-complexity, toda
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-30-1
kind: theorem
status: accepted
latex: |-
  If parity has no depth-d circuit family of size 2^{(log n)^c} for any constants c and d, then some oracle A satisfies PHᴬ ≠ PSPACEᴬ.
informal: |-
  Circuit lower bounds imply oracle separation: If parity has no depth-d circuit family of size 2^{(log n)^c} for any constants c and d, then some oracle A satisfies PHᴬ ≠ PSPACEᴬ.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:30.1
  package_source_id: kozen2006
  module_id: kozen2006:30
  entry_type: Theorem
  label: 30.1
  name: Circuit lower bounds imply oracle separation
  pdf_page: 205
  printed_page: 194
  importance: core
  tags: circuit-complexity, oracles
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-31-1
kind: lemma
status: accepted
latex: |-
  Under the lecture’s random partial valuation, the probability that fewer than √n/2 variables remain unassigned is at most (2/e)^{√n/2}.
informal: |-
  Many variables survive a random restriction: Under the lecture’s random partial valuation, the probability that fewer than √n/2 variables remain unassigned is at most (2/e)^{√n/2}.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:31.1
  package_source_id: kozen2006
  module_id: kozen2006:31
  entry_type: Lemma
  label: 31.1
  name: Many variables survive a random restriction
  pdf_page: 210
  printed_page: 199
  importance: technical
  tags: circuit-lower-bounds, random-restrictions
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-31-2
kind: lemma
status: accepted
latex: |-
  For a constant c and a variable set A with c ≤ |A| and |A| = o(n^{1/c}), the probability that a random partial valuation leaves more than c variables of A unassigned is at most n^{1−c/2} for all sufficiently large n.
informal: |-
  Few variables survive inside a small set: For a constant c and a variable set A with c ≤ |A| and |A| = o(n^{1/c}), the probability that a random partial valuation leaves more than c variables of A unassigned is at most n^{1−c/2} for all sufficiently large n.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:31.2
  package_source_id: kozen2006
  module_id: kozen2006:31
  entry_type: Lemma
  label: 31.2
  name: Few variables survive inside a small set
  pdf_page: 210
  printed_page: 199
  importance: technical
  tags: circuit-lower-bounds, random-restrictions
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-31-3
kind: lemma
status: accepted
latex: |-
  Let S contain at least b log n pairwise disjoint variable sets, each of size <a. If E(A) is the event that all variables in A are assigned 0, then for sufficiently large n the probability that no E(A) occurs is at most n^{b log(1−2^{-a})}.
informal: |-
  Hitting many disjoint small sets: Let S contain at least b log n pairwise disjoint variable sets, each of size <a. If E(A) is the event that all variables in A are assigned 0, then for sufficiently large n the probability that no E(A) occurs is at most n^{b log(1−2^{-a})}.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:31.3
  package_source_id: kozen2006
  module_id: kozen2006:31
  entry_type: Lemma
  label: 31.3
  name: Hitting many disjoint small sets
  pdf_page: 211
  printed_page: 200
  importance: technical
  tags: circuit-lower-bounds, random-restrictions
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-31-4
kind: lemma
status: accepted
latex: |-
  If parity has polynomial-size depth-d circuits, then it has polynomial-size depth-d t-circuits for some constant t.
informal: |-
  Bounded bottom fan-in: If parity has polynomial-size depth-d circuits, then it has polynomial-size depth-d t-circuits for some constant t.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:31.4
  package_source_id: kozen2006
  module_id: kozen2006:31
  entry_type: Lemma
  label: 31.4
  name: Bounded bottom fan-in
  pdf_page: 211
  printed_page: 200
  importance: technical
  tags: circuit-lower-bounds, random-restrictions
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-31-5
kind: lemma
status: accepted
latex: |-
  If parity has polynomial-size depth-d t-circuits with d≥3 and t≥1, then it has polynomial-size depth-d (t−1)-circuits.
informal: |-
  Reduce bottom fan-in: If parity has polynomial-size depth-d t-circuits with d≥3 and t≥1, then it has polynomial-size depth-d (t−1)-circuits.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:31.5
  package_source_id: kozen2006
  module_id: kozen2006:31
  entry_type: Lemma
  label: 31.5
  name: Reduce bottom fan-in
  pdf_page: 211
  printed_page: 200
  importance: technical
  tags: circuit-lower-bounds, random-restrictions
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-31-6
kind: lemma
status: accepted
latex: |-
  If parity has polynomial-size depth-d 1-circuits, then it has polynomial-size circuits of depth d−1.
informal: |-
  Remove a circuit level: If parity has polynomial-size depth-d 1-circuits, then it has polynomial-size circuits of depth d−1.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:31.6
  package_source_id: kozen2006
  module_id: kozen2006:31
  entry_type: Lemma
  label: 31.6
  name: Remove a circuit level
  pdf_page: 211
  printed_page: 200
  importance: technical
  tags: circuit-lower-bounds, random-restrictions
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-31-7
kind: lemma
status: accepted
latex: |-
  No (n−1)-CNF and no (n−1)-DNF computes parity on n inputs.
informal: |-
  Parity is not shallow CNF/DNF: No (n−1)-CNF and no (n−1)-DNF computes parity on n inputs.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:31.7
  package_source_id: kozen2006
  module_id: kozen2006:31
  entry_type: Lemma
  label: 31.7
  name: Parity is not shallow CNF/DNF
  pdf_page: 214
  printed_page: 203
  importance: technical
  tags: circuit-lower-bounds, random-restrictions
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-31-8
kind: theorem
status: accepted
latex: |-
  Parity is not in AC⁰.
informal: |-
  Furst–Saxe–Sipser lower bound: Parity is not in AC⁰. Significance: A foundational unconditional circuit lower bound.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:31.8
  package_source_id: kozen2006
  module_id: kozen2006:31
  entry_type: Theorem
  label: 31.8
  name: Furst–Saxe–Sipser lower bound
  pdf_page: 214
  printed_page: 203
  importance: core
  tags: circuit-lower-bounds, random-restrictions
  extraction_scope: numbered formal statement
  review_status: curated
  significance: A foundational unconditional circuit lower bound.
```

```yaml
id: st.lem.complexity.kozen2006-l-h-1
kind: lemma
status: accepted
latex: |-
  Let M be a minterm of φ∧C. Assign the variables shared by M and clause C in the unique way that keeps M nonzero. Then the restricted formula φ∧C equals the restricted φ, and the restricted M is a minterm of the restricted φ.
informal: |-
  Minterm restriction lemma: Let M be a minterm of φ∧C. Assign the variables shared by M and clause C in the unique way that keeps M nonzero. Then the restricted formula φ∧C equals the restricted φ, and the restricted M is a minterm of the restricted φ.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:H.1
  package_source_id: kozen2006
  module_id: kozen2006:H
  entry_type: Lemma
  label: H.1
  name: Minterm restriction lemma
  pdf_page: 216
  printed_page: 205
  importance: technical
  tags: switching-lemma, circuit-lower-bounds
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-h-2
kind: lemma
status: accepted
latex: |-
  For φ^{-W}=∧_{τ:W→{0,1}}τ(φ): (i) if φ is CNF, φ^{-W} has an equivalent CNF with no more clauses; (ii) any minterm of φ disjoint from W remains a minterm of φ^{-W}; (iii) restrictions fixing no variable of W commute with −W; and (iv) under such restrictions, φ is true iff φ^{-W} is true.
informal: |-
  Eliminating a variable set: For φ^{-W}=∧_{τ:W→{0,1}}τ(φ): (i) if φ is CNF, φ^{-W} has an equivalent CNF with no more clauses; (ii) any minterm of φ disjoint from W remains a minterm of φ^{-W}; (iii) restrictions fixing no variable of W commute with −W; and (iv) under such restrictions, φ is true iff φ^{-W} is true.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:H.2
  package_source_id: kozen2006
  module_id: kozen2006:H
  entry_type: Lemma
  label: H.2
  name: Eliminating a variable set
  pdf_page: 216
  printed_page: 205
  importance: technical
  tags: switching-lemma, circuit-lower-bounds
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-h-3
kind: lemma
status: accepted
latex: |-
  Let φ be a t-CNF. Independently set each variable to 0 or 1 with probability (1−p)/2 each, or leave it unset with probability p. Then Pr[the restricted φ is not equivalent to an s-DNF] ≤ αˢ, where α=4pt/ln 2≈5.77pt.
informal: |-
  Håstad switching lemma: Let φ be a t-CNF. Independently set each variable to 0 or 1 with probability (1−p)/2 each, or leave it unset with probability p. Then Pr[the restricted φ is not equivalent to an s-DNF] ≤ αˢ, where α=4pt/ln 2≈5.77pt.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:H.3
  package_source_id: kozen2006
  module_id: kozen2006:H
  entry_type: Lemma
  label: H.3
  name: Håstad switching lemma
  pdf_page: 217
  printed_page: 206
  importance: core
  tags: switching-lemma, circuit-lower-bounds
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-h-4
kind: theorem
status: accepted
latex: |-
  For no constants c,d does parity have a depth-d circuit family of size 2^{(log n)^c}.
informal: |-
  Strong constant-depth parity lower bound: For no constants c,d does parity have a depth-d circuit family of size 2^{(log n)^c}. Significance: Strong enough to produce a relativized PH–PSPACE separation.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:H.4
  package_source_id: kozen2006
  module_id: kozen2006:H
  entry_type: Theorem
  label: H.4
  name: Strong constant-depth parity lower bound
  pdf_page: 220
  printed_page: 209
  importance: core
  tags: switching-lemma, circuit-lower-bounds
  extraction_scope: numbered formal statement
  review_status: curated
  significance: Strong enough to produce a relativized PH–PSPACE separation.
```

```yaml
id: st.cor.complexity.kozen2006-c-h-5
kind: corollary
status: accepted
latex: |-
  There exists an oracle A such that PHᴬ ≠ PSPACEᴬ.
informal: |-
  Oracle separation of PH and PSPACE: There exists an oracle A such that PHᴬ ≠ PSPACEᴬ.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.82
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:C:H.5
  package_source_id: kozen2006
  module_id: kozen2006:H
  entry_type: Corollary
  label: H.5
  name: Oracle separation of PH and PSPACE
  pdf_page: 221
  printed_page: 210
  importance: core
  tags: switching-lemma, circuit-lower-bounds
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-32-1
kind: theorem
status: accepted
latex: |-
  For every total recursive f with f(x)≥x, there is a time bound T such that DTIME(f∘T)=DTIME(T); hence the interval between T and f(T) contains no new deterministic time class.
informal: |-
  Gap theorem: For every total recursive f with f(x)≥x, there is a time bound T such that DTIME(f∘T)=DTIME(T); hence the interval between T and f(T) contains no new deterministic time class.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:32.1
  package_source_id: kozen2006
  module_id: kozen2006:32
  entry_type: Theorem
  label: 32.1
  name: Gap theorem
  pdf_page: 227
  printed_page: 216
  importance: core
  tags: complexity-pathology, speedup
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-32-2
kind: theorem
status: accepted
latex: |-
  For every monotone total recursive f with f(n)≥n², there is a recursive language A such that every TM Mᵢ deciding A has another decider Mⱼ for A with f(Tⱼ(x))<Tᵢ(x) for almost all x.
informal: |-
  Blum speedup theorem: For every monotone total recursive f with f(n)≥n², there is a recursive language A such that every TM Mᵢ deciding A has another decider Mⱼ for A with f(Tⱼ(x))<Tᵢ(x) for almost all x.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:32.2
  package_source_id: kozen2006
  module_id: kozen2006:32
  entry_type: Theorem
  label: 32.2
  name: Blum speedup theorem
  pdf_page: 227
  printed_page: 216
  importance: core
  tags: complexity-pathology, speedup
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-33-1
kind: theorem
status: accepted
latex: |-
  For every total recursive index transformation σ, there is an index i with φᵢ=φ_{σ(i)}; such an i is effectively computable from an index for σ.
informal: |-
  Recursion theorem: For every total recursive index transformation σ, there is an index i with φᵢ=φ_{σ(i)}; such an i is effectively computable from an index for σ. Significance: Formalizes self-reference for programs.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:33.1
  package_source_id: kozen2006
  module_id: kozen2006:33
  entry_type: Theorem
  label: 33.1
  name: Recursion theorem
  pdf_page: 235
  printed_page: 224
  importance: core
  tags: computability, recursion-theorem
  extraction_scope: numbered formal statement
  review_status: curated
  significance: Formalizes self-reference for programs.
```

```yaml
id: st.thm.complexity.kozen2006-t-34-1
kind: theorem
status: accepted
latex: |-
  In any Gödel numbering, there is no infinite recursively enumerable list consisting entirely of minimal indices.
informal: |-
  No enumerable list of minimal indices: In any Gödel numbering, there is no infinite recursively enumerable list consisting entirely of minimal indices.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:34.1
  package_source_id: kozen2006
  module_id: kozen2006:34
  entry_type: Theorem
  label: 34.1
  name: No enumerable list of minimal indices
  pdf_page: 239
  printed_page: 228
  importance: supporting
  tags: computability, godel-numbering
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-34-2
kind: lemma
status: accepted
latex: |-
  In every Gödel numbering there is a total recursive σ such that σ(x)>x and φₓ=φ_{σ(x)} for all x.
informal: |-
  Effective padding lemma: In every Gödel numbering there is a total recursive σ such that σ(x)>x and φₓ=φ_{σ(x)} for all x.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:34.2
  package_source_id: kozen2006
  module_id: kozen2006:34
  entry_type: Lemma
  label: 34.2
  name: Effective padding lemma
  pdf_page: 239
  printed_page: 228
  importance: technical
  tags: computability, godel-numbering
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-34-3
kind: theorem
status: accepted
latex: |-
  For any two Gödel numberings (φᵢ) and (ψᵢ) of the partial recursive functions, there is a recursive bijection ρ of N such that φᵢ=ψ_{ρ(i)} for every i.
informal: |-
  Rogers isomorphism theorem: For any two Gödel numberings (φᵢ) and (ψᵢ) of the partial recursive functions, there is a recursive bijection ρ of N such that φᵢ=ψ_{ρ(i)} for every i.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:34.3
  package_source_id: kozen2006
  module_id: kozen2006:34
  entry_type: Theorem
  label: 34.3
  name: Rogers isomorphism theorem
  pdf_page: 240
  printed_page: 229
  importance: core
  tags: computability, godel-numbering
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-j-1
kind: theorem
status: accepted
latex: |-
  For an abstract complexity measure Φ and every total recursive f(x)≥x, there is a total recursive t with C_t^Φ=C_{f∘t}^Φ. Equivalently, every program bounded by f(t(x)) almost everywhere has an equivalent program bounded by t(x) almost everywhere.
informal: |-
  Abstract gap theorem: For an abstract complexity measure Φ and every total recursive f(x)≥x, there is a total recursive t with C_t^Φ=C_{f∘t}^Φ. Equivalently, every program bounded by f(t(x)) almost everywhere has an equivalent program bounded by t(x) almost everywhere.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:J.1
  package_source_id: kozen2006
  module_id: kozen2006:J
  entry_type: Theorem
  label: J.1
  name: Abstract gap theorem
  pdf_page: 243
  printed_page: 232
  importance: core
  tags: abstract-complexity
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-j-2
kind: theorem
status: accepted
latex: |-
  For every abstract complexity measure Φ and total recursive f, there is a total recursive function g such that every index i for g has another index j for g with f(n,Φⱼ(n))<Φᵢ(n) almost everywhere.
informal: |-
  Abstract speedup theorem: For every abstract complexity measure Φ and total recursive f, there is a total recursive function g such that every index i for g has another index j for g with f(n,Φⱼ(n))<Φᵢ(n) almost everywhere.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:J.2
  package_source_id: kozen2006
  module_id: kozen2006:J
  entry_type: Theorem
  label: J.2
  name: Abstract speedup theorem
  pdf_page: 243
  printed_page: 232
  importance: core
  tags: abstract-complexity
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-j-3
kind: theorem
status: accepted
latex: |-
  For every recursively enumerable nondecreasing list f₀≤f₁≤… of total recursive bounds, there is a total recursive f such that C_f^Φ=⋃ᵢC_{fᵢ}^Φ.
informal: |-
  Union theorem: For every recursively enumerable nondecreasing list f₀≤f₁≤… of total recursive bounds, there is a total recursive f such that C_f^Φ=⋃ᵢC_{fᵢ}^Φ.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:J.3
  package_source_id: kozen2006
  module_id: kozen2006:J
  entry_type: Theorem
  label: J.3
  name: Union theorem
  pdf_page: 245
  printed_page: 234
  importance: core
  tags: abstract-complexity
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-35-1
kind: theorem
status: accepted
latex: |-
  A∈Σₙ⁰ iff A={x:∃y₁∀y₂∃y₃…Qₙyₙ R(x,y₁,…,yₙ)} for some decidable R, with Qₙ=∃ for odd n and ∀ for even n. Dually, A∈Πₙ⁰ iff the prefix begins universally and alternates.
informal: |-
  Quantifier characterization of the arithmetic hierarchy: A∈Σₙ⁰ iff A={x:∃y₁∀y₂∃y₃…Qₙyₙ R(x,y₁,…,yₙ)} for some decidable R, with Qₙ=∃ for odd n and ∀ for even n. Dually, A∈Πₙ⁰ iff the prefix begins universally and alternates.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:35.1
  package_source_id: kozen2006
  module_id: kozen2006:35
  entry_type: Theorem
  label: 35.1
  name: Quantifier characterization of the arithmetic hierarchy
  pdf_page: 248
  printed_page: 237
  importance: core
  tags: arithmetic-hierarchy
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-36-1
kind: lemma
status: accepted
latex: |-
  FINHP is many-one complete for Σ₃⁰. More generally, if A is many-one complete for Σₙ⁰, then FIN_A is many-one complete for Σ_{n+2}⁰.
informal: |-
  Finite-halting completeness lift: FINHP is many-one complete for Σ₃⁰. More generally, if A is many-one complete for Σₙ⁰, then FIN_A is many-one complete for Σ_{n+2}⁰.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:36.1
  package_source_id: kozen2006
  module_id: kozen2006:36
  entry_type: Lemma
  label: 36.1
  name: Finite-halting completeness lift
  pdf_page: 254
  printed_page: 243
  importance: core
  tags: arithmetic-hierarchy, complete-problems
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-37-1
kind: theorem
status: accepted
latex: |-
  There exists a recursively enumerable, nonrecursive language that is not r.e.-complete.
informal: |-
  Post’s theorem on intermediate m-degrees: There exists a recursively enumerable, nonrecursive language that is not r.e.-complete.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:37.1
  package_source_id: kozen2006
  module_id: kozen2006:37
  entry_type: Theorem
  label: 37.1
  name: Post’s theorem on intermediate m-degrees
  pdf_page: 259
  printed_page: 248
  importance: core
  tags: recursion-theory, degrees
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.def.complexity.kozen2006-d-37-2
kind: definition
status: accepted
latex: |-
  A set A⊆N is immune when it is infinite but contains no infinite recursively enumerable subset.
informal: |-
  Immune set: A set A⊆N is immune when it is infinite but contains no infinite recursively enumerable subset.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:D:37.2
  package_source_id: kozen2006
  module_id: kozen2006:37
  entry_type: Definition
  label: 37.2
  name: Immune set
  pdf_page: 260
  printed_page: 249
  importance: foundational
  tags: recursion-theory, degrees
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.def.complexity.kozen2006-d-37-3
kind: definition
status: accepted
latex: |-
  A set B⊆N is simple when B is recursively enumerable and its complement is immune; equivalently, the complement is infinite and B meets every infinite r.e. set.
informal: |-
  Simple set: A set B⊆N is simple when B is recursively enumerable and its complement is immune; equivalently, the complement is infinite and B meets every infinite r.e. set.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:D:37.3
  package_source_id: kozen2006
  module_id: kozen2006:37
  entry_type: Definition
  label: 37.3
  name: Simple set
  pdf_page: 260
  printed_page: 249
  importance: foundational
  tags: recursion-theory, degrees
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.def.complexity.kozen2006-d-37-4
kind: definition
status: accepted
latex: |-
  A set C⊆N is productive when there is a total recursive function σ such that Wₓ⊆C implies σ(x)∈C∖Wₓ. Such σ is a productive function.
informal: |-
  Productive set: A set C⊆N is productive when there is a total recursive function σ such that Wₓ⊆C implies σ(x)∈C∖Wₓ. Such σ is a productive function.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:D:37.4
  package_source_id: kozen2006
  module_id: kozen2006:37
  entry_type: Definition
  label: 37.4
  name: Productive set
  pdf_page: 260
  printed_page: 249
  importance: foundational
  tags: recursion-theory, degrees
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-37-6
kind: lemma
status: accepted
latex: |-
  There exists a simple set.
informal: |-
  Existence of a simple set: There exists a simple set.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:37.6
  package_source_id: kozen2006
  module_id: kozen2006:37
  entry_type: Lemma
  label: 37.6
  name: Existence of a simple set
  pdf_page: 261
  printed_page: 250
  importance: technical
  tags: recursion-theory, degrees
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-37-7
kind: lemma
status: accepted
latex: |-
  If B is simple, then its complement is not productive.
informal: |-
  Simple complements are not productive: If B is simple, then its complement is not productive.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:37.7
  package_source_id: kozen2006
  module_id: kozen2006:37
  entry_type: Lemma
  label: 37.7
  name: Simple complements are not productive
  pdf_page: 261
  printed_page: 250
  importance: technical
  tags: recursion-theory, degrees
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-37-8
kind: lemma
status: accepted
latex: |-
  If A is r.e.-complete, then its complement is productive.
informal: |-
  Completeness implies productivity of the complement: If A is r.e.-complete, then its complement is productive.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:37.8
  package_source_id: kozen2006
  module_id: kozen2006:37
  entry_type: Lemma
  label: 37.8
  name: Completeness implies productivity of the complement
  pdf_page: 261
  printed_page: 250
  importance: technical
  tags: recursion-theory, degrees
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-38-1
kind: theorem
status: accepted
latex: |-
  There exists an r.e. set A of intermediate Turing degree: ∅ <ᵀ A <ᵀ K.
informal: |-
  Friedberg–Muchnik theorem: There exists an r.e. set A of intermediate Turing degree: ∅ <ᵀ A <ᵀ K. Significance: Solves Post’s problem by constructing an intermediate r.e. Turing degree.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:38.1
  package_source_id: kozen2006
  module_id: kozen2006:38
  entry_type: Theorem
  label: 38.1
  name: Friedberg–Muchnik theorem
  pdf_page: 264
  printed_page: 253
  importance: core
  tags: priority-method, degrees
  extraction_scope: numbered formal statement
  review_status: curated
  significance: Solves Post’s problem by constructing an intermediate r.e. Turing degree.
```

```yaml
id: st.def.complexity.kozen2006-d-38-2
kind: definition
status: accepted
latex: |-
  An r.e. set A is low when Kᴬ ≤ᵀ K; equivalently, the halting problem relative to A is no harder than the ordinary halting problem.
informal: |-
  Low set: An r.e. set A is low when Kᴬ ≤ᵀ K; equivalently, the halting problem relative to A is no harder than the ordinary halting problem.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:D:38.2
  package_source_id: kozen2006
  module_id: kozen2006:38
  entry_type: Definition
  label: 38.2
  name: Low set
  pdf_page: 265
  printed_page: 254
  importance: foundational
  tags: priority-method, degrees
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-38-3
kind: lemma
status: accepted
latex: |-
  If A is low, then A <ᵀ K.
informal: |-
  Low sets are incomplete: If A is low, then A <ᵀ K.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:38.3
  package_source_id: kozen2006
  module_id: kozen2006:38
  entry_type: Lemma
  label: 38.3
  name: Low sets are incomplete
  pdf_page: 265
  printed_page: 254
  importance: technical
  tags: priority-method, degrees
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.kozen2006-l-38-4
kind: lemma
status: accepted
latex: |-
  There exists a low simple set.
informal: |-
  Low simple set: There exists a low simple set.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:L:38.4
  package_source_id: kozen2006
  module_id: kozen2006:38
  entry_type: Lemma
  label: 38.4
  name: Low simple set
  pdf_page: 265
  printed_page: 254
  importance: technical
  tags: priority-method, degrees
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-40-1
kind: theorem
status: accepted
latex: |-
  Over the natural numbers, the inductive relations are exactly the Π₁¹ relations, and the hyperelementary relations are exactly the Δ₁¹ relations.
informal: |-
  Kleene’s theorem: Over the natural numbers, the inductive relations are exactly the Π₁¹ relations, and the hyperelementary relations are exactly the Δ₁¹ relations. Significance: Connects inductive definitions with the first analytic level.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:40.1
  package_source_id: kozen2006
  module_id: kozen2006:40
  entry_type: Theorem
  label: 40.1
  name: Kleene’s theorem
  pdf_page: 275
  printed_page: 264
  importance: core
  tags: kleene, analytic-hierarchy
  extraction_scope: numbered formal statement
  review_status: curated
  significance: Connects inductive definitions with the first analytic level.
```

```yaml
id: st.thm.complexity.kozen2006-t-40-2
kind: theorem
status: accepted
latex: |-
  A set A⊆N is inductive iff there is a hyperelementary relation R with A={x:∃α<ω₁^{CK} R(x,α)}; equivalently, the existential witness can be a code for a recursive ordinal.
informal: |-
  Ordinal characterization of inductive sets: A set A⊆N is inductive iff there is a hyperelementary relation R with A={x:∃α<ω₁^{CK} R(x,α)}; equivalently, the existential witness can be a code for a recursive ordinal.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:40.2
  package_source_id: kozen2006
  module_id: kozen2006:40
  entry_type: Theorem
  label: 40.2
  name: Ordinal characterization of inductive sets
  pdf_page: 277
  printed_page: 266
  importance: supporting
  tags: kleene, analytic-hierarchy
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.kozen2006-t-41-1
kind: theorem
status: accepted
latex: |-
  There is a recursive bijective encoding τ from binary trees to nontrivial full ω-trees such that a binary tree is fairly terminating for the condition (true,last(0)) iff τ(T) is well-founded.
informal: |-
  Harel’s theorem: There is a recursive bijective encoding τ from binary trees to nontrivial full ω-trees such that a binary tree is fairly terminating for the condition (true,last(0)) iff τ(T) is well-founded.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:T:41.1
  package_source_id: kozen2006
  module_id: kozen2006:41
  entry_type: Theorem
  label: 41.1
  name: Harel’s theorem
  pdf_page: 282
  printed_page: 271
  importance: core
  tags: fair-termination, program-verification
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.cor.complexity.kozen2006-c-41-2
kind: corollary
status: accepted
latex: |-
  Fair termination is Π₁¹-complete.
informal: |-
  Complexity of fair termination: Fair termination is Π₁¹-complete. Significance: Places a natural program-termination problem at Π₁¹-complete complexity.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.82
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:C:41.2
  package_source_id: kozen2006
  module_id: kozen2006:41
  entry_type: Corollary
  label: 41.2
  name: Complexity of fair termination
  pdf_page: 282
  printed_page: 271
  importance: core
  tags: fair-termination, program-verification
  extraction_scope: numbered formal statement
  review_status: curated
  significance: Places a natural program-termination problem at Π₁¹-complete complexity.
```

```yaml
id: st.def.complexity.np-ch2-d-2-1
kind: definition
status: accepted
latex: |-
  A language L is in NP iff there are a polynomial p and a polynomial-time verifier M such that x∈L exactly when some certificate u∈{0,1}^{p(|x|)} satisfies M(x,u)=1.
informal: |-
  Verifier definition of NP: A language L is in NP iff there are a polynomial p and a polynomial-time verifier M such that x∈L exactly when some certificate u∈{0,1}^{p(|x|)} satisfies M(x,u)=1.
source_ids:
- src.complexity.np-ch2
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: np_ch2:D:2.1
  package_source_id: np_ch2
  module_id: np_ch2:2.1
  entry_type: Definition
  label: 2.1
  name: Verifier definition of NP
  pdf_page: 2
  printed_page: 39
  importance: foundational
  tags: np, certificates, nondeterminism
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.def.complexity.np-ch2-d-2-5
kind: definition
status: accepted
latex: |-
  L∈NTIME(T(n)) when some nondeterministic TM decides L in O(T(n)) time on every computation branch.
informal: |-
  Nondeterministic time: L∈NTIME(T(n)) when some nondeterministic TM decides L in O(T(n)) time on every computation branch.
source_ids:
- src.complexity.np-ch2
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: np_ch2:D:2.5
  package_source_id: np_ch2
  module_id: np_ch2:2.1
  entry_type: Definition
  label: 2.5
  name: Nondeterministic time
  pdf_page: 4
  printed_page: 41
  importance: foundational
  tags: np, certificates, nondeterminism
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.np-ch2-t-2-6
kind: theorem
status: accepted
latex: |-
  NP = ⋃_{c∈N} NTIME(nᶜ).
informal: |-
  Machine characterization of NP: NP = ⋃_{c∈N} NTIME(nᶜ).
source_ids:
- src.complexity.np-ch2
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: np_ch2:T:2.6
  package_source_id: np_ch2
  module_id: np_ch2:2.1
  entry_type: Theorem
  label: 2.6
  name: Machine characterization of NP
  pdf_page: 4
  printed_page: 41
  importance: core
  tags: np, certificates, nondeterminism
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.def.complexity.np-ch2-d-2-7
kind: definition
status: accepted
latex: |-
  L≤ᵖL′ when a polynomial-time function f maps x∈L exactly to f(x)∈L′. A language is NP-hard if every NP language reduces to it, and NP-complete if it is both NP-hard and in NP.
informal: |-
  Karp reduction, NP-hardness, NP-completeness: L≤ᵖL′ when a polynomial-time function f maps x∈L exactly to f(x)∈L′. A language is NP-hard if every NP language reduces to it, and NP-complete if it is both NP-hard and in NP.
source_ids:
- src.complexity.np-ch2
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: np_ch2:D:2.7
  package_source_id: np_ch2
  module_id: np_ch2:2.2
  entry_type: Definition
  label: 2.7
  name: Karp reduction, NP-hardness, NP-completeness
  pdf_page: 5
  printed_page: 42
  importance: foundational
  tags: reductions, np-completeness
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.np-ch2-t-2-8
kind: theorem
status: accepted
latex: |-
  (1) Polynomial-time Karp reductions are transitive. (2) If an NP-hard language lies in P, then P=NP. (3) An NP-complete language lies in P iff P=NP.
informal: |-
  Consequences of polynomial reductions: (1) Polynomial-time Karp reductions are transitive. (2) If an NP-hard language lies in P, then P=NP. (3) An NP-complete language lies in P iff P=NP.
source_ids:
- src.complexity.np-ch2
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: np_ch2:T:2.8
  package_source_id: np_ch2
  module_id: np_ch2:2.2
  entry_type: Theorem
  label: 2.8
  name: Consequences of polynomial reductions
  pdf_page: 6
  printed_page: 43
  importance: core
  tags: reductions, np-completeness
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.np-ch2-t-2-9
kind: theorem
status: accepted
latex: |-
  TMSAT = {⟨α,x,1ⁿ,1ᵗ⟩ : some u∈{0,1}ⁿ makes machine Mα accept ⟨x,u⟩ within t steps} is NP-complete.
informal: |-
  NP-completeness of TMSAT: TMSAT = {⟨α,x,1ⁿ,1ᵗ⟩ : some u∈{0,1}ⁿ makes machine Mα accept ⟨x,u⟩ within t steps} is NP-complete.
source_ids:
- src.complexity.np-ch2
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: np_ch2:T:2.9
  package_source_id: np_ch2
  module_id: np_ch2:2.2
  entry_type: Theorem
  label: 2.9
  name: NP-completeness of TMSAT
  pdf_page: 6
  printed_page: 43
  importance: core
  tags: reductions, np-completeness
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.np-ch2-t-2-10
kind: theorem
status: accepted
latex: |-
  SAT is NP-complete, and 3SAT is NP-complete.
informal: |-
  Cook–Levin theorem: SAT is NP-complete, and 3SAT is NP-complete. Significance: The central theorem establishing natural NP-complete problems.
source_ids:
- src.complexity.np-ch2
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: np_ch2:T:2.10
  package_source_id: np_ch2
  module_id: np_ch2:2.3
  entry_type: Theorem
  label: 2.10
  name: Cook–Levin theorem
  pdf_page: 8
  printed_page: 45
  importance: core
  tags: cook-levin, sat
  extraction_scope: numbered formal statement
  review_status: curated
  significance: The central theorem establishing natural NP-complete problems.
```

```yaml
id: st.lem.complexity.np-ch2-l-2-11
kind: lemma
status: accepted
latex: |-
  SAT is NP-hard.
informal: |-
  NP-hardness of SAT: SAT is NP-hard.
source_ids:
- src.complexity.np-ch2
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: np_ch2:L:2.11
  package_source_id: np_ch2
  module_id: np_ch2:2.3
  entry_type: Lemma
  label: 2.11
  name: NP-hardness of SAT
  pdf_page: 8
  printed_page: 45
  importance: supporting
  tags: cook-levin, sat
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.lem.complexity.np-ch2-l-2-14
kind: lemma
status: accepted
latex: |-
  SAT ≤ᵖ 3SAT.
informal: |-
  Reduction from SAT to 3SAT: SAT ≤ᵖ 3SAT.
source_ids:
- src.complexity.np-ch2
used_symbols: []
depends_on: []
confidence: 0.84
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: np_ch2:L:2.14
  package_source_id: np_ch2
  module_id: np_ch2:2.3
  entry_type: Lemma
  label: 2.14
  name: Reduction from SAT to 3SAT
  pdf_page: 12
  printed_page: 49
  importance: supporting
  tags: cook-levin, sat
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.np-ch2-t-2-15
kind: theorem
status: accepted
latex: |-
  INDSET is NP-complete.
informal: |-
  NP-completeness of independent set: INDSET is NP-complete.
source_ids:
- src.complexity.np-ch2
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: np_ch2:T:2.15
  package_source_id: np_ch2
  module_id: np_ch2:2.4
  entry_type: Theorem
  label: 2.15
  name: NP-completeness of independent set
  pdf_page: 14
  printed_page: 51
  importance: core
  tags: np-complete-problems, reductions
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.np-ch2-t-2-16
kind: theorem
status: accepted
latex: |-
  0/1 IPROG is NP-complete.
informal: |-
  NP-completeness of 0/1 integer programming: 0/1 IPROG is NP-complete.
source_ids:
- src.complexity.np-ch2
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: np_ch2:T:2.16
  package_source_id: np_ch2
  module_id: np_ch2:2.4
  entry_type: Theorem
  label: 2.16
  name: NP-completeness of 0/1 integer programming
  pdf_page: 15
  printed_page: 52
  importance: core
  tags: np-complete-problems, reductions
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.np-ch2-t-2-17
kind: theorem
status: accepted
latex: |-
  The directed Hamiltonian path language dHAMPATH is NP-complete.
informal: |-
  NP-completeness of directed Hamiltonian path: The directed Hamiltonian path language dHAMPATH is NP-complete.
source_ids:
- src.complexity.np-ch2
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: np_ch2:T:2.17
  package_source_id: np_ch2
  module_id: np_ch2:2.4
  entry_type: Theorem
  label: 2.17
  name: NP-completeness of directed Hamiltonian path
  pdf_page: 16
  printed_page: 53
  importance: core
  tags: np-complete-problems, reductions
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.np-ch2-t-2-18
kind: theorem
status: accepted
latex: |-
  If P=NP, then for every NP language and every polynomial-time verifier, a valid certificate for any yes-instance can be found in polynomial time.
informal: |-
  Decision-to-search under P=NP: If P=NP, then for every NP language and every polynomial-time verifier, a valid certificate for any yes-instance can be found in polynomial time. Significance: Shows that, for NP problems, efficient decision would yield efficient witness recovery.
source_ids:
- src.complexity.np-ch2
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: np_ch2:T:2.18
  package_source_id: np_ch2
  module_id: np_ch2:2.6
  entry_type: Theorem
  label: 2.18
  name: Decision-to-search under P=NP
  pdf_page: 18
  printed_page: 55
  importance: core
  tags: conp, exp, nexp
  extraction_scope: numbered formal statement
  review_status: curated
  significance: Shows that, for NP problems, efficient decision would yield efficient witness recovery.
```

```yaml
id: st.def.complexity.np-ch2-d-2-19
kind: definition
status: accepted
latex: |-
  coNP = {L : the complement of L is in NP}.
informal: |-
  coNP by complementation: coNP = {L : the complement of L is in NP}.
source_ids:
- src.complexity.np-ch2
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: np_ch2:D:2.19
  package_source_id: np_ch2
  module_id: np_ch2:2.6
  entry_type: Definition
  label: 2.19
  name: coNP by complementation
  pdf_page: 18
  printed_page: 55
  importance: foundational
  tags: conp, exp, nexp
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.def.complexity.np-ch2-d-2-20
kind: definition
status: accepted
latex: |-
  A language L is in coNP iff there are a polynomial p and polynomial-time M such that x∈L exactly when M(x,u)=1 for every u∈{0,1}^{p(|x|)}.
informal: |-
  Universal-certificate characterization of coNP: A language L is in coNP iff there are a polynomial p and polynomial-time M such that x∈L exactly when M(x,u)=1 for every u∈{0,1}^{p(|x|)}.
source_ids:
- src.complexity.np-ch2
used_symbols: []
depends_on: []
confidence: 0.95
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: np_ch2:D:2.20
  package_source_id: np_ch2
  module_id: np_ch2:2.6
  entry_type: Definition
  label: 2.20
  name: Universal-certificate characterization of coNP
  pdf_page: 19
  printed_page: 56
  importance: foundational
  tags: conp, exp, nexp
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.np-ch2-t-2-22
kind: theorem
status: accepted
latex: |-
  If EXP ≠ NEXP, then P ≠ NP.
informal: |-
  Padding implication: If EXP ≠ NEXP, then P ≠ NP.
source_ids:
- src.complexity.np-ch2
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: np_ch2:T:2.22
  package_source_id: np_ch2
  module_id: np_ch2:2.7
  entry_type: Theorem
  label: 2.22
  name: Padding implication
  pdf_page: 20
  printed_page: 57
  importance: core
  tags: complexity-philosophy
  extraction_scope: numbered formal statement
  review_status: curated
```

```yaml
id: st.thm.complexity.k-res-bppph
kind: theorem
status: accepted
latex: |-
  BPP ⊆ Σ₂ᵖ ∩ Π₂ᵖ. The proof amplifies the randomized algorithm and uses a small family of XOR shifts to cover the random-bit space.
informal: |-
  BPP lies low in PH: BPP ⊆ Σ₂ᵖ ∩ Π₂ᵖ. The proof amplifies the randomized algorithm and uses a small family of XOR shifts to cover the random-bit space.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: K-RES-BPPPH
  package_source_id: kozen2006
  module_id: kozen2006:14
  entry_type: Core result
  label:
  name: BPP lies low in PH
  pdf_page: 93
  printed_page: 82
  importance: core
  tags: bpp, polynomial-hierarchy, derandomization
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Core result imported as theorem-level canonical statement.
```

```yaml
id: st.thm.complexity.k-res-ip
kind: theorem
status: accepted
latex: |-
  Every PSPACE language has an interactive proof, and every language with an interactive proof is in PSPACE; therefore IP = PSPACE.
informal: |-
  IP = PSPACE: Every PSPACE language has an interactive proof, and every language with an interactive proof is in PSPACE; therefore IP = PSPACE.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: K-RES-IP
  package_source_id: kozen2006
  module_id: kozen2006:16
  entry_type: Core result
  label:
  name: IP = PSPACE
  pdf_page: 114
  printed_page: 103
  importance: core
  tags: interactive-proofs, pspace
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Core result imported as theorem-level canonical statement.
```

```yaml
id: st.thm.complexity.k-res-pcpweak
kind: theorem
status: accepted
latex: |-
  NP ⊆ PCP(n³,1), proved using arithmetization, linearity testing, tensor-consistency tests, and random self-correction.
informal: |-
  Weak PCP construction: NP ⊆ PCP(n³,1), proved using arithmetization, linearity testing, tensor-consistency tests, and random self-correction.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: K-RES-PCPWEAK
  package_source_id: kozen2006
  module_id: kozen2006:19
  entry_type: Core result
  label:
  name: Weak PCP construction
  pdf_page: 130
  printed_page: 119
  importance: core
  tags: pcp, linearity-testing
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Core result imported as theorem-level canonical statement.
```

```yaml
id: st.thm.complexity.k-res-realadd
kind: theorem
status: accepted
latex: |-
  The first-order theory Th(R,+,≤) is complete for STA(*,2^{O(n)},n).
informal: |-
  Exact complexity of real addition: The first-order theory Th(R,+,≤) is complete for STA(*,2^{O(n)},n).
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: K-RES-REALADD
  package_source_id: kozen2006
  module_id: kozen2006:22
  entry_type: Core result
  label:
  name: Exact complexity of real addition
  pdf_page: 151
  printed_page: 140
  importance: core
  tags: logic, real-addition, alternation
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Core result imported as theorem-level canonical statement.
```

```yaml
id: st.thm.complexity.k-res-presburger
kind: theorem
status: accepted
latex: |-
  The first-order theory Th(Z,+,≤) is complete for STA(*,2^{2^{n^{O(1)}}},n).
informal: |-
  Exact complexity of Presburger arithmetic: The first-order theory Th(Z,+,≤) is complete for STA(*,2^{2^{n^{O(1)}}},n).
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.86
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: K-RES-PRESBURGER
  package_source_id: kozen2006
  module_id: kozen2006:24
  entry_type: Core result
  label:
  name: Exact complexity of Presburger arithmetic
  pdf_page: 162
  printed_page: 151
  importance: core
  tags: logic, presburger-arithmetic
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Core result imported as theorem-level canonical statement.
```

# Derived Statements

```yaml
id: st.obs.complexity.kozen2006-c-14-2
kind: observation
status: accepted
latex: |-
  In the amplified BPP setup, let m be the number of random bits and Aₓ = {y : M(x,y) accepts}. Then x ∈ A iff there exist m shifts z₁,…,zₘ ∈ {0,1}ᵐ such that ⋃ⱼ(Aₓ ⊕ zⱼ) = {0,1}ᵐ.
informal: |-
  XOR-shift covering claim: In the amplified BPP setup, let m be the number of random bits and Aₓ = {y : M(x,y) accepts}. Then x ∈ A iff there exist m shifts z₁,…,zₘ ∈ {0,1}ᵐ such that ⋃ⱼ(Aₓ ⊕ zⱼ) = {0,1}ᵐ.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.72
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:C:14.2
  package_source_id: kozen2006
  module_id: kozen2006:14
  entry_type: Claim
  label: 14.2
  name: XOR-shift covering claim
  pdf_page: 95
  printed_page: 84
  importance: supporting
  tags: bpp, polynomial-hierarchy
  extraction_scope: numbered formal statement
  review_status: curated
  normalization: Claim imported as derived observation.
```

```yaml
id: st.obs.complexity.kozen2006-c-27-1
kind: observation
status: accepted
latex: |-
  The nondeterministic Büchi automaton B accepts x iff, in the determinized construction, some color’s bell rings infinitely often while that color’s buzzer sounds only finitely often.
informal: |-
  Acceptance invariant in Safra’s construction: The nondeterministic Büchi automaton B accepts x iff, in the determinized construction, some color’s bell rings infinitely often while that color’s buzzer sounds only finitely often.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.72
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: kozen2006:C:27.1
  package_source_id: kozen2006
  module_id: kozen2006:27
  entry_type: Claim
  label: 27.1
  name: Acceptance invariant in Safra’s construction
  pdf_page: 180
  printed_page: 169
  importance: supporting
  tags: omega-automata, safra
  extraction_scope: numbered formal statement
  review_status: curated
  normalization: Claim imported as derived observation.
```

```yaml
id: st.obs.complexity.np-ch2-c-2-4
kind: observation
status: accepted
latex: |-
  P ⊆ NP ⊆ EXP.
informal: |-
  Basic inclusions: P ⊆ NP ⊆ EXP.
source_ids:
- src.complexity.np-ch2
used_symbols: []
depends_on: []
confidence: 0.72
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: np_ch2:C:2.4
  package_source_id: np_ch2
  module_id: np_ch2:2.1
  entry_type: Claim
  label: 2.4
  name: Basic inclusions
  pdf_page: 4
  printed_page: 41
  importance: supporting
  tags: np, certificates, nondeterminism
  extraction_scope: numbered formal statement
  review_status: curated
  normalization: Claim imported as derived observation.
```

```yaml
id: st.obs.complexity.np-ch2-c-2-13
kind: observation
status: accepted
latex: |-
  Every Boolean function f:{0,1}^ℓ→{0,1} has an ℓ-variable CNF formula of size at most ℓ·2^ℓ that computes f.
informal: |-
  Universality of AND, OR, NOT: Every Boolean function f:{0,1}^ℓ→{0,1} has an ℓ-variable CNF formula of size at most ℓ·2^ℓ that computes f.
source_ids:
- src.complexity.np-ch2
used_symbols: []
depends_on: []
confidence: 0.72
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: np_ch2:C:2.13
  package_source_id: np_ch2
  module_id: np_ch2:2.3
  entry_type: Claim
  label: 2.13
  name: Universality of AND, OR, NOT
  pdf_page: 9
  printed_page: 46
  importance: supporting
  tags: cook-levin, sat
  extraction_scope: numbered formal statement
  review_status: curated
  normalization: Claim imported as derived observation.
```

```yaml
id: st.obs.complexity.k-con-tm
kind: observation
status: accepted
latex: |-
  A finite-control machine with a semi-infinite read/write tape, a head, input and tape alphabets, and a transition function δ:Q×Γ→Q×Γ×{L,R}; it accepts or rejects by entering distinguished halting states.
informal: |-
  Deterministic one-tape Turing machine: A finite-control machine with a semi-infinite read/write tape, a head, input and tape alphabets, and a transition function δ:Q×Γ→Q×Γ×{L,R}; it accepts or rejects by entering distinguished halting states.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: K-CON-TM
  package_source_id: kozen2006
  module_id: kozen2006:1
  entry_type: Concept
  label:
  name: Deterministic one-tape Turing machine
  pdf_page: 16
  printed_page: 5
  importance: foundational
  tags: turing-machines, models-of-computation
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

```yaml
id: st.obs.complexity.k-con-ntm
kind: observation
status: accepted
latex: |-
  A Turing machine whose transition rule is a finite relation rather than a function. Its computation is a tree, and it accepts when some branch reaches an accepting configuration.
informal: |-
  Nondeterministic Turing machine: A Turing machine whose transition rule is a finite relation rather than a function. Its computation is a tree, and it accepts when some branch reaches an accepting configuration.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: K-CON-NTM
  package_source_id: kozen2006
  module_id: kozen2006:1
  entry_type: Concept
  label:
  name: Nondeterministic Turing machine
  pdf_page: 18
  printed_page: 7
  importance: foundational
  tags: turing-machines, nondeterminism
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

```yaml
id: st.obs.complexity.k-con-cross
kind: observation
status: accepted
latex: |-
  The sequence of finite-control states seen as a one-tape TM crosses a fixed boundary between adjacent tape cells. Crossing sequences transfer all information communicated across that boundary.
informal: |-
  Crossing sequence: The sequence of finite-control states seen as a one-tape TM crosses a fixed boundary between adjacent tape cells. Crossing sequences transfer all information communicated across that boundary.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: K-CON-CROSS
  package_source_id: kozen2006
  module_id: kozen2006:1
  entry_type: Concept
  label:
  name: Crossing sequence
  pdf_page: 19
  printed_page: 8
  importance: foundational
  tags: lower-bounds, crossing-sequences
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

```yaml
id: st.obs.complexity.k-con-lst
kind: observation
status: accepted
latex: |-
  A total deterministic logspace machine with read-only input, O(log n) read/write work space, and a write-only output tape. Its output defines a logspace-computable function.
informal: |-
  Logspace transducer: A total deterministic logspace machine with read-only input, O(log n) read/write work space, and a write-only output tape. Its output defines a logspace-computable function.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: K-CON-LST
  package_source_id: kozen2006
  module_id: kozen2006:5
  entry_type: Concept
  label:
  name: Logspace transducer
  pdf_page: 37
  printed_page: 26
  importance: foundational
  tags: logspace, transducers
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

```yaml
id: st.obs.complexity.k-con-lred
kind: observation
status: accepted
latex: |-
  A≤ₘˡᵒᵍB when a logspace-computable function σ satisfies x∈A iff σ(x)∈B. Hardness and completeness are defined using this reduction.
informal: |-
  Logspace many-one reduction: A≤ₘˡᵒᵍB when a logspace-computable function σ satisfies x∈A iff σ(x)∈B. Hardness and completeness are defined using this reduction.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: K-CON-LRED
  package_source_id: kozen2006
  module_id: kozen2006:5
  entry_type: Concept
  label:
  name: Logspace many-one reduction
  pdf_page: 38
  printed_page: 27
  importance: foundational
  tags: reductions, logspace, completeness
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

```yaml
id: st.obs.complexity.k-con-lattice
kind: observation
status: accepted
latex: |-
  A complete lattice has a supremum for every subset. An operator τ is monotone when x≤y implies τ(x)≤τ(y); chain-continuity preserves suprema of chains, and finitary set operators depend only on finite subsets.
informal: |-
  Complete lattice and monotone operator: A complete lattice has a supremum for every subset. An operator τ is monotone when x≤y implies τ(x)≤τ(y); chain-continuity preserves suprema of chains, and finitary set operators depend only on finite subsets.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: K-CON-LATTICE
  package_source_id: kozen2006
  module_id: kozen2006:A
  entry_type: Concept
  label:
  name: Complete lattice and monotone operator
  pdf_page: 49
  printed_page: 38
  importance: foundational
  tags: lattices, fixed-points
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

```yaml
id: st.obs.complexity.k-con-fix
kind: observation
status: accepted
latex: |-
  A prefixpoint satisfies τ(x)≤x; a fixpoint satisfies τ(x)=x. A closure operator is monotone, extensive, and idempotent.
informal: |-
  Prefixpoint, fixpoint, and closure operator: A prefixpoint satisfies τ(x)≤x; a fixpoint satisfies τ(x)=x. A closure operator is monotone, extensive, and idempotent.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: K-CON-FIX
  package_source_id: kozen2006
  module_id: kozen2006:A
  entry_type: Concept
  label:
  name: Prefixpoint, fixpoint, and closure operator
  pdf_page: 50
  printed_page: 39
  importance: foundational
  tags: lattices, fixed-points
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

```yaml
id: st.obs.complexity.k-con-atime
kind: observation
status: accepted
latex: |-
  ATIME(T) and ASPACE(S) are the languages accepted by alternating TMs whose every path respects the stated time or space bound.
informal: |-
  Alternating time and space classes: ATIME(T) and ASPACE(S) are the languages accepted by alternating TMs whose every path respects the stated time or space bound.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: K-CON-ATIME
  package_source_id: kozen2006
  module_id: kozen2006:7
  entry_type: Concept
  label:
  name: Alternating time and space classes
  pdf_page: 59
  printed_page: 48
  importance: foundational
  tags: alternation, complexity-classes
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

```yaml
id: st.obs.complexity.k-con-circuit
kind: observation
status: accepted
latex: |-
  A Boolean circuit is an acyclic network of Boolean gates. CVP supplies both a circuit and its input assignment and asks for the output value.
informal: |-
  Boolean circuit and circuit value problem: A Boolean circuit is an acyclic network of Boolean gates. CVP supplies both a circuit and its input assignment and asks for the output value.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: K-CON-CIRCUIT
  package_source_id: kozen2006
  module_id: kozen2006:6
  entry_type: Concept
  label:
  name: Boolean circuit and circuit value problem
  pdf_page: 42
  printed_page: 31
  importance: foundational
  tags: circuits, p-completeness
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

```yaml
id: st.obs.complexity.k-con-oracle
kind: observation
status: accepted
latex: |-
  An oracle machine may ask membership questions about a fixed set B and receive each answer in one step, enabling relativized classes such as Pᴮ and NPᴮ.
informal: |-
  Oracle Turing machine: An oracle machine may ask membership questions about a fixed set B and receive each answer in one step, enabling relativized classes such as Pᴮ and NPᴮ.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: K-CON-ORACLE
  package_source_id: kozen2006
  module_id: kozen2006:9
  entry_type: Concept
  label:
  name: Oracle Turing machine
  pdf_page: 70
  printed_page: 59
  importance: foundational
  tags: oracles, relativization
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

```yaml
id: st.obs.complexity.k-con-ptm
kind: observation
status: accepted
latex: |-
  A deterministic TM with access to a read-only random bit tape; acceptance probability is measured over uniformly random bit strings.
informal: |-
  Probabilistic Turing machine: A deterministic TM with access to a read-only random bit tape; acceptance probability is measured over uniformly random bit strings.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: K-CON-PTM
  package_source_id: kozen2006
  module_id: kozen2006:13
  entry_type: Concept
  label:
  name: Probabilistic Turing machine
  pdf_page: 88
  printed_page: 77
  importance: foundational
  tags: randomized-computation
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

```yaml
id: st.obs.complexity.k-con-pcp
kind: observation
status: accepted
latex: |-
  PCP(r(n),q(n)) consists of languages with polynomial-time proof verifiers using O(r(n)) random bits and O(q(n)) oracle queries, with perfect completeness and constant soundness.
informal: |-
  PCP(r,q): PCP(r(n),q(n)) consists of languages with polynomial-time proof verifiers using O(r(n)) random bits and O(q(n)) oracle queries, with perfect completeness and constant soundness.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: K-CON-PCP
  package_source_id: kozen2006
  module_id: kozen2006:18
  entry_type: Concept
  label:
  name: PCP(r,q)
  pdf_page: 124
  printed_page: 113
  importance: foundational
  tags: pcp, proof-systems
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

```yaml
id: st.obs.complexity.k-con-fologic
kind: observation
status: accepted
latex: |-
  A structure interprets a signature over a domain; terms denote elements, formulas receive truth values under valuations, sentences have no free variables, and Th(A) is the set of sentences true in A.
informal: |-
  First-order structure, formula, sentence, and theory: A structure interprets a signature over a domain; terms denote elements, formulas receive truth values under valuations, sentences have no free variables, and Th(A) is the set of sentences true in A.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: K-CON-FOLOGIC
  package_source_id: kozen2006
  module_id: kozen2006:E
  entry_type: Concept
  label:
  name: First-order structure, formula, sentence, and theory
  pdf_page: 139
  printed_page: 128
  importance: foundational
  tags: logic, model-theory
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

```yaml
id: st.obs.complexity.k-con-buchi
kind: observation
status: accepted
latex: |-
  An automaton on infinite words whose run is accepting when a designated accepting state occurs infinitely often.
informal: |-
  Büchi automaton: An automaton on infinite words whose run is accepting when a designated accepting state occurs infinitely often.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: K-CON-BUCHI
  package_source_id: kozen2006
  module_id: kozen2006:25
  entry_type: Concept
  label:
  name: Büchi automaton
  pdf_page: 166
  printed_page: 155
  importance: foundational
  tags: omega-automata, buchi
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

```yaml
id: st.obs.complexity.k-con-muller
kind: observation
status: accepted
latex: |-
  An automaton on infinite words with an acceptance family F⊆2^Q; a run is accepting when its set of infinitely recurring states belongs to F.
informal: |-
  Muller automaton: An automaton on infinite words with an acceptance family F⊆2^Q; a run is accepting when its set of infinitely recurring states belongs to F.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: K-CON-MULLER
  package_source_id: kozen2006
  module_id: kozen2006:25
  entry_type: Concept
  label:
  name: Muller automaton
  pdf_page: 168
  printed_page: 157
  importance: foundational
  tags: omega-automata, muller
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

```yaml
id: st.obs.complexity.k-con-rabin
kind: observation
status: accepted
latex: |-
  A deterministic ω-automaton with pairs (Gᵢ,Rᵢ); a run accepts when some Gᵢ is visited infinitely often while the corresponding Rᵢ is visited only finitely often.
informal: |-
  Rabin automaton: A deterministic ω-automaton with pairs (Gᵢ,Rᵢ); a run accepts when some Gᵢ is visited infinitely often while the corresponding Rᵢ is visited only finitely often.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: K-CON-RABIN
  package_source_id: kozen2006
  module_id: kozen2006:26
  entry_type: Concept
  label:
  name: Rabin automaton
  pdf_page: 173
  printed_page: 162
  importance: foundational
  tags: omega-automata, rabin
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

```yaml
id: st.obs.complexity.k-con-sparse
kind: observation
status: accepted
latex: |-
  A language S is sparse when the number of strings of length at most n in S is bounded by a polynomial in n.
informal: |-
  Sparse language: A language S is sparse when the number of strings of length at most n in S is bounded by a polynomial in n.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: K-CON-SPARSE
  package_source_id: kozen2006
  module_id: kozen2006:29
  entry_type: Concept
  label:
  name: Sparse language
  pdf_page: 186
  printed_page: 175
  importance: foundational
  tags: sparse-sets, np-completeness
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

```yaml
id: st.obs.complexity.k-con-usat
kind: observation
status: accepted
latex: |-
  USAT is the promise-style satisfiability problem restricted to formulas having at most one satisfying assignment; it is used as the target of the Valiant–Vazirani randomized reduction.
informal: |-
  Unique satisfiability: USAT is the promise-style satisfiability problem restricted to formulas having at most one satisfying assignment; it is used as the target of the Valiant–Vazirani randomized reduction.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: K-CON-USAT
  package_source_id: kozen2006
  module_id: kozen2006:F
  entry_type: Concept
  label:
  name: Unique satisfiability
  pdf_page: 191
  printed_page: 180
  importance: foundational
  tags: unique-sat, randomized-reductions
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

```yaml
id: st.obs.complexity.k-con-sharp
kind: observation
status: accepted
latex: |-
  #P consists of functions counting accepting computation paths of nondeterministic polynomial-time machines. P^#P denotes polynomial-time computation with access to such counts.
informal: |-
  The class #P: #P consists of functions counting accepting computation paths of nondeterministic polynomial-time machines. P^#P denotes polynomial-time computation with access to such counts.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: K-CON-SHARP
  package_source_id: kozen2006
  module_id: kozen2006:G
  entry_type: Concept
  label:
  name: The class #P
  pdf_page: 196
  printed_page: 185
  importance: foundational
  tags: counting-complexity, toda
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

```yaml
id: st.obs.complexity.k-con-ac0
kind: observation
status: accepted
latex: |-
  AC⁰ is the class of constant-depth, polynomial-size Boolean circuit families with unbounded-fan-in AND and OR gates and negations at inputs.
informal: |-
  AC⁰: AC⁰ is the class of constant-depth, polynomial-size Boolean circuit families with unbounded-fan-in AND and OR gates and negations at inputs.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: K-CON-AC0
  package_source_id: kozen2006
  module_id: kozen2006:30
  entry_type: Concept
  label:
  name: AC⁰
  pdf_page: 204
  printed_page: 193
  importance: foundational
  tags: circuit-complexity, lower-bounds
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

```yaml
id: st.obs.complexity.k-con-godel
kind: observation
status: accepted
latex: |-
  An effective enumeration φ₀,φ₁,… of the partial recursive functions supporting universal simulation and effective program manipulation.
informal: |-
  Gödel numbering: An effective enumeration φ₀,φ₁,… of the partial recursive functions supporting universal simulation and effective program manipulation.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: K-CON-GODEL
  package_source_id: kozen2006
  module_id: kozen2006:33
  entry_type: Concept
  label:
  name: Gödel numbering
  pdf_page: 231
  printed_page: 220
  importance: foundational
  tags: computability, godel-numbering
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

```yaml
id: st.obs.complexity.k-con-arith
kind: observation
status: accepted
latex: |-
  The classes Σₙ⁰ and Πₙ⁰ classify sets definable by n alternating first-order number quantifiers over a decidable predicate, beginning existentially or universally.
informal: |-
  Arithmetic hierarchy: The classes Σₙ⁰ and Πₙ⁰ classify sets definable by n alternating first-order number quantifiers over a decidable predicate, beginning existentially or universally.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: K-CON-ARITH
  package_source_id: kozen2006
  module_id: kozen2006:35
  entry_type: Concept
  label:
  name: Arithmetic hierarchy
  pdf_page: 247
  printed_page: 236
  importance: foundational
  tags: arithmetic-hierarchy, computability
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

```yaml
id: st.obs.complexity.k-con-degrees
kind: observation
status: accepted
latex: |-
  A≤ₘB uses a total recursive many-one map; A≤ᵀB means A is decidable with oracle B. Mutual reducibility defines m-degrees and Turing degrees.
informal: |-
  Many-one and Turing degrees: A≤ₘB uses a total recursive many-one map; A≤ᵀB means A is decidable with oracle B. Mutual reducibility defines m-degrees and Turing degrees.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: K-CON-DEGREES
  package_source_id: kozen2006
  module_id: kozen2006:37
  entry_type: Concept
  label:
  name: Many-one and Turing degrees
  pdf_page: 258
  printed_page: 247
  importance: foundational
  tags: reducibility, degrees
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

```yaml
id: st.obs.complexity.k-con-analytic
kind: observation
status: accepted
latex: |-
  The analytic hierarchy extends the arithmetic hierarchy by allowing second-order quantification over sets or functions; its first universal level Π₁¹ contains well-foundedness-type problems.
informal: |-
  Analytic hierarchy: The analytic hierarchy extends the arithmetic hierarchy by allowing second-order quantification over sets or functions; its first universal level Π₁¹ contains well-foundedness-type problems.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: K-CON-ANALYTIC
  package_source_id: kozen2006
  module_id: kozen2006:39
  entry_type: Concept
  label:
  name: Analytic hierarchy
  pdf_page: 268
  printed_page: 257
  importance: foundational
  tags: analytic-hierarchy, second-order-logic
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

```yaml
id: st.obs.complexity.k-con-fair
kind: observation
status: accepted
latex: |-
  A computation tree is fairly terminating when every fair path terminates; the lecture reduces this property to well-foundedness of recursively encoded ω-trees.
informal: |-
  Fair termination: A computation tree is fairly terminating when every fair path terminates; the lecture reduces this property to well-foundedness of recursively encoded ω-trees.
source_ids:
- src.complexity.kozen2006
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: K-CON-FAIR
  package_source_id: kozen2006
  module_id: kozen2006:41
  entry_type: Concept
  label:
  name: Fair termination
  pdf_page: 278
  printed_page: 267
  importance: foundational
  tags: program-verification, analytic-hierarchy
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

```yaml
id: st.obs.complexity.n-con-cert
kind: observation
status: accepted
latex: |-
  A polynomial-length string u that causes a polynomial-time verifier M(x,u) to accept, thereby certifying that x is a yes-instance of an NP language.
informal: |-
  Certificate / witness: A polynomial-length string u that causes a polynomial-time verifier M(x,u) to accept, thereby certifying that x is a yes-instance of an NP language.
source_ids:
- src.complexity.np-ch2
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: N-CON-CERT
  package_source_id: np_ch2
  module_id: np_ch2:2.1
  entry_type: Concept
  label:
  name: Certificate / witness
  pdf_page: 2
  printed_page: 39
  importance: foundational
  tags: np, certificates
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

```yaml
id: st.obs.complexity.n-con-ndtm
kind: observation
status: accepted
latex: |-
  A TM with multiple transition choices. It accepts an input when at least one sequence of nondeterministic choices reaches the accepting state.
informal: |-
  Nondeterministic Turing machine: A TM with multiple transition choices. It accepts an input when at least one sequence of nondeterministic choices reaches the accepting state.
source_ids:
- src.complexity.np-ch2
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: N-CON-NDTM
  package_source_id: np_ch2
  module_id: np_ch2:2.1
  entry_type: Concept
  label:
  name: Nondeterministic Turing machine
  pdf_page: 4
  printed_page: 41
  importance: foundational
  tags: np, nondeterminism
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

```yaml
id: st.obs.complexity.n-con-cnf
kind: observation
status: accepted
latex: |-
  A CNF formula is a conjunction of clauses, each a disjunction of literals. SAT asks whether a CNF formula is satisfiable; 3SAT restricts each clause to at most three literals.
informal: |-
  CNF, SAT, and 3SAT: A CNF formula is a conjunction of clauses, each a disjunction of literals. SAT asks whether a CNF formula is satisfiable; 3SAT restricts each clause to at most three literals.
source_ids:
- src.complexity.np-ch2
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: N-CON-CNF
  package_source_id: np_ch2
  module_id: np_ch2:2.3
  entry_type: Concept
  label:
  name: CNF, SAT, and 3SAT
  pdf_page: 7
  printed_page: 44
  importance: foundational
  tags: sat, cnf, np-completeness
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

```yaml
id: st.obs.complexity.n-con-levin
kind: observation
status: accepted
latex: |-
  A Levin reduction efficiently maps both instances and witnesses between NP problems. A parsimonious reduction additionally preserves the number of witnesses.
informal: |-
  Levin and parsimonious reductions: A Levin reduction efficiently maps both instances and witnesses between NP problems. A parsimonious reduction additionally preserves the number of witnesses.
source_ids:
- src.complexity.np-ch2
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: N-CON-LEVIN
  package_source_id: np_ch2
  module_id: np_ch2:2.4
  entry_type: Concept
  label:
  name: Levin and parsimonious reductions
  pdf_page: 13
  printed_page: 50
  importance: foundational
  tags: reductions, counting
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

```yaml
id: st.obs.complexity.n-con-selfred
kind: observation
status: accepted
latex: |-
  SAT can recover a satisfying assignment by repeatedly fixing one variable and querying satisfiability of the smaller formulas; this converts a decision procedure into a search procedure.
informal: |-
  Downward self-reducibility: SAT can recover a satisfying assignment by repeatedly fixing one variable and querying satisfiability of the smaller formulas; this converts a decision procedure into a search procedure.
source_ids:
- src.complexity.np-ch2
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: N-CON-SELFRED
  package_source_id: np_ch2
  module_id: np_ch2:2.6
  entry_type: Concept
  label:
  name: Downward self-reducibility
  pdf_page: 18
  printed_page: 55
  importance: foundational
  tags: search-vs-decision, self-reduction
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

```yaml
id: st.obs.complexity.n-con-nexp
kind: observation
status: accepted
latex: |-
  EXP is deterministic exponential time ⋃₍c₎DTIME(2^{nᶜ}); NEXP is its nondeterministic analogue ⋃₍c₎NTIME(2^{nᶜ}).
informal: |-
  EXP and NEXP: EXP is deterministic exponential time ⋃₍c₎DTIME(2^{nᶜ}); NEXP is its nondeterministic analogue ⋃₍c₎NTIME(2^{nᶜ}).
source_ids:
- src.complexity.np-ch2
used_symbols: []
depends_on: []
confidence: 0.78
proof_sketch: ''
notes: |-
  imported_from: complexity_theory_kb.zip
  source_archive: /Users/afreitas/Downloads/complexity_theory_kb.zip
  package_entry_id: N-CON-NEXP
  package_source_id: np_ch2
  module_id: np_ch2:2.6
  entry_type: Concept
  label:
  name: EXP and NEXP
  pdf_page: 19
  printed_page: 56
  importance: foundational
  tags: exponential-time, padding
  extraction_scope: curated unnumbered concept/result
  review_status: curated
  normalization: Concept imported as derived observation.
```

# Imported Relations

| relation_id | subject_statement_id | predicate | object_statement_id | package_subject_id | package_object_id | note |
|---|---|---|---|---|---|---|
| rel.complexity.001 | st.def.complexity.np-ch2-d-2-1 | equivalent_via | st.thm.complexity.np-ch2-t-2-6 | np_ch2:D:2.1 | np_ch2:T:2.6 | Verifier and nondeterministic-machine definitions of NP are equivalent. |
| rel.complexity.002 | st.thm.complexity.np-ch2-t-2-6 | aligns_with | st.def.complexity.kozen2006-d-2-4 | np_ch2:T:2.6 | kozen2006:D:2.4 | Both identify NP with polynomial nondeterministic time. |
| rel.complexity.003 | st.def.complexity.np-ch2-d-2-5 | aligns_with | st.def.complexity.kozen2006-d-2-2 | np_ch2:D:2.5 | kozen2006:D:2.2 | Both define nondeterministic time classes. |
| rel.complexity.004 | st.def.complexity.np-ch2-d-2-7 | weaker_than | st.obs.complexity.k-con-lred | np_ch2:D:2.7 | K-CON-LRED | The chapter uses polynomial-time Karp reductions; Kozen often uses the stronger logspace many-one reductions. |
| rel.complexity.005 | st.lem.complexity.kozen2006-l-5-4 | explains | st.def.complexity.np-ch2-d-2-7 | kozen2006:L:5.4 | np_ch2:D:2.7 | Every logspace many-one reduction is also a polynomial-time Karp reduction. |
| rel.complexity.006 | st.thm.complexity.np-ch2-t-2-10 | aligns_with | st.thm.complexity.kozen2006-t-6-2 | np_ch2:T:2.10 | kozen2006:T:6.2 | Both state Cook–Levin; Kozen strengthens the reduction to logspace many-one completeness. |
| rel.complexity.007 | st.lem.complexity.np-ch2-l-2-11 | component_of | st.thm.complexity.np-ch2-t-2-10 | np_ch2:L:2.11 | np_ch2:T:2.10 | SAT hardness is the main hardness half of Cook–Levin. |
| rel.complexity.008 | st.lem.complexity.np-ch2-l-2-14 | component_of | st.thm.complexity.np-ch2-t-2-10 | np_ch2:L:2.14 | np_ch2:T:2.10 | SAT ≤ᵖ 3SAT transfers NP-hardness from SAT to 3SAT. |
| rel.complexity.009 | st.thm.complexity.np-ch2-t-2-8 | aligns_with | st.lem.complexity.kozen2006-l-5-1 | np_ch2:T:2.8 | kozen2006:L:5.1 | Both use transitivity of reductions. |
| rel.complexity.010 | st.thm.complexity.np-ch2-t-2-8 | aligns_with | st.lem.complexity.kozen2006-l-5-3 | np_ch2:T:2.8 | kozen2006:L:5.3 | Both express closure of efficient computation under reduction. |
| rel.complexity.011 | st.thm.complexity.kozen2006-t-6-1 | parallel_to | st.thm.complexity.kozen2006-t-6-2 | kozen2006:T:6.1 | kozen2006:T:6.2 | CVP is complete for P; SAT is complete for NP. |
| rel.complexity.012 | st.thm.complexity.kozen2006-t-8-2 | uses | st.thm.complexity.kozen2006-t-7-4 | kozen2006:T:8.2 | kozen2006:T:7.4 | QBF membership and hardness are naturally expressed through alternation. |
| rel.complexity.013 | st.thm.complexity.kozen2006-t-8-4 | reduces_from | st.thm.complexity.kozen2006-t-8-2 | kozen2006:T:8.4 | kozen2006:T:8.2 | Generalized geography is shown PSPACE-hard by reducing QBF. |
| rel.complexity.014 | st.thm.complexity.kozen2006-t-11-3 | same_statement_as | st.thm.complexity.kozen2006-t-12-1 | kozen2006:T:11.3 | kozen2006:T:12.1 | Lecture 11 states Ruzzo’s theorem; Lecture 12 proves it. |
| rel.complexity.015 | st.thm.complexity.k-res-ip | summarizes | st.def.complexity.kozen2006-d-15-1 | K-RES-IP | kozen2006:D:15.1 | The IP definition is the basis for the equality IP=PSPACE. |
| rel.complexity.016 | st.thm.complexity.kozen2006-t-18-1 | strengthens | st.thm.complexity.k-res-pcpweak | kozen2006:T:18.1 | K-RES-PCPWEAK | The full PCP theorem improves randomness from O(n³) to O(log n) while retaining O(1) queries. |
| rel.complexity.017 | st.thm.complexity.kozen2006-t-f-2 | feeds_into | st.thm.complexity.kozen2006-t-g-1 | kozen2006:T:F.2 | kozen2006:T:G.1 | Valiant–Vazirani isolation is one of the randomized/counting ingredients around Toda’s theorem. |
| rel.complexity.018 | st.thm.complexity.kozen2006-t-h-4 | implies | st.cor.complexity.kozen2006-c-h-5 | kozen2006:T:H.4 | kozen2006:C:H.5 | The strong parity circuit lower bound yields an oracle with PHᴬ≠PSPACEᴬ via Theorem 30.1. |
| rel.complexity.019 | st.lem.complexity.kozen2006-l-38-4 | supports | st.thm.complexity.kozen2006-t-38-1 | kozen2006:L:38.4 | kozen2006:T:38.1 | A low simple set supplies the intermediate r.e. degree used in the Friedberg–Muchnik theorem. |
| rel.complexity.020 | st.thm.complexity.np-ch2-t-2-22 | uses_technique | st.thm.complexity.kozen2006-t-3-1 | np_ch2:T:2.22 | kozen2006:T:3.1 | Both use padding/diagonalization ideas to transfer separations across resource scales. |

# Open Gaps

# Change Log

- 2026-07-11: Imported complexity_theory_kb.zip into P vs NP KB (152 canonical, 35 derived, 20 relations added; 0 statements already present).
- 2026-03-11: Parsed deep-research-report.md into PvsNP KB Added 64 canonical and 0 derived statements.

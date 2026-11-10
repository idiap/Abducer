<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Strict-Prefix Qrep Replay Normalizer

- Status: `proved_in_revised_tex`
- TeX proposition: `Strict-prefix Qrep replay normalizer`
- TeX label: `prop:strict-prefix-qrep`
- Criteria affected: `C5`, `C8`, `C10`, `C11`
- Result role: `proof_system_bridge`

## Purpose

This packet converts the latest Qrep discovery thread into a paper-level bridge rather than another exploratory result.  The issue is whether quotient compression can be counted as transparent support.  The answer is yes only when every quotient representative use is replayable from a same-theory certificate that was already visible at a strict earlier proof prefix.

## Statement

Consider a finite proof transcript with ordinary displayed support \(K_0(\pi)\) and quotient-representative dictionary entries
\[
  e=(a_e,r_e,F_e,t_e,u_e,\operatorname{rank}(e)).
\]
Here \(a_e\) is the row being replaced, \(r_e\) is the representative, \(F_e\) is a same-theory certificate forest for \(a_e\equiv r_e\), \(t_e\) is the certificate line, and \(u_e\) is the first representative-use line.

If every used entry is strict-prefix, rank-decreasing, dependency-closed, and append-only, then there is a canonical replay expansion replacing each representative use by \(r_e\) plus the already charged certificate forest \(F_e\).  The expanded transcript has support contained in
\[
  K_{\mathrm{Qrep}}(\pi)
    = K_0(\pi)\cup\bigcup_{e\in\operatorname{Used}(\pi)}
       \bigl(\operatorname{supp}(F_e)\cup\{a_e,r_e\}\bigr),
\]
and size/ledger bounded by the displayed support plus the dictionary charge
\[
  D_Q(\pi)=\sum_{e\in\operatorname{Used}(\pi)}
       \bigl(|F_e|+|\operatorname{supp}(F_e)|+1\bigr).
\]
Therefore any support-local normalization whose only compressed step is strict-prefix Qrep inherits the formula-footprint lower bound with support budget enlarged by \(O(D_Q(\pi))\).

If strict-prefix visibility fails, no transparent-support conclusion follows.  The first unsafe representative use gives a private-row falsifier in the abstract label model: two completions agree on the visible prefix but differ on the hidden row or hidden certificate bit controlling the quotient merge.

## Before/After Shift

Before this packet, Qrep quotient compression was only a promising discovery-loop convention.  After it, quotient compression has an admission test: it is allowed only as proof-carrying, strict-prefix, rank-decreasing replay.  Delayed same-theory evidence is no longer harmless bookkeeping; it is hidden support.

## Boundary

This is not a lower bound for \(P\) versus \(NP\), not a lower bound for \(H_N\), and not a theorem for arbitrary semantic SAT pruning.  It does not prove a RealSATInfluenceRealizer theorem.  It applies only to proof objects where the quotient dictionary, certificate forests, ranks, dependencies, and first-use lines are verifier-visible.

## Gate Impact

This is C11-admitted as a proof-system bridge.  It strengthens the same formula-footprint spine by making quotient compression replayable only when its support is already charged.  It does not create a new result package or replace the remaining top-paper blocker: a stronger recognizable proof system still needs an independently proved support audit, controlled expansion, or explicit SAT-family theorem.

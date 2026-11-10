<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Support-Audit Necessity Separator

- Status: `proved_in_revised_tex`
- TeX proposition label: `prop:support-audit-necessity`
- Criteria affected: `C5`, `C8`, `C9`, `C11`

## Result

The revised paper now proves that support audits are not cosmetic metadata.

For every finite formula-label set \(T\) and every labeling
\(\alpha:T\to\{0,1\}\), define:

- unit constraints \(\Gamma_T\) fixing each \(Y_u\) to \(\alpha(u)\);
- one blocking clause \(\Phi_T\) forbidding the joint assignment \(\alpha\).

Then \(\Phi_T\wedge\Gamma_T\) has an LRAT-style clausal refutation of length
\(O(|T|)\), but any sound support declaration \(S\) for \(\Gamma_T\) must contain
all of \(T\).  If \(u\in T\setminus S\), a completion can agree with
\(\alpha\) on \(S\) and flip \(u\), making \(\Gamma_T\) unsatisfiable.

## Proof Skeleton

1. Resolve the blocking clause against the \(|T|\) unit clauses one variable at
   a time; this gives a linear-size clausal refutation.
2. If a declared support omits \(u\in T\), choose a completion that preserves
   the support and flips \(u\).
3. The corresponding unit clause in \(\Gamma_T\) is false, so no auxiliary
   witness can satisfy the constraint package.
4. Therefore clausal refutation soundness alone does not prove a small
   completion-local support.  The support audit is an independent invariant.

## Gate Impact

This is a C11-admitted boundary result.  It strengthens the LRAT discussion by
explaining why unaudited LRAT/DRAT cannot simply inherit the support-audited
normalizer: a checked unsatisfiability trace may be short while the sound
support needed for completion locality is as large as the hidden label set it
fixes.

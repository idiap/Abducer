<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Strict-Prefix Qrep Prefix-Scan Examples

- Status: `implemented`
- Verifier: `agentic/scripts/check_strict_prefix_qrep_examples.py`
- Criteria affected: `C5`, `C8`, `C10`, `C11`
- Supports theorem: `prop:strict-prefix-qrep`

## Purpose

This artifact makes the Qrep replay proposition finite and inspectable.  The checker scans proof-visible quotient dictionary entries and verifies the exact temporal condition used in the paper: the same-theory certificate forest must be displayed before the representative is first used.

## Accepted Example

`valid_two_row_strict_prefix_merge` has one dictionary entry \(qrep\_A\_B\).  The certificate line is `3`, the first representative-use line is `4`, the dependency list is empty, the entry is append-only, and the representative is advice-free.  The prefix scan accepts and computes
\[
  K_{\mathrm{Qrep}}=\{\texttt{final\_lb\_line},\texttt{formula\_eval\_parent},\texttt{row\_A},\texttt{row\_B}\},
  \qquad D_Q=4.
\]

## Rejected Example

`delayed_certificate_private_row_falsifier` has the same local merge but sets `cert_line = 5` and `first_use_line = 4`.  The checker rejects it with `certificate_not_strict_prefix`.  This is the finite version of the private-row falsifier in the paper: before line `4`, the visible prefix has not charged the same-theory evidence, so quotient representative reuse is hidden support.

## Boundary

The examples check only the strict-prefix Qrep replay condition.  They do not prove a lower bound for \(P\) versus \(NP\), do not prove an \(H_N\) lower bound, do not instantiate `RealSATInfluenceRealizer_N^{arb}`, and do not give an unaudited LRAT/DRAT support audit.

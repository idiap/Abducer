<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# YM Artifact-Or-Stop Generative Quality Fixtures

These cases are prompt-level fixtures for review cycles. They test whether a
polished theorem-shaped packet is rejected when it preserves the same endpoint
artifact debt instead of producing a decisive artifact, falsifier, demotion
packet, or quarantine packet.

## Case A: fluent packet with no endpoint artifact

Input: a fluent Route A theorem narrative with definitions, equations,
falsifiers, and a final request to compute endpoint source intervals and
`T_tail` later.

Expected verdict: reject repeated artifact-free request.

## Case B: new wording of the same T_tail blocker

Input: a packet renames the blocker as a regulator-uniform boundary-OPE
remainder but still asks for the endpoint source table and `T_tail` next.

Expected verdict: classify as incremental drift and reject broad reasoning.

## Case C: table contract but no data

Input: a packet attaches the endpoint source table contract with all fields but
does not compute any source row.

Expected verdict: accept only as artifact_sprint. Do not promote the proof.

## Case D: negative I_gate interval

Input: a packet attaches an endpoint row table with `I_gate` upper endpoint
below zero and a cutoff-uniform tail.

Expected verdict: accept as a finite falsifier with explicit overclaim boundary.

## Case E: physical impact without carrier

Input: a packet claims major Yang-Mills relevance but names no gauge-invariant
physical carrier, same-theory transfer, or Clay-facing target gate.

Expected verdict: reject physical promotion and route to demotion or reframe.

<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Generative Visual QA: Reasoning Monitor

## Purpose

Use this checklist when reviewing `agentic/reports/reasoning_monitor/latest.html` as a mathematical reasoning monitor rather than a decorative dashboard.

## Required Probes

1. Open the HTML from the filesystem and verify that no network access is needed.
2. Confirm the first viewport names `yang-mills-existence-and-mass-gap-target`, shows target commitments, frontier count, candidate count, proof obligations, and stale-workflow findings.
3. Use the lane, status, commitment, evidence, and text filters. The visible cards should change without losing access to evidence paths or proof obligations.
4. Inspect at least one proof-queue route and one discovery-branch route. Each must expose target relevance, drift risk, cited commitments, validation gates, obligations, and disconfirming observations.
5. Inspect the Drift tab. Historical P vs NP and Hille-Yosida artifacts may be listed only as historical, never as active Yang-Mills state.

## Rejection Criteria

Reject the report if:

- visual polish makes proof debt look solved;
- uncertainty appears only in hidden details;
- evidence paths are absent or only decorative;
- route cards omit target relevance or drift risk;
- the page requires external scripts, CSS, fonts, or images;
- the active target differs from `agentic/state/current_target.json`;
- mobile or narrow width causes controls, headings, or cards to overlap.

## Passing Standard

The report passes when a mathematician can see the active target spine, a researcher can inspect why each route is active or blocked, and an epistemologist can trace every substantive claim to evidence or an explicit obligation.

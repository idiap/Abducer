<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Release Gates

Advance stages only when the current gate is satisfied.

## Gate 1: Spec Ready

- Problem statement is concrete.
- In-scope and out-of-scope are explicit.
- Acceptance evidence is named.
- Unknowns and assumptions are separated.

## Gate 2: Contract Ready

- Invocation mode is named.
- Inputs and outputs are typed.
- One durable primary output is clear.
- Reasoning-log sidecar is defined.
- Runtime boundaries and provenance are explicit when relevant.

## Gate 3: Quality Criteria Ready

- Deterministic and interface-side quality criteria are explicit.
- Generative and content-side quality criteria are explicit.
- Criteria include examples of good versus weak behavior.
- Criteria include a usable scoring or verdict method.
- Criteria identify likely failure modes worth testing.

## Gate 4: Mapping Ready

- Current repo surfaces are evidence-backed.
- Proposed touch set is narrow and justified.
- Reusable code and risky zones are identified.
- Test and doc surfaces are known.

## Gate 5: Dependency Map Ready

- `uv` bundles, runtime dependencies, reference KBs, backend profiles, and workspace mounts are named when relevant.
- Declared, inferred, and hidden dependencies are separated.
- Verification commands or checks are named for important dependencies.
- Planning and testing stages can rely on the dependency picture without guessing.

## Gate 6: Slice Ready

- Each slice has exit criteria.
- File touch expectations are explicit.
- Validation is attached per slice.
- Rejected alternatives are recorded.
- The active plan is reflected in `to-do.md`.

## Gate 7: Test Strategy Ready

- Deterministic test surfaces are named.
- Generative probe families are named.
- Codex validation protocol is explicit.
- The oracle for content quality is explicit.
- Important failures have a path to become regressions.

## Gate 8: Execution Ready

- The active slice is identified.
- Deviations from spec are called out.
- Deterministic and generative tests are named before coding finishes.
- The active item or slice is visible in `to-do.md`.

## Gate 9: Reflective Refinement Ready

- The quality criteria are being used, not merely referenced.
- At least two refinement cycles have been run unless the first pass was blocked before meaningful output existed.
- Each cycle localizes concrete weaknesses.
- Revisions are targeted and evidence-backed.
- The loop ends with a clear status: improved, blocked, or still weak.

## Gate 10: Verification Ready

- Findings are severity-ranked.
- Supported claims and unsupported claims are separated.
- Deterministic and generative test evidence are recorded.
- Dependency evidence and remaining setup risk are recorded.
- Residual risk is named.
- Release gate verdict is explicit.

## Gate 11: Handoff Ready

- Final artifact map is complete.
- Prism onboarding translation is clear.
- Dependency translation is clear.
- `to-do.md` is reconciled with finished, deferred, or blocked work.
- Remaining debt is separated from shipped work.
- Next import or adoption steps are concrete.

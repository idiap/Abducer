---
name: to-prism
description: Convert an external Codex, Claude, OpenCode, or Open Agent Skills project into a checked, separately runnable Prism project. Use for an end-to-end conversion; use a narrower to-prism skill for one review phase.
---
<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Convert a project to Prism

Coordinate the conversion while leaving deterministic extraction, validation,
rendering, and comparison to [`bin/to-prism`](../../bin/to-prism).

## Establish the boundary

Read [the conversion contract](../../references/conversion-contract.md) before
starting. Require explicit, disjoint source and output paths and identify the
requested output class (`linked` or `portable`). Treat source as read-only.
Discovery never authorizes commands, hooks, scripts, package installation,
network access, or model calls.

Read [the output contract](../../references/output-contract.md) when planning
generation or assessing completion. The deliverable must contain canonical,
checked `.prism` workflow source. JSON IR and reports are supporting evidence,
not alternative final representations.

Use [the layer model](../../references/layers.md) to keep discovery, review
artifacts, canonical `.prism`, material adapters, and verification evidence
separate. Use [the type taxonomy](../../references/type-taxonomy.md) whenever a
conversion chooses provenance, assurance, reasoning, capability, or failure
contracts.

## Route by gated phase

Use `bin/to-prism <command> --help` for the installed command syntax, then
advance only when the preceding artifacts validate:

1. `inspect`: create the source fingerprint and complete inventory without
   execution.
2. Baseline, only if useful: apply `$to-prism-baseline`; show the exact proposed
   descriptor and obtain authorization before native execution.
3. Types: apply `$to-prism-derive-types` to derive reviewed, project-specific
   domain and epistemic contracts. Do not admit generic public ports. Require
   its occurrence-granularity test and many-to-many occurrence/skill map;
   skill count never determines reasoning count.
4. `model`: apply `$to-prism-model-workflows` to resolve material contract or
   topology judgments using the reviewed types; retain uncertainty that does
   not yet need resolution.
5. Reasoning: apply `$to-prism-map-reasoning` only when source evidence shows a
   genuine epistemic operation. Operational-only is a valid result. In this
   conversion profile every epistemic occurrence returns `Generated[T]`;
   stronger provenance or assurance belongs to an explicit later boundary. A
   mixed workflow may interleave `material_kind: agent` occurrences with
   `material_kind: computed` operational steps only when each computed step is
   backed by an exact reviewed Python leaf adapter and a named deterministic
   procedure that explicitly constructs `Computed[T]`.
   For a mixed workflow, require an approved `reasoning_projection` before
   emitting `reasoning.prism`. The projection aggregates material steps by
   epistemic commitment, records every occurrence-to-material mapping, and
   declares sequence/parallel topology explicitly. Never derive it from hook,
   skill, file, or prompt order. Generated `reasoning.prism` contains only
   imports, concise comments, and the core `reasoning` block; occurrence
   signatures and relation contracts are emitted separately.
   Materialization must then compile the deduplicated skills contributed by
   each occurrence's reviewed `material_steps`, emit an exact typed occurrence
   implementation and relation builders, and instantiate the named reasoning
   workflow. For projected mixed workflows, treat `main.prism` as the
   human-scale reasoning entrypoint and retain the detailed pipeline in
   `material_main.prism`.
6. Documentation: apply `$to-prism-document-workflows` when workflow purpose
   and stage composition should be emitted as comments. Documentation may
   explain only reviewed, source-grounded workflows, occurrences, and exact
   nominal contracts; it must not introduce or disguise a generic port,
   semantic gap, skill-derived occurrence boundary, or stronger assurance.
7. Review the plan: ensure critical proposed choices are reviewed/approved and
   unsupported behavior is explicit.
8. `generate`: let the CLI render, dependency-lock, check, and compile in
   staging. Require every projected occurrence and relation to have a concrete
   binding and run the projected `main.prism` smoke fixture. Do not manually
   patch generated output to bypass an IR decision.
9. Parallel tests, when parity evidence is requested: apply
   `$to-prism-design-parallel-tests` to freeze workflow correspondence, typed
   observables, normalizers, independent oracles, negative controls, and the
   authority envelope. Apply `$to-prism-run-parallel-tests` only to an approved
   manifest. Parallel tests compare the reviewed workflow contracts; they do
   not excuse generic types, alter occurrence granularity, or promote
   `Generated[T]` to a stronger epistemic status.
10. `verify`: apply `$to-prism-review-preservation` to the resulting independent
   evidence and publication claims.
11. Publish only through the CLI's atomic publication path.

For a changed upstream project or an existing conversion, route to
`$to-prism-update` instead of starting a clean conversion.

## Stop at real gates

Pause for user input when authorization would expand to native/live execution,
network or credential access, or package installation. Also pause when distinct
answers to an ambiguous contract, workflow boundary, custom reasoning method,
critical unsupported behavior, or oracle would materially change generated
types or publication eligibility.

Do not ask about ambiguity that can remain explicitly unresolved without
changing the current phase. Record proposed, reviewed, and approved decisions
with their evidence; never encode a guess only in prose.

## Completion

Finish only when source fingerprints are unchanged, all in-scope elements have
a disposition, generated entry points check and compile, the selected
dependency closure is locked, preservation claims satisfy the reviewed policy,
and the output has been atomically published. A portable result additionally
needs a successful offline clean-room relocation test. Report linked bindings,
unestablished preservation levels, unsupported behavior, and unresolved debt
without softening them.

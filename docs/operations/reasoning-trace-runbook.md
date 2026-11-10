<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Public reasoning trace runbook

Use this runbook to build and review the expert HTML trace for a named workflow. Generic mode is opt-in; the established main-workflow reports remain unchanged.

## Build and validate

Commands accept repository-relative paths. Use the help flag for the exact options supported by the installed implementation.

```bash
python agentic/scripts/build_public_reasoning_trace.py --help
python agentic/scripts/build_public_reasoning_monitor_packet.py --help
python agentic/scripts/generate_public_reasoning_trace_html.py --help
python agentic/scripts/validate_public_reasoning_trace.py
python agentic/scripts/validate_public_reasoning_trace.py path/to/trace.json
python agentic/scripts/build_reasoning_trace_coverage.py --help
```

With no trace argument, the validator checks the complete committed named-workflow and Route-A fixture set, matching packet identity and embedded HTML data, offline HTML constraints, and control, semantic, evidence, authority, and HTML coverage; pass one or more paths for a focused trace-only check. Build order is trace, packet, validation, HTML, and coverage. Validation failures stop release; an intentional incomplete legacy trace may render, but its incomplete requirements must remain visible and cannot count as semantic coverage. The repository's default read-only `agentic_check.py` gate runs the no-argument release-fixture validation without regenerating reports.

## Authoring a public inference

Record only an inspectable summary that a reviewer can evaluate from artifacts:

1. Identify the run, workflow, profile if any, step, skill, attempt, event, and causal parents.
2. State the public question and typed premises.
3. Name the transformation or inference operator and provide a bounded public warrant.
4. State the conclusion, uncertainty, scientific scope, and before/after scope.
5. Link typed evidence as supporting, refuting, constraining, or background.
6. Record alternatives, their dispositions, falsifiers, and unresolved obligations.
7. State the authority exercised and the authority explicitly absent.
8. Record artifact validation, claim epistemic status, and workflow disposition separately.

Do not record private chain-of-thought, prompts, secrets, arbitrary tool payloads, or rationales inferred only from filenames and successful hooks. If the available artifact does not establish a premise or warrant, emit `trace_incomplete` and identify the missing requirement.

## Expert review

Review the HTML from the filesystem with networking disabled. An expert should be able to answer:

- What changed, and what question did the change answer?
- Which premises, evidence, and transformation support the conclusion?
- What was rejected, refuted, demoted, quarantined, or left unknown?
- In which model or regime does the claim hold, and did scope change?
- Which authority was exercised, and which authority was absent?
- What proof debt or other obligation remains?
- Which gate decided the disposition, and where was the result handed off?

Inspect the Trace Coverage view last. Control-event, substantive inference, evidence-resolution, negative-evidence, authority, and HTML-visibility coverage are separate measures. A hook-only run must not report complete semantic coverage.

## Failure triage

- `missing-causal-parent` or `causal-cycle`: repair event correlation; do not reorder historical events to hide it.
- `non-portable-path`: replace local absolute paths with repository-relative paths, or explicitly mark an external reference.
- `missing-public-rationale`: add an artifact-grounded summary or keep the gap as `trace_incomplete`.
- `authority-free-epistemic-upgrade`: restore the prior epistemic state or route to an authorized gate.
- `unsupported-scope-widening`: supply an explicit bridge with evidence or retain the narrower claim.
- HTML packet mismatch: regenerate from the validated packet; never patch embedded JSON by hand.
- Blind-review identity leak: remove identity from adjudication events and expose it only in the post-decision audit lane.

## Release gate

Release requires all workflow and Route-A semantic fixtures, negative paths, offline HTML checks, compatibility tests, the coverage report, and an expert review record to agree. Cross-workflow handoffs must be included. Do not switch the main default as part of this release.

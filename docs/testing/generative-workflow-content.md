<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Generative workflow content tests

These tests ask a model to perform the substantive work described by each
workflow's real skill instructions, then ask a separate model session to judge
the resulting content. They complement native hook and schema tests. A valid
JSON packet or a fluent paragraph does not establish that a derivation, critique,
evidence interpretation or final synthesis is correct.

The initial inventory has 19 canonical workflows and 273 evaluation bindings.
Bindings include declared steps, profile specialists, DAG nodes and unordered
task members. The inventory preserves those distinctions: it does not invent
runtime ordering or imply that a disabled workflow was activated.

## Prepare a run

From the repository root:

```sh
.venv/bin/python tests/generative/workflow_content_suite.py prepare /tmp/workflow-content-run
```

This freezes source hashes, full skill instructions and 38 constructive/adverse
case packets plus four conditional-activation probes: two P-vs-NP cases, a paper-ready handoff and an active Route A matrix audit. Authors receive `author_packets/` only. Judges receive the matching
`judge_packets/`, which include explicit expected outcomes and the independent
content rubric. Preparing packets does not generate any candidate or judgment.
The command also writes the reusable five-probe judge control packet and its
separate answer key. Judges receive only `controls/packet.json`; keep the key
out of their task context. Both files are bound into the run manifest.

Use separate session tasks to author and judge. Capture their actual task IDs in
`author_session` and `judge_session`. The session model/version or usage must stay
unknown when not exposed by the host; task separation does not prove different
model or training provenance. All inputs are labeled synthetic research fixtures,
not real literature or native proof receipts.
This separation is enforced by task instructions in the shared workspace, not
by filesystem access control. It is not a cryptographic blinding guarantee.

## Content to generate and judge

Each author writes `candidates/<case_id>.json` with the case/workflow/packet
identities, `execution_mode: session_content_exercise`, its actual task identity,
every canonical step ID and skill ID, explicit source or upstream-step references,
the substantive output text, and a whole-workflow synthesis with unresolved
obligations. Steps should contain actual calculations, hypotheses, critiques,
decisions or manuscript text, rather than descriptions of what a skill would do.

For example, the supplied diagonal transfer operator permits an exact finite
spectral calculation. A good result computes that bound, uses the right temporal
spacing, and explains why it does not establish a continuum Yang–Mills theorem.
A failure can be a wrong factor, an unsupported uniformity claim, a generic
refusal that ignores the solvable finite problem, or a downstream synthesis that
silently reinstates a previously rejected inference.

Separate judges write `judgments/<case_id>.json`. They bind the canonical candidate
hash, assess every step and the full workflow, score each anchored rubric
dimension, and record noncompensatory gates. Evidence records quote literal
candidate text, explain its significance and cite supplied source IDs. Shared
quotes may support multiple criteria when the reasoning actually applies to
each. Missing content requires an explicit searched scope and missing obligation.

The harness checks evidence integrity and complete accounting; it does not
replace these semantic judgments with keywords. Fluent invalid, contradicted,
scope-inflated and cross-target controls test judge sensitivity. A correct bounded
positive result tests whether judges merely reject everything. Preserve all
original judgments when reviewers disagree.

## Audit and inspect

```sh
.venv/bin/python tests/generative/workflow_content_suite.py audit /tmp/workflow-content-run
.venv/bin/python -m pytest -q tests/generative/test_workflow_content_suite.py
```

The audit writes JSON, Markdown and a standalone HTML report with expandable
step content and judgments. Exit 1 means missing/invalid coverage, missing conditional applicability/positive-branch probes, or incomplete/failed judge calibration; exit 2 means
coverage is complete but some content is partial or failing; exit 0 means all
audited case verdicts pass and each actual judge passes its hidden controls.
Unresolved disagreements must also be reviewed before interpreting the suite as semantically reliable.
The pytest tests exercise auditor rejection boundaries, not model quality.

No evaluation installs hooks, changes skill composition, executes production
workflows, invokes scientific providers, publishes results or grants theorem
authority. Native preservation remains separately pinned by
`test_pre_normalization_hook_compatibility.py`.

Additional refinement cases can be prepared with the `extend` command. It
rejects changes to any previous author or oracle packet, adds only new cases,
and records the previous manifest digest. Existing candidate/judge evidence is
retained; an extension never retroactively rewrites an author's input.

The recorded first run is in
`.prism/realistic-generative-workflow-tests/run-v1/`. Its HTML report exposes all
generated content and primary assessments. A failed content gate is an observed
failure of that case's output; it is not by itself proof that every execution of
the underlying workflow fails. Alternative branches and profiles are exercised
separately, and the inventory records where native ordering is unspecified.

The supplemental conditional applicability audit distinguishes active content,
inactive guard decisions and unknown conditional proposals. Inactive/unknown
scientific-content scores are null; primary rubric numbers on such rows assess
the actual guard explanation, not an executed scientific operation. Read these
supplements alongside the primary report. The original rubric requested null
inapplicable scores, while its compact validator required numeric dimensions.
The harness now validates a separate applicability account, including source
quotes, candidate hashes and mandatory null scientific-content scores for
inactive/unknown guards. It requires an active probe for each guarded binding.
This preserves original numeric guard assessments without relabeling them as
scientific execution.

The first run also retains a third-review adjudication for the atlas cases. Its
canonical philosophical vocabulary was absent from the sealed source packet;
the primary failure is therefore qualified as a useful missing-input partial.
The original failure and both reviewers' reasoning remain available. All other
material failures retain their original interpretation. Future fully supplied
atlas cases are needed to assess that complete canonical sweep.

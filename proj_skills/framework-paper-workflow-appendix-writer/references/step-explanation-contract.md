<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Step explanations that a reader can reconstruct

This contract is shared by extraction, example design, both appendix writers,
review and assembly. It closes a specific failure: covering every signature while
leaving the reasoning inside each operation compressed into a general paragraph.

## Authoring unit

Create a `StepExplanationPacket` in the manual paper lane. Freeze scope from the
native manifest, not the manuscript. Identify each step by workflow and exact local
binding, including unresolved projections. Keep native signatures and source hashes.
For each step author seven substantive fields:

1. `purpose`: the question this step resolves and why the next step needs it.
2. `input`: actual information consumed, including retained context and named joins.
3. `procedure`: the internal moves prescribed by the sources; explain how the
   input changes. State when the native algorithm is unspecified.
4. `criterion`: what distinguishes an admissible result from a rejected or
   inconclusive one. Do not invent thresholds or total decision rules.
5. `output`: what the result adds, restricts or leaves conditional.
6. `failure_next`: what failure changes and who consumes the output. Distinguish
   original routing policy from an executable native branch.
7. `example`: concrete before/after content in one continuous case per workflow.

## Structured, succinct presentation

Present a step as a short title and native binding, followed by separate **Purpose,
Input, Method, Check, Output, Next, Example** fields in that order. These display
labels map to the seven existing fields above; they do not change the packet schema.
Use the reusable renderer for the appendix so no field disappears into another.

Write Purpose as one direct sentence. Write Input and Output as short noun phrases
or semicolon-separated named items: scientific object first, then indispensable
scope, premises, retained context or qualification. Output names the returned
artifact and its epistemic status; Next names its consumer and conditional routing.
For example: **Input:** candidate claim; regime; retained premises. **Output:**
targeted counterexample; rejected premise; surviving conditional claim. **Next:**
send the claim and finding to calibration. Do not present a proposed route as a
native branch, or turn an assessment into a proved result through compression.

Keep Method's distinctive transformation, Check's admissibility condition and
Example's concrete before/after reasoning. Remove repeated setup and generic
phrases such as “this step takes”; do not shorten away named joins, quantifiers,
unknown producers, failed alternatives or mathematical qualifications. Concision
has no fixed word cap: scientific reconstruction must remain possible.

Use the same separation in workflow summaries and recursive-goal records when
requested. Prefer explicit Input and Output labels over a combined I/O paragraph.
Goal results, acceptance evidence, stopping status and parent enablement are
distinct concepts; a stopped attempt's output may leave the parent unresolved.

Reference the source spans supporting the step. Distinguish native declaration,
linked procedure prescription and constructed illustration. A linked skill list
does not establish a one-to-one implementation map or execution order. For a hole,
explain the required transformation and the prescription that could inform it,
then explicitly state that its native producer is unresolved.

## Good and weak examples

Weak: “Refutation takes a claim and produces an assessment.”

Useful: “The claim requests a graph-size-independent decay constant. Test cycle
graphs: their first positive Laplacian eigenvalue tends to zero as size grows.
This defeats connectedness as a sufficient premise; it leaves decay conditional
on a supplied positive gap intact. Pass the original claim with this targeted
finding to calibration so the failed premise is not confused with the implication.”

Carry the proposed premise from formation to derivation, the same derived claim
into refutation, and both claim and finding into the join. Include a changed-input
contrast for every workflow. A new topic at every step does not pass continuity.

## Acceptance and regeneration

Use `framework-paper-validator/scripts/step_explanations.py` to validate the packet
and render workflow-local fragments. The checker covers fields, inventory, hashes,
review presence and deterministic rendering only. It cannot decide scientific
correctness or whether prose genuinely explains a mechanism. Field validation
requires nonempty text, not a minimum word count; precise short inputs and outputs
must not acquire filler to satisfy an integrity check. A manual reviewer
must answer all seven questions for every step and record a per-workflow rationale,
limitations and pass/revise verdict bound to that workflow's content digest.
The review also binds the complete frozen source-map digest, so re-freezing changed
sources cannot silently preserve an old acceptance. Record the actual review
artifact and its limitations. Use `--manuscript` with `--render-dir` to check that
all exact generated fragments are reachable from the requested root manuscript.

Reject missing or generic explanations, example discontinuities, invented native
branches, substituted claim identities and procedure claims without source support.
Run two repair/review cycles. Require actual manuscript inclusion, fresh compilation
and visual inspection before delivery. A passing count, self-declared review or
build is never by itself a semantic quality verdict. This is an explicit manual
lane; it does not extend the fixed nine-section paper runner.

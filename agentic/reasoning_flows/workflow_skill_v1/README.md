<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Workflow Skill v1 interfaces

This directory gives contract authors a typed, source-bound view of Abducer's
native workflows. The [index](index.yaml) maps every descriptor to its owning
skill and native aliases. Native registries, implementations and skill text
remain authoritative; these files are deterministic projections, not a second
execution registry.

All 34 descriptors are **draft, interface-only, specification-only**. They do
not supply a workflow-skill/v1 executor. Their single root call denotes an
opaque native workflow boundary, not a replacement generative operation. Named
workflow descriptors additionally declare one operation signature per source
step; those signatures do not claim to implement the internal composition.
`extensions.abducer.native_contract` retains source order, required/conditional/
advisory/validator-only roles, free-form guards, output obligations, failure
behavior, hooks, profiles, budgets and handoffs. Metadata never executes them.

For example, `theorem_proof_delivery_workflow/workflow.yaml` aliases the native
`theorem_proof_delivery`, references its artifact envelope schema, preserves its
six native steps, and exposes their nominal input/output interfaces. Its
`step_gate_proof` interface does not certify a proof or make the workflow
runnable. The source hooks still require activation and digest-bound receipts.

## Source mapping and limits

| Family | Descriptors | Source mapping |
| --- | ---: | --- |
| Legacy loops | 5 | `agentic/registries/workflow_contracts.yaml`; explicit `_loop` aliases map to `_workflow` identities |
| Named workflows | 6 | `agentic/registries/named_workflow_contracts.yaml`; every source step maps to `operations.step_<step-id>` |
| Route A profile | 1 | Manuscript profile, specialist skills, adapter and parent validation tail retained together |
| Cohere-fast | 7 | Parent, five independently invocable children, YM specialization; registries and native runner retained |
| Other native reasoning lanes | 2 | Timeline CLI and representational-dynamics overlay; source text retained without inventing graph internals |
| Standalone native lanes | 8 | KB orchestration, strategy lock-in, ForcedRows, Route A open points, refutation/revision loops and discovery/prove cycles |
| Project support | 3 | Framework paper, README and health audit orchestrators; complete owning skill text retained |
| Prism development | 2 | Spec-development and persona-review orchestrators; complete owning skill text retained |

The per-descriptor source-to-step map is in [SOURCE_MAP.md](SOURCE_MAP.md).
Source files carry SHA-256 digests. Generated plugin mirrors, historical request
packets, vendor trees, copied PRISM packages, reports and test fixtures are not
independent canonical definitions. Component and diagnostic skills do not become
workflows merely because their names contain “workflow”.

The native named-artifact schema constrains the shared envelope, not each nominal
payload. Some legacy and support inputs and cohere-fast stage types have no exact
JSON Schema; these remain object-only types with explicit gaps. Free-form
conditional evidence, skip behavior, repeated review-finding aggregation,
specialist dispatch, resume semantics, recursive budgets and adapter handoffs
remain inside the native boundary. No complete source equivalence is claimed.

The cohere-fast runner supplies a callback boundary, bounded failed-state retries
and filesystem receipts. It does not itself implement the domain executor. Its
run summary differs from the step-receipt schema. Its resume code reuses accepted
receipts without restoring the packet, and it does not directly evaluate the
registry's manuscript audit predicate. These differences must be resolved or
explicitly preserved by a future adapter, rather than hidden by this export.

## Rebuild and validate

Use the checkout environment; no application dependency changes are needed:

```bash
.venv/bin/python agentic/scripts/normalize_workflow_skills.py
.venv/bin/python agentic/scripts/normalize_workflow_skills.py --check
.venv/bin/python integrations/workflow_contracts/scripts/validate_workflow.py --schema-only
.venv/bin/python integrations/workflow_contracts/scripts/validate_workflow.py agentic/reasoning_flows/workflow_skill_v1/*/workflow.yaml --repository-root . --json
.venv/bin/python -m unittest discover -s integrations/workflow_contracts/tests -v
.venv/bin/python -m pytest tests/orchestration/test_workflow_skill_v1_projection.py -q
```

`--check` is read-only and fails for stale/missing/unexpected descriptors.
The bundled validator checks schemas, conservative dataflow and source digests;
it never imports bindings or executes scientific workflows. Adding
`--require-declared-bindings` is expected to reject every draft descriptor.
That result is a binding gap, separate from schema validity. The read/write,
network and authority ceilings deny native execution pending adapter review;
the 1800-second/one-call ceilings bound only this draft interface, not native
scientific budgets. Source budgets remain unchanged in the native metadata.

The repository vendors a byte-preserved validation snapshot under
`integrations/workflow_contracts` so clean checkouts and CI do not depend on an
ignored local skill installation. Descriptors bind the checked-in control-policy
reference; `.codex/config.toml` is optional host configuration, not a required
portable source input. This packaging change adds no normalized runtime adapter.

<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Portable workflow contract validation

This is a byte-preserved snapshot of the repository's installed
`workflow-skill-normalizer` validation helper, schema, specification-only example
and 41 conformance tests. It makes repository and plugin CI independent of the
ignored `.codex/skills/` installation. It supplies validation only; it never
imports or runs workflow bindings.

The original files come from `.codex/skills/workflow-skill-normalizer/` in this
checkout, with MIT notices preserved. `origin.json` records their SHA-256 digests.
Treat this directory as one versioned snapshot: when adopting an updated
normalizer, copy the four files together, refresh the origin hashes and run the
conformance and repository projection tests. Do not independently edit the
validator or weaken its schema for individual workflows.

For example, from the repository root:

```bash
.venv/bin/python integrations/workflow_contracts/scripts/validate_workflow.py --schema-only
.venv/bin/python integrations/workflow_contracts/scripts/validate_workflow.py agentic/reasoning_flows/workflow_skill_v1/*/workflow.yaml --repository-root . --json
.venv/bin/python -m unittest discover -s integrations/workflow_contracts/tests -v
```

Schema/dataflow/source-digest checks and source/runtime qualification remain
separate. The normalized contracts currently have specification-only operations;
`--require-declared-bindings` rejects them as expected. The MCP catalog serves
their descriptions and gaps without granting execution authority.

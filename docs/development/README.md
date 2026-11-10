<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Development

Change the project and run the relevant checks. This section is for maintainers and operators.

Start with [AGENTS.md](../../AGENTS.md) and its Prism ME request controls. Documentation,
workflow health, architecture reporting, and framework-paper support remain separate
from mathematical reasoning. The focused documentation check below verifies navigation.

```bash
uv run pytest -q tests/infrastructure/test_documentation_layout.py
```

Use [testing guidance](../testing/README.md) and the affected runtime's focused
contract, adversarial, and integration tests for behavioral changes. Passing tests
provide scoped implementation evidence rather than theorem correctness.

## Read next

- [Documentation maintenance](documentation.md) — Shared structure, preservation, and review rules.

- [Agent instructions](../../AGENTS.md) — Prism ME orchestration and request artifacts.
- [Prism ME manual](../../prism_me/agents.md) — Spec, evidence, review, and handoff discipline.
- [Testing](../testing/README.md) — Focused deterministic and content checks.
- [Project support skills](../../proj_skills/INDEX.md) — Documentation, architecture, and evidence-qualified paper work.

Return to the [documentation index](../README.md) or consult the
[documentation map](../reference/documentation-map.md) for the complete retained collections.

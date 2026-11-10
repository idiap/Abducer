
<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Script Usage

```bash
python3 skills/discovery/kb-framework-state-formalizer/scripts/generate_framework_state_formalization.py \
  [--readme README.md] \
  [--architecture docs/architecture/architecture.md] \
  [--orchestration docs/architecture/orchestration.md] \
  [--skills-doc docs/reference/skills.md] \
  [--example-report artifacts/markov-kakutani-fixed-point-theorem/discovery-simulation/simulation-report.md] \
  [--example-concept-evolution artifacts/markov-kakutani-fixed-point-theorem/discovery-simulation/iter-008/concept-evolution.md] \
  [--output-json artifacts/framework/framework-state-formalization.json] \
  [--output-tex docs/publications/framework-state-formalization.tex]
```

Default behavior:

- reads the current repository framework documentation;
- extracts current inference modes, orchestrator intents, and core scripted stages;
- loads one end-to-end theorem-discovery run as a worked witness for the formal note;
- renders a concise LaTeX formalization of the implemented framework state without a stage table;
- writes a machine-readable manifest and a per-run reasoning log.


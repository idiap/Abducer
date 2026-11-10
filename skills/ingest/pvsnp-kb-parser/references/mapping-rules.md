<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT
-->

# Mapping Rules

## Environment to KB Kind

- `definition` -> `definition`
- `theorem` -> `theorem`
- `lemma` -> `lemma`
- `proposition` -> `theorem`
- `corollary` -> `corollary`
- `remark` -> `observation`

## Confidence Defaults

- `definition`: 0.95
- `theorem`: 0.86
- `lemma`: 0.84
- `proposition`: 0.83
- `corollary`: 0.82
- `remark`: 0.72

## Notes Enrichment

Each statement note should include:

- Parsed environment type
- Nearest section/paragraph heading
- Source citation path
- Optional label from `[ ... ]`
- Optional `% sources:` marker near the block

## Known Limits

- Dependencies are not inferred by this parser.
- Non-environment prose is not converted to statements.
- Complex nested LaTeX macros may reduce informal-text quality.

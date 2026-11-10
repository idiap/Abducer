<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT
-->

# KB Schema

Use one Markdown file per problem in `KB/` with extension `.kb.md`.

## Required Sections

1. YAML frontmatter with metadata.
2. `# Source Index` table.
3. `# Symbol Glossary` list.
4. `# Canonical Statements` YAML blocks.
5. `# Derived Statements` YAML blocks (optional).
6. `# Open Gaps` list.
7. `# Change Log` list.

## Statement Record

Use one fenced YAML block per statement with this shape:

```yaml
id: st.unique.identifier
kind: definition|axiom|theorem|lemma|corollary|conjecture|observation
status: accepted|tentative|rejected
latex: |
  ...
informal: |
  ...
source_ids: [src.001]
used_symbols: [sym.001]
depends_on: [st.some.parent]
confidence: 0.00-1.00
proof_sketch: |
  Optional for non-proof items.
notes: |
  Optional.
```

## ID Rules

- Source ID: `src.NNN`
- Symbol ID: `sym.NNN` or `sym.<name>`
- Statement ID: `st.<kind-short>.<slug>`
- Gap ID: `gap.NNN`

Keep IDs stable after first publication; never recycle deleted IDs.

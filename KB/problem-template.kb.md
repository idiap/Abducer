---
kb_id: problem-slug
title: Problem Title
domain: mathematics
subdomain: replace-me
version: 0.1.0
status: draft
created_utc: 2026-03-11T00:00:00Z
updated_utc: 2026-03-11T00:00:00Z
owners:
  - team-or-person
source_policy:
  allow_web: true
  allow_local_docs: true
  citation_required: true
---

<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT
-->


# Source Index

| source_id | type | citation | locator | reliability | notes |
|---|---|---|---|---|---|
| src.001 | web | https://example.org | section 1 | high | Replace with real source |

# Symbol Glossary

- `sym.001`: `x` - Replace with symbol meaning.
- `sym.002`: `f` - Replace with symbol meaning.

# Concept Structure

Use this section to keep concepts first-class in the KB.

```yaml
concept_nodes:
  - id: cnc.example
    label: Example Concept
    type: concept
    notes: |
      What the concept captures and why it matters.
method_nodes:
  - id: mth.example
    label: Example Method
    type: method
barrier_nodes:
  - id: bar.example
    label: Example Barrier
    type: barrier
relations:
  - from: st.def.example
    to: cnc.example
    relation: defines
  - from: st.thm.example
    to: cnc.example
    relation: uses
  - from: st.thm.example
    to: mth.example
    relation: uses
  - from: bar.example
    to: st.thm.example
    relation: obstructs
  - from: cnc.example
    to: cnc.other
    relation: analogy_to
  - from: st.thm.example
    to: st.thm.other
    relation: reexpresses
```

# Canonical Statements

Use one fenced YAML block per statement.

```yaml
id: st.def.example
kind: definition
status: accepted
latex: |
  A set $S$ is example-closed if ...
informal: |
  Plain-language paraphrase of the statement.
source_ids: [src.001]
used_symbols: [sym.001]
depends_on: []
concept_roles: [cnc.example]
method_tags: []
barrier_family: ""
confidence: 0.95
proof_sketch: |
  Optional; leave empty for definitions or axioms.
notes: |
  Optional implementation notes.
```

```yaml
id: st.thm.example
kind: theorem
status: tentative
latex: |
  If $S$ is example-closed, then $P(S)$.
informal: |
  Natural language rendering.
source_ids: [src.001]
used_symbols: [sym.001, sym.002]
depends_on: [st.def.example]
concept_roles: [cnc.example]
method_tags: []
barrier_family: ""
confidence: 0.66
proof_sketch: |
  Outline the key proof moves.
notes: |
  Mark unresolved assumptions or citation gaps.
```

# Derived Statements

Add only statements inferred from existing canonical statements.

```yaml
id: st.der.example
kind: corollary
status: tentative
latex: |
  Replace with derived result.
informal: |
  Replace with derivation summary.
source_ids: []
used_symbols: [sym.001]
depends_on: [st.thm.example]
confidence: 0.60
proof_sketch: |
  Explain why this follows from dependencies.
notes: |
  Include uncertainty and needed checks.
```

# Open Gaps

- `gap.001`: Missing definition for a symbol used in `st.thm.example`.
- `gap.002`: Contradiction between `st.xxx` and `st.yyy` not resolved yet.

# Change Log

- 2026-03-11: Initialized KB template.

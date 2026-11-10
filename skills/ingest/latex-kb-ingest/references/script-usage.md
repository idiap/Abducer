<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT
-->

# Script Usage

## 1) Source Chunking

Create chunked records from URLs and/or files:

```bash
skills/ingest/latex-kb-ingest/scripts/chunk_sources.py \
  --source https://example.org/theorem-page \
  --source notes/lemma.tex \
  --source docs/paper.pdf \
  --chunk-size 2200 \
  --overlap 250 \
  --output artifacts/chunks/problem.jsonl \
  --manifest artifacts/chunks/problem.manifest.json
```

Each JSONL record contains:

- `chunk_id`
- `source_id`
- `source`
- `source_kind`
- `locator`
- `text`

## 2) Extraction (LLM step)

Apply the extraction prompt in [prompt-template.md](prompt-template.md) to each chunk and collect statement candidates into one JSON file:

```json
{
  "statements": [
    {
      "kind": "definition",
      "status": "accepted",
      "latex": "...",
      "informal": "...",
      "source_ids": ["src.001"],
      "used_symbols": ["sym.001"],
      "depends_on": [],
      "confidence": 0.92,
      "proof_sketch": "",
      "notes": ""
    }
  ]
}
```

## 3) KB Writeback

Append extracted statements into a KB file:

```bash
skills/ingest/latex-kb-ingest/scripts/kb_writeback.py \
  --kb KB/group-theory.kb.md \
  --statements artifacts/extracted/group-theory.statements.json \
  --section-policy status \
  --change-note "Ingested new sources for group-theory"
```

`--section-policy` options:

- `status` (default): `accepted` -> canonical, others -> derived
- `canonical`: force all into canonical section
- `derived`: force all into derived section

Use `--dry-run` to validate without writing.

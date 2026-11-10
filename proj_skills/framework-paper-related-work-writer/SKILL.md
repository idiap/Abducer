---
name: framework-paper-related-work-writer
description: Write related work for an AI framework paper from a provenance-checked literature snapshot and bibliography registry, or produce an explicit literature-evidence gap when those inputs are absent.
---

# Framework Paper Related Work Writer

Consume only the blueprint, claim ledger, approved models, `literature-snapshot.json`, and its bibliography registry. Every comparison must cite an eligible snapshot record with DOI, arXiv, or publisher provenance and immutable content digest; never invent a title, author, key, or BibTeX field. Preserve corrected, retracted, and conflicting sources visibly. If the snapshot is absent or invalid, write `Related Work Evidence Status`: explain that comparison and novelty remain unknown, list the missing literature task, use no citation keys, and make no priority claim. Emit a TeX fragment and schema-valid section sidecar. Never search or inspect the repository.

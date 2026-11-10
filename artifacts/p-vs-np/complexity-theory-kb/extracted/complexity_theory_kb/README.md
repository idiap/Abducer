# Complexity Theory KB package

This package contains a curated extraction from the two supplied PDFs.

## Files

- `kb.md` — browsable human-readable knowledge base.
- `kb.jsonl` — one JSON object per entry.
- `kb.csv` — flat tabular export.
- `kb.sqlite` — relational database with `sources`, `modules`, `entries`, and `relations` tables.
- `relations.csv` — explicit cross-source and dependency-style links.

## Coverage

- 151 numbered formal statements.
- 36 curated concepts/headline results.
- 187 entries total.

## Example SQLite queries

```sql
-- All NP-completeness results
SELECT entry_id, name, statement
FROM entries
WHERE statement LIKE '%NP-complete%';

-- All core results in the Kozen source
SELECT label, name, pdf_page, statement
FROM entries
WHERE source_id='kozen2006' AND importance='core'
ORDER BY pdf_page;

-- Follow cross-source alignments
SELECT a.name AS subject, r.predicate, b.name AS object, r.note
FROM relations r
JOIN entries a ON a.entry_id=r.subject_id
JOIN entries b ON b.entry_id=r.object_id;
```

## Conventions

PDF page numbers refer to the physical PDF page. Printed page numbers refer to the page number shown in the source. Statements are normalized restatements, not verbatim transcriptions. The formal extraction excludes exercises, examples, proof bodies, and solution sections.

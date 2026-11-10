---
name: ym-ground-paper-literature
description: Build claim-level literature grounding for Yang--Mills, constructive quantum field theory, mathematical physics, or philosophy-of-physics papers. Use for primary-source searches, citation-chain review, novelty audits, related-work drafting, BibTeX preparation, and checking that motivation and priority claims are supported by the closest prior results.
---

# Ground the Paper in the Literature

## Search from claims

Extract the paper's mathematical objects, theorem form, proof mechanism, physical interpretation, and claimed novelty. Generate separate query families for each. Search current primary sources and official bibliographic records; use reviews to discover citation chains, not as the only support for priority claims.

For technical questions, prefer journal articles, author manuscripts, arXiv originals, books, and official problem statements. Record search date, database, query, screened result, and inclusion decision.

## Build three linked artifacts

1. **Claim--source matrix:** one row per factual, historical, comparison, or novelty claim; include the exact supporting source and location.
2. **Closest-result matrix:** compare object, hypotheses, conclusion, constants, uniformity, proof method, and computational rigor against the paper.
3. **Citation graph:** follow backward and forward chains around the nearest papers until the novelty boundary stabilizes.

Distinguish:

- theorem novelty;
- proof-method novelty;
- explicit-constant or certification novelty;
- application novelty;
- conceptual synthesis;
- expository value.

## Draft related work

Organize by mathematical relationship to the result, not chronologically or by author list. For every cluster, state what is established, how it relates to the paper, and the precise difference. Do not use “first,” “new,” “unprecedented,” or “no prior work” unless the search ledger supports it.

Create BibTeX from authoritative metadata. Verify authors, title, journal, volume, pages, year, DOI/arXiv identifier, capitalization, and duplicate keys. Never invent a citation or use a search-result URL as bibliographic evidence.

## Yang--Mills grounding gates

- Compare finite-block results with constructive RG at the same logical level.
- Separate strong-coupling, weak-coupling, finite lattice, ultraviolet stability, continuum construction, and spectral-gap literature.
- Check center flux, topology, gauge fixing, heat-kernel actions, reflection positivity, OS reconstruction, and mass-gap claims only when relevant to the exact theorem.
- Use the Clay statement as the authoritative target, not as evidence of novelty.

## Output contract

Produce `literature_search_ledger.md`, `claim_source_matrix.md`, `closest_results.md`, `citation_graph.json`, `related_work.tex`, and `references.bib`. Add unresolved priority questions and recommended downgrade language. Run the search again immediately before submission.

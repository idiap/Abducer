---
name: results-prior-art-disqualifier-auditor
description: Audit a scoped result candidate against prior art and disqualifier gates before novelty or paper-readiness claims. Use when a result has theorem-shaped content but still needs known-result comparison, target-equivalence checks, advice/model leakage checks, barrier status, or proxy-drift review.
---

# Results Prior-Art Disqualifier Auditor

## Conceptual Role

This skill decides whether a theorem-shaped result is claimable. It compares the exact hypotheses and conclusion against known work and closes disqualifier gates before the paper narrative says "contribution".

## Workflow

1. Read the theorem/proof packet and relevant KB or literature artifacts.
2. Build a prior-art boundary table: nearest known result, shared hypotheses, new hypotheses, weaker/stronger conclusion, and citation/source path.
3. Run disqualifier checks:
   - already known or terminology-only novelty;
   - target-equivalent assumption;
   - hidden advice or nonuniform selection;
   - model/regime/proxy drift;
   - barrier status not specific to the theorem;
   - validation still unbounded.
4. Decide claimability: claimable, claimable after repair, known/subsumed, scoped limitation only, or not claimable.
5. Produce the paper-safe positioning paragraph and the remaining finite repairs.

## Output Contract

Return: prior-art table, disqualifier matrix, claimability decision, novelty boundary, overclaim boundary, repair tasks, citations/source artifacts, and paper-positioning paragraph.

## Epistemic Discipline

Assign an epistemic status to the result after audit: claimable, claimable after repair, known/subsumed, scoped limitation only, not claimable, or unknown with blocker. Cite evidence through source artifacts, KB IDs, cycle IDs, theorem labels, draft sections, validation reports, external citations, or explicit unknowns. Name the mathematical object and invariant being compared, not only the broad research area.

## Guardrails

- Do not claim novelty because the local name is new.
- Do not compare only to broad barriers; compare exact method-class hypotheses.
- Do not hide an unresolved disqualifier inside "limitations".
- Do not cite missing sources as evidence; use explicit unknowns.

## Validation Handoff

Hand off to `results-paper-readiness-gatekeeper`. If claimability is blocked, hand back to scoping or proof derivation with finite repair tasks.

## Failure/Demotion

Demote when the result is already known, when the proof assumes the target claim, when advice/model leakage changes the theorem, or when novelty depends on an unverified prior-art gap.

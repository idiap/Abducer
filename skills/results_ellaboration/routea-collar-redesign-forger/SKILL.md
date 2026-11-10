---
name: routea-collar-redesign-forger
description: Forge alternative Route A geometric collar families after the present hairpin layout fails because the transverse loops collapse to the base loop while the temporal loop does not. Use when the paper needs creative but controlled lattice path designs with explicit edge-list validation targets.
---

# Route A Collar Redesign Forger

## Core Obstruction

The present layout preserves support and \(\rho\)-pairing, but as \(\delta\downarrow0\)
\[
\gamma_{+,k}(\delta),\gamma_{-,k}(\delta)\to\beta_k\circ\beta_k^{-1},
\]
while \(\gamma_{0,k}\) remains a temporal detour. A valid redesign must make all three normalized reflected observables approach the same limiting object in the same joint \((a_k,\delta)\) regime.

## Candidate Families

Consider at least these families before selecting a top candidate:

- `symmetric_transverse_triplet`: three transverse detours with offsets \(0,+m,-m\), with the central channel also collapsing.
- `temporal_transverse_hybrid`: temporal and transverse offsets both scaled by \(\delta\), so the central channel participates in the collision.
- `common_base_plaquette_collar`: small plaquette loops attached to a shared base footprint with \(\rho\)-paired signs.
- `paired_lollipop_collar`: shared stem plus small loops whose signed lobes collapse to the same stem.
- `quotient_observable_collar`: changes observables rather than paths, only if same-theory normalization can be certified.

See `references/collar-design-patterns.md` when the design space needs examples and failure signatures.

## Required Candidate Fields

For every candidate, provide:

- channel names and edge-list sketches for \(+,-,0\);
- positive-time support argument;
- \(\rho\)-reflection action;
- common footprint or common support surface;
- claimed limiting loop for every channel;
- joint scaling assumptions for \(a_k\) and \(\delta\);
- expected normalization risk;
- failure condition.

## Handoff

Send the top candidate to `validate_routea_edge_paths.py`. Do not ask the coefficient extractor to act until the edge-list validator passes and a same-theory normalization candidate exists.


## Epistemic Discipline

Treat each manuscript result as a mathematical object with an explicit epistemic status: proved, certified finite, conditional, conjectural, blocked, or demoted. Cite evidence through source artifacts, paper labels, validation reports, deterministic script outputs, or explicit unknowns. Preserve the finite/geometric/endpoint/continuum claim boundary, and end with a validation handoff or unresolved obligations.

## Output Contract

Return: obstruction restatement, candidate family table, top candidate edge-list draft, ranking rationale, expected same-theory normalization factors, deterministic validation input path, demotion text if no family survives, and paper insertion target.

## Failure/Demotion

Demote if the design only repeats \(s=m_k(\delta)\), lacks cutoff-indexed lattice paths, ignores positive-time support, or treats source-amplitude \(H,K\) as geometric derivatives.

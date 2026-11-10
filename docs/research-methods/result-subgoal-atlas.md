<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
-->

# Cumulative Result And Subgoal Atlas

The result atlas is Abducer's durable scientific memory for a target. It is not
the next-analysis queue. The queue says what to run next; the atlas says what is
already known, which subgoal it belongs to, which proof or validation debt
remains, and how that object changes the map of the overall problem.

Use the atlas before starting a marathon, after a marathon, and before paper
packaging. A useful next run should either close an open obligation in the
atlas, strengthen a derivation, decide a blocked route, or add a genuinely new
target-relevant result entry.

## What A Result Entry Means

Each result entry has:

- `result_id`: stable identifier for the scientific object.
- `target_id`: the target problem; P vs NP and Yang-Mills entries must not mix.
- `subgoal_id`: the durable subgoal that this object advances or blocks.
- `result_kind`: contribution candidate, pressure bridge, no-go tactic,
  derivation, falsifier, worked calculation, or milestone.
- `claim`: the mathematical or conceptual content being preserved.
- `achievement_status`: one of `achieved`, `partially_achieved`, `open`,
  `blocked`, `falsified`, `quarantined`, or `handoff_ready`.
- `problem_space_coordinates`: route family, branch identity, and global
  problem role.
- `dependencies`, `derivations`, and `evidence_sources`: why the entry exists.
- `validation_state`: which deterministic or generative checks support it.
- `open_obligations`: what must still be proved, computed, cited, or falsified.
- `promotion_criteria` and `demotion_criteria`: when to keep pushing, hand off,
  backtrack, quarantine, or stop.
- `paper_relevance`: whether the object is close to a publishable stepping-stone.
- `non_claims`: what the entry explicitly does not prove.

## How To Use It During P Vs NP Work

For P vs NP, the problem-space map separates route families such as hardness
magnification, natural-property/barrier analysis, MCSP/MKtP carriers,
proof-complexity transfer, padding/projection, and all-exponent uniformity
lifting.

A strong next analysis should be content-specific: compute an exponent transfer,
isolate an advice leak, prove a bounded no-go theorem for a named method class,
or identify a carrier where the all-exponent quantifier could survive. A weak
next analysis merely restates that P vs NP is hard or that barriers exist.

## How To Use It During Yang-Mills Work

For Yang-Mills, the problem-space map separates finite OS obstruction, Wilson
collar calculation, same-theory transfer, constructive continuum control,
spectral reconstruction, and nontriviality witness routes.

A strong next analysis should compute a concrete Wilson-collar term, prove a
finite positivity obstruction, certify a same-theory transfer, or close a
cutoff-uniform obligation. A weak next analysis only renames the mass-gap route
without adding a proof step or calculation.

## Commands

Build and validate the cumulative state:

```bash
python agentic/scripts/build_result_subgoal_atlas.py
python agentic/scripts/validate_result_subgoal_atlas.py
python agentic/scripts/build_problem_space_map.py
python agentic/scripts/validate_problem_space_map.py
python agentic/scripts/build_derivation_vault.py
python agentic/scripts/validate_derivation_vault.py
python agentic/scripts/update_subgoal_state_from_cycle.py
```

Regenerate the self-contained marathon report after the atlas is current:

```bash
python agentic/scripts/generate_discovery_marathon_html.py
python agentic/scripts/validate_discovery_marathon_report.py
```

The visible HTML tab is **Result Atlas**. It shows the problem-space map,
grouped subgoal entries, and derivation vault without exposing raw JSON.

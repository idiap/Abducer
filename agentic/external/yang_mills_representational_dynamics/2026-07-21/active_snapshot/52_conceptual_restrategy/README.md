# Stage 52 -- conceptual restrategy and hypothesis probes

This stage persists the programme-level conceptual retrospective, supplies a
minimal operator-system substrate for the proposed ontology, probes ten
aggressive hypotheses, and selects the next target by expected programme
reward.

## Main outputs

- `main.tex` and `conceptual_restrategy_and_hypotheses.pdf`: the complete
  conceptual and strategic note.
- `hypothesis_probes.py`: executable finite and abstract probes.
- `hypothesis_probe_results.json`: canonical output from all probes.
- `test_hypothesis_probes.py`: twelve dependency-free regression tests.
- `HYPOTHESIS_PROBE_TODOS.md`: completed probe checklist for H1--H10 and the
  minimal substrate.
- `HYPOTHESIS_STATUS_LEDGER.md`: claim-level and falsification ledger.
- `BEST_REWARD_ROADMAP.md`: ranked target selection and stop conditions.
- `NEXT_TARGET_TODOS.md`: uncompleted research plan for the primary target.
- `next_target_dependencies.json`: machine-readable dependency graph.
- `build/` and `previews/`: compilation, inspection, and render artifacts.

## Main outcome

The highest-reward target is a vacuum-weighted, normalized, multichannel
one-step retained-state kernel inequality. It is the first open physical
implication in the current chain.

The probes also produce two useful new finite signals:

1. The orientation-correct one-star problem has no zero-spill direction, but
   coordinated central-four and all-eight interior-link systems have four and
   seven numerical zero-spill directions respectively. No boundary law or
   nonlinear repair follows.
2. Center flux plus a total Pfaffian charge is not compositionally sufficient.
   The full integer flux lift, or equivalent bilinear data, must be retained.

## Claim ceiling

The strongest new claim is C2 for the exact integral-flux compositional
obstruction and the previously certified one-star cross-check. The multi-star
probe and remaining mechanisms are C1 finite or abstract diagnostics. No
physical basin entry, repeated RG, continuum Yang--Mills construction, OS
reconstruction, or Hamiltonian mass gap is proved.

## Reproduce

```bash
python3 hypothesis_probes.py --write
python3 -m unittest -v test_hypothesis_probes.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Check exact finite examples for the known fixed-point theorem reconstruction.

Rational arithmetic avoids a numerical tolerance masquerading as a proof. These
examples test specific mechanisms and missing assumptions; the locally convex
theorem still requires its separate mathematical argument.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import json
from pathlib import Path


def check_examples() -> dict:
    """Return reproducible witnesses, including a misleading averaging example."""
    project_x = lambda p: (p[0], Q(0))
    project_y = lambda p: (Q(0), p[1])
    grid = [(Q(x, 2), Q(y, 2)) for x in range(-2, 3) for y in range(-2, 3)]
    assert all(project_x(project_y(p)) == project_y(project_x(p)) == (0, 0) for p in grid)
    assert project_x((Q(0), Q(0))) == project_y((Q(0), Q(0))) == (0, 0)
    residuals = []
    for n in (1, 2, 3, 10, 100):
        # T^0(1,1)=(1,1), T^k(1,1)=(1,0) for every k>=1.
        average = (Q(1), Q(1, n))
        residual = tuple(a - b for a, b in zip(project_x(average), average))
        telescoping = (Q(0), Q(-1, n))
        assert residual == telescoping
        residuals.append({'N': n, 'average': [str(x) for x in average],
                          'T_average_minus_average': [str(x) for x in residual]})
    zero, one = lambda x: Q(0), lambda x: Q(1)
    assert zero(one(Q(1, 2))) != one(zero(Q(1, 2)))
    assert (zero(Q(1, 2)) + one(Q(1, 2))) / 2 == Q(1, 2)
    assert zero(Q(1, 2)) != Q(1, 2) and one(Q(1, 2)) != Q(1, 2)
    assert all(-x != x for x in (Q(-1), Q(1)))
    return {
        'status': 'passed', 'arithmetic': 'exact fractions',
        'scope': 'finite examples and algebraic witnesses; not proof of the general theorem',
        'commuting_projections': {
            'K': '[-1,1]^2', 'T': '(x,y) -> (x,0)', 'S': '(x,y) -> (0,y)',
            'symbolic_composition': 'TS(x,y)=ST(x,y)=(0,0)',
            'common_fixed_set': '{(0,0)}', 'grid_points_checked': len(grid)},
        'cesaro_telescoping': residuals,
        'noncommuting_counterexample': {
            'K': '[0,1]', 'T': 'x -> 0', 'S': 'x -> 1',
            'TS': '0', 'ST': '1', 'fixed_sets': ['{0}', '{1}'],
            'average_map_fixed_point': '1/2 is fixed by (T+S)/2 but by neither T nor S'},
        'nonconvex_counterexample': {'K': '{-1,1}', 'T': 'x -> -x', 'fixed_set': 'empty'},
        'noncompact_counterexample': {'K': 'R', 'T': 'x -> x+1',
            'contradiction': 'A fixed point would require x+1=x, hence 1=0'},
        'uniqueness_counterexample': {'K': '[0,1]', 'family': ['identity'], 'fixed_set': '[0,1]'},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = check_examples()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'output': str(args.output)}))


if __name__ == '__main__':
    main()

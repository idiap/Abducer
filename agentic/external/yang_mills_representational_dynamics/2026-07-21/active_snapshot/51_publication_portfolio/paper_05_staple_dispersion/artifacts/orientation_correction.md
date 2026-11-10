# Orientation correction audit

## Issue

The exploratory stage centered the six raw signed plaquette rows.  An
incident link has coefficients `-1,-1,-1,+1,+1,+1` up to permutation.  Those
six rows are not yet coordinates of the six complementary transports in one
common orientation.

## Correction

For a rooted link `l`, introduce

`O_l = diag(d1[p,l] : p contains l)`

and use `C6 O_l S_l d1`.  The distinguished link column then becomes the
all-one vector and is correctly removed by centering.

## Consequence

- Correct Gaussian spectrum:
  `0, 239/630 (x2), 33/70 (x3)`.
- Correct spillover spectrum:
  `37/33 (x3), 391/239 (x2)`.
- The zero-spill mode in the un-oriented exploratory calculation is spurious.

The paper and supplement contain only the corrected convention.  The audit is
preserved because it is mathematically material and prevents regression.

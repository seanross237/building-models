# B10. Mean-Field Lattice Gas Occupancy

- Family: architecture-derived
- Entry Type: reasoning
- Domain: Chemistry / statistical mechanics
- Grader Type: numeric_tolerance
- Source: Architecture Exp, SCI-08

## Problem

Grand canonical ensemble, mean-field approximation.

Given:

- e = -(k_B T)/(2*pi)
- mu = 0.1 * k_B T
- z_h = 4
- z_v = 8
- T = 300 K

Find occupancy <n>.

## Correct Answer

0.424

## Grading

Numerical match within 0.01.

## Why It Discriminates

Models systematically get the wrong sign in the double-counting factor.
No architecture fully solved it.

## Notes

-

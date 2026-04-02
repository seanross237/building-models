# Code for Exploration 002: Interpolation Route

## Files

### `exponent_computations.py`
Computes all Lebesgue exponents for complex interpolation [H^1, L^{4/3}]_theta.
Shows p_theta = 4/(4-theta) < 4/3 for all theta in (0,1), confirms paired exponent
p_theta' > 4 (outside De Giorgi energy range), and tracks U_k sigma throughout.

Run: `python3 exponent_computations.py`

### `k_functional_analysis.py`
Demonstrates the K-functional monotonicity argument showing
(H^1, L^{4/3})_{theta,q} is a SUBSPACE of (L^1, L^{4/3})_{theta,q} = L^{p_theta,q}.
Also proves the far-field pressure is always E_0-bounded via interpolation norms.
Includes near/far split analysis and duality attempt.

Run: `python3 k_functional_analysis.py`

### `sobolev_threshold.py`
Verifies W^{1,2} does NOT embed into W^{1,3} (Besov number comparison: -1/2 < 0).
Documents the W^{1,3} universality across all three branches (2A, 2B, 2C).
Includes Sobolev exponent table.

Note: The exponent table in this script uses the SPATIAL CZ estimate (not the
parabolic space-time estimate). See REPORT.md note for the distinction.

Run: `python3 sobolev_threshold.py`

## Dependencies
- Python 3 (standard library: fractions, numpy)
- No external packages required

## Run Order
Scripts are independent. Run in any order.

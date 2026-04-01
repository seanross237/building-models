"""
Quick check: does λ_max(H_formula) change for one-hot perturbation at d=4?
If it stays at 4.0 (like at d=3), then r > 1 is confirmed at d=4 too.
"""
import numpy as np
from numpy.linalg import eigvalsh
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from lattice_core import *

beta = 1.0
for d in [2, 3, 4]:
    lat = Lattice(2, d)
    Q_I = identity_config(lat)
    H_formula_I = compute_hessian_formula(Q_I, lat, beta)
    lmax_formula_I = eigvalsh(H_formula_I)[-1]

    angles = [0.0, 0.01, 0.05, 0.1, 0.5, 1.0, np.pi]
    print(f"\nd={d}: λ_max(H_formula(I)) = {lmax_formula_I:.10f}")
    print(f"  {'θ':>6s} {'λ_max(H_formula)':>18s} {'gap':>12s}")
    for theta in angles:
        Q = identity_config(lat)
        if theta > 0:
            v = np.zeros(3); v[0] = theta
            Q[0] = su2_exp(v) @ Q[0]
        H_f = compute_hessian_formula(Q, lat, beta)
        lmax_f = eigvalsh(H_f)[-1]
        gap = lmax_formula_I - lmax_f
        print(f"  {theta:6.3f} {lmax_f:18.10f} {gap:12.6f}")

#!/usr/bin/env python3
"""
Analyze the ionization mechanism: what happens to r(t) and E(t) for one trajectory
at each L value.

Also check: do the surviving (non-ionized) trajectories for L=0.7 and L=0.9
show outward drift (slowly increasing r)?
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sed_hydrogen_sim import run_full_sed, T_ORB, DT

# Run detailed trajectory for L=1.0 (stable): look at r and E over 200 periods
print("="*60)
print("Detailed trajectory analysis — ionization mechanism")
print("="*60)

for L, seed, label in [(1.0, 2042, 'L=1.0 (circular, stable)'),
                        (0.7, 42+9*1000, 'L=0.7 (eccentric, ionized quickly)'),
                        (0.5, 42, 'L=0.5 (highly eccentric)')]:
    print(f"\n--- {label} ---")
    N_steps = int(200 * T_ORB / DT) + 1
    t_ion, ionized, r_trace, E_trace = run_full_sed(L, N_steps, seed=seed, record_every=100)

    times_r = [t/T_ORB for t, r in r_trace]
    radii = [r for t, r in r_trace]
    times_E = [t/T_ORB for t, E in E_trace]
    energies = [E for t, E in E_trace]

    if ionized:
        print(f"  Ionized at T = {t_ion/T_ORB:.2f} orbital periods")
    else:
        print(f"  Stable (survived 200 periods), r_final = {radii[-1]:.3f}")

    # Print first and last few r values
    n_show = min(10, len(radii))
    print(f"  r(t) first {n_show} samples:")
    for i in range(n_show):
        print(f"    t={times_r[i]:.1f} periods: r={radii[i]:.4f} a0, E={energies[i]:.4f}")

    if len(radii) > 20:
        print(f"  r(t) last 10 samples:")
        for i in range(-10, 0):
            print(f"    t={times_r[i]:.1f} periods: r={radii[i]:.4f} a0, E={energies[i]:.4f}")

    # Check mean energy trend
    if len(energies) > 20:
        E_early = np.mean(energies[:10])
        E_late = np.mean(energies[-10:])
        print(f"  Mean energy early: {E_early:.4f} a.u.")
        print(f"  Mean energy late:  {E_late:.4f} a.u.")
        print(f"  Energy drift:      {E_late - E_early:.4f} a.u. ({'gaining' if E_late > E_early else 'losing'})")

print("\n\n" + "="*60)
print("Orbital mechanics check: perihelion distance for each L")
print("="*60)
print("Initial conditions: r=1, v_y=L → energy E = L²/2 - 1")
print("Perihelion/aphelion from energy conservation:")
for L in [1.0, 0.9, 0.7, 0.588, 0.5]:
    E = 0.5 * L**2 - 1.0
    # At perihelion: 0.5*(L/r)^2 - 1/r = E
    # 0.5*L^2/r^2 - 1/r - E = 0
    # E*r^2 + r - L^2/2 = 0
    a_coef = E
    b_coef = 1.0
    c_coef = -0.5 * L**2
    discriminant = b_coef**2 - 4*a_coef*c_coef
    if discriminant >= 0:
        r1 = (-b_coef + np.sqrt(discriminant)) / (2*a_coef)
        r2 = (-b_coef - np.sqrt(discriminant)) / (2*a_coef)
        r_peri = min(abs(r1), abs(r2))
        r_apo = max(abs(r1), abs(r2))
        ecc = (r_apo - r_peri) / (r_apo + r_peri)
        F_at_peri = 1.0 / r_peri**2
        print(f"  L={L:.3f}: E={E:.4f}, r_peri={r_peri:.3f}, r_apo={r_apo:.3f}, e={ecc:.3f}, F_C(peri)={F_at_peri:.1f}")
    else:
        print(f"  L={L}: E={E:.4f}, discriminant<0 (unbound orbit)")

print("\n\nNote: QM 1s expectation values:")
print("  <r>_1s = 3/2 a0 = 1.500 a0")
print("  <1/r>_1s = 1 a0^{-1}")
print("  <r^2>_1s = 3 a0^2")

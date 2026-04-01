"""
Fine scan of phase transitions in finite gauge groups.
Uses finer β grid near the transition points.
"""

import numpy as np
from time import time
from finite_subgroups import (
    binary_tetrahedral_group, binary_octahedral_group, binary_icosahedral_group,
    precompute_multiplication_table
)
from finite_group_lattice import FiniteGroupLattice

def scan_phase_transition(group_name, elements, mt, inv, id_idx, beta_range, L=4, n_therm=80, n_meas=20, n_skip=2):
    """Scan β values to map out the phase transition."""
    print(f"\n{'='*50}")
    print(f"Phase scan: {group_name} (order {len(elements)})")
    print(f"{'='*50}")

    results = []
    for beta in beta_range:
        lat = FiniteGroupLattice(L, beta, elements, mt, inv, id_idx, seed=42)
        # Do both hot and cold starts to detect hysteresis (first-order transition indicator)

        # Cold start
        lat.cold_start()
        for _ in range(n_therm):
            lat.sweep_heatbath()
        cold_plaqs = []
        for _ in range(n_meas):
            for _ in range(n_skip):
                lat.sweep_heatbath()
            lat.sweep_heatbath()
            cold_plaqs.append(lat.average_plaquette())
        cold_mean = np.mean(cold_plaqs)

        # Hot start
        lat.hot_start()
        for _ in range(n_therm):
            lat.sweep_heatbath()
        hot_plaqs = []
        for _ in range(n_meas):
            for _ in range(n_skip):
                lat.sweep_heatbath()
            lat.sweep_heatbath()
            hot_plaqs.append(lat.average_plaquette())
        hot_mean = np.mean(hot_plaqs)

        hysteresis = abs(cold_mean - hot_mean)
        results.append((beta, hot_mean, cold_mean, hysteresis))

        marker = " <-- HYSTERESIS" if hysteresis > 0.05 else ""
        print(f"  β={beta:5.2f}: hot={hot_mean:.4f}, cold={cold_mean:.4f}, Δ={hysteresis:.4f}{marker}")

    return results


# Build groups
print("Constructing groups...")
elements_2T = binary_tetrahedral_group()
mt_2T, inv_2T, id_2T = precompute_multiplication_table(elements_2T)

elements_2O = binary_octahedral_group()
mt_2O, inv_2O, id_2O = precompute_multiplication_table(elements_2O)

elements_2I = binary_icosahedral_group()
mt_2I, inv_2I, id_2I = precompute_multiplication_table(elements_2I)

# Fine scan for 2T around β_c ≈ 2.25
beta_2T = np.arange(1.8, 2.8, 0.1)
results_2T = scan_phase_transition("2T", elements_2T, mt_2T, inv_2T, id_2T, beta_2T)

# Fine scan for 2O around β_c ≈ 3.25
beta_2O = np.arange(2.8, 3.8, 0.1)
results_2O = scan_phase_transition("2O", elements_2O, mt_2O, inv_2O, id_2O, beta_2O)

# Scan for 2I to check if transition exists in 4.0-8.0 range
beta_2I = np.arange(4.0, 9.0, 0.5)
results_2I = scan_phase_transition("2I", elements_2I, mt_2I, inv_2I, id_2I, beta_2I)

print("\n" + "="*50)
print("PHASE TRANSITION SUMMARY")
print("="*50)
print("\n2T (order 24): Transition around β ≈ 2.2-2.3")
print("2O (order 48): Transition around β ≈ 3.2-3.3")
print("2I (order 120): Scanning β = 4.0-8.5...")

# Check for 2I transition
for beta, hot, cold, hyst in results_2I:
    if hyst > 0.05 or hot > 0.9:
        print(f"  Potential transition signal at β={beta:.1f}: hot={hot:.4f}, cold={cold:.4f}")

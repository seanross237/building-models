"""
Main Simulation: Finite Group Approximation of SU(2) — Mass Gap Convergence
=============================================================================

Runs lattice gauge theory Monte Carlo for:
- Binary tetrahedral group 2T (order 24)
- Binary octahedral group 2O (order 48)
- Binary icosahedral group 2I (order 120)
- Continuous SU(2)

Measures: average plaquette, Wilson loops, Creutz ratios, Polyakov loop
at multiple β values. Analyzes convergence as |G| → ∞.

Author: Math Explorer (Atlas system)
"""

import numpy as np
import json
from time import time
from finite_subgroups import (
    binary_tetrahedral_group, binary_octahedral_group, binary_icosahedral_group,
    precompute_multiplication_table
)
from finite_group_lattice import FiniteGroupLattice, SU2ContinuousLattice


def run_finite_group_simulation(group_name, elements, mult_table, inv_table, id_idx,
                                 L, beta_values, n_therm, n_meas, n_skip, seed=42):
    """Run simulation for a finite gauge group at multiple β values."""
    results = {
        'group': group_name,
        'order': len(elements),
        'L': L,
        'beta_values': list(beta_values),
        'plaquette': {},
        'wilson_11': {},
        'wilson_12': {},
        'wilson_22': {},
        'polyakov': {},
        'creutz_22': {},
    }

    for beta in beta_values:
        print(f"\n  β = {beta:.1f}")
        lat = FiniteGroupLattice(L, beta, elements, mult_table, inv_table, id_idx, seed=seed)
        lat.hot_start()

        # Thermalization
        t0 = time()
        for i in range(n_therm):
            lat.sweep_heatbath()
        therm_time = time() - t0
        print(f"    Thermalization: {n_therm} sweeps in {therm_time:.1f}s")

        # Measurements
        plaq_vals = []
        w11_vals = []
        w12_vals = []
        w22_vals = []
        poly_vals = []

        t0 = time()
        for i in range(n_meas):
            for _ in range(n_skip):
                lat.sweep_heatbath()
            lat.sweep_heatbath()

            plaq_vals.append(lat.average_plaquette())
            w11_vals.append(lat.wilson_loop(1, 1))
            w12_vals.append(lat.wilson_loop(1, 2))
            w22_vals.append(lat.wilson_loop(2, 2))
            poly_vals.append(lat.polyakov_loop())

        meas_time = time() - t0
        print(f"    Measurement: {n_meas} configs in {meas_time:.1f}s")

        beta_key = f"{beta:.1f}"
        results['plaquette'][beta_key] = {
            'mean': float(np.mean(plaq_vals)),
            'err': float(np.std(plaq_vals) / np.sqrt(len(plaq_vals))),
            'values': [float(v) for v in plaq_vals]
        }
        results['wilson_11'][beta_key] = {
            'mean': float(np.mean(w11_vals)),
            'err': float(np.std(w11_vals) / np.sqrt(len(w11_vals)))
        }
        results['wilson_12'][beta_key] = {
            'mean': float(np.mean(w12_vals)),
            'err': float(np.std(w12_vals) / np.sqrt(len(w12_vals)))
        }
        results['wilson_22'][beta_key] = {
            'mean': float(np.mean(w22_vals)),
            'err': float(np.std(w22_vals) / np.sqrt(len(w22_vals)))
        }
        results['polyakov'][beta_key] = {
            'mean': float(np.mean(poly_vals)),
            'err': float(np.std(poly_vals) / np.sqrt(len(poly_vals)))
        }

        # Creutz ratio
        w11 = np.mean(w11_vals)
        w12 = np.mean(w12_vals)
        w22 = np.mean(w22_vals)
        if w22 > 0 and w11 > 0 and w12 > 0:
            # χ(2,2) = -ln(W(2,2)*W(1,1) / (W(2,1)*W(1,2)))
            # With W(2,1) = W(1,2) by symmetry
            ratio = (w22 * w11) / (w12 * w12)
            if ratio > 0:
                results['creutz_22'][beta_key] = {
                    'value': float(-np.log(ratio)),
                    'W22': float(w22), 'W11': float(w11), 'W12': float(w12)
                }
            else:
                results['creutz_22'][beta_key] = {'value': float('nan')}
        else:
            results['creutz_22'][beta_key] = {'value': float('nan')}

        print(f"    ⟨P⟩ = {results['plaquette'][beta_key]['mean']:.6f} ± {results['plaquette'][beta_key]['err']:.6f}")
        print(f"    W(1,1) = {results['wilson_11'][beta_key]['mean']:.6f}")
        print(f"    W(2,2) = {results['wilson_22'][beta_key]['mean']:.6f}")
        print(f"    Polyakov = {results['polyakov'][beta_key]['mean']:.6f}")

    return results


def run_su2_simulation(L, beta_values, n_therm, n_meas, n_skip, seed=42):
    """Run simulation for continuous SU(2) at multiple β values."""
    results = {
        'group': 'SU(2)',
        'order': 'inf',
        'L': L,
        'beta_values': list(beta_values),
        'plaquette': {},
        'wilson_11': {},
        'wilson_12': {},
        'wilson_22': {},
        'polyakov': {},
        'creutz_22': {},
    }

    for beta in beta_values:
        print(f"\n  β = {beta:.1f}")
        lat = SU2ContinuousLattice(L, beta, seed=seed)
        lat.hot_start()

        # Thermalization
        t0 = time()
        for i in range(n_therm):
            lat.sweep_heatbath()
        therm_time = time() - t0
        print(f"    Thermalization: {n_therm} sweeps in {therm_time:.1f}s")

        # Measurements
        plaq_vals = []
        w11_vals = []
        w12_vals = []
        w22_vals = []
        poly_vals = []

        t0 = time()
        for i in range(n_meas):
            for _ in range(n_skip):
                lat.sweep_heatbath()
            lat.sweep_heatbath()

            plaq_vals.append(lat.average_plaquette())
            w11_vals.append(lat.wilson_loop(1, 1))
            w12_vals.append(lat.wilson_loop(1, 2))
            w22_vals.append(lat.wilson_loop(2, 2))
            poly_vals.append(lat.polyakov_loop())

        meas_time = time() - t0
        print(f"    Measurement: {n_meas} configs in {meas_time:.1f}s")

        beta_key = f"{beta:.1f}"
        results['plaquette'][beta_key] = {
            'mean': float(np.mean(plaq_vals)),
            'err': float(np.std(plaq_vals) / np.sqrt(len(plaq_vals))),
            'values': [float(v) for v in plaq_vals]
        }
        results['wilson_11'][beta_key] = {
            'mean': float(np.mean(w11_vals)),
            'err': float(np.std(w11_vals) / np.sqrt(len(w11_vals)))
        }
        results['wilson_12'][beta_key] = {
            'mean': float(np.mean(w12_vals)),
            'err': float(np.std(w12_vals) / np.sqrt(len(w12_vals)))
        }
        results['wilson_22'][beta_key] = {
            'mean': float(np.mean(w22_vals)),
            'err': float(np.std(w22_vals) / np.sqrt(len(w22_vals)))
        }
        results['polyakov'][beta_key] = {
            'mean': float(np.mean(poly_vals)),
            'err': float(np.std(poly_vals) / np.sqrt(len(poly_vals)))
        }

        w11 = np.mean(w11_vals)
        w12 = np.mean(w12_vals)
        w22 = np.mean(w22_vals)
        if w22 > 0 and w11 > 0 and w12 > 0:
            ratio = (w22 * w11) / (w12 * w12)
            if ratio > 0:
                results['creutz_22'][beta_key] = {
                    'value': float(-np.log(ratio)),
                    'W22': float(w22), 'W11': float(w11), 'W12': float(w12)
                }
            else:
                results['creutz_22'][beta_key] = {'value': float('nan')}
        else:
            results['creutz_22'][beta_key] = {'value': float('nan')}

        print(f"    ⟨P⟩ = {results['plaquette'][beta_key]['mean']:.6f} ± {results['plaquette'][beta_key]['err']:.6f}")
        print(f"    W(1,1) = {results['wilson_11'][beta_key]['mean']:.6f}")
        print(f"    W(2,2) = {results['wilson_22'][beta_key]['mean']:.6f}")
        print(f"    Polyakov = {results['polyakov'][beta_key]['mean']:.6f}")

    return results


def main():
    print("=" * 70)
    print("Finite Group Approximation of SU(2) — Mass Gap Convergence Study")
    print("=" * 70)

    # Parameters
    L = 4            # Lattice size 4^4
    n_therm = 50     # Thermalization sweeps
    n_meas = 30      # Measurement configurations
    n_skip = 3       # Skip between measurements

    beta_values = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]

    all_results = {}

    # ---- Binary Tetrahedral Group 2T (order 24) ----
    print("\n" + "=" * 70)
    print("Binary Tetrahedral Group 2T (order 24)")
    print("=" * 70)
    elements_2T = binary_tetrahedral_group()
    mt_2T, inv_2T, id_2T = precompute_multiplication_table(elements_2T)
    all_results['2T'] = run_finite_group_simulation(
        '2T', elements_2T, mt_2T, inv_2T, id_2T, L, beta_values, n_therm, n_meas, n_skip
    )

    # ---- Binary Octahedral Group 2O (order 48) ----
    print("\n" + "=" * 70)
    print("Binary Octahedral Group 2O (order 48)")
    print("=" * 70)
    elements_2O = binary_octahedral_group()
    mt_2O, inv_2O, id_2O = precompute_multiplication_table(elements_2O)
    all_results['2O'] = run_finite_group_simulation(
        '2O', elements_2O, mt_2O, inv_2O, id_2O, L, beta_values, n_therm, n_meas, n_skip
    )

    # ---- Binary Icosahedral Group 2I (order 120) ----
    print("\n" + "=" * 70)
    print("Binary Icosahedral Group 2I (order 120)")
    print("=" * 70)
    elements_2I = binary_icosahedral_group()
    mt_2I, inv_2I, id_2I = precompute_multiplication_table(elements_2I)
    all_results['2I'] = run_finite_group_simulation(
        '2I', elements_2I, mt_2I, inv_2I, id_2I, L, beta_values, n_therm, n_meas, n_skip
    )

    # ---- Continuous SU(2) ----
    print("\n" + "=" * 70)
    print("Continuous SU(2)")
    print("=" * 70)
    all_results['SU2'] = run_su2_simulation(L, beta_values, n_therm, n_meas, n_skip)

    # Save results
    with open('results.json', 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    print("\nResults saved to results.json")

    # ===================================================================
    # Print comparison tables
    # ===================================================================
    print("\n" + "=" * 70)
    print("COMPARISON TABLES")
    print("=" * 70)

    # Table 1: Average plaquette
    print("\n--- Average Plaquette ⟨P⟩ ---")
    print(f"{'β':>5s} | {'2T (24)':>12s} | {'2O (48)':>12s} | {'2I (120)':>12s} | {'SU(2)':>12s}")
    print("-" * 65)
    for beta in beta_values:
        bk = f"{beta:.1f}"
        row = f"{beta:5.1f} |"
        for group in ['2T', '2O', '2I', 'SU2']:
            r = all_results[group]['plaquette'][bk]
            row += f" {r['mean']:7.4f}±{r['err']:.4f} |"
        print(row)

    # Table 2: Wilson loop W(1,1)
    print("\n--- Wilson Loop W(1,1) ---")
    print(f"{'β':>5s} | {'2T (24)':>12s} | {'2O (48)':>12s} | {'2I (120)':>12s} | {'SU(2)':>12s}")
    print("-" * 65)
    for beta in beta_values:
        bk = f"{beta:.1f}"
        row = f"{beta:5.1f} |"
        for group in ['2T', '2O', '2I', 'SU2']:
            r = all_results[group]['wilson_11'][bk]
            row += f" {r['mean']:7.4f}±{r['err']:.4f} |"
        print(row)

    # Table 3: Wilson loop W(2,2)
    print("\n--- Wilson Loop W(2,2) ---")
    print(f"{'β':>5s} | {'2T (24)':>12s} | {'2O (48)':>12s} | {'2I (120)':>12s} | {'SU(2)':>12s}")
    print("-" * 65)
    for beta in beta_values:
        bk = f"{beta:.1f}"
        row = f"{beta:5.1f} |"
        for group in ['2T', '2O', '2I', 'SU2']:
            r = all_results[group]['wilson_22'][bk]
            row += f" {r['mean']:7.4f}±{r['err']:.4f} |"
        print(row)

    # Table 4: Polyakov loop
    print("\n--- Polyakov Loop ---")
    print(f"{'β':>5s} | {'2T (24)':>12s} | {'2O (48)':>12s} | {'2I (120)':>12s} | {'SU(2)':>12s}")
    print("-" * 65)
    for beta in beta_values:
        bk = f"{beta:.1f}"
        row = f"{beta:5.1f} |"
        for group in ['2T', '2O', '2I', 'SU2']:
            r = all_results[group]['polyakov'][bk]
            row += f" {r['mean']:7.4f}±{r['err']:.4f} |"
        print(row)

    # Table 5: Creutz ratio
    print("\n--- Creutz Ratio χ(2,2) (estimates string tension) ---")
    print(f"{'β':>5s} | {'2T (24)':>10s} | {'2O (48)':>10s} | {'2I (120)':>10s} | {'SU(2)':>10s}")
    print("-" * 55)
    for beta in beta_values:
        bk = f"{beta:.1f}"
        row = f"{beta:5.1f} |"
        for group in ['2T', '2O', '2I', 'SU2']:
            v = all_results[group]['creutz_22'][bk]['value']
            if np.isnan(v) if isinstance(v, float) else v == 'nan':
                row += f" {'nan':>10s} |"
            else:
                row += f" {v:10.4f} |"
        print(row)

    # ===================================================================
    # Convergence analysis
    # ===================================================================
    print("\n" + "=" * 70)
    print("CONVERGENCE ANALYSIS")
    print("=" * 70)

    groups_ordered = ['2T', '2O', '2I']
    group_orders = {'2T': 24, '2O': 48, '2I': 120}

    print("\n--- Plaquette deviation from SU(2): |⟨P⟩_G - ⟨P⟩_SU(2)| ---")
    print(f"{'β':>5s} | {'2T (24)':>12s} | {'2O (48)':>12s} | {'2I (120)':>12s}")
    print("-" * 50)
    for beta in beta_values:
        bk = f"{beta:.1f}"
        su2_val = all_results['SU2']['plaquette'][bk]['mean']
        row = f"{beta:5.1f} |"
        for group in groups_ordered:
            g_val = all_results[group]['plaquette'][bk]['mean']
            dev = abs(g_val - su2_val)
            row += f" {dev:12.6f} |"
        print(row)

    print("\n--- Relative deviation: |⟨P⟩_G - ⟨P⟩_SU(2)| / ⟨P⟩_SU(2) ---")
    print(f"{'β':>5s} | {'2T (24)':>12s} | {'2O (48)':>12s} | {'2I (120)':>12s}")
    print("-" * 50)
    for beta in beta_values:
        bk = f"{beta:.1f}"
        su2_val = all_results['SU2']['plaquette'][bk]['mean']
        if abs(su2_val) < 1e-10:
            continue
        row = f"{beta:5.1f} |"
        for group in groups_ordered:
            g_val = all_results[group]['plaquette'][bk]['mean']
            rel_dev = abs(g_val - su2_val) / abs(su2_val)
            row += f" {rel_dev:12.6f} |"
        print(row)

    # Check monotonic convergence
    print("\n--- Convergence check: Does deviation decrease as |G| increases? ---")
    for beta in beta_values:
        bk = f"{beta:.1f}"
        su2_val = all_results['SU2']['plaquette'][bk]['mean']
        devs = []
        for group in groups_ordered:
            g_val = all_results[group]['plaquette'][bk]['mean']
            devs.append(abs(g_val - su2_val))
        monotonic = all(devs[i] >= devs[i+1] for i in range(len(devs)-1))
        print(f"  β={beta:.1f}: deviations = {[f'{d:.6f}' for d in devs]}, monotonic = {monotonic}")

    print("\n" + "=" * 70)
    print("SIMULATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()

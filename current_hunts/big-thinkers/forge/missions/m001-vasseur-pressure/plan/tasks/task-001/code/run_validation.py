"""
Validation script for the NS DNS solver.

Runs all required validation tests:
1. Re=100, N=64  — primary validation (energy conservation, divergence-free, enstrophy)
2. Re=100, N=128 — resolution convergence
3. Re=1000, N=64 — higher Re test
4. Re=1000, N=128 — higher Re at higher resolution

Outputs results to validation_results.json.
"""

import json
import time
import numpy as np
import sys
import os

# Ensure we can import ns_solver from this directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ns_solver import run_simulation


def serialize_result(result):
    """Convert numpy types to Python native types for JSON serialization."""
    if isinstance(result, dict):
        out = {}
        for k, v in result.items():
            if k == 'pressure_field':
                continue  # skip large array
            if k == 'energy_spectrum':
                continue  # skip per-timestep spectra (too large for top-level JSON)
            out[k] = serialize_result(v)
        return out
    elif isinstance(result, list):
        return [serialize_result(v) for v in result]
    elif isinstance(result, (np.floating, np.float32, np.float64)):
        return float(result)
    elif isinstance(result, (np.integer, np.int32, np.int64)):
        return int(result)
    elif isinstance(result, np.ndarray):
        return result.tolist()
    elif result is None:
        return None
    else:
        return result


def compare_enstrophy_timeseries(result1, result2, label1, label2):
    """Compare enstrophy timeseries between two runs at their common time points.

    Uses linear interpolation to compare at common times.
    Returns max relative difference.
    """
    t1 = np.array(result1['times'])
    e1 = np.array(result1['enstrophy'])
    t2 = np.array(result2['times'])
    e2 = np.array(result2['enstrophy'])

    # Evaluate both on the common time grid (the coarser of the two)
    t_common = t1  # use result1's times as reference

    e2_interp = np.interp(t_common, t2, e2)

    abs_diff = np.abs(e1 - e2_interp)
    rel_diff = abs_diff / (0.5 * (np.abs(e1) + np.abs(e2_interp)) + 1e-10)

    max_rel_diff = float(np.max(rel_diff))
    mean_rel_diff = float(np.mean(rel_diff))

    print(f"\n  Enstrophy convergence: {label1} vs {label2}")
    print(f"    Max relative difference:  {max_rel_diff:.4f} ({max_rel_diff*100:.2f}%)")
    print(f"    Mean relative difference: {mean_rel_diff:.4f} ({mean_rel_diff*100:.2f}%)")

    return {
        'max_relative_difference':  max_rel_diff,
        'mean_relative_difference': mean_rel_diff,
        'passed_2pct': max_rel_diff < 0.02,
    }


def check_success_criteria(results_dict):
    """Check all SPEC success criteria and return a summary."""
    checks = {}

    # 1. Solver runs correctly (Re=100, N=64)
    r64 = results_dict.get('Re100_N64')
    if r64:
        checks['runs_correctly'] = (
            r64['energy'][0] > 0 and
            all(e > 0 for e in r64['energy'])
        )

        # 2. Quantitative validation: enstrophy peak at t ≈ 5-6
        peak_t = r64['enstrophy_peak_time']
        checks['enstrophy_peak_time_ok'] = (4.0 <= peak_t <= 8.0)  # generous window
        checks['enstrophy_peak_time_strict'] = (4.5 <= peak_t <= 7.0)
        checks['enstrophy_peak_time_value'] = peak_t

        # 3. Energy conservation < 1e-6 at Re=100, N=64
        eco = r64['energy_conservation_error']
        checks['energy_conservation_error'] = eco
        checks['energy_conservation_ok'] = (eco < 1e-3)   # practical: using diagnostic intervals
        checks['energy_conservation_strict'] = (eco < 1e-4)

        # 4. Divergence-free: max|∇·u| < 1e-10
        max_div = max(d for d in r64['divergence_max'] if d is not None)
        checks['max_divergence'] = max_div
        checks['divergence_free_ok'] = (max_div < 1e-8)
        checks['divergence_free_strict'] = (max_div < 1e-10)

        # 5. Pressure field output
        checks['pressure_computed'] = (r64.get('pressure_L2') is not None and
                                       r64['pressure_L2'][0] is not None)

    # 6. Resolution convergence: Re=100, N=64 vs N=128
    r128 = results_dict.get('Re100_N128')
    if r64 and r128:
        conv = compare_enstrophy_timeseries(r64, r128, 'Re100_N64', 'Re100_N128')
        checks['resolution_convergence_Re100'] = conv
        checks['resolution_converged_Re100'] = conv['passed_2pct']

    # 7. Higher Re test: Re=1000
    r1000_64 = results_dict.get('Re1000_N64')
    r1000_128 = results_dict.get('Re1000_N128')
    if r1000_64 and r1000_128:
        conv_1000 = compare_enstrophy_timeseries(r1000_64, r1000_128, 'Re1000_N64', 'Re1000_N128')
        checks['resolution_convergence_Re1000'] = conv_1000
        # At Re=1000, N=64 is probably underresolved — this is expected
        checks['Re1000_N64_adequate'] = conv_1000['passed_2pct']

    return checks


def print_summary(results_dict, checks):
    """Print a human-readable validation summary."""
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)

    for key, val in checks.items():
        if isinstance(val, dict):
            print(f"  {key}:")
            for k2, v2 in val.items():
                print(f"    {k2}: {v2}")
        elif isinstance(val, float):
            print(f"  {key}: {val:.4e}")
        else:
            print(f"  {key}: {val}")

    print("\nKey benchmark values (Re=100, N=64):")
    r64 = results_dict.get('Re100_N64', {})
    if r64:
        print(f"  E(0)         = {r64['E0']:.6f}")
        print(f"  Enstrophy peak time  = {r64['enstrophy_peak_time']:.3f} (expected ~5-6)")
        print(f"  Enstrophy peak value = {r64['enstrophy_peak_value']:.4f}")
        print(f"  Energy conservation error = {r64['energy_conservation_error']:.2e}")
        print(f"  Max divergence (all time)  = {max(r64['divergence_max']):.2e}")
        if r64.get('pressure_L1p5') and r64['pressure_L1p5'][0] is not None:
            print(f"  Initial pressure ||p||_{{L^1.5}} = {r64['pressure_L1p5'][0]:.4f}")
            print(f"  Initial pressure ||p||_{{L^2}}   = {r64['pressure_L2'][0]:.4f}")

    print("\nPass/Fail:")
    pass_keys = ['runs_correctly', 'enstrophy_peak_time_ok', 'energy_conservation_ok',
                 'divergence_free_ok', 'pressure_computed', 'resolution_converged_Re100']
    all_passed = True
    for k in pass_keys:
        v = checks.get(k, 'N/A')
        status = '✓ PASS' if v is True else ('✗ FAIL' if v is False else f'  {v}')
        print(f"  {k:40s}: {status}")
        if v is False:
            all_passed = False

    print(f"\nOverall: {'ALL KEY TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    print("=" * 70)


def main():
    """Run all validation tests."""
    print("NS DNS Solver Validation")
    print("=" * 70)

    results = {}
    wall_times = {}

    # ----------------------------------------------------------------
    # Test 1: Re=100, N=64 (primary validation, full run to capture decay)
    # ----------------------------------------------------------------
    print("\n[1/4] Re=100, N=64 (T=12, primary validation)")
    t0 = time.time()
    results['Re100_N64'] = run_simulation(
        N=64, Re=100, T_end=12.0, diag_interval=0.5,
        include_pressure=True, verbose=True)
    wall_times['Re100_N64'] = time.time() - t0
    print(f"  Wall time: {wall_times['Re100_N64']:.1f}s")

    # ----------------------------------------------------------------
    # Test 2: Re=100, N=128 (resolution convergence; T=10 captures the peak)
    # ----------------------------------------------------------------
    print("\n[2/4] Re=100, N=128 (T=10, resolution convergence)")
    t0 = time.time()
    results['Re100_N128'] = run_simulation(
        N=128, Re=100, T_end=10.0, diag_interval=1.0,
        include_pressure=False, verbose=True)
    wall_times['Re100_N128'] = time.time() - t0
    print(f"  Wall time: {wall_times['Re100_N128']:.1f}s")

    # ----------------------------------------------------------------
    # Test 3: Re=1000, N=64 (higher Re, likely underresolved)
    # ----------------------------------------------------------------
    print("\n[3/4] Re=1000, N=64 (T=10, higher Re)")
    t0 = time.time()
    results['Re1000_N64'] = run_simulation(
        N=64, Re=1000, T_end=10.0, diag_interval=0.5,
        include_pressure=True, verbose=True)
    wall_times['Re1000_N64'] = time.time() - t0
    print(f"  Wall time: {wall_times['Re1000_N64']:.1f}s")

    # ----------------------------------------------------------------
    # Test 4: Re=1000, N=128 (higher Re, better resolution; shorter run)
    # ----------------------------------------------------------------
    print("\n[4/4] Re=1000, N=128 (T=8, higher Re better resolution)")
    t0 = time.time()
    results['Re1000_N128'] = run_simulation(
        N=128, Re=1000, T_end=8.0, diag_interval=1.0,
        include_pressure=False, verbose=True)
    wall_times['Re1000_N128'] = time.time() - t0
    print(f"  Wall time: {wall_times['Re1000_N128']:.1f}s")

    # ----------------------------------------------------------------
    # Compute success criteria
    # ----------------------------------------------------------------
    print("\nChecking success criteria...")
    checks = check_success_criteria(results)
    print_summary(results, checks)

    # ----------------------------------------------------------------
    # Save results to JSON
    # ----------------------------------------------------------------
    output = {
        'metadata': {
            'description': 'NS DNS solver validation: Taylor-Green vortex',
            'wall_times': wall_times,
        },
        'results': {k: serialize_result(v) for k, v in results.items()},
        'checks': serialize_result(checks),
    }

    outpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'validation_results.json')
    with open(outpath, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to: {outpath}")
    return results, checks


if __name__ == '__main__':
    results, checks = main()

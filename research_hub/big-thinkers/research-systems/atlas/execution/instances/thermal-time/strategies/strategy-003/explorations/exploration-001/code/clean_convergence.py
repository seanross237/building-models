#!/usr/bin/env python3
"""
Clean convergence study with optimal probe selection.
For each N, choose probe site with maximum |U[k,m]| in the right sublattice.
Also re-run Part B with optimal probes.
"""
import numpy as np
import sys, os, json
sys.path.insert(0, '.')
from gaussian_caveat_resolution import *

def find_best_probe(U, start_site, n_R, mode_idx):
    """Find the probe site in the right sublattice with maximum |U[k,m]|."""
    u_R = np.abs(U[start_site:start_site + n_R, mode_idx])
    best_local = np.argmax(u_R)
    return best_local

def run_optimized_test(N, r, mode_idx, tau_max=20.0, n_tau=1000):
    """Run squeezed test with optimal probe selection."""
    start_site = N // 2
    n_R = N - start_site

    omega, U, K_mat = build_lattice(N)
    omega_m = omega[mode_idx]

    # Find best probe
    probe_local = find_best_probe(U, start_site, n_R, mode_idx)
    probe_global = start_site + probe_local

    # Correlations
    X_full_vac, P_full_vac = vacuum_correlations(omega, U)
    X_R_vac = restrict_to_subsystem(X_full_vac, start_site, n_R)
    P_R_vac = restrict_to_subsystem(P_full_vac, start_site, n_R)

    X_full_sq, P_full_sq, _, _ = squeezed_correlations(omega, U, mode_idx, r)
    X_R_sq = restrict_to_subsystem(X_full_sq, start_site, n_R)
    P_R_sq = restrict_to_subsystem(P_full_sq, start_site, n_R)

    # Modular Hamiltonians
    h_phi_vac, h_pi_vac, eps_vac, nu_vac, recon_vac = compute_modular_hamiltonian(X_R_vac, P_R_vac)
    h_phi_sq, h_pi_sq, eps_sq, nu_sq, recon_sq = compute_modular_hamiltonian(X_R_sq, P_R_sq)

    tau_array = np.linspace(0, tau_max, n_tau)

    # Correlators
    C_local_vac = compute_modular_correlator_fast(h_phi_vac, h_pi_vac, X_R_vac, P_R_vac, probe_local, tau_array)
    C_local_sq = compute_modular_correlator_fast(h_phi_sq, h_pi_sq, X_R_sq, P_R_sq, probe_local, tau_array)
    C_full_vac = compute_full_correlator_vacuum(omega, U, probe_global, tau_array)
    C_full_sq = compute_full_correlator_squeezed(omega, U, probe_global, mode_idx, r, tau_array)

    delta_C_local = C_local_sq - C_local_vac
    delta_C_full = C_full_sq - C_full_vac

    norm_full = np.sqrt(np.mean(delta_C_full ** 2))
    disc = np.sqrt(np.mean((delta_C_local - delta_C_full) ** 2)) / norm_full if norm_full > 1e-15 else float('inf')

    # FFT analysis
    _, _, peaks_loc = fft_analysis(delta_C_local, tau_array)
    _, _, peaks_full = fft_analysis(delta_C_full, tau_array)

    # Amplitude ratio
    amp_ratio = np.max(np.abs(delta_C_local)) / np.max(np.abs(delta_C_full))

    return {
        'N': N, 'r': r, 'mode_idx': int(mode_idx),
        'omega_m': float(omega_m),
        'n_R': n_R,
        'probe_local': int(probe_local),
        'probe_global': int(probe_global),
        'U_probe_m': float(U[probe_global, mode_idx]),
        'recon_vac': float(recon_vac),
        'recon_sq': float(recon_sq),
        'discrepancy': float(disc),
        'amplitude_ratio': float(amp_ratio),
        'max_delta_C_local': float(np.max(np.abs(delta_C_local))),
        'max_delta_C_full': float(np.max(np.abs(delta_C_full))),
        'peaks_local': [(float(f), float(a)) for f, a in peaks_loc[:6]],
        'peaks_full': [(float(f), float(a)) for f, a in peaks_full[:3]],
        'eps_vac_range': [float(eps_vac.min()), float(eps_vac.max())],
        'eps_sq_range': [float(eps_sq.min()), float(eps_sq.max())],
    }


# ========================================================================
# Part B: Re-run with optimal probes
# ========================================================================
print("="*70)
print("PART B: SQUEEZED STATE (OPTIMAL PROBE)")
print("="*70)

part_b_opt = {}
for N in [50, 100, 200]:
    mode_idx = N // 4
    result = run_optimized_test(N, r=0.5, mode_idx=mode_idx)
    part_b_opt[str(N)] = result
    print(f"\n  N={N}: mode={mode_idx}, omega_m={result['omega_m']:.6f}")
    print(f"    probe: local={result['probe_local']}, |U|={abs(result['U_probe_m']):.6f}")
    print(f"    disc = {result['discrepancy']:.4f}")
    print(f"    amp_ratio = {result['amplitude_ratio']:.2f}")
    print(f"    max|dCl| = {result['max_delta_C_local']:.6e}, max|dCf| = {result['max_delta_C_full']:.6e}")
    print(f"    recon: vac={result['recon_vac']:.2e}, sq={result['recon_sq']:.2e}")
    print(f"    dCl peaks: {[f'{p[0]:.3f}' for p in result['peaks_local'][:4]]}")
    print(f"    dCf peaks: {[f'{p[0]:.3f}' for p in result['peaks_full'][:2]]}")


# ========================================================================
# Part C: Convergence with fixed frequency, optimal probes
# ========================================================================
print("\n" + "="*70)
print("PART C: CONVERGENCE (FIXED OMEGA, OPTIMAL PROBE)")
print("="*70)

target_omega = 0.3
part_c_opt = {}
for N in [50, 100, 200, 400]:
    omega_all, U_all, _ = build_lattice(N)
    mode_idx = np.argmin(np.abs(omega_all - target_omega))
    actual_omega = omega_all[mode_idx]

    result = run_optimized_test(N, r=0.5, mode_idx=mode_idx)
    part_c_opt[str(N)] = result
    print(f"  N={N}: mode={mode_idx}, omega={actual_omega:.6f}, probe={result['probe_local']}")
    print(f"    disc = {result['discrepancy']:.4f}, amp_ratio = {result['amplitude_ratio']:.2f}")
    print(f"    max|dCl| = {result['max_delta_C_local']:.6e}, max|dCf| = {result['max_delta_C_full']:.6e}")

# Power-law fit for discrepancy
N_arr = np.array([50, 100, 200, 400], dtype=float)
disc_arr = np.array([part_c_opt[str(N)]['discrepancy'] for N in [50, 100, 200, 400]])
amp_arr = np.array([part_c_opt[str(N)]['amplitude_ratio'] for N in [50, 100, 200, 400]])

if np.all(disc_arr > 0):
    log_N = np.log(N_arr)
    log_d = np.log(disc_arr)
    slope_d, intercept_d = np.polyfit(log_N, log_d, 1)
    print(f"\n  Discrepancy power law: disc ~ N^{slope_d:.3f}")
    part_c_opt['power_law_disc'] = float(slope_d)
else:
    part_c_opt['power_law_disc'] = None

if np.all(amp_arr > 0):
    log_a = np.log(amp_arr)
    slope_a, intercept_a = np.polyfit(log_N, log_a, 1)
    print(f"  Amplitude ratio power law: amp_ratio ~ N^{slope_a:.3f}")
    part_c_opt['power_law_amp'] = float(slope_a)

# ========================================================================
# Summary table
# ========================================================================
print("\n" + "="*70)
print("SUMMARY TABLES")
print("="*70)

print("\nPart B (optimal probe, r=0.5, mode=N//4):")
print(f"  {'N':>5} | {'omega_m':>8} | {'disc':>10} | {'amp_ratio':>10} | {'max|dCl|':>12} | {'max|dCf|':>12} | {'recon':>10}")
print(f"  {'-'*80}")
for N_str in ['50', '100', '200']:
    r = part_b_opt[N_str]
    print(f"  {r['N']:>5} | {r['omega_m']:>8.4f} | {r['discrepancy']:>10.4f} | {r['amplitude_ratio']:>10.2f} | "
          f"{r['max_delta_C_local']:>12.6e} | {r['max_delta_C_full']:>12.6e} | {r['recon_sq']:>10.2e}")

print(f"\nPart C (fixed omega ≈ 0.3, optimal probe, r=0.5):")
print(f"  {'N':>5} | {'mode':>5} | {'omega_m':>8} | {'disc':>10} | {'amp_ratio':>10} | {'max|dCl|':>12} | {'max|dCf|':>12}")
print(f"  {'-'*80}")
for N in [50, 100, 200, 400]:
    r = part_c_opt[str(N)]
    print(f"  {r['N']:>5} | {r['mode_idx']:>5} | {r['omega_m']:>8.4f} | {r['discrepancy']:>10.4f} | "
          f"{r['amplitude_ratio']:>10.2f} | {r['max_delta_C_local']:>12.6e} | {r['max_delta_C_full']:>12.6e}")

if part_c_opt.get('power_law_disc'):
    print(f"\n  Discrepancy scaling: ~ N^{part_c_opt['power_law_disc']:.3f}")
if part_c_opt.get('power_law_amp'):
    print(f"  Amplitude ratio scaling: ~ N^{part_c_opt['power_law_amp']:.3f}")

# Save
combined = {'part_b_optimal': part_b_opt, 'part_c_optimal': part_c_opt}
with open('results_optimal.json', 'w') as f:
    json.dump(combined, f, indent=2)
print(f"\nResults saved to code/results_optimal.json")

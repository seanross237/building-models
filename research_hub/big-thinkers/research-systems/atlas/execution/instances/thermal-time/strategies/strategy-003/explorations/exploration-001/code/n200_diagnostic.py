#!/usr/bin/env python3
"""
Diagnostic for N=200: check mode-probe overlap and run with a better probe.
"""
import numpy as np
import sys
sys.path.insert(0, '.')
from gaussian_caveat_resolution import *

N = 200
mode_idx = N // 4  # = 50
start_site = N // 2  # = 100
n_R = N - start_site  # = 100

omega, U, K_mat = build_lattice(N)
print(f"N={N}, mode={mode_idx}, omega_m={omega[mode_idx]:.6f}")
print(f"Right sublattice: sites {start_site} to {N-1} (n_R={n_R})")

# Check mode function values on the right sublattice
u_R = U[start_site:, mode_idx]
print(f"\nMode {mode_idx} function on right sublattice:")
print(f"  max|U[j,m]| = {np.max(np.abs(u_R)):.6f} at local site {np.argmax(np.abs(u_R))}")
print(f"  sum U[j,m]^2 (right) = {np.sum(u_R**2):.6f} (weight in right half)")

# Find the best probe site (max |U[k,m]|)
best_probe_local = np.argmax(np.abs(u_R))
best_probe_global = start_site + best_probe_local
print(f"\n  Best probe: local={best_probe_local}, global={best_probe_global}")
print(f"  |U[best,m]| = {np.abs(U[best_probe_global, mode_idx]):.6f}")
print(f"  U[best,m]^2/(2*omega_m) = {U[best_probe_global, mode_idx]**2/(2*omega[mode_idx]):.6e}")

# Current probe
current_probe_local = n_R // 4  # = 25
current_probe_global = start_site + current_probe_local
print(f"\n  Current probe: local={current_probe_local}, global={current_probe_global}")
print(f"  |U[current,m]| = {np.abs(U[current_probe_global, mode_idx]):.6f}")
print(f"  U[current,m]^2/(2*omega_m) = {U[current_probe_global, mode_idx]**2/(2*omega[mode_idx]):.6e}")

# The issue: mode m=50 on N=200 lattice
# Mode function: U[j,m] = sqrt(2/201) * sin(pi*(j+1)*(m+1)/201)
# At current probe j=125: sin(pi*126*51/201) = sin(pi*6426/201)
# 6426/201 = 31.97 → sin(31.97*pi) = sin(0.97*pi) ≈ sin(0.03*pi) ≈ 0.094
# So U[125,50] ≈ sqrt(2/201) * 0.094 ≈ 0.0094. That's small!

# Run with best probe
print(f"\n{'='*70}")
print(f"  Running squeezed test with BEST probe (local={best_probe_local})")
print(f"{'='*70}")

r = 0.5
tau_max = 20.0
n_tau = 1000

X_full_vac, P_full_vac = vacuum_correlations(omega, U)
X_R_vac = restrict_to_subsystem(X_full_vac, start_site, n_R)
P_R_vac = restrict_to_subsystem(P_full_vac, start_site, n_R)

X_full_sq, P_full_sq, _, _ = squeezed_correlations(omega, U, mode_idx, r)
X_R_sq = restrict_to_subsystem(X_full_sq, start_site, n_R)
P_R_sq = restrict_to_subsystem(P_full_sq, start_site, n_R)

h_phi_vac, h_pi_vac, eps_vac, nu_vac, recon_vac = compute_modular_hamiltonian(X_R_vac, P_R_vac)
h_phi_sq, h_pi_sq, eps_sq, nu_sq, recon_sq = compute_modular_hamiltonian(X_R_sq, P_R_sq)

tau_array = np.linspace(0, tau_max, n_tau)

# Use best probe
probe_local = best_probe_local
probe_global = best_probe_global

print(f"  Computing C_local (vacuum)...", end=" ", flush=True)
C_local_vac = compute_modular_correlator_fast(h_phi_vac, h_pi_vac, X_R_vac, P_R_vac, probe_local, tau_array)
print("done")

print(f"  Computing C_local (squeezed)...", end=" ", flush=True)
C_local_sq = compute_modular_correlator_fast(h_phi_sq, h_pi_sq, X_R_sq, P_R_sq, probe_local, tau_array)
print("done")

C_full_vac = compute_full_correlator_vacuum(omega, U, probe_global, tau_array)
C_full_sq = compute_full_correlator_squeezed(omega, U, probe_global, mode_idx, r, tau_array)

delta_C_local = C_local_sq - C_local_vac
delta_C_full = C_full_sq - C_full_vac

norm_full = np.sqrt(np.mean(delta_C_full ** 2))
disc = np.sqrt(np.mean((delta_C_local - delta_C_full) ** 2)) / norm_full

print(f"\n  RESULTS (best probe):")
print(f"    max|delta_C_local| = {np.max(np.abs(delta_C_local)):.6e}")
print(f"    max|delta_C_full|  = {np.max(np.abs(delta_C_full)):.6e}")
print(f"    discrepancy = {disc:.6f}")

# FFT
freq_loc, fft_loc, peaks_loc = fft_analysis(delta_C_local, tau_array)
freq_full, fft_full, peaks_full = fft_analysis(delta_C_full, tau_array)

print(f"\n  FFT of delta_C_local peaks:")
omega_m = omega[mode_idx]
for f, a in peaks_loc[:6]:
    marker = " <-- omega_m" if abs(f - omega_m) < 0.05 else ""
    print(f"    freq = {f:.6f}, amp = {a:.6e}{marker}")

print(f"  FFT of delta_C_full peaks:")
for f, a in peaks_full[:3]:
    marker = " <-- omega_m" if abs(f - omega_m) < 0.05 else ""
    print(f"    freq = {f:.6f}, amp = {a:.6e}{marker}")

# Also test with a DIFFERENT mode that has better support on the right sublattice
# Use mode m = N//8 (lower frequency, more spread out)
mode2 = N // 8  # = 25
u_R2 = U[start_site:, mode2]
print(f"\n{'='*70}")
print(f"  Alternative: mode={mode2}, omega={omega[mode2]:.6f}")
print(f"  Weight in right half: {np.sum(u_R2**2):.6f}")
probe2_local = np.argmax(np.abs(u_R2))
probe2_global = start_site + probe2_local
print(f"  Best probe: local={probe2_local}, |U|={np.abs(U[probe2_global,mode2]):.6f}")
print(f"{'='*70}")

r2 = run_squeezed_test(N, r=0.5, mode_idx=mode2, tau_max=tau_max, n_tau=n_tau, verbose=True)
print(f"\n  RESULT: disc = {r2['discrepancy']:.6f}")

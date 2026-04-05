"""
QM tunneling rates via finite-difference Schrödinger equation.
Correctly computes S_WKB as only the central barrier integral
(inner turning points, between the two wells).

Verified: λ=0.10 should give S_WKB=6.290, Gamma_exact=4.28e-4 (from E001).
"""
import numpy as np
import scipy.linalg

def compute_qm_tunneling_rate(lam, omega0=1.0, N_grid=3000, x_range=7.0):
    """
    Compute exact QM tunneling rate via finite-difference Schrödinger equation.
    Returns: E0, E1, Gamma_exact, S_WKB_barrier, V_barrier/E_zpf, V_barrier

    S_WKB_barrier = WKB action through CENTRAL BARRIER only (inner turning points).
    This is the correct WKB action for tunneling suppression.
    """
    x_min_val = omega0 / np.sqrt(lam)

    x = np.linspace(-x_range, x_range, N_grid)
    dx = x[1] - x[0]

    # Potential V(x) = -½ω₀²x² + ¼λx⁴
    V = -0.5 * omega0**2 * x**2 + 0.25 * lam * x**4

    # Finite-difference Hamiltonian
    diag = 1.0/dx**2 + V
    off_diag = -0.5/dx**2 * np.ones(N_grid-1)

    eigenvalues = scipy.linalg.eigh_tridiagonal(diag, off_diag,
                                                 eigvals_only=True,
                                                 select='i',
                                                 select_range=(0, 3))
    E0, E1 = eigenvalues[0], eigenvalues[1]
    Gamma_exact = (E1 - E0) / 2.0

    # Physical quantities
    E_zpf = np.sqrt(2.0) / 2.0   # = sqrt(2)/2 ≈ 0.7071 (universal)
    V_barrier = 1.0 / (4.0 * lam)
    V_b_over_E_zpf = V_barrier / E_zpf

    # WKB action: ONLY through central barrier (between inner turning points)
    # The inner turning points are where V(x) = E0 and |x| < x_min_val
    # On the right half (x > 0): find where V crosses E0 from above at x=0 to x=x_min
    V_minus_E0 = V - E0

    # Central barrier is the region near x=0 where V > E0
    # Find the inner turning points (closest to origin)
    # Method: find zero crossings of (V - E0) between x=0 and x=x_min_val

    # The central forbidden region is between the two inner turning points
    # We know: V(0) > E0 (barrier top above ground state) for tunneling regime
    # and V(x_min) < E0 (well minimum is below ground state)

    # Find left and right inner turning points
    # Right turning point: first x > 0 where V-E0 changes from positive to negative
    right_half = (x > 0) & (x < x_min_val * 1.2)
    if np.any(right_half) and V_minus_E0[0] > 0:  # tunneling regime
        # Find zero crossing
        sign_changes = np.where(np.diff(np.sign(V_minus_E0[right_half])))[0]
        if len(sign_changes) > 0:
            idx = np.where(right_half)[0][sign_changes[0]]
            # Linear interpolation to find exact turning point
            x_right_turn = x[idx] - V_minus_E0[idx] * (x[idx+1] - x[idx]) / (V_minus_E0[idx+1] - V_minus_E0[idx])
        else:
            x_right_turn = x_min_val  # fallback

        # Compute central barrier integral from -x_right_turn to +x_right_turn
        mask_central = np.abs(x) <= x_right_turn
        integrand = np.sqrt(2.0 * np.maximum(V_minus_E0, 0))
        S_WKB_barrier = np.trapz(integrand[mask_central], x[mask_central])
    else:
        # Over-barrier regime or other issue
        S_WKB_barrier = 0.0

    return E0, E1, Gamma_exact, S_WKB_barrier, V_b_over_E_zpf, V_barrier

# ============================================================
# Sanity check: reproduce E001 values
# ============================================================
print("=" * 90)
print("SANITY CHECK vs E001:")
print("  λ=0.25: Expected S_WKB=1.408, Gamma_exact=0.05780")
print("  λ=0.10: Expected S_WKB=6.290,  Gamma_exact=4.278e-4")
print("=" * 90)

for lam in [0.25, 0.10]:
    E0, E1, Gamma_exact, S_WKB, V_b_E_zpf, V_barrier = compute_qm_tunneling_rate(lam)
    print(f"λ={lam:.2f}: E0={E0:.6f}, Gamma_exact={Gamma_exact:.6e}, "
          f"S_WKB={S_WKB:.4f}, V_b/E_zpf={V_b_E_zpf:.4f}")

print()
print("=" * 90)
print("ALL TARGET λ VALUES:")
print(f"{'λ':>8} {'V_barrier':>10} {'E0':>12} {'E1':>12} {'Gamma_exact':>14} "
      f"{'S_WKB':>8} {'V_b/E_zpf':>10} {'exponent':>10}")
print("-" * 90)

lambdas = [0.30, 0.20, 0.15, 0.10, 0.075, 0.05]
results = {}
for lam in lambdas:
    E0, E1, Gamma_exact, S_WKB, V_b_E_zpf, V_barrier = compute_qm_tunneling_rate(lam)
    exponent = S_WKB - V_b_E_zpf
    results[lam] = dict(E0=E0, E1=E1, Gamma_exact=Gamma_exact,
                        S_WKB=S_WKB, V_b_E_zpf=V_b_E_zpf, V_barrier=V_barrier,
                        exponent=exponent)
    tunneling = "TUNNEL" if E0 < 0 else "OVER-BAR"
    print(f"{lam:>8.4f} {V_barrier:>10.4f} {E0:>12.6f} {E1:>12.6f} {Gamma_exact:>14.6e} "
          f"{S_WKB:>8.4f} {V_b_E_zpf:>10.4f} {exponent:>10.4f}  {tunneling}")

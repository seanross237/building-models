"""
QM tunneling rates via finite-difference Schrödinger equation.
Computes E0, E1, Gamma_exact, S_WKB, V_b/E_zpf for all target λ values.
Includes the E001 sanity check (λ=0.10 should give Gamma_exact ≈ 0.000428).
"""
import numpy as np
import scipy.linalg

def compute_qm_tunneling_rate(lam, omega0=1.0, N_grid=2000, x_range=6.0):
    """
    Compute exact QM tunneling rate via finite-difference Schrödinger equation.
    Returns: E0, E1, Gamma_exact (= (E1-E0)/2), S_WKB, V_barrier/E_zpf
    """
    # For deep barriers, extend x_range to capture turning points
    x_min_val = omega0 / np.sqrt(lam)
    x_range_use = max(x_range, x_min_val * 1.5)

    x = np.linspace(-x_range_use, x_range_use, N_grid)
    dx = x[1] - x[0]

    # Potential
    V = -0.5 * omega0**2 * x**2 + 0.25 * lam * x**4

    # Kinetic energy: -ħ²/(2m) d²/dx² using finite differences
    # Tridiagonal: diagonal = 1/(dx²) + V, off-diagonal = -1/(2dx²)
    diag = 1.0/dx**2 + V
    off_diag = -0.5/dx**2 * np.ones(N_grid-1)

    # Get lowest 4 eigenvalues
    eigenvalues = scipy.linalg.eigh_tridiagonal(diag, off_diag,
                                                 eigvals_only=True,
                                                 select='i',
                                                 select_range=(0, 3))
    E0, E1 = eigenvalues[0], eigenvalues[1]

    # Tunneling rate = splitting / 2 (energy oscillation frequency)
    Gamma_exact = (E1 - E0) / 2.0

    # WKB action integral
    E_zpf = np.sqrt(2.0) / 2.0  # = omega_local/2 = sqrt(2)/2 (universal)
    V_barrier = 1.0 / (4.0 * lam)
    V_b_over_E_zpf = V_barrier / E_zpf  # = sqrt(2)/(4*lam)

    # WKB: integrate sqrt(2(V-E0)) over classically forbidden region
    S_WKB = np.trapz(np.sqrt(2.0 * np.maximum(V - E0, 0)), x)

    return E0, E1, Gamma_exact, S_WKB, V_b_over_E_zpf, V_barrier

# Test λ values: sanity check + new values
lambdas = [0.10, 0.30, 0.20, 0.15, 0.075, 0.05]

print("λ         V_barrier  E0         E1         Gamma_exact    S_WKB      V_b/E_zpf  E0<V_bar?")
print("-" * 110)
for lam in lambdas:
    E0, E1, Gamma_exact, S_WKB, V_b_E_zpf, V_barrier = compute_qm_tunneling_rate(lam)
    tunneling = "YES" if E0 < 0 else "NO (over-barrier)"
    print(f"λ={lam:.4f}  Vb={V_barrier:.4f}  E0={E0:.6f}  E1={E1:.6f}  "
          f"Γ_exact={Gamma_exact:.6e}  S_WKB={S_WKB:.4f}  Vb/Ezpf={V_b_E_zpf:.4f}  {tunneling}")

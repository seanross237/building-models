"""
Debug the S_WKB computation. E001 reported:
  λ=0.25: S_WKB=1.408
  λ=0.10: S_WKB=6.290

Let's check what the formula computes and understand the discrepancy.
"""
import numpy as np
import scipy.linalg

def compute_qm_fixed(lam, omega0=1.0, N_grid=2000, x_range=6.0):
    """Exact copy of E001 code - fixed x_range=6.0"""
    x = np.linspace(-x_range, x_range, N_grid)
    dx = x[1] - x[0]
    V = -0.5 * omega0**2 * x**2 + 0.25 * lam * x**4
    diag = 1.0/dx**2 + V
    off_diag = -0.5/dx**2 * np.ones(N_grid-1)
    eigenvalues = scipy.linalg.eigh_tridiagonal(diag, off_diag, eigvals_only=True,
                                                  select='i', select_range=(0, 3))
    E0, E1 = eigenvalues[0], eigenvalues[1]
    Gamma_exact = (E1 - E0) / 2.0
    E_zpf = np.sqrt(2.0) / 2.0
    V_barrier = 1.0 / (4.0 * lam)
    V_b_over_E_zpf = V_barrier / E_zpf
    S_WKB = np.trapz(np.sqrt(2.0 * np.maximum(V - E0, 0)), x)
    return E0, E1, Gamma_exact, S_WKB, V_b_over_E_zpf

# Test the sanity check values from E001
for lam in [0.25, 0.10]:
    E0, E1, Gamma_exact, S_WKB, V_b_E_zpf = compute_qm_fixed(lam)
    print(f"λ={lam}: E0={E0:.4f}, Gamma_exact={Gamma_exact:.6e}, S_WKB={S_WKB:.4f}, V_b/E_zpf={V_b_E_zpf:.4f}")

print()
print("Expected from E001: λ=0.25 S_WKB=1.408, λ=0.10 S_WKB=6.290")

# Now check with extended x_range for deep barriers
print()
print("With extended x_range:")
for lam, xr in [(0.25, 6.0), (0.10, 6.0), (0.10, 7.0)]:
    x = np.linspace(-xr, xr, 2000)
    V = -0.5*x**2 + 0.25*lam*x**4
    E0, E1, Gamma_exact, S_WKB, _ = compute_qm_fixed(lam, x_range=xr)
    print(f"λ={lam}, x_range={xr}: S_WKB={S_WKB:.4f}")

# The key question: what regions contribute to S_WKB for lambda=0.25?
print()
print("Analyzing forbidden regions for λ=0.25:")
lam = 0.25
x = np.linspace(-6, 6, 2000)
V = -0.5*x**2 + 0.25*lam*x**4
E0 = -0.4276  # from E001
mask = V > E0
x_forbidden = x[mask]
print(f"  Forbidden x ranges: {x_forbidden[0]:.3f} to {x_forbidden[-1]:.3f}")
# Find the breaks in the forbidden region
transitions = np.diff(mask.astype(int))
break_points = x[:-1][transitions != 0]
print(f"  Transition points (turning points): {break_points}")

print()
print("Analyzing forbidden regions for λ=0.10:")
lam = 0.10
x = np.linspace(-6, 6, 2000)
V = -0.5*x**2 + 0.25*lam*x**4
E0 = -1.8208  # from E001
mask = V > E0
transitions = np.diff(mask.astype(int))
break_points = x[:-1][transitions != 0]
print(f"  Transition points (turning points): {break_points}")

# Compute S_WKB only over central barrier (|x| < smallest outer turning point)
integrand = np.sqrt(2.0 * np.maximum(V - E0, 0))
# central barrier only: between inner turning points
if len(break_points) >= 2:
    x_inner_turn = min(abs(break_points[:2]))
    mask_central = (x >= -x_inner_turn) & (x <= x_inner_turn)
    S_central = np.trapz(integrand[mask_central], x[mask_central])
    print(f"  S_WKB central barrier only (|x|<{x_inner_turn:.3f}): {S_central:.4f}")
print(f"  S_WKB all forbidden regions: {np.trapz(integrand, x):.4f}")

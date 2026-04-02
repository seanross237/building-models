"""
WKB Tunneling Rate Computation for V(x) = -½ω₀²x² + ¼λx⁴

Steps:
1. Solve Schrödinger equation numerically (finite-difference) to get exact E_0 and E_1
2. Compute WKB action integral S_WKB = ∫ sqrt(2m(V-E_0)) dx over forbidden region
3. Report Γ_WKB = (ω_local/π) × exp(-S_WKB/ħ)
   and also the exact level splitting Γ_exact = (E_1-E_0)/ħ (quantum oscillation rate)

Note: The QM "tunneling rate" is defined as Γ = ΔE/(2ħ) where ΔE = E_1 - E_0 is the
tunnel splitting. This gives the Rabi oscillation frequency between the two well states.
"""

import numpy as np
from scipy.integrate import quad
from scipy.linalg import eigh_tridiagonal

# ── Parameters ────────────────────────────────────────────────────────────────
omega0 = 1.0
m      = 1.0
hbar   = 1.0

def run_wkb(lam):
    """Compute WKB and exact QM rates for given λ."""
    x_min_val  = omega0 / np.sqrt(lam)             # well minimum
    V_barrier  = omega0**4 / (4*lam)               # barrier height = V(0)-V(x_min)
    omega_local = omega0 * np.sqrt(2.0)            # ω_local = sqrt(V''(x_min)/m)
    # V(x) = -½ω₀²x² + ¼λx⁴
    # V'(x) = -ω₀²x + λx³ = 0 at x_min = ω₀/√λ
    # V''(x) = -ω₀² + 3λx² → V''(x_min) = -ω₀² + 3ω₀² = 2ω₀²
    # So ω_local = √(2ω₀²) = √2 ω₀  (same for all λ in this parameterization)

    print(f"\n{'='*60}")
    print(f"λ = {lam}")
    print(f"  x_min = ±{x_min_val:.4f}")
    print(f"  V_barrier = {V_barrier:.4f}")
    print(f"  ω_local = {omega_local:.4f} ω₀")

    def V(x):
        return -0.5*omega0**2*x**2 + 0.25*lam*x**4

    # ── Exact QM ground state via finite differences ─────────────────────────
    # Set up Hamiltonian on grid [-L, L]
    L     = max(6.0, 3*x_min_val)
    Ngrid = 2000
    x_grid = np.linspace(-L, L, Ngrid)
    dx = x_grid[1] - x_grid[0]

    Vgrid = V(x_grid)

    # Kinetic energy: -ħ²/(2m) × d²/dx² (finite difference, 3-point)
    diag    = hbar**2/(m*dx**2) + Vgrid         # main diagonal
    off     = -hbar**2/(2*m*dx**2) * np.ones(Ngrid-1)  # off-diagonal

    # Only need the lowest 3 eigenvalues
    # Use scipy eigh_tridiagonal (symmetric tridiagonal)
    eigvals = eigh_tridiagonal(diag, off, eigvals_only=True, select='i',
                                select_range=(0, 4))

    E0 = eigvals[0]   # ground state
    E1 = eigvals[1]   # first excited state
    delta_E = E1 - E0  # tunnel splitting

    print(f"  QM (exact diagonalization):")
    print(f"    E₀ = {E0:.6f} ħω₀")
    print(f"    E₁ = {E1:.6f} ħω₀")
    print(f"    ΔE = E₁ - E₀ = {delta_E:.8f} ħω₀")

    # Γ_exact: tunneling rate as Rabi oscillation (half-period of oscillation)
    # If particle starts in |R>, it tunnels to |L> after time T/2 = πħ/ΔE
    # Rate = 1/(T/2) = ΔE/(πħ)  [this is the "crossing rate" analog]
    # OR: Γ = ΔE/(2ħ)  [as frequency of full Rabi cycle]
    # The GOAL definition: Γ_WKB = (ω₀/π) × exp(-S_WKB/ħ)
    # This matches: Γ = ΔE/ħ × (1/π) ≈ ω_local/π × exp(-S/ħ) for the splitting formula
    # I'll report both definitions

    Gamma_exact_rabi    = delta_E / hbar                   # angular freq of Rabi oscillation
    Gamma_exact_crossing = delta_E / (2 * hbar)            # crossing rate (once per half-Rabi)

    print(f"    Γ_tunnel (Rabi freq) = ΔE/ħ = {Gamma_exact_rabi:.8f} ω₀")
    print(f"    Γ_tunnel (crossing)  = ΔE/(2ħ) = {Gamma_exact_crossing:.8f} ω₀")

    # ── WKB action integral ──────────────────────────────────────────────────
    # Forbidden region: where V(x) > E₀
    # Find turning points x₁ < x₂ where V(x) = E₀ (in range [0, x_min_val])

    # Find inner turning point x₁ ∈ [0, x_min_val] where V(x₁) = E₀
    # V is a quartic with V(0)=0 > E₀ and V(x_min_val)=V_min < E₀
    # Solve numerically
    from scipy.optimize import brentq

    def V_minus_E0(x):
        return V(x) - E0

    # Inner turning point: between 0 and x_min_val
    # V(0) = 0 > E₀ (since E₀ < 0), V(x_min_val) < 0 < E₀?
    # Wait: E₀ < 0 (ground state energy) and V(x_min_val) = -V_barrier < 0
    # Is V(x_min_val) < E₀?
    print(f"\n  Finding turning points:")
    print(f"    V(0) = 0, E₀ = {E0:.4f}")
    print(f"    V(x_min) = {V(x_min_val):.4f}")

    if V(0) > E0 and V(x_min_val) < E0:
        x_tp_inner = brentq(V_minus_E0, 0.001, x_min_val)
        print(f"    Inner turning point: x₁ = {x_tp_inner:.6f}")
    else:
        print("    ERROR: Can't find inner turning point — E₀ might be above V_barrier")
        print(f"    V_barrier = {V_barrier}, E₀ = {E0}")
        if E0 > 0:
            print("    E₀ > 0 means particle is ABOVE barrier — no tunneling!")
            return None
        x_tp_inner = 0.01  # fallback

    # WKB integrand: sqrt(2m(V(x)-E₀)) from -x₁ to +x₁
    def wkb_integrand(x):
        val = V(x) - E0
        if val < 0:
            return 0.0
        return np.sqrt(2 * m * val)

    S_wkb, S_err = quad(wkb_integrand, -x_tp_inner, x_tp_inner, limit=200)
    print(f"    S_WKB = ∫√(2m(V-E₀)) dx = {S_wkb:.6f} ħ  (integration error: {S_err:.2e})")

    # WKB tunneling rate using GOAL formula
    Gamma_WKB_goal = (omega0/np.pi) * np.exp(-S_wkb/hbar)
    Gamma_WKB_local = (omega_local/np.pi) * np.exp(-S_wkb/hbar)

    print(f"\n  WKB rates:")
    print(f"    Γ_WKB (ω₀/π prefactor)     = {Gamma_WKB_goal:.8f} ω₀")
    print(f"    Γ_WKB (ω_local/π prefactor) = {Gamma_WKB_local:.8f} ω₀")
    print(f"    Γ_exact (crossing rate)      = {Gamma_exact_crossing:.8f} ω₀")

    return {
        'lam': lam,
        'x_min': x_min_val,
        'V_barrier': V_barrier,
        'omega_local': omega_local,
        'E0': E0,
        'E1': E1,
        'delta_E': delta_E,
        'S_WKB': S_wkb,
        'Gamma_WKB_goal': Gamma_WKB_goal,
        'Gamma_WKB_local': Gamma_WKB_local,
        'Gamma_exact_crossing': Gamma_exact_crossing,
        'Gamma_exact_rabi': Gamma_exact_rabi,
        'x_tp_inner': x_tp_inner,
    }

# ── Run for all three λ values ────────────────────────────────────────────────
results = {}

for lam in [0.25, 0.1, 1.0]:
    r = run_wkb(lam)
    if r is not None:
        results[lam] = r

# ── Summary table ─────────────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("SUMMARY TABLE")
print("=" * 80)
print(f"{'λ':>6} {'V_bar':>8} {'E₀':>10} {'S_WKB':>10} {'Γ_WKB(goal)':>14} {'Γ_exact':>14} {'ΔE':>12}")
print("-" * 80)
for lam, r in sorted(results.items()):
    print(f"{lam:>6.2f} {r['V_barrier']:>8.4f} {r['E0']:>10.5f} {r['S_WKB']:>10.5f} "
          f"{r['Gamma_WKB_goal']:>14.8f} {r['Gamma_exact_crossing']:>14.8f} {r['delta_E']:>12.8f}")

print()
print("COMPARISON WITH SED RATES (from simulation):")
sed_rates = {0.25: (0.066279, 0.003505)}  # will add more after running other sims
for lam, (g_sed, g_sem) in sed_rates.items():
    if lam in results:
        r = results[lam]
        ratio_exact = g_sed / r['Gamma_exact_crossing'] if r['Gamma_exact_crossing'] > 0 else float('inf')
        ratio_wkb   = g_sed / r['Gamma_WKB_goal'] if r['Gamma_WKB_goal'] > 0 else float('inf')
        print(f"  λ={lam}: Γ_SED={g_sed:.6f}±{g_sem:.6f}  "
              f"Γ_WKB(goal)={r['Gamma_WKB_goal']:.8f}  "
              f"Γ_exact={r['Gamma_exact_crossing']:.8f}")
        print(f"         Ratio Γ_SED/Γ_WKB(goal) = {ratio_wkb:.4f}")
        print(f"         Ratio Γ_SED/Γ_exact      = {ratio_exact:.4f}")

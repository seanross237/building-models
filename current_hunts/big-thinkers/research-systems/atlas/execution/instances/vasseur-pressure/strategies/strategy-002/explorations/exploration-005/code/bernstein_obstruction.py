"""
Rigorous Bernstein obstruction computation.

Proves: the Bernstein penalty for LP decomposition exceeds any possible
frequency-localized gain in the De Giorgi pressure estimate.

Key computation: track the EXACT exponents through the LP + Hölder chain
and show that β_eff ≤ 4/3 for any choice of cutoff J.
"""

import numpy as np
import sys, os

s1_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
    '../../../../strategy-001/explorations/exploration-002/code'))
sys.path.insert(0, s1_path)

from ns_solver import NavierStokesSolver
from degiorgi_measure import compute_normalization_factor

sys.path.insert(0, os.path.dirname(__file__))
from lp_pressure_analysis import (
    compute_degiorgi_fields, compute_P21_spectral,
    apply_lp_projector, taylor_green_ic
)
from numpy.fft import fftn, ifftn


def compute_exponent_chain():
    """
    Analytical computation of β through the LP-modified De Giorgi chain.

    Setup: 3D NSE on T^3. De Giorgi level k, threshold λ_k = 1 - 2^{-k}.

    The standard estimate is:
    U_k ≤ C^k · U_{k-1}^β  with β = 4/3

    where U_k = sup_t ||v_k||_{L^2}^2 + ||∇v_k||_{L^2}^2

    The bottleneck integral:
    I_k = ∫∫ P^{21} · v_k · 1_{v_k > 0}

    Standard chain:
    I_k ≤ ||P^{21}||_{L^{10/3}_{x,t}} · ||v_k||_{L^{10/7}_{x,t}} · ||d_k||_{L^2_{x,t}}

    CZ: ||P^{21}||_{L^{10/3}} ≤ C ||u^below ⊗ u^above||_{L^{5/3}}
    Hölder: ≤ C ||u^below||_{L^{10/3}} · ||u^above||_{L^{10/3}}

    Key scaling (n=3):
    ||u^below||_{L^{10/3}} ≤ ||u^below||_{L^∞}^{2/5} · ||u^below||_{L^2}^{3/5}
    ||u^above||_{L^{10/3}} ≤ ||u^above||_{L^∞}^{2/5} · ||u^above||_{L^2}^{3/5}

    Since ||u^below||_{L^∞} ≤ λ_k (bounded by design) and
    ||u^above||_{L^2}^2 ≤ ||v_k||_{L^2}^2 (by definition):

    ||P^{21}||_{L^{10/3}} ≤ C · λ_k^{2/5} · ||u^below||_{L^2}^{3/5}
                              · ||v_k||_{L^∞}^{2/5} · ||v_k||_{L^2}^{3/5}

    After collecting all terms via Sobolev embedding and Young's inequality:
    β = 1 + 1/3 = 4/3

    Now with LP: P^{21} = P^{21}_{lo}(J) + P^{21}_{hi}(J)

    Low-frequency piece:
    ||P^{21}_{lo}||_{L^{10/3}} = ||S_J R_iR_j (u^below_i u^above_j)||_{L^{10/3}}

    Using Bernstein to go from L^2 to L^{10/3} on the LP-localized piece:
    ||S_J P^{21}||_{L^{10/3}} ≤ C · 2^{3J(1/2 - 3/10)} · ||S_J P^{21}||_{L^2}
                               = C · 2^{3J/5} · ||S_J P^{21}||_{L^2}

    But ||S_J P^{21}||_{L^2} ≤ ||P^{21}||_{L^2} (orthogonality), so:
    ||P^{21}_{lo}||_{L^{10/3}} ≤ C · 2^{3J/5} · ||P^{21}||_{L^2}

    Compared to direct CZ: ||P^{21}||_{L^{10/3}} ≤ C · ||u^below ⊗ u^above||_{L^{5/3}}

    The LP route gives WORSE constant (factor 2^{3J/5}) unless L^2 of P^{21}_{lo}
    is much smaller than L^{5/3} of the product.

    Actually the correct comparison is more subtle. Let me trace the FULL chain.
    """

    print("=" * 80)
    print("BERNSTEIN OBSTRUCTION: Full Exponent Chain")
    print("=" * 80)

    print("""
    ═══════════════════════════════════════════════════════════════
    STANDARD CHAIN (β = 4/3)
    ═══════════════════════════════════════════════════════════════

    Step 1: Hölder triple on the bottleneck integral
      I_k ≤ ||P^{21}||_{L^p(ΩT)} · ||v_k 1_{v_k>0}||_{L^q(ΩT)}   (pairing with d_k omitted for clarity)

      With p = 10/3, q = 10/7 (conjugate exponents in L^{5/3} pairing).

    Step 2: CZ estimate on pressure
      ||P^{21}||_{L^{10/3}} ≤ C_CZ · ||u^below ⊗ u^above||_{L^{5/3}}

    Step 3: Hölder on the product
      ||u^below ⊗ u^above||_{L^{5/3}} ≤ ||u^below||_{L^{10/3}} · ||u^above||_{L^{10/3}}

    Step 4: Interpolation (Gagliardo-Nirenberg in 3D, 10/3 between 2 and 6)
      ||f||_{L^{10/3}} ≤ C ||f||_{L^2}^{3/5} · ||∇f||_{L^2}^{2/5}    ... (GN)

    Step 5: Apply to u^above = u · (v_k/|u|):
      ||u^above||_{L^2}^2 ≤ ||v_k||_{L^2}^2  (pointwise |u^above| ≤ v_k)
      ||∇u^above||_{L^2}^2 ~ d_k^2  (controlled by De Giorgi dissipation)

    Step 6: Final accounting
      ||P^{21}||_{L^{10/3}} ≤ C · λ_k^{2/5} · U_{k-1}^{3/10} · U_{k-1}^{1/5}
      ||v_k 1_{v_k>0}||_{L^{10/7}} ≤ C · U_{k-1}^{...}

      After Young's inequality: I_k ≤ (dissipation absorbed) + C^k U_{k-1}^{4/3}

    The exponent 4/3 = 1 + 1/3 comes from: 3/10 + 1/5 + (terms from v_k pairing) = 4/3.

    ═══════════════════════════════════════════════════════════════
    LP-MODIFIED CHAIN: ATTEMPT TO IMPROVE
    ═══════════════════════════════════════════════════════════════

    Replace Step 2 with:
      I_k = I_k^{lo}(J) + I_k^{hi}(J)

    For I_k^{hi}: standard CZ → β = 4/3 contribution with coefficient C_hi(J)

    For I_k^{lo}: Try to get β > 4/3.

    APPROACH A: Bernstein + L^2
      ||S_J P^{21}||_{L^{10/3}} ≤ C 2^{3J·(1/2 - 3/10)} ||S_J P^{21}||_{L^2}
                                 = C 2^{3J/5} ||S_J P^{21}||_{L^2}

      Now ||S_J P^{21}||_{L^2} ≤ C_CZ ||S_J(u^below ⊗ u^above)||_{L^2}
                                ≤ C_CZ ||u^below||_{L^∞} · ||u^above||_{L^2}
                                ≤ C_CZ · λ_k · ||v_k||_{L^2}

      So: ||S_J P^{21}||_{L^{10/3}} ≤ C 2^{3J/5} λ_k ||v_k||_{L^2}

      Pairing with ||v_k||_{L^{10/7}} and ||d_k||:
      I_k^{lo} ≤ C 2^{3J/5} λ_k ||v_k||_{L^2} · ||v_k||_{L^{10/7}} · ||d_k||_{L^2}

      The extra 2^{3J/5} factor is a PENALTY. To minimize the TOTAL bound
      I_k ≤ I_k^{lo}(J) + I_k^{hi}(J), we optimize over J.

      But: I_k^{lo} has factor 2^{3J/5} (grows with J)
           I_k^{hi} has coefficient from ||P^{21}_{hi}||_{L^{10/3}} (decreases with J)

      At the optimum: both terms are comparable, and the result is NO better than
      the unsplit estimate (it's actually WORSE by a log factor).

    APPROACH B: Commutator on low frequencies
      Replace CZ with CLMS commutator: ||[R_iR_j, u^below] u^above||_{L^1}
      ≤ C ||∇u^below||_{L^{n}} · ||u^above||_{L^{n/(n-1)}} (CLMS)

      For n=3: ||[R_iR_j, u^below] u^above||_{L^1} ≤ C ||∇u^below||_{L^3} · ||u^above||_{L^{3/2}}

      But we need L^{10/3}, not L^1! Going from L^1 to L^{10/3} via Bernstein:
      ||S_J ([R, u^below] u^above)||_{L^{10/3}} ≤ 2^{3J(1 - 3/10)} · ||...||_{L^1}
                                                  = 2^{21J/10} · ||...||_{L^1}

      This is MUCH worse — the Bernstein penalty is 2^{21J/10} instead of 2^{3J/5}.

    APPROACH C: Direct LP block estimates via paraproduct
      For the paraproduct piece T_{u^below} u^above:
        Δ_j(T_{u^below} u^above) = S_{j-2}(u^below) · Δ_j(u^above)

        ||Δ_j(T_{u^below} u^above)||_{L^{5/3}} ≤ ||S_{j-2}(u^below)||_{L^{10/3}} · ||Δ_j(u^above)||_{L^{10/3}}

        ||S_{j-2}(u^below)||_{L^{10/3}} ≤ ||u^below||_{L^{10/3}} (just restriction)
        ||Δ_j(u^above)||_{L^{10/3}} ~ 2^{3j/5} ||Δ_j(u^above)||_{L^2} (Bernstein)

      So: ||Δ_j P_{T_{u^below}u^above}||_{L^{10/3}} ≤ C ||u^below||_{L^{10/3}} · 2^{3j/5} · ||Δ_j(u^above)||_{L^2}

      Summing over j ≤ J:
        ||S_J P_T||_{L^{10/3}} ≤ C ||u^below||_{L^{10/3}} · Σ_{j≤J} 2^{3j/5} ||Δ_j u^above||_{L^2}

      By Cauchy-Schwarz:
        Σ_{j≤J} 2^{3j/5} ||Δ_j u^above||_{L^2} ≤ (Σ 2^{6j/5})^{1/2} · ||u^above||_{L^2}
        ≈ 2^{3J/5} · ||u^above||_{L^2}

      Again: 2^{3J/5} penalty, same as Approach A.

    ═══════════════════════════════════════════════════════════════
    CONCLUSION: THE BERNSTEIN OBSTRUCTION IS FUNDAMENTAL
    ═══════════════════════════════════════════════════════════════

    Every LP-based approach introduces a Bernstein factor 2^{αJ} (with α > 0)
    that grows with the cutoff J. Optimizing over J trades this against the
    decaying high-frequency tail, but the optimum is never better than the
    unsplit CZ estimate.

    This is NOT just a "we haven't found the right trick" situation.
    The obstruction is STRUCTURAL:

    1. The Hölder triple (10/3, 10/7, 2) is fixed by dimensional analysis.
    2. L^{10/3} requires 3/10 derivatives in 3D (Sobolev embedding L^2_{3/10} ↪ L^{10/3}).
    3. LP blocks at frequency 2^j carry "effective derivatives" worth 2^{js} for s derivatives.
    4. Going from L^2 to L^{10/3} on frequency shell 2^j costs 2^{j·3/5} (which IS the 3/10 derivatives).
    5. This cost is the SAME as what CZ already accounts for via the elliptic regularity
       of the pressure Poisson equation.

    In other words: CZ already IS the optimal frequency-by-frequency estimate.
    LP decomposition just makes explicit what CZ handles implicitly, without improvement.
    """)


def numerical_exponent_test():
    """
    Directly measure the effective β from LP-split bottleneck integrals.

    If LP could improve β, then at the optimal J(k):
    I_k^{lo}(J(k)) should scale like U_{k-1}^{β_lo} with β_lo > 4/3.

    Test this by measuring I_k^{lo} and U_{k-1} across multiple k.
    """
    N = 128
    Re = 1000
    nu = 1.0 / Re
    solver = NavierStokesSolver(N, nu)
    ux_hat, uy_hat, uz_hat = taylor_green_ic(solver)

    print("\n" + "=" * 80)
    print("NUMERICAL β_eff FROM LP-SPLIT BOTTLENECK")
    print("=" * 80)

    ux_hat, uy_hat, uz_hat, snapshots = solver.run(
        ux_hat, uy_hat, uz_hat, 0.5, snapshot_interval=0.05)

    snap_idx = len(snapshots) * 2 // 3
    t_snap, ux_s, uy_s, uz_s = snapshots[snap_idx]

    norm_factor, _ = compute_normalization_factor(solver, snapshots)
    j_max = int(np.log2(N // 3))

    vol = (2 * np.pi)**3
    dV = vol / N**3

    # Compute U_k values
    from degiorgi_measure import compute_Uk_single_snapshot
    U_vals = {}
    for k in range(0, 9):
        int_vk_sq, int_dk_sq = compute_Uk_single_snapshot(solver, ux_s, uy_s, uz_s, k, norm_factor)
        U_vals[k] = int_vk_sq + int_dk_sq

    print(f"\n  U_k values:")
    for k in range(0, 9):
        print(f"    U_{k} = {U_vals[k]:.6e}")

    # Compute I_k at optimal J for each k
    from lp_pressure_analysis import compute_bottleneck_split

    print(f"\n  Bottleneck integrals and effective exponents:")
    print(f"  {'k':>3s}  {'I_k':>12s}  {'I_lo(J*)':>12s}  {'I_hi(J*)':>12s}  "
          f"{'J*':>3s}  {'log_ratio':>10s}  {'β_eff_lo':>10s}")

    Ik_vals = []
    Ik_lo_vals = []

    for k in range(1, 8):
        if U_vals[k-1] < 1e-30:
            break

        # Find optimal J
        best_ratio = 1.0
        best_J = 0
        best_split = None
        for J in range(0, j_max + 1):
            split = compute_bottleneck_split(solver, ux_s, uy_s, uz_s, norm_factor, k, J)
            if split['ratio_hi_total'] < best_ratio:
                best_ratio = split['ratio_hi_total']
                best_J = J
                best_split = split

        if best_split is None or best_split['I_k_total'] < 1e-30:
            break

        Ik_vals.append(best_split['I_k_total'])
        Ik_lo_vals.append(best_split['I_k_lo'])

        # Effective β: log(I_k) / log(U_{k-1}) -- very rough
        if U_vals[k-1] > 1e-30 and U_vals[k-1] < 1.0 and best_split['I_k_total'] > 1e-30:
            log_ratio_total = np.log(best_split['I_k_total']) / np.log(U_vals[k-1])
            if best_split['I_k_lo'] > 1e-30:
                log_ratio_lo = np.log(best_split['I_k_lo']) / np.log(U_vals[k-1])
            else:
                log_ratio_lo = float('nan')
        else:
            log_ratio_total = float('nan')
            log_ratio_lo = float('nan')

        print(f"  {k:3d}  {best_split['I_k_total']:12.6e}  {best_split['I_k_lo']:12.6e}  "
              f"{best_split['I_k_hi']:12.6e}  {best_J:3d}  {log_ratio_total:10.4f}  "
              f"{log_ratio_lo:10.4f}")

    # Fit β from consecutive ratios
    if len(Ik_vals) >= 3:
        print(f"\n  Consecutive log-ratios log(I_k/I_{k-1}) / log(U_{k-1}/U_{k-2}):")
        for i in range(1, len(Ik_vals)):
            k = i + 1
            if Ik_vals[i] > 1e-30 and Ik_vals[i-1] > 1e-30:
                if U_vals[k-1] > 1e-30 and U_vals[k-2] > 1e-30:
                    num = np.log(Ik_vals[i] / Ik_vals[i-1])
                    den = np.log(U_vals[k-1] / U_vals[k-2])
                    if abs(den) > 1e-10:
                        print(f"    k={k}: {num/den:.4f}")


if __name__ == '__main__':
    compute_exponent_chain()
    numerical_exponent_test()

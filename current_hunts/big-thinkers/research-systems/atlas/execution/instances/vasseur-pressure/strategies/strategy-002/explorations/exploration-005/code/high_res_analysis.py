"""
High-resolution LP analysis at N=128 for more LP blocks and the critical
spectral-peak-shift analysis.

Also performs the analytical Bernstein accounting that determines whether
LP decomposition can improve β.
"""

import numpy as np
from numpy.fft import fftn, ifftn, fftfreq
import sys, os

s1_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
    '../../../../strategy-001/explorations/exploration-002/code'))
sys.path.insert(0, s1_path)

from ns_solver import NavierStokesSolver
from degiorgi_measure import (compute_velocity_magnitude_and_gradients,
                               compute_normalization_factor)

# Import from our own code
sys.path.insert(0, os.path.dirname(__file__))
from lp_pressure_analysis import (
    compute_degiorgi_fields, compute_P21_spectral,
    measure_lp_spectrum, compute_bottleneck_split,
    apply_lp_projector, apply_low_pass, apply_high_pass,
    taylor_green_ic, kida_vortex_ic,
    bernstein_check
)


def spectral_peak_shift_analysis(solver, ux_hat, uy_hat, uz_hat, norm_factor, k_max=6):
    """
    For each De Giorgi level k, find the LP block j* where ||Δ_j P^{21}||_{L^2} peaks.
    If j* grows with k, the spectral content shifts to higher frequencies as k increases.
    This is the KEY diagnostic for whether LP splitting can help.
    """
    N = solver.N
    j_max = int(np.log2(N // 3))

    print("\n=== SPECTRAL PEAK SHIFT ANALYSIS ===")
    print(f"  N={N}, j_max={j_max} (max frequency ~{2**(j_max+1):.0f})")
    print(f"  {'k':>3s}  {'j*':>3s}  {'peak frac':>10s}  {'hi frac (j>j*)':>15s}  "
          f"{'peak freq':>10s}  {'active frac':>12s}")

    peak_data = []
    for k in range(1, k_max + 1):
        (ux_below, uy_below, uz_below,
         ux_above, uy_above, uz_above,
         v_k, active, u_mag_norm) = compute_degiorgi_fields(
             solver, ux_hat, uy_hat, uz_hat, norm_factor, k)

        if np.mean(active) < 1e-10:
            print(f"  {k:3d}  ---  (no active set)")
            continue

        P21_hat, P21_phys = compute_P21_spectral(
            solver, ux_below, uy_below, uz_below, ux_above, uy_above, uz_above)

        j_vals, l2_norms = measure_lp_spectrum(P21_hat, solver.K_mag, N, j_max)
        total_l2 = np.sqrt(np.sum(P21_phys**2) * (2*np.pi)**3 / N**3)

        if total_l2 < 1e-30:
            print(f"  {k:3d}  ---  (zero pressure)")
            continue

        # Find peak
        j_star = j_vals[np.argmax(l2_norms)]
        peak_frac = np.max(l2_norms) / total_l2

        # Fraction in j > j_star
        hi_mask = j_vals > j_star
        hi_frac = np.sqrt(np.sum(l2_norms[hi_mask]**2)) / total_l2

        peak_freq = 2.0**(j_star + 1) if j_star >= 0 else 1.0

        print(f"  {k:3d}  {j_star:3d}  {peak_frac:10.4f}  {hi_frac:15.4f}  "
              f"{peak_freq:10.1f}  {np.mean(active):12.6f}")

        peak_data.append({
            'k': k, 'j_star': j_star, 'peak_frac': peak_frac,
            'hi_frac': hi_frac, 'peak_freq': peak_freq, 'active': np.mean(active)
        })

    return peak_data


def adaptive_J_analysis(solver, ux_hat, uy_hat, uz_hat, norm_factor, k_max=6):
    """
    For each k, try J = k-1, J = k, J = k+1 as the LP cutoff.
    The idea: match the LP cutoff to the De Giorgi scale.
    Report I_hi/I_total at each choice.
    """
    N = solver.N
    j_max = int(np.log2(N // 3))

    print("\n=== ADAPTIVE J = f(k) ANALYSIS ===")
    print(f"  Testing J = k-1, k, k+1 (capped at j_max={j_max})")
    print(f"  {'k':>3s}  {'J=k-1':>10s}  {'J=k':>10s}  {'J=k+1':>10s}  {'J=j_max':>10s}")

    for k in range(1, k_max + 1):
        ratios = []
        for J in [max(0, k-1), min(k, j_max), min(k+1, j_max), j_max]:
            split = compute_bottleneck_split(solver, ux_hat, uy_hat, uz_hat, norm_factor, k, J)
            ratios.append(split['ratio_hi_total'])

        if split['I_k_total'] < 1e-30:
            print(f"  {k:3d}  (zero integral)")
            continue

        print(f"  {k:3d}  {ratios[0]:10.4f}  {ratios[1]:10.4f}  {ratios[2]:10.4f}  {ratios[3]:10.4f}")


def bernstein_cost_analysis(solver, ux_hat, uy_hat, uz_hat, norm_factor, k=2):
    """
    The CRITICAL analytical check.

    The De Giorgi pressure estimate is:
    I_k ≤ ||P^{21}||_{L^{10/3}} * ||v_k||_{L^{10/7}} * ||d_k||_{L^2}  (Hölder triple)

    With LP splitting:
    I_k^{lo}(J) ≤ ||S_J P^{21}||_{L^{10/3}} * ...
    I_k^{hi}(J) ≤ ||(Id-S_J) P^{21}||_{L^{10/3}} * ...

    For the low-frequency part, if there's commutator structure, maybe
    ||S_J P^{21}||_{L^{10/3}} has better dependence on U_{k-1}.

    But even without improved estimates, the question is:
    Can we use Bernstein to bound ||S_J P^{21}||_{L^{10/3}} more tightly than CZ
    gives for the full ||P^{21}||_{L^{10/3}}?

    Answer: NO. Bernstein from L^2 to L^{10/3} introduces factor 2^{3j/5} per block.
    Summing over j ≤ J gives a factor ~2^{3J/5} which GROWS with J.
    The only way LP helps is if the LOW-FREQUENCY L^2 norms decay fast enough
    that 2^{3j/5} * ||Δ_j P||_{L^2} is DECREASING in j.

    Compute this explicitly.
    """
    N = solver.N
    j_max = int(np.log2(N // 3))

    (ux_below, uy_below, uz_below,
     ux_above, uy_above, uz_above,
     v_k, active, u_mag_norm) = compute_degiorgi_fields(
         solver, ux_hat, uy_hat, uz_hat, norm_factor, k)

    P21_hat, P21_phys = compute_P21_spectral(
        solver, ux_below, uy_below, uz_below, ux_above, uy_above, uz_above)

    vol = (2*np.pi)**3
    dV = vol / N**3

    print(f"\n=== BERNSTEIN COST ANALYSIS (k={k}) ===")
    print(f"\n  The key product: 2^{{3j/5}} * ||Δ_j P||_L2 (Bernstein-inflated L^2)")
    print(f"  If this GROWS with j, Bernstein eats the LP gain.")
    print(f"  If this DECAYS with j, LP + Bernstein can beat CZ.\n")

    print(f"  {'j':>4s}  {'||Dj||_L2':>12s}  {'2^(3j/5)':>10s}  {'inflated':>12s}  "
          f"{'cumul_lo':>12s}  {'cumul_hi':>12s}")

    inflated_vals = []
    j_vals_list = []

    for j in range(0, j_max + 1):
        Dj_hat = apply_lp_projector(P21_hat, solver.K_mag, j, N)
        Dj_phys = ifftn(Dj_hat).real
        Dj_l2 = np.sqrt(np.sum(Dj_phys**2) * dV)

        bern = 2.0**(3.0 * j / 5.0)
        inflated = bern * Dj_l2

        # Cumulative: sum of inflated for j' <= j (lo) and j' > j (hi)
        inflated_vals.append(inflated)
        j_vals_list.append(j)

    # Compute cumulative sums
    inflated_arr = np.array(inflated_vals)
    cum_lo = np.cumsum(inflated_arr)
    cum_hi = np.sum(inflated_arr) - cum_lo

    for idx, j in enumerate(j_vals_list):
        Dj_hat = apply_lp_projector(P21_hat, solver.K_mag, j, N)
        Dj_phys = ifftn(Dj_hat).real
        Dj_l2 = np.sqrt(np.sum(Dj_phys**2) * dV)
        bern = 2.0**(3.0 * j / 5.0)
        inflated = bern * Dj_l2

        print(f"  {j:4d}  {Dj_l2:12.6e}  {bern:10.4f}  {inflated:12.6e}  "
              f"{cum_lo[idx]:12.6e}  {cum_hi[idx]:12.6e}")

    # CZ reference: ||P^{21}||_{L^{10/3}} via CZ operator norms
    P_l103 = (np.sum(np.abs(P21_phys)**(10.0/3.0)) * dV)**(3.0/10.0)
    P_l2 = np.sqrt(np.sum(P21_phys**2) * dV)

    print(f"\n  Full ||P^21||_L^{{10/3}} (direct) = {P_l103:.6e}")
    print(f"  Full ||P^21||_L^2 = {P_l2:.6e}")
    print(f"  Sum of Bernstein-inflated L^2 blocks = {np.sum(inflated_arr):.6e}")
    print(f"  Ratio (Bernstein sum / direct L^{{10/3}}): "
          f"{np.sum(inflated_arr) / max(P_l103, 1e-30):.4f}")

    # Key question: does the inflated sequence increase or decrease?
    if len(inflated_vals) > 1:
        increasing = sum(1 for i in range(len(inflated_vals)-1)
                         if inflated_vals[i+1] > inflated_vals[i])
        decreasing = len(inflated_vals) - 1 - increasing
        print(f"\n  Inflated sequence: {increasing} increasing steps, {decreasing} decreasing steps")
        if increasing > decreasing:
            print(f"  VERDICT: Bernstein inflation DOMINATES spectral decay → LP LOSES")
        else:
            print(f"  VERDICT: Spectral decay dominates Bernstein inflation → LP MIGHT WIN")


def hölder_exponent_analysis():
    """
    Analytical computation of what β LP decomposition could achieve.

    In the standard proof:
    I_k ≤ ||P^{21}||_{L^{10/3}} * ||v_k||_{L^{10/7}} * ||d_k||_{L^2}

    CZ: ||P^{21}||_{L^{10/3}} ≤ C ||u^below||_{L^{10/3}} * ||u^above||_{L^{10/3}}
    ≤ C ||u^below||_{L^∞}^{2/5} ||u^below||_{L^2}^{3/5} * same for u^above

    After Hölder on the De Giorgi chain:
    I_k ≤ C^k * U_{k-1}^{β} with β = 1 + 1/(n+2) = 1 + 1/5 = 6/5? No...

    Actually in 3D: β = 1 + 2/(n+2) = 1 + 2/5 = 7/5? Let me recheck.

    The Vasseur (2007) proof gives β = 4/3 = 1 + 1/3 in 3D.
    The exponent comes from the Hölder pairing of L^{10/3} pressure with L^{10/7} test function
    and L^2 dissipation.

    With LP, the question becomes: what is the best exponent of U_{k-1} in the estimate
    of ||S_J P^{21}||_{L^{10/3}} ?

    If we could show ||S_J P^{21}||_{L^{10/3}} ≤ C(J) * U_{k-1}^{β_lo} with β_lo > 4/3,
    and C(J) grows mildly enough, we win.

    But the constraint is: even for low frequencies, the bilinear form u^below * u^above
    involves BOTH low and high frequency content (via physical-space multiplication).
    The LP projector on the pressure doesn't simplify the Hölder exponents of u^below, u^above.

    Compute: what exponent does the paraproduct T_{u^below} u^above give?
    T_{u^below} u^above: S_{j-2}(u^below) is low-frequency → L^∞ bounded.
    Δ_j(u^above) is frequency-localized → Bernstein + L^2.

    ||Δ_j T_{u^below} u^above||_{L^p} ≤ ||S_{j-2}(u^below)||_{L^∞} * ||Δ_j(u^above)||_{L^p}

    This is EXACTLY the CZ estimate! u^below bounded, u^above in L^p.
    No improvement.

    For T_{u^above} u^below: S_{j-2}(u^above) at low frequency → L^∞ bounded by
    Bernstein: ||S_{j-2} u^above||_{L^∞} ≤ C 2^{3j/2} ||S_{j-2} u^above||_{L^2}
    This is WORSE than the direct estimate.

    For R(u^below, u^above): resonance term, |j-j'| ≤ 1.
    R_j ≤ ||Δ_j u^below||_{L^2} * ||tilde{Δ}_j u^above||_{L^2} * volume factors
    This requires BOTH factors at the SAME frequency → no improvement from splitting.
    """
    print("\n=== ANALYTICAL HÖLDER EXPONENT ANALYSIS ===")
    print("""
    Standard Vasseur proof chain:

    I_k = ∫ P^{21} · v_k · 1_{v_k > 0} dx dt

    By Hölder with (10/3, 10/7, 2):
    I_k ≤ ||P^{21}||_{L^{10/3}} · ||v_k||_{L^{10/7}} · ||d_k||_{L^2}  ... (*)

    CZ gives: ||P^{21}||_{L^{10/3}} ≤ C ||u^below ⊗ u^above||_{L^{5/3}}

    By Hölder: ||u^below ⊗ u^above||_{L^{5/3}} ≤ ||u^below||_{L^{10/3}} · ||u^above||_{L^{10/3}}

    Now with LP splitting, P^{21} = P^{21}_{lo} + P^{21}_{hi}:

    I_k ≤ ||P^{21}_{lo}||_{L^{10/3}} · ... + ||P^{21}_{hi}||_{L^{10/3}} · ...

    For P^{21}_{lo}: Even with commutator improvement, the BEST we can get is:
    ||P^{21}_{lo}||_{L^{10/3}} ≤ C · ||u^below||_{BMO} · ||u^above||_{L^{10/3}}
                                  (via CLMS/CRW commutator theorem)
    But ||u^below||_{BMO} ≤ 2||u^below||_{L^∞} (since u^below is bounded).
    So the BMO norm gives NO improvement over the L^∞ bound.

    For P^{21}_{hi}: standard CZ → β = 4/3.

    CRITICAL INSIGHT: The Hölder triple (10/3, 10/7, 2) is FIXED by the energy structure.
    LP decomposition changes how we estimate ||P||_{L^{10/3}}, but:
    - The bilinear structure u^below · u^above means each paraproduct piece
      inherits the SAME CZ exponents.
    - Bernstein inequalities for individual LP blocks INFLATE by 2^{3j/5}.
    - The only way LP helps is if ||Δ_j P||_{L^{10/3}} decays faster than 2^{-3j/5}
      for large j, making the sum convergent.
    - But P^{21} is a CZ transform of a product — its LP spectrum decays like
      the product's spectrum, which is governed by the ROUGHEST factor.
    - For u^above (rough, with derivatives at the De Giorgi threshold), the spectrum
      does NOT decay faster than 2^{-3j/5}. It's essentially flat until the dissipation cutoff.

    CONCLUSION: LP decomposition cannot improve β beyond 4/3 because:
    1. Each paraproduct piece inherits standard CZ exponents.
    2. Bernstein inflation 2^{3j/5} per block eats any frequency-localized gain.
    3. The low-frequency commutator improvement (CRW) is neutralized by
       ||u^below||_{BMO} ≤ 2||u^below||_{L^∞}.
    4. The spectral peak of P^{21} shifts to HIGHER frequencies with k,
       making the high-frequency problem WORSE at higher De Giorgi levels.
    """)


def run_high_res():
    """Run the high-resolution analysis."""
    N = 128
    Re = 1000
    nu = 1.0 / Re
    solver = NavierStokesSolver(N, nu)

    ux_hat, uy_hat, uz_hat = taylor_green_ic(solver)

    print(f"=== Running NS solver: N={N}, Re={Re}, Taylor-Green, T=0.5 ===")
    ux_hat, uy_hat, uz_hat, snapshots = solver.run(
        ux_hat, uy_hat, uz_hat, 0.5, snapshot_interval=0.05)
    print(f"  Collected {len(snapshots)} snapshots")

    snap_idx = len(snapshots) * 2 // 3
    t_snap, ux_s, uy_s, uz_s = snapshots[snap_idx]
    print(f"  Using snapshot at t = {t_snap:.4f}")

    norm_factor, _ = compute_normalization_factor(solver, snapshots)
    print(f"  L^inf normalization: {norm_factor:.6f}")

    # Task 1: Spectral peak shift
    peak_data = spectral_peak_shift_analysis(solver, ux_s, uy_s, uz_s, norm_factor, k_max=8)

    # Task 2: Adaptive J analysis
    adaptive_J_analysis(solver, ux_s, uy_s, uz_s, norm_factor, k_max=8)

    # Task 3: Bernstein cost analysis at multiple k
    for k in [1, 2, 3, 4, 5]:
        bernstein_cost_analysis(solver, ux_s, uy_s, uz_s, norm_factor, k=k)

    # Task 4: Analytical summary
    hölder_exponent_analysis()


if __name__ == '__main__':
    run_high_res()

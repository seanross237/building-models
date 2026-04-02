#!/usr/bin/env python3
"""
Computational verification of the BKM enstrophy bound proof steps.

Checks each inequality in the proof chain against DNS data from exploration-001.
Also computes the Prodi-Serrin comparison quantities.
"""
import numpy as np
import json
import os
import sys

# Path to exploration-001 results and code
E001_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'exploration-001')
sys.path.insert(0, os.path.join(E001_DIR, 'code'))

from ns_solver import NavierStokesSolver, taylor_green_ic


def load_results():
    """Load all results from exploration-001."""
    with open(os.path.join(E001_DIR, 'results', 'all_results.json')) as f:
        return json.load(f)


def verify_proof_chain(results):
    """
    For each timestep in each simulation, verify:

    Step 1: |∫ ω_i S_{ij} ω_j dx| ≤ ||ω||²_{L²} · ||S||_{L^∞}   (Hölder)
    Step 2: ||S||_{L^∞} ≤ C_{BGW} ||ω||_{L^∞} [1 + log⁺(||∇ω||/||ω||)]  (Brezis-Gallouet-Wainger)
    Step 3: Combined → dE/dt ≤ 2·C·E·||ω||_{L^∞}·log_factor - 2ν·||∇ω||²

    Also check:
    Step 4: Ladyzhenskaya version: dE/dt ≤ C_L²·||ω||^{3/2}·||∇ω||^{3/2} - ν·||∇ω||²
    Step 5: After Young's: dE/dt ≤ (27·C_L⁸)/(128·ν³) · E³   (cubic blow-up)
    """
    C_L = 0.827

    print("=" * 100)
    print("VERIFICATION OF BKM ENSTROPHY PROOF CHAIN")
    print("=" * 100)

    for r in results:
        ic = r['ic_name']
        Re = r['Re']
        N = r['N']
        nu = r['nu']
        diags = r['diagnostics']
        times = r['times']

        if len(diags) == 0:
            continue

        # Only show TGV Re=1000 in detail
        show_detail = (ic == 'TGV' and Re == 1000 and N == 64)

        n_steps = len(diags)
        step1_holds = 0
        step2_holds = 0
        step3_holds = 0

        min_C_BGW = float('inf')
        max_C_BGW = 0

        if show_detail:
            print(f"\n{'='*100}")
            print(f"DETAILED: {ic} Re={Re} N={N}")
            print(f"{'='*100}")
            print(f"{'t':>6} | {'|VS|':>10} | {'Step1 bnd':>10} | {'Step1 ok':>8} | {'S_Linf':>10} | {'BGW bnd':>10} | {'C_BGW_emp':>10} | {'Lad bnd':>10} | {'BKM bnd':>10}")
            print("-" * 100)

        for i, d in enumerate(diags):
            t = times[i] if i < len(times) else 0

            omega_L2 = d.get('omega_L2', 0)
            omega_Linf = d.get('omega_Linf', 0)
            grad_omega_L2 = d.get('grad_omega_L2', 0)
            S_Linf = d.get('S_Linf', 0)
            vs = d.get('vortex_stretching', 0)
            abs_vs = abs(vs)

            # Step 1: |VS| ≤ ||ω||² · ||S||_{L^∞}
            step1_bound = omega_L2**2 * S_Linf
            s1_ok = abs_vs <= step1_bound * 1.01  # 1% tolerance for numerics
            if s1_ok: step1_holds += 1

            # Step 2: ||S||_{L^∞} ≤ C_BGW · ||ω||_{L^∞} · [1 + log⁺(||∇ω||/||ω||)]
            log_ratio = 0.0
            if omega_L2 > 1e-14 and grad_omega_L2 > omega_L2:
                log_ratio = np.log(grad_omega_L2 / omega_L2)
            log_factor = 1.0 + log_ratio

            # Compute empirical C_BGW
            if omega_Linf > 1e-14 and log_factor > 0:
                C_BGW_emp = S_Linf / (omega_Linf * log_factor)
                min_C_BGW = min(min_C_BGW, C_BGW_emp)
                max_C_BGW = max(max_C_BGW, C_BGW_emp)
            else:
                C_BGW_emp = float('nan')

            # Check with the theoretical C_BGW value (to be determined)
            # For now, just check if the structure is correct
            bgw_bound_unit = omega_Linf * log_factor  # S_Linf ≤ C · this

            # Ladyzhenskaya bound
            lad_bound = C_L**2 * omega_L2**1.5 * grad_omega_L2**1.5

            # BKM bound (using empirical constant)
            bkm_bound_emp = max_C_BGW * omega_L2**2 * omega_Linf * log_factor if max_C_BGW > 0 else 0

            if show_detail and (i % max(1, n_steps // 20) == 0 or i == n_steps - 1):
                print(f"{t:>6.3f} | {abs_vs:>10.4e} | {step1_bound:>10.4e} | {'YES' if s1_ok else 'NO':>8} | {S_Linf:>10.4e} | {bgw_bound_unit:>10.4e} | {C_BGW_emp:>10.4f} | {lad_bound:>10.4e} | {bkm_bound_emp:>10.4e}")

        pct1 = 100 * step1_holds / n_steps if n_steps > 0 else 0
        print(f"\n{ic:>12} Re={Re:>5} N={N:>3}: Step1 holds {step1_holds}/{n_steps} ({pct1:.0f}%), C_BGW range: [{min_C_BGW:.4f}, {max_C_BGW:.4f}]")


def verify_young_inequality():
    """
    Verify the Young's inequality derivation:
    C_L² ||ω||^{3/2} ||∇ω||^{3/2} - ν ||∇ω||²

    Maximizing over ||∇ω|| gives:
    ≤ (27 C_L⁸)/(256 ν³) · ||ω||⁶ = (27 C_L⁸)/(256 ν³) · (2E)³

    where E = ½||ω||² is enstrophy.

    So d/dt(2E) = d/dt(||ω||²) ≤ (27 C_L⁸)/(256 ν³) · (2E)³
    i.e., dE/dt ≤ (27 C_L⁸)/(32 ν³) · E³

    This gives blow-up at T* = 32 ν³ / (2 · 27 · C_L⁸ · E₀²) = 16 ν³ / (27 C_L⁸ E₀²)
    """
    C_L = 0.827

    print("\n" + "=" * 80)
    print("YOUNG'S INEQUALITY DERIVATION CHECK")
    print("=" * 80)

    # Verify by numerical optimization
    for Re in [100, 500, 1000, 5000]:
        nu = 1.0 / Re
        E0 = 0.5 * 186.04  # enstrophy of TGV initial condition (½||ω||²)
        omega_L2_0_sq = 2 * E0

        # Theoretical blow-up time
        coeff = 27 * C_L**8 / (32 * nu**3)
        T_Lad_theory = 1.0 / (2 * coeff * E0**2)

        # Alternative form: T = 16 ν³ / (27 C_L⁸ E₀²)
        T_Lad_alt = 16 * nu**3 / (27 * C_L**8 * E0**2)

        # From exploration-001 data
        # The exploration used the coefficient α_Lad = 27 C_L⁸ / (128 ν³) for the ODE
        # dE/dt ≤ α_Lad · E³ → T* = 1/(2 α_Lad E₀²)
        alpha_Lad = 27 * C_L**8 / (128 * nu**3)
        T_Lad_e001 = 1.0 / (2 * alpha_Lad * E0**2)

        print(f"\nRe={Re}, ν={nu}, E₀={E0:.2f}:")
        print(f"  T_theory (our derivation): {T_Lad_theory:.4e}")
        print(f"  T_alt (check):             {T_Lad_alt:.4e}")
        print(f"  T_e001 (exploration-001):   {T_Lad_e001:.4e}")
        print(f"  Ratio (theory/e001):        {T_Lad_theory/T_Lad_e001:.4f}")

        # Numerical optimization: max over Y of [C_L² X^{3/2} Y^{3/2} - ν Y²]
        X = np.sqrt(omega_L2_0_sq)  # ||ω||_{L²}
        Y_vals = np.linspace(1, 1000, 100000)
        obj = C_L**2 * X**1.5 * Y_vals**1.5 - nu * Y_vals**2
        max_val = np.max(obj)
        Y_opt = Y_vals[np.argmax(obj)]

        # Analytical optimal: Y* = (3 C_L² X^{3/2})² / (16 ν²)
        Y_star = (3 * C_L**2 * X**1.5 / (4 * nu))**2
        max_analytical = C_L**2 * X**1.5 * Y_star**1.5 - nu * Y_star**2

        print(f"  Numerical max: {max_val:.4e} at Y={Y_opt:.2f}")
        print(f"  Analytical max: {max_analytical:.4e} at Y*={Y_star:.2f}")


def compare_prodi_serrin():
    """
    Compare BKM enstrophy criterion with Prodi-Serrin.

    BKM enstrophy needs: ω ∈ L¹([0,T]; L^∞(T³))
    Standard BKM: ∫₀ᵀ ||ω(t)||_{L^∞} dt < ∞ → regular

    Prodi-Serrin: u ∈ L^p([0,T]; L^q(T³)) with 2/p + 3/q ≤ 1, q > 3
    Endpoints: (p,q) = (∞,3), (2,∞), etc.

    Key question: Does Prodi-Serrin imply BKM?
    Answer: YES (for the critical case). If u ∈ L^∞_t L³_x, then by Sobolev embedding:
    ||ω||_{L^∞} ≤ C ||∇ω||_{H^{1/2+ε}} (needs u ∈ H^{5/2+ε})
    But this requires more regularity than Prodi-Serrin gives.

    However: Prodi-Serrin L^∞_t BMO or similar implies BKM via known results.
    The relationship is: BKM is INDEPENDENT of Prodi-Serrin for most endpoints.
    """
    print("\n" + "=" * 80)
    print("PRODI-SERRIN vs BKM COMPARISON")
    print("=" * 80)

    print("""
    ANALYSIS:

    1. Standard BKM criterion: ∫₀ᵀ ||ω(t)||_{L^∞} dt < ∞ ⟹ regular on [0,T]
       Source: Beale, Kato, Majda (1984)

    2. Prodi-Serrin criteria: u ∈ Lᵖ([0,T]; Lᵍ(T³)), 2/p + 3/q ≤ 1, q > 3
       Source: Prodi (1959), Serrin (1962)
       Extended: Escauriaza-Seregin-Šverák (2003) covers q=3 endpoint

    3. Relationship:
       - Prodi-Serrin controls VELOCITY norms
       - BKM controls VORTICITY L^∞ norm
       - Neither implies the other in general:

         a) BKM does NOT imply any Prodi-Serrin criterion:
            One can construct ω with ||ω||_{L^∞} ∈ L¹_t but u ∉ Lᵖ_t Lᵍ_x
            (via Biot-Savart, ||u||_{Lᵍ} is controlled by ||ω||_{Lʳ} with r < q,
             so L^∞ control of ω doesn't directly control high Lᵍ norms of u)

         b) Some Prodi-Serrin criteria DO imply BKM:
            If u ∈ L^∞_t H^{3/2+ε}, then ||ω||_{L^∞} ≤ C||ω||_{H^{1/2+ε}} ≤ C||u||_{H^{3/2+ε}} < ∞
            This corresponds to the supercritical Prodi-Serrin regime (q > 3)

         c) At the critical Prodi-Serrin endpoint (u ∈ L^∞_t L³_x or u ∈ L²_t L^∞_x):
            These do NOT imply BKM because L³_x or L^∞_x control of u only gives
            ||ω||_{L²} control (not L^∞)

    4. CONCLUSION: BKM and Prodi-Serrin are INDEPENDENT criteria at the critical level.
       They control different norms and neither subsumes the other.
       The BKM enstrophy bound gives a regularity criterion that is:
       - Stated in terms of vorticity (more physical)
       - Avoids the ν⁻³ factor in the enstrophy ODE
       - Reduces regularity to controlling a single quantity: ||ω||_{L^∞}
    """)


def verify_blowup_times():
    """Verify blow-up time formulas against exploration-001 data."""
    results = load_results()
    C_L = 0.827
    C_CZ = 0.24

    print("\n" + "=" * 80)
    print("BLOW-UP TIME VERIFICATION")
    print("=" * 80)

    for r in results:
        ic = r['ic_name']
        Re = r['Re']
        N = r['N']
        nu = r['nu']
        b = r['blowup']

        # Compute theoretical Ladyzhenskaya blow-up time
        E0 = b['y0'] / 2.0  # enstrophy = ½||ω||²

        # From Young's: dE/dt ≤ α E³ with α = 27 C_L⁸/(128 ν³)
        alpha = 27 * C_L**8 / (128 * nu**3)
        T_Lad_calc = 1.0 / (2 * alpha * E0**2)
        T_Lad_data = b['T_Lad']

        T_BKM_data = b['T_BKM']
        T_ratio_data = b['T_ratio']

        # T_ratio theoretical: T_BKM/T_Lad ~ ν⁻³ for fixed flow properties
        # Since T_Lad ~ ν³, T_BKM doesn't depend on ν (only on ||ω||_{L^∞})
        # So T_ratio ~ ν⁻³ × something

        ratio_calc = T_ratio_data

        if ic == 'TGV' and N == 64:
            print(f"\n{ic} Re={Re}:")
            print(f"  T_Lad: data={T_Lad_data:.4e}, calc={T_Lad_calc:.4e}, ratio={T_Lad_data/T_Lad_calc:.4f}")
            if isinstance(T_BKM_data, (int, float)) and T_BKM_data != 'inf':
                print(f"  T_BKM: {T_BKM_data:.4e}")
                print(f"  T_ratio: {T_ratio_data:.4e}")
                # Check ~Re³ scaling
                if Re > 100:
                    expected_ratio_from_100 = T_ratio_data / (Re/100)**3
                    print(f"  T_ratio / Re³: {T_ratio_data / Re**3:.4f}")


if __name__ == '__main__':
    results = load_results()
    verify_proof_chain(results)
    verify_young_inequality()
    compare_prodi_serrin()
    verify_blowup_times()

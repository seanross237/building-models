#!/usr/bin/env python3
"""
Detailed analysis of strain-vorticity alignment statistics from saved results.

Reads the JSON results from decomposition.py and produces:
1. Time evolution of alignment statistics
2. Eigenvalue statistics
3. Depletion factor analysis
4. Physical interpretation of the geometric factor
"""

import json
import numpy as np
from pathlib import Path


def load_results(re_value):
    """Load results from JSON file."""
    filepath = Path(__file__).parent / f'results_Re{re_value}.json'
    with open(filepath, 'r') as f:
        return json.load(f)


def analyze_alignment_evolution(results, re_label):
    """Print alignment statistics evolution over time."""
    print(f"\n{'='*90}")
    print(f"ALIGNMENT EVOLUTION: {re_label}")
    print(f"{'='*90}")

    print(f"\n{'t':>6s} {'⟨cos²θ₁⟩_ω':>12s} {'⟨cos²θ₂⟩_ω':>12s} {'⟨cos²θ₃⟩_ω':>12s} {'Depl.Factor':>12s} {'||∇ξ||':>10s} {'α_geom':>8s}")
    print("-" * 80)

    for r in results:
        if r['t'] < 0.01:
            continue  # skip t=0 (trivial)
        ca = r['cos2_enstrophy_avg']
        print(f"{r['t']:6.3f} {ca[0]:12.4f} {ca[1]:12.4f} {ca[2]:12.4f} "
              f"{r['depletion_factor']:12.4f} {r['xi_grad_L2']:10.2f} {r['alpha_geom']:8.2f}")


def analyze_eigenvalue_structure(results, re_label):
    """Analyze enstrophy-weighted eigenvalue statistics."""
    print(f"\n{'='*90}")
    print(f"EIGENVALUE STRUCTURE: {re_label}")
    print(f"{'='*90}")

    print(f"\n{'t':>6s} {'⟨λ₁⟩_ω':>10s} {'⟨λ₂⟩_ω':>10s} {'⟨λ₃⟩_ω':>10s} {'λ₂/λ₁':>8s} {'λ₃/λ₁':>8s} {'trace':>10s}")
    print("-" * 70)

    for r in results:
        if r['t'] < 0.01:
            continue
        la = r['lambda_avg']
        ratio_21 = la[1] / la[0] if abs(la[0]) > 1e-15 else 0
        ratio_31 = la[2] / la[0] if abs(la[0]) > 1e-15 else 0
        trace = la[0] + la[1] + la[2]
        print(f"{r['t']:6.3f} {la[0]:10.4f} {la[1]:10.4f} {la[2]:10.4f} "
              f"{ratio_21:8.4f} {ratio_31:8.4f} {trace:10.2e}")


def explain_geometric_factor(results, re_label):
    """
    Physical explanation of why α_geom has its observed value.

    The geometric factor α_geom = VS_Hölder / VS_actual
    = (||S||_{L²} × ||ω||²_{L⁴}) / |∫ S_{ij}ω_iω_j dx|

    This ratio measures how much Hölder's inequality overestimates the integral.
    Hölder treats S and ωω as arbitrary L² and L¹ functions that could be
    perfectly aligned everywhere. In reality:

    1. Vorticity preferentially aligns with certain strain eigenvectors
    2. The sign structure of Sωω varies in space (cancellation)
    3. High-|ω| regions may not coincide with high-|S| regions

    The depletion factor gives a complementary view:
    depl = ∫(λ₁cos²θ₁ + λ₂cos²θ₂ + λ₃cos²θ₃)|ω|²dx / ∫λ₁|ω|²dx

    If depl < 1, vorticity is partially shielded from maximum stretching.
    """
    print(f"\n{'='*90}")
    print(f"GEOMETRIC FACTOR ANALYSIS: {re_label}")
    print(f"{'='*90}")

    # Find the 237× slack point
    min_idx = min(range(len(results)), key=lambda i: abs(results[i].get('total_slack', float('inf')) - 237))
    r = results[min_idx]

    if r['t'] < 0.01:
        # Fall back to peak enstrophy
        min_idx = max(range(len(results)), key=lambda i: results[i]['enstrophy'])
        r = results[min_idx]

    print(f"\nAt t={r['t']:.4f} (total slack ≈ {r.get('total_slack', 'N/A'):.1f}):")
    print(f"  α_geom = {r['alpha_geom']:.4f}")
    print(f"  Depletion factor = {r['depletion_factor']:.4f}")

    ca = r['cos2_enstrophy_avg']
    la = r['lambda_avg']

    print(f"\n  Enstrophy-weighted alignment:")
    print(f"    ⟨cos²θ₁⟩_ω = {ca[0]:.4f}  (extensional, λ₁ = {la[0]:+.4f})")
    print(f"    ⟨cos²θ₂⟩_ω = {ca[1]:.4f}  (intermediate, λ₂ = {la[1]:+.4f})")
    print(f"    ⟨cos²θ₃⟩_ω = {ca[2]:.4f}  (compressive, λ₃ = {la[2]:+.4f})")
    print(f"    Sum = {ca[0]+ca[1]+ca[2]:.4f} (should be 1.0)")

    print(f"\n  Physical interpretation:")
    print(f"    Isotropic expectation: cos²θ_i = 1/3 = 0.3333 for each")
    print(f"    Departure from isotropy:")
    for i, name in enumerate(['extensional', 'intermediate', 'compressive']):
        dep = ca[i] - 1/3
        print(f"      {name}: {dep:+.4f} ({dep/(1/3)*100:+.1f}% relative)")

    # Effective stretching rate
    # In the isotropic case: VS ~ ⟨λ_1/3 + λ_2/3 + λ_3/3⟩ |ω|² = 0 (by trace-free)
    # Actual: VS ~ ⟨λ_1 cos²θ_1 + λ_2 cos²θ_2 + λ_3 cos²θ_3⟩ |ω|²
    eff_rate = la[0] * ca[0] + la[1] * ca[1] + la[2] * ca[2]
    max_rate = la[0]  # worst case: all aligned with λ₁
    iso_rate = (la[0] + la[1] + la[2]) / 3  # isotropic (should be ~0)

    print(f"\n  Effective stretching rate decomposition:")
    print(f"    Σ λ_i ⟨cos²θ_i⟩ = {eff_rate:.4f}")
    print(f"    Maximum possible (all aligned with λ₁): {max_rate:.4f}")
    print(f"    Isotropic (trace/3): {iso_rate:.6f} ≈ 0")
    print(f"    Ratio actual/max = depletion factor = {eff_rate/max_rate:.4f}" if max_rate > 1e-15 else "")

    # Why α_geom ≈ 5:
    # The Hölder bound ||S||_{L²}||ω||²_{L⁴} treats S and ωω as independent
    # But S_{ij}ω_iω_j = |ω|² (λ₁cos²θ₁ + λ₂cos²θ₂ + λ₃cos²θ₃)
    # The worst case for Hölder would have |ω|² concentrated where S is largest
    # and the alignment maximized. The actual flow has:
    # (a) Partial cancellation from the sign structure (λ₃ < 0 contributes negatively)
    # (b) Correlation structure: |ω| and |S| are correlated but not perfectly
    # (c) The alignment is not worst-case

    # Decompose the geometric factor further
    # α_geom = (||S||_{L²} × ||ω||²_{L⁴}) / |∫ Sωω dx|
    # = (||S||_{L²} × ||ω||²_{L⁴}) / |∫ |ω|²(λ₁c₁ + λ₂c₂ + λ₃c₃) dx|
    # ≤ (||S||_{L²} × ||ω||²_{L⁴}) / (∫ |ω|² |λ₁c₁ + λ₂c₂ + λ₃c₃| dx)  [if no cancellation]
    # The Hölder bound is Cauchy-Schwarz on ∫ (Σ S_{ij})(ω_iω_j) dx

    print(f"\n  Sources of geometric slack (α_geom = {r['alpha_geom']:.2f}):")
    print(f"    1. Sign structure: λ₃ < 0 means compressive alignment REDUCES stretching")
    print(f"       Fraction of VS from compressive: λ₃⟨cos²θ₃⟩ = {la[2]*ca[2]:.4f}")
    print(f"       This partially cancels extensional: λ₁⟨cos²θ₁⟩ = {la[0]*ca[0]:.4f}")
    cancellation_ratio = abs(la[2]*ca[2]) / (la[0]*ca[0]) if la[0]*ca[0] > 1e-15 else 0
    print(f"       Cancellation ratio: {cancellation_ratio:.2f} (1.0 = complete cancellation)")
    print(f"    2. Depletion: vorticity not fully aligned with max strain")
    print(f"       Depletion factor = {r['depletion_factor']:.4f}")
    print(f"    3. Cauchy-Schwarz loss: |S| and |ω|² not colocated")
    # This is harder to compute directly — it's the remaining factor


def print_histogram_summary(results, re_label):
    """Print summary of alignment PDFs at peak enstrophy."""
    # Find peak enstrophy
    peak_idx = max(range(len(results)), key=lambda i: results[i]['enstrophy'])
    r = results[peak_idx]

    print(f"\n{'='*90}")
    print(f"ALIGNMENT PDF SUMMARY at peak enstrophy (t={r['t']:.4f}): {re_label}")
    print(f"{'='*90}")

    for name in ['extensional', 'intermediate', 'compressive']:
        hist = r['hist_data'][name]
        centers = np.array(hist['centers'])
        density = np.array(hist['density'])

        # Find mode
        mode_idx = np.argmax(density)
        mode_val = centers[mode_idx]

        # Compute median from CDF
        cumsum = np.cumsum(density) * (centers[1] - centers[0])
        median_idx = np.searchsorted(cumsum / cumsum[-1], 0.5)
        median_val = centers[min(median_idx, len(centers)-1)]

        # Fraction with cos²θ > 0.5 (strongly aligned)
        strong_mask = centers > 0.5
        frac_strong = np.sum(density[strong_mask]) * (centers[1] - centers[0])

        print(f"\n  cos²θ_{name[0]}:")
        print(f"    Mode = {mode_val:.3f}, Median = {median_val:.3f}")
        print(f"    P(cos²θ > 0.5) = {frac_strong:.3f}")

        # Print ASCII histogram
        max_d = max(density) if max(density) > 0 else 1
        n_bars = 20
        step = len(centers) // n_bars
        print(f"    PDF: ", end='')
        for k in range(0, len(centers), step):
            bar_len = int(density[k] / max_d * 30)
            print(f"\n      [{centers[k]:.2f}] {'█' * bar_len}", end='')
        print()


if __name__ == '__main__':
    for re_val, re_label in [(100, "Re=100"), (1000, "Re=1000")]:
        results = load_results(re_val)

        analyze_alignment_evolution(results, re_label)
        analyze_eigenvalue_structure(results, re_label)
        explain_geometric_factor(results, re_label)
        print_histogram_summary(results, re_label)

    # Cross-Re comparison at the 237× point
    print(f"\n{'='*90}")
    print("CROSS-RE COMPARISON at total slack ≈ 237")
    print(f"{'='*90}")

    for re_val, re_label in [(100, "Re=100"), (1000, "Re=1000")]:
        results = load_results(re_val)
        min_idx = min(range(len(results)), key=lambda i: abs(results[i].get('total_slack', float('inf')) - 237))
        r = results[min_idx]
        if r['t'] < 0.01:
            continue
        ca = r['cos2_enstrophy_avg']
        la = r['lambda_avg']
        print(f"\n  {re_label} at t={r['t']:.3f}:")
        print(f"    α_geom={r['alpha_geom']:.2f}, α_Lad={r['alpha_Lad']:.2f}")
        print(f"    ⟨cos²θ₁⟩_ω={ca[0]:.4f}, ⟨cos²θ₂⟩_ω={ca[1]:.4f}, ⟨cos²θ₃⟩_ω={ca[2]:.4f}")
        print(f"    ⟨λ₁⟩_ω={la[0]:.4f}, ⟨λ₂⟩_ω={la[1]:.4f}, ⟨λ₃⟩_ω={la[2]:.4f}")
        print(f"    Depletion = {r['depletion_factor']:.4f}")
        print(f"    ||∇ξ||_L² = {r['xi_grad_L2']:.2f}")

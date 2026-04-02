#!/usr/bin/env python3
"""
Part C: Littlewood-Paley decomposition analysis.

Decompose f = Σ_j Δ_j f where Δ_j localizes to |k| ~ 2^j.
Compute:
1. Diagonal contribution: Σ_j ||Δ_j f||⁴_{L⁴}
2. Cross-term contributions
3. Which terms dominate for Kolmogorov spectra?
"""

import numpy as np
from numpy.fft import fftn, ifftn, fftfreq
import json

def setup_grid(N):
    k = fftfreq(N, d=1.0/N)
    KX, KY, KZ = np.meshgrid(k, k, k, indexing='ij')
    K2 = KX**2 + KY**2 + KZ**2
    K_mag = np.sqrt(K2)
    return KX, KY, KZ, K2, K_mag


def dyadic_decomposition(f_hat, K_mag, N, j_max=None):
    """
    Littlewood-Paley decomposition: Δ_j f has Fourier support in 2^{j-1} ≤ |k| < 2^j.
    (Using sharp cutoffs for simplicity; smooth cutoffs give equivalent bounds.)

    Returns list of (j, Δ_j f_hat) pairs.
    """
    if j_max is None:
        j_max = int(np.ceil(np.log2(N/2)))

    pieces = []
    for j in range(0, j_max+1):
        if j == 0:
            # Low-frequency piece: |k| < 1
            mask = K_mag < 1
        else:
            mask = (K_mag >= 2**(j-1)) & (K_mag < 2**j)

        dj_hat = f_hat * mask
        if np.any(mask):
            pieces.append((j, dj_hat))

    return pieces


def compute_LP_analysis(N, alpha, n_samples=200, k_max_factor=0.4):
    """
    For power-law spectrum |f̂_k| ~ k^{-α}, decompose into LP pieces and compute:
    1. ||Δ_j f||⁴_{L⁴} for each j (diagonal)
    2. Cross terms: ∫(Δ_i f)²(Δ_j f)² for i≠j
    3. Verify: ||f||⁴_{L⁴} = diagonal + cross terms
    """
    KX, KY, KZ, K2, K_mag = setup_grid(N)

    k_max = int(k_max_factor * N)
    active_mask = (K_mag >= 1) & (K_mag <= k_max)

    # Build positive-half indices (for reality)
    indices = np.where(active_mask.ravel())[0]
    pos_indices = []
    for idx in indices:
        ix, iy, iz = np.unravel_index(idx, (N, N, N))
        kx = KX[ix, iy, iz]
        ky = KY[ix, iy, iz]
        kz = KZ[ix, iy, iz]
        if kx > 0 or (kx == 0 and ky > 0) or (kx == 0 and ky == 0 and kz > 0):
            pos_indices.append(idx)
    pos_indices = np.array(pos_indices)

    K_mag_flat = K_mag.ravel()
    amplitudes = K_mag_flat[pos_indices] ** (-alpha)

    results_all = []

    for sample in range(n_samples):
        # Random phases
        phases = np.random.uniform(0, 2*np.pi, len(pos_indices))

        # Build real field
        f_hat = np.zeros((N, N, N), dtype=complex)
        for i, idx in enumerate(pos_indices):
            ix, iy, iz = np.unravel_index(idx, (N, N, N))
            jx, jy, jz = (-ix) % N, (-iy) % N, (-iz) % N
            c = amplitudes[i] * np.exp(1j * phases[i])
            f_hat[ix, iy, iz] = c
            f_hat[jx, jy, jz] = np.conj(c)

        # Normalize
        F_k = N**3 * f_hat
        f_phys = ifftn(F_k).real
        f_L2_sq = np.mean(f_phys**2)
        f_hat /= np.sqrt(f_L2_sq)
        F_k = N**3 * f_hat
        f_phys = ifftn(F_k).real

        # Full L⁴ norm
        L4_full = np.mean(f_phys**4)

        # LP decomposition
        pieces = dyadic_decomposition(f_hat, K_mag, N)

        # Physical-space pieces
        piece_phys = []
        for j, dj_hat in pieces:
            Fj = N**3 * dj_hat
            dj_phys = ifftn(Fj).real
            piece_phys.append((j, dj_phys))

        # Diagonal: Σ_j ||Δ_j f||⁴_{L⁴}
        diagonal = 0.0
        band_L4 = {}
        band_L2 = {}
        for j, dj_phys in piece_phys:
            L4j = np.mean(dj_phys**4)
            L2j = np.mean(dj_phys**2)
            diagonal += L4j
            band_L4[j] = L4j
            band_L2[j] = L2j

        # Cross terms: the full ||f||⁴_{L⁴} = Σ_{i,j,k,l} ∫Δ_i Δ_j Δ_k Δ_l
        # More practically: ||f||⁴ = ∫f⁴ = ∫(Σ Δ_j f)⁴
        # = Σ_j ∫(Δ_j f)⁴ + (cross terms of various orders)
        #
        # The main cross terms are the "pairwise" type: 6 Σ_{i<j} ∫(Δ_i f)²(Δ_j f)²
        # (from the multinomial expansion of (Σ_j x_j)⁴)
        #
        # Actually: (x₁+x₂+...)⁴ = Σ x_j⁴ + 6 Σ_{i<j} x_i² x_j² + 4 Σ_{i≠j} x_i³ x_j + ...
        # The ∫ of these products depends on whether the modes interact.

        pairwise = 0.0
        for a in range(len(piece_phys)):
            for b in range(a+1, len(piece_phys)):
                _, da = piece_phys[a]
                _, db = piece_phys[b]
                pairwise += 6 * np.mean(da**2 * db**2)

        # Triple and higher-order cross terms
        cross_higher = L4_full - diagonal - pairwise

        results_all.append({
            'L4_full': L4_full,
            'diagonal': diagonal,
            'pairwise': pairwise,
            'cross_higher': cross_higher,
            'band_L4': band_L4,
            'band_L2': band_L2,
        })

    # Average
    avg = {
        'L4_full': np.mean([r['L4_full'] for r in results_all]),
        'diagonal': np.mean([r['diagonal'] for r in results_all]),
        'pairwise': np.mean([r['pairwise'] for r in results_all]),
        'cross_higher': np.mean([r['cross_higher'] for r in results_all]),
    }
    avg['diag_frac'] = avg['diagonal'] / avg['L4_full']
    avg['pair_frac'] = avg['pairwise'] / avg['L4_full']
    avg['higher_frac'] = avg['cross_higher'] / avg['L4_full']

    # Band-by-band averages
    all_j = sorted(set(j for r in results_all for j in r['band_L4']))
    avg['band_L4'] = {j: np.mean([r['band_L4'].get(j, 0) for r in results_all]) for j in all_j}
    avg['band_L2'] = {j: np.mean([r['band_L2'].get(j, 0) for r in results_all]) for j in all_j}

    return avg


def main():
    N = 32

    print("="*70)
    print("LITTLEWOOD-PALEY DECOMPOSITION ANALYSIS")
    print("="*70)

    # Kolmogorov spectrum: α = 11/6
    print("\n--- α = 11/6 (Kolmogorov) ---")
    res_kolm = compute_LP_analysis(N, 11.0/6.0, n_samples=300)
    print(f"  ||f||⁴_{{L⁴}} = {res_kolm['L4_full']:.6f}")
    print(f"  Diagonal:       {res_kolm['diagonal']:.6f} ({res_kolm['diag_frac']*100:.1f}%)")
    print(f"  Pairwise cross: {res_kolm['pairwise']:.6f} ({res_kolm['pair_frac']*100:.1f}%)")
    print(f"  Higher cross:   {res_kolm['cross_higher']:.6f} ({res_kolm['higher_frac']*100:.1f}%)")

    print("\n  Band contributions to ||f||⁴_{L⁴} (diagonal):")
    for j in sorted(res_kolm['band_L4'].keys()):
        L4j = res_kolm['band_L4'][j]
        L2j = res_kolm['band_L2'][j]
        if L2j > 1e-15:
            # Kurtosis of this band: <Δ_j f⁴> / <Δ_j f²>² ≈ 3 if Gaussian
            kurt = L4j / max(L2j**2, 1e-30)
            print(f"    j={j}: ||Δ_j f||⁴_4 = {L4j:.2e}, ||Δ_j f||²_2 = {L2j:.2e}, "
                  f"kurtosis = {kurt:.2f} (Gaussian=3)")

    # α = 5/6 (GOAL convention)
    print("\n--- α = 5/6 ---")
    res_56 = compute_LP_analysis(N, 5.0/6.0, n_samples=200)
    print(f"  ||f||⁴ = {res_56['L4_full']:.6f}")
    print(f"  Diagonal: {res_56['diag_frac']*100:.1f}%, Pairwise: {res_56['pair_frac']*100:.1f}%, "
          f"Higher: {res_56['higher_frac']*100:.1f}%")

    # α = 3/2
    print("\n--- α = 3/2 ---")
    res_32 = compute_LP_analysis(N, 3.0/2.0, n_samples=200)
    print(f"  ||f||⁴ = {res_32['L4_full']:.6f}")
    print(f"  Diagonal: {res_32['diag_frac']*100:.1f}%, Pairwise: {res_32['pair_frac']*100:.1f}%, "
          f"Higher: {res_32['higher_frac']*100:.1f}%")

    # Flat spectrum
    print("\n--- α = 0 (flat spectrum) ---")
    res_flat = compute_LP_analysis(N, 0.0, n_samples=200)
    print(f"  ||f||⁴ = {res_flat['L4_full']:.6f}")
    print(f"  Diagonal: {res_flat['diag_frac']*100:.1f}%, Pairwise: {res_flat['pair_frac']*100:.1f}%, "
          f"Higher: {res_flat['higher_frac']*100:.1f}%")

    # Analysis
    print("\n" + "="*70)
    print("ANALYSIS")
    print("="*70)
    print()
    print("For a Gaussian random field with independent LP bands,")
    print("E[f⁴] = 3(E[f²])² = 3(Σ E[Δ_j f²])²")
    print("while diagonal = Σ 3(E[Δ_j f²])² (if each band is Gaussian)")
    print("So diagonal/total = (Σ σ_j⁴) / (Σ σ_j²)²")
    print("where σ_j² = ||Δ_j f||²_2")
    print()
    print("If one band dominates (e.g., j=0), then diagonal ≈ total ≈ 3σ₀⁴.")
    print("If many bands contribute equally, diagonal << total")
    print("  (N bands of equal σ: diagonal = N×3σ⁴ = 3σ²_tot/N, ")
    print("   total = 3(Nσ²)² = 3N²σ⁴, ratio = 1/N)")
    print()

    for name, res in [("Kolmogorov", res_kolm), ("α=5/6", res_56), ("α=3/2", res_32), ("flat", res_flat)]:
        sigma_sq = sorted(res['band_L2'].items())
        total_var = sum(v for _, v in sigma_sq)
        hhi = sum(v**2 for _, v in sigma_sq) / total_var**2 if total_var > 0 else 0
        print(f"  {name}: HHI (spectral concentration) = {hhi:.4f}, "
              f"effective # bands = {1/hhi:.1f}")

    print()
    print("For Kolmogorov spectrum, most L² energy is in the lowest band.")
    print("=> Diagonal term dominates => LP decomposition does NOT improve the bound.")
    print("This is because ||f||_{L⁴} ≈ 3^{1/4} ||f||_{L²} ≈ 3^{1/4} ||Δ_0 f||_{L²}")
    print("and the improvement needs to come from ||∇f|| >> ||f||, not from LP splitting.")


if __name__ == '__main__':
    main()

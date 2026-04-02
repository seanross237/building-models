"""
Complex Arithmetic Matrices — GUE Screening
Exploration 001, Strategy 002, Riemann Hypothesis

Tests 6 complex Hermitian matrix constructions:
- GUE random control (theoretical baseline)
- C1: Random phase Mangoldt Hankel
- C2a: Dirichlet χ₄ phases
- C2b: Dirichlet χ₈ phases
- C3a: Gauss sum phases (p=97)
- C3b: Gauss sum phases (p=997)
- C4: Zeta-value phases

For each: computes level repulsion exponent β, NN spacing distribution,
chi² vs GUE/GOE Wigner surmises.
"""

import numpy as np
from scipy.linalg import eigh
from scipy.optimize import curve_fit
from scipy.stats import chi2
import json
import sys

# ─── Von Mangoldt function ────────────────────────────────────────────────────

def von_mangoldt(n):
    """Λ(n): log p if n = p^k, else 0."""
    if n < 2:
        return 0.0
    # trial division
    temp = n
    for p in range(2, int(n**0.5) + 1):
        if temp % p == 0:
            log_p = np.log(p)
            while temp % p == 0:
                temp //= p
            if temp == 1:
                return log_p  # n is a prime power
            else:
                return 0.0
    # n itself is prime
    return np.log(n)

# Precompute Von Mangoldt values up to 2*N
def precompute_mangoldt(max_n):
    vals = np.zeros(max_n + 1)
    for n in range(2, max_n + 1):
        vals[n] = von_mangoldt(n)
    return vals

# ─── Unfolding ────────────────────────────────────────────────────────────────

def unfold_eigenvalues(evals):
    """Unfold eigenvalues using smooth cumulative density (polynomial fit)."""
    n = len(evals)
    evals_sorted = np.sort(evals)
    # Empirical cumulative distribution
    cum = np.arange(1, n + 1, dtype=float)
    # Fit smooth polynomial to get N(E)
    # Use degree-15 polynomial (Chebyshev basis for stability)
    x_norm = (evals_sorted - evals_sorted.mean()) / (evals_sorted.std() + 1e-10)
    try:
        poly_coeffs = np.polyfit(x_norm, cum, deg=15)
        smooth_cum = np.polyval(poly_coeffs, x_norm)
    except Exception:
        smooth_cum = cum  # fallback: no unfolding
    return smooth_cum

def compute_spacings(evals):
    """Compute nearest-neighbor spacings after unfolding."""
    unfolded = unfold_eigenvalues(evals)
    spacings = np.diff(unfolded)
    # Normalize so mean spacing = 1
    spacings = spacings / spacings.mean()
    return spacings[spacings > 0]  # remove any zero or negative spacings

# ─── Statistics ───────────────────────────────────────────────────────────────

def wigner_gue(s):
    """GUE Wigner surmise: P(s) = (32/π²) s² exp(-4s²/π)"""
    return (32.0 / np.pi**2) * s**2 * np.exp(-4.0 * s**2 / np.pi)

def wigner_goe(s):
    """GOE Wigner surmise: P(s) = (π/2) s exp(-πs²/4)"""
    return (np.pi / 2.0) * s * np.exp(-np.pi * s**2 / 4.0)

def level_repulsion_model(s, beta, B):
    """P(s) ~ s^β exp(-B s²), unnormalized fit."""
    return s**beta * np.exp(-B * s**2)

def fit_beta(spacings, s_max=0.5):
    """Fit level repulsion exponent β from small-s regime."""
    # Histogram with fine bins for small-s
    bins = np.linspace(0, s_max, 20)
    hist, edges = np.histogram(spacings, bins=bins, density=True)
    centers = (edges[:-1] + edges[1:]) / 2
    mask = hist > 0
    if mask.sum() < 4:
        return np.nan, np.nan
    try:
        popt, pcov = curve_fit(
            level_repulsion_model,
            centers[mask], hist[mask],
            p0=[1.0, 1.0],
            bounds=([0, 0.01], [5, 20]),
            maxfev=5000
        )
        beta_err = np.sqrt(np.diag(pcov))[0] if pcov is not None else np.nan
        return popt[0], beta_err
    except Exception as e:
        return np.nan, np.nan

def compute_chi2_vs_wigner(spacings, wigner_func, n_bins=30):
    """Compute chi² of spacings vs a Wigner surmise."""
    s_max = 4.0
    bins = np.linspace(0, s_max, n_bins + 1)
    observed, edges = np.histogram(spacings, bins=bins, density=False)
    centers = (edges[:-1] + edges[1:]) / 2
    bin_width = bins[1] - bins[0]
    expected = wigner_func(centers) * bin_width * len(spacings)
    # Avoid division by zero
    mask = expected > 0.5
    if mask.sum() < 5:
        return np.nan
    chi2_val = np.sum((observed[mask] - expected[mask])**2 / expected[mask])
    return chi2_val / mask.sum()  # reduced chi²

def analyze_construction(evals_list, name):
    """
    Full analysis of a construction given a list of eigenvalue arrays.
    Returns dict with β, chi²_GUE, chi²_GOE.
    """
    all_spacings = []
    for evals in evals_list:
        sp = compute_spacings(evals)
        all_spacings.append(sp)
    spacings = np.concatenate(all_spacings)

    beta, beta_err = fit_beta(spacings, s_max=0.5)
    chi2_gue = compute_chi2_vs_wigner(spacings, wigner_gue)
    chi2_goe = compute_chi2_vs_wigner(spacings, wigner_goe)

    gue_better = (chi2_gue < chi2_goe) if (not np.isnan(chi2_gue) and not np.isnan(chi2_goe)) else None

    result = {
        'name': name,
        'N_matrices': len(evals_list),
        'N': len(evals_list[0]),
        'n_spacings': len(spacings),
        'beta': float(beta) if not np.isnan(beta) else None,
        'beta_err': float(beta_err) if not np.isnan(beta_err) else None,
        'chi2_gue': float(chi2_gue) if not np.isnan(chi2_gue) else None,
        'chi2_goe': float(chi2_goe) if not np.isnan(chi2_goe) else None,
        'gue_better': bool(gue_better) if gue_better is not None else None,
    }
    return result, spacings

# ─── Matrix Builders ──────────────────────────────────────────────────────────

def build_gue_random(N, rng):
    """True GUE random matrix: H = (A + A†)/2, A_{jk} ~ CN(0,1)."""
    A = (rng.standard_normal((N, N)) + 1j * rng.standard_normal((N, N))) / np.sqrt(2)
    H = (A + A.conj().T) / 2
    return H

def build_c1_random_phase(N, mangoldt_vals, rng):
    """C1: H_{jk} = Λ(|j-k|+1) × exp(2πi φ_{jk}), φ_{jk} random, φ_{kj}=φ_{jk}*."""
    H = np.zeros((N, N), dtype=complex)
    for i in range(N):
        for j in range(i, N):
            diff = abs(i - j)
            amp = mangoldt_vals[diff + 1]
            if i == j:
                H[i, j] = amp  # real diagonal
            else:
                phase = rng.uniform(0, 2 * np.pi)
                H[i, j] = amp * np.exp(1j * phase)
                H[j, i] = amp * np.exp(-1j * phase)
    return H

def dirichlet_char_q4(n):
    """Dirichlet character mod 4: χ₄(1)=1, χ₄(3)=-1, χ₄(even)=0."""
    n_mod = n % 4
    if n_mod == 1:
        return 1.0 + 0j
    elif n_mod == 3:
        return -1.0 + 0j
    else:
        return 0.0 + 0j

def dirichlet_char_q8(n):
    """Dirichlet character mod 8: χ₈(1)=1, χ₈(3)=1, χ₈(5)=-1, χ₈(7)=-1, even=0."""
    n_mod = n % 8
    vals = {1: 1, 3: 1, 5: -1, 7: -1}
    return complex(vals.get(n_mod, 0))

def build_c2_dirichlet(N, mangoldt_vals, char_func):
    """C2: H_{jk} = Λ(|j-k|+1) × χ(j-k)/|χ(j-k)|. Off-diag only where χ≠0."""
    H = np.zeros((N, N), dtype=complex)
    for i in range(N):
        for j in range(N):
            diff = i - j  # signed difference for character argument
            amp = mangoldt_vals[abs(diff) + 1]
            if i == j:
                H[i, j] = amp  # diagonal: real
            else:
                chi_val = char_func(diff)
                if abs(chi_val) > 1e-10:
                    phase = chi_val / abs(chi_val)
                    H[i, j] = amp * phase
                else:
                    H[i, j] = 0.0
    # Force Hermitian: H = (H + H†)/2
    H = (H + H.conj().T) / 2
    return H

def build_c3_gauss(N, mangoldt_vals, p):
    """C3: H_{jk} = Λ(|j-k|+1) × exp(2πi × (j·k mod p) / p)."""
    H = np.zeros((N, N), dtype=complex)
    # 1-indexed: j, k go from 1 to N
    for i in range(N):
        for j in range(N):
            diff = abs(i - j)
            amp = mangoldt_vals[diff + 1]
            if i == j:
                H[i, j] = amp  # diagonal real
            else:
                # Use 1-indexed positions
                phase = 2 * np.pi * ((i + 1) * (j + 1) % p) / p
                H[i, j] = amp * np.exp(1j * phase)
    # Force Hermitian
    H = (H + H.conj().T) / 2
    return H

def zeta_on_critical_line(t_vals, N_terms=100):
    """
    Compute Im(ζ(1/2 + it)) via partial Euler sum.
    ζ(s) ≈ Σ_{n=1}^{N_terms} n^{-s}
    """
    results = []
    for t in t_vals:
        s = 0.5 + 1j * t
        zeta_val = sum(n**(-s) for n in range(1, N_terms + 1))
        results.append(np.imag(zeta_val))
    return np.array(results)

def build_c4_zeta_phases(N, mangoldt_vals):
    """C4: H_{jk} = Λ(|j-k|+1) × exp(2πi × Im(ζ(1/2 + i(j-k))))."""
    # Precompute Im(ζ) for t = 0, 1, ..., N-1
    print(f"  Computing zeta values for C4 (N={N})...")
    t_vals = np.arange(0, N, dtype=float)
    # Use mpmath for better precision
    try:
        import mpmath
        mpmath.mp.dps = 15
        zeta_imag = np.array([float(mpmath.im(mpmath.zeta(0.5 + 1j * float(t))))
                               for t in t_vals])
    except ImportError:
        zeta_imag = zeta_on_critical_line(t_vals, N_terms=50)

    H = np.zeros((N, N), dtype=complex)
    for i in range(N):
        for j in range(N):
            diff = abs(i - j)
            amp = mangoldt_vals[diff + 1]
            if i == j:
                H[i, j] = amp
            else:
                zeta_im = zeta_imag[diff]
                phase = 2 * np.pi * zeta_im
                H[i, j] = amp * np.exp(1j * phase)
    # Force Hermitian
    H = (H + H.conj().T) / 2
    return H

# ─── Vectorized builders (faster) ────────────────────────────────────────────

def build_c1_random_phase_fast(N, mangoldt_vals, rng):
    """Vectorized C1 builder."""
    i_idx, j_idx = np.meshgrid(np.arange(N), np.arange(N), indexing='ij')
    diff = np.abs(i_idx - j_idx)
    amp = mangoldt_vals[diff + 1]

    # Random phases — only upper triangle, then mirror
    phases = np.zeros((N, N))
    upper = np.triu(np.ones((N, N), dtype=bool), k=1)
    phases[upper] = rng.uniform(0, 2 * np.pi, size=upper.sum())
    phases = phases - phases.T  # antisymmetric phase (so H_{ij} = conj(H_{ji}))

    H = amp * np.exp(1j * phases)
    # Force diagonal to be real
    np.fill_diagonal(H, np.real(np.diag(H)))
    # Force Hermitian
    H = (H + H.conj().T) / 2
    return H

def build_c2_dirichlet_fast(N, mangoldt_vals, char_array):
    """Vectorized C2 builder. char_array[d] = χ(d) for d in range(N)."""
    i_idx, j_idx = np.meshgrid(np.arange(N), np.arange(N), indexing='ij')
    # Signed difference for character
    signed_diff = i_idx - j_idx  # range [-(N-1), N-1]
    diff = np.abs(i_idx - j_idx)
    amp = mangoldt_vals[diff + 1]

    # Map signed diff to char values (handle negative indices)
    # char_array is defined for d = 0..N-1; use modular property
    chi_vals = np.array([char_array[int(d) % len(char_array)] for d in signed_diff.flatten()]).reshape(N, N)

    # Phase: chi / |chi| where chi != 0
    mag = np.abs(chi_vals)
    phase = np.where(mag > 1e-10, chi_vals / mag, 0.0)

    H = amp * phase
    np.fill_diagonal(H, mangoldt_vals[1])  # Λ(1)=0, but set real diagonal
    H = (H + H.conj().T) / 2
    return H

def build_c3_gauss_fast(N, mangoldt_vals, p):
    """Vectorized C3 builder."""
    i_idx, j_idx = np.meshgrid(np.arange(N), np.arange(N), indexing='ij')
    diff = np.abs(i_idx - j_idx)
    amp = mangoldt_vals[diff + 1]

    # Gauss phases: exp(2πi jk/p) using 1-indexed
    jk_mod_p = ((i_idx + 1) * (j_idx + 1)) % p
    phases = 2 * np.pi * jk_mod_p / p

    H = amp * np.exp(1j * phases)
    np.fill_diagonal(H, np.real(np.diag(H)))
    H = (H + H.conj().T) / 2
    return H

def build_c4_zeta_fast(N, mangoldt_vals):
    """Vectorized C4 builder."""
    print(f"  Computing zeta values for C4 (N={N}, t=0..{N-1})...")
    try:
        import mpmath
        mpmath.mp.dps = 15
        # Only need t = 0, 1, ..., N-1
        zeta_imag = np.zeros(N)
        for d in range(N):
            if d % 50 == 0:
                print(f"    t={d}/{N}...")
            zeta_imag[d] = float(mpmath.im(mpmath.zeta(0.5 + 1j * float(d))))
    except Exception as e:
        print(f"  mpmath failed ({e}), using partial sum")
        zeta_imag = np.array([np.imag(sum(n**(-0.5 - 1j * float(d))
                              for n in range(1, 51))) for d in range(N)])

    i_idx, j_idx = np.meshgrid(np.arange(N), np.arange(N), indexing='ij')
    diff = np.abs(i_idx - j_idx)
    amp = mangoldt_vals[diff + 1]

    phases = 2 * np.pi * zeta_imag[diff]
    H = amp * np.exp(1j * phases)
    np.fill_diagonal(H, np.real(np.diag(H)))
    H = (H + H.conj().T) / 2
    return H

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    N = 500
    N_MATRICES = 3  # Average over 3 matrices per construction to reduce noise
    rng = np.random.default_rng(42)

    print(f"Precomputing Von Mangoldt values up to {2*N}...")
    mangoldt_vals = precompute_mangoldt(2 * N)
    print(f"  Λ(2)={mangoldt_vals[2]:.4f}, Λ(4)={mangoldt_vals[4]:.4f}, "
          f"Λ(6)={mangoldt_vals[6]:.4f}, Λ(8)={mangoldt_vals[8]:.4f}")

    results = []

    # ── GUE control ──────────────────────────────────────────────────────────
    print(f"\n=== GUE Control (N={N}, {N_MATRICES} matrices) ===")
    evals_list = []
    for k in range(N_MATRICES):
        H = build_gue_random(N, rng)
        evals = eigh(H, eigvals_only=True)
        evals_list.append(evals)
        sys.stdout.flush()
    result, spacings = analyze_construction(evals_list, "GUE Control")
    results.append(result)
    print(f"  β = {result['beta']:.3f} ± {result['beta_err']:.3f}")
    print(f"  chi²_GUE = {result['chi2_gue']:.3f}, chi²_GOE = {result['chi2_goe']:.3f}")
    print(f"  GUE better: {result['gue_better']}")

    # ── C1: Random phases ────────────────────────────────────────────────────
    print(f"\n=== C1: Random Complex Phases (N={N}, {N_MATRICES} matrices) ===")
    evals_list = []
    for k in range(N_MATRICES):
        H = build_c1_random_phase_fast(N, mangoldt_vals, rng)
        evals = eigh(H, eigvals_only=True)
        evals_list.append(evals)
        sys.stdout.flush()
    result, spacings_c1 = analyze_construction(evals_list, "C1: Random Phase Hankel")
    results.append(result)
    print(f"  β = {result['beta']:.3f} ± {result['beta_err']:.3f}")
    print(f"  chi²_GUE = {result['chi2_gue']:.3f}, chi²_GOE = {result['chi2_goe']:.3f}")
    print(f"  GUE better: {result['gue_better']}")

    # ── C2a: Dirichlet χ₄ ────────────────────────────────────────────────────
    print(f"\n=== C2a: Dirichlet χ₄ (N={N}) ===")
    # Precompute character array
    char4_array = np.array([dirichlet_char_q4(d) for d in range(2 * N + 1)])
    evals_list = []
    H = build_c2_dirichlet_fast(N, mangoldt_vals, char4_array)
    evals = eigh(H, eigvals_only=True)
    evals_list.append(evals)
    result, _ = analyze_construction(evals_list, "C2a: Dirichlet χ₄")
    results.append(result)
    print(f"  β = {result['beta']:.3f} ± {result['beta_err']:.3f}")
    print(f"  chi²_GUE = {result['chi2_gue']:.3f}, chi²_GOE = {result['chi2_goe']:.3f}")
    print(f"  GUE better: {result['gue_better']}")

    # ── C2b: Dirichlet χ₈ ────────────────────────────────────────────────────
    print(f"\n=== C2b: Dirichlet χ₈ (N={N}) ===")
    char8_array = np.array([dirichlet_char_q8(d) for d in range(2 * N + 1)])
    evals_list = []
    H = build_c2_dirichlet_fast(N, mangoldt_vals, char8_array)
    evals = eigh(H, eigvals_only=True)
    evals_list.append(evals)
    result, _ = analyze_construction(evals_list, "C2b: Dirichlet χ₈")
    results.append(result)
    print(f"  β = {result['beta']:.3f} ± {result['beta_err']:.3f}")
    print(f"  chi²_GUE = {result['chi2_gue']:.3f}, chi²_GOE = {result['chi2_goe']:.3f}")
    print(f"  GUE better: {result['gue_better']}")

    # ── C3a: Gauss p=97 ──────────────────────────────────────────────────────
    print(f"\n=== C3a: Gauss phases (p=97, N={N}) ===")
    H = build_c3_gauss_fast(N, mangoldt_vals, 97)
    evals = eigh(H, eigvals_only=True)
    result, _ = analyze_construction([evals], "C3a: Gauss p=97")
    results.append(result)
    print(f"  β = {result['beta']:.3f} ± {result['beta_err']:.3f}")
    print(f"  chi²_GUE = {result['chi2_gue']:.3f}, chi²_GOE = {result['chi2_goe']:.3f}")
    print(f"  GUE better: {result['gue_better']}")

    # ── C3b: Gauss p=997 ─────────────────────────────────────────────────────
    print(f"\n=== C3b: Gauss phases (p=997, N={N}) ===")
    H = build_c3_gauss_fast(N, mangoldt_vals, 997)
    evals = eigh(H, eigvals_only=True)
    result, _ = analyze_construction([evals], "C3b: Gauss p=997")
    results.append(result)
    print(f"  β = {result['beta']:.3f} ± {result['beta_err']:.3f}")
    print(f"  chi²_GUE = {result['chi2_gue']:.3f}, chi²_GOE = {result['chi2_goe']:.3f}")
    print(f"  GUE better: {result['gue_better']}")

    # ── C4: Zeta phases ──────────────────────────────────────────────────────
    print(f"\n=== C4: Zeta-value phases (N={N}) ===")
    H = build_c4_zeta_fast(N, mangoldt_vals)
    evals = eigh(H, eigvals_only=True)
    result, spacings_c4 = analyze_construction([evals], "C4: Zeta phases")
    results.append(result)
    print(f"  β = {result['beta']:.3f} ± {result['beta_err']:.3f}")
    print(f"  chi²_GUE = {result['chi2_gue']:.3f}, chi²_GOE = {result['chi2_goe']:.3f}")
    print(f"  GUE better: {result['gue_better']}")

    # ── Summary ───────────────────────────────────────────────────────────────
    print("\n" + "="*70)
    print("SUMMARY SCORECARD")
    print("="*70)
    print(f"{'Construction':<30} {'β':>6} {'±err':>6} {'chi²_GUE':>10} {'chi²_GOE':>10} {'GUE?':>6}")
    print("-"*70)

    # Add baseline
    print(f"{'Hankel (S001 baseline)':<30} {'0.44':>6} {'':>6} {'':>10} {'':>10} {'No':>6}")

    for r in results:
        beta_str = f"{r['beta']:.3f}" if r['beta'] is not None else "N/A"
        err_str = f"{r['beta_err']:.3f}" if r['beta_err'] is not None else ""
        chi2g_str = f"{r['chi2_gue']:.2f}" if r['chi2_gue'] is not None else "N/A"
        chi2go_str = f"{r['chi2_goe']:.2f}" if r['chi2_goe'] is not None else "N/A"
        gue_str = "Yes" if r['gue_better'] else "No"
        print(f"{r['name']:<30} {beta_str:>6} {err_str:>6} {chi2g_str:>10} {chi2go_str:>10} {gue_str:>6}")

    # Save results to JSON
    output_path = "/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-002/explorations/exploration-001/code/results.json"
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {output_path}")

    # Find best construction
    valid = [(r['beta'], r['name']) for r in results if r['beta'] is not None and r['name'] != 'GUE Control']
    if valid:
        best_beta, best_name = max(valid)
        print(f"\nBest β: {best_beta:.3f} ({best_name})")
        if best_beta > 1.5:
            print("  → PRIMARY SUCCESS: β > 1.5 achieved!")
        elif best_beta > 1.0:
            print("  → SECONDARY SUCCESS: β > 1.0 achieved")
        elif best_beta > 0.44:
            print("  → PARTIAL SUCCESS: improvement over Hankel baseline")
        else:
            print("  → FAILURE: no improvement over Hankel baseline")

if __name__ == "__main__":
    main()

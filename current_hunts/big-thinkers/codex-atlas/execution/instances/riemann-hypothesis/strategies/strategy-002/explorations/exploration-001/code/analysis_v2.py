"""
Complex Arithmetic Matrices — GUE Screening v2
Fixed β estimation using full Wigner-like fit and Brody distribution.

Key changes from v1:
- β fitted over full s range (0 to 4), not just s < 0.5
- Brody parameter fit as secondary estimator
- KS distance added
- More diagnostic output
"""

import numpy as np
from scipy.linalg import eigh
from scipy.optimize import curve_fit, minimize_scalar
from scipy.special import gamma
from scipy.stats import kstest
import json
import sys
import time

# ─── Von Mangoldt ─────────────────────────────────────────────────────────────

def precompute_mangoldt(max_n):
    vals = np.zeros(max_n + 1)
    for n in range(2, max_n + 1):
        temp = n
        found_prime = None
        for p in range(2, int(n**0.5) + 1):
            if temp % p == 0:
                found_prime = p
                while temp % p == 0:
                    temp //= p
                break
        if found_prime is None:
            vals[n] = np.log(n)  # n is prime
        elif temp == 1:
            vals[n] = np.log(found_prime)  # n is prime power
    return vals

# ─── Unfolding ────────────────────────────────────────────────────────────────

def unfold_eigenvalues(evals):
    """Unfold using degree-15 polynomial fit of cumulative density."""
    evals_sorted = np.sort(evals)
    n = len(evals_sorted)
    cum = np.arange(1, n + 1, dtype=float)
    x_norm = (evals_sorted - evals_sorted.mean()) / (evals_sorted.std() + 1e-10)
    try:
        poly_coeffs = np.polyfit(x_norm, cum, deg=15)
        smooth_cum = np.polyval(poly_coeffs, x_norm)
    except Exception:
        smooth_cum = cum
    return smooth_cum

def compute_spacings(evals):
    """Compute nearest-neighbor spacings after unfolding, normalized to mean 1."""
    unfolded = unfold_eigenvalues(evals)
    spacings = np.diff(unfolded)
    spacings = spacings[spacings > 0]
    return spacings / spacings.mean()

# ─── Spacing distributions ────────────────────────────────────────────────────

def wigner_gue(s):
    """GUE Wigner surmise."""
    return (32.0 / np.pi**2) * s**2 * np.exp(-4.0 * s**2 / np.pi)

def wigner_goe(s):
    """GOE Wigner surmise."""
    return (np.pi / 2.0) * s * np.exp(-np.pi * s**2 / 4.0)

def wigner_poisson(s):
    """Poisson: P(s) = exp(-s)."""
    return np.exp(-s)

def wigner_interpolated(s, beta):
    """
    Wigner-like interpolation: P(s; β) = A s^β exp(-B s²)
    with normalization constants:
      A = 2 * Γ((β+2)/2)^(β+1) / Γ((β+1)/2)^(β+2)
      B = Γ((β+2)/2)² / Γ((β+1)/2)²
    These come from the normalization ∫P(s)ds = 1 and ∫s P(s)ds = 1.
    """
    # Compute normalization
    g1 = gamma((beta + 1) / 2)
    g2 = gamma((beta + 2) / 2)
    B = (g2 / g1)**2
    A = 2 * (g2**(beta + 1)) / (g1**(beta + 2))
    return A * s**beta * np.exp(-B * s**2)

def brody_distribution(s, beta):
    """
    Brody distribution (interpolates Poisson to GOE to GUE-like):
    P_Brody(s; β) = (β+1) b s^β exp(-b s^(β+1))
    where b = [Γ((β+2)/(β+1))]^(β+1)
    Note: Brody is defined for β in [0,1] strictly, but can be extended.
    """
    gval = gamma((beta + 2) / (beta + 1))
    b = gval**(beta + 1)
    return (beta + 1) * b * s**beta * np.exp(-b * s**(beta + 1))

# ─── Fitting ──────────────────────────────────────────────────────────────────

def fit_wigner_interpolated(spacings, n_bins=50):
    """Fit full Wigner-like interpolation P(s) = A s^β exp(-B s²) to spacings."""
    s_max = 4.0
    bins = np.linspace(0, s_max, n_bins + 1)
    hist, edges = np.histogram(spacings, bins=bins, density=True)
    centers = (edges[:-1] + edges[1:]) / 2
    mask = hist > 0

    if mask.sum() < 5:
        return np.nan, np.nan

    def model(s, beta):
        try:
            return wigner_interpolated(s, beta)
        except Exception:
            return np.ones_like(s) * 1e-10

    try:
        popt, pcov = curve_fit(
            model,
            centers[mask], hist[mask],
            p0=[1.0],
            bounds=([0.0], [4.0]),
            maxfev=10000
        )
        beta = popt[0]
        beta_err = np.sqrt(np.diag(pcov))[0] if pcov is not None else np.nan
        return float(beta), float(beta_err)
    except Exception as e:
        return np.nan, np.nan

def fit_brody(spacings, n_bins=50):
    """Fit Brody distribution to spacings."""
    s_max = 4.0
    bins = np.linspace(0, s_max, n_bins + 1)
    hist, edges = np.histogram(spacings, bins=bins, density=True)
    centers = (edges[:-1] + edges[1:]) / 2
    mask = hist > 0

    if mask.sum() < 5:
        return np.nan

    def neg_log_likelihood(beta):
        """Minimize negative log-likelihood."""
        if beta <= 0 or beta > 3:
            return 1e10
        try:
            gval = gamma((beta + 2) / (beta + 1))
            b = gval**(beta + 1)
            log_probs = np.log((beta + 1) * b) + beta * np.log(np.maximum(spacings, 1e-10)) - b * spacings**(beta + 1)
            return -np.sum(log_probs)
        except Exception:
            return 1e10

    result = minimize_scalar(neg_log_likelihood, bounds=(0.01, 3.0), method='bounded')
    return float(result.x) if result.success else np.nan

def compute_chi2_reduced(spacings, wigner_func, n_bins=30, s_max=4.0):
    """Compute reduced chi² of spacings vs a Wigner surmise."""
    bins = np.linspace(0, s_max, n_bins + 1)
    observed, edges = np.histogram(spacings, bins=bins, density=False)
    centers = (edges[:-1] + edges[1:]) / 2
    bin_width = bins[1] - bins[0]
    expected = wigner_func(centers) * bin_width * len(spacings)
    mask = expected > 0.5
    if mask.sum() < 5:
        return np.nan
    chi2_val = np.sum((observed[mask] - expected[mask])**2 / expected[mask])
    return chi2_val / mask.sum()

def compute_ks(spacings, wigner_func):
    """KS test vs theoretical distribution (using empirical CDF comparison)."""
    # Integrate wigner_func numerically to get CDF
    s_eval = np.linspace(0, 5, 2000)
    ds = s_eval[1] - s_eval[0]
    pdf_vals = wigner_func(s_eval)
    cdf_vals = np.cumsum(pdf_vals) * ds
    cdf_vals /= cdf_vals[-1]  # normalize

    # Empirical CDF
    sp_sorted = np.sort(spacings)
    n = len(sp_sorted)
    empirical_cdf = np.arange(1, n + 1) / n

    # Interpolate theoretical CDF at empirical points
    theo_cdf_at_sp = np.interp(sp_sorted, s_eval, cdf_vals)
    ks = np.max(np.abs(empirical_cdf - theo_cdf_at_sp))
    return float(ks)

# ─── Full analysis ────────────────────────────────────────────────────────────

def analyze(evals_list, name):
    """Full analysis of eigenvalue arrays."""
    all_spacings = []
    for evals in evals_list:
        sp = compute_spacings(evals)
        all_spacings.append(sp)
    spacings = np.concatenate(all_spacings)

    print(f"  n_spacings={len(spacings)}, min={spacings.min():.3f}, max={spacings.max():.3f}")

    # β from Wigner interpolation fit (full range)
    beta_wigner, beta_err = fit_wigner_interpolated(spacings)
    print(f"  Wigner-interp β = {beta_wigner:.3f} ± {beta_err:.3f}")

    # Brody parameter (full MLE)
    beta_brody = fit_brody(spacings)
    print(f"  Brody β = {beta_brody:.3f}")

    # Chi² comparisons
    chi2_gue = compute_chi2_reduced(spacings, wigner_gue)
    chi2_goe = compute_chi2_reduced(spacings, wigner_goe)
    chi2_poi = compute_chi2_reduced(spacings, wigner_poisson)
    print(f"  chi²: GUE={chi2_gue:.2f}, GOE={chi2_goe:.2f}, Poisson={chi2_poi:.2f}")

    # KS distances
    ks_gue = compute_ks(spacings, wigner_gue)
    ks_goe = compute_ks(spacings, wigner_goe)
    ks_poi = compute_ks(spacings, wigner_poisson)
    print(f"  KS: GUE={ks_gue:.3f}, GOE={ks_goe:.3f}, Poisson={ks_poi:.3f}")

    best = min([(ks_gue, 'GUE'), (ks_goe, 'GOE'), (ks_poi, 'Poisson')])
    print(f"  → Best fit: {best[1]} (KS={best[0]:.3f})")

    return {
        'name': name,
        'N': len(evals_list[0]),
        'N_matrices': len(evals_list),
        'n_spacings': len(spacings),
        'beta_wigner': float(beta_wigner) if not np.isnan(beta_wigner) else None,
        'beta_err': float(beta_err) if not np.isnan(beta_err) else None,
        'beta_brody': float(beta_brody) if not np.isnan(beta_brody) else None,
        'chi2_gue': float(chi2_gue) if not np.isnan(chi2_gue) else None,
        'chi2_goe': float(chi2_goe) if not np.isnan(chi2_goe) else None,
        'chi2_poi': float(chi2_poi) if not np.isnan(chi2_poi) else None,
        'ks_gue': float(ks_gue),
        'ks_goe': float(ks_goe),
        'ks_poi': float(ks_poi),
        'best_fit': best[1],
    }, spacings

# ─── Matrix builders ──────────────────────────────────────────────────────────

def build_gue(N, rng):
    A = (rng.standard_normal((N, N)) + 1j * rng.standard_normal((N, N))) / np.sqrt(2)
    return (A + A.conj().T) / 2

def build_c1_random_phase(N, mgv, rng):
    """C1: H_{jk} = Λ(|j-k|+1) × exp(2πi φ_{jk})."""
    i_idx, j_idx = np.meshgrid(np.arange(N), np.arange(N), indexing='ij')
    diff = np.abs(i_idx - j_idx)
    amp = mgv[diff + 1]

    # Random upper-triangular phases
    upper = np.triu(np.ones((N, N), dtype=bool), k=1)
    phi = np.zeros((N, N))
    phi[upper] = rng.uniform(0, 2 * np.pi, size=upper.sum())
    phi_antisym = phi - phi.T  # ensures H_{ij} = conj(H_{ji})

    H = amp * np.exp(1j * phi_antisym)
    np.fill_diagonal(H, mgv[1])  # Λ(1) = 0
    # Force exactly Hermitian
    H = (H + H.conj().T) / 2
    return H

def dirichlet_char_q4(n):
    n_mod = n % 4
    if n_mod == 1: return 1.0 + 0j
    elif n_mod == 3: return -1.0 + 0j
    else: return 0.0 + 0j

def dirichlet_char_q8(n):
    n_mod = n % 8
    vals = {1: 1, 3: 1, 5: -1, 7: -1}
    return complex(vals.get(n_mod, 0))

def build_c2_dirichlet(N, mgv, char_func):
    """C2: H_{jk} = Λ(|j-k|+1) × χ(j-k)/|χ(j-k)|."""
    i_idx, j_idx = np.meshgrid(np.arange(N), np.arange(N), indexing='ij')
    diff_abs = np.abs(i_idx - j_idx)
    signed_diff = i_idx - j_idx
    amp = mgv[diff_abs + 1]

    chi_vals = np.vectorize(lambda d: char_func(int(d)))(signed_diff)
    mag = np.abs(chi_vals)
    phase = np.where(mag > 1e-10, chi_vals / np.where(mag > 1e-10, mag, 1), 0.0)

    H = amp * phase
    np.fill_diagonal(H, float(np.real(mgv[1])))
    H = (H + H.conj().T) / 2
    return H

def build_c3_gauss(N, mgv, p):
    """C3: H_{jk} = Λ(|j-k|+1) × exp(2πi jk/p) [1-indexed]."""
    i_idx, j_idx = np.meshgrid(np.arange(N), np.arange(N), indexing='ij')
    diff_abs = np.abs(i_idx - j_idx)
    amp = mgv[diff_abs + 1]

    jk_mod = ((i_idx + 1) * (j_idx + 1)) % p
    phases = 2 * np.pi * jk_mod / p
    H = amp * np.exp(1j * phases)
    np.fill_diagonal(H, float(np.real(mgv[1])))
    H = (H + H.conj().T) / 2
    return H

def build_c4_zeta(N, mgv):
    """C4: H_{jk} = Λ(|j-k|+1) × exp(2πi Im(ζ(1/2 + i|j-k|)))."""
    print(f"  Computing Im(ζ(1/2+it)) for t=0..{N-1}...")
    try:
        import mpmath
        mpmath.mp.dps = 15
        zeta_imag = np.zeros(N)
        for d in range(N):
            if d % 100 == 0:
                print(f"    t={d}/{N}")
            zeta_imag[d] = float(mpmath.im(mpmath.zeta(0.5 + 1j * float(d))))
    except Exception as e:
        print(f"  mpmath unavailable ({e}), using partial Euler sum")
        zeta_imag = np.array([
            np.imag(sum(n**(-0.5 - 1j * float(d)) for n in range(1, 51)))
            for d in range(N)
        ])

    i_idx, j_idx = np.meshgrid(np.arange(N), np.arange(N), indexing='ij')
    diff_abs = np.abs(i_idx - j_idx)
    amp = mgv[diff_abs + 1]

    phases = 2 * np.pi * zeta_imag[diff_abs]
    H = amp * np.exp(1j * phases)
    np.fill_diagonal(H, float(np.real(mgv[1])))
    H = (H + H.conj().T) / 2
    return H

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    N = 500
    N_REP = 3  # matrices per construction for noise reduction
    rng = np.random.default_rng(42)

    print(f"Precomputing Von Mangoldt up to {2*N}...")
    mgv = precompute_mangoldt(2 * N)
    print(f"  Λ: {[(n, round(mgv[n],3)) for n in [1,2,3,4,5,6,7,8,9,10]]}")

    all_results = []

    # ──────────────────────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("GUE CONTROL")
    print("="*60)
    t0 = time.time()
    evals_list = []
    for k in range(N_REP):
        H = build_gue(N, rng)
        evals_list.append(eigh(H, eigvals_only=True))
    result, sp = analyze(evals_list, "GUE Control")
    all_results.append(result)
    print(f"  Time: {time.time()-t0:.1f}s")

    # ──────────────────────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("C1: RANDOM PHASE HANKEL")
    print("="*60)
    t0 = time.time()
    evals_list = []
    for k in range(N_REP):
        H = build_c1_random_phase(N, mgv, rng)
        evals_list.append(eigh(H, eigvals_only=True))
    result, sp = analyze(evals_list, "C1: Random Phase")
    all_results.append(result)
    print(f"  Time: {time.time()-t0:.1f}s")

    # ──────────────────────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("C2a: DIRICHLET χ₄")
    print("="*60)
    t0 = time.time()
    H = build_c2_dirichlet(N, mgv, dirichlet_char_q4)
    evals = eigh(H, eigvals_only=True)
    result, _ = analyze([evals], "C2a: Dirichlet χ₄")
    all_results.append(result)
    print(f"  Time: {time.time()-t0:.1f}s")

    # ──────────────────────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("C2b: DIRICHLET χ₈")
    print("="*60)
    t0 = time.time()
    H = build_c2_dirichlet(N, mgv, dirichlet_char_q8)
    evals = eigh(H, eigvals_only=True)
    result, _ = analyze([evals], "C2b: Dirichlet χ₈")
    all_results.append(result)
    print(f"  Time: {time.time()-t0:.1f}s")

    # ──────────────────────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("C3a: GAUSS PHASES (p=97)")
    print("="*60)
    t0 = time.time()
    H = build_c3_gauss(N, mgv, 97)
    evals = eigh(H, eigvals_only=True)
    result, _ = analyze([evals], "C3a: Gauss p=97")
    all_results.append(result)
    print(f"  Time: {time.time()-t0:.1f}s")

    # ──────────────────────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("C3b: GAUSS PHASES (p=997)")
    print("="*60)
    t0 = time.time()
    H = build_c3_gauss(N, mgv, 997)
    evals = eigh(H, eigvals_only=True)
    result, _ = analyze([evals], "C3b: Gauss p=997")
    all_results.append(result)
    print(f"  Time: {time.time()-t0:.1f}s")

    # ──────────────────────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("C4: ZETA-VALUE PHASES")
    print("="*60)
    t0 = time.time()
    H = build_c4_zeta(N, mgv)
    evals = eigh(H, eigvals_only=True)
    result, _ = analyze([evals], "C4: Zeta Phases")
    all_results.append(result)
    print(f"  Time: {time.time()-t0:.1f}s")

    # ──────────────────────────────────────────────────────────────────────────
    print("\n" + "="*70)
    print("FINAL SCORECARD")
    print("="*70)
    print(f"{'Name':<28} {'β_W':>6} {'β_B':>6} {'chi²_GUE':>9} {'chi²_GOE':>9} {'KS_GUE':>7} {'KS_GOE':>7} {'Best':>8}")
    print("-"*70)
    # Baseline
    print(f"{'Hankel S001 baseline':<28} {'0.44':>6} {'-':>6} {'-':>9} {'-':>9} {'-':>7} {'-':>7} {'GOE?':>8}")

    for r in all_results:
        bw = f"{r['beta_wigner']:.3f}" if r['beta_wigner'] is not None else "N/A"
        bb = f"{r['beta_brody']:.3f}" if r['beta_brody'] is not None else "N/A"
        cg = f"{r['chi2_gue']:.2f}" if r['chi2_gue'] is not None else "N/A"
        cgo = f"{r['chi2_goe']:.2f}" if r['chi2_goe'] is not None else "N/A"
        kg = f"{r['ks_gue']:.3f}"
        kgo = f"{r['ks_goe']:.3f}"
        print(f"{r['name']:<28} {bw:>6} {bb:>6} {cg:>9} {cgo:>9} {kg:>7} {kgo:>7} {r['best_fit']:>8}")

    # Save
    out = "/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/riemann-hypothesis/strategies/strategy-002/explorations/exploration-001/code/results_v2.json"
    with open(out, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\nSaved to {out}")

    # Best construction (excluding GUE control)
    arithmetic = [r for r in all_results if r['name'] != 'GUE Control']
    best_ks = min(arithmetic, key=lambda r: r['ks_gue'])
    best_chi2 = min(arithmetic, key=lambda r: r['chi2_gue'] if r['chi2_gue'] is not None else 1e9)
    print(f"\nBest KS_GUE: {best_ks['name']} (KS={best_ks['ks_gue']:.3f})")
    print(f"Best chi²_GUE: {best_chi2['name']} (chi²={best_chi2['chi2_gue']:.2f})")

    beta_winner = max(arithmetic, key=lambda r: r['beta_wigner'] or 0)
    print(f"Highest β_Wigner: {beta_winner['name']} (β={beta_winner['beta_wigner']:.3f})")

if __name__ == "__main__":
    main()

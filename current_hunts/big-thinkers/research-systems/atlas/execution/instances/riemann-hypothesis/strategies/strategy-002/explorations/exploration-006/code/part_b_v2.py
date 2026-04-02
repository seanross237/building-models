"""
Part B v2: Complex Dirichlet Character Matrix

Uses proper beta estimation matching exploration-001:
- Degree-15 polynomial unfolding
- Fit model P(s) = s^beta * exp(-B*s^2) using log-space least squares

Tests:
1. Real Hankel baseline (should get beta≈0.44)
2. chi mod 5 multiplicative (phi=g(j)+g(k))
3. chi mod 13 multiplicative (phi=g(j)+g(k))
4. chi mod 5 factorizable (unitarily equivalent to real Hankel)
"""

import numpy as np

N_MATRIX = 500

# ─────────────────────────────────────────────────────────────────────────────
# Utilities
# ─────────────────────────────────────────────────────────────────────────────
def von_mangoldt_table(limit):
    Lambda = np.zeros(limit + 1)
    is_prime = np.ones(limit + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = False
    for p in np.where(is_prime)[0]:
        pm, log_p = int(p), np.log(float(p))
        while pm <= limit:
            Lambda[pm] = log_p
            pm *= int(p)
    return Lambda

def char_mod5_vec(n_arr):
    """chi mod 5: 1→1, 2→i, 3→-i, 4→-1, 0→0"""
    r = np.asarray(n_arr, dtype=int) % 5
    return np.array([0, 1, 1j, -1j, -1], dtype=complex)[r]

def char_mod13_vec(n_arr):
    """Primitive character mod 13, chi(2^k) = exp(2*pi*i*k/12)"""
    r = np.asarray(n_arr, dtype=int) % 13
    dlog = np.zeros(13, dtype=int)
    pow2 = 1
    for k in range(1, 13):
        pow2 = (pow2 * 2) % 13
        dlog[pow2] = k
    k_arr = dlog[r]
    return np.where(r == 0, 0+0j, np.exp(2j * np.pi * k_arr / 12))

def unfold_eigenvalues(eigs, deg=15):
    """Unfold using degree-15 polynomial (following exploration-001)."""
    n = len(eigs)
    cum = np.arange(n, dtype=float)
    # Normalize for numerical stability
    e_min, e_max = eigs[0], eigs[-1]
    if e_max == e_min:
        return eigs.copy()
    x_norm = (eigs - e_min) / (e_max - e_min) * 2 - 1  # scale to [-1, 1]
    try:
        poly_coeffs = np.polyfit(x_norm, cum, deg=min(deg, n//10))
        smooth_cum = np.polyval(poly_coeffs, x_norm)
    except Exception:
        smooth_cum = cum
    return smooth_cum

def get_spacings(H):
    """Diagonalize H and get unfolded spacings."""
    eigs = np.sort(np.real(np.linalg.eigvalsh(H)))
    n = len(eigs)

    # Use middle 80%
    start = n // 10
    eigs_mid = eigs[start:n - start]

    # Unfold
    smooth = unfold_eigenvalues(eigs_mid, deg=15)
    spacings = np.diff(smooth)
    spacings = spacings[spacings > 0]
    # Normalize to mean spacing 1
    spacings = spacings / np.mean(spacings)
    return spacings

def fit_beta(spacings, s_max=0.5, n_bins=30):
    """
    Fit P(s) = A * s^beta * exp(-B*s^2) using weighted least squares in log space.
    Returns (beta, B, chi2_gue, chi2_poisson).

    Following exploration-001: fit in range [very small s, s_max].
    """
    hist, edges = np.histogram(spacings, bins=n_bins, range=(0, 3.0), density=True)
    centers = (edges[:-1] + edges[1:]) / 2
    dbin = edges[1] - edges[0]

    # Fit range
    mask = (centers > 0.02) & (centers <= s_max) & (hist > 0)
    if np.sum(mask) < 4:
        return np.nan, np.nan, np.nan

    s_fit = centers[mask]
    p_fit = hist[mask]

    # Log-space fit: log P = log A + beta * log s - B * s^2
    # Design matrix: [1, log(s), -s^2]
    X = np.column_stack([np.ones(len(s_fit)), np.log(s_fit), -s_fit**2])
    y = np.log(p_fit)

    # Weighted: weight by P (more weight to higher probability bins)
    W = np.diag(p_fit)

    # Solve: (X^T W X) c = X^T W y
    XtW = X.T @ W
    try:
        c = np.linalg.solve(XtW @ X, XtW @ y)
    except np.linalg.LinAlgError:
        c = np.linalg.lstsq(X, y, rcond=None)[0]

    beta = c[1]
    B = c[2]  # should be > 0 for repulsion

    # Chi2 vs GUE Wigner surmise
    def gue_pdf(s): return (32/np.pi**2) * s**2 * np.exp(-4*s**2/np.pi)
    def poisson_pdf(s): return np.exp(-s)

    expected_gue = gue_pdf(centers) * dbin * len(spacings)
    expected_poisson = poisson_pdf(centers) * dbin * len(spacings)
    observed = hist * dbin * len(spacings)

    eps = 1e-10
    chi2_gue = np.sum((observed - expected_gue)**2 / (expected_gue + eps))
    chi2_poisson = np.sum((observed - expected_poisson)**2 / (expected_poisson + eps))

    return beta, B, chi2_gue, chi2_poisson, hist, centers

# ─────────────────────────────────────────────────────────────────────────────
# Matrix construction
# ─────────────────────────────────────────────────────────────────────────────
def build_hankel_real(N):
    Lambda = von_mangoldt_table(2*N + 2)
    idx = np.arange(N)
    return Lambda[np.abs(idx[:, None] - idx[None, :]) + 1]

def build_matrix_multiplicative(N, chi_vec):
    """H_{jk} = Lambda(|j-k|+1) * chi(j+1) * chi(k+1)"""
    Lambda = von_mangoldt_table(2*N + 2)
    idx = np.arange(N)
    H_lam = Lambda[np.abs(idx[:, None] - idx[None, :]) + 1]
    chi_vals = chi_vec(np.arange(1, N+1))
    # Note: chi(j)*chi(k) NOT chi(j)*conj(chi(k))
    chi_outer = np.outer(chi_vals, chi_vals)
    H = H_lam * chi_outer
    H = (H + H.conj().T) / 2  # Hermitianize
    return H

def build_matrix_factorizable(N, chi_vec):
    """H_{jk} = Lambda(|j-k|+1) * chi(j+1) * conj(chi(k+1))"""
    Lambda = von_mangoldt_table(2*N + 2)
    idx = np.arange(N)
    H_lam = Lambda[np.abs(idx[:, None] - idx[None, :]) + 1]
    chi_vals = chi_vec(np.arange(1, N+1))
    chi_outer_herm = np.outer(chi_vals, np.conj(chi_vals))
    H = H_lam * chi_outer_herm
    return H

# ─────────────────────────────────────────────────────────────────────────────
# Verify unfolding on GUE control
# ─────────────────────────────────────────────────────────────────────────────
print("CONTROL: GUE random matrix (should get beta≈2.0)")
np.random.seed(42)
A_gue = np.random.randn(N_MATRIX, N_MATRIX)
H_gue = (A_gue + A_gue.T) / (2 * np.sqrt(N_MATRIX))  # GOE
# For GUE: use complex
A_gue_c = (np.random.randn(N_MATRIX, N_MATRIX) + 1j*np.random.randn(N_MATRIX, N_MATRIX)) / np.sqrt(2)
H_gue_c = (A_gue_c + A_gue_c.conj().T) / (2 * np.sqrt(N_MATRIX))
sp_gue = get_spacings(H_gue_c)
res_gue = fit_beta(sp_gue, s_max=0.5)
beta_gue = res_gue[0]
print(f"Beta (GUE control): {beta_gue:.3f} (expected 2.0)")

sp_goe = get_spacings(H_gue)
res_goe = fit_beta(sp_goe, s_max=0.5)
beta_goe = res_goe[0]
print(f"Beta (GOE control): {beta_goe:.3f} (expected 1.0)")

# ─────────────────────────────────────────────────────────────────────────────
# Main constructions
# ─────────────────────────────────────────────────────────────────────────────
import time
t0 = time.time()

results_list = []

print("\n" + "="*60)
print("1. Real Hankel baseline")
print("="*60)
H_real = build_hankel_real(N_MATRIX)
sp_real = get_spacings(H_real)
res_real = fit_beta(sp_real, s_max=0.5)
beta_real = res_real[0]
print(f"Beta: {beta_real:.3f}")
results_list.append(('Real Hankel', beta_real, sp_real))

print(f"\n2. chi mod 5, factorizable (expect same as real Hankel)")
H_f5 = build_matrix_factorizable(N_MATRIX, char_mod5_vec)
sp_f5 = get_spacings(H_f5)
res_f5 = fit_beta(sp_f5, s_max=0.5)
beta_f5 = res_f5[0]
print(f"Beta: {beta_f5:.3f}")
results_list.append(('Factorizable mod 5', beta_f5, sp_f5))

print(f"\n3. chi mod 5, multiplicative")
H_m5 = build_matrix_multiplicative(N_MATRIX, char_mod5_vec)
print(f"   Non-zero frac: {np.sum(np.abs(H_m5)>1e-10)/H_m5.size:.3f}")
sp_m5 = get_spacings(H_m5)
res_m5 = fit_beta(sp_m5, s_max=0.5)
beta_m5 = res_m5[0]
print(f"Beta: {beta_m5:.3f}")
results_list.append(('Multiplicative mod 5', beta_m5, sp_m5))

print(f"\n4. chi mod 13, factorizable (sanity check)")
H_f13 = build_matrix_factorizable(N_MATRIX, char_mod13_vec)
sp_f13 = get_spacings(H_f13)
res_f13 = fit_beta(sp_f13, s_max=0.5)
beta_f13 = res_f13[0]
print(f"Beta: {beta_f13:.3f}")
results_list.append(('Factorizable mod 13', beta_f13, sp_f13))

print(f"\n5. chi mod 13, multiplicative")
H_m13 = build_matrix_multiplicative(N_MATRIX, char_mod13_vec)
print(f"   Non-zero frac: {np.sum(np.abs(H_m13)>1e-10)/H_m13.size:.3f}")
sp_m13 = get_spacings(H_m13)
res_m13 = fit_beta(sp_m13, s_max=0.5)
beta_m13 = res_m13[0]
print(f"Beta: {beta_m13:.3f}")
results_list.append(('Multiplicative mod 13', beta_m13, sp_m13))

# ─────────────────────────────────────────────────────────────────────────────
# Investigate: does multiplicative construction have sparse rows?
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("STRUCTURAL ANALYSIS OF MULTIPLICATIVE MATRICES")
print("="*60)

# For mod 5: chi(n)=0 when 5|n. So H_{jk}=0 when 5|(j+1) OR 5|(k+1).
# This means 1/5 of rows and columns are all-zero → big degeneracy at 0!
chi5_nonzero = char_mod5_vec(np.arange(1, N_MATRIX+1))
zero_rows_5 = np.sum(chi5_nonzero == 0)
print(f"mod 5: {zero_rows_5} indices where chi(j+1)=0 (→ zero rows/cols)")
print(f"       = {100*zero_rows_5/N_MATRIX:.1f}% of all rows")
print(f"       This means ~{zero_rows_5}^2 = {zero_rows_5**2} zero-only matrix elements")
print(f"       → many near-zero eigenvalues → excess small spacings → low beta")

chi13_nonzero = char_mod13_vec(np.arange(1, N_MATRIX+1))
zero_rows_13 = np.sum(chi13_nonzero == 0)
print(f"\nmod 13: {zero_rows_13} zero indices ({100*zero_rows_13/N_MATRIX:.1f}% of rows)")

# Count eigenvalues very close to 0
eigs5 = np.sort(np.real(np.linalg.eigvalsh(H_m5)))
eigs13 = np.sort(np.real(np.linalg.eigvalsh(H_m13)))
print(f"\nEigenvalues near 0 (|λ|<0.01):")
print(f"  mod 5 multiplicative: {np.sum(np.abs(eigs5)<0.01)}")
print(f"  mod 13 multiplicative: {np.sum(np.abs(eigs13)<0.01)}")
print(f"  real Hankel: {np.sum(np.abs(np.linalg.eigvalsh(H_real))<0.01)}")

# ─────────────────────────────────────────────────────────────────────────────
# Alternative: exclude zero-chi rows for mod 5
# Remove indices where chi(j+1)=0
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("ALTERNATIVE: Exclude zero-chi rows (mod 5)")
print("="*60)
# For mod 5, chi(j+1)=0 iff 5|(j+1) iff j=4,9,14,...
# Keep only rows where chi(j+1)≠0
chi5_vals = char_mod5_vec(np.arange(1, N_MATRIX+1))
nonzero_mask = chi5_vals != 0
N_nonzero = np.sum(nonzero_mask)
idx_nz = np.where(nonzero_mask)[0]
print(f"Keeping {N_nonzero} indices with chi≠0")

# Build sub-matrix
Lambda = von_mangoldt_table(2*N_MATRIX + 2)
H_m5_sub = np.zeros((N_nonzero, N_nonzero), dtype=complex)
chi_nz = chi5_vals[nonzero_mask]
for i, j_real in enumerate(idx_nz):
    for k_idx, k_real in enumerate(idx_nz):
        H_m5_sub[i, k_idx] = Lambda[abs(j_real - k_real) + 1] * chi_nz[i] * chi_nz[k_idx]
H_m5_sub = (H_m5_sub + H_m5_sub.conj().T) / 2
sp_m5_sub = get_spacings(H_m5_sub)
res_m5_sub = fit_beta(sp_m5_sub, s_max=0.5)
beta_m5_sub = res_m5_sub[0]
print(f"Beta (mod 5, no-zero rows, N={N_nonzero}): {beta_m5_sub:.3f}")

# Same for mod 13
chi13_vals = char_mod13_vec(np.arange(1, N_MATRIX+1))
nonzero_mask_13 = chi13_vals != 0
N_nz13 = np.sum(nonzero_mask_13)
idx_nz13 = np.where(nonzero_mask_13)[0]
print(f"mod 13: keeping {N_nz13} indices")
H_m13_sub = np.zeros((N_nz13, N_nz13), dtype=complex)
chi_nz13 = chi13_vals[nonzero_mask_13]
for i, j_real in enumerate(idx_nz13):
    for k_idx, k_real in enumerate(idx_nz13):
        H_m13_sub[i, k_idx] = Lambda[abs(j_real - k_real) + 1] * chi_nz13[i] * chi_nz13[k_idx]
H_m13_sub = (H_m13_sub + H_m13_sub.conj().T) / 2
sp_m13_sub = get_spacings(H_m13_sub)
res_m13_sub = fit_beta(sp_m13_sub, s_max=0.5)
beta_m13_sub = res_m13_sub[0]
print(f"Beta (mod 13, no-zero rows, N={N_nz13}): {beta_m13_sub:.3f}")

# ─────────────────────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("SUMMARY SCORECARD")
print("="*70)
print(f"{'Construction':>50} | {'Beta':>6}")
print("-"*60)
print(f"{'GUE (random matrix control)':>50} | {beta_gue:.3f}")
print(f"{'GOE (random matrix control)':>50} | {beta_goe:.3f}")
print(f"{'Real Hankel baseline':>50} | {beta_real:.3f}")
print(f"{'chi mod 5, factorizable (=real Hankel)':>50} | {beta_f5:.3f}")
print(f"{'chi mod 5, multiplicative (with zero rows)':>50} | {beta_m5:.3f}")
print(f"{'chi mod 5, multiplicative (no zero rows)':>50} | {beta_m5_sub:.3f}")
print(f"{'chi mod 13, factorizable':>50} | {beta_f13:.3f}")
print(f"{'chi mod 13, multiplicative (with zero rows)':>50} | {beta_m13:.3f}")
print(f"{'chi mod 13, multiplicative (no zero rows)':>50} | {beta_m13_sub:.3f}")
print()
print(f"Reference: Gauss sums C3b from exploration-001: beta≈1.09")
print(f"Success criterion: beta > 1.0")

print(f"\nTotal time: {time.time()-t0:.1f}s")

# ─────────────────────────────────────────────────────────────────────────────
# Save
# ─────────────────────────────────────────────────────────────────────────────
OUT = "/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-002/explorations/exploration-006/code/part_b_v2_results.npz"
np.savez(OUT,
         beta_gue=beta_gue, beta_goe=beta_goe,
         beta_real=beta_real, beta_f5=beta_f5, beta_m5=beta_m5,
         beta_f13=beta_f13, beta_m13=beta_m13,
         beta_m5_sub=beta_m5_sub, beta_m13_sub=beta_m13_sub,
         sp_real=sp_real, sp_m5=sp_m5, sp_m13=sp_m13,
         sp_m5_sub=sp_m5_sub, sp_m13_sub=sp_m13_sub)
print(f"Saved to {OUT}")
print("Done.")

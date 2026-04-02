"""
Part B: Complex Dirichlet Character Matrix

Test whether H_{jk} = Lambda(|j-k|+1) * chi((j+1)*(k+1)) using complex
Dirichlet characters mod 5 and mod 13 can achieve beta > 1 (GUE-like).

Phase structure:
- Factorizable: phi(j,k) = g(j) - g(k)  → unitarily equivalent to real Hankel
- Multiplicative: phi(j,k) = g(j) + g(k) → breaks time-reversal symmetry → expect beta > 1
"""

import numpy as np

N_MATRIX = 500  # Matrix size

# ─────────────────────────────────────────────────────────────────────────────
# 1. Von Mangoldt function
# ─────────────────────────────────────────────────────────────────────────────
def von_mangoldt_table(limit):
    """Compute Lambda(n) for n up to limit."""
    Lambda = np.zeros(limit + 1)
    is_prime = np.ones(limit + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = False
    primes = np.where(is_prime)[0]
    for p in primes:
        pm = int(p)
        log_p = np.log(float(p))
        while pm <= limit:
            Lambda[pm] = log_p
            pm *= int(p)
    return Lambda

# ─────────────────────────────────────────────────────────────────────────────
# 2. Dirichlet characters (vectorized)
# ─────────────────────────────────────────────────────────────────────────────
def char_mod5_vec(n_arr):
    """chi mod 5: chi(1)=1, chi(2)=i, chi(3)=-i, chi(4)=-1, chi(0)=0"""
    r = np.asarray(n_arr, dtype=int) % 5
    table = np.array([0, 1, 1j, -1j, -1], dtype=complex)
    return table[r]

def char_mod13_vec(n_arr):
    """
    Primitive character mod 13.
    Generator g=2: 2^1=2, 2^2=4, ..., 2^12=1 mod 13.
    chi(2^k) = exp(2*pi*i*k/12).
    """
    r = np.asarray(n_arr, dtype=int) % 13
    # dlog table (discrete log base 2 mod 13)
    dlog = np.zeros(13, dtype=int)
    pow2 = 1
    for k in range(1, 13):
        pow2 = (pow2 * 2) % 13
        dlog[pow2] = k
    k_arr = dlog[r]
    result = np.where(r == 0, 0.0+0j, np.exp(2j * np.pi * k_arr / 12))
    return result

# ─────────────────────────────────────────────────────────────────────────────
# 3. Build matrices
# ─────────────────────────────────────────────────────────────────────────────
def build_matrix_multiplicative(N, chi_vec):
    """
    H_{jk} = Lambda(|j-k|+1) * chi(j+1) * chi(k+1)
    (using multiplicativity: chi((j+1)(k+1)) = chi(j+1)*chi(k+1))
    Phase: phi(j,k) = g(j+1) + g(k+1) — NOT factorizable as g(j)-g(k)
    """
    Lambda = von_mangoldt_table(2*N + 2)

    # Lambda row: Lambda[|j-k|+1] for fixed j as k varies
    # H_{jk} = Lambda(|j-k|+1) * chi(j+1) * chi(k+1)
    # = [Lambda Hankel] * outer_product(chi, chi)
    # This is a HADAMARD product of Hankel matrix with outer product

    # Build Lambda Hankel matrix
    idx = np.arange(N)
    H_lam = Lambda[np.abs(idx[:, None] - idx[None, :]) + 1]

    # chi values
    chi_vals = chi_vec(np.arange(1, N+1))

    # Phase matrix: chi(j+1) * chi(k+1) = chi_j * chi_k
    # This has phi(j,k) = arg(chi_j) + arg(chi_k) = g(j) + g(k)
    chi_outer = np.outer(chi_vals, chi_vals)  # chi_j * chi_k (NOT conj)

    H = H_lam * chi_outer

    # Hermitianize
    H = (H + H.conj().T) / 2
    return H

def build_matrix_factorizable(N, chi_vec):
    """
    H_{jk} = Lambda(|j-k|+1) * chi(j+1) * conj(chi(k+1))
    Phase: phi(j,k) = g(j) - g(k) — UNITARILY EQUIVALENT to real Hankel
    H = D * H_real * D^dagger where D = diag(chi(1),...,chi(N))
    """
    Lambda = von_mangoldt_table(2*N + 2)
    idx = np.arange(N)
    H_lam = Lambda[np.abs(idx[:, None] - idx[None, :]) + 1]

    chi_vals = chi_vec(np.arange(1, N+1))
    # chi(j) * conj(chi(k)) = D * I * D^dagger applied element-wise
    chi_outer_herm = np.outer(chi_vals, np.conj(chi_vals))

    H = H_lam * chi_outer_herm
    return H

# ─────────────────────────────────────────────────────────────────────────────
# 4. Compute beta from eigenvalue spacings
# ─────────────────────────────────────────────────────────────────────────────
def compute_beta_robust(H):
    """Fit beta from spacing distribution via log-log histogram fit."""
    # Diagonalize
    eigs = np.sort(np.real(np.linalg.eigvalsh(H)))
    n = len(eigs)

    # Use middle 80% to avoid edge effects
    start = n // 10
    eigs_mid = eigs[start:n - start]
    n_mid = len(eigs_mid)

    # Unfold with degree-5 polynomial
    poly = np.polyfit(eigs_mid, np.arange(n_mid), 5)
    unfolded = np.polyval(poly, eigs_mid)
    spacings = np.diff(unfolded)
    spacings = spacings[spacings > 0]
    spacings = spacings / np.mean(spacings)

    # Histogram
    n_bins = 50
    hist, edges = np.histogram(spacings, bins=n_bins, range=(0, 4), density=True)
    centers = (edges[:-1] + edges[1:]) / 2

    # Fit beta in log-log: log P(s) = beta * log(s) + const
    mask_fit = (centers > 0.02) & (centers < 0.8) & (hist > 0)
    if np.sum(mask_fit) < 4:
        return np.nan, spacings, hist, centers, np.nan

    x_fit = np.log(centers[mask_fit])
    y_fit = np.log(hist[mask_fit])
    coeffs = np.polyfit(x_fit, y_fit, 1)
    beta = coeffs[0]

    # KS test vs GUE Wigner surmise CDF
    def gue_cdf(s):
        return 1 - np.exp(-4*s**2/np.pi) * (1 + 4*s**2/np.pi)

    # Manual KS: sort spacings, compare to CDF
    s_sorted = np.sort(spacings)
    empirical_cdf = np.arange(1, len(s_sorted)+1) / len(s_sorted)
    theoretical_cdf = gue_cdf(s_sorted)
    ks_stat = np.max(np.abs(empirical_cdf - theoretical_cdf))

    return beta, spacings, hist, centers, ks_stat

# ─────────────────────────────────────────────────────────────────────────────
# 5. Run all constructions
# ─────────────────────────────────────────────────────────────────────────────

import time
t0 = time.time()
Lambda = von_mangoldt_table(2*N_MATRIX + 2)

# --- Real Hankel baseline ---
print("="*60)
print("BASELINE: Real Hankel (Von Mangoldt)")
print("="*60)
idx = np.arange(N_MATRIX)
H_real = Lambda[np.abs(idx[:, None] - idx[None, :]) + 1]
beta_r, sp_r, hist_r, cen_r, ks_r = compute_beta_robust(H_real)
print(f"Beta (real Hankel): {beta_r:.3f}")
print(f"KS stat vs GUE: {ks_r:.4f}")
print(f"Expected: beta≈0.44")

# --- Mod 5, factorizable (sanity check) ---
print("\n" + "="*60)
print("chi mod 5, factorizable (H_{jk}=Lambda*chi(j)*conj(chi(k)))")
print("Expected: same beta as real Hankel (unitary equivalence)")
print("="*60)
H_fact5 = build_matrix_factorizable(N_MATRIX, char_mod5_vec)
print(f"Hermitian error: {np.max(np.abs(H_fact5 - H_fact5.conj().T)):.2e}")
beta_f5, sp_f5, hist_f5, cen_f5, ks_f5 = compute_beta_robust(H_fact5)
print(f"Beta (factorizable mod 5): {beta_f5:.3f}")
print(f"KS stat vs GUE: {ks_f5:.4f}")
print(f"({time.time()-t0:.1f}s)")

# --- Mod 5, multiplicative ---
print("\n" + "="*60)
print("chi mod 5, multiplicative (H_{jk}=Lambda*chi(j+1)*chi(k+1))")
print("Phase: g(j)+g(k) → breaks time-reversal → expect beta > 1")
print("="*60)
H_mul5 = build_matrix_multiplicative(N_MATRIX, char_mod5_vec)
print(f"Hermitian error: {np.max(np.abs(H_mul5 - H_mul5.conj().T)):.2e}")
# Check if matrix has mostly zeros (would signal cancellation)
nz = np.sum(np.abs(H_mul5) > 1e-10) / H_mul5.size
print(f"Non-zero fraction: {nz:.3f}")
beta_m5, sp_m5, hist_m5, cen_m5, ks_m5 = compute_beta_robust(H_mul5)
print(f"Beta (multiplicative mod 5): {beta_m5:.3f}")
print(f"KS stat vs GUE: {ks_m5:.4f}")
print(f"({time.time()-t0:.1f}s)")

# --- Mod 13, factorizable (sanity check) ---
print("\n" + "="*60)
print("chi mod 13, factorizable (sanity check)")
print("="*60)
H_fact13 = build_matrix_factorizable(N_MATRIX, char_mod13_vec)
beta_f13, sp_f13, hist_f13, cen_f13, ks_f13 = compute_beta_robust(H_fact13)
print(f"Beta (factorizable mod 13): {beta_f13:.3f}")
print(f"KS stat vs GUE: {ks_f13:.4f}")

# --- Mod 13, multiplicative ---
print("\n" + "="*60)
print("chi mod 13, multiplicative (H_{jk}=Lambda*chi(j+1)*chi(k+1))")
print("12 distinct phases → more diversity than mod 5 (4 phases)")
print("="*60)
H_mul13 = build_matrix_multiplicative(N_MATRIX, char_mod13_vec)
print(f"Hermitian error: {np.max(np.abs(H_mul13 - H_mul13.conj().T)):.2e}")
nz13 = np.sum(np.abs(H_mul13) > 1e-10) / H_mul13.size
print(f"Non-zero fraction: {nz13:.3f}")
beta_m13, sp_m13, hist_m13, cen_m13, ks_m13 = compute_beta_robust(H_mul13)
print(f"Beta (multiplicative mod 13): {beta_m13:.3f}")
print(f"KS stat vs GUE: {ks_m13:.4f}")
print(f"({time.time()-t0:.1f}s)")

# ─────────────────────────────────────────────────────────────────────────────
# 6. Summary scorecard
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("SUMMARY SCORECARD")
print("="*70)
print(f"{'Construction':>45} | {'Beta':>6} | {'KS vs GUE':>10}")
print("-"*65)
print(f"{'GUE target':>45} | {'2.00':>6} | {'0.000':>10}")
print(f"{'GOE target':>45} | {'1.00':>6} | {'~0.1':>10}")
print(f"{'Real Hankel baseline':>45} | {beta_r:>6.3f} | {ks_r:>10.4f}")
print(f"{'chi mod 5, factorizable':>45} | {beta_f5:>6.3f} | {ks_f5:>10.4f}")
print(f"{'chi mod 5, multiplicative':>45} | {beta_m5:>6.3f} | {ks_m5:>10.4f}")
print(f"{'chi mod 13, factorizable':>45} | {beta_f13:>6.3f} | {ks_f13:>10.4f}")
print(f"{'chi mod 13, multiplicative':>45} | {beta_m13:>6.3f} | {ks_m13:>10.4f}")
print()
print(f"Gauss sum (C3b from exploration-001): beta≈1.09 (reference)")
print(f"Success criterion: beta > 1.0")

# ─────────────────────────────────────────────────────────────────────────────
# 7. Spacing histograms
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("SPACING HISTOGRAMS (small-s region shows beta)")
print("="*60)
def gue_pdf(s): return (32/np.pi**2) * s**2 * np.exp(-4*s**2/np.pi)
def poisson_pdf(s): return np.exp(-s)
def goe_pdf(s): return (np.pi/2) * s * np.exp(-np.pi*s**2/4)

print(f"{'s':>5} | {'Poisson':>8} | {'GOE':>8} | {'GUE':>8} | {'Real':>8} | {'Mul5':>8} | {'Mul13':>8}")
print("-"*65)
for s_t in [0.1, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 2.5]:
    ir = np.argmin(np.abs(cen_r - s_t))
    im5 = np.argmin(np.abs(cen_m5 - s_t))
    im13 = np.argmin(np.abs(cen_m13 - s_t))
    p_val = poisson_pdf(s_t)
    go_val = goe_pdf(s_t)
    g_val = gue_pdf(s_t)
    r_val = hist_r[ir] if ir < len(hist_r) else 0
    m5_val = hist_m5[im5] if im5 < len(hist_m5) else 0
    m13_val = hist_m13[im13] if im13 < len(hist_m13) else 0
    print(f"{s_t:5.2f} | {p_val:8.4f} | {go_val:8.4f} | {g_val:8.4f} | {r_val:8.4f} | {m5_val:8.4f} | {m13_val:8.4f}")

# ─────────────────────────────────────────────────────────────────────────────
# 8. Save
# ─────────────────────────────────────────────────────────────────────────────
OUT = "/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-002/explorations/exploration-006/code/part_b_results.npz"
np.savez(OUT,
         beta_real=beta_r, beta_fact5=beta_f5, beta_mul5=beta_m5,
         beta_fact13=beta_f13, beta_mul13=beta_m13,
         ks_real=ks_r, ks_mul5=ks_m5, ks_mul13=ks_m13,
         spacings_real=sp_r, spacings_mul5=sp_m5, spacings_mul13=sp_m13)
print(f"\nResults saved to {OUT}")
print(f"Total time: {time.time()-t0:.1f}s")
print("Done.")

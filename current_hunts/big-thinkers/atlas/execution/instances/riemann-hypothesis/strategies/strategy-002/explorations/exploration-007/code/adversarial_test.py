"""
Adversarial Test for C1 Pair Correlation Claim
Exploration 007, Strategy 002, Riemann Hypothesis mission

Tests:
  1a. GUE control matrix (N=500, 5 realizations)
  1b. Flat-amplitude random phase Hermitian (N=500, 5 realizations)
  1c. Flat-amplitude Toeplitz random phase (N=500, 5 realizations)
  2.  C1 realization stability (N=500, 20 realizations)
  3.  Severity table (printed)

All pair correlations computed with degree-5 polynomial unfolding,
dr=0.05 bins [0,6], MRD over r in [0.5, 4.0].
"""

import numpy as np
from math import gamma, log, gcd

rng = np.random.default_rng(42)

# ─────────────────────────────────────────────
# Von Mangoldt function
# ─────────────────────────────────────────────
def von_mangoldt(n):
    """Return Λ(n) = log(p) if n=p^k for prime p, else 0."""
    if n < 2:
        return 0.0
    # Check if n is a prime power
    for p in range(2, int(n**0.5) + 1):
        if n % p == 0:
            # p is the smallest prime factor
            k = n
            while k % p == 0:
                k //= p
            if k == 1:
                return log(p)
            else:
                return 0.0
    # n is prime
    return log(n)

# Precompute Von Mangoldt table
MAX_N = 1001   # need Λ(1)..Λ(N) where N=500 → differences up to 499
vm_table = np.array([von_mangoldt(n) for n in range(MAX_N + 1)])

# ─────────────────────────────────────────────
# Matrix builders
# ─────────────────────────────────────────────
def build_C1(N, rng):
    """C1: H_{jk} = Λ(|j-k|+1) * exp(2πi φ_{jk}), Hermitian."""
    # Random phases for upper triangle
    phi = rng.uniform(0, 1, (N, N))
    H = np.zeros((N, N), dtype=complex)
    for j in range(N):
        for k in range(j + 1, N):
            amp = vm_table[abs(j - k) + 1]
            phase = np.exp(2j * np.pi * phi[j, k])
            H[j, k] = amp * phase
            H[k, j] = amp * phase.conjugate()
    # Diagonal: Λ(1) = 0
    return H

def build_C1_fast(N, rng):
    """Fast vectorized C1 builder."""
    phi = rng.uniform(0, 1, (N, N))
    # Build amplitude matrix via outer differences
    idx = np.arange(N)
    diff = np.abs(idx[:, None] - idx[None, :]) + 1   # (N,N), entries 1..N
    amp = vm_table[diff]                               # broadcast lookup
    phase = np.exp(2j * np.pi * phi)
    H_raw = amp * phase
    # Make Hermitian: (H + H†)/2  (diagonal is Λ(1)=0)
    H = (H_raw + H_raw.conj().T) / 2.0
    return H

def build_GUE(N, rng):
    """Standard GUE: (A + A†)/sqrt(2N), A complex Gaussian."""
    A = (rng.standard_normal((N, N)) + 1j * rng.standard_normal((N, N))) / np.sqrt(2)
    H = (A + A.conj().T) / np.sqrt(2 * N)
    return H

def build_flat_random_phase(N, rng):
    """Flat-amplitude random phase: H_{jk} = exp(2πi φ_{jk}) for j<k, Hermitian."""
    phi = rng.uniform(0, 1, (N, N))
    phase = np.exp(2j * np.pi * phi)
    H = (phase + phase.conj().T) / 2.0
    # zero diagonal
    np.fill_diagonal(H, 0.0)
    return H

def build_toeplitz_random_phase(N, rng):
    """Flat Toeplitz random phase: H_{jk} = exp(2πi ψ_{|j-k|}), ψ_0=0.

    Uses one random phase per lag — different from flat_random_phase.
    Note: H_{jk} = H_{kj}* by construction since ψ_{-l} = ψ_l*.
    """
    # One complex phase per lag 0..N-1; lag 0 is real (diagonal)
    psi = np.exp(2j * np.pi * rng.uniform(0, 1, N))
    psi[0] = 1.0  # diagonal is real
    idx = np.arange(N)
    lag = np.abs(idx[:, None] - idx[None, :])
    # H_{jk} = psi[lag] for j<k, conjugate for j>k → already Hermitian if psi[-l]=psi[l]*
    # We set: for j<k, H_{jk} = psi[lag]; for j>k, H_{jk} = conj(psi[lag])
    H = np.where(idx[:, None] <= idx[None, :], psi[lag], psi[lag].conj())
    np.fill_diagonal(H, 0.0)
    return H.astype(complex)

# ─────────────────────────────────────────────
# Eigenvalue unfolding
# ─────────────────────────────────────────────
def unfold(eigenvalues, poly_degree=5):
    """Degree-5 polynomial unfolding of sorted eigenvalues."""
    eigs = np.sort(eigenvalues)
    N = len(eigs)
    # Cumulative count (empirical CDF * N)
    cum = np.arange(1, N + 1, dtype=float)
    # Fit polynomial to map eigenvalue → cumulative count
    coeffs = np.polyfit(eigs, cum, poly_degree)
    unfolded = np.polyval(coeffs, eigs)
    return unfolded

# ─────────────────────────────────────────────
# Pair correlation R₂(r)
# ─────────────────────────────────────────────
def pair_correlation_mrd(unfolded_eigs_list, dr=0.05, r_min=0.5, r_max=4.0, r_end=6.0):
    """
    Compute mean pair correlation R₂(r) over multiple realizations,
    then compute MRD vs Montgomery formula.

    unfolded_eigs_list: list of 1D arrays (one per realization)
    Returns: r_centers, R2_computed, R2_montgomery, mrd
    """
    r_bins = np.arange(0, r_end + dr, dr)
    r_centers = 0.5 * (r_bins[:-1] + r_bins[1:])

    R2_sum = np.zeros(len(r_centers))

    for unfolded in unfolded_eigs_list:
        N = len(unfolded)
        # All pairwise separations (upper triangle)
        diffs = []
        for i in range(N):
            d = np.abs(unfolded[i + 1:] - unfolded[i])
            diffs.append(d)
        diffs = np.concatenate(diffs)

        # Histogram
        counts, _ = np.histogram(diffs, bins=r_bins)
        # Normalize: R₂(r) = count / (N * dr)
        R2 = counts / (N * dr)
        R2_sum += R2

    R2_mean = R2_sum / len(unfolded_eigs_list)

    # Montgomery formula
    R2_montgomery = 1 - (np.sinc(r_centers))**2  # sinc(x) = sin(πx)/(πx)

    # MRD over [r_min, r_max]
    mask = (r_centers >= r_min) & (r_centers <= r_max)
    mrd = np.mean(np.abs(R2_mean[mask] - R2_montgomery[mask]) / R2_montgomery[mask])

    return r_centers, R2_mean, R2_montgomery, mrd

# ─────────────────────────────────────────────
# β_Wigner fitting (Brody distribution, grid search)
# ─────────────────────────────────────────────
def fit_brody_beta(unfolded_eigs_list, n_bins=30, s_min=0.05, s_max=3.0):
    """
    Fit Brody distribution β via grid search over β ∈ [0, 3].
    Averages the NNS histogram over realizations, then fits.
    """
    s_bins = np.linspace(s_min, s_max, n_bins + 1)
    s_centers = 0.5 * (s_bins[:-1] + s_bins[1:])
    ds = s_bins[1] - s_bins[0]

    hist_sum = np.zeros(n_bins)
    total_spacings = 0

    for unfolded in unfolded_eigs_list:
        spacings = np.diff(np.sort(unfolded))
        # Filter to [s_min, s_max]
        spacings = spacings[(spacings >= s_min) & (spacings <= s_max)]
        counts, _ = np.histogram(spacings, bins=s_bins)
        hist_sum += counts
        total_spacings += len(spacings)

    # Normalize
    hist_norm = hist_sum / (hist_sum.sum() * ds)

    # Grid search
    beta_grid = np.linspace(0, 3, 121)
    best_beta, best_chi2 = 0.0, 1e18

    for beta in beta_grid:
        B = gamma((beta + 2) / (beta + 1)) ** (beta + 1)
        theory = (1 + beta) * B * s_centers**beta * np.exp(-B * s_centers**(beta + 1))
        theory_norm = theory / (theory.sum() * ds)
        chi2 = np.sum((hist_norm - theory_norm)**2 / (theory_norm + 1e-10))
        if chi2 < best_chi2:
            best_chi2 = chi2
            best_beta = beta

    return best_beta, best_chi2

# ─────────────────────────────────────────────
# Main computation
# ─────────────────────────────────────────────
N = 500
N_null_real = 5
N_c1_stability = 20

print("=" * 60)
print("ADVERSARIAL TEST — Exploration 007")
print(f"N={N}, null realizations={N_null_real}, C1 stability realizations={N_c1_stability}")
print("=" * 60)

# ─────────────────────────────────────────────
# Test 1a: GUE control
# ─────────────────────────────────────────────
print("\n[TEST 1a] GUE control matrix")
gue_unfolded = []
gue_betas = []
for i in range(N_null_real):
    H = build_GUE(N, rng)
    eigs = np.linalg.eigvalsh(H)
    u = unfold(eigs)
    gue_unfolded.append(u)
    print(f"  Realization {i+1}: eigenvalue range [{eigs.min():.3f}, {eigs.max():.3f}]")

r_c, R2_gue, R2_mont, mrd_gue = pair_correlation_mrd(gue_unfolded)
beta_gue, _ = fit_brody_beta(gue_unfolded)
print(f"  GUE MRD = {mrd_gue*100:.2f}%")
print(f"  GUE β_Wigner = {beta_gue:.3f}")

# ─────────────────────────────────────────────
# Test 1b: Flat-amplitude random phase
# ─────────────────────────────────────────────
print("\n[TEST 1b] Flat-amplitude random phase")
flat_unfolded = []
for i in range(N_null_real):
    H = build_flat_random_phase(N, rng)
    eigs = np.linalg.eigvalsh(H)
    u = unfold(eigs)
    flat_unfolded.append(u)
    print(f"  Realization {i+1}: eigenvalue range [{eigs.min():.3f}, {eigs.max():.3f}]")

r_c2, R2_flat, _, mrd_flat = pair_correlation_mrd(flat_unfolded)
beta_flat, _ = fit_brody_beta(flat_unfolded)
print(f"  Flat MRD = {mrd_flat*100:.2f}%")
print(f"  Flat β_Wigner = {beta_flat:.3f}")

# ─────────────────────────────────────────────
# Test 1c: Flat Toeplitz random phase
# ─────────────────────────────────────────────
print("\n[TEST 1c] Flat Toeplitz random phase")
toep_unfolded = []
for i in range(N_null_real):
    H = build_toeplitz_random_phase(N, rng)
    eigs = np.linalg.eigvalsh(H)
    u = unfold(eigs)
    toep_unfolded.append(u)
    print(f"  Realization {i+1}: eigenvalue range [{eigs.min():.3f}, {eigs.max():.3f}]")

r_c3, R2_toep, _, mrd_toep = pair_correlation_mrd(toep_unfolded)
beta_toep, _ = fit_brody_beta(toep_unfolded)
print(f"  Toeplitz MRD = {mrd_toep*100:.2f}%")
print(f"  Toeplitz β_Wigner = {beta_toep:.3f}")

# ─────────────────────────────────────────────
# Test 2: C1 stability (20 realizations)
# ─────────────────────────────────────────────
print("\n[TEST 2] C1 realization stability (20 realizations)")
c1_mrds = []
c1_unfolded_all = []
for i in range(N_c1_stability):
    H = build_C1_fast(N, rng)
    eigs = np.linalg.eigvalsh(H)
    u = unfold(eigs)
    c1_unfolded_all.append(u)
    # Compute MRD for this single realization
    _, _, _, mrd_i = pair_correlation_mrd([u])
    c1_mrds.append(mrd_i)
    print(f"  Realization {i+1:2d}: MRD = {mrd_i*100:.2f}%")

c1_mrds = np.array(c1_mrds)
print(f"\n  C1 (20 realizations):")
print(f"    Mean MRD = {c1_mrds.mean()*100:.2f}%")
print(f"    Std  MRD = {c1_mrds.std()*100:.2f}%")
print(f"    Min  MRD = {c1_mrds.min()*100:.2f}%")
print(f"    Max  MRD = {c1_mrds.max()*100:.2f}%")
print(f"    90th pct = {np.percentile(c1_mrds, 90)*100:.2f}%")
print(f"    Frac ≤10% = {(c1_mrds <= 0.10).mean()*100:.0f}%")

# Also compute pooled MRD (average over all 20)
_, _, _, mrd_c1_pooled = pair_correlation_mrd(c1_unfolded_all)
beta_c1, _ = fit_brody_beta(c1_unfolded_all)
print(f"    Pooled MRD (all 20 averaged) = {mrd_c1_pooled*100:.2f}%")
print(f"    β_Wigner (all 20) = {beta_c1:.3f}")

# ─────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"{'Matrix':<35} {'MRD':>8} {'β_Wigner':>10} {'≤10%?':>8}")
print("-" * 65)
print(f"{'C1 Von Mangoldt Hankel (prior)':<35} {'7.9%':>8} {'1.18':>10} {'YES':>8}")
print(f"{'C1 Von Mangoldt (20 real, pooled)':<35} {mrd_c1_pooled*100:7.2f}% {beta_c1:>10.3f} {'YES' if mrd_c1_pooled<=0.10 else 'NO':>8}")
print(f"{'GUE control':<35} {mrd_gue*100:7.2f}% {beta_gue:>10.3f} {'YES' if mrd_gue<=0.10 else 'NO':>8}")
print(f"{'Flat-amp random phase':<35} {mrd_flat*100:7.2f}% {beta_flat:>10.3f} {'YES' if mrd_flat<=0.10 else 'NO':>8}")
print(f"{'Flat Toeplitz random phase':<35} {mrd_toep*100:7.2f}% {beta_toep:>10.3f} {'YES' if mrd_toep<=0.10 else 'NO':>8}")
print(f"{'Zeta zeros baseline (2000 zeros)':<35} {'9.1%':>8} {'N/A':>10} {'YES':>8}")

print(f"\nC1 stability (20 realizations):")
print(f"  Mean ± Std = {c1_mrds.mean()*100:.2f}% ± {c1_mrds.std()*100:.2f}%")
print(f"  Frac ≤10% = {(c1_mrds <= 0.10).mean()*100:.0f}%")
print(f"  90th pct  = {np.percentile(c1_mrds, 90)*100:.2f}%")

# ─────────────────────────────────────────────
# Save results
# ─────────────────────────────────────────────
np.savez(
    "/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/riemann-hypothesis/strategies/strategy-002/explorations/exploration-007/code/results.npz",
    r_centers=r_c,
    R2_montgomery=R2_mont,
    R2_gue=R2_gue,
    R2_flat=R2_flat,
    R2_toep=R2_toep,
    mrd_gue=mrd_gue,
    mrd_flat=mrd_flat,
    mrd_toep=mrd_toep,
    beta_gue=beta_gue,
    beta_flat=beta_flat,
    beta_toep=beta_toep,
    c1_mrds=c1_mrds,
    mrd_c1_pooled=mrd_c1_pooled,
    beta_c1=beta_c1,
)
print("\nResults saved to code/results.npz")

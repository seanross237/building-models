# Exploration 005 — Constraint Rescoring + Gauss Prime Sweep

## Mission Context

We are investigating the Riemann Hypothesis through random matrix theory. Previous exploration (strategy-002, exploration-001) built complex Hermitian arithmetic matrices and found:

- **C1 (Random complex phases on Von Mangoldt Hankel):** β = 1.675, GUE best fit on spacing distribution (KS_GUE = 0.028). Scored 4 PASS, 2 PARTIAL, 2 NOT COMPUTED, 2 N/A on the 10-constraint catalog. The NOT COMPUTED constraints (pair correlation #2 and spectral rigidity #7) were missed due to code bugs.

- **C3b (Gauss sum phases, p=997):** β = 1.092, GOE best fit. This is the most arithmetically meaningful result — exp(2πi jk/997) is a genuine number-theoretic phase.

- **Trend discovered:** C3a (p=97) → β=0.88, C3b (p=997) → β=1.09. The larger the prime p, the higher the β. This raises the question: does β → 2 as p → ∞?

## Your Task — Two Parts

### Part A: Full 10-Constraint Rescoring for C1

The previous exploration had bugs in pair correlation normalization (MRD = 0.996, meaningless) and Δ₃ formula (values 10-25× too small). Fix these and compute the correct scores for constraints 2 and 7.

**C1 construction:** N=500 Hermitian matrix with entries H_{jk} = Λ(|j-k|+1) × exp(2πi × φ_{jk}) where φ_{jk} are independent uniform random phases (Hermitian: φ_{kj} = -φ_{jk}).

**Reuse the saved matrix data from exploration-001** if available:
- Path: `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-002/explorations/exploration-001/code/`
- Files: `c1_full_analysis.json` (has β and spacing data), eigenvalues may not be saved

If eigenvalues not saved, regenerate: construct 5 independent N=500 C1 matrices and average statistics across them.

#### Corrected Pair Correlation (Constraint 2)

```python
def pair_correlation_correct(eigenvalues, r_bins, bandwidth=0.3):
    """Compute R₂(r) = density of pairs with separation r in unfolded spectrum."""
    # Step 1: Unfold eigenvalues to mean spacing 1
    eigs_sorted = np.sort(eigenvalues)
    N = len(eigs_sorted)

    # Fit smooth density (polynomial degree 5 to cumulative)
    ranks = np.arange(1, N+1)
    poly = np.polyfit(eigs_sorted, ranks, deg=5)
    unfold = np.polyval(poly, eigs_sorted)
    # Normalize to mean spacing 1
    unfold = unfold * (N - 1) / (unfold[-1] - unfold[0])

    # Step 2: Compute all pairwise separations
    diffs = []
    for i in range(N):
        d = unfold[i+1:] - unfold[i]
        d = d[d < max(r_bins)]
        diffs.extend(d.tolist())
    diffs = np.array(diffs)

    # Step 3: Histogram and normalize to pair density
    counts, _ = np.histogram(diffs, bins=r_bins)
    dr = r_bins[1] - r_bins[0]
    # Normalize: R₂(r) → 1 as r → ∞ for uncorrelated spectrum
    # Normalization: R₂(r) = (2 × count) / (N × dr × ρ)
    # where ρ = N/(L_unfolded) = 1 for unfolded spectrum
    # For N eigenvalues over L, each r bin has expected count N*(N-1)*dr (Poisson)
    # So R₂(r) = (counts / (dr * bin_expected))
    # Expected pairs at separation r: N × 1 (density) × dr = N × dr
    # (for unfolded spectrum with N eigenvalues, density ρ=1)
    bin_expected = N * dr
    R2 = counts / bin_expected

    return R2

# For C1: average R₂ over multiple matrix realizations
```

Compare to Montgomery: R₂_Montgomery(r) = 1 - (sin(πr)/(πr))²

Report mean relative deviation (MRD) for r in [0.5, 4.0]:
MRD = mean(|R₂_computed(r) - R₂_Montgomery(r)| / R₂_Montgomery(r))

**Target:** MRD < 10% is good (GUE-like). MRD > 50% is bad.

#### Corrected Δ₃ (Constraint 7)

```python
def delta3_correct(unfolded, L, n_windows=200):
    """Correctly compute Δ₃(L) using Dyson-Mehta formula."""
    N = len(unfolded)
    delta3_values = []

    # Sample random window starts
    window_starts = np.random.uniform(unfolded[0], unfolded[-1] - L, n_windows)

    for E0 in window_starts:
        # Select eigenvalues in window [E0, E0 + L]
        mask = (unfolded >= E0) & (unfolded < E0 + L)
        ys = unfolded[mask]
        n = len(ys)
        if n < 3:
            continue

        # Rank in window (counting function within window)
        ranks = np.arange(1, n+1).astype(float)

        # Fit N(E) ≈ a*E + b in window (minimize residuals)
        xs = ys - E0  # shift to [0, L]
        A = np.column_stack([xs, np.ones(n)])
        result, _, _, _ = np.linalg.lstsq(A, ranks, rcond=None)
        a, b = result

        # Compute residuals
        residuals = ranks - (a * xs + b)

        # Δ₃(L) for this window = (1/L) * integral of residuals²
        # For a staircase, the integral from 0 to L of [N(E) - aE - b]² dE
        # = sum over intervals between eigenvalues:
        # For eigenvalue at position x_i with jump at x_i:
        # integral = sum_{i=0}^{n} (r_i - a*x - b)² integrated over [x_i, x_{i+1}]
        # where r_i = i (count before x_{i+1})

        # Approximate: Σ residuals² × mean_spacing / L
        # But correct version: integrate piecewise constant function

        # Add boundary points
        xs_ext = np.concatenate([[0], xs, [L]])
        residuals_ext = np.concatenate([[0 - b, ], residuals, [n - (a*L + b)]])
        # Count function value in each interval [xs_ext[i], xs_ext[i+1]]
        # Between xs[i-1] and xs[i], count = i-1 (0-indexed)

        integral = 0
        for j in range(len(xs_ext) - 1):
            x_left = xs_ext[j]
            x_right = xs_ext[j+1]
            dx = x_right - x_left
            if dx <= 0:
                continue
            # Count function value in [x_left, x_right] = j (number of eigenvalues before x_right)
            # In unshifted terms: count = j (we've passed j-1 eigenvalues at x_left if j>0)
            count_val = j  # 0 before first, 1 after first, etc.
            # Linear fit value at midpoint
            x_mid = (x_left + x_right) / 2
            fit_val = a * x_mid + b
            integral += (count_val - fit_val)**2 * dx

        delta3_values.append(integral / L)

    return np.nanmean(delta3_values)
```

Compute Δ₃(L) for L = 5, 10, 15, 20, 25, 30, 40, 50.

**Target zeta values (from strategy-001):** Δ₃ = 0.156 ± 0.005 for L > 15 (the "super-rigidity" finding)

**For C1:** Report the saturation value. Does it match the zeta value of 0.156, or is it closer to the GUE prediction?

Also compute the GUE prediction for comparison:
Δ₃_GUE(L) ≈ (1/π²) × (log(2πL) + γ + 1 - π²/8) where γ ≈ 0.5772

### Part B: Gauss Prime Sweep (Extend C3b to Larger Primes)

Test the Gauss sum construction H_{jk} = Λ(|j-k|+1) × exp(2πi jk/p) for p = 9973, 99991 (primes near 10^4 and 10^5). Also include p = 997 for continuity.

For each prime:
1. Construct N=500 matrix
2. Compute β_Wigner (level repulsion exponent)
3. Compare to GUE (β=2), GOE (β=1), Poisson (β=0)

Produce a trend plot: β vs log(p).

**Key question:** Is there a clear trend β → 2 as p → ∞? Or does β plateau somewhere below 2?

If β increases with p, extrapolate: at what p would β = 2?

#### Implementation notes for Gauss phases:

```python
def gauss_hankel(N, p, lambda_max=None):
    """Construct N×N complex Hermitian matrix with Gauss sum phases."""
    from sympy import primerange
    # Precompute von Mangoldt function
    Λ = np.zeros(2*N + 2)
    for pk in primerange(2, 2*N+2):
        pk_m = pk
        while pk_m <= 2*N+1:
            Λ[pk_m] = np.log(pk)
            pk_m *= pk

    # Build matrix
    H = np.zeros((N, N), dtype=complex)
    for j in range(N):
        for k in range(N):
            amplitude = Λ[abs(j-k) + 1]  # Von Mangoldt
            if amplitude > 0:
                phase = np.exp(2j * np.pi * j * k / p)
                H[j, k] = amplitude * phase

    # Ensure Hermitian (H + H†)/2
    H = (H + H.conj().T) / 2
    return H
```

Note: For p >> N, the phase exp(2πi jk/p) varies slowly → nearly real matrix → β close to 0 or 1. For p ≈ N, the phases span many cycles → more diversity. For p << N, the phases repeat many times → also periodic structure. The maximum β may occur at p ≈ N.

**Test this:** Also run p = N = 500, 251 (prime near N/2), 997 (prime near 2N).

#### Scoring table format:

| p | N | β_Wigner | β_Brody | Best fit | χ²_GUE | χ²_GOE | Notes |
|---|---|---|---|---|---|---|---|
| 97 | 500 | 0.88 | 0.93 | GOE | 10.9 | 1.47 | (from S002-E001) |
| 251 | 500 | ? | ? | ? | ? | ? | |
| 499 | 500 | ? | ? | ? | ? | ? | prime near N |
| 997 | 500 | 1.09 | 0.96 | GOE | 5.0 | 0.64 | (from S002-E001) |
| 9973 | 500 | ? | ? | ? | ? | ? | |
| 99991 | 500 | ? | ? | ? | ? | ? | |

## Success Criteria

**Primary success:**
1. Pair correlation MRD for C1 is < 50% (confirming it's at least in the GUE direction)
2. Δ₃ for C1 computes to a non-trivially wrong formula value (even if not 0.156)
3. Gauss β trend shows clear increase with p up to some value

**Secondary success:**
1. Gauss construction reaches β > 1.5 for some prime p — this would make it an arithmetic construction in the GUE range
2. C1 pair correlation MRD < 20%

**Failure:**
1. C1 pair correlation MRD > 80% (spacing is GUE-like but correlations are not)
2. Gauss β plateaus below 1.5 for all primes tested

## Exploration Directory

`/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-002/explorations/exploration-005/`

Write scripts to `code/`, REPORT.md incrementally, REPORT-SUMMARY.md last.

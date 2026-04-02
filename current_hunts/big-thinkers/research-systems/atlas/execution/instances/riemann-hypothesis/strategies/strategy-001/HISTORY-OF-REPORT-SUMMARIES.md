# Exploration History

## Exploration 001: GUE Pair Correlation and Nearest-Neighbor Spacing

### Goal
Compute zeta zeros and test pair correlation / nearest-neighbor spacing against GUE predictions.

### What Was Done
- Computed 2,000 low-height zeros (t in [14, 2515]) and 500 high-height zeros (t in [9450, 9878]) using mpmath
- Computed pair correlation R2(r) and compared to Montgomery's conjecture R2 = 1 - (sin(pi*r)/(pi*r))^2
- Computed nearest-neighbor spacing P(s) and compared to GUE Wigner surmise
- Compared against all four standard ensembles: Poisson, GOE, GUE, GSE
- Performed KS tests and chi-squared analysis with statistical uncertainty estimates

### Outcome: SUCCEEDED

**The pair correlation matches Montgomery/GUE to 9% mean relative deviation, with deviations statistically consistent with noise (68% within 1sigma).** The nearest-neighbor spacing matches GUE Wigner surmise to 4% mean absolute deviation. GUE is the best-fitting ensemble at both low and high heights.

### Key Takeaway
GUE is definitively the correct universality class. Poisson ruled out (5x worse), GOE ruled out (2x worse), GSE disfavored (1.2x worse). The Riemann operator must act on a complex Hilbert space and break time-reversal symmetry (or have half-integer spin).

### Leads Worth Pursuing
1. Higher-order unfolding (chi^2/dof = 1.50 mildly elevated)
2. Exact GUE vs Wigner surmise (KS marginally rejects Wigner at 5%)
3. Number variance and spectral rigidity (long-range correlations, Berry saturation)

### Computations Identified
1. Number variance Sigma^2(L) computation
2. Exact GUE spacing CDF (Fredholm determinant of sine kernel)
3. Large-scale zero computation via Odlyzko-Schonhage algorithm

## Exploration 002: Number Variance, Spectral Rigidity, and Berry's Saturation

### Goal
Compute number variance Sigma^2(L), spectral rigidity Delta_3(L), and spectral form factor K(tau) for the first 2000 zeta zeros. Test Berry's (1985) saturation prediction.

### What Was Done
- Computed 2000 zeros via mpmath (311s), unfolded with standard formula
- Calculated Sigma^2(L) for 50 L-values from 0.1 to 100
- Calculated Delta_3(L) for 28 L-values from 0.7 to 100
- Calculated K(tau) for 200 tau-values with ensemble averaging (16 blocks of 400 zeros)
- Generated GUE random matrix simulation as finite-size control
- Validated computation against Poisson process

### Outcome: SATURATION DETECTED

Berry's saturation confirmed definitively:
1. Sigma^2(L) saturates at ~0.3-0.5 for L > 2 (GUE predicts growth to 1.38 at L=100)
2. Delta_3(L) saturates at 0.156 for L > 15 (GUE theory: 0.50 at L=100) — most dramatic signal
3. Form factor ramp slope = 1.010 (GUE: 1.0), plateau = 1.043 (GUE: 1.0) — GUE confirmed at short range
4. Zeta zeros are ~50% MORE rigid than even finite-size GUE simulation at large scales

### Key Takeaway
Zeta zeros are GUE at short range but MORE ordered than GUE at long range — "super-rigidity" from prime periodic orbits. This constrains the operator's orbit structure. Saturation onset at L~2-5 is earlier than Berry's predicted L_max~100, possibly due to mixing heights or finite-N effects.

### Combined Constraint Catalog (10 items across 2 explorations)
1. GUE symmetry class (beta=2), no time-reversal symmetry
2. Pair correlation matches Montgomery (9% relative deviation, noise-consistent)
3. NN spacing matches GUE Wigner surmise (4% absolute deviation)
4. Poisson, GOE definitively ruled out; GSE disfavored
5. Quadratic level repulsion (P(s) ~ s^2)
6. Number variance saturates beyond GUE at L > 2
7. Spectral rigidity saturates at Delta_3 = 0.156 for L > 15
8. Form factor ramp slope = 1.010, plateau = 1.043
9. Super-rigidity: zeros 30-50% more rigid than finite-size GUE at large L
10. Periodic orbit structure related to primes (saturation encodes sum over log(p)^2/p)

### Computations Identified
1. Height-resolved saturation analysis (bin zeros by T, test L_max vs height)
2. Quantitative comparison to Berry's explicit formula (prime sum prediction)
3. Use precomputed zero tables (LMFDB) for better statistics

## Exploration 003: Berry-Keating xp Operator — Spectrum Computation

### Goal
Compute spectra of three Hilbert-Polya candidate operators and score against the 10-point constraint catalog.

### What Was Done
- **A: Sierra-Townsend regularization** — equally spaced E_n = n (2000 eigenvalues)
- **B: BBM PT-symmetric operator** — H in N=120 harmonic oscillator basis
- **C: Connes-inspired zeta zero matrix** — 200 zeta zeros in Hermitian matrix vs GUE ensemble

### Outcome
- **Approach A: 0/10 PASS.** Crystalline spectrum, fails everything. Just the "mean field" of xp.
- **Approach B: 0/10 PASS (1 PARTIAL).** Doublet spectrum, negative level repulsion (beta=-0.57), wrong scaling. HO basis truncation destroys PT-symmetric structure.
- **Approach C: 5/10 PASS, 4 PARTIAL.** Zeta zeros (trivially) match GUE local statistics. Confirmed super-rigidity (45-56% more rigid than GUE at L=5-15).

### Key Takeaway
**The prime number input is the entire ball game.** xp provides only the smooth Weyl part. All interesting structure (GUE statistics, super-rigidity, form factor) comes from fluctuations determined by primes via the explicit formula. No simple xp regularization captures this. A successful operator must have primes encoded in its structure.

### Unexpected Findings
- GUE vs GSE indistinguishable at N=200 (L1 = 0.068 for both)
- BBM effectively Hermitian in truncated HO basis (max|H-H†| = 4e-13)
- Super-rigidity confirmed independently (45-56% at L=5-15)

### Computations Identified
1. Trace formula reconstruction: start from equally-spaced spectrum, add oscillatory prime corrections, check how many constraints are satisfied
2. BBM in position-space basis (avoid HO truncation artifacts)
3. Rerun Approach C with 2000 zeros for better statistics

## Exploration 004: Trace Formula Reconstruction — xp + Primes = Zeta Zeros?

### Goal
Test whether smooth xp spectrum + prime oscillatory corrections can reconstruct the zeta zero spectrum and its GUE statistics.

### What Was Done
- Computed 2000 actual zeros + 2000 smooth zeros (inverting N_smooth)
- Corrected formula error (removed spurious ln(p) factor)
- Discovered fundamental 0.5 Gibbs offset in prime sum at zeros
- Tested linearized and root-finding reconstruction for P_max = 10 to 10000
- Computed GUE statistics for actual, smooth, and corrected spectra
- Analyzed convergence and residual structure

### Outcome: SUCCEEDED (important negative result)

**Individual zero reconstruction from the explicit formula fundamentally does not work.** Three key findings:
1. N_osc is a step function at zeros — prime sum (sine series) converges to midpoint (Gibbs phenomenon), giving irreducible 0.5 offset
2. At smooth zeros, N_osc is ALWAYS exactly ±0.5 (mathematical identity). Linearized correction has constant magnitude, destroying level repulsion.
3. More primes = WORSE individual reconstruction (variance explained: 80% at P_max=10, -6% at P_max=10000)

**BUT: Sign prediction is 100% accurate** (primes know which side the zero is on).
**AND: Number variance improves 75%** (primes help bulk statistics).

### Key Takeaway
The trace formula relates primes to the counting function N(T), NOT to individual zero positions. The Berry-Keating operator, if it exists, contains MORE information than the trace formula — its eigenvectors and matrix elements determine GUE correlations, not primes alone. "The primes determine SPECTRAL DENSITY but not SPECTRAL CORRELATIONS."

### Computations Identified
1. Non-linear reconstruction with regularized summation (Cesaro/Abel to tame Gibbs)
2. Spectral determinant approach (bypass counting function entirely)
3. Two-point trace formula for pair correlation (primes → correlations?)

## Exploration 005: Two-Point Correlation from Prime Pairs (FAILED)

### Goal
Compute Montgomery's pair correlation formula from primes and compare to numerical pair correlation from zeros.

### Outcome: TIMED OUT / CRASHED
Explorer tmux session was lost. Only a 33-line report skeleton exists. Code was written (prime sum and form factor computations) but never executed to completion. Partial data file (part1_results.npz) exists.

### What we know
- The prime sum for the form factor diverges and needs proper normalization (discovered before crash)
- The question remains open: do primes determine pair correlations through the two-point formula?

## Exploration 006: Arithmetic Operator Construction — Von Mangoldt Toeplitz Matrix

### Goal
Construct matrices from arithmetic functions (von Mangoldt Lambda, Mobius mu), compute eigenvalues, classify spectral statistics.

### What Was Done
- Von Mangoldt Toeplitz at N=200, 500, 1000
- Normalized von Mangoldt Toeplitz at N=500
- Mobius Toeplitz at N=500
- Von Mangoldt Hankel at N=500

### Outcome: SUCCEEDED — Clear Classification

**All Toeplitz variants are Poisson** (beta ~ -0.3, flat pair correlation, no level repulsion). 0/4 constraints satisfied.

**Hankel variant is intermediate Poisson-GOE** (beta = 0.44, partial level repulsion). Number variance at L=10 accidentally matches GUE.

### Key Takeaway
Simply encoding primes into a matrix does NOT produce GUE statistics. Matrix structure (Toeplitz vs Hankel) matters more than arithmetic content. Real symmetric matrices can only reach GOE (beta=1), never GUE (beta=2). Complex entries are required for GUE.

### Unexpected Finding
Toeplitz vs Hankel dichotomy: same function Lambda(n), same size, but Toeplitz → Poisson while Hankel → partial GOE.


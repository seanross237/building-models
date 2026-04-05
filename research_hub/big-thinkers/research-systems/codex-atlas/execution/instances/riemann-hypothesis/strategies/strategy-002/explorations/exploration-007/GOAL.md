# Exploration 007 — Adversarial Review of C1 Pair Correlation Claim

## Mission Context

You are a Math Explorer in an Atlas research system investigating whether arithmetic operators can be constructed whose eigenvalue spectra approximate Riemann zeta zeros. This is Exploration 007 of Strategy 002 for the Riemann Hypothesis mission.

## Your Task: Adversarial Review

Play devil's advocate against the primary finding of this mission so far:

**CLAIM: "The C1 random-phase Von Mangoldt Hankel matrix satisfies Montgomery's pair correlation formula at the 7.9% MRD level, suggesting it captures the two-point spectral statistics of GUE."**

Your job is to ATTACK this claim. Run three specific tests to determine if the claim is ESTABLISHED, SUPPORTED, SPECULATIVE, or REFUTED.

## Background: What C1 Is

C1 construction (from S002-E001/E005):
```python
# N=500 Hermitian matrix
# H_{jk} = Λ(|j-k|+1) × exp(2πi φ_{jk})
# Where Λ(n) = log(p) if n=p^m, else 0 (Von Mangoldt function)
# And φ_{jk} are iid Uniform[0,1] (independent random phases)
```

Results from 5 realizations (N=500):
- Pair correlation MRD = 7.9% → PASS (vs Montgomery R₂(r) = 1 - (sin(πr)/πr)²)
- β_Wigner = 1.18 ± 0.22 (PARTIAL — target β=2.0)
- KS_GUE = 0.042 → PASS
- Δ₃ saturation = 0.285 (PARTIAL — GUE gives 0.565, zeta gives 0.156)
- Full scorecard: 3 PASS, 4 PARTIAL, 0 FAIL

Zeta zeros baseline (2000 zeros): pair correlation MRD = 9.1% vs Montgomery formula.

## The Three Adversarial Tests

### Test 1: Null Matrix (MOST IMPORTANT)

**Question:** Does the Von Mangoldt amplitude structure actually matter for the pair correlation result, or does ANY complex Hermitian matrix with random phases achieve comparable MRD?

**Compute pair correlation MRD for three null matrices at N=500, 5 realizations each:**

**(a) GUE control:** H = (A + A†)/√(2N), where A is N×N complex Gaussian. This is a properly normalized GUE matrix.

**(b) Flat-amplitude random phase:** H_{jk} = exp(2πi φ_{jk}) (no Von Mangoldt weight). Hermitian: H_{jk} = exp(2πi φ_{jk}) for j<k, H_{kj} = H_{jk}^*, H_{jj} = 0. The question is: does this already pass pair correlation at ≤10% MRD?

**(c) Flat-amplitude but using Hankel structure (control for structure):** H_{jk} = 1 × exp(2πi ψ_{|j-k|}). (Toeplitz random phase — should be Poisson by phase factorizability but let's confirm.)

For each null matrix, compute pair correlation MRD exactly as for C1 (see formula below).

**Verdict:**
- If null (a) or (b) achieves MRD ≤ 10%: the Von Mangoldt structure is unnecessary → claim is WEAKENED (GUE statistics are generic, not specific to C1)
- If null (a) ≤ 10% but null (b) > 10%: Von Mangoldt matters but random GUE also passes → claim is COSMETIC (C1 is GUE class, but the arithmetic content isn't doing the work)
- If all nulls > 10% but C1 = 7.9%: Von Mangoldt genuinely matters → claim is STRENGTHENED

### Test 2: Realization Stability

**Question:** Is MRD=7.9% stable, or was it a lucky estimate from 5 realizations?

**Compute:** Run 20 independent C1 realizations at N=500. Report:
- Mean MRD and standard deviation
- Fraction of realizations with MRD ≤ 10%
- 90th percentile of MRD

**Verdict:**
- If mean ± std is entirely within ≤10%: claim is STABLE
- If some realizations exceed 10%: state the fraction and whether 7.9% is unusually good
- If mean > 10%: claim is REFUTED (the 5-realization average was lucky)

### Test 3: Severity Assessment

After computing tests 1 and 2, fill out this table:

| Attack | Severity | Evidence | Verdict |
|---|---|---|---|
| "Von Mangoldt amplitude unnecessary" | FATAL/SERIOUS/MODERATE/COSMETIC | [result from Test 1] | ESTABLISHED/SUPPORTED/SPECULATIVE/REFUTED |
| "7.9% MRD not stable" | FATAL/SERIOUS/MODERATE/COSMETIC | [result from Test 2] | ... |
| "GUE class doesn't mean Riemann-like" | SERIOUS/MODERATE | β=1.18 vs target 2.0; Δ₃=0.285 vs zeta 0.156 | ESTABLISHED |
| "3/10 PASS scorecard is not strong evidence" | MODERATE/COSMETIC | Full scorecard: 3 PASS, 4 PARTIAL | ... |
| "Pair correlation insensitive to structure" | SERIOUS/MODERATE | [MRD for GUE control] | ... |

Severity definitions:
- **FATAL:** If true, the claim is refuted entirely
- **SERIOUS:** Significantly weakens the claim; requires clarification in any publication
- **MODERATE:** Noteworthy limitation; should be mentioned as caveat
- **COSMETIC:** Real but doesn't change the core conclusion

## Exact Formulas (use these precisely)

### Pair Correlation R₂(r) — [MUST USE THIS FORMULA]

From 5 realizations of C1 (or null matrices), for each realization:
1. Compute all N(N-1)/2 pairwise separations of unfolded eigenvalues (after degree-5 polynomial unfolding)
2. Bin into histogram with dr = 0.05 from r=0 to r=6
3. Normalize: R₂_computed(r) = (count in bin) / (N × dr)
4. Compare to R₂_Montgomery(r) = 1 - (sin(πr)/(πr))²
5. MRD = mean(|R₂_computed(r) - R₂_Montgomery(r)| / R₂_Montgomery(r)) over r ∈ [0.5, 4.0]

Average R₂_computed over 5 (or 20) realizations before computing MRD.

### β_Wigner Fitting

Use the Brody distribution P(s) = (1+β) B s^β exp(-B s^{β+1}) where B = Γ((β+2)/(β+1))^{β+1}. Fit via chi-squared minimization over s ∈ [0.05, 3.0] with 30 bins.

**scipy fallback:** If `scipy.optimize` throws `ImportError: cannot import name 'Inf' from 'numpy'`, use manual grid search:
```python
beta_grid = np.linspace(0, 3, 61)
best_beta, best_chi2 = 0.0, 1e9
for beta in beta_grid:
    B = gamma((beta+2)/(beta+1))**(beta+1)
    theory = (1+beta)*B*s_centers**beta*np.exp(-B*s_centers**(beta+1))
    theory /= theory.sum() * ds
    chi2 = np.sum((hist_counts/hist_counts.sum() - theory/theory.sum())**2 / (theory/theory.sum() + 1e-10))
    if chi2 < best_chi2:
        best_chi2, best_beta = chi2, beta
```

## Success/Failure Criteria

**SUCCESS:** You complete all three tests and produce a severity table with quantitative evidence for each attack.

**PARTIAL SUCCESS:** You complete at least Test 1 (null matrices) and Test 3 (severity assessment) even if Test 2 (stability) is incomplete.

**FAILURE:** You cannot compute the null matrix comparison.

The primary question to answer: **"Is the 7.9% pair correlation MRD a meaningful result that depends on the Von Mangoldt structure, or is it a generic property of any GUE-class Hermitian matrix?"**

## Output Requirements

Write all results to this directory:
- `code/adversarial_test.py` — main computation
- `code/results.npz` — all numerical results
- `REPORT.md` — full report with tables
- `REPORT-SUMMARY.md` — 1-page summary (write this LAST)

The REPORT-SUMMARY.md signals completion. Write it only when everything else is done.

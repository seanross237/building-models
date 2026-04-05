# Exploration 004: N²/p Scaling Universality for Gauss Sum Matrices

## Mission Context

We are investigating whether the Gauss sum matrix H_{jk} = Λ(|j−k|+1) × exp(2πijk/p) can produce GUE-like statistics. Strategy-002 Exploration-005 found that at N=500, the peak Brody β = 1.154 occurs at p=809 (N²/p = 309). The claim "N²/p ≈ 250–310 is a universal constant" has been flagged as PREMATURE because only N=500 has been tested.

**Goal:** Test N=250 and N=1000 to determine whether N²/p_opt ≈ 275 holds universally, or whether the constant is N-dependent.

## Working Directory

Your working directory is `explorations/exploration-004/` (relative to the strategy directory). All code, data, and reports go here.

---

## Background

### The Matrix

```python
# 1-INDEXED (critical — 0-indexed breaks the baseline reproduction)
H = np.zeros((N, N), dtype=complex)
for j in range(1, N+1):
    for k in range(1, N+1):
        amplitude = von_mangoldt(abs(j-k) + 1)  # Λ(|j-k|+1)
        phase = np.exp(2*np.pi*1j * j * k / p)
        H[j-1, k-1] = amplitude * phase
H = (H + H.conj().T) / 2  # Hermitianize
```

The von Mangoldt function: Λ(n) = log(p) if n=p^k for some prime p and k≥1, else 0.

### What S002 Found at N=500

| p | N²/p | β (Brody) |
|---|------|-----------|
| 97 | 2577 | 0.930 |
| 251 | 996 | 0.581 |
| 499 | 501 | 0.776 |
| **809** | **309** | **1.154** (PEAK) |
| 997 | 251 | 1.092 |
| 9973 | 25 | 0.744 |
| 99991 | 2.5 | 0.108 |

**Key pattern:** β peaks sharply at N²/p ≈ 250–310. If universal: N=250 should peak near p ≈ 250²/275 ≈ 227; N=1000 should peak near p ≈ 1000²/275 ≈ 3636.

### Brody Distribution

The Brody parameter β interpolates between Poisson (β=0) and Wigner-Dyson GUE (β=2):
```
ρ(s) = (1+β) × b × s^β × exp(−b·s^(β+1))
b = [Γ((β+2)/(β+1))]^(β+1)
```
β=0: Poisson, β=1: GOE, β=2: GUE.

**scipy.optimize IS BROKEN** (numpy.Inf removed). Use manual Brody fit:
```python
from scipy.optimize import minimize

def brody_cdf(s, beta):
    b = gamma((beta+2)/(beta+1))**(beta+1)
    return 1 - np.exp(-b * s**(beta+1))

def neg_log_likelihood(params, spacings):
    beta = params[0]
    if beta <= 0 or beta >= 3: return 1e10
    b = gamma((beta+2)/(beta+1))**(beta+1)
    pdf = (1+beta)*b*spacings**beta * np.exp(-b*spacings**(beta+1))
    pdf = np.clip(pdf, 1e-300, None)
    return -np.sum(np.log(pdf))

result = minimize(neg_log_likelihood, x0=[1.0], args=(spacings,),
                  method='Nelder-Mead', options={'xatol':1e-5})
beta_fit = result.x[0]
```

---

## Tasks

### Task 1: Replicate N=500 Baseline [SECTION COMPLETE when done]

Before testing new N values, replicate the known N=500 result to confirm your code is correct:
- Test p ∈ {499, 809, 997}
- Compute eigenvalue spacings for each (excluding 5% outliers at each tail)
- Fit Brody β for each
- PASS criterion: β(p=809) in range [1.05, 1.25] and β(p=499) in range [0.70, 0.85]

If FAIL: debug the matrix construction. Most likely cause is wrong indexing (0-indexed vs. 1-indexed shifts β by 0.3–0.5).

Save: `np.savez('baseline_N500.npz', p_values=[499,809,997], beta_values=[...])`

**Write Task 1 results to REPORT.md before proceeding.**

### Task 2: N=250 Sweep [SECTION COMPLETE when done]

Test N=250 with p values chosen to span N²/p ∈ {25, 100, 200, 230, 250, 280, 310, 500, 1000, 2500}:
- N²/p=250 → p=250 (prime nearby: p=251)
- N²/p=280 → p≈223 (prime: p=223)
- N²/p=310 → p≈202 (prime: p=199)
- N²/p=100 → p=625 (prime: p=619)
- N²/p=500 → p=125 (prime: p=127)
- N²/p=25 → p=2500 (prime: p=2503)

For each p:
1. Construct H (N=250, 1-indexed)
2. Compute eigenvalues (np.linalg.eigvalsh)
3. Unfold: divide by mean spacing
4. Compute nearest-neighbor spacing distribution
5. Fit Brody β

Record: p, N²/p, β. Find p_opt where β is maximum.

Save: `np.savez('sweep_N250.npz', p_values=..., N2_over_p=..., beta_values=...)`

**Write Task 2 results to REPORT.md before proceeding.**

### Task 3: N=1000 Sweep [SECTION COMPLETE when done]

Test N=1000 with p values chosen to span N²/p ∈ {25, 100, 200, 250, 280, 310, 500, 1000}:
- N²/p=280 → p=1000²/280≈3571 (prime: p=3571)
- N²/p=250 → p=4000 (prime: p=3989)
- N²/p=310 → p=3226 (prime: p=3229)
- N²/p=100 → p=10000 (prime: p=9973)
- N²/p=500 → p=2000 (prime: p=1999)

**Warning:** N=1000 eigenvalue computation takes ~5-10 minutes per matrix. Test no more than 6-8 p values. Use `np.linalg.eigvalsh` (symmetric) — it's ~3× faster than `eigvals`.

Save: `np.savez('sweep_N1000.npz', p_values=..., N2_over_p=..., beta_values=...)`

**Write Task 3 results to REPORT.md before proceeding.**

### Task 4: Universality Assessment [SECTION COMPLETE when done]

From Tasks 1–3, extract:
- p_opt(N=250): p where β is maximized
- p_opt(N=500) = 809 (known from S002)
- p_opt(N=1000): p where β is maximized

Compute:
- N²/p_opt for each N
- β_peak for each N

**Question 1 (Universality):** Is N²/p_opt ≈ constant across N ∈ {250, 500, 1000}?
- If all three N²/p_opt fall in [200, 400]: UNIVERSAL (strong claim)
- If they differ by >50%: N-DEPENDENT (claim must be revised)

**Question 2 (β peak height):** Does β_peak increase, decrease, or stay constant as N increases?
- β_peak(N=500) ≈ 1.154 (GOE-class, less than GUE=2)
- If β_peak(N=1000) > 1.3: might be converging toward GUE
- If β_peak saturates at ≈1.1–1.2: permanently GOE-class

**Question 3 (Comparison to Fyodorov-Mirlin):** For random band matrices, the Poisson→GOE transition occurs at W²/N ≈ 1. The Gauss sum analog would be N²/p_opt ≈ ? Compare.

Save: `np.savez('universality_results.npz', N_values=[250,500,1000], p_opt=..., N2_over_p_opt=..., beta_peak=...)`

**Write Task 4 results to REPORT.md before proceeding.**

---

## Success Criteria

**Success (Strong):** N²/p_opt is constant ≈ 250–310 for all three N values → universality confirmed, the ratio is a genuine property of the matrix class.

**Success (Moderate):** N²/p_opt varies but follows a clear power law N^α → systematic understanding of the N-dependence.

**Failure:** N²/p_opt is essentially random (no trend) → the claim is an artifact of the single N=500 data point.

**Bonus (if time allows):** Test whether β_peak is converging to GUE (β=2) as N→∞ or saturating below 2.

---

## Key Reference Values

- N=500, p=809: β=1.154 (this is your verification target)
- N=500, p=499: β=0.776
- N=500, p=997: β=1.092 (also near peak)
- GUE: β=2, GOE: β=1, Poisson: β=0
- Fyodorov-Mirlin transition for random band matrices: W²/N ≈ 1 (different class but structurally analogous)

## Timing Notes

- N=250: eigenvalue computation ~0.5 min/matrix, expect ~5 min total
- N=500: eigenvalue computation ~2 min/matrix, known β values from S002
- N=1000: eigenvalue computation ~8-10 min/matrix, plan for 60+ min total
- Use `np.linalg.eigvalsh` (Hermitian-optimized), not `np.linalg.eig`

## Output Required

Write `REPORT.md` incrementally — after EACH task, write that section's results before starting the next.

At the end, write `REPORT-SUMMARY.md` (150–300 words): universality verdict, the three N²/p_opt values, whether β_peak is converging to GUE, recommendation for next step.

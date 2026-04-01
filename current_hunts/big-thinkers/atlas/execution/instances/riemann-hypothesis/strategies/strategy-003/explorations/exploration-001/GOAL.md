# Exploration 001: Off-Diagonal Form Factor and Predicted Δ₃

## Mission Context

You are working on the Riemann Hypothesis. The mission is to understand the spectral statistics of Riemann zeta zeros and construct operators whose eigenvalues reproduce them.

**The central unsolved problem:** Zeta zeros have spectral rigidity Δ₃_sat = 0.155. The best matrix construction (random-phase GUE-class matrix at N=500) achieves Δ₃_sat ≈ 0.243. This is a 40% gap. No construction in 18 prior explorations has closed it.

**Why the gap exists (theoretical prediction):** Berry (1985) showed that the diagonal approximation to the form factor — K_diag(τ) = τ for τ<1, K_diag=1 for τ≥1 — explains the GUE-level ramp but NOT the plateau or saturation. The saturation to Δ₃=0.155 requires the *off-diagonal* periodic orbit pairs (correlated prime pairs), which encode Hardy-Littlewood-type correlations between primes. GUE matrices contain only diagonal orbit structure. The off-diagonal corrections are what makes zeta zeros MORE rigid than GUE.

**Your goal:** Compute the off-diagonal form factor correction K_off-diag(τ) from the literature, add it to K_diag to get the full K(τ), and use the Dyson-Mehta relation to predict Δ₃_sat. Compare to 0.155.

## What Has Already Been Established (Do Not Redo)

- **Δ₃_sat(zeta) = 0.1550 ± 0.0008** (measured from 2000 zeta zeros, confirmed in two strategies)
- **Δ₃_sat(GUE, N=500) = 0.23–0.26** (NOT the infinite-N GUE theory value of 0.566!)
- **Berry's formula (1/π²)log(log(T/2π)) confirmed to 7.6%** — predicts 0.155 correctly
- **K_diag(τ) from prime sums confirmed** (MAD=14.5% vs K_zeros) — diagonal ramp is established
- **K_diag fails for τ>1** — no plateau mechanism; diagonal approximation gives GUE, not super-rigidity

These are ground truth. You need NOT recompute them.

## Your Task

### Step 1: Extract the Off-Diagonal Formula

Access the following papers (via web search, arXiv, or any means available):

**Primary target:**
- Berry, M.V. (1985). "Semiclassical theory of spectral rigidity." *Proc. R. Soc. Lond. A* 400, 229-251.
  - Focus on Section 5 and Section 6 where Berry discusses the off-diagonal orbit pairs
  - Look for the formula: K(τ) = K_diag(τ) + K_off-diag(τ)
  - The off-diagonal term should involve sums over pairs of periodic orbits with correlated actions

**Secondary targets (if Berry 1985 formula is inaccessible):**
- Bogomolny, E.B. & Keating, J.P. (1996). "Gutzwiller's trace formula and spectral statistics: beyond the diagonal approximation." *Phys. Rev. Lett.* 77, 1472-1475.
- Keating, J.P. & Snaith, N.C. (2000). "Random matrix theory and ζ(1/2+it)." *Comm. Math. Phys.* 214, 57-89.
- Berry, M.V. & Keating, J.P. (1999). "The Riemann zeros and eigenvalue asymptotics." *SIAM Rev.* 41, 236-266.

**What to extract:** The specific mathematical formula for K_off-diag(τ). This should be something like a sum over prime pairs p, p' of the form Λ(p)Λ(p') × [correlation factor] / N_pairs, where the correlation factor encodes prime pair correlations (Hardy-Littlewood twin prime conjecture type).

**If the formula involves Hardy-Littlewood twin prime constants:** Note which specific constants are used. The standard Hardy-Littlewood constant for twin primes is C₂ ≈ 1.32032 (the twin prime constant). For general prime pairs with offset k, C(k) = 2C₂ × Π_{p|k,p>2} (p-1)/(p-2).

**If you find multiple formulations:** Implement BOTH and report results from each.

### Step 2: Implement K_diag(τ)

```python
def K_diag(tau):
    """GUE diagonal approximation"""
    if tau < 1:
        return tau
    else:
        return 1.0  # plateau
```

Also implement using the prime sum (already established in prior explorations):
- T = 1682.0 (height of the 1000th zero approximately)
- rho_bar = log(T / (2*pi)) / (2*pi)  # mean density
- K_diag_primes(tau) = sum over primes p of (log(p))^2 * [cos terms] / (2*pi*rho_bar*tau_H)^2

Use the exact formula confirmed in prior explorations: K_density = (1/(4*pi²)) * |Σ_p Λ(p) * exp(-2πi * τ * log(p) / τ_H)|² where τ_H = 2π/rho_bar is the Heisenberg time and K_primes = K_density / (2πρ̄)².

### Step 3: Implement K_off-diag(τ)

Using the formula from Step 1. Code it up in Python/mpmath.

**IMPORTANT normalization guidance:** Based on confirmed convention from prior explorations:
- The form factor is normalized so K_diag(τ) → τ for small τ (GUE ramp)
- The off-diagonal correction must be normalized consistently with this
- If the formula gives K(τ=0) → 0 and K(τ=∞) → 1, that's the correct normalization
- If both K_diag and K_off-diag have the same normalization, K_total = K_diag + K_off-diag should not be re-normalized

### Step 4: Compute K_total(τ) = K_diag(τ) + K_off-diag(τ)

Compute for τ ∈ [0, 5] with N_tau = 100 points. Use T = 1682 (height of ~1000th zero) throughout.

### Step 5: Compute Predicted Δ₃(L) via Dyson-Mehta Relation

The spectral rigidity Δ₃(L) is related to the two-point cluster function Y₂(r) and the form factor K(τ):

**Route 1 (via Y₂):**
The pair correlation function R₂(r) = 1 - Y₂(r), and for GUE: Y₂(r) = (sin(πr)/πr)². The form factor and cluster function are related by: b₂(r) = ∫₀^∞ K(τ) exp(2πiτr) dτ (or similar — check the Berry 1985 paper for the exact relation).

Then Δ₃(L) = (2/L⁴) ∫₀^L (L³ - 2L²r + r³) [1 - b₂(r)] dr where b₂(r) = ∫ K(τ) cos(2πτr) dτ.

**Route 2 (direct from K(τ)):**
Berry (1985) gives the direct Dyson-Mehta formula:
Δ₃(L) = L/15 - (1/2π²L) ∫₀^∞ [(sin(πLτ))/(πτ)]² / (πτ)² × g(τ) dτ

where g(τ) relates to K(τ). Extract the exact formula from the paper.

**If you cannot find the exact Dyson-Mehta formula:** Use the Fourier route:
1. Compute b₂(τ) = K(τ) - 1 + δ(τ) [the connected part]
2. b₂(r) = ∫ b₂(τ) cos(2πτr) dτ (Fourier transform in the unfolded coordinate)
3. Y₂(r) = 1 - R₂(r) where the cluster function relates to b₂
4. Δ₃(L) = (2/L⁴) ∫₀^L (L³ - 2L²r + r³) Y₂(r) dr

Document which route you used and why.

### Step 6: Compare Predicted Δ₃_sat to 0.155

- What is the predicted Δ₃ at L = 20 (saturation regime)?
- What is the percentage error: |predicted - 0.155| / 0.155 * 100%
- Does the off-diagonal correction REDUCE Δ₃ from the GUE value toward 0.155?
- What fraction of the gap is closed: (Δ₃_diag - Δ₃_total) / (Δ₃_diag - 0.155)?

### Step 7: Test at Different Height T

Repeat Steps 4-6 at T = 600 (height of ~200th zero, lower T) and T = 3000 (higher T).

- Does the predicted Δ₃_sat change with T?
- Berry's formula predicts Δ₃_sat = (1/π²)log(log(T/2π)), which increases with T
- Does your computed Δ₃_sat from K_total(τ) show the same T-dependence?

## Confirmed Formulas (Do NOT Change These)

**Δ₃ formula (use the integral form, NOT the sum form — the sum form gives approximately half the correct value):**
```
Δ₃(L) = (1/L) × min_{a,b} ∫₀ᴸ [N(x) − ax − b]² dx

Analytic form for eigenvalues y₁ < ... < yₙ sorted in [0, L]:
I₀ = n·L − Σyₖ
I₁ = n·L²/2 − (1/2)Σyₖ²
I₂ = n²·L − Σ(2k-1)yₖ
F_min = I₂ − I₀²/L − 12(I₁ − I₀L/2)²/L³
Δ₃(L) = F_min / L
```

**Sanity check targets:**
- GUE random matrix N=500: Δ₃_sat ≈ 0.23–0.26 (NOT 0.566!)
- Zeta zeros: Δ₃_sat = 0.155 ± 0.001
- GUE theoretical (infinite N): Δ₃_sat = (1/π²)log(L/2π²) - 0.0687... grows logarithmically

## Success and Failure Criteria

### This exploration SUCCEEDS if:
1. You extract a specific formula for K_off-diag(τ) from the literature
2. You compute a specific predicted Δ₃_sat value (a NUMBER, not "approximately reduced")
3. You quantify the percentage match to 0.155

### This exploration PARTIALLY SUCCEEDS if:
- The formula is found but the numerical integral doesn't converge reliably
- The formula requires inputs (Hardy-Littlewood constants) that are conjectural — note this explicitly
- The predicted Δ₃_sat changes direction (reduces toward 0.155) but the magnitude doesn't match

### This exploration FAILS if:
- The off-diagonal formula cannot be found in the referenced papers (after genuine search)
- The computation is numerically unstable or the integral diverges
- The formula is trivially circular (predicts 0.155 by construction because it was derived FROM zeta zeros — note this explicitly if it's the case)

**CRITICAL:** If the off-diagonal formula is circular (derived from assuming RH), report this as a FINDING, not a failure. It would be the first explicit demonstration of circularity in this framework.

## Warning: Known Pitfalls

1. **Normalization**: K(τ=0) behavior and K(τ→∞) behavior determine the normalization. Check that K_diag → τ for small τ and K_total → 1 for large τ.

2. **Numerical integration**: The Dyson-Mehta integral has an oscillating integrand. Use enough quadrature points (N ≥ 1000). Check convergence by halving the grid.

3. **scipy.optimize is BROKEN** in this environment (numpy.Inf removed). Do not use scipy.optimize for any fits. Use explicit formula fits if needed.

4. **Two normalization variants exist** for Berry's formula: (1/π²) vs (1/2π²). The confirmed correct one is (1/π²). If you encounter the other, implement both and report.

5. **The sum form of Δ₃ gives ~half the correct value.** Always use the integral form (formula given above).

## Required Output Structure

Write REPORT.md in this directory. Mark each section complete before moving to the next:

```
## Section 1: Off-Diagonal Formula Extraction [SECTION COMPLETE or FAILED]
## Section 2: K_diag Implementation [SECTION COMPLETE or FAILED]
## Section 3: K_off-diag Implementation [SECTION COMPLETE or FAILED]
## Section 4: K_total Computation [SECTION COMPLETE or FAILED]
## Section 5: Δ₃ Prediction [SECTION COMPLETE or FAILED]
## Section 6: Height Dependence Test [SECTION COMPLETE or FAILED]
## Section 7: Summary and Interpretation [SECTION COMPLETE or FAILED]
```

**Write each section to REPORT.md IMMEDIATELY after completing it, before starting the next section.**

Save all intermediate computation arrays (.npz files) after each numerical step.

Write REPORT-SUMMARY.md last — a concise 1-page summary of what you found and what it means.

## Exploration Directory

Your working directory: `explorations/exploration-001/` within the strategy-003 directory.
Put all code in `code/` subdirectory.

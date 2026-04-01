# Computation Registry

Computations identified during explorations that would significantly advance the mission. Maintained by the strategizer, read by the missionary and future strategizers.

## 1. Number Variance Sigma^2(L) Computation
- **What:** Count zeros in sliding windows of length L (unfolded coordinates), compute variance, compare to GUE prediction Sigma^2(L) ~ (2/pi^2)(log(2*pi*L) + gamma + 1 - pi^2/8)
- **Why:** Probes long-range correlations where Berry predicts saturation effects. Different from pair correlation — sensitive to non-universal corrections.
- **Would resolve:** Whether there are deviations from GUE at long range (which would constrain the periodic orbit structure of the Riemann operator)
- **Source:** Exploration 001
- **Difficulty:** Easy (~50-line numpy script, uses same 2000 zeros)
- **Key references:** Berry (1985) "Semiclassical theory of spectral rigidity", Bogomolny & Keating (1996)

## 2. Exact GUE Spacing Distribution (Fredholm Determinant)
- **What:** Replace Wigner surmise with exact GUE spacing distribution (Fredholm determinant of sine kernel), compare to zeta zero spacings
- **Why:** Exploration 001's KS test marginally rejected Wigner surmise at 5%. Need to distinguish Wigner approximation error from real signal.
- **Would resolve:** Whether the marginal KS failure is an artifact of the Wigner approximation or a genuine departure from GUE
- **Source:** Exploration 001
- **Difficulty:** Medium (~100-line script using Bornemann's method or Gaudin's recursion)
- **Key references:** Bornemann (2010) "On the numerical evaluation of Fredholm determinants", Mehta (2004) "Random Matrices"

## 3. Large-Scale Zero Computation (Odlyzko-Schonhage Algorithm)
- **What:** Implement Riemann-Siegel formula + FFT to compute 10^5-10^6 zeros at heights t ~ 10^6
- **Why:** Would sharpen all GUE statistics by 10-30x, enable definitive GSE exclusion, and test height-dependence of GUE match
- **Would resolve:** Whether GUE agreement improves at large height (as Odlyzko's published results suggest), sharpen GSE exclusion from 1.2x to definitive
- **Source:** Exploration 001
- **Difficulty:** Hard (~500-line specialized script)
- **Key references:** Odlyzko (1987, 2001), Odlyzko & Schonhage (1988)

## 4. Height-Resolved Saturation Analysis
- **What:** Bin the 2000 zeros by height (e.g., T < 500, 500 < T < 1500, T > 1500), compute Sigma^2(L) separately for each bin. Test whether saturation scale L_max increases with height as Berry predicts.
- **Why:** Exploration 002 found saturation onset at L~2-5, earlier than Berry's L_max~100 for geometric mean height. This could be due to height mixing or indicate stronger-than-expected prime orbit corrections.
- **Would resolve:** Whether the early saturation onset is a height-mixing artifact or a genuine physical effect
- **Source:** Exploration 002
- **Difficulty:** Easy (~30-line extension of existing code)
- **Key references:** Berry (1985), exploration 002 analysis code

## 5. Quantitative Comparison to Berry's Explicit Saturation Formula
- **What:** Berry (1985) gives an explicit formula for saturated Sigma^2 in terms of sums over primes. Compute this theoretical prediction and compare to our measured saturation values (Sigma^2 ~ 0.3-0.5).
- **Why:** Would test quantitative, not just qualitative, correctness of Berry's theory. If the predicted saturation value matches, it confirms the prime orbit interpretation.
- **Would resolve:** Whether the EXACT saturation level matches Berry's prediction, or whether there's an unexplained quantitative discrepancy
- **Source:** Exploration 002
- **Difficulty:** Medium (~50-line script plus formula extraction from Berry's paper)
- **Key references:** Berry (1985) eq. 3.15 or similar, Bogomolny & Keating

## 7. Fix Pair Correlation Normalization + Δ₃ Formula (Strategy-002 Identified)
**STATUS: COMPLETED in S002-E005**
- C1 pair correlation MRD = 7.9% (PASS). C1 Δ₃ saturation = 0.285 (~50% of GUE).
- Correct formulas: R₂(r) = density estimate with dr=0.05 normalization; Δ₃ = staircase integral via window minimization.

## 8. Gauss Sum Phase Sweep: Large Primes (Strategy-002 Identified)
**STATUS: COMPLETED in S002-E005**
- β does NOT → 2 as p → ∞. β peaks at p=809 (β=1.154) then collapses. p=99991 gives β=0.086 (near Poisson).
- Pattern: N²/p ≈ 250-310 is optimal. Gauss sums permanently GOE.

## 9. Complex Dirichlet Character Phases (Strategy-002 Identified)
**STATUS: COMPLETED + PROVED IMPOSSIBLE in S002-E006**
- Multiplicative χ(jk) construction: Hermitianizing gives Re(χ(j)χ(k)) = real matrix → GOE.
- Factorizable χ(j)χ*(k) = exp(i(g_j-g_k)) = D A D† → unitarily equivalent to real → GOE.
- Neither route can give GUE. Best β = 0.281 (χ_13). Algebraically proved, not just empirical.

## 10. Null Amplitude Test: Does Von Mangoldt Matter for Pair Correlation?
**STATUS: COMPLETED in S002-E007**
- Flat-amplitude random phase: MRD=6.8% (< C1's 7.9%). GUE control: 7.8%. Toeplitz GOE-class: 9.0%.
- Verdict: Von Mangoldt amplitude is UNNECESSARY for pair correlation pass. Result is due to GUE class membership alone.

## 11. Flat-Amplitude Δ₃ Test (S002 Identified)
- **What:** Compute Δ₃_sat for H_{jk} = exp(2πi φ_{jk}) (flat amplitude, random complex phases) vs C1 (Von Mangoldt amplitudes + random phases). C1 gives Δ₃_sat=0.285 (intermediate, between GUE=0.565 and zeta=0.156).
- **Why:** E007 showed Von Mangoldt amplitude is NOT needed for pair correlation. Does removing it also destroy the anomalous intermediate Δ₃ rigidity? If flat-amplitude gives Δ₃≈0.565 (GUE), the Von Mangoldt structure IS causing the anomaly. If flat-amplitude also gives ≈0.285, the rigidity comes from GUE class membership alone.
- **Would resolve:** Whether the C1 anomalous Δ₃ is an arithmetic effect or a generic GUE-class property.
- **Source:** S002-E008 (highest priority recommendation for S003)
- **Difficulty:** Easy — same Δ₃ code as E005, replace Λ(n) amplitude with flat=1
- **Equations:** Δ₃(L) = min_{A,B} (1/L)∫₀ᴸ [N(x) - Ax - B]² dx; saturation at L=20-30

## 12. N-Scaling of N²/p Optimal Ratio (S002 Identified)
**STATUS: COMPLETED + REFUTED in S003-E004**
- Peak N²/p values: 225.6 (N=250), 309.0 (N=500), 200.0 (N=1000) — 1.5× spread, NO convergence
- Peak β_max DECREASES with N: 1.318 → 1.154 → 1.019 — finite-size effect, not universal law
- S002 used Wigner interpolated distribution (not Brody); "β=1.154" is Wigner β not Brody
- VERDICT: Gauss sum matrix N²/p scaling claim is an N=500 artifact. Approach eliminated.

## 15. Non-Perturbative K(τ) from Prime Pair Sums (S003-E001 identified)
- **What:** Compute K(τ) directly from the prime pair correlation sum (eq 4.18 in Berry-Keating 1999) WITHOUT the perturbative 1/⟨d⟩² expansion. Then compute Σ₂(L) = (2/π²)∫₀^∞ K(τ)/τ² sin²(πLτ) dτ and Δ₃(L) = (2/L⁴) ∫₀^L (L³-2L²r+r³) Σ₂(r) dr.
- **Why:** The perturbative Berry-Keating corrections (R¹_c, R²_c) blow up at T=1682 because ⟨d⟩=0.89 << 1 (expansion requires ⟨d⟩>>1, valid only for T>>10^{10}). The non-perturbative prime sum directly gives K(τ) without any asymptotic expansion.
- **Would resolve:** Whether the off-diagonal prime pair correlations CAN close the Δ₃ gap when computed non-perturbatively (not perturbatively in 1/⟨d⟩²)
- **Source:** S003-E001
- **Difficulty:** Medium — need Hardy-Littlewood twin prime constant implementation; sum over prime pairs
- **Key equations:** Berry-Keating (1999) eq 4.18: K(τ) = 1 + Σ_{p,p' prime pairs} contribution; b(ξ) = Π_p(1-(p^{iξ}-1)²/(p-1)²); Σ₂ and Δ₃ as above

## 16. Off-Diagonal Corrections at High T (S003-E001 identified)
- **What:** Repeat the Berry-Keating perturbative computation (R¹_c, R²_c) using Odlyzko's zero tables at T~10^{12} where ⟨d⟩≈3.9. At this height, the perturbative expansion should be valid.
- **Why:** The perturbative approach failed at T=1682 (⟨d⟩=0.89), but at T=10^{12} the expansion parameter 1/⟨d⟩² ≈ 0.07 << 1 and the approach should work.
- **Would resolve:** Whether the off-diagonal corrections DO close the gap at high T (which would confirm Berry-Keating theory), or if the gap persists even in the perturbative regime
- **Source:** S003-E001
- **Difficulty:** Hard — requires Odlyzko zero tables and high-precision computation at T~10^{12}
- **Key equations:** Same as S003-E001 but with T=10^{12}, ⟨d⟩=3.9

## 13. Li Coefficients at Large n (S003-E002 identified)
- **What:** Compute λ_n for n=1 to 5000 using 10,000+ zeta zeros (requires zetazero caching)
- **Why:** The ratio λ_n^zeta/λ_n^GUE falls to 0.95 at n=500. Computing to n=5000 would show whether this divergence continues (suggesting arithmetic structure) or converges back to 1 (finite-size effect)
- **Would resolve:** Whether Li coefficient deviation from GUE is an artifact of truncation (2000 zeros) or a genuine signal of super-rigidity in Li space
- **Source:** S003-E002
- **Difficulty:** Medium (mainly time — ~1 hour for zeros, then fast λ_n calculation)
- **Key references:** Li (1997) Li-criterion; Bombieri-Lagarias (1999) asymptotics; Coffey (2004) refined asymptotics

## 14. Li Coefficient Phase Distribution Formalization (S003-E002 identified)
- **What:** Formalize the chain: |1-1/ρ| = 1 → convergence by phase cancellation → λ_n > 0 iff sum of cos(n·θ_k) > sum of 1 contributions
- **Why:** If this chain holds, Li's criterion reduces to a Fourier/equidistribution problem on the zero phases θ_k = arg((ρ_k-1)/ρ_k)
- **Would resolve:** Whether phase equidistribution (Weyl theorem-type) implies λ_n > 0 in some limit
- **Source:** S003-E002
- **Difficulty:** Hard (requires analytic number theory expertise for formalization)
- **Key references:** Li (1997); Weyl equidistribution theorem; Diophantine approximation

## 6. Precomputed Zero Tables (LMFDB)
- **What:** Download zeros from LMFDB database (zeros up to height ~10^10) and rerun all statistics with 10^4-10^6 zeros
- **Why:** Would dramatically improve statistical significance of all results. Would enable definitive GSE exclusion and sharper saturation measurements.
- **Would resolve:** All precision-limited questions from explorations 001-002
- **Source:** Exploration 002
- **Difficulty:** Easy-Medium (mainly data format parsing)
- **Key references:** LMFDB (https://www.lmfdb.org), Odlyzko tables


## 17. K(τ) from Prime Orbit Sums → Δ₃ Prediction (S003-E003 identified — highest priority)
**STATUS: PARTIALLY COMPLETED in S003-E006**
- Berry's direct formula confirmed: Δ₃_sat=(1/π²)log(log(T/2π)) gives 0.154 at T=600 (0.6% error), 0.167 at T=1127 (8% error). Formula explains the gap analytically.
- K→Σ₂ integral route has ~2x normalization error (see item 19 to fix).
- CORRECT weight: (log p)²/p^m (not (log p)² alone) — semiclassical amplitude factor required.
- K_primes with cap ≈ GUE within 3.3% via integral route — super-rigidity not visible at τ<1.
- **Verdict:** Prime structure DOES explain the gap, via Berry's closed-form. The integral route requires normalization fix (item 19).
- **What:** Compute K(τ) via Berry's diagonal approximation (prime periodic orbits): K_primes(τ) = (1/(2πρ̄)²) × Σ_{p,m} (log p)² × gauss(τ - m·log(p)/log(T/2π), σ). Then add saturation cap K(τ)=1 for τ>1 and compute predicted Δ₃ via Σ₂ route. Compare to measured Δ₃_sat=0.155.
- **Why:** E003 confirmed Δ₃_sat=0.155 but SKIPPED the prime orbit explanation (Tasks 3 and 5). The key question: does the diagonal prime approximation PREDICT Δ₃_sat=0.155 or 0.294? If K_primes+saturation gives 0.155, the prime structure explains the gap.
- **Would resolve:** Whether the Δ₃ gap is explained by the prime orbit structure — the central unsolved question.
- **Source:** S003-E003 (Tasks 3 and 5 skipped)
- **Difficulty:** Easy-Medium — same framework as S003-E003, add the prime sum loop
- **Key equations:** K_primes(τ) from primes p≤1500 (96% of weight), σ=0.1 smoothing; then Σ₂/Δ₃ via verified route

## 18. Flat Saturation Plateau — Is It Known? (S003-E003 identified)
- **What:** E003 found Δ₃(L) varies <1% from L=15 to L=30 for zeta zeros, while GUE continues growing logarithmically. Search Berry (1985), Bogomolny-Keating (1996), Odlyzko (1987, 2001) for documentation of this extreme flatness.
- **Why:** The flatness of Δ₃ plateau is a stronger constraint than its level. GUE only asymptotically approaches a constant; zeta zeros reach it by L≈15 with <1% variation.
- **Would resolve:** Whether the flat plateau is a known feature, a new observation, or a finite-sample artifact.
- **Source:** S003-E003 (Task 4)
- **Difficulty:** Easy — standard Explorer literature search

## 19. Fix K→Σ₂ Normalization (S003-E006 identified)
- **What:** E006 found that the formula Σ₂(L) = L - (2/π²)∫[1-K(τ)]/τ² sin²(πLτ)dτ gives ~2x too large values for GUE (Δ₃(L=10) = 0.491 vs known 0.226). Identify and fix the factor.
- **Why:** This normalization fix would allow validation of the K_primes → Δ₃ integral route and give a definitive numerical check of Berry's mechanism.
- **Would resolve:** Whether K_primes with saturation cap predicts Δ₃_sat ≈ 0.155 through the integral route (not just via Berry's closed-form formula).
- **Source:** S003-E006
- **Difficulty:** Easy — likely a factor of 2 from angular vs ordinary frequency convention in the Fourier transform
- **Key check:** After fix, GUE control should give Δ₃(L=10) ≈ 0.226, Δ₃(L=20) ≈ 0.261

## 20. Berry Formula at Higher T — Growing Discrepancy (S003-E006 identified)
- **What:** Berry formula gives 0.154 at T=600 (0.6% error) but 0.167 at T=1127 (8% error). Is this known? Does the formula require a finite-T correction, or does the measured Δ₃_sat underestimate at this height (N=2000 zeros insufficient)?
- **Why:** If the discrepancy grows with T, either Berry's formula has a correction term or our Δ₃ measurement is height-dependent in unexpected ways.
- **Would resolve:** Whether Berry's formula is asymptotically exact or has systematic error; whether T=600 is the "correct" effective height for our 2000-zero dataset.
- **Source:** S003-E006
- **Difficulty:** Medium — requires larger zero datasets (LMFDB) at T≈600 and T≈1127 separately

## 21. λ_n Ratio Convergence as K=N→∞ (S003-E008 identified — highest priority)
- **What:** Compute ratio λ_n^zeta(K) / λ_n^GUE(N=K) for K=N=500, 1000, 2000, 3000, 5000 (with ~50 GUE realizations each). Plot ratio vs K to find limit.
- **Why:** E008 found the ratio is 0.949 at K=N=2000 (7.3σ) but is truncation-sensitive: at K=4500 zeros vs FIXED N=2000 GUE, ratio > 1. The key question is whether lim_{K=N→∞} ratio = 1 (artifact) or converges to constant < 1 (genuine structural difference).
- **Would resolve:** Whether the λ_n^zeta/λ_n^GUE crossover is a genuine novel signal or a truncation artifact. This is the decisive test for the strategy's main novel claim.
- **Source:** Exploration 008 (S003)
- **Difficulty:** Medium — E008 computed zeros 1-5000 and partial results already cached. Need 50 GUE realizations at N=3000 and N=5000 (slow but feasible in ~30 min each). Key computation: for each K, use K zeros + K×K GUE matrices scaled to the same range.
- **Key data:** E008 cached zeros 1-5000 in `explorations/exploration-008/t_zeros_5k.npy` (or similar). GUE λ_n(N=2000) = 925.78 at n=500. λ_zeta(K=5000) = 935.20 at n=500.

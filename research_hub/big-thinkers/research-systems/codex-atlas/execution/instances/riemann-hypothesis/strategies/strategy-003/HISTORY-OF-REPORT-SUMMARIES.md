# Exploration History

## Exploration 001: Off-Diagonal Form Factor and Predicted Δ₃

**Status: PARTIAL SUCCESS**

**Goal:** Extract off-diagonal form factor formula from Berry-Keating (1999), compute K_total(τ), predict Δ₃_sat via Dyson-Mehta, compare to 0.155.

**Key Findings:**
- **R²_c (off-diagonal) closes only 1.6% of the Δ₃ gap** (0.211 → 0.210 at L=20 vs target 0.155)
- **R¹_c (diagonal correction) blows up**: perturbative expansion requires ⟨d⟩ >> 1, but ⟨d⟩ = 0.89 at T=1682. Expansion is INVALID at the heights used in prior explorations.
- **The perturbative regime threshold is very high**: Berry-Keating corrections valid only for T >> 10^{10}
- **Berry's closed-form formula still works**: (1/π²)log(log(T/(2π))) = 0.154 at T=600 (0.6% match to 0.155!), = 0.174 at T=1682 (12% high)
- **GUE ground truth confirmed**: Δ₃_GUE(N=500, L=20) = 0.217 ± 0.002
- **Correct Δ₃ formula verified**: Σ₂ → Δ₃ via kernel (L³−2L²r+r³), confirmed to 3% against GUE matrices
- **Off-diagonal formula extracted**: R²_c(x) = (1/(2(πρ̄)²)) × [-cos(2πx)/ξ² + |ζ(1+iξ)|² × Re{exp(2πix) × b(ξ)}] where b(ξ) = Π_p(1-(p^{iξ}-1)²/(p-1)²)

**Implication:** The Berry-Keating perturbative corrections cannot explain the super-rigidity gap at finite T. A non-perturbative approach (computing K(τ) directly from prime orbit sums) is needed.

**Lead:** Non-perturbative K(τ) from prime orbit sums — instead of 1/⟨d⟩² expansion, compute the full prime pair correlation sum and evaluate Δ₃ directly.

---

## Exploration 002: Li's Criterion — Computational Probing

**Status: SUCCEEDED**

**Goal:** Compute Li's criterion coefficients λ_n for n=1 to 500 using 2000 zeta zero pairs at 50-digit precision. Verify positivity, analyze asymptotic residuals, and search for patterns.

**Key Findings:**
- All 500 Li coefficients strictly positive (consistent with RH): λ_1 = 0.02265, λ_500 = 881.43
- **|1-1/ρ| = 1 exactly for zeros on the critical line** — convergence by phase cancellation, not amplitude decay. Each zero contributes 2(1 - cos(n·θ_k)) where θ_k ≈ 1/t_k.
- GUE-zeta Li coefficient correlation: 97.1%, but zeta has 5× higher residual std than GUE
- **λ_n^zeta/λ_n^GUE < 1 for n > 300, falling to 0.95 at n=500** — the super-rigidity appears in Li space
- Truncation convergence ratio r ≈ 0.646, uniformly across ALL n values
- No significant prime correlation in residuals (t=-1.33, not significant)
- FFT dominant period: 451 (but power dominated by linear growth, not oscillation)

**Novel Insight:** Li's criterion is fundamentally about Fourier properties of the zero phase distribution. An off-critical-line zero would break the unit-modulus property, potentially driving λ_n negative.

**Leads:**
- Compute to n=5000 with 10,000+ zeros
- Formalize the connection between phase equidistribution and λ_n > 0
- The λ_n^zeta/λ_n^GUE ratio at large n may quantify super-rigidity in a new way

---

## Exploration 003: Non-Perturbative K(τ) from Prime Pair Sums

**Status: SUCCESS**

**Goal:** Compute K(τ) non-perturbatively from pair correlations of zeta zeros and determine whether it predicts Δ₃_sat ≈ 0.155.

**Key Findings:**
- **Δ₃_sat = 0.1545 CONFIRMED** via direct sliding-window least-squares from 2000 unfolded zeta zeros (matches target 0.155 to 3 significant figures) [COMPUTED]
- **GUE analytic Δ₃_sat ≈ 0.294** — zeta zeros are **47% more rigid** than GUE (ratio = 0.527)
- **The R₂ → Σ₂ → Δ₃ integral chain FAILS with N=2000**: gives 0.220 (43% overestimate) due to R₂ noise amplification through double integration
- **K(τ) from R₂ Fourier transform is qualitatively correct** (ramp + saturation) but quantitatively noisy with Gibbs spike at τ=1
- **Saturation is extremely flat**: Δ₃ varies <1% from L=15 to L=30. GUE continues growing logarithmically. This extreme flatness may be as important as the depressed value itself.
- **R₂ shows stronger anti-bunching at r≈1 than GUE**: R₂(1) ≈ 0.921 for zeta vs R₂(1) ≈ 0.999 for GUE — the pair-level signature of super-rigidity.

**Critical Methodological Finding:** The R₂ → Σ₂ → Δ₃ chain requires many more zeros (10,000+) to be quantitatively reliable. For N=2000, use the direct sliding-window method only.

**Leads:**
- Repeat with 10,000+ zeros to make the integral chain reliable
- Compute K(τ) via prime orbit sums (Task 3 skipped) — avoids zero-counting noise
- Hardy-Littlewood twin-prime correction to K(τ) (Task 5 skipped) — may explain excess rigidity

---

## Exploration 004: N²/p Scaling Universality — Gauss Sum Matrices

**Status: SUCCEEDED (negative result)**

**Goal:** Test whether N²/p_opt ≈ 275 is a universal scaling law for peak Brody β across N ∈ {250, 500, 1000}.

**Key Findings:**
- **N²/p universality claim REJECTED**: Peak N²/p values are 225.6 (N=250), 309.0 (N=500), 200.0 (N=1000) — 1.5× spread with no convergence [COMPUTED]
- **Peak β_max DECREASES with N**: 1.318 → 1.154 → 1.019 (opposite of what a converging law predicts) — finite-size effect [COMPUTED]
- **S002 used Wigner interpolated distribution, not Brody**: the "β=1.154" target is Wigner β; corresponding Brody β ~1.010 [CHECKED]
- **p≈N resonance** causes a β→0 collapse contaminating results near N²/p≈N
- The apparent S002 "peak at N²/p≈275" was a favorable fluctuation at N=500

**Critical Implication:** The Gauss sum matrix approach does NOT have a universal scaling law. The observed spectral repulsion at intermediate N²/p is a finite-size effect. This eliminates the Gauss sum matrix as a serious candidate for explaining or reproducing the zeta zero statistics.

---

## Exploration 005: Gauss Δ₃ Hierarchy + C1 Rescoring

**Status: SUCCEEDED (unexpected direction — explorer navigated to wrong directory, ran Gauss/C1 computations instead of prime orbit K(τ))**

**Goal intended:** K(τ) from prime orbit sums → Δ₃ prediction
**Goal executed:** C1 matrix rescoring + Gauss Δ₃ computation

**Key Findings:**
- **Rigidity hierarchy established**: Zeta (0.155) < C1 (0.285) < Gauss-best (0.415) < GUE (0.581) [COMPUTED]
- **C1 is 1.46× more rigid than best Gauss matrix** despite similar β values (~1.1-1.2) — Δ₃ and β decouple [COMPUTED]
- **C1 pair correlation MRD = 7.9% (PASS)** with corrected normalization; Δ₃_sat = 0.285 confirmed [COMPUTED]
- **β → 2 hypothesis definitively refuted**: all 47 primes give β < 1.2; p=99991 gives β=0.086 (near Poisson) [COMPUTED]
- Large prime-to-prime β fluctuations: p=809 β=1.154 vs p=853 β=0.731 (ΔΒ=0.42 between neighboring primes)

**Critical Implication:** Random phase diversity (C1: independent U(1) per entry) produces stronger long-range rigidity than arithmetic phases (Gauss: globally correlated). Rigidity (Δ₃) and level repulsion (β) decouple — matrices with similar β can have 1.46× different Δ₃.

**Leads:**
- Prime orbit K(τ) computation (ORIGINAL E005 goal, still undone) — should be E006
- Hybrid phases mixing random U(1) with arithmetic structure to bridge C1→zeta gap

---

## Exploration 006: K(τ) from Prime Orbit Sums — Does Diagonal Approximation Predict Δ₃=0.155?

**Status: PARTIAL SUCCESS**

**Goal:** Compute K_primes(τ) from Berry's diagonal approximation, feed through K→Σ₂→Δ₃ chain, determine whether prime orbit structure predicts Δ₃_sat=0.155 or 0.294.

**Key Findings:**
- **Berry's direct formula works**: Δ₃_sat = (1/π²)log(log(T/2π)) gives 0.143-0.167 for T∈[383,1127], matching measured 0.155. At T=600: 0.154 (0.6% error). At T_geo=1127: 0.167 (8% error). [COMPUTED]
- **K(τ) → Σ₂ route has ~2x normalization error**: GUE control gives Δ₃(L=10)=0.491 vs known 0.226. Suspect Fourier convention mismatch (angular vs ordinary frequency). Results from this route are inconclusive (absolute values cannot be trusted).
- **Normalization bug discovered**: GOAL.md template had wrong weight: (log p)² instead of (log p)²/p^m. The 1/p^m factor is the semiclassical amplitude — without it, K_primes was O(100). With it, K_primes ≈ 0.94·τ for τ<1 (6% below GUE).
- **K_primes with cap ≈ GUE (only 3.3% difference)**: The diagonal approximation K_primes ≈ 0.94τ for τ<1 is close enough to K_GUE=τ that they cannot be differentiated through the integral transform. Super-rigidity is NOT in the τ<1 region.
- **Physical picture**: K_primes decays to ~0 past τ=1 (peaking at ~1.32 near τ≈1.1-1.2). GUE K stays at 1 for all τ>1. The missing K=1 plateau requires off-diagonal orbit-pair correlations (Sieber-Richter pairs). Berry's log(log(T)) formula analytically captures this saturation failure.

**Conclusion:** Prime orbit structure DOES explain Δ₃_sat=0.155 — but via Berry's direct formula, not via the K(τ)→Δ₃ integral route. The diagonal approximation is too close to GUE at τ<1 to differentiate them; the super-rigidity mechanism lives in the saturation behavior (τ>1 region).

**Leads:**
- Fix the K→Σ₂ normalization (2x factor) to validate the integral route
- Literature search: does Berry (1985) derive the 1/p^m weight? Is the formula Σ₂=(2/π²)∫K/τ² sin² or L-(2/π²)∫(1-K)/τ² sin²?
- Is the Berry formula overestimate at high T known/explained?

---

## Exploration 007: Adversarial Novelty Review — Two Live Claims

**Status: PARTIAL SUCCESS (completed with timed-out Synthesis section)**

**Goal:** Literature search to assess novelty of λ_n^zeta/λ_n^GUE crossover and Berry formula accuracy table. Pre-settle 3 other claims.

**Key Findings:**
- **λ_n^zeta < λ_n^GUE crossover: NOVEL (4/5)** — Exhaustive search of Li (1997), Bombieri-Lagarias (1999), Keiper (1992), Schumayer-Hutchinson (2011 review) found ZERO prior papers comparing λ_n^zeta to λ_n^GUE. The two communities (Li criterion / number theory vs RMT / quantum chaos) have never been cross-pollinated on this specific observable. Bombieri-Lagarias gives asymptotic λ_n ~ (1/2)n log n for zeta only; no GUE ensemble comparison anywhere. [FOUND]
- **Berry formula accuracy (0.2%→12.5% with T): ARTIFACT/WEAK (1-2/5)** — No prior paper has this T-resolved accuracy table. However, the most likely explanation is sparse-sampling: at T≈2245, only the last few hundred zeros from N=2000 are in the bin, giving unreliable Δ₃ measurements biased downward. Berry (1985) has no correction terms; BK (1996) does not give a closed-form Δ₃ correction. NOT clearly novel.
- **Flat plateau**: NOT NOVEL (Berry 1985 predicted it, Odlyzko confirmed). Record and close.
- **K_primes normalization**: WEAK (Berry 1985 is prior source). Record and close.
- **C1 Δ₃=0.285**: RETRACTED (finite-N GUE baseline error from S002 work).

**Strongest Surviving Novel Claim:** λ_n^zeta/λ_n^GUE < 1 crossover at n≈300 (ratio 0.95 at n=500). To validate: need ≥10,000 zeros and GUE N≥500 averaged over ≥5,000 matrices. The mechanism (super-rigidity → uniform zero phases → efficient phase cancellation → smaller large-n λ_n) is also new.

**Unexpected finding:** Complete absence of Li-vs-RMT comparison in literature is itself notable — natural comparison, never made.

**Leads:**
- Validate λ_n ratio with 5,000+ zeros and larger GUE ensemble (E008 candidate)
- Berry formula accuracy table with Odlyzko high-T zeros to distinguish artifact from signal

---

## Exploration 008: λ_n^zeta/λ_n^GUE Crossover — Truncation Sensitivity Analysis

**Status: PARTIAL SUCCESS (signal confirmed at K=N=2000 but truncation-sensitive)**

**Goal:** Validate the novel λ_n crossover finding from E002 using 5,000 zeros and larger GUE ensembles.

**Key Findings:**
- **[COMPUTED] E002 replication confirmed**: At K=N=2000, ratio = 0.949 at n=500, crossover at n≈272, 7.3σ below 1 with 100 GUE realizations (20× more than E002). The signal is real at this truncation level.
- **[COMPUTED] CRITICAL: At K=4500 zeros vs N=2000 GUE (UNFAIR comparison), λ_500^zeta = 930.60 vs GUE = 925.62 → ratio = 1.005 (ABOVE 1!)**. The crossover disappears when K≠N.
- **[COMPUTED] Truncation is severe**: λ_500^zeta increases +6.1% from K=2000 to K=5000, +11.4% at n=1000.
- **[COMPUTED] GUE λ_n scales linearly with N**: N=500→235, N=2000→926, N=3000→1385 at n=500. Only valid comparison is when N_GUE = K_zeros.
- **[CONJECTURED] Crossover may be truncation artifact**: Matched K=N=5000 test was still computing at cutoff. Whether ratio converges to < 1 or → 1 as K=N→∞ unknown.

**Verdict:** Novel claim WEAKENED. The crossover at K=N=2000 is real (7.3σ, 100 realizations), but its physical meaning requires knowing whether it persists as K=N→∞. The convergence rate analysis is needed to close this.

**Open question:** What is lim_{K=N→∞} λ_n^zeta(K) / λ_n^GUE(N=K)?

---

## Exploration 009: λ_n Ratio Convergence — Decisive Verdict

**Status: SUCCEEDED (negative result, definitively concluded)**

**Goal:** Compute matched ratio λ_n^zeta(K) / λ_n^GUE(N=K) at K=N=500, 1000, 2000, 3000, 5000 and determine convergence trend.

**Key Findings:**
- **[COMPUTED] Ratio at n=500 is MONOTONICALLY INCREASING:**

| K=N | Ratio at n=500 | Significance |
|-----|---------------|--------------|
| 500 | 0.888 | -22.3σ below 1 |
| 1000 | 0.898 | -16.9σ below 1 |
| 2000 | 0.952 | -7.3σ below 1 |
| 3000 | 1.004 | +0.5σ (consistent with 1.0) |
| 5000 | 1.090 | +9.7σ ABOVE 1 |

- **[COMPUTED] The crossover point DISAPPEARS at K=N ≥ 3000**: At K=N=3000 ALL ratios are >1 (zeta exceeds GUE at all n=100-500). At K=N=5000, ratios range from 1.09 (n=500) to 1.34 (n=100).
- **[COMPUTED] Root cause: GUE scaling breaks down**: Linear scaling of N=K semicircle eigenvalues to [t_1, t_K] creates density mismatch. As K grows, GUE eigenvalues spread to large t (small contributions), while zeta zeros have logarithmically growing density. This is a structural flaw in the comparison method.

**Verdict: ARTIFACT — novel claim fully refuted.** The ratio < 1 at K=N=2000 is a finite-K artifact of the linear scaling convention. It reverses at K=N=3000 and reaches 1.09 at K=N=5000. The comparison requires a self-consistent scaling method (e.g., unfolding to unit mean spacing) to be meaningful.

---

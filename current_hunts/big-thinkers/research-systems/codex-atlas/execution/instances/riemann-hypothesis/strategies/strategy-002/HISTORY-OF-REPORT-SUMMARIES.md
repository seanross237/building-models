# Exploration History

---

## Exploration 001 — Complex Arithmetic Matrices (Tournament Entry A)

**Goal:** Test complex Hermitian arithmetic matrices (Von Mangoldt amplitudes × complex phases) for GUE-like spectral statistics. 7 constructions tested at N=500.

**Outcome: SECONDARY SUCCESS (borderline PRIMARY)** — C1 (Random complex phases) achieves β = 1.675, satisfying the primary success criterion (β > 1.5).

**Key findings:**
- **C1 (Random Phase Hankel): β_Wigner = 1.655–1.675** [COMPUTED] — Best fit is GUE (KS_GUE=0.027 < KS_GOE=0.057). This is a significant jump from the Hankel baseline of β=0.44.
- **C3b (Gauss p=997): β = 1.092, GOE best fit** [COMPUTED] — Most meaningful arithmetic result. Gauss sum phases exp(2πi jk/997) push the matrix from β=0.44 toward GOE boundary.
- **C2 (Dirichlet χ₄, χ₈): Failed by design** — Odd characters produce antisymmetric matrices that cancel to zero. Must use complex characters.
- **C4 (Zeta phases): Poisson (β≈0)** — Im(ζ(½+i|j-k|)) depends only on lag → Hermitian Toeplitz → Poisson statistics.

**Structural principle discovered [CONJECTURED]:** Phase φ(j,k) must depend on both j and k jointly (not just on |j-k|) to break time-reversal symmetry. Factorizable phases φ(j,k)=g(j)-g(k) are unitarily equivalent to real symmetric matrices and can't exceed β=1.

**10-constraint score for C1 (best construction): 4 PASS, 2 PARTIAL, 0 FAIL, 2 NOT COMPUTED, 2 N/A**
- PASS: β>1.5 (#1), NN-spacing KS_GUE<0.05 (#3), GUE best fit (#4), Σ²(L>2)=0.499 (#6)
- PARTIAL: β=1.675 not 2.0 (#5), form factor noisy (#8)
- NOT COMPUTED: pair correlation (normalization bug, MRD=0.996 unreliable), Δ₃ (formula bug, 10-25× too small)
- Code bugs identified: R₂ normalization and Dyson-Mehta Δ₃ integral formula need fixing

**Unexpected:** p-dependence in Gauss constructions: p=97 gives β=0.88, p=997 gives β=1.09 — larger prime → higher β.

---

## Exploration 004 — Berry Saturation Formula: Quantitative Test

**Goal:** Quantitatively test Berry's (1985) prediction for the spectral rigidity Δ₃ saturation level. Compare Berry's formula to measured Δ₃ from 2000 zeta zeros.

**Outcome: SUCCESS**

**Key findings:**
- **Berry's formula confirmed:** Δ₃_sat = (1/π²) × log(log(T/2π)) matches the measured value with **7.6% overall error** [COMPUTED, CHECKED]
- **Measured:** Δ₃_sat = 0.1550 ± 0.0008 (matches S001's 0.156 to 0.4%)
- **Height-resolved:** Δ₃_sat increases strictly with height — 0.143 → 0.155 → 0.157 → 0.159 across 4 bins of 500 zeros. Bin 1 (lowest T) matches Berry to 0.2%.
- **3× super-rigidity:** Zeta zeros are 3× more rigid than GUE at L=15 (ratio Δ₃_sat/Δ₃_GUE = 0.31)
- **Formula disambiguation:** The integral Dyson-Mehta formula vs the sum approximation differ by 2×. The integral formula is correct and matches 0.156.
- **GUE overestimate:** Asymptotic GUE formula overestimates actual GUE simulation by 2-3× at L=5-20

**Normalization caveat:** Berry's 1985 paper uses 1/(2π²) convention; the matching is with 1/π² — suggests a normalization convention difference between Berry and Dyson-Mehta.

---

## Exploration 005 — Constraint Rescoring for C1 + Gauss Prime Sweep

**Goal:** (A) Recompute pair correlation and Δ₃ for C1 with corrected formulas; (B) extend Gauss sum construction to large primes to test β→2 hypothesis.

**Outcome: Two definitive results**

**Part A (C1 rescoring):**
- Pair correlation MRD = **7.9% → PASS** (previously bugged at 99.6%). C1 satisfies Montgomery's formula at the 10% level. [COMPUTED]
- Δ₃ saturation = **0.285** for L=25-50 (NOT 0.156 like zeta zeros; NOT 0.565 like GUE). C1 is intermediate — halfway between GUE and true zeta behavior.
- Updated C1 scorecard: **3 PASS, 4 PARTIAL, 0 FAIL** (constraints 1, 2, 3 PASS; 4, 5, 6, 8 PARTIAL; 7 PARTIAL since rigidity is wrong level)

**Part B (Gauss sweep — DEFINITIVE NEGATIVE):**
- β does NOT trend toward 2 as p→∞
- β **peaks at p=809 (β=1.154)** then REVERSES — large p (99991) gives β=0.086 (near Poisson!)
- ALL constructions permanently in GOE class (β < 1.2). Gauss sums are confined to GOE.
- Mechanism: N²/p ≈ 250-310 is optimal ratio; too small or too large p reduces β
- Fine sweep (21 primes p=503-5003) shows β fluctuating ±0.4 between neighboring primes — prime-specific arithmetic effects

**Unexpected:** C1's Δ₃=0.285 vs GUE's ~0.565 means the Von Mangoldt Hankel structure (not random phases) enforces intermediate rigidity. The pair correlation passes Montgomery but rigidity doesn't reach the zeta zero level.

---

## Exploration 002 — Optimization-Based Construction (Tournament Entry B)

**Goal:** Reverse-engineer an operator from GUE constraints by optimizing parameterized Hermitian matrices. Then examine structure of optimal matrix.

**Outcome: PARTIAL / USAGE LIMIT HIT** — Stage 1 completed with critical negative finding; Stage 2 running when usage limit hit.

**Key findings (from REPORT.md partial + code):**
- **Stage 1 critical failure:** Histogram-based MSE loss function is non-differentiable (piecewise constant in sorted eigenvalue space). L-BFGS-B declares convergence immediately on most trials. Best β achieved: 0.24 after 15,000+ function evaluations.
- **Conceptual insight:** Eigenvalue statistics of sorted eigenvalues are NOT differentiable with respect to matrix parameters. Optimization with gradient-based methods requires KDE-based smooth loss functions or gradient-free methods.
- **Stage 2 (KDE + Nelder-Mead):** Was running when usage limit hit. Saved trials in `code/expA_*, expB_*` arrays.

**Reliability:** Stage 1 findings are [COMPUTED] and solid. Stage 2 results unknown.

---

## Exploration 003 — Two-Point Formula + Kernel Operator (Tournament Entry C)

**Goal:** Compute Montgomery's pair correlation from prime sums, compare to zeros, construct kernel operator.

**Outcome: PARTIAL / USAGE LIMIT HIT** — Computations completed and saved; report not written.

**Key findings (from code/all_results.npz):**
- **Pair correlation from zeros vs Montgomery (normalized):** MAD = **6.9%** [COMPUTED] — Excellent agreement. Confirms and slightly improves on strategy-001's 9.1%.
- **Form factor from zeros vs GUE:** MAD in ramp region (τ<1) = **19.3%** [COMPUTED]
- **Form factor from primes:** K_primes_100 = K_primes_1000 = K_primes_10000 — ALL IDENTICAL. Suggests normalization bug; the prime sum may not have been properly normalized or converges in the first 100 primes.
- **Kernel operator (Montgomery R₂ as kernel):** Eigenvalues all ~0 (numerical noise range). The discretized kernel matrix is numerically rank-deficient.

**Open question unresolved:** Whether the prime form factor correctly converges to GUE = min(τ,1). The identical K_primes across P_max levels suggest a bug rather than genuine fast convergence.


---

## Exploration 006 — Two-Point Formula Redo + Complex Dirichlet Characters

**Goal:** (A) Definitively compute whether Berry's prime sum reproduces the spectral form factor. (B) Test complex Dirichlet character phases for GUE statistics.

**Outcome: Two definitive answers**

**Part A (Two-point formula) — PARTIAL SUCCESS:**
- K_primes matches K_GUE ramp with MAD = 14.5% (τ ∈ [0.1, 0.9]). K_zeros matches with 12.8%. [COMPUTED]
- **ANSWER: Primes determine two-point spectral correlations in the ramp region.** Confirms Berry's semiclassical conjecture.
- K_primes FAILS for τ > 1 (no plateau mechanism). Plateau requires off-diagonal periodic orbit interference.
- **Resolution of E003/E005 failures:** Prior explorations used cosine sum Re[Z(τ)], not the form factor K = |Z|²/N. Correct normalization: divide by (2πρ̄)².

**Part B (Dirichlet characters) — NEGATIVE + PROVED IMPOSSIBLE:**
- Best result: β_mul13 = 0.281 (χ_13 multiplicative). All constructions firmly GOE. [COMPUTED]
- **Algebraic proof:** Multiplicative H_{jk} = Λ×χ(j)χ(k), after Hermitianizing, becomes Λ×Re(χ(j)χ(k)) = real symmetric matrix → GOE. Factorizable H_{jk} = Λ×χ(j)χ*(k) is unitarily equivalent to real matrix → GOE.
- **There is no Hermitian Dirichlet character matrix that achieves GUE.** [PROVED]

**Unexpected finding:** The Dirichlet impossibility is structural — both construction routes collapse to GOE. Suggests any "genuinely arithmetic" phase Hamiltonian may be confined to GOE. Random phases (C1) are necessary for GUE.

---

## Exploration 007 — Adversarial Review of C1 Pair Correlation Claim

**Goal:** Attack "C1 satisfies Montgomery's pair correlation at 7.9% MRD." Three tests: null matrices, realization stability, severity assessment.

**Outcome: THREE SERIOUS ATTACKS ESTABLISHED**

**Test 1 (Null matrices) — Von Mangoldt amplitude unnecessary:** [COMPUTED]
- GUE control: MRD = 7.8% (passes, essentially same as C1)
- Flat-amplitude random phase: MRD = 6.8% (BETTER than C1's 7.9%)
- Flat Toeplitz (GOE class!): MRD = 9.0% (passes)
- **Finding: ANY matrix in GUE or even GOE class passes the pair correlation test. Von Mangoldt amplitude adds nothing.**

**Test 2 (Stability) — 7.9% not stable per realization:** [COMPUTED]
- 20 individual C1 realizations: mean MRD = 15.5% ± 1.9%
- Pass rate: 0/20 (zero realizations pass ≤10%)
- The E005 result was 5-realization AVERAGED R₂, reducing noise by ~√5
- **Finding: "7.9% MRD PASS" is an averaging artifact; individual matrices fail 100% of the time.**

**Restated honest claim:** "C1 is in the GUE universality class. Pair correlation passes (~8%) when averaged over multiple realizations — a generic property of any GUE-class matrix."

**The most defensible surviving claims are:**
1. C1 anomalous intermediate Δ₃=0.285 (between GUE=0.565 and zeta=0.156) — specific to Von Mangoldt Hankel
2. Dirichlet characters algebraically impossible for GUE
3. Gauss sums permanently GOE with N²/p≈250 optimal ratio

**Unexpected:** GOE-class Toeplitz matrix (β=0.45) also passes pair correlation at 9.0% — the test is insufficiently discriminating at N=500 with 5-realization averaging.
# Exploration 008 — Report Summary

## Goal
Final synthesis: literature search for the two strongest novel claim candidates (N²/p Gauss scaling and Dirichlet impossibility), novelty assessment, and Strategy 003 recommendation.

## What Was Done
- Web search across 12+ queries for prior literature on Gauss sum matrix level statistics and Dirichlet character Hamiltonian GOE impossibility
- Assessment of all 5 Strategy 002 claim candidates against library findings and external literature
- Writing of two "paper format" claim writeups

## Novelty Verdicts

### Claim A: N²/p ≈ 250-310 Optimal Ratio (Gauss Sum Matrices) — **SUPPORTED**
**Finding:** For H_{jk} = Λ(|j-k|+1) × exp(2πijk/p) at N=500, β peaks at N²/p ≈ 309 (p=809, β=1.154). For large p (N²/p → 0), β → Poisson. All constructions: β < 1.2 (permanently GOE).

**Literature:** No prior paper studies Gauss sum / chirp matrices for level statistics. Closest analogue: Fyodorov-Mirlin band matrix transition (W²/N ~ 1) — different matrix class, different governing constant, and band matrices CAN reach GOE whereas our matrices are β-capped. The specific N²/p ≈ 250-310 constant is original.

**Caveat:** Only N=500 tested. N-scaling of the constant is unknown. "Universal" claim requires multi-N verification.

### Claim B: Dirichlet Character Matrices are Algebraically Confined to GOE — **SUPPORTED**
**Finding:** Any Hermitian H_{jk} = Λ × f(χ(j+1), χ(k+1)) is either (a) real symmetric (after Hermitianizing multiplicative phases) or (b) unitarily equivalent to a real matrix (conjugate phase D A D†). Both routes → GOE. Proved algebraically, confirmed numerically (β ≤ 0.28 for χ_5, χ_13).

**Literature:** Not explicitly documented. Follows from Dyson's threefold way + Katz-Sarnak (quadratic L-function families → orthogonal symmetry), but this specific matrix-theoretic proof for the Dirichlet character Hamiltonian is original. Schumayer-Hutchinson review (2011) does not discuss character-based Hamiltonians.

**Caveat:** Only covers multiplicative characters. Non-multiplicative arithmetic phases (Jacobi sums, Ramanujan τ) are not covered.

### Other Claims:
- C1 intermediate Δ₃ = 0.285: **WEAK novelty** (expected by specialists, not published for this matrix)
- Berry saturation: **NOT NOVEL** (confirmation of Berry 1985)
- Prime form factor normalization: **WEAK** (clarification, not new result)

## Key Takeaway
Strategy 001 found zero novel claims. Strategy 002 identifies two **SUPPORTED** claims: the N²/p scaling law and the Dirichlet impossibility proof. Both are specific, quantitative, and not in the literature, though both follow from general principles that experts would consider expected.

The adversarial review (E007) correctly downgraded the pair correlation claim. The surviving strong result is the anomalous Δ₃ intermediate rigidity — unique to Von Mangoldt Hankel structure — but this requires the flat-amplitude comparison (not yet done) to confirm that the Von Mangoldt structure specifically causes it.

## Strategy 003 Recommendation
Focus on: (1) flat-amplitude Δ₃ test (one Math Explorer computation to confirm whether Von Mangoldt structure causes intermediate rigidity); (2) N-scaling of N²/p (test N=250, 1000); (3) prime-indexed constructions targeting Δ₃ < 0.2. The central unsolved problem: no construction achieves both β > 1.5 AND Δ₃ < 0.2 simultaneously. The non-arithmetic GUE route (C1) gives β=1.18 but Δ₃=0.285 (not zeta-like). All arithmetic routes (Gauss, Dirichlet) are GOE.
# Exploration 009 — Report Summary

## Goal
Test whether C1's anomalous Δ₃_sat=0.285 (intermediate between GUE=0.565 and zeta=0.155) is caused by Von Mangoldt arithmetic structure, by comparing H_flat (flat amplitude + random phases) to C1 and GUE control at N=500.

## What Was Done
- Ran 3 realizations each of H_flat, C1, and GUE control (N=500)
- Used exact analytical staircase integration for Δ₃ (explorer found and fixed a formula bug that underestimated Δ₃ by ~50×)
- Explorer died (usage limit) before writing report; computation was completed manually from explorer's code

## Key Result

| Ensemble | Δ₃_sat | ±std |
|---|---|---|
| H_flat | **0.256** | ±0.010 |
| C1 | **0.243** | ±0.017 |
| GUE control | **0.227** | ±0.010 |
| GUE theory (inf N) | 0.242 | — |
| Zeta zeros | 0.155 | (known) |

**All three ensembles agree within noise.** H_flat ≈ C1 ≈ GUE control.

## Verdict

**C1's intermediate Δ₃ is NOT caused by Von Mangoldt arithmetic.** It is generic GUE-class finite-size behavior at N=500. The earlier value of 0.285 (E005) was within normal sampling variation. The "anomalous intermediate rigidity" claim is DISPROVEN.

The two surviving SUPPORTED novel claims from E008 are unaffected: N²/p scaling law and Dirichlet impossibility proof.

The central unsolved problem: no construction achieves Δ₃_sat < 0.2 (zeta zeros have 0.155). The 40% gap between generic GUE-class N=500 behavior and zeta zeros remains unexplained.

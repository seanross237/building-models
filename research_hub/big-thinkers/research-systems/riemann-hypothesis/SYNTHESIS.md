# Riemann Hypothesis Investigation — Complete Synthesis

**Date:** 2026-04-04 to 2026-04-06
**Agents run:** ~30
**Waves:** 8+
**Starting point:** A YouTube video (Sabine Hossenfelder) about Hartnoll-Yang's "Conformal Primon Gas at the End of Time"

---

## The Riemann Hypothesis in One Sentence

All nontrivial zeros of the Riemann zeta function lie on the critical line Re(s) = 1/2, which means the prime numbers are distributed as regularly as they possibly can be — with no hidden long-range conspiracies.

---

## What We Did

Launched ~30 AI agents across 8+ waves exploring unconventional cross-disciplinary approaches to RH: thermodynamics, information theory, cellular automata, billiard optimization, kernel positivity (Polya frequency), functional equation analysis, Gaussian multiplicative chaos, martingale theory, and finally algebraic geometry / arithmetic geometry (Connes, Deninger, F₁).

Every analytic and probabilistic approach converged to the same wall. The investigation then traced that wall to its geometric core, arriving at a precise 5-problem research agenda that, if solved, would prove RH.

---

## The Journey (8 Waves)

### Wave 1: Three Wild Ideas
| Agent | Result |
|-------|--------|
| **Entropy Ceiling** (2A) | Canonical concavity proved (C(β)>0 for all β>1). Ensemble equivalence gap identified — equivalent to RH. Novel Fisher information conjecture proposed. |
| **Spectral Breeder** (5A) | CA Rule 137 enters GUE universality class (KS=0.070). First evolutionary search over CA rules targeting zeta-zero statistics. |
| **Billiard Inversion** (4A) | Weyl law no-go: no bounded billiard can match zeta zeros asymptotically. But 1D Schrödinger with 12-mode potential matches 15 zeros to <3.6%. |

### Wave 2: Dig Deeper Into Wave 1
| Agent | Result |
|-------|--------|
| **Fisher Information** | Perturbative theorem PROVED (d²I/dσ² = 4[(β-1)²+4t²]/β³ > 0). Naive full conjecture DISPROVED. "Stealth" characterization: zeros at σ=1/2 are maximally hard to detect. |
| **Truncated Primon** | Z_N has NO zeros — they're emergent phase transitions. Bohr-Jessen variance diverges at σ=1/2, converges above. This IS the phase boundary. |
| **Polya Kernel** | Log-concavity proved on [0,3] via interval arithmetic. Initial "globally impossible" claim later CORRECTED in Wave 3. |

### Wave 3: What's the Actual Gap?
| Agent | Result |
|-------|--------|
| **Goldilocks Condition** | MAJOR CORRECTION: Φ IS globally log-concave (PF₂). Feb 2026 paper: PF₄ holds, PF₅ fails by 2.27%. The "Goldilocks" lives between PF₄ and PF₅. |
| **Phase Boundary Lock** | AFE zeros snap to σ=1/2 with 10⁻⁵⁷ precision. But symmetry alone insufficient — Davenport-Heilbronn has same symmetry, off-line zeros. |
| **Amplitude Bound** | At zeros, functional equation is trivially satisfied (0=χ·0). Davenport-Heilbronn kills this approach. Euler product is the essential ingredient. |
| **Squeeze Lambda** | Information-theoretic methods can't see Λ — locality-globality mismatch. Λ determined by single closest zero pair; info theory averages over all. |
| **Schrödinger V_N** | V_N(x) does NOT converge on fixed domain. Operator needs [0,∞) or non-compact surface. |
| **GMC Repulsion** | Log-correlated structure confirmed at σ=1/2 only. γ_eff → √2 (critical GMC) only at critical line. Statistical, not deterministic. |

### Wave 4: Attack the Precise Gap
| Agent | Result |
|-------|--------|
| **PF₄-Modular** | NOVEL: "Modular boost" — theta terms individually fail PF₄ but sum passes via τ→-1/τ symmetry. PF₅ fails by only 2.27% in tiny region. |
| **Euler Repulsion** | NOVEL: Gamma factor is NOT the sole bottleneck — it's the complex multiplication Xi = Re[G]·Re[ζ] - Im[G]·Im[ζ] (subtraction). Convolution vs addition is the key dichotomy. |
| **Four-Fold Architecture** | σ=1/2 is special in 4 independent ways (PF boundary, Bohr-Jessen, functional equation, GMC). But conjunction doesn't yield proof — measure vs topology gap. Novel (ζ,ζ') joint distribution reformulation. |

### Wave 5: Bridge the 2.27% Gap
| Agent | Result |
|-------|--------|
| **PF₅ Perturbation** | DEFINITIVE: PF_∞ is structurally impossible for functions WITH zeros (Schoenberg 1951). PF controls zero EXISTENCE, not LOCATION. Entire PF framework closed. |
| **Gamma Bypass** | Confirmed: no repackaging helps. Schoenberg's convolution theorem caps any multiplicative modification at PF₄. |
| **Joint (ζ,ζ')** | Derivative constraint is weaker than thought (net |ζ'| grows for σ₀ < 0.85). Joint distribution compatible with off-line zeros. |

### Wave 6: The Probabilistic Turn
| Agent | Result |
|-------|--------|
| **Möbius Martingale** | Prime-by-prime filtration is already known (Harper, Gorodetsky-Wong). Approach is CIRCULAR — the massive cancellation between innovations IS the content of RH. |
| **Convolution Invariant** | NOVEL: The "finite variance property" is the correct replacement for PF_∞. Preserved by convolution, destroyed by addition, transitions at σ=1/2. But probabilistic → deterministic gap remains. |

### Wave 7: Jensen, Almost-Periodicity, and the Geometric Turn
| Agent | Result |
|-------|--------|
| **Jensen-Concentration** | Jensen converts pointwise→counting, but we need average→pointwise. Arrow points wrong way. Concentration is weaker than existing zero-density estimates. |
| **Almost-Periodic** | AP gap grows doubly-exponential, concentration gap only singly-exponential. AP becomes too weak before it can contradict concentration. |
| **Geometric Bridge** | THE KEY RESULT. Connes reduced RH to Weil positivity. Proved at archimedean place + any finite S. Gap: all places. Deninger's cohomology proved for model systems. Arithmetic site exists but lacks intersection theory. |

### Wave 8: The Arithmetic Core
| Agent | Result |
|-------|--------|
| **Weil Positivity Bridge** | Exact obstruction: semilocal Sonin spaces stabilize, but S-dependent inner products don't (Euler product fluctuations). Weak limits can be harmonic-measure-smoothed. Missing: uniform semilocal tightness. |
| **Arithmetic Intersection** | SYNTHESIS: Proposed construction — adelically regularized, theta-theoretic, Arakelov-style intersection pairing on S^(2). Additive (not multiplicative) globalization. Kudla/Siegel-Weil as positivity engine. |
| **Tropical Deligne Pairing** | Mapped exactly what exists vs what's missing for Step 1. 5 precise gaps identified (see below). |

---

## Key Theorems Proved

1. **Canonical concavity of the primon gas:** C(β) > 0 for all β > 1 (each summand positive in Euler product series).
2. **Perturbative Fisher information minimum:** d²I/dσ² = 4[(β-1)²+4t²]/β³ > 0 at σ=1/2 for each zero pair. Unique global minimum.
3. **Φ is globally log-concave (PF₂):** Analytical proof via n=1 term dominance + bounded correction.
4. **PF₅ fails:** Certified by interval arithmetic (Feb 2026 paper, arXiv 2602.20313).
5. **PF_∞ is structurally impossible** for functions with zeros (Schoenberg 1951).
6. **Truncated Euler product has no zeros:** Emergent phenomenon of infinite product.
7. **No bounded billiard matches zeta zeros:** Weyl law incompatibility (76% deficit by n=30).

---

## Key Novel Discoveries

1. **The modular boost:** Theta-function terms individually fail PF₄ but their sum passes via modular symmetry τ→-1/τ. The modular structure RAISES the PF order.
2. **Convolution vs addition dichotomy:** Euler product (convolution) preserves structure; Davenport-Heilbronn (addition) destroys it. This is WHY ζ has on-line zeros and DH doesn't.
3. **The finite variance property** as the correct convolution invariant replacing PF_∞. Transitions at σ=1/2.
4. **Emergent zeros as phase transitions:** Identical to Lee-Yang zeros in statistical mechanics.
5. **"Stealth" characterization:** Zeros at σ=1/2 minimize parametric Fisher information (hardest to detect from thermodynamic data).
6. **The gamma factor is NOT the sole bottleneck:** It's the complex multiplication (subtraction Re·Re - Im·Im) that limits PF order.
7. **The Euler product and functional equation live in complementary half-planes:** Concentration works for σ>1/2, symmetry bridges to σ<1/2, they never overlap. Bridging them IS RH.
8. **Additive not multiplicative globalization:** The log log N divergence of partial Euler products disappears when you sum local energies (intersection theory) instead of multiplying local norms.
9. **The decoupling lemma (Wave 9):** For any prime envelope {B_p} and any t-grid, the pointwise minimax LP for additive evidence depends on the B_p only through their total mass. Independent per-prime weights have ZERO optimization content. This explains why mollifier methods work (coupling) and why pure envelope methods can't (no coupling).
10. **Refinement of insight #8:** "Additive globalization" requires COUPLED additive structure (mollifiers, intersection pairings, theta lifts). Independent per-prime decompositions are too crude — they lose the analytic structure needed to detect zeros.

---

## Key Corrections Made During Investigation

1. **"Φ is NOT globally log-concave"** → WRONG. Φ IS log-concave (PF₂). The original agent confused PF₂ with PF_∞.
2. **"The gamma factor is the bottleneck"** → PARTIALLY WRONG. The gamma factor alone is PF₅. The bottleneck is the complex multiplication structure of Xi.
3. **"Derivative at off-line zeros is vanishingly small"** → OVERSTATED. Net |ζ'| ~ t^{0.85-σ₀}, which grows for σ₀ < 0.85.
4. **"Fisher information is minimized at σ=1/2"** → TRUE perturbatively, FALSE for the full non-perturbative version.
5. **"Additive globalization works"** → REFINED. Only COUPLED additive structures work (mollifiers, intersection pairings). Independent per-prime weights are insufficient (decoupling lemma, Wave 9).

---

## Doors Definitively Closed

| Approach | Why it's closed |
|----------|----------------|
| PF/Kernel framework | PF_∞ impossible for functions with zeros (Schoenberg). Controls existence, not location. |
| Functional equation alone | Davenport-Heilbronn counterexample |
| Amplitude mismatch | 0 = χ·0 trivially satisfied at zeros |
| Information-theoretic global methods | Can't detect individual zeros (locality-globality) |
| Möbius martingale CLT | Circular — the cancellation IS RH |
| Jensen + concentration | Wrong arrow (pointwise→counting, need inverse) |
| Almost-periodicity + concentration | Growth rates incompatible (doubly-exp vs singly-exp) |
| Joint (ζ,ζ') distribution | Compatible with off-line zeros |
| Any multiplicative globalization | Inherits log log N divergence |
| Additive evidence with independent per-prime weights | LP infeasible — bounded envelope can't dominate logarithmic singularities of -log\|ζ\| |

---

## The Refined Additive Insight (Wave 9)

We initially concluded "additive globalization works where multiplicative fails." This was correct but underspecified. The **additive-evidence** experiment refined it:

**Additive with INDEPENDENT per-prime weights → fails.** If you bound each weight by C(log p)^A / p^{1+ε} so the sum converges, you get a bounded envelope. But -log|ζ(σ+it)| has logarithmic singularities at every zero. No bounded envelope can dominate an unbounded target. The minimax LP is infeasible at σ = 0.55, 0.6, 0.7 no matter how many primes.

**Additive with COUPLED t-dependent weights (mollifiers) → frontier.** Mollifier methods (Levinson, Conrey, Conrey-Iwaniec-Soundararajan, Guth-Maynard) work because the weights w_p(t) = Re(a_p · p^{-σ-it}) are NOT independent — they share frequency structure inherited from the Dirichlet series. This coupling exploits ζ's analytic structure in a way pure envelopes cannot.

**Decoupling lemma (novel, elementary):** For any envelope {B_p} and any t-grid, the pointwise minimax LP optimum depends on the B_p only through their total mass — you can reshuffle the weights freely. This means independent per-prime weights have ZERO optimization content; all the action is in the coupling.

**Why Neyman-Pearson fails:** The "zero at t₀" alternative is Lebesgue-singular w.r.t. the Bohr-Jessen null distribution. Any L¹-convergent detector is band-limited and cannot resolve the logarithmic singularity at a zero. Same probabilistic→deterministic wall, in detection-theory language.

**Lesson for the broader program:** "Additive globalization" only works when the additive structure is COUPLED (intersection theory pairings, mollifier coefficients, theta lifts). Pure independent per-prime decompositions are too crude — they lose the analytic structure needed to detect zeros.

---

## Where the Proof Actually Lives

### The Answer: Algebraic Geometry

RH is not an analytic statement that happens to be hard — it is a **geometric statement** that happens to have an analytic formulation. Every serious approach converges on the same requirement: a positivity theorem (the arithmetic Hodge index theorem) on a geometric object (Spec(Z) × Spec(Z) over F₁) that has not yet been constructed.

### The Closest Approach: Connes' Program

Connes reduced RH to **Weil positivity** — a single positivity statement on the idele class group. He proved it:
- At the archimedean place (2021)
- At any finite set of primes (via quasi-innerity + semilocal Sonin spaces)

The gap: proving it at ALL places simultaneously. The obstruction:
- Semilocal Sonin spaces stabilize (vector spaces are fine)
- But S-dependent inner products diverge (weighted by partial Euler products)
- Archimedean compensation is inherently finite (can't handle infinitely many primes)
- Weak limits can be harmonic-measure-smoothed (smearing = off-line zeros undetectable)

### The Proposed Construction

An **adelically regularized, theta-theoretic, Arakelov-style intersection pairing on the square of the scaling site:**
- Scaling site S^(2) as ambient surface (Connes-Consani)
- Additive globalization via constant-term regularization (Arakelov)
- Theta/Siegel-Weil positivity mechanism (Kudla)

### The 5 Precise Gaps (Research Agenda)

| # | Gap | Description |
|---|-----|-------------|
| 1 | **Chow/Picard theory on S^(2)** | Build a category of correspondences containing H₁, H₂, Δ, Ψ^λ |
| 2 | **Excess-intersection formula** | Δ · Ψ^λ has 1D fixed locus (orbit C_p) — need orbital Lefschetz formula |
| 3 | **Green kernels on S^(2)** | Extract Connes' prolate/Toeplitz (∞) and Hankel/scattering (p) as Green functions |
| 4 | **Semilocal compatibility** | Finite truncations must match existing semilocal positive forms |
| 5 | **Hodge index theorem on S^(2)** | Primitive negativity — where RH enters as geometry |

### The Conjectural Theorem

**Arithmetic Hodge-Siegel-Weil Principle:** There exists a theta lift Θ: S(A_Q) → Corr^adm(S^(2))_prim such that:
1. S-truncations reproduce Connes' semilocal forms
2. Globally: Q_W(f,g) = ⟨Θ(f), Θ(g)⟩
3. Primitive classes satisfy ⟨ξ,ξ⟩ ≤ 0
4. Lefschetz trace recovers the unsmeared Weil distribution

If proved → RH follows.

---

## The Dictionary: Function Fields vs Number Fields

| Function Field (C/F_q) | Number Field (Q) | Status |
|------------------------|-------------------|--------|
| Curve C | Spec(Z) / Scaling site S | Constructed (Connes-Consani) |
| Finite field F_q | Field with one element F₁ | Multiple candidates |
| Frobenius Frob_q | Scaling action of R*₊ | Best candidate; not endomorphism |
| Surface C × C | S^(2) = S ×_{F₁} S | Partially constructed |
| Étale cohomology H¹(C) | H¹(Spec Z) (Deninger) | Not constructed |
| Intersection pairing | Arakelov pairing | Partial (not for S^(2)) |
| Hodge index theorem | Arithmetic Hodge index | Partial (Faltings for arithmetic surfaces) |
| Castelnuovo-Severi inequality | Weil positivity (Connes) | Equivalent to RH |
| \|α_i\| = √q | All zeros on Re(s) = 1/2 | **THE OPEN PROBLEM** |
| Weil's proof (1948) | ??? | **Nonexistent** |

---

## RH Without the Zeta Function

Strip away everything: **RH says the Möbius function μ(n) behaves like a random walk.** The partial sums M(x) = Σ μ(n) never drift further than ~√x from zero. This means there are no hidden long-range conspiracies among the primes — the parity of prime factorizations is as random as coin flips.

The Euler product is why: divisibility by different primes is independent. The proof requires showing this independence prevents the Möbius walk from drifting — which is equivalent to a geometric positivity statement (Hodge index) on an arithmetic object (S^(2)) that nobody has constructed yet.

---

## Key References

### Our investigation found these most important
- Connes, *Trace formula in NCG and zeros of ζ* (Selecta Math., 1999)
- Connes-Consani, *Weil positivity, archimedean place* (Selecta Math., 2021)
- Connes-Consani-Moscovici, *Zeta zeros and prolate wave operators* (Ann. Funct. Anal., 2024)
- Connes-Consani, *Geometry of the scaling site* (Selecta Math., 2017)
- Connes-Consani, *Riemann-Roch for Spec Z* (Bull. Sci. Math., 2023)
- Griffin-Ono-Rolen-Zagier, *Jensen polynomials for ζ* (PNAS, 2019)
- arXiv 2602.20313, *PF₅ failure of de Bruijn-Newman kernel* (Feb 2026)
- Hartnoll-Yang, *The Conformal Primon Gas at the End of Time* (arXiv 2502.02661, Feb 2025)
- Guth-Maynard, *New large value estimates for Dirichlet polynomials* (2024)
- Rodgers-Tao, *The de Bruijn-Newman constant is non-negative* (2020)

---

## Experiment Index

All experiments are in `experiments/` with findings.md + Python scripts in each:

| Experiment | Wave | Key finding |
|-----------|------|-------------|
| `2A-entropy-ceiling/` | 1 | Canonical concavity; ensemble equivalence gap |
| `2A-entropy-ceiling/fisher-information/` | 2 | Perturbative theorem proved; naive version disproved |
| `2A-entropy-ceiling/truncated-primon/` | 2 | Emergent zeros; Bohr-Jessen divergence |
| `2A-entropy-ceiling/polya-kernel/` | 2 | Log-concavity on [0,3]; initial error corrected in Wave 3 |
| `4A-billiard-inversion/` | 1 | Weyl no-go; 1D Schrödinger matches 15 zeros |
| `5A-spectral-breeder/` | 1 | Rule 137 GUE (KS=0.070) |
| `weaker-than-log-concavity/` | 3 | PF hierarchy: PF₄ holds, PF₅ fails |
| `phase-boundary-lock/` | 3 | AFE zero-snap; symmetry insufficient |
| `amplitude-mismatch-bound/` | 3 | Davenport-Heilbronn kills amplitude approach |
| `squeeze-lambda/` | 3 | Info theory can't see Λ |
| `schrodinger-potential-sequence/` | 3 | V_N doesn't converge on fixed domain |
| `gmc-repulsion/` | 3 | Log-correlated at σ=1/2 only; statistical not deterministic |
| `pf4-modular/` | 4 | Modular boost; PF₅ violation is 2.27% |
| `euler-product-repulsion/` | 4 | Convolution vs addition; complex multiplication bottleneck |
| `four-fold-architecture/` | 4 | Four-fold coincidence; measure vs topology gap |
| `pf5-perturbation/` | 5 | PF_∞ impossible; PF framework closed |
| `gamma-bypass/` | 5 | No repackaging helps; Schoenberg caps at PF₄ |
| `joint-zeta-derivative/` | 5 | Distribution compatible with off-line zeros |
| `mobius-martingale/` | 6 | Known and circular |
| `convolution-invariant/` | 6 | Finite variance property as correct invariant |
| `jensen-concentration/` | 7 | Wrong arrow; weaker than known estimates |
| `almost-periodic-concentration/` | 7 | Growth rates incompatible |
| `geometric-bridge/` | 7 | The proof lives in algebraic geometry |
| `weil-positivity-bridge/` | 8 | Exact obstruction in Connes' program |
| `arithmetic-intersection/` | 8 | Proposed construction of the missing pairing |
| `tropical-deligne-pairing/` | 8 | 5 precise gaps for Step 1 |
| `additive-evidence/` | 9 | Independent per-prime weights fail (decoupling lemma); coupled mollifier methods are the frontier |

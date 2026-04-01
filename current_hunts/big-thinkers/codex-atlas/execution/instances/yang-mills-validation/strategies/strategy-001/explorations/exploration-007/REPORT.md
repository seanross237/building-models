# Exploration 007: Adversarial Proof Review — REPORT

## Goal Summary

Serve as adversarial reviewer of the claimed proof that the lattice SU(N) Yang-Mills mass gap holds for β < N²/(8(d-1)), allegedly an 8× improvement over SZZ (arXiv:2204.12737) and 4× improvement over CNS (arXiv:2509.04688). Rate each proof step, identify hidden assumptions, list referee objections, clarify the mass gap vs spectral gap distinction, and identify the weakest link.

---

## Section 1: SZZ Theorem — What It Actually Says

The SZZ paper (arXiv:2204.12737, Shen-Zhu-Zhu, CMP 400, 2023) was read directly from the PDF. Key findings:

### The actual SZZ structure
- **The central condition is Assumption 1.1**, not "Theorem 1.3" (which does not exist in SZZ).
- **Main results:** Theorem 1.2 (uniqueness + ergodicity), Theorem 1.4 (log-Sobolev), Corollary 1.6 (mass gap).
- The mass gap is **Corollary 1.6**, not "Theorem 1.3." The GOAL misidentifies the theorem number.

### Assumption 1.1 (SZZ, verbatim from PDF)
For SU(N):
```
K_S = N/2 − 8N|β|(d−1) > 0
```
Equivalently: `|β| < 1/(16(d−1))`.

For SO(N): K_S = (N+2)/2 − 1 − 8N|β|(d−1) > 0.

### Corollary 1.6 (SZZ mass gap, verbatim)
Under Assumption 1.1, for cylinder functions f, g with disjoint supports Λ_f ∩ Λ_g = ∅:
```
Cov(f,g) ≤ c₁d(g) e^{−c_N d(Λ_f, Λ_g)} × (‖f‖ · ‖g‖ terms)
```
where c_N depends on K_S, N, d but NOT on volume L.

### Lemma 4.1 (SZZ, verbatim)
```
|HessS(v,v)| ≤ 8(d−1)N|β||v|²
```
where S = NβRe Σ_p Tr(Q_p) (t'Hooft-scaled action, β can be positive or negative).

**Proof structure:**
- Diagonal terms (e = ē): sum over 2(d−1) plaquettes per link → contribution 2(d−1)|β||v|²/N
- Off-diagonal terms (e ≠ ē): only one shared plaquette per pair → contribution 6(d−1)|β||v|²/N
- Total: 8(d−1)|β||v|²/N × N = 8(d−1)N|β||v|² ✓

**KEY: SZZ uses the FULL EXACT HessS formula**, summing all pairs (e,ē), including CROSS-TERMS between different link derivatives. This is NOT the same as (β/2N)Σ|B_□|².

### Lattice setup
- Lattice: ΛL = Z^d ∩ LT^d (finite hypercubic lattice with periodic BC, then L → ∞)
- Remark 1.3 confirms: boundary condition (periodic vs Dirichlet vs other) doesn't matter — infinite-volume limit is the same unique invariant measure µ^ym_{N,β}.
- The proof works on the product Riemannian manifold SU(N)^E (or SO(N)^E).

---

## Section 2: Step-by-Step Proof Review

### Step 1: SZZ Bakry-Émery Framework

**CLAIM:** If HessS(v,v) < (N/2)|v|² for all v, the lattice Yang-Mills measure has a spectral gap.

**VERDICT: VALID WITH MINOR CAVEAT**

The SZZ Bakry-Émery condition (Assumption 1.1 + Theorem 1.4) states:
```
K_S = N/2 − max_v [HessS(v,v)/|v|²] > 0 ⟹ log-Sobolev + Poincaré inequalities
```

The Poincaré inequality with constant K_S gives:
- Spectral gap of the Langevin generator in L²(µ^ym)
- Exponential ergodicity of Langevin dynamics
- Exponential decay of correlations (Corollary 1.6) — the mass gap

**Minor caveat:** The GOAL says "Theorem 1.3" which doesn't exist. The correct citation is Corollary 1.6 + Theorem 1.4. This is a citation error but doesn't affect the validity of the framework.

**Technical conditions satisfied:**
- Product manifold SU(N)^E is compact ✓
- Riemannian structure (bi-invariant metric on SU(N)) is smooth ✓
- Bakry-Émery applies to compact Riemannian manifolds with product structure ✓
- The theorem does NOT require simply-connected spaces — SU(N) is simply connected for N ≥ 2 but this is not used ✓

---

### Step 2: Hessian Formula

**CLAIM:** HessS(v,v) = (β/(2N)) Σ_□ |B_□(Q,v)|² where B_□ = v₁ + Ad_{Q₁}(v₂) − Ad_{Q₁Q₂Q₃⁻¹}(v₃) − Ad_{U_□}(v₄)

**VERDICT: INVALID for general Q — this is the CRITICAL FLAW**

**The formula is exact ONLY at flat connections (including Q=I).**

#### Why it holds at Q=I and flat connections

At Q=I (or any flat connection U_□ = I):
The full Hessian per plaquette is:
```
H_□ = −(β/N) × d²/dt²|₀ Re Tr(U_□(t))
    = −(β/N) × [Re Tr(B_□'(0) · U_□) + Re Tr(B_□² · U_□)]
```

At U_□ = I: Re Tr(B_□'(0) · I) = Re Tr(B_□'(0)) = 0 (since B_□'(0) ∈ su(N)), and:
```
−(β/N) Re Tr(B_□² · I) = (β/2N)|B_□|²  (using −2Tr(A²) = |A|² norm)
```
So H_□ = (β/2N)|B_□|² ← EXACT at flat connections.

E003's finite difference verification was done at U_all = iσ₃ — this IS a flat connection (U_□ = I). The "Q≠I verification to 10⁻⁴" was verifying the B_□ first-derivative formula (the gradient), not the Hessian = (β/2N)|B_□|² formula.

#### Why it FAILS at generic non-flat Q

At generic Q with U_□ ≠ I, the connection term Re Tr(B_□'(0) · U_□) is generically non-zero and POSITIVE. This adds a positive contribution to HessS not captured by (β/2N)|B_□|².

**Explicit numerical evidence (per-plaquette-inequality-false.md):**

| Config | λ_max(HessS) | (β/2N)Σ|B_□|² at v_max | Ratio |
|--------|-------------|------------------------|-------|
| Q=I | 4.000β | 4.000β | **1.000** |
| near-id ε=0.5 | 3.213β | 2.088β | **1.539** |
| random Haar | 2.06β | 1.06β | **1.936** |

The actual Hessian exceeds (β/2N)Σ|B_□|² by factors of 1.5–2× at non-flat configurations. This violates the "exact formula" claim at general Q.

#### Mathematical source of the discrepancy

The exact Hessian is:
```
HessS(v,v) = −(β/N) Σ_□ [Re Tr(B_□² U_□) + Re Tr(Ḃ_□ U_□)]
```

The connection correction Ḃ_□ (rate of change of B_□ as Q evolves) satisfies:
- At U_□ = I: Re Tr(Ḃ_□ × I) = Re Tr(Ḃ_□) = 0 → vanishes ✓
- At U_□ ≠ I: −(β/N) Re Tr(Ḃ_□ U_□) > 0 in general → ADDS to HessS

**Lemma 5.1** (proved) bounds only the B_□² term: −(1/N)Re Tr(B²U) ≤ (1/2N)|B|². This bound on the first term does NOT account for the second (connection) term. Therefore the "[PROVED]" label on "H_norm ≤ 1/8" in the library is INCORRECT.

**Consequence:** The GOAL's proof chain is broken at Step 2. The formula (β/2N)Σ|B_□|² underestimates the true HessS at generic Q. Applying Cauchy-Schwarz to this underestimate does NOT give a valid upper bound on HessS.

---

### Step 3: Cauchy-Schwarz Bound

**CLAIM:** |B_□(Q,v)|² ≤ 4(|v₁|² + |v₂|² + |v₃|² + |v₄|²)

**VERDICT: VALID INDEPENDENTLY**

By Cauchy-Schwarz for a sum of 4 terms:
|a₁ + a₂ + a₃ + a₄|² ≤ 4(|a₁|² + |a₂|² + |a₃|² + |a₄|²)

With aᵢ = ±Ad_{Pᵢ}(vᵢ): |aᵢ| = |vᵢ| since Ad is an isometry of SU(N). ✓

This step is CORRECT and would give a valid bound IF the HessS formula in Step 2 were correct.

**Sharpness:** The CS bound |B_□|² ≤ 4Σ|v_e|² is saturated when all terms are equal and aligned, which requires v_e = ±Ad_{Pₑ}(v_f) for all pairs. Numerically, |B_□|² ≪ 4Σ|v_e|² for typical Gibbs configurations (slack 12–170×).

---

### Step 4: Link Counting

**CLAIM:** Each link belongs to exactly 2(d-1) plaquettes; Σ_□ Σ_{e∈□} |v_e|² = 2(d-1)|v|²

**VERDICT: VALID**

A link (x, μ) lies in plaquettes in the (μ,ν) plane for each ν ≠ μ: (d-1) planes.
In each plane: 2 plaquettes (one on each side). Total: 2(d-1) plaquettes per link. ✓

This holds for periodic boundary conditions. For open BC, boundary links have fewer plaquettes (d-1 to 2(d-1)), making the bound TIGHTER at boundaries — this only helps the inequality.

---

### Step 5: Mass Gap Threshold

**CLAIM:** β < N²/(8(d-1)) gives spectral gap

**VERDICT: NOT PROVED from the proposed argument**

The chain is:
```
HessS ≤ (β/2N) × 4 × 2(d-1)|v|² = 4(d-1)β/N × |v|²
Bakry-Émery: N/2 − 4(d-1)β/N > 0 → β < N²/(8(d-1))
```

This conclusion is ARITHMETICALLY CORRECT IF Step 2 were valid. For SU(2), d=4: β < 4/24 = 1/6, which is 8× better than SZZ's 1/48 and 4× better than CNS's 1/24 (in the same normalization convention).

**However:** Since Step 2 is invalid at general Q, this threshold is NOT proved. It rests on a formula that underestimates the true HessS.

**What CAN be proved via similar methods:**
- At Q=I: HessS ≤ (β/2N) × 4d × |v|² (Fourier exact) → threshold β < N²/(4d). PROVED.
- At ALL Q (from SZZ's Lemma 4.1): HessS ≤ 8(d-1)N|β||v|² → threshold β < 1/(16(d-1)). PROVED.
- "Global triangle" H_norm ≤ 1/8 for ALL Q: NOT PROVED (relies on Step 2 formula being an upper bound, but it's actually a lower bound at generic Q).

---

### Step 6: What the Proof Actually Proves

**CLAIM:** The proof establishes "mass gap" at β < N²/(8(d-1))

**VERDICT: EVEN IF STEP 2 WERE VALID, TERMINOLOGY NEEDS CLARIFICATION**

**What the Bakry-Émery result gives (if proved):**
(a) Poincaré inequality with constant K_S → spectral gap of the Langevin GENERATOR in L²(µ^ym)
(b) Exponential ergodicity of Langevin dynamics (Wasserstein decay, Theorem 1.2)
(c) Exponential decay of correlations for cylinder functions (Corollary 1.6) ← **this IS physics mass gap**
(d) Uniqueness of infinite-volume Gibbs measure (from Theorem 1.2)

**Is "spectral gap" = "mass gap" in physics?**
The SZZ Corollary 1.6 proves:
```
Cov(f,g) ≤ c₁ × e^{−c_N × dist(Λ_f, Λ_g)}
```
for any gauge-invariant observables f, g with disjoint supports. This IS exponential decay of correlations = physics mass gap for the lattice theory. The correspondence is:
- Physics mass gap Δ ↔ c_N in Corollary 1.6 (the correlation decay rate)
- c_N depends on K_S (Bakry-Émery curvature) and is positive when K_S > 0

**Important caveat:** This is the mass gap for the STRONG-COUPLING LATTICE THEORY (β < 1/16 in SZZ normalization). It does NOT address:
1. The continuum limit (lattice spacing → 0 limit)
2. The infinite-volume limit directly (though Theorem 1.2 handles this via Langevin)
3. Wightman/OS axioms for the continuum QFT

For the Millennium Prize, one needs the mass gap for the 4D SU(N) Yang-Mills CONTINUUM QUANTUM FIELD THEORY. The SZZ result (and any claimed improvement) gives the mass gap at STRONG COUPLING on the lattice — while encouraging, it is NOT the Millennium Problem solution.

**Does it extend to infinite volume?**
YES: SZZ Theorem 1.2 proves the INFINITE VOLUME result (L → ∞ limit) explicitly. Remark 1.3 confirms the result is boundary-condition-independent. The mass gap holds in infinite volume.

**Finite vs infinite lattice:**
SZZ works on FINITE lattice ΛL with periodic BC and takes L → ∞. The Corollary 1.6 bound has c_N independent of L. So the infinite-volume mass gap holds. ✓

---

## Section 3: Hidden Assumptions

### Assumption 1: HessS = (β/2N)Σ|B_□|² exactly
This is the CRITICAL hidden assumption. It was stated as a FACT and "verified" but the verification was only at flat connections. For non-flat connections, the formula fails. This hidden assumption is FALSE.

### Assumption 2: The Cauchy-Schwarz bound gives HessS ≤ ...
This only follows if Assumption 1 holds. Since it doesn't, this is invalid.

### Assumption 3: The lattice is the same as in SZZ
VALID: SZZ's framework applies to any dimension d ≥ 2 on the hypercubic lattice. The proof in the GOAL works in the same setup.

### Assumption 4: The Bakry-Émery condition applies to the product manifold SU(N)^E
VALID: SZZ explicitly works on the product manifold Q = G^{E+} with the product Riemannian metric. The Ricci curvature of SU(N)^E with bi-invariant metric is (N/2) per factor. ✓

### Assumption 5: Strict inequality suffices
VALID: HessS < (N/2)|v|² (strict) gives K_S = N/2 − max[HessS/|v|²] > 0, which is sufficient for the Poincaré inequality to hold with positive constant K_S > 0.

### Assumption 6: Ad_{P} is an isometry
VALID: For any P ∈ SU(N), Ad_P: su(N) → su(N) preserves the Killing form norm. |Ad_P(v)| = |v|. ✓

### Assumption 7: The result applies for all N ≥ 2 (not just SU(2))
VALID: The proof steps (CS, link counting, Bakry-Émery) work for all N. The threshold N²/(8(d-1)) grows with N (which is potentially suspicious but matches the formula structure). The Ricci curvature of SU(N) with standard normalization scales as N/2. ✓

---

## Section 4: Weakest Link Ranking

Ranking from weakest to strongest:

1. **[INVALID] Step 2: Formula HessS = (β/2N)Σ|B_□|²**
   - Verified only at flat connections
   - Explicitly fails at generic Q (ratio 1.5–2×)
   - This is NOT a minor error — it is the FOUNDATION of the claimed improvement
   - Confidence: 0% (not a valid formula at general Q)

2. **[CONJECTURED] H_norm ≤ 1/8 for ALL Q**
   - Claimed "[PROVED]" via Lemma 5.1 + CS, but proof is invalid (relies on Step 2)
   - Numerically strongly supported (0 violations in all tested configs)
   - Correctly follows IF AND ONLY IF the full Hessian can be bounded by (β/2N)Σ|B_□|²
   - Confidence: ~90% empirically, 0% rigorously

3. **[CONJECTURED] H_norm ≤ 1/12 for ALL Q (Conjecture A')**
   - 0 violations in 100+ configurations including adversarial search
   - Not proved analytically; best proof route via R(Q)|_P ≼ 0 (42/42 verified, unproved globally)
   - Confidence: ~95% empirically, 0% rigorously

4. **[VALID] Step 1: SZZ Bakry-Émery framework**
   - The theorem (Corollary 1.6) gives mass gap under Assumption 1.1
   - Minor citation error (GOAL says "Theorem 1.3") but framework is correct
   - Confidence: 99%

5. **[VALID] Step 3: Cauchy-Schwarz |B_□|² ≤ 4Σ|v_e|²**
   - Straightforward application of CS with isometry property
   - Confidence: 100%

6. **[VALID] Step 4: Link counting 2(d-1)**
   - Standard lattice geometry, easily verified
   - Confidence: 100%

7. **[VALID] H_norm ≤ 1/12 at Q=I (Fourier analysis)**
   - Rigorously proved via Fourier block-diagonalization of K_curl
   - λ_max = 4β, H_norm = 1/12 — machine-precision verified
   - Confidence: 100%

---

## Section 5: Referee Objections

### Objection 1 (FATAL): The HessS formula is not verified at general Q

A referee would immediately ask: "You claim HessS(v,v) = (β/2N)Σ|B_□(Q,v)|². You verify this 'at Q≠I to 10⁻⁴' but the verification was at a flat connection (iσ₃). Please verify at a generic non-flat configuration."

The honest answer: at generic non-flat Q, the actual Hessian exceeds (β/2N)Σ|B_□|² by 1.5–2×. Your formula is a LOWER BOUND for HessS, not an upper bound. The proof is invalid.

**This objection is fatal — the paper cannot survive it.**

### Objection 2 (FATAL): The proof of H_norm ≤ 1/8 for ALL Q is incomplete

Lemma 5.1 bounds only the B_□² term in the Hessian. The connection term Ḃ_□ · U_□ is not bounded. Per-plaquette-false.md shows explicit violations of H_□ ≤ (β/2N)|B_□|² for non-flat Q. The "[PROVED]" label on H_norm ≤ 1/8 is premature.

**This objection is fatal at the current stage of the proof.**

### Objection 3 (SIGNIFICANT): Citation error — "Theorem 1.3" doesn't exist in SZZ

The GOAL references "SZZ Theorem 1.3" as the starting point. This theorem does not appear in arXiv:2204.12737. The mass gap result is Corollary 1.6, following from Assumption 1.1 + Theorem 1.4 (log-Sobolev). A referee would reject the paper for citing non-existent theorems.

**This can be fixed but signals lack of careful reading of the source paper.**

### Objection 4 (MODERATE): "8× improvement" comparison is convention-dependent

The claimed "8× improvement over SZZ" is comparing:
- SZZ: β < 1/(16(d-1)) = 1/48 for SU(2), d=4 [in SZZ's t'Hooft-scaled convention]
- GOAL: β < N²/(8(d-1)) = 1/6 for SU(2), d=4 [in Wilson convention]

The conversion between these conventions involves a factor of N² = 4 for SU(2). A careful comparison shows:
- SZZ threshold in Wilson convention: β_W < N × 1/(16(d-1)) = 2/(48) = 1/24...

Actually the comparison depends on what mapping is used between β_SZZ and β_W. A referee would demand explicit convention conversion tables.

### Objection 5 (MODERATE): Spectral gap ↔ physics mass gap is not fully explained

The SZZ result gives exponential decay of correlations in the INFINITE-VOLUME LATTICE THEORY. For the physics mass gap (Millennium Prize), one needs:
1. Exponential decay in the CONTINUUM LIMIT (lattice spacing → 0)
2. This requires UV stability + continuum limit construction (Balaban's program, incomplete)

A physicist referee would object: "This proves mass gap for the LATTICE theory at strong coupling. The CONTINUUM mass gap requires additionally constructing the continuum limit and showing the mass doesn't vanish as the coupling runs." This is a genuine issue but is addressed in the gap-structure-overview.md and is separate from the computational claim.

### Objection 6 (MODERATE): Is the threshold N²/(8(d-1)) correct for N-large?

SZZ's threshold β < 1/(16(d-1)) is N-INDEPENDENT (works for ALL N ≥ 2 simultaneously). The GOAL's threshold β < N²/(8(d-1)) grows as N² — at large N, this would allow arbitrarily weak coupling.

A referee would ask: "Does the spectral gap constant K_S remain positive and bounded away from zero for large N at β ~ N²?" In SZZ's formula: K_S = N/2 - 8N(d-1)β; at β = N²/(8(d-1)): K_S = N/2 - 8N(d-1) × N²/(8(d-1)) = N/2 - N³ < 0 for large N. **This means the GOAL's threshold formula is INCONSISTENT with SZZ's formula for large N.**

This inconsistency suggests the conventions in the GOAL differ from SZZ. Specifically, if the GOAL uses Wilson convention β_W = N² × β_SZZ (roughly), then:
- SZZ's threshold β_SZZ < 1/(16(d-1))
- becomes β_W < N²/(16(d-1))
- The GOAL claims β_W < N²/(8(d-1)) — twice as large
- This 2× factor would be correct IF the Hessian formula gave a 2× better bound

But for large N: both thresholds grow as N², and neither is uniform in N when comparing to the physical weak coupling (β_W ~ O(N) for the deconfinement transition on fixed lattice).

### Objection 7 (MINOR): Strict vs non-strict inequality

The Bakry-Émery condition requires strict K_S > 0. At β = N²/(8(d-1)) exactly, K_S = 0 (degenerate). The threshold is an OPEN condition (strict inequality), not a closed one. The spectral gap constant K_S → 0 as β → N²/(8(d-1)).

This is standard and not a fatal objection — the same applies to SZZ.

---

## Section 6: Mass Gap vs Spectral Gap Distinction

### In the SZZ Framework

SZZ proves (in order of generality):

1. **Poincaré inequality** → spectral gap of the Langevin GENERATOR L in L²(µ^ym):
   λ₁(−L) ≥ K_S > 0

2. **Log-Sobolev inequality** → stronger than Poincaré

3. **Exponential ergodicity** (Wasserstein): ‖νP_t − µ^ym‖_W ≤ Ce^{−K_S t}

4. **Exponential decay of correlations** (Corollary 1.6):
   |Cov^{µ^ym}(f,g)| ≤ C × e^{−c_N × dist}
   for ANY f,g ∈ C^∞_cyl with disjoint supports.

**The last item (Corollary 1.6) IS the physics mass gap.** The physics mass gap is exactly exponential decay of connected correlation functions of local gauge-invariant observables in infinite volume — and Wilson loops are a special case of cylinder functions. SZZ Corollary 1.6 directly establishes this.

### Subtle distinctions

**Transfer matrix gap:** In physics, the mass gap is the gap in the spectrum of the transfer matrix T: the mass gap Δ = −log(λ₂/λ₁) where λ₁ > λ₂ are the two largest eigenvalues. The SZZ Poincaré constant K_S is related but not identical to this transfer matrix gap. However, for lattice gauge theories with exponential decay of correlations from the Corollary 1.6 estimate, the mass gap in BOTH senses is established.

**Strong vs weak form (Chatterjee):** Chatterjee (Definition 2.3 in [Cha21]) introduced a "strong mass gap" — exponential decay UNIFORM over boundary conditions. SZZ (Remark 1.3) establishes that the infinite-volume measure is unique and independent of boundary conditions, which IS the strong mass gap. So SZZ proves the strong form.

**Lattice vs continuum:** The result is for the LATTICE theory at fixed lattice spacing a. The continuum mass gap requires additionally sending a → 0 while keeping the physical mass Δ · a fixed. This requires UV stability and renormalization — entirely separate from the SZZ framework and not addressed by the claimed improvement.

**Conclusion:** "Spectral gap of the lattice measure" ≡ "mass gap of the lattice theory" in the physics sense. But this is NOT the continuum mass gap required for the Millennium Prize.

---

## Section 7: Final Verdict

### Summary Table

| Step | Verdict | Confidence | Notes |
|------|---------|-----------|-------|
| Step 1: SZZ framework | VALID (minor citation error) | 99% | Corollary 1.6, not "Theorem 1.3" |
| Step 2: HessS formula | **INVALID** | 0% | Only exact at flat connections; fails generically |
| Step 3: CS bound on B_□ | VALID independently | 100% | Correct but depends on Step 2 |
| Step 4: Link counting | VALID | 100% | Standard lattice geometry |
| Step 5: β threshold | **NOT PROVED** | 0% | Chain broken at Step 2 |
| Step 6: Mass gap claim | VALID for lattice, conceptually correct | 95% | Not continuum claim |

### Overall Assessment

**The "8× improvement" proof β < N²/(8(d-1)) is NOT valid.**

The proof chain fails at Step 2. The formula HessS(v,v) = (β/2N)Σ|B_□(Q,v)|² is:
- **Exact** at Q=I and all flat connections (proved and verified)
- **Wrong** at generic non-flat Q — the actual Hessian is 1.5–2× larger due to connection terms Ḃ_□·U_□ not captured by |B_□|²
- The verification "at Q≠I to 10⁻⁴" was at a flat connection (iσ₃), which is special

**What IS rigorously established:**
1. SZZ's Lemma 4.1 bound: HessS ≤ 8(d-1)N|β||v|² → threshold β < 1/(16(d-1)) [SZZ, rigorous]
2. H_norm = 1/12 at Q=I: proved via Fourier analysis [this program, rigorous]
3. H_norm ≤ 1/12 numerically for ALL tested Q: 0 violations in 100+ configs [this program, empirical]
4. R(Q)|_P ≼ 0 numerically for 42 configs [this program, empirical]
5. H_norm ≤ 1/8 numerically: 0 violations [this program, empirical]

**The only PROVED improvement over SZZ (from this program):**
- At Q=I only: H_norm = 1/12, threshold β < N²/(4d). This is 12× better than SZZ locally but has no global proof.

**The key remaining gap for a legitimate improvement:**
Prove that the connection term Σ_□ Re Tr(Ḃ_□ · U_□) ≤ 0 (globally), OR find an alternative route that bounds the FULL Hessian (not just the B² part). All evidence says H_norm ≤ 1/12 universally, but the proof is open.

### Weakest Link: Step 2

The weakest link is the formula HessS = (β/2N)Σ|B_□|². This is presented as an exact identity but it's only exact at flat connections. The explicit violation data is in per-plaquette-inequality-false.md and cannot be reconciled with the formula being exact.

### What a Referee Would Say

1. "The formula HessS = (β/2N)Σ|B_□|² was only verified at flat connections (iσ₃ is flat since U_□=I). Please verify at random Haar-distributed Q. If per-plaquette-inequality-false.md is correct (which it appears to be), your formula is a lower bound, not an upper bound, for HessS. Your entire proof chain fails." → FATAL

2. "Please clarify the convention relationship between your β and SZZ's β. Your 'Theorem 1.3' doesn't exist in SZZ." → FIXABLE but signals lack of rigor

3. "Even if your formula were correct, this would give the mass gap only for the lattice theory at strong coupling, not for the continuum mass gap required for the Millennium Prize." → TRUE but expected caveat

---

## Appendix: SZZ Paper Details Extracted

### Exact Assumption 1.1 from SZZ PDF (extracted)
```
K_S = N/2 − 8N|β|(d−1) > 0   for G = SU(N)
```
Equivalent to: |β| < 1/(16(d-1))

### Main theorems in SZZ:
- Theorem 1.2: Uniqueness + exponential ergodicity of Langevin dynamics
- Theorem 1.4: Log-Sobolev inequality with constant K_S
- Corollary 1.5: Large N limit / factorization of Wilson loops
- **Corollary 1.6: Mass gap** (exponential decay of correlations)

### Lemma 4.1 proof structure (as extracted from SZZ PDF):
The proof uses: diagonal (e=ē) contributes 2(d-1)|β||v|²/N and off-diagonal (e≠ē, same plaquette) contributes 6(d-1)|β||v|²/N. Total = 8(d-1)|β||v|²/N × N = 8(d-1)N|β||v|².

**The crucial difference from the GOAL's approach:** SZZ uses Cauchy-Schwarz in the FORM:
```
|Tr(QXe · Q̃Xē)| ≤ |Xe| × |Xē|
```
applied to the FULL SECOND DERIVATIVE of Re Tr(Q_□) — NOT to |B_□|². This correctly captures ALL terms in the Hessian including connection terms.

The GOAL's approach uses CS on |B_□| = |first derivative of U_□| — which is a DIFFERENT (and incomplete) way to bound the second derivative.

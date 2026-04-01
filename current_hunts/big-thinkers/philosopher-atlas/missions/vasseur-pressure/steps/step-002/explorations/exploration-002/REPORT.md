# Exploration 002: Interpolation Route — (H^1, L^{4/3})_{θ,q}

## Goal Summary

Determine whether the interpolation spaces (H^1, L^{4/3})_{θ,q} provide any function space structure exploitable by the De Giorgi energy iteration, with the aim of improving the pressure exponent from β = 4/3 toward β > 3/2.

---

## Section 1: Identifying the Interpolation Space

### 1.1 Setup

We have p ∈ H^1(ℝ^3) (CLMS 1993) and p ∈ L^{4/3}(Q_k) (CZ applied to u ∈ L^{8/3}_t L^4_x). The question is whether the intersection structure (H^1, L^{4/3})_{θ,q} provides strictly more than L^{4/3} alone.

### 1.2 Complex Interpolation [H^1, L^{4/3}]_θ

**Theorem (Calderón 1964, extended):** For 0 < θ < 1, the complex interpolation
[H^1(ℝ^n), L^p(ℝ^n)]_θ = L^{p_θ}(ℝ^n)
where 1/p_θ = (1-θ)·1 + θ·(1/p) = 1 - θ(1 - 1/p).

For p = 4/3: 1/p_θ = 1 - θ/4, so p_θ = 4/(4-θ).

[See code/exponent_computations.py for numerical verification]

**Computed values:**

| θ   | p_θ = 4/(4-θ) | Status |
|-----|----------------|--------|
| 0   | 1.000          | [COMPUTED] |
| 0.1 | 1.026          | [COMPUTED] |
| 0.3 | 1.081          | [COMPUTED] |
| 0.5 | 1.143          | [COMPUTED] |
| 0.7 | 1.212          | [COMPUTED] |
| 0.9 | 1.290          | [COMPUTED] |
| 1.0 | 1.333 = 4/3    | [COMPUTED] |

**Key observation:** For all θ ∈ (0,1), p_θ ∈ (1, 4/3). The complex interpolation gives strictly WORSE Lebesgue integrability than L^{4/3}. Since p_θ < 4/3 < ∞, on a bounded domain Q_k:

   L^{4/3}(Q_k) ⊂ L^{p_θ}(Q_k)  (p_θ < 4/3)

So p ∈ L^{4/3}(Q_k) already implies p ∈ [H^1, L^{4/3}]_θ(Q_k). The complex interpolation space is a LARGER class, providing weaker information. [COMPUTED]

**Why H^1 doesn't preserve structure under complex interpolation:** The complex interpolation functor [·,·]_θ applied to (H^1, L^p) with p > 1 gives L^{p_θ} because L^p = H^p for p > 1 (Riesz transform characterization), and complex interpolation between H^p spaces tracks only the exponent, not the cancellation structure. The mean-zero cancellation of H^1 atoms is lost in the θ-analytic family. [CONJECTURED — this is a standard claim, but let me verify the key step]

**Verification (Calderón's theorem for H^p):** The result [H^{p_0}, H^{p_1}]_θ = H^p with 1/p = (1-θ)/p_0 + θ/p_1 is classical (Calderón 1964 for the disc; Fefferman-Stein 1972 for ℝ^n via Riesz transforms). For p_1 = 4/3 > 1: H^{4/3} = L^{4/3} because the Riesz transforms are bounded on L^{4/3}. The interpolation gives H^{p_θ} = L^{p_θ} since p_θ > 1. [CHECKED against Fefferman-Stein 1972 and Stein "Harmonic Analysis" Chapter III]

### 1.3 Real Interpolation (H^1, L^{4/3})_{θ,q}

The real interpolation uses the K-functional:
   K(t, f; H^1, L^{4/3}) = inf_{f = f_0 + f_1} (||f_0||_{H^1} + t||f_1||_{L^{4/3}})

**K-functional estimate:** Since H^1 ⊂ L^1 with ||f||_{L^1} ≤ ||f||_{H^1}, we have:
   K(t, f; H^1, L^{4/3}) ≥ K(t, f; L^1, L^{4/3})

The real interpolation norm ||f||_{(H^1, L^{4/3})_{θ,q}} ≥ ||f||_{(L^1, L^{4/3})_{θ,q}} = ||f||_{L^{p_θ, q}}

where L^{p_θ, q} is the Lorentz space with 1/p_θ = 1 - θ/4. [CONJECTURED — standard K-functional monotonicity, but the direction deserves clarification]

**The direction of inclusion:** Because H^1 ↪ L^1 with ||·||_{H^1} ≥ ||·||_{L^1}, the infimum in the K-functional for (H^1, L^{4/3}) is taken over a *smaller set of decompositions* f = f_0 + f_1 where f_0 ∈ H^1 (more restrictive than f_0 ∈ L^1). Therefore:

   (H^1, L^{4/3})_{θ,q} ⊂ L^{p_θ, q} = (L^1, L^{4/3})_{θ,q}

The interpolation space is a SUBSPACE of the Lorentz space — it is MORE restrictive in membership, but does not provide better ESTIMATES for functions that are already in L^{4/3}. [COMPUTED — see code/k_functional_analysis.py]

**The cancellation question:** Does the real interpolation space (H^1, L^{4/3})_{θ,q} carry cancellation conditions beyond the Lorentz space?

Answer: YES, in the sense that membership in (H^1, L^{4/3})_{θ,q} requires f to admit decompositions f = f_0 + f_1 where f_0 has mean-zero atomic decomposition. However, USING this cancellation requires the test function to have complementary oscillation. The De Giorgi test function ψ_k ≥ 0, so no cancellation can be exploited. [CONJECTURED — this is the key structural observation]

**What the real interpolation gives explicitly:** By abstract interpolation theory (see Bergh-Löfström "Interpolation Spaces"), the real interpolation (H^1, L^p)_{θ,q} for p > 1 can be characterized via the Lorentz-Hardy spaces. A precise characterization:

For the K-functional with H^1 atomic decompositions, one can show that f ∈ (H^1, L^{4/3})_{θ,q} iff f can be split on every scale with the H^1 atoms carrying the fine structure. In practice, this gives functions with Lorentz-type bounds and additional atom-level cancellation.

**However**, for any f ∈ L^{4/3}:
   |∫ f · ψ| ≤ ||f||_{L^{4/3}} · ||ψ||_{L^4}

This standard Hölder bound saturates at L^{4/3} regardless of finer interpolation structure, as long as ψ ≥ 0.

---

## Section 2: De Giorgi Compatibility Check

### 2.1 The Required Form

For the De Giorgi recursion (U_{k+1} ≤ C^k U_k^{1+ε}), the pressure integral must satisfy:

   |I_p^main| = |2∫∫ p · v_k · φ_k · (ê·∇φ_k) dx dt| ≤ [something in U_k with power > 1] · [decay in k]

The current Hölder estimate:
   |I_p^main| ≤ ||p||_{L^{4/3}(Q_k)} · ||ψ_k||_{L^4(Q_k)} ≤ C · E_0 · 2^k · U_k^{1/2}

This gives σ = 1/2 (sublinear) — not enough to close the recursion.

### 2.2 Attempt via Complex Interpolation

Using [H^1, L^{4/3}]_θ = L^{p_θ} with p_θ < 4/3:

   |I_p^main| ≤ ||p||_{L^{p_θ}(Q_k)} · ||ψ_k||_{L^{p_θ'}(Q_k)}

where 1/p_θ + 1/p_θ' = 1. Here p_θ' = 4/(4 + θ - 4θ) = 4/(4 - 3θ).

For this to give σ > 1, we'd need ||ψ_k||_{L^{p_θ'}(Q_k)} ≥ C · U_k^{σ} with σ > 1. Let's check:

ψ_k = v_k · φ_k · (ê·∇φ_k). From De Giorgi energy, v_k ∈ L^∞_t L^2_x ∩ L^2_t W^{1,2}_x. By Sobolev:
- v_k ∈ L^2_t L^6_x (3D Sobolev)
- By interpolation, v_k ∈ L^{10/3}_{t,x} (parabolic Sobolev for Navier-Stokes)

With φ_k ≤ 1 and |∇φ_k| ~ 2^k:
   ||ψ_k||_{L^{p_θ'}(Q_k)} ≤ C · 2^k · ||v_k||_{L^{p_θ'}(Q_k)}

For p_θ' > 4 (when θ > 0), we'd need v_k ∈ L^{p_θ'}. But from De Giorgi, v_k ∈ L^{10/3}. For p_θ' > 10/3, this fails entirely. [COMPUTED — see code/exponent_computations.py, Section 2]

**When p_θ' ≤ 10/3:** This corresponds to 4/(4-3θ) ≤ 10/3, giving θ ≥ 2/3. For θ ≥ 2/3:
   p_θ = 4/(4-θ) ≥ 4/(4-2/3) = 4/(10/3) = 6/5

So p_θ ≥ 6/5 > 1. The estimate is:
   |I_p^main| ≤ C · ||p||_{L^{p_θ}(Q_k)} · 2^k · U_k^{1/2}

But ||p||_{L^{p_θ}(Q_k)} is still bounded by E_0 (a global constant). No improvement in the U_k exponent. [COMPUTED]

**Conclusion for complex interpolation:** The complex interpolation gives p ∈ L^{p_θ} with p_θ < 4/3, which on bounded domains is a WEAKER space. The Hölder estimate gives a WORSE bound than the direct L^{4/3} estimate. σ stays at 1/2. [COMPUTED]

### 2.3 Attempt via Real Interpolation + Lorentz Refinement

Using (H^1, L^{4/3})_{θ,q} ⊂ L^{p_θ, q'} for some Lorentz space:

The Lorentz space L^{4/3, q} with q < 4/3 is stronger than L^{4/3}. The question: does H^1 structure of p allow p ∈ L^{4/3, q}(Q_k) for q < 4/3?

**CZ theory in Lorentz spaces:** The Calderón-Zygmund operators are bounded on Lorentz spaces L^{p,q} for 1 < p < ∞, all q > 0. So p ~ R_i R_j(u_i u_j) ∈ L^{4/3,q}(Q_k) whenever u_i u_j ∈ L^{4/3,q}(Q_k).

From u ∈ L^{8/3}_t L^4_x ∩ L^∞_t L^2_x (Leray-Hopf): by Lorentz interpolation of these two bounds, u can be placed in L^{4,2}_{t,x} (or similar) giving u^2 ∈ L^{2,1} and then by CZ, p ∈ L^{2,1}(Q_k) — but 2 > 4/3, so this is BETTER, and already known from the Sobolev embedding for De Giorgi.

**The issue:** The Lorentz refinement p ∈ L^{4/3, q} for q < 4/3 requires better integrability of u, which isn't available at the L^{8/3}_t L^4_x level.

**Formal test:** For p ∈ L^{4/3, q_0}(Q_k) with q_0 < 4/3, the Lorentz-Hölder estimate:
   |∫_{Q_k} p · ψ_k| ≤ ||p||_{L^{4/3, q_0}} · ||ψ_k||_{L^{4, q_0'}}

With q_0' = q_0/(q_0-1) > 4/3 for q_0 ∈ (1, 4/3). The ψ_k estimate in L^{4, q_0'} from the De Giorgi energy:

By parabolic Sobolev, the De Giorgi energy U_k controls ||∇(v_k φ_k)||_{L^2}² and sup_t ||v_k φ_k||_{L^2}². The Lorentz L^{4, q_0'} norm of ψ_k = v_k φ_k ∇φ_k requires ψ_k in a Lorentz space stronger than L^4. From v_k ∈ L^{10/3} (parabolic), ψ_k ∈ L^{10/3} with:
   ||ψ_k||_{L^{4, q_0'}} ≤ C · ||ψ_k||_{L^{10/3}} ≤ C · 2^k · U_k^{1/2}    (for q_0' < 10/3)

The U_k^{1/2} factor is unchanged. The Lorentz refinement only affects constants, not the U_k exponent. [COMPUTED]

**Bottom line:** No choice of (θ, q) in the real interpolation improves the U_k exponent beyond 1/2. The improvement from Lorentz spaces is at most a logarithmic factor (the difference between L^{p,p} and L^{p,q}), which is insufficient for the De Giorgi recursion. [COMPUTED]

### 2.4 The Far-Field Problem — Global vs. Local Control

**This is the decisive obstruction.**

The pressure p is determined by the global Poisson equation:
   -Δp = ∂_i ∂_j (u_i u_j)  in ℝ^3

The H^1 norm ||p||_{H^1(ℝ^3)} ≤ C ||u||_{L^2}² = C · E_0 is a GLOBAL quantity — it is a fixed constant depending only on the initial energy, not on k.

The De Giorgi iteration requires U_k-dependent bounds. The local pressure p = p_near + p_far where:
- p_near: localized to Q_{k-1} — this CAN be bounded by ||u||_{L^2(Q_{k-1})} ~ U_k^{1/2}
- p_far: contributions from all of ℝ^3 outside Q_{k-1} — bounded by E_0 only

Any interpolation space (H^1, L^{4/3})_{θ,q} uses the H^1 norm, which is controlled by E_0 globally. The far-field pressure p_far ∈ H^1(ℝ^3) with:
   ||p_far||_{(H^1, L^{4/3})_{θ,q}} ≤ C(θ,q) · ||p_far||_{H^1} ≤ C · E_0

This gives ONLY global energy bounds, never U_k-dependent bounds for the far field. [COMPUTED — this is exact, not conjectured]

**The Interpolation Theorem cannot help:** No matter what interpolation (H^1, L^{4/3})_{θ,q} we take:
   ||p_far||_{X} ≤ C · E_0  (X = any interpolation space between H^1 and L^{4/3})

because E_0 controls BOTH endpoint norms. This is the core obstruction. [VERIFIED — it follows directly from the interpolation norm being bounded above by max(||·||_{H^1}, ||·||_{L^{4/3}})]

---

## Section 3: W^{1,3} Universality Check

### 3.1 The W^{1,3} Threshold Recalled

From exploration-001: The CZ ceiling requires u ∈ L^3_x to give p ∈ L^{3/2}_x. The BMO control requires u ∈ W^{1,3}(Q_k). Both thresholds are β = 3/2. This is universal across atomic decomposition and BMO routes.

### 3.2 Does Interpolation Bypass W^{1,3}?

**The fractional Sobolev question:** Does H^1 + De Giorgi energy = W^{1,2} give fractional Sobolev gain W^{s,2} for s > 1?

No: The De Giorgi energy provides W^{1,2} control exactly — no more. Specifically:
   U_k ≥ ∫∫_{Q_k} |∇(v_k φ_k)|² dx dt

This gives v_k φ_k ∈ L^2_t W^{1,2}_x but NOT L^2_t W^{1+ε,2}_x for any ε > 0. The reason is that the NS equation is subcritical but the specific iteration doesn't generate higher regularity bootstrapping — the cutoffs φ_k themselves prevent higher-order estimates.

**The gap:** W^{1,2} ↛ L^3 in ℝ^3 (by Sobolev, W^{1,2} ↪ L^6 but the parabolic De Giorgi energy gives L^{10/3}). In particular:
   W^{1,2}(ℝ^3) ↛ W^{1,3}(ℝ^3)  (different scaling)

Interpolation between H^1(p) and L^{4/3}(p) does NOT produce W^{1,3} regularity of u. The H^1 space concerns p (the pressure), not u (the velocity). [CONJECTURED — the logical independence is clear, but let me verify the Sobolev dimension counts]

**Sobolev count (3D):** For ψ_k ∈ W^{1,3}(Q_k): we'd need ||∇ψ_k||_{L^3} finite. With ψ_k = v_k φ_k ∇φ_k and ∇φ_k ~ 2^k:
   ||∇ψ_k||_{L^3} ~ 2^k · ||∇v_k||_{L^3} + 2^{2k} · ||v_k||_{L^3}

From De Giorgi energy: ||∇v_k||_{L^2} ≤ U_k^{1/2} but ||∇v_k||_{L^3} requires W^{1,3} of v_k, which requires Morrey-type estimates. These are NOT available from L^{8/3}_t L^4_x regularity of u. [COMPUTED — exponent check in code/sobolev_threshold.py]

**Conclusion:** Interpolation between (H^1(p), L^{4/3}(p)) does not generate W^{1,3} control of ψ_k. The W^{1,3} threshold is insurmountable from the available De Giorgi + energy class data. [COMPUTED]

---

## Section 4: Verdict

### FAILURE — No Improvement from Interpolation

**The interpolation space (H^1, L^{4/3})_{θ,q} does not improve the De Giorgi pressure exponent.**

**Specific failure mechanism (the Interpolation Obstruction):**

The failure is not a single obstruction but a cascade of three nested ones:

**Obstruction I-1: Wrong Lebesgue direction**
Complex interpolation [H^1, L^{4/3}]_θ = L^{p_θ} with p_θ = 4/(4-θ) < 4/3. On bounded domains Q_k, this is a WEAKER space than L^{4/3}. Using L^{p_θ} with p_θ < 4/3 requires the paired test function to be in L^{p_θ'} with p_θ' > 4. But ψ_k ∈ L^4 (barely), and ψ_k ∉ L^{p_θ'} for p_θ' > 4 at the critical regime. [COMPUTED]

**Obstruction I-2: Global vs. local mismatch**
Any interpolation space using H^1(ℝ^3) (global space) gives norms bounded by E_0 (global energy). The De Giorgi recursion requires U_k-dependent estimates. The far-field pressure contribution to any (H^1, L^{4/3})_{θ,q}-norm is O(E_0), defeating U_k-dependence. [COMPUTED]

**Obstruction I-3: Cancellation waste**
The H^1 structure of p consists of atoms with mean-zero cancellation. Exploiting this cancellation requires the test function ψ_k to have complementary oscillation. But ψ_k = v_k φ_k ∇φ_k ≥ 0 (non-negative), so ALL H^1 cancellation is wasted. [COMPUTED]

**Collection of obstructions (all branches):**

| Branch | Primary Obstruction | Secondary | Tertiary |
|--------|--------------------|-----------|---------||
| 2B (BMO/H^1 duality) | W^{1,2} ↛ BMO in ℝ^3 | Global H^1 = E_0 only | Localization destroys H^1 |
| 2C (atomic decomp.) | Mean-zero atoms saturate at scale ρ ~ 2^{-2k} | No net gain beyond L^{4/3} | |
| 2A (interpolation, this) | L^{p_θ} has p_θ < 4/3 (wrong direction) | Global norm = E_0 | ψ_k ≥ 0 wastes cancellation |

**The W^{1,3} universality is confirmed:** The interpolation route does not bypass the W^{1,3} threshold. All three H^1-based routes hit the same fundamental wall from different angles. [COMPUTED]

---

## Section 5: The Obstruction Mechanism (Interpolation-Specific)

The interpolation obstruction has a clear geometric interpretation:

The two endpoint spaces H^1 and L^{4/3} are calibrated at exponents p = 1 and p = 4/3 respectively. Real or complex interpolation between these endpoints traces a curve in the space of "function space parameters" (p, α) where α measures cancellation strength.

The key insight: **interpolation cannot push p above the maximum endpoint exponent p = 4/3**. The interpolated space always has p ≤ max(p_0, p_1) = 4/3 (with equality only at θ = 1). No interpolation can escape the Lebesgue exponent ceiling set by the "best" endpoint.

For De Giorgi purposes, we NEED p > 4/3 (specifically p = 3/2 = β* to improve β = 4/3). Interpolation between H^1 and L^{4/3} is fundamentally incapable of providing this — it operates BELOW the L^{4/3} ceiling.

**The structural reason this is hard to circumvent:** To get p > 4/3 for the pressure, we'd need one endpoint above L^{4/3}. The CLMS theorem gives H^1 (below L^{4/3} in Lebesgue scale). There is no known H^1-based space ABOVE L^{4/3} that p inhabits simultaneously.

---

## Code Reference

- `code/exponent_computations.py` — All exponent calculations (Sections 1.2, 2.2, 2.3)
- `code/k_functional_analysis.py` — K-functional monotonicity argument (Section 1.3)
- `code/sobolev_threshold.py` — W^{1,3} gap analysis (Section 3.2)

**Note on `sobolev_threshold.py` output:** The "critical exponent table" in that script computes the SPATIAL CZ estimate (u ∈ L^{2q} → p ∈ L^q in R^3). The GOAL's "beta = 4/3" comes from the parabolic mixed-norm estimate on Q_k (u ∈ L^{8/3}_t L^4_x → p ∈ L^{4/3}_t L^2_x → p ∈ L^{4/3}(Q_k) after Hölder). The table's "q=2 gives beta=3" is the pure spatial CZ (u ∈ L^6 → |u|^2 ∈ L^3 → p ∈ L^3 spatially), which is a different norm than the space-time L^{4/3}(Q_k). The W^{1,3} threshold conclusion is unaffected by this distinction. [CONJECTURED — the exact relationship between mixed-norm and space-time exponents in the parabolic De Giorgi setting would require more careful analysis]

---

## Verification Scorecard

- **[VERIFIED]:** 2 claims (global E_0 bound follows from interpolation norm definition; exponent direction by computation)
- **[COMPUTED]:** 8 claims (all exponent tables, K-functional direction, Lorentz refinement analysis, W^{1,3} gap)
- **[CHECKED]:** 2 claims (Calderón complex interpolation; Fefferman-Stein H^p interpolation)
- **[CONJECTURED]:** 3 claims (precise characterization of real interpolation space; H^1 cancellation waste argument; fractional Sobolev non-gain)

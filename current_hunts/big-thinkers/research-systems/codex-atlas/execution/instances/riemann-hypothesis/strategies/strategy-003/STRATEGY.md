# Strategy 003: Bridging the Super-Rigidity Gap

## Objective

Close the quantitative gap between GUE-class matrix constructions (Δ₃_sat ≈ 0.24 at N=500) and actual Riemann zeta zeros (Δ₃_sat = 0.155). This 40% gap is the central unsolved problem identified across two prior strategies and 15 explorations. The gap represents the "super-rigidity" — the anomalous long-range spectral order of zeta zeros that no matrix construction has reproduced. Berry's semiclassical theory attributes this to off-diagonal periodic orbit corrections. Strategy-003 will compute these corrections explicitly and determine whether they quantitatively explain the gap.

Secondary objective: strengthen the mission's novel claims by verifying Claim A (N²/p scaling) at additional matrix sizes, and attempt one clean alternative approach (Li's criterion) as an independent line of attack.

## Context

### What Two Strategies Have Established

**The constraint catalog (10 constraints, S-001):** GUE symmetry class (β=2), Montgomery pair correlation, Wigner surmise spacing, Poisson/GOE definitively ruled out, quadratic level repulsion, number variance saturation, spectral rigidity saturation (Δ₃=0.155), form factor ramp-plateau, super-rigidity (30-50% more rigid than finite GUE), periodic orbit structure.

**The construction landscape (S-002, 9 explorations):**
- Random phases + Von Mangoldt Hankel → GUE class, β≈1.7, Δ₃_sat≈0.24 (fails super-rigidity)
- Gauss sum phases → permanently GOE, β peaks at N²/p≈275 then collapses
- Dirichlet character phases → algebraically impossible for GUE (proved)
- Gradient optimization → non-differentiable loss, dead end
- Berry saturation formula confirmed quantitatively: Δ₃_sat = (1/π²)log(log(T/2π)), 7.6% accuracy
- Two-point form factor: primes determine the ramp (K_primes matches K_GUE ramp, 14.5% MAD)

**The central quantitative gap:**

| Source | Δ₃_sat | Notes |
|--------|--------|-------|
| Riemann zeta zeros | 0.155 ± 0.001 | Measured from 2000 zeros |
| Berry formula from primes | 0.155 ± 7.6% | Matches — primes PREDICT the rigidity |
| GUE-class matrices (N=500) | 0.24 ± 0.02 | Generic finite-size GUE behavior |
| **Gap** | **~40%** | No construction bridges this |

**Why the gap matters:** Berry's formula PREDICTS the correct Δ₃ from prime sums, yet no matrix construction reproduces it. The information that creates super-rigidity is encoded in the FULL periodic orbit structure (diagonal + off-diagonal), not just the diagonal ramp. The diagonal approximation gives generic GUE (Δ₃≈0.24). The off-diagonal corrections — encoding prime pair correlations (Hardy-Littlewood type) — are what suppress Δ₃ to 0.155.

### Two Novel Claims Carried Forward from S-002

**Claim A: N²/p Gauss sum scaling** — β peaks at N²/p≈275 for N=500. SUPPORTED. Needs multi-N verification.

**Claim B: Dirichlet character impossibility** — Both multiplicative and factorizable character constructions algebraically collapse to GOE. SUPPORTED. Proof complete; no additional verification needed.

### What NOT to Repeat

- Random-phase explorations (GUE class is easy; the problem is super-rigidity)
- Gradient optimization (non-differentiable loss function)
- Dirichlet character constructions (proved impossible)
- Gauss sum variations (β-capped at 1.2)
- Testing pair correlation as a discrimination metric (insufficiently discriminating at N=500)

## Methodology: Focused Attack → Diversify → Close Out

This is a focused, final strategy. Every exploration targets a specific quantitative question. No surveys, no literature reviews, no open-ended construction attempts. Each exploration either computes a specific number or it has failed.

### Phase 1: The Off-Diagonal Correction (2 explorations, CAN RUN IN PARALLEL)

**Exploration A: Off-Diagonal Form Factor and Predicted Δ₃**

This is the single most important computation of the entire mission. Berry (1985) and Bogomolny-Keating (1996) showed that the spectral form factor K(τ) for the Riemann zeros is:

K(τ) = K_diagonal(τ) + K_off-diagonal(τ)

where:
- K_diagonal(τ) = τ for τ < 1 (the GUE ramp, already confirmed in S-002)
- K_off-diagonal(τ) encodes prime pair correlations ("off-diagonal orbit pairs")

The full form factor K(τ) determines Δ₃ via the Dyson-Mehta integral:

Δ₃(L) = (2/L⁴) ∫₀ᴸ (L³ - 2L²r + r³)(1 - K̃(r/L)) dr

(where K̃ is the Fourier-related kernel; the exact formula connects K to the cluster function Y₂, from which Δ₃ follows).

**The computation:**
1. Extract the off-diagonal periodic orbit formula from Berry (1985) or Bogomolny-Keating (1996). The key expression involves sums over pairs of prime powers with correlated actions.
2. Compute K(τ) = K_diag + K_off-diag numerically for τ ∈ [0, 5] at the height T corresponding to the 1000th zero (~1682).
3. From K(τ), compute the predicted Δ₃(L) via the Dyson-Mehta relation.
4. Compare the predicted Δ₃_sat to the measured 0.155.
5. **Target result:** If predicted Δ₃_sat = 0.155 ± 10%, the off-diagonal corrections EXPLAIN the super-rigidity gap. If not, something beyond semiclassical theory is needed.

**References to extract formulas from:**
- Berry, M.V. (1985). "Semiclassical theory of spectral rigidity." Proc. R. Soc. Lond. A 400, 229-251.
- Bogomolny, E.B. & Keating, J.P. (1996). "Gutzwiller's trace formula and spectral statistics: beyond the diagonal approximation." Phys. Rev. Lett. 77, 1472-1475.
- Berry, M.V. & Keating, J.P. (1999). "The Riemann zeros and eigenvalue asymptotics." SIAM Rev. 41, 236-266.

**CRITICAL:** The explorer MUST extract the actual mathematical formula from one of these papers and implement it, not derive it from scratch or reason about what it "should" be. The formula exists in the literature. Find it, code it, compute it.

**Exploration B: Li's Criterion — Computational Probing**

RH is equivalent to: λ_n ≥ 0 for all n ≥ 1, where

λ_n = Σ_ρ [1 - (1 - 1/ρ)^n]

summed over non-trivial zeros ρ. Li (1997) proved this equivalence.

**The computation:**
1. Compute λ_n for n = 1, 2, ..., 500 using high-precision arithmetic (mpmath, 50+ digits)
2. Verify λ_n > 0 for all computed n (sanity check — if any λ_n < 0, RH is false!)
3. Plot λ_n vs n. Known asymptotic: λ_n ~ (n/2)log(n/2πe) + (n/2)(γ-1) + O(log n)
4. Compute the RESIDUAL: δ_n = λ_n - [(n/2)log(n/2πe) + (n/2)(γ-1)]
5. Does δ_n show structure? Oscillations? Correlations with prime gaps? Monotonicity?
6. Compute the growth rate d(λ_n)/dn and compare to the theoretical n/2·log(n)

**Key question:** Is there a pattern in the Li coefficients beyond the known leading asymptotics that connects to the spectral constraint catalog?

**Note:** Li coefficients can be computed from the completed zeta function ξ(s) using Maclaurin coefficients. Use the formula via the logarithmic derivative of ξ. mpmath has the tools for this.

### Phase 2: Deepen + Verify (2-3 explorations)

Based on Phase 1 results:

**If Exploration A succeeds (predicted Δ₃ matches 0.155):**
- **Exploration C:** Extract the EXPLICIT constraint on the Riemann operator from the off-diagonal correction. What operator property generates the K_off-diagonal term? The answer encodes the operator's eigenvector statistics or matrix element distribution. This is the Tier 4 result — advancing the operator proof strategy.
- **Exploration D:** Construct a matrix model that INCLUDES off-diagonal corrections. Start from a GUE matrix (which has the correct diagonal) and perturbatively add structure that reproduces K_off-diagonal. Test whether the perturbed matrix's Δ₃ reaches 0.155.

**If Exploration A fails (predicted Δ₃ doesn't match):**
- **Exploration C:** Investigate WHY. Is the failure in the off-diagonal formula itself (higher-order corrections needed)? Or in the K → Δ₃ integral? Or in the asymptotic regime (T too low)? This would be the first quantitative demonstration that semiclassical theory is insufficient, which is also novel.
- **Exploration D:** Try an alternative: Conrey-Farmer-Keating-Rubinstein-Snaith (CFKRS) moment conjectures. These give higher-order corrections to zeta function moments that are independent of the periodic orbit approach.

**Regardless of Exploration A result:**
- **Exploration E (LOW COST): N²/p scaling verification.** Compute the Gauss sum scaling peak for N=250 and N=1000 (in addition to N=500 from S-002). If the constant 275 is N-independent, Claim A is strengthened. If it changes, revise or retract. This is a single exploration with 2 matrix-size runs — takes ~30 minutes of computation.

### Phase 3: Mandatory Adversarial + Final Synthesis (2 explorations, NON-NEGOTIABLE)

**Exploration F (MANDATORY): Adversarial Review**
Take the strongest claim from Phases 1-2 and attack it:
- If the off-diagonal Δ₃ prediction matches: is the match trivially guaranteed by how Berry's formula was derived? (Berry's formula IS derived from zeta zeros, so if we use it to predict Δ₃ of zeta zeros, is that circular?)
- Search for the specific published paper that already contains this computation
- Test the computation at a different height (T = 5000 instead of 1682)
- Check whether the off-diagonal formula is used with conjectural inputs (Hardy-Littlewood) and assess sensitivity to those conjectures

**Exploration G (MANDATORY): Final Mission Synthesis**
Survey ALL findings from all three strategies (15+ explorations). Write the consolidated novel claims section:
- Claim A (N²/p scaling) — updated with N-scaling verification
- Claim B (Dirichlet impossibility) — carried forward from S-002
- Any new claim from this strategy (off-diagonal gap explanation, Li coefficient patterns, operator constraint)
- For each claim: statement, evidence, novelty search, strongest counterargument, status

## Validation Criteria

### This strategy succeeds if:
- The off-diagonal form factor correction is computed numerically (Exploration A produces a number, not a qualitative argument)
- The predicted Δ₃ from the full form factor (diagonal + off-diagonal) is compared to 0.155 with a quantitative error
- At least one finding from this strategy would cause an expert to say "I hadn't seen that specific result before"
- The final synthesis produces a coherent narrative across all three strategies

### This strategy is exhausted if:
- The off-diagonal formula cannot be extracted from the literature (the papers are too abstract)
- The computation diverges or is numerically intractable
- After 4 explorations, no new quantitative result has been produced
- The off-diagonal prediction matches 0.155 trivially (by construction/circularity)

### What would count as Tier 4 (advancing a proof strategy):
- Proving that the super-rigidity gap is EXACTLY explained by off-diagonal orbit corrections (quantitative match)
- Deriving an explicit new constraint on the Riemann operator from the off-diagonal structure
- Constructing a matrix whose Δ₃ reaches 0.155 (bridging the gap)
- A formal identification of WHERE semiclassical theory breaks down (if it does)
- A new pattern in Li coefficients that connects to spectral constraints

## Computation Platform Notes

- **mpmath** for high-precision zeta zeros and Li coefficients (50+ digits). The zetazero() function works for the first ~2000 zeros.
- **numpy/scipy** for matrix computations and numerical integration.
- **Avoid scipy.optimize** — documented failures in S-002.
- **Write each computation result to REPORT.md immediately after computing it** — do NOT defer report writing. Mark each section [SECTION COMPLETE] as you go.
- **Include GUE/GOE controls in every comparison** — learned from S-002 adversarial review.
- **If a formula from a paper is ambiguous, implement BOTH interpretations and report both results** — the Berry normalization convention issue (1/π² vs 1/2π²) cost significant debugging time in S-002.

## Budget

8 explorations total (7 planned + 1 buffer):
- Phase 1: 2 (parallel)
- Phase 2: 3 (sequential, direction depends on Phase 1)
- Phase 3: 2 (mandatory)
- Buffer: 1

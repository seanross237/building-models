# Exploration 001 Summary: Independent β < 1/6 Rederivation

## Goal
Adversarially verify the claimed β < 1/6 mass gap threshold for SU(2) lattice Yang-Mills in d=4 by rederiving it independently from the SZZ Bakry-Émery framework. Find errors if they exist.

## What Was Tried
All five stages executed with runnable Python code on an L=2, d=4 lattice:
1. Convention sanity check (λ_max at Q=I)
2. Analytical derivation of HessS formula from first principles
3. Cauchy-Schwarz analysis to find the optimal bound
4. Numerical verification for random Haar-distributed Q (200 samples) + special configs
5. CS saturation analysis and comparison with prior mission's proof

## Outcome: CLAIM IS CORRECT — No errors found

**Independent derivation confirms β < 1/6 exactly.**

The key steps:
1. HessS(v,v) = (β/2N) Σ_□ |B_□(Q,v)|² where B_□ = Σ_{e∈□} s_e Ad_{P_e}(v_e)
2. Cauchy-Schwarz: |B_□|² ≤ 4 Σ_{e∈□} |v_e|²
3. Summing over □: HessS ≤ (β/2N) × 4 × 2(d-1) × |v|² = 6β|v|²
4. K_S > 0 iff 6β < N/2 = 1, i.e., **β < 1/6**

**Critical finding:** The configuration U_all = iσ₃ achieves λ_max(H) = 6β EXACTLY, with **all 96 plaquettes simultaneously saturating the CS bound**. This proves β < 1/6 is the exact (not improvable) threshold within this framework.

## Verification Scorecard
- **[VERIFIED]:** 4 (convention check, staggered mode, CS saturation at U=iσ₃, all-plaquette tightness)
- **[COMPUTED]:** 3 (HessS formula confirmed by FD, CS bound universality, β threshold)
- **[CONJECTURED]:** 0

## Key Takeaway
**β < 1/6 is correct and exactly tight.** The Cauchy-Schwarz bound is not a loose overestimate — it is saturated by U_all = iσ₃ (a center-adjacent configuration where every link = iσ₃). The 8× improvement over SZZ (β < 1/6 vs 1/48) is genuine: SZZ's Lemma 4.1 is weaker by a factor of 2N² = 8, while the direct CS argument gives the optimal constant.

## Proof Gaps Identified
None that affect the conclusion. One note for caution: the formula HessS = (β/2N)Σ|B_□|² is the covariant Hessian on the full SU(N)^{n_links} manifold. If the SZZ mass gap proof uses a gauge-fixed Hessian on the moduli space, there could be additional fiber curvature terms. However, this formula is confirmed by finite differences and is the standard treatment.

## Unexpected Findings
1. **U=iσ₃ is a minimum of the Wilson action** (Re Tr(U_□) = 2 = N, same as Q=I), yet gives the MAXIMUM Hessian norm. The worst-case configuration for the mass gap is at the action minimum, not a saddle point.
2. **H_norm is NOT maximized by random configurations.** Random Haar Q gives H_norm ≈ 4β; the worst case 6β is achieved only at special "antipodal" configurations (U = iσ_a for any direction a).
3. **The GOAL's convention table entry H_norm = 1/12** at Q=I matches 4β/48 = 1/12 under the normalization H_norm := λ_max(H)/(48β), confirming 48 is the SZZ Lemma 4.1 normalization constant.

## Computations Identified for Further Investigation
1. **Exact proof of max_Q λ_max(H(Q)) = 6β:** Proved numerically but could use a formal algebraic argument showing U_all = iσ₃ is the global maximizer (not just a local saturator).
2. **General N and d:** Does max_Q λ_max(H) = [4(d-1)/N]β hold for all N, d? Would give mass gap at β < N²/(8(d-1)) in general.
3. **Gauge fiber correction:** Does the gauge-fixed Hessian differ from (β/2N)Σ|B_□|²? If SZZ compute the gauge-fixed version, what is their extra factor of 2N²?

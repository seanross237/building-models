# Exploration 001: Orientation and Landscape Verification — Summary

## What Was the Goal
Verify the mission premises: confirm beta = 4/3 is current best pressure exponent in De Giorgi NS, verify the 3/2 threshold, search for prior H^1 + De Giorgi work, and clarify the "Tran-Yu 2014 AIHPC" reference.

## What Was Tried
Parallel literature searches across four research agents: (1) Vasseur publication history and pressure exponent state of the art; (2) H^1/Hardy space + De Giorgi NS prior work; (3) Tran-Yu identification and 3/2 threshold derivation; (4) Direct fetch and read of Vasseur 2007 preprint for the precise beta = 4/3 origin; (5) Direct fetch and read of Choi-Vasseur 2014 (arXiv:1105.1526) for the pressure decomposition details.

## Outcome: Succeeded — all four premises resolved

**Confirmed:** beta = 4/3 is the current best recursion exponent. Source: Vasseur 2007, page 24, explicit statement — "the exponent 4/3 < 3/2 comes from the pressure term which is not in divergence form." The specific obstruction is the term P_{k21} div(uv_k/|u|) in equation (19) of Vasseur 2007, which cannot be written as a divergence. No paper from 2007–2026 has improved this.

**Confirmed:** beta > 3/2 is needed for full regularity. Source: Vasseur 2007 Appendix A, Conjecture 14 — explicitly states that if the De Giorgi recursion held with exponent β > 3/2 (instead of 4/3), then all suitable weak solutions of 3D NS would be locally bounded and hence regular. 3/2 is the scale of the NS equation.

**Corrected:** "Tran-Yu 2014 AIHPC" does not exist. The actual paper is **Choi-Vasseur 2014** (Kyudong Choi and Alexis Vasseur), Ann. IHP, Vol 31 No 5, pp. 899–945, arXiv:1105.1526. No paper by "Tran and Yu" appears in AIHPC 2014. Tran-Yu papers exist (Nonlinearity, J. Math. Phys., Appl. Math. Lett.) but in different journals, different years, different topic (Prodi-Serrin criteria, not De Giorgi).

**Corrected (partially):** H^1 + De Giorgi is NOT an unexplored route. The Vasseur school has been combining H^1/Hardy space with De Giorgi since 2007. Choi-Vasseur 2014 contains the most advanced treatment: a three-way pressure decomposition (P = P_{1,k} + P_{2,k} + P_3) designed specifically to exploit H^1 structure despite the non-bounded maximal operator. However, the **specific Step 2B angle — H^1-BMO duality with De Giorgi test functions ψ_k as BMO elements** — does not appear in any Vasseur paper and remains genuinely untried.

## Key Takeaway
The mission premises are mostly correct but need one significant update: the H^1 route has been tried by the Vasseur school, and the documented ceiling is 4/3 via the Choi-Vasseur 2014 decomposition. The genuine novel angle is whether the De Giorgi test functions ψ_k are uniformly BMO-bounded, which would allow replacing the Hölder inequality with an H^1-BMO duality estimate. This specific question is open.

## Kill Condition Assessment
- **(A) Someone pushed past beta = 4/3:** NOT triggered. No improvement in 2007–2026.
- **(B) H^1 + De Giorgi tried and failure documented:** PARTIALLY triggered. General H^1 approach is extensively developed; documented ceiling at 4/3 (Choi-Vasseur 2014). But the specific H^1-BMO duality angle (Step 2B) has not been tried.
- **(C) beta = 4/3 proven sharp for all decompositions:** NOT triggered.

**Recommendation:** Proceed to Step 1 with the Choi-Vasseur 2014 decomposition (not just Vasseur 2007) as the primary reference. The comparison Caffarelli-Vasseur (SQG succeeds) vs. NS (fails at 4/3) should use Choi-Vasseur 2014's terminology. The P_3 algebraic absorption trick is a key structural insight that Step 1 must understand.

## Leads Worth Pursuing
- **Choi-Vasseur 2014 Lemma 3.3** (the three-way pressure decomposition) should be central to Step 1's analysis — it's the state of the art for pressure handling in De Giorgi NS.
- **BMO boundedness of ψ_k:** The De Giorgi test functions in Choi-Vasseur 2014 are level-set truncations of u. Whether these are uniformly BMO-bounded is the precise question Step 2B must answer. Cutoffs of Lipschitz functions are BMO, but ψ_k involves composite operations that could destroy this.
- **Vasseur-Yang 2021's vorticity approach:** By reformulating via ω = curl u, pressure drops out of the local analysis entirely. This is an alternative route to regularity that bypasses the pressure problem rather than solving it. May be worth comparison.

## Unexpected Findings
1. **Vasseur's own 2007 paper contains the 3/2 conjecture explicitly.** The mission conjecture (that 3/2 is the target) is not an inference from scaling — it's Conjecture 14 in the original paper's appendix. Vasseur knew the gap precisely from day one.
2. **The H^1 route has already been developed for 17 years by the Vasseur school**, with the most advanced version (Choi-Vasseur 2014) achieving 4/3 via a sophisticated three-way decomposition. The school then moved to vorticity (2021), suggesting H^1 pressure approach may have been abandoned as exhausted.
3. **The "Tran-Yu" reference is a clean misidentification** of Choi-Vasseur. The mission chain should be corrected at every occurrence.

## Computations Identified
None in this exploration — this was pure literature. The following computations are identified for Step 1:
- **Explicit verification of Bogovskii corrector scaling:** Compute the growth rate of ‖P_{1,k}‖_{L^∞} ~ 2^{12k} vs. De Giorgi energy decay rate U_{k-1}^{7/6}. Check whether the geometric decay wins. (50-line computation using explicit bounds from Choi-Vasseur 2014 Lemma 3.3.)
- **BMO norm estimate for ψ_k:** For the Choi-Vasseur 2014 test functions, compute ‖ψ_k‖_{BMO} or bound it in terms of k. This is the core gate for Step 2B. (Analysis computation — probably not numerical, but requires tracing through the definition of ψ_k in the paper.)

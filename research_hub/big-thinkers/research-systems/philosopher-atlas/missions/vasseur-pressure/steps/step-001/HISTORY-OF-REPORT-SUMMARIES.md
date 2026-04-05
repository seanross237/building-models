# History of Report Summaries — Step 0+1

## Exploration 002: Pressure Term Dissection (Math Explorer)

**Outcome:** SUCCEEDED — all 4 tasks completed (14 [COMPUTED], 5 [CHECKED], 1 [CONJECTURED]).

**Key finding:** The beta = 4/3 bottleneck is DISTRIBUTED across two interacting constraints:
1. **CZ ceiling:** u in L^{3,infinity} gives p in L^{3/2,infinity} (weak type only). Strong-type requires beta < 3/2.
2. **De Giorgi recursion structure:** Local pressure gives U_k^{8/5} (superlinear, closes). Far-field pressure has a FIXED CONSTANT coefficient — sublinear U_k exponent, only controlled in epsilon-regularity.

**Critical insights for Step 2:**
- Local pressure is NOT the problem (delta_local = 3/5 > 0)
- Far-field pressure IS the sole obstruction — any technique bounding ||p_far||_{L^infty(Q_k)} in terms of U_k would close the recursion
- Bogovskii corrector FAILS — 2^{2k} compound growth from cutoff gradient (2^k) x operator constant on thin annuli (2^k). Strictly worse than original pressure.
- The measure exponent 1/10 in local pressure is beta-independent (structural)
- The gap is 1/6 in reciprocal: 1/(4/3) - 1/(3/2) = 1/12

**Leads for H^1 route:**
1. Focus on far-field pressure control (not local)
2. Avoid pressure localization via cutoffs (Bogovskii kills the recursion)
3. The 1/10 universality suggests deeper structure worth exploiting
4. Even logarithmic improvement to a priori velocity bound could cross 3/2

**Unexpected:** Bogovskii corrector is strictly worse than the original problem (2^{2k} vs 2^k growth). This is a strong negative result against localization strategies.

---

## Exploration 001: Orientation and Landscape Verification (Standard Explorer)

**Outcome:** SUCCEEDED — all four premises resolved (2 confirmed, 2 corrected).

**Confirmed:**
- beta = 4/3 is current best, unchanged since 2007. Source: Vasseur 2007 page 24, explicit statement.
- beta > 3/2 needed for full regularity. Source: Vasseur 2007 Conjecture 14 (Appendix A).

**Corrected:**
- "Tran-Yu 2014 AIHPC" does NOT exist. The actual paper is Choi-Vasseur 2014 (arXiv:1105.1526).
- H^1 + De Giorgi is NOT unexplored in general — Vasseur school has used it since 2007. Choi-Vasseur 2014 is the most advanced version (three-way pressure decomposition P = P_{1,k} + P_{2,k} + P_3). BUT: the specific H^1-BMO duality angle (Step 2B) has NOT been tried.

**Kill conditions:**
- (A) NOT triggered — no one pushed past 4/3
- (B) PARTIALLY triggered — general H^1 approach is documented; specific H^1-BMO duality untried
- (C) NOT triggered — no sharpness result

**Key context for Step 2:**
- Choi-Vasseur 2014 Lemma 3.3 is the state of the art — must be baseline
- P_3 absorbed via algebraic identity (eq. 47) — already solved
- P_{k21} is the specific obstruction term (non-divergence-form)
- Vasseur school moved to vorticity (2021), implicitly declaring H^1 pressure ceiling reached
- The novel angle: are De Giorgi test functions psi_k uniformly BMO-bounded?

**Unexpected:** Vasseur 2007's appendix contains Conjecture 14 = our exact mission statement. The gap has been known precisely for 19 years.

# Step 0+1 Results: Orientation and Pressure Term Dissection

## Step Goal Achievement: COMPLETE

Both sub-goals (Step 0: orientation, Step 1: pressure dissection) are satisfied. Two explorations ran in parallel and both succeeded.

---

## Key Findings

### 1. Landscape Verification (Exploration 001)

**beta = 4/3 is confirmed as the current best**, unchanged since Vasseur 2007. No paper in 2007-2026 has improved the pressure exponent in the De Giorgi NS framework.

**beta > 3/2 is confirmed as the threshold** for full regularity. This is Vasseur's own Conjecture 14 (Appendix A of the 2007 paper): "3/2 corresponds to the scale of the equation."

**Critical correction:** "Tran-Yu 2014 AIHPC" does not exist. The paper is **Choi-Vasseur 2014** (Kyudong Choi and Alexis Vasseur, Ann. IHP Vol 31 No 5, pp. 899-945, arXiv:1105.1526). All downstream references must be updated.

**Critical correction:** H^1 + De Giorgi is NOT unexplored in general. The Vasseur school has used H^1 structure of pressure since 2007, with Choi-Vasseur 2014 as the most advanced version (three-way pressure decomposition P = P_{1,k} + P_{2,k} + P_3). **However:** the specific H^1-BMO duality angle (testing whether De Giorgi functions psi_k are uniformly BMO-bounded) has NOT been tried. This is the genuine novel angle.

**The Vasseur school moved to vorticity in 2021** (Vasseur-Yang, ARMA), implicitly suggesting the H^1 pressure route has hit its ceiling without a new idea.

### 2. Pressure Term Dissection (Exploration 002)

**The beta = 4/3 bottleneck is DISTRIBUTED** across two interacting constraints:

| Constraint | Source | Effect |
|---|---|---|
| CZ ceiling | u in L^{3,infinity} → p in L^{3/2,infinity} (weak type only) | Strong-type L^beta requires beta < 3/2 |
| Far-field pressure | ||p_far||_{L^infinity(Q_k)} is a FIXED CONSTANT | Sublinear U_k exponent; only controlled in epsilon-regularity |

**Local pressure is NOT the problem.** The local part gives U_k^{8/5} in the recursion (delta_local = 3/5 > 0, superlinear). It closes.

**Far-field pressure IS the sole obstruction.** Its coefficient is proportional to ||u||_{L^2}^2 / r_k^3 — a fixed constant not controlled by U_k. Only in the epsilon-regularity setting (smallness assumption) is this manageable.

**Bogovskii corrector FAILS.** The corrector introduces 2^{2k} compound growth (cutoff gradient 2^k x operator constant on thin annuli 2^k), which is strictly worse than the original pressure perturbation (2^k). Best corrector U_k exponent: 9/10 < 1 (sublinear). This eliminates Bogovskii-type localization from the H^1 strategy.

**The measure exponent 1/10 is beta-independent.** This structural universality in the local pressure estimate suggests deeper cancellation that might extend to the far-field.

### 3. Drift-Diffusion Comparison

| Term | Drift-Diffusion (CV 2010) | Navier-Stokes (V 2007) |
|---|---|---|
| Transport IBP | Clean (scalar, div-free) | Leaves pressure residual (vector) |
| Pressure | ABSENT | Far-field: fixed constant coefficient |
| Recursion | CLOSES (delta = 2/5) | PARTIAL (epsilon-regularity only) |
| Result | Full regularity | Partial regularity |

The gap is entirely due to the pressure term. Without pressure, the identical De Giorgi machinery reaches criticality.

---

## Kill Condition Assessment

| Kill Condition | Status | Evidence |
|---|---|---|
| (A) Someone pushed past 4/3 | NOT triggered | No improvement 2007-2026 |
| (B) H^1 + De Giorgi tried, failure documented | PARTIALLY triggered | General H^1 approach extensively developed; H^1-BMO duality untried |
| (C) beta = 4/3 proven sharp | NOT triggered | No sharpness result exists |

**Verdict:** No full kill. Mission proceeds with refined scope: the novel angle is H^1-BMO duality (not general H^1 structure).

---

## What Step 2 Needs

The following deliverables are ready for Step 2:

1. **The specific inequality to target:** The far-field pressure pairing integral p_far * v_k * nabla(phi_k), estimated via Holder as ||p_far||_{L^beta} * ||v_k nabla phi_k||_{L^{beta'}}. Replace Holder with H^1-BMO duality.

2. **Bogovskii is eliminated:** Do NOT pursue Bogovskii-type localization. The compound 2^{2k} growth kills the recursion.

3. **The comparison baseline:** In drift-diffusion, transport IBP is clean (scalar). In NS, it leaves a pressure residual. The H^1-BMO route must handle this residual without localization.

4. **The precise question for Branch 2B:** Are the Choi-Vasseur 2014 De Giorgi test functions psi_k uniformly bounded in BMO? If yes, then |integral p * psi_k| <= ||p||_{H^1} * ||psi_k||_{BMO}, and the H^1 norm of pressure (from CLMS compensated compactness) replaces the L^{4/3} norm. Trace through the recursion to determine the effective beta.

5. **The reference to use:** Choi-Vasseur 2014 (arXiv:1105.1526), not just Vasseur 2007. The three-way decomposition in Lemma 3.3 is the state of the art.

---

## Unexpected Discoveries

1. **Vasseur knew the gap for 19 years.** Conjecture 14 in his 2007 paper is precisely our mission statement.
2. **Bogovskii is strictly worse than the original problem** — a strong negative result that eliminates an entire class of localization strategies.
3. **The Vasseur school's strategic shift to vorticity (2021)** is circumstantial evidence that H^1 pressure is exhausted without a new idea. H^1-BMO duality may be that new idea.
4. **The 1/10 universality** in the measure exponent suggests unexploited structural cancellation.

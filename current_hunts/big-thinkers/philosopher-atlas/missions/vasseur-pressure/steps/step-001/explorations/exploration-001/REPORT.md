# Exploration 001: Orientation and Landscape Verification

## Goal
Verify premises of the Vasseur pressure exponent mission. Specifically:
1. Confirm beta = 4/3 is still the best known pressure exponent in De Giorgi NS regularity
2. Search for prior work combining H^1/Hardy space pressure estimates with De Giorgi iteration
3. Clarify "Tran-Yu 2014 AIHPC" reference
4. Verify the 3/2 threshold claim

---

## 1. State of the Art Summary

The Vasseur 2007 De Giorgi approach to Navier-Stokes partial regularity is confirmed to produce the exponent β = 4/3 in the De Giorgi recursion U_{k+1} ≤ C^k U_k^{4/3} for the local pressure term, and Vasseur himself explicitly states in an appendix (Conjecture 14) that β > 3/2 would imply full regularity of all suitable weak solutions. The gap 4/3 → 3/2 is the precise obstruction to full regularity, and it has not been closed as of 2024–2026. However, **the H^1/Hardy space structure of the pressure is NOT unexplored territory** — the Vasseur school has been using it since 2007 and the key limitation (H^1 lacks a bounded maximal operator) is a documented obstruction. The most recent development (Vasseur-Yang 2021) sidesteps pressure entirely by working on the vorticity equation, which reformulates the problem but does not directly close the 4/3 → 3/2 gap. The "Tran-Yu 2014 AIHPC" reference in the mission chain is a misidentification: the actual paper is Choi-Vasseur 2014 (same journal, same volume).

---

## 2. Paper-by-Paper Findings

### Vasseur (2007) — "A new proof of partial regularity of solutions to Navier-Stokes equations"
- **Venue:** NoDEA Nonlinear Differential Equations Appl. 14(5-6), 753–785
- **arXiv:** possibly math/0603588; preprint at https://web.ma.utexas.edu/users/vasseur/documents/preprints/NS2.pdf
- **Key result:** First application of De Giorgi iteration to Navier-Stokes partial regularity, recovering the Caffarelli-Kohn-Nirenberg theorem by a new route.
- **Pressure exponent — precise finding:**
  - Works with P ∈ L^p_loc(L^1_loc) for 1 < p < 4/3 (Proposition 5/Theorem 2)
  - The exponent **4/3 is a HARD THRESHOLD** in the iteration: Proposition 5 is stated for 1 < p < 4/3 because the Riesz/Hölder chain used for P_{k21} requires 4/(2−p) ≤ 6, which holds for p < 4/3.
  - **The specific obstruction** (page 24, near eq. (19)–(20)): The local pressure decomposition gives a term **P_{k21} div(uv_k/|u|)** which is NOT in divergence form. All other pressure terms can be written as divergences and absorbed. This specific term yields a bound of C·U_{k-1}^{4/3} via: ‖1_{|u|≥1−2^{-k}}‖_{L^2} · ‖G_{222}‖_{L^2} ≤ C·U_{k-1}^{5/6} · U_{k-1}^{1/2} = C·U_{k-1}^{4/3}.
  - **Vasseur's own words** (page 24): "Again the exponent 4/3 < 3/2 comes from the pressure term which is not in divergence form in (16)."
- **The 3/2 gap — Conjecture 14 (Appendix A):** Vasseur conjectures that if the recursion could be established with exponent β > 3/2 (instead of the achieved 4/3), then ALL suitable weak solutions of 3D NS would be locally bounded, hence fully regular. He states: "Notice that 3/2 corresponds to the scale of the equation."
- **Relevance to mission:** This is the founding paper. Premises are confirmed exactly as stated. The precise obstruction term is identified.

---

### Caffarelli-Vasseur (2010) — "The De Giorgi method for regularity of solutions of elliptic equations and its applications to fluid dynamics"
- **Venue:** Discrete Contin. Dyn. Syst. Ser. S, 3(3), 409–427
- **Key result:** Survey paper applying De Giorgi to SQG (global regularity proved) and NS. SQG has no pressure term; the De Giorgi iteration reaches criticality (analogous to β → 1 in the recursion, sufficient for L^∞). This is the "control case" for the mission: without pressure, the iteration closes at the optimal exponent.
- **H^1 role:** Explains how CLMS compensated compactness gives ∇²p ∈ H^1(ℝ³) for NS, but this is where the difficulty begins: H^1 lacks a bounded maximal operator.
- **Relevance:** Key comparison point for Step 1 of the chain: SQG succeeds (no pressure), NS fails (pressure term hits 4/3 barrier). The exact term-by-term comparison is available from Vasseur 2007 above.

---

### Vasseur (2010) — "Higher derivatives estimate for the 3D Navier-Stokes equation"
- **Venue:** Ann. Inst. H. Poincaré Anal. Non Linéaire 27(5), 1189–1204. arXiv: 0904.2422
- **Key result:** Estimates on higher derivatives of NS solutions up to potential blow-up time using De Giorgi with Hardy spaces and maximal functions.
- **H^1/Hardy role:** Second derivatives of pressure lie in Hardy H^1 ⊂ L^1 (CLMS). Explicitly acknowledges that the maximal function is not L^1-bounded, forcing a new pressure splitting strategy.
- **Relevance:** First explicit documentation of the H^1 maximal operator obstruction in the De Giorgi NS context.

---

### Choi-Vasseur (2014) — "Estimates on fractional higher derivatives of weak solutions for the Navier-Stokes equations"
- **Venue:** Ann. Inst. H. Poincaré Anal. Non Linéaire 31(5), 899–945. arXiv: 1105.1526
- **KEY NOTE: This is almost certainly the paper referred to as "Tran-Yu 2014 AIHPC" in the mission chain. The journal, volume, year, and topic all match. No paper by "Tran and Yu" exists in AIHPC 2014.**
- **Key result:** Proves ∇^α u is locally integrable in weak-L^{4/(α+1),∞} for any real α ∈ (1, 3), for Leray-Hopf weak solutions with L² data.
- **Pressure decomposition (Lemma 3.3) — the most sophisticated H^1-pressure + De Giorgi work to date:**
  - Decomposes P = P_{1,k} + P_{2,k} + P_3
  - P_3 (k-independent non-local part): absorbed into level-set functional E_k via algebraic identity (47): div(uP_3) + (v_k/|u| − 1)u·∇P_3 = (v_k/|u|)u·∇P_3 ≥ 0. This removes P_3 from the De Giorgi inequality entirely.
  - P_{1,k} (k-dependent non-local): grows as 2^{12k} but only in L^∞ on shrinking regions
  - P_{2,k} (k-dependent local): supported on shrinking domains, controlled via Riesz transforms
  - **The second derivatives of pressure lie in H^1 via CLMS**, explicitly stated on page 5. The new decomposition is designed specifically to work with H^1 pressure structure despite the non-bounded maximal operator.
- **Exponent achieved:** U_k ≤ C^k · U_{k-1}^{7/6}, which can be made close to 4/3 (Remarks 3.1, 3.6). The scaling-optimal target is 4/3 = 4/(d+1) for d=2, and 7/6 > 1 suffices for convergence. **This does NOT reach 3/2.** The paper is about higher-derivative estimates, not about closing the 4/3 → 3/2 gap.
- **Relevance to mission:** This paper IS the most advanced H^1 + De Giorgi work for NS pressure. It documents that the H^1 structure is already exploited in the Vasseur pressure decomposition, and it achieves ~4/3 (not 3/2).

---

### Vasseur-Yang (2021) — "Second Derivatives Estimate of Suitable Solutions to the 3D Navier-Stokes Equations"
- **Venue:** Arch. Ration. Mech. Anal. 241(2), 683–727. arXiv: 2009.14291
- **Key result:** Second spatial derivatives of suitable weak solutions are locally in Lorentz space L^{4/3,q} for any q > 4/3, improving the previous L^{4/3,∞} bound of Choi-Vasseur.
- **Pressure strategy:** The local De Giorgi analysis is performed on the **vorticity equation** (ω = curl u), which has no pressure term. This CIRCUMVENTS the pressure problem entirely rather than solving it.
- **Relevance:** Suggests that the Vasseur school has moved away from the H^1 pressure route (toward vorticity), which implicitly suggests the H^1 pressure route has hit a ceiling. However, this does NOT close the 4/3 → 3/2 gap for the full regularity conjecture.

---

### Papers on Tran and Yu (not 2014 AIHPC)
Tran and Yu (different pair of authors from Choi-Vasseur) have several NS papers, but none in AIHPC 2014 and none addressing the De Giorgi pressure exponent:
- **Tran-Yu (2015)** "Depletion of nonlinearity in NS flows" — *Nonlinearity* 28, 1295–1306
- **Tran-Yu (2016)** "Pressure moderation and effective pressure in NS flows" — *Nonlinearity* 29, 2990–3005
- **Tran-Yu (2017)** "Regularity of NS flows with bounds for the pressure" — *Appl. Math. Lett.* 67, 21–27
- **Tran-Yu (2017)** "Note on Prodi-Serrin-Ladyzhenskaya type criteria" — *J. Math. Phys.* 58, 011501
These papers use Prodi-Serrin type criteria (not De Giorgi). Not relevant to the 4/3 question. The "Tran-Yu 2014 AIHPC" reference in the chain must be corrected to Choi-Vasseur 2014.

---

### Other Relevant Post-2014 Papers (Not Using De Giorgi)

**Chamorro-Lemarié-Rieusset-Mayoufi (2018)** — "The Role of the Pressure in the Partial Regularity Theory for Weak Solutions"
- *Arch. Ration. Mech. Anal.* 228:237–277. arXiv: 1602.06137
- Generalizes CKN partial regularity to distributional pressure (most general framework). Not De Giorgi.

**Barker-Wang (2023)** — "Estimates of the singular set for NS with supercritical pressure"
- *J. Differential Equations* 365:379–407. arXiv: 2111.15444
- Supercritical (weaker than L^{5/4}) pressure conditions. Singular set dimension can be made small. Not De Giorgi.

**Kwon (2023)** — "The role of the pressure in the regularity theory for NS"
- *J. Differential Equations* (2023). arXiv: 2104.03160
- Allows distributional pressure. Not De Giorgi.

---

## 3. Kill Condition Assessment

### (A) Someone pushed past beta = 4/3 using ANY method
**NOT TRIGGERED.**

No paper from 2007–2026 improves the recursion exponent beyond 4/3 in the De Giorgi approach to NS full regularity. The Vasseur line of work has:
- Choi-Vasseur 2014: achieved ~4/3 (specifically 7/6) for fractional derivative estimates — same ceiling
- Vasseur-Yang 2021: circumvented pressure via vorticity for second-derivative estimates — but didn't close the 4/3 → 3/2 gap for full regularity

No other school has entered the De Giorgi NS full-regularity question. The 4/3 exponent stands as the best in the Vasseur 2007 framework for the partial regularity De Giorgi recursion.

**Verdict:** Mission premise (A) confirmed — beta = 4/3 is current best. Proceed.

---

### (B) H^1 + De Giorgi already tried and failure documented
**PARTIALLY TRIGGERED — requires nuanced assessment.**

The H^1/Hardy space structure of the pressure IS already exploited extensively by the Vasseur school:
- Vasseur 2007: first use
- Vasseur 2010: H^1 maximal operator non-boundedness documented as explicit limitation
- Choi-Vasseur 2014: most advanced treatment — new pressure decomposition designed specifically to work with H^1 pressure via three-way split

**What has been tried:** Using the H^1 structure of ∇²p (the CLMS fact) to build a pressure decomposition that controls the De Giorgi iteration. The best known result (Choi-Vasseur 2014) achieves the scaling-optimal exponent 4/3 (≈ 7/6) but cannot reach 3/2.

**The documented obstruction:** H^1 does not have a bounded maximal operator. This prevents direct application of standard L^p maximal function estimates in the De Giorgi scheme, requiring the elaborate three-way pressure decomposition.

**What has NOT been tried (the mission's specific angle):** The Step 2B of the chain asks whether **De Giorgi test functions ψ_k are uniformly BMO-bounded**, which would allow using the H^1-BMO duality pairing ∫ fg ≤ ‖f‖_{H^1}·‖g‖_{BMO} instead of the standard Hölder inequality. This specific route — replacing Hölder with H^1-BMO duality — does **not appear in any Vasseur paper**. The Choi-Vasseur approach uses Hardy spaces and maximal functions but does not use H^1-BMO duality with the De Giorgi test functions as BMO elements.

**Assessment:** Kill condition (B) is partially triggered for the general H^1 approach but NOT triggered for the specific H^1-BMO duality angle that is the mission's core novelty (Step 2B).

---

### (C) beta = 4/3 proven sharp for ALL decompositions
**NOT TRIGGERED.**

No sharpness result or lower bound has been proved showing that no decomposition strategy can exceed 4/3 in the De Giorgi NS recursion. The Vasseur school's movement to vorticity (Vasseur-Yang 2021) bypassed the pressure decomposition question rather than proving it sharp.

---

## 4. Verdict on Mission Premises

| Premise | Status | Notes |
|---|---|---|
| "beta = 4/3 is current best pressure exponent" | **CONFIRMED** | Vasseur 2007 explicitly states this; Choi-Vasseur 2014 confirmed at same ceiling |
| "beta > 3/2 needed for full regularity" | **CONFIRMED** | Vasseur's own Conjecture 14 in Appendix A of 2007 paper |
| "Tran-Yu 2014 AIHPC is relevant" | **CORRECTED** | The paper is Choi-Vasseur 2014 AIHPC Vol 31 No 5 pp. 899–945 |
| "H^1 + De Giorgi route is unexploited" | **CORRECTED** | Extensively developed by Vasseur school, H^1 used since 2007. BUT: H^1-BMO duality with De Giorgi test functions (the specific Step 2B angle) appears NOT to have been tried |
| "3/2 threshold comes from scaling" | **CONFIRMED** | Vasseur: "3/2 corresponds to the scale of the equation"; also confirmed from 3/s + 2/r = 2 for scale-invariant pressure norms |

---

## 5. Implications for Next Steps

### Critical corrections before proceeding:

1. **Choi-Vasseur 2014 is the reference to read for Step 1.** It contains the state-of-the-art pressure decomposition (Lemma 3.3) and the explicit ceiling at 4/3. The mission needs to understand what this decomposition does and why it stops at 4/3 before attempting H^1-BMO duality.

2. **The specific obstruction is known:** The non-divergence-form term P_{k21} div(uv_k/|u|) in Vasseur 2007 (and its equivalent in Choi-Vasseur 2014) is the precise term that forces the 4/3 exponent. Any H^1 strategy must overcome THIS term specifically. Step 1 of the chain should focus on this term and why Choi-Vasseur's decomposition can't push it to 3/2.

3. **H^1-BMO duality (Step 2B) remains viable as an untried angle.** The Vasseur school has used H^1 structure of the pressure (second derivatives of p are in H^1 via CLMS) but has NOT tested whether the De Giorgi test functions ψ_k are uniformly BMO-bounded. If they are, the H^1-BMO duality pairing replaces Hölder and potentially achieves the 3/2 threshold. This is the genuine novel angle.

4. **Vorticity route (Vasseur-Yang 2021) is an alternative.** By reformulating via ω = curl u (which has no pressure term), the pressure obstruction is avoided. However, this does NOT directly address the full-regularity conjecture (Conjecture 14 of Vasseur 2007) — it achieves second-derivative estimates, not L^∞ bounds.

5. **The pressure decomposition in Choi-Vasseur 2014 (P = P_{1,k} + P_{2,k} + P_3)** needs to be compared with the simpler Vasseur 2007 decomposition in Step 1 of the chain. The P_3 absorption trick (via the algebraic identity at eq. 47) is a key structural insight that should be understood before attempting H^1-BMO.

### Recommended modifications to mission chain:

- **Step 1 focus:** Compare Vasseur 2007 decomposition vs. Choi-Vasseur 2014 decomposition. Understand why the P_3 algebraic trick doesn't also push the P_{k21} term past 3/2.
- **Step 2B (most promising):** Estimate ‖ψ_k‖_{BMO} for the De Giorgi test functions, using Choi-Vasseur 2014's ψ_k construction (not just Vasseur 2007's). This is the untried angle.
- **Reference update:** Replace "Tran-Yu 2014" everywhere in the chain with "Choi-Vasseur 2014 (Choi-Vasseur, Ann. IHP, Vol 31 No 5, 2014, arXiv:1105.1526)."

---

## 6. Unexpected Finding

**Vasseur-Yang 2021 effectively declares the H^1 pressure route has hit a structural ceiling**, by moving to vorticity in 2021 — the most recent paper from the founding school of this approach. This is circumstantial evidence that the H^1 pressure route (without a new idea like H^1-BMO duality) has been exhausted. However, the vorticity route also doesn't close the full-regularity gap. The mission's H^1-BMO angle may be the key insight that neither route has tried.

---

## Sources

- Vasseur 2007 (NoDEA): https://link.springer.com/article/10.1007/s00030-007-6001-4 ; preprint: https://web.ma.utexas.edu/users/vasseur/documents/preprints/NS2.pdf
- Caffarelli-Vasseur 2010 (DCDS-S): http://www.aimsciences.org/article/doi/10.3934/dcdss.2010.3.409
- Vasseur 2010 (Ann. IHP): https://ems.press/journals/aihpc/articles/4076951 ; arXiv:0904.2422
- Choi-Vasseur 2014 (Ann. IHP): https://www.numdam.org/articles/10.1016/j.anihpc.2013.08.001/ ; arXiv:1105.1526
- Vasseur-Yang 2021 (ARMA): https://link.springer.com/article/10.1007/s00205-021-01661-4 ; arXiv:2009.14291
- Chamorro-Lemarié-Rieusset-Mayoufi 2018 (ARMA): arXiv:1602.06137
- Barker-Wang 2023 (JDE): arXiv:2111.15444

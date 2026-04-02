# Exploration 005: Choi-Vasseur (2014) Alternative Decomposition and Recent Developments

## Goal
Survey post-Vasseur-2007 literature on alternative pressure decompositions in the De Giorgi framework for NS regularity. Focus on Choi-Vasseur (2014, AIHP) and arXiv:2501.18402, plus a broader landscape survey. Determine whether any alternative decomposition improves the recurrence exponent beta beyond 4/3 or changes the bottleneck structure.

---

## 1. Choi-Vasseur (2014) Three-Way Decomposition

**[PAPER]** Choi & Vasseur, "Estimates on fractional higher derivatives of weak solutions for the Navier-Stokes equations," Ann. Inst. Henri Poincare, Anal. Non Lineaire 31(5), 899-945, 2014. (arXiv:1105.1526)

### The Decomposition (Lemma 3.3, Eq. 26)

Given A_ij in L^1(B_0) and P in L^1(B_0) with -Delta P = sum_{ij} d_i d_j A_ij in B_0, the pressure is decomposed for each k >= 1 as:

**P = P_{1,k} + P_{2,k} + P_3  in B_{1/3}** (Eq. 26)

where each piece is defined by a Poisson equation:

**P_{1,k} (non-local, k-dependent):**
```
-Delta P_{1,k} = sum_{ij} d_i d_j ((psi_1 - psi_k) A_ij)
```
This captures contributions from the annular region B_{1/6} \ B_{k-2/3}, i.e., between the outer cutoff scale and the k-th iteration scale. P_{1,k} is defined via the representation formula (Newton potential). The key bound is:
```
||nabla P_{1,k}||_{L^infty(B_{k-1/3})} + ||P_{1,k}||_{L^infty(B_{k-1/3})} <= Lambda_1 * 2^{12k} * sum_{ij} ||A_ij||_{L^1(B_{1/6})}  (Eq. 27)
```

**P_{2,k} (local, k-dependent):**
```
-Delta P_{2,k} = sum_{ij} d_i d_j (psi_k A_ij)  in R^3   (Eq. 28)
```
This is the localized pressure within the k-th ball, defined globally via Riesz transforms (Calderon-Zygmund theory). The key feature is that psi_k A_ij has support in B_{k-5/6}, so CZ theory applies.

**P_3 (non-local, k-INDEPENDENT):**
```
-Delta P_3 = -sum_{ij} d_j[(d_i psi_1)(A_ij)] - sum_{ij} d_i[(d_j psi_1)(A_ij)]
             + sum_{ij} (d_i d_j psi_1)(A_ij) - 2 div((nabla psi_1)P) + P Delta psi_1
```
This collects all terms involving derivatives of the OUTER cutoff psi_1. Since psi_1 and its derivatives have support in B_{1/6} \ B_{1/3}, which is separated from the iteration region B_{2/3}, P_3 is defined via the Newton potential and satisfies:
```
||nabla P_3||_{L^infty(B_{2/3})} <= Lambda_1 (||P||_{L^1(B_{1/6})} + sum_{ij} ||A_ij||_{L^1(B_{1/6})})  (Eq. 29)
```
**Crucially: Lambda_1 is a totally independent constant.** (stated explicitly after Eq. 29)

### Comparison with Vasseur (2007) Four-Way Decomposition

In Vasseur (2007) [reference 42 in CV14], the pressure was decomposed as P_k^1, P_k^{21}, P_k^{22}, P_k^{23}, where:
- P_k^1: non-local piece (similar to P_{1,k})
- P_k^{21}: the BOTTLENECK piece, defined by -Delta P_k^{21} = sum d_i d_j [phi_k * u_j(1-v_k/|u|) * u_i(1-v_k/|u|)]
- P_k^{22}: local divergence-form piece
- P_k^{23}: another local piece

The critical difference: **In Vasseur (2007), the terms P_k^{22} and P_k^{23} are in divergence form and contribute favorable exponents > 3/2. P_k^{21} is the non-divergence piece that limits beta to < 4/3.**

In Choi-Vasseur (2014), the decomposition is reorganized:
- P_{1,k} absorbs the non-local piece (analogous to P_k^1)
- P_{2,k} absorbs ALL local terms including the CZ-critical piece (analogous to combining P_k^{21}, P_k^{22}, P_k^{23})
- P_3 captures terms from the outer cutoff derivatives — a genuinely NEW piece that **does not depend on k**

**[INTERPRETATION]** The key structural innovation is NOT splitting the local pressure further into divergence/non-divergence parts, but rather separating out a k-independent piece P_3 that can be absorbed into the truncation level.

---

## 2. How P_3 Is "Absorbed" into the Velocity Equation

**[PAPER]** This is the central innovation (stated at line 919 and proven around Eq. 46-47 of the paper).

### The Mechanism

Since nabla P_3 is bounded in L^1_t L^infty_x (by Eq. 29 and Eq. 41), the authors define a **time-dependent truncation level**:

```
E_k(t) = (1 - 2^{-k})_+ * integral_{-1}^{t} ||nabla P_3(s, .)||_{L^infty(B_{2/3})} ds    (Eq. 30)
```

This replaces the constant truncation level (1 - 2^{-k}) used in Vasseur (2007). The truncated velocity is then:

```
v_k = (|u| - E_k)_+
```

Because E_k depends on time (but NOT on space), when computing the time derivative of the energy epsilon_k = v_k^2/2, the P_3 term appears as:

```
d_t(epsilon_k) = ... - v_k * d_t E_k + (v_k/|u| - 1) u . nabla P_3 + ...
               = ... - v_k * ||nabla P_3||_{L^infty} + (v_k/|u|) u . nabla P_3 + ...
```

The key identity (Eq. 47):
```
v_k * ||nabla P_3(t,.)||_{L^infty(B_{2/3})} + (v_k/|u|) * u . nabla P_3 >= 0
```
on (-2,0) x B_{2/3}, because |u . nabla P_3 / |u|| <= ||nabla P_3||_{L^infty} and v_k >= 0.

**This means the P_3 contribution to the energy inequality has a FAVORABLE sign and can be dropped.** The resulting energy inequality (Eq. 46) contains only P_{1,k} and P_{2,k}:

```
d_t(epsilon_k) + div(w * epsilon_k) + d_k^2 - Delta(epsilon_k)
    + div(u(P_{1,k} + P_{2,k})) + (v_k/|u| - 1) u . nabla(P_{1,k} + P_{2,k}) <= 0   (Eq. 46)
```

**Remark 3.5 explicitly states: "Note that the above inequality (46) does not contain the P_3 term."**

**[INTERPRETATION]** The absorption works because P_3 is k-independent with bounded L^1_t L^infty_x norm. By making the truncation level adapt to the accumulated nabla P_3, the pressure gradient and the time-derivative of the truncation level cancel each other out with a favorable sign. This is a genuinely clever trick: you "pay" for the pressure gradient by letting the truncation level rise, and since nabla P_3 is integrable in time, the total rise is bounded.

---

## 3. Resulting Exponent

**[PAPER]** The main De Giorgi iteration result is Lemma 3.4 (Eq. after line 1216):

```
U_k <= (C_1_bar)^k * U_{k-1}^{7/6}     for any k >= 1, if r >= s_1
U_k <= (1/r^3) * (C_1_bar)^k * U_{k-1}^{7/6}     for any k >= 1, if r < s_1
```

**The exponent achieved is beta = 7/6.**

**[PAPER]** Remark 3.1 states explicitly: "It will be clear that the exponent 7/6 is not optimal and we can make it close to (4/3) arbitrarily. However, any exponent bigger than 1 is enough for our study."

**[INTERPRETATION]** This is a critical finding. Choi-Vasseur achieve beta = 7/6, which is LESS than Vasseur's beta < 4/3. They note that they could push it close to 4/3 but don't need to. The paper's purpose is NOT to improve beta — it is to prove that fractional derivatives nabla^alpha u are locally integrable for 1 < alpha < 3. For this purpose, any beta > 1 suffices for the De Giorgi iteration to converge.

**The paper does NOT improve beta beyond 4/3. It actually uses a weaker exponent (7/6) because the goal is different.**

---

## 4. Does This Bypass the P_k^{21} Problem?

**[INTERPRETATION]** Short answer: **No, it does not bypass the fundamental bottleneck.**

Here is the detailed analysis:

### What the Decomposition Changes

In Vasseur (2007), the local pressure was split into:
- P_k^{21} (non-divergence, bounded by CZ independently of U_{k-1} -> exponent 0 -> bottleneck)
- P_k^{22}, P_k^{23} (divergence form, favorable exponents)

In Choi-Vasseur (2014), the local pressure P_{2,k} is NOT further decomposed. It is defined by:
```
-Delta P_{2,k} = sum_{ij} d_i d_j (psi_k * w_i * u_j)
```
where w is the advection velocity. When this appears in the energy inequality (Eq. 46), it will face the SAME bottleneck: the portion involving u(1 - v_k/|u|) factors (which are bounded by 1) will produce a CZ bound independent of U_{k-1}, limiting beta.

### What P_3 Absorption Actually Achieves

The P_3 absorption removes the terms involving derivatives of the outer cutoff psi_1 from the iteration. In Vasseur (2007), this type of term was part of the non-local pressure P_k^1, which was ALREADY controlled (it gives favorable exponents because of the spatial separation between the support of derivatives of psi_1 and the iteration region B_k).

**[INTERPRETATION]** The P_3 absorption is a technical convenience that simplifies the proof structure — it removes certain terms from the energy inequality entirely rather than bounding them. But it does NOT address the P_k^{21} bottleneck, which lives in the LOCAL pressure P_{2,k}. The CZ-limited non-divergence term is still present within P_{2,k}; Choi-Vasseur simply chose not to decompose P_{2,k} further because they don't need beta > 7/6 for their purpose.

### Could the Three-Way Decomposition Be EXTENDED to Improve Beta?

**[INTERPRETATION]** No. The three-way decomposition in CV14 is a simplification, not an improvement, of the pressure treatment. If one further decomposed P_{2,k} into divergence and non-divergence parts (as Vasseur 2007 did), one would recover the same P_k^{21}-type bottleneck. The fundamental issue — that the non-divergence piece of the local pressure is bounded by a k-independent constant via CZ theory — is a structural feature of the Navier-Stokes pressure equation, not an artifact of the decomposition strategy.

---

## 5. arXiv:2501.18402 — Main Result

**[PAPER]** Pedro Gabriel Fernandez-Dalgo, "Dynamic Refinement of Pressure Decomposition in Navier-Stokes Equations," arXiv:2501.18402v2, April 2025. Based at BCAM, Bilbao.

### The Main Result (Theorem 1)

The paper proves that a "relevant critical energy" of a Leray-type solution inside a backward paraboloid — regardless of its aperture parameter a — is controlled near the vertex by critical behavior confined to a neighborhood of the paraboloid's boundary. This neighborhood excludes the interior near the vertex.

Specifically, Theorem 1 has two parts:
- **Part A:** Under hypotheses on bounded intermediate-scale energy (Eq. 1.13) and L^{3,infinity} bounds (Eq. 1.14), critical scaling-invariant quantities f, g_gamma, h_gamma are bounded.
- **Part B:** Under stronger hypotheses including pressure information, interior bounds in B(b/16) are obtained.
- **Corollary 2:** Under all assumptions, (0,0) is a regular point.

### The "Dynamic Refinement" (Section 3.1)

The paper introduces a **time-dependent pressure decomposition** with three pieces:

```
eta_N(x,tau) * p(x,tau) = p_1(x,tau) + p_2(x,tau) + p_3(x,tau)    (Eq. 3.6)
```

where eta_N is a smooth cutoff adapted to the paraboloid. The key innovation is that the cutoff eta_N depends on time through the parabolic scaling factor theta_a(tau) = sqrt(-a*tau):

- **p_1:** Inner region contribution, from B((N/2+1)*theta_a(tau)). Bounded by distance separation (Eq. 3.7): |p_1| <= C/(N^3 * theta_a^3) * integral |v|^2.
- **p_2:** Intermediate annular region, from B((N+3)*theta_a^{1/2}) \ B((N/2+1)*theta_a). Controlled via CZ theory (Eq. 3.10): ||p_2||_{L^{3/2,inf}} <= C * ||v||^2_{L^{3,inf}}.
- **p_3:** Outer region where supports separate by C*theta_a^{1/2}. Bounded (Eq. 3.9): |p_3| <= C/theta^{3/2} * integral (|v|^2 + |p|).

**The "dynamic" aspect:** The cutoff regions themselves MOVE in time (because they depend on theta_a(tau)), so the decomposition adapts to the paraboloid geometry. This is different from Vasseur (2007) and Choi-Vasseur (2014), where the cutoffs were purely spatial and static.

### Technical Methodology

The paper uses a Gronwall-type argument (Section 2) to bound the critical energy, with the key differential inequality:
```
theta_a^2 * d_s g_gamma + A * g_gamma <= C
```

This is an energy method approach, NOT a De Giorgi iteration. The paraboloid geometry replaces the nested balls of De Giorgi.

---

## 6. Connection to the Beta Exponent

**[PAPER]** The Fernandez-Dalgo paper does **NOT** address the De Giorgi iteration exponent beta. It operates in a fundamentally different framework:

- **Vasseur (2007) / Choi-Vasseur (2014):** De Giorgi iteration on nested balls, recurrence U_k <= C^k * U_{k-1}^beta, need beta > 1.
- **Fernandez-Dalgo (2025):** Energy methods on paraboloids, Gronwall inequality, no iterative recurrence.

**[INTERPRETATION]** The paper's "dynamic refinement" is about optimal localization of the pressure in a paraboloid geometry for epsilon-regularity purposes. It does not attempt to improve the De Giorgi iteration exponent. The pressure decomposition is structurally similar to CV14 (three-way split) but adapted to time-dependent domains.

The paper extends earlier work by Fernandez-Dalgo (reference [2] in the paper), which had a restriction on the aperture parameter a ~ 1. The dynamic decomposition relaxes the L^3 hypothesis from exterior regions to intermediate scales, requiring only L^{3,infinity} localized behavior.

**Bottom line:** This paper is about epsilon-regularity criteria in a paraboloid geometry, not about the De Giorgi recurrence exponent. It represents progress in a DIFFERENT direction from the beta problem.

---

## 7. Landscape of Post-2007 De Giorgi Approaches

| Year | Authors | Paper/Result | Relation to beta | Status |
|------|---------|-------------|-------------------|--------|
| 2007 | Vasseur | New proof of partial regularity via De Giorgi | beta < 4/3 (Prop 3), bottleneck is P_k^{21} | Published, foundational |
| 2010 | Vasseur | Higher derivatives estimate for 3D NS | Uses De Giorgi iteration, proves nabla^2 u in L^{4/3,inf} | Published |
| 2010 | Caffarelli-Vasseur | De Giorgi method for regularity (survey) | Pedagogical review, no beta improvement | Published |
| 2012 | Caffarelli-Vasseur | De Giorgi method for nonlocal fluid dynamics | Extension to nonlocal operators, not beta improvement | Published |
| 2014 | Choi-Vasseur | Fractional higher derivatives (CV14) | beta = 7/6 used (weaker than 4/3, sufficient for their goal). New P_3 absorption trick | Published |
| 2016 | Vasseur | De Giorgi method survey (Morningside Lectures) | Review, no beta improvement | Published |
| 2018 | Colombo-De Lellis-Massaccesi | Generalized CKN for hyperdissipative NS | CKN extension to s > 1 (fractional Laplacian), different framework from De Giorgi iteration | Published 2020 |
| 2019 | Choi-Kang(?) | One-scale epsilon-regularity | Pressure decomposition for one-scale criteria, not directly about beta | Published |
| 2021 | Vasseur-Yang | Second derivatives estimate for 3D NS | De Giorgi on vorticity equation, obtains nabla^2 u in L^{4/3,q} for q > 4/3. Does NOT need or improve beta for velocity | Published |
| 2021 | Barker-Prange | Quantitative regularity via spatial concentration | Uses De Giorgi-type techniques for quantitative blow-up bounds, different from beta problem | Published |
| 2022 | Albritton-Barker-Prange | Epsilon regularity via weak-strong uniqueness | New concise proof of one-scale epsilon regularity, not about beta | Published 2023 |
| 2022 | Lei-Ren | Quantitative partial regularity of NS | Log improvement of CKN, pigeonholing, not De Giorgi iteration | Published 2024 |
| 2025 | Fernandez-Dalgo | Dynamic refinement of pressure decomposition | Paraboloid geometry, Gronwall approach, NOT about beta | Preprint |

### Notable Absent Approaches

**[INTERPRETATION]** A striking pattern emerges: **No paper since Vasseur (2007) has attempted to improve beta in the De Giorgi iteration for the standard NS equations.** The post-2007 literature divides into:

1. **Applications of De Giorgi to HIGHER REGULARITY** (Vasseur 2010, CV14, Vasseur-Yang 2021): Using the De Giorgi framework to prove integrability of higher derivatives. These papers ACCEPT beta < 4/3 (or even use weaker exponents like 7/6) and build on top of it.

2. **Alternative regularity frameworks** (CKN improvements, epsilon-regularity criteria, concentration/quantitative methods): These achieve regularity results by different means — Gronwall, comparison principles, weak-strong uniqueness — and do not use the De Giorgi level-set iteration at all.

3. **Extensions to other equations** (hyperdissipative NS, nonlocal operators): CKN-type results for modified equations.

**No paper has attempted a direct assault on improving the recurrence exponent beta beyond 4/3 in Vasseur's De Giorgi framework.**

---

## 8. Current State of the Art

### The beta = 4/3 barrier is UNTOUCHED

**[INTERPRETATION — supported by comprehensive literature survey]** As of early 2025:

1. **beta < 4/3 remains the best known exponent** in Vasseur's De Giorgi iteration for NS regularity. No publication has claimed to improve it.

2. **The Choi-Vasseur (2014) decomposition does NOT improve beta.** It achieves beta = 7/6 (weaker) and absorbs P_3 through a time-dependent truncation trick. This trick removes a k-independent term but does not address the P_k^{21} bottleneck that limits beta.

3. **Vasseur's Conjecture 14** (that beta > 3/2 implies regularity of all suitable weak solutions) remains open. The gap from 4/3 to 3/2 is > 1/6 and no approach has narrowed it.

4. **The P_k^{21} bottleneck is structural.** As confirmed by Exploration 004 (CZ slack is k-independent) and this survey (no decomposition has circumvented it), the non-divergence local pressure term bounded independently of U_{k-1} by CZ theory is a fundamental obstacle.

5. **Alternative decompositions reorganize but don't improve.** Both CV14 and Fernandez-Dalgo (2025) offer different ways to decompose and handle the pressure, but neither changes the fundamental exponent. CV14's P_3 absorption is about terms that were ALREADY favorable in Vasseur (2007). Fernandez-Dalgo's dynamic approach is about epsilon-regularity, not De Giorgi iteration.

### What WOULD Be Needed

**[INTERPRETATION]** To improve beta, one would need to find a way to make the non-divergence pressure contribution depend on U_{k-1} (i.e., get small as the level sets get small). The CZ theory gives ||P_k^{21}||_{L^q} <= C * ||source||_{L^q}, where the source involves u(1-v_k/|u|) bounded by 1. This bound is TIGHT (confirmed computationally in Exploration 004). Possible routes:

- **Exploit cancellations in the source term** beyond what CZ theory captures (e.g., the source is a product of two copies of u(1-v_k/|u|), so it has a specific quadratic structure)
- **Use regularity of the source** (it is not merely L^inf; it has spatial regularity that CZ theory ignores)
- **Change the test function** in the energy inequality to reduce the weight of the P_k^{21} term
- **Use a completely different iteration scheme** that avoids the pressure altogether (e.g., vorticity-based De Giorgi, as Vasseur-Yang (2021) partially do)

---

## Summary of Key Findings

1. **Choi-Vasseur (2014) decomposes P = P_{1,k} + P_{2,k} + P_3** where P_3 is k-independent and absorbed into the truncation level via a time-dependent threshold E_k(t). This removes P_3 from the energy inequality entirely.

2. **The absorption mechanism** works because nabla P_3 is in L^1_t L^inf_x: the truncation level rises by the accumulated nabla P_3, and the resulting sign is favorable (Eq. 47).

3. **The exponent achieved is beta = 7/6** (Lemma 3.4), explicitly noted as "not optimal" with any exponent > 1 sufficient for their purpose.

4. **This does NOT bypass the P_k^{21} bottleneck.** The local pressure P_{2,k} contains the same non-divergence CZ-limited term. CV14 simply doesn't decompose P_{2,k} further because they don't need to.

5. **arXiv:2501.18402** (Fernandez-Dalgo 2025) is about dynamic pressure decomposition in paraboloid geometry for epsilon-regularity, NOT about the De Giorgi recurrence exponent. It uses Gronwall methods, not De Giorgi iteration.

6. **No paper since 2007 has improved beta beyond 4/3** in the De Giorgi iteration for NS. The 4/3 barrier is untouched and appears to be a hard open problem.

7. **The post-2007 literature has moved in orthogonal directions:** higher derivatives, quantitative regularity, epsilon-regularity criteria, and hyperdissipative extensions — all accepting beta < 4/3 rather than trying to improve it.

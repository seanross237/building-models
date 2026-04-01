# Exploration 003: Tran-Yu on Galilean Invariance and the Pressure Term

## Goal
Assess the Tran-Yu research program (2015-2021) on using Galilean invariance to improve pressure estimates in Navier-Stokes regularity, and determine whether their approach offers a viable path to improving the De Giorgi recurrence exponent beta beyond 4/3.

---

## 0. Paper Identification

The GOAL referenced "Tran-Yu (2014, Ann. Inst. Henri Poincare)" — no such paper exists. The actual Tran-Yu program consists of **five papers** (the date/journal was misremembered):

| # | Paper | Year | Journal |
|---|-------|------|---------|
| 1 | "Depletion of nonlinearity in the pressure force driving NS flows" | 2015 | Nonlinearity 28(5), 1295-1306 |
| 2 | "Pressure moderation and effective pressure in NS flows" | 2016 | Nonlinearity 29, 2990-3005 |
| 3 | "Logarithmic improvement of regularity criteria for NS in terms of pressure" | 2016 | Appl. Math. Lett. 58 |
| 4 | "Note on Prodi-Serrin-Ladyzhenskaya type regularity criteria for NS" | 2017 | J. Math. Phys. 58(1), 011501 |
| 5 | "Velocity-pressure correlation in NS flows and global regularity" | 2021 | J. Fluid Mech. 911, A18 |

Paper 5 (2021) is the one that explicitly uses Galilean invariance. Papers 1-4 build the foundation. All are co-authored by Chuong V. Tran (St Andrews) and Xinwei Yu (Alberta).

---

## 1. What Tran and Yu Prove

### The Common Framework

All five papers work from the **L^q energy evolution equation** for q >= 3. Taking the inner product of the NS equation with |u|^{q-2}u and integrating by parts:

```
(1/q) d/dt ||u||_{L^q}^q + (4(q-1)/q^2) ||nabla|u|^{q/2}||_{L^2}^2
    = (q-1) integral p |u|^{q-3} u . nabla|u| dx
```

**[TRAN-YU]** The RHS is the "pressure driving term." The entire program studies whether and how this term can be controlled to prevent blowup.

### Paper 1 (2015): Depletion of Nonlinearity

**Main result (Theorem 1):** The pressure driving term on the RHS is **naturally depleted** due to a negative correlation between |u| and |nabla|u||. On level sets of |u|, we have nabla|u| = 0 at maxima, so the integrand vanishes where |u| is largest. The depletion bound:

```
|integral p |u|^{q-3} u.nabla|u| dx| <= (q-2) ||p||_{L^{3/2}(Omega)} ||  |u|^{q-2} |nabla|u||  ||_{L^3}
```

where Omega = {x : |u(x,t)| > c||u||_{L^q}} is the high-velocity region with |Omega| -> 0 as q -> infinity.

**Regularity criterion:** If ||p||_{L^{3/2}(Omega)} -> 0 as |Omega| -> 0, then ||u||_{L^q} grows at most mildly (non-singularly).

### Paper 2 (2016): Pressure Moderation

**Central innovation: the pressure moderator.** **[TRAN-YU]** The pressure p in the L^q evolution is determined only up to a function P(x,|u|). Any function P satisfying:

```
integral nabla . (P |u|^{q-2} u) dx = 0
```

can be freely added to p without changing the evolution equation for ||u||_{L^q}^q. This gives the **effective pressure:**

```
p_eff = p + P(x, |u|)
```

**[TRAN-YU] Theorem 2:** Under the same setup, if

```
integral_0^T ||p + P||_{L^{3/2}(Omega(t))}^{q/(q-3)} dt < infinity
```

for some admissible pressure moderator P, then u remains smooth beyond T. Since P can be chosen to reduce |p + P| in Omega, this is a **strictly weaker** condition than the unmoderated criterion.

**Simple moderation scheme:** Choose P so that on every streamline, P = -p at the point of maximum |u|. Then p_eff = 0 at velocity maxima — the effective pressure vanishes precisely where the velocity is largest.

### Paper 4 (2017): Prodi-Serrin Improvement

**[TRAN-YU] Theorem 1 (velocity):** u in L^r(0,T; L^s) . ||u||_{L^3}^{-alpha} < infinity for 2/r + 3/s <= 1 + alpha improves the classical criterion.

**[TRAN-YU] Theorem 2 (pressure):** ||p||_{L^r(0,T; L^s)} . ||u||_{L^3}^{-beta} < infinity for 2/r + 3/s <= 2 + beta improves the Berselli-Galdi criterion.

**Mechanism:** Near blowup, ||u||_{L^3} must blow up (by Escauriaza-Seregin-Sverak), so ||u||_{L^3}^{-alpha} -> 0, compensating the blowup. **No Galilean invariance used here.**

### Paper 5 (2021): Velocity-Pressure Correlation (THE KEY PAPER)

**[TRAN-YU]** This paper **explicitly uses Galilean boosts.** The NS equations are Galilean invariant: if (u,p) is a solution, then for any constant u_0:

```
u~(x,t) = u(x - u_0 t, t) - u_0
p~(x,t) = p(x - u_0 t, t)
```

is also a solution.

**The velocity-pressure correlation coefficient** Gamma_s(t) in [-1,1] measures the degree of correlation between high velocity and low pressure.

**[TRAN-YU] Theorem 3.1:** A Leray-Hopf solution smooth on (0,T) remains smooth beyond T if:

```
integral_0^T (Gamma_s(t) / R_0^2)^{s/(s-3)} ||u(t)||_{L^s}^{2s/(s-3)} dt < infinity
```

**[TRAN-YU] Lemma 3.2 (Evolution with Galilean frame):** For any constant u_0 in R^3:

```
d/dt ||u - u_0||_{L^s}^s + c ||nabla|u - u_0|^{s/2}||_{L^2}^2
    <= (s-1) integral |p| |u - u_0|^{s-2} |nabla|u - u_0|| dx
```

Choosing u_0 optimally minimizes ||p||_{L^{s/(s-2)}} on Omega' = {x : |u - u_0| > c||u - u_0||_{L^s}}.

**Physical interpretation:** "As long as global pressure minimum(a) and velocity maximum(a) are mutually exclusive, regularity is likely to persist."

---

## 2. How Galilean Invariance Enters Their Argument

### Classification: BETTER CONSTANT (modest improvement)

**[INTERPRETATION]** Galilean invariance enters the Tran-Yu program in one specific way:

**In the 2021 paper (Paper 5):** The Galilean boost u -> u - u_0 is used to **reduce the effective L^s norm of the velocity** in the pressure driving term. The frame shift does NOT change the pressure (see Section 4 below for why), but it changes the velocity factor |u - u_0|^{s-2} in the energy estimate, which can be made smaller by choosing u_0 appropriately.

This is:
- **A better constant in existing estimates** — the same inequality, but with ||u - u_0||_{L^s} replacing ||u||_{L^s}
- **NOT a better exponent** — the Holder/CZ exponents are unchanged
- **NOT a structural change** — the same terms appear, in the same order

### What it does NOT do

**[INTERPRETATION, CRITICAL]** The Galilean boost does **not** improve the CZ bound on the pressure. The reason is fundamental:

For incompressible flow (div u = 0), the pressure Poisson equation is:
```
-Delta p = sum_{i,j} partial_i partial_j (u_i u_j)
```

Under u -> u - u_0 (constant u_0):
```
-Delta p' = sum_{i,j} partial_i partial_j ((u_i - u_{0,i})(u_j - u_{0,j}))
          = sum partial_i partial_j (u_i u_j) - 2 sum u_{0,i} partial_i (partial_j u_j) - sum u_{0,i} u_{0,j} partial_i partial_j (1)
          = sum partial_i partial_j (u_i u_j)   [since div u = 0 and d^2(const) = 0]
```

**The pressure Poisson equation is Galilean invariant for divergence-free flows.** The CZ bound ||p||_{L^q} <= C_q ||u||_{L^{2q}}^2 is unchanged by the frame shift because the source term is identical.

---

## 3. Connection to the De Giorgi Framework

### The Tran-Yu program and Vasseur's De Giorgi iteration address DIFFERENT frameworks

**[INTERPRETATION, CRITICAL]** This is the key structural finding of this exploration.

**Vasseur (2007):** Works with the **local energy inequality** on nested balls B_k, with level-set truncations v_k = (|u| - (1 - 2^{-k}))_+. The pressure is decomposed into:
- P_k^1 (nonlocal, harmonic on B_k) — controlled by mean value property
- P_k^2 (local, CZ-controlled) — further split into divergence form (P_k^{22}) and non-divergence form (P_k^{21})

The bottleneck is the **specific term**:
```
I_k = integral integral |P_k^{21}| . |d_k| . 1_{v_k > 0} dx dt
```

where P_k^{21} satisfies -Delta P_k^{21} = sum partial_i partial_j [u_j(1 - v_k/|u|) u_i(1 - v_k/|u|)].

**Tran-Yu (2015-2021):** Works with the **global L^q energy equation**:
```
(1/q) d/dt ||u||_{L^q}^q = -(viscous term) + (pressure driving term)
```

There are **no nested balls**, **no level-set truncations**, **no local pressure decomposition**. The pressure appears as the full global pressure p in the L^q energy equation, not as a decomposed local piece P_k^{21}.

### Does Tran-Yu's result directly improve Vasseur's beta?

**NO.** For three structural reasons:

**(a) Different energy functionals.** Vasseur's U_k = integral |v_k|^2 dx dt (level-set energy on nested balls) vs. Tran-Yu's ||u||_{L^q}^q (global L^q norm). The recurrence U_k <= C^k U_{k-1}^{beta} does not appear in the Tran-Yu framework.

**(b) Different pressure objects.** Vasseur's bottleneck is P_k^{21} (a specific piece of the locally decomposed pressure on B_k, associated with the non-divergence part involving the truncation function). Tran-Yu's pressure moderation applies to the **full global pressure p**. There is no obvious way to insert a pressure moderator P(x,|u|) into the De Giorgi iteration at the level of P_k^{21}.

**(c) The Galilean boost doesn't help P_k^{21}.** The CZ bound on P_k^{21} comes from the source term u_j(1 - v_k/|u|) u_i(1 - v_k/|u|), which is bounded by 1 (since both factors are bounded by 1). A Galilean boost u -> u - u_0 changes the source to (u_j - u_{0,j})(1 - v_k/|u - u_0|) (u_i - u_{0,i})(1 - v_k/|u - u_0|). On the support of the truncation (where |u - u_0| >= 1 - 2^{-k}), the factors (u_i - u_{0,i})(1 - v_k/|u - u_0|) are still bounded by 1. **The CZ bound is unchanged.**

### How Galilean invariance ACTUALLY helps in the De Giorgi context

**[INTERPRETATION]** The Vasseur school (Vasseur 2010, Choi-Vasseur 2014) uses Galilean invariance **differently** — not as a pressure moderation scheme, but as a **blow-up rescaling along Lagrangian trajectories**:

```
v(s,y) = epsilon . u(t + epsilon^2 s, X(t + epsilon^2 s, t, x) + epsilon y) - epsilon . u_epsilon(...)
Q(s,y) = epsilon^2 . P(t + epsilon^2 s, ...) + epsilon . y . partial_s[u_epsilon(...)]
```

This subtraction of the local mean velocity u_epsilon enforces **mean-zero** for v. The mean-zero condition:
- Eliminates the large constant drift from the convection term (u . nabla)u
- Ensures ||v||_{L^p} is controlled by nabla u alone (Poincare inequality)
- Makes the CZ bound on the rescaled pressure Q tighter in the interaction integral

**But this already appears in Vasseur's existing framework.** The improvement from the mean-zero property is already absorbed into the current bound beta < 4/3. It is not a new lever to push beta higher.

---

## 4. Correctness Assessment

### Are the Tran-Yu results correct?

**[INTERPRETATION]** Based on the available evidence (abstracts, secondary descriptions, and the mathematical framework reconstructed from multiple sources):

**(a) The pressure moderation identity is correct.** The observation that P(x,|u|) can be added to p in the L^q energy equation (provided the admissibility integral vanishes) is a straightforward consequence of integration by parts and the divergence-free condition. This is not in doubt.

**(b) The Galilean invariance of the pressure Poisson equation is correct and well-known.** The cross-terms vanish exactly because div u = 0.

**(c) The velocity-pressure correlation criterion (2021) is likely correct** but represents a different type of result than what our mission needs. It provides a new regularity criterion (conditions under which solutions remain smooth), not a new method for proving regularity for all solutions.

### Key limitation to flag

**[INTERPRETATION]** The Tran-Yu criteria are of the form "if [condition on p] holds, then regularity holds." They do **not** prove that the condition holds for all Leray-Hopf solutions. The question of NS regularity is whether these conditions are automatically satisfied, which remains open. The Tran-Yu results are **conditional** regularity criteria, not unconditional regularity proofs.

This is not a flaw — all classical criteria (Prodi-Serrin, Berselli-Galdi, etc.) are also conditional. But it means the results don't directly close the gap in Vasseur's beta.

---

## 5. What Galilean Invariance Contributes (Classification)

### Better constant: YES (modest)

In the L^q energy framework, choosing u_0 optimally reduces ||u - u_0||_{L^s} compared to ||u||_{L^s}. The pressure itself is unchanged (Galilean invariant), but the velocity factor in the energy estimate is reduced. This gives a better constant in the regularity criterion but does not change the scaling exponents.

### Better exponent: NO

The Holder exponents, CZ exponents, and scaling relations are all unchanged by the frame shift. The condition 2/r + 3/s <= 2 (for pressure criteria) remains the same regardless of frame.

### Structural improvement: PARTIALLY (in the 2021 paper)

The velocity-pressure correlation coefficient Gamma_s(t) is a genuinely new quantity. The insight that singularity requires simultaneous collocation of velocity maxima and pressure minima is physically meaningful. However, this structural insight has not been translated into a quantitative improvement of any unconditional regularity result.

### For the De Giorgi bottleneck P_k^{21}: NO improvement

The Galilean boost does not help with P_k^{21} because:
1. The pressure Poisson source is Galilean-invariant (for div-free flows)
2. The truncation factors (1 - v_k/|u|) remain bounded by 1 regardless of frame
3. The CZ bound ||P_k^{21}||_{L^q} <= C_q is a constant independent of the level-set energy — this "constant" character is unchanged by any frame shift

---

## 6. Assessment for Our Mission

### Grade: **(C) Not applicable — the improvement is orthogonal to the De Giorgi bottleneck**

**Justification:**

The Tran-Yu program is mathematically sound and provides genuine insights into the role of pressure in NS regularity. However:

1. **Different framework:** Tran-Yu works in L^q global energy space; Vasseur's bottleneck is in local De Giorgi level-set space. The two frameworks have different pressure objects, different energy functionals, and different iteration structures.

2. **The Galilean boost doesn't help the bottleneck term.** The pressure Poisson equation is Galilean-invariant for incompressible flow. The CZ bound on P_k^{21} is determined by the source u(1-v_k/|u|), which is bounded by 1 independently of the frame. No constant-velocity frame shift can improve this.

3. **The pressure moderation trick can't be inserted into De Giorgi.** The admissible class P(x,|u|) is defined relative to the L^q energy equation's integration-by-parts structure. The De Giorgi iteration has a different local structure (nested balls, truncation functions) where this identity doesn't apply.

4. **The conditional criteria are orthogonal to beta.** Tran-Yu's criteria say "if the effective pressure is small on Omega, regularity holds." Vasseur's iteration says "we need beta > 3/2 for the level-set energy to converge." These are different questions about different objects.

### What IS potentially useful from Tran-Yu

**[INTERPRETATION]** Two ideas merit further thought, even though they don't directly help beta:

**(a) The nonlinear depletion observation (2015).** The fact that the pressure driving term vanishes at velocity maxima (because nabla|u| = 0 there) is a structural feature that might be exploitable in other contexts. In the De Giorgi framework, the analogous quantity would be the gradient of the truncation function d_k = nabla v_k, which also vanishes at the center of the level set. Whether this "depletion at maxima" can be quantified in the De Giorgi recurrence is an open question.

**(b) The velocity-pressure anti-correlation (2021).** If high velocity and low pressure are genuinely anti-correlated (as the Bernoulli principle suggests for smooth flows), then the interaction integral I_k = integral |P_k^{21}| . |d_k| . 1_{v_k > 0} might be empirically smaller than the CZ worst-case bound. This would not improve the analytical bound on beta, but it could explain why the empirical beta (from DNS) exceeds 4/3. This connects to the "CZ slack on P_k^{21}" computation identified in Exploration 001.

---

## Sources

- [Velocity-pressure correlation in NS flows (JFM 2021)](https://www.cambridge.org/core/journals/journal-of-fluid-mechanics/article/velocitypressure-correlation-in-navierstokes-flows-and-the-problem-of-global-regularity/CE28509C5B6844BC5F27F3EF52075E47)
- [Pressure moderation and effective pressure (Nonlinearity 2016)](https://www.researchgate.net/publication/306270433_Pressure_moderation_and_effective_pressure_in_Navier-Stokes_flows)
- [Depletion of nonlinearity in the pressure force (Nonlinearity 2015)](https://www.researchgate.net/publication/275157447_Depletion_of_nonlinearity_in_the_pressure_force_driving_Navier-Stokes_flows)
- [Note on Prodi-Serrin-Ladyzhenskaya type criteria (JMP 2017)](https://pubs.aip.org/aip/jmp/article/58/1/011501/317302/Note-on-Prodi-Serrin-Ladyzhenskaya-type-regularity)
- [Regularity of NS flows with pressure bounds (AML 2017)](https://www.sciencedirect.com/science/article/pii/S0893965916302993)
- [Xinwei Yu publication list](http://www.math.ualberta.ca/~xinweiyu/)
- [Pineau-Yu: New Regularity Criteria in Terms of Pressure (arXiv:1910.08911)](https://arxiv.org/abs/1910.08911)
- [Higher derivatives estimate (Vasseur 2010, Numdam)](https://www.numdam.org/item/AIHPC_2010__27_5_1189_0.pdf)
- [Fractional higher derivatives (Choi-Vasseur 2014, Numdam)](https://www.numdam.org/item/AIHPC_2014__31_5_899_0.pdf)
- [Dynamic Refinement of Pressure Decomposition (arXiv:2501.18402)](https://arxiv.org/abs/2501.18402)

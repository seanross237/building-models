---
topic: Tran-Yu Galilean invariance program — orthogonal to De Giorgi bottleneck
confidence: verified
date: 2026-03-30
source: vasseur-pressure exploration-003
---

## Finding

The Tran-Yu research program (5 papers, 2015-2021: Nonlinearity 2015, Nonlinearity 2016, AML 2016, JMP 2017, JFM 2021) studies how Galilean invariance and pressure moderation affect NS regularity criteria in the **global L^q energy framework**. Their approach is **orthogonal to the De Giorgi bottleneck** — it cannot improve beta.

## The Tran-Yu Program

All five papers work from the L^q energy evolution equation:

```
(1/q) d/dt ||u||_{L^q}^q + (viscous term) = (q-1) integral p |u|^{q-3} u . nabla|u| dx
```

Key innovations:
- **Pressure moderation (2016):** Any P(x,|u|) satisfying an admissibility integral can be freely added to p, giving an "effective pressure" p_eff = p + P. Choosing P optimally weakens the regularity criterion.
- **Galilean boost (2021):** u -> u - u_0 reduces ||u - u_0||_{L^s} in the energy estimate. The pressure is unchanged (Galilean-invariant for div-free flows: the cross-terms vanish because div u = 0).

## Classification: Better Constant Only

- **Better constant: YES (modest)** — optimal u_0 reduces the velocity factor in energy estimates
- **Better exponent: NO** — Holder/CZ exponents unchanged by frame shift (2/r + 3/s <= 2 is invariant)
- **Structural: PARTIAL** — the velocity-pressure correlation coefficient Gamma_s(t) is a genuinely new quantity, but has not produced a quantitative unconditional improvement

## Why It Cannot Improve Beta

Three structural reasons:

**(a) Different energy functionals.** Vasseur's U_k = integral |v_k|^2 (level-set energy on nested balls) vs. Tran-Yu's ||u||_{L^q}^q (global L^q norm). The De Giorgi recurrence U_k <= C^k U_{k-1}^{beta} does not appear in the Tran-Yu framework.

**(b) Different pressure objects.** Vasseur's bottleneck is P_k^{21} (non-divergence part of locally decomposed pressure on B_k). Tran-Yu's moderation applies to the full global pressure p. The pressure moderator P(x,|u|) has no insertion point in the De Giorgi iteration at the level of P_k^{21}.

**(c) Galilean boost doesn't help P_k^{21}.** The pressure Poisson equation is Galilean-invariant. The CZ bound on P_k^{21} comes from source terms bounded by 1 (truncation factors (1 - v_k/|u|) remain bounded regardless of frame). No constant-velocity frame shift changes this.

## Conditional vs. Unconditional

All Tran-Yu results are **conditional** regularity criteria ("if effective pressure is small on Omega, regularity holds"). They do not prove the condition holds for all Leray-Hopf solutions. This is standard (all classical criteria are conditional), but it means the results don't directly address whether beta > 3/2.

## Vasseur School's Different Use of Galilean Invariance

Vasseur (2010) and Choi-Vasseur (2014) use Galilean invariance **differently** — as blow-up rescaling along Lagrangian trajectories (subtracting local mean velocity to enforce mean-zero). This is already absorbed into the current beta < 4/3. It is not a new lever.

## Potentially Useful Ideas

Two observations from Tran-Yu merit further thought despite not directly helping beta:

1. **Nonlinear depletion (2015):** The pressure driving term vanishes at velocity maxima (nabla|u| = 0 there). The De Giorgi analogue would be d_k = nabla v_k vanishing at level-set centers. Whether this "depletion at maxima" is quantifiable in the recurrence is open.

2. **Velocity-pressure anti-correlation (2021):** If high velocity and low pressure are genuinely anti-correlated (Bernoulli principle for smooth flows), the interaction integral I_k might be empirically smaller than the CZ worst-case bound. This would not improve analytical beta but could explain why empirical beta exceeds 4/3.

## Assessment Grade: C (Not applicable — orthogonal to the De Giorgi bottleneck)

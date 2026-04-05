---
topic: Vasseur-Yang 2021 vorticity De Giorgi — universal 4/3 barrier
confidence: verified
date: 2026-03-30
source: "vasseur-pressure exploration-008"
---

## Main Result

Vasseur, A. and Yang, J. "Second Derivatives Estimate of Suitable Solutions to the 3D Navier-Stokes Equations." *Archive for Rational Mechanics and Analysis* 241, 683-727 (2021). arXiv:2009.14291.

The paper applies De Giorgi iteration to a pressure-free variable v = -curl(phi_sharp * Delta^{-1} * phi * omega), where phi, phi_sharp are smooth cut-off functions and omega = curl u. This variable:
- Is divergence-free and compactly supported
- Has the same scaling and regularity as velocity u
- Inherits a local energy inequality from u (Theorem A.1)
- Depends only on LOCAL information — no pressure

The De Giorgi iteration on v has the same level-set structure as Vasseur (2007): rising energy levels c_k = 1 - 2^{-k}, dyadic cylinders, energy functional U_k = ||v_k||^2_{L^inf L^2} + ||d_k||^2_{L^2}.

## The Recurrence and Its Closure

The iteration achieves the recurrence (Proposition 5.1):

U_k <= C^k * U_{k-1}^{min{4/3, 5/3 - 2/(3p_3)}}

where p_3 = (1/p_1 + 1/p_2)^{-1} > 1. Maximum achievable exponent (as p_3 -> infinity) is 4/3.

**The iteration CLOSES** because:
- U_0 can be made arbitrarily small via blow-up (Proposition 4.1)
- For small U_0, beta > 1 suffices for convergence
- 4/3 > 1, so the iteration converges to U_k -> 0

This contrasts with Vasseur (2007) where beta > 3/2 was needed (for large U_0) and 4/3 < 3/2 meant failure.

## The New Bottleneck: Trilinear Form

The 4/3 arises from the interior trilinear form (Section 5.1):

|T_nabla[alpha_k v, rho_k^sharp beta_k v, beta_k v]| <= ||nabla(beta_k v)||_{L^2} * U_{k-1}^{5/6} <= U_{k-1}^{4/3}

The decomposition: 1/2 (one derivative costs U^{1/2}) + 5/6 (two nonlinear factors at velocity scale) = 4/3.

This comes from the Riesz operator term nabla R(u tensor v) in the v equation, NOT from the NS pressure. The Riesz operator R = (1/2)tr - Delta^{-1} div div combines the kinetic energy gradient and pressure gradient in a different form.

## Universal Barrier Interpretation

The pressure bottleneck P_k^{21} is genuinely ABSENT. But the quadratic nonlinearity of NS produces a new 4/3 bottleneck from a different mechanism:

| Feature | Velocity (Vasseur 2007) | Vorticity (Vasseur-Yang 2021) |
|---|---|---|
| Source of 4/3 | P_k^{21} (non-divergence local pressure) | Trilinear Riesz operator nabla R(v tensor v) |
| Mechanism | CZ theory bounds P_k^{21} independently of U_{k-1} | Derivative costs U^{1/2}; cubic nonlinearity provides U^{5/6} |
| Nature | External: pressure couples via Poisson equation | Internal: nonlinear self-interaction |

**The 4/3 appears to be a universal barrier for De Giorgi iterations on NS, encoded in the product structure of the quadratic nonlinearity, not in any specific formulation artifact.**

## Local Bootstrap to Full Smoothness

Under local smallness (Theorem 1.3), the paper achieves:
1. |v| <= 1 (De Giorgi, Proposition 5.1)
2. omega^{3/4} bounded (Proposition 6.1a)
3. omega bounded (Proposition 6.1b)
4. All nabla^n omega bounded (Proposition 6.2, induction)
5. nabla^n omega in L^infinity for all n (Sobolev embedding)

This is MORE than the velocity approach achieves — full local C^infinity smoothness vs. just L^infinity bounds on velocity.

## Beltrami Connection

For exact Beltrami flows (omega = lambda u): omega x u = 0, so vorticity equation reduces to the heat equation (trivially regular). The trilinear bottleneck from nabla R(v tensor v) also simplifies because the bilinear commutator B = 0 when omega x u = 0. For near-Beltrami u = u_B + eps v_pert: Lamb vector enters at O(eps), trilinear bottleneck at O(eps^2).

## Implications for the Mission

1. **No reformulation preserving quadratic nonlinearity will improve beta beyond 4/3.** The bottleneck is encoded in the product structure (one derivative x two velocity-scale factors), not in formulation artifacts.
2. **The gap between 4/3 and 3/2 may be fundamental** to the mathematical structure of 3D NS.
3. **The blow-up + smallness approach is a viable workaround** — converts the problem from needing beta > 3/2 to needing only beta > 1. But this does not solve the millennium problem.

## S2-E001 Cross-Comparison Detail

Strategy-002 Exploration 001 provided a detailed side-by-side audit confirming that the vorticity formulation produces the SAME 1/2 + 5/6 chain through identical mathematical steps: Sobolev H^1→L^6 → L^{10/3} interpolation → Chebyshev → L^2 indicator norm. The 4/3 appears in the trilinear terms T_∇[alpha_k v, rho_k beta_k v, beta_k v] that cannot be written in divergence form, involving a gradient factor (nabla in T_∇) contributing U_{k-1}^{1/2} and a Chebyshev indicator factor contributing U_{k-1}^{5/6}. The free parameters (truncation, Sobolev target, Holder pairs, cutoffs) are all identically exhausted. This confirms the 4/3 is NOT a pressure artifact — it is encoded in the product structure of the quadratic nonlinearity. Full sharpness audit at `proposition-3-sharpness-audit.md`.

## S2-E003 Universal Formula Confirmation

S2-E003 derived the universal formula beta = 1 + s/n for the generic De Giorgi recursion exponent (dimension n, dissipation order s). This confirms 4/3 for 3D NS is the dimensional value 1 + 1/3, not a formulation artifact. The formula was verified across 9 model PDEs (Burgers, 2D NS, 3D NS, 4D NS, MHD, SQG direct, SQG extension, fractional NS at alpha=5/4 and 3/2). SQG's success despite generic beta = 5/4 < 3/2 comes from drift structure (multiplicative constant from BMO^{-1} norm), not from beating the Chebyshev step. Brigati-Mouhot (2025) independently confirm beta = 1 + 2/d for scalar equations. Full table and derivation in `chebyshev-universality-and-model-pde-comparison.md`.

## S2-E004 Third Evidence Point for Universality

S2-E004 provides a third piece of evidence for the universality of the 4/3 barrier: even attempting to improve the CZ bound via compensated compactness (CLMS div-curl) or commutator estimates (CRW) fails at three independent levels. The informal theorem states beta = 4/3 is sharp within the class {energy inequality, Sobolev/interpolation, CZ theory including commutator/CLMS variants, Chebyshev estimates}. This is a qualitatively different type of evidence from E008's vorticity formulation — it shows that the entire analytical toolkit (not just specific formulations) saturates at 4/3. Combined with S2-E003's universal formula beta = 1 + s/n, the picture is now: the 4/3 arises from dimensional analysis, survives formulation changes, and resists the full commutator/compensated compactness toolkit. Full analysis in `compensated-compactness-commutator-obstruction.md`.

## E009 Adversarial Assessment

**The "universality" claim is an induction from two data points, not a theorem.** Vasseur (2007) and Vasseur-Yang (2021) are two specific De Giorgi constructions. There exist infinitely many possible test functions, truncation schemes, and auxiliary variables. The two 4/3's arise from DIFFERENT mechanisms (CZ loss vs. derivative-nonlinearity tradeoff) — so they are not even instances of the same obstruction. This somewhat weakens the "universal structural barrier" narrative but also somewhat strengthens it: if it were easy to beat 4/3, one of these independent mechanisms would have been circumvented. **Corrected framing:** "The 4/3 barrier appears in both velocity-based (CZ pressure bounds) and vorticity-based (derivative-nonlinearity tradeoff) De Giorgi iterations, via independent mechanisms. No improvement has been achieved in 17 years across 13+ papers. Strong evidence that 4/3 is a fundamental obstacle for De Giorgi methods, though a proof of universality remains open." Grade: B (strong but overclaimed). **Partially novel** — individual results are published; the dual-mechanism synthesis framing is new.

## S2-E005 Fourth Evidence Point: LP Toolkit Also Saturates at 4/3

S2-E005 provides a fourth line of evidence for the universality of the 4/3 barrier: Littlewood-Paley frequency decomposition — a qualitatively different analytical toolkit from CZ, commutator, or compensated compactness — also cannot improve beta. The Bernstein exchange rate 2^{3j/5} is the dimensional cost of converting LP regularity to L^{10/3} integrability, and it exactly reproduces the CZ bound. Combined with the prior evidence: (1) velocity De Giorgi: CZ pressure bound saturates at 4/3 (Vasseur 2007), (2) vorticity De Giorgi: trilinear form saturates at 4/3 (Vasseur-Yang 2021), (3) CZ+commutator/CLMS class: all three obstruction layers (S2-E004), (4) LP/frequency-localized: Bernstein structural obstruction (S2-E005). The picture is now: 4/3 arises from dimensional analysis, survives formulation changes, resists the commutator toolkit, and resists frequency-localized decomposition. Full analysis in `frequency-localized-degiorgi-lp-obstruction.md`.

## S2-E006 Fifth Evidence Point: Non-CZ Routes Confirm Tool-Independence

S2-E006 provides a fifth line of evidence via three non-CZ pressure handling routes: (1) direct integration by parts gives beta = 1 (WORSE — proves CZ consolidation is essential, not just convenient); (2) H^1/BMO duality gives beta = 4/3 via a COMPLETELY DIFFERENT mechanism (U-scaling absorbed into ||v_k||_{H^1} rather than ||P^{21}||_{L^{3/2}}); (3) commutator variant gives beta <= 1 (confirms S2-E004). The H^1/BMO match is the strongest new evidence: it shows the 4/3 is not CZ-specific but arises whenever the Chebyshev level-set extraction meets the quadratic nonlinearity, regardless of analytical tool. Survey of 12 published approaches confirms no method achieves beta > 4/3.

**Combined evidence for universality (6 lines):**
1. Velocity De Giorgi + CZ: beta = 4/3 (Vasseur 2007) — pressure bound mechanism
2. Vorticity De Giorgi: beta = 4/3 (Vasseur-Yang 2021) — trilinear form mechanism, pressure eliminated
3. CZ + commutator/CLMS class: three-layer obstruction (S2-E004) — analytical toolkit exhaustion
4. LP/frequency-localized: Bernstein structural obstruction (S2-E005) — frequency-space confirmation
5. Non-CZ routes (IBP, H^1/BMO, CRW): tool-independence confirmed (S2-E006) — different mechanisms, same exponent
6. Chebyshev step provably tight for div-free fields (S2-E008) — constant field extremizer closes last potentially improvable step; all 4 De Giorgi chain steps individually tight under NS constraints

The picture is now: 4/3 arises from dimensional analysis (universal formula 1 + s/n), survives formulation changes (velocity/vorticity), resists the commutator toolkit, resists frequency-localized decomposition, resists non-CZ analytical methods entirely, AND each individual step of the De Giorgi chain is provably tight. Full analysis in `chebyshev-sharpness-constant-field-extremizer.md` (S2-E008) and `non-cz-pressure-routes-tool-independence.md` (S2-E006).

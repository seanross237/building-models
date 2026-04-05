# Exploration 008: Vasseur-Yang (2021) Vorticity-Based De Giorgi

## Goal
Assess whether Vasseur-Yang's vorticity-based De Giorgi approach avoids the pressure bottleneck (beta < 4/3) that limits the velocity-based De Giorgi framework for Navier-Stokes regularity.

## Paper
Vasseur, A. and Yang, J. "Second Derivatives Estimate of Suitable Solutions to the 3D Navier-Stokes Equations." *Archive for Rational Mechanics and Analysis* 241, 683-727 (2021). arXiv:2009.14291.

---

## 1. What Exactly Does Vasseur-Yang Prove?

### Main Theorem (Theorem 1.1)
**[VASSEUR-YANG]** For smooth solutions u to the 3D incompressible Navier-Stokes equations with smooth divergence-free initial data u₀ ∈ L², for any integer n ≥ 0 and any real number q > 1, the vorticity ω = curl u satisfies:

$$\| |∇^n ω|^{4/(n+2)} \mathbf{1}_{\{|∇^n ω|^{4/(n+2)} > C_n t^{-2}\}} \|_{L^{1,q}((0,T) \times \mathbb{R}^3)} \leq C_{q,n} \|u_0\|^2_{L^2}$$

For n = 1, this estimate also holds for suitable weak solutions with only L² divergence-free initial data.

### Corollary 1.2 (The Headline Result)
**[VASSEUR-YANG]** For suitable weak solutions with initial data u₀ ∈ L², for any q > 4/3 and K ⊂⊂ (0,∞) × ℝ³:

$$\|\nabla^2 u\|_{L^{4/3,q}(K)} \leq C_{q,K}(\|u_0\|^{3/2}_{L^2} + 1)$$

This improves from the prior result ∇²u ∈ L^{4/3,∞} (Lions 1996) to ∇²u ∈ L^{4/3,q} for all q > 4/3, a Lorentz space improvement. This is NOT an improvement of the spatial/temporal integrability exponent 4/3, but an improvement within the Lorentz space scale at that exponent.

### Local Theorem (Theorem 1.3)
**[VASSEUR-YANG]** There exists a universal η₁ > 0 such that for any suitable weak solution u in (-4,0) × ℝ³ satisfying:
1. Zero mean condition: ∫_{B₁} u(t,x) φ(x) dx = 0 a.e. t ∈ (-4,0)
2. Smallness: ‖∇u‖_{L^{p₁}_t L^{q₁}_x(Q₂)} + ‖ω‖_{L^{p₂}_t L^{q₂}_x(Q₂)} ≤ η₁

where 4/3 ≤ p₁ ≤ ∞, 1 ≤ p₂ ≤ ∞, 1 ≤ q₁, q₂ < 3 with 1/p₁ + 1/p₂ < 1 and 1/q₁ + 1/q₂ ≤ 7/6,

then for any integer n ≥ 0: ‖∇ⁿω‖_{L^∞(Q_{8^{-n-2}})} ≤ Cₙ.

**[INTERPRETATION]** This is the core result: under LOCAL smallness assumptions (achievable via blow-up), the vorticity and ALL its derivatives are bounded in L^∞. The pressure plays NO role in this local theorem. This is explicitly stated in the paper: the local theorem "needs nothing from the pressure."

---

## 2. How Does De Giorgi Apply to the Vorticity Equation?

### The Key Innovation: The Variable v

**[VASSEUR-YANG]** The paper does NOT apply De Giorgi iteration directly to the vorticity ω. Instead, inspired by Chamorro-Lemarié-Rieusset-Mayoufi (2018), they introduce a new variable:

$$v := -\text{curl}\, \varphi^\sharp \Delta^{-1} \varphi\, \omega$$

where φ and φ♯ are smooth spatial cut-off functions (1_{B_{6/5}} ≤ φ ≤ 1_{B_{5/4}}, 1_{B_{4/3}} ≤ φ♯ ≤ 1_{B_{3/2}}).

**Why v instead of ω?** The paper explains (p.12): "directly working with u is difficult due to the lack of control on the pressure, which is nonlocal. Therefore, we would like to work on vorticity... Since ω is one derivative of u, we have less integrability to do any parabolic regularization, and we don't have the local energy inequality to perform De Giorgi iteration."

**[INTERPRETATION]** The variable v is essentially a "localized inverse curl" of vorticity — it has the same scaling and regularity as velocity u, but its evolution depends only on LOCAL quantities. It sits between ω and u: it's minus-one-derivative of (localized) ω, so it recovers the regularity of u while being pressure-free.

### Properties of v
**[VASSEUR-YANG]** The variable v:
- Is divergence-free and compactly supported
- Scales the same as u
- Has the same regularity as u
- Inherits a local energy inequality from u (proved in Appendix A, Theorem A.1)
- Its evolution depends only on LOCAL information — no pressure

The localization gives a decomposition: φu = v + w, where w is harmonic inside B₁.

### Equation for v
**[VASSEUR-YANG]** The equation for v is (equation 4.4):

$$\partial_t v + \omega \times v + \nabla R(u \otimes v) = B + L + W + \Delta v, \quad \text{div}\, v = 0$$

where:
- R = ½ tr − Δ⁻¹ div div is a symmetric Riesz operator
- B = quadratic commutator (from localization of curl(ω × u))
- L = linear commutator (from [−curl φ♯Δ⁻¹φ, Δ]ω)
- W = remainder involving w (harmonic part) and ϖ

### The Level-Set Functions
**[VASSEUR-YANG]** Identical structure to Vasseur (2007):
- Rising energy levels: cₖ = 1 − 2⁻ᵏ
- Level-set truncations: vₖ = (|v| − cₖ)₊
- Multipliers: βₖ = vₖ/|v|, αₖ = 1 − βₖ
- Indicator: 1ₖ = 1_{Ωₖ} where Ωₖ = {vₖ > 0}

Dyadically shrinking cylinders: Q♭ₖ, Q♮ₖ, Q♯ₖ with radii r♭ₖ = ½(1 + 8⁻ᵏ), etc.

### The Energy Functional
**[VASSEUR-YANG]** (p.19):
$$d_k^2 = \mathbf{1}_k(\alpha_k |\nabla|v||^2 + \beta_k |\nabla v|^2)$$
$$U_k = \|v_k\|^2_{L^\infty(-T_k^\flat, 0; L^2(B_k^\flat))} + \|d_k\|^2_{L^2(Q_k^\flat)}$$

This is exactly analogous to the velocity-based De Giorgi energy.

### The Recurrence Relation
**[VASSEUR-YANG]** From the proof of Proposition 5.1 (p.26):

$$U_k \leq C^k \cdot U_{k-1}^{\min\{4/3,\; 5/3 - 2/(3p_3)\}}$$

where p₃ = (1/p₁ + 1/p₂)⁻¹ > 1, provided U_{k-1} < 1.

**The iteration CLOSES** because: (1) the exponent exceeds 1 (since p₃ > 1 ensures both 4/3 > 1 and 5/3 − 2/(3p₃) > 1), and (2) U₀ is small (Proposition 4.1 gives U₀ ≤ η for arbitrarily small η). This implies Uₖ → 0 as k → ∞, giving |v| ≤ 1 in Q_{1/2}.

---

## 3. What Is the New Bottleneck?

### The 4/3 Exponent: Source

The min{4/3, 5/3 − 2/(3p₃)} in the recurrence has TWO competing terms.

**Term 1: 4/3 — from the interior trilinear form.**

This comes from the highest-order nonlinear term (Section 5.1). The nonlinear coupling in the v equation produces trilinear forms T∇, T◦, T_div. When the interior part (ρ♯ₖ v ⊗ v) of u ⊗ v is handled, the critical estimate (equation 5.6 and surrounding) is:

$$|T_\nabla[\alpha_k v, \rho_k^\sharp \beta_k v, \beta_k v]|, \;|T_{\text{div}}[\beta_k v, \rho_k^\sharp \alpha_k v, (\beta_k+1)v]| \lesssim \|\nabla(\beta_k v)\|_{L^2(Q_{k-1})} \cdot U_{k-1}^{5/6} \leq U_{k-1}^{4/3}$$

The 4/3 arises as 1/2 + 5/6 = 4/3:
- The factor ‖∇(βₖv)‖_{L²} ≤ 3‖dₖ‖_{L²} ≤ 3U_{k-1}^{1/2} contributes the 1/2 (one derivative costs one power of energy)
- The remaining nonlinear factors (two copies of v at the truncation level) contribute U_{k-1}^{5/6} through the nonlinearization Corollary 5.3

**Term 2: 5/3 − 2/(3p₃) — from the lower-order terms.**

This comes from the bilinear terms B (equation 5.7), linear term L (equation 5.8), and the W + W₂ terms (equation 5.9). These are ALL lower-order:
- B (bilinear commutator): ‖ρₖB‖_{L^{p₃}_t L^∞_x} ≤ η → contribution U_{k-1}^{5/3 − 2/(3p₃)}
- L (linear commutator): ‖ρₖL‖_{L^{p₂}_t L^∞_x} ≤ η → contribution U_{k-1}^{5/3 − 2/(3p₂)}
- W (remainders): contribution U_{k-1}^{5/3 − 2/(3p₃)}

When p₃ ≥ 2, the second term ≥ 4/3, so the minimum is 4/3.

### How Does This Compare to the Velocity Bottleneck?

**[INTERPRETATION]** The bottleneck is structurally DIFFERENT from the velocity case:

| | Velocity (Vasseur 2007) | Vorticity (Vasseur-Yang 2021) |
|---|---|---|
| **Source of 4/3** | Pressure term P_k^{21} | Trilinear Riesz operator ∇R(v ⊗ v) |
| **Mechanism** | CZ theory bounds P_k^{21} independently of Uₖ₋₁, giving a k-independent piece | Derivative ∇ costs U^{1/2}; cubic nonlinearity provides U^{5/6} |
| **Nature** | External: pressure couples to velocity via Poisson equation | Internal: nonlinear self-interaction through the Riesz operator |

The pressure bottleneck is GONE. But a new bottleneck of exactly the same numerical strength (4/3) emerges from the nonlinear structure of the equation itself.

### Does Pressure Reappear "Through the Back Door"?

**[INTERPRETATION]** No, in a precise sense. The Riesz operator R(u ⊗ v) = ½ tr(u ⊗ v) − Δ⁻¹ div div(u ⊗ v) is NOT the pressure. Rather, it's a reformulation of the nonlinear advection term. The original NS equation can be rewritten as (equation A.5):

$$\partial_t u + \omega \times u + \nabla R(u \otimes u) = \Delta u$$

where ∇R(u ⊗ u) = ∇(|u|²/2) + ∇P. The ∇R operator combines the kinetic energy gradient and the pressure gradient. When restricted to the v equation, the coupling ∇R(u ⊗ v) retains the same analytical structure (requiring CZ-type estimates for Riesz transforms) but is no longer the NS pressure.

The 4/3 bottleneck from the trilinear form is thus a manifestation of the QUADRATIC nonlinearity of NS itself, not the pressure specifically. The pressure is one way this nonlinearity manifests in the velocity formulation; the Riesz operator coupling is another way it manifests in the vorticity formulation.

---

## 4. What Exponent Do They Achieve?

**[VASSEUR-YANG]** The recurrence exponent is:

$$\beta = \min\left\{\frac{4}{3},\; \frac{5}{3} - \frac{2}{3p_3}\right\}$$

where p₃ > 1. The maximum achievable value (as p₃ → ∞) is **4/3**.

### Crucial Context Difference

**[INTERPRETATION]** However, the 4/3 plays a fundamentally different role here than in Vasseur (2007):

**Vasseur (2007) — velocity approach:**
- Goal: unconditional L^∞ bounds on u from global energy
- U₀ depends on the FULL energy ‖u₀‖²_{L²}, which is NOT small
- Needs β > 3/2 for the iteration to converge when U₀ is O(1)
- Gets β < 4/3 → **FAILURE** (iteration does NOT close)

**Vasseur-Yang (2021) — vorticity approach:**
- Goal: conditional L^∞ bounds on v under local smallness from blow-up
- U₀ ≤ η, where η can be chosen arbitrarily small (Proposition 4.1)
- Needs only β > 1 for convergence when U₀ is small
- Gets β = 4/3 > 1 → **SUCCESS** (iteration closes, gives |v| ≤ 1)

**The same 4/3 is a failure in one context and a success in another.** The blow-up technique converts the problem from "close the iteration with large initial data" to "close the iteration with small initial data." For small data, β > 1 suffices; for large data, β > 3/2 is needed.

---

## 5. Can the Vorticity Approach Prove Regularity?

### What It Does Prove

**[VASSEUR-YANG]** The local theorem gives: under local smallness of ∇u and ω, ALL derivatives ∇ⁿω are bounded in L^∞. The bootstrap proceeds:
1. v is small in energy space (Proposition 4.1, via Grönwall)
2. De Giorgi iteration gives |v| ≤ 1 (Proposition 5.1)
3. ω^{3/4} bounded in energy space (Proposition 6.1(a))
4. ω bounded in energy space (Proposition 6.1(b))
5. All higher derivatives ∇ⁿω bounded in energy space (Proposition 6.2, by induction)
6. Sobolev embedding gives ∇ⁿω ∈ L^∞ for all n

This is full local smoothness. The vorticity approach achieves MORE than the velocity approach: it gives all derivatives, not just L^∞ bounds on velocity.

### What It Doesn't Prove

**[INTERPRETATION]** The local theorem requires the smallness condition (1.5):
$$\|\nabla u\|_{L^{p_1}_t L^{q_1}_x(Q_2)} + \|\omega\|_{L^{p_2}_t L^{q_2}_x(Q_2)} \leq \eta_1$$

This is NOT known to hold at every point for arbitrary initial data. The blow-up argument converts this local condition into a bound on the maximal function, which gives the improved Lorentz space integrability — but NOT unconditional global regularity.

### The Logical Circle

**[INTERPRETATION]** There is no logical circle in the Vasseur (2007) sense (where BKM + L^∞ bounds would close the problem). The Vasseur-Yang approach is a legitimate conditional result: IF you have local smallness THEN you get full smoothness. The question is whether local smallness can be guaranteed everywhere.

If one could prove that the blow-up procedure yields smallness at EVERY point (not just at most points), the Navier-Stokes millennium problem would be solved. This is equivalent to showing the singular set is empty, which is the open problem.

### Comparison with BKM Criterion

The Beale-Kato-Majda criterion states: if ‖ω‖_{L^∞} < ∞ on [0,T), then the solution is smooth on [0,T]. The vorticity-based De Giorgi iteration gives L^∞ bounds on ω, but only LOCALLY and CONDITIONALLY. It does not give global L^∞ bounds unconditionally, so it cannot directly invoke BKM to prove global regularity.

---

## 6. Connection to Beltrami Structure

### Exact Beltrami Flows

**[INTERPRETATION]** For exact Beltrami flows (ω = λu, hence ω × u = 0), the vorticity equation becomes:

$$\partial_t \omega + (u \cdot \nabla)\omega = (\omega \cdot \nabla)u + \Delta\omega$$

But the advection and stretching combine to give:
$$\partial_t \omega + \text{curl}(\omega \times u) = \Delta\omega$$

Since ω × u = 0 for Beltrami flows, this reduces to the HEAT EQUATION:
$$\partial_t \omega = \Delta\omega$$

This is trivially regular. The De Giorgi iteration is unnecessary.

In the v equation (4.4), for Beltrami flows: the ω × v term becomes λu × v = λ(v + w) × v = λw × v (since v × v = 0), which is a lower-order term. The critical trilinear form involving ∇R(u ⊗ v) also simplifies because B = -curl Δ⁻¹(∇φ × (ω × u)) = 0 when ω × u = 0.

### Near-Beltrami Flows

**[INTERPRETATION]** For near-Beltrami flows u = u_B + εv_pert:
- The Lamb vector ω × u enters at O(ε)
- The trilinear bottleneck ∇R(v ⊗ v) enters at O(ε²)
- Both are small when ε is small

The vorticity approach has the SAME favorable properties for Beltrami flows as the velocity approach identified in exploration 006: the nonlinearity simplifies. But this simplification is already captured by the general framework (blow-up gives smallness) rather than requiring separate Beltrami analysis.

### Key Observation for Beltrami

**[INTERPRETATION]** The vortex stretching term (ω · ∇)u, which is the characteristic difficulty of the vorticity equation, simplifies dramatically for Beltrami flows:
$$(ω \cdot ∇)u = λ(u \cdot ∇)u = λ\nabla(|u|^2/2) \quad \text{(pure gradient, for exact Beltrami)}$$

This is absorbed into the pressure-like term ∇R(u ⊗ u). For the v equation, this means the stretching contribution to the trilinear form is a gradient — it does not contribute to the curl-type nonlinearity in ω × v. This is consistent with exploration 006's finding that Beltrami structure eliminates the Lamb vector.

---

## 7. Comparison Table: Velocity vs Vorticity De Giorgi

| Feature | Velocity De Giorgi (Vasseur 2007) | Vorticity De Giorgi (Vasseur-Yang 2021) |
|---|---|---|
| **Level-set quantity** | \|u\| | \|v\| where v = −curl φ♯Δ⁻¹φω |
| **Equation iterated** | NS velocity eq with pressure | Modified v eq (4.4), pressure-free |
| **Bottleneck term** | P_k^{21} (non-divergence local pressure) | Interior trilinear form T∇[αₖv, ρ♯ₖβₖv, βₖv] |
| **β achieved** | < 4/3 | min{4/3, 5/3 − 2/(3p₃)} ≤ 4/3 |
| **β needed for closure** | > 3/2 (unconditional, large U₀) | > 1 (conditional, small U₀) |
| **Does iteration close?** | NO (4/3 < 3/2) | YES (4/3 > 1, with small U₀) |
| **Pressure role** | Direct bottleneck | Absent entirely |
| **Stretching role** | Controlled by Sobolev embedding | Enters through ω × v; contributes to trilinear form |
| **Proves what?** | Partial regularity (singular set has zero 1D Hausdorff measure) | Improved Lorentz space integrability of ∇²u |
| **Unconditional regularity?** | No | No |
| **Requires smallness?** | Not explicitly (uses energy inequality) | Yes (blow-up argument) |
| **Bootstrap to all derivatives** | Not directly | Yes (Propositions 6.1, 6.2) |
| **Local energy inequality** | Standard (for u) | Derived for v (Theorem A.1) |
| **Novel tools** | De Giorgi level-set truncation for NS | v = −curl φ♯Δ⁻¹φ ω; skewed cylinder maximal function |

---

## 8. Assessment for Our Mission

### Grade: C (Instructive negative result)

### Justification

The vorticity-based approach **successfully eliminates the pressure** from the De Giorgi iteration. The P_k^{21} bottleneck, which dominates the velocity approach, is structurally absent. This is a genuine advance — the paper proves that the local theorem "needs nothing from the pressure."

**However, a new bottleneck of exactly the same numerical strength (4/3) emerges from the nonlinear self-interaction** through the Riesz operator term ∇R(u ⊗ v). The 4/3 arises from the fundamental structure of the quadratic nonlinearity: one derivative factor costs U^{1/2} and two nonlinear factors provide U^{5/6}, giving U^{4/3} in total.

### Why This Matters for the Mission

This result has a profound implication: **the 4/3 barrier is NOT specific to pressure.** It reflects a deeper property of the Navier-Stokes nonlinearity itself. When pressure is removed, the same 4/3 reappears from a different source. This strongly suggests that:

1. **No reformulation of NS that preserves the quadratic nonlinearity will improve β beyond 4/3.** The bottleneck is encoded in the product structure of the nonlinearity (one derivative × two velocity-scale factors), not in any specific formulation artifact.

2. **The gap between 4/3 and 3/2 may be fundamental** to the mathematical structure of 3D NS, not an artifact of incomplete estimates.

3. **The blow-up + smallness approach is a viable workaround** — by trading unconditional results for conditional ones, the 4/3 becomes sufficient. But this does not solve the millennium problem.

### What the Paper Does Accomplish

Despite not breaking the 4/3 barrier, the paper achieves significant results:
- First Lorentz space improvement for second derivatives of NS solutions since Lions (1996)
- Pressure-free framework for local NS regularity
- Complete bootstrap from L^p smallness to C^∞ smoothness (locally)
- Novel variable v that provides a pressure-free proxy for velocity

### Viability for β > 3/2

**Not viable.** The 4/3 bottleneck from the trilinear form appears to be as tight as the pressure bottleneck. Without a fundamentally different treatment of the quadratic nonlinearity (not just a reformulation), the 4/3 will persist.

### Possible Paths Forward (Speculative)

1. **Exploit cancellations in the trilinear form** — unlike the pressure bottleneck where CZ theory gives a tight bound, the trilinear form may have structural cancellations that could improve the 5/6 factor. This has not been investigated.

2. **Combine vorticity approach with geometric conditions** — the Beltrami/coherence results from exploration 006 show that geometric structure can improve the effective β. In the vorticity framework, such conditions might be easier to exploit since the stretching term is more directly visible.

3. **Use the full power of the skewed maximal function** — Yang's (2020) maximal function for transport equations is one of the innovations enabling the Lorentz improvement. Further development of this tool might give additional control.

---

## Summary of Key Finding

**The pressure bottleneck (P_k^{21}) is genuinely eliminated in the vorticity-based De Giorgi approach. But the quadratic nonlinearity of Navier-Stokes produces a new 4/3 bottleneck through the interior trilinear form, independent of pressure. The 4/3 appears to be a universal barrier for De Giorgi-type iterations on NS, arising from the fundamental product structure of the nonlinearity: one derivative costs U^{1/2}, and two nonlinear factors at the velocity scale contribute U^{5/6}, giving U^{1/2 + 5/6} = U^{4/3}.**

This is the most important finding of this exploration: the pressure is not the ultimate obstacle. The obstacle is the quadratic nonlinearity itself.

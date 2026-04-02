<!-- explorer-type: standard -->

# Exploration 006: Beltrami-Near Structure and Geometric Conditional Regularity

## Goal

Survey the literature on geometric regularity criteria for Navier-Stokes that exploit velocity-vorticity alignment (Beltrami-near structure). Determine whether this structural property can improve the De Giorgi recurrence exponent β for Beltrami-near flows.

## Background: Why This Matters

DNS measurements of the De Giorgi recurrence exponent (exploration 002) showed a dramatic outlier:

**ABC (Beltrami) flows have beta_eff ~ 1.0 and bottleneck gamma > 1.0 at all Re**, versus beta_eff = 0.35-0.73 and gamma < 1.0 for all other ICs. Specifically:

| IC | Re=1000 beta_eff | Re=1000 gamma |
|---|---|---|
| ABC (Beltrami) | **1.009** | **1.103** |
| VortexTubes | 0.730 | 1.154 |
| TaylorGreen | 0.591 | 0.632 |
| KidaVortex | 0.490 | 0.459 |
| RandomGauss | 0.386 | 0.618 |

The Beltrami property is: curl(u) = λu (velocity is an eigenfunction of curl, so velocity and vorticity are perfectly aligned). ABC flows with A=B=C=1 satisfy this exactly.

**Key observation:** The pressure integral bottleneck (P_k^{21}) that limits β is dramatically better-behaved for Beltrami flows. This suggests that velocity-vorticity alignment provides genuine analytical leverage on the pressure term.

**The regularity threshold** is β > 3/2. Even ABC's best measured value (β_eff ≈ 1.0, gamma ≈ 1.1) is still below 3/2. But the direction is right — understanding WHY Beltrami structure helps could reveal what property of the pressure is needed.

## Required Deliverables

### Geometric Regularity Criteria Literature:

1. **What geometric regularity criteria exist for NS?** Survey the literature on conditions involving the direction of velocity, vorticity, or their alignment that are sufficient for regularity. Key papers to find:
   - Constantin & Fefferman (1993) — direction of vorticity
   - Beirao da Veiga & Berselli (2002) — alignment of velocity and vorticity
   - Chae & Lee (2002), Neustupa & Penel (2001) — related criteria
   - Any post-2010 results on geometric conditions

2. **What EXACTLY do these results prove?** For each result, state:
   - The geometric condition (what alignment/direction assumption is made)
   - The conclusion (regularity of weak solutions? Strong solutions? For all time?)
   - The mathematical mechanism (how does the geometric condition control the nonlinearity?)

### Connection to De Giorgi Framework:

3. **Why does Beltrami structure help the pressure?** For a Beltrami flow (curl u = λu), what happens to the pressure Poisson equation -Δp = -∂_i∂_j(u_iu_j)? Specifically:
   - Does the Beltrami property create cancellations in the pressure source term?
   - Does it reduce the L^q norm of the pressure relative to ||u||²?
   - What happens to the specific bottleneck piece P_k^{21}? Does its source term simplify?

   This is the key question: what STRUCTURAL property of Beltrami flows makes the pressure term better-behaved in the De Giorgi iteration?

4. **Can Beltrami-near structure be inserted into Vasseur's De Giorgi proof?** If the velocity is "ε-close to Beltrami" (meaning ||curl u - λu|| ≤ ε||u|| for some λ), can this be used to:
   - Improve the CZ bound on P_k^{21}? (Probably not, based on exploration 004 — but check whether the STRUCTURE matters even if the CZ CONSTANT doesn't)
   - Provide a better estimate on the bottleneck integral I_k = ∫|P_k^{21}|·|d_k|·1_{v_k>0} dx dt?
   - Change which term is the bottleneck?

5. **Conditional regularity statement.** Can you formulate (or find in the literature) a precise conditional result: "If the velocity field satisfies [Beltrami-near condition], then β > 3/2 (or β > 4/3, or some improvement)"? What is the strongest such statement that can be made?

### Pressure Structure for Beltrami Flows:

6. **Pressure of Beltrami flows.** For exact Beltrami flows (curl u = λu), compute:
   - The nonlinear term u·∇u = ω×u + ∇(|u|²/2) = λu×u + ∇(|u|²/2) = ∇(|u|²/2) (since u×u = 0!)
   - Therefore -Δp = ∇²(|u|²/2) → p = -|u|²/2 + harmonic
   - This means: for exact Beltrami flows, the pressure is fully determined by the velocity magnitude. There is NO nonlinear pressure contribution (the vortex stretching cancels).

   **Verify or correct this calculation.** If correct, it explains why the De Giorgi iteration works so much better for ABC: the pressure source term is trivial.

7. **What breaks for near-Beltrami flows?** If u = u_B + εv where u_B is Beltrami:
   - What are the leading-order corrections to the pressure?
   - At what order in ε does the "bad" P_k^{21} contribution reappear?
   - Is the improvement continuous in ε (gradual degradation) or discontinuous (any perturbation restores the full bottleneck)?

### Assessment:

8. **Viability assessment.** Grade the Beltrami conditional regularity path:
   - (A) Directly viable — a conditional result with clear β improvement can be stated
   - (B) Promising but needs work — the mechanism is real but the formalization is nontrivial
   - (C) Marginal — the improvement is real for exact Beltrami but doesn't survive perturbation
   - (D) Not viable — the mechanism is specific to exact Beltrami and has no conditional generalization

## What to Distinguish

- **[LITERATURE]** vs **[INTERPRETATION]** vs **[COMPUTATION]** — flag every claim
- **Exact Beltrami** vs **near-Beltrami** — the difference is crucial
- **Regularity criteria on the velocity direction** vs **improved De Giorgi exponent** — these are related but different goals

## Success Criteria

✅ **Success:** Deliverables 1-8 answered. The mechanism by which Beltrami structure helps the pressure is identified. The viability of conditional regularity is assessed.

❌ **Failure:**
- The pressure simplification for Beltrami flows (deliverable 6) is wrong → explain why and what the actual pressure structure is
- No geometric regularity criteria exist → highly unlikely but report what was searched
- The connection between geometric criteria and De Giorgi is unexplored in the literature → this is a valuable finding (potential novelty); describe what WOULD need to be proved

## Output Format

Sections matching deliverables 1-8. Use LaTeX notation for equations. Cite specific papers with theorem/equation numbers.

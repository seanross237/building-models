# Sprint 7: Is g₂ RG-Irrelevant? Does the Theory Flow to GR?

**Date:** 2026-03-21
**Status:** FAIL — g₂ does not flow to 0. The pure Pretko theory is Gaussian (no running). The fracton-elasticity duality shows g₂ is stable.

## The Question

Is g₂ (the coupling that controls deviation from GR) irrelevant under RG, so the Pretko theory flows to g₂ = 0 (linearized GR) in the IR?

## Pass/Fail Criteria

- PASS: g₂ is irrelevant, theory flows to GR
- PARTIAL: g₂ is marginal with undetermined sign
- FAIL: g₂ is relevant or does not run at all

## Calculator Result: Argued PASS (but flawed)

The Calculator found:
1. g₂/g₁ is dimensionless (classically marginal) at both z=1 and z=2
2. g₂ = 0 is a fixed point, protected by non-anomalous linearized diffeomorphism symmetry
3. Argued β(g₂) > 0 (marginally irrelevant) by analogy with massive gauge theories (Appelquist-Carazzone decoupling)
4. Concluded the theory flows toward GR

**The Calculator's argument has a critical flaw:** The analogy with massive gauge theories (Proca, QED) applies to INTERACTING theories. The pure Pretko theory is free (Gaussian). The Checker identified this error.

## Checker Result: FAIL (decisive correction)

### Critical Finding: The Pure Pretko Theory Is Gaussian

The Pretko action S = ∫ [(1/2μ)Ė²_ij - (g₁/2)B²_kij - g₂(∂_j A_ij)²] is **quadratic in A_ij**. There are no cubic or quartic vertices in the pure gauge sector. A Gaussian theory does not renormalize — its couplings do not run.

**Therefore g₂/g₁ is exactly constant under RG in the pure theory.** It does not flow toward 0 or away from 0. It stays fixed.

### The Condensed Phase

In the condensed phase, interactions arise from:
- The condensate potential V(A) (polynomial self-interactions)
- Matter coupling (if present)

These interactions DO generate Feynman diagrams and running. But:
- The running of g₂ depends on the specific interaction structure, not on any universal argument
- There is no known mechanism that specifically drives g₂ → 0 through condensate interactions
- The condensate-generated vertices respect the fracton gauge symmetry (δA = ∂²α), NOT the enhanced symmetry (δA = ∂ξ + ∂ξ). So loop corrections from these vertices generically produce g₂ ≠ 0 terms.

### Fracton-Elasticity Duality (Decisive)

Via the Pretko-Radzihovsky duality (2018):
- A_ij ↔ strain tensor u_ij
- g₁ ↔ isotropic elastic moduli
- g₂ ↔ elastic anisotropy

In the elastic dual, g₂ maps to the anisotropy of elastic constants. Under RG (coarse-graining):
- Elastic anisotropy is a **stable** property — crystals don't become isotropic under coarse-graining
- The cubic fixed point in φ⁴ theory (well-studied for N ≥ 3) shows the isotropic point is UNSTABLE to cubic perturbations
- The duality suggests g₂ ≠ 0 is stable, and g₂ = 0 is repulsive (or at best neutral)

### Checker's Verdict

g₂ = 0 is a protected fixed point (non-anomalous enhanced symmetry), but it is **NOT an attractor**. The theory does not flow toward GR from generic initial conditions. Whether GR emerges depends entirely on whether the condensation mechanism selects g₂ = 0 at tree level — which is the gauge enhancement question, and Sprint 3 showed this fails.

## Skeptic Attacks

### FATAL 1: Ghost Kills the Theory During Any Flow
The Afxonidis spin-1 ghost exists at ALL g₂ ≠ 0. Vacuum decay rate ~ M_Pl⁴ (one Planck time). Even if g₂ flows to 0, the theory cannot survive the ghost instability during the flow. The ghost disappears only AT g₂ = 0, but the theory must pass through g₂ ≠ 0 to get there.

### SERIOUS 2: Logarithmic Running Too Slow
Even if g₂ were marginally irrelevant, the decoupling scale is μ ~ M_Pl × exp(-16π²/g₂(Λ)) ~ 10⁻⁵⁰ GeV. Extra DOF would be active at all experimentally accessible energies.

### FATAL 3 (conditional): Non-Renormalizability
If the interacting theory is non-renormalizable, infinitely many couplings are generated, and g₂ is just one. Even if g₂ flows to 0, other couplings can reintroduce the same problems.

### SERIOUS 4: Elasticity Duality Shows g₂ Is Stable
Same as Checker's finding. The cubic anisotropy fixed point (N ≥ 3 in φ⁴ theory) is the IR attractor, not the isotropic point.

### CONCERN 5: g₂ = 0 Is Measure-Zero in Parameter Space
Among UV completions (lattice fracton models), g₂ = 0 requires continuous diffeomorphism invariance that no lattice has.

## Synthesis: FAIL

### What Sprint 7 Established

1. **The pure Pretko theory is Gaussian — g₂ does not run.** This is the decisive result. Without interaction vertices, there are no loops, no running, and no RG flow toward GR.

2. **g₂ = 0 is a protected fixed point but NOT an attractor.** The enhanced gauge symmetry (linearized diffeos) is non-anomalous, so g₂ = 0 is stable once reached. But generic initial conditions with g₂ ≠ 0 do not flow there.

3. **The fracton-elasticity duality shows g₂ is stable.** Elastic anisotropy does not flow to isotropy. By duality, g₂ does not flow to 0.

4. **The ghost problem is dispositive.** At any g₂ ≠ 0, the spin-1 Hamiltonian is unbounded below. The vacuum decays in one Planck time. No RG flow can save a theory whose vacuum doesn't exist.

5. **GR from FDCG requires g₂ = 0 to be selected by the condensation mechanism.** This is exactly the gauge enhancement question — and Sprint 3 proved it fails.

### The Circle Is Complete

Sprint 7's conclusion connects back to Sprint 3:

- Sprint 3: Gauge enhancement (getting g₂ = 0 from condensation) FAILS
- Sprint 7: RG flow (getting g₂ → 0 from dynamics) FAILS
- Both routes to g₂ = 0 are closed

The only way to have g₂ = 0 is to impose it by hand — which is not "emergent" GR but assumed GR.

## FDCG as Emergent GR: Terminal Verdict

After 7 sprints (0 PASS, 2 PARTIAL, 5 FAIL), every mechanism for recovering GR from the Pretko rank-2 symmetric tensor gauge theory has been eliminated:

| Mechanism | Sprint | Result |
|-----------|--------|--------|
| Gauge enhancement | 3 | FAILS |
| Mass decoupling (potential) | 4 | FAILS (Schur's lemma) |
| Derivative interactions | 5 | FAILS (vanish at k=0) |
| Radiative corrections | 5 | FAILS (Schur at all loops) |
| Nematic condensation | 6 | FAILS (wrong Goldstones) |
| RG flow of g₂ | 7 | FAILS (Gaussian theory, no running) |

**The Pretko rank-2 symmetric tensor gauge theory cannot produce emergent GR by any known mechanism.**

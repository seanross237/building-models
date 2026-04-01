---
topic: constraints/recovery
confidence: verified
date: 2026-03-24
source: exploration-001-structural-recovery-constraints
---

# Graviton Propagator IR Matching (Constraint B3)

**Statement:** The full dressed graviton propagator must reduce to the GR propagator at momenta far below the Planck scale: G(p²) → (P^(2) - ½P^(0))/(p² + iε) as p² → 0.

**Mathematical form:**
- At low momenta: G_TT(p²) ~ Z/p² with Z > 0 (positive residue = no ghost)
- The two running gravitational couplings (from the spin-2 and spin-0 sectors) must converge to the same value G_N in the IR

**Restrictiveness: HIGH**

This is stronger than just Newtonian gravity — it fixes the full tensor structure including the relative coupling of the spin-0 component.

## Subsumes Weaker Constraints

**Newtonian gravity (B1):** V(r) = -G_N M / r + O(r^{-2}) corrections. Single graviton exchange in the Born approximation yields Fourier transform of 1/|q|² → -1/r potential. G_N = κ²/(32π). Most theories satisfy this by construction.

**Linearized Einstein equations (B2):** □h̄_μν = -16πG T_μν (Lorenz gauge). The graviton propagator in the IR takes the form G_μναβ(q) = (P^(2)_μναβ - ½ P^(0)_μναβ) / q². Automatically satisfied if diffeomorphism invariance is maintained. Fixes the tensor structure, not just the 1/q² falloff.

## Verification Across Approaches

- **Asymptotic Safety:** Bonanno et al. (2022) verified that the dressed graviton propagator's two tensorial components have "non-trivial yet equal residues at the massless pole."
- **LQG:** The graviton propagator computed from spin foam models has been shown to have "the correct large-distance asymptotics nonperturbatively and independently of the spin foam model used."

## Dependency

Genuinely independent. Newtonian gravity (B1) and linearized Einstein equations (B2) are derived from this constraint.

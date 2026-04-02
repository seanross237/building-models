# Exploration 001 Summary: Classical Eigenvalue Concavity/Convexity Theorems

## Goal
Survey the classical mathematical literature on eigenvalue concavity/convexity (Davis-Lewis, Ando, Löwner, matrix convexity, Fan/Weyl) and assess applicability to proving λ_max(H(Q)) has a global max at Q=I for H(Q) a Hermitian matrix-valued function on SU(N)^E.

## What Was Tried
Web literature survey covering: Davis 1957 (convex invariant functions), Lewis 1996 (spectral functions), Ando 1979 (concavity on positive definite matrices), Löwner 1934 (operator monotone characterization), Fan 1951 (eigenvalue sums convexity), Weyl 1912 (perturbation bounds), Kostant 1973 (compact group orbit projection), AGS 1982 (moment map convexity), and two 2024 papers (unitary eigenvalue convexity, geodesic convexity of eigenvalue problems). Also searched for any applications to lattice gauge theory.

## Outcome
**Succeeded** — clear catalog of ≥8 major theorems with precise statements, domains, and applicability assessments. The landscape is now well-mapped.

## Key Takeaway

**The classical literature has a fundamental domain gap: all major theorems (Davis, Lewis, Ando, Löwner, Fan, Weyl) operate on H_n as a VECTOR SPACE or H_n^{++} as an open cone. None directly address λ_max(H(Q)) as a function on a compact group SU(N)^E.**

Moreover, even on vector spaces, λ_max is **CONVEX** (it is the max of linear functions), not concave. The classical results give the wrong direction for proving a global maximum.

The two results closest to our setting are:
1. **arXiv:2408.16906 (2024):** "Convexity of sums of eigenvalues of a segment of unitaries." Shows that the sum of the top m eigenvalue phases θ₁+...+θ_m of u(t) = e^{itx}e^{iy} is **convex** as a function of t, provided ‖u(t)-I‖ < √2. This is LOCAL convexity of eigenvalue sums of the GROUP ELEMENT near identity — it gives the RIGHT domain (compact group) but the WRONG direction (convexity, not concavity of λ_max∘H) and the WRONG object (eigenvalues of u itself, not of a derived matrix H(Q)).
2. **Kostant/AGS convexity theorems:** These give convexity of PROJECTIONS of orbits or moment map images — not of λ_max(H(Q)) as a scalar function.

## Critical Observation

The 2024 unitary result shows eigenvalue sums are convex (not concave) near identity. This is consistent with the existing numerical falsification of global concavity: global concavity fails because paths that leave the ‖u-I‖ < √2 neighborhood see different behavior. But locally near I, the eigenvalue function is convex (in the eigenvalue-sum sense), which is the OPPOSITE of what's needed.

**The right path forward is not "prove full concavity" (already falsified) but:**
1. Prove LOCAL concavity at Q=I via direct second-variation/Hessian analysis of λ_max∘H specifically (this is separate from generic eigenvalue theory)
2. Prove no other local max exists (topological/structural argument)
3. Perhaps exploit the plaquette-sum structure of H(Q) to find restricted concavity along specific directions

## Leads Worth Pursuing

1. **Second-variation analysis of λ_max(H(Q)) at Q=I** — this is not covered by classical eigenvalue convexity theory but is directly computable. Local negative-definiteness of the Hessian of λ_max∘H at Q=I would establish local concavity.

2. **Restricted concavity along gauge orbits** — if H(Q) is gauge-covariant, eigenvalue functions may be concave along gauge orbit directions (they would be constant along gauge orbits if H is gauge-invariant). This would restrict the optimization to the moduli space.

3. **Schur-Horn/Kostant applied to plaquette structure** — the sum-of-plaquettes structure of H(Q) might allow a Schur-Horn type argument that eigenvalues of H(Q) are always dominated by eigenvalues at Q=I, i.e., λ(H(Q)) ≺ λ(H(I)) in majorization order. This would give λ_max(H(Q)) ≤ λ_max(H(I)) directly. Worth exploring.

4. **The 2024 paper arXiv:2408.16906** deserves more attention — its proof technique (second-variation formula for eigenvalue phases of unitary matrices) might be adaptable to eigenvalues of H(Q) if H(Q) has a specific form.

## No Applications to Lattice Gauge Theory Found
Search found no papers applying these classical theorems to Yang-Mills Hessians or eigenvalue functions on SU(N)^E. This is a genuine gap in the literature.

## Unexpected Findings

1. **Convexity, not concavity, near identity in the unitary group** — The 2024 result reveals that the "natural" behavior of eigenvalue sums near the identity is convexity, not concavity. This is surprising: it means the flat connection Q=I is not a local max in the eigenvalue-sum sense — it's locally a min or saddle. This seems to CONTRADICT the known numerical finding that Q=I is a local max of λ_max(H(Q)). The resolution must be that H(Q) is NOT the same as the eigenvalue function of Q — it is a derived matrix with different curvature behavior.

2. **Counterexample to prior claim of gap-independent convexity (2024)** — A prior claim that geodesic convexity of the eigenvalue problem is gap-independent was shown to be WRONG in the 2024 Geodesic Convexity paper. This suggests one should be skeptical of any "clean" global geodesic convexity/concavity claims in this area.

## Computations Identified

1. **Direct second-variation of λ_max(H(Q)) at Q=I** — Compute d²λ_max(H(Q(t)))/dt²|_{t=0} for all geodesics Q(t) through I. If always negative, Q=I is a local max. This requires the explicit formula for H(Q) (the Yang-Mills Hessian at flat connection). Moderate difficulty (10-30 lines of scipy/sympy for the SU(2) case). Inputs: The Weitzenbock formula / D+C decomposition of the Hessian at Q=I from the library.

2. **Majorization test: λ(H(Q)) ≺ λ(H(I)) for all Q?** — If the eigenvalues of H(Q) are always majorized by those of H(I), then λ_max(H(Q)) ≤ λ_max(H(I)) and we'd have a direct proof. This is a concrete numerical experiment: compute H(Q) for many random Q ∈ SU(2)^E and check majorization. Easy to compute, decisive if true.

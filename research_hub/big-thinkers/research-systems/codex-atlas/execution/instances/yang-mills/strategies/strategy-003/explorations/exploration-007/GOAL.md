# Exploration 007: Prove M(Q) ≼ M(I) via Pure Gauge Orbit + Convexity Argument

## Mission Context
This is a YANG-MILLS mission (strategy-003). Do not confuse with other missions.

## Background

**Target:** M(Q) ≼ M(I) for all Q ∈ SU(N)^E (positive semidefinite operator inequality).

**Phase 1 structural insights:**
1. **Pure gauge characterization** (E002): λ_max(M(Q)) = 4d iff Q is pure gauge. Non-pure-gauge has λ_max < 4d.
2. **Isometry for pure gauge** (E006 Task 2 analytical argument): For pure gauge Q_e = g_{s(e)} g_{t(e)}⁻¹, the map v → ṽ = Ad_{g⁻¹} v is an isometry satisfying M(Q_pure) = Ad_{g}^T M(I) Ad_{g} (isospectral with M(I)).
3. **Non-pure-gauge has smaller M** (E002): 500 random non-pure-gauge Q all satisfy λ_max(M(Q)) < 4d.
4. **B_P chain broken** (E004): Must use direct spectral approach, not per-plaquette bounds.
5. **Corrected B_□ formula** (E001/E002): GOAL.MD had errors. The correct formula has transport INCLUDING the backward edge holonomy.

**Convention:** S = -(β/N) ∑_□ Re Tr(U_□), |A|² = -2Tr(A²). β = 1.0.

## The Proof Structure

We want to prove: for any Q ∈ SU(N)^E and any v ∈ ⊕_e su(N):

  ∑_□ |B_□(Q,v)|² ≤ ∑_□ |B_□(I,v)|² = ∑_□ |ω_□(v)|² ≤ 4d|v|²

where B_□(I,v) = ω_□(v) = discrete curl (proved ≤ 4d|v|² by E004 Fourier theorem).

So it suffices to prove: **∑_□ |B_□(Q,v)|² ≤ ∑_□ |ω_□(v)|²** for all Q, v.

In operator form: M(Q) ≼ M(I).

## Approach: Gauge Orbit + Maximum Principle

**Key insight from E002:** Q=I is the maximum of F(Q) = λ_max(M(Q)) among all Q on the gauge orbit of I (trivially: the gauge orbit of I is all pure gauge configurations, and they all achieve F = 4d). For non-pure-gauge Q, F(Q) < 4d.

**Proposed proof strategy:**

Step 1: Show that Q=I is the maximum of F(Q) = λ_max(M(Q)) on SU(N)^E.

Step 2: Claim: F(Q) is DECREASING along the gradient flow of the Wilson action S(Q). Specifically:
  d/dt F(Q_t) ≤ 0 along the flow dQ_{x,μ}/dt = -∇_{Q_{x,μ}} S

If true, and if the gradient flow converges to the pure gauge manifold (which minimizes S), and pure gauge has F = 4d, then for all Q in the starting configuration, F(Q) ≤ 4d = F(I).

Wait — this gives F(Q) ≤ F(I) = 4d (the maximum over pure gauge), which is exactly what we want!

### Approach A: Gradient Flow Monotonicity

**Claim:** Along the gradient flow Q_t of -S (i.e., heat flow), F(Q_t) = λ_max(M(Q_t)) is monotone decreasing.

**Evidence:** At Q=I, dF/dt = 0 (critical point). Moving AWAY from I increases S... wait, Q=I minimizes S, so the gradient flow moves TOWARD Q=I. Let me reconsider.

Actually: S(Q) is minimized at pure gauge configurations. The gradient flow dQ/dt = -∇S moves toward pure gauge. If F is maximized on pure gauge and decreasing as we move away from pure gauge, then:
- Starting from pure gauge: F = 4d and gradient flow keeps us there (it's a minimum of S)
- Starting from general Q: gradient flow moves toward pure gauge where F = 4d

This would mean F(Q_t) INCREASES toward 4d along the gradient flow, not decreases. We need F(Q) ≤ 4d for all Q, not just the pure gauge configurations.

Hmm, let me re-examine. Actually: we want to show F(Q) ≤ 4d for ALL Q, not just for Q near pure gauge.

The key: does there exist any non-pure-gauge Q with F(Q) > 4d? E002 found 500 random non-pure-gauge Q all have F < 4d. So empirically F ≤ 4d everywhere.

### Approach B: Direct Proof via Plaquette Holonomy Bound

**Structural observation:** For each plaquette □, B_□(Q,v) = ∑_e s_e Ad_{P_{□,e}}(v_e) where s_e = ±1 is the orientation and P_{□,e} ∈ SU(N) is the partial holonomy from link e's base to a fixed basepoint.

The key: at Q=I, B_□(I,v) = ∑_e s_e v_e (no adjoint rotation, since P_{□,e} = I). For Q≠I, the Ad_{P_{□,e}} rotates v_e.

**Lemma attempt:** For each plaquette □ and tangent vectors (v_e)_{e∈□}:

  |∑_e s_e Ad_{P_e}(v_e)|² ≤ |∑_e s_e v_e|²

for all P_e ∈ SU(N) when the vectors v_e are drawn from the staggered mode v_stag.

This would follow if: the alignment of the staggered mode is MAXIMALLY aligned at Q=I, and any rotation can only decrease alignment.

**Key observation from E003:** The staggered mode has the property that the vectors v_{x,μ} all point in the SAME color direction (scaled by (-1)^{|x|+μ}). The discrete curl of this staggered mode at Q=I achieves |B_□|² = 4|v₀|². For Q≠I, the adjoint rotations Ad_{P_e} rotate these vectors away from their common direction, DECREASING the magnitude of the sum.

**Your task:** Formalize this argument. Show that for the staggered mode and general Q:

  |B_□(Q, v_stag)|² ≤ |ω_□(v_stag)|² = 4|v₀|²

by showing that the adjoint rotations reduce the sum.

### Approach C: SU(2)-Specific Identity

For SU(2), the adjoint representation is 3-dimensional real (so(3)). The Cauchy-Schwarz inequality and special properties of SO(3) might give a direct bound.

**For SU(2):** Each Ad_{P_e} ∈ SO(3) is a rotation. The sum ∑_e s_e Ad_{P_e}(v_e) can be bounded using:
  |∑_e s_e Ad_{P_e}(v_e)|² ≤ (∑_e |v_e|²) × max_unit_vectors |∑_e s_e R_e u_e|²

where R_e ∈ SO(3). The maximum of |∑_e s_e R_e u_e|² over all R_e ∈ SO(3) and unit vectors u_e is at most (∑_e 1)² = 16 per plaquette (4 links per plaquette, each contributing at most 1). But this gives the weak bound 16 = 4² which equals the SZZ bound, not our tighter bound.

Can we use the sign pattern s_e = (+1,+1,-1,-1) to get a tighter bound of ≤ 4 per plaquette (instead of ≤ 16)?

**Key:** ∑_e s_e = 0 (two positive, two negative). This cancellation is the key feature of the discrete curl. For SU(2), since ∑_e s_e = 0, there might be a symmetry argument showing |∑_e s_e Ad_{P_e}(v_e)|² ≤ C × max_e |v_e|² for some C < 16.

### Approach D: Direct Computation for L=2 Full Lattice

For L=2, SU(2), d=4: there are 64 links and 96 plaquettes. The operator M(Q) is a 192×192 matrix. Compute:
  M(Q) - M(I) = ∑_□ [B_□(Q) B_□(Q)^T - ω_□ ω_□^T]
for several specific Q configurations and check whether ALL eigenvalues of M(Q)-M(I) are ≤ 0.

**Note:** E006 does this numerically. Your task is to find an ANALYTICAL reason.

## Required Elements

1. **Analytical proof of B_□ decrease under rotation** (for any approach that works). Show that the adjoint rotations Ad_{P_e} reduce |B_□|² for the specific configurations that matter.

2. **Pure gauge orbit argument.** Prove that for pure gauge Q, M(Q) = M(I) (up to isometry). Then show that any non-pure-gauge Q "decoherently" reduces M(Q).

3. **Worked example.** For Q_{0,0} = exp(ε τ₁) (single-link excitation), compute M(Q) - M(I) explicitly for small ε and show it's negative semidefinite. E003 found cos(ε) suppression for this case — formalize this calculation.

4. **Literature search:** Look for:
   - "Lindblad operator" or "quantum channel" bounds on ∑ Ad_{P_e} — these might give a group-theoretic bound
   - "Matrix convexity" of the function Q → M(Q) on a compact Lie group
   - Any proof that "gauge transport decreases curl magnitude"

## Success Criteria

**Full success:** A proof (even partial) that M(Q) ≼ M(I) using the pure gauge characterization + one of the approaches above.

**Partial success:** A proof that |B_□(Q, v)|² ≤ |ω_□(v)|² per plaquette for the STAGGERED MODE v_stag (this would be enough for our purposes since H_norm is maximized at v_stag).

**Useful failure:** Clear identification of why all three approaches fail, with the minimal additional ingredient needed.

## Output Format

Write REPORT.md section by section:
1. Setup: M(Q) ≼ M(I) structure and pure gauge isometry
2. Approach B: Staggered mode bound per plaquette
3. Approach C: SU(2)-specific identity
4. Approach D: Single-link worked example
5. Literature findings
6. Summary

Write REPORT-SUMMARY.md (1 page): What was proved? What remains?

## Notes
- This is a MATHEMATICAL PROOF task.
- Write after completing each section.
- Focus on Approach B (staggered mode) first — it's the most concrete.
- The pure gauge isometry argument (Task 2 of E006) should be written here as well if E006 hasn't produced it.

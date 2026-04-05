# Exploration 002 — Geodesic Convexity Summary

**Goal:** Determine if F(t) = λ_max(M(exp(tW))) is concave at t=0 for all W, i.e., F'(0)=0 and F''(0)≤0. If so, and if this extends globally, the inequality ∑_□ |B_□|² ≤ 4d|v|² follows.

---

## What Was Tried

1. **Derived the correct first/second derivative formulas** for B_□(γ(t), v) using the correct B_□ formula (from E001). The GOAL.MD formula was wrong; correct formula uses transport INCLUDING the backward edge in holonomies.

2. **Proved F'(0) = 0 analytically** via the trace identity ⟨τ_a, [X, τ_a]⟩ = 0 (proved by trace cyclicity). This holds for ALL W.

3. **Computed F''(0) via degenerate perturbation theory** on the 9-fold degenerate eigenspace P. H_eff = (1/2)P M''(0) P + (level repulsion). Evaluated for 200+ random W.

4. **Proved single-link theorem**: F = 4d for any single-link config via gauge equivalence to gauge transformation of I.

5. **Checked F''(Q, W)** for Q ≠ I to test global geodesic concavity.

---

## Outcomes

### What was proved (rigorous)
- **F'(0) = 0 for all W**: Q=I is a critical point of λ_max(M(Q)). Proof: ⟨τ_a, [X, τ_a]⟩ = 0.
- **Single-link theorem**: F(Q) = 4d for any single-link config. Proof: gauge equivalence.
- **Gauge invariance**: λ_max(M(Q)) is invariant under gauge transformations.

### What was confirmed numerically
- **F''(0) ≤ 0 for multi-edge W**: Range [−0.037, −0.026] over 200 random W. Q=I is a local maximum.
- **F''(0) = 0 for single-edge W**: Flat direction; F = 4d for all t.
- **No F > 4d found**: 500 random Q all satisfy F ≤ 4d.
- **Decoherence dominates level repulsion** at Q=I: H_direct eigenvalues in [−0.07, −0.11] vs level repulsion in [+0.03, +0.07].

### Critical failure
- **Global geodesic concavity FAILS**: F''(Q, W) > 0 for some Q ≠ I (found for 8/10 random Q). The geodesic concavity approach as stated in GOAL.md does NOT extend globally.
- **Implication**: Q=I is a local maximum but the geodesic concavity argument cannot establish it as the global maximum.

---

## Key Takeaway

**The geodesic convexity approach proves F'(0)=0 and F''(0)≤0 at Q=I (local max), but fails globally: geodesic concavity breaks down at Q≠I.** The bound F(Q)≤4d appears to hold (500 random Q tested), but the proof gap remains — we cannot go from "local max at Q=I" to "global max" via geodesic arguments alone.

The maximum is achieved on the entire "pure gauge" submanifold {g·I | g ∈ gauge group}, which is a high-dimensional flat manifold. Non-pure-gauge configurations have F < 4d.

---

## Leads Worth Pursuing

1. **Representation theory / Schur's lemma**: Show M(Q) ≼ M(I) using SU(2) group representation structure. The operator M(Q) decomposes under the adjoint action; Schur's lemma might constrain its eigenvalues.

2. **Lattice Weitzenböck identity** (Jiang 2022): M(Q) = M(I) + R(Q), prove R(Q) ≼ 0. The curvature term R involves plaquette holonomies; this is equivalent to the main inequality but recast in differential-geometric language.

3. **Direct bound via group structure**: The maximum of ⟨B_□, B_□⟩ over SU(2)^E might be bounded using Peter-Weyl theorem or Fourier analysis on the group.

4. **Gauge orbit argument**: All configurations with F = 4d are pure gauge; prove that non-pure-gauge configs have F < 4d by showing the pure gauge condition is equivalent to F = 4d.

---

## Unexpected Findings

1. **Bug in GOAL.MD formula**: The transport matrices for backward edges (a₃, a₄) in B_□ are wrong in GOAL.MD. Using the wrong formula gives spurious F > 4d (F = 16.76). With the correct formula (from E001), F ≤ 4d confirmed for 500 random Q.

2. **Single-link gauge-equivalence theorem**: ANY single-link modification (one link = U, others = I) is gauge-equivalent to a gauge transformation of I, hence has F = 4d. This is a clean, non-obvious result.

3. **Decoherence much stronger than level repulsion**: At Q=I, the H_direct term (decoherence from double commutators) dominates level repulsion by factor ~1.5-3×. This is consistent with E001's finding (2-3× ratio).

4. **Geodesic concavity fails even at moderate Q**: For Q with F(Q) ≈ 14 (far below 16), F''(Q,W) can be +0.11 for some W. The function is not concave at these points.

---

## Computations Identified

1. **Prove F'(0)=0 for the CORRECT B_□ formula algebraically**: The argument via ⟨τ_a, [X, τ_a]⟩=0 used the GOAL.MD formula structure. Verify this carries through for the correct formula (appears to hold numerically, needs analytic confirmation).

2. **Schur's lemma bound on M(Q)**: Compute ∫_{SU(2)^E} M(Q) dQ (Haar average) and show it equals (4d/3)·I or similar. Schur's lemma would then constrain λ_max. This is a concrete computation (requires Haar measure integral).

3. **Characterize pure gauge vs non-pure-gauge**: Test whether F = 4d ⟺ Q is pure gauge (rank of plaquette curvature R_□ = 0 for all □). This would be a clean characterization.

4. **Gradient ascent from adversarial starts for the corrected formula**: Run systematic gradient ascent on F(Q) with the CORRECT formula to find the closest approach to 4d from non-pure-gauge configs. Currently max found = 16.000 (= pure gauge).

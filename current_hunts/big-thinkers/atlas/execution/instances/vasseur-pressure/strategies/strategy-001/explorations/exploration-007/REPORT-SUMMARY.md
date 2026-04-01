# Exploration 007 Summary: Beltrami Deficit + Hessian/Lamb Decomposition

## Goal
Determine whether the Beltrami conditional regularity mechanism (identified in Exploration 006) survives the De Giorgi truncation u_below = u·min(1, λ_k/|u|).

## Outcome: SUCCESS — Mechanism Survives

**Task A (Beltrami deficit):** For ABC flows, B_k = ||curl(u_below) − λ_opt·u_below||/||u_below|| ≈ 0.56 × 2^{−k}. The deficit vanishes geometrically with k. For Taylor-Green and random Gaussian controls, B_k ≈ B_full ≈ 3–12 (constant, large). The truncation preserves Beltrami structure for ABC while having no effect on non-Beltrami flows.

**Task B (Pressure decomposition):** The pressure P_k^{21} decomposes as P_hessian + P_remainder where P_hessian = −|u_b|²/2 (Bernoulli, CZ-lossless). For ABC: the remainder contributes only 4.4% of the bottleneck integral at k=4 and 0.2% at k=8. For controls: remainder fraction > 100% (massive Hessian/remainder cancellation, R_frac = 1.2–1.7).

**Critical finding:** The truncation breaks div-free (||div(u_below)|| = O(2^{−k})), invalidating the standard Hessian/Lamb identity. But the pressure remains Bernoulli-dominated regardless — the Beltrami property is geometrically robust.

**All ABC results are Re-independent** (correct: ABC decays self-similarly, L∞-normalized pattern is invariant). The mechanism is not a low-Re artifact.

## Verification Scorecard
- **[COMPUTED]:** 8 claims (B_k scaling, R_frac scaling, bottleneck ratios, Re-independence, div violation, control behavior)
- **[CHECKED]:** 1 (Re-independence cross-checked across Re=100/500/1000 + sanity check at t=0)
- **[VERIFIED]:** 1 (sign convention verified by sanity check: exact Beltrami at t=0 gives R_frac → 0)
- **[CONJECTURED]:** 0

## Key Takeaway
The De Giorgi truncation preserves Beltrami structure with deficit O(2^{−k}), and the resulting pressure is > 95% Bernoulli at k≥4. This removes the CZ bottleneck from the De Giorgi iteration for Beltrami flows, enabling β_eff to approach the geometric limit 5/3 instead of being CZ-capped.

## Proof Gaps
- The O(2^{−k}) scaling of B_k is observed numerically but not proved analytically. A pointwise analysis of how the truncation interacts with the curl eigenvalue equation would close this.
- The connection from "small remainder fraction" to "improved β_eff" needs the full CZ-split argument made rigorous.

## Unexpected Findings
- Truncation breaks incompressibility: div(u_below) ≠ 0. This was not anticipated and invalidates the standard Hessian/Lamb/compressibility three-way split. The two-way Bernoulli/remainder split is the correct approach.
- A sign error in the pressure Poisson solve (missing minus sign) was present in prior exploration code (exploration-002/004). It doesn't affect |P| measurements but matters for signed decompositions.

## Computations Identified
- Prove B_k = O(2^{−k}) analytically for Beltrami flows
- Test perturbed ABC (ABC + noise) to measure how B_k degrades with departure from exact Beltrami
- Compute β_eff directly with the CZ-split applied (replace ||P_k^{21}|| with ||P_hessian|| + C_q||P_remainder||)

# Strategy 002: Close the 9D Eigenspace Gap

## Objective

Prove Conjecture 1 for the full 9-dimensional top eigenspace, completing the proof that lambda_max(M(Q)) <= 16 for all Q in SU(2)^E on the d=4, even-L hypercubic torus.

Strategy 001 proved this for the 3D uniform-color subspace of P (staggered modes with fixed color direction n). The remaining gap: 6 direction-dependent modes where color varies with spatial direction mu.

**This strategy has ONE target:** prove (or find an obstruction to proving) the per-vertex bound

  F_x(Q, T) = sum_{mu<nu} |B_{(x,mu,nu)}(Q, v)|^2 <= 16 ||T||^2

for all 4x3 matrices T with constraint sum_mu T_mu = 0, where v_{x,mu} = (-1)^{|x|+mu} T_mu.

## What's Already Proved (DO NOT REDERIVE)

### The Combined Bound Lemma (Strategy 001, E006 — PROVED)

For any A, B, D in SO(3) and unit n in R^3:
  f(A) + f(B) + f(AD) + f(DB^T) - f(D) - f(ADB^T) >= 0
where f(R) = 1 - n^T R n.

Proof: LHS = n^T(I-A)D(I-B^T)n + f(A) + f(B), then Cauchy-Schwarz + AM-GM.

### The Cube-Face Inequality for Uniform Color (Strategy 001, E006 — PROVED)

For uniform-color staggered mode v = (-1)^{|x|+mu} n:
  n^T M_total n <= 64|n|^2  (equivalently, 64I - M_total >= 0 as 3x3 matrix)

Proof: trace identity c + Tr(P) = 64, expansion 64I - M = 2[group_02 + group_13 + group_active], each group >= 0 by Combined Bound Lemma.

### Key Facts About the Gap (Strategy 001, E007-E008)

1. The per-vertex contribution F_x for general modes involves a 12x12 matrix M_12, restricted to V = {T : sum_mu T_mu = 0} (9-dim).
2. The constraint sum_mu T_mu = 0 is ESSENTIAL (without it, eigenvalue reaches ~21).
3. Maximizing T is NOT always rank-1 (min rank-1 fraction = 0.56 at adversarial maxima).
4. Harmful cross-color term < 8.2% of f_same — enormous safety margin.
5. The E006 trace identity FAILS for general spatial patterns. Cannot use trace arguments.
6. 110K+ numerical tests, max lambda = 15.997/16 (0 violations).
7. 350+ adversarial gradient ascent trials converge below 16.

## Methodology: Focused Parallel Attack

This is a single-gap-closure strategy. The gap is precisely characterized, the safety margin is enormous (8.2% cross-term vs 100% budget), and the target is a concrete matrix inequality. The methodology is designed accordingly.

### Phase 1: Two Parallel Technique Explorations (2 explorations, run in parallel)

Each exploration must:
- Be a math explorer
- Compute F_x for 100+ random Q with general T (not just uniform color) FIRST
- Verify the 8.2% cross-term ratio independently
- Identify whether the technique can close the gap
- State the exact sub-inequality that would suffice for a proof

**Exploration A: SDP / Sum-of-Squares Certificate**

The problem: for fixed Q, F_x(Q, T) is a quadratic form in the 9-vector of independent T entries (after eliminating T_4 = -T_1 - T_2 - T_3). So F_x <= 16||T||^2 is equivalent to a 9x9 matrix inequality.

Task: For 50+ random Q, compute the 9x9 matrix M_9(Q) = M_12|_V and verify lambda_max(M_9) < 16. Then: can we write 16I_9 - M_9(Q) as a sum of squares (SOS) in the rotation parameters? Specifically:
1. Parametrize the 10 SO(3) matrices (4 base links R_mu, 6 cross-links D_{mu nu}) as functions of angle-axis coordinates.
2. For each vertex, write 16I_9 - M_9 symbolically.
3. Check if it has an SOS decomposition using the algebraic structure.
4. If not globally, check if it has an SOS decomposition modulo the SO(3) constraint (R^T R = I).

**Exploration B: Block Extension of Combined Bound Lemma**

The Combined Bound Lemma works for scalar f(R) = 1 - n^T R n. The 9D problem needs a MATRIX version: F(R) = I_3 (x) I_3 - something involving R.

Task:
1. Write F_x(Q, T) = sum_{mu<nu} ||A_{mu nu} vec(T)||^2 where A_{mu nu} are matrices depending on Q. Express this as T : M_12 : T (Frobenius inner product).
2. Decompose M_12 into blocks: same-color (mu=nu color index) and cross-color (mu!=nu). The same-color blocks reduce to the proved uniform-color case.
3. Bound the cross-color blocks. The key question: can the cross-color terms be absorbed by the same-color surplus (which is large — the 8.2% ratio)?
4. Specifically: if 16||T||^2 - F_same >= epsilon ||T||^2 for some epsilon > 0, and |F_cross| <= delta ||T||^2 with delta < epsilon, then F_x <= 16||T||^2. Compute epsilon and delta numerically.

### Phase 2: Proof Construction + Adversarial (3-4 explorations, sequential)

**Exploration 3: Synthesis**
Read both Phase 1 reports. Identify which technique is closer to a proof. Write the proof outline. Identify the single hardest remaining step. This MUST be a standard explorer (reading + reasoning, not computation).

**Exploration 4: Focused proof attempt**
Attack the hardest step identified by E3. Math explorer. ONE approach only (whichever E3 recommends). If the synthesis says neither technique works, this exploration should try a THIRD technique: direct representation theory using the constraint sum_mu T_mu = 0 as a projection onto the irreducible component.

**Exploration 5: Adversarial review**
Math explorer. Independent verification of the proof from E4. Try to break it. Gradient ascent on lambda_max(M_9) for 500+ configs. Check all claimed inequalities.

**Exploration 6 (if needed): Repair or alternative**
Only launch if E5 finds a gap. If the proof is confirmed, skip E6 and write the final report.

### Phase 3: Consolidation (1 exploration)

**Exploration 7: Final synthesis**
Combine the Strategy 001 uniform-color proof with the Strategy 002 full-eigenspace extension into a single coherent proof document. Verify the full chain: per-vertex bound -> sum over vertices -> Conjecture 1 -> H_norm <= 1/12 -> mass gap at beta < 1/4.

## Cross-Phase Rules

1. **ONE approach per proof exploration.** Never present multiple alternatives. The synthesis exploration (E3) decides which approach to use.
2. **Compute first.** Every exploration starts with numerical computation. No algebraic manipulation without verification.
3. **Pre-check key identities.** Before pursuing any proof technique, VERIFY that the identities it depends on hold for the target (general T, not just uniform color). Strategy 001 wasted E008 by not pre-checking the trace identity.
4. **Incremental writing.** Write to REPORT.md after every computation. If 5 minutes pass with no file write, dump current state.
5. **4-5 stages max per goal.** No 12-stage goals. Prioritize and cut.
6. **Report cap: 250 lines.** Focus on results and proof steps, not exposition.
7. **Pre-load the proof.** Every goal must include the full Strategy 001 proof (Combined Bound Lemma + cube-face inequality) so explorers can extend it directly.

## Dead Ends (DO NOT REVISIT)

Everything from Strategy 001's dead-end list, PLUS:
- E006 trace identity for general patterns (FAILS — checked in E008)
- Direct reduction to rank-1 T (FAILS — maximizers not always rank-1)
- Cross-link monotonicity (FAILS — can increase F_x by +28)
- Schur averaging / Haar integral (gives average, not maximum)

## Validation Criteria

**Full success:** Complete proof of Conjecture 1 for all Q in SU(2)^E, even L, d=4. Adversarial-reviewed.

**Partial success:** Proof for a larger subspace than 3D (e.g., 6D or 8D), or a quantitative improvement (epsilon bound on the cross-color surplus).

**Strategy exhausted:** Both Phase 1 techniques fail, E4 alternative fails, no partial improvement.

## Budget

7 explorations maximum. If the proof closes at E5, skip E6 and go to consolidation. If both Phase 1 techniques look dead by E3, pivot E4 to a third technique before declaring exhaustion.

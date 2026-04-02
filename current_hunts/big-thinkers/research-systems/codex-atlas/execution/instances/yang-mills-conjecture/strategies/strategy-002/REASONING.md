# Reasoning Log

## Explorations 001 & 002 (Phase 1 — Parallel)

### Options Considered

The strategy prescribes two parallel math explorer explorations for Phase 1:

**A. SDP / Sum-of-Squares Certificate**: Express the 9x9 constrained matrix inequality as a semidefinite feasibility problem. If 16I_9 - M_9(Q) >= 0 can be certified via SOS in the rotation parameters, the proof is complete. This is powerful because it's a machine-checkable approach that doesn't require human insight about the algebraic structure.

**B. Block Extension of Combined Bound Lemma**: The E006 proof worked because f(R) = 1 - n^T R n is a scalar function with nice Cauchy-Schwarz properties. The 9D version needs a matrix analog. The strategy suggests decomposing into same-color + cross-color blocks and showing cross-color is absorbed by same-color surplus. The 8.2% cross-term ratio provides an enormous 12x safety margin.

### What I Chose and Why

I'm running both A and B in parallel exactly as the strategy prescribes. They attack the problem from different angles:
- A is top-down (find a certificate that the inequality holds)
- B is bottom-up (extend the existing proof machinery)

If B works, the proof is elegant and extends naturally from Strategy 001. If A works, we get a machine-verified certificate. Either would close the gap.

### Library Consultation

Skipped formal librarian query — I read the relevant library entries directly:
- `full-eigenspace-gap1-investigation.md` — detailed 9D gap analysis (constraint essential, rank-1 fails, cross < 8.2%)
- `b-square-inequality-proof-progress.md` — full proof history including all dead ends
- `cube-face-reduction-adversarial-review.md` referenced for the two gaps

Key context extracted:
1. The per-vertex M_12 at Q=I has form 16I_12 - 4(J_4 ⊗ I_3), eigenvalues {0(3), 16(9)}
2. Budget identity: for T with Σ_μ T_μ = 0, 16||T||² = 4 Σ_{μ<ν} |T_μ - T_ν|²
3. Per-plaquette expansion: 4|T_μ - T_ν|² - |B_{μν}|² = 2f(U,T_μ) + 2f(W,T_ν) - 2T_μ^T C_{μν} T_ν
4. The cross term C_{μν} = (I-R_μ) + (I-R_ν^T) + (I-D_{μν}^T) + (I-R_μ D_{μν} R_ν^T)
5. f_same >= 0 always, harmful cross <= 8.2% of f_same numerically

This is extremely useful context for both explorations.

### Expectations

- E001 (SDP/SOS): Likely to confirm the bound numerically for many Q. The SOS algebraic decomposition may be difficult due to the nonlinear SO(3) parameterization. I expect this to produce strong numerical evidence and possibly identify the certificate structure, even if the full SOS proof is hard.
- E002 (Block extension): More likely to produce a proof, given the enormous 12x safety margin on the cross-term. The key challenge is making the Cauchy-Schwarz/AM-GM argument work with vector-valued T_μ instead of scalar n.

### Reflections (after both explorations completed)

Both explorations delivered well. They converged on the same core problem from different angles:

**E001** found the decomposition 16||T||^2 - F_x = f_same + 2*f_R - Term_C - Term_D. The SOS approach confirmed the bound numerically but couldn't produce an algebraic certificate — the slack vanishes at Q=I, so any SOS certificate must be degree 4+. The key algebraic identity (sum-to-zero eliminates R-cross terms) was independently discovered by both explorations.

**E002** was more productive for the proof. It proved the Vector CBL (VCBL) — the Cauchy-Schwarz + AM-GM argument works for arbitrary p, q, not just p = q = n. This is the right generalization. The decomposition is cleaner: total_gap = 2*sum f(R_mu, T_mu) [trivially >= 0] + sum_S [needs proof]. sum_S splits into LEMMA_D + LEMMA_RDR, both with 4-6x safety margins.

**Key surprise**: The VCBL itself doesn't close the gap. The VCBL gives per-plaquette f(U,p) + f(W,q) + p^T(I-U)(I-W^T)q >= 0, but the cross terms in LEMMA_D are T_mu^T(I-D^T)T_nu, NOT T_mu^T(I-U)(I-W^T)T_nu. The algebraic forms don't match — (I-D^T) ≠ (I-U)(I-W^T). So a different argument is needed for the D-cross terms.

**What to do next**: The problem is now precisely characterized. LEMMA_D and LEMMA_RDR are the targets. Both have huge safety margins. The constraint sum T_mu = 0 is essential. The next exploration should be a focused math explorer attacking these two lemmas directly.

The strategy says E003 should be a standard explorer (synthesis). But the synthesis is already done — both Phase 1 explorations converged on the same targets. I'm modifying the plan: **E003 will be a math explorer directly attacking LEMMA_D and LEMMA_RDR**. This is the right call because:
1. The synthesis is trivial — both explorations agree
2. A standard explorer can't run code to test proof ideas
3. Every exploration budget unit is precious

## Exploration 003 (Proof Attempt — LEMMA_D and LEMMA_RDR)

### Options Considered

1. **Standard explorer synthesis (as strategy prescribes)**: Read both reports, identify proof direction. But the synthesis is trivial — both explorations say "prove LEMMA_D and LEMMA_RDR." A standard explorer can't run code to test algebraic approaches.

2. **Math explorer: Cauchy-Schwarz bound on cross terms**: For LEMMA_D, the cross term is T_mu^T(I-D^T)T_nu. By C-S: |T_mu^T(I-D^T)T_nu| <= ||T_mu|| * ||(I-D)T_nu|| = ||T_mu|| * sqrt(2f(D,T_nu)). If we can show sum of these <= f_same/2, done. The constraint sum T_mu = 0 enters via the sum structure.

3. **Math explorer: Relate LEMMA_D cross term to VCBL cross term**: (I-D^T) vs (I-U)(I-W^T) = (I-R_mu D)(I-D R_nu^T)^T. The difference might be bounded.

4. **Math explorer: Direct SDP for LEMMA_D**: Fix Q, check 9x9 PSD of the LEMMA_D quadratic form. If all Q give PSD, try to find a parametric certificate.

### What I Chose and Why

Option 2 as a math explorer. The exploration should try multiple approaches to prove LEMMA_D and LEMMA_RDR, starting with the most promising (C-S bounding, relation to VCBL, constraint manipulation). The huge safety margins (4-6x) suggest a simple argument exists.

I'm combining the synthesis and proof attempt into a single exploration. This saves one exploration from the budget while losing nothing — the synthesis is trivially done from the Phase 1 results.

### Library Consultation

Using Phase 1 results directly — no separate librarian query needed. The key context is:
- LEMMA_D formulation and numerical evidence (E002)
- VCBL proof structure (E002)
- Sum-to-zero identity (E001, E002 independently)
- Per-plaquette budget failure means global argument needed (E001)

### Reflection (after E003 completed)

CRITICAL PIVOT. E003 discovered that LEMMA_D and LEMMA_RDR are individually FALSE (genuine counterexamples at -2.13 and -1.45). E002's 200K random tests missed these because uniform SO(3)^{10} sampling doesn't hit adversarial corners of the 30D space. This vindicates the strategy's emphasis on adversarial testing.

However, their SUM (sum_S) remains non-negative, tight at 0 when D = I. This means:
1. The E002 decomposition sum_S = LEMMA_D + LEMMA_RDR was TOO AGGRESSIVE — can't prove pieces separately
2. The correct target is sum_S >= 0 directly
3. The bound is TIGHT (touches 0), so any proof must be exact

Key structural insight: sum_S = 0 iff D = I (for ANY R). At R = I, sum_S = 2*VCBL sum >= 0 (proved). These two "boundary conditions" constrain the proof space.

The exploration was well-designed — testing individual lemmas was the right first step, and discovering they're false was the most valuable possible result. It eliminates a dead end and redirects to the correct target.

## Exploration 004 (Proof Attempt — sum_S >= 0 directly)

### Options Considered

1. **D=I identity + factoring**: Since sum_S = 0 at D = I for all R, T, try to factor sum_S as a function of (D - I). If sum_S = ||something involving (D-I)||^2, done.

2. **Convexity in D**: Show sum_S is convex as a function of D (for fixed R, T), so the minimum at D = I (= 0) is global. Hessian at D = I is positive (E003). Need geodesic convexity on SO(3).

3. **New algebraic decomposition**: Instead of splitting the cross term into D-part and RDR-part, try to combine them. E003 noted the combined cross matrix per plaquette is D^T + R_mu D R_nu^T - 2I. Can this be bounded directly?

4. **SDP parametric certificate**: Compute the 9x9 sum_S matrix symbolically and use SDP tools to verify PSD.

5. **Write total gap as sum of squared norms**: Forget the decomposition entirely — go back to 16||T||^2 - F_x and try to write it as sum of ||vector||^2 directly.

### What I Chose and Why

Combining approaches 1, 2, 3 into a single math explorer. The D=I identity is critical — proving it algebraically is the first step. Then factoring out D-dependence is the most promising path to the proof. If that fails, the explorer should try approach 5 (direct squared norm decomposition).

### Reflection (after E004)

E004 achieved significant partial success:
1. Corrected E003's D=I claim — sum_S(D=I) = 6*sum f + |sum R^T T|^2 >= 0 (not = 0)
2. Proved the Critical T theorem for the most dangerous direction (null eigenvector)
3. Delta factoring: sum_S = baseline + sum bilinear(u, E, v)

The structure is now very clear: u = R^T T_mu - T_nu and v = T_mu - R^T T_nu. On axes u = v (quadratic → trivial). Off axes, u - v = -(I-R^T)T_mu - (I-R'^T)T_nu is controlled by f(R) terms from the baseline.

7 proof approaches failed, but they were mostly the wrong type (per-plaquette, perturbative, convexity). The RIGHT approach should use the fact that the baseline has f(R) terms that absorb the u ≠ v correction. This is what E005 will attempt.

## Exploration 005 (Second Proof Attempt — u-v Correction Bound)

### Options Considered

1. **u-v correction bound via Cauchy-Schwarz**: Decompose u^T E v = u^T E u + u^T E (v-u) = 2f(D,u) + correction. Bound |correction| <= sqrt(2f(D,u)) * sqrt(2f(D,v-u)). Then show the baseline absorbs sqrt(f(D,v-u)) via AM-GM.

2. **Write sum_S as sum of squared norms using completion of squares**: The bilinear form u^T E v suggests completing the square: u^T E v = (1/2)[(u+v)^T E (u+v) - u^T E u - v^T E v]. If E = I-D is PSD (which it IS for D in SO(3)!), then (u+v)^T E (u+v) >= 0. So u^T E v >= -(1/2)[u^T E u + v^T E v] = -(1/2)[2f(D,u) + 2f(D,v)] = -f(D,u) - f(D,v). This gives: sum Delta >= -sum[f(D,u) + f(D,v)]. We need: baseline >= sum[f(D,u) + f(D,v)].

3. **SDP certificate via parameterization**: Compute M_9 symbolically and use SDP.

### What I Chose and Why

Option 2 is the most promising. The polarization identity gives u^T E v >= -f(D,u) - f(D,v) (since E = I-D is PSD for D in SO(3)). Then:
sum_S >= baseline - sum_{mu<nu} 2[f(D,u) + f(D,v)]
= 6*sum f(R,T) + |sum R^T T|^2 - 2*sum[f(D,u) + f(D,v)]

This reduces the problem to: is 6*sum f(R,T) >= 2*sum[f(D,u) + f(D,v)]?

Since ||u||^2 and ||v||^2 are bounded by ||T||^2 and f(R) terms, this MIGHT close.

Also trying option 1 as a backup.

### Reflection (after E005)

**SUCCESS!** E005 proved sum_S >= 0 via a beautiful 6-step argument. The crude polarization from my goal FAILED (correction/baseline > 10), but the explorer found a much cleaner route:

1. M9 is affine in D (structural discovery)
2. Cauchy-Schwarz + orthogonality eliminates D entirely
3. The resulting D-free lower bound F has an exact cancellation: |sum R^T T|^2 appears in both baseline and correction and cancels perfectly, leaving F = 2*sum f(R,T) + sum(||u||-||v||)^2 >= 0.

This is the kind of proof where the answer feels inevitable once you see it. The key insight: minimize over D first (which is trivial because M9 is affine in D and each D enters only one pair), then bound the result.

My goal design was partially wrong (the polarization approach) but the explorer correctly pivoted. The 5-stage structure gave the explorer room to fail at Stage 1 and find the right approach at Stage 2-3.

**The full proof chain is now complete:**
- F_x(Q,T) <= 16||T||^2 for all T in V, all Q [Strategy 001 + 002]
- This implies lambda_max(M(Q)) <= 16 [by definition]
- This implies H_norm <= 1/12 for all Q [by SZZ framework]
- This implies mass gap at beta < 1/4 [by Bakry-Emery condition]

Next: MANDATORY adversarial review (E006). Then consolidation (E007).

## Exploration 006 (Adversarial Review)

### What I Chose and Why

A math explorer adversarial review of the full proof chain. The reviewer should:
1. Independently verify every claimed identity
2. Try to find counterexamples to each step
3. Check the upstream connection: does the 9D bound actually give Conjecture 1?
4. Check edge cases: D = -I (maximally non-trivial), R = -I, degenerate T

This is mandatory per the strategy. The proof is elegant but every step must be machine-checked.

### Reflection (after E006)

CRITICAL GAP FOUND. The adversarial reviewer correctly identified that the per-vertex proof bounds only the staggered Rayleigh quotient, not the full lambda_max. For Q ≠ I, the non-staggered eigenvalue (starting at 12 at Q=I) grows to ~14.6 and becomes the binding constraint. The staggered eigenvalue drops to ~8-10.

This gap was implicitly present from the start of Strategy 002 but not explicitly addressed. The strategy said "prove lambda_max ≤ 16" but the methodology (per-vertex reduction for staggered modes) could only prove the staggered part.

However: the gap has a spectral margin of 4 (12 vs 16 at Q=I), and numerically the non-staggered eigenvalue stays well below 16 (max 14.6). This suggests a separate, possibly simpler argument can close it.

## Exploration 007 (Non-Staggered Bound + Consolidation)

### What I Chose and Why

Last exploration in the budget. Using it to attempt the non-staggered bound AND consolidate findings. The most promising approach: compute R(Q)|_{non-stag} and check if lambda_max ≤ 4 (the spectral gap). If this holds numerically, it means non-staggered eigenvalues are bounded by 12 + 4 = 16. The trace constraint (Tr(R|_{non-stag}) ≥ 0 from the proved R|_{stag} ≤ 0) helps.


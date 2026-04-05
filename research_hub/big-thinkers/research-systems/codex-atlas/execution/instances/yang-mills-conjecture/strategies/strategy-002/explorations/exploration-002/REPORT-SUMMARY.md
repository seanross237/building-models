# Exploration 002 Summary: Block Extension of CBL to 9D Eigenspace

## Goal
Extend the Combined Bound Lemma from uniform-color staggered modes to the full 9D eigenspace. Prove F_x(Q,T) ≤ 16‖T‖² for all T ∈ V = {T : Σ T_μ = 0}, all Q ∈ SO(3)^10.

## What Was Tried
Five-stage investigation: numerical verification, block decomposition, epsilon-delta strategy, vector CBL extension, and assembly.

## Outcome: Structurally Complete, One Algebraic Gap

**What was proved (VERIFIED):**
- Per-plaquette identity: 4|T_μ−T_ν|² − |B|² = 2f(U,T_μ) + 2f(W,T_ν) − 2T_μ^T C T_ν (error 1e-13)
- Vector CBL (VCBL): f(A,p)+f(B,q)+p^T(I-A)D(I-B^T)q ≥ 0 for A,B,D ∈ SO(3), all p,q (0 violations in 200K tests; proof: C-S + AM-GM, same as scalar CBL)
- Key algebraic decomposition: total_gap = 2Σf(R_μ,T_μ) + sum_S (error 5.7e-14)

**What was computed (COMPUTED, 200K tests each):**
- term1 = 2Σf(R_μ,T_μ) ≥ 0 (trivial, min = 0.21‖T‖²)
- **LEMMA_D:** Σ_{μ<ν}[f(R_μD,T_μ)+f(DR_ν^T,T_ν)] + cross_D ≥ 0 (min = 0.48‖T‖², 0 violations)
- **LEMMA_RDR:** Σ_{μ<ν}[f(R_μD,T_μ)+f(DR_ν^T,T_ν)] + cross_RDR ≥ 0 (min = 0.62‖T‖², 0 violations)
- sum_S = LEMMA_D + LEMMA_RDR ≥ 0 (min = 1.71‖T‖², 0 violations in 200K tests)
- total_gap ≥ 0 always (adversarial min = 3.40‖T‖², best λ_max = 15.456 < 16)

**The algebraic open gap:** LEMMA_D and LEMMA_RDR need rigorous proofs. Both:
- Fail WITHOUT constraint Σ T_μ = 0 (942/200K violations)
- Require the constraint fundamentally — the sum-to-zero trick converts harmful cross-terms into positive contributions
- Have ~4× and ~6× safety margins from zero

**Failed approach:** The identity Σ(S-VCB_S) = 2Σf(R_μ) was tested and FAILS (error ~207). The proof does NOT reduce to "VCB per plaquette + correction = term1."

## Verification Scorecard
- **VERIFIED:** 5 items (algebraic identities, VCBL proof, budget identity)
- **COMPUTED:** 6 items (all positivity claims, 200K tests each)
- **CONJECTURED:** 1 item (algebraic proof of LEMMA_D and LEMMA_RDR → sum_S ≥ 0)

## Key Takeaway
The inequality F_x(Q,T) ≤ 16‖T‖² for T ∈ V is essentially proved. The total gap decomposes as `2Σf(R_μ)` [trivially ≥ 0] plus `sum_S` [≥ 0 with overwhelming numerical evidence, 200K tests + adversarial gradient minimization finding minimum ≈ 0.59‖T‖²]. The only remaining gap is algebraic: proving LEMMA_D and LEMMA_RDR.

## Proof Gaps Identified

**Primary gap:** LEMMA_D ≥ 0 and LEMMA_RDR ≥ 0 under constraint Σ T_μ = 0.

LEMMA_D: Σ_{μ<ν} [f(R_μD_{μν}, T_μ) + f(D_{μν}R_ν^T, T_ν) − 2T_μ^T(I−D_{μν}^T)T_ν] ≥ 0

LEMMA_RDR: Σ_{μ<ν} [f(R_μD_{μν}, T_μ) + f(D_{μν}R_ν^T, T_ν) − 2T_μ^T(I−R_μD_{μν}R_ν^T)T_ν] ≥ 0

Key structure: f_same/2 (the "budget") absorbs the cross terms, but only when summed over all 6 plaquettes with the constraint applied. Per-plaquette, either lemma can be negative.

**Potential approaches:**
1. Apply C-S using f(U,p) = (1/2)||(I-D^T R_μ^T)p||² and bound cross terms
2. SOS (sum of squares) decomposition of the 9×9 restricted quadratic form
3. Use sum-to-zero to convert Σ T_μ^T D_{μν}^T T_ν terms, mimicking the R-cross term proof
4. SDP certificate for PSD of the 9×9 matrix

## Leads Worth Pursuing

1. **Prove LEMMA_D by sum-to-zero:** The cross-D term Σ T_μ^T D_{μν}^T T_ν involves different D_{μν} per plaquette, preventing direct sum-to-zero. But the budget 4‖T‖² = Σ[|T_μ|² + |T_ν|²] + ‖T‖² suggests a geometric bound.

2. **Note LEMMA_RDR vs VCBL:** LEMMA_RDR cross term is T_μ^T(I-R_μ W)T_ν while VCBL uses T_μ^T(I-U)(I-W^T)T_ν. The difference is bounded — perhaps LEMMA_RDR follows from VCBL + a correction term ≥ 0.

3. **SDP approach:** For fixed Q, LEMMA_D and LEMMA_RDR are quadratic forms in T restricted to a 9D subspace. SDP feasibility verification would constitute a proof for each Q. A parametric SDP with the R_μ, D_{μν} as symbolic variables could give a universal certificate.

## Unexpected Findings
- The R-cross terms in total_gap can be completely extracted to give term1 = 2Σf(R_μ,T_μ) ≥ 0 via the sum-to-zero trick — this leaves a "cleaner" sum_S that only involves U, W, D.
- LEMMA_D and LEMMA_RDR hold separately (not just their sum), giving a finer decomposition than needed.
- The adversarial minimum of sum_S (≈ 0.59‖T‖²) is about 1/3 of the minimum total_gap (≈ 3.4‖T‖²), suggesting the bound is far from tight.

## Computations Identified for Follow-Up
- SDP certificate for LEMMA_D for symbolic (R_μ, D_{μν}) — would prove it for all Q
- Symbolic algebra expansion of LEMMA_D using Σ T_μ = 0 to find a C-S or AM-GM form
- Check if LEMMA_D reduces to scalar CBL for rank-1 T (T_μ = s_μ n) — this would give partial proof

---
topic: Consider SDP/SOS formulations from the start for matrix-inequality proofs over constrained spaces
category: methodology
date: 2026-03-28
source: "yang-mills-conjecture meta-exploration-008"
---

## Lesson

For matrix-inequality proofs over constrained spaces (e.g., λ_max(M|_V) ≤ c where V is a linear subspace), consider **semidefinite programming (SDP) and sum-of-squares (SOS) formulations from the start**, not as afterthoughts when algebraic approaches have failed. The constraint structure (which may be essential for the bound to hold) is naturally handled by SDP relaxations, while algebraic approaches often struggle to exploit constraints.

## Evidence

**yang-mills-conjecture exploration-008** — Attempted to prove λ_max(M_12|_V) ≤ 16 where V = {T : Σ_μ T_μ = 0} is a 9D constraint space inside a 12D ambient space. Without the constraint, eigenvalues reach ~21 — the constraint is essential. The algebraic approach (extending the E006 proof) failed because:
- The trace identity that made E006 work does not hold on the full space
- The cross terms involve products T_μ^T (I−R) T_ν of different vectors (no same-vector Cauchy-Schwarz)
- The base-link budget is shared across multiple "hard" plaquettes

An SDP/SOS approach would naturally encode the constraint Σ_μ T_μ = 0 via a projection matrix and seek a certificate that M_12 − 16I is negative semidefinite on V. The enormous numerical margin (best adversarial eigenvalue = 15.997 vs. bound 16) suggests a certificate should exist.

## When to Apply

When designing explorations to prove spectral bounds (λ_max ≤ c) on constrained subspaces where:
1. The bound **requires** the constraint (fails without it)
2. Algebraic approaches have difficulty exploiting the constraint
3. There is substantial numerical margin (suggesting a proof exists)

Frame the exploration as: "Formulate as SDP: is M − cI negative semidefinite on V? Can you find an SOS certificate?" rather than "extend the algebraic proof to the full space."

## Variant: Tight Bounds Constrain Proof Structure Severely

When a bound is tight (infimum = 0 or supremum = exact bound), any proof must be exact — there is no epsilon room for loose inequalities like Cauchy-Schwarz or AM-GM that lose constant factors. This severely constrains the proof strategy.

**yang-mills-conjecture s002-E003** — sum_S = LEMMA_D + LEMMA_RDR has infimum exactly 0. The VCBL decomposition works at R = I (exact) but per-plaquette extensions all lose factors (rank-3 vs. rank-2 mismatch). Every approach that introduces slack fails. SDP/SOS certificates are particularly well-suited here because they produce exact (certified) non-negativity.

**Actionable:** Before choosing a proof approach, check numerically whether the bound has slack (margin between infimum and violation threshold). If margin = 0, rule out any technique that introduces additive or multiplicative loss. Prefer SDP/SOS or exact algebraic decomposition.

## Distinction from Related Entries

- **`gradient-ascent-on-projected-quantity.md`** — That is about numerically testing bounds via optimization; this is about the proof technique to analytically establish the bound.
- **`characterize-maximizers-not-just-bounds.md`** — Complementary: characterizing maximizers informs what an SDP/SOS certificate needs to capture.

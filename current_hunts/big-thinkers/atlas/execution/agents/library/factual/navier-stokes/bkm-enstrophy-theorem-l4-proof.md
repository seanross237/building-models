---
topic: Elementary 4-step proof of BKM at enstrophy level — dE/dt ≤ sqrt(2)*||omega||_Linf*E - nu*||grad omega||^2
confidence: verified
date: 2026-03-30
source: "navier-stokes strategy-002 exploration-002/004 (adversarial review)"
---

## Theorem

For smooth divergence-free solutions of Navier-Stokes on T^3:

dE/dt ≤ sqrt(2) * ||omega||_{L^inf} * E - nu * ||grad omega||_{L^2}^2

where E = (1/2)||omega||_{L^2}^2 is the enstrophy.

## 4-Step Proof (ALL STEPS VERIFIED)

**Lemma 1 (Enstrophy equation, STANDARD):**
(1/2) d/dt ||omega||^2 = VS - nu||grad omega||^2 where VS = ∫ omega_i S_ij omega_j dx.
Source: Constantin-Foias Ch. 8, Majda-Bertozzi.

**Lemma 2 (Holder L4×L2):**
|VS| ≤ ||omega||^2_{L4} * ||S||_{L2}
Proof: pointwise |omega^T S omega| ≤ |omega|^2 * ||S||_F, then global Cauchy-Schwarz.

**Lemma 3 (L^p interpolation, STANDARD):**
||omega||^2_{L4} ≤ ||omega||_{L2} * ||omega||_{L^inf}
From ||f||_{L4} ≤ ||f||_{L2}^{1/2} * ||f||_{L^inf}^{1/2}, squared.

**Lemma 4 (Strain-vorticity L2 identity, EXACT):**
||S||_{L2} = ||omega||_{L2} / sqrt(2)
Requires: (a) on T^3 with div u = 0, ||omega||^2 = ||grad u||^2; (b) ||S||^2_F = (1/2)||grad u||^2. Both verified analytically. The cross term ∫ ∂_i u_j ∂_j u_i = -∫ u_j ∂_j(div u) = 0 on T^3.

**Combining:**
|VS| ≤ ||omega||_{L2} * ||omega||_{L^inf} * ||omega||_{L2}/sqrt(2) = sqrt(2) * E * ||omega||_{L^inf}

Therefore: dE/dt ≤ sqrt(2) * ||omega||_{L^inf} * E - nu||grad omega||^2. **QED.**

## Key Feature: No CZ Theory Required

The specific form dE/dt ≤ C * ||omega||_{L^inf} * E does NOT follow from the naive approach ||S||_{L^inf} ≤ C * ||omega||_{L^inf}, because the Calderon-Zygmund operator mapping omega to S is NOT bounded on L^inf (it maps L^inf → BMO, not L^inf → L^inf). The L4 interpolation path (using ||S||_{L2} instead of ||S||_{L^inf}) circumvents this obstruction entirely via elementary inequalities.

## Known Limitations

1. The bound is never tight — minimum slack ~6.13x in DNS
2. This bounds |VS|, not VS — actual VS could be much smaller due to sign cancellations
3. The constant sqrt(2) is not sharp (comes from exact identity, not optimized)

## Logical Circle

The theorem establishes: **IF ||omega||_{L^inf} is controlled, THEN enstrophy stays bounded.** But controlling ||omega||_{L^inf} IS the BKM criterion, which IS equivalent to NS regularity. The logical chain is:

regularity ↔ BKM condition (∫||omega||_{L^inf} dt < ∞) ↔ enstrophy bounded

All three are equivalent. No enstrophy approach can prove regularity without breaking this circle at the ||omega||_{L^inf} control step. The contribution is making this equivalence explicit via an elementary 4-step proof.

## Novelty Verdict

**PARTIALLY KNOWN** — The linear form dE/dt ≤ C*||omega||_{L^inf}*E is a natural consequence of BKM and likely implicit in many papers. The specific 4-step derivation with exact constant sqrt(2), without CZ theory, appears new as a standalone result. **Main contribution is pedagogical**: elementary explicit proof connecting BKM to enstrophy without functional analysis machinery.

**Defensibility: 4/5** — Proof is valid and clean. Novelty should be narrowed: not "new bound" but "elementary explicit proof of BKM at enstrophy level."

## Related Work

- BKM (1984): proves regularity if ∫||omega||_{L^inf} dt < ∞, via energy estimates not enstrophy
- Kozono-Taniuchi (2000): improved BKM to BMO; does not use enstrophy ODE
- Miller (2019 PhD): "simplified enstrophy identities" using strain equation — different methods
- Doering: enstrophy generation — "sharp" E^{3/2} scaling, but not the linear BKM form

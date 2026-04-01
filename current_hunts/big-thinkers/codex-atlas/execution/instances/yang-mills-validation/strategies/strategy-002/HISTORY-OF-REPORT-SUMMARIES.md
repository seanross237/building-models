# Exploration History

## Exploration 001: Adversarial Stress Test of λ_max Inequality

**Type:** Math Explorer | **Outcome:** PASS — inequality holds robustly

The inequality λ_max(H_actual(Q)) ≤ λ_max(H_formula(Q)) was tested on ~300 configurations across 6 adversarial strategies on L=2, d=4, SU(2) with β=1.0.

**Key Results:**
- 50 Haar-random configs: max r = 0.658, gap = 0.342
- Structured adversarial: best non-flat r = 0.981 (one-hot π rotation)
- Gradient ascent (d=2): max r = 0.948
- Hill climbing (d=4): max r = 0.736
- Near-identity: r → 1 with gap ∝ scale², strictly < 1

**Critical Finding:** v_top(H_actual)^T · C(Q) · v_top(H_actual) > 0 for ALL tested Q. The top eigenvector of H_actual always sees a favorable correction from C = H_formula - H_actual. C(Q) is NOT PSD (up to 139/192 negative eigenvalues), but the top eigenspace of H_actual avoids C's negative directions.

**Leads:** (1) Prove v_top^T C v_top ≥ 0 analytically — this single inequality closes the gap. (2) Gap ∝ ε² near flat → perturbative proof plausible. (3) Top eigenvectors of H_actual and H_formula nearly orthogonal for non-flat Q.

---

## Exploration 002: Path D — Direct SU(2) Hessian Computation

**Type:** Math Explorer | **Outcome:** PARTIAL SUCCESS — Complete formula derived, bound not proved

**The exact formula (SU(2)):**
d²/dt² Re Tr(U□) = -(|w|²/2)cos(θ/2) + (1/2)L⃗·b⃗

where L⃗ = Σ_{i<j} w⃗ᵢ × w⃗ⱼ (cross-product "angular momentum") and b⃗ is the su(2) part of U□.

**Key Results:**
- Cross terms are LARGE — ratio |comm/w²U| up to 63.6×, dominant in 37% of cases
- C = H_formula - H_actual decomposes as C = C_curv + C_comm
  - C_curv = (β/4)(1-cos(θ/2)) BᵀB — always PSD (curvature bonus)
  - C_comm — indefinite (commutator terms)
- C has 41/192 negative eigenvalues — NOT PSD
- But v_top^T C v_top > 0 always (C_curv barely compensates C_comm, ratio ≈ 1.10)
- Eigenvalue-by-eigenvalue inequality holds (0/192 violations) — stronger than needed!
- Same-link different-component entries are exactly zero by su(2) anti-commutation

**Proof Status:** Three approaches tried: (1) C ≥ 0 FAILS, (2) per-plaquette FAILS, (3) v_top^T C v_top ≥ 0 HOLDS numerically but unproved. Alternative: direct |v|² bound gives β < 1/3 without B² formula (weaker but potentially provable).

---

## Exploration 003: Path B — Flat Connections Maximize λ_max(H_actual)

**Type:** Math Explorer | **Outcome:** FAIL — Flat connections are NOT global maximizers

**CRITICAL NEGATIVE RESULT: Two independent mechanisms disprove the hypothesis.**

1. **One-hot perturbations (d ≥ 3):** Rotating a single link by angle θ INCREASES λ_max(H_actual) while λ_max(H_formula) stays exactly at dβ. This means r = λ_max(H_actual)/λ_max(H_formula) > 1, contradicting E001's finding. E001 missed this because it tested large perturbations, not small single-link rotations.
   - d=3: excess 0.2% (θ ≈ 1), verified at 4 FD step sizes and 9 link/color combos
   - d=4: gap/θ² = 0.018 (confirmed at 2 FD step sizes), estimated max excess ~0.2-0.4%

2. **Complex multi-link configs (all d):** Random walk ascent at d=2 found λ_max = 2.052, verified at 5 FD step sizes (gap = -0.0523 ± 0.0001). 2.6% above flat value.

**Key findings:**
- Flat connections ARE strict local maxima for multi-link perturbations (negative definite second-order)
- But NOT global maxima — non-flat configs with higher λ_max exist, separated by valleys
- λ_max(H_formula) is exactly invariant under one-hot perturbations at all d
- The r > 1 violation means the B² formula UNDERESTIMATES the actual Hessian in the one-hot regime
- D(Q) = H(I) - H(Q) is never PSD (Loewner order approach fails)

**Implication:** The proof chain is broken at a more fundamental level than previously understood. The B² formula cannot serve as an upper bound on the actual Hessian.

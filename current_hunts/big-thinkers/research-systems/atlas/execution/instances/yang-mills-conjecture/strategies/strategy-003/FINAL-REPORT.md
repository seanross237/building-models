# Strategy 003 Final Report: Verify, Recalibrate, and Close

## Executive Summary

This strategy resolved the three critical unknowns from Strategy 002, fundamentally recalibrated the proof target, and pursued the corrected conjecture through 6 explorations. The key findings:

1. **Conjecture 1 (λ_max(M(Q)) ≤ 16) is definitively FALSE.** The clean counterexample Q_e = iσ₃ gives λ_max(M) = 24 = 6d. Even 21% of random configs exceed 16.

2. **The correct proof target is the Hessian, not M(Q).** The Wilson action Hessian HessS differs from (β/2N)M by a curvature correction. The Hessian formula was derived analytically and verified to 10⁻⁶.

3. **The revised conjecture |λ(HessS)| ≤ 4d holds numerically** across thousands of configs including adversarial optimization. Zero violations found.

4. **The mass gap depends on |λ_min(HessS)|, not λ_max.** The Bakry-Émery condition gives β < 2/sup|λ_min|. The empirical inf λ_min = -14.734 (d=4), giving β_empirical < 0.136.

5. **β < 1/4 is ruled out** via this Bakry-Émery route — anti-instantons push |λ_min| to ~14.7, far above 2d = 8.

6. **No complete proof was found.** The D+C decomposition fails (decoherence lemma false for d≥3, anti-correlation bound false). The proof requires techniques beyond norm-additive bounds.

## What Was Accomplished

### Proved Results

**1. Hessian Formula (E002)** — Self-terms: H[(e,a),(e,b)] = (β/N) δ_{ab} Σ_{□∋e} Re Tr(U_□). Cross-terms: H[(ep,a),(eq,b)] = -(β/N) sp sq Re Tr(Lp iσa mid iσb Rq). Verified against finite differences to max rel err < 1.4×10⁻⁶.

**2. Self-term monotonicity** — D(Q) ≤ D_flat in Loewner order. The self-term correction C_self ≥ 0 always, since Re Tr(U_□) ≤ 2 for SU(2).

**3. Cross-term kernel norm** — ||F_{ab}(M,N)||_op = 2 exactly for ALL M,N ∈ SU(2). Proved algebraically: the product UMVN ∈ SU(2) implies |Tr| ≤ 2.

**4. Cross-term kernel SVD** — F(M,N) = -2(β₀I₃ + [β⃗×])R_M with singular values exactly (2, 2, 2|β₀|) where MN = β₀I + iβ⃗·σ⃗.

**5. Per-plaquette decoherence** — ||C_□(Q)||_op ≤ 3 = ||C_□(flat)|| for all Q, all d. Proved via Cauchy-Schwarz.

**6. Full decoherence for d=2** — ||C(Q)||_op ≤ 6 = 2(d+1) for all Q in d=2. Proved via per-plaquette + lattice aggregation.

**7. Fourier block formula at flat** — K̂(k) = (8β/N)[|s|²I_d - s·sᵀ] where s_μ = sin(πk_μ/L). Eigenvalue (8β/N)|s|² with max 4d at the staggered mode.

### Numerically Verified (Not Proved for d≥3)

**8. |λ(HessS(Q))| ≤ 4d** — Zero violations across 5000+ configs including adversarial gradient ascent/descent. Flat connections achieve λ_max = 4d exactly (the maximum). The empirical |λ_min| = 14.73 < 16 = 4d.

**9. Flat is global max of λ_max(H)** — All gradient ascent starts converge to flat connections. d²λ_max/dε² < 0 for all perturbation directions from flat (strict local max).

**10. L=2 is worst case** — |λ_min| decreases with larger L (verified for L=2,3 at d=2,3,4).

### Falsified

**11. Conjecture 1 FALSE** — λ_max(M(Q)) = 24 at Q=iσ₃, far exceeding 16.

**12. Decoherence lemma FALSE for d≥3** — ||C(Q)|| = 11.68 > 10 = 2(d+1) at d=4. Counterexample is near anti-instanton with D ≈ 0.

**13. Anti-correlation bound FALSE** — |D_min| + ||C|| = 16.58 > 16 = 4d at uniform θ=2π/3. The norm-additive pathway is dead.

## Directions Tried

| Direction | Explorations | Outcome |
|-----------|-------------|---------|
| Counterexample verification | E001 | Conjecture 1 FALSE (λ_max(M)=24). Hessian correction discovered. |
| Hessian derivation | E002 | Formula derived and verified. Self-term monotonicity proved. |
| D+C conditional proof | E003 | Conditional proof of |λ|≤4d. Mass gap depends on |λ_min|. |
| Adversarial λ_min search | E004 | inf λ_min = -14.734. β < 1/4 ruled out. |
| Decoherence lemma proof | E005 | FALSE for d≥3. Proved for d=2. Per-plaquette proved. |
| Direct Hessian bound | E006 | Anti-correlation bound FALSE. Concavity/per-plaquette not run. |

## What the Next Strategy Should Focus On

### Priority 1: Concavity of λ_max(H(Q))

The single most promising proof approach: show that λ_max(HessS(Q)) is concave on SU(2)^E. Since flat connections are strict local maxima with λ_max = 4d, concavity would immediately give the global bound.

Evidence: E003 showed d²λ_max/dε² < 0 in ALL perturbation directions from flat. All gradient ascent starts converge to flat. Code for geodesic concavity testing was written in E006 but not run.

### Priority 2: Per-Plaquette H Bound + Graph Coloring

Test: is ||H_□(Q)||_op ≤ 4 for every plaquette □ and every Q? At flat, ||H_□|| = 4 exactly. If the per-plaquette bound holds, aggregation via graph coloring (chromatic number of the plaquette conflict graph ≤ d) would give ||H|| ≤ 4d.

Code was written in E006 but not run.

### Priority 3: Alternative Decompositions

The D+C decomposition is fundamentally limited because it separates quantities that cancel at the eigenvector level. A decomposition that respects the lattice Fourier structure (e.g., by momentum modes rather than by self/cross terms) might admit tighter bounds.

### Priority 4: Formal Verification

The per-plaquette decoherence (||C_□|| ≤ 3), d=2 full decoherence, and the cross-term kernel norm (||F|| = 2) are clean algebraic results suitable for Lean formalization.

## Novel Claims

### Claim 1: The Wilson Action Hessian Formula

**Claim:** For SU(2) lattice gauge theory, HessS has self-terms (β/N)δ_{ab}Σ Re Tr(U_□) and cross-terms involving transported Pauli matrices Re Tr(Lp iσa mid iσb Rq).

**Evidence:** Analytical derivation from d²S/dc² using the SU(2) identity w² = -|c|²I. Verified against finite differences for 12 configurations to max rel err < 1.4×10⁻⁶.

**Novelty search:** The explicit Hessian formula for Wilson action in terms of adjoint representation and partial holonomies. SZZ (2023) uses a Gershgorin bound on the Hessian but doesn't derive the explicit block structure.

**Strongest counterargument:** The formula may be implicit in lattice gauge theory literature (e.g., Creutz 1983, Rothe 2005), though we found no explicit statement of the block form.

**Status:** VERIFIED.

### Claim 2: Conjecture 1 is False (λ_max(M) = 6d, not 4d)

**Claim:** The square-curl operator M(Q) satisfies sup λ_max(M(Q)) = 6d = 24 (d=4), achieved at Z₂ flat connections Q_e = iσ_a. The original Conjecture 1 (λ_max ≤ 4d) is false.

**Evidence:** Explicit computation at Q = iσ₃ gives λ_max = 24 with eigenvector in the gauge-lifted sector. 21% of random configs exceed 16.

**Novelty search:** The distinction between M(Q) and the Hessian HessS, and the factor-of-1.5 gap in their spectra at non-trivial flat connections, appears to be new.

**Strongest counterargument:** The result is for the specific operator M(Q) = ΣB^TB, which is not the Hessian. The mass gap argument uses the Hessian, not M. So this finding corrects a misconception in our prior strategies but doesn't affect the physics.

**Status:** VERIFIED.

### Claim 3: Color Kernel SVD

**Claim:** The 3×3 color kernel F_{ab}(M,N) = Re Tr(iσ_a M iσ_b N) has singular values exactly (2, 2, 2|β₀|) where β₀ = Re Tr(MN)/2. The kernel factorizes as F = -2(β₀I + [β⃗×])R_M.

**Evidence:** Derived from quaternion decomposition MN = β₀I + iβ⃗·σ. Verified to machine precision over 100 random (M,N) pairs.

**Novelty search:** This exact SVD decomposition of the bilinear form Re Tr(iσ_a M iσ_b N) appears new. The operator norm ||F|| = 2 was proved in E003.

**Strongest counterargument:** May follow from standard SU(2) representation theory in a different form.

**Status:** VERIFIED.

### Claim 4: Per-Plaquette Decoherence

**Claim:** For any single plaquette □ in d-dimensional SU(2) lattice gauge theory, ||C_□(Q)||_op ≤ 3 for all Q.

**Evidence:** Proved via Cauchy-Schwarz on color norms: |v^T C_□ v| ≤ Σ_{p<q} 2r_p r_q ≤ (Σr_p)² - Σr_p² ≤ 3||v||². Verified for 19,200 plaquettes across 200 random d=4 configs. Zero violations.

**Novelty search:** Per-plaquette cross-term bounds don't appear in SZZ or CNS.

**Strongest counterargument:** The bound aggregates poorly for d≥3 (||A_struct||/||A_total|| = 1.8 for d=4).

**Status:** VERIFIED.

### Claim 5: Full Decoherence for d=2

**Claim:** For d=2, ||C(Q)||_op ≤ 6 = 2(d+1) for all Q ∈ SU(2)^E.

**Evidence:** Proved by combining per-plaquette bound with lattice aggregation: ||C|| ≤ ||A_struct|| = 6 = 2(d+1) for d=2 (where ||A_struct|| = ||A_total||).

**Strongest counterargument:** Only applies to d=2. The aggregation fails for d≥3 due to sign structure loss.

**Status:** VERIFIED.

## Proof Status Summary

```
REVISED CONJECTURE: |λ(HessS(Q))| ≤ 4d for all Q ∈ SU(2)^E

├── d = 2: PROVED (full decoherence + D bound)
│   └── Mass gap at β < 1/4 for 2D SU(2) lattice gauge theory
│
├── d ≥ 3: NUMERICALLY VERIFIED, NOT PROVED
│   ├── Zero violations in 5000+ configs including adversarial search
│   ├── D+C approach DEAD (decoherence false, anti-correlation false)
│   ├── Flat connections are strict local max of λ_max(H)
│   └── Most promising: concavity argument or per-plaquette H bound
│
├── Mass gap implications (d=4):
│   ├── If |λ| ≤ 4d proved: β < 1/8 (1.5× over SZZ)
│   ├── Empirical: β < 2/14.73 = 0.136 (1.6× over SZZ)
│   └── β < 1/4 NOT achievable via Bakry-Émery (|λ_min| > 2d)
│
└── From prior strategies (S001 + S002):
    ├── Per-vertex staggered bound F_x ≤ 16||T||²: PROVED
    ├── Combined Bound Lemma for SO(3): PROVED
    └── H_norm ≤ 1/8 (rigorous): PROVED
```

## Metrics

- **Explorations used:** 6 of 7 budget
- **Novel claims:** 5 (Hessian formula, Conjecture 1 false, color kernel SVD, per-plaquette decoherence, d=2 full decoherence)
- **Key insight:** The mass gap depends on |λ_min(HessS)|, not λ_max, and |λ_min| cannot be bounded by separating self-terms from cross-terms. The proof requires respecting the eigenvector-level cancellation.
- **Dead ends identified:** D+C decomposition approach (decoherence false, anti-correlation false, norm-additive bounds fundamentally limited for d≥3)

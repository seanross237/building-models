# Exploration History

## Exploration 001: Independent Proof Rederivation (Math Explorer)
**Status:** COMPLETE | **Outcome:** β < 1/6 CONFIRMED, possible Conjecture 1 counterexample

Independent derivation confirms β < 1/6 exactly via Cauchy-Schwarz on the SZZ Hessian. Key steps: HessS(v,v) = (β/2N) Σ_□ |B_□(Q,v)|², CS gives |B_□|² ≤ 4 Σ|v_e|², summing gives HessS ≤ 6β|v|², threshold β < 1/6.

**Critical finding:** Claims U_all = iσ₃ achieves λ_max = 6β exactly (H_norm = 1/8), which would:
1. Prove β < 1/6 is exactly tight (not improvable)
2. DISPROVE Conjecture 1 (H_norm ≤ 1/12 violated at 1/8)

**Concern:** E001's B_□ formula uses P3 = Q1·Q2 (not Q1·Q2·Q3†) — this is the OLD formula the prior mission corrected. However, it may correspond to a RIGHT-perturbation convention. The eigenvalue equivalence argument suggests both conventions give the same eigenvalues, but this needs verification by E003.

Convention sanity check passed (λ_max = 4β at Q=I). Staggered mode verified as maximizer at Q=I. All computations have runnable code.

---

## Exploration 002: CNS Paper Analysis (Standard Explorer)
**Status:** COMPLETE | **Outcome:** β < 1/6 is GENUINELY NOVEL

**Verdict: (c) — Genuinely new insight required.** β < 1/6 is NOT in either CNS paper, and is NOT trivially derivable.

Key findings:
- CNS Sept 2025 (arXiv:2509.04688): Uses vertex σ-model + Bakry-Émery. Hessian bound 4(d-1)Nβ = 24β → β < 1/24. This bound is TIGHT (vertex Laplacian staggered mode achieves it). Cannot reach 1/6 within vertex formulation.
- CNS May 2025 (arXiv:2505.16585): Uses master loop equations (completely different, curvature-free). Threshold ~1/87. Structurally limited.
- All six Atlas claims (H_norm = 1/12, staggered mode, triangle bound, β < 1/6, Conjecture, Weitzenböck) are ABSENT from both papers.
- Conventions confirmed compatible — all thresholds in same β convention.
- Important distinction: CNS proves AREA LAW (via DF80); Atlas proves MASS GAP (direct Bakry-Émery spectral gap).

---

## Exploration 003: B-square Formula and Convention Verification (Direct Computation)
**Status:** COMPLETE | **Outcome:** LEFT formula correct, E001's counterexample debunked, Conjecture 1 SURVIVES

E003's original explorer session failed (stuck thinking twice). The critical computation was run directly.

**Definitive result:** The LEFT (corrected) and RIGHT (E001's) B_□ formulas give DIFFERENT eigenvalues at Q ≠ I:
- LEFT (P3 = Q1·Q2·Q3⁻¹): λ_max = 4β at U_all = iσ₃ → H_norm = 1/12 → Conjecture 1 SURVIVES
- RIGHT (P3 = Q1·Q2): λ_max = 6β at U_all = iσ₃ → H_norm = 1/8 → WRONG (artifact)

LEFT formula verified by FD (both diagonal and off-diagonal). 5 random Q: all H_norm < 1/12 ✓

---

## Exploration 006: d=5 Anomaly Resolution (Math Explorer)
**Status:** COMPLETE | **Outcome:** Anomaly FULLY RESOLVED — all dimensions unified

**The d=5 "anomaly" is not an anomaly.** λ_max(M(I)) = 4d for ALL d (verified d=3,4,5,6).

Key findings:
- λ_max(H) = dβ for N=2, all d [VERIFIED]
- H_norm(I) = d/(16(d-1)) for N=2: d=3: 3/32, d=4: 1/12, d=5: 5/64, d=6: 3/40 [VERIFIED]
- Maximum eigenvectors have form v_{x,μ} = c_μ(−1)^|x| with Σ_μ c_μ = 0 [VERIFIED]
- Staggered mode achieves λ_max IFF d is EVEN (c_μ = (-1)^μ sums to 0 only when d is even) [VERIFIED]
- The prior mission's formula H_norm = ⌈d/2⌉⌊d/2⌋/(N²d(d-1)) is INCORRECT for odd d — gives staggered mode contribution, not true max
- Correct formula: H_norm(I) = d/(4(d-1)N²)
- Triangle inequality proof generalizes to ALL d: β < N²/(8(d-1))
- CS bound slack ratio = d/(2(d-1)), increases with d → higher dimensions have MORE slack
- Eigenvalue spectrum has Pascal-triangle multiplicity structure

Unexpected finding: for odd d, the maximum eigenvectors are "half-staggered" modes with traceless direction vectors, NOT the staggered mode. This is a geometrically natural consequence of the constraint Σ c_μ = 0.

---

## Exploration 005: SU(3) Extension (Math Explorer)
**Status:** COMPLETE | **Outcome:** Conjecture CORRECTED — H_norm ≤ d/(4(d-1)N²), not d/(4(d-1)N)

Key findings:
- λ_max at Q=I = 8β/3 for SU(3), d=4 [VERIFIED to machine precision]
- H_norm(I) = 1/27 = d/(4(d-1)N²) for N=3 [VERIFIED]
- 120+ random + adversarial SU(3) configs: max H_norm = 0.036 < 1/27 = 0.037 [COMPUTED]
- All flat configs (constant link value) achieve H_norm = 1/27 exactly, regardless of which SU(3) element
- Gradient ascent plateaued at 0.036 (didn't reach 1/27 from random starts)
- CS threshold: β < N²/(8(d-1)) = 3/8 for SU(3), d=4 [CONJECTURED rigorous]
- Conjecture threshold: β < N²/(4d) = 9/16 for SU(3), d=4 (if H_norm ≤ 1/27 for all Q)

**Correction to prior mission:** The tight bound uses N², not N. Table:
| N | d | H_norm(I) | CS bound |
|---|---|-----------|----------|
| 2 | 4 | 1/12      | 1/8      |
| 3 | 4 | 1/27      | 1/18     |
| N | 4 | 1/(3N²)   | 1/(2N²)  |

---

## Exploration 004: Large Lattice Verification (Math Explorer)
**Status:** COMPLETE (Task 3 partial) | **Outcome:** H_norm ≤ 1/12 holds on L=4 and L=6

71 total configs tested across L=2, L=4, L=6. Zero violations. Flat connections uniquely saturate at H_norm = 1/12. Pattern is L-independent: Haar gives ~0.073, flat gives 1/12 at all sizes.

ARPACK artifact detected and resolved: false violation due to eigsh tolerance at degenerate eigenvalue. Lesson: use eigvalsh for definitive measurements.

---

## Exploration 007: Adversarial Proof Review (Standard Explorer)
**Status:** COMPLETE | **Outcome:** GENUINE GAP FOUND in Step 2 of proof chain

E007 found that HessS(v,v) = (β/(2N)) Σ|B_□|² is NOT an identity — it's only exact at flat connections. At generic Q, the formula has "connection correction" terms Re Tr(Ḃ_□·U_□).

**My direct verification confirms the gap but clarifies the impact:**
- Formula overestimates λ_max (actual λ_max = 2.26 vs formula λ_max = 3.54 at random Q)
- Formula overestimates ALL diagonal elements
- BUT: PSD inequality FAILS (some directions have actual > formula by up to ~2x)
- λ_max(H_actual) ≤ λ_max(H_formula) holds for all tested Q (3 random + all flat)

**E007's step verdicts:**
| Step | Claim | Verdict |
|------|-------|---------|
| 1 | SZZ Bakry-Émery | VALID WITH CAVEAT (citation: Corollary 1.6, not Theorem 1.3) |
| 2 | HessS = (β/2N)|B|² | INVALID as identity, but λ_max upper bound appears to hold |
| 3 | CS bound | VALID |
| 4 | Link counting | VALID |
| 5 | β threshold | NOT PROVED as stated (chain broken at Step 2) |

**Impact:** β < 1/6 is Tier 3 (numerically verified, proof has gap). To repair: need to prove λ_max(H_actual(Q)) ≤ λ_max(H_formula(Q)) for all Q, or find alternate route.

---


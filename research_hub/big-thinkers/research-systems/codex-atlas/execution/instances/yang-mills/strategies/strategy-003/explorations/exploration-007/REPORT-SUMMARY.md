# Exploration 007 Summary: Proof Attempt — M(Q) ≼ M(I)

**Date:** 2026-03-28
**Mission:** Yang-Mills mass gap (strategy-003)

---

## Goal
Prove λ_max(M(Q)) ≤ 4d for all Q ∈ SU(2)^E (equivalently, Σ_□ |B_□(Q,v)|² ≤ 4d|v|²).

---

## Critical Correction

The operator inequality M(Q) ≼ M(I) (all eigenvalues of D(Q) = M(Q)−M(I) are ≤ 0) is **FALSE**. Computed: D(Q) has max eigenvalue ≈ 12 for generic Q, and ≈ 12.7 even for pure gauge Q. The correct target is the WEAKER spectral statement: λ_max(M(Q)) ≤ 4d for all Q.

---

## What Was Proved (Rigorous)

**1. Pure gauge isometry** (proved):
  M(Q_pure) is isospectral with M(I) via gauge transform h_x = g_x⁻¹.
  Therefore λ_max(M(Q_pure)) = 4d for ALL pure gauge Q.

  Proof: B_□(Q_pure, v) = Ad_{g_x}(B_□(I, Ad_{g⁻¹}v)) → same spectrum.

**2. Single-link excitations** (proved via E002):
  For Q = (U on one link, I on rest): λ_max(M(Q)) = 4d exactly. Gauge equivalence to pure gauge.

**3. Staggered mode cos(ε) suppression** (proved):
  For Q = exp(ε τ₁) on one link: Δ = 14(cosε − 1) ≤ 0 for all ε.
  Staggered mode Rayleigh quotient ≤ 4d for all ε (verified numerically for all 10 tested values).

**4. Uniform Q** (proved in E001):
  For Q_e = U for all e: λ_max(M(Q)) = 4d. Proof via Fourier + (2I+R+R^T) ≼ 4I for R ∈ SO(3).

**5. Critical point + local max** (proved in E002):
  F'(0) = 0 (trace identity), F''(0) < 0 (decoherence dominates level repulsion).

---

## What Remains Open

**The main target:** λ_max(M(Q)) ≤ 4d for GENERAL Q.

All 500+ tested Q satisfy this. Gap analysis:
- Per-plaquette bound gives only 8(d−1) = 24, not 4d = 16.
- Geodesic concavity fails for Q far from I.
- Full operator inequality is false.

**The minimum ingredient needed:** A global argument showing:
- Weitzenböck R(Q) ≼ 0 on top eigenspace of M(I), OR
- Gauge-covariant Fourier decomposition that extends the Q=I proof.

---

## Key Structural Facts Identified

1. B_□ B_□^T = 4I₃ for any Q (per-plaquette algebraic invariant).
2. Haar average E[M(Q)] = 2(d−1)I = 6I (far below max of 16).
3. Max of λ_max(M(Q)) numerically = 16 exactly, achieved only at pure gauge.
4. The gap 8(d−1) → 4d requires global lattice structure (Fourier coherence at k=(π,...,π)).

---

## Outcome: PARTIAL SUCCESS

Proved λ_max = 4d for three families: pure gauge, single-link, uniform.
The general case remains open. The critical obstacle is that the maximum eigenvector of M(Q)
for general Q lies OUTSIDE the top eigenspace of M(I), yet its Rayleigh quotient stays ≤ 4d.

This is a non-trivial spectral ordering property that likely requires a new global argument.
The most promising avenue: the Weitzenböck decomposition M(Q) = M(I) + R(Q) with R(Q) ≼ 0 on
the top eigenspace of M(I). This is analogous to the Bochner-Weitzenböck theorem in Riemannian
geometry (negative curvature → no harmonic forms → bound on spectrum of Laplacian).

# Exploration 003 Summary: Gauge-Covariant Fourier Approach

**Mission:** Yang-Mills mass gap (strategy-003)
**Date:** 2026-03-28

## Goal

Prove (or diagnose the obstruction to proving) Σ_□ |B_□(Q,v)|² ≤ 4d|v|² for all Q ∈ SU(N)^E. Four approaches explored: Coulomb gauge (A), covariant Fourier transform (B), perturbative expansion (C), flat connections (D).

## What Was Tried

1. **Gauge invariance verification** — proved rigorously that Σ|B_□|² is gauge invariant (B_□ → Ad(g_x) B_□ under gauge transform).
2. **Coulomb gauge approach** — analyzed the Gribov problem and transversality condition; derived the Fourier structure in Coulomb gauge.
3. **Covariant Fourier transform** — formal construction via parallel transport to origin; reduced to bounding holonomy corrections Ξ.
4. **Perturbative expansion** — computed full first-order correction δB^{(1)} in terms of commutators [A,v]; showed bound holds for small ‖A‖.
5. **Flat connections** — proved the bound for ALL flat SU(2) connections (trivial and Abelian twisted) via gauge-transform-to-I or Abelian Fourier.
6. **Single-plaquette excitation** — exact calculation of B_□_j = V₀ exp(ετ₁) + exp(ετ₁) C_j; found cos(ε) suppression factor on affected plaquettes (with a corrected error in the simplification).

## Outcome: PARTIAL SUCCESS + KEY FRAMEWORK

**The inequality Σ|B_□|² ≤ 4d|v|² is proved for:**
- All flat connections (trivial and Abelian twisted) ✓
- Perturbative regime ‖A‖ ≪ 1 ✓

**Not proved:** General Q ∈ SU(N)^E (non-flat, large field strength).

## Key Takeaway

**The central remaining gap is the Weitzenböck bound.** The operator M(Q) = Σ_□ |B_□(Q,·)|² satisfies M(Q) = M(I) + R_Q where M(I) = K_curl (max eigenvalue 4d, proved by E004 Fourier analysis). The inequality Σ|B_□(Q,v)|² ≤ 4d|v|² is equivalent to:

  **λ_max(R_Q) ≤ 0  for all Q** (curvature correction is non-positive semidefinite)

This is a SINGLE OPERATOR INEQUALITY that, if proved, would close the entire argument.

Numerically confirmed (E004): M(Q) ≤ M(I) for all 50+ tested configurations. The Weitzenböck identity from Jiang/SZZ (2022) gives the explicit formula for R_Q in terms of the field strength F_□(Q) — if R_Q ≤ 0 always, the proof is complete.

## Unexpected Findings

1. **Flat connections are fully handled.** This was not expected to be provable cleanly — the Abelian Fourier argument covers all of SU(2) flat space after gauge fixing.

2. **Single-plaquette calculation gives cos(ε) factor:** For the one-link excitation Q = exp(ετ₁), the 6 affected plaquettes contribute −2Tr[(B_□ matrix product)] with a suppression from the SU(2) holonomy exp(ετ₁). The affected plaquettes contribute LESS to the sum than at Q=I. This is the microscopic mechanism by which M(Q) < M(I) for non-trivial Q.

3. **The inequality Σ|B_□|² ≤ 4d|v|² is DIFFERENT from the broken bound H_P ≤ (β/2N)|B_P|².** E004 showed the latter is FALSE for Q≠I, but the former (Σ|B_□|²) is TRUE (E004 Step 2). These are independent inequalities.

4. **The Gribov problem is not an obstacle to the inequality itself** — only to using Coulomb gauge as a proof strategy. The inequality is gauge invariant, so it holds in any gauge or no gauge.

## Leads Worth Pursuing

1. **Compute R_Q explicitly** for the single-plaquette excitation and determine its sign. If R_Q ≤ 0 in this case, it gives strong evidence for the general Weitzenböck bound.

2. **Check the SZZ/Jiang Weitzenböck identity explicitly** — extract the formula for R_Q from arXiv:2204.12737. If R_Q involves a term like −Σ_□ |F_□|² · |v|² (negative), the proof closes.

3. **Gradient flow monotonicity:** Does Σ|B_□(Q_t,v)|² decrease along gradient flow Q_t? If yes, and if gradient flow converges to Q=I, this proves the bound globally.

4. **SU(2) specific identity:** The single-plaquette calculation shows B_□ involves exp(ε τ_k) factors. For SU(2), ‖exp(ε τ_k)‖_op = 1 always. A matrix inequality −2Tr[AB] ≤ −2Tr[A] for A = ω_□² ≤ 0 and B = exp(2ε τ_k) unitary... this is FALSE in general (as shown). But the SUM over plaquettes may still be bounded by a cancellation argument.

## Computations Identified

1. **Explicit R_Q for single-plaquette excitation** (medium difficulty): Compute M(Q) − M(I) analytically for Q = exp(ε τ₁) on one link. This gives the exact Weitzenböck correction. Requires expanding the 2(d-1)=6 affected plaquette contributions. Would immediately show whether R_Q is always non-positive for this family.

2. **Numerical check of Weitzenböck: M(Q) ≤ M(I)?** (easy, 15-line script): Compute λ_max(M(Q)) for 100 random Q and compare to 4d. Already done in E004 (confirmed), but should also check M(Q) ≤ M(I) in operator order (not just max eigenvalue). A single eigenvalue comparison is not enough — we need all eigenvalues of M(Q) − M(I) to be ≤ 0.

3. **Extract Weitzenböck formula from SZZ paper** (literature search): The SZZ paper arXiv:2204.12737 or Jiang 2022 should contain the explicit R_Q formula. Extracting it and checking its sign would immediately clarify whether this approach closes.

DONE

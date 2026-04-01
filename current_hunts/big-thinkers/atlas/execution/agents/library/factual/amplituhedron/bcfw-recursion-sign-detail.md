---
topic: BCFW recursion for 4-point MHV — sign convention from bracket antisymmetry
confidence: verified
date: 2026-03-27
source: amplituhedron strategy-001 exploration-001
---

## Finding

BCFW recursion on the 4-point MHV amplitude requires tracking a critical sign arising from the antisymmetry of spinor angle brackets (⟨ij⟩ = −⟨ji⟩). Naive sub-amplitude product gives the wrong sign; the correct formula includes an explicit (−1). This was verified both analytically (direct Cauchy residue) and numerically.

## [1,2⟩ Shift

Spinor shifts:
- |1̂⟩ = |1⟩ + z|2⟩ (holomorphic)
- |2̂] = |2] − z|1] (anti-holomorphic)
- |1̂] = |1], |2̂⟩ = |2⟩ (unchanged)

Preserves on-shell conditions and momentum conservation for all z.

## Pole Structure

The shifted amplitude A₄(z) = ⟨12⟩³/(⟨23⟩⟨34⟩(⟨41⟩ + z⟨42⟩)) has **exactly one pole** at z_A = −⟨14⟩/⟨24⟩ from ⟨41̂⟩ = 0. [VERIFIED analytically]

Corresponds to channel {4,1̂}|{2̂,3} with propagator P = p₁ + p₄.

At z_A, internal line K = p̂₁ + p₄ is on-shell (K² = 0), and the amplitude factorizes:

```
A₄ = A₃^{anti-MHV}(4⁺, 1̂⁻, (−P̂)⁺) × A₃^{MHV}(P̂⁻, 2̂⁻, 3⁺) / P²₁₄
```

## Critical Sign [VERIFIED]

The Parke-Taylor denominator contains ⟨41⟩ + z⟨42⟩. The propagator is P₁₄² = (⟨14⟩ + z⟨24⟩)[14].

Since ⟨41⟩ = −⟨14⟩:

```
⟨41⟩ + z⟨42⟩ = −(⟨14⟩ + z⟨24⟩) = −P₁₄²/[14]
```

This introduces a relative **(−1)** between the naive sub-amplitude product and the BCFW result:

```
A₄ = −(A_L × A_R / s₁₄)
```

Verified by direct Cauchy residue computation (independent of sub-amplitude factorization).

## Cross-Check: Direct Cauchy Method

An independent implementation evaluates A₄(z) = ⟨12⟩³/(⟨23⟩⟨34⟩(⟨41⟩+z⟨42⟩)) directly and extracts the residue without forming 3-point sub-amplitudes. This method:
- Avoids spinor extraction for the internal momentum
- Confirms the sign analytically
- Agrees with sub-amplitude BCFW and Parke-Taylor to machine precision

## Cost Analysis

- Operations (n=4): ~40 — compute z_A, shift spinors, extract K, compute 3 brackets for A_L and A_R, propagator, combine
- Terms (n=4): 1 diagram
- n-point scaling: O(n²) terms — BCFW reduces n-point to (n−1)-point, depth O(n), total terms grow quadratically. Each term involves only on-shell lower-point amplitudes (no off-shell or gauge-dependent quantities)

## Conceptual Note

BCFW is a genuine recursive method (not a formula), works for any tree amplitude (not just MHV), and never introduces off-shell or gauge-dependent quantities. The sign subtlety is a feature of the bracket antisymmetry convention and is absent in the other representations.

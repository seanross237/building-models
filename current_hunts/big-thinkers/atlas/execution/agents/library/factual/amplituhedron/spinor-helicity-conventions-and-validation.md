---
topic: Spinor-helicity formalism — conventions and numerical validation
confidence: verified
date: 2026-03-27
source: amplituhedron strategy-001 exploration-001
---

## Finding

A complete spinor-helicity implementation for 4-point massless kinematics was built and validated to machine precision. All standard identities hold to < 10⁻¹⁵.

## Conventions

- Metric signature: (+,-,-,-)
- σ^μ = (I, σ_x, σ_y, σ_z)
- Momentum matrix: p^{αα̇} = p_μ σ^μ = |p⟩[p| (rank-1 for massless)
- Angle bracket: ⟨ij⟩ = λ_i^1 λ_j^2 − λ_i^2 λ_j^1
- Square bracket: [ij] = λ̃_i^1 λ̃_j^2 − λ̃_i^2 λ̃_j^1
- Mandelstam: s_{ij} = ⟨ij⟩[ij]
  - Note: differs from (-,+,+,+) convention where s = ⟨ij⟩[ji]

## Spinor Extraction

Given lightlike p^μ, construct p^{αα̇} = p_μ σ^μ (rank-1 matrix). Factor as |p⟩[p| by selecting the dominant column for |p⟩ and dividing to get [p|. This is O(1).

## Validation Results [COMPUTED]

For COM kinematics with E=1, θ=π/3:

| Check | Result |
|---|---|
| Momentum conservation |Σp| < 10⁻¹⁵ | ✓ |
| Masslessness |p_i²| < 10⁻¹⁵ for all i | ✓ |
| Mandelstam (spinor vs 4-vector) | agree to 10⁻¹⁵ | ✓ |
| s + t + u = 0 | to 10⁻¹⁵ | ✓ |
| Schouten identity: ⟨12⟩⟨34⟩ + ⟨13⟩⟨42⟩ + ⟨14⟩⟨23⟩ = 0 | to machine precision | ✓ |

Validated across **8 distinct kinematic configurations** (4 COM, 4 random seeds).

## Kinematics Convention

`make_kinematics_com(E, θ)` generates 2→2 COM scattering with all-outgoing convention. The center-of-mass frame has particles 1,2 back-to-back along z, particles 3,4 deflected by angle θ.

## Note on Phase Conventions

Spinor extraction has a phase ambiguity. The implementation fixes this by selecting the dominant column of p^{αα̇}. Physical results (amplitudes, cross-sections) are phase-independent, but intermediate bracket values depend on the phase choice.

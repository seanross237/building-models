# Sprint 4: Do the Extra DOF Decouple?

**Date:** 2026-03-21
**Status:** FAIL — Mass degeneracy theorem kills simple decoupling. Possible ghost in spin-1 sector.

## The Question

In the s-wave condensate with Planck-scale gaps for the scalar and spin-1 modes, are the extra DOF effectively invisible at low energies, making FDCG indistinguishable from 2-DOF GR below some cutoff scale?

## Pass/Fail Criteria

- PASS: Extra modes get Planck-scale masses and decouple (effective GR below M_Pl)
- PARTIAL: Extra modes get masses but at a scale that could be experimentally relevant
- FAIL: Extra modes are massless or ghosts (theory is sick or ruled out)

## Calculator Result

### Mass Spectrum (Quadratic Action Around s-Wave Condensate)

The Calculator expanded A_ij = φ₀ δ_ij + a_ij with the Ginzburg-Landau potential V(A) = -μ² Tr(A²) + λ₁[Tr(A²)]² + λ₂ Tr(A⁴), performed SVT decomposition, and found:

| Mode | DOF | Speed² | Mass² | Ghost? |
|------|-----|--------|-------|--------|
| TT (graviton) | 2 | 2μg₁ | 8μλ₂φ₀² | No |
| Vector | 2 | μ(g₁ + g₂/2) | 8μλ₂φ₀² | No (q≠0) |
| Scalar (Φ=τ-σ) | 1 | 2μg₁ | 8μ(2λ₁+λ₂)φ₀² | No |

### THE MASS DEGENERACY THEOREM (Key New Result)

**For ANY SO(3)-invariant local potential around the isotropic s-wave condensate ⟨A_ij⟩ = φ₀ δ_ij, the TT modes and the vector modes get IDENTICAL masses: m_TT = m_V.**

This follows from **Schur's lemma**: the potential V depends on SO(3) invariants of A_ij. The mass matrix V''_{ijkl} must commute with SO(3) rotations. The TT and vector modes belong to the same representation once the mass matrix is restricted to the traceless sector. Therefore, they receive the same eigenvalue.

**Consequence:** It is IMPOSSIBLE to gap the vector without also gapping the graviton using local potential terms alone.

### Three Unacceptable Options

1. **g₂ = 0 exactly (by assumption)**: 2 DOF, matches GR. But requires gauge enhancement, which Sprint 3 showed fails.
2. **g₂ ≠ 0, λ₂ = 0 (massless graviton)**: 4 massless DOF (2 TT + 2 vector) + 1 massive scalar. The two massless vector modes mediate long-range spin-1 forces at gravitational strength. **Ruled out by Solar System tests.**
3. **g₂ ≠ 0, λ₂ ≠ 0 (massive graviton)**: 5 massive DOF. The graviton is massive → gravity has Yukawa decay → no 1/r² law. **Ruled out.**

### Speed Hierarchy (Lorentz Violation)

For g₂ ≠ 0:
- c_TT² = 2μg₁
- c_V² = μ(g₁ + g₂/2) ≠ c_TT² (Lorentz violation)
- c_Φ² = 2μg₁ = c_TT²

The vector propagates at a different speed than the graviton. Even at the enhanced point g₂ = 0, c_V² = μg₁ = c_TT²/2 — the vector still propagates at √(1/2) times the graviton speed. Matching c_V = c_TT requires g₂ = g₁, a special tuning.

### Scalar Mode: CAN Be Independently Gapped

At λ₂ = 0 (massless graviton/vector): m_Φ² = 16μλ₁φ₀². This CAN be at the Planck scale for O(1) λ₁. The scalar decouples. This is the one success of the decoupling hypothesis.

## Checker Result

The Checker used four independent methods:

1. **Hamiltonian constraint analysis**: Confirmed 5 DOF in condensed phase. The condensation does not change the constraint count.
2. **Dimensional analysis**: Found m_extra ~ coupling × M_Pl. Planck-scale masses are natural for O(1) couplings.
3. **Comparison with known theories**: The condensed Pretko theory resembles Einstein-Aether theory (same DOF decomposition: 2+2+1). All experimental bounds trivially satisfied for Planck-mass modes.
4. **Limiting cases**: g₂ → 0 gives enhanced gauge symmetry (vector becomes pure gauge). φ₀ → ∞ decouples all extra modes but also sends G → 0.

**Checker's verdict: PASS** — but the Checker's dimensional analysis MISSED the mass degeneracy theorem. The Checker assumed the vector mass scales independently as g₂ M_Pl, which the Calculator's explicit computation contradicts.

### Checker-Calculator Disagreement

The Checker's dimensional estimate (m_V ~ g₂ M_Pl) is incorrect. The actual mass computation shows m_V = m_TT = √(8μλ₂) φ₀, which does NOT scale with g₂. The g₂ coupling affects the SPEED of propagation, not the MASS. The mass comes entirely from the potential, and SO(3) symmetry forces m_TT = m_V.

**Resolution: Calculator wins.** The explicit computation trumps dimensional analysis. The Checker's method 2 fails because it does not account for the symmetry constraint on the mass matrix.

## Skeptic Attacks

### FATAL 1: Ghost Problem in Spin-1 Sector

Afxonidis et al. (2024, arXiv:2406.19268) found:
- The spin-1 modes have a dynamical instability (linear growth in time)
- The Hamiltonian for spin-1 modes is **always unbounded below**, regardless of coupling constants
- This cannot be fixed by any choice of g₁, g₂

**Calculator-Skeptic disagreement:** The Calculator found positive kinetic terms (no ghost by the ȧ² > 0 test). BUT the Afxonidis result refers to the full Hamiltonian (kinetic + gradient energy), not just the kinetic term. The gradient energy can be negative for certain momentum configurations even when the kinetic term is positive. This is the more standard definition of "ghost" / "instability."

**This requires further investigation.** The Calculator's kinetic-term ghost check is necessary but not sufficient. The full Hamiltonian boundedness requires checking that the total energy (kinetic + gradient + mass) is non-negative for all field configurations. The Afxonidis paper claims this fails for the spin-1 sector.

**Severity:** Potentially FATAL. If confirmed, FDCG cannot be a consistent quantum theory.

### FATAL 2: Scalar "Meissner Mechanism" is Wrong

The scalar (trace) mode is a gauge singlet — it does not transform under the fracton gauge symmetry. The Meissner/Anderson-Higgs mechanism gaps GAUGE bosons, not gauge singlets. The claim in GRAND-THEORY.md that the scalar is "gapped by Meissner mechanism at m ~ M_Pl" is conceptually incorrect.

The scalar CAN get a mass from the condensate potential (as the Calculator confirms: m_Φ² = 8μ(2λ₁+λ₂)φ₀²). This is legitimate — it's just not a Meissner mechanism. The mass is a free parameter set by the potential couplings, not predicted by a gauge mechanism.

### SERIOUS 3: Naturalness of g₂ = 0

The RG flow of g₂ is unknown. If g₂ is RG-relevant, it grows in the IR and the extra DOF become MORE prominent at low energies (fatal). If irrelevant, g₂ → 0 in the IR and the theory flows to GR (good). The one-loop beta function for g₂ has not been computed.

### SERIOUS 4: vDVZ Discontinuity Analog

If the vector modes are massless (as forced by the mass degeneracy theorem when the graviton is massless), they mediate long-range forces that modify gravity at O(1). There is no known Vainshtein-type screening mechanism for the Pretko theory.

### SERIOUS 5: Matter Coupling and Equivalence Principle

The extra modes generically couple to the stress-energy tensor and violate the equivalence principle. For Planck-mass modes this is unobservable, but the mass degeneracy theorem forces the vector to be massless if the graviton is massless — so the coupling IS observationally relevant.

## Synthesis and Verdict: FAIL

### What Sprint 4 Established

1. **The mass degeneracy theorem is the sprint's key result.** For any SO(3)-invariant local potential, m_TT = m_V. A massless graviton requires massless vectors. This is a clean, algebraic result from Schur's lemma.

2. **The scalar mode CAN be independently gapped** at the Planck scale. The "Meissner mechanism" language is wrong, but the condensate potential does give the scalar a mass.

3. **Ghost-free at the kinetic level** (all ȧ² terms positive). But this may not extend to the full Hamiltonian — Afxonidis et al. report the spin-1 Hamiltonian is unbounded below. This contradiction needs resolution.

4. **Three options, all bad:** (a) g₂ = 0 with gauge enhancement — fails per Sprint 3. (b) Massless graviton + massless vectors — ruled out observationally. (c) Massive everything — no long-range gravity.

5. **Possible escape routes:**
   - Derivative interactions (higher-order gradient terms) that break the m_TT = m_V degeneracy
   - Nematic (non-isotropic) condensation instead of s-wave
   - g₂ flowing to 0 under RG (making vectors gauge DOF, not massive DOF)
   - Nonlinear effects stabilizing the spin-1 sector (addressing the Afxonidis ghost)

### What FDCG's Status Is Now

| Claimed | Sprint 3 | Sprint 4 |
|---------|----------|----------|
| Scalar gapped by Meissner at M_Pl | — | Scalar gapped by potential (not Meissner). Mass is free parameter. |
| Extra DOF decouple | — | Vector CANNOT decouple independently (m_V = m_TT). |
| Theory is ghost-free | — | Kinetic terms OK. Full Hamiltonian may be unbounded (Afxonidis). |
| 5 DOF → effective 2 DOF | No resolution | FAILS for simple G-L potential. Derivative terms needed. |

### Recommended Next Sprint

**Sprint 5 should investigate whether derivative interactions (higher-order gradient terms) can break the mass degeneracy m_TT = m_V.** Specifically: terms like (∂_i A_jk)² Tr(A) in the effective action have different SVT structure from the potential and CAN distinguish TT from vector modes. This is the last realistic escape route for FDCG before confronting the possibility that the theory simply doesn't produce GR.

Alternatively, investigate the Afxonidis ghost claim in detail — if the spin-1 Hamiltonian is truly unbounded below, no amount of mass engineering saves the theory.

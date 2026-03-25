# Sprint 5: Can Derivative Interactions Break the Mass Degeneracy?

**Date:** 2026-03-21
**Status:** FAIL — Derivative interactions structurally cannot produce mass terms. Mass degeneracy is exact.

## The Question

Can higher-order gradient terms in the effective action (derivative interactions) break the Sprint 4 mass degeneracy theorem m_TT = m_V, allowing a massless graviton with massive vectors?

## Pass/Fail Criteria

- PASS: A specific derivative operator breaks the degeneracy, gapping vectors while keeping graviton massless
- PARTIAL: Derivative operators can break the degeneracy in principle but only with fine-tuning
- FAIL: The degeneracy is robust against all derivative corrections

## Calculator Result: FAIL

### Enumeration of Derivative Operators

The Calculator enumerated all independent SO(3)-invariant operators of the form (∂A)(∂A)(A) — the leading derivative interactions beyond the standard magnetic terms. Approximately 10 independent operators exist (O₁ through O₁₀), classified into:
- Laplacian-type: (∂_k A_ij)(∂_k A_ij) Tr(A)
- Cross-derivative: (∂_k A_ij)(∂_i A_kj) Tr(A)
- Divergence-type: (∂_j A_ij)(∂_k A_kj) Tr(A)
- A-directed: A_kl (∂_k A_ij)(∂_l A_ij)
- Mixed contractions

### SVT Decomposition Results

For each operator, expanding around ⟨A_ij⟩ = φ₀ δ_ij and collecting quadratic terms:

| Operator type | TT contribution | Vector contribution | Scalar contribution |
|--------------|-----------------|--------------------|--------------------|
| Q₁ = (∂_k a_ij)² | k² \|h̃^TT\|² | 2k⁴ \|Ṽ\|² | k² × scalar norms |
| Q₂ = (∂_k a_ij)(∂_i a_kj) | 0 | k⁴ \|Ṽ\|² | scalar terms |
| Q₃ = (∂_j a_ij)² | **0** | k⁴ \|Ṽ\|² | scalar terms |
| B² = B_kij B_kij | 2k² \|h̃^TT\|² | 2k⁴ \|Ṽ\|² | scalar terms |

**Key observations:**
- Divergence-type operators (Q₃) contribute to vectors but NOT TT — maximum speed discrimination
- ALL contributions are proportional to k^n (n ≥ 2) — they vanish at k=0
- The effect is always a speed (or higher-order dispersion) correction, NEVER a mass correction

### The Fundamental Theorem

**No derivative operator can produce a mass splitting between TT and vector modes around a spatially uniform condensate.**

**Proof:** Consider any local operator O containing N_d ≥ 1 spatial derivatives. When expanded around A_ij = φ₀ δ_ij + a_ij:
- Derivatives of the condensate: ∂(φ₀ δ_ij) = 0 (condensate is uniform)
- Therefore all N_d derivatives must act on fluctuation fields a_ij
- In Fourier space, each derivative produces a factor of ik_m
- At k = 0, the contribution of O to the quadratic action vanishes identically

Since the mass is defined as the k = 0 gap in the dispersion relation, no derivative operator contributes to the mass matrix. The mass matrix receives contributions EXCLUSIVELY from the potential V(A). For those, Schur's lemma forces m_TT = m_V (Sprint 4).  **QED.**

## Checker Result: FAIL (independently confirmed)

### Method 1: Representation Theory
At k = 0, the full SO(3) symmetry is restored (no preferred direction from momentum). The traceless sector is the irreducible spin-2 representation. Schur's lemma forces all traceless modes to have the same eigenvalue. Derivative operators, being k-dependent, cannot contribute at k = 0.

### Method 2: EFT Counting
Enumerated all SO(3)-invariant quadratic operators up to 4 derivatives. Each operator involving spatial derivatives produces terms proportional to k^(2n) with n ≥ 1. At k = 0, all vanish. The mass (k = 0 value) is determined exclusively by the potential.

### Method 3: Liquid Crystal Analogy
In nematic liquid crystals, the Frank elastic constants K₁, K₂, K₃ differ because the nematic condensate BREAKS SO(3). For an isotropic condensate (which preserves SO(3)), the analog of the mass matrix is degenerate. This confirms: mass splitting requires anisotropic condensation.

### Method 4: Weinberg Consistency
No fundamental obstruction from soft graviton theorems to having m_V ≠ m_TT — the constraint is purely from the internal symmetry structure (SO(3) + isotropic condensate), not from Lorentz or gravity consistency.

### Checker Summary
The mass degeneracy is robust against ALL local derivative corrections for the isotropic condensate. Speed splitting IS possible (and already present: c_TT ≠ c_V from g₂). Mass splitting is NOT.

## Skeptic Attacks

### Attack 1: Schur's Lemma and Derivatives — BENIGN
Attack confirms the degeneracy rather than threatening it. At k = 0, full SO(3) is restored.

### Attack 2: Derivatives Vanish at k=0 — FATAL (for Sprint 5 hypothesis)
The core argument: derivative interactions are k-dependent BY DEFINITION. Mass is k-INDEPENDENT by definition. These are structurally incompatible. Derivative interactions cannot produce mass terms. Period.

### Attack 3: Condensate-Derivative Cross Terms — FATAL (confirms Attack 2)
Cross terms like φ₀ × (∂a)(∂a) still vanish at k = 0. The condensate provides amplitude (φ₀) but no momentum. Only derivatives of fluctuation fields provide momentum, and those vanish at k = 0.

### Attack 4: Naturalness — SERIOUS (academic given Attacks 2-3)
Even if derivative interactions could split masses, the required hierarchy (m_TT = 0 exactly, m_V ~ M_Pl) would need to be radiatively stable.

### Attack 5: Goldstone Protection Extends to Vectors — FATAL
**The deepest result of Sprint 5.** Loop corrections (Coleman-Weinberg potential) are SO(3)-invariant. Schur's lemma applies to the radiatively corrected mass matrix. Therefore:
- The Goldstone theorem forces δm_TT = 0 (graviton stays massless)
- Schur's lemma forces δm_V = δm_TT = 0 (vector inherits protection)

**The vectors are "accidentally massless" — protected not by their own symmetry, but by sharing a representation with the graviton.** This holds to ALL loop orders.

### Attack 6: Spin-1 Ghost — FATAL (independent of Sprint 5)
The Afxonidis ghost persists regardless of mass engineering. A massive ghost is WORSE (faster instability rate). Even if Sprint 5 succeeded, the ghost would kill the theory.

## Synthesis: FAIL

### What Sprint 5 Established

1. **The mass degeneracy m_TT = m_V is EXACT to all orders in the derivative expansion and to all loop orders.** The argument rests on two pillars: (a) derivative operators contribute zero at k=0, and (b) Schur's lemma constrains the potential at k=0.

2. **Derivative operators CAN and DO distinguish TT from vector in the gradient sector** — different speeds, different higher-order dispersion. But speed ≠ mass.

3. **The Goldstone protection of the graviton extends to the vectors via Schur's lemma.** Even radiative corrections cannot split the masses. The vectors are "accidentally massless" at every order in perturbation theory.

4. **The ONLY remaining structural escape route is nematic condensation** (breaking SO(3)). In a nematic condensate, TT and vector modes belong to different SO(2) representations, and Schur's lemma no longer forces degenerate masses.

### Updated Escape Route Assessment

| Escape Route | Status After Sprint 5 |
|-------------|----------------------|
| Derivative interactions | **DEAD** — proven impossible |
| Nematic condensation | **ONLY VIABLE STRUCTURAL ROUTE** — breaks SO(3), allows mass splitting |
| g₂ → 0 under RG | Still open — requires beta function computation |
| Accept 5-DOF modified gravity | Always available as fallback |
| Nonlinear stabilization of ghost | Open but speculative |

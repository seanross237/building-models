# Research Sprints — Knowledge Document

Accumulated findings from focused sprint investigations.

## Foundation

This loop builds on FDCG (Fracton Dipole Condensate Gravity), established by prior research:
- Spacetime = fracton dipole condensate
- Graviton = Goldstone boson of dipole condensation
- ~~Linearized AND nonlinear GR reproduced~~ **CAVEAT (Sprint 3):** Only the spin-2 TT sector matches GR. The full theory has 5 DOF, not 2. See Sprint 3 reassessment.
- ~~Gauge enhancement algebraically proven~~ **RETRACTED (Sprint 3):** Iterations 10/12 of prior research showed gauge enhancement FAILS. GRAND-THEORY.md contradicts these findings.
- Oppenheim prediction: σ_a = √(Gℏ/R³)
- See ~/kingdom_of_god/science/previous-attempts/03-grand-unified-theory/GRAND-THEORY.md for full details

## Completed Sprints

### Sprint 1: Oppenheim Prediction Analysis (2026-03-21) — PARTIAL PASS

**Question:** Where does FDCG's Oppenheim prediction sit relative to other models and experiments?

**Results:**
- σ_a = √(Gℏ/R³) is **not unique to FDCG** — any gravitational decoherence model with DP-like scaling at saturation gives the identical formula. FDCG's unique contribution is the physical mechanism for WHY saturation occurs.
- FDCG scaling (R⁻³/²) IS distinguishable from unsaturated DP/KTM scaling (R⁻²). Key diagnostic: FDCG predicts mass-independent noise at fixed radius.
- FDCG evades Donadi et al. (2021) constraint that killed parameter-free DP because it predicts less noise at small scales.
- **Best experimental prospect:** Diamond microsphere (R ~ 1-10 μm) with next-gen optomechanics, but current experiments are 5-6 OOM away from required sensitivity.
- **Smoking gun test:** Measure σ_a for objects of same R but different density. FDCG predicts identical noise; other models predict density-dependent difference.
- **Open issue:** Frequency spectrum of noise unspecified (white vs. 1/f²). Could change SNR estimates by orders of magnitude.
- **Open issue:** Saturation assumed, not derived from fracton condensate.

**Files:** Moved to `~/kingdom_of_god/science/grand-unified-theory/oppenheim-prediction-analysis/` (sprint-01-oppenheim.md, sprint-01-oppenheim-predictions.md, sprint-01-skeptic-review.md)

### Sprint 2: Noise Spectrum Derivation (2026-03-21) — PARTIAL PASS

**Question:** What is the full acceleration noise PSD S_a(f) for a test mass embedded in the fracton condensate ground state?

**Results:**
- **Parametric scaling S_a ~ Gℏ/R³ is derivable** from zero-point fluctuations of the Pretko field with UV cutoff at k_max ~ 1/R (test mass size). Calculator obtained S_a = Gℏ/(2π²R³). Confirmed by dimensional analysis and zero-point fluctuation estimates.
- **Spectrum is approximately white** at all laboratory frequencies. Roll-off at f ~ c/(2πR) ~ 10¹⁵ Hz. Subtle f vs f³ dependence within lab band unresolved.
- **FDCG predicts much more noise than standard perturbative QG.** Standard QG vacuum noise goes as f⁵ (unmeasurably small at lab frequencies). FDCG gives flat noise many OOM larger. This IS distinctive.
- **The c-independence of Gℏ/R³ is a genuine FDCG signature.** In FDCG, c = √(ρ_s/χ) is derived. The noise formula not involving c is consistent with this.

**Fatal Gaps Identified:**
1. **The h_00 construction is missing.** A_ij is spatial (i,j=1,2,3). Gravitational acceleration requires h_00. The Stueckelberg mechanism should produce h_00 from Goldstone modes, but this has NOT been explicitly constructed. Without h_00, acceleration noise cannot rigorously be computed.
2. **The Oppenheim bound framing is a category error.** The Oppenheim bound assumes gravity is fundamentally classical (CQ framework). FDCG is fundamentally quantum. These are incompatible. FDCG should NOT claim to "saturate the Oppenheim bound" — it should claim the condensate's zero-point fluctuations produce noise that numerically coincides with the bound.

**Recommended Reframing:** "FDCG predicts acceleration noise S_a = Gℏ/(2π²R³) from ground-state fluctuations of the fracton condensate, via zero-point metric noise with UV cutoff at the test mass scale. This coincides with the Oppenheim decoherence-diffusion bound, suggesting a deep connection between condensate quantum fluctuations and the CQ gravity framework."

**Files:** sprints/sprint-02-noise-spectrum.md

### Sprint 3: Construct h_00 from Stueckelberg Sector (2026-03-21) — FAIL

**Question:** Does the Stueckelberg/Goldstone sector of the condensed Pretko theory produce h_00 with ∇²h_00 = -8πG T_00?

**Results:**
- **The Stueckelberg/Goldstone construction FAILS.** Three fatal problems:
  1. **Gauge enhancement was already disproven** by iterations 10/12 of the prior research loop. GRAND-THEORY.md contradicts these findings without resolving the objections.
  2. **The theory has 5 propagating DOF, not 2.** Established by Afxonidis et al. (2024, arXiv:2406.19268) and confirmed by prior research. The extra scalar mode is a gauge singlet — cannot be removed by any mechanism.
  3. **Stueckelberg fields are gauge artifacts** (pure gauge, can be set to zero). h_00 must be physical (determines Newtonian potential). These are logically incompatible.

- **A partial alternative exists:** The Pretko theory's full (non-gauge-fixed) formulation includes A_00 as a Lagrange multiplier enforcing the Gauss law. Defining h_00 = (2/c²)∇²A_00 converts the biharmonic equation ∇⁴A_00 = ρ/χ into the Poisson equation ∇²h_00 = -8πG ρ/c². This gives G = c²/(4πρ_s). BUT this requires a derivative field redefinition (not a direct identification) and does NOT resolve the 5-DOF problem.

- **The Gauss law has wrong differential structure.** ∂_i∂_j E^ij (double divergence) ≠ ∇²(Tr E) (Laplacian of trace). Potentially salvageable in the trace sector of the s-wave condensate but not demonstrated.

**Critical Reassessment of FDCG:**

| Claimed | Actual |
|---------|--------|
| Gauge enhancement proven | Gauge enhancement shown to FAIL (iterations 10/12) |
| Linearized GR reproduced | Only spin-2 TT sector matches; 5 DOF total |
| Graviton propagator matches GR | Only at special point g₂=0 |
| Stueckelberg gives h_00 | Stueckelberg fields are gauge artifacts |

**What FDCG genuinely achieves:**
1. Produces a massless spin-2 mode (graviton) as a Goldstone boson
2. Gives c and G from condensate parameters
3. Noise prediction S_a ~ Gℏ/R³ from zero-point fluctuations
4. h_00 extractable via A_00 constraint structure (derivative relation)

**What FDCG cannot currently do:**
1. Match linearized GR in all sectors (extra spin-1 + spin-0 DOF)
2. Couple to arbitrary matter (only fracton charges)
3. Demonstrate gauge enhancement
4. Explain why extra DOF are unobserved

**Files:** sprints/sprint-03-h00-construction.md

## Key Findings

1. **The "saturated Oppenheim bound" is a model class, not a specific theory.** S_a = Gℏ/R³ characterizes any model where gravitational decoherence follows DP scaling and the decoherence-diffusion trade-off is saturated. FDCG, KTM-at-saturation, and generic-DP-at-saturation all give this prediction.

2. **Mass-independence at fixed radius is the experimental diagnostic for the saturated class.** This distinguishes saturated models from unsaturated ones (where noise depends on both m and R).

3. **~~Deriving saturation from the condensate~~ PARTIALLY RESOLVED (Sprint 2).** Zero-point fluctuations with k_max ~ 1/R reproduce S_a ~ Gℏ/R³. The "saturation" is reinterpreted as: ground-state condensate fluctuations produce the minimum possible noise. This is natural at T=0 (no fine-tuning). However, the Oppenheim bound itself doesn't apply to a fully quantum theory — the coincidence needs a deeper explanation.

4. **~~The noise frequency spectrum~~ PARTIALLY RESOLVED (Sprint 2).** The spectrum is white (frequency-independent) at f ≪ c/R, which includes ALL laboratory frequencies. Detailed spectral shape (white vs f³ from phonon modes) within the lab band remains uncertain but experimentally the difference is small over narrow bandwidth.

5. **~~The h_00 structural gap~~ ADDRESSED BUT NOT RESOLVED (Sprint 3).** The Stueckelberg route fails (gauge artifacts, gauge enhancement disproven). The A_00 Lagrange multiplier route gives h_00 = (2/c²)∇²A_00, which formally produces the Poisson equation. But this is a derivative relation, not a direct identification, and it doesn't fix the 5-DOF problem.

6. **FDCG noise is DISTINCTIVE from standard QG.** Standard perturbative quantum gravity gives acceleration noise ∝ f⁵ (vanishing at low frequencies). FDCG gives flat noise ~ Gℏ/R³. This is because FDCG's condensate provides a physical mechanism (zero-point condensate fluctuations) that standard QFT-on-curved-spacetime does not have.

7. **The c-independence of Gℏ/R³ is a non-trivial consistency check.** In FDCG, c is emergent. A prediction that doesn't involve c is naturally expressible in pre-geometric (fracton) variables, as expected.

8. **FDCG has 5 propagating DOF, not 2 (Sprint 3).** This is the MOST CRITICAL finding. The condensed Pretko theory produces 2 spin-2 + 2 spin-1 + 1 spin-0 modes. The scalar is a gauge singlet. The spin-1 modes may be ghosts. Published by Afxonidis et al. (2024). The theory is NOT equivalent to linearized GR.

9. **The gauge enhancement claim in GRAND-THEORY.md is WRONG (Sprint 3).** Iterations 10/12 of the prior research demonstrated gauge enhancement fails with four rigorous arguments. The GRAND-THEORY.md summary contradicts these without resolution. This must be corrected.

10. **h_00 CAN be extracted via A_00 constraint, not Stueckelberg (Sprint 3).** The full Pretko theory includes A_00 as a Lagrange multiplier. Via derivative relation h_00 = (2/c²)∇²A_00, the Poisson equation emerges. G = c²/(4πρ_s).

### Sprint 4: Extra DOF Decoupling (2026-03-21) — FAIL

**Question:** Do the extra 3 DOF (2 spin-1 + 1 spin-0) acquire Planck-scale masses and decouple in the s-wave condensate?

**Results:**

- **MASS DEGENERACY THEOREM (Key New Result):** For ANY SO(3)-invariant local potential around the isotropic condensate, the TT graviton and vector modes get IDENTICAL masses: m_TT = m_V. This follows from Schur's lemma. It is IMPOSSIBLE to gap the vector without also gapping the graviton using local potential terms alone.

- **Scalar CAN be independently gapped.** m_Φ² = 8μ(2λ₁+λ₂)φ₀². At λ₂ = 0 (massless graviton), m_Φ can be at the Planck scale. The "Meissner mechanism" language is wrong (scalar is a gauge singlet), but the condensate potential legitimately gives it a mass.

- **Three options, all bad:**
  1. g₂ = 0 (gauge enhancement): Sprint 3 showed this fails.
  2. g₂ ≠ 0, λ₂ = 0 (massless graviton): Forces 4 massless DOF (2 TT + 2 vector). Extra long-range vector forces ruled out by Solar System tests.
  3. g₂ ≠ 0, λ₂ ≠ 0 (massive graviton): All 5 modes massive. No long-range 1/r² gravity.

- **Ghost-free at kinetic level** (all ȧ² terms positive). But Afxonidis et al. (2024) report the spin-1 HAMILTONIAN is unbounded below (including gradient energy). These are compatible — positive kinetic term ≠ bounded Hamiltonian. Further investigation needed.

- **Speed hierarchy (Lorentz violation):** c_V² = μ(g₁ + g₂/2) ≠ c_TT² = 2μg₁ for g₂ ≠ 0. Even at g₂ = 0, c_V = c_TT/√2. Matching speeds requires g₂ = g₁ (special tuning).

- **Possible escape routes:** (1) Derivative interactions that break m_TT = m_V degeneracy; (2) Nematic condensation instead of s-wave; (3) g₂ → 0 under RG flow; (4) Nonlinear stabilization of spin-1 sector.

**Files:** sprints/sprint-04-extra-dof-decoupling.md

### Sprint 5: Derivative Interactions and Mass Degeneracy (2026-03-21) — FAIL

**Question:** Can higher-order gradient terms (derivative interactions) in the effective action break the mass degeneracy m_TT = m_V?

**Results:**

- **Derivative interactions CANNOT produce mass terms.** Proven by all three agents independently. The argument: "mass" = k=0 gap; derivative interactions produce terms ∝ k^n (n≥1) in Fourier space; at k=0, all derivative contributions vanish identically. This holds because the s-wave condensate is spatially uniform (∂(condensate) = 0), so all derivatives must act on fluctuation fields.

- **The mass degeneracy is EXACT to all orders in the derivative expansion.** No local operator with spatial derivatives can contribute to the k=0 mass matrix around a uniform condensate. The mass is determined exclusively by the potential V(A).

- **Goldstone protection extends to vectors via Schur's lemma at all loop orders.** The Coleman-Weinberg effective potential (one-loop and beyond) is SO(3)-invariant. Schur's lemma applies to the radiatively corrected mass matrix. The Goldstone theorem forces δm_TT = 0; Schur forces δm_V = δm_TT = 0. The vectors are "accidentally massless" — protected by sharing a representation with the graviton.

- **Derivative operators DO distinguish TT from vector in the gradient sector.** Divergence-type operators (∂_j a_ij)² contribute to vectors but NOT TT. This is why c_TT ≠ c_V. But speed ≠ mass.

- **The ONLY remaining structural escape is nematic condensation** (breaking SO(3) → SO(2) or lower). In a nematic condensate, TT and vector modes belong to different irreducible representations. Schur's lemma no longer forces degenerate masses.

**Files:** sprints/sprint-05-derivative-mass-splitting.md

### Sprint 6: Nematic Condensation (2026-03-21) — FAIL

**Question:** Can a nematic (anisotropic) condensate ⟨A_ij⟩ = diag(φ_∥, φ_⊥, φ_⊥) save FDCG by allowing independent masses for the graviton and vector modes?

**Results:**

- **NEMATIC NO-GO THEOREM:** The nematic produces the OPPOSITE mass hierarchy from what gravity needs. The m=±1 modes (vectors) are MASSLESS Goldstones of SO(3)→SO(2). The m=±2 modes (graviton candidates) are MASSIVE with m² = |4λ₂|φ_⊥Δ. This is because SO(3) generators are spin-1, so breaking SO(3)→SO(2) produces spin-1 Goldstones, NOT spin-2.

- **Anisotropic gravity ruled out.** A nematic condensate predicts gravitational anisotropy ε ~ S (nematic order parameter). For useful mass splitting, S ~ O(1). Current bounds: ε ≲ 10⁻¹⁰ to 10⁻¹⁵. Ruled out by 10+ orders of magnitude.

- **Cosmological alignment problem.** The nematic director must be uniform across the observable universe. Domain walls from phase transition have Planck-scale tension, excluded by ~90 orders of magnitude.

- **To get spin-2 Goldstones, you need spin-2 symmetry generators — i.e., diffeomorphisms.** This is circular: it requires what FDCG is trying to derive.

- **The spin-1 ghost (Afxonidis) persists regardless of condensate type.** It comes from the Pretko kinetic structure, not the potential.

**Files:** sprints/sprint-06-nematic-condensation.md

## Key Findings

1. **The "saturated Oppenheim bound" is a model class, not a specific theory.** S_a = Gℏ/R³ characterizes any model where gravitational decoherence follows DP scaling and the decoherence-diffusion trade-off is saturated. FDCG, KTM-at-saturation, and generic-DP-at-saturation all give this prediction.

2. **Mass-independence at fixed radius is the experimental diagnostic for the saturated class.** This distinguishes saturated models from unsaturated ones (where noise depends on both m and R).

3. **~~Deriving saturation from the condensate~~ PARTIALLY RESOLVED (Sprint 2).** Zero-point fluctuations with k_max ~ 1/R reproduce S_a ~ Gℏ/R³. The "saturation" is reinterpreted as: ground-state condensate fluctuations produce the minimum possible noise. This is natural at T=0 (no fine-tuning). However, the Oppenheim bound itself doesn't apply to a fully quantum theory — the coincidence needs a deeper explanation.

4. **~~The noise frequency spectrum~~ PARTIALLY RESOLVED (Sprint 2).** The spectrum is white (frequency-independent) at f ≪ c/R, which includes ALL laboratory frequencies. Detailed spectral shape (white vs f³ from phonon modes) within the lab band remains uncertain but experimentally the difference is small over narrow bandwidth.

5. **~~The h_00 structural gap~~ ADDRESSED BUT NOT RESOLVED (Sprint 3).** The Stueckelberg route fails (gauge artifacts, gauge enhancement disproven). The A_00 Lagrange multiplier route gives h_00 = (2/c²)∇²A_00, which formally produces the Poisson equation. But this is a derivative relation, not a direct identification, and it doesn't fix the 5-DOF problem.

6. **FDCG noise is DISTINCTIVE from standard QG.** Standard perturbative quantum gravity gives acceleration noise ∝ f⁵ (vanishing at low frequencies). FDCG gives flat noise ~ Gℏ/R³. This is because FDCG's condensate provides a physical mechanism (zero-point condensate fluctuations) that standard QFT-on-curved-spacetime does not have.

7. **The c-independence of Gℏ/R³ is a non-trivial consistency check.** In FDCG, c is emergent. A prediction that doesn't involve c is naturally expressible in pre-geometric (fracton) variables, as expected.

8. **FDCG has 5 propagating DOF, not 2 (Sprint 3).** This is the MOST CRITICAL finding. The condensed Pretko theory produces 2 spin-2 + 2 spin-1 + 1 spin-0 modes. The scalar is a gauge singlet. The spin-1 modes may be ghosts. Published by Afxonidis et al. (2024). The theory is NOT equivalent to linearized GR.

9. **The gauge enhancement claim in GRAND-THEORY.md is WRONG (Sprint 3).** Iterations 10/12 of the prior research demonstrated gauge enhancement fails with four rigorous arguments. The GRAND-THEORY.md summary contradicts these without resolution. This must be corrected.

10. **h_00 CAN be extracted via A_00 constraint, not Stueckelberg (Sprint 3).** The full Pretko theory includes A_00 as a Lagrange multiplier. Via derivative relation h_00 = (2/c²)∇²A_00, the Poisson equation emerges. G = c²/(4πρ_s).

11. **MASS DEGENERACY THEOREM (Sprint 4): m_TT = m_V for any SO(3)-invariant local potential.** Schur's lemma forces the graviton and vector modes to have identical masses around the isotropic (s-wave) condensate. This makes simple decoupling (gap vectors but not graviton) IMPOSSIBLE with potential terms alone.

12. **The scalar "Meissner mechanism" is conceptually wrong (Sprint 4).** The scalar is a gauge singlet — the Meissner/Higgs mechanism does not apply to it. The scalar IS gapped by the condensate potential (a legitimate mechanism), but the mass is a free parameter, not predicted by a gauge mechanism.

13. **Speed hierarchy violates Lorentz invariance (Sprint 4).** The vector mode propagates at c_V ≠ c_TT for g₂ ≠ 0. Matching c_V = c_TT requires g₂ = g₁ (special tuning). This is a separate problem from the mass degeneracy.

14. **The mass degeneracy is EXACT to all orders in the derivative expansion (Sprint 5).** No local derivative operator can contribute to the k=0 mass matrix around a spatially uniform condensate. The mass is determined exclusively by the potential. This closes the "derivative interaction" escape route from Sprint 4.

15. **Goldstone protection extends to vectors via Schur's lemma (Sprint 5).** Even radiative corrections (Coleman-Weinberg) cannot split the masses. The vectors are "accidentally massless" — protected not by their own symmetry, but by sharing a representation with the Goldstone graviton. This holds to all loop orders.

16. **~~Nematic condensation is the ONLY remaining structural escape (Sprint 5).~~ ELIMINATED (Sprint 6).** The nematic produces the wrong mass hierarchy: massless vectors (Goldstones) and massive graviton candidates (not Goldstones). SO(3) → SO(2) gives spin-1 Goldstones, not spin-2.

17. **The Nematic No-Go Theorem (Sprint 6): SO(3) breaking cannot produce spin-2 Goldstones.** SO(3) generators are spin-1 (J_x, J_y, J_z). Any breaking SO(3) → H produces Goldstones with spin ≤ 1. To get massless spin-2 modes as Goldstones, one needs a symmetry group with spin-2 generators — i.e., diffeomorphism invariance. This is circular for an emergent gravity theory.

18. **FDCG as emergent GR is ruled out at the Pretko level (Sprints 3-6).** Every structural mechanism for recovering 2-DOF GR has been eliminated: gauge enhancement (Sprint 3), mass decoupling (Sprint 4), derivative interactions (Sprint 5), radiative corrections (Sprint 5), nematic condensation (Sprint 6). The Pretko rank-2 symmetric tensor gauge theory cannot produce emergent GR.

19. **~~The only untested mechanism is RG flow of g₂ → 0.~~ ELIMINATED (Sprint 7).** The pure Pretko theory is Gaussian (free) — g₂ does not run. In the condensed phase, interactions exist but don't drive g₂ → 0. The fracton-elasticity duality shows g₂ (elastic anisotropy) is stable. g₂ = 0 is a protected fixed point but NOT an attractor.

20. **FDCG as emergent GR is ruled out (Sprints 3-7).** Every mechanism tested and eliminated. The fundamental circularity: a massless spin-2 particle requires diffeomorphism invariance (either as gauge symmetry or as a broken symmetry with spin-2 generators), which is what the theory is trying to derive.

## Emerging Patterns

1. **FDCG's predictions are parametrically correct but structurally flawed.** Sprints 1-2 find the right scaling laws. Sprints 3-4 reveal the structural foundation is broken at multiple levels.

2. **The Oppenheim connection is a red herring for FDCG.** FDCG should frame its predictions in terms of condensate physics (zero-point fluctuations, emergent decoherence), not in terms of the CQ framework (which assumes classical gravity).

3. **FDCG's best feature is its physical mechanism, not its formal structure.** The microscopic picture (condensate → gravitons) is valuable. But the Pretko theory as currently formulated is NOT linearized GR — it's a modified gravity theory with extra DOF that cannot be simply decoupled.

4. **The Pretko theory is a dead end for emergent GR (Sprints 3-6).** S-wave: gauge enhancement fails (3), mass degeneracy (4-5). Nematic: wrong Goldstones — spin-1 not spin-2 (6). BOTH condensate types fail. The fundamental issue: to get a massless spin-2 particle as a Goldstone, you need spin-2 symmetry generators (diffeomorphisms), which is what you're trying to derive.

5. **Research summaries cannot be trusted at face value.** Sprint 3 discovered that GRAND-THEORY.md's claims contradict the detailed calculations that preceded it. Sprint 4 found that the Checker's dimensional estimates disagree with the Calculator's explicit algebra. Always verify with explicit computation.

6. **FDCG faces a cascade of structural failures:** gauge enhancement fails (Sprint 3), simple decoupling fails (Sprint 4), derivative interactions can't help (Sprint 5), Meissner mechanism claim is wrong (Sprint 4), and spin-1 Hamiltonian may be unbounded below (Afxonidis et al.). These stem from the fundamental mismatch between Pretko gauge symmetry (1 scalar parameter) and GR's diffeomorphism symmetry (4 parameters).

7. **FDCG has reached a terminal verdict on emergent GR.** After 6 sprints (0 PASS, 2 PARTIAL, 4 FAIL), every structural mechanism for recovering GR from the Pretko theory has been eliminated. The remaining options are: (a) RG flow of g₂ → 0 (the one untested mechanism), (b) accept 5-DOF modified gravity, (c) pivot to a different fracton theory, or (d) abandon FDCG.

8. **The circularity problem is fundamental.** To get a massless spin-2 particle (graviton), you need either gauge enhancement to diffeomorphisms (fails, Sprint 3) or spin-2 Goldstone bosons from a broken symmetry with spin-2 generators (which IS diffeomorphism invariance). There is no third option within the standard framework. This suggests that emergent gravity from a rank-2 symmetric tensor may require a fundamentally different mechanism than condensation + Goldstone.

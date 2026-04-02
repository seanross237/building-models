# Exploration 003: Lee-Wick Quantum Gravity — Full Viability Assessment

## Goal
Comprehensive assessment of Lee-Wick quantum gravity as a complete theory of quantum gravity, with focus on unitarity status, comparison to QG+F (Anselmi's fakeon approach), and viability as our primary construction target.

---

## Task 1: Reconstruct the Theory

### Key Papers Found

1. **Modesto & Shapiro, "Superrenormalizable quantum gravity with complex ghosts"** (arXiv: 1512.07600, Phys. Lett. B 755, 2016)
   - First proposal of superrenormalizable QG with complex ghost poles
   - Higher-derivative terms arranged so ALL unphysical massive states have complex poles
   - Claims unitarity via Lee-Wick quantization

2. **Leonardo Modesto, "Super-renormalizable or Finite Lee-Wick Quantum Gravity"** (arXiv: 1602.02421, Nucl. Phys. B 909, 2016)
   - THE founding paper for Lee-Wick quantum gravity
   - Extends to arbitrary dimensions and arbitrary numbers of complex pole pairs
   - Super-renormalizable in even dimensions, finite in odd dimensions
   - Computes singularity-free Newtonian potentials
   - Spectrum: graviton + "anti-gravitons" (short-lived, repulsive at short distances)

3. **Anselmi & Piva, "A new formulation of Lee-Wick quantum field theory"** (arXiv: 1703.04584, JHEP 2017)
   - Reformulates Lee-Wick QFT using nonanalytically Wick-rotated Euclidean theories
   - Proves one-loop unitarity with only physical DOF in cuts
   - This is the bridge paper where Anselmi begins developing the fakeon from Lee-Wick ideas

4. **Anselmi, "On the quantum field theory of the gravitational interactions"** (arXiv: 1704.07728, JHEP 2017)
   - Anselmi's quantum gravity theory — uses the SAME action as Stelle but with fakeon prescription
   - Action: linear combination of R, R_μν R^μν, R², and cosmological term
   - Only the graviton propagates in cutting equations → unitarity

5. **Anselmi & Piva, "Quantum Gravity, Fakeons And Microcausality"** (arXiv: 1806.03605, JHEP 2018)
   - Graviton multiplet: massless spin-2 (h_μν) + massive scalar (φ) + spin-2 fakeon (χ_μν)
   - Width of χ_μν is NEGATIVE → microcausality violation at energies > fakeon mass
   - One-loop investigation confirms unitarity with fakeon prescription

6. **Kubo & Kugo, "Unitarity Violation in Field Theories of Lee-Wick's Complex Ghost"** (arXiv: 2308.09006, PTEP 2023)
   - CRITICAL: Proves unitarity IS violated above threshold with LW prescription
   - Complex ghosts are actually created, contradicting Lee-Wick's original argument

7. **Anselmi, "Purely virtual particles versus Lee-Wick ghosts"** (arXiv: 2202.10483, Phys. Rev. D 105, 2022)
   - Three fatal problems with LW: non-Hermitian classical limit, unbounded Hamiltonian, observation clash
   - Proposed fix breaks general covariance → can't apply to gravity

8. **⭐ Anselmi, Briscese, Calcagni, & Modesto, "Amplitude prescriptions in field theories with complex poles"** (arXiv: 2503.01841, JHEP05(2025)145, March 2025)
   - **THE DEFINITIVE PAPER** — co-authored by BOTH Anselmi AND Modesto
   - Compares four inequivalent prescriptions for handling complex poles
   - **VERDICT: Only the fakeon/AP prescription is physically viable**

9. **Asorey, Krein, Pardina & Shapiro, "Bound states of massive complex ghosts in superrenormalizable QG theories"** (arXiv: 2408.16514, JHEP 2025)
   - Complex ghost pairs can form bound states confining unphysical excitations
   - BUT: theory "does not admit a Källén-Lehmann representation and does not satisfy the positivity criterion"
   - Confinement strategy, not unitarity restoration

10. **Oda, "Bound States in Lee's Complex Ghost Model"** (arXiv: 2602.05562, Feb 2026)
    - Shows "bound states cannot be created from ghosts by contributions of a complex delta function"
    - "Violation of the unitarity is also connected to the non-existence of bound states"
    - Does NOT resolve the ghost problem

11. **Buoninfante, "Remarks on ghost resonances"** (arXiv: 2501.04097, JHEP 2025)
    - Ghost propagator has complex conjugate poles in FIRST Riemann sheet (unlike ordinary resonances which have poles only in second sheet)
    - Clarifies differences between ghost resonance and ordinary resonance for Feynman, anti-Feynman, and fakeon prescriptions

12. **Modesto, Rachwał & Shapiro, "Renormalization group in super-renormalizable quantum gravity"** (Eur. Phys. J. C 78, 555, 2018)
    - Derives one-loop beta functions for six-derivative Lee-Wick QG
    - RG flow of four-derivative couplings (Weyl², R², Gauss-Bonnet)

### Action and Propagator Structure

**The Action (Quadratic/Stelle-type):**
The simplest Lee-Wick QG has the SAME action structure as Stelle's quadratic gravity:

```
S = ∫ d⁴x √(-g) [M_P²R/2 + α R_μν R^μν + β R² + Λ]
```

Using the identity R_μν R^μν = C_μνρσ C^μνρσ + R²/3 + total derivative (Gauss-Bonnet in 4D), this is equivalent to the form used in QG+F:

```
S = ∫ d⁴x √(-g) [M_P²R/2 - (1/2f₂²) C²_μνρσ + (1/6f₀²) R²]
```

**For the six-derivative (super-renormalizable) version**, additional R³-type terms are added, pushing the UV behavior to ~ 1/p⁶ or higher. Modesto's construction can include N pairs of complex poles, giving UV behavior ~ 1/p^{2(N+1)}.

**The Graviton Propagator:**

For the simplest (four-derivative) case, the propagator decomposes into spin-2 and spin-0 sectors:

- **Spin-2 sector**: 1/p² − 1/(p² + M₂²) where M₂ is the massive spin-2 mass
- **Spin-0 sector**: 1/(p² + M₀²) where M₀ is the massive scalar mass

In Stelle gravity, M₂² is real and positive → the massive spin-2 is a ghost.

In Lee-Wick QG (six-derivative and higher), the masses can be COMPLEX CONJUGATE pairs: M² = m² ± iΓ, so the propagator components take the form:

```
𝒢̃(−k²) = −iM² / [(k² + m²)² + M⁴]
```

This is purely imaginary, which drives the need for a specific prescription.

**The Four Prescriptions** (from the 2025 definitive paper):

| Prescription | Lorentz Inv. | Optical Theorem | Power-Counting | Analyticity |
|---|---|---|---|---|
| By-the-book (Wick rotation) | ✓ | ✗ | ✓ | ✓ |
| Lee-Wick-Nakanishi (LWN/CLOP) | **✗** | ✓ | Patch-wise | ✗ |
| **Fakeon/AP** | **✓** | **✓** | **✓** | ✗ |
| Direct Minkowski | ✓ | ✗ | ✗ | ✓ |

**The LWN/CLOP prescription breaks Lorentz invariance** because: loop energy integrates along a complex contour while spatial momenta are constrained to ℝ^(D-1). Under a Lorentz boost, spatial components become complex, violating the constraint. Nakanishi noticed this in 1971.

**The fakeon/AP prescription** fixes this via domain deformation: both energy AND spatial momenta integrate on complex paths. The key formula:
```
ℳ_AP(p²) = ½[ℳ(p² − iε) + ℳ(p² + iε)]   (average continuation)
```

### Spectral Dimension

From the goal context and propagator analysis:
- With N pairs of complex poles: propagator ~ 1/p^{2(N+1)} at high energy
- This gives d_s = 4/(N+1) × 2 = ... actually needs careful computation
- For the four-derivative (N=0, one pair of poles): d_s = 2 (same as QG+F)
- For six-derivative (N=1): d_s could be different

**Important note**: The spectral dimension depends on the propagator's UV behavior, which is set by the ACTION, not the prescription. Since both Lee-Wick and fakeon use the same action, they should have the same spectral dimension. The difference is in the S-matrix, not the propagator.

For the four-derivative theory (same action as QG+F): **d_s = 2**.

---

## Task 2: Unitarity Status — THE KEY QUESTION

### Summary Verdict: Lee-Wick prescription FAILS. Fakeon prescription SUCCEEDS. Modesto himself agrees.

Four independent lines of evidence:

#### Evidence 1: Kubo & Kugo (2023) — Direct Unitarity Violation
- Complex ghosts ARE created in fourth-order derivative theories above a threshold energy
- Mechanism: radiative corrections give complex masses; "complex delta function" at vertices enforces complex energy conservation → ghost production
- Below threshold: unitary. Above threshold: unitarity violated.
- **Devastating for LW QG** — violation occurs at high energies where QG matters

#### Evidence 2: Anselmi (2022) — Structural Problems
- Removing LW ghosts from external states → non-Hermitian classical limit
- Including all states → unbounded Hamiltonian or negative norms
- LW ghosts are NOT purely virtual — leave imaginary remnants
- The fix (superposition of fakeon + particle) breaks general covariance → can't apply to gravity

#### Evidence 3: Anselmi, Briscese, Calcagni & Modesto (2025) — Definitive Comparison
- LWN/CLOP prescription breaks Lorentz invariance at quantum level
- Only fakeon/AP prescription is "physically viable" for quantum gravity
- **Modesto himself is a co-author** — the creator of LW QG now agrees the LW prescription must be replaced by fakeon

#### Evidence 4: Oda (2026) — Bound State Impossibility
- Bound states cannot be created from ghosts via complex delta functions
- "Violation of the unitarity is also connected to the non-existence of bound states"
- The ghost confinement strategy (Asorey et al. 2025) doesn't actually work to restore unitarity

#### Evidence 5: Buoninfante (2025) — Ghost Resonance Structure
- Ghost propagator has complex conjugate poles in the FIRST Riemann sheet
- Ordinary unstable particles have poles only in the second sheet
- This structural difference means ghosts cannot be treated like ordinary unstable resonances
- Confirms the fundamental distinction between ghost resonances and ordinary resonances

### The Critical Implication
**Lee-Wick QG with the LW/CLOP prescription is not a viable theory.** If you use the fakeon prescription instead, you get QG+F (Anselmi's theory). The action may be the same, but the prescription is what distinguishes the physics. The only viable prescription for complex poles in quantum gravity is the fakeon one.

---

## Task 3: Tier 1 Validation

| Criterion | LW Prescription | Fakeon Prescription (= QG+F) |
|-----------|----------------|------------------------------|
| Correct DOF (massless spin-2) | ✅ Graviton is only real pole | ✅ |
| Unitarity | ❌ Violated above threshold | ✅ Proven to all orders |
| Ghost freedom | ❌ Complex ghosts created above threshold | ✅ Fakeons purely virtual |
| UV completion | ✅ Super-renorm (6-deriv) or renorm (4-deriv) | ✅ Renormalizable (4-deriv) |
| Diffeomorphism invariance | ✅ By construction | ✅ |
| Renormalizability | ✅ Super-renorm or renorm | ✅ Renormalizable |

**Verdict: With LW prescription — FAILS Tier 1 (unitarity).**
**With fakeon prescription — PASSES Tier 1, but IS QG+F, not LW QG.**

---

## Task 4: Tier 2 Validation

### Newtonian Potential
The Newtonian potential with complex poles is **singularity-free** at r = 0. This is a key result from Modesto (2016).

For complex conjugate mass pairs M² = m² ± iΓ, the potential takes the form of a damped oscillating correction to the standard -Gm/r:

```
V(r) = -Gm/r [1 + corrections involving e^{-mr}cos(Γr) and e^{-mr}sin(Γr)]
```

The "anti-gravitons" contribute a repulsive (positive) correction at short distances, effectively regularizing the singularity. At distances r >> 1/m, the corrections are exponentially suppressed and V(r) → -Gm/r (standard Newton).

**Note**: For the four-derivative theory specifically (Stelle gravity = same action as QG+F), the potential at tree level has been computed to be regular at the origin. The one-loop quantum corrections (computed by Bjerrum-Bohr et al.) improve the behavior but are "not enough to remove the curvature singularity in r=0" by themselves.

### Recovery of GR at Low Energies
Yes. The higher-derivative corrections are suppressed by powers of E/M where M is the mass scale of the complex poles (~ Planck scale). At low energies, the theory reduces to GR + small corrections.

### PPN Parameters
For the four-derivative theory, at long distances the massive modes are exponentially suppressed (Yukawa-type). The PPN parameters are:
- γ = β = 1 (same as GR) at distances r >> 1/M
- Corrections are of order exp(-Mr), completely negligible at solar system scales

### Gravitational Wave Speed
The massless spin-2 graviton propagates at speed c exactly. The massive modes don't propagate as free particles at low energies (they're either ghosts, fakeons, or short-lived). So **GW speed = c** in this class of theories.

However, the Weyl-squared coefficient can modify the GW speed on curved backgrounds (cosmological backgrounds). With the fakeon prescription, this is a small quantum correction.

---

## Task 5: Comparison to QG+F

### THE KEY INSIGHT: They share the same action. The difference is ONLY the prescription.

For the four-derivative theory:

| Property | QG+F (Fakeon) | Lee-Wick QG (CLOP) |
|----------|---------------|---------------------|
| **Action** | S = ∫√-g [M²_P R/2 - C²/2f₂² + R²/6f₀²] | **SAME** (or 6-derivative generalization) |
| **Propagator poles** | 1/p² + fakeon(1/(p²+M₂²)) + standard(1/(p²+M₀²)) | 1/p² + CLOP(1/(p²+M₂²)) + standard(1/(p²+M₀²)) |
| **Ghost resolution** | Fakeon prescription (removed from ALL states, purely virtual) | CLOP (removed from external states only, propagate internally) |
| **Lorentz invariance** | ✅ Preserved (domain deformation) | ❌ Broken at quantum level (Nakanishi 1971) |
| **Optical theorem** | ✅ Satisfied | ✅ Satisfied (in its own frame) |
| **Unitarity** | ✅ **Proven to all orders** (Anselmi-Piva 2017-2018) | ❌ **Violated above threshold** (Kubo-Kugo 2023) |
| **Classical limit** | ✅ Hermitian | ❌ Non-Hermitian (imaginary remnants) |
| **Renormalizability** | ✅ Renormalizable (4-deriv), BPHZ structure | ⚠️ Renorm (4-deriv) or super-renorm (6-deriv), but patch-wise |
| **d_s** | 2 (4-derivative) | 2 (4-derivative) — SAME action |
| **Predictions: r** | [0.0004, 0.0035] (4/3 < N²r < 12) | **Same action → same predictions IF viable** |
| **Predictions: n_s** | ~0.967 | Same |
| **Microcausality** | Violated at E > m_χ (fakeon mass) | Not well-defined (Lorentz violation) |
| **Physical viability** | ✅ **Viable** | ❌ **Not viable** (2025 paper by BOTH Anselmi AND Modesto) |

### The Super-Renormalizable (6-Derivative) Extension
The six-derivative version of the theory (Modesto's specific construction) is super-renormalizable with only finitely many divergent diagrams. This is a potential advantage over QG+F's four-derivative action. However:
- The same prescription issue applies — must use fakeon, not CLOP
- With fakeon prescription on a six-derivative action, this becomes "super-renormalizable QG with fakeons" — not exactly QG+F (which is four-derivative), but in the same family
- The extra derivatives buy super-renormalizability but add free parameters (the masses of additional complex poles)

---

## Task 6: Novelty Assessment

### Is "Lee-Wick quantum gravity" an existing active research program?
**Yes, but very small and now effectively absorbed into the fakeon program.**

#### Key researchers:
- **Leonardo Modesto** (Southern University of Science and Technology, China → now collaborating with Anselmi)
- **Ilya Shapiro** (UFJF, Brazil)
- **Lesław Rachwał** (collaborator on RG calculations)
- **Damiano Anselmi** (Pisa, Italy) — originally developed fakeon as an improvement of LW
- **Gianluca Calcagni** (CSIC, Spain) — collaborator on nonlocal/LW gravity
- **Jisuke Kubo & Taichiro Kugo** (Japan) — critics showing unitarity violation
- **Manuel Asorey, Gastao Krein** — bound state studies
- **Ichiro Oda** (2026) — further unitarity analysis

#### Paper count:
Approximately 15-25 papers directly on "Lee-Wick quantum gravity" (as distinct from the much larger literature on Lee-Wick QFT in particle physics). The community is ~5-10 active researchers.

#### Status evolution (critical trajectory):
1. **2015-2016**: Modesto & Shapiro propose LW QG as super-renormalizable. Optimistic claims about unitarity via CLOP.
2. **2017**: Anselmi & Piva reformulate LW QFT, developing the fakeon as an improvement. Bridge period.
3. **2018**: Anselmi & Piva prove fakeon unitarity to all orders. QG+F crystallizes as distinct from LW.
4. **2022**: Anselmi explicitly argues LW ghosts are inferior to fakeons (non-Hermitian classical limit).
5. **2023**: Kubo & Kugo prove unitarity IS violated in LW theories above threshold.
6. **2025 (March)**: Anselmi AND Modesto co-author paper agreeing only fakeon prescription is viable. **This effectively ends LW QG as independent program.**
7. **2025-2026**: Remaining work focuses on ghost bound states, ghost resonances — trying to salvage something, but conclusions are negative (Oda 2026: bound states don't form, unitarity violation confirmed).

### What has NOT been computed (gaps):
- Full two-loop calculations in the six-derivative theory with fakeon prescription
- Explicit cosmological predictions specific to the super-renormalizable (6-derivative) version with fakeon
- Non-perturbative aspects of ghost confinement
- Complete RG flow to low energies with fakeon prescription in 6-derivative theory

---

## Task 7: Overall Verdict

### Does Lee-Wick QG pass Tier 1?
**NO** — with the LW/CLOP prescription, it fails unitarity. This is now confirmed by multiple independent groups, including Modesto himself (2025).

### Is it a genuinely distinct theory from QG+F?
**The action can be different** (LW QG can use 6-derivative action vs QG+F's 4-derivative), **but the prescription must be the same** (fakeon). So:

- **Four-derivative LW action + fakeon prescription = QG+F exactly.** Not distinct.
- **Six-derivative LW action + fakeon prescription = super-renormalizable QG with fakeons.** This IS distinct from four-derivative QG+F — it's a super-renormalizable cousin with more free parameters.

The interesting question is whether the six-derivative version with fakeon prescription is worth pursuing. Pros: super-renormalizable (better UV than QG+F). Cons: more free parameters, same prescription issues, less predictive.

### If distinct: what is the sharpest observational difference?
Between four-derivative QG+F and six-derivative super-renormalizable QG with fakeons:
- Different running of couplings (different beta functions)
- Potentially different spectral dimension flow
- The super-renormalizable version has fewer divergent diagrams → potentially different quantum corrections to observables
- But both share the same IR physics and the same basic predictions for r and n_s (dominated by the R² term / Starobinsky inflation)

### Is this worth pursuing as our primary construction target?

**NO.** For three reasons:

1. **The LW prescription is dead.** Multiple independent results (Kubo-Kugo 2023, Anselmi 2022, Anselmi+Modesto 2025, Oda 2026) confirm it doesn't work. You MUST use the fakeon prescription.

2. **With fakeon prescription, four-derivative version IS QG+F.** There's no independent "Lee-Wick QG" — it collapses onto Anselmi's theory. We'd just be rediscovering QG+F.

3. **The six-derivative version is a possible variant but less attractive.** It's super-renormalizable (nice) but introduces more free parameters (masses of additional complex poles) and has the same predictions at leading order. It's not "novel" — it's a known extension of QG+F.

**Bottom line: Lee-Wick QG is not a viable independent construction target. It's either the same as QG+F (with fakeon prescription) or non-unitary (with LW prescription). Our search should look elsewhere for genuinely novel theories.**

---

## Sources

- [Modesto, Super-renormalizable or Finite Lee-Wick Quantum Gravity](https://arxiv.org/abs/1602.02421)
- [Modesto & Shapiro, Superrenormalizable quantum gravity with complex ghosts](https://arxiv.org/abs/1512.07600)
- [Anselmi & Piva, A new formulation of Lee-Wick quantum field theory](https://link.springer.com/article/10.1007/JHEP06(2017)066)
- [Anselmi, On the quantum field theory of the gravitational interactions](https://arxiv.org/abs/1704.07728)
- [Anselmi & Piva, Quantum Gravity, Fakeons And Microcausality](https://arxiv.org/abs/1806.03605)
- [Anselmi, Fakeons and Lee-Wick models](https://link.springer.com/article/10.1007/JHEP02(2018)141)
- [Anselmi, Purely virtual particles versus Lee-Wick ghosts](https://arxiv.org/abs/2202.10483)
- [Kubo & Kugo, Unitarity Violation in Field Theories of Lee-Wick's Complex Ghost](https://arxiv.org/abs/2308.09006)
- [Anselmi, Briscese, Calcagni & Modesto, Amplitude prescriptions in field theories with complex poles](https://arxiv.org/abs/2503.01841)
- [Asorey, Krein, Pardina & Shapiro, Bound states of massive complex ghosts](https://arxiv.org/abs/2408.16514)
- [Oda, Bound States in Lee's Complex Ghost Model](https://arxiv.org/abs/2602.05562)
- [Buoninfante, Remarks on ghost resonances](https://arxiv.org/abs/2501.04097)
- [Anselmi, Bianchi & Piva, Predictions of quantum gravity in inflationary cosmology](https://arxiv.org/abs/2005.10293)
- [Calcagni & Modesto, Testing quantum gravity with primordial gravitational waves](https://arxiv.org/abs/2206.07066)
- [Modesto, Rachwał & Shapiro, Renormalization group in super-renormalizable quantum gravity](https://link.springer.com/article/10.1140/epjc/s10052-018-6035-2)

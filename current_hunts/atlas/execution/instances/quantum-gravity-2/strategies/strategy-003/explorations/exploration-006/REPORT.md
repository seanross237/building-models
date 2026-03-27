# Exploration 006: Analyticity Reconciliation — Can QG+F's Analyticity Sacrifice Coexist with AS?

## Goal
Determine whether QG+F's sacrifice of S-matrix analyticity is reconcilable with Asymptotic Safety's Euclidean functional RG framework. Does AS require standard analyticity, or is its analytic structure already non-standard?

---

## 1. QG+F's Analyticity Sacrifice — What Exactly Is Given Up

From Anselmi et al. (JHEP 2025, arXiv:2503.01841): The fakeon is one of four inequivalent quantization prescriptions for theories with complex poles.

| Prescription | Unitarity | Lorentz inv. | Analyticity | Renormalizability |
|---|---|---|---|---|
| Textbook Wick rotation | ❌ | ✅ | ✅ | ✅ |
| Lee-Wick-Nakanishi | ✅* | ❌ | ✅ | ✅ |
| **Fakeon** | **✅** | **✅** | **❌** | **✅** |
| Direct Minkowski | ❌ | ✅ | ✅ | ❌ |

The fakeon is the ONLY prescription preserving both unitarity and Lorentz invariance. The cost: **no S-matrix analyticity**. Concretely:
- No dispersion relations (Kramers-Kronig requires analyticity)
- No S-matrix bootstrap (assumes analyticity + crossing + unitarity)
- No standard Wick rotation — the Euclidean↔Lorentzian connection is modified
- Crossing symmetry limited in standard form

**Critical subtlety:** QG+F does NOT prohibit working in Euclidean signature. It prohibits the standard *analytic* continuation between Euclidean and Lorentzian. The fakeon uses "average continuation" — a nonanalytic but well-defined operation. Amplitudes are obtained by (nonanalytically) Wick-rotating their Euclidean versions, taking the average of limits from different directions rather than analytic continuation (Anselmi, JHEP 2018; arXiv:1801.00915).

## 2. Does AS Require Analyticity?

**Answer: No. AS does not fundamentally require S-matrix analyticity.**

The Wetterich equation (exact functional RG equation) is formulated in Euclidean signature. It integrates out quantum fluctuations shell-by-shell in momentum space. But:

1. **The FRG is a computational tool, not an analyticity assumption.** The Wetterich equation produces a scale-dependent effective action Γ_k. It requires well-defined Euclidean correlation functions but does NOT require that these have standard analytic continuation properties to Lorentzian signature.

2. **Physical predictions require continuation to Lorentzian.** This is where analyticity traditionally enters — one Wick-rotates back. But this step is *separate* from the FRG computation itself. The FRG can run entirely in Euclidean space without any S-matrix analyticity.

3. **The Osterwalder-Schrader framework** provides sufficient conditions (reflection positivity) under which Euclidean correlators reconstruct a unitary Lorentzian theory. But Osterwalder-Schrader is sufficient, not necessary — theories violating OS axioms may still have consistent Lorentzian physics through alternative continuation procedures.

4. **AS already has analyticity problems of its own** (see Section 3). The graviton propagator develops complex poles that obstruct standard Wick rotation.

**Key finding:** The Euclidean FRG computes the effective action. How one extracts Lorentzian physics from that action is a separate question. Standard analytic Wick rotation is one method — but it's not the only one, and AS itself cannot always use it.

## 3. Complex Poles in AS — The Wick Rotation Is Already Obstructed

This is the most important finding for the reconciliation question: **AS already has non-standard analytic structure.**

### Donoghue's Critique (Frontiers in Physics, 2020; arXiv:1911.02967)

Donoghue identified that the ghost state in quadratic gravity (the natural truncation of AS) creates **an obstruction to Wick rotation**:

- The ghost pole sits in the **upper right quadrant** of the complex q₀ plane
- Standard Wick rotation requires rotating the q₀ contour by 90° — this rotation sweeps over the ghost pole
- **Any truncation without tachyons will likely have one or more poles obstructing analytic continuation** from Euclidean to Lorentzian space
- This is recognized as a major open problem within the AS program itself

### Draper, Knorr, Ripken, Saueressig (PRL 125, 2020; JHEP 2020)

Working within AS, they found that the graviton propagator has **infinite towers of spin-0 and spin-2 poles at imaginary squared momentum**. These are not standard poles on the real axis. The resulting scattering amplitudes are:
- Compatible with unitarity bounds
- Causal
- Scale-free at trans-Planckian energy

But the pole structure is highly non-standard. Poles at imaginary p² means poles in the complex q₀ plane that obstruct naive Wick rotation.

### Bonanno, Denz, Pawlowski, Reichert (SciPost Phys. 12, 2022)

Reconstructed the Lorentzian graviton spectral function from Euclidean FRG data. Critical admissions:
- They **assume** "the existence of a standard Wick rotation at least for backgrounds close to flat ones"
- They **exclude** complex conjugate poles, stating such extensions "may signal the loss of unitarity"
- They acknowledge Wick rotation remains "one of the remaining challenges yet to be met" in AS
- The background graviton spectral function has negative parts (paralleling QCD gluons — gauge artifact, not unitarity violation)

### Implication

**AS's own analytic structure is already non-standard.** The complex pole towers and ghost pole obstructions mean that AS cannot rely on standard Wick rotation any more than QG+F can. The supposed tension — "QG+F breaks analyticity but AS needs it" — is based on a false premise. AS doesn't have standard analyticity either.

## 4. Lorentzian AS — Euclidean Signature Is Optional

The Euclidean formulation of AS is NOT fundamental. Lorentzian formulations exist.

### D'Angelo, Drago, Pinamonti, Rejzner (Phys. Rev. D 109, 2024; arXiv:2310.20603)

**Landmark result:** First background-independent evidence of asymptotic safety directly in Lorentzian signature.
- NGFP exists in Lorentzian signature at (g*, λ*) = (1.15, 0.42)
- **No Wick rotation needed** — Lorentzian FRGE "directly developed in Lorentzian spacetimes with a covariant formalism"
- **No analyticity required** — operates without analytic continuation
- Fixed point values differ from Euclidean (0.34, 0.3), reflecting different signatures and regulators

### Manrique, Reuter, Saueressig (2011; arXiv:1102.5012)

Introduced causal FRG connecting Euclidean and Lorentzian RG flows without standard analytic continuation.

### Foliated AS (2025; arXiv:2501.03752)

Recent work achieves Wick rotation by rotating the lapse function rather than the time coordinate. Key findings:
- Euclidean and Lorentzian beta functions are **identical** with careful regulator choice
- Requires spatial regulators that don't introduce new poles in the complex plane
- The equivalence is "highly non-trivial and should be established based on explicit computations"

### Implication

AS can be formulated entirely in Lorentzian signature. The Euclidean formulation is a computational convenience, NOT a fundamental requirement. This eliminates any argument that AS's Euclidean nature demands analyticity.

## 5. Fakeon Prescription and Wick Rotation — Compatible Operations

The fakeon's "average continuation" and AS's Euclidean FRG can coexist because they operate at different levels:

1. **FRG level (Euclidean):** The Wetterich equation computes the scale-dependent effective action Γ_k. This computation happens entirely in Euclidean signature. No continuation is needed at this stage. The fakeon prescription doesn't interfere here — it's about how to handle poles when extracting Lorentzian physics.

2. **Physics extraction level (Euclidean → Lorentzian):** Here is where the fakeon prescription enters. Instead of standard analytic Wick rotation (which fails due to complex poles anyway), one uses average continuation. This is where QG+F and AS face the *same* problem and QG+F offers a *solution*.

3. **Lorentzian FRG (alternative):** If one uses the Lorentzian FRG directly, neither standard Wick rotation nor average continuation is needed. The Lorentzian FRGE computes physics directly without continuation.

**The fakeon prescription may actually SOLVE a problem AS already has.** AS's complex pole towers obstruct standard Wick rotation. The average continuation provides a systematic, nonanalytic way to extract Lorentzian physics from Euclidean data despite complex poles. If QG+F = AS, the fakeon prescription could be exactly the tool AS needs.

## 6. Platania & Wetterich on Ghosts and Unitarity

Platania & Wetterich (PLB 811, 2020; arXiv:2009.06637) propose a different ghost resolution: ghosts in truncated effective actions are **fictitious** — their residues vanish when all symmetry-compatible operators are included.

Relevance to our question:
- They do NOT assume or require S-matrix analyticity
- They do NOT mention the fakeon prescription
- Their mechanism is orthogonal to analyticity: if ghosts vanish entirely, the complex poles that obstruct Wick rotation may also disappear
- **If correct, this dissolves the analyticity question entirely** — no ghost poles means no Wick rotation obstruction, and both AS and QG+F could have standard analytic properties in the full theory

However, this remains speculative — the full nonperturbative calculation hasn't been done. The Platania-Wetterich mechanism is **compatible** with both QG+F and standard AS regardless of how analyticity is handled.

## 7. Verdict: SUPPORTS

**The apparent tension between QG+F's analyticity sacrifice and AS's Euclidean framework is not a real contradiction. It dissolves on examination.**

### The argument in three steps:

**Step 1: AS doesn't require analyticity.**
The Wetterich equation is a computational tool in Euclidean signature. It doesn't require the resulting effective action to have standard analytic continuation properties. Physical prediction extraction is a separate step.

**Step 2: AS already has non-standard analytic structure.**
- Ghost poles in the upper right quadrant obstruct standard Wick rotation (Donoghue 2020)
- Infinite towers of poles at imaginary p² (Draper et al. 2020)
- Bonanno et al. (2022) must *assume* Wick rotation works — they can't derive it
- The AS community recognizes this as an open problem

**Step 3: Lorentzian AS bypasses the issue entirely.**
D'Angelo et al. (2024) demonstrated an NGFP directly in Lorentzian signature without any Wick rotation. If AS can be formulated without analyticity, it cannot require it.

### The deeper point:

The QG+F analyticity sacrifice and AS's Wick rotation obstruction may be **the same phenomenon seen from different angles.** QG+F explicitly acknowledges and systematically handles the non-analyticity (via the fakeon/average continuation). AS has the same non-analyticity hidden in its complex pole structure but hasn't yet developed a systematic way to handle it. The fakeon prescription could be the missing tool that AS needs for Euclidean→Lorentzian extraction.

### Strength of evidence:

| Evidence | Weight |
|---|---|
| Lorentzian AS exists without analyticity | Strong |
| AS's own poles obstruct standard Wick rotation | Strong |
| FRG is computational tool, not analyticity requirement | Moderate |
| Fakeon average continuation could solve AS's Wick rotation problem | Suggestive |
| Platania-Wetterich ghost disappearance might eliminate the issue | Speculative |

**Verdict: SUPPORTS** — with confidence. The analyticity sacrifice is not a barrier to QG+F = AS. If anything, it's a feature that could help AS solve its own known problems.

---

## Sources
- Anselmi et al., JHEP 05 (2025) 145; arXiv:2503.01841
- Anselmi, JHEP 02 (2018) 141; arXiv:1801.00915 (fakeon prescription, average continuation)
- Anselmi, arXiv:2601.06346 (causality paper, 2026)
- Donoghue, Front. Phys. 8 (2020) 56; arXiv:1911.02967 (AS critique, Wick rotation obstruction)
- Draper, Knorr, Ripken, Saueressig, PRL 125 (2020) 181301; arXiv:2007.00733 (complex pole towers)
- Draper et al., JHEP 11 (2020) 136; arXiv:2007.04396 (graviton scattering amplitudes)
- Bonanno, Denz, Pawlowski, Reichert, SciPost Phys. 12 (2022) 001; arXiv:2102.02217 (spectral reconstruction)
- Platania, JHEP 09 (2022) 167; arXiv:2206.04072 (causality, unitarity, stability conditions)
- Platania, Wetterich, PLB 811 (2020) 135911; arXiv:2009.06637 (fictitious ghosts)
- D'Angelo, Drago, Pinamonti, Rejzner, Phys. Rev. D 109 (2024) 066012; arXiv:2310.20603 (Lorentzian AS)
- Manrique, Reuter, Saueressig, arXiv:1102.5012 (causal FRG)
- Baldazzi, D'Angelo, Falls, arXiv:2501.03752 (foliated AS, 2025)
- Knorr, Ripken, Saueressig, arXiv:1907.02903 (form factors in AS)
- Knorr et al., arXiv:2111.12365 (form factors: ghost-free gravity vs AS)

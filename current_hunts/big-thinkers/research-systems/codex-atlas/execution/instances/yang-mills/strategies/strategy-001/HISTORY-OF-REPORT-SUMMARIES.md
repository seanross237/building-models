# Exploration History

## Exploration 001: Balaban's RG Program for Lattice Yang-Mills

**Outcome: SUCCEEDED**

Produced a theorem-level technical map of Balaban's 14-paper series (1983-1989). Key findings:

1. **Paper inventory**: 14 papers in 4 phases — foundational tools (1-8), 3D UV stability (9), small-field 4D RG (10-12), large-field 4D (13-14)
2. **Precise stopping point**: Achieves UV stability of 4D lattice YM in finite volume (uniform bounds on partition function as ε→0 on T⁴). Does NOT achieve: control of observables, uniqueness, infinite volume, mass gap, or OS/Wightman axioms.
3. **Two-tier gap structure**:
   - Tier 1 (potentially tractable): Control observables (Gap 1), prove uniqueness (Gap 2), verify OS axioms on T⁴ (Gap 3)
   - Tier 2 (needs new ideas): Prove mass gap (Gap 4), infinite volume T⁴→R⁴ (Gap 5)
4. **Modern developments**: Dimock (2011-22, expository + 3D QED), Chatterjee (2018-24, probabilistic but Gaussian), Chandra-Hairer-Shen-Chevyrev (2024, stochastic quantization of 3D YMH)
5. **Key quote**: Jaffe-Witten state "no present ideas point the direction to establish the existence of a mass gap"
6. **Computations identified**: RG map contraction analysis for uniqueness; Wilson loop RG tracking for observable control

## Exploration 002: Constructive QFT — What Works in 2D/3D and What Breaks in 4D

**Outcome: SUCCEEDED**

Cataloged 8 major rigorous QFT constructions and identified 3 specific 4D failure modes. Key findings:

1. **Catalog**: φ⁴₂ (Glimm-Jaffe-Spencer 1974), φ⁴₃ (Feldman-Osterwalder 1976), Yukawa₂, Gross-Neveu₂ (first rigorous asymptotically free QFT), YM₂ (topological), lattice gauge theories (Brydges-Fröhlich-Seiler), Balaban's program, YM-Higgs₃ (Chandra-Chevyrev-Hairer-Shen 2024)
2. **Core distinction**: Super-renormalizability (d=2,3: finitely many divergent diagrams) vs. just-renormalizability (d=4: infinitely many). Entire constructive toolbox is built for super-renormalizable case.
3. **Three 4D failure modes**: (a) cluster expansion divergence (no automatic small factors), (b) large field problem (insufficient action suppression at critical dimension), (c) infinite RG convergence (must prove non-perturbative convergence of infinite procedure)
4. **φ⁴₄ triviality** (Aizenman-Duminil-Copin 2021): Proves 4D obstruction is structural, not just technical. YM expected to escape via asymptotic freedom but unproven.
5. **CRITICAL REFRAMING**: Magnen-Rivasseau-Sénéor (1993) constructed YM₄ with IR cutoff but no UV cutoff. **The UV problem for 4D YM is solved. The entire difficulty is IR** (confinement, mass gap).
6. **Gross-Neveu insight**: Asymptotically free theories CAN be rigorously constructed (with Pauli principle for fermions). Finding a bosonic analog is open.
7. **Computations identified**: Numerical verification of Balaban's bounds on small lattices; non-perturbative beta function comparison.

## Exploration 004: Lattice-to-Continuum Limit — Bridging Numerical Evidence and Rigorous Proof

**Outcome: SUCCEEDED**

Mapped the lattice-continuum gap with extraordinary detail. Key findings:

1. **Numerical lattice results are extraordinary**: SU(3) glueball spectrum fully mapped below 4 GeV (0++ at 1730±80 MeV), string tension √σ ≈ 420 MeV, asymptotic scaling verified over β = 5.7-7.5, universality confirmed, large-N scaling checked for N=2,...,12. All NUMERICAL ONLY.
2. **2020-2025 rigorous progress explosion**: Adhikari-Cao (2025) mass gap for FINITE gauge groups. Chatterjee (2024) first non-abelian scaling limit in d>2 (but Gaussian). Area law in 't Hooft limit (2025). Stochastic quantization of 3D YMH (Chandra-Chevyrev-Hairer-Shen 2024).
3. **7-step gap structure**: Steps 1-2 (UV stability, tightness) DONE (Balaban). Steps 3-5 (observables, uniqueness, OS axioms) TIER 1 — believed achievable. Step 6 (mass gap) THE MILLENNIUM PROBLEM — no known technique. Step 7 (infinite volume) conditional on Step 6.
4. **Key bottleneck**: Finite-to-continuous gauge group transition is the single most important barrier.
5. **Most promising paths**: Chatterjee probabilistic school (steadiest progress), completing Balaban on T⁴ (would be "major breakthrough" per Jaffe-Witten), spectral gap methods for transfer matrix.
6. **Computations identified**: Transfer matrix spectral gap on small lattices; finite group approximation convergence to SU(2).

## Exploration 003: SU(2) Lattice Gauge Theory — Mass Gap Observables (Math Explorer)

**Outcome: SUCCEEDED**

Implemented full SU(2) Wilson lattice gauge theory MC simulation in Python. Key findings:

1. **Confinement confirmed**: Area law with R²>0.996 at all β values. String tension σ = 0.593(13) at β=2.0 down to σ=0.132(3) at β=3.0.
2. **Mass gap evidence**: Positive string tension, vanishing Polyakov loop, exponentially decaying Wilson loops. Glueball mass m₀ ~ 1.8-2.5 lattice units estimated.
3. **Implementation verified**: Plaquette values match published SU(2) results within 1-2σ. Internal consistency checks pass.
4. **Glueball correlator failed** on small lattices (4⁴-8⁴) — noise-dominated for t>0. Consistent with large mass gap m₀ >> 1/L. Professional results need 16⁴-32⁴.
5. **Scaling not demonstrated** — lattice sizes below scaling window (needs β≥2.4 on ≥16⁴).
6. **Verification**: 4 VERIFIED, 12 COMPUTED, 3 CHECKED, 2 CONJECTURED claims.
7. **Key gap**: Rigorous bound σ(β,L) ≥ c > 0 uniform in both L and β is the core missing mathematical ingredient.

## Exploration 006: The Modern Rigorous Frontier — Adhikari-Cao, Chatterjee, and the Path Forward

**Outcome: SUCCEEDED**

Deep technical analysis of 17 papers from 2018-2026. Key findings:

1. **Adhikari-Cao Theorem 1.1**: Proves exponential correlation decay for ALL finite gauge groups at weak coupling using novel "swapping map" technique (NOT cluster expansion). Inherently finite-group.
2. **FOUR layers of finite→continuous obstruction**: (a) discrete→uncountable homomorphism space, (b) counting bounds meaningless for continuous G, (c) swapping map requires discrete bijections with no continuous analog, (d) spectral gap Δ_G → 0 as subgroups approach SU(2). ALL STRUCTURAL, not technical.
3. **Chatterjee's conditional theorem** (CMP 385, 2021): Strong mass gap ⟹ center symmetry ⟹ confinement. One-directional, conditional on unproven mass gap.
4. **Every existing result avoids the core difficulty**: Wrong groups (finite), wrong coupling (strong), wrong dimension (3D), wrong limit (large-N), or trivial (Gaussian).
5. **Timeline assessment: 20-50+ year problem.** Conceptual breakthrough required — a genuinely new technique for proving spectral gaps in continuous gauge theories.
6. **Three independent research fronts**: Chatterjee (probabilistic), Chandra-Hairer (regularity structures), Shen-Zhu-Zhu (stochastic/Langevin).
7. **Unexpected**: Adhikari-Cao innovation is topological/combinatorial, not analytical. Chatterjee's 2026 3D result only gives logarithmic confinement (weaker than area law).

## Exploration 005: Finite Group Approximation of SU(2) — Mass Gap Convergence (Math Explorer)

**Outcome: SUCCEEDED — Strong convergence confirmed**

Implemented lattice gauge theory for binary polyhedral subgroups of SU(2) (2T=24, 2O=48, 2I=120 elements) on 4⁴ lattice. Key findings:

1. **Binary icosahedral group (120 elements) reproduces SU(2) to < 0.5% accuracy** for all observables across full β=1.0-4.0 range. String tension matches to 0.03% at β=3.5.
2. **Phase transition structure**: β_c(2T)≈2.2, β_c(2O)≈3.2, β_c(2I)≈5.8. Scales as ~|G|^{0.6}. Hysteresis weakens: 0.39→0.18→0.09. Transition disappears as |G|→∞.
3. **Convergence rate**: |obs_G - obs_SU(2)| ~ |G|^{-α} with α ≈ 0.7-2.5.
4. **Strong coupling universality**: Even 2T (24 elements) matches SU(2) to 0.8% at β=1.0.
5. **Proof gaps**: Need uniform lower bound on mass gap in confining phase, controlled convergence rate, rigorous β_c→∞ proof.
6. **Verification**: 3 VERIFIED, 11 COMPUTED, 4 CONJECTURED.
7. **Potential novelty**: Systematic quantitative study of finite-subgroup convergence to SU(2) in lattice gauge theory may be new.

## Exploration 007: Novelty Search for Finite Group Convergence Results

**Outcome: SUCCEEDED — Clear novelty assessment achieved**

Comprehensive literature search identifying 6+ relevant papers. Key findings:

1. **Phase transitions and qualitative convergence known since 1980** (Petcher-Weingarten). β_c values confirmed by Hartung et al. (2022): 2T→2.15, 2O→3.20, 2I→5.70.
2. **Novelty assessment**:
   - Convergence rates α ~ |G|^{-α} (α=0.7-2.5): **APPEARS NOVEL** — no prior measurement
   - β_c ~ |G|^{0.6} scaling: **PARTIALLY KNOWN** — β_c values known, power-law description new but inferior to existing analytic formula β_c(N) based on cyclic order
   - Hysteresis Δ⟨P⟩ = 0.39→0.18→0.09: **APPEARS NOVEL** — jump magnitudes never tabulated
   - <0.5% icosahedral accuracy: **PARTIALLY KNOWN** — qualitative accuracy known, specific bound new
3. **Correction**: Hartung (2022) has analytic formula β_c(N) = ln(1+√2)/(1-cos(2π/N)) — our power-law is a cruder version
4. **Publishable**: A systematic paper measuring convergence rates + comparing to Fibonacci spiral construction would be publishable, especially with relevance to quantum computing error budgets.

## Exploration 008: Spectral Gap and Adhikari-Cao Bound Analysis (Math Explorer — partial)

**Outcome: PARTIAL SUCCESS (code ran, explorer timed out, results obtained by strategizer)**

Computed spectral gaps of group Laplacians and Adhikari-Cao bounds. Key findings:

1. **Spectral gaps**: Δ_G(Cayley) = 4.0 (2T), 1.76 (2O), 2.29 (2I). Δ_G(heat kernel) ≈ 0.567 for all three.
2. **Adhikari-Cao bounds COMPLETELY VACUOUS**: β_min = 31.7/73.7/58.1 (Cayley) vs measured β_c = 2.2/3.2/5.8. Ratio 10-23x too large.
3. **β_min DIVERGES as |G|→∞**: Δ_G ~ |G|^{-0.31}, so β_min → ∞. Bound is vacuous for SU(2).
4. **Transfer matrix mass gap converges**: m(β=1) ≈ 0.83 for all three groups (0+1D model).
5. **STRONGEST QUANTITATIVE RESULT**: The Adhikari-Cao technique is not merely loose — it's fundamentally vacuous in the physical regime. Extending to SU(2) requires new ideas, not tighter bounds. (NOTE: Exploration 010 adversarial review found the correct Δ_G values give β_min ratios of 57-69x, not 10-23x — even MORE vacuous than originally computed.)

## Exploration 009: Complete Obstruction Atlas and Proof Strategy Assessment

**Outcome: SUCCEEDED**

Capstone synthesis integrating all 8 prior explorations. Key findings:

1. **9-approach obstruction atlas**: Balaban (TRACTABLE for existence, FUNDAMENTAL BARRIER for mass gap), Constructive QFT (FUNDAMENTAL), Lattice→continuum (FUNDAMENTAL), Stochastic quantization (FUNDAMENTAL), Chatterjee (HARD — most active), Adhikari-Cao (FUNDAMENTAL — 4-layer), Shen-Zhu-Zhu (FUNDAMENTAL at weak coupling), Large-N (HARD), OS reconstruction (TARGET).
2. **5 bottleneck theorems**: (a) Uniqueness of T⁴ limit ~5-10yr, (b) Observable control ~3-7yr, (c) SU(2) mass gap at ANY coupling — revolutionary, (d) Uniform mass gap for finite group sequence ~10-20yr, (e) Non-Gaussian scaling limit — potentially decades.
3. **Most promising unexplored combination**: Multi-scale RG (Balaban) + Bakry-Émery spectral gap (Shen-Zhu-Zhu) — coarse-grained effective actions where coupling stays controlled.
4. **Shen-Zhu-Zhu underappreciated**: First rigorous mass gap for continuous non-abelian group (SU(N) at β<1/48). Just at wrong coupling.
5. **Recommendation**: Focus on Bottleneck Theorem 3 via Bakry-Émery extension. Test RG + Bakry-Émery numerically first.

## Exploration 010: Adversarial Review of Novel Claims

**Outcome: SUCCEEDED — Found one explicit error, two qualifications**

1. **Claim 1 (convergence rates α≈0.7-2.5): SERIOUS qualification needed.** Power law fit to 3 points has zero degrees of freedom. At β=1.0, all deviations below MC noise floor — α≈2.4 is noise. α range is β-dependent, not observable-dependent. **Survives as:** qualitative monotone ordering and <0.5% accuracy for 2I.
2. **Claim 2 (Adhikari-Cao vacuousness): SERIOUS — error found but conclusion STRENGTHENED.** Wrong Δ_G definition used (Cayley graph vs. character minimum). Correct ratios: 57-69x (not 10-23x). Bounds are 4x MORE vacuous than reported. Also: only 3 binary polyhedral subgroups exist, so "divergence as |G|→∞" is extrapolation of analytic formula, not literal sequence limit.
3. **Claim 3 (four-layer structural barrier): MODERATE qualification.** Layers are our analytical construction, not independent (all stem from G being discrete). "Structural" is a prediction about future math. Shen-Zhu-Zhu already circumvents all four for continuous groups. **Survives as:** roadmap for why extending Adhikari-Cao specifically requires new ideas.


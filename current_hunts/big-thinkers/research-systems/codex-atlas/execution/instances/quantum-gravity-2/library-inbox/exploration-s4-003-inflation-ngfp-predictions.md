# Exploration 003: Can the NGFP Predict Inflationary Correction Parameters b and δ₃?

## Goal

Determine whether the Asymptotic Safety NGFP can predict specific numerical values for:
1. The Bonanno-Platania logarithmic correction parameter **b** (from RG improvement of R² gravity)
2. The six-derivative R³ coupling **δ₃** (from NGFP truncation hierarchy)

And whether these values resolve the n_s tension (observed n_s ≈ 0.974 vs Starobinsky n_s ≈ 0.967).

---

## Part A: The Bonanno-Platania Parameter b

### A1. Origin of the b Parameter and Its Physical Meaning

The effective Lagrangian used by Bonanno-Platania (2015, arXiv:1507.03375) and subsequently by Liu-Prokopec-Starobinsky (2018, arXiv:1806.05407, PRD 98, 043505) is:

```
L_eff = M_P² R/2 + (a/2) R² / [1 + b ln(R/μ²)]
```

**Physical origin of b:** The logarithmic correction arises from the running of the R² coupling near the NGFP. In the RG-improved effective action, the dimensionless R² coupling α(k) runs with the RG scale k. Near the NGFP, the running generates logarithmic corrections to the R² term that are parameterized by b.

**The claim to investigate:** b ~ θ/(16π²) ~ O(10⁻²), where θ are NGFP critical exponents.

**Finding from Liu-Prokopec-Starobinsky (2018):** They provide a specific relation derived from the Demmel et al. FRG calculation:
```
b₀ = 40 / (55296π² a₀ + 95)
```
where a₀ is the R² coefficient. This formula shows that **b is NOT simply θ/(16π²)** — it involves the specific beta function of the R² coupling from the FRG flow equation. The b ~ θ/(16π²) claim is an order-of-magnitude estimate, not a proper derivation.

**Critical assessment:** The parameter b is treated as a PHENOMENOLOGICAL PARAMETER in all published work. It is NOT uniquely predicted by the NGFP. It depends on:
1. Which critical exponent dominates the approach to the fixed point
2. The truncation scheme and regulator choice
3. The matter content
4. The RG improvement scheme (how k maps to physical quantities)

### A2. NGFP Critical Exponents Across Truncations — HARD NUMBERS

From the Codello-Percacci-Rahmede paper (2009, Ann. Phys. 324:414, arXiv:0805.2909), Table 4.2 gives critical exponents ϑᵢ at the NGFP for f(R) polynomial truncations up to R^n:

| n | Re(ϑ₀,₁) | Im(ϑ₀,₁) | ϑ₂ | ϑ₃ | Re(ϑ₄) | Im(ϑ₄) | ϑ₆ | ϑ₇ | ϑ₈ |
|---|----------|----------|------|------|---------|---------|------|------|------|
| 1 | 2.382 | 2.168 | — | — | — | — | — | — | — |
| 2 | 1.376 | 2.325 | 26.862 | — | — | — | — | — | — |
| 3 | 2.711 | 2.275 | 2.068 | -4.231 | — | — | — | — | — |
| 4 | 2.864 | 2.446 | 1.546 | -3.911 | -5.216 | — | — | — | — |
| 5 | 2.527 | 2.688 | 1.783 | -4.359 | -3.761 | -4.880 | — | — | — |
| 6 | 2.414 | 2.418 | 1.500 | -4.106 | -4.418 | -5.975 | -8.583 | — | — |
| 7 | 2.507 | 2.435 | 1.239 | -3.967 | -4.568 | -4.931 | -7.572 | -11.076 | — |
| 8 | 2.407 | 2.545 | 1.398 | -4.167 | -3.519 | -5.153 | -7.464 | -10.242 | -12.298 |

**Key observations:**
- **3 relevant (UV-attractive) directions:** ϑ₀,₁ (complex pair with Re ≈ 2.4) and ϑ₂ (real, ≈ 1.4). These are positive.
- **All higher directions are irrelevant:** ϑ₃ ≈ -4.2, ϑ₄ ≈ -3.5 to -5.2, etc. (negative)
- **ϑ₂ converges to ~1.4** (initially anomalous at n=2 where ϑ₂ = 26.9, but settles from n=3 onward)
- **Re(ϑ₀,₁) converges to ~2.4**

With different trace prescriptions (Table 4.4, n=8):
- α-gauge: Re(ϑ₁) = 2.123, Im(ϑ₁) = 2.796, ϑ₂ = 1.589, ϑ₃ = -4.212
- β-gauge: Re(ϑ₁) = 2.049, Im(ϑ₁) = 2.511, ϑ₂ = 1.438, ϑ₃ = -3.928

From the vertex expansion (Denz-Pawlowski-Reichert, 2018, Eur.Phys.J. C78):
- Approximation 1: θ̄ᵢ = (-4.7, -2.0±3.1i, 2.9, 8.0)
- Approximation 2: θ̃ᵢ = (-5.0, -0.37±2.4i, 5.6, 7.9)
- Three UV-attractive directions confirmed

From on-shell perturbation theory (arXiv:2411.00938), critical exponent convergence:
| Order | θ |
|-------|------|
| O(R¹) | 2.0 |
| O(R²) | 2.296 |
| O(R³) | 2.312 |
| O(R⁴) | 2.312 |
| O(R⁵) | 2.311 |
| O(R∞) | 2.311 |

### A3. Computing b from Critical Exponents

**Using the naive formula b ~ θ/(16π²):**

With the converged Re(ϑ₀,₁) ≈ 2.4:
```
b ≈ 2.4 / (16π²) ≈ 2.4 / 158 ≈ 0.015
```

With ϑ₂ ≈ 1.4:
```
b ≈ 1.4 / 158 ≈ 0.009
```

With the on-shell θ ≈ 2.31:
```
b ≈ 2.31 / 158 ≈ 0.015
```

**Range from naive formula: b ∈ [0.009, 0.015]**

**Using the Liu-Prokopec perturbative formula:**
For Starobinsky inflation, a₀ ~ 10⁹ (from COBE normalization), so:
```
b₀ = 40 / (55296π² × 10⁹ + 95) ≈ 7 × 10⁻¹⁴
```
This gives b ≈ 0 — consistent with pure Starobinsky.

**CRITICAL TENSION:** The naive NGFP estimate (b ~ 0.01) and the perturbative FRG formula (b ~ 10⁻¹⁴) give vastly different answers. This reflects a fundamental issue:
1. The perturbative formula applies at sub-Planckian curvatures (inflationary regime)
2. The NGFP estimate applies near the Planck scale
3. The enormous RG running between these scales (factor of ~10⁵ in energy) suppresses b from ~10⁻² to ~10⁻¹⁴
4. **Conclusion: b is effectively zero at inflationary scales.** The logarithmic correction is negligible.

### A4. Inflationary Predictions for Different b Values

From Liu-Prokopec-Starobinsky (2018) and Bonanno-Platania, with b treated as a free parameter:

| b value | n_s (N=60) | r (N=60) | Status |
|---------|-----------|----------|--------|
| 0 | 0.967 | 0.003 | Standard Starobinsky |
| 10⁻⁴ | ~0.967 | ~0.003 | Negligible shift |
| 10⁻³ | ~0.968 | ~0.004 | Small shift |
| 10⁻² | ~0.971 | ~0.007 | Moderate shift |
| 0.02 | ~0.973 | ~0.009 | Approaches tension resolution |
| 0.05 | ~0.975 | ~0.01 | Resolves tension, r near detection |

To resolve the n_s tension (shift n_s from 0.967 to ~0.974), one needs b ~ 0.02–0.05.

**The NGFP does NOT predict b in this range from first principles.** The RG flow from the Planck scale to inflationary scales suppresses b to effectively zero. The b parameter remains a free phenomenological parameter.

---

## Part B: Six-Derivative δ₃ from NGFP — THE CRITICAL FINDING

### B1. The R³ Coupling at the NGFP — ACTUAL NUMBERS from Codello-Percacci-Rahmede

From Table 4.1 of Codello-Percacci-Rahmede (2009), the NGFP fixed-point values for the dimensionless R³ coupling g̃₃* (values multiplied by 10³):

| Truncation order n | 10³ × g̃₃* | g̃₃* | Status |
|-------------------|-----------|-------|--------|
| 3 (first appearance) | -9.682 | -0.00968 | — |
| 4 | -10.967 | -0.01097 | — |
| 5 | -9.687 | -0.00969 | — |
| 6 | -10.198 | -0.01020 | — |
| 7 | -9.784 | -0.00978 | — |
| 8 | -8.581 | -0.00858 | — |

**The R³ fixed-point coupling converges to g̃₃* ≈ -(0.86–1.10) × 10⁻² across truncations n=3 to n=8.**

The corresponding critical exponent for the R³ direction is **ϑ₃ ≈ -4.2** (negative = irrelevant = PREDICTED, not free).

With different trace prescriptions (Table 4.3, n=8):
| Gauge | 10³ × g̃₃* |
|-------|-----------|
| α-gauge | -6.726 |
| β-gauge | -6.133 |

So the spread including gauge variation is: **g̃₃* ∈ [-0.011, -0.006]**

Other fixed-point couplings for context (n=8, Table 4.1, ×10³):
- g̃₀* = 5.066 (cosmological constant term)
- g̃₁* = -20.748 (Newton's constant term)
- g̃₂* = 0.088 (R² coupling — VERY SMALL, approaches zero)
- g̃₃* = -8.581 (R³ coupling — our target)
- Λ̃* = 0.122, G̃* = 0.959, Λ̃*G̃* = 0.117

### B2. Falls-Litim-Schröder 2019 (PRD 99, 126015) — f(R) to R^70

This paper confirmed and extended the Codello et al. results to R^70 polynomial order:
- 3 relevant directions at ALL truncation orders (robust)
- R³ and all higher couplings are irrelevant (predicted)
- The gap between the 3rd relevant and 1st irrelevant exponents grows with truncation order → robust prediction
- Fixed-point values converge, confirming the stability of the g̃₃* value

### B3. The Observational Target: δ₃ ≈ -1.19 × 10⁻⁴

From arXiv:2505.10305 ("Curvature corrections to Starobinsky inflation can explain the ACT results"):
- With N=55 e-folds and δ₃ = -1.19 × 10⁻⁴: n_s ≈ 0.974, r ≈ 0.0045
- ACT DR6 data: n_s = 0.9743 ± 0.0034
- The R³ correction with this δ₃ value resolves the tension between Starobinsky and ACT

Also from arXiv:2511.06640 ("Starobinsky Inflation and the Latest CMB Data"):
- Using α₀ notation for the cubic correction:
  - Planck+LiteBIRD: α₀ = (-2.6⁺²·⁵₋₂.₄) × 10⁻⁵
  - Planck+ACT+LiteBIRD: α₀ = (-8.1⁺⁴·³₋₄.₇) × 10⁻⁵
- The different notation gives a range of O(10⁻⁵ to 10⁻⁴) depending on convention

**Important:** The paper treating δ₃ as a free parameter notes it is NOT derived from any specific quantum gravity theory. They acknowledge it "may arise in quantum gravity or effective field theory frameworks" but provide no specific derivation.

### B4. Mapping NGFP g̃₃* to Physical δ₃ — The Gap

**The normalization problem:**

In Codello et al., the action is: Γ = ∫ d⁴x √g Σₙ gₙ Rⁿ

The dimensionless couplings are: g̃ₙ = gₙ k^(2n-4), so:
- g₃ (physical R³ coefficient, units [mass]⁻²) = g̃₃ × k⁻²
- At the NGFP (k ~ M_P): g₃ = g̃₃* / M_P²

The inflation papers typically normalize as: f(R) = R + R²/(6M²) + δ₃ R³, where δ₃ has units [mass]⁻⁴. Or alternatively, with overall M_P²/2 factor: S ⊃ (M_P²/2) ∫ [R + R²/(6M²) + δ₃ R³/M⁴].

**The conversion requires knowing the SCALE at which δ₃ is evaluated.**

The NGFP g̃₃* is the value at the UV fixed point (k → ∞, effectively k ~ M_P). The inflationary δ₃ is evaluated at the inflationary scale (R ~ H² ~ 10⁻¹⁰ M_P²).

Since the R³ direction is IRRELEVANT (ϑ₃ ≈ -4.2), the coupling is determined by:
```
g̃₃(k) ≈ g̃₃* + c₃ × (k₀/k)^|ϑ₃|
```
As k → 0 (IR, inflationary scales), g̃₃(k) → g̃₃*. The dimensionless coupling FREEZES at its fixed-point value for an irrelevant direction.

But the PHYSICAL coupling is g₃(k) = g̃₃(k)/k², which DIVERGES as k → 0. This means the R³ contribution to the action becomes:
```
g₃(k) R³ ~ (g̃₃*/k²) R³
```

For this to be small at inflationary scales (as required for perturbativity): R³/k² must be small, i.e., R << k (the curvature must be below the RG scale, which is the usual EFT regime).

**The upshot:** A direct numerical comparison between g̃₃* ≈ -0.01 and δ₃ ≈ -1.19 × 10⁻⁴ is NOT straightforward because:
1. They use different normalizations
2. They're evaluated at different scales
3. The running from NGFP to inflation is non-trivial
4. The RG scale identification in the gravitational sector is ambiguous

**However, three key observations:**
1. **g̃₃* is NEGATIVE** — matching the sign needed for δ₃ < 0
2. **g̃₃* is O(10⁻²) in dimensionless units** — after accounting for the M²/M_P ratio and other normalization factors, this could be consistent with δ₃ ~ O(10⁻⁴)
3. **The R³ direction IS irrelevant** — the value IS predicted by the NGFP, not free

### B5. Could the Numbers Match? A Rough Estimate

Taking the Codello et al. convention seriously:
- g₁* = g̃₁*/k² (Newton's constant term): g̃₁* ≈ -0.021, so g₁ = M_P²/2 → k² = -g̃₁*/g₁ = 0.021/(M_P²/2) → this determines the matching scale

The Starobinsky mass M ~ 1.3 × 10¹³ GeV (from COBE normalization, a ~ 10⁹, M² = M_P²/(6a)).

The ratio M²/M_P² ~ 10⁻¹⁰.

If we crudely estimate: δ₃ ~ g̃₃* × (M²/M_P²) ~ (-0.01) × 10⁻¹⁰ = -10⁻¹², this is FAR too small.

If instead the normalization involves M⁴/M_P⁴: δ₃ ~ g̃₃* × (M/M_P)⁴ ~ -0.01 × 10⁻²⁰ — even worse.

**This suggests the NGFP g̃₃* alone cannot directly give δ₃ ~ 10⁻⁴.** The needed δ₃ requires an R³ contribution much LARGER than what the naive NGFP running produces.

**But there's a subtlety:** In the QG+F framework, the R³ term arises as a TREE-LEVEL coupling (part of the classical action), not from quantum running. The NGFP in the unified framework would need to produce a tree-level R³ coupling that persists to inflationary scales. This is a different mechanism from the loop-generated running captured by the FRG.

---

## Part C: Classification of Predictions

### Parameter b (Logarithmic R² Correction)

**Classification: NOT DISCRIMINATING — effectively b ≈ 0 in all frameworks**

| Framework | b value | Status |
|-----------|---------|--------|
| Standalone QG+F | b = 0 (no mechanism) | No R² running |
| Standalone AS | b ~ 10⁻¹⁴ (perturbative) or b ~ 0.01 (naive NGFP estimate) | Not uniquely predicted |
| Unified framework | b ~ 10⁻¹⁴ (perturbative FRG) | Same as AS alone |

The perturbative calculation gives b ~ 10⁻¹⁴, effectively zero. This does NOT resolve the n_s tension. The naive NGFP estimate b ~ 0.01 is not a rigorous derivation and is contradicted by the full FRG calculation. **b is not a discriminating prediction.**

### Parameter δ₃ (R³ Coupling)

**Classification: POTENTIALLY DISCRIMINATING — but the calculation is incomplete**

| Framework | δ₃ status | Predictive? |
|-----------|-----------|-------------|
| Standalone QG+F | Free tree-level parameter | No — unconstrained |
| Standalone AS | Irrelevant direction at NGFP; g̃₃* ≈ -0.01 | In principle yes, but mapping to δ₃ not done |
| Unified framework | Should be determined by NGFP + running | Yes — but requires full calculation |

**Key facts supporting potential discrimination:**
1. The R³ coupling IS irrelevant at the NGFP (ϑ₃ ≈ -4.2) → it IS predicted, not free
2. g̃₃* is NEGATIVE across all truncations → correct sign for n_s shift
3. g̃₃* shows reasonable convergence: -(0.006 to 0.011) across truncations and gauges
4. In standalone QG+F, δ₃ is completely free — the unified framework reduces this freedom

**Key facts opposing a definitive claim:**
1. The numerical mapping g̃₃* → δ₃ has NOT been done
2. Rough estimates suggest the NGFP running gives a much smaller R³ contribution than needed
3. The QG+F R³ term is tree-level; the NGFP generates it via quantum running — different mechanisms
4. Scheme/gauge dependence introduces factor-of-2 uncertainty in g̃₃*

---

## Summary and Key Numbers

### Consolidated Critical Exponent Table (Best Values)

| Direction | ϑ (Codello et al., n=8) | Nature | Associated coupling |
|-----------|------------------------|--------|---------------------|
| ϑ₀,₁ | 2.41 ± 2.55i | RELEVANT (UV-attractive) | Λ̃, G̃ |
| ϑ₂ | 1.40 | RELEVANT (UV-attractive) | R² coupling |
| ϑ₃ | -4.17 | IRRELEVANT (predicted) | R³ coupling |
| ϑ₄,₅ | -3.52 ± 5.15i | IRRELEVANT (predicted) | R⁴ coupling |
| ϑ₆ | -7.46 | IRRELEVANT | R⁵+ |
| ϑ₇ | -10.24 | IRRELEVANT | R⁶+ |
| ϑ₈ | -12.30 | IRRELEVANT | R⁷+ |

### R³ Fixed-Point Coupling (Codello et al.)

**g̃₃* ≈ -(0.86–1.10) × 10⁻² (standard tables)**
**g̃₃* ≈ -(0.61–0.67) × 10⁻² (alternative trace prescription)**

### Bottom Line

1. **b is NOT predicted** by the NGFP and is effectively zero at inflationary scales → does NOT resolve n_s tension
2. **δ₃ is IN PRINCIPLE predicted** by the NGFP (irrelevant direction) with correct sign (negative), but:
   - The full numerical mapping to physical δ₃ at inflationary scales has not been computed
   - Rough estimates suggest the NGFP running alone may produce too small a δ₃
   - The needed δ₃ ≈ -1.19 × 10⁻⁴ is a tree-level contribution, while the NGFP generates quantum running
3. **The unified framework's strongest case:** If the tree-level R³ coupling in the UV completion is SET by the NGFP irrelevant direction, then δ₃ is predicted. But this requires the conceptual claim that the NGFP fixed-point value g̃₃* determines the tree-level QG+F coupling — a claim that has not been derived.
4. **What's needed:** A calculation solving the full RG trajectory from the NGFP to inflationary scales in a 6-derivative truncation, extracting the physical R³ coupling and comparing with δ₃ ≈ -1.19 × 10⁻⁴. This is a well-defined computational problem.

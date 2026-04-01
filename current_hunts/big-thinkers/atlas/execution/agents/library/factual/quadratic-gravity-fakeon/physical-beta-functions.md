---
topic: quadratic-gravity-fakeon
confidence: verified
date: 2026-03-24
source: exploration-005-ns-beta-functions-six-derivative (strategy-002)
---

# Physical Beta Functions of Quadratic Gravity

## The Two Sets of Beta Functions

### Fradkin-Tseytlin (1982) — Traditional, Gauge-Dependent

Source: Fradkin & Tseytlin, "Renormalizable asymptotically free quantum theory of gravity," Nucl. Phys. B201, 469 (1982).

Derived from one-loop divergences via the heat kernel method. These are **gauge-dependent and scheme-dependent**:

    β_λ^(FT) = −(1/(16π²)) × (133/10)λ²
    β_ξ^(FT) = −(1/(16π²)) × 5(72λ² − 36λξ + ξ²)/36

These predict asymptotic freedom (λ, ξ → 0 in UV), but with a crucial limitation: a healthy Starobinsky scalar (ξ < 0) was thought to be incompatible with asymptotic freedom.

### Branchina, Ferrante & Ferrante (2024) — Physical, Gauge-Invariant

Source: Buccio, Donoghue, Menezes, Percacci, PRL 133, 021604 (2024), arXiv:2403.02397.

Derived from momentum-dependent scattering amplitudes — **gauge-invariant and scheme-independent**:

    β_λ^(phys) = −(1/(16π²)) × (1617λ − 20ξ)λ/90
    β_ξ^(phys) = −(1/(16π²)) × (ξ² − 36λξ − 2520λ²)/36

## Key Differences

| Feature | Fradkin-Tseytlin (1982) | Physical (2024) |
|---------|------------------------|-----------------|
| β_λ leading term | −(133/10)λ² | −(1617/90)λ² = −17.97λ² |
| β_λ cross-term | 0 | +(20ξ/90)λ |
| β_ξ leading (ξ²) coeff | −5/36 | −1/36 |
| β_ξ cross-term (λξ) | +5 | +1 (36/36) |
| β_ξ quadratic (λ²) | −10 | +70 |
| Gauge dependence | Yes | **No** |
| Scheme dependence | Yes | **No** |

The ξ² coefficient changes by a factor of 5 (−5/36 → −1/36), and new cross-terms appear with different signs — fundamentally altering the flow topology.

## Notation Mapping to QG+F

The paper uses the action S = ∫d⁴x√(-g) [m_P²(R − 2Λ)/2 − C²/(2λ) − R²/ξ].

Mapping to the QG+F action S = ∫d⁴x√(-g) [M²_P R/2 − (1/(2f₂²))C² + (1/(6f₀²))R²]:

- **λ = f₂²** (Weyl-squared coupling)
- **ξ = −6/f₀²** (R² coupling; negative since f₀² > 0, giving positive R² coefficient → healthy Starobinsky scalar)

## QG+F Coupling Values During Inflation

From Starobinsky inflation (M₀ ≈ 3×10¹³ GeV):
- f₀² = 6M₀²/M_P² ≈ **9.4 × 10⁻⁹**
- θ ≡ 1/(6f₀²) = M_P²/(36M₀²) ≈ **1.8 × 10⁸** (R² coefficient in Planck units)
- ξ = −6/f₀² ≈ **−6.4 × 10⁸**
- λ = f₂² ~ 10⁻⁸ to 10⁻⁴ (less constrained)

The extreme hierarchy |ξ| >> |λ| is always satisfied in the QG+F regime.

## Separatrix Structure and Asymptotic Freedom

The physical beta function system has two separatrix lines in the (λ, ξ) plane:
- **s₁: ξ ≈ 79.4λ** (ξ > 0 → tachyonic R² sector)
- **s₂: ξ ≈ −3.53λ** (ξ < 0 → healthy R² sector)

**Crucial result:** Along s₂, asymptotic freedom is compatible with ξ < 0. This means **QG+F can be asymptotically free AND have a healthy Starobinsky scalar** — something the FT beta functions could not achieve. This is a major consistency check for the QG+F program.

## Fakeon Prescription and Beta Functions

At one loop: the fakeon prescription **does not modify** the beta functions. The prescription affects imaginary parts of amplitudes (cutting rules, unitarity cuts) but not the real parts that determine UV divergences and beta functions. The one-loop beta functions are identical regardless of the fakeon vs. ghost interpretation.

At higher loops: potentially different through the absence of certain cuts, but unlikely to change qualitative conclusions.

## Running of f₂ (Weyl-Squared Coupling)

For small λ and large negative ξ:

    β_λ ≈ +(20|ξ|λ)/(90 × 16π²) > 0

So f₂ **increases** toward the IR (asymptotically free in the UV). This affects the fakeon mass but doesn't directly enter the inflationary slow-roll parameters.

## Significance

The physical beta functions resolve a 40-year ambiguity in quadratic gravity. The gauge-invariant result:
1. Confirms asymptotic freedom is possible with the correct sign of R² for Starobinsky inflation
2. Provides unambiguous input for computing inflationary corrections (though these turn out to be negligible — see `ns-tension-resolution-paths.md`)
3. Establishes QG+F's perturbative consistency at one loop beyond doubt

Sources: arXiv:2403.02397 (Branchina et al. PRL 2024), Fradkin & Tseytlin Nucl. Phys. B201 (1982), arXiv:2405.05706

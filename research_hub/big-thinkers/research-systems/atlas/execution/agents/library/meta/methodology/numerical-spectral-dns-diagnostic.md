---
topic: Numerical spectral analysis on DNS data as diagnostic tool
confidence: confirmed
date: 2026-03-30
source: "vasseur-pressure s2-meta-004"
---

## Lesson

**Numerical spectral analysis on DNS data (frequency-resolved energy decomposition) is a powerful diagnostic tool for mathematical questions about PDE structure.** It can reveal whether an obstruction is a high-frequency or low-frequency phenomenon — information that purely analytical arguments would miss.

## Evidence

Vasseur-pressure Strategy-002, Exploration 004: The commutator decomposition of P^{21} has two parts — the commutator terms and the divergence-error remainder. Analytically, both are O(1). But the numerical spectral decomposition revealed:

- **Commutator part**: faster spectral decay (better high-frequency regularity)
- **Remainder part**: 18x larger at wavenumber k=20 (dominates high frequencies)

This immediately tells us that any improvement route based on the commutator must somehow handle the high-frequency remainder — it's not just a perturbation. This diagnostic information was invisible to the analytical computation (which only showed both terms are O(1) in the same norm).

## Protocol

When testing whether a mathematical structure (compensated compactness, commutator, cancellation) applies to a PDE decomposition:

1. **Compute the decomposition numerically on DNS data** at moderate resolution (N=64 sufficient for qualitative structure)
2. **Measure L^2 norms** of each component (absolute and as fraction of total)
3. **Compute spectral energy distribution** (Fourier-space energy per wavenumber band)
4. **Compare spectral decay rates** between components
5. **Report the dominant component at high frequencies** — this identifies the analytical bottleneck

## When to Apply

- When an analytical decomposition has multiple terms and you need to know which term limits the overall regularity
- When testing whether a cancellation/structure improvement is "large enough" to matter
- When a mathematical argument predicts a certain regularity gain and you want to check whether numerical evidence supports it before committing to a full analytical proof attempt

## Relationship to Other Lessons

Distinct from `sufficient-ic-diversity-for-outliers` (which is about choosing initial conditions; this is about frequency-resolved analysis of a fixed decomposition). Complementary to `include-trivial-control-checks` (numerical spectral analysis serves as a consistency check on analytical claims about regularity). Related to `math-explorer-dimensional-analysis` in spirit — both use numerical computation to resolve analytical questions that would otherwise remain ambiguous.

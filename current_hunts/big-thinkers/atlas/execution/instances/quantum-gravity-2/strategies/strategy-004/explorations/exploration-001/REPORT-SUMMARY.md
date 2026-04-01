# Exploration 001 Summary: Ghost Propagator Specification

## Goal
Derive the specific quantitative prediction for the spin-2 ghost propagator in C²-extended FRG, for the unified QG+F–AS framework.

## What Was Tried
Searched for and extracted numerical values from five key papers: Benedetti et al. (2009) for NGFP fixed-point couplings, Draper et al. (2020) for the complex pole tower mechanism, Knorr-Saueressig (2022) for propagator reconstruction methodology, Becker et al. (2017) for the scalar ghost mass-divergence mechanism, and Lü et al. (2015) for the BH instability threshold. Cross-referenced with the existing Atlas library on ghost fate mechanisms.

## Outcome: PARTIAL SUCCESS

The prediction can be sharpened significantly beyond "the ghost should dissolve somehow," but a fully discriminating numerical prediction remains blocked by one uncomputed quantity.

## Key Results

**Ghost mass at the NGFP:** m₂/k = √(g₁*/g₃*) = √(0.0101/0.0050) = √2.02 ≈ **1.42** (from Benedetti et al. fixed-point values). Physical mass: m₂ ~ 0.5–2 M̄_P. BH instability threshold: r_H ≈ 0.876/m₂ ≈ 0.6 l_P (sub-Planckian).

**Predicted mechanism:** Complex conjugate pole tower (Draper et al. type). The perturbative Stelle ghost pole at p² = −m₂² dissolves into infinite towers of poles at imaginary p², with form G_TT(p²) = 1/(p²(1 + p² f_C(p²))) where f_C interpolates from constant (IR) to tanh form (UV). Mass divergence is RULED OUT for spin-2 (g₃* ≠ 0 at NGFP).

**Computational specification:** Compute spin-2 TT propagator in (R + R² + C²) FRG truncation with momentum-dependent form factors. Unified prediction: complex pole tower. Null hypothesis: persistent real ghost pole requiring external fakeon prescription.

**Classification:** Partially discriminating (can refute but not uniquely confirm unification), novel (neither framework alone predicts C² pole tower), numerically specific to factor ~4 for m₂.

## Key Takeaway

The prediction is a **well-specified falsifiable consistency check**, not a sharp discriminating prediction. The deepest discriminating content is the **amplitude equivalence test**: do scattering amplitudes from the complex pole tower equal fakeon-prescription amplitudes? This requires the actual C²-extended FRG computation — which has never been done by anyone. The single most valuable next step would be identifying whether any group is pursuing this computation, or whether the framework can predict the value of c_C (the dimensionless pole-spacing parameter) from first principles.

## Leads Worth Pursuing
1. Has anyone computed (or is computing) the C²-extended FRG propagator? This is the critical missing calculation.
2. Can the amplitude equivalence (fakeon ↔ complex pole tower) be tested analytically in a toy model before the full gravity computation?
3. The parameter c_C might be constrained by the critical exponents at the NGFP — worth checking.

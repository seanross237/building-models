# Exploration 006: EFT-Hedron — Computational Verification of Positivity Bounds

## Mission Context

The EFT-hedron (Arkani-Hamed, T.-C. Huang, Y.-T. Huang, arXiv:2012.15849, JHEP 2021) translates positive geometry into concrete, real-world constraints on Wilson coefficients of effective field theories. This is the most concrete physical consequence of the amplituhedron program — it gives specific inequalities that constrain which EFTs can be UV-completed.

Prior explorations established that the amplituhedron is a reformulation within N=4 SYM, but the EFT-hedron extends the program to real-world physics. Now we need to verify this computationally.

## Your Goal

**Implement the EFT-hedron positivity constraints for 2→2 scalar scattering and photon-photon scattering. Compute specific bounds on Wilson coefficients. Verify against published results. Characterize what these bounds physically imply.**

This is a COMPUTATION task. Write modular scripts. Break into stages.

## Background

For a generic 2→2 EFT amplitude, the low-energy expansion is:

M(s,t) = Σ_{p,q} g_{p,q} s^p t^q (+ crossing symmetry constraints)

where g_{p,q} are Wilson coefficients. The EFT-hedron says:

**If M(s,t) admits a UV completion (i.e., comes from a UV-complete, unitary, local theory), then the g_{p,q} must satisfy certain positivity and nonlinear constraints.**

The simplest constraint is g_{2,0} ≥ 0 (the forward-limit positivity bound, known since Adams et al. 2006). The EFT-hedron gives infinitely many more:

1. **Linear positivity bounds**: Certain linear combinations of g_{p,q} must be ≥ 0.
2. **Nonlinear bounds**: Certain determinants formed from g_{p,q} must be ≥ 0 (Hankel matrix positivity).
3. **Two-sided bounds**: Some coefficients are bounded from both above and below, given others.

## What to Compute

### Stage 1: Scalar 2→2 Basics

Implement the partial wave expansion for 2→2 scalar scattering:

M(s,t) = 16π Σ_l (2l+1) a_l(s) P_l(cos θ)

where a_l(s) are partial wave amplitudes satisfying 0 ≤ Im(a_l) ≤ 1 (unitarity).

Use the dispersive representation:
g_{p,q} = (1/π) ∫_{M²}^∞ ds' ρ(s') / s'^(p+q+1) × [polynomial in l]

where ρ(s') is the spectral function.

### Stage 2: Forward Limit Bounds

Compute the forward-limit (t=0) positivity bounds:
- g_{2,0} ≥ 0 (the Adams et al. bound)
- g_{3,0} ≥ 0
- Higher: g_{n,0} ≥ 0 for all n ≥ 2

These are the simplest bounds. Verify you get the same signs as the published results.

### Stage 3: Hankel Matrix Bounds

The key EFT-hedron result: form the Hankel matrix H_{ij} = g_{i+j,0}. Then:

det(H) ≥ 0 for all principal submatrices

This gives nonlinear bounds. For 2×2:
g_{2,0} × g_{4,0} ≥ g_{3,0}²

Compute the first few Hankel determinants and verify.

### Stage 4: Photon-Photon (If Time)

For photon-photon scattering, the EFT amplitude involves:
M = α₁ F⁴ + α₂ F²F̃² + β₁ D²F⁴ + ...

The EFT-hedron bounds constrain combinations of α₁, α₂, β₁, etc. These have been applied to low-energy QED and to gravity. Implement the photon-photon bounds if time allows.

### Stage 5: Physical Interpretation

For each bound computed:
- What does it physically imply? (E.g., "if g_{2,0} < 0, the EFT cannot come from any UV-complete theory")
- Does it constrain any known theory?
- How tight are the bounds compared to known UV completions?

## Implementation Notes

- Use numpy for linear algebra, scipy for integration
- Break into modular scripts: `partial_waves.py`, `forward_bounds.py`, `hankel_bounds.py`
- Use simple numerics — this is about verifying the structure, not about precision

## Success Criteria

- **SUCCESS**: Forward limit and Hankel bounds computed and matching published results. Physical interpretation of each bound provided.
- **PARTIAL**: Forward bounds computed but Hankel or photon-photon incomplete.
- **FAILURE**: Cannot implement the basic dispersive representation.

## Output

Report: `explorations/exploration-006/REPORT.md` (target 200-400 lines)
Summary: `explorations/exploration-006/REPORT-SUMMARY.md`
Code: `explorations/exploration-006/code/`

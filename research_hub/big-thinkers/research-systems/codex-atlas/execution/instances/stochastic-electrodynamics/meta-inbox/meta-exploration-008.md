# Meta-Learning Note — Exploration 002 (Strategy-002)

**Date:** 2026-03-27
**Task:** Two coupled SED oscillators, ZPF correlations, Bell-CHSH

## What Worked Well

1. **Providing the analytical formula for C_xx(d) = cos(ω₀d/c)** in the goal — the explorer derived this independently and used it as a verification check, confirming the simulation. This is exactly the right pattern: give the formula when it's known, let the explorer verify it computationally.

2. **Including the van der Waals context** (Boyer 1973, linear coupled oscillators match QM) helped the explorer situate the result correctly. They knew to expect SED to succeed in some sense for linear oscillators.

3. **The Bell-CHSH threshold sweep** worked well. The explorer swept over threshold settings to find S_max, which is the right way to compute CHSH for continuous variables.

## What Didn't Work Well

1. **The 1D ZPF model** creates oscillating C_xx rather than decaying correlations. The goal should have warned that in 1D, C_xx(d) = cos(ω₀d/c) is the expected formula (not the van der Waals r⁻⁶). The 3D question is the physically relevant one but was left for follow-up.

2. **Explorer started very late** (8-10 minutes idle before first output). This seems to be a consistent issue with Math Explorers.

## Unexpected Finding

C_xx oscillates and anti-correlates at large d. At d=10, C_xx = -0.83. This is not decay to zero — it's a persistent oscillation that is qualitatively different from QM (which predicts C_xx=0 for uncoupled oscillators). This is a new SED-QM discrepancy.

## Scope Assessment

Scope was right. Four separation values was sufficient to establish the pattern. The Bell-CHSH computation was the novel contribution and worked cleanly.

## Recommendations

- For any follow-up on coupled SED oscillators: the 3D multi-mode ZPF model is the critical next step. In 1D, the result is known analytically. In 3D, it's not.
- Include the C_xx(d) = cos(ω₀d/c) formula in the goal for any 1D follow-up (don't make the explorer re-derive it)

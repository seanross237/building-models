---
topic: Modified inertia vs. modified gravity is not a labeling choice — specify this distinction upfront in any modified-dynamics exploration
category: goal-design
date: 2026-03-27
source: "compton-unruh strategy-001 meta-exploration-008"
---

## Lesson

In any exploration of "modified dynamics" (MOND-like theories), require the explorer to specify
upfront whether the modification is to **inertia** (m_i in F = m_i a) or to **gravity** (the
Poisson equation for Φ). This is not a labeling choice — it has concrete, decisive observational
consequences, especially for gravitational lensing. Failing to specify this early causes the
exploration to conflate two theories with very different empirical signatures.

## Evidence

**compton-unruh strategy-001 exploration-008** — Seven prior explorations built and tested the
T_U/T_dS model, including rotation curve fits (χ²/dof ~ 1 for NGC 3198 and NGC 2403). None of
them identified that the model, as modified inertia, is observationally falsified by gravitational
lensing. The adversarial exploration (E008) immediately caught this by asking: "what does this
modification do to the Poisson equation?"

The answer: **modified inertia changes m_i but leaves ∇²Φ = 4πGρ unchanged**. Photons travel
on geodesics of Φ. Therefore lensing is unaffected by the inertia modification, and lensing
masses are predicted to equal baryonic masses only. Observed cluster lensing masses are 5–10×
above baryonic — the model is falsified by every well-studied cluster.

This failure was intrinsic and would have been identified at exploration 3 or 4 if the
inertia/gravity distinction had been specified in the goal.

## The Concrete Consequences

| Modified Inertia (changes m_i) | Modified Gravity (changes ∇²Φ) |
|-------------------------------|-------------------------------|
| Poisson equation unchanged | Poisson equation modified |
| Photon geodesics = baryonic potential only | Photon geodesics enhanced by modified potential |
| Cluster lensing: fails by 5–10× | Cluster lensing: partially enhanced (MOND: ~5.7×) |
| Bullet Cluster: predicts lensing at gas, not stars | Same morphology problem, but amplitude OK |
| Momentum conservation: not guaranteed | Guaranteed via Lagrangian (AQUAL) |
| Action principle: absent | Action principle: Bekenstein-Milgrom AQUAL |

## Recommended Goal Language

Add to any modified-dynamics goal:

> "At the outset, specify whether the model modifies **inertia** (F = m_i a, Poisson equation
> unchanged) or **gravity** (Poisson equation modified). This is decisive for gravitational
> lensing predictions. For each observational test, state which type of modification is assumed."

## Relationship to Other Entries

- `use-classification-schemes.md` — Force honest binary classification; FATAL/SERIOUS/MODERATE
  for failure modes; apply the inertia/gravity classification to each observational test.
- `specify-failure-paths.md` — Include "if this is modified inertia, predict lensing masses and
  compare to Bullet Cluster" as a mandatory failure path.
- `require-quantification-in-stress-tests.md` — The lensing failure is only decisive when
  quantified (5.7× vs. baryonic mass, not just "lensing might be a problem").

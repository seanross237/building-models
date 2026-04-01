---
topic: Include 5+ ICs covering different flow topologies to catch outliers
category: methodology
date: 2026-03-30
source: "vasseur-pressure meta-exploration-002"
---

## Lesson

For measurement campaigns involving initial conditions or input configurations, use **at least 5 ICs covering different structural classes** (symmetry types, flow topologies, spectral characteristics). Fewer ICs risk missing qualitatively different behavior from structurally distinct configurations.

## Evidence

- **vasseur-pressure exploration-002** — The ABC (Arnold-Beltrami-Childress) flow was the 5th IC tested and produced dramatically different results: beta_eff = 1.01 (vs 0.35-0.73 for the other 4 ICs), R^2 = 0.999 (vs 0.78-0.97), and gamma > 1 at all Re (vs gamma < 1 for most others at Re >= 500). With only 3-4 ICs (Taylor-Green, Vortex Tubes, Random Gaussian, Kida), the most important finding — that Beltrami structure provides genuine analytical leverage — would have been missed entirely.

## When to Apply

- DNS measurement campaigns where the quantity of interest may depend on flow structure
- Parameter sweeps where qualitative behavior (not just quantitative values) can vary across configurations
- Any exploration testing universality claims — the outlier is the most informative data point

## Design Guidance

Cover distinct structural classes rather than 5 variations of the same type:
- **Symmetric vs. random** (Taylor-Green vs. Random Gaussian)
- **2D-like vs. fully 3D** (z-invariant tubes vs. ABC)
- **Special algebraic structure** (Beltrami: curl u = u; Kida: high-symmetry vortex)
- **Low vs. high intermittency** (U_0 ranges from ~100 to ~5000 across ICs)

## Relationship to Other Entries

Distinct from `anticipate-symmetry-degeneracies-in-ics.md` (which is about *avoiding* ICs where the quantity vanishes; this is about *including enough* to catch qualitative outliers). Distinct from `require-trend-tabulation-for-negative-results.md` (presentation format vs. IC selection). Complements `require-independent-verification-baseline.md` (verification = checking the same answer twice; this = systematic coverage to avoid missing phenomena).

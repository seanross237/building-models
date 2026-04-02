---
topic: Brezis-Gallouet-Wainger estimate fails in 3D for H^1 fields — C ≤ 0.81 is a DNS artifact
confidence: verified
date: 2026-03-30
source: "navier-stokes strategy-002 exploration-002/004 (adversarial review)"
---

## Overview

The Brezis-Gallouet-Wainger (BGW) logarithmic Sobolev estimate, which bounds ||S||_{L^inf} ≤ C * ||omega||_{L^inf} * [1 + log(||grad omega||/||omega||)], is **NOT valid in 3D** with only H^1 regularity. The empirically observed C ≤ 0.81 from DNS is a **resolution artifact** from the spectral dealiasing cutoff.

**Status: SUPERSEDED** — the BKM enstrophy proof (see `bkm-enstrophy-theorem-l4-proof.md`) uses the L4 interpolation approach instead, which requires no BGW estimate.

## The Obstruction

In 3D, the critical Sobolev embedding H^s ↪ L^∞ requires s > 3/2. The enstrophy equation provides only ||grad omega||_{L2}, giving H^1 regularity — not H^{3/2}.

In Fourier space: bounding the high-frequency tail ∑_{|k|>Λ} |ω̂(k)| requires summable weights. With ||grad omega||_{L2}, we have |ω̂(k)| ≤ ||omega||_{L2}/|k| decaying like 1/|k|. But ∑_{|k|>Λ} 1/|k|^2 **diverges in 3D** (harmonic series).

The 3D BGW estimate requires H^{5/2} regularity (not H^1):
||f||_{L^inf} ≤ C * ||f||_{H^{3/2}} * (1 + log(||f||_{H^s}/||f||_{H^{3/2}}))^{1/2} for s > 3/2

## Why C ≤ 0.81 Is an Artifact

On a spectral grid with N/3 dealiasing cutoff, the Fourier sum becomes finite (truncated to |k| ≤ N/3). The "BGW constant" measured in DNS is actually the constant of a finite-dimensional inequality that has no continuum limit. As N → ∞, the sum diverges and C → ∞.

## Literature

- Brezis-Gallouet (1980), Brezis-Wainger (1980): original estimates, work in 2D or require H^{d/2+1} in d dimensions
- In 3D: H^{d/2+1} = H^{5/2}, far stronger than the H^1 available from the enstrophy equation

## Significance

This negative result motivated the switch to the L4 interpolation approach (Lemma 3 in the BKM enstrophy theorem), which sidesteps the L^∞ control problem entirely. The identification of the 3D BGW obstruction is a useful methodological warning for NS regularity research.

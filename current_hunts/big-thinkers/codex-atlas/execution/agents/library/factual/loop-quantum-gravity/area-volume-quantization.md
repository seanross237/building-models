---
topic: loop-quantum-gravity
confidence: verified
date: 2026-03-22
source: https://arxiv.org/html/2412.14156
---

# LQG Area and Volume Quantization

## Area Spectrum

A central result of LQG is that geometric operators (area, volume) have discrete eigenvalues. The area operator acting on a surface S that is punctured by spin network edges has the eigenvalue formula:

A = 8 * pi * gamma * l_P^2 * sum_I sqrt(j_I * (j_I + 1))

where:
- gamma is the Barbero-Immirzi parameter (~0.274)
- l_P is the Planck length (~1.616 x 10^-35 m)
- j_I are the spin quantum numbers (half-integers: 0, 1/2, 1, 3/2, ...) labeling the SU(2) representations on edges puncturing the surface
- The sum is over all edges I that intersect the surface

The smallest nonzero area eigenvalue (the "area gap") occurs for j = 1/2:

A_min = 4 * pi * gamma * sqrt(3) * l_P^2

This is approximately 10^-70 m^2.

## Volume Quantization

Volume operators associated with regions of space also have discrete spectra. Volume eigenvalues arise from the recoupling theory of spin network edges meeting at nodes (vertices). The volume spectrum is more complex than the area spectrum and depends on the specific structure of the intertwiner at each node.

## Critical Caveat: Gauge Invariance

An important open question is whether this kinematical discreteness survives at the gauge-invariant (physical) level. Research by Dittrich and Thiemann (arXiv:0708.1721) has shown that "kinematical discreteness of the spectrum does not necessarily survive at the gauge invariant level. Whether or not this happens depends crucially on how the gauge invariant completion is performed." Discrete spectra of gauge-dependent operators can become continuous when converted to gauge-invariant observables. This means fundamental discreteness at the Planck scale in LQG remains formally unestablished at the fully physical level.

Sources:
- https://arxiv.org/html/2412.14156
- https://ar5iv.labs.arxiv.org/html/0708.1721
- https://pmc.ncbi.nlm.nih.gov/articles/PMC5567241/

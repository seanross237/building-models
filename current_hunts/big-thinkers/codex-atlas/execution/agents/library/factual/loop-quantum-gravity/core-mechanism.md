---
topic: loop-quantum-gravity
confidence: verified
date: 2026-03-22
source: https://pmc.ncbi.nlm.nih.gov/articles/PMC5567241/
---

# LQG Core Mechanism: Ashtekar Variables, Holonomies, and Spin Networks

Loop Quantum Gravity is a non-perturbative, background-independent quantization of general relativity. Its core mechanism proceeds in several steps:

## Ashtekar-Barbero Connection Formulation

Classical GR is reformulated using a phase space based on a smooth real SU(2) connection A^i_a(x) and a densitized triad (electric field) E^a_i(x). The connection relates to the extrinsic curvature via:

A^i_a = Gamma^i_a + gamma * K^i_a

where Gamma^i_a is the spin connection compatible with the triad, K^i_a is the extrinsic curvature, and gamma is the Barbero-Immirzi parameter. Setting gamma = i yields Ashtekar's original self-dual SL(2,C) connection; real values of gamma (the Barbero connection) give a real SU(2) gauge theory.

## Holonomies and Wilson Loops

The fundamental variables for quantization are not the connection itself but holonomies (parallel transports of the connection along edges) and fluxes of the densitized triad across surfaces. Wilson loops — traces of holonomies around closed loops — satisfy the Mandelstam identities. The set of Wilson lines and electric field fluxes forms an overcomplete coordinate system on the phase space that is closed under Poisson brackets, providing the departure point for quantization.

## Spin Networks

Spin networks (introduced by Penrose, adopted by Rovelli and Smolin) resolve the overcompleteness of the loop basis. A spin network is a graph where:
- Each edge carries an irreducible SU(2) representation (labeled by spin j = 0, 1/2, 1, 3/2, ...)
- Each node carries an intertwiner (invariant tensor coupling the representations of adjacent edges)

Spin networks form an orthonormal basis for the gauge-invariant kinematical Hilbert space of LQG. They represent quantum states of 3-dimensional spatial geometry.

## Spin Foams

Spin foams provide the covariant (path integral) formulation. A spin foam is a 2-complex with faces labeled by representations and edges labeled by intertwiners. It represents a history interpolating between spin network states — the boundary of a spin foam is a spin network, analogous to how a manifold's boundary is a lower-dimensional manifold. The evolution has characteristic scale on the order of the Planck length (~10^-35 m).

Sources:
- https://pmc.ncbi.nlm.nih.gov/articles/PMC5567241/
- https://arxiv.org/abs/gr-qc/0409061
- https://en.wikipedia.org/wiki/Spin_foam

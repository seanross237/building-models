---
topic: loop-quantum-gravity
confidence: verified
date: 2026-03-22
source: https://pmc.ncbi.nlm.nih.gov/articles/PMC5567241/
---

# LQG Spin Networks

Spin networks are the fundamental mathematical objects representing quantum states of the gravitational field in Loop Quantum Gravity. They form an orthonormal basis for gauge-invariant quantum states in the theory's Hilbert space.

## Structure

A spin network is a colored graph consisting of:

- **Edges (links)**: One-dimensional, oriented lines, each carrying an irreducible SU(2) representation labeled by a half-integer spin value j (j = 1/2, 1, 3/2, 2, ...). The spin labels derive from the same mathematics as spin numbers in particle physics.
- **Nodes (vertices)**: Zero-dimensional junction points where edges meet. Each node contains invariant tensors (intertwiners) that satisfy Clebsch-Gordan conditions, ensuring gauge invariance at the junction.

Spin network states solve the "overcompleteness problem" that plagued earlier loop representations in LQG, providing a complete, orthonormal basis for calculations.

Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC5567241/

## Quantized Geometry

A key physical result is that the quantum operators for area and volume have discrete spectra:

- Each **node** in a spin network represents an elementary "quantum of volume" -- a chunk of three-dimensional space.
- Each **link** represents a "quantum of area" of the surface separating adjacent volume quanta.
- The area eigenvalues are given by a(j) = 8pi l_p^2 gamma sqrt(j(j+1)), where l_p is the Planck length and gamma is the Barbero-Immirzi parameter.
- Area discreteness occurs at the scale of the Planck area, approximately 10^-66 square centimeters.

This discreteness is not imposed by hand but emerges naturally from the quantum geometry, realizing Wheeler's concept of "spacetime foam." Physical space exhibits a polymer-like structure at the smallest scales.

Source: https://www.einstein-online.info/en/spotlight/spin_networks/

## Spin Foams: Evolution of Spin Networks

Spin foams extend spin networks into the time dimension. While spin networks describe the quantum geometry of space at a single moment, spin foams model how that geometry evolves over time, providing a spacetime picture. A spin foam is essentially the "worldsheet" traced out by an evolving spin network.

The covariant (spin foam) formulation provides a path-integral approach to the dynamics. The dominant modern formulation is the EPRL model (Engle-Pereira-Rovelli-Livine), with additional contributions from Freidel (FK model) and Lewandowski (KKL model). The evolution of spin networks has a characteristic scale on the order of the Planck length, approximately 10^-35 meters.

Source: http://jdc.math.uwo.ca/spin-foams/

## Mathematical Formalism

### Hilbert Space Construction
Quantum states are constructed as functionals of the SU(2) connection. Cylindrical states -- functionals depending only on holonomies along graph links -- form a complete basis. The Ashtekar-Lewandowski measure provides rigorous mathematical grounding: the scalar product involves integration over SU(2) using the Haar measure, creating a well-defined inner product on cylindrical functions.

### Loop Operators
Elementary operators include:
- **Wilson loop operators**: trace of holonomy around closed loops
- **Higher-order loop variables**: Wilson loops with E-field insertions
- **Grasp operations**: fundamental operations acting on loop states

These generate a Poisson algebra representation on the quantum Hilbert space. The loop transform provides unitary equivalence between the loop representation (direct algebraic formulation using spin network basis) and the connection representation (wave functionals of the SU(2) connection, formalized through C*-algebra methods).

### Computational Elements
Spin foam amplitudes rely on quantities called "10j symbols" that encode geometric and quantum information. The mathematical machinery employs Penrose spin networks, SU(2) representation theory, Kauffman recoupling theory, Temperley-Lieb algebras, and C*-algebraic spectral methods.

Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC5567241/

## Quantum Spin Dynamics
The theory permits networks to evolve through creation and annihilation of lines, with spin labels increasing or decreasing -- a process termed "Quantum Spin Dynamics" by analogy with quantum chromodynamics.

Source: https://www.einstein-online.info/en/spotlight/spin_networks/

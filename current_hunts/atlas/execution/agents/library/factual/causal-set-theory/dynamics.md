---
topic: causal-set-theory
confidence: verified
date: 2026-03-22
source: https://arxiv.org/abs/gr-qc/9904062
---

# Dynamics of Causal Sets

## Classical Sequential Growth (CSG) Dynamics

The leading dynamical model for causal sets was developed by Rideout and Sorkin (1999). In CSG dynamics, the universe grows one element at a time in a stochastic process of "cosmological accretion."

### The Growth Process

At each stage n, a new element e_{n+1} is "born" as the offspring of some subset of the existing n elements (those that will lie in its causal past). The transition from a causal set of n elements to one of n+1 elements is governed by a probability distribution.

### Axioms

The CSG dynamics is derived from two physical principles:

1. **Discrete General Covariance (Label Invariance)**: The probability of producing a particular causal set is independent of the order in which elements are born. Only the final causal structure matters, not the labeling of elements. This is the discrete analogue of diffeomorphism invariance.

2. **Bell Causality**: The probability of a new element being born to the future of a given set of elements depends only on the causal past of those elements, not on spacelike-separated parts of the causet. This is a discrete form of relativistic causality.

### Coupling Constants

These two axioms constrain the dynamics to a family of models parameterized by countably many coupling constants {t_0, t_1, t_2, ...}. Each t_k governs the relative probability of births involving k-element "precursor sets." The resulting models are called "generalized percolation" dynamics.

### Emergent Matter

A striking feature: the CSG dynamics can be expressed as state models for Ising spins living on the causal relations. This demonstrates how non-gravitational matter (analogous to gauge fields) can arise dynamically from the causal set without being built in at the fundamental level.

## The Benincasa-Dowker Action

The discrete analogue of the Einstein-Hilbert gravitational action was found by Benincasa and Dowker (2010). In 4 dimensions, the action for a causal set C is:

    S[C]/hbar = N - N_1 + 9*N_2 - 16*N_3 + 8*N_4

where N is the total number of elements and N_k counts the number of (k+1)-element inclusive order intervals (causal intervals of size k+1).

In the continuum limit (for a causal set faithfully embedded in a spacetime), the mean of this action converges to the integral of the Ricci scalar:

    <S> -> integral( R * sqrt(|g|) d^4x )

This was later generalized to arbitrary spacetime dimensions by Dowker and Glaser.

## The Discrete d'Alembertian

A discrete version of the d'Alembertian wave operator (Box) was constructed from alternating sums of scalar field values at elements at fixed order-theoretic distances. In the continuum limit, it converges to the standard d'Alembertian, enabling a theory of scalar fields propagating on a causal set background.

## Toward Quantum Dynamics

The CSG models are classical (stochastic). The major open challenge is to construct a quantum version -- a quantum sequential growth process with complex amplitudes replacing probabilities. This requires a quantum measure theory (or "decoherence functional") compatible with general covariance, which remains an active area of research.

Sources:
- https://arxiv.org/abs/gr-qc/9904062
- https://www.emergentmind.com/topics/causal-set-approach-to-quantum-gravity
- https://www.einstein-online.info/en/spotlight/causal_sets/
- https://arxiv.org/abs/1103.6272

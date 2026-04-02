---
topic: asymptotic-safety
confidence: verified
date: 2026-03-22
source: https://pmc.ncbi.nlm.nih.gov/articles/PMC5256001/
---

# Asymptotic Safety in Quantum Gravity: Core Idea and Framework

Asymptotic safety (also referred to as nonperturbative renormalizability) is a scenario for constructing a consistent and predictive quantum theory of the gravitational field without requiring perturbative renormalizability. It was proposed by Steven Weinberg in 1976/1979.

## The Problem

General relativity is perturbatively nonrenormalizable because Newton's constant G has negative mass dimension (mass dimension -2 in 4D). Divergences appear at one-loop level with matter fields, and at two-loop level in pure gravity. Standard perturbative quantization fails. Asymptotic safety retains quantum fields as the theoretical arena and instead abandons only the traditional program of perturbative renormalization.

## The Solution: Nonperturbative Renormalizability

Asymptotic safety generalizes the concept of renormalizability. Instead of requiring coupling constants to vanish in the UV (asymptotic freedom), the theory requires all dimensionless coupling constants to approach finite values at a nontrivial (non-Gaussian) UV fixed point of the renormalization group flow.

### Mathematical Definition

In an asymptotically safe theory, dimensionless couplings g_i satisfy:

lim (mu -> infinity) g_i(mu) = g_i*, where 0 < g_i* < infinity

The couplings do not need to be small or tend to zero in the high energy limit but rather tend to finite values: they approach a nontrivial UV fixed point.

### Key Requirements (Weinberg's Conditions)

1. A nontrivial UV fixed point must exist in the RG flow.
2. The UV critical surface (the set of trajectories attracted to the fixed point at high energies) must be finite-dimensional, ensuring predictivity -- the number of free parameters equals the dimension of this surface.

## How It Differs from Asymptotic Freedom

In asymptotic freedom (e.g., QCD), couplings flow to the trivial Gaussian fixed point (g = 0) in the UV. In asymptotic safety, couplings flow to a nontrivial interacting fixed point (g = g* != 0). Both scenarios render the theory UV complete and predictive.

## The Functional Renormalization Group Approach

The effective average action Gamma_k depends on an infrared cutoff scale k. It satisfies an exact functional renormalization group equation (the Wetterich equation adapted to gravity). This framework is valid beyond perturbation theory and enables nonperturbative treatment of gravitational fluctuations. The FRG has been the main tool enabling progress in Asymptotic Safety over the last 20+ years.

## Einstein-Hilbert Truncation Results

In the simplest truncation of the form:

Gamma_k[g] = (1/16piG_k) integral d^4x sqrt(g)(R - 2*Lambda_k)

with two running couplings (Newton's constant G_k and cosmological constant Lambda_k), a nontrivial non-Gaussian fixed point is clearly present. Results show convergence across different truncation schemes.

## Key Evidence from Multiple Frameworks

1. **2 + epsilon expansion**: Newton's constant exhibits asymptotic safety in 2+epsilon dimensions with a one-dimensional unstable manifold.
2. **Higher derivative theories**: Strictly renormalizable theories with quartic curvature terms contain a non-Gaussian fixed point.
3. **Large N expansion**: Including O(N) matter fields leads to a nontrivial fixed point with a three-dimensional unstable manifold.
4. **2+2 symmetry reduction**: Restricting to geometries with two commuting Killing vectors yields a model where all linearized perturbations decay for mu -> infinity.
5. **Truncated FRGE results**: The Einstein-Hilbert truncation and extensions with matter couplings consistently show a non-Gaussian fixed point.

## Anti-screening Mechanism

The scenario posits that quantum gravitational self-interactions predominantly exhibit anti-screening in the ultraviolet -- analogous to the mechanism underlying asymptotic freedom in Yang-Mills theory. In four dimensions, Einstein gravity is "antiscreening": Newton's constant increases at large distances.

## Status

The idea remains a conjecture. No rigorous proof exists that gravity possesses a suitable fixed point in the exact theory, but substantial evidence from functional RG computations supports the scenario.

Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC5256001/

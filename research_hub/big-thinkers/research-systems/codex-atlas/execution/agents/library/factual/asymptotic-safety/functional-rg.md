---
topic: asymptotic-safety
confidence: verified
date: 2026-03-22
source: https://arxiv.org/abs/0708.1317
---

# Functional Renormalization Group Approach to Gravity

The primary computational tool for investigating asymptotic safety in quantum gravity is the Wetterich equation (also called the functional renormalization group equation, FRGE), adapted to the gravitational setting.

## The Wetterich Equation

The exact flow equation for the effective average action Gamma_k takes the form:

    d/dt Gamma_k = (1/2) Tr [ (Gamma_k^(2) + R_k)^{-1}  d/dt R_k ]

where:
- t = ln(k) is the logarithmic RG scale
- Gamma_k^(2) is the second functional derivative (Hessian) of the effective average action
- R_k is an infrared regulator that suppresses fluctuations with momenta below k
- The trace Tr sums over all field modes

This equation is exact -- it encodes the full nonperturbative RG flow. It implements the Wilsonian idea of integrating out quantum fluctuations shell-by-shell in momentum space.

## Einstein-Hilbert Truncation

The simplest truncation ansatz for the gravitational effective average action is:

    Gamma_k[g] = (1/16 pi G_k) integral d^4x sqrt(g) (R - 2 Lambda_k) + S_gf + S_ghost

where G_k and Lambda_k are the running Newton constant and cosmological constant, S_gf is the gauge-fixing term, and S_ghost is the Faddeev-Popov ghost action.

Inserting this ansatz into the Wetterich equation and projecting onto the relevant operators yields coupled beta functions for the dimensionless couplings g_k = k^2 G_k and lambda_k = Lambda_k / k^2.

## Key Properties of the Flow Equation

1. No explicit UV cutoff dependence -- the equation is finite.
2. It interpolates between the microscopic action (k -> infinity) and the full quantum effective action (k -> 0).
3. The one-loop approximation is recovered by replacing Gamma_k^(2) with the bare action S^(2) on the right-hand side.
4. Truncations are necessary in practice because the full theory space is infinite-dimensional.

## The 2+epsilon Expansion

In d = 2+epsilon dimensions, the beta function for Newton's constant has the form:

    dg_N/d(ln mu) = (d-2) g_N + gamma g_N^2

where gamma depends on the reference operator. This yields a nontrivial fixed point at g_N* = (2-d)/gamma with a one-dimensional unstable manifold.

## Key Reference

The foundational textbook treatment is: M. Reuter and F. Saueressig, "Quantum Gravity and the Functional Renormalization Group: The Road towards Asymptotic Safety" (Cambridge University Press, 2019).

Source: https://arxiv.org/abs/0708.1317
Additional source: https://arxiv.org/pdf/2003.00044

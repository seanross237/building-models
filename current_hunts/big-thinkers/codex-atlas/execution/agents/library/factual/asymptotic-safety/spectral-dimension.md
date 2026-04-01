---
topic: asymptotic-safety
confidence: verified
date: 2026-03-22
source: https://arxiv.org/abs/hep-th/0511260
---

# Spectral Dimension Running in Asymptotic Safety

A striking prediction of asymptotically safe gravity is that the effective dimensionality of spacetime changes with the energy scale, a phenomenon known as dynamical dimensional reduction.

## The Result

The spectral dimension d_s of spacetime flows from:
- **d_s = 4** at macroscopic (IR) length scales
- **d_s = 2** at sub-Planckian (UV) length scales

This result, derived by Lauscher and Reuter (2005), is an exact consequence of asymptotic safety and does not depend on the specific truncation used.

## How Spectral Dimension Is Defined

The spectral dimension is defined via the return probability P(T) of a random walk (diffusion process) on the spacetime manifold. For a diffusion time T:

    P(T) = Tr[exp(-T * Delta)]

where Delta is the Laplacian on the manifold. The spectral dimension is:

    d_s = -2 d(ln P)/d(ln T)

For a smooth d-dimensional manifold, d_s = d. Quantum corrections modify the effective Laplacian, changing the scaling behavior.

## Connection to the Anomalous Dimension

The dimensional reduction is driven by the anomalous dimension eta_N of Newton's constant at the fixed point. At the non-Gaussian fixed point in d=4:

    eta_N = -2

This large anomalous dimension modifies the graviton propagator at short distances, so that it behaves as in a 2-dimensional theory. The residual interactions become effectively two-dimensional in the extreme UV.

## Universality Across Approaches

The d_s -> 2 result in the UV is remarkably universal. It appears independently in:
- **Asymptotic safety** (Lauscher and Reuter, via FRG): three scaling regimes emerge -- classical (d_s = 4), quantum near fixed point (d_s = 2), and intermediate semiclassical
- **Causal Dynamical Triangulations** (CDT): numerical simulations find d_s = 4.02 +/- 0.10 at large distances and d_s = 1.80 +/- 0.25 at small distances; reduction occurs at about ten Planck lengths
- **Horava-Lifshitz gravity** and other modified gravity theories (curvature-squared models)
- **Loop quantum gravity** / spin foam models: flow from d_s = 4 to d_s = 2 at small scales
- **Causal Set Theory**: Myrheim-Meyer dimension shows d_MM ~ 2 for small sets
- **High-temperature string theory**: thermodynamic dimension d_th1 = 2
- **Noncommutative geometry**: models (Snyder space, kappa-Minkowski) also show dimensional reduction
- **Polymer quantization** approaches
- **Wheeler-DeWitt analysis** in the short-distance limit

This convergence across independent approaches to quantum gravity is considered strong evidence for the physical reality of dimensional reduction. Carlip (arXiv:1705.05417, Universe 5(3):83, 2019) notes this convergence "seems rather unlikely...merely by accident," and CDT results have been "checked independently and verified analytically in a simplified toy model."

## Mechanism in Asymptotic Safety

The mechanism is mathematically precise: operators at the fixed point acquire precisely the anomalous dimensions necessary to make the theory appear two-dimensional. This occurs because the Einstein-Hilbert action is scale-invariant only in two dimensions. At the non-Gaussian ultraviolet fixed point, the gravitational anomalous dimension eta_N = 2 - d produces propagators with 1/p^d behavior, formally equivalent to massless fields in two-dimensional theory.

## Physical Interpretation

At the UV fixed point, spacetime acquires a fractal-like microstructure with local Hausdorff dimension 2. This suggests that quantum gravity effectively reduces the number of active degrees of freedom at the shortest scales, potentially resolving UV divergences through geometric means. Multiple measurement methods (spectral, thermodynamic, Hausdorff) yield consistent d ~ 2 results.

## CDT Evidence for Asymptotic Safety

Coumbe and Jurkiewicz (arXiv:1411.7712, JHEP 2015) found that CDT simulations show "the dimension of spacetime smoothly decreases from approximately 4 on large distance scales to approximately 3/2 on small distance scales." This may help resolve longstanding theoretical objections to the asymptotic safety scenario.

Source: https://arxiv.org/abs/hep-th/0511260
Additional sources: https://ar5iv.labs.arxiv.org/html/1705.05417, https://arxiv.org/abs/1411.7712

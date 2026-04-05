---
topic: loop-quantum-gravity
confidence: verified
date: 2026-03-22
source: https://arxiv.org/html/2412.14156
---

# LQG Black Hole Entropy

## The Bekenstein-Hawking Formula

The target result is the Bekenstein-Hawking entropy:

S = k_B * A / (4 * l_P^2)

where A is the horizon area, l_P is the Planck length, and k_B is Boltzmann's constant.

## LQG Derivation

In LQG, the entropy calculation proceeds as follows (Ashtekar, Baez, Corichi, Krasnov, 1997):

1. The geometry outside a black hole is described by spin networks, some of whose edges puncture the event horizon.
2. Each puncture contributes a quantum of area: a(j) = 8*pi*l_P^2*gamma*sqrt(j(j+1)).
3. The quantum geometry of the horizon is described by a U(1) Chern-Simons theory (or SU(2) in later formulations).
4. The entropy is obtained by counting the number of distinct spin network microstates consistent with a total horizon area A.

## The Immirzi Parameter Issue

The LQG entropy calculation yields the correct A/4 proportionality only when the Barbero-Immirzi parameter is fixed to:

gamma = ln(2) / (pi * sqrt(3)) ≈ 0.274

This value must be chosen specifically to match the Bekenstein-Hawking result. This has been criticized because gamma appears as a free parameter that must be tuned rather than predicted. The area spectrum and all geometric eigenvalues depend on gamma, so its value affects the entire theory.

## Microstate Interpretation

A strength of the LQG approach: the microstates have a clear geometric interpretation — they are the distinct quantum geometries of the horizon consistent with its macroscopic area and topology. This contrasts with some other approaches where the nature of the microstates is less transparent.

## Higher-Order Corrections

LQG predicts logarithmic corrections to the Bekenstein-Hawking entropy:

S = A / (4 * l_P^2) - (3/2) * ln(A / l_P^2) + O(1)

The -3/2 coefficient of the logarithmic correction is a robust prediction independent of the Immirzi parameter.

## Recent Developments

More recent work in the covariant (spin foam) formulation has derived the first law of black hole mechanics, the Unruh temperature, and the Hawking entropy distribution directly from the full quantum theory, for generic non-singular black holes, and independently of the Immirzi parameter. This has been described as the only known derivation of this formula from a fundamental theory for generic non-singular black holes.

## Derivation Methods for the Immirzi Parameter

Multiple independent methods converge on the same value of gamma:

### Traditional Approach (Boltzmann-Gibbs Statistics)
Equating the Bekenstein-Hawking entropy with microstate counting on punctured surfaces yields the standard gamma value when the minimum spin j_min = 1/2.

### Landauer Principle Method
By applying Landauer's principle -- connecting information erasure to thermodynamic cost -- researchers derive the same gamma value without invoking Boltzmann-Gibbs statistics directly. When a black hole loses one bit of information, the area quantum matches predictions from information theory.

### Alternative Entropy Frameworks
The research extends to modified entropy models:
- **Barrow Entropy**: gamma_B depends on a fractal deformation parameter Delta and horizon area, recovering the standard gamma as Delta approaches 0.
- **Modified Kaniadakis Entropy**: gamma_MKE increases with deformation parameter kappa and scales with horizon area, also reducing to standard gamma when kappa approaches 0.

### Complex Immirzi Parameter
Some researchers argue that the quantum degrees of freedom of a spherical black hole correspond to an SU(2) Chern-Simons theory when the Immirzi parameter takes the special values plus or minus i, strongly indicating that gamma may be a regulator that should be fixed to plus or minus i at some point.

Source: https://arxiv.org/html/2412.14156

Sources:
- https://arxiv.org/html/2412.14156
- https://en.wikipedia.org/wiki/Immirzi_parameter
- https://pmc.ncbi.nlm.nih.gov/articles/PMC5567241/
- https://arxiv.org/abs/hep-th/9808091
- https://arxiv.org/abs/gr-qc/0407052

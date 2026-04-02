---
topic: barandes-stochastic
confidence: provisional
date: 2026-03-28
source: barandes-stochastic strategy-001 exploration-004
---

# Fundamental Gaps: Phase Erasure and Structural Limitations

The ISP transition matrix Gamma_ij = |Theta_ij|^2 is the modulus squared of the amplitude, deliberately erasing phase information. This coarse-graining creates four fundamental (not merely technical) gaps.

## Gap 1 -- Entanglement Completely Obscured (FUNDAMENTAL)

Entanglement entropy, Schmidt rank, entanglement witnesses -- all defined via off-diagonal density matrix elements. ISP erases the phase information needed to compute entanglement.

**The stochastic data says nothing about entanglement:** Two ISPs with the same Gamma can correspond to separable and maximally entangled quantum states (the multiple-Theta freedom). A two-qubit system in the singlet state |Psi^-> = (|01> - |10>)/sqrt(2) has the SAME diagonal density matrix elements as the maximally mixed state rho = I/4. The ISP for both has the same transition matrix.

This is inherent to the coarse-graining -- the "classical" spirit of ISP deliberately suppresses the information that encodes entanglement.

## Gap 2 -- No Continuous Generators (PARTIALLY TECHNICAL)

The Schrodinger equation gives a local generator H specifying dynamics everywhere, with H = T + V making eigenvalue problems natural, perturbation theory straightforward, and conservation laws (Noether) transparent. ISP specifies Gamma(t<-t_0) for pairs of times -- no natural generator exists.

Recovering H requires log of U = Theta, which involves choosing a branch of the matrix logarithm (compounding the phase freedom). A "generator" formalism within ISP would inherit the same phase non-uniqueness, making it much more complicated than the Hermitian H of standard QM.

Barandes acknowledges this: ISPs are specified by transition maps, not generators. But this means ISP describes *quantum processes* (what happens from t_0 to t), not *quantum systems* (what structure the system has). For most physics, you want the latter.

## Gap 3 -- QFT and the Standard Model Out of Reach (FUNDAMENTAL)

ISP requires a finite configuration space (N states). QFT operates in infinite-dimensional Fock space. Three specific failures:

1. **Particle creation/annihilation:** e+e- -> 2gamma changes particle number. The "configuration space" changes. ISP has no mechanism for changing N.
2. **Lorentz symmetry:** ISP uses non-relativistic configuration space (positions). Lorentz-covariant ISP would require stochastic processes on spacetime, running into relativistic causality problems.
3. **Renormalization:** UV divergences arise from infinite-dimensional QFT. ISP avoids this by working in finite N -- an avoidance, not a solution.

Explicitly acknowledged by Barandes as "future work," but the obstacles are not merely technical -- ISP's ontological commitment to a classical configuration space conflicts with the field-theoretic picture where fields (not particles) are fundamental.

## Gap 4 -- Superposition Invisible (FUNDAMENTAL)

In Hilbert space, superposition is explicit: |L> + |R> with computable interference fringes. In ISP, a double-slit particle is described by a non-Markovian stochastic process where the transition matrix cannot be factored. Interference is present but encoded only as non-factorizability.

You cannot look at the ISP transition matrix and say "interference is happening here" -- only "this matrix can't be factored." This is analogous to knowing a process has memory without knowing why or how. The Hilbert space formulation makes the mechanism (amplitude superposition) transparent; ISP correctly identifies interference as a source of non-Markovianity but gives no insight into the mechanism.

## Summary

All four gaps stem from the same root cause: the deliberate suppression of phase information in the ISP description. This is not a bug but a feature of the framework's "deflationary" stance. However, it means that the very information quantum mechanics was built to organize (phases, amplitudes, coherences) is systematically unavailable in the ISP language.

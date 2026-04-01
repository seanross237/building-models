---
topic: SED established successes
confidence: verified
date: 2026-03-27
source: "SED strategy-001 exploration-002 (landscape survey); Boyer 2019 review"
---

## SED Systems That Match QM Exactly

### The Core Four

| System | SED Result | Key Reference |
|--------|-----------|---------------|
| Harmonic oscillator ground state | E_0 = 1/2 hbar omega, Gaussian distribution | Marshall (1963), Boyer (1975); numerically confirmed SED exploration-001 |
| Casimir effect | F = -pi^2 hbar c / (240 a^4) | Boyer (1973) |
| Van der Waals forces | Correct 1/r^6 (unretarded) and 1/r^7 (retarded) | Boyer (1973) |
| Blackbody radiation | Planck spectrum rho(omega, T) | Boyer (1969), Marshall (1965) |

### Additional Successes

- **Diamagnetism:** Correct diamagnetic susceptibility of a charged harmonic oscillator (follows directly from HO result).
- **Unruh effect:** Boyer showed uniformly accelerated detector in ZPF sees thermal spectrum (deep result but hard to compute quantitatively).
- **Specific heat decrease at low temperatures:** SED's quantized oscillator energy naturally gives the Einstein model of specific heats.

### Key Pattern

All 4+3 successes involve either **linear systems** (harmonic oscillators) or **free-field calculations** (Casimir, blackbody). This is not coincidental -- linearity is the key ingredient enabling SED's successes.

### Important Caveat on the HO Result

The HO "success" is specifically for the **position distribution** (variance + Gaussianity) and
**potential energy**. The total energy is UV-divergent in SED and is NOT directly comparable to
E0 = hbar*w0/2 without mass renormalization. The velocity variance also diverges logarithmically
with the UV cutoff. See sed-ho-uv-divergence-structure.md for details.
For numerical verification and parameter sensitivity, see sed-ho-numerical-verification.md.

### References

- Marshall, T.W. (1963). "Random Electrodynamics." Proc. R. Soc. A 276, 475.
- Boyer, T.H. (1969). "Derivation of the Blackbody Radiation Spectrum without Quantum Assumptions." Phys. Rev. 182, 1374.
- Boyer, T.H. (1973). "Retarded van der Waals forces at all distances." Phys. Rev. A 7, 1832.
- Boyer, T.H. (1975). "Random electrodynamics." Phys. Rev. D 11, 790.
- Boyer, T.H. (2019). "Stochastic Electrodynamics: The Closest Classical Approximation to Quantum Theory." Atoms 7(1), 29. [arXiv:1903.00996]

# Q9 — CARS — Opus Run 2 (Hybrid M2+M4)

## PLAN
**Constraints/entities extracted:**
- CARS = Coherent Anti-Stokes Raman Scattering (nonlinear four-wave mixing)
- Broadband CARS microscopy with a broadband pump beam
- Anti-Stokes signal at ωAS = ωp - ωS + ωprobe; vibrational resonance when ωp - ωS matches molecular vibration
- Broadband pump: many frequency pairs drive multiple vibrational modes simultaneously

**Shortest path (3 steps):**
1. Can a broadband pump generate an anti-Stokes signal? (eliminates A, E)
2. Does the anti-Stokes signal contain distinguishable vibrational info? (discriminates B vs C)
3. Select answer

## SOLVE
- **Step 1**: Broadband pump contains many frequency components. Intrapulse beating between different frequency pairs acts as simultaneous pump+Stokes excitation, generating a coherent anti-Stokes signal. Eliminates A and E.
- **Step 2**: Each spectral component of the anti-Stokes output maps to a specific vibrational frequency (ωvib = ωp - ωS). Spectrally resolving the anti-Stokes beam recovers distinct vibrational modes — this is the foundation of multiplex/broadband CARS spectroscopy. Eliminates B.
- **Step 3**: Answer is C.

**Opposite check**: Could the information be scrambled/indistinguishable (favoring B)? No — spectral resolution of the anti-Stokes output directly maps to vibrational frequencies. The entire utility of broadband CARS depends on this distinguishability.

## ANSWER: C

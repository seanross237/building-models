# Riemann Hypothesis — Unconventional Attack Strategies

## Background

The Riemann Hypothesis (RH) is a Clay Millennium Prize Problem worth $1M. It states that all nontrivial zeros of the Riemann zeta function lie on the critical line Re(s) = 1/2. If true, it implies the primes are distributed as regularly as they possibly can be.

Recent work by Sean Hartnoll and Ming Yang ("The Conformal Primon Gas at the End of Time", arXiv 2502.02661, Feb 2025) found that gravitational dynamics near black hole singularities naturally produce a "primon gas" — a system whose partition function is related to the Riemann zeta function. This reopened interest in physics-based approaches to RH.

This directory documents 10 cross-disciplinary attack strategies and tracks experimental attempts on the most promising ones.

## The 10 Strategies

See `approaches/` for full documentation of each strategy.

### Novelty Tier List

| Rank | Strategy | Direction | Novel? | Feasible for us? |
|------|----------|-----------|--------|-------------------|
| 1 | 5A — Spectral Breeder | Evolved CA | Yes — completely unoccupied | Very high (Python + GPU) |
| 2 | 4A — Billiard Table Inversion | Quantum Reservoir | Yes — tools exist, nobody tried | High (FEM + optimization) |
| 3 | 2A — Entropy Ceiling | Primon Gas Thermo | Yes — microcanonical gap | High (math + numerics) |
| 4 | 3B — Knot Surgery / Li Coefficients | Arithmetic Topology | Yes — three fields unassembled | Medium (SnapPy + math) |
| 5 | 1A — Cut-and-Project Guillotine | Quasicrystal | Partially — basic tests undone | Medium (numerics + theory) |
| 6 | 2B — Holographic Primon Censorship | Primon Gas Thermo | Yes — specific framing novel | Low (deep QG expertise) |
| 7 | 3A — Chern-Simons Zeta Machine | Arithmetic Topology | Partially — U(1) extension open | Low (specialist math) |
| 8 | 1B — Bragg or Bust | Quasicrystal | Partially novel | Medium (specialist math) |
| 9 | 4B — Chaotic Echo Spectroscopy | Quantum Reservoir | Partially novel | No (needs lab) |
| 10 | 5B — Arithmetic Terrarium | Evolved CA | Somewhat novel | High (compute only) |

## Experiments

See `experiments/` for computational attempts on the top 3 strategies.

- `experiments/5A-spectral-breeder/` — Evolving CAs to match GUE statistics
- `experiments/4A-billiard-inversion/` — Shape-optimizing billiard domains to match zeta zeros
- `experiments/2A-entropy-ceiling/` — Microcanonical entropy analysis of the primon gas (run 2026-04-04: canonical concavity proved, ensemble equivalence gap identified, Fisher information variational principle proposed)

## Key References

- Hartnoll & Yang, "The Conformal Primon Gas at the End of Time" (arXiv 2502.02661)
- Julia (1990), "Statistical mechanics and the partition function of number theory"
- Montgomery (1973), pair correlation conjecture
- Odlyzko (1987), numerical verification of Montgomery's conjecture
- Dyson (2009), quasicrystal conjecture for zeta zeros
- Kim (2015-2016), arithmetic Chern-Simons theory
- Baake & Grimm, "Aperiodic Order" (Cambridge, 2013)
- Shaughnessy (arXiv 2410.03673), quasicrystal scattering approach
- Remmen (2021), amplitudes and the Riemann zeta function (PRL)
- LeClair & Mussardo (JHEP 2024), Riemann zeros as quantized energies

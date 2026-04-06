# Riemann Hypothesis — Research Investigation

## Status: Exhaustive exploration complete. Geometric core identified.

**Investigation dates:** 2026-04-04 to 2026-04-06
**Agents run:** ~32 across 9 waves
**Start:** Hossenfelder video on Hartnoll-Yang "Conformal Primon Gas at the End of Time"
**End:** Precise 5-problem research agenda for an arithmetic Hodge index theorem on the scaling-site square

## Key Documents

- **`SYNTHESIS.md`** — Complete synthesis of all findings, key theorems, novel discoveries, corrections, closed doors, and the research agenda. **Read this first.**
- **`approaches/all-strategies.md`** — The original 10 cross-disciplinary strategies
- **`experiments/`** — 25 experiment directories, each with `findings.md` + Python scripts

## The One-Paragraph Summary

We exhaustively explored analytic, probabilistic, thermodynamic, information-theoretic, and dynamical approaches to RH. Every one hit the same wall: bridging probabilistic concentration (Euler product, σ > 1/2) to deterministic zero-location (functional equation, across σ = 1/2). The Euler product and functional equation live in complementary half-planes and never overlap. We traced this wall to its geometric core: the proof requires constructing an **arithmetic Hodge index theorem on Spec(Z) × Spec(Z) over F₁** — the analog of what Weil used to prove RH for curves over finite fields. Connes has the closest approach (Weil positivity proved at archimedean place + any finite set of primes). The gap: extending to all places, which requires a global intersection pairing whose positivity survives the infinite limit.

## Approach Status

| Framework | Status | Key finding |
|-----------|--------|-------------|
| PF / Kernel | **CLOSED** | PF_∞ impossible for functions with zeros (Schoenberg) |
| Functional equation | **INSUFFICIENT** | Davenport-Heilbronn counterexample |
| Thermodynamic | **REFORMULATION** | Ensemble equivalence = RH |
| Information-theoretic | **CAN'T SEE ZEROS** | Locality-globality mismatch |
| Probabilistic / martingale | **CIRCULAR** | Cancellation IS RH |
| Almost-periodic | **GROWTH RATES WRONG** | Doubly-exp vs singly-exp |
| Algebraic geometry | **WHERE THE PROOF LIVES** | Arithmetic Hodge index theorem on S^(2) |
| Additive evidence (independent weights) | **CLOSED** | Decoupling lemma — bounded envelope can't dominate logarithmic singularities of -log\|ζ\| |
| Mollifier methods (coupled additive) | **THE FRONTIER** | Guth-Maynard etc. — coupling exploits ζ's analytic structure |

## The 5-Problem Research Agenda

If these are solved, RH follows:

1. **Chow/Picard theory on S^(2)** — category of correspondences on scaling-site square
2. **Excess-intersection formula** — Δ · Ψ^λ with orbital fixed loci
3. **Green kernels** — extract Connes' operators as Green functions on S^(2)
4. **Semilocal compatibility** — finite truncations match Connes' positive forms
5. **Hodge index theorem** — primitive negativity on S^(2)

## Experiment Index

See `SYNTHESIS.md` for the full experiment index with wave numbers and key findings for each of the 25 experiments.

## Key References

- Connes, *Trace formula in NCG and zeros of ζ* (Selecta Math., 1999)
- Connes-Consani, *Weil positivity, archimedean place* (Selecta Math., 2021)
- Connes-Consani-Moscovici, *Zeta zeros and prolate wave operators* (2024)
- Connes-Consani, *Geometry of the scaling site* (Selecta Math., 2017)
- Connes-Consani, *Riemann-Roch for Spec Z* (Bull. Sci. Math., 2023)
- Griffin-Ono-Rolen-Zagier, *Jensen polynomials for ζ* (PNAS, 2019)
- arXiv 2602.20313, *PF₅ failure of de Bruijn-Newman kernel* (Feb 2026)
- Hartnoll-Yang, *Conformal Primon Gas at the End of Time* (arXiv 2502.02661)
- Guth-Maynard, *New large value estimates* (2024)
- Rodgers-Tao, *de Bruijn-Newman constant is non-negative* (2020)

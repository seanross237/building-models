---
topic: T_U/T_dS = μ_MOND novelty survey — six prior papers checked, web search, none publish the ratio
confidence: provisional
date: 2026-03-27
source: "compton-unruh strategy-001 exploration-005"
---

## Finding

After a thorough literature search across six directly relevant papers and an explicit web search, the
specific algebraic identity T_U/T_dS = μ_standard_MOND has **not been explicitly published** as an
identification. The ingredients are all known (Deser-Levin 1997 for T_dS; Milgrom 1983 for μ_standard),
and the connection between de Sitter temperature and MOND scale is known since Milgrom 1999. But the
specific ratio has not appeared in any paper found. **LIKELY NOVEL as an explicit statement.**

## Systematic Prior Work Comparison

| Paper | Formula Used | Why Different from T_U/T_dS |
|-------|-------------|------------------------------|
| Milgrom 1999 | T_dS − T_GH (excess temperature) | Excess, not ratio; different μ; a₀ = 2cH₀ |
| Deser-Levin 1997 | Derived T_dS formula | No MOND connection anywhere in paper |
| Verlinde 2016 | Elastic entropy displacement | Different mechanism; no T_U/T_dS; deep-MOND only |
| Pikhitsa 2010 | Thermodynamics of gravity | Different mechanism; a₀ = 2cH₀; no T_U/T_dS |
| Smolin 2017 | Quantum gravity regime below T_GH | Regime condition, not a ratio; no explicit μ |
| Luo 2026 | Spectral broadening of quantum states | Different mechanism; different interpolation function |

**Web search:** Direct search for "T_U/T_dS" combined with "MOND interpolation function" returned
**zero results**. Strong confirmation that the specific ratio and its identification with the standard
MOND interpolation function has not appeared in any indexed paper.

## Key Distinction: Milgrom 1999 vs. T_U/T_dS Ratio

This is the most important distinction because Milgrom 1999 is the closest prior work.

**Milgrom 1999** (Phys. Lett. A 253, 273–279, arXiv:astro-ph/9805346):
- Uses the temperature EXCESS (difference), not the ratio:

      Modified inertia ∝ T_dS(a) − T_GH = T_GH × [√(1 + (a/cH₀)²) − 1]

- Interpolation function from the excess temperature:
  μ_excess(x) = √(1+x²) − 1  (normalized to linear at large x)
  This is NOT the standard MOND function μ_standard(x) = x/√(1+x²)
- Only analyzed asymptotic limits (a ≫ a₀ and a ≪ a₀); did not write the full interpolating function
- Predicted a₀ = 2cH₀ (factor of 2 discrepancy from a₀ = cH₀ in the ratio approach)
- Explicitly acknowledged: "this would reflect on a 'linear', constant-acceleration motion, while
  circular trajectories will probably behave differently"

**The T_U/T_dS ratio:**
- Gives the EXACT standard MOND interpolation function μ_standard(x) = x/√(1+x²)
- Valid at all acceleration scales, not just asymptotics
- a₀ = cH₀ (different from Milgrom 1999's a₀ = 2cH₀)

## Smolin 2017 — Structural Proximity Without Formula

Smolin 2017 (*Phys. Rev. D* 96, 083523, arXiv:1704.00780) shares the insight that de Sitter temperature
sets the MOND scale: the regime condition T_U < T_GH is equivalent to a < cH₀, which is exactly where
the T_U/T_dS ratio is significantly below 1. However, Smolin does NOT compute T_U/T_dS or identify it
as the MOND interpolation function — he uses a quantum gravity regime framework with no explicit formula.

## Luo 2026 — Completely Different Mechanism

Luo 2026 (arXiv:2602.14515, February 2026) derives
a_eff^r = √[(a_N + a_bg)² − a_bg²] (deep-MOND limit ≈ √(2a_N a_bg)) via *spectral broadening
of quantum states* during non-equilibrium short-time acceleration. Completely different from T_U/T_dS:
no temperature ratio, no thermal equilibrium, uses second-order moment quantum fluctuations, different
interpolation function form.

## Novelty Assessment

**LIKELY NOVEL as an explicit statement.** The identity is:
1. Algebraically trivial (ratio of two known formulas)
2. Potentially significant (identifies EXACT standard MOND interpolation function, not just asymptotics)
3. Historically missed (Milgrom 1999 used excess temperature, not the ratio)
4. Unconfirmed by first-principles physics (m_i ∝ T_U/T_dS has no derivation)

The observation is sharper than Milgrom 1999: he noted that T_dS − T_GH has the right asymptotic
behavior for MOND, whereas T_U/T_dS has EXACTLY the right functional form at all scales for the
standard MOND interpolation function.

**Caveat:** The identity is simple algebra — it might have been noticed informally in unpublished notes.
Given its simplicity, informal observation is plausible. But no systematic identification appears in
any indexed paper.

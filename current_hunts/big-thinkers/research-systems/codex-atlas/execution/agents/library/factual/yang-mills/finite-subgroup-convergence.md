---
topic: Finite subgroup convergence to SU(2) Yang-Mills — numerical evidence
confidence: provisional
date: 2026-03-27
source: "yang-mills strategy-001 exploration-005; code/finite_subgroups.py, code/finite_group_lattice.py; Monte Carlo computation on 4⁴ lattice"
---

## Summary

Monte Carlo simulations of 4D lattice Yang-Mills with three finite subgroups of SU(2) — Binary Tetrahedral (2T, order 24), Binary Octahedral (2O, order 48), Binary Icosahedral (2I, order 120) — show that mass gap observables converge rapidly to SU(2) values as group order increases. This directly probes the finite→continuous transition relevant to extending Adhikari-Cao (2025) from finite groups to SU(2).

**Simulation parameters:** 4⁴ = 256-site lattice; β ∈ {1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0}; 50 thermalization sweeps, 30 measurements with 3-sweep spacing.

## Main Result: Binary Icosahedral Group Tracks SU(2) Across Full β Range

The 2I group (120 elements) achieves:
- **< 0.5% relative deviation from SU(2) for average plaquette ⟨P⟩ across the entire tested β range (1.0–4.0)**
- **< 0.3% deviation for Creutz ratio χ(2,2) at β = 3.5 and 4.0** (absolute differences 0.0003 and 0.0011 respectively)
- String tension σa² ≈ 0.69 at β = 2.0 — consistent with SU(2) and with the other groups

Convergence is monotonic in |G| at 6 out of 7 tested β values (exception: β = 1.5, where all deviations are < 0.5% and within statistical noise).

## Phase Structure: First-Order Bulk Transitions Scaling with |G|

All three finite groups exhibit first-order bulk phase transitions (confirmed by hysteresis analysis: hot vs. cold starts converge to different values at the transition):

| Group | Order | β_c         | Hysteresis gap Δ⟨P⟩ |
|-------|-------|-------------|---------------------|
| 2T    | 24    | 2.1 – 2.3   | ≈ 0.39              |
| 2O    | 48    | 3.1 – 3.4   | ≈ 0.18              |
| 2I    | 120   | 5.5 – 6.0   | ≈ 0.09              |
| SU(2) | ∞    | None        | —                   |

Above β_c the finite group enters a trivial/frozen phase (⟨P⟩ → 1, near-zero string tension, no confinement). SU(2) has no bulk transition.

**Scaling law:** β_c ~ |G|^α with α ≈ 0.6. So β_c → ∞ as |G| → ∞. This means the bulk phase transition is a **lattice artifact of the finite group** that disappears in the continuum limit. Below β_c, each finite group accurately reproduces SU(2) confinement physics; the confining window expands without bound as |G| increases.

The hysteresis gap also shrinks with |G|: 0.39 → 0.18 → 0.09, suggesting the transition weakens (and ultimately disappears) in the SU(2) limit.

## Confinement Consistent Across All Groups Below the Transition

At β = 2.0 (within the confining phase for all groups):
- Area law ratio −ln W(2,2) / −ln W(1,1) ≈ 3.7–3.8 for all groups (pure area law prediction: 4.0; deviation expected from perimeter corrections at small loops)
- Wilson loops W(1,1), W(1,2), W(2,2) agree across all groups to within a few percent
- All Polyakov loop measurements at this lattice size are dominated by finite-volume / Z₂ tunneling effects and are not reliable order parameters

## Implications for Adhikari-Cao Extension (Conjectured)

**[CONJECTURED]** The four-layer structural obstruction in Adhikari-Cao (2025) prevents their specific swapping-map proof technique from extending to SU(2) — see `adhikari-cao-technique-and-obstruction.md`. The numerical evidence here is relevant to "Extension Direction 1" in that file: whether uniform finite-group bounds could support a limit argument.

The computation suggests:

1. **The physical barrier to a finite→continuous limit argument appears technical, not fundamental.** Observable convergence is rapid and monotonic. The physics of confinement (plaquette, Wilson loops, Creutz ratios, string tension) is essentially identical to SU(2) in the confining phase of finite groups.

2. **The β_c → ∞ structure is favorable.** For any fixed physical β, sufficiently large finite groups (|G| beyond a threshold set by β_c ~ |G|^0.6) will have β below their critical coupling and thus in the confining phase. A mass gap result for G_n at β < β_c(G_n) could in principle survive the |G_n| → ∞ limit.

3. **Rate estimates (provisional):** Observable convergence rate is approximately |G|^{-0.7} to |G|^{-2.5} depending on β and observable (faster at high β below β_c). For a rigorous limit argument, one would need:
   - |m(G_n, β) − m(SU(2), β)| ≤ C(β) · |G_n|^{-α} for some α > 0
   - m(G_n, β) ≥ c > 0 uniformly across G_n and β in a compact set

   The numerical data is consistent with α ≈ 1 for plaquette and string tension.

**Caveats:** The computation is on a small 4⁴ lattice; finite-volume effects are present throughout. The convergence rates are extracted from only three group orders and should be treated as rough estimates. All implications for the Adhikari-Cao extension are conjectures; whether the convergence rate is uniform in the mathematical sense needed for a rigorous argument is not established.

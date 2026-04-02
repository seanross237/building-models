# Exploration 004 — Report Summary

## Goal
Use the island formula to compute R_δ(t) = S(R,t)/S_T − 1 through BH evaporation. Identify the classicality transition. Assess whether "Page-time classicality transition" is a new QD result or a restatement.

## What Was Done
Implemented the island formula in Python (linear model + CFT/log model), computed R_δ(t) for BH sizes from 10 bits to 10^77 bits, tabulated classicality transition times, and compared the exterior vs. interior budget structure. Code saved to `code/island_formula.py`, three plots produced.

## Outcome: Success

## Key Numerical Results  [COMPUTED]

**Classicality transition times (linear model, S_T = 1 bit):**
- Formula: t_classical = t_Page × (2/S_BH)
- Solar mass (S_BH=10^77): t_class/t_Page = 2×10^{-77} — exterior becomes classically informative almost immediately
- S_BH=100: t_class/t_Page = 0.02 — at 2% of Page time
- S_BH=10: t_class/t_Page = 0.20 — at 20% of Page time

**R_δ at Page time = S_BH/2 − 1** (enormous for any macroscopic BH — budget never constrains).

**CFT model:** t_Page/t_evap = exp(−3·S_BH/(2c)) ≪ 0.5 for large S_BH (Page time is early in the total evaporation timeline, not at the halfway point).

## Key Structural Finding  [COMPUTED]

There are **two distinct classicality transitions:**

1. **Exterior transition** at t ≈ (2/S_BH)·t_Page: Hawking radiation first accumulates 1 bit → exterior facts become QD-classical. This happens vastly before the Page time for large BHs.

2. **Interior transition** at t = t_Page: The island appears; R_δ_int undergoes a **discontinuous jump** from −1 (no interior access) to S_BH/2 − 1 (full interior reconstructability). This is an abrupt classicality switch for interior facts.

## Verdict on Novelty  [CONJECTURED]

The "Page-time classicality transition for interior operators" is a **restatement in QD language** of the known entanglement wedge / island result. HQEC says the interior IS reconstructable after the Page time; QD says the interior gains positive redundancy (R_δ > 0) after the Page time. Same physics, new vocabulary.

**What QD genuinely adds:** The quantitative R_δ budget; the two-stage structure (exterior early, interior at Page time) as an organizing principle; the explicit measurement-theoretic criterion for "classical observability." These are new ways of packaging known results, not independent physical predictions.

## Verification Scorecard
- **[COMPUTED]:** 7 (all numerical results from running Python code)
- **[CONJECTURED]:** 2 (novelty assessment, "organizing insight" label)
- **[VERIFIED]:** 0

## Key Takeaway
The island formula cleanly produces a two-stage classicality structure. Interior classicality is gated at the Page time (sharp jump in R_δ_int). Exterior classicality is nearly instant. The former is new QD packaging of a known result; the latter is a mildly novel observation about Hawking radiation informativeness that hasn't been emphasized before.

## Proof Gaps
None (no Lean formalization attempted; this is a computation exploration).

## Unexpected Findings
- CFT model has t_Page ≪ t_evap/2 for large S_BH (exponentially early), which means the "Page time is at half-evaporation" intuition is wrong in the CFT model. This has implications for how one should think about the classicality budget timeline.
- The interior R_δ jump is discontinuous — R_δ_int goes from −1 to S_BH/2−1 instantaneously at the Page time. This is a consequence of the island formula selecting a discrete topology (no island → island). This is a quantum phase transition in the replica geometry sense.

## Further Computations Identified
- Apply this framework to the *Karch-Randall* braneworld model where a partially transparent membrane controls when the island appears — the transition would be tunable.
- Compute the "entanglement shadow" region where R_δ_int = 0 even though some partial interior information has leaked; this connects to the Python AGT/AMPS firewalls literature.
- Quantify the QD budget for specific *observables* (e.g., mass, position of infalling matter) rather than bulk entropy, using approximate quantum error correction bounds.

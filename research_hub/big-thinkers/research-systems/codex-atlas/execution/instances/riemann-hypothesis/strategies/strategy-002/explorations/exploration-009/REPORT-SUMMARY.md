# Exploration 009 — Report Summary

## Goal
Test whether C1's anomalous Δ₃_sat=0.285 (intermediate between GUE=0.565 and zeta=0.155) is caused by Von Mangoldt arithmetic structure, by comparing H_flat (flat amplitude + random phases) to C1 and GUE control at N=500.

## What Was Done
- Ran 3 realizations each of H_flat, C1, and GUE control (N=500)
- Used exact analytical staircase integration for Δ₃ (explorer found and fixed a formula bug that underestimated Δ₃ by ~50×)
- Explorer died (usage limit) before writing report; computation was completed manually from explorer's code

## Key Result

| Ensemble | Δ₃_sat | ±std |
|---|---|---|
| H_flat | **0.256** | ±0.010 |
| C1 | **0.243** | ±0.017 |
| GUE control | **0.227** | ±0.010 |
| GUE theory (inf N) | 0.242 | — |
| Zeta zeros | 0.155 | (known) |

**All three ensembles agree within noise.** H_flat ≈ C1 ≈ GUE control.

## Verdict

**C1's intermediate Δ₃ is NOT caused by Von Mangoldt arithmetic.** It is generic GUE-class finite-size behavior at N=500. The earlier value of 0.285 (E005) was within normal sampling variation. The "anomalous intermediate rigidity" claim is DISPROVEN.

The two surviving SUPPORTED novel claims from E008 are unaffected: N²/p scaling law and Dirichlet impossibility proof.

The central unsolved problem: no construction achieves Δ₃_sat < 0.2 (zeta zeros have 0.155). The 40% gap between generic GUE-class N=500 behavior and zeta zeros remains unexplained.

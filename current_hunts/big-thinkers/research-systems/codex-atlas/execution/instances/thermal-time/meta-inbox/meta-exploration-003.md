# Meta-Learning Note — Exploration 003
**Date:** 2026-03-27 | **Written by:** Strategizer (thermal-time, strategy-001)

## What the exploration did
Phase 2 critical comparison: computed C_full_QM (H_AB evolution) vs C_local_TTH (K_A/β evolution) for coupled oscillators. Found 82.7% discrepancy at λ=0.3 due to structural difference (beats vs. single frequency). Confirmed control check C_global = C_full at machine zero.

## What worked well
- **Setting up the control check explicitly** (C_global = C_full): This was crucial. It confirmed that the discrepancy isn't a computation error — it's a genuine local-vs-global modular flow difference.
- **The "single most important number" framing** in the GOAL.md: The explorer delivered exactly that number (0.827) prominently. This metric is exactly what Phase 2 needed.
- **FFT analysis to reveal the structural difference**: The explorer went beyond just reporting the norm and revealed the physical cause (two peaks in C_full vs. one in C_local). This is the kind of interpretation that makes a report useful.
- **Stability check (N=15, N=20, N=25)**: The 1 ppb stability confirms the result is physical, not numerical.

## What didn't work well
- **Sign correction in ω_eff**: Exploration-002's formula predicted ω_eff > ω_A, but exploration-003 found ω_eff < ω_A. This sign error propagated from exploration-002 and needed correction in exploration-003. Better: when exploration-002 found the period shift formula, should have verified the sign immediately.

## Lessons for future goals
1. **Always include a control check that equals something trivially.** Here, C_global = C_full was trivial (K_AB = βH_AB) but invaluable. Design goals to include a "should equal X by construction" check.
2. **"Structural vs. quantitative" framing**: If two predictions differ structurally (different number of frequency peaks), no amount of parameter tuning fixes it. Future goals should ask: "is the discrepancy structural or just a scale factor?" — this separates real predictions from normalization errors.
3. **The literature disambiguation question (local vs. global) should have been in exploration-002 or even exploration-001.** We spent two explorations computing assuming the local interpretation without confirming it was Connes-Rovelli's intent. Future strategy: resolve the interpretation before computing consequences.

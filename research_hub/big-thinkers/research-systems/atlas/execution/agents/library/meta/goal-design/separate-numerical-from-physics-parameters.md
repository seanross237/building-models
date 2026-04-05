---
topic: Separate numerical method parameters from physics parameters in scan goals
category: goal-design
date: 2026-03-27
source: "stochastic-electrodynamics strategy-001 meta-exploration-005"
---

## Lesson

When designing parameter scan explorations, explicitly **separate numerical method parameters** (integration timestep dt, numerical precision, convergence tolerances) **from physics parameters** (cutoff frequencies, coupling constants, system sizes). If the goal doesn't specify which to hold fixed, explorers will make "natural" choices (e.g., dt = π/ω_max for Nyquist sampling) that couple numerical and physical parameters — confounding the analysis and causing instabilities.

## Evidence

- **SED strategy-001 exploration-005** — Goal was to scan ω_max ∈ {10, 20, 30} and τ ∈ {0.01, 0.005, 0.002}. The explorer initially chose dt = π/ω_max (the Nyquist criterion — a natural choice). This caused numerical instabilities for β=1 at large dt: Euler-Cromer requires dt < 2/ω_eff_max ≈ 0.29, and dt=π/10≈0.314 exceeds this. Approximately 5 minutes of debugging resulted. The fix — holding dt=0.05 fixed for all ω_max runs — is correct because ω_max controls the *noise spectrum cutoff*, not the time resolution.

## Template Specification

For parameter scan goals involving numerical simulations:

```
Scan: [list of physics parameters to vary]
Hold FIXED: [list of numerical parameters with exact values]
Hold FIXED: [list of other physics parameters held constant]
Note: [explain why fixed parameters are held fixed if non-obvious]
```

Example for SED: "Scan ω_max ∈ {10, 20, 30}. Hold dt=0.05 fixed for all runs (same as E004). The UV cutoff ω_max controls only the noise power spectral density cutoff, not the time resolution."

## Why This Matters

- Parameters that "naturally" co-vary (like Nyquist dt ~ 1/ω_max) are often *correctly* separated for the physics purpose
- Confounded parameters produce artifacts that look like physical results
- The instability/artifact may only appear at extremes of the scan range, making it appear as anomalous data rather than a setup error

## Related Entries

- `specify-computation-parameters.md` — General lesson about providing exact simulation parameters
- `instruct-incremental-writing.md` — Stability during long simulation runs

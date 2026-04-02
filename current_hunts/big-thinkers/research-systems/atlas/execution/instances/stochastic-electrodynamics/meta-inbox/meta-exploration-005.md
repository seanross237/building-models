# Meta-Learning Note — Exploration 005

## What worked well
- **Reusing E004 code** was efficient. The explorer copied ald_simulate.py and modified it for the parameter scan.
- **Sequential parameter scans** continued to work well. 13 combinations all completed.
- **The key finding was unambiguous.** The ω_max scan showed only 18% reduction when tripling the cutoff — clear evidence the error is real.

## What didn't work well
- **Initial runs with dt=π/ω_max caused instability.** The explorer had to switch to fixed dt=0.05 for all ω_max values. This cost ~5 minutes of debugging. The GOAL should have specified "keep dt=0.05 fixed, only vary ω_max through the noise spectrum cutoff."
- **The τ scan lower bound (0.002) wasn't low enough** to see clear τ scaling. Going to τ=0.001 would have given a better power-law fit.

## Key lesson
**When scanning parameters, fix everything else.** The dt=π/ω_max choice was natural but wrong — it changed the time integration simultaneously with the noise spectrum cutoff, confounding the analysis. Future parameter scan explorations should explicitly state which parameters are fixed and which are varied.

Also: **The most interesting result was unexpected.** We expected the error to go away with higher ω_max (UV artifact). Instead it persisted. This contradicts the conjecture from E004. The lesson: always design parameter scans to distinguish between hypotheses, and be prepared for either outcome.

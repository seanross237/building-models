# First Sprint — What To Run First

## Goal

Kill or justify the Theory 1 track quickly using the smallest honest analysis.

## Exact Order

1. **Run the synthetic self-check**
   - confirm the background-only script can recover a fiducial `LCDM` toy dataset
   - do not touch real data until this works

2. **Load one BAO summary and one SN summary**
   - `DESI DR2 BAO`
   - `Pantheon+`

3. **Fit the baseline ladder**
   - `LCDM`
   - constant-`w`
   - CPL

4. **Fit the first theory-faithful deformation**
   - smooth-step `w(z)` with fixed `Δz`

5. **Swap the SN sample**
   - replace `Pantheon+` with `DES-SN5YR`

6. **Only then add the CMB anchor**
   - `Planck` first
   - `ACT` as the first robustness swap

## Minimal Parameterization

Use these in order:

- `LCDM`: `Ω_m`, `H0`, fixed `w=-1`
- `wCDM`: `Ω_m`, `H0`, `w0`
- `CPL`: `Ω_m`, `H0`, `w0`, `wa`
- `step`: `Ω_m`, `H0`, `A`, `z_t`, with fixed `Δz`

Keep `r_d` fixed in the first pass. If the fit only works by moving `r_d`, that is not evidence for this late-time theory.

## Pass / Fail Criteria

**Keep going if:**

- `wCDM` or CPL improves over `LCDM`
- the step model is at least competitive with CPL
- the low-`z` trend survives both `Pantheon+` and `DES-SN5YR`

**Stop early if:**

- the signal only appears in one SN compilation
- the preferred region shifts wildly under small dataset swaps
- the step model adds freedom but no stable structure

## Immediate Deliverables

- one runnable script
- one dataset manifest template
- one results note for the first real-data pass

## What Not To Do In Sprint 1

- no full Boltzmann-code theory build
- no perturbation/growth modeling before the background signal survives
- no narrative about unfinished spacetime as if it is already established

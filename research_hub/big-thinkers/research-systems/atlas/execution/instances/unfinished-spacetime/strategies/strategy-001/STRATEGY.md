# Strategy 001: Background-First Screening

## Objective

Determine whether the "unfinished spacetime / formation-pressure" idea deserves further theory construction by testing the smallest late-time deformation that could plausibly absorb the live cosmology tensions. This strategy is a screen, not a final theory.

The central deliverable is a robust comparison of:

- flat `LCDM`
- constant-`w` dark energy
- CPL `w(a)=w0+wa(1-a)`
- a smooth low-redshift turn-on model for `w(z)`

against public summary cosmology data.

## Methodology

### Phase 0: Baseline and scaffolding

Before touching the theory-specific model:

1. Build or verify a background-distance pipeline that computes:
   - `E(z)`
   - `D_M(z)`
   - `D_L(z)`
   - `μ(z)`
   - BAO observables such as `D_M/r_d` and `D_H/r_d`
2. Run a synthetic self-check so the code is not first exercised on real data.
3. Confirm the pipeline gives sane behavior for `LCDM`, `wCDM`, and CPL.

**Phase 0 gate:** if the pipeline cannot stably reproduce standard cosmologies, do not proceed.

### Phase 1: Background-only empirical screen

Fit public summary data in ascending complexity:

1. `LCDM`
2. constant-`w`
3. CPL
4. smooth-step `w(z)`

Use:

- `DESI DR2 BAO`
- `Pantheon+`
- `DES-SN5YR`

At this phase, the point is not to prove the theory. It is to see whether the data wants a stable low-redshift deformation at all.

**Default theory-faithful model**

Use:

`w(z) = -1 + A / (1 + exp((z - z_t)/Δz))`

with `Δz` fixed or tightly constrained. Starting with a free nonparametric `w(z)` reconstruction is forbidden in this strategy because it confuses signal with flexibility.

### Phase 2: Robustness anchors

Only if Phase 1 produces a nontrivial preference:

1. Add a `Planck 2018` distance anchor or full-likelihood route.
2. Swap to `ACT DR6`.
3. Swap SN compilations one at a time.
4. Leave out one tracer family or redshift block where practical.

The signal must survive at least one anchor swap and one SN swap to stay alive.

### Phase 3: Growth cross-check

Only if Phase 2 survives:

1. Add DESI full-shape products.
2. Add DES Y3 weak lensing or equivalent public growth probes.
3. Check whether the preferred background region worsens `S8`-sensitive quantities.

If the background win disappears under growth, downgrade the result immediately.

## Cross-Phase Rules

1. **No ontology inflation early.** Do not build a microscopic completion-field model until the background signal survives.
2. **Keep the early universe fixed at first.** If the model needs to move `r_d`, `N_eff`, curvature, or neutrino mass in the first pass, that is a different mission.
3. **Sample dependence is a failure mode, not a detail.** The same low-`z` trend must appear in more than one SN compilation.
4. **Report simple metrics first.** `χ²`, `Δχ²`, AIC/BIC, posterior shifts. Use Bayes factors only when the likelihood setup justifies them.
5. **Do not overfit redshift structure.** If the step model is not preferred over CPL in a stable way, stop there.
6. **Growth is not optional if the background result looks good.** A late-time cosmology claim that ignores growth is incomplete.

## Validation Criteria

**Strategy succeeds if:**

- the pipeline is executable and reproducible on synthetic data
- real-data fits are obtained for `LCDM`, `wCDM`, CPL, and smooth-step `w(z)`
- the preferred deviation, if any, survives at least one independent anchor swap
- pass/fail conditions are documented clearly enough to stop the mission if the signal is fragile

**Strategy is exhausted if:**

- the low-redshift deviation is sample-dependent
- the signal vanishes under `Planck` vs `ACT`
- the improvement never exceeds a trivial nuisance-level shift
- growth cross-checks clearly disfavor the same region

## Success Tiers

- **Tier 2:** reproducible baseline and synthetic self-check
- **Tier 3:** stable background-only deviation worth a note
- **Tier 4:** background + robustness + growth survive, earning a true theory build-out

## Immediate Implementation Target

The first code artifact for this strategy is a background-only analysis skeleton under:

`strategies/strategy-001/explorations/exploration-001/code/background_only_analysis.py`

It should be able to:

- load simple BAO/SN summary files
- evaluate the four model families
- run a coarse grid search
- print comparison metrics
- self-check on synthetic data

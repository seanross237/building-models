# Mission Validation Guide — Unfinished Spacetime

## What Success Looks Like

Either:

- a stable, reproducible low-redshift deviation from `LCDM` that survives independent datasets and justifies a theory-specific build-out, or
- a disciplined null result showing the apparent signal collapses under robustness checks.

Both are valuable. A fragile best fit is not.

## Validation Tiers

### Tier 1: Reproduction

- `LCDM`, `wCDM`, and CPL runs reproduce the broad direction of published late-time fits.
- The fitting code returns sensible baselines on toy and real summary datasets.
- Distance calculations are numerically stable across the redshift range of interest.

### Tier 2: Background-Only Signal

- A late-time deviation improves the fit beyond flat `LCDM`.
- The improvement is not just a single-bin or single-sample effect.
- The preferred redshift structure is qualitatively interpretable, not a fit oscillation.

### Tier 3: Robustness

- The same trend survives `Planck` vs `ACT`.
- The same trend survives multiple SN compilations.
- Reasonable nuisance and calibration changes do not erase the signal.

### Tier 4: Growth Compatibility

- The preferred background model does not obviously fail once growth information is added.
- The same parameter region remains viable under `S8`-related probes.
- If the model modifies perturbations, the perturbation prescription is explicit.

### Tier 5: Theory-Earning Threshold

- The empirical shape preferred by the data can be mapped to a specific completion-pressure model.
- The model offers at least one prediction beyond "some flexible `w(z)` fits a bit better."
- The strongest alternative explanation is explicitly addressed: dataset systematics, sample dependence, or generic dark-energy flexibility.

## Exhaustion Conditions

This strategy is exhausted when any one of these becomes clear:

- the low-redshift signal does not survive independent datasets
- the apparent improvement is calibration-driven
- the model only works by moving early-universe quantities that the theory was not supposed to touch
- the same effect is already captured by generic CPL with no theory-specific gain

At that point, either stop or downgrade the mission to a phenomenology note rather than a breakthrough search.

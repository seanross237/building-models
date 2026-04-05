# Mission: Unfinished Spacetime — Does Late-Time Formation Pressure Beat LCDM?

## Mission Standard

The mission succeeds only if it produces a result we would be willing to defend in public: either a robust late-time deviation from `LCDM` that survives independent datasets, or a clean negative result showing the idea collapses under current data. Interesting language without a stable fit is not success.

## The Core Question

Treat "unfinished spacetime" as a late-time effective dark-sector hypothesis:

- spacetime completion generates an effective negative pressure
- the pressure turns on or changes at low redshift
- the effect should look like evolving `w(z)` before it looks like deep new ontology

The immediate question is not "is the metaphysics right?" It is:

**Can a low-redshift formation-pressure model outperform flat `LCDM` in public cosmology data without falling apart under robustness checks?**

## Why This Mission Exists

This is the only one of the recent speculative directions that directly touches the live anomaly cluster in [KNOWN-ANOMALIES.md](../../validation/KNOWN-ANOMALIES.md):

1. Hubble tension
2. S8 tension
3. cosmological constant problem
4. DESI dark-energy evolution
5. possibly CMB lensing tension if growth is modified later

That does not make the theory true. It makes it worth a disciplined screen.

## The Execution Chain

### Step 1: Reproduce the ordinary late-time baseline

**What to do**
- Fit background-only `LCDM`, constant-`w`, and CPL `w(a)=w0+wa(1-a)` to public late-time summaries.
- Use `DESI DR2 BAO + Pantheon+ + DES-SN5YR` first.
- Keep the theory out of the fit at this stage. This is a calibration run.

**Kill condition**
- If we cannot reproduce the broad published direction of the data with standard parameterizations, stop. The pipeline is not trustworthy.

**Output**
- A baseline table of best-fit parameters and simple comparison metrics for `LCDM`, `wCDM`, and CPL.

### Step 2: Screen the minimal theory-faithful deformation

**What to do**
- Introduce a low-redshift turn-on model for the dark-sector pressure.
- The first theory-faithful screen is a smooth step in `w(z)`:
  `w(z) = -1 + A / (1 + exp((z - z_t)/Δz))`
- Keep `Δz` fixed or tightly prior'd. Do not start with an over-flexible reconstruction.

**Kill condition**
- If the apparent signal reduces to one nuisance direction, one SN compilation, or one redshift bin, stop. That is not a theory win; it is a fit artifact.

**Output**
- Fit comparison of `LCDM`, `wCDM`, CPL, and smooth-step `w(z)`.

### Step 3: Robustness against independent anchors

**What to do**
- Swap `Planck 2018` and `ACT DR6` as the CMB anchor.
- Swap `Pantheon+`, `DES-SN5YR`, and any additional public SN sample one at a time.
- Leave one DESI tracer or redshift block out where practical.

**Kill condition**
- If the low-`z` feature survives only one CMB anchor or one SN calibration choice, stop.

**Output**
- A stability table: which deviations survive which anchor and which do not.

### Step 4: Growth cross-check

**What to do**
- Only if the background result survives, add public growth information:
  - DESI full-shape products
  - DES Y3 weak lensing
  - lensing-related cross-checks where feasible

**Kill condition**
- If the same parameter region that improves distances obviously worsens growth, the mission becomes "background-only curiosity," not a breakthrough track.

**Output**
- Joint background/growth compatibility check.

### Step 5: Decide whether the ontology earned the right to exist

**What to do**
- Only after Steps 1-4 pass do we ask whether "unfinished spacetime" is better than generic evolving dark energy.
- At that point the task becomes deriving the preferred `w(z)` shape from a genuine completion-field model.

**Kill condition**
- If the data only wants generic flexibility and not a stable low-`z` structure, do not escalate into deeper theory-building.

## What Counts as Success

- **Strong success:** the same low-redshift deviation appears in at least two independent distance probes, survives `Planck` vs `ACT`, and still looks viable when growth is added.
- **Moderate success:** a stable empirical signal appears in background data but remains unresolved on the growth side.
- **Useful failure:** the signal depends on one dataset family or one calibration choice, and we can show that cleanly.

## What Counts as a Waste of Time

- Building an elaborate microscopic theory before the late-time screen survives.
- Letting `r_d`, curvature, neutrino mass, and dark-energy freedom all float at once in the first pass.
- Calling a one-dataset preference a breakthrough.

## Available Local Assets

- Validation suite at [execution/validation](../../validation/README.md)
- anomaly map at [KNOWN-ANOMALIES.md](../../validation/KNOWN-ANOMALIES.md)
- public-data guide at [DATA-SOURCES.md](../../validation/DATA-SOURCES.md)

## Immediate Deliverable

The first deliverable is not a paper. It is a defensible first-pass pipeline that can answer:

1. Does background-only public data prefer something beyond `LCDM`?
2. Is the preference stable enough to deserve a theory-specific model?
3. Is the right next move deeper cosmology, or stop?

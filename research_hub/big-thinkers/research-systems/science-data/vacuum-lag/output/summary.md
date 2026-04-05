# Vacuum Lag vs DESI DR2

## Setup

I tested two late-time vacuum-lag backgrounds using the local official DESI DR2 public `base_w_wa` chains already present in the repo and fixed today's cosmology to `H0 = 67.4 km/s/Mpc`, `Omega_m = 0.315`, `Omega_DE = 0.685`.

- Model A: `d rho_vac / dt = -(rho_vac - rho_Lambda,bare) / tau`, with today's `w0` used as the stable second parameter and the implied early-time offset `delta` reported at `z_init = 50`
- Model B: `d rho_vac / dt = -(rho_vac - (rho_Lambda,bare + beta rho_m)) / tau`, with `beta` free and `rho_vac(z_init) = rho_eq(z_init)` enforced

Weighted DESI chain summaries are:

- DESI DR2 + CMB: `w0 = -0.419 +- 0.205`, `wa = -1.746 +- 0.580`
- DESI DR2 + CMB + Pantheon+: `w0 = -0.838 +- 0.055`, `wa = -0.618 +- 0.207`
- DESI DR2 + CMB + DES Y5 SN: `w0 = -0.752 +- 0.057`, `wa = -0.861 +- 0.222`
- DESI DR2 + CMB + Union3: `w0 = -0.666 +- 0.089`, `wa = -1.089 +- 0.294`

## Structural Result

For a first-order relaxation equation, `rho_vac(t)` is an exponential memory average of the target `rho_eq(t)`. If the target is constant (Model A), the sign of `rho_vac - rho_eq` never flips. If the target is monotonic in time (Model B with constant `beta` because `rho_m` is monotonic), the lag keeps the same sign as well.

Numerically, I found no phantom-to-quintessence crossing anywhere in the scanned parameter grids:

- Model A crossings found: `0`
- Model B crossings found: `0`

So this specific ODE family does not realize the advertised `w < -1` at high z and `w > -1` at low z behavior. The sign of `w + 1` stays fixed.

## Best Fits To DESI

I used the weighted DESI `w0-wa` means and covariances as a Gaussian proxy likelihood. `chi2 <= 5.99` corresponds roughly to being inside the 95% ellipse in the `w0-wa` plane.

### DESI DR2 + CMB

- Model A: `tau = 3.78 Gyr = 0.26 / H0`, `delta(z=50) = -0.407`, `w0 = -1.014`, `wa = -0.095`, `chi2 = 8.39`, inside 95% = `False`
- Model B: best fit is the exact `beta = 0` LCDM branch, so `tau` is unconstrained by DESI; representative background point has `w0 = -1.000`, `wa = 0.000`, `chi2 = 9.38`, inside 95% = `False`

### DESI DR2 + CMB + Pantheon+

- Model A: `tau = 4352.19 Gyr = 300.00 / H0`, `delta(z=50) = -1.03`, `w0 = -0.959`, `wa = -0.036`, `chi2 = 8.36`, inside 95% = `False`
- Model B: best fit is the exact `beta = 0` LCDM branch, so `tau` is unconstrained by DESI; representative background point has `w0 = -1.000`, `wa = 0.000`, `chi2 = 9.32`, inside 95% = `False`

### DESI DR2 + CMB + DES Y5 SN

- Model A: `tau = 4352.19 Gyr = 300.00 / H0`, `delta(z=50) = -1.02`, `w0 = -0.923`, `wa = -0.074`, `chi2 = 12.86`, inside 95% = `False`
- Model B: best fit is the exact `beta = 0` LCDM branch, so `tau` is unconstrained by DESI; representative background point has `w0 = -1.000`, `wa = 0.000`, `chi2 = 18.71`, inside 95% = `False`

### DESI DR2 + CMB + Union3

- Model A: `tau = 4352.19 Gyr = 300.00 / H0`, `delta(z=50) = -1.02`, `w0 = -0.941`, `wa = -0.055`, `chi2 = 12.60`, inside 95% = `False`
- Model B: best fit is the exact `beta = 0` LCDM branch, so `tau` is unconstrained by DESI; representative background point has `w0 = -1.000`, `wa = 0.000`, `chi2 = 14.47`, inside 95% = `False`

For the DES Y5 combination, which matches the user-specified `w0 ~ -0.75`, `wa ~ -0.86`, the best fits are:

- Model A: `tau = 4352.19 Gyr`, `u = 300.00`, `delta = -1.02`, `w0 = -0.923`, `wa = -0.074`, `chi2 = 12.86`
- Model B: `beta = 0` collapses exactly to LCDM, so DESI leaves `tau` unconstrained; the background sits at `w0 = -1.000`, `wa = 0.000`, `chi2 = 18.71`

Both models miss the DESI-preferred quadrant for the same reason: they do not generate a sign flip in `w + 1`.

For Model A the fit keeps improving toward the slow-relaxation edge of the scan (`u = 300`), so DESI is effectively pushing this model toward the near-static limit rather than selecting a finite `tau`.

## MOND Link Test

The observed MOND scale implies `tau_MOND = c / a0 = 79.22 Gyr = 5.46 / H0`.

- Model A best-fit DES Y5 prediction within the scanned range: `a0 = 2.184e-12 m/s^2`, factor needed to hit the observed value = `54.938`
- Model B does not give a usable `a0` prediction here, because the DESI fit runs to the exact `beta = 0` LCDM branch where `tau` drops out of the background entirely.

Model A is not close to MOND once the fit is allowed to drift toward the slow-relaxation limit, and Model B does not constrain `tau` at all on its best-fit branch.

## Cross-Checks

- DES Y5 CPL mean crosses `w = -1` at `z ~= 0.40`
- Model A DES Y5 best-fit crossing: `None`
- Model B DES Y5 best-fit crossing: `None`
- If you instead impose the hypothesis `H = 1 / tau` as the crossover condition, MOND's `tau` gives `1/tau = 0.183 H0`, which is below the entire past expansion history since `H(z >= 0) >= H0`. That criterion predicts no positive-redshift crossover at all.
- Relative to LCDM with the same `H0`, Model A gives `H/H_LCDM = 1.016` at `z=0.5` and `1.013` at `z=1.0`
- Relative to LCDM with the same `H0`, Model B gives `H/H_LCDM = 1.000` at `z=0.5` and `1.000` at `z=1.0`
- Lower-than-LCDM `H(z)` at intermediate redshift could in principle help with a higher local `H0`, but these backgrounds are not tuned enough to make a clean claim without refitting the actual distance data.
- The model does not supply a controlled definition of an effective dark-matter fraction. A proxy such as `|rho_vac - rho_eq|` can grow at high z, but that is not the same thing as producing the right clustering source term.

## Verdict

This two-parameter first-order vacuum-lag idea does not pass the DESI shape test.

- The math is well behaved over part of parameter space, but the desired phantom-to-quintessence crossover does not happen in either simple model.
- In `w0-wa` space, the accessible manifolds sit away from the DESI-preferred region; the best points generally remain outside the 95% ellipse for the main combined datasets.
- The `a0 = c / tau` link does not survive the fit: Model A is driven toward `tau >> c / a0`, while Model B leaves `tau` unconstrained on its best-fit `beta = 0` branch.
- Model B is especially fragile conceptually: `rho_eq = rho_Lambda,bare + beta rho_m` is monotonic, so with first-order relaxation it cannot make `w + 1` change sign without extra structure.

The obvious next step, if this direction is to be salvaged at all, is not a different parameter fit. It needs a different dynamical law: a non-monotonic target, a time-dependent coupling, or higher-order vacuum dynamics that can overshoot.

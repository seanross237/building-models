# Cosmic shielding vs. DESI DR2

## Setup

I tested the simplest version of the hypothesis,

\[
\rho_{\rm DE,eff}(z) = \rho_{\Lambda, bare} - \alpha \, \rho_{m,0} (1+z)^3,
\]

against the public DESI DR2 `base_w_wa` Cobaya chains and the public DESI DR2 compressed BAO points.

Weighted summaries from the official DESI public chains are:

- DESI + CMB: `w0 = -0.419 +- 0.205`, `wa = -1.746 +- 0.580`
- DESI + CMB + Pantheon+: `w0 = -0.838 +- 0.055`, `wa = -0.618 +- 0.207`
- DESI + CMB + DES Y5 SN: `w0 = -0.752 +- 0.057`, `wa = -0.861 +- 0.222`
- DESI + CMB + Union3: `w0 = -0.666 +- 0.089`, `wa = -1.089 +- 0.294`

## Exact prediction of the one-parameter model

Define

\[
q \equiv \alpha \frac{\Omega_{m,0}}{\Omega_{\rm DE,0}}.
\]

Then

\[
w_{\rm eff}(z) = -1 - \frac{q(1+z)^3}{1 + q - q(1+z)^3}.
\]

Expanding around today and matching to CPL,

\[
w_0 = -1 - q,
\qquad
w_a = -3 q (1+q) = -3 w_0 (1+w_0).
\]

So the model does **not** fill the `w0-wa` plane. It is a single fixed curve:

- if `w0 > -1`, it predicts `wa > 0`
- if `w0 < -1`, it predicts `wa < 0`

DESI DR2 prefers `w0 > -1` and `wa < 0` in every main combined fit above, so the sign pattern is already wrong.

## Posterior test

I built smoothed posterior-density maps from the public chains and evaluated the maximum posterior density reachable anywhere along the shielding curve.

- DESI + CMB: best curve point `alpha = 0.050`, `w0 = -1.027`, `wa = -0.083`, inside 95% HPD = `False`
- DESI + CMB + Pantheon+: best curve point `alpha = -0.013`, `w0 = -0.994`, `wa = 0.018`, inside 95% HPD = `False`
- DESI + CMB + DES Y5 SN: best curve point `alpha = -1.707`, `w0 = -0.200`, `wa = 0.480`, inside 95% HPD = `False`
- DESI + CMB + Union3: best curve point `alpha = 0.042`, `w0 = -1.020`, `wa = -0.062`, inside 95% HPD = `False`

For the Pantheon+ combination, the DESI mean values imply `alpha = -0.358` if you force the model to reproduce `w0` alone. But that same alpha predicts `wa = 0.407`, which has the wrong sign relative to the actual posterior mean `wa = -0.618`.

## Why the model is structurally too simple

Putting the ansatz into Friedmann gives

\[
\frac{H^2(z)}{H_0^2} =
\Omega_r (1+z)^4 + (1-\alpha) \Omega_m (1+z)^3 + \Omega_{\Lambda, bare}.
\]

So at the background level, the model is exactly equivalent to `LambdaCDM` with a rescaled matter term. It is not a genuinely new late-time evolution law.

That means any alpha large enough to create an apparent shift away from `w = -1` also forces a large shift in the matter contribution:

- Pantheon+ mean `w0` alone requires `alpha = -0.358`, which implies `Omega_m,eff = 0.423` instead of the chain mean `Omega_m = 0.311`
- DES Y5 mean `w0` alone requires `alpha = -0.529`, giving `Omega_m,eff = 0.488`
- Union3 mean `w0` alone requires `alpha = -0.686`, giving `Omega_m,eff = 0.552`

These are huge shifts, not subtle perturbations.

## BAO multi-redshift check

Using the public DESI DR2 compressed BAO points and fixing the non-alpha background parameters to the Pantheon+ chain weighted means, the one-parameter BAO scan gives:

- best BAO anchor-test fit at `alpha = -0.025`
- `chi2(alpha=0) = 22.67`
- `chi2_min = 17.38`
- approximate 95% interval in this anchored one-parameter test: `[-0.047, -0.005]`
- `chi2(alpha from Pantheon+ mean w0) = 671.95`
- `chi2(alpha from DES Y5 mean w0) = 1329.21`
- `chi2(alpha from Union3 mean w0) = 2041.43`

So the alpha values needed to mimic the DESI `w0 > -1` trend by themselves are catastrophic for the actual BAO distances.

## High-z prediction

If you nonetheless force the model to match the Pantheon+ mean `w0`, the shielding prediction bends toward matter-like behavior:

- `alpha = -0.358`
- `w_shield(z=2) = -0.161`
- `w_CPL(z=2) = -1.250`
- `w_shield(z=4) = -0.040`

That is the opposite of DESI's preferred CPL trend, which becomes more negative at higher redshift.

## Verdict

The constant-alpha linear shielding model is **garbage as an explanation of the DESI DR2 signal**.

- It predicts the wrong `w0-wa` sign correlation.
- In background evolution, it collapses to `LambdaCDM` with a rescaled matter term.
- The alpha needed to move `w0` appreciably away from `-1` implies a very large effective matter shift and fails the BAO check.
- The high-redshift prediction goes toward `w(z) -> 0` for the `w0 > -1` branch, not toward the DESI-preferred behavior.

What this means physically: if there is a viable "matter shielding" idea here, it cannot be this linear `rho_Lambda - alpha rho_m` model with constant alpha. You would need at least one extra ingredient that changes sign or geometry with time, such as a non-linear dependence on density, an explicit structure-formation variable, or a redshift-dependent coupling.

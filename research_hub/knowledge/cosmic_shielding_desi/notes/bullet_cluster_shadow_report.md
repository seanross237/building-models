# Bullet Cluster Shadow Test

## Goal

Write down the simplest explicit shielding law that matches the "gravity as expansion shadow"
intuition, then see whether that law can put the Bullet Cluster lensing peaks on the galaxies
instead of on the hot gas.

## Observational inputs

- Clowe et al. 2007 summarize the Bullet Cluster lensing result as lensing aligned with the
  galaxies, which are roughly `10%` of the observed baryons, rather than the X-ray plasma, which
  is roughly `90%`: <https://arxiv.org/abs/astro-ph/0611496>
- Clowe et al. 2006 report an `8 sigma` offset between the total-mass and baryonic-gas centroids:
  <https://arxiv.org/abs/astro-ph/0608407>
- The same 2006 paper states that, in the subcluster, the total visible mass at the plasma peak is
  greater by a factor of about `2` than at the BCG, yet the lensing peak sits near the BCG:
  <https://www.physics.rutgers.edu/~saurabh/690/Clowe-etal-2006.pdf>

These two facts are the core constraint:

1. **Global**: stars must out-weight gas enough to overcome a `90/10` gas/star split.
2. **Local**: at the relevant subcluster peak, the theory must invert a `2:1` baryonic ordering so
   that the BCG beats the plasma peak.

## Candidate shielding law

Use a projected shielding source instead of bare baryonic column density:

```text
rho_bar_lambda(x) = integral G_lambda(x-x') rho_b(x') d^3x'
rho_sh(x) = rho_b(x) * (rho_bar_lambda(x) / rho0)^beta * eta_phase
Sigma_sh(x_perp) = integral rho_sh(x_perp, z) dz
```

Interpretation:

- `G_lambda` is a smoothing kernel that sets the geometric shielding scale.
- `beta >= 0` measures how strongly denser regions shield more effectively per unit baryonic mass.
- `eta_phase` is an optional phase factor that can distinguish stars from hot gas.

This is the smallest family I know how to write that still encodes your premise:
mass blocks expansion, denser matter may block it more, and the result can be geometry-dependent.

## Family 1: coarse-grained monotone shielding

Set `eta_phase = 1`, so the only enhancement comes from cluster-scale density:

```text
rho_sh = rho_b * (rho_bar_lambda / rho0)^beta
```

Inside one smoothing kernel of volume `V_lambda`, the effective source scales like

```text
S_lambda ~ M_lambda * (M_lambda / V_lambda)^beta
         ~ M_lambda^(1+beta) / V_lambda^beta
```

So if the plasma peak already contains more baryonic mass than the BCG on the same smoothing scale,
then any monotone `beta >= 0` makes the plasma peak at least as strong and usually stronger.

With the Bullet local ratio `M_plasma / M_BCG ~= 2.0`:

- `beta = 0` gives `S_plasma / S_BCG = 2.0`
- `beta = 1` gives `S_plasma / S_BCG = 4.0`
- `beta = 2` gives `S_plasma / S_BCG = 8.0`

That means **no coarse-grained monotone shielding law can move the peak from the plasma to the
BCG** once the plasma already wins on the relevant baryonic smoothing scale.

## Family 2: microscopic phase weighting

To rescue the Bullet Cluster, you have to let stars count more than hot gas per unit baryonic mass:

```text
rho_sh = eta_phase * rho_b
eta = eta_star / eta_gas
```

Bullet then requires at least:

- `eta > 9.0` from the global `90/10` gas/star split
- `eta > 2.0` from the local `2:1` plasma excess

The global requirement is the real killer. If `eta ~= 9`, then a galaxy that is `90%` gas and `10%`
stars stops behaving like a gas-dominated system at all. Its effective stellar fraction becomes
`50%`.

This matters because gas-rich galaxies are one of the standard clean MOND-style tests:
<https://arxiv.org/abs/1102.3913>

So a universal phase-weighted rule that rescues Bullet pushes directly against the gas-rich-galaxy
motivation behind the whole MOND-like phenomenology.

## If the phase weighting comes from microscopic density

Suppose the phase factor itself comes from a weak density law:

```text
eta = (rho_star / rho_gas)^beta
```

For plausible microscopic density contrasts:

- `rho_star / rho_gas ~ 1e20` needs only `beta = 0.048` to reach `eta = 9`
- `rho_star / rho_gas ~ 1e24` needs only `beta = 0.040` to reach `eta = 9`
- `rho_star / rho_gas ~ 1e30` needs only `beta = 0.032` to reach `eta = 9`

So the microscopic-density escape hatch is too efficient. Even an extremely weak density dependence
already makes stars dominate over gas by the amount Bullet needs.

## What this means

The Bullet Cluster does not yet prove that every imaginable "expansion shadow" model is impossible.
But it **does** kill the two obvious minimal families:

1. **Cluster-scale monotone shielding** fails immediately because the plasma peak already beats the
   BCG in visible baryons locally.
2. **Microscopic phase-weighted shielding** can rescue Bullet only by making stars dominate over
   gas so strongly that gas-rich galaxy phenomenology becomes hard to preserve.

## Bottom line

My best current read is:

- The simplest explicit shielding law is now written down.
- The natural coarse-grained version is ruled out by Bullet.
- The natural microscopic rescue becomes pathological almost immediately.

That leaves the theory in a bad place. To keep going, you would need a **third ingredient** beyond
"denser matter shields more":

- a non-universal shock/temperature dependence,
- a history-dependent merger effect,
- or a second field that changes how shielding gravitates.

At that point, the theory is no longer a simple expansion-shadow mechanism. It becomes a tuned
cluster-specific model.

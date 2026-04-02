# Exploration 003 Report

## Decision target

For the exact-NS pair `(E_flux, P_flux^-)`, does the exact filtered local energy balance yield a precursor lower bound / no-hidden-transfer statement, or does it leave the earlier slab `R_-` unconstrained so that the pair cannot support a real firewall theorem by exact-identity methods alone?

## 1. Executive verdict

[CHECKED] The exact-identity route fails for the preferred pair.

[CHECKED] The filtered local energy balance is too time-local to force a nontrivial lower bound on the earlier precursor slab `R_-` from the later event `E_flux`.

[VERIFIED] The exact balance controls the later witness gain by same-window transfer, transport, and viscous terms. The earlier slab `R_-` does not appear in any exact control term.

[CHECKED] Therefore no no-hidden-transfer statement of the form

```text
P_flux^-(R_-) <= epsilon  =>  E_flux is impossible
```

can be obtained from the exact filtered-energy identities alone for this pair.

[CHECKED] This is a structural negative on the pair, not yet an explicit exact-NS counterexample. The obstruction is the absence of any backward-memory term or monotonicity principle linking the earlier cumulative flux slab to the later burst window.

## 2. Exact balance setup

[VERIFIED] For exact NS observed through a smooth coarse-graining filter at scale `s`, the standard filtered local kinetic-energy balance has the form

```text
partial_t (1/2 |u_bar_s|^2) + div J_s
  = - Pi_s - nu |grad u_bar_s|^2
```

with

```text
Pi_s = - grad u_bar_s : tau_s(u,u),
tau_s(u,u) = overline(u tensor u)_s - u_bar_s tensor u_bar_s.
```

[CHECKED] The witness channel fixed in exploration 001 was

```text
W(t)
  = (1/2) integral_{B_r(x_*)} (|u_bar_{ell/rho}|^2 - |u_bar_ell|^2)(x,t) dx.
```

[CHECKED] Subtracting the filtered balances at scales `ell/rho` and `ell`, then integrating over the later event window `[t_* - delta, t_*]`, yields schematically

```text
W(t_*) - W(t_* - delta)
  = integral_{later} (Pi_ell - Pi_{ell/rho})
    + boundary transport terms
    + viscous band terms.
```

[CHECKED] The key point is structural: the witness gain is controlled by quantities on the later event window itself. No exact term in this identity contains the earlier predecessor slab `R_-`.

## 3. Theorem target audit

[CHECKED] The natural theorem target was:

```text
small P_flux^-(R_-) rules out later E_flux.
```

[CHECKED] But the precursor

```text
P_flux^-(R_-)
  = integral_{t_* - Delta}^{t_* - delta} integral_{B_r(x_*)} (Pi_ell)_+ dx dt
```

only measures cumulative positive forward transfer on the earlier disjoint slab `R_-`.

[CHECKED] The exact later-window balance does not constrain that earlier integral. At the level of identities:

- later witness gain depends on later band-flux difference `Pi_ell - Pi_{ell/rho}`,
- boundary transport can move energy across `B_r` during the later window,
- viscous terms also live on the later window,
- none of these impose a sign or lower bound on earlier cumulative `Pi_ell^+`.

[CHECKED] So the pair has no exact-identity memory link. The earlier precursor and the later event are tied by mechanism family, but not by a usable exact backward constraint.

## 4. Structural obstruction

[CHECKED] The obstruction is **dynamical time-locality**, not mere proof failure.

[CHECKED] More precisely:

1. The balance law is local in time. It controls changes over the chosen integration window, not over a disjoint earlier slab.
2. The event `E_flux` is triggered by a short later burst plus witness gain. The exact identity allows that burst to be concentrated inside the final window.
3. Because `P_flux^-` is defined on the earlier slab only, small earlier cumulative flux does not contradict a later same-scale burst.
4. The boundary transport terms further weaken any attempt to infer earlier interior buildup from later interior witness gain.

[CHECKED] This means the pair fails as a firewall candidate by exact-identity methods alone. The remaining near-tautology issue from exploration 002 has become a sharp structural failure:

- the precursor is close enough to the event to feel natural,
- but not close enough to inherit any exact memory constraint from the later witness balance.

[CHECKED] What extra input would be required to rescue a firewall theorem:

- a temporal modulus of continuity or one-sided persistence bound for `Pi_ell`,
- a monotonicity principle for a cumulative transfer quantity,
- a transport-control estimate tying boundary flux to earlier interior buildup,
- or a different precursor family with genuine built-in memory rather than a disjoint earlier slice of the same transfer mechanism.

## 5. Implications for the strategy

[CHECKED] This is the strongest structural negative obtained so far:

- exploration 001 found a faithful exact event,
- exploration 002 found the least-tautological precursor pair,
- exploration 003 shows that even this strongest pair does not support a no-hidden-transfer theorem by the exact filtered-energy route.

[CHECKED] The right strategic implication is that the preferred pair does **not** furnish a usable hidden-precursor firewall object.

[CHECKED] One short adversarial synthesis pass remains worthwhile before finalizing, to confirm that the Duchon-Robert backup does not change the conclusion and that this negative is not just an artifact of choosing `P_flux^-` rather than another nearby flux-like quantity.

[CHECKED] But the center of gravity has shifted strongly toward a terminal negative verdict rather than toward a positive firewall.

# Exploration 001 Report: Phase 0 Definition Gate for a Physical-Space Delayed-Transfer Event

## 1. Executive verdict

Decision target:

```text
Either there exists one preferred physical-space delayed-transfer event, on exact NS or one
faithful reduced model with an explicit exact-NS derivation, that has a named output channel,
spacetime localization, baseline regime, threshold-crossing condition, and measurable
hidden-until-threshold clause, or all honest formulations collapse into non-canonical
packet/circuit constructions or closed-route quantities and the strategy should stop.
```

[CHECKED] The gate passes.

[VERIFIED] Tao's delayed-abrupt-transfer mechanism is best read physically as a delayed forward handoff into smaller scales, not as a pressure criterion and not as a standalone trigger observable. The local library fixes that mechanism sharply in shell/helical language.

[CHECKED] A faithful physical-space event can be defined directly on exact Navier-Stokes by coarse-graining the exact solution at one scale interface and measuring a short-window burst of **localized forward interscale energy flux** into a narrow subscale channel.

[CHECKED] The preferred event is:

```text
Localized delayed-transfer event E_flux:
on a parabolic cylinder Q = B_r(x_*) x [t_* - Delta, t_*],
the exact-NS coarse-grained forward flux Pi_ell becomes large only in the final
short window [t_* - delta, t_*], while the local subscale witness channel rises
abruptly there and stays small earlier.
```

[CHECKED] The faithful test object is exact NS itself. No reduced dynamical model is needed. Filtering is only an observability convention applied to the exact solution.

[CHECKED] A defensible backup event exists, but only as a backup: a localized Duchon-Robert inertial-dissipation burst `D_ell(u)` on the same parabolic cylinder. It is more singularity-oriented and less directly a "next-carrier" witness than the preferred flux event.

[CHECKED] The event-definition gate therefore passes, but only narrowly. The next gate must decide one precursor observable for this exact event and prove it is not just the event restated earlier in time.

## 2. Tao delayed-transfer map to candidate physical-space event

[VERIFIED] The Tao reconstruction fixed in the local library has five causal roles:

- current carrier `a1`,
- slow clock `a2`,
- tiny trigger `a3`,
- conduit `a4`,
- next carrier `a5`.

[VERIFIED] The load-bearing feature is delayed transfer, not mere growth: the trigger stays dynamically quiet until a narrow threshold window, then the conduit switches on and the next carrier receives the handoff.

[CHECKED] In physical space, the closest exact-NS analogue is not a five-role packet object. It is an interscale transfer event:

- the "next carrier" becomes a narrow subscale energy channel below a chosen coarse-graining scale `ell`,
- the causal handoff becomes positive forward subgrid-scale flux across `ell`,
- delayed activation becomes a short-window surge in that flux after an earlier quiet interval.

[VERIFIED] Standard filtered NS balance provides the exact physical-space transfer rate. For a smooth filter `G_ell`,

```text
u_bar_ell = G_ell * u,
tau_ell(u,u) = overline(u tensor u)_ell - u_bar_ell tensor u_bar_ell,
Pi_ell = - grad u_bar_ell : tau_ell(u,u).
```

[CHECKED] `Pi_ell(x,t) > 0` is the exact local forward transfer rate from resolved scales `> ell` into unresolved scales `< ell`. This is the right physical-space replacement for Tao's handoff arrow. It is exact NS post-processing, not a reduced interaction graph.

[CHECKED] To keep a named output channel rather than only a rate, define the local subscale witness on a ball `B_r(x_*)` by

```text
W_{ell,rho,r}(t)
  = (1/2) integral_{B_r(x_*)} (|u_bar_{ell/rho}|^2 - |u_bar_ell|^2)(x,t) dx,
```

with fixed scale ratio `rho > 1`. This is a physical-space band-energy proxy for the newly populated smaller-scale channel.

[CHECKED] Then the Tao map is:

- delayed trigger logic -> earlier small `Pi_ell^+`,
- conduit switch-on -> short-window burst of `Pi_ell^+`,
- next-carrier activation -> abrupt rise of `W_{ell,rho,r}`.

## 3. Preferred event definition

[CHECKED] Preferred event: **Localized delayed forward-flux burst with subscale witness gain**.

Fix once and for all:

- an exact NS solution `u`,
- a smooth coarse-graining kernel `G`,
- scale `ell`,
- scale ratio `rho > 1`,
- center-time point `(x_*, t_*)`,
- radius `r`,
- long pre-window `Delta`,
- short activation window `delta` with `0 < delta << Delta`,
- thresholds `eta_flux`, `eta_w`, `A_flux`, `A_w`.

Define:

```text
F_ell(t) = integral_{B_r(x_*)} (Pi_ell(x,t))_+ dx,
W(t) = W_{ell,rho,r}(t).
```

The event `E_flux(x_*, t_*; ell, rho, r, Delta, delta)` occurs when:

1. [CHECKED] Earlier hidden regime:

```text
sup_{t in [t_* - Delta, t_* - delta]} F_ell(t) <= eta_flux,
sup_{t in [t_* - Delta, t_* - delta]} W(t) <= eta_w.
```

2. [CHECKED] Threshold-window transfer burst:

```text
integral_{t_* - delta}^{t_*} F_ell(t) dt >= A_flux.
```

3. [CHECKED] Output-channel activation:

```text
W(t_*) - W(t_* - delta) >= A_w.
```

4. [CHECKED] Hidden-until-threshold is measurable by the contrast between item 1 and items 2-3. Nothing earlier in the same declared region exceeds the pre-threshold budgets.

[CHECKED] This is one event, not a catalog:

- setting: exact NS,
- output channel: local band-energy witness `W`,
- localization: declared parabolic cylinder,
- baseline regime: small earlier positive forward flux and small band-energy content,
- threshold crossing: large final-window forward flux plus abrupt witness gain,
- hidden clause: same quantities remain below declared pre-threshold bounds earlier.

[CHECKED] Why this is the preferred event:

- it lives directly in physical space,
- it is exact-NS faithful,
- it names both a transfer rate and an output channel,
- it does not require any packet support or circuit bookkeeping,
- it is closer to Tao's delayed handoff than Lamb-vector geometry or generic enstrophy production.

## 4. Backup event or rejection of alternatives

[CHECKED] Backup event: **Localized Duchon-Robert inertial-dissipation burst**.

[VERIFIED] Duchon-Robert defines a local inertial energy-defect density `D_ell(u)` through exact spatial increments and local coarse-graining. It measures short-scale energy transfer/dissipation in physical space and has already been used as a singularity-detection diagnostic in later physical literature.

[CHECKED] Backup event `E_DR`:

- same spacetime cylinder `Q`,
- earlier small positive part of `D_ell(u)`,
- final short-window burst of positive `D_ell(u)`.

[CHECKED] Why this is only backup:

- it is more dissipation-facing than handoff-facing,
- it does not provide as clean a "next carrier" witness channel as `W`,
- it is less obviously a delayed-transfer event and more obviously a singularity detector.

[CHECKED] Rejected alternatives:

- **Exact shell/helical event**: rejected as preferred object because it is not physical space and collapses back into the already-killed packet/circuit branch.
- **Lamb-vector / Beltrami-deficit event**: rejected as preferred object because the local library already records its measure-zero fragility under tiny perturbations. It may still matter later as a precursor candidate or adversarial comparator, but not as the main delayed-transfer event.
- **Enstrophy-production / vortex-stretching event**: rejected for Phase 0 because it names generic amplification, not a delayed handoff into a specific smaller-scale witness channel.
- **Pressure-Hessian / De Giorgi / epsilon-regularity event**: rejected because those routes are already closed or tool-independent and would be a disguised reopening.

## 5. Faithful test object and fidelity ledger

[CHECKED] Preferred test object: **exact Navier-Stokes solution, observed through exact coarse-graining**.

[CHECKED] Preserved exact-NS structure:

- incompressibility,
- exact nonlinear transport and pressure coupling,
- exact viscosity,
- exact physical-space locality of the chosen observation region,
- exact filtered energy balance identity generating `Pi_ell`,
- exact local increment structure generating the Duchon-Robert backup.

[CHECKED] Discarded structure:

- none at the dynamical level.

[CHECKED] User-chosen observability conventions:

- filter kernel `G`,
- interface scale `ell`,
- scale ratio `rho`,
- region radius `r`,
- time windows `Delta, delta`,
- threshold budgets `eta_flux, eta_w, A_flux, A_w`.

[CHECKED] These are measurement conventions, not model changes. They do not trivialize the hidden-precursor question, because the question is precisely whether exact NS can keep a physically declared transfer observable quiet until a short activation window.

[CHECKED] Reduced-model fallback:

- not needed for Phase 0,
- and undesirable here because the whole point is to avoid drifting back into an engineered mechanism model.

## 6. Gate analysis and pass/fail verdict

[CHECKED] Positive-firewall target for this event:

```text
If E_flux occurs at (x_*, t_*) with parameters (ell, rho, r, Delta, delta),
then some earlier physical-space observable P on a declared predecessor region
must exceed a quantitative lower bound.
```

[CHECKED] Counterexample target:

```text
Construct or justify an exact-NS or faithful reduced-model scenario in which E_flux
occurs while the chosen precursor observable stays uniformly small on the declared
earlier region.
```

[CHECKED] Definition-level failure would have meant:

- no physical-space event except packet/circuit language,
- no named output channel,
- or no measurable hidden-until-threshold clause.

[CHECKED] That failure did not occur.

[CHECKED] Model-level negative would have meant:

- only a reduced model survives,
- or the event depends on discarding exact-NS structure in a way that trivializes the question.

[CHECKED] That also did not occur at Phase 0, because the preferred event lives on exact NS itself.

[CHECKED] Main residual risk:

- the preferred event may still be attacked later as "generic cascade activity" rather than Tao-specific delayed transfer.

[CHECKED] That is not a Phase 0 death blow. The event is narrow enough to test, and the Tao-specificity attack belongs to the adversarial screen after a precursor pair is chosen.

## Pass/Fail Verdict

```text
pass
```

[CHECKED] Exploration 001 succeeds. The strategy should proceed to the precursor-and-fidelity gate for the preferred exact-NS event `E_flux`, with the Duchon-Robert burst retained only as backup.

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

[CHECKED] A faithful physical-space event can be defined directly on exact Navier-Stokes by coarse-graining the exact solution on a fixed adjacent-scale ladder and measuring a short-window burst of **localized nonlinear transfer into one adjacent band** together with abrupt growth of that same band's energy.

[CHECKED] The preferred event is:

```text
Localized delayed-transfer event E_flux:
on a parabolic cylinder Q = B_r(x_*) x [t_* - Delta, t_*],
the exact-NS adjacent-band transfer F_n^phi becomes large only in the final
short window [t_* - delta, t_*], while the exact localized band-energy channel
K_n^phi rises abruptly there and stays small earlier.
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

[CHECKED] In physical space, the closest exact-NS analogue is not a five-role packet object. It is an **adjacent-band handoff** event on a fixed coarse-graining ladder:

- the "next carrier" becomes one localized band-pass kinetic-energy channel,
- the causal handoff becomes exact nonlinear transfer into that band,
- delayed activation becomes a short-window surge of that band-transfer after an earlier quiet interval.

[VERIFIED] Primary-source anchor: Eyink-Aluie (Physics of Fluids 21, 115107, 2009, DOI `10.1063/1.3266883`) derive exact pointwise band-pass kinetic-energy densities and their local space-scale budget for smooth coarse-graining. Fix a smooth kernel `G`, a ratio `rho > 1`, and scales `ell_n = rho^{-n} L`. Then

```text
u_n = G_{ell_n} * u,
tau_n(u,u) = overline(u tensor u)_{ell_n} - u_n tensor u_n,
Pi_n = - grad u_n : tau_n(u,u),
k_n = (1/2) tau_{n-1}(u_n,u_n).
```

[CHECKED] Here `Pi_n` is the exact low-pass forward transfer across `ell_n`, while `k_n` is the exact band-pass kinetic-energy density for the adjacent band between `ell_{n-1}` and `ell_n`.

[CHECKED] Localized output channel and transfer channel:

```text
K_n^phi(t) = integral phi(x) k_n(x,t) dx,
F_n^phi(t) = integral phi(x) (Pi_{n-1}(x,t) - Pi_n(x,t))_+ dx,
```

with `phi = phi_{x_*,r}` a smooth cutoff for `B_r(x_*)`.

[CHECKED] Then the Tao map is:

- delayed trigger logic -> earlier small `F_n^phi`,
- conduit switch-on -> short-window burst of `F_n^phi`,
- next-carrier activation -> abrupt rise of `K_n^phi`.

## 3. Preferred event definition

[CHECKED] Preferred event: **Localized delayed adjacent-band handoff**.

Fix once and for all:

- an exact NS solution `u`,
- a smooth coarse-graining kernel `G`,
- a fixed scale ratio `rho > 1`,
- a scale index `n` on the ladder `ell_n = rho^{-n} L`,
- center-time point `(x_*, t_*)`,
- radius `r`,
- long pre-window `Delta`,
- short activation window `delta` with `0 < delta << Delta`,
- thresholds `eta_F`, `eta_K`, `A_F`, `A_K`.

Define:

```text
F(t) = F_n^phi(t),
K(t) = K_n^phi(t).
```

The event `E_flux(x_*, t_*; n, rho, r, Delta, delta)` occurs when:

1. [CHECKED] Earlier hidden regime:

```text
sup_{t in [t_* - Delta, t_* - delta]} F(t) <= eta_F,
sup_{t in [t_* - Delta, t_* - delta]} K(t) <= eta_K.
```

2. [CHECKED] Threshold-window transfer burst:

```text
integral_{t_* - delta}^{t_*} F(t) dt >= A_F.
```

3. [CHECKED] Output-channel activation:

```text
K(t_*) - K(t_* - delta) >= A_K.
```

4. [CHECKED] Hidden-until-threshold is measurable by the contrast between item 1 and items 2-3. Nothing earlier in the same declared region exceeds the pre-threshold budgets.

[VERIFIED] Notation table:

| Item | Choice |
|---|---|
| setting | exact NS smooth solution |
| output / witness channel | localized adjacent-band energy `K_n^phi` |
| spacetime localization | `phi_{x_*,r}` on `B_r(x_*)`, time window `[t_* - Delta, t_*]` |
| baseline regime before threshold | small earlier `F` and small earlier `K` |
| threshold-crossing condition | final-window `∫ F >= A_F` and `K(t_*) - K(t_* - delta) >= A_K` |
| measurable `hidden until threshold` | the same predeclared `F` and `K` stay below `eta_F, eta_K` on the whole earlier interval |

[CHECKED] This is one event, not a catalog:

- setting: exact NS,
- output channel: exact localized adjacent-band energy `K`,
- localization: declared parabolic cylinder,
- baseline regime: small earlier net transfer into the band and small band-energy content,
- threshold crossing: large final-window band transfer plus abrupt band-energy gain,
- hidden clause: same quantities remain below declared pre-threshold bounds earlier.

[CHECKED] Why this is the preferred event:

- it lives directly in physical space,
- it is exact-NS faithful,
- it names both a transfer rate and an output channel,
- it does not require any packet support or circuit bookkeeping,
- it is closer to Tao's delayed handoff than Lamb-vector geometry or generic enstrophy production.

## 4. Backup event or rejection of alternatives

[CHECKED] Backup event: **Localized Duchon-Robert inertial-dissipation burst**.

[VERIFIED] Duchon-Robert (Nonlinearity 13, 249-255, 2000) defines a local inertial energy-defect density `D_ell(u)` through exact spatial increments and local coarse-graining. It measures short-scale energy transfer/dissipation in physical space and has already been used as a singularity-detection diagnostic in later physical literature.

[CHECKED] Backup event `E_DR`:

- same spacetime cylinder `Q`,
- earlier small positive part of `D_ell(u)`,
- final short-window burst of positive `D_ell(u)`.

[CHECKED] Why this is only backup:

- it is more dissipation-facing than handoff-facing,
- it does not provide as clean a "next carrier" witness channel as `K_n^phi`,
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
- exact adjacent-band energy balance identities generating `Pi_n`, `k_n`, `F_n^phi`, and `K_n^phi`,
- exact local increment structure generating the Duchon-Robert backup.

[CHECKED] Discarded structure:

- none at the dynamical level.

[CHECKED] User-chosen observability conventions:

- filter kernel `G`,
- band index `n` on the ladder `ell_n = rho^{-n} L`,
- scale ratio `rho`,
- region radius `r`,
- time windows `Delta, delta`,
- threshold budgets `eta_F, eta_K, A_F, A_K`.

[CHECKED] These are measurement conventions, not model changes. They do not trivialize the hidden-precursor question, because the question is precisely whether exact NS can keep a physically declared transfer observable quiet until a short activation window.

[CHECKED] Reduced-model fallback:

- not needed for Phase 0,
- and undesirable here because the whole point is to avoid drifting back into an engineered mechanism model.

## 6. Gate analysis and pass/fail verdict

[CHECKED] Positive-firewall target for this event:

```text
If E_flux occurs at (x_*, t_*) with parameters (n, rho, r, Delta, delta),
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

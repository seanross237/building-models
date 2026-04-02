# Exploration 002 Report

## Decision target

Either there exists one preferred precursor observable `P` and one earlier region `R_-` for the exact-NS event `E_flux` such that `P` is dynamically tied to the delayed-transfer burst without merely restating the event earlier in time and without collapsing into a closed route, or no such precursor pair survives and the strategy should stop with the correct failure category.

## 1. Executive verdict

[CHECKED] The gate passes, but only after rejecting the obvious same-flux-earlier candidate as too tautology-adjacent.

[CHECKED] Preferred precursor observable:

```text
P(t) := K_{n-1}^{phi_r}(t),
```

the exact localized feeder-band energy in the band immediately upstream of the event band.

[CHECKED] Preferred earlier region:

```text
R_- := B_r(x_*) x [t_* - r^2, t_* - delta],
```

with `0 < delta < r^2`, i.e. the earlier slice of the same backward parabolic cylinder used to localize the event.

[VERIFIED] Primary-source anchors used to lock this pair:

- Eyink-Aluie, "Localness of energy cascade in hydrodynamic turbulence. I. Smooth coarse-graining," *Physics of Fluids* 21 (2009), DOI `10.1063/1.3266883`. This gives the exact smooth-filtered band-pass energy densities `k_n` and the exact transfer identity `T_n = Pi_{n-1} - Pi_n`.
- Barker-Seregin, "A necessary condition of potential blowup for the Navier-Stokes system in half-space," *Mathematische Annalen* 369 (2017). Its notation section uses the standard local NS region

```text
Q(z_0,R) = B(x_0,R) x (t_0 - R^2, t_0).
```

[CHECKED] One key shift settled the gate:

```text
The smallest non-tautological precursor is not the same handoff observable watched earlier.
It is the earlier current-carrier reservoir for that handoff.
```

[CHECKED] No backup pair is retained. The closest alternatives are either too close to `E_flux`, too pressure-adjacent, or too generic to stay Tao-facing.

## 2. Candidate precursor audit

[CHECKED] Audit criterion:

```text
The candidate must stay inside the exact-NS delayed-transfer map from exploration 001, but it
must not simply re-time the event, and it must not reopen a closed pressure / De Giorgi /
epsilon-regularity branch.
```

### 2.1 Earlier same-band flux

[CHECKED] First near-miss candidate:

```text
F_n^{phi_r}(t) = integral phi_r(x) (Pi_{n-1}(x,t) - Pi_n(x,t))_+ dx
```

measured on the earlier slab `t in [t_* - r^2, t_* - delta]`.

[CHECKED] Rejection reason: as a preferred precursor this is still too close to the event. It uses the same transfer channel into the same band and changes only the time interval. Making the interval disjoint helps, but not enough for this prompt's anti-tautology requirement.

[CHECKED] I also considered the one-step-upstream flux

```text
F_{n-1}^{phi_r}(t) = integral phi_r(x) (Pi_{n-2}(x,t) - Pi_{n-1}(x,t))_+ dx.
```

[CHECKED] That is less tautological than same-band flux, but I still rejected it as the preferred object. Small earlier `F_{n-1}^{phi_r}` can coexist with a pre-loaded feeder reservoir `K_{n-1}^{phi_r}`, so it is weaker as a "no earlier warning" witness than feeder-band energy itself.

### 2.2 Duchon-Robert activity

[CHECKED] Candidate family: earlier Duchon-Robert activity on the predecessor region.

[CHECKED] Rejection reason: this is better treated as a backup event family than as the precursor to the chosen event. It is exact-NS faithful, but less tightly tied to the specific adjacent-band witness `K_n^{phi_r}`.

### 2.3 Lamb-vector / Beltrami-deficit geometry

[VERIFIED] The local library already contains the decisive negative input: exact-Beltrami simplification is real, but the near-Beltrami advantage collapses under tiny perturbations.

[CHECKED] Rejection reason: too fragile and too pressure-route-adjacent to serve as the one preferred precursor for the delayed-transfer gate.

### 2.4 Vortex stretching / enstrophy production

[CHECKED] Candidate family: localized vortex-stretching or enstrophy-production quantities on an earlier region.

[CHECKED] Rejection reason: these measure amplification in general rather than the declared handoff from feeder band to witness band. They are too generic for the Tao-facing role map.

### 2.5 Feeder-band energy reservoir

[CHECKED] Surviving candidate:

```text
P(t) = K_{n-1}^{phi_r}(t).
```

[CHECKED] Why this survives while earlier flux does not:

- it remains inside the exact band-pass budget underlying `E_flux`,
- it shifts one role upstream in the mechanism map rather than merely shifting time,
- it measures stored capacity for the later handoff, not the handoff itself,
- it is still exact-NS observable with no model change.

## 3. Preferred precursor-and-region pair

[CHECKED] Preferred precursor observable:

```text
P(t) := K_{n-1}^{phi_r}(t)
     := integral phi_r(x) k_{n-1}(x,t) dx,
```

where

```text
k_{n-1}(x,t) := (1/2) tau_{n-2}(u_{n-1}, u_{n-1})(x,t),
u_m := G_{ell_m} * u,
tau_m(a,b) := overline(a tensor b)_{ell_m} - a_m tensor b_m.
```

[VERIFIED] Eyink-Aluie give the corresponding exact adjacent-band transfer identity

```text
T_n = Pi_{n-1} - Pi_n,
```

which is the exact transfer channel already used to define `E_flux`.

[CHECKED] Preferred earlier region:

```text
Q_r(z_*) := B_r(x_*) x (t_* - r^2, t_*),
R_-      := B_r(x_*) x [t_* - r^2, t_* - delta]
         = Q_r(z_*) cap {t <= t_* - delta}.
```

[VERIFIED] The backward parabolic cylinder is the canonical local NS region from primary PDE literature. I looked for a more mission-specific backward cone / predecessor paraboloid convention and did not find one locally. The only sharp backward-paraboloid lead I found was pressure-program literature, which I rejected for this gate as orthogonal and too closed-route-adjacent.

[CHECKED] Exact spacetime measurement set:

- exact NS solution `u`,
- exact smooth filter ladder `ell_n = rho^{-n} L`,
- exact localized cutoff `phi_r = phi_{x_*,r}`,
- times `t in [t_* - r^2, t_* - delta]`.

[CHECKED] Smallness condition representing "no earlier warning":

```text
sup_{t in [t_* - r^2, t_* - delta]} K_{n-1}^{phi_r}(t) <= eta_P.
```

[CHECKED] Why this is dynamically tied to `E_flux`:

- `E_flux` is a late burst of transfer into band `n` plus abrupt gain of `K_n^{phi_r}`,
- the immediate feeder object for that handoff is energy already present in band `n-1`,
- in Tao's role map this is the current carrier feeding the next-carrier witness.

[CHECKED] Why this is not just `E_flux` restated earlier:

- the event channel is transfer into band `n`,
- the precursor is stored energy in band `n-1`,
- the event asks for a late burst and output activation,
- the precursor asks whether the feeder reservoir stayed small throughout the earlier region.

[CHECKED] Why this is not a disguised closed pressure / De Giorgi / epsilon-regularity quantity:

- it is defined from exact smooth-filtered band energies and transfer identities,
- it does not invoke pressure decomposition, truncation levels, or `U_k`-style recurrences,
- the dynamics remain exact NS; only the observation map is filtered.

[CONJECTURED] If a later no-hidden-transfer theorem is true, `K_{n-1}^{phi_r}` is a better candidate than earlier upstream flux because it captures both slowly accumulated reservoir and rapidly accumulated reservoir before the final activation window.

## 4. Backup pair or rejection of alternatives

[CHECKED] No backup pair is retained.

[CHECKED] Closest rejected alternative:

- `F_{n-1}^{phi_r}` on `R_-` is the nearest live backup, but I do not retain it because it is still transfer-family-adjacent to the event and can miss a reservoir loaded before the predecessor window.

[CHECKED] Rejected Duchon-Robert backup:

- exact and meaningful,
- but too easy to reinterpret as a second event definition rather than a precursor to `E_flux`.

[CHECKED] Rejected Lamb-vector / Beltrami deficit:

- perturbatively fragile,
- pressure-route-adjacent,
- not a stable exact-NS delayed-transfer witness.

[CHECKED] Rejected vortex stretching / enstrophy production:

- generic amplification metric,
- weak tie to the chosen adjacent-band witness channel,
- high risk of drifting into "activity gets large" language.

## 5. Fidelity ledger and tautology/closed-route screen

[CHECKED] Fidelity ledger:

| Item | Status |
|---|---|
| dynamical system | exact NS itself |
| observation formalism | exact smooth coarse-graining / localized band energy |
| model change | none |
| exact structures preserved | incompressibility, viscosity, exact nonlinearity, exact local band-energy budget |
| discarded structures | none dynamically; only user-chosen filter / cutoff conventions |

[CHECKED] Tautology screen:

- rejected: same-band earlier flux as preferred precursor,
- accepted: feeder-band energy `K_{n-1}^{phi_r}` because it changes mechanism role, not only observation time.

[CHECKED] Closed-route screen:

- rejected: backward-paraboloid pressure geometry as preferred region,
- rejected: Lamb-vector / Beltrami-deficit route,
- rejected: vortex-stretching / enstrophy route,
- accepted: localized feeder-band energy because it stays inside the exact coarse-grained energy ledger from exploration 001.

[CHECKED] Honest limitation:

```text
This choice is theorem-facing, not theorem-proved.
The actual lower bound or counterexample question is Phase 2.
```

[CHECKED] Honest dead end:

```text
I explicitly checked whether a more canonical backward cone / paraboloid region was already
available locally. It was not. The only sharp paraboloid lead belonged to a pressure-localization
program, so I did not import that geometry into the present flux-based gate.
```

## 6. Gate analysis and pass/fail verdict

[CHECKED] What would count as a precursor lower bound theorem:

```text
If E_flux(x_*, t_*; n, r, delta) occurs, then
sup_{t in [t_* - r^2, t_* - delta]} K_{n-1}^{phi_r}(t) >= c(A_F, A_K, eta_F, eta_K, ...),
```

for some quantitative lower bound `c > 0`.

[CHECKED] What would count as a no-hidden-transfer statement:

```text
If
sup_{t in [t_* - r^2, t_* - delta]} K_{n-1}^{phi_r}(t) <= epsilon,
then E_flux cannot occur later on the final window of the same Q_r(z_*).
```

[CHECKED] What would count as a counterexample:

```text
An exact NS solution, or an exact-NS-derived observation setup with no model change,
for which E_flux occurs but
sup_{t in [t_* - r^2, t_* - delta]} K_{n-1}^{phi_r}(t)
```

stays arbitrarily small.

[CHECKED] What would count as failure of the precursor gate:

- only same-band earlier flux survives as "precursor,"
- only pressure / De Giorgi adjacent objects survive,
- or every non-tautological candidate is too generic or too fragile.

[CHECKED] That failure did not occur. One pair survives sharply enough to justify quantitative testing.

## Pass/Fail Verdict

```text
pass
```

[CHECKED] Exploration 002 succeeds. The strategy should proceed to Phase 2 with exactly one theorem-facing pair:

- preferred precursor observable: `K_{n-1}^{phi_r}`,
- preferred earlier region: `R_- = B_r(x_*) x [t_* - r^2, t_* - delta]`,
- no backup pair retained.

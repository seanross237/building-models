# Step 3 Should Start With A Neutral Eulerian Parabolic Localization Package

Status: `INFERRED` with `PROPOSED` protocol details

For Step 3 of the geometry route, the fixed localization protocol should start
from a neutral Eulerian parabolic package rather than from tube-adapted or
fully Lagrangian coordinates.

The concrete protocol chosen in Exploration 002 is:

- intensity threshold: `|omega(x,t)| >= r^-2`
- spatial scale: one dyadic ball `B_r(x_*)` centered at the candidate intense
  point
- time window: the backward parabolic interval `[t_* - r^2, t_*]`
- localization type: `Eulerian`

Equivalently, the audit package is the intense set

`E_r(t) = { x in B_r(x_*) : |omega(x,t)| >= r^-2 }`

inside the parabolic cylinder

`Q_r(x_*, t_*) = B_r(x_*) x [t_* - r^2, t_*]`.

This choice is operationally preferred because it keeps the geometry neutral
at the definition stage. Tube persistence then has to emerge from the behavior
of the intense set instead of being installed by a tube-fitted axis or by a
transported coordinate package. That makes the protocol auditable across both
the primary `filament or tube concentration` scenario and the `sheet or
pancake concentration` comparator.

The main rejection behind this entry is also reusable: tube-adapted or fully
Lagrangian localization should not be primary here because they risk hidden
normalization by encoding the hoped-for coherent tube family into the
localization itself before the bounded observables are defined.

One residual risk remains visible even under this protocol. The center
`(x_*, t_*)` and dyadic scale `r` can still be tuned after seeing favorable
geometry, so later comparisons have to keep the same scale and center
discipline across the primary and comparator scenarios.

Filed from:
- `missions/beyond-de-giorgi/library-inbox/step-003-exploration-002-localization-protocol.md`

# Direction-Field Diffusion Burden Exceeds The Inherited Step-3 Package

Status: `INFERRED` with `VERIFIED` support

On the intense set `|omega| >= r^-2`, the direction field
`xi = omega / |omega|` is protected from division by zero but not from
derivative-sensitive diffusion loss.

The Step-4 dynamic screen isolates the burden:

- preserving direction coherence over one Eulerian `r^2` window inherits
  diffusion terms involving derivatives of `omega` or equivalently
  `nabla xi`-type control;
- the Step-3 package supplies an amplitude threshold on `|omega|`, not the
  stronger derivative control needed to propagate `xi` coherence dynamically;
- importing that stronger package would push the branch back toward known
  direction-regularity criteria instead of extending the audited geometry
  route inside its existing bounds.

This is the compact reusable reason the direction half of the hybrid remains
fragile under the fixed Eulerian package even when the intense set stays away
from zero vorticity.

Filed from:
- `missions/beyond-de-giorgi/library-inbox/step-004-exploration-001-primary-hybrid-dynamic-screen.md`

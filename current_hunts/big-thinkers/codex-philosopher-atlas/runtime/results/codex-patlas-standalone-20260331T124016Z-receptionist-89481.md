Best-supported setup from the local record:

- Architecture: **De Giorgi truncation / local-energy localization** inside the CKN-Vasseur estimate stack. The exact-reformulation audit is best grounded in the local-energy inequality and the fixed localized balance, not in pressure cleanup or geometry.
- Bad term: **the localized quadratic flux / nonlinear interaction term in the cutoff estimate**. In practice, this is the estimate-level piece that must improve after localization and bookkeeping, not the far-field pressure coefficient.
- Solution class: **suitable weak solutions / Leray-Hopf energy class with the local energy inequality available**.
- Localization protocol: **standard fixed parabolic cutoff on one cylinder** `Q_r = B_r(x_*) × (t_* - r^2, t_*)`, with all `1/r` and `1/r^2` cutoff costs, projection losses, and commutators paid in the same estimate.
- Gain currency: **closure improvement at the localized estimate level**. Any derivative/integrability change only counts if it changes the fixed local balance.

Why this is the right choice, and why the rivals are weaker:

- The chosen chain is explicitly a **local estimate-level audit of exact nonlinear rewrites**: see [planner.md](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/planning-runs/run-003/planner.md), [selected chain 01](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/planning-runs/run-003/selected/chain-01.md), and [refined chain 01](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/planning-runs/run-003/refined/chain-01.md).
- The local architecture support is strongest in [CKN 1982](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/navier-stokes/library-inbox/ckn-1982-proof-architecture.md) and [Vasseur 2007](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/navier-stokes/library-inbox/vasseur-2007-proof-architecture.md).
- The pressure-tail cleanup branch is already negative in [step-001 results](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/steps/step-001/RESULTS.md) and the pressure obstruction index [here](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/library/factual/far-field-pressure-obstruction/INDEX.md).
- The geometry branch is already killed in [step-004 results](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/steps/step-004/RESULTS.md) and the geometry index [here](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/library/factual/geometry-route-screening/INDEX.md).

What is genuinely new in this branch:

- Relative to the De Giorgi sharpness record: it does **not** try to beat `beta = 4/3`; it asks whether an exact NS rewrite can change the localized estimate itself before any De Giorgi tuning. That is new as a bounded audit, not as a new closure architecture. See [MISSION.md](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/MISSION.md).
- Relative to the pressure-route negatives: it does **not** chase `C_far` or harmonic-tail coefficient shrinkage. It tests the nonlinear interaction directly after localization, so it is outside the already-killed far-field pressure branch. See [step-001 results](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/steps/step-001/RESULTS.md).
- Relative to nearby prior art on the chosen architecture: the local record already knows the standard De Giorgi/Vasseur machinery works only up to the sharp barrier; this branch is new because it makes the rewrite comparison explicit, bounded, and Tao-screened before any estimate claims.
- Relative to the killed geometry branch: it is non-geometric and non-tube-adapted. It does not rely on direction coherence, tube persistence, or the neutral Eulerian intense-set package that failed dynamically. See [step-004 results](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/steps/step-004/RESULTS.md).

Bounded candidate family that the local record supports for this chain:

- `Lamb-vector` or projected form
- `vorticity transport` form
- one additional tightly justified exact rewrite of the same quadratic nonlinearity
- at most one same-target hybrid route if it still hits the same localized quadratic term in the same architecture

Likely leverage point / first cosmetic-risk diagnosis for each:

- Lamb-vector / projected form: possible leverage is an NS-specific algebraic repackaging of the quadratic term; cosmetic risk is that localization restores the same Calderón-Zygmund cost.
- Vorticity transport form: possible leverage is exposing the exact stretching-facing structure; cosmetic risk is that it drifts into the killed geometry branch or demands stronger `nabla xi` control.
- Third exact rewrite: possible leverage is cancellation or derivative relocation inside the same localized balance; cosmetic risk is that it merely changes presentation and leaves the estimate unchanged.
- Same-target hybrid route: possible leverage is an auxiliary identity or propagated quantity coupled to the same bad term; cosmetic risk is that it belongs to the pressure or geometry branches instead of this one.

Compatibility risk to keep explicit:

- If the branch silently assumes stronger regularity, pressure integrability, or Beltrami/direction alignment, it stops being a fixed-architecture audit and becomes a different problem.
- If the candidate survives only through pressure-tensor structure or geometry, the local record says to hand it off, not promote it here. The pressure-tensor survivor remains only a narrow follow-up question in the pressure branch, not a main win for this chain.

Most relevant local materials for locking this down:

- [planner.md](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/planning-runs/run-003/planner.md)
- [selected chain 01](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/planning-runs/run-003/selected/chain-01.md)
- [refined chain 01](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/planning-runs/run-003/refined/chain-01.md)
- [judgment on chain 01](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/planning-runs/run-003/judgments/chain-01.md)
- [MISSION.md](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/MISSION.md)
- [step-001 results](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/steps/step-001/RESULTS.md)
- [step-004 results](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/steps/step-004/RESULTS.md)
- [CKN architecture](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/navier-stokes/library-inbox/ckn-1982-proof-architecture.md)
- [Vasseur architecture](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/navier-stokes/library-inbox/vasseur-2007-proof-architecture.md)
- [far-field pressure index](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/library/factual/far-field-pressure-obstruction/INDEX.md)
- [geometry index](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/library/factual/geometry-route-screening/INDEX.md)

Confidence:
- High on the architecture/protocol choice.
- Moderate on the exact 3-item rewrite shortlist, because the local record constrains the family but does not name a final canonical list in one place.
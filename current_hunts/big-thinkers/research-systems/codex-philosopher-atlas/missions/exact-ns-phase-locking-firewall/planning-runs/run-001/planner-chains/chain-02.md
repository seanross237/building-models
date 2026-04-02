# Chain 02 - Small Exact Phase-Locked Counterexample

## Central premise

The cleanest way to kill the firewall is not to argue against it abstractly but
to build the smallest honest exact Navier-Stokes subsystem that phase-locks for
long enough to realize Tao-like delayed transfer. This chain treats the mission
adversarially: if the firewall is false, a compact exact construction should
surface quickly once all forced companion modes are included.

## Verifiable result target

Either:

- a concrete helical/Fourier subsystem with a phase-locked or near-phase-locked
  manifold that sustains the required delayed transfer window;
- a sharp infeasibility memo showing why no such minimal subsystem survives
  exact accounting; or
- a narrowed handoff to another chain identifying the exact obstruction that
  killed the construction.

## Prior context to carry forward

- Tao's required causal jobs are fixed:
  slow clock,
  tiny trigger,
  amplifier,
  rotor exchange,
  next-stage pump.
- Exact NS support must include the forced conjugate partners and any mirror or
  companion modes needed for a real velocity field and exact triad closure.
- Earlier packet gates may be used as diagnostics, but the goal here is an
  explicit exact subsystem, not a packet admissibility score.

## Ordered steps

### Step 1 - Freeze the smallest honest support family

- Depends on: none.
- Actions:
  - pick the smallest exact mode/packet family that could plausibly implement
    Tao's five causal roles;
  - include all modes forced by conjugate completion, the Leray projector, and
    any companion triads that appear immediately once the core family is active;
  - specify the geometric parameters to vary:
    triad shape,
    helicity signs,
    scale ratio,
    and amplitude hierarchy.
- Expected output:
  - one exact support sheet with no hidden missing modes,
  - one parameter list for the search.
- Kill condition:
  - if no finite honest support family can even be written without immediate
    uncontrolled spillover, close with that negative result.

### Step 2 - Derive the exact reduced dynamics and candidate locking manifolds

- Depends on: Step 1.
- Actions:
  - write the exact projected ODEs for the chosen family;
  - identify gauge freedoms, conserved quantities, and candidate constant-phase
    or slowly drifting phase manifolds;
  - mark which phase relations correspond to the desired transfer directions.
- Expected output:
  - an exact finite-dimensional dynamics ledger,
  - one or more candidate phase-locked manifolds or relative equilibria.
- Kill condition:
  - if the exact reduced system has no meaningful phase-locking ansatz even
    before parameter tuning, stop.

### Step 3 - Search for Tao-like role separation inside the exact subsystem

- Depends on: Step 2.
- Actions:
  - ask whether geometry and helicity choices can produce the needed hierarchy:
    weak clock,
    tiny seed,
    strong amplifier,
    strong rotor,
    and effective next-stage pump;
  - identify whether any small parameter or scale ratio gives a usable delayed
    window rather than immediate transfer.
- Expected output:
  - a feasibility sheet recording which Tao-like roles can or cannot be realized
    simultaneously,
  - one best candidate regime if the answer is positive.
- Kill condition:
  - if the exact subsystem can only produce ordinary cascade behavior with no
    delayed-threshold regime, stop and record that sharply.

### Step 4 - Test stability of the locking window against spectators and viscosity

- Depends on: Step 3.
- Actions:
  - measure how long the phase-locking manifold or near-manifold persists;
  - quantify whether spectator channels stay subordinate during that window;
  - check whether viscosity or forced feedback destroys the regime before the
    next-stage transfer happens.
- Expected output:
  - one time-window stability report,
  - either a surviving exact candidate or a named failure mode.
- Kill condition:
  - if the locking window collapses before a meaningful delayed transfer event,
    the chain fails as a counterexample route.

### Step 5 - Compare the survivor against the firewall claim

- Depends on: Step 4.
- Actions:
  - match the surviving behavior against the mission's real success test:
    sustained phase coherence long enough for delayed transfer, not just
    transient favorable phases;
  - if the subsystem succeeds, state exactly why the firewall should be dropped;
  - if it fails, hand off the precise obstruction:
    coefficient rigidity,
    spectator blowup,
    incompatibility of locking conditions,
    or no honest delayed window.
- Expected output:
  - either a counterexample memo,
  - or a precise failure memo that another chain can reuse.
- Kill condition:
  - if the "success" is only numerical plausibility with no exact support and no
    closed reduced system, it does not count.

## Why this chain is meaningfully different

This is the only chain whose positive outcome kills the entire firewall idea by
construction. It is not trying to prove a lower bound or define a new
functional. It tries to build the smallest exact subsystem that survives honest
phase accounting.

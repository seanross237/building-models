# Favored Route Sketch

## Working Name

Canonical helical-packet variational route with a homochiral bottleneck.

## Core Object

Let an admissible packet family consist of:

- a finite sign-closed helical support `S`
- a partition into Tao-role packets `P_A, P_B, P_C, P_D, P_A_next`
- a target-edge hypergraph `G_target`
- exact helical-triad drive functionals `Drive_e`
- a declared delayed-trigger time window

## Canonical Functionals

Define:

- `Drive_target`: normalized total drive along the declared Tao target edges
- `Leak`: normalized spectator leakage, internal plus external, divided by `Drive_target`
- `SignDefect`: a functional measuring departure from sign-definite / near-homochiral organization on the active support
- `Cost = Leak + lambda * SignDefect`

The exact choice of `SignDefect` is open, but it should be computed from the helical triad ledger rather than from a coarse phenomenological statistic.

## First Theorem Targets

### Target A: Positive obstruction

Prove:

- for every Tao-like admissible packet family, `Leak + lambda * SignDefect >= c0`

for some explicit `c0 > 0`.

Interpretation:

- Either the packet family leaks too much to behave like Tao's near-isolated circuit, or it becomes too sign-coherent and loses the forward-transfer behavior needed for the Tao mechanism.

### Target B: Canonical extremizer

If Target A fails, prove:

- every minimizing sequence for `Cost` has a compact representative up to exact symmetries

and identify the resulting canonical extremizer.

Interpretation:

- Even failure is useful because it produces the canonical packet object that the local program still lacks.

## Why Homochiral Structure Matters

- The helical-decimated model shows sign-definite helicity can create extra critical control.
- The helical triad literature shows minority-helicity modes are what re-enable forward transfer.
- That suggests a structural squeeze:
  - suppress minority-helicity modes and gain control / inverse-transfer tendencies
  - keep minority-helicity modes and recover forward transfer, but also recover the spectator couplings that destroy near-isolation

## Immediate Continuation Tasks

1. Formalize `SignDefect` in exact helical-triad language.
2. Prove basic compactness or coercivity statements for `Leak` and `SignDefect` under normalization.
3. Test the route first on the smallest admissible packet supports suggested by the local exploration-001 summary.

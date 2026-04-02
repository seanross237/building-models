# Route Map

## Current Route Families

### R1. Canonical Exact Helical Packet Model

- Status: active
- Route type: bridge route plus verification route
- Current score: 0.80
- Why live:
  - Directly matches the authoritative local frontier.
  - Uses exact Navier-Stokes structure rather than another estimate chain.
  - Can be turned into a theorem-facing object.
- Main risk:
  - May stall at arbitrary packet choices if no canonization principle is added.

### R1a. Homochiral Bottleneck Inside the Canonical Packet Model

- Status: favored
- Route type: bridge route plus constraint route
- Current score: 0.86
- Core idea:
  - Define exact Tao-like packet roles canonically in helical variables.
  - Add a sign-defect functional measuring how far the candidate packet family is from sign-definite helicity / homochiral dominance.
  - Show that minimizing leakage pushes packets toward near-homochiral behavior.
  - Then use the external homochiral evidence to argue that near-homochiral packets do not support the Tao-style forward delayed-threshold circuit.
- Why it won:
  - It converts local packet ambiguity into a variational problem.
  - It adds a one-sided gain missing from pure canonization.
  - It is tightly aligned with Tao's "use finer nonlinear structure" message and with helical triad literature.

### R1b. Pure Minimal-Leakage Canonical Packet Model

- Status: backup
- Route type: bridge route
- Current score: 0.71
- Core idea:
  - Canonicalize by minimizing normalized spectator leakage over sign-closed helical supports satisfying the Tao screen.
- Why downgraded:
  - Strongly aligned with local needs.
  - But without a second monotone or sign-sensitive quantity, it risks remaining a pure model-building exercise.

### R2. Wavelet-First Packet Canonization

- Status: downgraded to auxiliary tool
- Route type: analogy route plus evidence-finding route
- Current score: 0.55
- Core idea:
  - Use a single-scale exact wavelet representation to define the packets first in physical space, then map to helical supports.
- Why not favored:
  - Useful for extraction.
  - But the local open object lives in exact helical triad bookkeeping, so a wavelet-first theorem object adds one more layer of choice rather than removing one.

### R3. Critical-Space / Concentration-Compactness Restart

- Status: pruned
- Route type: decomposition route
- Final score before pruning: 0.25
- Why pruned:
  - The local status memo closes standard host-space retries.
  - External critical-space work is substantial already.
  - No new one-sided mechanism surfaced in the checked sources.

### R4. Anisotropic Geometric Criteria / Near-Eigenfunction Route

- Status: pruned as main route
- Route type: constraint route
- Final score before pruning: 0.32
- Why pruned:
  - Interesting criteria exist.
  - But the checked sources made this look more like a mature conditional-criterion family than an underexplored theorem object with high downstream leverage.

## Route Evolution By Cycle

### After Cycle 1

- Strongest route: R1 canonical exact helical packet model.
- Newly pruned:
  - singleton exact Tao circuit
  - trigger-only exact Tao object

### After Cycle 2

- Strengthened:
  - R1 because external helical/helicity literature supplied a possible one-sided mechanism.
- Weakened:
  - R3 and R4 because they looked more explored and less aligned with the local frontier.
- New subroutes:
  - R1a homochiral bottleneck
  - R1b pure minimal-leakage canonization
  - R2 wavelet-first extraction route

### After Cycle 3

- Final ranking:
  1. `R1a` canonical helical packet + homochiral bottleneck
  2. `R1b` canonical helical packet + pure leakage minimization
  3. `R2` wavelet extraction as auxiliary layer
  4. `R4` anisotropic route
  5. `R3` critical-space restart

## Chosen Route

- Chosen route: `R1a`
- Reason:
  - It is the narrowest route that is still locally live.
  - It upgrades "packet model first" into a concrete optimization-and-obstruction program.
  - It benefits from exact helical triad structure and from the sampled sign-definite helicity literature.
  - It offers two valuable outputs:
    - a positive obstruction bound
    - or a canonical extremizer for further analysis

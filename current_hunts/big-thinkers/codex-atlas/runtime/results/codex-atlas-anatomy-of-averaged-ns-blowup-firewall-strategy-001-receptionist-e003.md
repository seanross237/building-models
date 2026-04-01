# Pre-exploration briefing for Strategizer

## 1) Exact Fourier/helical form best suited to a minimal triad-level amplitude system

The local library does **not** contain a helical-basis or Waleffe-style triad decomposition that would let you write down a minimal exact triad amplitude system directly.

What it **does** contain is the exact NS obstruction language in Fourier/Riesz-projected form:

- `factual/navier-stokes/vasseur-de-giorgi/compensated-compactness-commutator-obstruction.md` gives the bottleneck pressure term as a rank-1 tensor fed through `R_i R_j`.
- `factual/navier-stokes/vasseur-de-giorgi/exact-far-field-pressure-obstruction.md` and `beta-current-value-four-thirds.md` isolate the exact pressure split `P = P_{k1} + P_{k2}` and identify `P_{k21}` as the load-bearing bad local term.
- `factual/navier-stokes/tao-averaged-ns-delayed-transfer-circuit.md` says the real exact-NS firewall question is whether triadic geometry can realize Tao-style engineered couplings and signs, not whether generic harmonic-analysis structure survives.

So, for a local-library-supported exact formulation, the right object is the Leray-projected quadratic nonlinearity / pressure-source formulation, not a helical amplitude basis. If the next exploration needs a helical triad model, it should go to primary sources directly.

## 2) Whether the library has helical-triad, Waleffe-style, or exact triad-geometry notes

The library has **no real helical-triad or Waleffe-style notes**.

What is present:

- `factual/navier-stokes/vasseur-de-giorgi/compensated-compactness-commutator-obstruction.md` mentions only a generic remaining direction: “vortex line structure or helicity conservation.”
- `factual/navier-stokes/vasseur-de-giorgi/pressure-bernoulli-dominance-truncated.md` asks an open question about “flows with helical structure.”
- `factual/navier-stokes/tao-averaged-ns-delayed-transfer-circuit.md` talks about exact NS triadic geometry at the firewall level, but not helical coefficients or Waleffe sign tables.

That is the extent of the local helical material. It is suggestive, not operational.

## 3) Leray-projection rigidity, target-mode projection, conjugate-mode constraints

The local notes are strongly aligned on rigidity:

- `factual/navier-stokes/vasseur-de-giorgi/h1-pressure-dead-end.md` says the surviving lead is an alternative harmonic far-field split, not Vasseur’s literal `P_{k21}` term, and that any Leray-Hopf-class route pairing pressure against De Giorgi test functions hits the `W^{1,3}` wall.
- `factual/navier-stokes/vasseur-de-giorgi/exact-far-field-pressure-obstruction.md` says the harmonic `P_{k1}` is already favorable; the bottleneck is the local non-divergence piece `P_{k21}`.
- `factual/navier-stokes/vasseur-de-giorgi/beta-current-value-four-thirds.md` makes the same point quantitatively: the only term stuck at `4/3 - 5/(3q) -> 4/3` is the local non-divergence pressure term.
- `factual/navier-stokes/vasseur-de-giorgi/strategy-001-adversarial-synthesis.md` and `near-beltrami-negative-result.md` both say Leray projection fixes `div(u_below) != 0` but does not change the qualitative picture.
- `factual/navier-stokes/vasseur-de-giorgi/compensated-compactness-commutator-obstruction.md` says truncation destroys div-curl structure and the commutator route is vacuous for bounded multipliers.

Net: the library treats Leray projection as a correction, not a source of extra flexibility. I did not find any local note on “target-mode projection” or “conjugate-mode constraints” in the Waleffe/helical sense.

## 4) Meta guidance for a minimal feasibility-test exploration

The best local meta guidance for the next phase is:

- `meta/goal-design/require-mechanism-layer-maps.md` - split exact PDE, reduced toy/circuit, and theorem layers; assign roles to variables.
- `meta/methodology/definition-extraction-gates-computation.md` - do a Phase 0 definition/mechanism extraction before spending compute.
- `meta/goal-design/specify-failure-paths.md` - require an explicit structural failure explanation and what would work instead.
- `meta/methodology/structural-vs-quantitative-discrepancy.md` - decide whether the candidate is structurally impossible or just quantitatively off.
- `meta/methodology/test-improvability-before-pursuing-variations.md` - test whether the target step is independently improvable before trying variants.
- `meta/methodology/adversarial-check-between-phases.md` - run a lightweight adversarial check after Phase 2 and before deeper commitment.
- `meta/methodology/model-pde-comparison-for-mechanism-identification.md` - compare against related PDEs to identify the mechanism, not just the estimate.

For this candidate, the sharpest feasibility test is: can exact NS realize the same load-bearing triadic coupling architecture with an explicit structural explanation if not? Avoid estimate-level elaboration.

## Bottom line

The local library supports the firewall question at the level of exact pressure/Leray rigidity and Tao-style engineered couplings, but it does **not** contain a genuine helical-triad/Waleffe toolkit. Treat helical triads as a primary-source task for the next exploration.

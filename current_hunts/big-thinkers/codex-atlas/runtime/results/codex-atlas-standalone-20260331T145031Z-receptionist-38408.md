The local library gives you a sharp pressure-side and method-limits picture, but it does not yet reconstruct Tao’s finite-dimensional cascade internals on its own.

**Most useful factual material**
- [Navier-Stokes index](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/agents/library/factual/navier-stokes/INDEX.md) already frames Tao (2016) as the benchmark: generic energy-level and harmonic-analysis structure is insufficient, and the local De Giorgi barrier lives at `P_{k21}`, not the favorable harmonic `P_{k1}`.
- [beta-current-value-four-thirds.md](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/beta-current-value-four-thirds.md) gives the exact recurrence arithmetic: `U_{k-1}^0 * U_{k-1}^{1/2} * U_{k-1}^{5/6} = U_{k-1}^{4/3}`.
- [exact-far-field-pressure-obstruction.md](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/exact-far-field-pressure-obstruction.md) is the cleanest notation reconciliation: `P_{k1}` is already favorable; `P_{k21}` is the obstruction; the only live lead is an alternative near/far decomposition that would have to move part of the dangerous interaction into a harmonic far-field piece.
- [non-cz-pressure-routes-tool-independence.md](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/non-cz-pressure-routes-tool-independence.md) is the strongest “this is structural” note: IBP gives `beta = 1`, H^1/BMO reproduces `beta = 4/3`, CRW gives `beta <= 1`, and the gap between IBP and CZ is exactly `1/3`.
- [s2-adversarial-review-beta-four-thirds.md](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/s2-adversarial-review-beta-four-thirds.md) connects directly to Tao: any proof of global regularity must use specific NS algebra, not just energy + harmonic analysis.
- [post-2007-beta-landscape.md](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/post-2007-beta-landscape.md) says no post-2007 paper improved `beta` beyond `4/3`, and cites Tao as the independent reason generic methods cannot work.
- [MISSION-VALIDATION-GUIDE.md](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/instances/navier-stokes/MISSION-VALIDATION-GUIDE.md) sets the benchmark: Tao’s 2016 obstruction is the standard any regularity proof must beat.
- [exploration-005-literature-vortex-stretching.md](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/instances/navier-stokes/library-inbox/exploration-005-literature-vortex-stretching.md) is the best local note with explicit averaged-operator formulas:
  - ordinary NS operator: `B(u,v) = -(1/2) P[(u·∇)v + (v·∇)u]`
  - Tao’s averaged operator: an average of rotated/dilated/order-zero-multiplier copies of `B`
  - key implication: blowup survives despite preserved cancellation and standard harmonic-analysis bounds.
- [far-field-pressure-harmonic-loophole REPORT 002](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/instances/far-field-pressure-harmonic-loophole/strategies/strategy-001/explorations/exploration-002/REPORT.md) gives the local primitive-variable averaged form:
  - `∂_t u + T(u,u) = Δu - ∇p`, `div u = 0`
  - `-Δp = div T(u,u)`
  - `T` is nonlocal because the averaging inserts order-zero Fourier multipliers before the pressure solve.

**What the local library does not yet give you**
- There is no dedicated local note that reconstructs Tao’s finite-dimensional cascade architecture, modal packets, or scale-to-scale transfer rules in enough detail to stand alone.
- So Phase 0 still needs the paper itself for the actual cascade internals and blowup trigger.
- The local library is strong on the operator/pressure mismatch and the “generic methods are insufficient” claim, but weak on the actual finite-dimensional mechanism.

**Meta guidance for GOAL.md**
- Separate the three layers explicitly: averaged operator, transfer architecture, final blowup mechanism.
- Ask for equations first, not prose.
- Force notation reconciliation before falsification:
  - `P_{k1}` is not the bottleneck.
  - `P_{k21}` is.
  - any later Wolf-style near/far split is a different vocabulary and must be aligned first.
- Ask the explorer to state exactly which NS structure averaging removes and whether Tao actually uses that absence at a specific step.
- Include a hard stop: if the cascade cannot be stated equation-level, report reconstruction failure rather than guessing a firewall.
- Avoid vague language like “more cancellation”; ask for the exact identity, sign structure, symmetry, or locality property.

I also wrote the sentinel briefing to:
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/runtime/results/codex-atlas-anatomy-of-averaged-ns-blowup-firewall-strategy-001-receptionist-e001.md`

And I appended the search log to:
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/agents/library/librarian-log.md`
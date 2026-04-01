# Pre-Exploration Briefing: Tao 2016 Averaged NS Blowup

## High-Value Factual Material

- **[High confidence]** The Navier-Stokes index already frames the mission correctly: Tao (2016) is the benchmark showing that generic energy-level / harmonic-analysis structure is insufficient, while the local De Giorgi barrier is tied to the `P_{k21}` pressure slot, not the favorable harmonic `P_{k1}`.
- **[High confidence]** The strongest factual anchor for the bottleneck is [`execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/beta-current-value-four-thirds.md`](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/beta-current-value-four-thirds.md): the load-bearing arithmetic is `U_{k-1}^0 * U_{k-1}^{1/2} * U_{k-1}^{5/6} = U_{k-1}^{4/3}`, and the bad term is the local non-divergence pressure piece `P_{k21}`.
- **[High confidence]** [`execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/exact-far-field-pressure-obstruction.md`](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/exact-far-field-pressure-obstruction.md) sharpens the notation:
  - `P_{k1}` is the harmonic/nonlocal term and is already favorable.
  - `P_{k21}` is the actual obstruction.
  - The only surviving lead is an alternative near/far decomposition that would have to move part of the dangerous local interaction into a harmonic far-field piece.
- **[High confidence]** [`execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/non-cz-pressure-routes-tool-independence.md`](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/non-cz-pressure-routes-tool-independence.md) is the best local statement of why the barrier is structural:
  - direct IBP gives `beta = 1`,
  - H^1/BMO gives `beta = 4/3`,
  - CRW/commutator gives `beta <= 1`,
  - the gap between IBP and CZ is exactly `1/3`,
  - Wolf-style local pressure decomposition is explicitly listed as untested.
- **[High confidence]** [`execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/s2-adversarial-review-beta-four-thirds.md`](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/s2-adversarial-review-beta-four-thirds.md) provides the clearest Atlas-side Tao connection: Tao (2016) says any proof of global regularity must use the specific algebraic structure of the NS nonlinearity, so energy + harmonic-analysis only methods are insufficient.
- **[High confidence]** [`execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/post-2007-beta-landscape.md`](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/post-2007-beta-landscape.md) carries the same message in survey form: no paper since 2007 improved `beta` beyond `4/3`, and Tao is cited as the independent reason generic methods cannot work.
- **[High confidence]** [`execution/instances/navier-stokes/MISSION-VALIDATION-GUIDE.md`](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/instances/navier-stokes/MISSION-VALIDATION-GUIDE.md) gives the mission benchmark: Tao’s 2016 obstruction is the standard by which any regularity proof must be judged.

## Explicit Tao Material Available Locally

- **[Provisional but useful]** The best local writeup with explicit averaged-operator formulas is [`execution/instances/navier-stokes/library-inbox/exploration-005-literature-vortex-stretching.md`](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/instances/navier-stokes/library-inbox/exploration-005-literature-vortex-stretching.md).
- It records the unaveraged operator as
  - `B(u,v) = -(1/2) P[(u·∇)v + (v·∇)u]`
- It records Tao’s averaged operator as an average of rotated/dilated/order-zero-multiplier copies of `B`.
- It records the key implication:
  - blowup can occur even though the averaged model preserves energy cancellation and standard harmonic-analysis estimates,
  - therefore a proof for real NS must use structure finer than harmonic analysis alone.

- **[High confidence]** The strongest Tao-filter note in the local instance archive is [`execution/instances/far-field-pressure-harmonic-loophole/strategies/strategy-001/explorations/exploration-002/REPORT.md`](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/instances/far-field-pressure-harmonic-loophole/strategies/strategy-001/explorations/exploration-002/REPORT.md):
  - Tao’s averaged primitive-variable form is `∂_t u + T(u,u) = Δu - ∇p`, `div u = 0`,
  - taking divergence gives `-Δp = div T(u,u)`,
  - `T` is nonlocal because the averaging inserts order-zero Fourier multipliers before the pressure solve,
  - the local Poisson law `-Δp = ∂_i∂_j(u_i u_j)` is therefore replaced by a pseudodifferentially averaged source.

## What The Local Library Does Not Yet Give You

- **[High confidence]** There is no dedicated local note that reconstructs Tao’s finite-dimensional cascade architecture in enough detail to supply the modal packets / transfer chain on its own.
- **[High confidence]** The library is strong on the barrier side and the pressure-side mismatch, but weak on the actual cascade internals.
- **[High confidence]** That means Phase 0 still needs reconstruction from the paper itself for:
  - the cascade variables,
  - the scale-to-scale transfer rules,
  - the final norm-inflation / blowup trigger.

## Meta-Guidance For A Tight GOAL.md

- Force an explicit separation between:
  - the averaged operator,
  - the finite-dimensional cascade or transfer architecture,
  - the final blowup mechanism.
- Ask for equations first, not prose summaries.
- Ask the explorer to state exactly which NS structure is absent after averaging and whether Tao actually exploits that absence at a specific step.
- Make notation reconciliation mandatory before falsification:
  - `P_{k1}` is not the bottleneck,
  - `P_{k21}` is,
  - any later Wolf-style near/far split is a different vocabulary and must be aligned before testing.
- Tell the explorer to stop and report reconstruction failure if the cascade cannot be stated equation-level.
- Avoid vague instructions like “find more cancellation”; instead ask for the exact identity, sign structure, or symmetry that matters.

## Search Log

- Started from [`execution/agents/library/factual/INDEX.md`](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/agents/library/factual/INDEX.md), [`execution/agents/library/factual/navier-stokes/INDEX.md`](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/agents/library/factual/navier-stokes/INDEX.md), [`execution/agents/library/meta/INDEX.md`](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/agents/library/meta/INDEX.md), and the mission/strategy files under `execution/instances/anatomy-of-averaged-ns-blowup-firewall/`.
- Followed the Navier-Stokes and Vasseur-De Giorgi branches, then cross-checked mission-specific prior notes and the far-field-pressure-harmonic-loophole Tao-filter writeup.
- Result: strong local support for the operator/pressure mismatch and Tao-as-generic-method-limit claim; weak local support for the finite-dimensional cascade internals themselves.

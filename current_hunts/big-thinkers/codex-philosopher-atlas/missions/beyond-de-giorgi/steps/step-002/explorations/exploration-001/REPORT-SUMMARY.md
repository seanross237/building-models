# Exploration 001 Summary

- Goal: benchmark the three geometry-route candidate families against the prior-art geometry frameworks explicitly named in the local repository, and identify where a Step 2 claim would only relabel that literature rather than add a mission-live ingredient.

- What was checked:
  - `missions/beyond-de-giorgi/steps/step-002/GOAL.md`
  - `missions/beyond-de-giorgi/MISSION.md`
  - `missions/beyond-de-giorgi/CHAIN.md`
  - `missions/beyond-de-giorgi/planning-runs/run-002/refined/chain-02.md`
  - `missions/beyond-de-giorgi/planning-runs/run-002/selected/chain-02.md`
  - `missions/beyond-de-giorgi/planning-runs/run-002/attacks/chain-02.md`
  - `missions/beyond-de-giorgi/planning-runs/run-002/judgments/chain-02.md`
  - `missions/beyond-de-giorgi/planning-runs/run-001/refined/chain-03.md`
  - `missions/beyond-de-giorgi/planning-runs/run-001/selected/chain-03.md`
  - `missions/beyond-de-giorgi/planning-runs/run-001/attacks/chain-03.md`
  - `missions/beyond-de-giorgi/planning-runs/run-001/judgments/chain-03.md`
  - `missions/beyond-de-giorgi/steps/step-001/RESULTS.md`
  - `library/factual/far-field-pressure-obstruction/INDEX.md`
  - `library/factual/far-field-pressure-obstruction/generic-harmonic-regularity-fails-the-tao-gate.md`
  - `library/factual/far-field-pressure-obstruction/algebraic-rewrites-and-local-geometry-fail-the-tao-gate.md`

- Outcome: succeeded

- One key takeaway: the local corpus already treats direction-regularity as established prior art, treats local Beltrami depletion as exact but fragile cancellation on the wrong object unless it reaches full stretching, and leaves tube persistence live only as an underdefined dynamic ingredient rather than a ready-made criterion.

- Benchmark verdict for `vorticity-direction coherence / direction-regularity`:
  - Existing framework in local record: Constantin-Fefferman (1993) plus later direction-coherence literature.
  - Claim boundary in local record: sufficiently regular vorticity direction implies regularity, but the repository does not restate the detailed theorem.
  - Forbid novelty claim rule: if Step 2 merely says "regularity follows from sufficiently regular/coherent vorticity direction," or gets there only by smuggling in stronger `nabla xi` control, it is a relabeling.
  - Remaining live gap: an NS-specific bridge from localized direction coherence to full `S omega . omega` control or to a new persistence mechanism.

- Benchmark verdict for `geometric depletion / local Beltrami or alignment`:
  - Existing framework in local record: exact Beltrami kills the Lamb-vector / pressure-side CZ loss, with `beta_eff -> 1.0`, but requires >98 percent global alignment and fails under 1 percent perturbation.
  - Claim boundary in local record: exact cancellation exists, but local deficit controls `u x omega`, not automatically `S omega` or full stretching; nonlocal strain remains.
  - Forbid novelty claim rule: no novelty claim may rest only on near-Beltrami language, Lamb-vector cancellation, or a Beltrami-to-criterion bridge that secretly imports stronger `xi`-regularity.
  - Remaining live gap: a scale-appropriate estimate from localized deficit to the full stretching mechanism, including exterior/nonlocal contributions.

- Benchmark verdict for `tube coherence or persistence`:
  - Existing framework in local record: coherent tubes/persistence are repeatedly named as a geometry family, but the repository does not provide a standalone theorem statement for a tube-persistence criterion.
  - Claim boundary in local record: tube persistence is only a possible NS-specific dynamic ingredient unless supplied with an explicit transport identity, coercive quantity, or rigorous persistence mechanism.
  - Forbid novelty claim rule: descriptive tube language without a propagated quantity, fixed scenario/localization, and a concrete effect on the full stretching estimate is not novel.
  - Remaining live gap: a transport or multiscale persistence mechanism tied to a fixed scenario and stretching representation.

- Leads worth pursuing:
  - narrow Step 2 to a dynamic-hybrid route, most plausibly `direction coherence + tube persistence`, under fixed scenario and localization choices;
  - demand a full-stretching target from the start, not a Lamb-vector or local-self-induced proxy;
  - use the pressure obstruction memo as a standing rule against static singular-integral or alignment-language restatements.

- Unexpected findings:
  - the repository has no dedicated factual packet for the geometry prior-art literature, so the benchmark had to stay at the level of the mission/planning record;
  - the strongest negative benchmark is actually the local judgment record on the geometry chains, not a separate theorem digest.

- Computations worth doing later if outside scope:
  - none numerical; the next useful work is conceptual, namely fixing a scenario class, localization protocol, and stretching representation for any surviving hybrid route.

- Whether any family remains live enough to justify Step 2 work:
  - not as a standalone family on the present record;
  - only a narrow dynamic-hybrid continuation remains honest, with tube persistence as the least pre-killed ingredient and direction coherence serving as a benchmark target rather than a novelty claim.

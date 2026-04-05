# Exploration 001 Report

## Goal

Benchmark the geometry-route candidate families against the prior-art geometry frameworks explicitly named in the local repository context, and determine where this branch would merely restate that literature rather than add a mission-live ingredient.

Candidate families:

- vorticity-direction coherence / direction-regularity routes
- geometric depletion / local Beltrami or alignment routes
- tube coherence or persistence routes

## Method

- Read the required mission, chain, planning, attack, judgment, and obstruction documents from the local repository.
- Extract only repository-supported prior-art benchmarks and claim boundaries.
- Mark direct repository-backed statements as `[VERIFIED]`.
- Mark calibration judgments that synthesize multiple repository statements as `[INFERRED]`.
- Record dead ends or missing support honestly.

## Working Notes

### Initial skeleton

- Report initialized before detailed source review.
- Repository check: the local corpus does not contain a standalone factual prior-art packet for the geometry literature; the strongest reusable sources are the mission/planning records plus the pressure-side obstruction memo. Source: `missions/beyond-de-giorgi/steps/step-002/REASONING.md`.

## Findings

### A. Benchmark frame and negative guardrail

- [VERIFIED] Step 2 explicitly requires a source-based benchmark against existing geometry frameworks, with candidate families limited to direction coherence, geometric depletion / near-Beltrami routes, and tube coherence or persistence. Sources:
  - `missions/beyond-de-giorgi/steps/step-002/GOAL.md`
  - `missions/beyond-de-giorgi/CHAIN.md`
  - `missions/beyond-de-giorgi/planning-runs/run-002/refined/chain-02.md`
- [VERIFIED] The local corpus also makes the pressure-side negative guardrail explicit: generic harmonic regularity, Calderon-Zygmund repackaging, and local geometry do not count as mission-live ingredients if they leave the surviving bad coefficient or nonlocal obstruction unchanged. Sources:
  - `missions/beyond-de-giorgi/steps/step-001/RESULTS.md`
  - `library/factual/far-field-pressure-obstruction/generic-harmonic-regularity-fails-the-tao-gate.md`
  - `library/factual/far-field-pressure-obstruction/algebraic-rewrites-and-local-geometry-fail-the-tao-gate.md`
- [INFERRED] For the geometry branch, this means a static singular-integral or alignment-language reformulation is disqualified unless it changes the estimate on the full stretching mechanism or supplies a genuinely NS-specific persistence ingredient that the averaged model plausibly destroys.

### B. Family 1: Vorticity-direction coherence / direction-regularity

#### What framework already exists in the local corpus

- [VERIFIED] The mission context records a concrete prior-art family here: "Constantin-Fefferman (1993): regularity holds if vorticity direction is sufficiently regular." The refined geometry chain also says Step 1 must benchmark against "Constantin-Fefferman-Majda style direction coherence" and "later vorticity-direction coherence work." Sources:
  - `missions/beyond-de-giorgi/MISSION.md`
  - `missions/beyond-de-giorgi/planning-runs/run-002/mission-context.md`
  - `missions/beyond-de-giorgi/planning-runs/run-002/refined/chain-02.md`
  - `missions/beyond-de-giorgi/planning-runs/run-002/attacks/chain-02.md`
  - `missions/beyond-de-giorgi/planning-runs/run-002/judgments/chain-02.md`
- [VERIFIED] The older geometry chain already treated "vorticity-direction regularity" as a candidate observable that would need to feed a known threshold statement, not as a new concept. Sources:
  - `missions/beyond-de-giorgi/planning-runs/run-001/selected/chain-03.md`
  - `missions/beyond-de-giorgi/planning-runs/run-001/planner-chains/chain-03.md`

#### What claim boundary that framework earns in the local record

- [VERIFIED] The strongest theorem-level boundary actually stated in-repo is only this: sufficiently regular vorticity direction implies regularity. The repository does not reconstruct the full hypothesis, norm, or proof details of Constantin-Fefferman or later papers. Sources:
  - `missions/beyond-de-giorgi/MISSION.md`
  - `missions/beyond-de-giorgi/planning-runs/run-002/mission-context.md`
- [INFERRED] So the honest benchmark boundary from the local record is broad but real: direction-regularity is already an established conditional regularity framework, but the local corpus does not contain a sharper estimate-level reconstruction beyond that headline.

#### What overlap would make a new claim only a relabeling

- [VERIFIED] The run-001 attack and judgment say the chain risks "repackaging known conditional criteria" unless it produces a genuinely new implication from a specific observable to a known regularity mechanism. Sources:
  - `missions/beyond-de-giorgi/planning-runs/run-001/attacks/chain-03.md`
  - `missions/beyond-de-giorgi/planning-runs/run-001/judgments/chain-03.md`
- [VERIFIED] The refined chain also warns that any route from Beltrami deficit to a known criterion may already pass through stronger `nabla xi`-type control. Sources:
  - `missions/beyond-de-giorgi/planning-runs/run-001/refined/chain-03.md`
  - `missions/beyond-de-giorgi/planning-runs/run-002/selected/chain-02.md`
- [INFERRED] `Forbid novelty claim rule:` if a Step 2 proposal says, in substance, "regularity follows if the vorticity direction is sufficiently regular/coherent," or if it reaches that statement only by smuggling in stronger `xi`-derivative control, then it is not a new ingredient. It is a relabeling of the already named Constantin-Fefferman / direction-coherence framework.

#### What gap remains before this family is mission-live

- [VERIFIED] The mission asks the new branch to answer a different question: can NS dynamics produce or preserve the needed vorticity-direction regularity? Sources:
  - `missions/beyond-de-giorgi/MISSION.md`
  - `missions/beyond-de-giorgi/planning-runs/run-002/mission-context.md`
- [VERIFIED] The refined chain requires any surviving route to control the full stretching mechanism in a fixed representation, not merely state coherence language. Sources:
  - `missions/beyond-de-giorgi/CHAIN.md`
  - `missions/beyond-de-giorgi/planning-runs/run-002/refined/chain-02.md`
- [INFERRED] This family is only live if it adds a new NS-specific bridge from localized direction coherence to full `S omega . omega` control or to a persistence mechanism not already absorbed by the known direction-regularity criteria. Without that bridge, it is benchmark material, not a Step 2 ingredient.

### C. Family 2: Geometric depletion / local Beltrami or alignment

#### What framework already exists in the local corpus

- [VERIFIED] The repository records a strong prior anchor here: exact Beltrami alignment kills the CZ-lossy pressure piece, with `beta_eff -> 1.0`, but the mechanism requires more than 98 percent global alignment and does not survive even 1 percent perturbation. Sources:
  - `missions/beyond-de-giorgi/MISSION.md`
  - `missions/beyond-de-giorgi/planning-runs/run-002/mission-context.md`
- [VERIFIED] The local planning history already proposed "local Beltrami structure near vortex tubes" as a conditional route and tied it to existing geometric criteria rather than presenting it as wholly new terrain. Sources:
  - `missions/beyond-de-giorgi/MISSION.md`
  - `missions/beyond-de-giorgi/planning-runs/run-001/selected/chain-03.md`
  - `missions/beyond-de-giorgi/planning-runs/run-001/planner-chains/chain-03.md`

#### What claim boundary that framework earns in the local record

- [VERIFIED] The exact cancellation boundary in-repo is on the Lamb-vector / pressure-loss side: Beltrami gives `L = omega x u = 0`, so the CZ-loss vanishes in that exact class. Sources:
  - `missions/beyond-de-giorgi/MISSION.md`
  - `missions/beyond-de-giorgi/planning-runs/run-002/mission-context.md`
- [VERIFIED] The planning attack and judgment also make a sharper negative boundary explicit: small local Beltrami deficit controls `u x omega`, not the dangerous stretching term `S omega`, and local tube-core alignment does not remove nonlocal exterior strain. Sources:
  - `missions/beyond-de-giorgi/planning-runs/run-001/attacks/chain-03.md`
  - `missions/beyond-de-giorgi/planning-runs/run-001/judgments/chain-03.md`
  - `missions/beyond-de-giorgi/planning-runs/run-002/judgments/chain-02.md`
- [INFERRED] So the benchmark boundary is sharper here than for direction coherence: the local record already says exact Beltrami buys an exact but fragile cancellation on the wrong target quantity for the geometry route, and local alignment has not yet earned control of full stretching.

#### What overlap would make a new claim only a relabeling

- [VERIFIED] The older geometry-chain critiques say that without a direct Beltrami-to-criterion bridge, the route collapses into known geometric criteria plus tube rhetoric. Sources:
  - `missions/beyond-de-giorgi/planning-runs/run-001/attacks/chain-03.md`
  - `missions/beyond-de-giorgi/planning-runs/run-001/judgments/chain-03.md`
- [VERIFIED] Step 2 planning also warns that if every path from local Beltrami deficit to a known criterion requires stronger `nabla xi`-type control, that is already the obstruction. Sources:
  - `missions/beyond-de-giorgi/planning-runs/run-001/refined/chain-03.md`
  - `missions/beyond-de-giorgi/planning-runs/run-002/selected/chain-02.md`
- [INFERRED] `Forbid novelty claim rule:` no Step 2 claim may call itself new if it does only one of the following:
  - restates exact or near-Beltrami cancellation of the Lamb vector / pressure term,
  - replaces stretching control with alignment language on tube cores,
  - or reaches an existing direction-coherence criterion only by importing stronger `xi`-regularity assumptions.

#### What gap remains before this family is mission-live

- [VERIFIED] The winning chain requires control of full `S omega . omega` in a fixed kernel-level representation, together with a plausible persistence story. Sources:
  - `missions/beyond-de-giorgi/CHAIN.md`
  - `missions/beyond-de-giorgi/planning-runs/run-002/refined/chain-02.md`
- [INFERRED] This family would become live only if it produced a scale-appropriate estimate taking localized Beltrami deficit on a chosen intense-vorticity scenario to the full stretching mechanism, including exterior/nonlocal contributions, rather than only the self-induced or Lamb-vector-looking piece.

### D. Family 3: Tube coherence or persistence

#### What framework already exists in the local corpus

- [VERIFIED] The local mission/planning record repeatedly names tube coherence or persistence as one of the three standing geometry families and as a possible NS-specific ingredient that Tao-style averaging might destroy. Sources:
  - `missions/beyond-de-giorgi/CHAIN.md`
  - `missions/beyond-de-giorgi/planning-runs/run-002/selected/chain-02.md`
  - `missions/beyond-de-giorgi/planning-runs/run-002/refined/chain-02.md`
  - `missions/beyond-de-giorgi/planning-runs/run-001/selected/chain-03.md`
- [VERIFIED] The local corpus does not contain a standalone theorem statement for a tube-persistence regularity criterion. Instead it records the family mainly as a coherent-structure / persistence mechanism that would need to be made explicit. Sources:
  - `missions/beyond-de-giorgi/steps/step-002/REASONING.md`
  - `missions/beyond-de-giorgi/planning-runs/run-001/attacks/chain-03.md`
  - `missions/beyond-de-giorgi/planning-runs/run-001/judgments/chain-03.md`

#### What claim boundary that framework earns in the local record

- [VERIFIED] The run-001 attack says "tube coherence" is dangerous language unless it comes with an explicit transport identity, coercive quantity, or rigorous persistence mechanism. Sources:
  - `missions/beyond-de-giorgi/planning-runs/run-001/attacks/chain-03.md`
- [VERIFIED] The refined chains and judgments move persistence earlier and treat it as the real bottleneck, not a late add-on. Sources:
  - `missions/beyond-de-giorgi/planning-runs/run-002/refined/chain-02.md`
  - `missions/beyond-de-giorgi/planning-runs/run-002/judgments/chain-02.md`
  - `missions/beyond-de-giorgi/planning-runs/run-001/judgments/chain-03.md`
- [INFERRED] So the local claim boundary is weaker than for the other two families: tube persistence is acknowledged as a prior-art-adjacent family of ideas, but in this repository it has not yet earned even a summarized theorem-level conditional criterion. Its current standing is "possible NS-specific persistence mechanism, still operationally undefined."

#### What overlap would make a new claim only a relabeling

- [VERIFIED] The planning attacks warn against "simulation-level intuition" and "suggestive tube language" without a transport law or persistence mechanism. Sources:
  - `missions/beyond-de-giorgi/planning-runs/run-001/attacks/chain-03.md`
  - `missions/beyond-de-giorgi/planning-runs/run-002/attacks/chain-02.md`
- [INFERRED] `Forbid novelty claim rule:` a Step 2 claim is not new if it merely says vortex tubes are coherent, concentrated, or persistent-looking without specifying:
  - what quantity is propagated,
  - on what scenario class and localization,
  - and how that persistence changes the full stretching estimate rather than just the geometry narrative.

#### What gap remains before this family is mission-live

- [VERIFIED] The winning chain requires one or two fixed scenario classes, one localization protocol, and a fixed stretching representation before any route can claim operational leverage. Sources:
  - `missions/beyond-de-giorgi/CHAIN.md`
  - `missions/beyond-de-giorgi/planning-runs/run-002/refined/chain-02.md`
- [INFERRED] Tube persistence remains the least pre-killed family only because its missing ingredient is dynamic rather than static: if a later step could specify a transport/coercive/multiscale persistence mechanism and connect it to full stretching control, it would add something not already contained in the bare static literature summary present here.

### E. Cross-family benchmark verdict

- [VERIFIED] The local judgments insist that Beltrami deficit, `xi`-regularity, and tube persistence must be separated rather than bundled. Sources:
  - `missions/beyond-de-giorgi/planning-runs/run-001/judgments/chain-03.md`
  - `missions/beyond-de-giorgi/planning-runs/run-002/judgments/chain-02.md`
- [INFERRED] Calibrated against the local corpus, the families rank as follows:
  - direction-regularity: strongest prior-art coverage, so highest relabeling risk;
  - local Beltrami / alignment: strongest negative benchmark, because the exact cancellation is already known to be fragile and misaligned with full stretching control;
  - tube persistence: weakest theorem-level local benchmark, but also the most underdefined and therefore not promotable without a concrete transport or persistence mechanism.
- [INFERRED] The pressure-side obstruction memo matters here as the main negative reference point: no static singular-integral, Calderon-Zygmund, or purely local geometry reformulation may be marketed as novel unless it changes the operative term in the target estimate. For Step 2 of this chain, the target estimate is full stretching, not the pressure-side coefficient from the killed branch, but the novelty discipline is the same.

## Preliminary Verdict

- [INFERRED] None of the three families is live as a standalone Step 2 observable on the present local record.
- [INFERRED] Vorticity-direction coherence is already prior-art-calibrated; by itself it is a benchmark target, not a new ingredient.
- [INFERRED] Local Beltrami / alignment is close to pre-killed as a standalone route: the corpus already says it controls the wrong quantity unless a new full-stretching bridge is supplied.
- [INFERRED] Tube coherence / persistence is the only family with any bounded Step 2 value left, but only in a narrow form: as a search for a genuinely NS-specific persistence ingredient or hybrid route, likely `direction coherence + tube persistence`, under a fixed scenario and localization protocol.
- [INFERRED] Bounded Step 2 verdict: the branch still has something worth carrying forward only if Step 2 is framed as a narrow dynamic-hybrid test. If Step 2 instead promotes any static direction-coherence, local alignment, or tube-language claim as already operational, that would merely restate prior-art or repackage the same local-cancellation intuition already judged insufficient.

## Dead Ends / Limits

- [VERIFIED] The repository does not provide full prior-art papers or a geometry-specific factual packet; for several frameworks, especially tube persistence and "later vorticity-direction coherence," the benchmark had to remain at the level the mission/planning corpus actually records. Source:
  - `missions/beyond-de-giorgi/steps/step-002/REASONING.md`
- [VERIFIED] I did not use external literature, per task constraint. That means no theorem details were imported beyond what the local record explicitly names.
- [INFERRED] The benchmark is therefore strongest as a "novelty boundary memo" and weaker as a full mathematical survey of the literature.

# Attack on Selected Chain 03

## Immediate meta-problem

The file `selected/chain-03.md` is titled "Chain 04." That is minor administratively, but it is also a planning smell: the chain is being treated as a distinct route while its identity is already blurred at the labeling level. For a compactness-and-rigidity program, sloppiness about which route is being evaluated is not harmless. It increases the chance that later conclusions quietly pool evidence from neighboring chains.

## Step-by-step critique

### Step 1 - Choose a critical phase space and pre-screen for rigidity

This step is sensible as a screening gate, but it hides the main difficulty inside the screening criterion.

Concrete weaknesses:

- The candidate list (`L^3`, `dot H^{1/2}`, `BMO^{-1}`) mixes spaces with very different compactness, stability, and uniqueness behavior, but the step acts as if "extraction feasibility" is a comparable scalar score. It is not. A space can be good for mild-solution local theory and still be bad for the kind of precompactness modulo symmetry that a critical-element scheme needs.
- The requirement that each candidate come with "one plausible rigidity lever" front-loads the hardest unsolved part. That is not a screening criterion; it is almost the whole problem. In Navier-Stokes, extraction and rigidity are not separable checkboxes.
- `BMO^{-1}` is especially suspect here. It is natural for small-data theory, but as a habitat for a minimal blowup object it is weak, nonlocal, and poorly matched to the kind of pointwise or geometric rigidity mechanisms later advertised.
- `L^3` and `dot H^{1/2}` are more realistic, but the chain does not state what notion of solution is being minimized over, what continuation criterion defines the threshold, or what stability theory is assumed. Without that, "rank realistic candidate spaces" is premature.
- The kill condition is calibrated too aggressively. "No plausible NS-specific rigidity handle" is likely true at the start, but that does not mean the route is worthless. It may still yield a sharp obstruction map. The chain claims to allow that outcome later, yet Step 1 would terminate before any serious obstruction analysis is done.

Fair point:

- Forcing an early confrontation with phase-space choice is good discipline. A critical-element program that is vague about the ambient norm usually dissolves into handwaving.

### Step 2 - Build the minimal-counterexample package

This is the standard move imported from dispersive concentration-compactness, but here the chain understates how much nontrivial machinery is being assumed.

Concrete weaknesses:

- "Formulate the hypothetical minimal blowup object" makes it sound as if the object is available once a space is chosen. In reality, this step may already require a profile decomposition, nonlinear perturbation theory, stability under the chosen topology, and a sharp threshold definition compatible with Navier-Stokes scaling.
- The phrase "normalize symmetries" hides a genuine issue: the symmetry group for Navier-Stokes is not just a technical nuisance. Translation and scaling are manageable in principle, but the pressure and nonlocal interactions make compactness modulo symmetry materially harder than in many semilinear dispersive models.
- "Record what almost-periodicity or concentration properties are needed" risks circularity. Those are not merely bookkeeping outputs; they are often the strongest conclusions of the extraction theorem. If the chain can only say what it wishes were true, the dossier has little evidentiary value.
- The distinction between "already available in the literature" and "missing" is necessary, but the chain does not force precision about theorem hypotheses. A result proved for mild solutions in one class and a rigidity argument stated for suitable weak solutions in another class do not combine automatically.
- The kill condition is underpowered. "Cannot be formulated cleanly" is too weak a standard. A minimal element can often be formulated in a paper sense while still lacking the compactness or regularity features needed for any contradiction argument. This step needs to reject pseudo-formulations, not merely ill-posed ones.

Fair point:

- If the mission were obstruction mapping rather than positive progress, this step could be genuinely useful. It can expose exactly where the analogy with Kenig-Merle style programs breaks.

### Step 3 - Stress-test one rigidity route against Tao's barrier

This is the strongest step conceptually, but it is also where the chain is most likely to collapse.

Concrete weaknesses:

- Choosing only one route creates selection bias. The chain can too easily "find" a surviving route by picking the least falsifiable candidate, or "find" obstruction by picking the weakest route. A serious stress test needs a reason for the selected route, not just a menu.
- The route list is too heterogeneous. Backward uniqueness, Liouville theorems, self-similar rigidity, and geometric concentration laws operate at different regularity levels and require different solution notions. Lumping them together invites false comparisons.
- The instruction to test whether a route uses "exact NS structure rather than only compactness plus harmonic analysis" is right in spirit but vague in practice. Many arguments use the NS equation explicitly while still providing no genuine leverage beyond Tao-preserved structure. The chain needs a sharper criterion than rhetorical NS-specificity.
- Tao's barrier is treated as a binary filter, but the relevant question is quantitative: does the rigidity route exploit a monotone quantity, sign structure, epsilon-regularity mechanism, or unique continuation input that survives the scaling and compactness regime of the minimal element? Without that refinement, the memo may only restate "this still looks too harmonic-analytic."
- The kill condition is again too compressed. A route can fail for reasons other than collapsing to Tao-preserved structure: wrong solution class, no time directionality, non-closedness under limits, incompatibility with almost-periodic scaling, or the need for extra decay that a critical element will not have.

Fair point:

- This is the one place where the chain honestly tries to distinguish genuine equation-specific leverage from generic criticality technology. That is real value.

### Step 4 - Organize any surviving rigidity route into a contradiction program

This step is structurally weaker than it looks, because if Step 3 really succeeded then most of this blueprint should already be visible.

Concrete weaknesses:

- The step assumes "one rigidity route survives" is a meaningful event. In practice, many routes survive only as slogans. Turning them into a contradiction program usually reveals that the surviving route needs a compactness property, decay estimate, or exclusion theorem equivalent in difficulty to the original problem.
- "Keep the dependence on the chosen phase space explicit" is necessary, but it is not enough. The contradiction path also depends on the solution class, normalization, time interval geometry, and what compactness topology is available. The chain is still underspecified.
- The bottleneck lemma requirement is useful, but the blueprint output can be misleadingly optimistic. Naming one bottleneck lemma often hides a stack of subordinate missing inputs.
- The kill condition correctly warns against requiring a theorem as hard as global regularity, but it arrives too late. A disciplined chain should actively test for disguised equivalence much earlier, especially in Steps 2 and 3.

Fair point:

- If any route survives in non-slogan form, packaging it as a contradiction blueprint is the right next move.

### Step 5 - Close with a calibrated global claim

This is a necessary reporting step, but it does not rescue earlier ambiguity.

Concrete weaknesses:

- The chain wants to end with either a positive program or a negative obstruction map, but those are not symmetric outcomes. A "concrete critical-element program" requires much stronger evidence than a "polished negative result." The wording makes it too easy to overstate partial viability.
- The warning against blurring multiple phase spaces or routes is good, but it should have been a standing constraint from Step 1 onward rather than a final cleanup rule.
- There is no explicit instruction to compare the final claim against known concentration-compactness and rigidity programs in Navier-Stokes or adjacent critical PDE. Without that, the chain risks rediscovering a familiar dead end and calling it a new obstruction map.

Fair point:

- Ending with a sharply delimited negative conclusion would still be useful. This chain is more credible as a failure-analysis pipeline than as a discovery pipeline.

## Structural weaknesses of the whole chain

### 1. The chain smuggles in its hardest requirement at the start

The supposed sequence is not really sequential. Step 1 already demands a plausible NS-specific rigidity lever, which is exactly the scarce resource the rest of the chain is supposed to uncover or disprove. Later steps mostly elaborate that same question in different language.

### 2. The chain is biased toward the Kenig-Merle template

That template is powerful, but here it may be more a framing trap than a guide. The chain assumes that if local mechanism hunts fail, the right global object is a minimal blowup profile. That is a substantive bet, not a neutral fallback. Navier-Stokes may resist this style of attack precisely because the available rigidity inputs are too weak or too noncritical to close the loop.

### 3. "NS-specific rigidity" is never operationalized tightly enough

This is the biggest methodological gap. Exact use of the Navier-Stokes equation is not the same as genuine new leverage. Without a concrete criterion such as a non-generic monotonicity, coercive sign structure, limit-stable geometric invariant, or unique continuation mechanism compatible with the critical compactness class, the chain can mistake formal equation dependence for actual progress.

### 4. The kill conditions are inconsistently calibrated

Some kill conditions are too early and may abort before the obstruction is diagnosed; others are too late and allow pseudo-progress to accumulate. The chain needs kill conditions that detect disguised equivalence to the original regularity problem, mismatch of solution classes, and dependence on non-limit-stable inputs.

### 5. The chain underweights solution-class compatibility

This matters throughout. Mild solutions in critical spaces, suitable weak solutions, local energy solutions, and ancient/self-similar limits each support different tools. A compactness argument that crosses these regimes without explicit compatibility checks is fragile.

### 6. The chain may rediscover known failure modes without noticing

A compactness-plus-rigidity route for critical Navier-Stokes has obvious prior-art adjacency. Without an explicit prior-art comparison checkpoint, the chain risks spending several steps to conclude something already broadly understood: extraction can be imagined, but no rigidity input closes the contradiction at critical scaling.

## Bottom line

This chain is stronger as an obstruction-auditing program than as a positive attack plan.

What is genuinely strong:

- It forces early commitment on phase space.
- It does try to separate generic harmonic-analysis technology from truly equation-specific leverage.
- It can produce a useful negative deliverable if run with discipline.

What is weak:

- It treats "find a plausible rigidity handle" as though it were a screening detail rather than the core unsolved obstacle.
- It imports a concentration-compactness template without first justifying that Navier-Stokes has the right rigidity ecology for that template to be more than aspirational.
- Its sequence of steps is partly cosmetic; the same missing ingredient is doing hidden work in Steps 1 through 4.

If this chain is kept, it should be judged almost entirely by the quality of its obstruction map. A positive program should only be credited if it identifies a rigidity mechanism that is not merely Navier-Stokes-flavored in wording, but demonstrably limit-stable, phase-space-compatible, and stronger than the generic structures Tao's barrier already preserves.

# Strategy 002: Attack the 4/3 Barrier

## Objective

Determine whether the De Giorgi recurrence exponent beta = 4/3 can be improved for 3D Navier-Stokes, and if so, produce a concrete improvement. This is the constructive "attack" phase following Strategy 001's "map" phase. The strategy operates on two tracks simultaneously:

**Track A (Obstruction):** Formalize and test the universality of the 4/3 barrier. Can we prove that ANY De Giorgi iteration on a quadratically nonlinear PDE in 3D must have beta <= 4/3? Or can we find a counterexample (another PDE where De Giorgi gives a better exponent)?

**Track B (Construction):** Attack the 1/2 + 5/6 = 4/3 decomposition directly. The 1/2 is from derivative cost (energy definition). The 5/6 is from Sobolev embedding + Chebyshev on nonlinear factors. Can either factor be improved through modified De Giorgi functionals, different embeddings, or structural exploitation?

The two tracks interact: if Track A produces a rigorous obstruction, Track B pivots to "beyond De Giorgi" alternatives. If Track B finds an improvement, Track A's counterexample effort benefits.

## Methodology

### Dual-Track Protocol with Early Branch Detection

**Phase 0: Decomposition Audit (1-2 explorations)**

Before attacking, understand exactly which steps in the De Giorgi argument produce the 1/2 and the 5/6. One exploration reads Vasseur (2007) Proposition 3 line-by-line and produces:

1. A step-by-step derivation showing where each exponent originates
2. For each step: what assumption is used? What structural property of NS is invoked? What is the sharp constant?
3. A "sensitivity table": if step X were improved by delta, what would the final beta become?
4. Identification of "free parameters" — choices in the proof (truncation function shape, Sobolev exponent, interpolation pair) that could be optimized

This exploration produces: (a) a complete map of the 4/3 decomposition with each contribution identified, (b) a ranked list of "most improvable" steps, (c) computable functions for testing improvements numerically.

**Phase 0 gate:** If the decomposition reveals that 1/2 and 5/6 are BOTH sharp (proven optimal, not just unimproved), the strategy pivots to Track A only + mission Step 2C (blow-up investigation).

**Phase 1: Parallel Attack Directions (3-5 explorations, concurrent)**

Based on Phase 0's ranked list, launch targeted attacks on the most improvable steps. The Strategizer selects specific directions based on Phase 0 findings, but the methodology prescribes these TYPES of attack:

**Track A explorations:**
- **Obstruction formalization.** Take the 4/3 decomposition (1/2 + 5/6) and abstract it: what properties of the PDE, the truncation, and the embedding drive each factor? Test on model problems: Burgers (1D quadratic), surface quasi-geostrophic (2D with fractional diffusion), magnetohydrodynamics (3D quadratic but different structure). If De Giorgi gives beta != 4/3 on any of these, the barrier is NOT universal and the difference reveals what NS-specific structure creates it.

**Track B explorations:**
- **Modified energy functional.** The standard U_k = sup ∫ v_k² + ∫∫ |nabla v_k|². Strategy-001 found U_k is NON-MONOTONE in k for some flows. Can a modified functional (e.g., weighted by |omega|, fractional H^s norm, logarithmic correction, Besov-type) improve the 5/6? The key computational test: does the modified functional give a better recurrence exponent on DNS data?
- **Improved Sobolev embedding for div-free fields.** H¹ hookrightarrow L⁶ is sharp for general functions in 3D. But div-free fields satisfy additional constraints. Is there a better embedding? The Coifman-Lions-Meyer-Semmes div-curl lemma gives Hardy space H¹ estimates. Could this improve the interpolation step that produces 5/6?
- **Optimized truncation function.** The standard beta_k(s) = s · min(1, lambda_k/s) is a hard clamp. Could a smooth or optimized truncation function (e.g., tanh-based, or one that preserves more structure of the original field) give a better exponent? Compute beta_eff for alternative truncation functions on DNS data.
- **Local Beltrami conditioning.** Vortex tubes in turbulence are LOCALLY near-Beltrami at their cores. Vasseur's framework already uses localized De Giorgi (on nested balls). A conditional result using the Beltrami deficit RESTRICTED TO THE SUPPORT OF v_k (the high-velocity region) might survive where the global version (E010) failed, because the high-velocity regions in turbulence tend to be vortex cores (high alignment). Compute local Beltrami deficit on support(v_k) across DNS cases.

**Lead Pursuit (0-2 explorations, optional):**
If Phase 1 surfaces promising leads, the Strategizer may run up to 2 additional explorations before Phase 2, provided each is a single-task goal. This is prescribed — do not skip straight to adversarial review if Phase 1 findings open new specific questions.

**Phase 2: Adversarial Review + Synthesis (2-3 explorations)**

1. **Adversarial review.** Stress-test all Track A and Track B claims. Mandatory if any exploration claims beta > 4/3. The adversarial review should specifically check:
   - Is the claimed improvement real or an artifact of the computation?
   - Does the modified functional/embedding/truncation satisfy all the other requirements of the De Giorgi framework?
   - Would the improvement survive in the worst case (near-singular solutions), not just on smooth DNS?

2. **Targeted follow-up on weakest claim** (lesson from Strategy 001). Budget at least 1 exploration after the adversarial review for testing the most vulnerable positive finding.

3. **Final synthesis.** Produces: (a) obstruction theorem or counterexample (Track A verdict), (b) best achieved beta improvement (Track B verdict), (c) mission status assessment.

## Cross-Phase Rules (mandatory for every exploration)

1. **Compute, don't argue.** Every quantitative claim must come from running code with numerical output. This includes testing modified functionals on DNS data, not just arguing that they "should" improve things.

2. **Direction Status Tracker.** The Strategizer maintains a table in REASONING.md:
   ```
   | Direction | Status | Evidence | Exploration |
   ```
   Updated after every exploration. Status: OPEN / PROMISING / CLOSED / EXHAUSTED. This prevents revisiting closed directions and tracks progress.

3. **Sensitivity over generality.** When testing an improvement, compute the SENSITIVITY: if this step is improved by delta, what happens to beta? A modification that improves one step but worsens another is net-negative. Track the full pipeline effect.

4. **Worst-case discipline.** Strategy-001's adversarial review correctly identified that DNS on smooth solutions can't diagnose near-singular behavior. For any claimed improvement, the explorer must ALSO provide the worst-case analytical argument, not just the DNS measurement. "This improves beta_eff on TG at Re=1000" is insufficient. "This improves the analytical bound because step X has a provably better constant by factor Y" is required.

5. **Cite equations precisely.** "Vasseur (2007), Proposition 3, equation (3.14), the step from line 3 to line 4" is the required citation level for any claimed improvement.

6. **Prior code available.** Strategy-001 DNS infrastructure is at `../strategy-001/explorations/exploration-002/code/`. Reuse the solver. Extend, don't rewrite.

7. **One task per exploration.** The meta-learnings are unanimous on this. Never combine "survey the literature" with "run computations" in one exploration.

## Validation Criteria

**Strategy succeeds if:**
- Track A produces either: (a) a rigorous proof that beta <= 4/3 is universal for De Giorgi on quadratic PDEs in 3D, or (b) a counterexample (another PDE where De Giorgi beats 4/3), identifying which structural property of NS creates the barrier
- Track B produces either: (a) a concrete modification to the De Giorgi functional/embedding/truncation that provably improves beta beyond 4/3 (even by epsilon), with both DNS verification and worst-case analytical argument, or (b) exhausts the main attack directions with clean negative results

**Strategy is exhausted if:**
- Phase 0 shows both 1/2 and 5/6 are provably sharp
- Track A produces a rigorous obstruction
- Track B has tested >=3 modification types with clean negatives
- No new leads remain from Phase 1 or lead pursuit

**Success tiers for this strategy:**
- Tier 3: Clean obstruction theorem (4/3 is universal for De Giorgi on quadratic PDEs) — genuine negative result, publishable
- Tier 4: Concrete beta improvement via modified functional/embedding (beta = 4/3 + delta) — breakthrough if achieved
- Tier 5: beta > 3/2 via any modification — would resolve the mission (extremely unlikely)

## Context

### From Strategy 001 (10 explorations, fully reviewed):

**The 4/3 decomposition:**
- 1/2: from ||nabla(beta_k v)||_{L²} <= U_{k-1}^{1/2} (energy definition, likely sharp)
- 5/6: from Sobolev embedding H¹ hookrightarrow L⁶ in 3D + Chebyshev on two velocity factors at truncation level. THIS is the more promising target.
- The decomposition 1/2 + 5/6 = 4/3 appears in BOTH the velocity formulation (via CZ pressure) and the vorticity formulation (via trilinear nonlinearity).

**Closed directions (do not revisit):**
- CZ slack improvement: CZ slack for P_k^{21} is k-independent, tighter than full pressure (1.7-3.9× vs 7.6-17.5×). CLOSED.
- Galilean invariance: pressure Poisson equation is Galilean-invariant for div-free flows. CLOSED.
- Choi-Vasseur (2014) alternative decomposition: achieves only beta = 7/6 (weaker). P_k^{21} bottleneck lives inside their P_{2,k}. CLOSED.
- Global Beltrami conditioning: >98% Beltrami alignment needed for beta > 1. Mechanism doesn't survive even 1% perturbation. CLOSED for global.
- Tran-Yu Galilean program: structurally inapplicable to De Giorgi. CLOSED.

**Open leads:**
- Non-monotonicity of U_k (E002): suggests current d_k² term is suboptimal
- Local Beltrami deficit on support(v_k): untested, might survive where global fails
- Vasseur-Yang (2021) vorticity approach gives 4/3 from different mechanism — might respond differently to modifications
- Post-2007 community moved orthogonally — quantitative regularity methods (profile decomposition, concentration-compactness) might offer different leverage

**Novel claims to carry forward:**
- Claim 2 (universality of 4/3): Strategy 002 Track A directly tests this
- Claim 3 (computational De Giorgi methodology): available infrastructure for Track B testing

### From meta-learnings:
- Test generalization EARLY (don't invest 3 explorations before testing if a mechanism survives perturbation)
- "Adversarial → targeted test" is the strongest quality pattern — budget for it
- Direction status tracking prevents wasted budget on closed paths
- Worst-case analytical arguments are essential — DNS alone is insufficient

## Budget Guidance

Target: 8-14 explorations. Phase 0: 1-2. Phase 1: 3-5 (parallel, split across tracks). Lead pursuit: 0-2. Phase 2: 2-3. Early stopping is appropriate if Track A produces a rigorous obstruction early (beta <= 4/3 is proven universal), in which case remaining budget should go to mission Step 2C (blow-up investigation) or to "beyond De Giorgi" alternatives, at the Strategizer's discretion.

I did not find a file that uses the phrase `harmonic loophole` verbatim. The closest operational match is the untested lead in the H^1 dead-end note: the far-field pressure is described as harmonic on the local cylinder, with oscillation decay via Harnack. The actual bottleneck the library pins down is still the Vasseur \(P_k^{21}\) non-divergence term.

**Most relevant factual material**
- [proposition-3-sharpness-audit.md](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/proposition-3-sharpness-audit.md) is the cleanest equation-first source. It gives the exact arithmetic:
  - \(U_k \le C_p^k (1+\|P\|)U_{k-1}^{\beta_p}\)
  - the bottleneck comes from \(-P_{k21}\,\mathrm{div}(u\,v_k/|u|)\)
  - the pressure factor splits as \(1/2\) from \(\|d_k\|_{L^2}\) and \(5/6\) from the indicator term
  - the combined exponent is \(1/2 + 5/6 = 4/3\), and with the \(q\)-pairing written explicitly it is \(4/3 - 5/(3q)\to 4/3\)
  - this is the exact slot where the obstruction enters: Step 5b of Proposition 3, after the Sobolev/Chebyshev raise and before the recurrence is closed.

- [beta-current-value-four-thirds.md](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/beta-current-value-four-thirds.md) is the compact bottleneck summary:
  - the only term below \(3/2\) is the non-divergence part of \(P_k^{21}\)
  - all other terms sit at \(5/3\)
  - the gap to regularity is \(1/6\), not a perturbative slack issue.

- [h1-pressure-dead-end.md](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/h1-pressure-dead-end.md) is the closest match to the “far-field / harmonic loophole” language:
  - it says the far-field pressure is the sole obstruction
  - local pressure closes
  - \(\|p\|_{H^1}\) is a fixed energy-level constant, so H^1 structure cannot make the far-field pressure \(U_k\)-dependent
  - it also lists an untested lead: far-field \(p_{\mathrm{far}}\) being harmonic on \(Q_k\), with oscillation decay via Harnack.

- [p21-tighter-than-full-pressure.md](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/p21-tighter-than-full-pressure.md) is useful for avoiding a false lead:
  - \(P_k^{21}\) has less CZ slack than the full pressure
  - so constant-factor refinement of CZ is not the way out
  - the bottleneck tensor is already the tightest place in the pressure decomposition.

- [non-cz-pressure-routes-tool-independence.md](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/non-cz-pressure-routes-tool-independence.md) matters because it shows the same \(4/3\) returns under a different mechanism:
  - IBP gives \(1\)
  - H^1/BMO gives \(4/3\)
  - CRW gives \(\le 1\)
  - so the exponent is locked to the NS quadratic structure, not to CZ specifically.

**Tao 2016 material to carry into the follow-up**
- [post-2007-beta-landscape.md](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/post-2007-beta-landscape.md) is the clearest source:
  - it says Tao (2016, JAMS) shows blowup can occur for “averaged NS”
  - the library’s takeaway is that any regularity proof must use the specific algebraic structure of the NS nonlinearity
  - generic energy-level methods, including De Giorgi-on-energy, are therefore structurally insufficient on their own.

- [s2-adversarial-review-beta-four-thirds.md](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/s2-adversarial-review-beta-four-thirds.md) gives the short operational summary:
  - generic methods like De Giorgi on the energy inequality cannot suffice
  - the review explicitly ties this to Tao’s 2016 supercritical barrier.

- [strategy-001-vasseur-pressure-learnings.md](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/meta/missionary/strategy-001-vasseur-pressure-learnings.md) adds the tactical lesson:
  - if a direction depends on whether harmonic analysis alone can improve things, check known obstructions first.

**Meta guidance for a tight equation-first GOAL.md**
- [request-equations-for-construction.md](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/meta/goal-design/request-equations-for-construction.md): ask for derivations, not just conceptual architecture.
- [preload-context-from-prior-work.md](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/meta/goal-design/preload-context-from-prior-work.md): paste the exact formulas and prior findings into the goal so the explorer does not re-research them.
- [specify-rigor-level.md](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/meta/goal-design/specify-rigor-level.md): use theorem-level precision and paper-by-paper verdict style.
- [name-specific-authors-and-papers.md](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/meta/goal-design/name-specific-authors-and-papers.md): name Vasseur 2007, Choi-Vasseur 2014, Vasseur-Yang 2021, Tao 2016, Vasseur 2025, and related Vasseur-school pressure decomposition papers.
- [adversarial-review-needs-complete-parallel-context.md](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/meta/goal-design/adversarial-review-needs-complete-parallel-context.md): if a constructive and adversarial exploration run in parallel, preload the constructive findings into the adversarial goal.
- [allow-analytic-extremizer-over-computation.md](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/meta/goal-design/allow-analytic-extremizer-over-computation.md): if you ask for an optimization check, explicitly allow an analytic extremizer first.
- [use-absolute-file-paths.md](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/meta/goal-design/use-absolute-file-paths.md): use full absolute paths in the goal.

A tight GOAL.md for this follow-up should read like:
- Task: derive the exact pressure pairing in Proposition 3, identify the recurrence slot, and reconstruct the \(1/2 + 5/6 \to 4/3\) arithmetic.
- Constraints: only this task; no broad Navier-Stokes survey; no novelty review unless explicitly needed.
- Context: preload the exact \(P_k^{21}\) formulas and the Tao 2016 averaged-NS obstruction note.
- Output: equation-by-equation derivation, then a short “why Tao matters here” paragraph, then a source table.

**Search log**
- Started from [factual/INDEX.md](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/factual/INDEX.md) and [meta/INDEX.md](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/meta/INDEX.md)
- Followed the Navier-Stokes / vasseur-de-giorgi branch only
- Read the proposition audit, beta summary, H^1 dead-end, non-CZ tool-independence, post-2007 landscape, Tao-adversarial note, and the goal-design entries above
- No library file used the exact phrase `harmonic loophole`; the closest match was the H^1 dead-end note’s untested harmonic far-field lead.

If you want, I can turn this into a ready-to-paste GOAL.md skeleton next.
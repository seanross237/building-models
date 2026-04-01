**Key Findings**

- The local material is strongest on the *operator/cascade scaffold*, not on a full step-by-step proof transcript. The best reconstruction is in the prior Tao-filter exploration report and the Tao paper snippets it extracted: `[REPORT.md](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/instances/far-field-pressure-harmonic-loophole/strategies/strategy-001/explorations/exploration-002/REPORT.md)`.
- The averaged equation layer is clear:
  - ordinary NS bilinear form: `B(u,v) = -(1/2) P[(u·∇)v + (v·∇)u]`
  - averaged operator: `\tilde B` is an average over rotations, dilations, and order-zero Fourier multipliers
  - primitive-variable form: `∂_t u + T(u,u) = Δu - ∇p`, with `-Δp = div T(u,u)`
- The local cascade layer is also clear:
  - Tao first reduces to a local cascade operator built from wave packets `ψ_{i,n}` with dyadic scaling `(1+ε_0)^n`
  - the key “mode” variables in the blowup proof are the 4 scale-local variables `X_{1,n}, X_{2,n}, X_{3,n}, X_{4,n}`
  - energy is concentrated at one scale `n`, then transferred abruptly to `n+1`; `X_{4,n}` is the conduit, `X_{1,n}` carries most energy, and `X_{2,n}, X_{3,n}` are small but dynamically necessary
- The blowup mechanism is not just “generic cascade”; it is a carefully engineered circuit:
  - scalar dyadic model: `\dot X_n = -λ^{2nα} X_n + λ^{n-1} X_{n-1}^2 - λ^n X_n X_{n+1}`
  - the scalar model fails because the transfer to `n+2` interferes too early
  - Tao fixes this by a vector-valued 4-mode circuit built from `pump`, `amplifier`, and `rotor` gates
  - the transfer is delayed and then made abrupt, so scale `n` hands off to `n+1` before `n+1` starts leaking to `n+2`
- The load-bearing averaging ingredients are explicit:
  - the singular Euler symbol lives on `ξ_1 + ξ_2 + ξ_3 = 0`
  - averaging over rotations “smears” that distribution
  - order-zero multipliers and imaginary-order modulation localize the symbol to comparable frequencies
  - dilation averaging is used to place the triad where a nondegeneracy condition holds
  - the base frequencies are normalized to `(0,1,0)`, `(-1,-1,0)`, `(1,0,0)` so `ξ_1^0 + ξ_2^0 + ξ_3^0 = 0`
  - the nondegeneracy coefficient is a sign-sensitive expression of the form `c_{σ1,σ2,σ3} ∼ -(1/8i)(-σ1 + (1/2)σ2 + (1/2)σ1σ2σ3)`, bounded away from zero for small `ε_0`
- The exact cancellations/symmetries Tao relies on are visible in the local cascade construction:
  - energy cancellation: `⟨\tilde B(u,u),u⟩ = 0`
  - symmetry of the structure constants: `α_{i1,i2,i3,μ1,μ2,μ3} = α_{i2,i1,i3,μ2,μ1,μ3}`
  - cancellation condition across the three mode slots: `Σ_{a,b,c} α_{...} = 0`
  - the proof also uses the fact that the averaged operator can be rewritten as an average of transformed copies of the Euler bilinear form after rotation/dilation/Fourier decomposition
- The most relevant prior Atlas notes on the “generic energy + harmonic-analysis methods hit a wall” theme are:
  - `[exploration 001 NS inequality catalog](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/instances/navier-stokes/library-inbox/exploration-001-ns-inequality-catalog.md)`  
    Generic inequalities, energy, Sobolev/GNS, Gronwall, and even the preserved cancellation `⟨(u·∇)u,u⟩=0` are not enough; the averaged NS can still blow up.
  - `[Exploration 005 summary](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/instances/navier-stokes/strategies/strategy-001/explorations/exploration-005/REPORT-SUMMARY.md)`  
    “Tao (2014) is a hard obstruction”: harmonic-analysis-only or Besov/Littlewood-Paley improvements cannot close NS regularity.
  - `[Navier-Stokes history log](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/instances/navier-stokes/strategies/strategy-001/HISTORY-OF-REPORT-SUMMARIES.md)`  
    Same conclusion, stated as a structural limit: any tighter regularity argument must exploit differential NS structure, not just Fourier-multiplier structure.
  - `[Vasseur De Giorgi index](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/INDEX.md)` and `[Tao connection note](/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/post-2007-beta-landscape.md)`  
    Tao is used there as the benchmark that says generic energy-level methods cannot suffice.
- The local library does **not** give a complete, self-contained reconstruction of every circuit coupling from the paper. It gives the operator formulas, the dyadic model, the 4-mode scale packets, the gate language, and the energy-transfer logic. A Phase 0 explorer should still read the paper itself for the exact Section 5/6 circuit wiring, but it will not be starting from scratch.

**What this means for the explorer**

- The explorer can safely separate three layers:
  - averaged operator: `B` vs `\tilde B` vs `T(u,u)`
  - transfer architecture: dyadic `X_n` model and 4-mode `X_{i,n}` circuit
  - blowup mechanism: delayed, abrupt scale-to-scale replication that outruns dissipation
- The explorer should not waste time asking for a vague “more cancellation” story. The concrete questions already visible in the local material are:
  - which exact local NS structure is destroyed when `u·∇u` is replaced by an averaged pseudodifferential interaction?
  - which part of the cascade needs pre-Poisson locality, not just post-Poisson harmonicity?
  - which of Tao’s cancellations are structural, and which are merely preserved by the averaging?
- The strongest current library conclusion is negative in spirit: Tao shows that harmonic-analysis-only structure is too weak. What remains open is whether exact NS has a specific locality/cancellation relation that Tao’s averaging erases and that could serve as a real firewall.

**Meta Guidance for `GOAL.md`**

- Use equation-first prompts with explicit slots for:
  - `B(u,v)`
  - `\tilde B`
  - `T(u,u)`
  - the dyadic ODE `X_n`
  - the 4-mode variables `X_{1,n},...,X_{4,n}`
  - the transfer identity and the nondegeneracy condition
- Require the explorer to label each statement as:
  - sourced formula
  - direct deduction
  - provisional inference
- Add a hard failure path:
  - if the mechanism cannot be reconstructed to the level of the cascade variables and transfer rules, stop and report reconstruction failure
- Include a notation-reconciliation warning before falsification:
  - do not test the wrong pressure object or the wrong split just because the notation changed
- Ask for a compact table with exactly these columns:
  - Tao step
  - local operator / variable
  - what averaging changes
  - what exact NS structure would be needed
  - status: clear / inferred / unknown
- Avoid vague phrasing like “more cancellation” or “extra regularity.” Require the explorer to name the precise symmetry, locality relation, or triadic constraint it thinks is load-bearing.

**Search Log**

- Checked factual Navier-Stokes index and Vasseur subindex for Tao-adjacent notes.
- Read the mission and strategy files for `anatomy-of-averaged-ns-blowup-firewall`.
- Read the prior Tao-filter reconstruction report and summary.
- Read the Navier-Stokes literature survey notes that explicitly mark Tao as the limit of generic energy/harmonic-analysis methods.
- Read the meta guidance on notation reconciliation and goal design.
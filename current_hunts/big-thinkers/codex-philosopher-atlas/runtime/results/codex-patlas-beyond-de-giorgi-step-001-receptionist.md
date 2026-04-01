**Most relevant prior materials**
- [`missions/vasseur-pressure/library-inbox/exploration-002-pressure-dissection-de-giorgi.md`]( /Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/vasseur-pressure/library-inbox/exploration-002-pressure-dissection-de-giorgi.md#L101-L143 ) gives the exact De Giorgi pressure pairing, including the main bad term `2∫∫ p v_k φ_k (ê·∇φ_k)` and the `2^k` cutoff loss.
- [`missions/navier-stokes/library-inbox/vasseur-2007-proof-architecture.md`]( /Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/navier-stokes/library-inbox/vasseur-2007-proof-architecture.md#L157-L182 ) gives the clean decomposition `P = P_k^1 + P_k^2`, with `P_k^1` harmonic/nonlocal and the actual pressure obstruction sitting in `P_k^{21}`, which saturates at exponent `4/3`.
- [`missions/vasseur-pressure/steps/step-001/RESULTS.md`]( /Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/vasseur-pressure/steps/step-001/RESULTS.md#L23-L38 ) is the best local summary of the pressure bottleneck: local pressure closes, far-field pressure is the sole obstruction, and Bogovskii localization is worse than the original problem.
- [`missions/vasseur-pressure/steps/step-002/RESULTS.md`]( /Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/vasseur-pressure/steps/step-002/RESULTS.md#L11-L21 ) is the key negative result for H^1-BMO: `W^{1,2} ↛ BMO`, global `H^1` stays at the fixed energy constant `E_0`, and localization destroys `H^1`.
- [`missions/beyond-de-giorgi/CHAIN.md`]( /Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/CHAIN.md#L28-L34 ) and [`missions/beyond-de-giorgi/planning-runs/run-001/mission-context.md`]( /Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/planning-runs/run-001/mission-context.md#L30-L44 ) are the main Tao-gate materials: they define what counts as an NS-specific ingredient versus generic harmonic analysis.
- [`missions/beyond-de-giorgi/planning-runs/run-001/attacks/chain-01.md`]( /Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/planning-runs/run-001/attacks/chain-01.md#L15-L21 ) is the sharpest note on the surviving harmonic-tail loophole and the need to quotient out already-killed modes before any gain claim.
- [`missions/navier-stokes/CHAIN-HISTORY.md`]( /Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/navier-stokes/CHAIN-HISTORY.md#L9-L13 ) gives the broader candidate-family context: vorticity alignment and pressure estimates were already flagged as structurally interesting.

**Concrete findings**
1. The surviving far-field pressure object from `vasseur-pressure` is the pairing against the cutoff gradient:
   `I_p^{far}` is the term that behaves like `∫∫ p v_k φ_k (ê·∇φ_k)`, and the prior planning memo records it in the form `I_p^far <= C_far 2^{12k/5} U_k^{6/5}` with `C_far ~ ||u||_{L^2}^2 / r_k^3`. The important point is not the `U_k` exponent anymore; it is that `C_far` is still a fixed energy-class constant.

2. On harmonic modes, the repository’s planning language is deliberately conservative: before any gain is claimed, constants, affine pieces, and other low-order harmonic modes should be treated as already quotiented out by the test/localization structure. What still matters is the actual exterior harmonic tail entering the bad pairing, not a prettier harmonic-polynomial remainder. In the earlier Vasseur decomposition, the analogous surviving pressure-side obstruction is the `P_k^{21}` piece, not the harmonic `P_k^1` piece.

3. The earlier `vasseur-pressure` work already tells you what is dead and what is not:
   - local pressure closes with `U_k^{8/5}` and is not the bottleneck,
   - far-field pressure is the sole obstruction at the De Giorgi level,
   - Bogovskii localization makes things worse,
   - H^1-BMO, atomic, and interpolation routes do not improve the recursion.
   So the only plausible remaining gain would have to come from a genuinely NS-specific effect on the far-field coefficient itself, not from harmonic regularity alone.

4. For Tao screening, the repository’s own filter is clear: energy identity, div-free, and all standard harmonic-analysis structure are preserved by the averaged model, so anything depending only on those is disqualified. The candidate NS-specific ingredients already named locally are:
   - the exact algebraic form of `u·∇u`,
   - vorticity stretching / strain alignment,
   - local Beltrami or near-Beltrami structure,
   - pressure-Hessian identities tied to `∂_i∂_j p = R_i R_j(u_i u_j)`.
   Those are the right things to test against Tao’s averaging. Pure harmonic tail smoothing is Tao-compatible, so it is not enough by itself.

5. The broader mission context also points to the same shortlist of structural leads: harmonic far-field pressure, profile decomposition / critical element ideas, geometric vorticity criteria, Lorentz-space De Giorgi, and local Beltrami structure. Of these, only the geometry/algebra items look likely to survive Tao’s filter.

**Confidence**
- High on the pressure decomposition, the far-field obstruction, and the H^1-BMO dead end.
- High on the Tao filter criteria as recorded in the local mission context.
- Moderate on the exact “which harmonic modes are killed” phrasing, because the repository frames that at planning level rather than as a fully formal theorem.

I also appended the requested search log to [`runtime/logs/codex-patlas-beyond-de-giorgi-step-001-receptionist-search.md`]( /Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/runtime/logs/codex-patlas-beyond-de-giorgi-step-001-receptionist-search.md ).
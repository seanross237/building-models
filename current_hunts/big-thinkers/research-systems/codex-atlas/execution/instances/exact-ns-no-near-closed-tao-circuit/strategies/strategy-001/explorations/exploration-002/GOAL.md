<!-- explorer-type: math-explorer -->

# Exploration 002: Exact Interaction Audit for a Minimal Helical Support

## Goal

Choose one explicit minimal helical support for the preferred Phase 0 definition and write the exact desired-vs-leakage interaction ledger.

This is the Phase 1 exact interaction audit. It is not a broad helical-triad survey. It must end with one explicit minimal configuration, unless an adversarial leakage-suppression arrangement is genuinely inequivalent and needed for the cheap counterexample screen.

## Decision Target

State one decision target first:

```text
Either there exists a concrete minimal support (K,σ) whose exact helical amplitude
equations realize all Tao target monomials and can therefore be stress-tested in Phase 2,
or even the static support/triad geometry already fails before any dynamical test.
```

## Preloaded Context

Read first:

- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/instances/exact-ns-no-near-closed-tao-circuit/strategies/strategy-001/explorations/exploration-001/REPORT.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/instances/exact-ns-no-near-closed-tao-circuit/strategies/strategy-001/explorations/exploration-001/REPORT-SUMMARY.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/runtime/results/codex-atlas-standalone-20260331T175433Z-receptionist-96805.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/factual/navier-stokes/tao-averaged-ns-delayed-transfer-circuit.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/factual/navier-stokes/exact-ns-triadic-coefficient-rigidity.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/factual/navier-stokes/exact-ns-unavoidable-spectator-couplings.md`

The receptionist already established:

1. the local library has no actual `(K,σ)` support-selection atlas,
2. mirror/conjugate closure is mandatory,
3. there is no local helical sign-pattern catalog for leakage suppression.

So use primary sources immediately for exact helical triad geometry and coefficient structure. Do not spend time pretending the local library already chose the support.

## Preferred Phase 0 Object To Audit

Use the preferred definition from exploration 001:

- five distinguished amplitudes `a1,...,a5`,
- desired monomials

```text
a1^2 -> a2,
a1^2 -> a3,
a2 a3 -> a3,
a1 a3 -> a4,
a3 a4 -> a1,
a4^2 -> a5,
```

- leakage split

```text
∂t aj = Fj^des + Fj^int-leak + Fj^ext-leak - ν|kj|^2 aj.
```

## Required Deliverables

Your `REPORT.md` and `REPORT-SUMMARY.md` must provide:

1. One explicit minimal support `(K,σ)` for the five Tao roles.
2. One adversarial alternative support or helicity arrangement designed to suppress leakage, if genuinely different.
3. The exact helical amplitude equations for `a1,...,a5` on the chosen support, including all terms forced by:
   - triad closure,
   - conjugate / mirror closure,
   - any third legs that remain inside the minimal active set.
4. An interaction ledger table with columns:
   - target equation,
   - source monomial / triad,
   - exact coefficient or structural coefficient form,
   - desired / spectator / forbidden,
   - tunable vs rigid,
   - relevance to leakage.
5. A sharp verdict on the minimal configuration:
   - `viable for Phase 2`,
   - or `already killed statically`.
6. If the configuration fails, say exactly where:
   - triad geometry,
   - mirror-mode closure,
   - coefficient/sign mismatch,
   - or support explosion.

## Required Discipline

- One minimal configuration first, then one adversarial alternative only if needed.
- Use the exact helical NS law, not a shell toy model in disguise.
- Keep the distinction explicit between:
  - desired channels,
  - spectator channels internal to the active support,
  - channels that force activation of external modes.
- If you use symbolic or numerical assistance, save it under `code/` and make the ledger reproducible.
- Do not claim a quantitative obstruction yet unless it already follows at the static-ledger stage.

## Helpful Questions

Use these as a checklist:

1. Can one five-role support even realize all six desired monomials under exact triad closure?
2. What extra modes are forced immediately by real-valuedness or by the third-leg closure of the desired triads?
3. Which desired coefficients are rigid once `(K,σ)` is fixed, and which can still be tuned by geometry?
4. Is there any helicity assignment that suppresses the most dangerous spectators without killing the desired monomials?
5. Does the minimal support stay finite and intelligible, or does it instantly enlarge beyond the intended circuit?

## Output Format

Write:

1. `REPORT.md`
2. `REPORT-SUMMARY.md`

Structure `REPORT.md` as:

1. Executive verdict
2. Chosen minimal support and rationale
3. Exact helical interaction equations
4. Desired-vs-leakage ledger
5. Adversarial support check
6. Phase 2 recommendation

Tag substantial statements as `[VERIFIED]`, `[CHECKED]`, `[COMPUTED]`, or `[CONJECTURED]`.

## Failure Mode To Avoid

Do not answer with "many extra couplings appear." The report must say exactly which couplings appear, how, and whether they are rigid, tunable, internal leakage, or support-breaking external leakage.

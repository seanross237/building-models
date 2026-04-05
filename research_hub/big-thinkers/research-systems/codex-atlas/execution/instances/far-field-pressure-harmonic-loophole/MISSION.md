# Mission: Far-Field Pressure Harmonic Loophole — Tao-Filtered Falsification

## Background

Three prior missions have systematically closed the known approaches to NS regularity:

1. **De Giorgi framework exhausted** (Atlas VP, 18 explorations): `beta = 4/3` is rigorously sharp. All four proof steps individually tight. Tool-independent (CZ, IBP, H^1/BMO, CRW all give `beta <= 4/3`). One-line extremizer: `u = (c,0,0)`. Universal formula: `beta = 1 + s/n`.

2. **Epsilon-regularity family exhausted** (Patlas NS, Step 1): CKN, Lin, and Vasseur all reduce to the same covering argument with the same scaling exponents. The `dim <= 1` singular set bound is forced by `E(r)` scale-invariance plus global energy bound. Not a proof artifact; structural.

3. **H^1 pressure route dead** (Patlas VP, 4 explorations): `W^{1,3}` wall. Local pressure closes (`delta = 3/5 > 0`). Far-field pressure is the sole obstruction. Bogovskii corrector is strictly worse (`2^{2k}` growth).

4. **Tao constraint (2016):** Methods using only energy identity plus harmonic analysis cannot resolve NS regularity. Blowup exists for averaged NS preserving all standard analytical structure. The proof must use a property that averaging destroys.

The one surviving lead: Patlas VP identified but never tested that `p_far` is harmonic on `Q_k` with oscillation decaying exponentially via Harnack. A local `H^1` norm of `p_far` could be much smaller than the global `H^1` norm. This works outside De Giorgi by exploiting harmonicity, a pointwise structural property rather than a norm estimate.

The question this mission answers: does the harmonicity of `p_far` provide a genuine beyond-De-Giorgi escape from the `beta = 4/3` barrier, or is it Tao-compatible and therefore unable to help?

## Mission Structure (Falsification-First)

### Step 1: Reconstruct the exact far-field obstruction

Reconstruct from Patlas VP and Atlas VP findings the precise mathematical object that blocks progress:

- the far-field pressure pairing: `∫∫ p_far · ψ_k dx dt`
- why its coefficient is `O(E_0)` — fixed, not `U_k`-dependent
- the specific term in the De Giorgi recurrence where this enters
- the exact exponent arithmetic showing how this term limits `beta` to `4/3`

Deliverable: a self-contained one-page mathematical statement of the obstruction, with equation numbers, suitable for applying the Tao filter.

Kill condition: if the obstruction cannot be precisely stated in equations, stop. Vague obstructions cannot be falsified.

### Step 2: Apply the Tao filter

Take the reconstructed obstruction and ask whether Tao's averaged NS has the same far-field pressure structure.

Specifically:

- in Tao's construction, the nonlinearity `u·∇u` is replaced by an averaged version; what happens to `-Δp = ∂_i ∂_j (u_i u_j)` under this averaging?
- is the far-field pressure of the averaged equation still harmonic on `Q_k`?
- does Harnack decay still apply?
- is the local `H^1` norm of `p_far` still potentially smaller than global?

Three outcomes:

- Tao-compatible: the averaged equation has the same harmonic far-field pressure structure, so the loophole cannot help; proceed directly to Step 5 as a negative result.
- Tao-incompatible: averaging destroys the harmonic structure, so the loophole might help; proceed to Step 3.
- Unclear: compatibility cannot be determined cleanly; design a computational or model test to distinguish.

Kill condition: if Tao-compatible, skip Steps 3-4 and write the negative result.

### Step 3: Build a falsification model

Only reached if Step 2 says Tao-incompatible.

Construct the simplest explicit model where:

- the far-field pressure is harmonic, as in real NS
- the local `H^1` norm of `p_far` is smaller than global
- test whether this actually makes the pressure pairing `U_k`-dependent

This is not "assume it works and see what happens." Build the simplest possible system with the harmonic far-field property and check whether the pressure coefficient actually improves.

Deliverable: either an explicit estimate showing the pressure pairing gains `U_k`-dependence from harmonicity, or an explicit construction showing that it does not and the coefficient stays `O(E_0)`.

Kill condition: if the coefficient stays `O(E_0)` even with harmonicity fully exploited, the loophole is closed. Proceed to Step 5.

### Step 4: Quantitative criterion

Only reached if Step 3 shows a genuine gain.

Convert the gain into a direct quantitative improvement:

- does the improved pressure pairing change `beta`, and to what value?
- if `beta` improves but stays below `3/2`, how much of the gap does it close?
- can the improvement be stated as a concrete inequality that could feed into Vasseur's Conjecture 14 framework?
- does the improvement require any regularity beyond Leray-Hopf (`W^{1,2}`)?

Critical check: verify the improvement is not just a rewriting of the same estimate in different notation. Compare the new bound term-by-term against the original. The gain must appear as a strictly smaller constant or a `U_k`-dependent factor where there was previously a fixed constant.

Kill condition: if the "improvement" is equivalent to the original estimate under a change of variables or rearrangement, it is notational rather than real. Close with the negative result.

### Step 5: Final report

One of two outcomes:

Negative (most likely): the far-field pressure harmonic loophole is Tao-compatible, or does not produce a `U_k`-dependent coefficient, or is notational rather than structural. The last identified lead from the De Giorgi obstruction mapping is closed. Progress toward NS regularity requires methods that do not pass through pressure estimates in the De Giorgi / epsilon-regularity family.

Positive (unlikely but transformative): harmonicity of `p_far` produces a specific quantitative gain, this gain is Tao-incompatible, the improved exponent is `beta = [value]`, and the next mission should pursue a sharply defined follow-up.

Either outcome should be clean and publishable.

## What Must Be Avoided

- Do not re-derive the `beta = 4/3` sharpness. It is already proven; cite Atlas VP.
- Do not re-test `H^1` routes. They are dead; cite Patlas VP.
- Do not attempt generic modifications to De Giorgi iteration. The framework is exhausted.
- Do not confuse "the far-field pressure is harmonic" with "we can bound the pressure in a better function space." The question is whether harmonicity gives pointwise control that norms miss.
- Do not propose a new proof architecture. This mission tests one specific loophole.

## Budget

4-6 explorations. This is a focused falsification rather than a landscape survey.

Most likely path:

- Step 1: 1 exploration
- Step 2: 1 exploration
- Step 5 folded into the synthesis of Step 2

Expected total for the negative result path: 2-3 explorations.

## Connection to Prior Work

Direct successor to:

- Patlas `vasseur-pressure` `MISSION-COMPLETE.md` — source of the harmonic `p_far` lead
- Atlas `vasseur-pressure` strategies 1 and 2 — source of `beta = 4/3` sharpness, tool-independence, universal formula
- Patlas `navier-stokes` Step 1 — source of epsilon-regularity universality
- Tao (2016), `arXiv:1402.0290` — the filter

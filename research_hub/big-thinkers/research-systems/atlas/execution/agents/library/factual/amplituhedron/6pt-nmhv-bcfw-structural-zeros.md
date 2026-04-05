---
topic: Structural vanishing of BCFW channels in 6-point NMHV
confidence: verified
date: 2026-03-27
source: amplituhedron strategy-001 exploration-002
---

## Finding

For A₆(1⁻,2⁻,3⁻,4⁺,5⁺,6⁺) in N=4 SYM, two sets of BCFW channels vanish for structural (not numerical) reasons.

---

## Result 1: [1,2⟩ Shift — Channel 3 is Exactly Zero

Under the [1,2⟩ shift, three factorization channels arise:
- Ch1: {1̂,6} | {2̂,3,4,5}
- Ch2: {1̂,6,5} | {2̂,3,4}
- Ch3: {1̂,6,5,4} | {2̂,3} ← **ZERO**

**Why Channel 3 vanishes:** At the Ch3 pole z₃* = [23]/[13] (from [2̂3]=0), the internal momentum K = p̂₁+p₄+p₅+p₆ has its angle spinor λ_K proportional to −λ_{1̂}, verified to machine precision:
```
K.lam / 1^.lam ratio (0): -1.000000+0.000000j
K.lam / 1^.lam ratio (1): -1.000000+0.000000j
```

**Consequence:** ⟨K, 1̂⟩ = 0 → the Parke-Taylor numerator ⟨K,1̂⟩⁴ = 0 for A₅^MHV(K⁻,1̂⁻,6⁺,5⁺,4⁺).

**Physical reason:** At the [2̂3]=0 pole, K = -(p̂₂+p₃) and becomes a rank-1 outer product at the residue with its dominant column proportional to λ_{1̂}. This is a structural consequence of the kinematics, not a numerical accident.

**Status: [VERIFIED]** — numerically confirmed across 3 kinematic seed values (seed=42,137,999).

---

## Result 2: [3,4⟩ Shift — All Three Channels Vanish

For the [3,4⟩ shift (h₃=−1, h₄=+1), all three factorization channels are exactly zero for independent structural reasons:

| Channel | Left sector | Right sector | Why zero |
|---------|-------------|--------------|----------|
| Ch A: {3̂,2} \| {4̂,5,6,1} | A₃ on left | A₅ on right | ⟨3̂2⟩=0 at pole → Parke-Taylor numerator zero; alternate A₃^aMHV needs 2 positive helicities but left has 2 negatives |
| Ch B: {3̂,2,1} \| {4̂,5,6} | A₄ on left | A₄ on right | Left A₄ has 3 negative helicities — vanishes by SWI (Supersymmetric Ward Identity) for gluons |
| Ch C: {3̂,2,1,6} \| {4̂,5} | A₅ on left | A₃ on right | [4̂5]=0 at right pole → A₃^aMHV numerator [4̂5]³ = 0 |

**Consequence:** The [3,4⟩ shift contributes zero from all finite poles. Either (a) this shift has a non-vanishing boundary term at z→∞ (suggesting the amplitude grows under this shift), or (b) the [1,2⟩ BCFW result is incorrect.

**Status: [VERIFIED]** for each individual channel vanishing; **[CONJECTURED]** regarding the overall implication about boundary terms.

---

## Significance

- The channel 3 structural zero under [1,2⟩ shift reduces the 6-point NMHV computation to only 2 non-trivial channels (Ch1 and Ch2).
- The [3,4⟩ all-zero result is a useful sanity check: any correct BCFW implementation must give these zeros, making it a diagnostic for bugs.
- For [1,2⟩ shift, Ch1 pole uses A₃^aMHV with λ_K = λ₆ (verified: K ∝ particle 6 at Ch1 pole).

## Supporting Data

6-particle kinematics via "3+3 balanced" construction (cluster 1: {1,2,3} with total K; cluster 2: {4,5,6} summing to −K) verified massless to 10⁻¹⁶ across seeds 42, 137, 999. Code: `code/kinematics_6pt.py`.

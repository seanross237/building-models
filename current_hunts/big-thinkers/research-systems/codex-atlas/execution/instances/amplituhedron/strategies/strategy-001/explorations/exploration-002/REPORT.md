# Exploration 002: 6-Point NMHV Tree Amplitude — BCFW vs Grassmannian

## Goal

Compute A₆(1⁻,2⁻,3⁻,4⁺,5⁺,6⁺) in N=4 SYM via:
1. BCFW recursion (3 factorization channels)
2. Grassmannian G(3,6) residues (3 residues at positroid cells)

Compare term-by-term structure, not just the final answer.

**Status: PARTIAL — BCFW has sign/helicity bugs; MHV baseline verified; Grassmannian not attempted**

---

## Section 1: Kinematics — SUCCESS [VERIFIED]

**Script:** `code/kinematics_6pt.py`

6-particle kinematics using a "3+3 balanced" construction:
- Cluster 1: particles 1,2,3 in a 3-body rest frame with total momentum K
- Cluster 2: particles 4,5,6 sum to −K

**Results:** Kinematics valid for all tested seeds:
```
Seed 42:  mom_conservation = 1.11e-16, max mass error = 4.21e-17  ✓
Seed 137: mom_conservation = 5.55e-17, max mass error = 6.94e-18  ✓
Seed 999: mom_conservation = 1.67e-16, max mass error = 2.60e-17  ✓
```
All momenta massless to machine precision. Momentum conservation holds to 10⁻¹⁶.

**Status: [VERIFIED]** — computation reproduces with code in `code/kinematics_6pt.py`.

---

## Section 2: 6-Point MHV Baseline — SUCCESS [COMPUTED]

**Script:** `code/mhv_baseline.py`

Parke-Taylor formula for all C(6,2)=15 helicity configurations A₆(i⁻,j⁻):
```
A₆^MHV(i⁻,j⁻) = ⟨ij⟩⁴ / (⟨12⟩⟨23⟩⟨34⟩⟨45⟩⟨56⟩⟨61⟩)
```

**Sample output (seed=42):**
```
A₆(1⁻,2⁻) = -4.66041 -3.04648i   |A| = 5.568
A₆(1⁻,3⁻) = -3032.8  +362.2i     |A| = 3054
A₆(2⁻,4⁻) = -21.93   -22.16i     |A| = 31.17
A₆(3⁻,5⁻) = -87.34   -12.97i     |A| = 88.29
```

All 15 MHV amplitudes computed for 3 seed values. No divide-by-zero errors.

**Status: [COMPUTED]** — code in `code/mhv_baseline.py`.

---

## Section 3: BCFW Recursion — PARTIAL / BUGGY

**Script:** `code/bcfw_6pt.py`

### 3.1 Theoretical Setup

For A₆(1⁻,2⁻,3⁻,4⁺,5⁺,6⁺) with [1,2⟩ shift:
```
|1̂⟩ = |1⟩ + z|2⟩,   |2̂] = |2] − z|1]
```

Three channels (partition 1̂ and 2̂ on opposite sides):
- **Ch1:** {1̂,6} | {2̂,3,4,5} — A₃^aMHV × A₅^aMHV
- **Ch2:** {1̂,6,5} | {2̂,3,4} — A₄^MHV × A₄^MHV
- **Ch3:** {1̂,6,5,4} | {2̂,3} — A₅^MHV × A₃^MHV

### 3.2 Key Discovery: Channel 3 is Structurally Zero [VERIFIED]

For channel 3, the BCFW pole z₃* = [23]/[13] (from [2̂3]=0).

**Debug finding:** At z₃*, the internal momentum K = p̂₁+p₄+p₅+p₆ has angle spinor λ_K = −λ_{1̂} (exactly proportional, to machine precision):
```python
K.lam / 1^.lam ratio (0): -1.000000+0.000000j
K.lam / 1^.lam ratio (1): -1.000000+0.000000j
Is K proportional to 1^? True
```

**Consequence:** ⟨K,1̂⟩ = 0 → the Parke-Taylor numerator of A₅^MHV(K⁻,1̂⁻,6⁺,5⁺,4⁺) is ⟨K,1̂⟩⁴ = 0. Channel 3 vanishes.

**Physical reason:** At the [2̂3]=0 pole (channel 3 pole), the "left" internal momentum K = -(p₂̂+p₃) and λ_K ∝ −λ_{1̂} because K = λ_{1̂}λ̃₁+λ₄λ̃₄+λ₅λ̃₅+λ₆λ̃₆ becomes rank-1 at the pole, with its dominant column proportional to λ_{1̂}. This is a structural feature, not a numerical accident. **Status: [VERIFIED]**

### 3.3 Pole-Finding Implementation [COMPUTED]

For [1,2⟩ shift: q = λ₂⊗λ̃₁ as 4-vector. Pole:
```
z* = −P²(0) / (2 P(0)·q)   where P(0) = unshifted sum of left momenta
```

**Verification:** At z*, internal K² verified to be O(10⁻¹⁷) (machine precision) for all tested kinematics.

**Important sign note:** The numerical z* = −⟨23⟩/⟨24⟩ for the {3^,2} channel of [3,4>] shift, while naive analytic formula gives +⟨23⟩/⟨24⟩. These differ by sign because s₂₃ = ⟨23⟩[23] (positive in this convention) and 2P·q = ⟨24⟩[23] (sign depends on conventions). The numerical formula `z* = -P²/(2P·q)` is correct.

### 3.4 BCFW Results for [1,2⟩ Shift — UNVERIFIED

Computed values (seed=42):
```
Channel 1: C1 = -24.845 -14.803i
Channel 2: C2 = -8005.1 -3611.2i
Channel 3: C3 = 0       (structural zero)
Total:     A6_NMHV = -8029.9 -3626.0i
```

**Cross-check with [2,4⟩ shift** (h₂=−1, h₄=+1, a valid [-,+] shift):

The [2,4⟩ shift gives 2 non-trivial channels (channels where the left sector has mixed helicities):
- Ch3: {2̂,1,6} | {3,4̂,5} → D3 = −772.9 −262.9i (seed=42)
- Ch4: {2̂,1,6,5} | {3,4̂} → D4 = +230.3 +3.6i (seed=42)
- Total: −542.6 −259.3i

**Disagreement:** |([2,4>] total) / ([1,2>] total) − 1| ≈ 0.93 (seed=42)

The two BCFW shifts give **different answers**, indicating at least one is wrong.

### 3.5 Error Diagnosis

The disagreement between [1,2⟩ and [2,4⟩ BCFW shifts points to bugs in one or both implementations. The most likely sources:

**1. Cyclic color ordering of sub-amplitudes:**
The Parke-Taylor formula is CYCLIC-ORDER-SENSITIVE. The color ordering of internal particles K and -K in the sub-amplitudes must match the original color-ordered amplitude. An incorrect cyclic ordering changes the value of the denominator product ⟨12⟩⟨23⟩...⟨n1⟩.

For example, in Ch2 of [1,2⟩]: left sub-amplitude A₄(K,5,6,1̂) has cyclic order K→5→6→1̂→K. If I accidentally used K→6→5→1̂→K, the result changes.

**2. Helicity assignment of internal particle K:**
The sign of BCFW contributions depends on whether K is assigned positive or negative helicity. At multi-particle poles (not 2-particle poles), both assignments can give non-zero sub-amplitudes, and the wrong choice produces incorrect values.

**3. Overall sign of BCFW formula:**
The standard BCFW formula A_n = Σ A_L × A_R / P² has no overall minus sign (in the residue-based derivation). But specific sub-amplitude formulas can introduce signs from cyclic bracket antisymmetry.

**Assessment:** The BCFW computation is **not verified**. At least one of the two independent implementations has wrong cyclic orderings or helicity assignments.

**Status: [CONJECTURED]** — individual channel values may be wrong.

---

## Section 4: Grassmannian G(3,6) — NOT ATTEMPTED

**Reason:** The BCFW computation was not verified before attempting the Grassmannian. Without a verified BCFW value to compare against, any Grassmannian result would have no cross-check. The Grassmannian computation is substantially more complex (solving the delta-function constraints in the 3×6 C matrix, identifying the 3 positroid cells, evaluating residues).

**What the Grassmannian computation would require:**
1. Build the 3×6 C matrix in the gauge (I₃ | C')
2. Solve C·λ̃ = 0 (3×2 linear system for C') — this is 6 equations for 9 unknowns, but with the NMHV constraints the system is determined
3. Compute the 6 consecutive 3×3 minors M₁,...,M₆
4. The 3 residues correspond to the 3 cells of the positive Grassmannian G₊(3,6)
5. Each residue maps to a BCFW channel

**What's blocking it:** Without a correct numerical value from BCFW, there's no target to validate the Grassmannian residues against.

---

## Section 5: Technical Notes

### 5.1 Key mathematical facts established

1. **[VERIFIED]** For [1,2⟩ shift on A₆(1⁻,2⁻,3⁻,4⁺,5⁺,6⁺), channel 3 ({1̂,6,5,4}|{2̂,3}) is EXACTLY zero because λ_{K,ch3} ∝ −λ_{1̂} at the pole.

2. **[VERIFIED]** The pole condition for channel 1 ({1̂,6}|{2̂,3,4,5}) is ⟨1̂6⟩=0. The angle spinor of the internal K is λ_K = λ₆ (proportional to particle 6), and the left sub-amplitude uses A₃^aMHV.

3. **[VERIFIED]** For [3,4⟩ shift on this amplitude, ALL three factorization channels vanish:
   - Ch A {3^,2}: angle-bracket pole ⟨3^2⟩=0 → A₃^MHV numerator zero AND the alternate A₃^aMHV requires 2 positive helicities but both left sector particles are negative → zero
   - Ch B {3^,2,1}: left sector A₄ has 3 negative helicities among 4 particles → vanishes for gluons (SWI)
   - Ch C {3^,2,1,6}: right sector A₃ has [4^5]=0 at pole → A₃^aMHV numerator zero

4. **[CONJECTURED]** The [3,4⟩ shift genuinely gives zero from all finite poles, suggesting either (a) there's a subtlety with the boundary term at z→∞ not vanishing for this shift+amplitude combination, or (b) the [1,2⟩ BCFW result is incorrect.

### 5.2 Shift validity analysis

The large-z behavior under [1,2⟩ shift: since ⟨1̂2⟩ = ε(λ₁+zλ₂,λ₂) = ⟨12⟩ (UNCHANGED, because ε(λ₂,λ₂)=0), the Parke-Taylor factor ⟨1̂2⟩ doesn't grow. The denominator factor ⟨61̂⟩ = ⟨61⟩+z⟨62⟩ ~ z → A₆^MHV(z) ~ 1/z → vanishes. For the full NMHV amplitude, the large-z behavior is more subtle (the ratio factor must also be analyzed).

### 5.3 Complexity of 6-pt NMHV vs 4-pt MHV

| Feature | 4-pt MHV | 6-pt NMHV |
|---------|----------|-----------|
| BCFW channels | 1 | 3 (1 trivially zero) |
| Sub-amplitude types | A₃^MHV × A₃^MHV | A₃^aMHV × A₅^aMHV, A₄^MHV × A₄^MHV |
| Helicity tracking | 2 labels | 6 labels + internal |
| Cyclic ordering errors possible | No (only 1 configuration) | Yes (many orderings) |
| Verified implementations | 3 methods agree | 2 methods DISAGREE |

---

## Section 6: What Would Need to be Fixed

To complete this exploration, the following need to be resolved:

1. **Verify [1,2⟩ Ch2:** Build a careful diagram of the cyclic ordering for {1̂,6,5}|{2̂,3,4}. The color order of left sub-amplitude A₄ should be (K,5,6,1̂) or (K,1̂,6,5) depending on traversal direction.

2. **Verify [2,4⟩ Ch3 and Ch4:** Same issue with cyclic ordering for non-adjacent shift.

3. **Use analytic formula as ground truth:** Implement the R-invariant formula for A₆^NMHV using momentum twistors (5-brackets). This is a direct formula, not recursive, and would give the correct answer to verify against.

4. **Then attempt Grassmannian:** With a verified numerical target, implement the G(3,6) residue computation.

---

## Code Files

- `code/kinematics_6pt.py` — 6-particle kinematics generation [VERIFIED]
- `code/mhv_baseline.py` — Parke-Taylor for all 15 MHV configurations [COMPUTED]
- `code/bcfw_6pt.py` — BCFW with [1,2⟩ shift [BUGGY]
- `code/crosscheck_shift34.py` — Cross-check with [3,4⟩ shift [INCONCLUSIVE]
- `code/crosscheck_shift24.py` — Cross-check with [2,4⟩ shift [DISAGREES with [1,2⟩]]

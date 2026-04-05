# Q5 Critique — Rhombohedral R3m Bragg Reflection Splitting

## Question
Perovskite family, rhombohedral R3m, pseudocubic indexing. How many Bragg reflections for {200}, {220}, {222}?

## Plan Under Review
> (1) Extract cubic multiplicities for {200}, {220}, {222}. (2) Apply rhombohedral R3m symmetry — 3-fold axis along [111] plus mirrors — to partition each cubic family into orbits of equivalent reflections. (3) Count distinct orbits (each = one resolved Bragg peak). Key insight: rhombohedral distortion preserves 3-fold cycling of [100],[010],[001] but distinguishes same-sign vs mixed-sign index combinations.

---

## Detailed Verification

### Check 1: Cubic family enumeration

| Family | Members | Multiplicity |
|--------|---------|-------------|
| {200} | (200), (-200), (020), (0-20), (002), (00-2) | 6 |
| {220} | (+/-2, +/-2, 0) and all permutations | 12 |
| {222} | (+/-2, +/-2, +/-2) | 8 |

**Verdict: Plan step (1) is standard and correct if these numbers are used.** No issue here.

### Check 2: R3m point group operations

R3m has point group 3m (C_3v), order 6. Operations:
1. Identity E
2. C_3 about [111]: (h,k,l) -> (l,h,k)
3. C_3^2 about [111]: (h,k,l) -> (k,l,h)
4. Mirror m_1 (perp to [1-10]): swaps h <-> k
5. Mirror m_2 (perp to [01-1]): swaps k <-> l
6. Mirror m_3 (perp to [-101]): swaps h <-> l

**Critical addition the plan underspecifies:** For diffraction (observable peak positions = d-spacings), the relevant symmetry is the **Laue group -3m** (order 12), which adds the inversion center (Friedel's law). The plan mentions 3-fold + mirrors but does not explicitly state that Friedel's law applies. This matters for orbit sizes but does not change the count of distinct d-spacings since d(hkl) = d(-h,-k,-l) regardless.

**Verdict: Correct but should explicitly invoke Friedel's law / Laue symmetry.**

### Check 3: Orbit counting — the critical step

The rhombohedral metric tensor for pseudocubic axes with a=b=c, alpha=beta=gamma (alpha != 90 degrees) gives:

d^{-2}(hkl) proportional to (h^2 + k^2 + l^2) + 2*cos(alpha)*(hk + kl + hl)

Therefore reflections with the same (h^2+k^2+l^2) split by their value of (hk+kl+hl).

#### {200} family:
All 6 members have h^2+k^2+l^2 = 4 and hk+kl+hl = 0.

| Orbit | Members | hk+kl+hl |
|-------|---------|-----------|
| A | (200), (020), (002), (-200), (0-20), (00-2) | 0 |

**Result: 1 Bragg reflection.** The 3-fold axis cycles (200)->(020)->(002) and Friedel handles the negatives.

#### {220} family:
All 12 members have h^2+k^2+l^2 = 8. Compute hk+kl+hl for each:

| Reflection | hk+kl+hl | Group |
|------------|-----------|-------|
| (220) | 4+0+0 = 4 | A |
| (022) | 0+4+0 = 4 | A |
| (202) | 0+0+4 = 4 | A |
| (-2-20) | 4+0+0 = 4 | A |
| (0-2-2) | 0+4+0 = 4 | A |
| (-20-2) | 0+0+4 = 4 | A |
| (-220) | -4+0+0 = -4 | B |
| (0-22) | 0-4+0 = -4 | B |
| (20-2) | 0+0-4 = -4 | B |
| (2-20) | -4+0+0 = -4 | B |
| (02-2) | 0-4+0 = -4 | B |
| (-202) | 0+0-4 = -4 | B |

Group A (hk+kl+hl = +4): 6 members — one orbit under -3m.
Group B (hk+kl+hl = -4): 6 members — one orbit under -3m.

Verification that B is a single orbit: C_3 cycles (-220)->(-202)->(0-22). Mirror (h<->k) maps (2-20)->(2-20) but mirror (k<->l) maps (2-20)->(20-2). C_3 maps (20-2)->(-220). So all of B are connected. Friedel maps (2-20) to (-220), also connecting subsets.

**Result: 2 Bragg reflections.**

#### {222} family:
All 8 members have h^2+k^2+l^2 = 12. Compute hk+kl+hl:

| Reflection | hk+kl+hl | Group |
|------------|-----------|-------|
| (222) | 4+4+4 = 12 | A |
| (-2-2-2) | 4+4+4 = 12 | A |
| (22-2) | 4-4-4 = -4 | B |
| (2-22) | -4-4+4 = -4 | B |
| (-222) | -4+4-4 = -4 | B |
| (-2-22) | 4-4-4 = -4 | B |
| (-22-2) | -4-4+4 = -4 | B |
| (2-2-2) | -4+4-4 = -4 | B |

Group A (hk+kl+hl = +12): {(222), (-2-2-2)} — 2 members. These lie along the [111] 3-fold axis.
Group B (hk+kl+hl = -4): remaining 6 members — one orbit.

Verification: C_3 maps (22-2)->(2-22)->(-222), connecting 3 members. Mirror (h<->k) maps (22-2)->(22-2) (invariant). Friedel maps (22-2)->(-2-22), connecting the +sign and -sign triples. All 6 are connected.

**Result: 2 Bragg reflections.**

### Check 4: Missing symmetry elements

No missing elements. The plan correctly identifies the key symmetry (3-fold + mirrors). The only nuance is that the Laue group -3m (not just 3m) governs diffraction peak positions, but since d(hkl) = d(-h,-k,-l) is always true, this doesn't change the orbit count for d-spacings.

---

## Issues Found

1. **MINOR — Friedel's law not explicit.** The plan should state that diffraction symmetry is -3m (Laue group), not just 3m. In practice this does not change the d-spacing count since d(hkl) = d(-h,-k,-l) is a geometric identity, but for intensity-distinct reflections it would matter.

2. **NO ERRORS in the logic.** The "key insight" about same-sign vs mixed-sign index combinations is exactly right. The splitting criterion is the value of (hk + kl + hl), which is the quantity that differentiates orbits when h^2+k^2+l^2 is held constant.

3. **SUGGESTION — Make the counting mechanism explicit.** The plan should state that the rhombohedral metric tensor makes d-spacing depend on both (h^2+k^2+l^2) AND (hk+kl+hl), so splitting within a cubic family occurs when members have different values of (hk+kl+hl). This is the computational backbone that the plan's "key insight" is reaching toward but doesn't fully articulate.

---

## VERDICT: APPROVED

## ISSUES:
1. Minor: Should explicitly invoke Friedel's law / Laue group -3m for completeness
2. Suggestion: Should name (hk+kl+hl) as the discriminating invariant under the rhombohedral metric tensor

## FINAL ANSWER:

| Family | Cubic multiplicity | Distinct d-spacings (hk+kl+hl values) | Bragg reflections |
|--------|-------------------|---------------------------------------|-------------------|
| {200} | 6 | 1 (all have hk+kl+hl = 0) | **1** |
| {220} | 12 | 2 (hk+kl+hl = +4 or -4) | **2** |
| {222} | 8 | 2 (hk+kl+hl = +12 or -4) | **2** |
| **Total** | **26** | | **5** |

## FINAL_PLAN:
(1) Enumerate cubic family members: {200}=6, {220}=12, {222}=8. (2) Note that the rhombohedral metric tensor (R3m, 3-fold axis along [111]) makes d-spacing depend on both (h^2+k^2+l^2) and (hk+kl+hl). Members of a cubic family share the first invariant, so splitting is governed entirely by distinct values of (hk+kl+hl). (3) Apply Laue group -3m (point group 3m + Friedel's law) to confirm orbit structure. (4) Count: {200} -> 1 peak (all hk+kl+hl=0), {220} -> 2 peaks (hk+kl+hl = +4 vs -4), {222} -> 2 peaks (hk+kl+hl = +12 vs -4). Total = 5 Bragg reflections.

# Q5 — XRD Bragg Reflections: Rhombohedral Perovskite (R3m)

## PHASE 1 — PLAN

### Constraints, Entities, Rules, and Relationships Extracted:

1. **Material**: Perovskite family, crystalline
2. **True structure**: Rhombohedral, space group R3m
3. **Indexing**: Done using a **pseudocubic** perovskite unit cell
4. **Measurement**: Highly resolved XRD pattern (meaning all splittings are resolved)
5. **Question**: How many Bragg reflections for {200}, {220}, and {222} families
6. **Key physics**: The cubic {hkl} family has a certain multiplicity. When symmetry is lowered to rhombohedral, some formerly equivalent planes become inequivalent, splitting the single cubic peak into multiple distinct peaks.

### Key Relationship — Cubic to Rhombohedral Splitting:

The rhombohedral distortion of a cubic perovskite occurs along the [111] direction (the body diagonal). This means:
- Planes related by permutations that differ in their relationship to the [111] axis will split apart.
- The rhombohedral distortion preserves the 3-fold axis along [111] but breaks the 4-fold axes along [100] directions.

### Plan (3 steps):

1. **Enumerate** the cubic multiplicity for each family {200}, {220}, {222}
2. **Apply the rhombohedral splitting rule**: Group the cubic reflections into subsets that remain equivalent under R3m symmetry (which has a 3-fold axis along [111] plus mirror planes)
3. **Count the distinct groups** for each family — each group = one Bragg reflection in the resolved pattern

---

## PHASE 2 — SOLVE

### Step 1: Cubic multiplicities

In cubic symmetry (m3m point group):
- **{200}**: The planes are (200), (020), (002), (-200), (0-20), (00-2) → multiplicity = 6
- **{220}**: The planes are (220), (2-20), (202), (20-2), (022), (0-22), and their negatives → multiplicity = 12
- **{222}**: The planes are (222), (-222), (2-22), (22-2), and their negatives → multiplicity = 8

### Step 2: Rhombohedral splitting analysis

The rhombohedral system (R3m, point group 3m) has a 3-fold rotation axis along [111]_cubic and mirror planes containing the [111] axis.

**For {200} family (cubic multiplicity 6):**

The 6 planes are: (200), (020), (002), (-200), (0-20), (00-2).

In powder diffraction, (hkl) and (-h,-k,-l) always give the same d-spacing (Friedel's law), so we work with pairs: {200, -200}, {020, 0-20}, {002, 00-2} — but these pairs already correspond to the same Bragg angle. So we have 3 distinct directions to consider: [100], [010], [001].

Under the 3-fold axis along [111], the three directions [100], [010], [001] are permuted cyclically. So all three remain equivalent under R3m.

**Result: {200} → 1 peak** (all 6 reflections remain equivalent under the 3-fold axis).

Wait — let me reconsider. The rhombohedral distortion stretches/compresses along [111]. The pseudocubic cell becomes a rhombohedron where a=b=c but α=β=γ≠90°.

For the (200), (020), (002) planes: In a rhombohedron with equal axes a=b=c and angle α, the d-spacing for (h00), (0k0), (00l) with same |h|=|k|=|l| are all the same by the 3-fold symmetry. So indeed {200} does NOT split.

**{200} → 1 reflection**

**For {220} family (cubic multiplicity 12):**

The 12 planes: (220), (-220), (2-20), (-2,20), (202), (-202), (20-2), (-2,0,2), (022), (0-22), (02-2), (0,-2,2).

In powder diffraction, (hkl) and (-h,-k,-l) give the same d-spacing, so distinct directions reduce to 6: (220), (2-20), (202), (20-2), (022), (02-2).

Under the 3-fold rotation along [111]: (220)→(022)→(202), so these three are equivalent. Similarly: (2-20)→(02-2)→(20-2), so these three are equivalent.

Now, do these two groups have the same d-spacing? In the rhombohedral system, (220) involves indices where both non-zero indices have the same sign, while (2-20) has opposite signs. Due to the rhombohedral distortion (α≠90°), these will generally have different d-spacings.

**{220} → 2 reflections**

**For {222} family (cubic multiplicity 8):**

The 8 planes: (222), (-2,-2,-2), (-222), (2,2,-2), (2,-2,2), (-2,2,-2), (-2,2,2), (2,-2,-2).

By Friedel's law, pairs give same d-spacing: (222)≡(-2-2-2), (-222)≡(22-2), (2-22)≡(-22-2), (-2,2,2)≡(2,-2,-2). Wait, let me be more careful.

Distinct directions (modulo ±): (222), (2,2,-2), (2,-2,2), (-2,2,2).

Under 3-fold rotation along [111]:
- (222) → (222) → (222): this is invariant (it IS the [111] direction). So (222) is its own orbit, multiplicity 1 from the 3-fold.
- (2,2,-2) → (-2,2,2) → (2,-2,2): these three cycle into each other.

So we have two groups:
- Group 1: (222) [and its Friedel pair (-2,-2,-2)] — 2 planes
- Group 2: (22-2), (2-22), (-222) [and their Friedel pairs] — 6 planes

Do these have different d-spacings? In a rhombohedron, the [111] direction is special (it's the unique axis). The d-spacing for (222) involves all indices the same sign — this probes the spacing along the 3-fold axis. The d-spacing for (22-2) type involves a different geometric relationship. With α≠90°, these are generally different.

**{222} → 2 reflections**

### Step 3: Final count

- {200}: **1** Bragg reflection
- {220}: **2** Bragg reflections
- {222}: **2** Bragg reflections

**Total: 1 + 2 + 2 = 5 Bragg reflections**

### Verification (opposite reading check):

Could {200} split? Only if the three cubic axes become inequivalent — but in rhombohedral symmetry they remain equivalent under the 3-fold axis. Confirmed: no split.

Could {220} give 3 or more peaks? The mirror planes in 3m relate some of the (hk0)-type reflections but the two groups identified above are NOT related by any symmetry operation. The 3-fold groups them into triplets, and there are exactly 2 orbits. Confirmed: 2.

Could {222} remain unsplit? Only if (222) and (22-2) have the same d-spacing, which would require α=90° (cubic). Since α≠90° in the rhombohedral case, they split. Confirmed: 2.

---

## ANSWER

**{200}: 1, {220}: 2, {222}: 2 → Total = 5 Bragg reflections**

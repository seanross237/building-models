# Q5 — XRD Bragg Reflections: Rhombohedral Perovskite (R3m) — Run 2

## PHASE 1 — PLAN

### Constraints, Entities, Rules, and Relationships Extracted:

1. **Material**: Perovskite family, crystalline
2. **True structure**: Rhombohedral, space group R3m (point group 3m, Laue class -3m)
3. **Indexing**: Pseudocubic perovskite cell — Miller indices are cubic, but actual symmetry is rhombohedral
4. **XRD resolution**: Highly resolved — all splittings are observable (no overlapping peaks assumed)
5. **Question**: Count distinct Bragg reflections for {200}, {220}, {222} families
6. **Key physics**: Rhombohedral distortion along [111] cubic direction. Lattice has a=b=c, α=β=γ≠90°.
7. **d-spacing formula for rhombohedral**: 1/d² depends on two quantities: (h²+k²+l²) and (hk+kl+hl). Two reflections coincide iff both quantities match.

### Opposite-reading check:
- Could this be about systematic absences rather than peak splitting? No — R3m has no extinction conditions that would eliminate these fundamental reflections in pseudocubic indexing. The question is about splitting of cubic-degenerate peaks.

### Plan (3 steps):

1. **For each cubic family**, list all distinct members (using Friedel's law to identify powder-equivalent pairs)
2. **Compute the two rhombohedral invariants** (h²+k²+l²) and (hk+kl+hl) for each member — reflections with identical values share a d-spacing
3. **Count distinct (h²+k²+l², hk+kl+hl) pairs** per family = number of resolved Bragg peaks

---

## PHASE 2 — SOLVE

### Step 1 & 2: Enumerate and compute invariants

**{200} family** (cubic multiplicity 6):

| Reflection | h²+k²+l² | hk+kl+hl |
|------------|-----------|-----------|
| (200)      | 4         | 0         |
| (020)      | 4         | 0         |
| (002)      | 4         | 0         |
| (-200)     | 4         | 0         |
| (0-20)     | 4         | 0         |
| (00-2)     | 4         | 0         |

All six have identical invariants (4, 0). **→ 1 distinct peak**

**{220} family** (cubic multiplicity 12, 6 unique by Friedel's law):

| Reflection | h²+k²+l² | hk+kl+hl |
|------------|-----------|-----------|
| (220)      | 8         | 4         |
| (202)      | 8         | 4         |
| (022)      | 8         | 4         |
| (2-20)     | 8         | -4        |
| (20-2)     | 8         | -4        |
| (02-2)     | 8         | -4        |

Two distinct groups: (8, 4) and (8, -4). **→ 2 distinct peaks**

**{222} family** (cubic multiplicity 8, 4 unique by Friedel's law):

| Reflection | h²+k²+l² | hk+kl+hl |
|------------|-----------|-----------|
| (222)      | 12        | 12        |
| (22-2)     | 12        | -4        |
| (2-22)     | 12        | -4        |
| (-222)     | 12        | -4        |

Two distinct groups: (12, 12) and (12, -4). **→ 2 distinct peaks**

### Step 3: Final count

| Family | Distinct Bragg reflections |
|--------|--------------------------|
| {200}  | 1                        |
| {220}  | 2                        |
| {222}  | 2                        |
| **Total** | **5**                 |

### Verification via exclusion:

- **Could {200} split?** Only if the three cubic axes [100], [010], [001] become inequivalent. The 3-fold axis along [111] permutes them cyclically, keeping them equivalent. The rhombohedral metric confirms: all have (h²+k²+l²=4, hk+kl+hl=0). Exclusion confirmed.
- **Could {220} give 3+ peaks?** The 3-fold axis groups (220)↔(022)↔(202) and (2-20)↔(02-2)↔(20-2). Mirror planes in 3m do NOT relate the two groups (they have different hk+kl+hl values: +4 vs -4). Exactly 2, exclusion confirmed.
- **Could {222} remain unsplit?** That would require (222) and (22-2) to have the same d-spacing, which requires hk+kl+hl to match — but 12 ≠ -4. They split unless α=90° (cubic). Exclusion confirmed.
- **Could {222} split into 3+ peaks?** The three members (22-2), (2-22), (-222) are related by the 3-fold axis and all have identical invariants (-4). So they cannot separate further. Exactly 2, confirmed.

---

## ANSWER

**{200}: 1, {220}: 2, {222}: 2 → Total = 5 Bragg reflections**

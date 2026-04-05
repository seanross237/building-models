# Q5 — Router + Planner Output

## Question
Suppose a crystalline material from the perovskite family stabilizes in a Rhombohedral structure with an R3m space group. How many Bragg reflections for {200}, {220} and {222} family of planes? Pseudocubic indexing.

## Route

ROUTE: DISCRIMINATION

## Rationale
This is constraint-satisfaction over a finite enumerable set. The solver must: (1) extract the extinction/reflection conditions imposed by the R-centering of the rhombohedral lattice, (2) enumerate every symmetry-equivalent plane in each pseudocubic family, (3) check each plane against the conditions to classify it as allowed or extinct. No extended computation or multi-step arithmetic chain is needed — the work is discriminating "allowed vs. forbidden" for each candidate reflection.

## Plan

PLAN:
1. **Extract constraints.** From R3m (rhombohedral, R-centering), the general reflection condition for the hexagonal axes is: -h+k+l = 3n (i.e., only reflections where -h+k+l is divisible by 3 are allowed). Restate this in pseudocubic indices: when pseudocubic (hkl) are converted to rhombohedral/hexagonal setting, the R-centering condition eliminates reflections where the sum h+k+l (in the rhombohedral primitive cell) is not a multiple of 3. In pseudocubic indexing, the relevant rule is that certain permutations within each {hkl} family will be split by the rhombohedral distortion and some become extinct under R-centering.
2. **List candidates.** Enumerate all symmetry-equivalent planes in the pseudocubic families:
   - {200}: the 6 permutations (200, 020, 002, -200, 0-20, 00-2) — but as Bragg reflections (hkl) and (-h,-k,-l) are equivalent, so 3 distinct: (200), (020), (002).
   - {220}: the 12 permutations — 6 distinct: (220), (202), (022), (-220), (20-2), (0-22), etc.
   - {222}: the 8 permutations — but with Friedel equivalence, distinct set: (222), (-222), (2-22), (22-2) → 4 distinct.
3. **Resolve in dependency order.** Apply the rhombohedral distortion + R3m extinction rules to each candidate. The rhombohedral distortion along the pseudocubic [111] direction breaks cubic degeneracy: planes whose Miller indices relate by the lost symmetry operations (those in m3m but not in R3m) become inequivalent and may split into separate peaks. Count the number of distinct allowed Bragg peaks for each family after applying both the symmetry-splitting and systematic absences.
END_PLAN

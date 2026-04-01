# Q6 — Mossbauer Hyperfine Field (Opus, Run 1, Hybrid M2+M4)

## PLAN

**Constraints and entities extracted:**

1. **Quantity to maximize:** Hyperfine field (internal magnetic field at the Fe nucleus) in 57Fe Mossbauer spectroscopy
2. **Hyperfine field components:**
   - **Fermi contact term** (dominant): proportional to unpaired electron spin density at the nucleus. Scales with total spin S and the degree to which unpaired electrons have s-orbital character via core polarization.
   - **Orbital contribution:** from unquenched orbital angular momentum
   - **Dipolar contribution:** from anisotropic spin distribution
3. **Key relationship:** Larger S (more unpaired electrons) generally means larger hyperfine field. The Fermi contact field for high-spin Fe(III) (S=5/2, d5) is typically the largest because all five d-electrons are unpaired and exchange polarization of core s-electrons is maximized by the symmetric half-filled shell.
4. **Oxidation state / spin analysis:**
   - Fe(III) d5, S=5/2 → 5 unpaired electrons (maximum possible for d-block)
   - Fe(II) d6, S=2 → 4 unpaired electrons
   - Fe(IV) d4, S=2 → 4 unpaired electrons
   - Fe(II) S=0 → 0 unpaired electrons
5. **Coordination geometry:** Affects orbital contribution and covalency but is secondary to the spin state for the Fermi contact term.

**Options quick-screen:**
- A: S=0, zero unpaired electrons → near-zero hyperfine field. ELIMINATE immediately.
- B: S=5/2 Fe(III) → 5 unpaired electrons, half-filled d5 shell. STRONGEST candidate.
- C: S=2 Fe(II) → 4 unpaired electrons.
- D: S=2 Fe(II) → 4 unpaired electrons.
- E: S=2 Fe(IV) → 4 unpaired electrons.

**Shortest path (3 steps):**
1. Hyperfine field is dominated by Fermi contact term, which scales with number of unpaired electrons and their core s-shell polarization efficiency.
2. S=5/2 Fe(III) has 5 unpaired electrons; all other options have 4 or 0.
3. The half-filled d5 configuration in high-spin Fe(III) produces the largest known hyperfine fields in iron Mossbauer (~50-55 T in ionic compounds), a well-established experimental fact.

## SOLVE

### Fermi contact term analysis

The internal hyperfine field at the 57Fe nucleus is dominated by the Fermi contact interaction:

B_hf ∝ -S * A_contact

where A_contact depends on the net s-electron spin density at the nucleus, generated primarily by exchange polarization of filled core s-shells (1s, 2s, 3s) by the unpaired d-electrons.

**High-spin Fe(III), d5, S=5/2:** Five unpaired electrons, all with the same spin orientation. This configuration produces the maximum possible exchange polarization of core s-electrons. The symmetric half-filled shell is particularly effective because every d-orbital contributes constructively — there is no partial cancellation from minority-spin d-electrons. Known experimental values: ~50-55 T in ionic Fe(III) compounds.

**Fe(II) S=2 and Fe(IV) S=2:** Four unpaired electrons. The Fermi contact field is substantial but necessarily smaller than the 5-electron case, all else being equal. Typical values: ~30-45 T depending on covalency.

**Fe(II) S=0:** No unpaired electrons, no net spin, no Fermi contact field. Hyperfine field is essentially zero (no magnetic hyperfine splitting observed).

### Geometry considerations (secondary)

- Planar geometry (option B): Unusual for Fe(III) S=5/2 but does not diminish the contact term significantly. May have some unquenched orbital angular momentum adding to the field.
- Linear geometry (option C): Very low coordination can reduce covalency and enhance the ionic character, potentially increasing the contact field per unpaired electron. But 4 unpaired electrons still cannot overcome the fundamental advantage of 5.
- Tetrahedral (option D): Standard geometry for high-spin Fe(II). Well-characterized hyperfine fields, typically ~35-45 T.
- Trigonal bipyramidal (option E): Fe(IV) is more covalent than Fe(III), which tends to reduce the contact field.

### Exclusion checks

1. **Opposite reading:** Could geometry effects (e.g., linear coordination in C) create an orbital contribution large enough to overcome the 1-electron deficit versus B? The orbital contribution is typically 5-10 T at most, while the contact term difference between S=5/2 and S=2 is ~10-15 T. So no, geometry cannot compensate.

2. **Surface pattern check:** Am I just picking the highest S? Not blindly — S=5/2 wins because (a) it has the most unpaired electrons, (b) the half-filled d5 shell has a special enhancement effect on core polarization, and (c) the Fermi contact term dominates. This is physically grounded.

3. **Misleading patterns:** The "planar" geometry for Fe(III) S=5/2 is unusual and might seem like a trap. But the question asks about expected hyperfine field, which is determined primarily by the electronic spin state, not the coordination geometry. The geometry mainly affects isomer shift and quadrupole splitting, not the magnetic hyperfine field to first order.

## ANSWER

**B. planar S = 5/2 Fe(III)**

The half-filled d5 configuration with S=5/2 produces the largest Fermi contact hyperfine field due to maximum exchange polarization of core s-electrons by five unpaired d-electrons. This is the dominant contribution to the total hyperfine field and cannot be matched by the 4-unpaired-electron configurations in options C, D, and E, regardless of geometry. Option A (S=0) has zero hyperfine field.

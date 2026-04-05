# Q1 — FTIR Tardigrade Hydrogel (Opus Run 2, Hybrid M2+M4)

## PHASE 1 — PLAN

### Entities
- Tardigrade proteins (intrinsically disordered proteins)
- Cold-setting hydrogels formed upon hydration
- FTIR amide I peaks

### Constraints (FTIR Peak Assignments)
| Peak (cm⁻¹) | Assignment |
|---|---|
| 1645 (broad) | Random coil / disordered |
| 1652 (shoulder) | Alpha helix |
| 1618 (shoulder) | Intermolecular beta sheet (low-freq component) |
| 1680 (shoulder) | Antiparallel beta sheet (high-freq component) |

Note: 1618 + 1680 together = classic signature of intermolecular antiparallel beta sheets.

### Observations
1. **Starting state:** Proteins are initially disordered → disorder-to-order transition upon gelation
2. **Heating:** 1645 grows (more disorder), 1618 + 1680 disappear (beta sheets melt) → beta sheets are thermally reversible cross-links
3. **Concentration titration:** Dual increase in 1652 (alpha helix) AND 1618 (beta sheet) → both structures form upon gelation

### Shortest Path (3 steps)
1. Starting state = disordered (explicitly stated). Gelation = ordering event.
2. Heating destroys 1618+1680 (beta sheets) while 1645 grows (disorder returns) → confirms beta sheet formation is the gelation mechanism.
3. Concentration titration shows dual increase in 1652 AND 1618 → both alpha helices and beta sheets form from disordered state. Only answer I matches.

## PHASE 2 — SOLVE

### Exclusion Analysis
| Answer | Verdict | Reason |
|---|---|---|
| A. α-helix → disordered | EXCLUDE | Wrong direction; starting state is disordered, not helical |
| B. disordered → α-helix | EXCLUDE | No beta sheet component; contradicts 1618+1680 peaks and concentration data |
| C. Coiled-coils | EXCLUDE | Coiled-coils show ~1630 cm⁻¹, not 1618+1680 antiparallel pair; doesn't explain dual increase |
| D. α-helix → β-sheet | EXCLUDE | Starting state is disordered, not alpha helix |
| E. β-sheet → α-helix | EXCLUDE | Starting state is disordered, not beta sheet |
| F. disordered → β-sheet | EXCLUDE | Doesn't account for 1652 (α-helix) increase in concentration titration |
| G. parallel → antiparallel swap | EXCLUDE | Starting state is disordered, not pre-existing beta sheets |
| H. β-sheet → disordered | EXCLUDE | Wrong direction; starting state is disordered |
| **I. disordered → β-sheets + α-helices** | **SURVIVES** | Matches all: starts disordered, forms both β-sheets (1618+1680) and α-helices (1652), heating reverses β-sheet component |

### Verification Checks
1. **Opposite reading:** Could 1652 be something other than α-helix? No — 1652 cm⁻¹ is squarely α-helix in amide I. Could 1618+1680 be non-β-sheet? No — this is the textbook intermolecular antiparallel β-sheet pair.
2. **Surface pattern trap:** Tempting to pick F (disordered → β-sheet only) since β-sheets dominate gelation signal, but concentration titration explicitly shows DUAL increase in both 1652 and 1618. Only I captures both secondary structures forming.
3. **Consistency with biology:** Tardigrade disordered proteins (like CAHS proteins) are known to form hydrogels with mixed secondary structure elements — both α-helical and β-sheet components have been reported in the literature.

## ANSWER

**I. Disordered structures fold into beta sheets and alpha helices upon gelation**

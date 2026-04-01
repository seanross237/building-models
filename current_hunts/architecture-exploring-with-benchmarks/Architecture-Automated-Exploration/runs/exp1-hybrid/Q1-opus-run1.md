# Q1 — FTIR Biophysics (Opus, Run 1, Hybrid M2+M4)

## PHASE 1 — PLAN

### Constraint Extraction

**Entities:**
- Tardigrade proteins (intrinsically disordered proteins / IDPs)
- Cold-setting hydrogels
- Initially disordered, assume order at high concentration

**FTIR Peak Assignments (constraints from spectroscopy):**
- 1645 cm⁻¹ (broad): Random coil / disordered structure
- 1652 cm⁻¹ (shoulder): Alpha helix
- 1618 cm⁻¹ (shoulder): Intermolecular beta sheet (aggregation-associated beta sheet)
- 1680 cm⁻¹ (shoulder): Beta turn or antiparallel beta sheet (high-frequency component)

**Behavioral constraints:**
1. **Heating experiment:** 1645 cm⁻¹ grows stronger (more disorder); 1618 and 1680 cm⁻¹ disappear (beta sheet structures melt away)
2. **Concentration titration:** Dual increase in 1652 cm⁻¹ AND 1618 cm⁻¹ as concentration increases (both alpha helix and beta sheet form simultaneously with increasing concentration)
3. **Gelation context:** Proteins are initially disordered but form ordered gel at high concentration

**Rules / Relationships:**
- The 1618 + 1680 cm⁻¹ pair appearing/disappearing together is diagnostic of intermolecular beta sheet (antiparallel beta sheet has both a low ~1618-1630 and high ~1680 component)
- Heating reverses gelation — structures that form during gelation should disappear on heating
- Concentration increase drives gelation — structures that form during gelation should increase with concentration

### Shortest Path to Answer (3 steps):

1. **Identify what forms during gelation:** The concentration experiment shows 1652 (alpha helix) AND 1618 (beta sheet) both increase together → gelation produces BOTH alpha helices and beta sheets simultaneously.
2. **Identify the starting state:** Proteins are described as "initially disordered" → the precursor is disordered/random coil (1645 cm⁻¹).
3. **Confirm with heating data:** Heating (which disrupts gel) causes 1645 to grow (more disorder returns) while 1618 and 1680 disappear (beta sheets melt) → consistent with ordered structures reverting to disorder. The 1618+1680 pair disappearing together on heating confirms these are thermally labile intermolecular beta sheets formed during gelation.

**Conclusion from plan:** Disordered structures fold into both beta sheets and alpha helices upon gelation → Answer I.

---

## PHASE 2 — SOLVE (Exclusion-First Verification)

### Grounding each claim in specific evidence:

**Claim 1: The starting state is disordered.**
- Evidence: Problem states "initially disordered but rapidly assume order at high enough concentration." The broad 1645 cm⁻¹ peak (random coil) is present and grows upon heating (reversing gelation back to disorder). CONFIRMED.

**Claim 2: Beta sheets form upon gelation.**
- Evidence: 1618 cm⁻¹ (intermolecular beta sheet) increases with concentration (concentration titration). The 1618 + 1680 cm⁻¹ pair disappears upon heating (thermal disruption of gel). The pairing of 1618 and 1680 is characteristic of antiparallel/intermolecular beta sheet. CONFIRMED.

**Claim 3: Alpha helices form upon gelation.**
- Evidence: 1652 cm⁻¹ (alpha helix) increases with concentration in the titration experiment. CONFIRMED.

### Checking the OPPOSITE of initial reading:

- **Could this be ONLY beta sheet formation (Answer F)?** No — the concentration titration explicitly shows DUAL increase of both 1652 (helix) and 1618 (sheet). If only beta sheets formed, we would not see 1652 increase. EXCLUDED.
- **Could this be coiled-coil formation (Answer C)?** Coiled-coils would show alpha-helical signature (~1652) but would NOT explain the 1618 cm⁻¹ beta sheet peak increasing with concentration. EXCLUDED.
- **Could 1652 be misassigned?** In FTIR, 1652 cm⁻¹ is solidly in the alpha-helix range (1650-1658). It is distinct from random coil (1640-1648). The problem labels 1645 as broad (random coil) and 1652 as a shoulder — these are resolved as separate peaks. Assignment is sound.

### Checking for misleading surface patterns:

- The 1680 cm⁻¹ peak disappearing on heating might suggest antiparallel-to-parallel beta sheet conversion (Answer G), but the 1618 cm⁻¹ peak ALSO disappears — both beta sheet markers vanish together, meaning beta sheets are melting entirely, not converting between configurations. EXCLUDED.
- Answer B (disorder → alpha helix only) fails because it ignores the 1618 cm⁻¹ beta sheet signal.
- Answer D (alpha helix → beta sheet) fails because the starting state is disordered, not helical.

### All three checks passed for Answer I. No other answer survives.

---

## ANSWER

**I. Disordered structures fold into beta sheets and alpha helices upon gelation.**

The concentration titration is the decisive experiment: both 1652 cm⁻¹ (alpha helix) and 1618 cm⁻¹ (intermolecular beta sheet) increase simultaneously with concentration, while the proteins start disordered. Heating reverses this by restoring the 1645 cm⁻¹ disordered peak and eliminating the beta sheet markers (1618 + 1680 cm⁻¹). Only answer I accounts for the simultaneous formation of both secondary structure types from an initially disordered state.

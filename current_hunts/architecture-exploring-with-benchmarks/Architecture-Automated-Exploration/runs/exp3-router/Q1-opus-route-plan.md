# Q1 — FTIR Tardigrade Protein Hydrogels

## ROUTE: DISCRIMINATION

## PLAN:

Extract every constraint, entity, rule, and relationship. List explicitly. Identify dependencies. Resolve independent constraints first, dependent ones after.

### Constraint Extraction

1. **Peak assignments (independent — resolve first):**
   - 1645 cm^-1 (broad): Assign to known secondary structure. This region is canonical for disordered/random coil (~1640-1650 cm^-1).
   - 1652 cm^-1 (shoulder): Assign. This is canonical alpha-helix (~1650-1658 cm^-1).
   - 1618 cm^-1 (shoulder): Assign. This is canonical intermolecular/aggregated beta-sheet (~1615-1625 cm^-1).
   - 1680 cm^-1 (shoulder): Assign. This is canonical anti-parallel beta-sheet high-frequency component (~1680-1690 cm^-1).

2. **Behavioral constraints (dependent — resolve after assignments):**
   - **Heating experiment:** 1645 grows stronger; 1618 and 1680 disappear. Interpretation: heating causes beta-sheet (both markers) to convert into disordered structure. This rules out options where heating would create order.
   - **Concentration titration:** Dual increase in 1652 AND 1618 as concentration rises. Interpretation: increasing concentration simultaneously drives formation of alpha-helix (1652) AND beta-sheet (1618). This means the starting disordered state converts into BOTH ordered structures upon concentration increase.

3. **Context constraint:** Proteins are initially disordered but assume order at high concentration. This confirms the direction: disordered -> ordered.

### Resolution — Match to Options

- Must start from disordered (eliminates A, E, G, H).
- Must produce BOTH alpha-helix (1652 increase) AND beta-sheet (1618 increase) (eliminates B [helix only], D [starts from helix], F [beta only]).
- Heating reversal: beta-sheet markers vanish, disordered grows — consistent with thermally reversible beta-sheet formation from disordered state.
- Only option producing both alpha-helix and beta-sheet from disordered: **I**.

### Answer to verify: I. Disordered into beta sheets and alpha helices

END_PLAN

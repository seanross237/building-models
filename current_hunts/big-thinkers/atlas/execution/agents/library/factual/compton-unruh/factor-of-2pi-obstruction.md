---
topic: Factor of 1/(2π) in MOND a₀ cannot be derived from T_U/T_dS internally — four approaches all fail
confidence: verified
date: 2026-03-27
source: "compton-unruh strategy-001 exploration-007"
---

## Finding

The T_U/T_dS ratio predicts a₀ = cH₀ = 6.8×10⁻¹⁰ m/s², which is 5.7× larger than the observed MOND
acceleration a₀_obs = 1.2×10⁻¹⁰ m/s². A factor of 1/(2π) ≈ 0.159 (so cH₀/(2π) ≈ 1.08×10⁻¹⁰,
within 10% of observed) would fix the scale. Four independent approaches to deriving this factor
internally from T_U/T_dS all **fail**. The correction must be imported from Verlinde's area-volume
entropy competition, which is an independent physical framework.

## Why 1/(2π) Appears in MOND a₀

Verlinde (2016) derives an effective MOND-like force from the "elasticity" of de Sitter entanglement
entropy. The key formula:

```
Σ_D(r)² = (cH₀ / 8πG) × Σ_B(r)
```

where Σ_D is the "apparent dark matter" surface density and Σ_B is the baryonic surface density.
This gives:

```
g_D = √(g_B × cH₀/(2π))    → a₀ = cH₀/(2π)
```

The factor 1/(2π) arises from the **competition between surface entropy (∝ r²) and volume entropy
(∝ r³)** in the de Sitter thermal medium. It is geometric, not kinematic.

## The Algebraic Reason T_U/T_dS Cannot Produce 1/(2π)

The two temperature formulas are:
```
T_U  = ℏa / (2πk_Bc)
T_dS = ℏH₀ / (2πk_B)
```

Both have the same factor of 2π in their denominators. In the ratio:
```
T_U/T_dS = a/(cH₀)
```

The 2π factors cancel exactly. This is algebraically inevitable — no modification of the ratio can
introduce a 1/(2π) suppression unless the temperature formulas themselves are changed.

## The Four Failed Approaches [COMPUTED]

All tested in `code/factor_sixth.py` (compton-unruh strategy-001 exploration-007):

**Approach A — Angular averaging:**
The Unruh temperature T_U = ℏa/(2πk_Bc) is already the full 3+1D KMS temperature. No additional
angular averaging is available. **Result: NO extra factor.**

**Approach B — Rindler vs. de Sitter horizon area:**
Regulated Rindler horizon area = πR_H². De Sitter horizon area = 4πR_H². Ratio = 1/4, not 1/(2π).
**Result: NOT 1/(2π).**

**Approach C — Entropy rate ratio:**
The Unruh entropy rate formula doesn't produce a 1/(2π) suppression when compared to the de Sitter
entropy rate. **Result: NO extra factor.**

**Approach D — Quantum information route:**
The ratio of Rindler to de Sitter entanglement entropy capacities goes as H₀/(ac), which is GROWING
at small a — not the MOND-like formula. **Result: WRONG direction.**

## Implications

This is a **genuine gap** in the T_U/T_dS framework:

| Model | a₀ | a₀/a₀_MOND |
|-------|-----|------------|
| T_U/T_dS (standard) | cH₀ = 6.8×10⁻¹⁰ | 5.67 (too large) |
| With Verlinde correction | cH₀/(2π) = 1.08×10⁻¹⁰ | 0.90 |
| Observed MOND | 1.2×10⁻¹⁰ | 1.00 |

The T_U/T_dS model **needs an external input** (from Verlinde) to get the correct a₀. It cannot derive
the scale internally.

**The key open problem**: Why is a₀ = cH₀/(2π)? This requires a first-principles connection between
the T_U/T_dS framework and Verlinde's elastic entropy — currently missing.

## Relationship to Other Entries

- `tu-tds-mond-identity.md` — the algebraic identity and its a₀ scale problem
- `verlinde-emergent-gravity-a0.md` — Verlinde's geometric derivation of a₀ = cH₀/(2π)
- `galaxy-rotation-curve-fits.md` — observational confirmation that cH₀/(2π) matches galaxy data

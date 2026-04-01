---
topic: T_U/T_dS model has fundamental ambiguity in which acceleration enters μ — three cases give contradictory predictions
confidence: verified
date: 2026-03-27
source: "compton-unruh strategy-001 exploration-008"
---

## Finding

The T_U/T_dS modified inertia formula m_i = m × μ(a/a₀) is **internally inconsistent** because the
"a" in μ is ambiguous. Three distinct physical interpretations (Cases A, B, C) give contradictory
predictions. Only Case B reproduces flat rotation curves, but Case B is not what the formula physically
states. This inconsistency was not caught in seven prior explorations and was only identified via
adversarial analysis.

## The Three Cases

### Case A: a = proper acceleration
The Unruh temperature T_U = ℏa/(2πck_B) uses **proper** acceleration. Stars in circular orbits are
in free fall — geodesics — with proper acceleration = 0. Therefore:

    T_U(0)/T_dS(0) = 0 → m_i = 0

This gives **zero inertial mass** for any freely-falling body. **Catastrophic failure** — the model
cannot apply to galaxy rotation curves at all. This is the free-fall objection (separately resolved via
de Sitter-relative acceleration; see `free-fall-objection-analysis.md`).

### Case B: a = centripetal acceleration (v²/r)
If a = v²/r is substituted into T_U/T_dS, the result is the standard MOND formula:

    μ(a/a₀) × a = g_N   where a = v²/r

In the deep MOND limit:
- a × (a/a₀) = GM/r²  →  a² = a₀ × GM/r²
- v²/r = √(a₀ × GM)/r  →  **v⁴ = GM × a₀ = CONSTANT**

This gives **flat rotation curves**. This is what explorations 004 and 006 actually computed,
achieving χ²/dof ~ 1 for NGC 3198 and NGC 2403.

### Case C: a = Newtonian gravitational acceleration g_N
The notation "m_i = m × μ(g_N/a₀)" implies this case. The modified inertia equation of motion is:

    m × μ(g_N/a₀) × v²/r = m × g_N
    v² = g_N × r / μ(g_N/a₀)

In deep MOND (g_N << a₀): μ ≈ g_N/a₀, so:
- v² ≈ a₀ × r
- **v ∝ √r — NOT flat rotation curves**

This case **fails to reproduce the key MOND phenomenology** (v = constant at large r). The rotation
curve rises outward without bound.

## The Internal Inconsistency

| Case | a in μ | Rotation curve | Status |
|------|--------|---------------|--------|
| A — proper acceleration | 0 for free fall | m_i = 0 (fatal) | CATASTROPHIC |
| B — centripetal (v²/r) | correct | flat v ✓ | ONLY CASE THAT WORKS |
| C — g_N (formula notation) | wrong | v ∝ √r ✗ | SILENT FAILURE |

The explorations 004 and 006 that produced successful χ²/dof ~ 1 fits used **Case B** implicitly.
But the GOAL.md notation "m_i = m × μ(g_N/a₀)" is **Case C**. The prior exploration success
was achieved by Case B, while the theoretical motivation points to Cases A or C.

**This inconsistency was not flagged in any of the seven prior constructive explorations.**

## Physical Significance

The ambiguity is not a notational issue — it reflects a genuine lack of a derivation for the formula.
If T_U/T_dS were properly derived from first principles, the derivation would specify which
acceleration enters. Without a derivation:
- The formula is phenomenologically motivated but physically undefined
- The "rotation curve success" in prior explorations was achieved by the one case that works
  (Case B), but Case B (centripetal acceleration = Unruh proper acceleration) is physically
  unmotivated

## Relationship to Other Entries

- `free-fall-objection-analysis.md` — Case A failure / how de Sitter approach resolves it
- `tu-tds-mond-identity.md` — the algebraic identity (assumes Case B for rotation curves)
- `tu-tds-viability-scorecard.md` — full model assessment (this ambiguity scores 1/10)

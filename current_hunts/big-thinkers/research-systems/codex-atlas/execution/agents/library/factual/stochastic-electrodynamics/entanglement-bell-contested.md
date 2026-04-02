---
topic: SED entanglement and Bell inequalities
confidence: provisional
date: 2026-03-27
source: "SED strategy-001 exploration-002; de la Pena et al. 2010; Marshall & Santos 1989; Santos 2020; Boyer 2018; SED strategy-002 exploration-006 adversarial review"
---

## Coupled Oscillators and Entanglement-like Correlations

de la Pena, Valdes-Hernandez & Cetto (2010): In Linear SED (LSED), two non-interacting particles coupled through shared ZPF at common resonance frequencies produce "non-factorizable states" corresponding to entangled QM states. For identical particles, predicts maximum entanglement.

**Critical caveat:** This uses LSED -- a specific formulation imposing additional statistical constraints beyond standard SED. LSED-to-standard-SED relationship is debated.

**E002 finding [CONJECTURED]:** Our direct simulation of two standard-SED oscillators shows S ≤ 2 (no Bell violation), contradicting the entanglement claim for standard SED. The apparent LSED "non-factorizable state" structure likely reflects formal mathematical equivalence that does not extend to Bell test predictions. LSED details differ from standard SED setup so the contradiction is not conclusive.

Boyer (1973) showed two SED oscillators coupled through ZPF exhibit van der Waals correlations consistent with QM (unretarded 1/r^6 and retarded 1/r^7). Uncontested SED success.

**Boyer (2018), arXiv:1804.03542:** Boyer explicitly states SED is a non-local hidden-variable theory — "the classical theory providing this agreement [van der Waals] is NOT local — random radiation phases distributed throughout space act as non-local hidden variables." SED gains its successes from this non-locality, not from quantum-like dynamics.

## Stochastic Optics and Bell Inequalities

Marshall & Santos (1989) developed "Stochastic Optics" (SO) as a local realistic alternative to quantum optics, treating vacuum fields as real. Their claim: entanglement is merely a signal-vacuum field correlation, and Bell's definition of local realism is "not general enough."

Santos (2020): In the Weyl-Wigner formalism, a local model of SPDC experiments can reproduce QM Bell-violating correlations. Argument hinges on treating vacuum field amplitudes as contextual hidden variables.

## Mainstream Response

Most physicists reject this line. Bell's theorem is considered rigorous. The detection efficiency loophole exploited by Marshall & Santos was closed by loophole-free Bell tests: Hensen et al. (2015), Giustina et al. (2015), Shalm et al. (2015). The contextuality argument is generally not accepted.

## DIRECT BELL-CHSH COMPUTATION [E002 — VERIFIED]

**First direct numerical computation of Bell-CHSH from two SED oscillators sharing a ZPF realization.** No prior published computation of this type found.

Two ALD harmonic oscillators at separations d = 0.0, 0.1, 1.0, 10.0 (c/ω₀). CHSH threshold measurements on 200 trajectories × 100,000 steps. Results:

| d (c/ω₀) | C_xx  | S_max (sim) |
|----------|-------|-------------|
| 0.0      | 1.000 | 2.000       |
| 0.1      | 0.995 | 1.949       |
| 1.0      | 0.538 | 1.092       |
| 10.0     | −0.833 | 1.613      |

**S never exceeds 2.** The d=0 case saturates at the classical maximum (perfectly correlated variables, degenerate settings A'=B identically — this is not a Bell violation, it is the classical bound being saturated).

**Theoretical closure:** Grid search over all bivariate Gaussian thresholds confirms S_max ≤ 2.000 for all correlation values ρ ∈ [−1, +1]. This is not a simulation artifact — Gaussian variables with any classical correlation cannot exceed the classical Bell bound. [COMPUTED]

**Conclusion:** The shared ZPF produces classical common-cause correlations (C_xx ≠ 0), not quantum entanglement. SED is a local realistic theory for this system in the sense that S ≤ 2.

See `sed-coupled-oscillator-zpf-correlations.md` for the C_xx(d) = cos(ω₀d/c) finding and full correlation data.

## ADVERSARIAL CORRECTION (E006) — QM Comparison Was Invalid

**CRITICAL:** The E002 framing "SED gives S ≤ 2 while QM gives S > 2" is INCORRECT. Two uncoupled harmonic oscillators in the QM vacuum state |0⟩⊗|0⟩ are in a **SEPARABLE** state. Separable QM states also give S ≤ 2. Bell violation in QM requires entangled states, which two uncoupled oscillators in vacuum are not.

**The correct comparison (E006):** SED and QM differ in the **ZPF-induced spatial correlation**, not Bell compliance:
- SED: C_xx(d) = cos(ω₀d/c) ≠ 0 — oscillating classical correlations from shared field phases
- QM: C_xx = 0 — no position correlations for uncoupled vacuum oscillators

Both give S ≤ 2. The Bell S ≤ 2 result is a tautology (SED is classical by construction). The scientifically meaningful comparison is C_xx ≠ 0 (SED) vs C_xx = 0 (QM).

**C_xx formula prior art:** Ibison & Haisch (1996), Phys. Rev. A 54, 2737, explicitly writes the ZPF two-point field correlator (their Eq. 41). C_xx(d) = cos(ω₀d/c) is a one-line consequence of the Boyer (1975) ZPF plane-wave expansion, implicit in every SED van der Waals calculation since 1973.

**Unresolved prior art risk:** Marshall, T.W. "Stochastic Electrodynamics and the Einstein-Podolsky-Rosen Argument" (1986, Springer) + a chapter titled "SED and the Bell Inequalities" (Springer book 978-94-009-5245-4, ch. 20, circa 1980s) — both paywalled. If either contains a Bell S ≤ 2 calculation for SED oscillators, E002's computation is not the first.

## Status

- Bell-CHSH direct computation: **S ≤ 2 confirmed [VERIFIED]** — but Bell comparison to QM was invalid (QM also gives S ≤ 2 for uncoupled oscillators); result is a tautology, not a contrast
- C_xx(d) = cos(ω₀d/c): confirmed [COMPUTED], but trivially derivable from Boyer (1975); modest novelty
- de la Pena LSED entanglement claim: **OPEN** (LSED differs from standard SED; formal structure not extended to Bell test predictions)
- Mainstream Bell arguments (Marshall & Santos loophole, Santos contextuality): **REJECTED** by loophole-free experiments
- Marshall-Santos 1986 Bell/SED chapter: **UNRESOLVED** (paywall; may predate E002's Bell computation)

## References

- de la Pena, L. et al. (2010). Physica E 42, 308-312.
- Marshall, T.W. & Santos, E. (1989). Phys. Rev. A 39, 6271.
- Santos, E. (2020). Found. Phys. 50, 1587-1607.
- Boyer, T.H. (2018). arXiv:1804.03542 — SED non-locality statement.
- Ibison, M. & Haisch, B. (1996). Phys. Rev. A 54, 2737 — ZPF two-point field correlator.
- Marshall, T.W. (1986). "SED and EPR Argument," Springer conference proceedings — PAYWALLED.
- SED strategy-001 exploration-002 (2026-03-27): first direct Bell-CHSH numerical computation.
- SED strategy-002 exploration-006 (2026-03-27): adversarial review identifying invalid QM comparison.

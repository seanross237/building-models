---
topic: quadratic-gravity-fakeon
confidence: verified
date: 2026-03-26
source: exploration-001-qgf-explanatory-debts (quantum-gravity-2 strategy-002)
---

# Sacrifice of S-Matrix Analyticity

## The Trade-Off

The fakeon prescription REQUIRES giving up analyticity of the S-matrix. A 2025 paper (Anselmi et al., JHEP 05, 2025, 145; arXiv:2503.01841) explicitly catalogs the four inequivalent quantization prescriptions for theories with complex poles and what each forfeits:

| Prescription | Unitarity (optical theorem) | Lorentz invariance | Analyticity | Renormalizability |
|---|---|---|---|---|
| (i) Textbook Wick rotation | ❌ | ✅ | ✅ | ✅ |
| (ii) Lee-Wick-Nakanishi | ✅* | ❌ | ✅ | ✅ |
| (iii) Fakeon | ✅ | ✅ | ❌ | ✅ |
| (iv) Direct Minkowski | ❌ | ✅ | ✅ | ❌ |

*Lee-Wick unitarity is only apparent — Kubo-Kugo (2023) and Anselmi-Modesto (2025) proved it definitively fails. See `../lee-wick-gravity/`.

The fakeon prescription is the ONLY choice that preserves both unitarity and Lorentz invariance, but the price is the loss of analyticity.

## What Analyticity Loss Means

The S-matrix in QG+F is NOT analytic: the peak region of the fakeon propagator is "outside the convergence domain" (Anselmi, JHEP 2022). Consequences:

1. **No dispersion relations** — Standard dispersion relations (Kramers-Kronig) relate real and imaginary parts of amplitudes and require analyticity. QG+F cannot use them.
2. **No S-matrix bootstrap** — The modern amplitudes/bootstrap program assumes analyticity, crossing symmetry, and unitarity. QG+F satisfies only unitarity. The powerful bootstrap techniques are unavailable.
3. **No standard Euclidean-Lorentzian connection** — Analyticity enables the Wick rotation between Euclidean and Lorentzian signatures. The fakeon prescription modifies this connection.
4. **Crossing symmetry applications limited** — Crossing symmetry in its standard form relies on analytic continuation.

## Anselmi's Radical Position on Causality (2026)

In arXiv:2601.06346 (Jan 2026), "On Causality and Predictivity," Anselmi takes a radical philosophical position: causality itself should be abandoned as a fundamental principle of physics. Key claims:

- Causality is "misleading" and "rests on metaphysical assumptions"
- The "illusory arrow of time associated with causality" is "inherently statistical"
- The maximum achievable in QG+F is "delayed prepostdictions" — not predictions or retrodictions, but a weakened form of inference
- Nonperturbative effects introduce a "new type of uncertainty" that limits predictivity fundamentally

This is not a critique from outside the program — it is the program's architect acknowledging a deep conceptual cost of the fakeon prescription.

## Average Continuation

QG+F does NOT prohibit working in Euclidean signature. It prohibits the standard *analytic* continuation between Euclidean and Lorentzian. The fakeon uses "average continuation" (Anselmi, JHEP 2018; arXiv:1801.00915) — a nonanalytic but well-defined operation where amplitudes are obtained by (nonanalytically) Wick-rotating their Euclidean versions, taking the average of limits from different directions rather than analytic continuation. This provides a systematic Euclidean→Lorentzian extraction procedure that handles complex poles.

## Comparison with Other Approaches

- **String theory:** Excellent analytic S-matrix properties. Full analyticity, crossing symmetry, bootstrap consistency.
- **LQG:** Doesn't use S-matrices (background-independent formulation).
- **Causal set theory:** No S-matrix formulation.
- **Asymptotic safety:** **Also has non-standard analytic structure** — ghost poles obstruct standard Wick rotation (Donoghue 2020), infinite pole towers at imaginary p² (Draper et al. 2020), Bonanno et al. (2022) must *assume* Wick rotation works. The supposed contrast with QG+F is a false premise. See `../cross-cutting/qgf-vs-as-analyticity-compatibility.md` for the full reconciliation analysis.

QG+F is the only major QG approach to **explicitly acknowledge and systematically handle** the analyticity sacrifice, but AS faces the same underlying issue.

## Significance

The analyticity sacrifice is MAJOR — it means QG+F cannot use the most powerful modern techniques for constraining scattering amplitudes. Understanding WHY analyticity must be sacrificed (and what replaces it as an organizing principle) could reveal a new framework. The analyticity-unitarity trade-off may itself be a new physical principle unique to theories with purely virtual particles.

This is closely connected to the fakeon's physical interpretation and microcausality violation — see `core-idea.md` (open problems), `microcausality-and-novel-signatures.md`, and `qcd-analogy-ghost-confinement.md`.

Sources: Anselmi et al., JHEP 05, 2025, 145 (arXiv:2503.01841); Anselmi, arXiv:2601.06346 (Jan 2026); Anselmi, JHEP 06, 058 (2022)

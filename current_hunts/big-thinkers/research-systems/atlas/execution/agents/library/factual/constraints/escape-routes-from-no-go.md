---
topic: constraints/analysis
confidence: verified
date: 2026-03-24
source: exploration-001-escape-routes-survey (strategy-002)
---

# Escape Routes from the Ghost/d_s=2 No-Go Theorem: Ranked Survey

## Context

The no-go theorem (`structural/ghost-spectral-dimension-no-go.md`) proves that {ghost freedom + Lorentz invariance + d_s = 2} are mutually incompatible for standard propagator structures. The constraint stack {d_s = 2, Lorentz invariance, diffeomorphism invariance, renormalizability} uniquely selects quadratic gravity with fakeon quantization (QG+F). This survey systematically investigates all 5 escape routes — relaxing each assumption in turn — to map what theory space remains.

**Key result: All 5 routes are OPEN.** None is empty. But they differ dramatically in how much novel theory space they open and how promising that space is.

## Ranked Verdicts

| Rank | Route | Verdict | Theory Space | Novelty Potential | Key Risk |
|------|-------|---------|-------------|-------------------|----------|
| 1 | **Route 5: Alternative Axioms** | OPEN | Large | Highest | Underdetermined without additional constraints |
| 2 | **Route 4: Relax Locality** | **CLOSED** | None (collapses to QG+F) | None | LW/CLOP unitarity definitively fails; fakeon prescription → QG+F |
| 3 | **Route 2: Relax Renormalizability (AS)** | OPEN | Moderate | Medium | SINGLETON risk — may reduce to QG+F |
| 4 | **Route 3: Relax d_s = 2** | OPEN | Vast | Low-Medium | Too underconstrained without replacement axiom |
| 5 | **Route 1: Relax Lorentz Invariance** | OPEN (narrow) | Small | Low | Super-Planckian LIV bounds; HL essentially unique |

## Route Summaries

### Route 1: Relax Lorentz Invariance — OPEN but NARROW

Anisotropic scaling z = 3 (giving d_s = 1 + D/z = 2 for D = 3) essentially selects Horava-Lifshitz gravity as the unique gravitational framework. The U(1) extension resolves the scalar mode pathologies, making HL self-consistent. But GRB 221009A LIV bounds already exceed E_Pl for n = 1, requiring any Planck-scale linear LIV to be experimentally dead. No convincing mechanism for emergent Lorentz invariance with adequate suppression has been demonstrated. See `horava-lifshitz/core-idea.md`.

### Route 2: Relax Strict Renormalizability (Asymptotic Safety) — OPEN with SINGLETON risk

AS provides d_s = 2 naturally from eta_N = -2, robust across all truncations. The Sen-Wetterich-Yamada (2022) result finds *two distinct* fixed points in the full fourth-order truncation — asymptotically free (Stelle theory) and asymptotically safe (NGFP). The bimetric structure opens largely unexplored theory space. A 2025 tension with Swampland conjectures could differentiate AS from string theory. However, there is significant risk that AS and QG+F describe the same physical theory from different perspectives. See `asymptotic-safety/swy-two-fixed-points.md`.

### Route 3: Relax d_s = 2 Exactly — OPEN but UNDERCONSTRAINED

The "universality" of d_s -> 2 is approximate at best: CDT gives ~1.80 +/- 0.25 (or ~3/2 in newer measurements), LQG gives 1 or 2 depending on coherent state, CST gives d_mm ~ 2.38. Relaxing d_s = 2 to d_s in [1.5, 2.5] removes the uniqueness constraint entirely — multiple propagator structures, all existing QG programs become candidates, continuous families parameterized by d_s. But this loses the constructive power of the sharp axiom. Best used in combination with Route 5: start from alternative axioms, predict d_s as output.

### Route 4: Relax Locality — CLOSED (collapses to QG+F)

The no-go theorem applies to entire functions (which have no poles). Meromorphic propagators (with complex conjugate poles) escape it mathematically. However, the physical viability of this loophole has been **definitively resolved negatively**: the CLOP prescription fails unitarity (Kubo-Kugo 2023), breaks Lorentz invariance (Nakanishi 1971, confirmed 2025), and has a non-Hermitian classical limit (Anselmi 2022). Modesto (the creator of LW QG) co-authored the 2025 paper concluding only the fakeon prescription works (arXiv:2503.01841). With the fakeon prescription, the four-derivative version IS QG+F; the six-derivative version is a super-renormalizable extension with more free parameters. **This route does not yield any theory independent of QG+F.** See `lee-wick-gravity/` for full details.

### Route 5: Replace d_s with Alternative Constructive Axioms — OPEN and MOST PROMISING

The only route that changes the *starting point* rather than modifying an assumption. Four information-theoretic axioms identified as viable constructive foundations: (1) Positivity of relative entropy, (2) Maximal vacuum entanglement hypothesis, (3) Quantum focusing condition, (4) Entropic action principle. These are physically well-motivated, mathematically sharp, do not presuppose d_s = 2 (but may predict it), and have not been systematically explored as axioms for UV-complete theories. See `cross-cutting/information-theoretic-constructive-axioms.md`.

## Cross-Cutting Insights

1. **The most novel theories will likely combine multiple routes.** E.g., Route 5 (information-theoretic axioms) + Route 2 (AS) could yield a theory from entropic principles that naturally predicts the NGFP. Note: Route 4 (Lee-Wick) is now closed — meromorphic propagators require the fakeon prescription, collapsing to QG+F.

2. **d_s should be a prediction, not an axiom.** Start from alternative axioms (Route 5) and see what d_s the resulting theory predicts. If it predicts d_s = 2, connect to QG+F. If d_s != 2, genuinely novel.

3. **The fakeon prescription is the key benchmark.** Every new theory must be compared to QG+F. Novelty is measured by prediction differences from QG+F.

4. **Information-theoretic foundations are the frontier.** 2024-2025 literature shows a clear trend: entropic gravity, holographic entanglement, quantum focusing. This is where genuinely new theories are most likely to be found.

## Specific Novel Theory Candidates Identified

1. **Entropic-action QG** (Bianconi 2025, Phys. Rev. D): Gravity = quantum relative entropy S(rho_metric || rho_matter). Predicts emergent Lambda and G-field dark matter. Very new, not yet widely scrutinized.
2. **~~Lee-Wick QG~~** — ELIMINATED. CLOP prescription fails unitarity and Lorentz invariance (Kubo-Kugo 2023, Anselmi+Modesto 2025). With fakeon prescription, collapses to QG+F (4-deriv) or a super-renormalizable variant (6-deriv). Not a novel independent candidate.
3. **Info-theoretic QG from Holographic Emergence Bound** (2025): Starting from positivity of relative entropy + unitary modular flow + QFC. The bound exists but no one has constructed a UV-complete theory from these axioms.
4. **Thermodynamic UV completion from Jacobson's framework**: Extend maximal vacuum entanglement hypothesis to the UV by specifying a particular entanglement structure at the Planck scale. Framework exists (Jacobson 2015) but UV extension not systematically explored.

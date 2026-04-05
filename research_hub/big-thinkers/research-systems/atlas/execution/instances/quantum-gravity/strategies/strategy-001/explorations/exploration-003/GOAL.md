# Exploration 003: Quadratic Gravity + Fakeon — Validation, Predictions, and Novelty Assessment

## Mission Context

We are building a novel quantum gravity theory. Exploration 002 showed that requiring spectral dimension d_s = 4 → 2 (a convergent result across 7+ QG approaches) + Lorentz invariance + diffeomorphism invariance + renormalizability uniquely selects the quadratic gravity action with fakeon quantization:

**S = ∫ d⁴x √(-g) [ (M_P²/2)(R - 2Λ) - (1/2f₂²) C_μνρσ C^μνρσ + (1/6f₀²) R² ]**

with the massive spin-2 ghost (mass M₂ = f₂ M_P/√2) quantized as a "fakeon" (Anselmi-Piva prescription) and the massive scalar (mass M₀ = f₀ M_P/√6) as a normal particle or fakeon.

This theory has only 2 new parameters beyond GR (M₂ and M₀). It is renormalizable and unitary. Now we need to validate it and find its novel predictions.

## Your Goal

Three tasks, in order of priority:

### Task 1: Novelty Assessment (CRITICAL)

Determine whether this theory — quadratic gravity with Anselmi-Piva fakeon prescription — is already a well-developed research program or if our constraint-driven derivation adds genuine novelty.

Specifically:
- How far has Anselmi's group (and others) developed this theory? Have they already computed the graviton propagator IR limit, post-Newtonian corrections, BH entropy, cosmological predictions?
- Is our derivation approach new? (Starting from d_s = 2 as axiom → deriving the action, rather than starting from the action → checking d_s)
- What aspects are genuinely novel vs. already known?
- Are there open problems in this program where our constraint-driven approach could contribute?

### Task 2: Tier 2-3 Validation

Check whether the theory passes these tests:
- **Graviton propagator IR limit:** Does G(p²) → GR propagator as p → 0? (Expected: yes by construction)
- **Newton's law recovery:** Does V(r) = -GM/r + corrections? What are the corrections?
- **Post-Newtonian parameters:** γ = 1, β = 1? (Within Cassini bounds |γ-1| < 2.3×10⁻⁵)
- **GW speed:** c_gw = c? (Within |c_gw/c - 1| < 6×10⁻¹⁵)
- **Graviton mass:** Zero (massless graviton + massive fakeon that doesn't propagate)
- **Bekenstein-Hawking entropy:** Can the theory reproduce S = A/(4G)? If not, what does it predict?
- **Lorentz invariance:** Preserved by construction (the theory is Lorentz-invariant)

### Task 3: Novel Predictions (Tier 4)

Identify predictions this theory makes that:
- Differ from standard GR
- Are potentially testable
- Are quantitative (numbers, not vague claims)

Candidate predictions to investigate:
- **Modified Newtonian potential:** V(r) = -GM/r × [1 + (1/3)exp(-M₀r) - (4/3)exp(-M₂r)] — what is the experimental signature?
- **Inflation:** Starobinsky inflation naturally arises from the R² term. What does the fakeon prescription add?
- **Cosmological constant:** Does the theory address the CC problem?
- **Scattering cross sections:** How do graviton scattering amplitudes differ from GR above the fakeon mass?
- **Microcausality violation:** What are its observable consequences?
- **Spacetime fluctuations:** Could GQuEST or LIGO detect signatures of the fakeon?
- **Primordial gravitational waves:** Predictions for tensor-to-scalar ratio r?

**IMPORTANT: Write your report incrementally, section by section. After every 2-3 findings, write to REPORT.md. Do NOT try to write the entire report at once.**

## Success Criteria

- Clear assessment of novelty (what's new vs. what's known)
- At least 3 validation tests checked with explicit calculations or references
- At least 1 quantitative novel prediction identified with a specific number or range
- Identification of what the open problems are in this program

## Failure Criteria

- Only reviewing the theory without checking against experimental bounds
- No assessment of novelty
- No quantitative predictions

## Output

Write to:
- `explorations/exploration-003/REPORT.md` (detailed — write incrementally!)
- `explorations/exploration-003/REPORT-SUMMARY.md` (concise — write last)

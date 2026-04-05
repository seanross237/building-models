# Exploration 002: Spectral Dimension as Constructive Axiom — What Does d_s = 4 → 2 Force?

## Mission Context

We are building a novel quantum gravity theory using a constraint-driven approach. Exploration 001 mapped 32 constraints for quantum gravity, identifying **spectral dimension running from d_s = 4 to d_s ≈ 2 in the UV** as one of the most promising underexploited constraints — it appears across 7+ independent approaches (CDT, asymptotic safety, string theory, LQG, Horava-Lifshitz, causal sets, noncommutative geometry) but is rarely used as a *starting axiom* for theory construction.

## Your Goal

Investigate what mathematical structures are *forced* by requiring the spectral dimension to flow from d_s = 4 in the IR to d_s = 2 in the UV. This is a constructive investigation — we want to work backward from the constraint to the theory, not forward from a theory to check the constraint.

**IMPORTANT: Write your report incrementally, section by section. Do NOT try to write the entire report at once. After every 2-3 web searches or significant findings, write what you've learned to REPORT.md.**

### Specific Questions to Answer

1. **What is the most general modified dispersion relation that produces d_s = 4 → 2?**
   - The spectral dimension is defined via the return probability of a random walk: P(σ) = ∫ d^d p/(2π)^d exp(-σf(p²))
   - d_s(σ) = -2 d ln P(σ)/d ln σ
   - What constraints does d_s(0) = 4, d_s(∞) = 2 place on f(p²)?
   - What is the most general f(p²) compatible with Lorentz invariance (or minimal breaking)?

2. **What propagator modifications give d_s → 2?**
   - If the propagator takes the form G(p²) = 1/f(p²), what f(p²) gives d_s → 2?
   - Is this compatible with ghost freedom (no additional poles)?
   - Is this compatible with unitarity?
   - How does this relate to Infinite Derivative Gravity (IDG), which uses G(p²) ~ exp(p²/M²)/p²?

3. **What action gives rise to this propagator?**
   - Given the forced propagator form, what is the corresponding gravitational action?
   - Can we write S = ∫ d⁴x √(-g) [R + R·F(□/M²)·R + ...] and determine F?
   - What are the ghost-freedom constraints on F?
   - What is the relationship to known actions (Stelle, IDG, asymptotic safety effective action)?

4. **Is there a unique theory, or a family?**
   - Does d_s → 2 plus ghost freedom plus Lorentz invariance narrow the theory to a finite-parameter family?
   - What additional constraints (from our constraint map) would be needed to get a unique theory?
   - What role does diffeomorphism invariance play in constraining the action further?

5. **What are the two common mechanisms for d_s → 2, and do they lead to different mathematical structures?**
   - Carlip identified two: (a) Scale invariance at UV fixed points, (b) Asymptotic silence (light cone collapse)
   - Do these correspond to distinct classes of theories?
   - Can both be realized simultaneously?

### Context from Exploration 001

Key constraints the resulting theory must also satisfy:
- **Unitarity:** S†S = 1, positive spectral weight
- **Ghost freedom:** No negative-norm states; propagator must have no additional poles (or only complex conjugate pairs that cancel in physical amplitudes)
- **Diffeomorphism invariance:** The action must be diff-invariant (or deformed diff-invariant reducing to standard in IR)
- **Lorentz invariance:** Linear LIV scale bounded above E_Pl by GRB 221009A; the theory must preserve Lorentz symmetry or break it only quadratically or softer
- **IR recovery:** Graviton propagator must reduce to GR propagator as p → 0
- **Bekenstein-Hawking entropy:** The theory must account for S = A/(4G)

### What Would Be a Breakthrough

If requiring d_s → 2 + ghost freedom + Lorentz invariance + diffeomorphism invariance produces a *unique* or *nearly unique* gravitational action that is distinct from all known approaches, that would be a major step toward a novel theory.

## Success Criteria

- Clear identification of what class of propagator/action modifications produce d_s → 2
- Assessment of ghost freedom for these modifications
- Identification of how many free parameters remain after imposing d_s → 2 + ghost freedom + Lorentz invariance
- At least one explicit candidate action written down

## Failure Criteria

- Only reviewing what existing approaches say about spectral dimension without working backward from the constraint
- No mathematical analysis of propagator forms
- No assessment of ghost freedom

## Output

Write to:
- `explorations/exploration-002/REPORT.md` (detailed — write incrementally!)
- `explorations/exploration-002/REPORT-SUMMARY.md` (concise — write last)

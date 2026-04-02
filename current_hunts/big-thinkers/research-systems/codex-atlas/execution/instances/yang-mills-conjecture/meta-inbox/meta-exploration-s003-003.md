# Meta-Learning: Exploration 003 (Strategy 003)

## What worked well
- Three parallel proof approaches (Gershgorin, per-plaquette, Fourier) were all tried. Two failed quickly, the third worked. This is the right approach for proof explorations — try multiple, invest in the winner.
- The D+C decomposition emerged organically from the Fourier analysis and is the right framework.
- The cross-term kernel bound (||F|| = 2 exactly) is a beautiful algebraic result with a clean proof.
- Asking the explorer to verify the SZZ normalization was critical — it revealed that the mass gap depends on |λ_min|, not λ_max.

## What didn't work
- The goal didn't specify the sign convention for the Bakry-Émery condition clearly enough. The explorer had to work it out, which cost time.
- The normalization confusion (iσ_a basis vs physicist basis) persists. Should pin this once and for all.
- The computation was slow on d=4 lattices. The explorer could have done more if the d=4 survey was faster (analytical formula vs finite differences).

## Lessons
1. **The mass gap depends on λ_min, not λ_max.** This was NOT obvious and reframes the entire problem. Future goals should focus on the most negative eigenvalue.
2. **The decoherence lemma is the key missing piece.** It's a clean mathematical statement: when you have a sum of tensor products (spatial ⊗ color), the operator norm is maximized when all color factors are aligned (proportional to I₃). This might follow from matrix concentration theory.
3. **Specify sign conventions explicitly.** The Bakry-Émery framework has subtleties about whether V = S or V = -S that change the relevant bound.
4. **The conditional proof structure (prove → identify gap → prove gap) is effective.** It tells us exactly what remains open.

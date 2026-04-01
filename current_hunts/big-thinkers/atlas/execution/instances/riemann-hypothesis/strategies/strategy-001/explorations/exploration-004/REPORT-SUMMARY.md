# Exploration 004 Summary: Trace Formula Reconstruction

## Goal
Test whether the smooth xp spectrum + prime oscillatory corrections can reconstruct the zeta zero spectrum. Compute 2000 zeros, apply explicit formula corrections at P_max = 100, 1000, 10000, and test against GUE constraints.

## What Was Tried
1. Computed 2000 actual zeta zeros (mpmath) and 2000 smooth zeros (inverting N_smooth)
2. Corrected a formula error in GOAL.md (removed spurious ln(p) factor, verified via mpmath)
3. Discovered and explained a constant 0.5 Gibbs offset in the prime sum at zeros
4. Tested linearized and root-finding zero reconstruction for P_max = 10 to 10000
5. Computed GUE statistics (spacing, number variance, level repulsion, form factor) for actual, smooth, and corrected spectra
6. Analyzed convergence of prime sum and structure of residuals

## Outcome: Succeeded (with a negative result)

**Individual zero reconstruction from the explicit formula fundamentally does not work.** This is not a numerical limitation — it's a mathematical obstruction:

- N_osc is a **step function** at the actual zeros (jumps ±1). The prime sum (being a sum of sine functions) converges to the step function's midpoint (Gibbs phenomenon), giving an irreducible 0.5 offset.
- At the smooth zeros, N_osc is **always exactly ±0.5** (mathematical identity from how smooth zeros are defined). The linearized correction δ = -N_osc/N_smooth' gives constant magnitude, destroying level repulsion.
- More primes = **worse** individual zero reconstruction (variance explained: 80% at P_max=10, -6% at P_max=10000).
- Even with **exact** N_osc (from mpmath, not prime sum), Newton iteration fails because it steps over the discontinuity.

**However, for bulk statistics, primes DO help:** Number variance improves 75% vs smooth spectrum.

## Key Takeaway

The trace formula (explicit formula) relates primes to the zero **counting function** N(T), not to individual zero positions. N(T) is a step function, and step functions cannot be reconstructed from Fourier-type sums at their discontinuities. The Berry-Keating framework is correct for spectral density but **insufficient for spectral correlations** — the GUE statistics must come from the operator's structure (eigenvectors, matrix elements), not from the prime sum alone. This is the precise sense in which "something beyond xp + primes is needed."

## Unexpected Findings

1. **Sign prediction is 100% accurate**: The direction of displacement (actual vs smooth) is perfectly predicted by the sign of N_osc at the smooth zeros. The primes know WHICH SIDE the actual zero is on, just not HOW FAR.

2. **Formula error in GOAL.md**: The explicit formula for N_osc does NOT contain a ln(p) factor. This factor belongs in the Chebyshev ψ-function explicit formula, not the zero-counting formula. With ln(p), the approximation error is 30× worse.

3. **Convergence exponent is -0.13**: The prime sum residual decays as P_max^{-0.13}, far slower than the P_max^{-0.5} expected from random cancellation. This matches the Gibbs phenomenon's characteristic slow convergence for step functions.

## Computations Identified

1. **Non-linear zero reconstruction**: Instead of the linearized formula, solve the full implicit equation N_smooth(t) + S_prime(t) = n - 0.5 using the PRINCIPAL VALUE of the prime sum (Cesàro or Abel summation to tame Gibbs). This might work where ordinary summation fails. Difficulty: moderate (100-line scipy script with careful summation).

2. **Spectral determinant approach**: Compute ξ(s) = (s/2)(s-1)π^{-s/2}Γ(s/2)ζ(s) directly from its Hadamard product over zeros, and compare to a product over primes. This bypasses the counting function entirely. Difficulty: moderate (Hadamard product convergence is tricky).

3. **Higher-order trace formula**: The pair correlation is related to a TWO-POINT trace formula involving pairs of primes. Computing this explicitly and testing against Montgomery's conjecture would directly test whether primes determine correlations, not just density. Difficulty: substantial (requires careful handling of diagonal and off-diagonal terms).

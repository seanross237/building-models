# Exploration 002 Summary: What Does d_s = 4 → 2 Force?

## Goal
Investigate what mathematical structures are *forced* by requiring the spectral dimension to flow from d_s = 4 (IR) to d_s = 2 (UV), combined with ghost freedom, Lorentz invariance, and diffeomorphism invariance. Work backward from constraint to theory.

## What Was Tried
Systematic mathematical analysis: derived the general relationship between f(p²) (the modified d'Alembertian eigenvalues) and spectral dimension using the heat kernel return probability framework. Computed what UV behavior of f(p²) is required for d_s = 2. Analyzed ghost-freedom constraints using Hadamard factorization theorem and Källén-Lehmann spectral representation. Classified all escape routes from the resulting no-go theorem.

## Outcome: **Succeeded — with a major finding**

### Key Finding: The No-Go Theorem
**Ghost-free Lorentz-invariant theories cannot produce d_s = 2.** In d = 4 dimensions, d_s = 2 requires f(p²) ~ (p²)², i.e., the propagator must fall as 1/p⁴. Ghost freedom requires f(p²)/p² to be an entire function with no zeros, but by Hadamard's theorem, such functions grow at least exponentially — they cannot grow as a polynomial like p². Additionally, the Källén-Lehmann bound states that local QFT propagators satisfying spectral positivity cannot fall faster than 1/p². All ghost-free nonlocal theories (IDG, etc.) give d_s → 0, not d_s = 2.

### Key Finding: Unique Theory Selection
The constraint stack {d_s = 4→2, Lorentz invariance, diffeomorphism invariance, renormalizability} uniquely selects **Stelle's quadratic gravity action**:

S = ∫ d⁴x √(-g) [M_P² R/2 - (1/2f₂²) C_μνρσ C^μνρσ + (1/6f₀²) R² - Λ]

with the massive spin-2 ghost resolved via **Anselmi-Piva fakeon quantization**. This theory is renormalizable, unitary (with fakeon prescription), has d_s = 4→2, and introduces only **2 new parameters** (the spin-2 fakeon mass M₂ and scalar mass M₀) beyond GR.

### Key Finding: The Table
| Theory | d_s (UV) | Ghost-free? | Lorentz inv.? |
|--------|----------|-------------|---------------|
| GR | 4 | ✓ | ✓ |
| **Stelle + Fakeon** | **2** | **✓ (fakeon)** | **✓** |
| IDG (exponential) | 0 | ✓ | ✓ |
| Hořava-Lifshitz z=3 | 2 | ✓ | ✗ |
| Lee-Wick (1 pair) | 4/3 | ~ | ✓ |

## Key Takeaway
**The spectral dimension constraint d_s = 4→2, treated as a constructive axiom rather than a consistency check, is powerful enough to essentially determine the gravitational action.** It forces quadratic curvature terms, which (by Gauss-Bonnet in 4D) leave exactly 2 free parameters. The unavoidable ghost must be resolved by the fakeon prescription. This yields a renormalizable, unitary quantum gravity theory that is far more constrained than usually appreciated.

## Leads Worth Pursuing
1. **Bekenstein-Hawking entropy** — does quadratic gravity with fakeons reproduce S = A/4G? This could fix one of the 2 remaining parameters.
2. **Asymptotic safety connection** — the fakeon theory's asymptotic freedom in f₂ may connect to the asymptotic safety UV fixed point. Are they the same theory from different perspectives?
3. **Cosmological predictions** — what does the quadratic gravity fakeon theory predict for the CMB, inflation, and the cosmological constant?
4. **The fakeon mass M₂** — is it predicted by any combination of other constraints?

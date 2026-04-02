# Exploration 006 Summary: Black Hole Entropy in Quadratic Gravity + Fakeon

## Goal
Compute black hole entropy for the quadratic gravity action with Anselmi-Piva fakeon quantization. This was the last open validation test (7th of 7) for the theory selected by the spectral dimension constraint.

## What Was Done
- Computed the Wald entropy formula explicitly for the quadratic gravity action (R + alpha R^2 + beta C^2)
- Analyzed black hole solutions in quadratic gravity (Schwarzschild and non-Schwarzschild branches, from Lu-Perkins-Pope-Stelle 2015)
- Determined the impact of the fakeon prescription on BH solutions and thermodynamics
- Estimated numerical corrections for astrophysical and Planck-scale BHs
- Assessed whether entropy constrains the free parameters
- Connected BH entropy to the spectral dimension d_s = 2
- Discovered a striking result about ghost-driven BH phase transitions (Buccio et al. 2025)

## Outcome: SUCCEEDED — Clean positive result

### The Wald entropy of Schwarzschild in quadratic gravity is exactly A/(4G)

Both higher-derivative corrections vanish on the Schwarzschild background:
- R^2 correction = 0 (because R = 0 on Schwarzschild)
- C^2 correction = 0 (the parameter-dependent part vanishes because f_1 r_0 = 1 on Schwarzschild; only a topological constant from the Gauss-Bonnet piece remains, which doesn't affect any observable)

This result holds for ALL values of the coupling constants — no fine-tuning needed.

### The fakeon eliminates non-Schwarzschild black holes

The non-Schwarzschild solutions (discovered by Lu et al. 2015) carry massive spin-2 Yukawa hair. In the fakeon theory, the massive spin-2 mode is purely virtual, so these solutions are unphysical. This is consistent with their independently-established instability.

### The fakeon prevents catastrophic ghost instabilities in BH evaporation

Recent work (Buccio et al., May 2025) shows that in standard quantization, evaporating Schwarzschild BHs undergo a ghost-driven phase transition at M ~ M_P, acquiring ghost Yukawa hair and potentially forming naked singularities. The fakeon prescription prevents this entirely.

### For astrophysical BHs, corrections are negligible

Higher-derivative corrections are suppressed by exp(-m_2 r_0) ~ exp(-10^46). The one-loop logarithmic correction is O(1) vs S ~ 10^77.

## Key Takeaway

**The 7th validation test is now passed.** The quadratic gravity + fakeon theory gives S = A/(4G) for Schwarzschild BHs, with the fakeon prescription providing the additional benefit of eliminating pathological non-Schwarzschild solutions and ghost-driven BH instabilities. The theory is now 7/7 on validation tests (with the tensor-to-scalar ratio r in [0.0004, 0.0035] as a testable prediction, not a pass/fail test).

## Leads Worth Pursuing
1. **Explicit one-loop BH entropy with fakeon prescription** — the Euclidean continuation of the fakeon Green's function for the BH partition function hasn't been worked out
2. **Kerr BH entropy** — the C^2 correction may be non-zero for rotating BHs (though negligible for astrophysical BHs)
3. **Sub-area-law entropy at the Planck scale** — the d_s = 2 UV behavior suggests entropy crosses over from area-law to sub-area-law for M ~ M_P
4. **The fakeon vs. IHO ghost resolution** — recent IHO approach (arXiv:2603.07150) may give different BH evaporation predictions; worth comparing

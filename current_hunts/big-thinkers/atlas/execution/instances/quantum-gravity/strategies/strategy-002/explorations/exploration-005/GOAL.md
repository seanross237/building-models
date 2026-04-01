# Exploration 005: Compute n_s from QG+F Physical Beta Functions

## Mission Context

We are developing a novel quantum gravity theory. Exploration 004 revealed that the n_s tension (QG+F predicts ~0.967, data suggests ~0.974 when DESI BAO is included) could be resolved by RG running of the R² coupling during inflation. A 2024 PRL paper (Branchina et al.) derived gauge-invariant physical beta functions for quadratic gravity for the first time. The question is: does the actual running of couplings in QG+F produce enough shift in n_s to resolve the tension?

This exploration has two sub-goals: (A) attempt the RG running calculation, and (B) construct the six-derivative gravity extension as an alternative.

## Your Specific Goal

### Part A: QG+F RG Running and n_s

**Task A1: Find and Reconstruct the Beta Functions**
- Find the 2024 PRL paper by Branchina, Ferrara, and collaborators on physical beta functions for quadratic gravity
- What are the gauge-invariant, scheme-independent beta functions for the couplings in S = ∫d⁴x√(-g)[M²_P R/2 - (1/2f₂²)C² + (1/6f₀²)R²]?
- The key coupling for n_s is f₀ (the R² coupling). What is β(f₀)?
- Also find: Fradkin-Tseytlin (1982) original beta functions. How do they compare to the new physical ones?

**Task A2: Estimate n_s Including Running**
- In Starobinsky inflation, n_s = 1 - 2/N where N is the number of e-folds
- With running R² coupling: the effective number of e-folds changes because the potential shape changes
- The slow-roll parameter ε = (V'/V)² × M²_P/2 gets corrections from the running coupling
- Estimate the shift: Δn_s = n_s(with running) - n_s(without running)
- Is |Δn_s| ≈ 0.007 (what's needed to resolve the tension)?
- Is the sign correct (positive shift)?

**Task A3: What's the Key Uncertainty?**
- Is the calculation well-defined at one loop?
- What about two-loop corrections?
- Does the fakeon prescription modify the beta functions?
- How does the running of f₂ (the C² coupling) affect things?

### Part B: Six-Derivative Extension

**Task B1: The Six-Derivative Action**
- Write down the most general six-derivative gravitational action: S = S_QG + α₁R³ + α₂R R_μν R^μν + α₃R_μν R^νρ R^ρ_μ + α₄R_μνρσ∇²R^μνρσ + ...
- How many independent sixth-order terms are there in 4D?
- Does the six-derivative theory preserve renormalizability? (It should be super-renormalizable)
- Does it require the fakeon prescription? (Yes — for the spin-2 ghosts)

**Task B2: Inflationary Predictions**
- The R³ term modifies the Starobinsky potential
- The paper arXiv:2505.10305 reportedly shows R³ resolves the n_s tension with δ₃ ≈ −10⁻⁴
- Find this paper and verify: what is the modified n_s as a function of δ₃?
- Is δ₃ ≈ −10⁻⁴ natural from the six-derivative theory's parameters?
- What is the predicted r in this case?

**Task B3: Novelty and Relation to QG+F**
- Is six-derivative QG with fakeon a genuinely different theory from four-derivative QG+F?
- Same action class (polynomial in curvature + fakeon) — but different predictions?
- What are the extra parameters beyond QG+F? How many?
- Is this theory being actively studied? By whom?

### Part C: Synthesis
- Compare the RG running approach (Part A) with the six-derivative approach (Part B)
- Which is more natural? Which has fewer free parameters?
- Could both effects contribute simultaneously?
- What is the sharpest prediction that could distinguish between: (1) pure QG+F (n_s ≈ 0.967), (2) QG+F with RG running, (3) six-derivative QG+F?

## Success Criteria
- Explicit beta functions for f₀ and f₂ with references
- Numerical estimate of Δn_s from RG running (even if approximate)
- Assessment of whether the running naturally resolves the tension
- Clear comparison of the two approaches

## Failure Criteria
- Vague discussion without actual numbers
- Not finding the 2024 PRL paper
- Confusing gauge-dependent and gauge-invariant beta functions

## Relevant Context

**QG+F action:** S = ∫d⁴x√(-g)[M²_P R/2 - (1/2f₂²)C² + (1/6f₀²)R²]
- f₀: R² coupling (dimensionless). Controls inflaton mass M₀ = f₀ M_P/√6
- f₂: C² coupling (dimensionless). Controls fakeon mass M₂ = f₂ M_P/√2
- Both are asymptotically free: f₀,f₂ → 0 as E → ∞

**Starobinsky inflation from R²:**
- Effective scalar potential: V(φ) = (3M²_P M²₀/4)(1 - e^{-√(2/3)φ/M_P})²
- n_s = 1 - 2/N for large N (N = 50-60)
- r = 12/N² ≈ 0.003

**The physical beta functions paper:** Branchina et al. (2024, PRL). Derived gauge-invariant, scheme-independent beta functions for quadratic gravity. This resolves a long-standing ambiguity: previous beta functions (Fradkin-Tseytlin, Avramidi-Barvinsky) were gauge-dependent.

**The n_s tension (from exploration 004):**
- CMB alone: n_s = 0.969 ± 0.003 (barely 1σ tension)
- CMB + DESI: n_s = 0.974 ± 0.003 (2.3σ, up to 3.9σ)
- Resolution needed: Δn_s ≈ +0.007

## Instructions
- Write to `explorations/exploration-005/REPORT.md` after every significant finding
- Write summary to `explorations/exploration-005/REPORT-SUMMARY.md` when done
- This is exploration-005, NOT any other exploration
- Be quantitative — we need actual numbers, not qualitative statements

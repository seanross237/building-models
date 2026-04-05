# Exploration 003: Conditional C(F₄) Bound + Multi-IC Slack Validation

## Mission Context

Strategy-001 found an empirical correlation C_{L,eff}/C_L ~ F₄^{-0.30} between the effective Ladyzhenskaya constant and vorticity flatness F₄, with correlation r = -0.93. Strategy-002 exploration-001 massively validated the BKM enstrophy bypass. Exploration-002 proved the BKM theorem modulo one gap.

Two open questions remain:
1. Can the C(F₄) empirical correlation be given a theoretical basis? (Direction B from STRATEGY.md)
2. Are the Strategy-001 slack atlas findings IC-robust? (Direction C from STRATEGY.md)

## Goal

Two tasks in one exploration (they share the DNS infrastructure):

### Task A: Derive and test C(F₄) bound

**Theory:** The Ladyzhenskaya inequality ||u||⁴_{L⁴} ≤ C_L⁴ ||u||_{L²} ||∇u||³_{L²} has its optimizer at a concentrated Dirac-like function. For fields with bounded vorticity flatness F₄ = ||ω||⁴_{L⁴} / (||ω||²_{L²})², this optimizer is excluded. The question: does F₄ ≤ M imply C_{L,eff} ≤ g(M) · C_L for some explicit function g(M) < 1?

**Specific computations:**
1. On a grid of N=64, generate 1000+ random div-free vector fields on T³ with controlled flatness F₄ (by mixing broad-spectrum fields with concentrated patches)
2. For each field, compute C_{L,eff} = ||f||_{L⁴}/(||f||_{L²}^{1/4}||∇f||_{L²}^{3/4})
3. Plot C_{L,eff}/C_L vs F₄ and fit the relationship
4. Check if C_{L,eff} ≤ A · F₄^{-β} for some constants A, β > 0
5. Attempt a PROOF: For F₄ ≤ M, can you bound C_{L,eff} rigorously using the relation between L⁴, L², and flatness?

**Proof approach hint:** F₄ = ||f||⁴_{L⁴}/(||f||²_{L²})², so ||f||⁴_{L⁴} = F₄ · (||f||²_{L²})². The Ladyzhenskaya optimizer has F₄ → ∞ (concentration). For F₄ ≤ M, the field is "spread out" and can't approach the optimizer. This should give C_{L,eff}⁴ ≤ C_L⁴ · h(F₄) for some decreasing function h.

### Task B: Multi-IC slack atlas validation

**Specific computations:**
1. Run the full 8-inequality slack atlas (from Strategy-001) on:
   - Random-phase Gaussian at Re=500, 1000
   - Kida vortex at Re=500, 1000
   - The adversarial anti-parallel tubes (σ=2.5) at Re=500, 1000
2. For each IC+Re combination, compute:
   - All 8 inequality slacks (vortex stretching, Prodi-Serrin, Kato-Ponce, Agmon, CZ pressure, Sobolev, Ladyzhenskaya, energy)
   - The 3-factor decomposition (α_geom × α_Lad × α_sym)
   - BMO/L^∞ ratio
   - C_{L,eff}/C_L
   - The C(F₄) relationship
3. Report: which Strategy-001 findings are IC-robust and which are TGV-specific?

## Existing Code

- NS solver: `../../strategy-001/explorations/exploration-002/code/ns_solver.py`
- Slack measurements: `../../strategy-001/explorations/exploration-002/code/slack_measurements.py`
- BKM comparison: `../exploration-001/code/bkm_comparison.py`

Copy and adapt these.

## Success Criteria

**Task A succeeds if:**
- C_{L,eff} vs F₄ relationship is measured on 500+ random fields
- A rigorous bound C_{L,eff} ≤ f(F₄) · C_L is proved, OR the proof breaks at a specific identified step
- The empirical -0.30 exponent from Strategy-001 is tested on new data

**Task B succeeds if:**
- Full slack atlas computed for ≥3 new ICs at ≥2 Re values
- Each Strategy-001 finding is classified as IC-robust (same ordering and similar magnitudes) or IC-specific

## Output

Write REPORT.md and REPORT-SUMMARY.md in this directory. Code in code/.

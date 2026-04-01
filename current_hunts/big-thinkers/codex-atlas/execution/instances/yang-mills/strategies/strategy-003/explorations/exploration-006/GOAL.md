# Exploration 006: Full Operator M(Q) ≼ M(I) Verification + Pure Gauge Characterization

## Mission Context
This is a YANG-MILLS mission (strategy-003). Do not confuse with other missions.

## Background

**Target inequality:** M(Q) ≼ M(I) as positive semidefinite operators on ⊕_e su(N), where M(Q) = ∑_□ B_□(Q,·) B_□(Q,·)^T.

Equivalently: ALL eigenvalues of M(Q) - M(I) are ≤ 0.

**Phase 1 findings:**
- E002 found: F(Q) = λ_max(M(Q)) = 4d = 16 iff Q is a PURE GAUGE configuration. Non-pure-gauge has F < 4d.
- E004 confirmed: λ_max(M(Q)) ≤ 4d for all 50+ L=4 configs tested.
- GOAL.MD B_□ formula had errors — use the corrected formula from E001 (verified by finite differences).

**Critical question 1:** Does M(Q) ≼ M(I) hold as an OPERATOR inequality (all eigenvalues, not just max)?
**Critical question 2:** Is the characterization "F = 4d iff pure gauge" provable?

**Convention:** Use corrected B_□ formula. SU(2) generators τ_a = iσ_a/2. For link (x,μ), the B_□ formula for plaquette □ = (x,μ,ν) is:
  B_□(Q,v) = Ã₁ + Ã₂ + Ã₃ + Ã₄ where signs/transport come from the corrected holonomy formula (verify against Q=I: should give discrete curl ω).

## Task 1 (Priority 1): Full Spectrum of M(Q) - M(I) for 50+ Configurations

For each Q configuration:
1. Build M(Q) = ∑_□ B_□ B_□^T (a 192×192 matrix at L=2, or use L=2 for speed)
2. Build M(I) = K_curl (the discrete curl Gram matrix at Q=I)
3. Compute eigenvalues of D(Q) = M(Q) - M(I) using numpy.linalg.eigvalsh
4. Report: are ALL eigenvalues of D(Q) ≤ 0? What is the largest eigenvalue of D(Q)?

**If any eigenvalue of D(Q) > 0 for any Q:** This is a counterexample to M(Q) ≼ M(I). REPORT IMMEDIATELY.

**Configurations to test (50+):**
- 5 pure gauge: Q = g·I·g⁻¹ for random gauge transforms g (should give D(Q) = 0 exactly)
- 20 random Haar Q
- 10 Gibbs samples at β = 0.5, 1.0, 2.0, 3.0
- 10 near-identity: Q = exp(ε A) for random A ∈ su(2)^64, ε ∈ {0.01, 0.1, 0.5}
- 5 adversarial: start from near-identity, use gradient ascent on λ_max(D(Q))

### IMPORTANT: Verify corrected B_□ formula first
Before any scan, verify M(I) = K_curl exactly (within numerical precision 1e-10). If M(I) ≠ K_curl, the B_□ formula is wrong — debug before proceeding.

Expected: M(I)_{(x,μ,a),(y,ν,b)} = (K_curl)_{(x,μ,a),(y,ν,b)} = ∑_□ [sign(x,μ)∈□ × sign(y,ν)∈□] × δ_{ab}

## Task 2 (Priority 2): Pure Gauge Characterization

E002 found: F(Q) = λ_max(M(Q)) = 4d iff Q is pure gauge (all plaquette holonomies = I).

Test this numerically:
1. Generate 20 pure gauge Q = {g_x Q_{x,μ} g_{x+ê_μ}⁻¹} for random g_x ∈ SU(2)
2. Verify F(Q) = 4d for all pure gauge Q
3. Generate 20 non-pure-gauge Q (random Q with non-trivial holonomies)
4. Verify F(Q) < 4d for all non-pure-gauge Q

Also test: **Is D(Q) = 0 for pure gauge Q?** (i.e., M(Q) = M(I) exactly for pure gauge)

If yes: pure gauge ↔ D(Q) = 0, which would mean the operator M(Q) depends only on the gauge field (plaquette holonomies), not the specific Q configuration. This would be a key structural result.

### Analytical argument for pure gauge:
For Q_e = g_{s(e)} g_{t(e)}⁻¹ (pure gauge), the plaquette holonomy U_□ = g_x g_x⁻¹ = I. The B_□ formula:
  B_□(Q,v) = v_1 + Ad_{g_{x}g_{x}⁻¹}(v_2) + ... = v_1 + v_2 - v_3 - v_4 (since all Ad = Ad_I = identity)

Wait — but for pure gauge Q_e = g_x g_y⁻¹, the adjoint transport Ad_{g_x g_y⁻¹} is NOT the identity unless g_x = g_y. Reconsider:

For pure gauge Q_{x,μ} = g_x g_{x+ê_μ}⁻¹:
  Ã₁ = v_{x,μ}
  Ã₂ = Ad_{Q_{x,μ}}(v_{x+ê_μ,ν}) = Ad_{g_x g_{x+ê_μ}⁻¹}(v_{x+ê_μ,ν})

Is there a gauge-transformed frame where this looks like Q=I? Yes — under the gauge transformation h_x = g_x⁻¹, we get Q̃_{x,μ} = h_x Q_{x,μ} h_{x+ê_μ}⁻¹ = g_x⁻¹ · g_x g_{x+ê_μ}⁻¹ · g_{x+ê_μ} = I. And the tangent vectors transform as ṽ_{x,μ} = Ad_{g_x⁻¹}(v_{x,μ}).

So B_□(Q, v) = Ad_{g_x}(B_□(I, Ad_{g⁻¹} v)) = Ad_{g_x}(ω_□(ṽ))

Thus |B_□(Q,v)|² = |Ad_{g_x}(ω_□(ṽ))|² = |ω_□(ṽ)|² (isometry).

Sum: ∑_□ |B_□(Q,v)|² = ∑_□ |ω_□(ṽ)|² where ṽ_{x,μ} = Ad_{g_x⁻¹}(v_{x,μ}) and |ṽ|² = |v|² (isometry).

So M(Q_pure) = Ad_{g⁻¹}^T M(I) Ad_{g⁻¹} which is ISOMETRIC to M(I), hence has the same eigenvalues. In particular λ_max(M(Q_pure)) = λ_max(M(I)) = 4d.

**This is an ANALYTICAL PROOF that M(Q_pure) is isospectral with M(I)**. Verify this numerically and write it up.

## Task 3 (Priority 3): Gradient Ascent on λ_max(D(Q))

Search for Q that MAXIMIZES the largest eigenvalue of D(Q) = M(Q) - M(I).

If D(Q) ≼ 0 always, gradient ascent should plateau at 0 (achieved by pure gauge). Use:
1. Start from 10 random Q configurations
2. Compute gradient ∂λ_max(D)/∂Q_{x,μ} (using eigenvector perturbation theory)
3. Ascend 200 steps
4. Report: where does λ_max(D(Q)) plateau? At 0 (pure gauge) or above 0 (counterexample)?

## Success Criteria

**Full success (most important):** All eigenvalues of D(Q) ≤ 0 for 50+ configs. Gradient ascent plateaus at 0. Analytical proof of M(Q_pure) = M(I) written up.

**Critical finding:** Any Q with a positive eigenvalue of D(Q) > 0 is a counterexample to M(Q) ≼ M(I). REPORT IMMEDIATELY.

## Output Format

**code/**:
- `full_operator_check.py` — builds M(Q), M(I), D(Q), checks eigenvalues
- `pure_gauge_test.py` — pure gauge generation and isometry verification
- `gradient_ascent_D.py` — ascent on λ_max(D)
- `results.json` — all numerical results

**REPORT.md** section by section:
1. Formula verification (M(I) = K_curl check)
2. Full D(Q) spectrum for 50+ configs
3. Pure gauge analytical proof + numerical verification
4. Gradient ascent results
5. Conclusions

**REPORT-SUMMARY.md** (1 page): Is M(Q) ≼ M(I) as operators? Pure gauge = isometry confirmed? Any counterexample?

## Notes
- L=2 is fine for speed (192×192 matrix, fast full diagonalization)
- Always verify M(I) = K_curl first — if this fails, debug before proceeding
- Print results as you compute them
- Write REPORT.md section by section

# Exploration 010: Resolve Open Conjecture — H_norm ≤ 1/12 for All Q

## Mission Context
This is a YANG-MILLS mission. Do not confuse with other missions.

## Background — What We Know

From E008 and E009, we have the following state of the main claim:

**PROVED (rigorous):**
- At Q=I: H_norm ≤ 1/12 (Fourier analysis of discrete curl)
- For ALL Q: H_norm ≤ 1/8 (triangle inequality) → mass gap threshold β < 1/6 (8× SZZ)
- At Q=I: staggered mode v_{x,μ} = (−1)^{|x|+μ} v₀ achieves H_norm = 1/12 EXACTLY (E009 verified numerically)
- Convention: S = −(β/N) Σ_□ Re Tr(U_□), inner product |A|² = −2Tr(A²)

**OPEN CONJECTURE:**
- For ALL Q: H_norm ≤ 1/12 → threshold β < 1/4 (12× SZZ, 6× CNS arXiv:2509.04688)
- The gap: need to prove ∑_□ |B_□(Q,v)|² ≤ 4d|v|² for all Q ∈ SU(2)^E

**Where B_□ comes from:**
For general Q, the exact plaquette Hessian is:
  H_□(v; Q) = −(β/N) Re Tr(B_□² U_□)
where B_□ = Ã₁ + Ã₂ + Ã₃ + Ã₄ is the sum of parallel-transported tangents:
  Ã₁ = v_{x,μ}
  Ã₂ = Q_{x,μ} v_{x+ê_μ,ν} Q_{x,μ}^{−1}
  Ã₃ = −(Q_{x,μ}Q_{x+ê_μ,ν}) v_{x+ê_ν,μ} (Q_{x,μ}Q_{x+ê_μ,ν})^{−1}
  Ã₄ = −(Q_{x,μ}Q_{x+ê_μ,ν}Q_{x+ê_ν,μ}^{−1}) v_{x,ν} (...)^{−1}

E008 proved: H_□(v;Q) ≤ (β/2N)|B_□|² (operator inequality, maximized at U_□=I).
Combined with ∑_□ |B_□|² ≤ 4d|v|² → H_norm ≤ 1/12 for ALL Q.

**E009 tested 5 random Q:** all gave max eigenvalue ≈ 2β < 4β. BUT 5 samples is insufficient.

## Your Tasks

### Part 1 (Priority 1): Large Numerical Scan (100+ Q configurations)

Test whether H_norm ever exceeds 1/12 for Q ≠ I.

**Setup:** L=2, d=4, SU(2). Build the 192×192 Hessian matrix for each Q, find λ_max via eigvalsh, compute H_norm = λ_max / 48β.

**Test these categories of Q (total ≥ 100 configs):**

A. **Random Q**: 30 configs drawn uniformly from SU(2)^64 (use Haar measure: random unit quaternions)

B. **Gibbs samples**: 20 configs from Gibbs measure at β = 0.5, 1.0, 2.0, 3.0 (5 per β). Use heat bath. These are physically relevant configurations.

C. **Perturbations of Q=I**: 20 configs Q_{x,μ} = exp(ε A_{x,μ}) where A_{x,μ} is random su(2), ε ∈ {0.01, 0.1, 0.3, 0.5, 1.0} (4 configs per ε).

D. **Adversarial gradient ascent**: 30 configs. Start from random Q, compute gradient of max eigenvalue w.r.t. Q, ascend 100 steps. Try to find Q that maximizes H_norm.

**Report:**
- max H_norm over all 100+ configs
- Distribution: histogram or percentiles
- Did any Q give H_norm > 1/12?
- For adversarial: did gradient ascent converge to Q=I? Or to something else?

**Critical:** Use the SZZ convention: S = −(β/N)Re Tr. Set β=1.0 for the scan. H_norm = λ_max / (8(d−1)Nβ) = λ_max / 48.

### Part 2 (Priority 2): Temporal Gauge Proof Attempt

Try to prove ∑_□ |B_□(Q,v)|² ≤ 4d|v|² in temporal gauge.

**Temporal gauge:** Fix Q_{x,0} = I for all x (time-direction links = identity). This is always achievable by a gauge transformation. Then:
- Time-space plaquettes (μ=0, ν=i): U_{x,0i} = Q_{x+ê₀,i} Q_{x,i}^{−1}
  B_□ for this plaquette = v_{x,0} + Q_{x,0}v_{x+ê₀,i}Q_{x,0}^{−1} − Q_{x,0}Q_{x+ê₀,i}v_{x+ê₀,0}(...)^{−1} − v_{x,i}
  At gauge-fixed Q_{x,0}=I: simplifies to v_{x,0} + v_{x+ê₀,i} − Q_{x,i}v_{x+ê₀,0}Q_{x,i}^{−1} − v_{x,i}

Wait, recompute this carefully using the exact B_□ formula above. In temporal gauge:
  Ã₁ = v_{x,0}  (time direction, link = I)
  Ã₂ = I · v_{x+ê₀,i} · I = v_{x+ê₀,i}  (since Q_{x,0}=I)
  Ã₃ = −(I · Q_{x+ê₀,i}) · v_{x+ê₀,0} · (I · Q_{x+ê₀,i})^{−1} = −Q_{x+ê₀,i} v_{x+ê₀,0} Q_{x+ê₀,i}^{−1}
  Ã₄ = −(I · Q_{x+ê₀,i} · Q_{x+ê₀,i}^{−1}) · v_{x,i} · ... = −v_{x,i}

So B_□^{(0,i)} = v_{x,0} + v_{x+ê₀,i} − Ad_{Q_{x+ê₀,i}}(v_{x+ê₀,0}) − v_{x,i}

The time-direction tangents v_{x,0} appear as "pure gauge modes" and their contribution may simplify.

**Task:** Attempt to bound ∑_{x,i} |B_□^{(0,i)}|² in temporal gauge. Show whether it satisfies the 4d bound. If the temporal gauge argument works for time-space plaquettes, analyze spatial plaquettes separately.

Even a partial result (e.g., "the bound holds in temporal gauge for β → 0" or "we found a symmetry argument") is useful.

### Part 3 (Priority 3): SZZ Convention Verification

The E008 proof assumes S = −(β/N) Σ Re Tr(U_□). Verify this matches SZZ arXiv:2204.12737.

**Quick check:** In SZZ (arXiv:2204.12737), Definition 2.2 or nearby gives the action S. Extract:
1. The action formula (is there a 1/N? Is it Re Tr or just Tr? Is the sign −β or +β?)
2. The inner product on su(N) they use (is it −2Tr? Or Killing form? Or something else?)
3. Their bound in Lemma 4.1: what is the exact coefficient?

Then check: under SZZ's convention, does H_norm = λ_max / (SZZ_bound_coefficient) match our convention?

**Web search hint:** The paper is at https://arxiv.org/abs/2204.12737

## Success Criteria

**Part 1 Success:** 100+ Q configs tested, max H_norm reported. If max H_norm < 1/12: strong support for conjecture. If max H_norm > 1/12: counterexample found — report the config.

**Part 2 Success:** Either a proof that ∑_□ |B_□|² ≤ 4d|v|² in temporal gauge, or a clear statement of why the temporal gauge argument fails.

**Part 3 Success:** SZZ convention confirmed or discrepancy identified.

**Failure:** Parts 1-3 all inconclusive (computation fails, proof attempt gives no progress).

## Output Format

**code/** directory:
- `scan_hessian.py` — builds and solves Hessian for 100+ Q configs
- `adversarial_search.py` — gradient ascent to maximize H_norm over Q
- `results.json` — all numerical results with Q configs and H_norm values

**REPORT.md** covering:
1. Setup (SZZ convention confirmation or flag)
2. Numerical scan results (100+ configs)
3. Adversarial search results
4. Temporal gauge proof attempt
5. Conclusions for the conjecture

**REPORT-SUMMARY.md** (1 page):
- What is max H_norm observed over all 100+ Q?
- Did adversarial search find anything above 1/12?
- Does the temporal gauge argument work?
- Final assessment: is H_norm ≤ 1/12 for all Q CONFIRMED / FALSIFIED / UNRESOLVED?

## Important Notes

- L=2, d=4, SU(2): 64 links, 192×192 Hessian per configuration
- Computing 100 Hessians at 192×192 each: ~10-20 seconds per config = 20-30 min total
- Save code FIRST before running
- Set β=1.0 for the scan (H_norm = λ_max/48)
- Print results as computed — don't wait to write everything at the end
- Write section by section, each section as you complete it
- The E008 REPORT.md at ../exploration-008/REPORT.md has the full mathematical framework
- The E009 code at ../exploration-009/code/ has working SU(2) Hessian code you can reuse

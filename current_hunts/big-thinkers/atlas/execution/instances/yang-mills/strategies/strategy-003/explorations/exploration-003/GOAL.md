# Exploration 003: Gauge-Covariant Fourier Approach to the B_□ Inequality

## Mission Context
This is a YANG-MILLS mission (strategy-003). Do not confuse with other missions.

## The One Inequality We Need to Prove

**The open problem:** For all Q ∈ SU(N)^E and all tangent vectors v ∈ ⊕_e su(N):

  ∑_□ |B_□(Q,v)|² ≤ 4d |v|²

**Convention (required):** S = −(β/N) Σ_□ Re Tr(U_□), |A|² = −2Tr(A²).

**Why this matters:** β < 1/4 mass gap for SU(2) Yang-Mills in d=4 (12× SZZ arXiv:2204.12737).

## The Q=I Proof (Background)

At Q=I, B_□ = ω_{x,μν}(v) = v_{x,μ} + v_{x+ê_μ,ν} − v_{x+ê_ν,μ} − v_{x,ν} (discrete curl).

The proof proceeds via Fourier decomposition:
1. Fourier transform: v → v̂_{k,μ} = Σ_x v_{x,μ} e^{-ik·x} / L^{d/2}
2. In Fourier space: ω̂_{k,μν} = (1-e^{ik_ν}) v̂_{k,μ} - (1-e^{ik_μ}) v̂_{k,ν} = c_ν v̂_{k,μ} - c_μ v̂_{k,ν}
3. Use |c ∧ v̂|² ≤ |c|²|v̂|² with |c_k|² = Σ_μ 4sin²(k_μ/2) ≤ 4d
4. Sum over k using Plancherel: Σ_□ |ω_{x,μν}|² ≤ 4d|v|²

The key: Fourier analysis works because the curl OPERATOR is translation-invariant at Q=I.

## Your Approach: Gauge-Covariant Extension

**Idea:** At general Q, the connection Q breaks translation invariance. BUT: under a gauge transformation g = (g_x) ∈ SU(N)^Λ, the link variables transform as Q_{x,μ} → g_x Q_{x,μ} g_{x+ê_μ}⁻¹ and the tangents transform as v_{x,μ} → g_x v_{x,μ} g_x⁻¹ (adjoint). The B_□ transform as B_□ → Ad_{g_x}(B_□), so |B_□(gQg⁻¹, gvg⁻¹)| = |B_□(Q,v)| (isometry). Thus the sum ∑_□ |B_□|² is GAUGE INVARIANT.

This suggests: pick the gauge where Q is "as close to I as possible" and then apply the Fourier argument.

### Approach A: Coulomb Gauge
Fix Q to Coulomb gauge: Σ_μ (Q_{x,μ} - Q_{x-ê_μ,μ}^†) = 0 (discrete transversality condition). In Coulomb gauge, Q is "almost diagonal in Fourier space." The connection Laplacian is minimized. Can the Fourier bound be applied after gauge-fixing?

Explicit steps:
1. Given Q ∈ SU(N)^E, find g such that gQg⁻¹ is in Coulomb gauge.
2. Write Q = exp(A_μ) in Coulomb gauge (perturbative, A small). Expand:
   B_□(Q,v) = ω_{x,μν}(v) + [correction terms involving A_{x,μ}]
3. Show the correction terms don't increase ∑|B_□|².

Note: This is a perturbative approach. It works for Q near I but may not extend globally.

### Approach B: Gauge-Covariant Fourier Transform
Define a "covariant Fourier transform" adapted to the connection Q:

  ṽ_{k,μ} = Σ_x [U_{x→0}]^{-1} v_{x,μ} U_{x→0} e^{-ik·x} / L^{d/2}

where U_{x→0} is the parallel transport from x to the origin along some canonical path. After this transform, the covariant curl Φ_{k,μν} = "covariant version of c_ν v̂_{k,μ} - c_μ v̂_{k,ν}" with c_{k,μ}(Q) depending on the connection.

Show: |c_k(Q)|² ≤ 4d for all Q (as the gauge-dependent analogue of the standard Fourier bound).

### Approach C: Holonomy Perturbation
Write Q_{x,μ} = exp(A_{x,μ}) where A_{x,μ} ∈ su(N) is the "gauge field." Expand B_□ perturbatively in A:

  B_□(Q,v) = ω_{x,μν}(v) + [A, ω] + [A, [A, ω]] + ...

Bound each term using |[A,v]| ≤ 2|A||v|. Show the series gives ∑|B_□|² ≤ 4d|v|² for small |A|.

This works perturbatively (for Q near I). For large Q, one would need to close the argument.

### Approach D: Direct Computation for Q = Flat Connection
For Q such that the holonomy around every plaquette is trivial (U_□ = I for all □) — a "flat connection" — the Fourier analysis might work exactly. Show:
- In a flat gauge, Q can be gauge-transformed to Q=I on simply-connected lattices (but NOT on tori with non-trivial holonomy).
- For tori: flat connections have the form Q_{x,μ} = exp(2πi n_μ/L) for integers n_μ. Compute B_□ for these configurations.

## Required Elements

1. **Explicit covariant curl formula.** Write B_□(Q,v) in terms of the gauge field A_{x,μ} (using Q_{x,μ} = exp(A_{x,μ})). Expand to second order in A.

2. **Worked example: Q = single plaquette excitation.** Set Q_{0,0} = exp(ε τ₁), all other links = I (a single "plaquette gauge field"). Compute ∑_□ |B_□(Q, v_stag)|² for this Q and verify it's ≤ 4d|v_stag|².

3. **Gauge invariance check.** Verify explicitly that ∑_□ |B_□(Q,v)|² = ∑_□ |B_□(gQg⁻¹, gvg⁻¹)|² for a specific gauge transformation g.

4. **For whichever approach gets furthest:** State precisely where the proof works and where it breaks down.

5. **Literature search:** Look for:
   - "gauge-covariant Fourier transform" or "covariant Fourier analysis" on lattices
   - "connection Laplacian" spectrum bounds
   - "Coulomb gauge Fourier decomposition" in lattice field theory
   - Any paper bounding ∑|B_□|² or analogues for lattice connections

## Success Criteria

**Full success:** Proof of ∑_□ |B_□(Q,v)|² ≤ 4d|v|² for all Q (any approach).

**Partial success:** Proof for Q in a neighborhood of I (perturbative), or proof for flat connections, with clear statement of what's needed globally.

**Useful failure:** Identification of where the gauge-covariant extension breaks down.

## Output Format

Write REPORT.md section by section:
- Section 1: Gauge invariance of ∑|B_□|²
- Section 2: Coulomb gauge approach (Approach A)
- Section 3: Covariant Fourier transform (Approach B)
- Section 4: Perturbative expansion (Approach C)
- Section 5: Flat connections (Approach D)
- Section 6: Worked example
- Section 7: Literature findings
- Section 8: Summary

Write REPORT-SUMMARY.md (1 page): Which approach got furthest? Is the inequality proved? What's the remaining gap?

## Notes
- Write as you go — don't wait to write.
- This is a MATHEMATICAL PROOF task. Equations, not code.
- Gauge invariance is the key structural property — use it.

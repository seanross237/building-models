# Exploration 008: Prove H_norm ≤ 4/(3d) for SU(N) Yang-Mills Hessian

## Mission Context
This is a YANG-MILLS mission. Do not confuse with other missions.

## Background — The Key Finding to Prove

From the adversarial review (Exploration 007), we found:

**The staggered tangent mode at identity achieves H_norm = 4/(3d) exactly:**
- Config: Q_e = I (identity) for all links e
- Tangent: v_{x,μ} = (-1)^{x₀+x₁+x₂+x₃+μ} v₀ (staggered by site+direction parity)
- H_norm = |HessS(v,v)| / (8(d-1)Nβ × |v|²) = 4/(3d)
  - d=3: 4/9 ≈ 0.444
  - d=4: 1/12 ≈ 0.083 [VERIFIED NUMERICALLY on L=4, L=2 lattices]
  - d=5: 3/40 = 0.075

**Derivation (from E007):**
In d=4, 6 plane-pairs (μ,ν) with μ < ν. The staggered mode:
- "Active" pairs: (0,1), (0,3), (1,2), (2,3) → contribute +4β per plaquette to HessS
- "Inactive" pairs: (0,2), (1,3) → contribute 0 (sign cancellation: (-1)^{μ+ν} = same parity)

HessS(v_stag, v_stag) = 4 active pairs × L⁴ plaquettes × 4β = 16L⁴β
|v_stag|² = L⁴ × d = 4L⁴
H_norm = 16L⁴β / (48β × 4L⁴) = 16/192 = **1/12** ✓

## Your Task

Write a formal mathematical proof that for ALL Q ∈ SU(N)^E and ALL tangent vectors v:
```
|HessS(v,v)| ≤ (4/(3d)) × 8(d-1)Nβ × |v|²
```

### Part 1: Prove the Identity Configuration Maximum

**Step 1.1:** At Q = I, compute HessS(v, v) explicitly. The Wilson action is:
S = -β Σ_{□} Re Tr(U_□) = -β Σ_{(x,μν)} Re Tr(U_{x,μ} U_{x+μ̂,ν} U_{x+ν̂,μ}⁻¹ U_{x,ν}⁻¹)

The second derivative with respect to U_{x,μ} at U = I along tangent v_{x,μ} ∈ su(N):
∂²S/∂t²|_{t=0} for U_{x,μ}(t) = exp(t v_{x,μ}) = -β Σ_{□∋(x,μ)} Re Tr(v_{x,μ}² U_{□/(x,μ)})

At Q = I: U_{□/(x,μ)} = I, so this = -β × N_{□/e} × Re Tr(v_{x,μ}²) where N_{□/e} = 2(d-1).

**Step 1.2:** Compute the off-diagonal Hessian terms (for e ≠ f sharing a plaquette □):
∂²S/∂t₁∂t₂|_{t=0} for edges e, f ∈ □

At Q = I, compute this exactly. It involves Re Tr(v_e × [remaining links in □]).

**Step 1.3:** Sum over all plaquettes to get the total HessS(v, v). Show that for the staggered mode v_{x,μ} = (-1)^{|x|+μ} v₀:
- The off-diagonal terms between different sites cancel due to the staggered pattern
- The per-plaquette contribution for "active" plane-pairs equals exactly 4β × |v₀|²
- The per-plaquette contribution for "inactive" plane-pairs equals exactly 0

Conclude: HessS(v_stag, v_stag) = 4 × (d-1)/2 × 2L^d × 4β × |v₀|² = 4β(d-1)/d × |v_stag|² × something...

Wait, actually compute it directly. For the formula to be 1/12 in d=4:
HessS(v_stag, v_stag) = (1/12) × 48β × |v_stag|² = 4β × L⁴ × d × |v₀|²/d = 4β × L⁴ × |v₀|²

Check: is this what E007 computed? Yes: 16L⁴β = 4β × 4L⁴ = 4β × |v_stag|² ✓

### Part 2: Prove the Upper Bound for All Q

This is the harder part. Need to show that for ANY Q ∈ SU(N)^E:
|HessS(v,v)| ≤ (4/(3d)) × 8(d-1)Nβ × |v|²

**Approach:**
1. Use SZZ Lemma 4.1 structure: bound per-plaquette, then sum
2. Show that the staggered mode saturates the bound, so the identity is the worst-case configuration

**Key inequality to prove:** For any Q, any v:
|∂²(Re Tr U_□)/∂t²| ≤ 4 × per_link_contribution

Combined with the staggered pattern cancellation: exactly (d-1)/2 × d/(d-1) = d/2... hmm, need to think through this.

**Alternative approach:** Use the fact that for any plaquette □ and any tangent v_e at link e ∈ □:
|Re Tr(v_e² U_{□/e})| ≤ |v_e|² × N (since |Tr(M)| ≤ N|M| for SU(N))

Then bound the sum over all plaquettes and links by grouping by plane direction.

### Part 3: State the New Lemma

Write a clean replacement for SZZ Lemma 4.1:

**Lemma A (Tighter Hessian Bound):** For the SU(N) Wilson action S = -β Σ_{□} Re Tr(U_□) on a d-dimensional hypercubic lattice, for any configuration Q ∈ SU(N)^E and any tangent vector v ∈ ⊕_e T_{Q_e}SU(N):
```
HessS(v,v) ≤ (4/(3d)) × 8(d-1)Nβ × |v|²
```
This bound is TIGHT: equality is achieved by Q=I and v = v_stag (staggered pattern).

**Corollary:** Under the Bakry-Émery framework (SZZ), the mass gap holds for:
```
β < N/2 / ((4/(3d)) × 8(d-1)Nβ) = 3d/(32(d-1)) = 1/4 (for SU(2), d=4)
```
This improves SZZ's threshold from 1/48 to **1/4**, a factor of 12×.

### Part 4: Check Related Literature

Before claiming novelty, search for:
a) Any paper that proves a bound tighter than 8(d-1)Nβ on the Wilson action Hessian
b) The specific formula H_norm_max = 4/(3d) or any equivalent statement
c) Any known "staggered mode instability" or "staggered field analysis" in lattice gauge theory

If found: acknowledge where the bound is known and state what is new.
If not found: state the claim as novel.

## Success Criteria

**Success:** A complete proof of Lemma A (Parts 1-3) with:
- Explicit calculation at Q=I with staggered mode (Part 1)
- Upper bound for all Q (Part 2) — even a partial bound (e.g., "we can prove it for all |U_□ - I| < ε") is valuable
- Clean statement of the Lemma and Corollary

**Partial Success:** Proof of Part 1 (identity case only) + explanation of why Part 2 is harder

**Failure:** The bound is wrong (some Q, v gives H_norm > 1/12). If this happens, find the configuration and report it.

## Output Format

Write REPORT.md section by section:
1. Setup (notation, action, Hessian formula)
2. Proof at identity configuration (Part 1)
3. Extension to all Q (Part 2) — or explanation of the gap
4. Statement of Lemma A + Corollary
5. Literature check

Write REPORT-SUMMARY.md (1 page):
- Is Lemma A proved? (Yes/Partial/No)
- What is the new threshold? (1/4 if proved, or best achievable)
- Is this claim novel?
- What further work is needed?

## Notes

- This is a MATHEMATICAL PROOF task. Write mathematics, not code.
- Use standard lattice gauge theory notation (see SZZ arXiv:2204.12737 Sections 2-3 for setup)
- The proof at identity (Part 1) should be completely rigorous
- For Part 2, even a heuristic or sketch is valuable if a full proof is too hard
- Write section by section, not all at once

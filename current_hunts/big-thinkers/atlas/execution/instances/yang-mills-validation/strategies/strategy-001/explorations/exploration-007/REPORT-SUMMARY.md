# Exploration 007: Adversarial Proof Review — Summary

## Goal
Adversarially review the claimed proof that lattice SU(N) Yang-Mills has a mass gap for β < N²/(8(d-1)), alleged to be an 8× improvement over SZZ (arXiv:2204.12737) and 4× improvement over CNS (arXiv:2509.04688). Rate each step VALID/INVALID, identify hidden assumptions, list referee objections, and clarify mass gap vs spectral gap.

## What Was Tried
1. Read the actual SZZ paper (arXiv:2204.12737) via pdftotext extraction to verify exact theorem statements
2. Reviewed all 6 prior explorations' findings (E001–E006)
3. Cross-referenced the library files `per-plaquette-inequality-false.md`, `b-square-inequality-proof-progress.md`, `fourier-hessian-proof-q-identity.md`
4. Traced each step of the proof chain for logical gaps

## Outcome: CRITICAL FLAW FOUND

**Step 2 is INVALID.** The proof claims HessS(v,v) = (β/2N)Σ_□ |B_□(Q,v)|² as a formula valid for all configurations Q. This is the linchpin of the entire chain.

**The flaw:** This formula is only exact at flat connections (U_□ = I for all plaquettes). The exact per-plaquette Hessian is:

H_□ = −(β/N)[Re Tr(B_□² · U_□) + Re Tr(Ḃ_□ · U_□)]

The second term Re Tr(Ḃ_□ · U_□) is the connection correction that vanishes when U_□ = I but is positive and nonzero for generic configurations. This makes the true Hessian **larger** than (β/2N)|B_□|², so using this formula to bound HessS from above (as required by the Bakry-Émery argument) is invalid.

**E003's verification was at U_all = iσ₃**, which is a flat connection. Agreement to 10⁻⁴ at that specific configuration does not validate the formula at generic Q. Library file `per-plaquette-inequality-false.md` provides explicit numerical evidence: the ratio H_□ / [(β/2N)|B_□|²] reaches 1.54 at ε=0.5 perturbations and 1.94 at Haar-random Q.

Since Step 2 is invalid, Step 5 (β threshold) is not proved. The chain breaks.

## Step-by-Step Verdicts

| Step | Claim | Verdict |
|------|-------|---------|
| 1 | SZZ Bakry-Émery theorem (cited as "Theorem 1.3") | VALID WITH CAVEAT — citation error; actual result is Corollary 1.6 + Assumption 1.1 |
| 2 | HessS = (β/2N)Σ\|B_□\|² | INVALID — only exact at flat connections; fails at generic Q by factor 1.5–2× |
| 3 | Cauchy-Schwarz: \|B_□\|² ≤ 4Σ\|v_e\|² | VALID — correct in isolation |
| 4 | Link counting: 2(d−1) plaquettes per link | VALID — standard lattice geometry |
| 5 | β < N²/(8(d−1)) threshold | NOT PROVED — chain broken at Step 2 |
| 6 | Spectral gap = mass gap for lattice | VALID for lattice (not continuum Millennium Prize) |

## Key Takeaway
The "8× improvement" proof is not valid. The Hessian formula used at its core (Step 2) was verified only at flat connections; it fails at generic Q. What remains rigorously established is SZZ's original result: β < 1/(16(d-1)) for SU(N). The CNS result β < 1/(24) in d=4 (from the vertex σ-model doubling argument, arXiv:2509.04688) may or may not also be independently valid, but the present chain does not improve on it.

## What IS Correct
- H_norm = 1/12 at Q = I is rigorously proved via Fourier analysis (E006/library)
- H_norm ≤ 1/12 is numerically supported across 100+ random configurations with 0 violations
- Conjecture A': Σ|B_□(Q,v)|² ≤ 4d|v|² for ALL Q — unproven but no counterexample found
- If Conjecture A' is proved, the improved threshold β < N²/(8(d-1)) would follow (this is the real open problem)

## Unexpected Findings
- **The "[PROVED]" label in `fourier-hessian-proof-q-identity.md`** is incorrect. The file marks "H_norm ≤ 1/8 for ALL Q" as proved, but this relies on the same invalid formula. The library contains a mislabeled claim.
- **SZZ's actual method** (Lemma 4.1) uses a Cauchy-Schwarz on Tr(QX_e · Q̃X_ē) form, NOT on |B_□|²; their bound directly gives 8(d-1)N|β| without needing the B² formula.
- **Citation error in GOAL.md**: "SZZ Theorem 1.3" does not exist. The mass gap result is SZZ Corollary 1.6 (proved under Assumption 1.1).

## Leads Worth Pursuing
1. **Prove Conjecture A' globally**: Σ|B_□(Q,v)|² ≤ 4d|v|². If true for all Q, the threshold β < N²/(8(d-1)) is proved. Partial progress exists (b-square-inequality-proof-progress.md).
2. **Characterize the connection correction term**: Re Tr(Ḃ_□·U_□) is positive at generic Q. Can it be bounded separately to recover an improved threshold?
3. **Can the CNS vertex σ-model approach** (which gave 4× improvement over SZZ) be improved further? That approach avoids the B² formula issue entirely.

## Computations Identified
- **Global maximum of H_norm over SU(N)^E**: Current numerical evidence shows max ≈ 1/12, but a rigorous analytical proof requires controlling Re Tr(Ḃ_□·U_□). A targeted computation could try gradient ascent on H_norm across higher dimensions (d=5,6) and larger N to check whether the 1/12 bound is stable or breaks. ~50-line scipy script, medium difficulty.
- **Worst-case connection correction**: Compute sup_Q Re Tr(Ḃ_□·U_□) / (β|v|²) analytically or numerically to bound the gap between the formula-based and true Hessian. This directly quantifies how much the Step 2 error affects the threshold. ~30-line script, low difficulty.

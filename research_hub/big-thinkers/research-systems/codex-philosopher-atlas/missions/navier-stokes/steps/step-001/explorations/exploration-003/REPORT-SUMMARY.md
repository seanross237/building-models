# Exploration 003 Summary: Vasseur (2007) Proof Architecture

## Goal
Extract five structural features from Vasseur's 2007 De Giorgi proof of partial regularity for Navier-Stokes and compare with CKN (1982).

## What Was Tried
Web research on the Vasseur 2007 preprint (NS2.pdf at web.ma.utexas.edu/users/vasseur), his lecture notes (DGPekin.pdf), and survey articles (Seregin-Shilkin arXiv:1402.7181, Lee REU 2024). All five structural features were successfully extracted with precise mathematical content.

## Outcome: Succeeded

## Key Findings by Item

### 1. Epsilon-Regularity Criterion
Vasseur's Theorem 1 states: if sup_t ∫_{B(1)} |u|² + ∫∫|∇u|² + ||P||_{L^p(L¹)}^2 ≤ C*, then u is bounded on the inner half-cylinder. This is stated at **fixed scale** on a unit cylinder — not in CKN's "for all r → 0" form. The CKN criterion E(u,r) < δ* is recovered as Theorem 2 via standard NS parabolic rescaling; Vasseur claims no novelty there. The pressure condition is weaker than CKN: P ∈ L^p(L¹) for any p > 1 (vs. CKN's P ∈ L^{3/2}).

### 2. Covering Argument
Identical to CKN. Vitali covering with parabolic balls Q_{r_i}, giving Σ r_i ≤ C∫∫|∇u|² < ∞ → H¹_parabolic(S) = 0. Vasseur explicitly says the novelty is only in Theorem 1; the covering runs unchanged.

### 3. Localization Mechanism
The core novelty. Vasseur defines decreasing cylinders Q_k → Q_∞ = [−1/2,1]×B(1/2) with increasing levels C_k = 1−2^{−k} → 1, tracking the level-set energy U_k = sup_t ∫|v_k|² + ∫∫ d_k² where v_k = [|u|−C_k]₊. The master inequality (Lemma 11 + Eq. 13) gives U_k ≤ C^k·(1+||P||_{L^p(L¹)})·U_{k−1}^{β_p} with β_p > 1. The key departure from CKN: the pressure is decomposed into a harmonic (non-local) part P_k^1 controlled by the single global norm ||P||_{L^p(L¹)}, plus a local part P_k^2 depending only on u inside B_{k−1}. This avoids the need for P ∈ L^{3/2}(Q_r) at every scale r → 0.

### 4. Critical Scaling Exponents
Parabolic Sobolev: L² energy → L^{10/3} (the critical exponent 2·5/3 for parabolic dimension 5 = 3+2). De Giorgi level sets give U_{k−1}^{5/3} for transport/velocity terms (better than CKN's 3/2). But the local pressure term P_k^{21} yields exponent β → 4/3 (as q → ∞). Summary: velocity terms β = 5/3 > 3/2 (De Giorgi beats CKN here); pressure β = 4/3 < 3/2 (new bottleneck). Net: β_p > 1 for all p > 1 → partial regularity; β_p < 3/2 in general → full regularity not achieved. Vasseur shows in an Appendix that β > 3/2 would imply **full regularity** — so the threshold 3/2 is precise.

### 5. Free-Parameter vs. Fixed-Constant Estimates
No per-step ε-absorption in the De Giorgi iteration (unlike CKN). The only free parameter is λ (chosen once in Proposition 5 to make a linear coefficient < 1/8). Lossiness is fixed by: geometric factors 2^{Ck} from cutoffs (absorbed into C^k in Lemma 4) and the hard exponent 4/3 from the local pressure term — not a proof artifact, but a structural obstruction. De Giorgi is strictly less lossy on the velocity side (5/3 vs 3/2 for transport terms) but encounters a new pressure bottleneck.

## Key Takeaway
Vasseur's De Giorgi proof arrives at dimension ≤ 1 via the **same Vitali covering applied to the same ε-regularity criterion** as CKN. The De Giorgi mechanism is used only to establish the ε-regularity threshold; once established, the dimension bound follows the CKN route. The structural bottleneck (H¹(S) = 0 but not H^α(S) = 0 for α < 1) is not a consequence of proof technique — it reflects the global energy bound and parabolic scaling, shared by all approaches. Vasseur's value-add is a sharper identification of the full-regularity obstruction: the local pressure term contributes exponent 4/3 < 3/2, and 3/2 is precisely the threshold for full regularity.

## Leads Worth Pursuing
- **Tran-Yu (2014, AIHP):** Claims to use De Giorgi + Galilean invariance to remove the "bad scaling" local pressure term. If successful, this might achieve β > 3/2. Worth verifying.
- **The β = 3/2 threshold:** Vasseur's Appendix Conjecture 14 is an explicit "here is what you'd need for full regularity" statement. Investigating whether any subsequent work has resolved this conjecture would directly answer the "same bottleneck or different path" question.
- **Comparison with exploration-001 (CKN) and exploration-002 (Lin):** All three proofs converge on the same Vitali covering of the same ε-criterion at H^1 dimension. The structural comparison should confirm: dimension ≤ 1 is not a proof-technique artifact.

## Unexpected Findings
- Vasseur's framework is more powerful as an obstruction identifier than as a regularity prover: his Appendix formally separates partial from full regularity at β = 3/2, which CKN's framework does not make explicit.
- The De Giorgi approach actually produces a *worse* pressure exponent (4/3 < 3/2) than CKN's direct pressure estimate, even though it requires only the weaker pressure condition P ∈ L^p(L¹). This means the "weaker assumptions → same conclusion" improvement comes at the cost of a harder internal obstruction.
- The parabolic Sobolev exponent 10/3 is universal: it appears identically in CKN (as the L^3 velocity norm arising from |u|³) and in Vasseur (as the interpolation exponent for level-set control). This confirms the parabolic dimension 5 is the structural fact, not the proof technique.

## Computations Identified
None required for this exploration (all results are extracted from paper; numerical computations would not clarify the proof architecture questions).

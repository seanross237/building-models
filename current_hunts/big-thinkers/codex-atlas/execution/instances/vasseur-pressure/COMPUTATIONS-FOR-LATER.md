# Computation Registry

Computations identified during explorations that would significantly advance the mission. Maintained by the strategizer, read by the missionary and future strategizers.

## 1. Empirical β Measurement from DNS

- **What:** Compute U_k for k=0,...,12 on Taylor-Green vortex, anti-parallel tube, random IC, and Kida vortex flows. Fit the De Giorgi recurrence U_k ≤ C^k · U_{k-1}^β to extract empirical β via log-log regression.
- **Why:** Determines whether the worst-case analytical β < 4/3 is tight for actual NS solutions. If empirical β > 4/3 (or even > 3/2), there is exploitable slack in the pressure term.
- **What it resolves:** Path A (slack exists, constructive attack) vs Path B (no slack, obstruction mapping) — the core branch determination for this strategy.
- **Source:** Exploration 001 (Vasseur framework extraction)
- **Difficulty:** Medium (~100 lines Python/spectral). Code skeleton provided in exploration-001/REPORT.md Approach A.
- **Equations involved:** Vasseur (2007) Proposition 3, eq. (5): U_k ≤ C_p^k (1 + ||P||_{Lp(L1)}) U_{k-1}^{β_p}. Level set truncations v_k = [|u| - (1-2^{-k})]_+.
- **Status:** COMPLETED (exploration-002). Result: All beta_eff < 4/3 (range 0.35-1.01). Bottleneck exponent gamma decreases with Re. Branch: Path B (gap genuine). ABC (Beltrami) flow is outlier with beta ~1.0, gamma > 1.0 at all Re.

## 1b. Empirical Beta on Perturbed-ABC (Beltrami-near) Flows

- **What:** Run the De Giorgi measurement on "mildly Beltrami" flows — e.g., ABC + perturbation with varying amplitude epsilon. Test whether beta_eff decreases continuously with epsilon (robust) or drops discontinuously (threshold).
- **Why:** ABC's favorable scaling (beta_eff → 1.0) may be exploitable for conditional regularity. Need to know if the advantage is continuous.
- **What it resolves:** Whether Beltrami-near structure → better beta is a viable conditional regularity path.
- **Source:** Exploration 002 (ABC finding)
- **Difficulty:** Low-Medium. Reuse exploration-002 code, just change IC.
- **Equations involved:** Same De Giorgi recurrence. ABC flow: u = (B sin y + C cos z, C sin z + A cos x, A sin x + B cos y). Perturbed: u_ABC + epsilon * u_random.

## 2. CZ Slack on P_k^{21} Specifically — COMPLETED (Exploration 004)

- **Result:** CZ slack for P_k^{21} is k-INDEPENDENT. Tightness ratios converge to IC-dependent constants by k ~ 3-4. P_k^{21} has LESS slack than full pressure (1.7-3.9× vs 7.6-17.5×). The "CZ slack improves beta" hypothesis is FALSIFIED.
- **Source:** Exploration 004
- **Implication:** Improvement to beta must come from OUTSIDE the CZ framework.

## 3. Div-Curl Structural Bounds on P_k^{21}

- **What:** Test whether div-curl type estimates (Coifman-Lions-Meyer-Semmes, or compensated compactness) can beat the CZ bound on P_k^{21} in a k-dependent way. The RHS tensor f^{21} = u_below ⊗ u_below has special structure: both factors are bounded AND divergence-free. Standard CZ ignores this structure.
- **Why:** Exploration 004 showed CZ is tight for generic L^q → L^q. But the specific structure of f^{21} is NOT generic — div-free × bounded could yield estimates in Hardy space H¹ or BMO, which might beat L^q CZ bounds and might have k-dependent improvement.
- **What it resolves:** Whether structural arguments beyond CZ can improve beta.
- **Source:** Exploration 004 (identified as lead #1)
- **Difficulty:** High. Requires analytical work (not pure computation). Literature survey on compensated compactness for bilinear forms of div-free fields.
- **Equations involved:** The key bilinear estimate to check: ||∂_i∂_j Δ^{-1}(f_i g_j)||_{H¹} ≤ C ||f||_{L²} ||g||_{L^∞} when div(f) = 0. If this holds with k-dependent ||g||_{L^∞} = λ_k = 1-2^{-k}, it could give the needed improvement.

## 4. Cancellation Between Pressure Pieces

- **What:** Instead of bounding P_k^{21}, P_k^{22}, P_k^{23} separately, analyze the combined contribution P_k^{21} + P_k^{22} + P_k^{23} = full pressure. The cross-term P_k^{22} may cancel with parts of P_k^{21} in the bottleneck integral.
- **Why:** The De Giorgi argument bounds each piece separately, losing potential cancellations. Joint treatment could improve the combined exponent.
- **What it resolves:** Whether inter-piece cancellation can push the effective exponent above 4/3.
- **Source:** Exploration 004 (identified as lead #2)
- **Difficulty:** Medium (computational) + High (analytical). Can measure cancellation from DNS; proving it requires new estimates.
- **Equations involved:** The bottleneck integral I_k = ∫∫ |P_k^{21}| · |d_k| · 1_{v_k>0} dx dt. Compare with ∫∫ P_k^{21} · d_k · 1_{v_k>0} dx dt (signed version — cancellation means |signed| << |unsigned|).

## 5. Choi-Vasseur (2014) Alternative Pressure Decomposition — COMPLETED (Exploration 005)

- **Result:** CV14 decomposes P = P_{1,k} + P_{2,k} + P_3. P_3 (k-independent) absorbed via time-dependent truncation level with favorable sign. But achieved beta = 7/6 (WEAKER than 4/3). The P_k^{21} bottleneck lives inside P_{2,k}, which CV14 don't further decompose. Does NOT bypass the fundamental bottleneck.
- **Source:** Exploration 005

## 6. Dynamic Refinement of Pressure Decomposition (arXiv:2501.18402) — COMPLETED (Exploration 005)

- **Result:** Fernandez-Dalgo (2025) uses dynamic pressure decomposition in paraboloid geometry for epsilon-regularity. Uses Gronwall methods, NOT De Giorgi iteration. Does not address beta at all. Orthogonal to the beta problem.
- **Source:** Exploration 005

## 7. Vasseur-Yang (2021) Vorticity-Based De Giorgi

- **What:** Read Vasseur-Yang (2021), "Second derivatives estimate of suitable solutions to the 3D NS equations." They apply De Giorgi iteration to the VORTICITY equation instead of the velocity equation, avoiding pressure entirely. Understand their framework and whether the P_k^{21} bottleneck is circumvented.
- **Why:** The velocity-based De Giorgi framework has been exhaustively analyzed (explorations 001-005) and the P_k^{21} bottleneck is confirmed structural. A vorticity-based approach is the most promising remaining direction — it doesn't have a pressure term.
- **What it resolves:** Whether vorticity-based De Giorgi avoids the beta barrier, or whether an equivalent obstruction appears.
- **Source:** Exploration 005 (landscape survey identified this as key unexplored direction)
- **Difficulty:** Medium-High (literature analysis). New framework to understand.
- **Equations involved:** The vorticity equation ∂ω/∂t + (u·∇)ω = (ω·∇)u + νΔω and its De Giorgi iteration structure.
- **Status:** COMPLETED (exploration-008). Result: Pressure eliminated but 4/3 reappears from trilinear nonlinearity (1/2 derivative + 5/6 nonlinear = 4/3). The barrier is UNIVERSAL across NS formulations. Beltrami advantage strengthened: trilinear bottleneck enters at O(ε²) vs O(ε) for pressure.

## 8. Beltrami Deficit of u_below on DNS Data

- **What:** For ABC flow at Re = 100, 500, 1000, compute B(u_below) = ||curl(u_below) − λu_below||_{L²}/||u_below||_{L²} as a function of De Giorgi level k. Determine whether truncation u → u_below preserves or destroys Beltrami structure.
- **Why:** Exploration 006 identified the key obstacle to Beltrami conditional regularity: the De Giorgi truncation breaks the Beltrami eigenfunction property. If B(u_below) stays small at all k levels, the mechanism is viable. If B(u_below) → 1 rapidly, the mechanism is killed by truncation.
- **What it resolves:** Whether the Hessian/Lamb path to improved beta survives the De Giorgi iteration structure.
- **Source:** Exploration 006 (identified as critical test)
- **Difficulty:** Low-Medium (~50 lines Python). Reuse exploration-002 DNS + De Giorgi infrastructure.
- **Equations involved:** curl(u_below) where u_below = u·min(1, λ_k/|u|). Beltrami deficit B = ||curl(u_below) − λu_below||/||u_below||.
- **Status:** COMPLETED (exploration-007). Result: B_k ≈ 0.56 × 2^{-k} for ABC — deficit vanishes geometrically. Controls: B_k ≈ const. Truncation PRESERVES Beltrami structure. Re-independent. Unexpected: div(u_below) ≠ 0 but Bernoulli dominance robust.

## 9. Bernoulli/Remainder Decomposition of P_k^{21} — COMPLETED (Exploration 007)

- **Result:** Two-way split (Bernoulli P_hessian = -|u_b|²/2 + remainder). For ABC: remainder = 4.4% of bottleneck at k=4, 0.2% at k=8. For controls: remainder > 100% (massive cancellation). Hessian/Lamb identity invalidated by div(u_below) ≠ 0 — Bernoulli/remainder is the correct decomposition.
- **Source:** Exploration 007
- **Note:** Original three-way Hessian/Lamb/compressibility split abandoned because truncation breaks div-free. The simpler Bernoulli/remainder split captures the essential physics.

## 10. Analytical Proof of B_k = O(2^{-k}) for Beltrami Flows

- **What:** Prove that for exact Beltrami flows (curl u = λu), the truncated velocity u_below = u·min(1, λ_k/|u|) satisfies B(u_below) = ||curl(u_below) − λu_below||/||u_below|| = O(2^{-k}).
- **Why:** Exploration 007 measured this computationally. A proof would make the conditional regularity claim rigorous.
- **What it resolves:** Whether the Beltrami deficit improvement is provable, not just observed.
- **Source:** Exploration 007 (proof gap #1)
- **Difficulty:** Medium-High. Pointwise analysis of how truncation interacts with curl eigenvalue equation. The key is that the perturbation from truncation is confined to the set {|u| > λ_k}, which has measure O(2^{-k}).
- **Equations involved:** curl(u·min(1, λ_k/|u|)) = curl(u)·min(1, λ_k/|u|) + u × ∇(min(1, λ_k/|u|)). The second term is the truncation error, supported on {|u| > λ_k}.

## 11. Perturbed-ABC: Continuous Degradation Test

- **What:** Run the De Giorgi measurement on u = u_ABC + ε·u_random for ε = 0.01, 0.05, 0.1, 0.2, 0.5. Measure B_k and R_frac as functions of ε and k.
- **Why:** The mechanism is verified for exact Beltrami. The conditional regularity question requires understanding how it degrades with departure from Beltrami. If B_k(ε) ≈ ε + O(2^{-k}), the mechanism is robustly continuous.
- **What it resolves:** Whether the conditional regularity path extends to near-Beltrami flows (not just exact Beltrami).
- **Source:** Exploration 007 (identified as key follow-up)
- **Difficulty:** Low-Medium. Reuse E007 code, vary IC.
- **Status:** COMPLETED (S1-exploration-010). Result: B_k decay LOST for any ε > 0. β_eff degrades continuously. β > 1 requires >98% Beltrami. Mechanism does NOT generalize.

## 12. Level-Set Distribution |{|u| > λ}| on DNS Near High-Velocity Regions

- **What:** For DNS solutions at various Re, compute the distribution function μ(λ) = |{x : |u(x,t)| > λ}| as a function of λ. Fit the decay rate: μ(λ) ~ λ^{-p}. Compare with the Chebyshev prediction p = 10/3 (from the L^{10/3} parabolic embedding).
- **Why:** Strategy-002 exploration-001 identified the Chebyshev estimate |{v_{k-1} > 2^{-k}}| ≤ C^k U_{k-1}^{5/3} as the SINGLE potentially improvable step in the entire De Giorgi chain. If the actual distribution decays faster than λ^{-10/3} for NS solutions, there is room for improvement. The improvement needed: p > 10/3 + 10/9 ≈ 4.44 to break the 4/3 barrier (δ > 1/3 in the Chebyshev exponent translates to faster tail decay).
- **What it resolves:** Whether the Chebyshev step has exploitable numerical slack on actual NS solutions.
- **Source:** Strategy-002 exploration-001 (decomposition audit)
- **Difficulty:** Medium. Reuse S1 DNS infrastructure. Post-processing: compute level-set measures at multiple thresholds, fit power law.
- **Equations involved:** Chebyshev: |{|f| > λ}| ≤ λ^{-p} ||f||_{Lp}^p with p = 10/3. The De Giorgi chain: v_k ∈ L^{10/3}(parabolic) → |{v_{k-1} > 2^{-k}}| ≤ 2^{10k/3} ||v_{k-1}||_{L^{10/3}}^{10/3} ≤ C^k U_{k-1}^{5/3}.
- **Status:** COMPLETED (S2-exploration-002). Result: Tail exponents IC-dependent (TG: p≈10, Random: p≈8-9, ABC: p≈2.1). De Giorgi tightness ratios ~3-5×, CONSTANT in k — does NOT improve β. Consistent with E003's analytical finding that Chebyshev improvement is circular with the regularity problem.

## 13. Commutator Estimate for P_{k21} via Hardy Space

- **What:** Write out the exact bilinear form of the bottleneck integral ∫∫ P_{k21}·div(u v_k/|u|) dx dt, where P_{k21} = Δ^{-1} ∂_i∂_j (u_i^{below} · u_j^{above}). Test whether this bilinear form has the div-curl structure needed for Coifman-Lions-Meyer-Semmes (1993) compensated compactness (Hardy space H¹ improvement over L¹). If so, compute what improvement in the U_{k-1} exponent results.
- **Why:** S2-E003 identified this as the most promising remaining route (Route 3). SQG succeeds in Caffarelli-Vasseur (2010) because the drift enters as a commutator [(-Δ)^{1/2}, u·], gaining an extra power. The NS nonlinear term involves a bilinear form of div-free fields — potentially amenable to compensated compactness.
- **What it resolves:** Whether the nonlinear coupling in the De Giorgi iteration can be improved by exploiting structure beyond Chebyshev, following the SQG precedent.
- **Source:** Strategy-002 exploration-003 (Route 3 identification)
- **Difficulty:** Medium-High. Symbolic computation of bilinear form structure + analytical argument for Hardy space membership. Verification via numerical test on DNS data.
- **Equations involved:** CLMS theorem: if f ∈ L^p, g ∈ L^q with div(f) = 0, curl(g) = 0, then f·g ∈ H¹ (Hardy space) ⊂ L¹. The question: does the specific bilinear form in P_{k21} have analogous structure?
- **Status:** COMPLETED (S2-exploration-004). Result: Route 3 CLOSED. Three independent obstructions: (1) no div-curl structure in truncated fields, (2) divergence-error remainder dominates P^{21} at high frequencies (61% of L², 18× at high k), (3) CRW gives no improvement for bounded multipliers. The commutator part of P^{21} HAS good high-frequency regularity (spectral ratio 0.67→0.09) but div-error remainder negates it. SQG-NS gap is structural: scalar vs vector, linear vs quadratic.

## 14. Frequency-Localized De Giorgi via Littlewood-Paley

- **What:** Apply Littlewood-Paley decomposition to the De Giorgi pressure P^{21}, treating low and high frequency modes with different estimates. Low modes: exploit commutator structure (confirmed by E004 to have good regularity). High modes: accept standard CZ bound. Test whether the high-mode contribution is subdominant (decays with De Giorgi level k), allowing the low-mode commutator improvement to dominate the recurrence.
- **Why:** S2-E004 showed that the divergence error (which kills compensated compactness) concentrates at HIGH frequencies. The commutator part of P^{21} has genuinely better high-frequency regularity (spectral ratio drops 0.67→0.09 at Fourier mode k=20). A frequency split could isolate the good structure from the bad.
- **What it resolves:** Whether frequency-localized estimates can bypass the 4/3 barrier by exploiting the frequency-dependent structure of the divergence error.
- **Source:** Strategy-002 exploration-004 (unexpected finding about frequency distribution of div error)
- **Difficulty:** High. Requires combining Littlewood-Paley theory with De Giorgi iteration — non-standard. Analytical + numerical verification needed.
- **Equations involved:** LP decomposition: P^{21} = Σ_j Δ_j P^{21} where Δ_j is the Littlewood-Paley projector. For low j: commutator estimate. For high j: CZ bound. Recurrence: U_k ≤ C^k [Σ_{j≤J} (improved bound)_j + Σ_{j>J} (CZ bound)_j] U_{k-1}^β_eff.
- **Status:** COMPLETED (S2-exploration-005). Result: NEGATIVE. Four independent lines: spectral peak shift to high j with k, growing I_hi/I_total (~1%→~20%), Bernstein penalty (5-10× worse than CZ), all three analytical approaches introduce irreducible 2^{αJ}. CZ is the optimal frequency-by-frequency estimate. Bernstein exchange rate 2^{3j/5} is fixed by dimensional analysis.

## 16. Non-CZ Pressure Handling (Direct Energy Estimates)

- **What:** Instead of bounding P^{21} in L^p via CZ and then using the L^p bound in the De Giorgi iteration, estimate ∫∫ P^{21}·v_k dx dt directly using the pressure Poisson equation Δp = -∂_i∂_j(u_iu_j). Test whether integration by parts on the Poisson equation produces a bound that avoids the CZ bottleneck entirely.
- **Why:** ALL attempts to improve β within the CZ framework are now closed (E001-E005). The only remaining constructive avenue is to bypass CZ entirely. Direct energy estimates on the pressure Poisson equation would produce a bound on ∫P·∇v_k that doesn't go through L^p of P.
- **What it resolves:** Whether the CZ framework itself is the obstruction, or whether the 4/3 barrier persists even without CZ.
- **Source:** Strategy-002 exploration-005 (identified as remaining direction)
- **Difficulty:** Medium-High. Requires careful integration by parts, commutator with truncation, and checking that no step reintroduces the CZ bottleneck.
- **Equations involved:** Δp = -∂_i∂_j(u_iu_j). Integration by parts: ∫p·∂_i v_k = ∫∂_i p · v_k = -∫(u_j ∂_j u_i)v_k. The question: does this direct form give a better U_{k-1} exponent than going through ||P^{21}||_{L^{3/2}}?
- **Status:** COMPLETED (S2-exploration-006). Result: NEGATIVE. Three routes: IBP gives β=1 (WORSE — loses CZ consolidation gain of 1/3), H¹/BMO gives β=4/3 (SAME — exponent invariant), CRW gives β≤1 (bounded multiplier blocks). β = 4/3 is TOOL-INDEPENDENT. Literature (12 papers): no published β > 4/3 by any method.

## 18. Wolf's Local Harmonic+Particular Pressure Decomposition

- **What:** Apply Wolf's (2015) local pressure decomposition p = p_harm + p_part (harmonic on suitably scaled parabolic cylinders + particular solution) within the De Giorgi iteration. This is genuinely CZ-free — the harmonic part satisfies mean-value estimates, and the particular part has explicit L^p bounds from the Poisson equation.
- **Why:** S2-E006 showed all standard non-CZ routes (IBP, H¹/BMO, CRW) give β ≤ 4/3. Wolf's decomposition is structurally different — it uses locality (parabolic cylinders) rather than global CZ transforms. Could the local structure interact with the De Giorgi level sets in a favorable way?
- **What it resolves:** Whether purely local pressure estimates, avoiding global CZ transforms entirely, can improve β.
- **Source:** Strategy-002 exploration-006 (identified as remaining genuinely CZ-free direction)
- **Difficulty:** High. Requires understanding Wolf's framework and integrating it with De Giorgi iteration.
- **Equations involved:** Wolf (2015): p = p_h + p_p on Q_r where Δp_h = 0 in Q_r and Δp_p = -∂_i∂_j(u_iu_j) with zero boundary data. Mean-value: ||p_h||_{L^∞(Q_{r/2})} ≤ C/r^{n+2} ||p_h||_{L^1(Q_r)}.

## 17. Time-Frequency Analysis (Modulation Spaces)

- **What:** Investigate whether joint space-time frequency estimates using modulation spaces or wave packet decomposition can circumvent the Bernstein barrier that kills LP approaches. The key idea: LP decomposes in spatial frequency only, but the De Giorgi iteration has parabolic structure — time and space are coupled at rate ω ~ |ξ|².
- **Why:** E005 showed LP fails because the Bernstein exchange rate 2^{3j/5} is fixed by spatial dimensional analysis. But parabolic PDE solutions have correlated space-time frequency content — this correlation is invisible to purely spatial LP.
- **What it resolves:** Whether parabolic space-time frequency structure of NS solutions provides additional information beyond spatial frequency decomposition.
- **Source:** Strategy-002 exploration-005 (identified as speculative direction)
- **Difficulty:** Very High. Modulation space theory for NS is largely uncharted territory.
- **Equations involved:** Modulation spaces M^{p,q}: ||f||_{M^{p,q}} = (Σ_k ||□_k f||_{L^p}^q)^{1/q} where □_k is a uniform frequency box decomposition. Parabolic version: boxes aligned to ω ~ |ξ|².

## 19. SDP Formalization of Chebyshev Sharpness Under NS Constraints

- **What:** Formulate a semidefinite program (SDP) that maximizes |{|u|>λ}| subject to: (i) div(u) = 0, (ii) ||u||_{L^2} ≤ E (energy bound), (iii) ||∇u||_{L^2} ≤ D (Sobolev bound), (iv) ||u||_{L^{10/3}} ≤ S (parabolic embedding bound). If the SDP optimal value matches the Chebyshev bound λ^{-10/3}S^{10/3}, then Chebyshev IS tight under NS constraints. If the SDP gives a strictly lower value, there's room for improvement.
- **Why:** S2-E007 (adversarial review) identified this as the most actionable path to formalizing Claim 3 (seven-route obstruction as sharpness result). Currently Claim 3 is informal — 8 routes tested, all give β ≤ 4/3. An SDP result would upgrade it to rigorous: "under NS structural constraints, the Chebyshev exponent cannot be improved."
- **What it resolves:** Whether the informal sharpness theorem "β = 4/3 is sharp within standard tools" can be made rigorous via optimization.
- **Source:** Strategy-002 exploration-007 (adversarial review, most actionable formalization)
- **Difficulty:** Medium. ~100 lines Python/CVXPY. Main challenge: formulating the div-free constraint in a finite-dimensional SDP relaxation (truncated Fourier).
- **Equations involved:** Chebyshev: |{|f|>λ}| ≤ λ^{-p}||f||_p^p. The SDP: max |{|u|>λ}| subject to div(u)=0, ||u||_2≤E, ||∇u||_2≤D, ||u||_{10/3}≤S. Dual: min over multipliers μ,ν,ρ of μE² + νD² + ρS^{10/3} subject to μ|u|² + ν|∇u|² + ρ|u|^{10/3} ≥ 1_{|u|>λ} for all div-free u.

## 15. Div-Free Truncation Existence

- **What:** Prove or disprove: does there exist a nonlinear map φ: R^3 → R^3 such that (i) div(φ(u)) = 0 whenever div(u) = 0, (ii) |φ(u)| ≤ λ (amplitude bound), (iii) φ(u) = u when |u| ≤ λ? If such a map existed, commutator methods could apply to the De Giorgi iteration.
- **Why:** S2-E004 identified that the SOLE reason compensated compactness fails for NS is that amplitude truncation breaks div-free. A div-free-preserving truncation would restore the commutator improvement.
- **What it resolves:** Whether the topological obstruction to commutator methods is fundamental or an artifact of the specific truncation choice.
- **Source:** Strategy-002 exploration-004 (unexpected finding)
- **Difficulty:** Medium. Likely impossible by degree theory (u/|u| has nontrivial degree on {|u|=λ}), but a rigorous proof is needed.
- **Equations involved:** Degree argument: on {|u| = λ + ε}, u/|u|: S^2 → S^2 has degree ±1. Any continuous φ with φ = u on {|u| ≤ λ} and |φ| ≤ λ would need to contract this to a point — impossible if deg ≠ 0.

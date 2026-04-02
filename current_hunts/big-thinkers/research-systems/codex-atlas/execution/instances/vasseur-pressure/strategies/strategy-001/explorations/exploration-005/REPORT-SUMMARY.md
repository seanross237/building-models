# Exploration 005 Summary: Choi-Vasseur (2014) Alternative Decomposition and Post-2007 Landscape

## Goal
Determine whether alternative pressure decompositions (especially Choi-Vasseur 2014 and Fernandez-Dalgo 2025) improve the De Giorgi recurrence exponent beta beyond 4/3, and survey the broader landscape of post-2007 approaches.

## Outcome: SUCCESS — All 8 deliverables answered. Clear negative result.

## Key Takeaway

**No paper since Vasseur (2007) has improved beta beyond 4/3. The barrier is untouched.** Choi-Vasseur (2014) introduces a three-way decomposition P = P_{1,k} + P_{2,k} + P_3 where P_3 (k-independent, from outer cutoff derivatives) is absorbed into the velocity equation by making the truncation level time-dependent: E_k(t) = (1-2^{-k}) + integral of ||nabla P_3||. This clever trick removes P_3 from the energy inequality entirely (favorable sign, Eq. 47). However, the achieved exponent is only beta = 7/6 — WEAKER than Vasseur's 4/3 — because their goal is proving fractional higher derivative integrability, where any beta > 1 suffices. The P_k^{21} bottleneck lives inside P_{2,k}, which CV14 don't further decompose. arXiv:2501.18402 (Fernandez-Dalgo) uses dynamic pressure decomposition in paraboloid geometry with Gronwall methods — NOT De Giorgi iteration — and does not address beta at all.

## Leads Worth Pursuing
- The P_3 absorption trick (time-dependent truncation level) could potentially be extended: what if MORE of the pressure could be absorbed this way? The method works for any term with bounded L^1_t L^inf_x gradient. If one could show parts of the local pressure have similar structure, more terms could be removed from the iteration.
- Vasseur-Yang (2021) uses De Giorgi on the VORTICITY equation, avoiding pressure entirely. This is a fundamentally different attack that might circumvent the P_k^{21} bottleneck.

## Unexpected Findings
The entire post-2007 literature has moved ORTHOGONALLY to the beta problem: higher derivatives, quantitative regularity, epsilon-regularity, concentration methods. Nobody is directly attacking beta > 4/3. This suggests the community views it as either (a) fundamentally hard or (b) not the most promising route to NS regularity. This is itself a significant finding for our mission.

## Computations Identified
None beyond those already identified in prior explorations. The key insight from this exploration is theoretical, not computational: the Choi-Vasseur decomposition confirms that the bottleneck is structural and cannot be circumvented by reorganizing the pressure decomposition.

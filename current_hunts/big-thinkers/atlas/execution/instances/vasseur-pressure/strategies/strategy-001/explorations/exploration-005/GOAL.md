<!-- explorer-type: standard -->

# Exploration 005: Choi-Vasseur (2014) Alternative Decomposition and Recent Developments

## Goal

Survey the post-Vasseur-2007 literature on alternative pressure decompositions in the De Giorgi framework for NS regularity. Focus on two specific works:

1. **Choi-Vasseur (2014, AIHP)** — "Estimates on fractional higher derivatives of weak solutions for the Navier-Stokes equations" (Ann. Inst. Henri Poincaré, Anal. Non Linéaire, 31(5), 899-945, 2014). This paper introduces a three-way pressure decomposition P = P_1k + P_2k + P_3 that reportedly absorbs the "bad" non-divergence pressure term P_3 into the velocity equation.

2. **arXiv:2501.18402** — "Dynamic Refinement of Pressure Decomposition" (January 2025). This very recent preprint appears to directly address pressure decomposition refinement in the De Giorgi context.

If either paper is not findable by these exact references, search for closely related works by the same authors or on the same topic.

## Background: Why This Matters

In Vasseur (2007), the De Giorgi iteration for NS regularity gives a recurrence U_k ≤ C^k · U_{k-1}^β with β < 4/3. The bottleneck is a SINGLE term — the non-divergence local pressure P_k^{21}, defined by:

```
-ΔP_k^{21} = Σ_{i,j} ∂_i∂_j [φ_k · u_j(1-v_k/|u|) · u_i(1-v_k/|u|)]
```

The factors u(1-v_k/|u|) are bounded by 1 (Lemma 10). CZ theory gives ||P_k^{21}||_{L^q} ≤ C_q (CONSTANT, independent of U_{k-1}). This constant bound contributes exponent 0 to the recurrence, limiting β to 4/3.

**We have computationally verified (exploration 004) that the CZ slack for P_k^{21} is k-independent** — the CZ bound is equally tight at every iteration level. P_k^{21} actually has LESS CZ slack than the full pressure (1.7-3.9× vs 7.6-17.5×). So improving β through better CZ constants is ruled out.

**We have computationally verified (exploration 002) that the empirical β_eff < 4/3 for all tested DNS flows**, with the bottleneck exponent gamma dropping below 4/3 at moderate Reynolds numbers for turbulent flows. The 4/3 bound appears close to sharp for general flows.

**The question:** Can an ALTERNATIVE decomposition of the pressure avoid the P_k^{21} bottleneck entirely? If Choi-Vasseur found a way to absorb the bad term into the velocity equation, this could change which term limits β.

## Required Deliverables

### On Choi-Vasseur (2014):

1. **What EXACTLY is the three-way decomposition?** State P = P_1k + P_2k + P_3 with the precise PDE defining each piece (RHS of each Poisson equation). How does this differ from Vasseur (2007)'s four-way decomposition (P_k^1, P_k^{21}, P_k^{22}, P_k^{23})?

2. **How is P_3 "absorbed into the velocity equation"?** What does this mean technically? Is P_3 treated as a gradient term that can be moved to the LHS of the velocity equation? Or is it controlled through an energy estimate that doesn't require bounding its L^q norm separately? State the specific inequality or identity.

3. **What exponent does this give?** After the rearrangement, what is the new recurrence exponent β? If it's still < 4/3, what is the NEW bottleneck? If it's unclear or not stated, explain why.

4. **Does this actually bypass the P_k^{21} problem?** Critical assessment: does the Choi-Vasseur decomposition genuinely avoid the term that limits Vasseur (2007), or does an equivalent bottleneck reappear elsewhere?

### On arXiv:2501.18402:

5. **What is the main result?** State the key theorem/proposition. What "dynamic refinement" means and how it differs from static decompositions.

6. **Connection to the β exponent.** Does this work improve β, or address a different aspect of the De Giorgi iteration?

### Broader Survey:

7. **Landscape of post-2007 De Giorgi approaches.** What other papers have attempted to improve Vasseur's β? List all approaches you find, with a brief description of what each tries and whether it succeeds. Key names to search: Vasseur, Choi, Yang, Shvydkoy, Cheskidov, Colombo, De Lellis, Isett (in the context of De Giorgi for NS, not just Onsager conjecture).

8. **Current state of the art.** As of 2024-2025, what is the best known β in a De Giorgi-type argument for NS? Is 4/3 still the frontier, or has it been improved?

## What to Distinguish

- **[PAPER]** vs **[INTERPRETATION]** — flag every claim by source
- **Different decomposition strategies** — don't conflate Vasseur (2007), Choi-Vasseur (2014), and any other approaches
- **Improving β** vs **proving other results using De Giorgi** (e.g., partial regularity, higher derivatives) — we care specifically about β

## Success Criteria

✅ **Success:** Deliverables 1-8 answered. Clear determination of whether any alternative decomposition improves β beyond 4/3 or changes the bottleneck structure.

❌ **Failure:**
- Cannot find Choi-Vasseur (2014) → survey whatever Choi-Vasseur papers exist and describe their De Giorgi-related results
- arXiv:2501.18402 is about a different topic → describe what it IS about and search for other recent pressure decomposition papers
- No post-2007 improvement to β exists → this is a POSITIVE finding (confirms the gap is a hard open problem); document it clearly

## Output Format

Sections matching deliverables 1-8. Cite specific theorem numbers, equation numbers, page references. For the landscape survey (#7), use a table format.

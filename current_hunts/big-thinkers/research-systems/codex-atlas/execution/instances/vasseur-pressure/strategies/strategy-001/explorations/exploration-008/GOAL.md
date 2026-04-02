<!-- explorer-type: standard -->

# Exploration 008: Vasseur-Yang (2021) Vorticity-Based De Giorgi

## Goal

Read Vasseur-Yang (2021) and assess whether their vorticity-based De Giorgi approach avoids the pressure bottleneck that limits beta to < 4/3 in the velocity-based approach.

## Paper

Vasseur, A. and Yang, J. "Second derivatives estimate of suitable solutions to the 3D Navier-Stokes equations." arXiv:2010.09525 (2020), published version in a journal (check).

## Background: Why This Matters

The entire velocity-based De Giorgi framework for NS regularity is blocked by a SINGLE bottleneck: the non-divergence local pressure term P_k^{21}. Our investigation has established:

1. **The analytical bound beta < 4/3 is untouched since 2007** (exploration 005 — 13 papers surveyed, none improve beta)
2. **CZ slack for P_k^{21} is k-independent** (exploration 004 — the bound is already tight)
3. **Empirical beta < 4/3 for general turbulent flows** (exploration 002 — gap appears genuine)
4. **No alternative decomposition avoids the bottleneck** (exploration 005 — Choi-Vasseur 2014 reorganizes but doesn't improve)
5. **Beltrami structure helps by eliminating the Lamb vector** (exploration 006 — Grade B mechanism identified)

The vorticity equation is:
```
∂ω/∂t + (u·∇)ω = (ω·∇)u + νΔω
```

This equation has NO pressure term. If De Giorgi iteration can be applied to the vorticity equation, the P_k^{21} bottleneck is structurally absent. The question is: what NEW bottleneck appears? The vortex stretching term (ω·∇)u introduces its own difficulties.

## Required Deliverables

1. **What EXACTLY does Vasseur-Yang prove?** State the main theorem with precise conditions and conclusions. What regularity result do they establish? Is it about velocity, vorticity, or higher derivatives?

2. **How does De Giorgi apply to the vorticity equation?** Describe the iteration structure:
   - What are the level-set functions? (Analogous to v_k = [|u| − (1−2^{-k})]_+)
   - What is the energy functional U_k? (Analogous to sup_t ∫ v_k² + ∫∫ d_k²)
   - What recurrence do they prove? U_k ≤ C^k · U_{k-1}^beta for what beta?

3. **What is the new bottleneck?** In the velocity equation, pressure limits beta. In the vorticity equation, what term limits the recurrence exponent? Is it:
   - The vortex stretching (ω·∇)u? (The nonlinear coupling between ω and u)
   - Some other structural term?
   - Does a pressure term reappear through the back door (e.g., through the velocity u that appears in the stretching term)?

4. **What exponent do they achieve?** What is their beta? Does it exceed 4/3? Does it approach or exceed 3/2?

5. **Can the vorticity approach prove regularity?** If they achieve beta > 1 for the vorticity, does this give L^∞ bounds on vorticity (which IS the BKM criterion)? Is there a logical circle analogous to the velocity-based one?

6. **Connection to Beltrami structure.** For Beltrami flows, ω = λu. Does the vorticity-based De Giorgi iteration have the SAME favorable properties as the velocity-based one? Does the vortex stretching term simplify for Beltrami flows?

7. **Comparison with velocity approach.** Side-by-side comparison:

| Feature | Velocity De Giorgi (Vasseur 2007) | Vorticity De Giorgi (Vasseur-Yang 2021) |
|---|---|---|
| Level-set quantity | |u| | |ω| (or other?) |
| Bottleneck term | P_k^{21} (non-div pressure) | ? |
| Beta achieved | < 4/3 | ? |
| Pressure role | Direct bottleneck | Absent? |
| Stretching role | Controlled by Sobolev | Direct bottleneck? |

8. **Assessment for our mission.** Does the vorticity approach offer a viable path to beta > 3/2? Grade as (A/B/C/D) with justification.

## What to Distinguish

- **[VASSEUR-YANG]** vs **[INTERPRETATION]**
- **Regularity of vorticity** vs **regularity of velocity** — controlling ω in L^∞ implies regularity (BKM), but the De Giorgi iteration on ω might give L^∞ bounds only under conditions
- **beta for vorticity iteration** vs **beta for velocity iteration** — these are different objects

## Success Criteria

✅ **Success:** All 8 deliverables answered. Clear determination of the vorticity-based approach's bottleneck and whether it avoids the pressure limitation.

❌ **Failure:**
- Cannot find the paper → search for Vasseur-Yang on NS higher derivatives, arXiv 2010.09525
- The paper doesn't use De Giorgi on vorticity directly → describe what it actually does and assess relevance
- The vorticity approach has an equivalent bottleneck → describe it precisely and compare with P_k^{21}

## Output Format

Sections matching deliverables 1-8 with a comparison table. Cite specific theorems and equations.

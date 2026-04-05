<!-- explorer-type: standard -->

# Exploration 003: Assess Tran-Yu (2014) on Galilean Invariance and the Pressure Term

## Goal

Read Tran-Yu (2014, Ann. Inst. Henri Poincaré, Anal. Non Linéaire) and assess their specific claim about using Galilean invariance to improve the pressure term in the Navier-Stokes regularity problem. Determine whether their approach improves the De Giorgi recurrence exponent β.

The paper may be: Tran, C.V. and Yu, X. "Note on Prodi-Serrin-Ladyzhenskaya type regularity criteria for the Navier-Stokes equations" (2014, J. Math. Phys.) or a related paper by the same authors on Galilean invariance and pressure. Search for: **Tran Yu Galilean invariance Navier-Stokes pressure regularity**.

## Background: Why This Matters

From Vasseur (2007, NoDEA), the De Giorgi iteration for NS regularity gives a recurrence:
```
U_k ≤ C_p^k · (1 + ||P||_{L^p(L^1)}) · U_{k-1}^{β_p}
```

The bottleneck for β is a SINGLE term — the non-divergence part of the local pressure P_k^{21}:
```
I_k = ∫∫ |P_k^{21}| · |d_k| · 1_{v_k > 0} dx dt
```

This gives β < 4/3. If β > 3/2, all weak solutions are regular. The gap is > 1/6.

P_k^{21} satisfies:
```
-ΔP_k^{21} = Σ_{i,j} ∂_i∂_j [u_j(1-v_k/|u|) u_i(1-v_k/|u|)]
```

The factors u(1-v_k/|u|) are bounded by 1. CZ theory gives ||P_k^{21}||_{L^q} ≤ C_q (constant, independent of U_{k-1}). This "constant" bound is what kills β.

**The question:** Galilean invariance means u → u - u₀ preserves the NS equations. Does a Galilean boost make the specific factors u(1-v_k/|u|) smaller or better-structured? If so, the CZ bound on P_k^{21} might tighten, improving β.

## Required Deliverables

1. **What EXACTLY do Tran and Yu prove?** State their main theorem/proposition with equation numbers. What condition on the pressure do they use? What conclusion do they reach?

2. **How does Galilean invariance enter their argument?** Is it:
   - A better constant in an existing inequality? (Modest improvement)
   - A better exponent? (Significant improvement)
   - A structural change that shifts which term is the bottleneck? (Game-changing)

3. **Connection to the De Giorgi framework.** Does their result directly improve Vasseur's β? Specifically:
   - Does their argument apply to the non-divergence pressure term P_k^{21}?
   - Can their Galilean invariance trick be inserted into the De Giorgi iteration?
   - If so, what exponent does it give? If not, why not (structural reason)?

4. **Is their result correct?** Check their key estimates. Identify any steps that assume more than stated, or any gaps. Pay particular attention to:
   - Whether they use Galilean invariance of the FULL equations or just part of the pressure
   - Whether the improvement survives when applied to the specific decomposed pressure piece P_k^{21}

5. **What EXACTLY does Galilean invariance contribute?** Classify precisely:
   - **Better constant:** The bound is ||P||_{L^q} ≤ C_q ||u-u₀||²_{L^{2q}} with some optimal u₀. Does this meaningfully reduce C_q or the RHS?
   - **Better exponent:** Does the Galilean-subtracted pressure have improved integrability (e.g., L^∞ instead of just L^q for all q < ∞)?
   - **Structural improvement:** Does the argument reveal a cancellation or sign structure invisible without the boost?

6. **Assessment for our mission.** Concise verdict: does Tran-Yu's approach offer a viable path to improving β beyond 4/3? Grade as: (A) directly applicable — insert into De Giorgi and get better β; (B) potentially applicable — needs adaptation but the idea is sound; (C) not applicable — the improvement is orthogonal to the De Giorgi bottleneck; (D) incorrect — the claimed improvement has a gap.

## What to Distinguish

- **[TRAN-YU]** vs **[INTERPRETATION]** — flag every claim by source
- **Improvement to full pressure** vs **improvement to P_k^{21} specifically** — the bottleneck is P_k^{21}, not the full pressure
- **Worst-case bound** vs **typical-case value**

## Success Criteria

✅ **Success:** All 6 deliverables answered. The connection (or disconnection) between Tran-Yu and Vasseur's De Giorgi framework is clearly established with equation-level precision.

❌ **Failure:**
- Cannot locate the specific Tran-Yu paper → report what you searched and found instead; survey any other papers that use Galilean invariance for NS pressure improvement
- Tran-Yu's result is about a different aspect of NS (not De Giorgi, not pressure improvement) → describe what it IS about and assess relevance

## Output Format

Sections matching deliverables 1-6. Cite specific theorem numbers, equation numbers, and page references.

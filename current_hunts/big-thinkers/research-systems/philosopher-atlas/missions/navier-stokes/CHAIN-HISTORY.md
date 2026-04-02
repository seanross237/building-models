# Chain History — Navier-Stokes Mission

## Planning Loop Run 1 — 2026-03-29

### Planner Output

5 chains produced:

- **Chain A: CKN Proof Dissection** — Bound-by-bound audit of CKN inequalities. Measure slack in each. Find the loosest.
- **Chain B: Ladyzhenskaya Inequality Slack** — Divergence-free vs. scalar optimal constants. Do NS solutions structurally avoid extremizers?
- **Chain C: Prodi-Serrin Endpoint** — How close do solutions get to critical norms? Connect to Tao's obstruction.
- **Chain D: Energy Cascade Constraint** — Enstrophy production vs. bounds. Vorticity alignment suppresses stretching.
- **Chain E: Pressure Estimates** — Calderon-Zygmund bounds loose for NS? Divergence-free structure tightens pressure?

### Selector Decision

Selected **Chain A** (CKN Proof Dissection). Reasoning: broadest scope, subsumes parts of other chains, systematic audit plays to Atlas's computational strengths, produces useful output even if no dramatic slack found. Other chains are single-inequality investigations that Chain A would cover anyway.

### Attacker Critique (Key Points)

1. **Wrong analogy to Yang-Mills.** Yang-Mills mass gap is quantitative; NS regularity is qualitative. Tightening individual constants in CKN doesn't change the qualitative conclusion (partial regularity with dimension <= 1 singular set).
2. **CKN is limited by epsilon-regularity bootstrap structure and parabolic scaling**, not by constant sharpness. The epsilon is existential.
3. **Computational methodology fundamentally limited.** 128^3 at Re=5000 is not DNS. Smooth solutions trivially satisfy CKN bounds with enormous slack — measuring this is uninformative.
4. **Absorption estimates are trivially loose.** Young's inequality with free epsilon is lossy by design.
5. **CKN proof is iterative, not linear.** Can't list "10-20 inequalities in order."
6. **Different versions (CKN, Lin, Vasseur) use different strategies.** Lin uses compactness with fewest explicit inequalities.
7. **Likely outcome is tautology:** composed bounds have slack, sharp constants already known.
8. **The interesting direction (cutoff function loss, alternative localization) is treated as fallback.**

### Judge Verdict: MODIFY

Most critiques ruled VALID. The chain was restructured from "which constant is suboptimal" to "which structural feature of the proof architecture is the binding constraint."

Key changes:
- Single proof → comparative analysis (CKN, Lin, Vasseur)
- Individual inequality sharpness → scaling exponent comparison
- 128^3 at Re=5000 → resolution matched to Re
- "Tighten loosest bound" → identify binding structural constraint
- Absorbed measurement ideas from Chains C (Prodi-Serrin norms), D (vorticity alignment), E (pressure Hessian)

Judge's probability of presentable result: 65-70%.

### Refined Chain

See `CHAIN.md` for the refined 4-step chain.

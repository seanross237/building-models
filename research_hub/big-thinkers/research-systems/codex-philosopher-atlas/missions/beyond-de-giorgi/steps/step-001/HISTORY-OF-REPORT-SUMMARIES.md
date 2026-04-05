# History of Report Summaries — Step 1

### Exploration 001 — Exact Far-Field Pressure Obstruction Reconstruction

- Goal: reconstruct the exact surviving far-field pressure pairing, identify which harmonic modes are already killed by the test structure, isolate the true bad coefficient, and state what would actually have to get smaller for progress.
- Outcome: succeeded.
- Key findings:
  - Full pairing: `I_p^far = -∬ p_far div(v_k φ_k^2 ê)`.
  - Expanded form:
    `I_p^far = -∬ p_far (ê·∇v_k) φ_k^2 - 2∬ p_far v_k φ_k (ê·∇φ_k) - ∬ p_far v_k φ_k^2 div(ê)`.
  - Dominant live term: `I_p^far,main = -2∬ p_far v_k φ_k (ê·∇φ_k)`.
  - Operative estimate: `I_p^far <= C_far 2^{12k/5} U_k^{6/5}` with `C_far ~ ||u||_{L^2}^2 / r_k^3`.
  - Constant harmonic mode is already killed by the divergence pairing; affine and higher harmonic modes generally survive.
- Key takeaway: the obstruction is coefficient-side, not exponent-side. Controlling `p_far` only modulo constants is cosmetic because constants are already annihilated.

### Exploration 002 — Tao Gate For The Pressure-Side Branch

- Goal: test the short list of pressure-relevant NS-specific ingredients against the Tao 2016 filter and decide whether any nontrivial harmonic-tail continuation survives.
- Outcome: failed as a live harmonic-tail continuation.
- Candidate verdicts:
  - exact algebraic form of `u · ∇u`: `fails Tao gate`
  - pressure-Hessian / tensor structure: `unclear but testable`
  - vorticity / strain geometry for this pressure pairing: `fails Tao gate`
- Key findings:
  - Generic harmonic regularity is disqualified because Tao's averaged model preserves the relevant harmonic-analysis structure.
  - The surviving issue is a moment problem for affine-or-higher harmonic content behind `C_far ~ ||u||_{L^2}^2 / r_k^3`.
  - No screened candidate currently acts on that coefficient at estimate level.
- Key takeaway: Step 2 should be downgraded, not green-lit as a broad harmonic-tail continuation. At most, preserve one narrow tensor-side follow-up question about remote-shell moment cancellation.

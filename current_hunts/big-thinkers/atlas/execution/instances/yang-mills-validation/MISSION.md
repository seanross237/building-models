# Mission: Validate Yang-Mills β < 1/6 Result

A prior Atlas mission (3 strategies, 30 explorations, March 2026) proved a mass gap for lattice SU(2) Yang-Mills in d=4 at coupling β < 1/6 — claimed to be an 8× improvement over Shen-Zhu-Zhu (2023) and 4× over Cao-Nissim-Sheffield (2025).

This mission validates that result: is the proof correct, is it novel, and how far does it extend?

## What to Validate

### 1. Proof Correctness

The proof chain:
1. SZZ Bakry-Émery condition (Theorem 1.3 of arXiv:2204.12737): mass gap holds for β < 1/(48 × H_norm)
2. H_norm = λ_max(M(Q)) / 48 for SU(2), d=4
3. Triangle inequality bound: λ_max(M(Q)) ≤ 8(d−1) = 24 for all Q
4. Therefore H_norm ≤ 24/48 = 1/2... wait, that gives β < 1/24, not 1/6.

**The "better exploitation" step from H_norm ≤ 1/2 to H_norm ≤ 1/8 is the critical step to verify.** The prior mission's reports describe this as coming from the "SZZ-style bound" applied to a split of |B_□|². Read the actual proof (in Strategy 002 exploration 008's REPORT.md and Strategy 003's FINAL-REPORT.md Theorem 5) and verify every step. Reproduce the argument independently.

Check:
- Is the SZZ convention correctly applied? (S = −(β/N) Σ Re Tr, with the 1/N factor)
- Is the B_□ formula correct? (backward edges include own link in holonomy — this was a corrected formula; the original had errors)
- Does the triangle inequality actually give H_norm ≤ 1/8, or is there a factor-of-2 error?
- Does H_norm ≤ 1/8 actually yield β < 1/6 through the Bakry-Émery condition?

### 2. Novelty — CNS Comparison

The prior mission flagged this as the top priority. Cao-Nissim-Sheffield (arXiv:2509.04688, September 2025) improved SZZ to β < 1/24.

- Read the CNS paper in detail. What technique do they use?
- Do they already prove β < 1/6 or better?
- If not, could their technique be trivially extended to match or beat 1/6?
- Is our proof using the same key insight or a genuinely different one?
- Check arXiv:2505.16585 (CNS May 2025) as well — different paper, different technique.

### 3. Numerical Verification on Larger Lattices

The prior mission tested H_norm ≤ 1/12 on L=2 and L=4 lattices only. Extend to:
- L=8: 4096 links, Hessian is 12288×12288. Sparse — use power iteration for λ_max.
- L=16 if tractable: 32768 links. May need to use Lanczos or ARPACK.
- Test with diverse Q: random Haar, Gibbs at multiple β, adversarial gradient ascent
- Report: does H_norm ≤ 1/12 hold? What is the maximum observed? Does it approach 1/12 on larger lattices or stay well below?

### 4. Extension to SU(3) and Higher N

All prior results are for SU(2). The conjecture H_norm ≤ 1/12 uses d/(4(d−1)N) which for N=3, d=4 gives H_norm ≤ 1/18.
- Test numerically: does H_norm ≤ 1/18 hold for SU(3)?
- If not, find the tight bound for SU(3).
- The proof of H_norm ≤ 1/8 should generalize to SU(N) — verify this.

### 5. The d=5 Anomaly

Strategy 002 found that for d=5, the staggered mode is NOT the maximum eigenvector of M(I). The true λ_max = 5β > 4.8β (staggered mode value). Investigate:
- What IS the maximum eigenvector for d=5?
- Is the conjecture λ_max(M(Q)) ≤ 4d false for d=5?
- What does this say about the d=4 result — is there something special about d=4?

## What NOT to Do

- Do NOT try to prove Conjecture 1 (λ_max ≤ 4d for all Q). That's a separate mission.
- Do NOT survey the Yang-Mills landscape broadly. The prior mission already did this exhaustively.
- Do NOT reproduce known results. Focus on verification and extension.

## Key Files from Prior Mission

Read these for full context:
- `../yang-mills/MISSION-COMPLETE.md` — consolidated claims and mission summary
- `../yang-mills/strategies/strategy-001/FINAL-REPORT.md` — obstruction atlas
- `../yang-mills/strategies/strategy-002/FINAL-REPORT.md` — the β < 1/6 proof details
- `../yang-mills/strategies/strategy-003/FINAL-REPORT.md` — conjecture analysis, Weitzenböck formula
- `../yang-mills/strategies/strategy-002/explorations/exploration-008/REPORT.md` — the actual proof
- `../yang-mills/strategies/strategy-002/explorations/exploration-009/REPORT.md` — eigenvalue verification

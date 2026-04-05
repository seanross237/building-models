# E008 Summary: λ_n^zeta / λ_n^GUE Crossover Validation

## Goal
Validate E002's finding that λ_n^zeta/λ_n^GUE < 1 for n > 300, using 5000 zeros and larger GUE ensembles.

## Outcome: PARTIAL — Signal confirmed at fixed N=K=2000, but NOT robust to increasing K

## Key Findings

- **[COMPUTED] E002 replication confirmed:** With 100 GUE realizations (vs E002's 5), the ratio at n=500 is 0.952, exactly matching E002. The signal is 7.3σ below 1. Crossover at n ≈ 272.

- **[COMPUTED] Truncation is severe:** λ_n^zeta is NOT converged at 2000 zeros for n ≥ 300. Going from 2000 → 5000 zeros, λ_500 increases from 881 to 935 (+6.1%). At n=1000, the change is +11.4%. The sum converges slowly.

- **[COMPUTED] GUE λ_n scales linearly with N:** At N=500, λ_500^GUE ≈ 235. At N=2000, ≈ 926. At N=3000, ≈ 1385. The comparison is only meaningful when N_GUE = K_zeros.

- **[COMPUTED] At fixed N=K=2000, the crossover is real and highly significant** — but this is a statement about finite sums, not about the full infinite series.

- **[CONJECTURED] The crossover may be an artifact of truncation.** With 5000 zeros, λ_500^zeta = 935 vs the N=2000 GUE value of 926 — ratio > 1. The fair matched comparison at N=K=5000 was still computing at cutoff.

- **[COMPUTED] GOAL.md had incorrect reference values:** λ_100^zeta = 114.18 (not 59.72), and E002 used N=2000 GUE with 5 trials (not N=100 with 1000 trials).

## Verification Scorecard
- Verified: 0 (no Lean proofs)
- Computed: 5 (all key numerical results reproducible)
- Checked: 1 (E002 replication exact match)
- Conjectured: 1 (artifact hypothesis)

## Key Takeaway
**The λ_n crossover is a real feature of the truncated sums at K=2000, confirmed with high statistics. But it is NOT robust to changing K: the zeta Li coefficients grow faster than expected as more zeros are added, suggesting the ratio moves toward or above 1 at larger K. The novel claim is WEAKENED — the crossover likely reflects truncation behavior rather than an intrinsic difference between zeta zeros and GUE.**

## Leads Worth Pursuing
- Complete the matched N=K=5000 comparison (5000×5000 GUE, ~10 trials needed)
- Study the RATE of convergence: does λ_n^zeta(K) / λ_n^GUE(K) converge to a limit as K → ∞? If so, is that limit 1 or something else?
- The per-zero contribution at large n may reveal meaningful structure even if the total ratio converges to 1

## Unexpected Findings
- E002's GUE setup (N=2000, 5 trials) was correctly done but barely sampled — the std was underestimated. With 100 trials, the std is ~6 at n=500 vs E002's ~2.7 (better statistics reveal larger variance).
- The slow convergence of Li coefficients means they are a POOR diagnostic for comparing zeta to GUE unless convergence rates are matched.

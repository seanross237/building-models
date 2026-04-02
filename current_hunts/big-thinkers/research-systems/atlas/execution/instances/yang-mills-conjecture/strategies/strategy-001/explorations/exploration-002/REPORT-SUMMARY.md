# Exploration 002 Summary: Per-Plaquette Contribution Structure

## Goal
Map f_□(Q) per plaquette for 50+ configs on L=2, d=4. Find groupings where each group sum ≤ 0.

## What Was Done
Computed f_□(Q) for all 96 plaquettes across 36 diverse configurations (Haar, near-identity, Gibbs, abelian, adversarial). Tested 4 grouping types. Derived algebraic formula for simplified case.

## Outcome: **Partial success with key proof route identified**

### Key results

**Per-plaquette structure [COMPUTED + PROVED]:**
- **Active plaquettes** (μ+ν odd): f_active ≤ 0 always — PROVED by triangle inequality
  - B = c₁(n+R_ξn) + c₂(R₁n+R_□n), triangle inequality gives |B| ≤ 4, so |B|² ≤ 16 = |B_I|²
- **Inactive plaquettes** (μ+ν even): f_inactive ≥ 0 always — trivial (|B_I|²=0)

**Cube-face grouping [COMPUTED]:**
Sum ∑_{μ<ν} f_{(x,μ,ν)} ≤ 0 for all x, all Q — **zero violations in 160,000 tests** (10,000 configs × 16 vertices). Adversarial gradient ascent targeting individual cube sums converges to Q=I (maximum at exactly 0).

**Algebraic proof for simplified case [PROVED]:**
When cross-links = I, the cube-face sum equals:
```
∑_{μ<ν} |B_{(x,μ,ν)}|² = 32 + 8⟨n, ∑_μ w_μ⟩ − |∑_μ s_μ w_μ|²  ≤  64
```
where w_μ = R_μ^{−1} n ∈ S². Proof: 8⟨n,W⟩ ≤ 8|W| ≤ 32 (triangle inequality) and −|A|² ≤ 0.

## Verification scorecard
- 4 PROVED claims (triangle inequality active bound; trivial inactive bound; cube-face for cross-links=I; formula derivation)
- 5 COMPUTED claims (global sum ≤ 0; cube-face 160K tests; adversarial convergence; inactive always positive; formula verified numerically)
- 0 CONJECTURED

## Key takeaway
The cube-face inequality ∑_{μ<ν} |B_{(x,μ,ν)}|² ≤ 64 is the central sub-inequality for Conjecture 1. It's been proved for the case when only base-vertex links vary (cross-links = I), with a clean algebraic formula. The full general case (arbitrary cross-links) is strongly supported by 160K numerical tests and adversarial verification but needs an algebraic proof.

The mechanism: the staggered sign structure forces A = ∑_μ s_μ w_μ → 0 at Q=I (since ∑s_μ = 0), making Q=I the global maximum of the cube-face sum.

## Proof gap identified
Need to prove cube-face inequality for general Q (arbitrary cross-links). Candidate approach: factor out R_ξ from each plaquette's B vector and apply a generalization of the base-link formula. Gauge transformation argument at neighboring vertices may help.

## Leads worth pursuing
1. **Generalize the algebraic formula** to include cross-links — the structure ∑|B|² = 32 + 8⟨n,W̃⟩ − |Ã|² should hold with extended definitions of W̃, Ã.
2. **Gauge invariance argument**: The cube-face sum at x is invariant under gauge transformations at vertices ≠ x. Can we use this to gauge away cross-links?
3. **Direct matrix bound**: Express ∑_{μ<ν}|B_{μν}|² as a Hilbert-Schmidt norm of some matrix and bound it.

## Unexpected findings
- The formula ∑|B|² = 32 + 8⟨n,W⟩ − |A|² reveals that the maximum Q=I requires TWO conditions: (1) all R_μ fix n (W = 4n, maximum inner product) AND (2) the staggered cancellation A = ∑s_μw_μ = 0. These hold simultaneously only at Q=I due to the staggered sign structure.
- Near-identity: the cube-face maximum for random near-identity configs (cross-links=I) is ~61.5, not 64 — confirming the bound is not tight for most configs.

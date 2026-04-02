# Exploration 005 — UV-Cutoff Scan: Resolving the β^0.40 vs O(β²) Question

## Mission Context

We've run 4 explorations on SED vs QM for the anharmonic oscillator V(x) = ½x² + βx⁴. Key results so far:

1. **Langevin approximation** (constant Γ = τω₀²): fails at O(β). var_x goes the wrong direction.
2. **Full ALD** (Landau-Lifshitz, position-dependent Γ_eff = τ(ω₀² + 12βx²)): fixes O(β) failure. Residual error grows as β^0.40.
3. **Pesquera & Claverie (1982)**: Proved analytically that SED with full ALD disagrees with QM at O(β²) in the τ→0, ω_max→∞ limit.

**The open question:** Our ALD simulation (ω_max=10) gives β^0.40 scaling, not O(β²). Is this a UV-cutoff artifact (because ω_max=10 is too small) or a genuine discrepancy with P&C?

## Your Task

Run the ALD simulation from exploration 004 at different UV cutoffs to resolve this.

### Part 1: ω_max scan at β = 1.0

Run the ALD simulation at β=1.0 (where the discrepancy is largest) with:
- ω_max = 10 (dt = 0.314) — reproduces E004
- ω_max = 20 (dt = 0.157)
- ω_max = 30 (dt = 0.105)

For each ω_max, report:
- var_x_ALD ± uncertainty
- Fractional error vs QM (var_x_QM = 0.2571)
- β-dependent excess Δe = (var_x_ALD - var_x_QM) - baseline_offset

The baseline_offset at each ω_max should be measured by running β=0 at the same cutoff.

### Part 2: ω_max scan at β = 0.1

Repeat for β=0.1 (where ALD matched QM within noise at ω_max=10):
- Does increasing ω_max improve the agreement further?
- Or does a new β-dependent error emerge at higher cutoff?

### Part 3: τ scan at β = 1.0

P&C's result is in the τ→0 limit. Run at β=1.0, ω_max=10 with:
- τ = 0.01 (reproduces E004)
- τ = 0.005
- τ = 0.002

Does the residual error decrease with τ? If it scales as τ, it's a radiation-reaction artifact. If it's τ-independent, it's a UV cutoff effect.

### Implementation

Start from the E004 code at `explorations/exploration-004/code/ald_simulate.py`. Copy it to your code/ directory and modify:

1. Accept command-line arguments for β, ω_max (or equivalently dt), and τ
2. Everything else stays the same: N_ensemble=200, T=20000, 50 samples/trajectory
3. For ω_max=20: dt = π/20 ≈ 0.157. For ω_max=30: dt = π/30 ≈ 0.105.
4. Warning: smaller dt means more time steps (N_t = T/dt). For ω_max=30, dt=0.105, N_t ≈ 190000. This should still be fast enough.

**Run each (β, ω_max, τ) combination SEQUENTIALLY.**

### Noise normalization (VERIFIED — use directly)

A_k = sqrt(S_F(ω_k) * N_t / (2 * dt)) where S_F(ω) = 2τω³

### Expected results

If the β^0.40 is a UV artifact:
- At higher ω_max, the ALD result should converge toward QM
- The β-dependent excess Δe should DECREASE with increasing ω_max
- At ω_max → ∞, Δe should scale as O(β²) (P&C prediction)

If the β^0.40 is real:
- Δe will be approximately independent of ω_max
- This would contradict P&C and be a novel finding

## Success Criteria

- At least 3 ω_max values tested at β=1.0
- At least 2 ω_max values tested at β=0.1
- At least 2 τ values tested at β=1.0
- Clear trend: does increasing ω_max reduce or not reduce the β-dependent excess?

## Deliverables

- `explorations/exploration-005/REPORT.md` (300-500 lines)
- `explorations/exploration-005/REPORT-SUMMARY.md` (30-50 lines)
- `explorations/exploration-005/code/` — modified simulation script

## UV Divergence Reminder
Velocity variance is UV-divergent. Focus on position-based observables only.

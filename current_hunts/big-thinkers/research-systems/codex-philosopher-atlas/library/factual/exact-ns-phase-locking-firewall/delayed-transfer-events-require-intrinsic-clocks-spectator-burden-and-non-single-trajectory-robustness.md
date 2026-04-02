# Delayed Transfer Events Require Intrinsic Clocks, Spectator Burden, And Non-Single-Trajectory Robustness

Status: `PROPOSED` threshold sheet with `INFERRED` motivation

The branch's delayed-transfer event time `t_*` is the first time
`J_B(t_*) >= (1/4) E_A(0)`.
It counts only if the same run also satisfies
`t_* >= 3 tau_turn(t_*)`
and
`t_* <= (1/4) tau_nu(S)`.

Here the intrinsic nonlinear clock is
`tau_turn(t) = inf_{0 <= s <= t} E_S(s) / Q_S(s)`,
with
`Q_S(t) = sum_{tau in T(S)} |C_tau| |a_p(t)| |a_q(t)| |a_k(t)|`,
and the strict viscous deadline is
`tau_nu(S) = 1 / (nu max_{m in S} |k_m|^2)`.

At the same event time, the spectator burden must satisfy
`J_R(t_*) <= (1/4) J_B(t_*)`.

The same metric sheet also freezes the robustness rule:
a single favorable trajectory never counts.
The branch accepts only either an open set of reduced initial data after
quotienting exact symmetries, or an exact invariant family or normally
hyperbolic manifold with at least one non-symmetry parameter.

These gates keep ordinary turnover-scale exchange, late viscous-decay
artifacts, spectator-heavy claims, and one-orbit luck from being packaged as
delayed transfer.

Filed from:
- `missions/exact-ns-phase-locking-firewall/library-inbox/step-001-exploration-003-metric-sheet-and-step-2-readiness-verdict.md`

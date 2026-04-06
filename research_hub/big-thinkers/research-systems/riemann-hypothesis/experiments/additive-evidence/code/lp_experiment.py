"""
Additive-evidence LP experiment (sign-corrected).

Setup:
  Let s = sigma + i t. For sigma > 1 we have the identity
      -log|zeta(s)| = - Re( log zeta(s) )
                    = - sum_p sum_{k>=1} cos(k t log p) / (k p^{k sigma}).

  We are searching for "additive evidence" weights w_p(t) (bounded in p by
  a convergent envelope B_p = C (log p)^A / p^{1+eps}) such that, for all
  candidate t in a finite grid,
        E_sigma(t) := sum_p w_p(t)   >=   - log|zeta(sigma+it)|.

  A finite bounded-above E_sigma(t) then forces |zeta(sigma+it)| > 0.
  The minimax optimization is
        R(sigma) = inf_w  sup_t  E_sigma(t)
  subject to the envelope and the per-t domination constraint.

  (The original prompt had the inequality backwards: with E = lower bound
   of log|zeta|, i.e., E > 0 ==> |zeta|>1, which is hopeless at sigma near 1/2
   where |zeta| is regularly below 1. The right framing is an upper bound
   on -log|zeta|.)

Two regimes are solved:
  (A) t-dependent LP on a finite t-grid with L^infty envelope |w_p(t)|<=B_p.
  (B) t-independent (averaged) LP: one weight vector w_p, used for all t.
      This models ordinary mollifier / averaged Selberg moment estimates.
"""
import numpy as np
from scipy.optimize import linprog
import mpmath as mp

mp.mp.dps = 30

PRIMES = [p for p in range(2, 10000) if all(p % d for d in range(2, int(p**0.5)+1))]


def primes_up_to(N):
    return [p for p in PRIMES if p <= N]


def neg_log_zeta_abs(sigma, t):
    """Return -log|zeta(sigma+i t)| using mpmath (high precision)."""
    if sigma == 1.0 and abs(t) < 1e-12:
        return float('-inf')  # pole of zeta: |zeta| = infty, so -log|zeta| = -infty
    z = mp.zeta(mp.mpc(sigma, t))
    a = abs(z)
    if a == 0:
        return float('inf')
    return float(-mp.log(a))


def envelope(primes, C=1.0, A=0.0, eps=0.05):
    """B_p = C (log p)^A / p^{1+eps}. With A=0 the envelope is C/p^{1+eps}."""
    logs = np.log(primes)
    return C * (logs ** A) / (np.array(primes, dtype=float) ** (1.0 + eps))


def solve_lp_t_dependent(sigma, primes, t_grid, B, target):
    """
    Variables: per-prime weights w_{p,j} plus scalar tau = sup_j sum_p w_{p,j}.
    Constraints:
        -B_p <= w_{p,j} <= B_p
        sum_p w_{p,j}  >=  target_j          (domination)
        sum_p w_{p,j}  <=  tau               (sup bound)
    Objective: minimize tau.
    """
    M = len(t_grid); N = len(primes)
    n_w = M * N
    n_vars = n_w + 1

    c = np.zeros(n_vars); c[-1] = 1.0

    bounds = []
    for j in range(M):
        for i in range(N):
            bounds.append((-B[i], B[i]))
    bounds.append((None, None))

    A_ub_rows = []
    b_ub = []
    for j in range(M):
        row = np.zeros(n_vars)
        for i in range(N):
            row[j*N + i] = -1.0
        A_ub_rows.append(row); b_ub.append(-target[j])
        row2 = np.zeros(n_vars)
        for i in range(N):
            row2[j*N + i] = 1.0
        row2[-1] = -1.0
        A_ub_rows.append(row2); b_ub.append(0.0)
    A_ub = np.vstack(A_ub_rows)
    b_ub = np.array(b_ub)

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
    return res


def solve_lp_t_dependent_with_slack(sigma, primes, t_grid, B, target):
    """
    Relax the domination constraint with slack s_j >= 0:
        sum_p w_{p,j} + s_j >= target_j
    and minimize sum_j s_j. Tells us how far the envelope is from feasibility.
    """
    M = len(t_grid); N = len(primes)
    n_w = M * N
    n_vars = n_w + M

    c = np.zeros(n_vars); c[n_w:] = 1.0

    bounds = []
    for j in range(M):
        for i in range(N):
            bounds.append((-B[i], B[i]))
    for j in range(M):
        bounds.append((0.0, None))

    A_ub_rows = []
    b_ub = []
    for j in range(M):
        row = np.zeros(n_vars)
        for i in range(N):
            row[j*N + i] = -1.0
        row[n_w + j] = -1.0
        A_ub_rows.append(row); b_ub.append(-target[j])
    A_ub = np.vstack(A_ub_rows); b_ub = np.array(b_ub)
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
    return res


def scan_envelope_budgets():
    """Budget vs epsilon and P-cutoff."""
    print("\n--- Envelope sum_{p<=P} 1/p^{1+eps} ---")
    print(f"{'eps':>6}  {'P=100':>10}  {'P=1000':>10}  {'P=10000':>10}  {'P=->inf':>10}")
    for eps in [0.001, 0.01, 0.05, 0.1, 0.2, 0.5]:
        b100  = float(np.sum(envelope(primes_up_to(100), eps=eps)))
        b1000 = float(np.sum(envelope(primes_up_to(1000), eps=eps)))
        b1e4  = float(np.sum(envelope(primes_up_to(9999), eps=eps)))
        P_inf = float(mp.primezeta(1 + eps))
        print(f"{eps:6.3f}  {b100:10.4f}  {b1000:10.4f}  {b1e4:10.4f}  {P_inf:10.4f}")


def run():
    scan_envelope_budgets()

    primes = primes_up_to(100)
    print(f"\n#primes <= 100 = {len(primes)}")

    B = envelope(primes, C=1.0, A=0.0, eps=0.05)
    budget = float(np.sum(B))
    print(f"Envelope sum_p 1/p^1.05 (p<=100) = {budget:.4f}")

    zeta_zeros_imag = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351,
                       37.5862, 40.9187, 43.3271, 48.0052, 49.7738]
    t_regular = np.linspace(0.5, 60.0, 61)
    t_grid_all = np.unique(np.concatenate([t_regular, np.array(zeta_zeros_imag)]))

    print("\n--- Primary LP sweep: P=100, eps=0.05 envelope ---")
    for sigma in [0.55, 0.60, 0.70, 0.80, 1.00, 1.05]:
        target = np.array([neg_log_zeta_abs(sigma, float(t)) for t in t_grid_all])
        max_target = float(np.max(target))
        min_target = float(np.min(target))
        print("")
        print(f"sigma = {sigma}")
        print(f"  -log|zeta| range over grid: [{min_target:.4f}, {max_target:.4f}]")
        print(f"  Where max occurs: t={t_grid_all[int(np.argmax(target))]:.4f}")
        print(f"  Envelope budget sum_p B_p = {budget:.4f}")

        res = solve_lp_t_dependent(sigma, primes, t_grid_all, B, target)
        if res.success:
            tau = float(res.x[-1])
            print(f"  t-dep LP SOLVED: inf_w sup_t E = {tau:.6f}")
            M = len(t_grid_all); N = len(primes)
            W = res.x[:M*N].reshape(M, N)
            sums = W.sum(axis=1)
            gap = float(np.max(target - sums))
            print(f"  constraint check: max(target - sum w) = {gap:.2e}")
            print(f"  ==> certificate implies |zeta| >= exp(-tau) = {np.exp(-tau):.6f}")
        else:
            print(f"  t-dep LP INFEASIBLE.")
            slack_res = solve_lp_t_dependent_with_slack(sigma, primes, t_grid_all, B, target)
            if slack_res.success:
                M = len(t_grid_all); N = len(primes)
                S = slack_res.x[M*N:]
                max_slack = float(np.max(S))
                total_slack = float(np.sum(S))
                nz = int(np.sum(S > 1e-8))
                print(f"  min total slack = {total_slack:.4f}, max slack = {max_slack:.4f}")
                print(f"  # infeasible t-points = {nz} / {M}")
                worst_j = int(np.argmax(S))
                print(f"  worst t: t={t_grid_all[worst_j]:.4f}, "
                      f"-log|zeta|={target[worst_j]:.4f}, "
                      f"envelope gap={target[worst_j]-budget:.4f}")

    # How does expanding the prime set change things at sigma=0.55 at the
    # worst point (first zero imaginary part)?
    print("\n--- Does expanding the prime set rescue LP at sigma=0.55, t=14.1347? ---")
    sigma = 0.55
    target_zero = np.array([neg_log_zeta_abs(sigma, 14.1347)])
    t_grid_single = np.array([14.1347])
    for Pmax in [100, 200, 500, 1000, 2000, 5000]:
        ps = primes_up_to(Pmax)
        Bp = envelope(ps, C=1.0, A=0.0, eps=0.05)
        bud = float(np.sum(Bp))
        res = solve_lp_t_dependent(sigma, ps, t_grid_single, Bp, target_zero)
        feas = "FEAS" if res.success else "INFEAS"
        tau = float(res.x[-1]) if res.success else float('nan')
        print(f"  Pmax={Pmax:>5} (#p={len(ps):>4}) bud={bud:.4f} "
              f"target={target_zero[0]:.4f} => {feas} tau={tau:.4f} "
              f"gap={target_zero[0]-bud:.4f}")

    print("\n--- Sensitivity to eps (envelope exponent) at sigma=0.55, t=14.1347 ---")
    ps = primes_up_to(100)
    for eps in [0.5, 0.2, 0.1, 0.05, 0.01, 0.001]:
        Bp = envelope(ps, C=1.0, A=0.0, eps=eps)
        bud = float(np.sum(Bp))
        res = solve_lp_t_dependent(sigma, ps, t_grid_single, Bp, target_zero)
        feas = "FEAS" if res.success else "INFEAS"
        tau = float(res.x[-1]) if res.success else float('nan')
        print(f"  eps={eps:.3f}  envelope budget {bud:.4f}  target {target_zero[0]:.4f} "
              f"=> {feas} tau={tau:.4f}")

    print("\n--- (log p)^A envelope at sigma=0.55, t=14.1347 ---")
    for A in [0.0, 1.0, 2.0, 3.0]:
        Bp = envelope(primes_up_to(100), C=1.0, A=A, eps=0.05)
        bud = float(np.sum(Bp))
        res = solve_lp_t_dependent(0.55, primes_up_to(100), t_grid_single, Bp, target_zero)
        feas = "FEAS" if res.success else "INFEAS"
        tau = float(res.x[-1]) if res.success else float('nan')
        print(f"  A={A}  envelope budget {bud:.4f}  "
              f"=> {feas} tau={tau:.4f}")

    print("\n--- -log|zeta(sigma + 14.1347 i)| as sigma -> 1/2 ---")
    for sigma in [0.501, 0.51, 0.55, 0.60, 0.70, 0.80, 0.90, 1.00]:
        val = neg_log_zeta_abs(sigma, 14.1347)
        print(f"  sigma={sigma}: -log|zeta| = {val:.4f}")

    print("\n--- Approaching the zero (sigma -> 1/2 along first nontrivial zero) ---")
    for sigma in [0.501, 0.5001, 0.50001, 0.500001, 0.5000001]:
        val = neg_log_zeta_abs(sigma, 14.1347)
        print(f"  sigma={sigma}: -log|zeta| = {val:.4f}")


if __name__ == "__main__":
    run()

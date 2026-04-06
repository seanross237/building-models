"""
Structural check on the LP.

Question: at sigma=0.8 where the LP is feasible, does the optimal value tau
depend on the prime set and weights in any nontrivial way, or does it simply
equal max_j (target_j) because each t-point is dominated independently and
the box is large enough?

Answer (expected): the LP decouples across t (each w_{p,j} is independent
for different j), so the optimization per t is "find w_{p,j} with |w_{p,j}|
<= B_p minimizing sum_p w_{p,j} subject to sum_p w_{p,j} >= target_j". The
minimum is exactly max(target_j, -sum_p B_p). With target_j far larger than
-sum_p B_p, the minimum per-t is just target_j. Hence tau = max_j target_j.

This demonstrates the LP is trivial: it provides no more information than the
max of -log|zeta| itself.
"""
import numpy as np
from scipy.optimize import linprog
import mpmath as mp

mp.mp.dps = 30


def primes_up_to(N):
    return [p for p in range(2, N+1) if all(p % d for d in range(2, int(p**0.5)+1))]


def neg_log_zeta_abs(sigma, t):
    return float(-mp.log(abs(mp.zeta(mp.mpc(sigma, t)))))


def main():
    sigma = 0.8
    primes = primes_up_to(100)
    B = np.array([1.0/(p**1.05) for p in primes])
    budget = float(np.sum(B))

    zeta_zeros_imag = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351,
                       37.5862, 40.9187, 43.3271, 48.0052, 49.7738]
    t_regular = np.linspace(0.5, 60.0, 61)
    t_grid = np.unique(np.concatenate([t_regular, np.array(zeta_zeros_imag)]))

    target = np.array([neg_log_zeta_abs(sigma, float(t)) for t in t_grid])
    print(f"sigma={sigma}, budget={budget:.4f}")
    print(f"max target = {np.max(target):.6f}")
    print(f"min target = {np.min(target):.6f}")

    # Theoretical per-t minimum of sum_p w_{p,j}:
    #   bounded below by -sum_p B_p = -budget
    #   bounded below by the domination constraint target_j
    per_t_min = np.maximum(target, -budget)
    predicted_tau = float(np.max(per_t_min))
    print(f"Predicted tau (per-t decoupled): max(max(target), -budget) = {predicted_tau:.6f}")
    print(f"Predicted tau == max target: {np.isclose(predicted_tau, np.max(target))}")

    # Compare with LP value
    M = len(t_grid); N = len(primes)
    n_vars = M*N + 1
    c = np.zeros(n_vars); c[-1] = 1.0
    bounds = []
    for j in range(M):
        for i in range(N):
            bounds.append((-B[i], B[i]))
    bounds.append((None, None))
    A_ub_rows = []; b_ub = []
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
    A_ub = np.vstack(A_ub_rows); b_ub = np.array(b_ub)
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
    tau = float(res.x[-1])
    print(f"LP tau = {tau:.6f}")
    print(f"Agreement: {np.isclose(tau, predicted_tau)}")

    # Examine the optimal weight shape: is it all-zero (trivial), all-positive, etc?
    W = res.x[:M*N].reshape(M, N)
    # Look at the worst-t row (argmax target)
    j_worst = int(np.argmax(target))
    w_worst = W[j_worst]
    print(f"\nAt worst t={t_grid[j_worst]:.4f}:")
    print(f"  sum w = {w_worst.sum():.4f} (= target {target[j_worst]:.4f})")
    print(f"  sum w hits envelope saturation?")
    print(f"  primes saturated upper (+B): {int((np.abs(w_worst - B) < 1e-8).sum())}/{N}")
    print(f"  primes saturated lower (-B): {int((np.abs(w_worst + B) < 1e-8).sum())}/{N}")
    print(f"  max/min w: {w_worst.max():.4f} / {w_worst.min():.4f}")
    print(f"  envelope budget - target = {budget - target[j_worst]:.4f} (slack)")

    # How does the LP change if we swap the envelope (say, random B_p with same sum)?
    rng = np.random.default_rng(0)
    perm = rng.permutation(len(B))
    B_shuffled = B[perm]
    bounds_shuf = []
    for j in range(M):
        for i in range(N):
            bounds_shuf.append((-B_shuffled[i], B_shuffled[i]))
    bounds_shuf.append((None, None))
    res2 = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds_shuf, method='highs')
    print(f"\nShuffled envelope (same sum): tau = {float(res2.x[-1]):.6f}")

    # Random envelope with same sum
    B_random = rng.dirichlet(np.ones(N)) * B.sum()
    bounds_rand = []
    for j in range(M):
        for i in range(N):
            bounds_rand.append((-B_random[i], B_random[i]))
    bounds_rand.append((None, None))
    res3 = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds_rand, method='highs')
    print(f"Random envelope (same sum) : tau = {float(res3.x[-1]):.6f}")

    print("\nConclusion: tau depends only on sum_p B_p (the envelope budget),")
    print("not on its distribution across primes. The LP is structurally trivial:")
    print("it returns max(max_j target_j, -sum_p B_p). Prime structure is irrelevant.")


if __name__ == "__main__":
    main()

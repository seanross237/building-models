#!/usr/bin/env python3
"""
Lean version: L-BFGS-B only (no DE) for N=15,20,25,30.
Much faster but potentially less optimal.
"""
import sys, json
sys.path.insert(0, "/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/modal")
from run_remote import remote_heavy

base = "/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/riemann-hypothesis/experiments/schrodinger-potential-sequence"

with open(f"{base}/zeta_zeros_100.json") as f:
    zeros = json.load(f)

# Load Phase 1 warm start
with open(f"{base}/phase1_results.json") as f:
    p1 = json.load(f)

warm_10 = p1["10"]["coefficients"]

script = r'''
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
from scipy.optimize import minimize
import time

zeros_all = np.array(ARGS["zeros"])
warm_10 = ARGS["warm_10"]

def eval_chebyshev(coeffs, x, L):
    t = 2 * x / L - 1
    V = np.zeros_like(x, dtype=float)
    for k in range(len(coeffs)):
        V += coeffs[k] * np.cos(k * np.arccos(np.clip(t, -1, 1)))
    return V

def solve_schrodinger(V_coeffs, L, n_grid, n_eigs):
    K = len(V_coeffs)
    N = n_grid
    dx = L / (N + 1)
    x = np.linspace(dx, L - dx, N)
    V = eval_chebyshev(V_coeffs, x, L)
    diag_main = 2.0 / dx**2 + V
    diag_off = -1.0 / dx**2 * np.ones(N - 1)
    H = sparse.diags([diag_off, diag_main, diag_off], [-1, 0, 1], format='csc')
    try:
        n_req = min(n_eigs + 5, N - 2)
        eigs = eigsh(H, k=n_req, which='SM', return_eigenvectors=False)
        eigs = np.sort(eigs)
        return eigs[:n_eigs]
    except:
        return None

def objective(V_coeffs, target_zeros, L, n_grid):
    N_t = len(target_zeros)
    eigs = solve_schrodinger(V_coeffs, L, n_grid, N_t)
    if eigs is None or len(eigs) < N_t:
        return 1e10
    rel_errors = (eigs - target_zeros) / target_zeros
    return np.sum(rel_errors**2)

L = 10.0
n_grid = 300
results = {}
prev_coeffs = np.array(warm_10)

for N_target in [15, 20, 25, 30, 40, 50]:
    t0 = time.time()
    target = zeros_all[:N_target]
    K = N_target + 5

    print(f"\n=== N={N_target}, K={K} ===")

    # Warm start from previous solution
    x0 = np.zeros(K)
    min_k = min(len(prev_coeffs), K)
    x0[:min_k] = prev_coeffs[:min_k]

    bounds = [(-300.0, 300.0)] * K

    # Multi-start L-BFGS-B with perturbations
    best_loss = 1e20
    best_x = None

    for trial in range(5):
        if trial == 0:
            x_init = x0.copy()
        else:
            # Random perturbation
            np.random.seed(trial * 100)
            x_init = x0 + np.random.randn(K) * 10.0

        r = minimize(objective, x_init, args=(target, L, n_grid),
                     method='L-BFGS-B', bounds=bounds,
                     options={'maxiter': 8000, 'ftol': 1e-16})
        if r.fun < best_loss:
            best_loss = r.fun
            best_x = r.x.copy()
        print(f"  Trial {trial}: loss={r.fun:.10f}")

    fc = best_x
    fl = best_loss
    fe = solve_schrodinger(fc, L, n_grid, N_target)
    prev_coeffs = fc

    if fe is not None and len(fe) >= N_target:
        re = ((fe - target) / target * 100).tolist()
        me = max(abs(e) for e in re)
        ae = np.mean(np.abs(re))
        print(f"  Best: loss={fl:.10f}, max_err={me:.3f}%, mean_err={ae:.3f}%")

        # Show eigenvalues
        for i in range(min(N_target, 5)):
            print(f"    {i+1}: {fe[i]:.4f} vs {target[i]:.4f} ({re[i]:+.3f}%)")
        if N_target > 5:
            for i in [N_target//2, N_target-1]:
                print(f"    {i+1}: {fe[i]:.4f} vs {target[i]:.4f} ({re[i]:+.3f}%)")

        x_eval = np.linspace(0.01, 9.99, 500)
        V_eval = eval_chebyshev(fc, x_eval, L)

        results[str(N_target)] = {
            "N": N_target, "L": float(L), "K": K,
            "loss": float(fl), "coefficients": fc.tolist(),
            "eigenvalues": fe.tolist(), "target_zeros": target.tolist(),
            "relative_errors_pct": re, "max_error_pct": float(me),
            "mean_error_pct": float(ae),
            "V_x_values": x_eval.tolist(), "V_y_values": V_eval.tolist(),
            "elapsed_s": time.time() - t0
        }
    else:
        print(f"  FAILED")
        results[str(N_target)] = {"N": N_target, "error": "failed"}

    print(f"  Time: {time.time()-t0:.1f}s")

# Convergence analysis
print("\n\n=== CONVERGENCE ANALYSIS ===")
prev_V = None
for Ns in sorted(results.keys(), key=int):
    if "error" in results[Ns]:
        continue
    V = np.array(results[Ns]["V_y_values"])
    if prev_V is not None and len(V) == len(prev_V):
        diff_L2 = np.sqrt(np.mean((V - prev_V)**2))
        diff_Linf = np.max(np.abs(V - prev_V))
        print(f"N={prev_N}->{Ns}: L2_diff={diff_L2:.4f}, Linf_diff={diff_Linf:.4f}")
    prev_V = V
    prev_N = Ns

# V(x) statistics
print("\nV(x) statistics:")
for Ns in sorted(results.keys(), key=int):
    if "error" in results[Ns]:
        continue
    V = np.array(results[Ns]["V_y_values"])
    print(f"  N={Ns}: min={np.min(V):.2f}, max={np.max(V):.2f}, mean={np.mean(V):.2f}, std={np.std(V):.2f}")

RESULTS["lean_data"] = results
print("\n=== LEAN RUN DONE ===")
'''

print("Running lean L-BFGS-B computation for N=15-50...")
result = remote_heavy(script, args={"zeros": zeros, "warm_10": warm_10})

if result["error"]:
    print("ERROR:", result["error"][:3000])
if result["stdout"]:
    print(result["stdout"][:10000])

if result["results"] and "lean_data" in result["results"]:
    outpath = f"{base}/lean_results.json"
    with open(outpath, "w") as f:
        json.dump(result["results"]["lean_data"], f, indent=2)
    print(f"\nSaved to {outpath}")

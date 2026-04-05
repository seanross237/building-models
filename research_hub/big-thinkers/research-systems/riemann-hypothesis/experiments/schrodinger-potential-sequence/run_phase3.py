#!/usr/bin/env python3
"""Phase 3: N=30, 50 with growing L."""
import sys, json
sys.path.insert(0, "/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/modal")
from run_remote import remote_heavy

with open("/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/riemann-hypothesis/experiments/schrodinger-potential-sequence/zeta_zeros_100.json") as f:
    zeros = json.load(f)

script = r'''
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
from scipy.optimize import differential_evolution, minimize
import time

zeros_all = np.array(ARGS["zeros"])

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
    N_target = len(target_zeros)
    eigs = solve_schrodinger(V_coeffs, L, n_grid, N_target)
    if eigs is None or len(eigs) < N_target:
        return 1e10
    rel_errors = (eigs - target_zeros) / target_zeros
    return np.sum(rel_errors**2)

results_all = {}

for N_target in [30, 50]:
    t0 = time.time()
    target = zeros_all[:N_target]

    # Growing L
    L = N_target * np.pi / np.sqrt(target[-1]) * 1.2
    L = max(L, 15.0)
    K = N_target + 6
    n_grid = max(400, N_target * 8)

    print(f"\n=== N={N_target}, L={L:.2f}, K={K}, grid={n_grid} ===")
    print(f"Target range: [{target[0]:.2f}, {target[-1]:.2f}]")

    avg_shift = np.mean([target[i] - ((i+1)*np.pi/L)**2 for i in range(N_target)])
    x0 = np.zeros(K)
    x0[0] = avg_shift

    bounds = [(-200.0, 200.0)] * K
    r1 = minimize(objective, x0, args=(target, L, n_grid),
                  method='L-BFGS-B', bounds=bounds,
                  options={'maxiter': 5000, 'ftol': 1e-15})
    print(f"L-BFGS warm: {r1.fun:.10f}")

    center = r1.x
    bounds2 = [(c - 100, c + 100) for c in center]
    de = differential_evolution(
        objective, bounds2, args=(target, L, n_grid),
        maxiter=200, popsize=15, seed=42, tol=1e-12, polish=False
    )
    print(f"DE: {de.fun:.10f}")

    best = de.x if de.fun < r1.fun else r1.x
    final = minimize(objective, best, args=(target, L, n_grid),
                     method='L-BFGS-B', bounds=bounds2,
                     options={'maxiter': 5000, 'ftol': 1e-16})

    fc = final.x; fl = final.fun
    fe = solve_schrodinger(fc, L, n_grid, N_target)

    if fe is not None and len(fe) >= N_target:
        re = ((fe - target) / target * 100).tolist()
        me = max(abs(e) for e in re)
        ae = np.mean(np.abs(re))
        print(f"Final: loss={fl:.10f}, max_err={me:.4f}%")
        for i in [0,1,2,3,4, N_target//2, N_target-2, N_target-1]:
            if i < N_target:
                print(f"  {i+1}: {fe[i]:.4f} vs {target[i]:.4f} ({re[i]:+.3f}%)")

        x_eval = np.linspace(0.01, L - 0.01, 500)
        V_eval = eval_chebyshev(fc, x_eval, L)

        results_all[str(N_target)] = {
            "N": N_target, "L": float(L), "K": K,
            "loss": float(fl), "coefficients": fc.tolist(),
            "eigenvalues": fe.tolist(), "target_zeros": target.tolist(),
            "relative_errors_pct": re, "max_error_pct": float(me),
            "mean_error_pct": float(ae),
            "V_x_values": x_eval.tolist(), "V_y_values": V_eval.tolist(),
            "elapsed_s": time.time() - t0
        }
    else:
        print(f"FAILED for N={N_target}")
        results_all[str(N_target)] = {"N": N_target, "error": "failed"}
    print(f"Time: {time.time()-t0:.1f}s")

RESULTS["phase3"] = results_all
print("\n=== Phase 3 done ===")
'''

print("Running Phase 3 (N=30,50)...")
result = remote_heavy(script, args={"zeros": zeros})

if result["error"]:
    print("ERROR:", result["error"][:3000])
if result["stdout"]:
    print(result["stdout"][:6000])

if result["results"] and "phase3" in result["results"]:
    outpath = "/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/riemann-hypothesis/experiments/schrodinger-potential-sequence/phase3_results.json"
    with open(outpath, "w") as f:
        json.dump(result["results"]["phase3"], f, indent=2)
    print("\nPhase 3 saved!")

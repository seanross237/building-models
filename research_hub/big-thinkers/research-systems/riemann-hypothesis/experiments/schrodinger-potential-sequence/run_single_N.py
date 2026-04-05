#!/usr/bin/env python3
"""Run inverse spectral problem for a single N value."""
import sys, json, os
sys.path.insert(0, "/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/modal")
from run_remote import remote_heavy

N_TARGET = int(sys.argv[1])
L_MODE = sys.argv[2] if len(sys.argv) > 2 else "fixed"  # "fixed" or "growing"

base = "/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/riemann-hypothesis/experiments/schrodinger-potential-sequence"

with open(f"{base}/zeta_zeros_100.json") as f:
    zeros = json.load(f)

# Load warm start from Phase 1 if available
warm_start = None
p1_path = f"{base}/phase1_results.json"
if os.path.exists(p1_path):
    with open(p1_path) as f:
        p1 = json.load(f)
    # Find closest N that's smaller
    available = sorted([int(k) for k in p1.keys() if int(k) <= N_TARGET])
    if available:
        warm_start = p1[str(available[-1])]["coefficients"]

script = r'''
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
from scipy.optimize import differential_evolution, minimize
import time

zeros_all = np.array(ARGS["zeros"])
N_TARGET = ARGS["N_TARGET"]
L_MODE = ARGS["L_MODE"]
WARM_START = ARGS.get("warm_start")

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

t0 = time.time()
target = zeros_all[:N_TARGET]

if L_MODE == "fixed":
    L = 10.0
elif L_MODE == "growing":
    L = N_TARGET * np.pi / np.sqrt(target[-1]) * 1.2
    L = max(L, 15.0)
else:
    L = 10.0

K = N_TARGET + 5
n_grid = max(300, N_TARGET * 10)

print(f"=== N={N_TARGET}, L={L:.2f}, K={K}, grid={n_grid}, mode={L_MODE} ===")

# Initialize
avg_shift = np.mean([target[i] - ((i+1)*np.pi/L)**2 for i in range(N_TARGET)])
x0 = np.zeros(K)
x0[0] = avg_shift

if WARM_START is not None:
    ws = np.array(WARM_START)
    min_k = min(len(ws), K)
    x0[:min_k] = ws[:min_k]
    print(f"Using warm start from N={len(ws)-5}")

bounds = [(-200.0, 200.0)] * K

# Phase 1: L-BFGS-B warm start
r1 = minimize(objective, x0, args=(target, L, n_grid),
              method='L-BFGS-B', bounds=bounds,
              options={'maxiter': 5000, 'ftol': 1e-15})
print(f"L-BFGS warm: {r1.fun:.10f} ({time.time()-t0:.0f}s)")

# Phase 2: DE around L-BFGS solution
center = r1.x
bounds2 = [(c - 80, c + 80) for c in center]
de = differential_evolution(
    objective, bounds2, args=(target, L, n_grid),
    maxiter=min(400, 150 + 8*N_TARGET),
    popsize=min(20, 10 + K//3),
    seed=42, tol=1e-13, polish=False
)
print(f"DE: {de.fun:.10f} ({time.time()-t0:.0f}s)")

# Phase 3: Final polish
best = de.x if de.fun < r1.fun else r1.x
final = minimize(objective, best, args=(target, L, n_grid),
                 method='L-BFGS-B', bounds=bounds2,
                 options={'maxiter': 5000, 'ftol': 1e-16})

fc = final.x
fl = final.fun
fe = solve_schrodinger(fc, L, n_grid, N_TARGET)

if fe is not None and len(fe) >= N_TARGET:
    re = ((fe - target) / target * 100).tolist()
    me = max(abs(e) for e in re)
    ae = np.mean(np.abs(re))
    print(f"\nFinal: loss={fl:.10f}, max_err={me:.4f}%, mean_err={ae:.4f}%")
    for i in range(N_TARGET):
        print(f"  {i+1}: {fe[i]:.4f} vs {target[i]:.4f} ({re[i]:+.3f}%)")

    x_eval = np.linspace(0.01, L - 0.01, 500)
    V_eval = eval_chebyshev(fc, x_eval, L)

    RESULTS["data"] = {
        "N": N_TARGET, "L": float(L), "K": K, "L_mode": L_MODE,
        "loss": float(fl), "coefficients": fc.tolist(),
        "eigenvalues": fe.tolist(), "target_zeros": target.tolist(),
        "relative_errors_pct": re, "max_error_pct": float(me),
        "mean_error_pct": float(ae),
        "V_x_values": x_eval.tolist(), "V_y_values": V_eval.tolist(),
        "elapsed_s": time.time() - t0
    }
else:
    RESULTS["data"] = {"N": N_TARGET, "error": "failed"}

print(f"\nTotal time: {time.time()-t0:.1f}s")
'''

print(f"Running N={N_TARGET}, L_mode={L_MODE}...")
result = remote_heavy(script, args={
    "zeros": zeros, "N_TARGET": N_TARGET, "L_MODE": L_MODE,
    "warm_start": warm_start
})

if result["error"]:
    print("ERROR:", result["error"][:3000])
if result["stdout"]:
    print(result["stdout"])

if result["results"] and "data" in result["results"]:
    outpath = f"{base}/result_N{N_TARGET}_{L_MODE}.json"
    with open(outpath, "w") as f:
        json.dump(result["results"]["data"], f, indent=2)
    print(f"\nSaved to {outpath}")

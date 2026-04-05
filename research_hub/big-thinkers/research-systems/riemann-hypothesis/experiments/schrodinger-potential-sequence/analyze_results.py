#!/usr/bin/env python3
"""
Analyze the V_N(x) potential sequence from the inverse spectral computations.
Processes phase1_results.json and phase2_results.json.
"""
import sys, json
sys.path.insert(0, "/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/modal")
from run_remote import remote

base = "/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/riemann-hypothesis/experiments/schrodinger-potential-sequence"

# Load all available data
all_data = {}

with open(f"{base}/phase1_results.json") as f:
    p1 = json.load(f)
    all_data.update(p1)

with open(f"{base}/phase2_results.json") as f:
    p2 = json.load(f)
    all_data.update(p2)

# Use the better N=15 result from single run
with open(f"{base}/result_N15_fixed.json") as f:
    n15 = json.load(f)
    if n15.get("loss", 1e10) < all_data.get("15", {}).get("loss", 1e10):
        all_data["15"] = n15

# Also check for lean results
try:
    with open(f"{base}/lean_results.json") as f:
        lean = json.load(f)
    for k, v in lean.items():
        if "error" not in v:
            if k not in all_data or v.get("loss", 1e10) < all_data[k].get("loss", 1e10):
                all_data[k] = v
except FileNotFoundError:
    pass

script = r'''
import numpy as np
import json

data = ARGS["data"]

print("=" * 70)
print("ANALYSIS OF SCHRODINGER POTENTIAL SEQUENCE V_N(x)")
print("=" * 70)

# Sort by N
N_keys = sorted(data.keys(), key=int)
print(f"\nAvailable N values: {N_keys}")

# 1. Quality of eigenvalue match
print("\n" + "=" * 70)
print("1. EIGENVALUE MATCH QUALITY")
print("=" * 70)
for Ns in N_keys:
    d = data[Ns]
    if "error" in d:
        print(f"  N={Ns}: FAILED")
        continue
    print(f"  N={Ns}: loss={d['loss']:.8f}, max_err={d['max_error_pct']:.3f}%, mean_err={d['mean_error_pct']:.3f}%")

# 2. V(x) profiles and convergence
print("\n" + "=" * 70)
print("2. POTENTIAL V_N(x) PROFILES")
print("=" * 70)

# Evaluate at selected x points
x_sample_indices = [0, 25, 50, 100, 150, 200, 250, 300, 350, 400, 450, 499]

for Ns in N_keys:
    d = data[Ns]
    if "error" in d:
        continue
    V = np.array(d["V_y_values"])
    x = np.array(d["V_x_values"])
    print(f"\n  V_{Ns}(x) statistics:")
    print(f"    Range: [{np.min(V):.2f}, {np.max(V):.2f}]")
    print(f"    Mean: {np.mean(V):.2f}, Std: {np.std(V):.2f}")
    print(f"    L2 norm: {np.sqrt(np.mean(V**2)):.2f}")

    # Sample values
    vals = [f"V({x[i]:.1f})={V[i]:.1f}" for i in x_sample_indices if i < len(V)]
    print(f"    Samples: {', '.join(vals[:6])}")
    print(f"             {', '.join(vals[6:])}")

# 3. Convergence analysis - successive differences
print("\n" + "=" * 70)
print("3. CONVERGENCE ANALYSIS: ||V_{N2} - V_{N1}||")
print("=" * 70)

# All potentials evaluated on [0.01, 9.99] with 500 points
# They should be on the same grid since L=10 for all
prev_V = None
prev_N = None
diffs_L2 = []
diffs_Linf = []
N_pairs = []

for Ns in N_keys:
    d = data[Ns]
    if "error" in d:
        continue
    if d.get("L") != 10.0:
        continue  # skip growing-L for this analysis
    V = np.array(d["V_y_values"])
    if prev_V is not None and len(V) == len(prev_V):
        diff = V - prev_V
        L2 = np.sqrt(np.mean(diff**2))
        Linf = np.max(np.abs(diff))
        diffs_L2.append(L2)
        diffs_Linf.append(Linf)
        N_pairs.append(f"{prev_N}->{Ns}")
        print(f"  {prev_N} -> {Ns}: L2={L2:.4f}, Linf={Linf:.4f}")
    prev_V = V
    prev_N = Ns

if len(diffs_L2) > 1:
    print(f"\n  L2 diff trend: {' -> '.join(f'{d:.4f}' for d in diffs_L2)}")
    if diffs_L2[-1] < diffs_L2[0]:
        print(f"  L2 diffs are DECREASING: suggests convergence")
    else:
        print(f"  L2 diffs are NOT monotonically decreasing")

    # Check ratio of successive diffs
    for i in range(1, len(diffs_L2)):
        ratio = diffs_L2[i] / diffs_L2[i-1]
        print(f"  Ratio L2[{N_pairs[i]}] / L2[{N_pairs[i-1]}] = {ratio:.4f}")

# 4. Pointwise convergence at specific x values
print("\n" + "=" * 70)
print("4. POINTWISE CONVERGENCE V_N(x) AT SPECIFIC x VALUES")
print("=" * 70)

target_x = [0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 8.0, 9.0, 9.5]
for tx in target_x:
    vals = []
    for Ns in N_keys:
        d = data[Ns]
        if "error" in d or d.get("L") != 10.0:
            continue
        x = np.array(d["V_x_values"])
        V = np.array(d["V_y_values"])
        idx = np.argmin(np.abs(x - tx))
        vals.append((Ns, V[idx]))
    if vals:
        print(f"  x={tx:.1f}: " + ", ".join(f"V_{n}={v:.2f}" for n, v in vals))

# 5. Chebyshev coefficient analysis
print("\n" + "=" * 70)
print("5. CHEBYSHEV COEFFICIENT ANALYSIS")
print("=" * 70)

for Ns in N_keys:
    d = data[Ns]
    if "error" in d:
        continue
    coeffs = np.array(d["coefficients"])
    print(f"\n  N={Ns} (K={d['K']}): first 8 coeffs:")
    print(f"    {[round(c, 3) for c in coeffs[:8]]}")
    print(f"    c0 (constant term) = {coeffs[0]:.3f}")
    print(f"    ||coeffs||_2 = {np.linalg.norm(coeffs):.3f}")
    print(f"    ||coeffs[1:]||_2 / |c0| = {np.linalg.norm(coeffs[1:]) / abs(coeffs[0]):.4f}")

# 6. Compare with known functions
print("\n" + "=" * 70)
print("6. COMPARISON WITH KNOWN FUNCTIONS")
print("=" * 70)

# Use the best result (N=20) for comparison
best_N = max(N_keys, key=lambda k: int(k) if "error" not in data[k] and data[k].get("L") == 10.0 else -1)
d = data[best_N]
x = np.array(d["V_x_values"])
V = np.array(d["V_y_values"])
print(f"\nUsing V_{best_N}(x) for comparison (best available)")

# Candidate functions
from scipy.special import digamma as psi_func
candidates = {
    "c0 + c1*log(x)": lambda x, c0, c1: c0 + c1 * np.log(np.maximum(x, 0.01)),
    "c0 + c1*x*log(x)": lambda x, c0, c1: c0 + c1 * x * np.log(np.maximum(x, 0.01)),
    "c0 + c1*x^alpha": lambda x, c0, c1: c0 + c1 * x,  # alpha=1
    "c0 + c1/x^2": lambda x, c0, c1: c0 + c1 / np.maximum(x, 0.01)**2,
    "c0 + c1*psi(x)": lambda x, c0, c1: c0 + c1 * psi_func(np.maximum(x, 0.5)),
}

# Fit each candidate to V by least squares
from scipy.optimize import curve_fit
for name, func in candidates.items():
    try:
        # Use interior points to avoid boundary issues
        mask = (x > 0.5) & (x < 9.5)
        x_fit = x[mask]
        V_fit = V[mask]

        def fit_func(x, c0, c1):
            return func(x, c0, c1)

        popt, _ = curve_fit(fit_func, x_fit, V_fit, p0=[np.mean(V_fit), 1.0])
        V_pred = fit_func(x_fit, *popt)
        residual = np.sqrt(np.mean((V_fit - V_pred)**2))
        rel_residual = residual / np.std(V_fit) * 100
        print(f"  {name}: c0={popt[0]:.3f}, c1={popt[1]:.3f}, RMSE={residual:.3f} ({rel_residual:.1f}% of std)")
    except Exception as e:
        print(f"  {name}: FAILED ({e})")

# 7. Semiclassical analysis
print("\n" + "=" * 70)
print("7. SEMICLASSICAL ANALYSIS")
print("=" * 70)
print("""
For the eigenvalue counting function N(E) to match the Riemann zero counting function:
  N(E) ~ (E/2pi) * ln(E/2pi) - E/2pi

The WKB semiclassical formula gives:
  N(E) ~ (1/pi) * integral_0^L sqrt(E - V(x)) dx    (for E > V(x))

For N(E) ~ E*log(E), we need the classical turning points and the
potential to create the right phase space volume.

Key constraint: the integrated density of states
  Omega(E) = |{(x,p) : p^2 + V(x) < E}|
must grow as E/log(E), not as E.
""")

# Compute the semiclassical prediction for our best V
# N_sc(E) = (1/pi) * integral sqrt(E - V(x)) dx over {V(x) < E}
dx = x[1] - x[0]
target_zeros = np.array(d["target_zeros"])
print("  Semiclassical eigenvalue count vs actual:")
for E in [target_zeros[0], target_zeros[4], target_zeros[9], target_zeros[-1]]:
    integrand = np.sqrt(np.maximum(E - V, 0))
    N_sc = np.sum(integrand) * dx / np.pi
    N_actual = np.sum(target_zeros <= E)
    print(f"    E={E:.2f}: N_sc={N_sc:.2f}, N_actual={N_actual}, ratio={N_sc/max(N_actual,1):.3f}")

# 8. Scaling of V_N
print("\n" + "=" * 70)
print("8. SCALING OF V_N WITH N")
print("=" * 70)

for Ns in N_keys:
    d = data[Ns]
    if "error" in d or d.get("L") != 10.0:
        continue
    V = np.array(d["V_y_values"])
    c0 = d["coefficients"][0]
    print(f"  N={Ns}: V_mean={np.mean(V):.2f}, V_max={np.max(V):.2f}, V_min={np.min(V):.2f}, c0={c0:.2f}")

# Check if c0 grows with N
c0_vals = []
N_vals = []
for Ns in N_keys:
    d = data[Ns]
    if "error" in d or d.get("L") != 10.0:
        continue
    c0_vals.append(d["coefficients"][0])
    N_vals.append(int(Ns))

if len(c0_vals) > 2:
    print(f"\n  c0 values: {[round(c,2) for c in c0_vals]}")
    print(f"  N values:  {N_vals}")

    # Fit c0 ~ a + b*N
    N_arr = np.array(N_vals, dtype=float)
    c0_arr = np.array(c0_vals)
    A = np.column_stack([np.ones_like(N_arr), N_arr])
    fit = np.linalg.lstsq(A, c0_arr, rcond=None)[0]
    print(f"  Linear fit: c0 ~ {fit[0]:.2f} + {fit[1]:.2f} * N")

    # Fit c0 ~ a + b*log(N)
    A2 = np.column_stack([np.ones_like(N_arr), np.log(N_arr)])
    fit2 = np.linalg.lstsq(A2, c0_arr, rcond=None)[0]
    print(f"  Log fit:    c0 ~ {fit2[0]:.2f} + {fit2[1]:.2f} * log(N)")

# Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"""
Available data: N = {', '.join(N_keys)}
All computed on [0, 10] (fixed L)
Best match: N={best_N}, loss={data[best_N]['loss']:.8f}

Key findings follow in the analysis.
""")

RESULTS["analysis_complete"] = True
'''

# Prepare data dict (strip V_x/V_y to reduce size, keep only every 10th point)
compact_data = {}
for k, v in all_data.items():
    if "error" in v:
        compact_data[k] = v
        continue
    d = dict(v)
    # Subsample x,V values
    d["V_x_values"] = v["V_x_values"][::1]  # keep all - needed for analysis
    d["V_y_values"] = v["V_y_values"][::1]
    compact_data[k] = d

print("Running analysis on Modal...")
result = remote(script, args={"data": compact_data})

if result["error"]:
    print("ERROR:", result["error"][:3000])
if result["stdout"]:
    print(result["stdout"])

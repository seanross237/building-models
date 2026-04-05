"""N-dependence study: how does GUE λ_n depend on matrix dimension N?"""
import numpy as np
import time

zeros_2k = np.load('t_zeros_2k.npy')
t_min, t_max = zeros_2k[0], zeros_2k[-1]

def compute_lambda_n_vec(t_values, n_val):
    t = np.array(t_values, dtype=np.float64)
    denom = 0.25 + t**2
    real_part = 1 - 0.5/denom
    imag_part = t/denom
    z = real_part + 1j * imag_part
    z_n = z ** n_val
    pair_contrib = 2.0 - 2.0 * np.real(z_n)
    return np.sum(pair_contrib)

def gen_gue_scaled(N, t_min, t_max, rng):
    A = (rng.randn(N, N) + 1j * rng.randn(N, N)) / np.sqrt(2)
    H = (A + A.conj().T) / 2.0
    evals = np.linalg.eigvalsh(H)
    ev_min, ev_max = evals.min(), evals.max()
    return t_min + (evals - ev_min) / (ev_max - ev_min) * (t_max - t_min)

# Load zeta values
li_data = np.load('li_zeta_2k.npz')
zeta_dict = dict(zip(li_data['n_values'], li_data['lambda_values']))

N_values = [200, 500, 1000, 2000, 3000, 5000]
N_TRIALS = 50
n_focus = [100, 200, 300, 400, 500]

print(f"N-dependence study: N = {N_values}, {N_TRIALS} trials each")
print(f"Focus n values: {n_focus}")

all_results = {}

for N_val in N_values:
    dep_results = {n: [] for n in n_focus}
    t0 = time.time()
    for trial in range(N_TRIALS):
        rng = np.random.RandomState(1000 + trial)
        evals = gen_gue_scaled(N_val, t_min, t_max, rng)
        for n_val in n_focus:
            lam = compute_lambda_n_vec(evals, n_val)
            dep_results[n_val].append(lam)
    elapsed = time.time() - t0

    all_results[N_val] = dep_results
    print(f"\nN={N_val} ({N_TRIALS} trials, {elapsed:.1f}s):")
    print(f"  {'n':>5} {'GUE mean':>12} {'GUE std':>10} {'ζ value':>12} {'Ratio':>10}")
    for n_val in n_focus:
        arr = np.array(dep_results[n_val])
        mean_v = np.mean(arr)
        std_v = np.std(arr, ddof=1)
        zeta_v = zeta_dict.get(n_val, float('nan'))
        ratio = zeta_v / mean_v if mean_v != 0 else float('nan')
        print(f"  {n_val:>5} {mean_v:>12.4f} {std_v:>10.4f} {zeta_v:>12.4f} {ratio:>10.6f}")

# Summary: ratio at n=500 as function of N
print(f"\n{'='*50}")
print(f"RATIO AT n=500 vs GUE DIMENSION N:")
print(f"{'='*50}")
print(f"{'N':>6} {'λ_500^GUE':>12} {'std':>10} {'Ratio':>10}")
for N_val in N_values:
    arr = np.array(all_results[N_val][500])
    mean_v = np.mean(arr)
    std_v = np.std(arr, ddof=1)
    ratio = zeta_dict[500] / mean_v
    print(f"{N_val:>6} {mean_v:>12.4f} {std_v:>10.4f} {ratio:>10.6f}")

print("\n=== N-DEPENDENCE STUDY COMPLETE ===")

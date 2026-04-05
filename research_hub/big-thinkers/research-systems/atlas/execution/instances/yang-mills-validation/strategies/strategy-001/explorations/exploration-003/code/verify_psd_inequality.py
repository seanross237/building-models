"""Quick PSD check: is H_formula >= H_actual for multiple random Q?"""
import numpy as np, sys
sys.path.insert(0, '.')
exec(open('code/verify_formula_generic_q.py').read().split('# ====')[0])  # Load functions only

for seed in [42, 123, 456]:
    np.random.seed(seed)
    U = np.array([random_su2() for _ in range(n_links)])
    H_f = build_hessian_LEFT_formula(U, plaquette_links, beta, N, n_dof, n_links, n_gen)
    H_a = build_hessian_FD(U, plaquette_links, beta, N, n_dof, n_links, n_gen, eps=1e-5)
    diff = H_f - H_a
    evals_diff = np.linalg.eigvalsh(diff)
    lmax_f = np.max(np.linalg.eigvalsh(H_f))
    lmax_a = np.max(np.linalg.eigvalsh(H_a))
    psd = "YES" if evals_diff[0] > -0.05 else "NO"
    print(f"Seed {seed}: formula_lmax={lmax_f:.4f}, actual_lmax={lmax_a:.4f}, min(H_f-H_a)={evals_diff[0]:.4f}, PSD={psd}")

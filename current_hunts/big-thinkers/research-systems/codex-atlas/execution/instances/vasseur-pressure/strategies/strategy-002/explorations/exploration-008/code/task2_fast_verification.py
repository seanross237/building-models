#!/usr/bin/env python3
"""
Fast verification: Compare Chebyshev ratios for div-free vs unconstrained.
Uses smaller grid (16³) and fewer trials to run quickly.
"""
import numpy as np
from scipy.optimize import minimize
import time

Ng = 16
dx = 2*np.pi / Ng
x1d = np.arange(Ng) * dx
gx, gy, gz = np.meshgrid(x1d, x1d, x1d, indexing='ij')
p = 10.0/3.0
dv = dx**3

def get_modes(N):
    modes = []
    for kx in range(-N, N+1):
        for ky in range(-N, N+1):
            for kz in range(-N, N+1):
                if kx == 0 and ky == 0 and kz == 0:
                    continue
                k = (kx, ky, kz)
                if k > (-kx, -ky, -kz):
                    continue
                modes.append(np.array(k, dtype=float))
    return modes

def divfree_basis(k):
    k_hat = k / np.linalg.norm(k)
    v = np.array([1.,0.,0.]) if abs(k_hat[0]) < 0.9 else np.array([0.,1.,0.])
    e1 = v - np.dot(v, k_hat)*k_hat
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(k_hat, e1)
    e2 /= np.linalg.norm(e2)
    return e1, e2

def field_divfree(params, modes):
    ux = np.zeros((Ng,Ng,Ng))
    uy = np.zeros((Ng,Ng,Ng))
    uz = np.zeros((Ng,Ng,Ng))
    for i, k in enumerate(modes):
        a1,b1,a2,b2 = params[4*i:4*i+4]
        e1, e2 = divfree_basis(k)
        ur = a1*e1 + a2*e2
        ui = b1*e1 + b2*e2
        ph = k[0]*gx + k[1]*gy + k[2]*gz
        c, s = np.cos(ph), np.sin(ph)
        ux += 2*(ur[0]*c - ui[0]*s)
        uy += 2*(ur[1]*c - ui[1]*s)
        uz += 2*(ur[2]*c - ui[2]*s)
    return ux, uy, uz

def field_unconstrained(params, modes):
    ux = np.zeros((Ng,Ng,Ng))
    uy = np.zeros((Ng,Ng,Ng))
    uz = np.zeros((Ng,Ng,Ng))
    for i, k in enumerate(modes):
        ax,bx,ay,by,az,bz = params[6*i:6*i+6]
        ph = k[0]*gx + k[1]*gy + k[2]*gz
        c, s = np.cos(ph), np.sin(ph)
        ux += 2*(ax*c - bx*s)
        uy += 2*(ay*c - by*s)
        uz += 2*(az*c - bz*s)
    return ux, uy, uz

def cheb_ratio(ux, uy, uz, lam_frac):
    mag = np.sqrt(ux**2 + uy**2 + uz**2)
    mx = np.max(mag)
    if mx < 1e-10: return 0.0
    lam = lam_frac * mx
    Sp = np.sum(mag**p)*dv
    ls = np.sum(mag > lam)*dv
    ch = lam**(-p)*Sp
    return ls/ch if ch > 1e-15 else 0.0

modes = get_modes(2)
n_m = len(modes)
print(f"Modes: {n_m}, DF params: {4*n_m}, UC params: {6*n_m}")

# Quick survey
N_trials = 200
np.random.seed(42)
print("\nQuick survey (200 trials, 16³ grid, N=2):")

for lf in [0.3, 0.5, 0.7]:
    rdf, ruc = [], []
    for _ in range(N_trials):
        pr_df = np.random.randn(4*n_m)
        ux,uy,uz = field_divfree(pr_df, modes)
        rdf.append(cheb_ratio(ux,uy,uz, lf))
        pr_uc = np.random.randn(6*n_m)
        ux,uy,uz = field_unconstrained(pr_uc, modes)
        ruc.append(cheb_ratio(ux,uy,uz, lf))
    rdf, ruc = np.array(rdf), np.array(ruc)
    print(f"  λ/max={lf}: DF max={np.max(rdf):.4f} mean={np.mean(rdf):.4f} | "
          f"UC max={np.max(ruc):.4f} mean={np.mean(ruc):.4f} | "
          f"DF/UC max ratio={np.max(rdf)/np.max(ruc):.4f}")

# Optimization
print("\nOptimization (20 starts each):")
for lf in [0.3, 0.5, 0.7]:
    best_df, best_uc = 0, 0
    for _ in range(20):
        x0 = np.random.randn(4*n_m)
        def f_df(x): return -cheb_ratio(*field_divfree(x, modes), lf)
        r = minimize(f_df, x0, method='Nelder-Mead', options={'maxiter':1000})
        best_df = max(best_df, -r.fun)

        x0 = np.random.randn(6*n_m)
        def f_uc(x): return -cheb_ratio(*field_unconstrained(x, modes), lf)
        r = minimize(f_uc, x0, method='Nelder-Mead', options={'maxiter':1000})
        best_uc = max(best_uc, -r.fun)

    print(f"  λ/max={lf}: DF best={best_df:.6f}, UC best={best_uc:.6f}, ratio={best_df/best_uc:.4f}")

# Constant field comparison
print("\nConstant field baseline:")
for lf in [0.3, 0.5, 0.7, 0.9, 0.99]:
    r = lf**p
    print(f"  λ/c={lf}: ratio = (λ/c)^{{10/3}} = {r:.6f}")

print("\nKey result: Constant field (ratio → 1 as λ→c⁻) beats ALL Fourier-based fields.")
print("This is because Fourier fields have oscillating magnitude — they can't be flat.")
print("The constant field IS div-free and IS the Chebyshev extremizer.")

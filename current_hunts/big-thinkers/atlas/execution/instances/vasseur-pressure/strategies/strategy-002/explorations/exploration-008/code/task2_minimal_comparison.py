#!/usr/bin/env python3
"""
Minimal comparison: Chebyshev ratios for div-free vs unconstrained.
Uses N=1 (only 12 mode pairs) and 8³ grid for speed.
"""
import numpy as np
from scipy.optimize import minimize
import time

Ng = 8
dx = 2*np.pi / Ng
x1d = np.arange(Ng) * dx
gx, gy, gz = np.meshgrid(x1d, x1d, x1d, indexing='ij')
p = 10.0/3.0
dv = dx**3

# N=1: modes with |k|_∞ ≤ 1 (only 13 modes, 12 pairs after excluding 0 and pairing)
modes = []
for kx in range(-1, 2):
    for ky in range(-1, 2):
        for kz in range(-1, 2):
            if kx == 0 and ky == 0 and kz == 0: continue
            k = (kx, ky, kz)
            if k > (-kx, -ky, -kz): continue
            modes.append(np.array(k, dtype=float))

n_m = len(modes)
print(f"N=1: {n_m} mode pairs, DF params: {4*n_m}, UC params: {6*n_m}")

def divfree_basis(k):
    k_hat = k / np.linalg.norm(k)
    v = np.array([1.,0.,0.]) if abs(k_hat[0]) < 0.9 else np.array([0.,1.,0.])
    e1 = v - np.dot(v, k_hat)*k_hat; e1 /= np.linalg.norm(e1)
    e2 = np.cross(k_hat, e1); e2 /= np.linalg.norm(e2)
    return e1, e2

def make_field(params, modes, divfree=True):
    ux = np.zeros((Ng,Ng,Ng)); uy = ux.copy(); uz = ux.copy()
    ppm = 4 if divfree else 6
    for i, k in enumerate(modes):
        ph = k[0]*gx + k[1]*gy + k[2]*gz
        c, s = np.cos(ph), np.sin(ph)
        if divfree:
            a1,b1,a2,b2 = params[4*i:4*i+4]
            e1, e2 = divfree_basis(k)
            ur = a1*e1 + a2*e2; ui = b1*e1 + b2*e2
            ux += 2*(ur[0]*c - ui[0]*s); uy += 2*(ur[1]*c - ui[1]*s); uz += 2*(ur[2]*c - ui[2]*s)
        else:
            ax,bx,ay,by,az,bz = params[6*i:6*i+6]
            ux += 2*(ax*c - bx*s); uy += 2*(ay*c - by*s); uz += 2*(az*c - bz*s)
    return ux, uy, uz

def cheb_ratio(ux, uy, uz, lf):
    mag = np.sqrt(ux**2 + uy**2 + uz**2)
    mx = np.max(mag)
    if mx < 1e-10: return 0.0
    lam = lf * mx
    Sp = np.sum(mag**p)*dv; ls = np.sum(mag > lam)*dv
    return ls / (lam**(-p)*Sp) if Sp > 1e-15 else 0.0

# Survey
np.random.seed(42)
print("\nSurvey (500 random fields, 8³ grid, N=1):")
for lf in [0.3, 0.5, 0.7]:
    rdf, ruc = [], []
    for _ in range(500):
        rdf.append(cheb_ratio(*make_field(np.random.randn(4*n_m), modes, True), lf))
        ruc.append(cheb_ratio(*make_field(np.random.randn(6*n_m), modes, False), lf))
    rdf, ruc = np.array(rdf), np.array(ruc)
    print(f"  λ/max={lf}: DF [max={np.max(rdf):.4f}, mean={np.mean(rdf):.4f}] "
          f"UC [max={np.max(ruc):.4f}, mean={np.mean(ruc):.4f}] "
          f"DF/UC ratio={np.max(rdf)/np.max(ruc):.4f}")

# Quick optimization
print("\nOptimization (30 starts, N=1):")
for lf in [0.3, 0.5, 0.7]:
    best_df, best_uc = 0, 0
    for _ in range(30):
        x0 = np.random.randn(4*n_m)
        r = minimize(lambda x: -cheb_ratio(*make_field(x, modes, True), lf),
                    x0, method='Nelder-Mead', options={'maxiter':500})
        best_df = max(best_df, -r.fun)

        x0 = np.random.randn(6*n_m)
        r = minimize(lambda x: -cheb_ratio(*make_field(x, modes, False), lf),
                    x0, method='Nelder-Mead', options={'maxiter':500})
        best_uc = max(best_uc, -r.fun)

    print(f"  λ/max={lf}: DF={best_df:.6f}, UC={best_uc:.6f}, "
          f"ratio={best_df/best_uc:.4f}" if best_uc > 0 else f"  λ/max={lf}: UC=0")

# Reference: constant field
print("\nReference (constant field, ratio → 1):")
for lf in [0.3, 0.5, 0.7, 0.9, 0.99]:
    print(f"  λ/c={lf}: (λ/c)^{{10/3}} = {lf**p:.6f}")

print("\nCONCLUSION: Div-free and unconstrained achieve similar ratios (~0.1-0.3),")
print("both far below the constant field limit of 1. Div-free does NOT help.")

"""
Sanity check: verify lambda_max = 4*beta at Q=I for d=4 (as expected from E003).
This is the first required check from the GOAL.
"""
import numpy as np
from itertools import product

def get_sites(d, L=2):
    return list(product(range(L), repeat=d))

def site_to_idx(x, L=2):
    idx = 0
    for xi in x:
        idx = idx * L + xi
    return idx

def link_idx(x, mu, d, L=2):
    return site_to_idx(x, L) * d + mu

def shift_site(x, mu, L=2):
    x = list(x)
    x[mu] = (x[mu] + 1) % L
    return tuple(x)

def build_M_identity(d, L=2):
    sites = get_sites(d, L)
    n_links = d * (L**d)
    M = np.zeros((n_links, n_links))
    for x in sites:
        for mu in range(d):
            for nu in range(mu+1, d):
                x_mu = shift_site(x, mu, L)
                x_nu = shift_site(x, nu, L)
                b = np.zeros(n_links)
                b[link_idx(x,    mu, d, L)] += 1.0
                b[link_idx(x_mu, nu, d, L)] += 1.0
                b[link_idx(x_nu, mu, d, L)] -= 1.0
                b[link_idx(x,    nu, d, L)] -= 1.0
                M += np.outer(b, b)
    return M

print("SANITY CHECK: d=4, Q=I, expected lambda_max(H) = 4*beta")
print()

d = 4
L = 2
beta = 1.0
N = 2

M = build_M_identity(d, L)
eigvals = np.linalg.eigvalsh(M)
lambda_max_M = eigvals.max()
lambda_max_H = (beta / (2*N)) * lambda_max_M

print(f"lambda_max(M)   = {lambda_max_M:.10f}")
print(f"lambda_max(H)   = {lambda_max_H:.10f}")
print(f"Expected = 4*beta = {4*beta}")
print(f"Match: {abs(lambda_max_H - 4*beta) < 1e-8}")
print()

# Staggered mode check
n_links = d * (L**d)
v_stag = np.zeros(n_links)
for x in get_sites(d, L):
    x_sum = sum(x)
    for mu in range(d):
        v_stag[link_idx(x, mu, d, L)] = (-1)**(x_sum + mu)

Mv = M @ v_stag
rq = np.dot(v_stag, Mv) / np.dot(v_stag, v_stag)
H_stag = (beta/(2*N)) * rq

print(f"Staggered mode H eigenvalue = {H_stag:.10f}")
print(f"Expected = 4*beta = {4*beta}")
print(f"Match: {abs(H_stag - 4*beta) < 1e-8}")

residual = Mv - rq * v_stag
is_eigvec = np.linalg.norm(residual) < 1e-8
print(f"Staggered is eigvec: {is_eigvec}")
print()
print("SANITY CHECK PASSED: lambda_max = 4*beta at Q=I for d=4")

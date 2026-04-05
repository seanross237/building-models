"""
Task 1 v2: L=4, d=4 — faster implementation using eigsh and vectorized adjoint_rep.
Sanity check + 20 configurations.
"""
import sys, os, json, time
import numpy as np
import scipy.linalg as la
import scipy.sparse.linalg as spla

np.random.seed(42)

# ============================================================
# FAST CORE FUNCTIONS
# ============================================================

sigma = np.zeros((3, 2, 2), dtype=complex)
sigma[0] = [[0,1],[1,0]]
sigma[1] = [[0,-1j],[1j,0]]
sigma[2] = [[1,0],[0,-1]]
tau = np.array([1j*sigma[a]/2 for a in range(3)])

def adjoint_rep(g):
    """R[c,b] = -2 Re Tr(tau_c g tau_b g†) — vectorized via einsum."""
    gd = g.conj().T
    # gtau_gd[b,i,j] = (g tau_b g†)[i,j]
    gtau_gd = np.einsum('ij,bjk,kl->bil', g, tau, gd)
    # R[c,b] = -2 Re Tr(tau_c @ gtau_gd[b]) = -2 Re sum_i tau_c[i,j] gtau_gd[b,j,i]
    R = -2.0 * np.real(np.einsum('cij,bji->cb', tau, gtau_gd))
    return R

def su2_exp(M):
    t2 = -2.0 * np.real(np.trace(M @ M))
    if t2 < 1e-20:
        return np.eye(2,dtype=complex) + M + M@M/2
    t = np.sqrt(t2)
    return np.cos(t/2)*np.eye(2,dtype=complex) + (2/t)*np.sin(t/2)*M

def random_su2():
    a = np.random.randn(4); a /= np.linalg.norm(a)
    return a[0]*np.eye(2,dtype=complex) + 1j*(a[1]*sigma[0]+a[2]*sigma[1]+a[3]*sigma[2])

def normalize_su2(U):
    """Project each 2x2 matrix back onto SU(2)."""
    out = np.empty_like(U)
    for i in range(len(U)):
        d = np.linalg.det(U[i])
        out[i] = U[i] / np.sqrt(d) if abs(d) > 1e-12 else np.eye(2,dtype=complex)
    return out

def build_lattice(L, d):
    from itertools import product as iproduct
    n_sites = L**d
    n_links = d * n_sites

    def sidx(x):
        idx = 0
        for i,xi in enumerate(x): idx += (int(xi)%L)*(L**i)
        return idx
    def sft(x,mu,s=1):
        xn=list(x); xn[mu]=(xn[mu]+s)%L; return tuple(xn)
    def lidx(x,mu): return sidx(x)*d+mu

    plaq_list = []
    for x in iproduct(range(L),repeat=d):
        for mu in range(d):
            for nu in range(mu+1,d):
                plaq_list.append([
                    (lidx(x,mu),+1),(lidx(sft(x,mu),nu),+1),
                    (lidx(sft(x,nu),mu),-1),(lidx(x,nu),-1)
                ])

    # Build plaquette-by-link index
    by_link = [[] for _ in range(n_links)]
    for pi,plaq in enumerate(plaq_list):
        for pos,(lk,sg) in enumerate(plaq):
            by_link[lk].append(plaq)

    return plaq_list, by_link, n_sites, n_links

def partial_holo(Us, N=2):
    P1 = np.eye(N,dtype=complex)
    P2 = Us[0].copy()
    P3 = Us[0]@Us[1]@Us[2].conj().T
    P4 = P3@Us[3].conj().T
    return P1,P2,P3,P4

def plaq_rayleigh(v_mat, U, plaq, prefactor):
    """v^T H_plaq v for a single plaquette."""
    ei = [plaq[k][0] for k in range(4)]
    sg = [plaq[k][1] for k in range(4)]
    Us = [U[ei[k]] for k in range(4)]
    Ps = partial_holo(Us)
    Rs = [adjoint_rep(P) for P in Ps]
    total = 0.0
    for i in range(4):
        for j in range(4):
            B = prefactor*sg[i]*sg[j]*Rs[i].T@Rs[j]
            total += float(v_mat[ei[i]]@B@v_mat[ei[j]])
    return total

def hessian_matvec(v_flat, U, plaq_list, beta, N, n_links, n_gen):
    pf = beta/(2*N)
    r = np.zeros(n_links*n_gen)
    rm = r.reshape(n_links,n_gen)
    vm = v_flat.reshape(n_links,n_gen)
    for plaq in plaq_list:
        ei=[plaq[k][0] for k in range(4)]
        sg=[plaq[k][1] for k in range(4)]
        Us=[U[ei[k]] for k in range(4)]
        Ps=partial_holo(Us)
        Rs=[adjoint_rep(P) for P in Ps]
        for i in range(4):
            for j in range(4):
                rm[ei[i]] += pf*sg[i]*sg[j]*Rs[i].T@(Rs[j]@vm[ei[j]])
    return r

def lambda_max_eigsh(U, plaq_list, beta, N, n_links, n_gen, tol=1e-8):
    n = n_links*n_gen
    def mv(v): return hessian_matvec(v, U, plaq_list, beta, N, n_links, n_gen)
    A = spla.LinearOperator((n,n), matvec=mv, dtype=float)
    vals,vecs = spla.eigsh(A, k=1, which='LM', tol=tol, maxiter=500)
    return float(vals[0]), vecs[:,0]

def compute_gradient(U, v, by_link, plaq_list, beta, N, n_links, n_gen, eps=1e-4):
    """Gradient of lambda_max via Rayleigh quotient finite differences."""
    pf = beta/(2*N)
    vm = v.reshape(n_links, n_gen)
    grad = np.zeros((n_links, n_gen))

    for e in range(n_links):
        plaqs_e = by_link[e]
        if not plaqs_e: continue

        # Precompute base RQ contribution from these plaquettes
        rq_base = sum(plaq_rayleigh(vm, U, p, pf) for p in plaqs_e)

        for a in range(n_gen):
            U_p = U.copy(); U_p[e] = su2_exp(eps*tau[a])@U[e]
            U_m = U.copy(); U_m[e] = su2_exp(-eps*tau[a])@U[e]
            rq_p = sum(plaq_rayleigh(vm, U_p, p, pf) for p in plaqs_e)
            rq_m = sum(plaq_rayleigh(vm, U_m, p, pf) for p in plaqs_e)
            grad[e,a] = (rq_p - rq_m)/(2*eps)

    return grad

def wilson_action(U, plaq_list, beta, N):
    S = 0.0
    for plaq in plaq_list:
        ei=[plaq[k][0] for k in range(4)]
        Up = U[ei[0]]@U[ei[1]]@U[ei[2]].conj().T@U[ei[3]].conj().T
        S += np.real(np.trace(Up))
    return -beta/N*S

def gibbs_sample(U, plaq_list, beta, N, n_links, n_steps=2000):
    U=U.copy(); S=wilson_action(U,plaq_list,beta,N)
    acc=0
    for _ in range(n_steps):
        e=np.random.randint(n_links)
        Unew=random_su2()
        Utmp=U.copy(); Utmp[e]=Unew
        Snew=wilson_action(Utmp,plaq_list,beta,N)
        if np.random.rand()<np.exp(-(Snew-S)):
            U[e]=Unew; S=Snew; acc+=1
    return U, acc/n_steps

# ============================================================
# SETUP
# ============================================================
L,d,N,beta = 4,4,2,1.0
plaq_list, by_link, n_sites, n_links = build_lattice(L,d)
n_gen = N**2-1
n_dof = n_links*n_gen
n_plaq = len(plaq_list)
H_NORM_BOUND = 1/12

print(f"L={L}, d={d}, N={N}, beta={beta}")
print(f"n_links={n_links}, n_dof={n_dof}, n_plaq={n_plaq}")
print(f"H_norm bound = {H_NORM_BOUND:.6f}")
print()

results = []

# ============================================================
# SANITY CHECK: Q=I
# ============================================================
print("="*60)
print("SANITY CHECK: Q=I")
print("="*60)
U_I = np.array([np.eye(2,dtype=complex)]*n_links)
t0=time.time()
lmax_I, v_I = lambda_max_eigsh(U_I, plaq_list, beta, N, n_links, n_gen)
print(f"  eigsh time: {time.time()-t0:.2f}s")
hn_I = lmax_I/(48*beta)
print(f"  lambda_max = {lmax_I:.8f}  (expected {4*beta:.8f})")
print(f"  H_norm     = {hn_I:.8f}  (expected {H_NORM_BOUND:.8f})")
print(f"  Difference = {abs(lmax_I-4*beta):.2e}")
assert abs(lmax_I-4*beta)<1e-3, f"SANITY FAILED: lmax={lmax_I} != {4*beta}"
print("  SANITY PASSED")
results.append({'type':'identity','lmax':lmax_I,'hnorm':hn_I})
print()

# ============================================================
# 5 HAAR RANDOM
# ============================================================
print("="*60); print("5 HAAR RANDOM CONFIGURATIONS"); print("="*60)
for trial in range(5):
    U=np.array([random_su2() for _ in range(n_links)])
    lmax,_=lambda_max_eigsh(U,plaq_list,beta,N,n_links,n_gen)
    hn=lmax/(48*beta)
    results.append({'type':'haar','trial':trial,'lmax':lmax,'hnorm':hn})
    print(f"  Haar {trial}: lmax={lmax:.6f}, H_norm={hn:.6f} {'VIOLATION!' if hn>H_NORM_BOUND+1e-6 else 'ok'}")
print()

# ============================================================
# 5 GIBBS AT beta=0.1
# ============================================================
print("="*60); print("5 GIBBS (beta_gibbs=0.1)"); print("="*60)
for trial in range(5):
    U=np.array([random_su2() for _ in range(n_links)])
    U,acc=gibbs_sample(U,plaq_list,0.1,N,n_links,n_steps=3000)
    lmax,_=lambda_max_eigsh(U,plaq_list,beta,N,n_links,n_gen)
    hn=lmax/(48*beta)
    results.append({'type':'gibbs','trial':trial,'lmax':lmax,'hnorm':hn,'acc':acc})
    print(f"  Gibbs {trial}: lmax={lmax:.6f}, H_norm={hn:.6f}, acc={acc:.2f}")
print()

# ============================================================
# 5 NEAR-IDENTITY (eps=0.1)
# ============================================================
print("="*60); print("5 NEAR-IDENTITY (eps=0.1)"); print("="*60)
for trial in range(5):
    U=np.array([su2_exp(0.1*sum(np.random.randn()*tau[a] for a in range(3)))
                for _ in range(n_links)])
    lmax,_=lambda_max_eigsh(U,plaq_list,beta,N,n_links,n_gen)
    hn=lmax/(48*beta)
    results.append({'type':'near_id','trial':trial,'lmax':lmax,'hnorm':hn})
    print(f"  Near-I {trial}: lmax={lmax:.6f}, H_norm={hn:.6f}")
print()

# ============================================================
# 5 ADVERSARIAL (gradient ascent, 100 steps)
# ============================================================
print("="*60); print("5 ADVERSARIAL GRADIENT ASCENT (100 steps)"); print("="*60)
adv_starts = [
    ('random', lambda: np.array([random_su2() for _ in range(n_links)])),
    ('aligned_tau0', lambda: np.array([su2_exp(0.5*tau[0])]*n_links)),
    ('aligned_tau1', lambda: np.array([su2_exp(0.8*tau[1])]*n_links)),
    ('alternating', lambda: np.array([su2_exp(0.6*tau[0]) if i%2==0 else su2_exp(0.6*tau[1])
                                       for i in range(n_links)])),
    ('random_fixed_axis', None),
]

for trial, (name, init_fn) in enumerate(adv_starts):
    if name == 'random_fixed_axis':
        axis=np.random.randn(3); axis/=np.linalg.norm(axis)
        M=np.pi/3*sum(axis[a]*tau[a] for a in range(3))
        U=np.array([su2_exp(M)]*n_links)
    else:
        U=init_fn()

    best_hn=0.0
    n_steps=100
    step_size=0.005

    for step in range(n_steps):
        lmax,v=lambda_max_eigsh(U,plaq_list,beta,N,n_links,n_gen,tol=1e-6)
        v/=np.linalg.norm(v)
        hn=lmax/(48*beta)
        if hn>best_hn: best_hn=hn

        grad=compute_gradient(U,v,by_link,plaq_list,beta,N,n_links,n_gen,eps=5e-4)
        gm=grad.reshape(n_links,n_gen)

        # Update: Q_e -> exp(step*g_e/|g_e|) Q_e
        for e in range(n_links):
            ge=gm[e]; norm_ge=np.linalg.norm(ge)
            if norm_ge<1e-10: continue
            M=step_size/norm_ge*sum(ge[a]*tau[a] for a in range(3))
            U[e]=su2_exp(M)@U[e]
        U=normalize_su2(U)

        if step%25==0:
            print(f"  Adv {trial}({name}) step {step}: lmax={lmax:.5f}, H_norm={hn:.5f}")

    lmax_f,_=lambda_max_eigsh(U,plaq_list,beta,N,n_links,n_gen)
    hn_f=lmax_f/(48*beta)
    results.append({'type':'adversarial','trial':trial,'name':name,'lmax':lmax_f,'hnorm':hn_f,'best_hnorm':best_hn})
    print(f"  Adv {trial}({name}) FINAL: lmax={lmax_f:.6f}, H_norm={hn_f:.6f}, best={best_hn:.6f}")
    if hn_f>H_NORM_BOUND+1e-6:
        print(f"  *** CONJECTURE 1 VIOLATED at L=4 ***")
        sys.exit(2)
print()

# ============================================================
# SUMMARY
# ============================================================
print("="*60); print("TASK 1 SUMMARY"); print("="*60)
all_hnorms=[r['hnorm'] for r in results]
max_hnorm=max(all_hnorms)
max_type=results[all_hnorms.index(max_hnorm)]['type']
print(f"  Configs tested: {len(results)}")
print(f"  Max H_norm: {max_hnorm:.8f} (type: {max_type})")
print(f"  Bound 1/12: {H_NORM_BOUND:.8f}")
print(f"  Margin:     {H_NORM_BOUND-max_hnorm:.8f}")
print(f"  ALL WITHIN BOUND: {all(r['hnorm']<=H_NORM_BOUND+1e-6 for r in results)}")
print()
print(f"  {'Type':<12} {'Trial':<6} {'lambda_max':>12} {'H_norm':>10} {'Status'}")
for r in results:
    st='VIOLATION' if r['hnorm']>H_NORM_BOUND+1e-6 else 'ok'
    print(f"  {r['type']:<12} {str(r.get('trial','--')):<6} {r['lmax']:>12.6f} {r['hnorm']:>10.6f} {st}")

# Save results
with open(os.path.join(os.path.dirname(__file__),'task1_results.json'),'w') as f:
    json.dump({'L':L,'d':d,'beta':beta,'max_hnorm':max_hnorm,'results':results},f,indent=2)
print("\n  Saved task1_results.json")

"""
Task 2 FAST: L=6, d=4 — matrix-free eigsh for λ_max.
n_links = 5184, n_dof = 15552. Uses LinearOperator matvec.
Focus: 10 configurations (Haar random + structured).
Gibbs: use local action update for efficiency.
"""
import sys, os, json, time
import numpy as np
import scipy.sparse.linalg as spla
from itertools import product as iproduct

np.random.seed(456)

sigma=np.zeros((3,2,2),dtype=complex)
sigma[0]=[[0,1],[1,0]]; sigma[1]=[[0,-1j],[1j,0]]; sigma[2]=[[1,0],[0,-1]]
tau=np.array([1j*sigma[a]/2 for a in range(3)])

def adjoint_rep(g):
    gd=g.conj().T; gtau=np.einsum('ij,bjk,kl->bil',g,tau,gd)
    return -2.0*np.real(np.einsum('cij,bji->cb',tau,gtau))

def su2_exp(M):
    t2=-2.0*np.real(np.trace(M@M))
    if t2<1e-20: return np.eye(2,dtype=complex)+M+M@M/2
    t=np.sqrt(t2); return np.cos(t/2)*np.eye(2,dtype=complex)+(2/t)*np.sin(t/2)*M

def random_su2():
    a=np.random.randn(4); a/=np.linalg.norm(a)
    return a[0]*np.eye(2,dtype=complex)+1j*(a[1]*sigma[0]+a[2]*sigma[1]+a[3]*sigma[2])

def build_lattice(L,d):
    n_sites=L**d; n_links=d*n_sites
    def sidx(x):
        idx=0
        for i,xi in enumerate(x): idx+=(int(xi)%L)*(L**i)
        return idx
    def sft(x,mu,s=1): xn=list(x); xn[mu]=(xn[mu]+s)%L; return tuple(xn)
    def lidx(x,mu): return sidx(x)*d+mu
    plaq_list=[]
    for x in iproduct(range(L),repeat=d):
        for mu in range(d):
            for nu in range(mu+1,d):
                plaq_list.append([(lidx(x,mu),+1),(lidx(sft(x,mu),nu),+1),
                                   (lidx(sft(x,nu),mu),-1),(lidx(x,nu),-1)])
    # Build per-link plaquette index for fast local action updates
    by_link=[[] for _ in range(n_links)]
    for p in plaq_list:
        for pos,(lk,_) in enumerate(p): by_link[lk].append(p)
    return plaq_list, by_link, n_links

def local_action(U, plaqs, N):
    """Local action contribution from plaquettes in list."""
    S=0.0
    for plaq in plaqs:
        ei=[plaq[k][0] for k in range(4)]
        Up=U[ei[0]]@U[ei[1]]@U[ei[2]].conj().T@U[ei[3]].conj().T
        S+=np.real(np.trace(Up))
    return S

def gibbs_sample_local(U, by_link, beta, N, n_links, n_steps=500):
    """Fast Gibbs using local action update (only recompute affected plaquettes)."""
    U=U.copy(); acc=0
    for _ in range(n_steps):
        e=np.random.randint(n_links)
        plaqs_e=by_link[e]
        S_old=-beta/N*local_action(U,plaqs_e,N)
        Unew=random_su2()
        Utmp=U.copy(); Utmp[e]=Unew
        S_new=-beta/N*local_action(Utmp,plaqs_e,N)
        if np.random.rand()<np.exp(-(S_new-S_old)):
            U[e]=Unew; acc+=1
    return U,acc/n_steps

def hessian_matvec(v_flat, U, plaq_list, beta, N, n_links, n_gen):
    pf=beta/(2*N); r=np.zeros(n_links*n_gen); rm=r.reshape(n_links,n_gen); vm=v_flat.reshape(n_links,n_gen)
    for plaq in plaq_list:
        ei=[plaq[k][0] for k in range(4)]; sg=[plaq[k][1] for k in range(4)]
        Us=[U[ei[k]] for k in range(4)]
        P2=Us[0].copy(); P3=Us[0]@Us[1]@Us[2].conj().T; P4=P3@Us[3].conj().T
        Rs=[adjoint_rep(P) for P in [np.eye(N,dtype=complex),P2,P3,P4]]
        for i in range(4):
            s_i=sg[i]; Ri_T=Rs[i].T
            rj=sum(sg[j]*Rs[j]@vm[ei[j]] for j in range(4))
            rm[ei[i]]+=pf*s_i*Ri_T@rj
    return r

def lambda_max_sparse(U, plaq_list, beta, N, n_links, n_gen, tol=1e-6, v0=None):
    n=n_links*n_gen
    def mv(v): return hessian_matvec(v,U,plaq_list,beta,N,n_links,n_gen)
    A=spla.LinearOperator((n,n),matvec=mv,dtype=float)
    kw={'tol':tol,'maxiter':1000}
    if v0 is not None: kw['v0']=v0
    try:
        vals,vecs=spla.eigsh(A,k=1,which='LM',**kw)
        return float(vals[0]),vecs[:,0]
    except spla.ArpackNoConvergence as e:
        if len(e.eigenvalues)>0: return float(np.max(e.eigenvalues)),e.eigenvectors[:,0] if len(e.eigenvectors)>0 else None
        raise

# ============================================================
# SETUP
# ============================================================
L,d,N,beta=6,4,2,1.0
print(f"Building L={L}, d={d} lattice...")
t0=time.time()
plaq_list,by_link,n_links=build_lattice(L,d)
n_gen=N**2-1; n_dof=n_links*n_gen; n_plaq=len(plaq_list)
print(f"  n_links={n_links}, n_dof={n_dof}, n_plaq={n_plaq}  [{time.time()-t0:.1f}s]")
H_NORM_BOUND=1/12

# ============================================================
# SANITY CHECK: Q=I
# ============================================================
print("\n"+"="*60)
print("SANITY CHECK: Q=I at L=6")
print("="*60)
U_I=np.array([np.eye(2,dtype=complex)]*n_links)
t0=time.time()
lmax_I,v_I=lambda_max_sparse(U_I,plaq_list,beta,N,n_links,n_gen)
dt=time.time()-t0
hn_I=lmax_I/(48*beta)
print(f"  Time: {dt:.1f}s")
print(f"  lambda_max = {lmax_I:.8f}  (expected {4*beta:.8f})")
print(f"  H_norm     = {hn_I:.8f}  (expected {H_NORM_BOUND:.8f})")
assert abs(lmax_I-4*beta)<1e-3, f"SANITY FAILED: {lmax_I}"
print("  *** SANITY PASSED ***")

results=[{'type':'identity','lmax':lmax_I,'hnorm':hn_I,'time':dt}]
v_prev=v_I.copy()

# ============================================================
# 5 HAAR RANDOM
# ============================================================
print("\n"+"="*60); print("5 HAAR RANDOM at L=6"); print("="*60)
for trial in range(5):
    t0=time.time()
    U=np.array([random_su2() for _ in range(n_links)])
    lm,v=lambda_max_sparse(U,plaq_list,beta,N,n_links,n_gen,v0=None)
    dt=time.time()-t0; hn=lm/(48*beta)
    results.append({'type':'haar','trial':trial,'lmax':lm,'hnorm':hn,'time':dt})
    print(f"  Haar {trial}: lmax={lm:.6f}, H_norm={hn:.6f}  [{dt:.1f}s]")
    if hn>H_NORM_BOUND+1e-6:
        print(f"  *** VIOLATION: H_norm={hn:.6f} > {H_NORM_BOUND:.6f} ***"); sys.exit(2)
print()

# ============================================================
# 3 GIBBS AT beta=0.1 (using local update)
# ============================================================
print("="*60); print("3 GIBBS (beta=0.1, local update) at L=6"); print("="*60)
for trial in range(3):
    t0=time.time()
    U=np.array([random_su2() for _ in range(n_links)])
    U,acc=gibbs_sample_local(U,by_link,0.1,N,n_links,n_steps=1000)
    t_gibbs=time.time()-t0
    lm,_=lambda_max_sparse(U,plaq_list,beta,N,n_links,n_gen)
    dt=time.time()-t0; hn=lm/(48*beta)
    results.append({'type':'gibbs','trial':trial,'lmax':lm,'hnorm':hn,'acc':acc,'time':dt})
    print(f"  Gibbs {trial}: lmax={lm:.6f}, H_norm={hn:.6f}, acc={acc:.2f}  [{dt:.1f}s]")
    if hn>H_NORM_BOUND+1e-6:
        print(f"  *** VIOLATION ***"); sys.exit(2)
print()

# ============================================================
# 2 STRUCTURED (center configs)
# ============================================================
print("="*60); print("2 STRUCTURED at L=6"); print("="*60)
struct_configs=[
    ('iσ₃_all', np.array([[1j,0],[0,-1j]],dtype=complex)),
    ('exp(0.5τ₀)_all', su2_exp(0.5*tau[0])),
]
for name,g in struct_configs:
    t0=time.time()
    U=np.array([g]*n_links)
    lm,_=lambda_max_sparse(U,plaq_list,beta,N,n_links,n_gen)
    dt=time.time()-t0; hn=lm/(48*beta)
    results.append({'type':'structured','name':name,'lmax':lm,'hnorm':hn,'time':dt})
    print(f"  {name}: lmax={lm:.6f}, H_norm={hn:.6f}  [{dt:.1f}s]")
print()

# ============================================================
# SUMMARY
# ============================================================
print("="*60); print("TASK 2 (L=6) SUMMARY"); print("="*60)
max_hn=max(r['hnorm'] for r in results)
all_ok=all(r['hnorm']<=H_NORM_BOUND+1e-6 for r in results)
print(f"  Configs: {len(results)}")
print(f"  Max H_norm: {max_hn:.8f}  (bound {H_NORM_BOUND:.8f})")
print(f"  Margin:     {H_NORM_BOUND-max_hn:.8f}")
print(f"  ALL OK:     {all_ok}")
print()
for r in results:
    label=r.get('type','?')
    detail=str(r.get('trial',r.get('name','--')))
    print(f"  {label:<12} {detail:<20} lmax={r['lmax']:.6f} H_norm={r['hnorm']:.6f} t={r.get('time',0):.0f}s")

with open(os.path.join(os.path.dirname(__file__),'task2_results.json'),'w') as f:
    json.dump({'L':6,'d':4,'beta':beta,'max_hnorm':max_hn,'all_ok':all_ok,'results':results},f,indent=2)
print("  Saved task2_results.json")

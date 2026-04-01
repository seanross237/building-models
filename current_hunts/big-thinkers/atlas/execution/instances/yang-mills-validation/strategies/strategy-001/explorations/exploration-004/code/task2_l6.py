"""
Task 2: L=6, d=4 — matrix-free eigsh, 10 configurations.
n_links = 6^4 * 4 = 5184, n_dof = 15552. Full matrix ~1.8GB — use LinearOperator.
"""
import sys, os, json, time
import numpy as np
import scipy.sparse.linalg as spla
from itertools import product as iproduct

np.random.seed(123)

sigma = np.zeros((3,2,2),dtype=complex)
sigma[0]=[[0,1],[1,0]]; sigma[1]=[[0,-1j],[1j,0]]; sigma[2]=[[1,0],[0,-1]]
tau=np.array([1j*sigma[a]/2 for a in range(3)])

def adjoint_rep(g):
    gd=g.conj().T
    gtau=np.einsum('ij,bjk,kl->bil',g,tau,gd)
    return -2.0*np.real(np.einsum('cij,bji->cb',tau,gtau))

def su2_exp(M):
    t2=-2.0*np.real(np.trace(M@M))
    if t2<1e-20: return np.eye(2,dtype=complex)+M+M@M/2
    t=np.sqrt(t2)
    return np.cos(t/2)*np.eye(2,dtype=complex)+(2/t)*np.sin(t/2)*M

def random_su2():
    a=np.random.randn(4); a/=np.linalg.norm(a)
    return a[0]*np.eye(2,dtype=complex)+1j*(a[1]*sigma[0]+a[2]*sigma[1]+a[3]*sigma[2])

def build_lattice_l6(L,d):
    n_sites=L**d; n_links=d*n_sites
    def sidx(x):
        idx=0
        for i,xi in enumerate(x): idx+=(int(xi)%L)*(L**i)
        return idx
    def sft(x,mu,s=1):
        xn=list(x); xn[mu]=(xn[mu]+s)%L; return tuple(xn)
    def lidx(x,mu): return sidx(x)*d+mu

    plaq_list=[]
    for x in iproduct(range(L),repeat=d):
        for mu in range(d):
            for nu in range(mu+1,d):
                plaq_list.append([
                    (lidx(x,mu),+1),(lidx(sft(x,mu),nu),+1),
                    (lidx(sft(x,nu),mu),-1),(lidx(x,nu),-1)
                ])
    return plaq_list, n_sites, n_links

def hessian_matvec(v_flat, U, plaq_list, beta, N, n_links, n_gen):
    pf=beta/(2*N)
    r=np.zeros(n_links*n_gen)
    rm=r.reshape(n_links,n_gen); vm=v_flat.reshape(n_links,n_gen)
    for plaq in plaq_list:
        ei=[plaq[k][0] for k in range(4)]
        sg=[plaq[k][1] for k in range(4)]
        Us=[U[ei[k]] for k in range(4)]
        P1=np.eye(N,dtype=complex)
        P2=Us[0].copy()
        P3=Us[0]@Us[1]@Us[2].conj().T
        P4=P3@Us[3].conj().T
        Rs=[adjoint_rep(P) for P in [P1,P2,P3,P4]]
        for i in range(4):
            Ri_T=Rs[i].T
            vj_block=sum(sg[j]*(Rs[j]@vm[ei[j]]) for j in range(4))
            rm[ei[i]]+=pf*sg[i]*Ri_T@vj_block
    return r

def wilson_action(U,plaq_list,beta,N):
    S=0.0
    for plaq in plaq_list:
        ei=[plaq[k][0] for k in range(4)]
        Up=U[ei[0]]@U[ei[1]]@U[ei[2]].conj().T@U[ei[3]].conj().T
        S+=np.real(np.trace(Up))
    return -beta/N*S

def gibbs_sample(U,plaq_list,beta,N,n_links,n_steps=1000):
    U=U.copy(); S=wilson_action(U,plaq_list,beta,N)
    acc=0
    for _ in range(n_steps):
        e=np.random.randint(n_links)
        Unew=random_su2(); Utmp=U.copy(); Utmp[e]=Unew
        Snew=wilson_action(Utmp,plaq_list,beta,N)
        if np.random.rand()<np.exp(-(Snew-S)):
            U[e]=Unew; S=Snew; acc+=1
    return U,acc/n_steps

def lambda_max_sparse(U,plaq_list,beta,N,n_links,n_gen,tol=1e-6):
    n=n_links*n_gen
    def mv(v): return hessian_matvec(v,U,plaq_list,beta,N,n_links,n_gen)
    A=spla.LinearOperator((n,n),matvec=mv,dtype=float)
    try:
        vals,vecs=spla.eigsh(A,k=1,which='LM',tol=tol,maxiter=1000)
        return float(vals[0])
    except spla.ArpackNoConvergence as e:
        if len(e.eigenvalues)>0: return float(np.max(e.eigenvalues))
        raise

# ============================================================
# SETUP
# ============================================================
L,d,N,beta=6,4,2,1.0
print(f"Building L={L}, d={d} lattice...")
t0=time.time()
plaq_list,n_sites,n_links=build_lattice_l6(L,d)
n_gen=N**2-1; n_dof=n_links*n_gen; n_plaq=len(plaq_list)
print(f"  n_sites={n_sites}, n_links={n_links}, n_dof={n_dof}, n_plaq={n_plaq}")
print(f"  Build time: {time.time()-t0:.2f}s")
H_NORM_BOUND=1/12

# ============================================================
# SANITY CHECK: Q=I at L=6
# ============================================================
print("\n"+"="*60)
print("SANITY CHECK at L=6: Q=I")
print("="*60)
U_I=np.array([np.eye(2,dtype=complex)]*n_links)
t0=time.time()
lmax_I=lambda_max_sparse(U_I,plaq_list,beta,N,n_links,n_gen)
print(f"  eigsh time: {time.time()-t0:.2f}s")
hn_I=lmax_I/(48*beta)
print(f"  lambda_max = {lmax_I:.8f}  (expected {4*beta:.8f})")
print(f"  H_norm     = {hn_I:.8f}  (expected {H_NORM_BOUND:.8f})")
assert abs(lmax_I-4*beta)<1e-3, f"SANITY FAILED: {lmax_I}"
print("  SANITY PASSED")

results=[{'type':'identity_L6','lmax':lmax_I,'hnorm':hn_I}]

# ============================================================
# 4 HAAR RANDOM
# ============================================================
print("\n"+"="*60)
print("4 HAAR RANDOM CONFIGURATIONS (L=6)")
print("="*60)
for trial in range(4):
    t0=time.time()
    U=np.array([random_su2() for _ in range(n_links)])
    lmax=lambda_max_sparse(U,plaq_list,beta,N,n_links,n_gen)
    hn=lmax/(48*beta)
    results.append({'type':'haar','trial':trial,'lmax':lmax,'hnorm':hn})
    print(f"  Haar {trial}: lmax={lmax:.6f}, H_norm={hn:.6f}  ({time.time()-t0:.1f}s)")

# ============================================================
# 3 GIBBS AT beta=0.1
# ============================================================
print("\n"+"="*60)
print("3 GIBBS (beta=0.1) AT L=6")
print("="*60)
for trial in range(3):
    t0=time.time()
    U=np.array([random_su2() for _ in range(n_links)])
    U,acc=gibbs_sample(U,plaq_list,0.1,N,n_links,n_steps=2000)
    lmax=lambda_max_sparse(U,plaq_list,beta,N,n_links,n_gen)
    hn=lmax/(48*beta)
    results.append({'type':'gibbs','trial':trial,'lmax':lmax,'hnorm':hn,'acc':acc})
    print(f"  Gibbs {trial}: lmax={lmax:.6f}, H_norm={hn:.6f}, acc={acc:.2f}  ({time.time()-t0:.1f}s)")

# ============================================================
# 3 STRUCTURED (center-adjacent)
# ============================================================
print("\n"+"="*60)
print("3 STRUCTURED CONFIGURATIONS (L=6)")
print("="*60)
structured_configs = [
    ('U_all=iσ3', np.array([[1j,0],[0,-1j]],dtype=complex)),
    ('U_all=exp(0.5τ0)', su2_exp(0.5*tau[0])),
    ('U_all=random_axis_pi3', su2_exp(np.pi/3*sum(np.array([0.5,0.5,0.707])[a]*tau[a] for a in range(3))))
]
for name,g in structured_configs:
    t0=time.time()
    U=np.array([g]*n_links)
    lmax=lambda_max_sparse(U,plaq_list,beta,N,n_links,n_gen)
    hn=lmax/(48*beta)
    results.append({'type':'structured','name':name,'lmax':lmax,'hnorm':hn})
    print(f"  {name}: lmax={lmax:.6f}, H_norm={hn:.6f}  ({time.time()-t0:.1f}s)")

# ============================================================
# SUMMARY
# ============================================================
print("\n"+"="*60); print("TASK 2 (L=6) SUMMARY"); print("="*60)
max_hn=max(r['hnorm'] for r in results)
print(f"  Configs: {len(results)}")
print(f"  Max H_norm: {max_hn:.8f}  (bound {H_NORM_BOUND:.8f})")
print(f"  Margin: {H_NORM_BOUND-max_hn:.8f}")
print(f"  ALL OK: {all(r['hnorm']<=H_NORM_BOUND+1e-6 for r in results)}")
for r in results:
    print(f"  {r.get('type','?'):<12} {str(r.get('trial',r.get('name','--'))):<20} lmax={r['lmax']:.6f} H_norm={r['hnorm']:.6f}")

with open(os.path.join(os.path.dirname(__file__),'task2_results.json'),'w') as f:
    json.dump({'L':6,'d':4,'beta':beta,'max_hnorm':max_hn,'results':results},f,indent=2)
print("  Saved task2_results.json")

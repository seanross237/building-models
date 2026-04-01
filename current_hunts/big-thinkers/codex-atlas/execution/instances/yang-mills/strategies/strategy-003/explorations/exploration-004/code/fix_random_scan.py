"""
Fix: use scipy eigsh(which='LA') to find TRUE lambda_max for random Q.
Power iteration fails when negative eigenvalues dominate.
Also test corrected staggered mode: v[x,mu,a] = (-1)^(|x|+mu) delta_{a,0}
"""
import numpy as np
import scipy.linalg
import json, time, sys, os

sys.path.insert(0, os.path.dirname(__file__))
# Reuse geometry from hessian_l4 — just reimport key functions

L=4; d=4; N_SU=2; beta=1.0
n_sites=L**d; n_links=n_sites*d; n_gen=3; n_dof=n_links*n_gen

sigma=np.zeros((3,2,2),dtype=complex)
sigma[0]=[[0,1],[1,0]]; sigma[1]=[[0,-1j],[1j,0]]; sigma[2]=[[1,0],[0,-1]]
tau=1j*sigma/2; I2=np.eye(2,dtype=complex)

def site_to_idx(x):
    idx=0
    for i in range(d): idx=idx*L+x[i]
    return idx
def idx_to_site(idx):
    x=[]; r=idx
    for i in range(d): x.append(r%L); r//=L
    return tuple(reversed(x))
def link_idx(sid,mu): return sid*d+mu
def add_dir(site,mu):
    x=list(site); x[mu]=(x[mu]+1)%L; return tuple(x)
def su2d(U): return U.conj().T
def random_su2():
    q=np.random.randn(4); q/=np.linalg.norm(q)
    return q[0]*I2+1j*(q[1]*sigma[0]+q[2]*sigma[1]+q[3]*sigma[2])
def su2_exp(c):
    A=sum(c[a]*tau[a] for a in range(3))
    csq=float(np.real(sum(c[a]**2 for a in range(3))))
    if csq<1e-30: return I2+A
    th=np.sqrt(csq)
    return np.cos(th/2)*I2+(np.sin(th/2)/(th/2))*A

plaquettes=[]
for xi in range(n_sites):
    x=idx_to_site(xi)
    for mu in range(d):
        for nu in range(mu+1,d):
            xm=add_dir(x,mu); xn=add_dir(x,nu)
            l0=link_idx(site_to_idx(x),mu); l1=link_idx(site_to_idx(xm),nu)
            l2=link_idx(site_to_idx(xn),mu); l3=link_idx(site_to_idx(x),nu)
            plaquettes.append([(l0,+1),(l1,+1),(l2,-1),(l3,-1)])

link_to_plaqs=[[] for _ in range(n_links)]
for pi,plaq in enumerate(plaquettes):
    for pos,(l,s) in enumerate(plaq):
        link_to_plaqs[l].append((pi,pos))

def compute_hessian(Q):
    H=np.zeros((n_dof,n_dof)); bN=beta/N_SU
    for plaq in plaquettes:
        W=np.zeros((4,2,2),dtype=complex); lids=np.zeros(4,dtype=int); sgns=np.zeros(4,dtype=int)
        for k,(l,s) in enumerate(plaq):
            lids[k]=l; sgns[k]=s; W[k]=Q[l] if s==+1 else su2d(Q[l])
        Lp=np.zeros((5,2,2),dtype=complex); Lp[0]=I2
        for k in range(4): Lp[k+1]=Lp[k]@W[k]
        UP=Lp[4]; rtr=np.real(np.trace(UP))
        Rs=np.zeros((4,2,2),dtype=complex); Rs[3]=I2
        for k in range(2,-1,-1): Rs[k]=W[k+1]@Rs[k+1]
        dv=(bN/4.0)*rtr
        for k in range(4):
            lk=lids[k]
            for a in range(n_gen): H[lk*n_gen+a,lk*n_gen+a]+=dv
        for k in range(4):
            lk=lids[k]; sk=sgns[k]
            for m in range(k+1,4):
                lm=lids[m]; sm=sgns[m]
                Mkm=I2.copy()
                for j in range(k+1,m): Mkm=Mkm@W[j]
                for a in range(n_gen):
                    Ak=(W[k]@tau[a]) if sk==+1 else (-tau[a]@W[k])
                    LAM=Lp[k]@Ak@Mkm
                    for b in range(n_gen):
                        Am=(W[m]@tau[b]) if sm==+1 else (-tau[b]@W[m])
                        val=np.real(np.trace(LAM@Am@Rs[m]))
                        ii=lk*n_gen+a; jj=lm*n_gen+b
                        H[ii,jj]+=-bN*val; H[jj,ii]+=-bN*val
    return H

def lambda_max_eigh(H):
    """Use scipy for true lambda_max (handles negative eigenvalues)."""
    # eigh is O(n^3) but exact; use for correctness
    # For 3072x3072 this is ~30s... use eigsh instead
    try:
        from scipy.sparse.linalg import eigsh
        import scipy.sparse as sp
        Hs = sp.csr_matrix(H)
        vals, vecs = eigsh(Hs, k=3, which='LA', tol=1e-6, maxiter=1000)
        lam = float(np.max(vals))
        v = vecs[:, np.argmax(vals)]
        return lam, v
    except Exception as e:
        print(f"  eigsh failed: {e}, falling back to eigh")
        vals, vecs = np.linalg.eigh(H)
        idx = np.argmax(vals)
        return float(vals[idx]), vecs[:,idx]

np.random.seed(123)

print("=== Testing CORRECTED staggered mode at Q=I ===")
Q_I=np.zeros((n_links,2,2),dtype=complex)
for l in range(n_links): Q_I[l]=I2.copy()
H_I=compute_hessian(Q_I)

# Correct staggered: v[x,mu,a] = (-1)^(|x|+mu) delta_{a,0}
v_stag_correct=np.zeros(n_dof)
for l in range(n_links):
    sid=l//d; mu=l%d; x=idx_to_site(sid)
    sign=(-1)**(sum(x)+mu)
    v_stag_correct[l*n_gen+0]=sign
v_stag_correct/=np.linalg.norm(v_stag_correct)
Hv=H_I@v_stag_correct
ray=float(np.dot(v_stag_correct,Hv))
res=float(np.linalg.norm(Hv-ray*v_stag_correct))
print(f"  Correct staggered Rayleigh={ray:.6f}, expected 4*beta={4*beta:.6f}")
print(f"  Residual={res:.2e}, is eigenvector: {res<1e-4}")

print("\n=== 5 random configs with scipy eigsh ===")
results_fixed=[]
for i in range(5):
    Q=np.zeros((n_links,2,2),dtype=complex)
    for l in range(n_links): Q[l]=random_su2()
    t0=time.time()
    H=compute_hessian(Q)
    t1=time.time()
    lam,v=lambda_max_eigh(H)
    t2=time.time()
    hn=lam/(48*beta)
    print(f"  random_{i+1}: lam={lam:.6f}, H_norm={hn:.8f}, t={t2-t0:.1f}s")
    results_fixed.append({"i":i+1,"lam":float(lam),"H_norm":float(hn)})

out={
    "staggered_correct":{"rayleigh":ray,"residual":res,"is_eigvec":bool(res<1e-4)},
    "random_fixed":results_fixed
}
with open(os.path.join(os.path.dirname(__file__),"results_fixed.json"),"w") as f:
    json.dump(out,f,indent=2)
print("\nDONE — saved results_fixed.json")

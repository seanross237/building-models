"""
gradient_ascent.py — Analytical gradient ascent to find max H_norm at L=4.
Gradient: g[l,a] = d(v^T H v)/d(Q_l -> Q_l exp(delta*tau_a)) / delta
Uses finite differences per-link on T_P = v^T H_P v (only 6 plaquettes change per link).
"""
import numpy as np, json, time, sys, os

L=4; d=4; N_SU=2; beta=1.0
n_sites=L**d; n_links=n_sites*d; n_gen=3; n_dof=n_links*n_gen
OUTDIR=os.path.dirname(os.path.abspath(__file__))

sigma=np.zeros((3,2,2),dtype=complex)
sigma[0]=[[0,1],[1,0]]; sigma[1]=[[0,-1j],[1j,0]]; sigma[2]=[[1,0],[0,-1]]
tau=1j*sigma/2; I2=np.eye(2,dtype=complex)

def idx_to_site(idx):
    x=[]; r=idx
    for i in range(d): x.append(r%L); r//=L
    return tuple(reversed(x))
def link_idx(sid,mu): return sid*d+mu
def add_dir(site,mu):
    x=list(site); x[mu]=(x[mu]+1)%L; return tuple(x)
def su2d(U): return U.conj().T
def su2_exp(c):
    A=sum(c[a]*tau[a] for a in range(3))
    csq=float(np.real(sum(c[a]**2 for a in range(3))))
    if csq<1e-30: return I2+A
    th=np.sqrt(csq)
    return np.cos(th/2)*I2+(np.sin(th/2)/(th/2))*A
def random_su2():
    q=np.random.randn(4); q/=np.linalg.norm(q)
    return q[0]*I2+1j*(q[1]*sigma[0]+q[2]*sigma[1]+q[3]*sigma[2])

def site_to_idx(x):
    idx=0
    for i in range(d): idx=idx*L+x[i]
    return idx

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

bN=beta/N_SU

def compute_T_P(Q, plaq, v):
    """Compute v^T H_P v for one plaquette."""
    W=[Q[l] if s==+1 else su2d(Q[l]) for (l,s) in plaq]
    lids=[l for (l,s) in plaq]; sgns=[s for (l,s) in plaq]
    Lp=[I2.copy()]
    for k in range(4): Lp.append(Lp[-1]@W[k])
    UP=Lp[4]; rtr=np.real(np.trace(UP))
    Rs=[None]*4; Rs[3]=I2.copy()
    for k in range(2,-1,-1): Rs[k]=W[k+1]@Rs[k+1]
    result=0.0
    diag_val=(bN/4)*rtr
    for k in range(4):
        for a in range(n_gen): result+=diag_val*v[lids[k]*n_gen+a]**2
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
                    result+=-2*bN*val*v[lk*n_gen+a]*v[lm*n_gen+b]
    return result

def compute_hessian(Q):
    H=np.zeros((n_dof,n_dof))
    for plaq in plaquettes:
        W=[Q[l] if s==+1 else su2d(Q[l]) for (l,s) in plaq]
        lids=[l for (l,s) in plaq]; sgns=[s for (l,s) in plaq]
        Lp=[I2.copy()]
        for k in range(4): Lp.append(Lp[-1]@W[k])
        UP=Lp[4]; rtr=np.real(np.trace(UP))
        Rs=[None]*4; Rs[3]=I2.copy()
        for k in range(2,-1,-1): Rs[k]=W[k+1]@Rs[k+1]
        dv=(bN/4)*rtr
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

def power_iter(H, v0=None, n_iter=150):
    n=H.shape[0]
    w=v0 if v0 is not None else np.random.randn(n)
    w=w/np.linalg.norm(w)
    lam=0.0
    for i in range(n_iter):
        Hw=H@w; lam_new=float(w@Hw)
        w=Hw/np.linalg.norm(Hw)
        if i>20 and abs(lam_new-lam)<1e-9*(abs(lam_new)+1): lam=lam_new; break
        lam=lam_new
    return lam, w

DELTA=1e-3; ALPHA=0.05; N_STEPS=20; BATCH=100

def gradient_ascent(label, Q_init, seed=0):
    np.random.seed(seed)
    Q=Q_init.copy()
    print(f"\n=== {label} ===")
    t0=time.time()
    H=compute_hessian(Q)
    lam,v=power_iter(H,n_iter=200)
    print(f"  Init: lam={lam:.6f}, H_norm={lam/48:.8f}, Hessian build={time.time()-t0:.1f}s")
    sys.stdout.flush()
    
    history=[]
    for step in range(N_STEPS):
        ts=time.time()
        # Compute gradient for batch
        batch=np.random.choice(n_links,BATCH,replace=False)
        grad=np.zeros((n_links,3))
        for l in batch:
            # Baseline T_P for plaquettes containing l
            T_base=[compute_T_P(Q,plaquettes[pi],v) for (pi,pos) in link_to_plaqs[l]]
            for a in range(3):
                Q_save=Q[l].copy()
                Q[l]=Q[l]@su2_exp([DELTA if aa==a else 0.0 for aa in range(3)])
                dT=sum(compute_T_P(Q,plaquettes[pi],v)-T_base[i]
                       for i,(pi,pos) in enumerate(link_to_plaqs[l]))
                grad[l,a]=dT/DELTA
                Q[l]=Q_save
        
        # Update batch links
        for l in batch:
            g_coeffs=[ALPHA*grad[l,a] for a in range(3)]
            gnorm=np.sqrt(sum(c**2 for c in g_coeffs))
            if gnorm>1e-12:
                Q[l]=Q[l]@su2_exp(g_coeffs)
                # Reorthogonalize to SU(2)
                U=Q[l]; d2=np.sqrt(abs(np.linalg.det(U)))
                if d2>1e-10: Q[l]=U/d2
        
        # Rebuild H every 5 steps
        if step%5==4:
            H=compute_hessian(Q)
        
        # Update v_max
        lam,v=power_iter(H,v0=v,n_iter=40)
        hnorm=lam/48.0
        dt=time.time()-ts
        print(f"  step {step+1:02d}: lam={lam:.6f}, H_norm={hnorm:.8f}, t={dt:.1f}s"
              +(" *** EXCEEDS 1/12 ***" if hnorm>1/12+1e-6 else ""))
        history.append({"step":step+1,"lam":float(lam),"H_norm":float(hnorm)})
        sys.stdout.flush()
        
        if hnorm>1/12+1e-5:
            print("  COUNTEREXAMPLE FOUND!")
            break
    
    return {"label":label,"final_lam":float(lam),"final_H_norm":float(hnorm),"history":history}

np.random.seed(42)
results_ga=[]

# Config 1: Q=I
Q_I=np.zeros((n_links,2,2),dtype=complex)
for l in range(n_links): Q_I[l]=I2.copy()
results_ga.append(gradient_ascent("Q=I (trivial vacuum)", Q_I, seed=1))

# Config 2: Small random perturbation of Q=I
Q_p=np.zeros((n_links,2,2),dtype=complex)
np.random.seed(10)
for l in range(n_links): Q_p[l]=Q_I[l]@su2_exp(0.3*np.random.randn(3))
results_ga.append(gradient_ascent("Q=I + eps=0.3 perturbation", Q_p, seed=2))

# Config 3: Random Haar
Q_r=np.zeros((n_links,2,2),dtype=complex)
np.random.seed(20)
for l in range(n_links): Q_r[l]=random_su2()
results_ga.append(gradient_ascent("Random Haar", Q_r, seed=3))

# Config 4: Large perturbation
Q_l2=np.zeros((n_links,2,2),dtype=complex)
np.random.seed(30)
for l in range(n_links): Q_l2[l]=Q_I[l]@su2_exp(1.0*np.random.randn(3))
results_ga.append(gradient_ascent("Q=I + eps=1.0 perturbation", Q_l2, seed=4))

# Config 5: Another random
Q_r2=np.zeros((n_links,2,2),dtype=complex)
np.random.seed(40)
for l in range(n_links): Q_r2[l]=random_su2()
results_ga.append(gradient_ascent("Random Haar 2", Q_r2, seed=5))

print("\n=== GRADIENT ASCENT SUMMARY ===")
for r in results_ga:
    flag="*** EXCEEDS 1/12 ***" if r['final_H_norm']>1/12+1e-6 else ""
    print(f"  {r['label']}: final H_norm={r['final_H_norm']:.8f} {flag}")

out_path=os.path.join(OUTDIR,"results_gradient.json")
with open(out_path,"w") as f:
    json.dump({"gradient_ascent":results_ga},f,indent=2)
print(f"Saved to {out_path}")
print("DONE gradient_ascent.py")

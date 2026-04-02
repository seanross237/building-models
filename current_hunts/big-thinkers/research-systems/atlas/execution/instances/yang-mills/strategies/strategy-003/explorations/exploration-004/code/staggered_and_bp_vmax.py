"""
staggered_and_bp_vmax.py

Two tasks:
1. Test staggered mode v[l(x,mu), a=0] = (-1)^(|x|+mu) as specified in GOAL.md
   (this is different from (-1)^|x| which was previously tested)
   Compare: isotropic (-1)^|x|, directional (-1)^|x|*delta_mu=0, and (-1)^(|x|+mu)

2. B_P bound with v_max (not random v):
   For 5 configurations (Q=I, near-identity eps=0.1, Gibbs beta=2, random x2),
   compute v_max via power iteration, then compute BP_sum / |v_max|^2 and compare to 4d=16.
"""

import numpy as np, json, time

L=4; d=4; N_SU=2; beta=1.0; bN=beta/N_SU
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
def link_idx(si,mu): return si*d+mu
def add_dir(site,mu):
    x=list(site); x[mu]=(x[mu]+1)%L; return tuple(x)
def su2d(U): return U.conj().T
def random_su2():
    q=np.random.randn(4); q/=np.linalg.norm(q)
    return q[0]*I2+1j*(q[1]*sigma[0]+q[2]*sigma[1]+q[3]*sigma[2])
def su2_exp(c):
    A=sum(c[a]*tau[a] for a in range(3))
    cs=float(np.real(sum(c[i]**2 for i in range(3))))
    if cs<1e-30: return I2+A
    th=np.sqrt(cs)
    return np.cos(th/2)*I2+(np.sin(th/2)/(th/2))*A

# Build plaquettes
plaquettes=[]
for xi in range(n_sites):
    x=idx_to_site(xi)
    for mu in range(d):
        for nu in range(mu+1,d):
            xm=add_dir(x,mu); xn=add_dir(x,nu)
            l0=link_idx(site_to_idx(x),mu); l1=link_idx(site_to_idx(xm),nu)
            l2=link_idx(site_to_idx(xn),mu); l3=link_idx(site_to_idx(x),nu)
            plaquettes.append([(l0,+1),(l1,+1),(l2,-1),(l3,-1)])

# ================================================================
# PART 1: Staggered mode comparison
# ================================================================
print("="*60)
print("PART 1: Staggered mode comparison at Q=I")
print("="*60)

# Build K_curl to compute Rayleigh quotients efficiently
K_curl=np.zeros((n_links,n_links))
for plaq in plaquettes:
    for (li,si) in plaq:
        for (lj,sj) in plaq:
            K_curl[li,lj]+=si*sj

# Mode A: isotropic staggered (-1)^|x| for all links, gen 0
v_A=np.zeros(n_dof)
for l in range(n_links):
    x=idx_to_site(l//d)
    v_A[l*n_gen+0]=(-1)**sum(x)
v_A/=np.linalg.norm(v_A)

# Mode B: directional staggered (-1)^|x| for mu=0 links only, gen 0
v_B=np.zeros(n_dof)
for l in range(n_links):
    mu=l%d
    if mu==0:
        x=idx_to_site(l//d)
        v_B[l*n_gen+0]=(-1)**sum(x)
v_B/=np.linalg.norm(v_B)

# Mode C: GOAL.md staggered (-1)^(|x|+mu) for all links, gen 0
v_C=np.zeros(n_dof)
for l in range(n_links):
    x=idx_to_site(l//d); mu=l%d
    v_C[l*n_gen+0]=(-1)**(sum(x)+mu)
v_C/=np.linalg.norm(v_C)

# Mode D: (-1)^(|x|+mu) for mu=0 only (same as mode B shifted by (-1)^0=1, so identical)
# Also try the "correct" directional staggered: v[l(x,mu)] = (-1)^|x| * delta_{mu,0} -- this is v_B

# Rayleigh quotient at Q=I: v^T H v = bN * v^T (K_curl tensor I3) v
# = bN * sum_{l,l'} K_curl[l,l'] sum_a v[l*n_gen+a] v[l'*n_gen+a]
# = bN * sum_a v_a^T K_curl v_a

def rayleigh_QI(v):
    # Extract per-generator components
    rq=0.0
    for a in range(n_gen):
        va=v[a::n_gen]  # component a of all links
        rq+=bN*float(va@K_curl@va)
    return rq

rA=rayleigh_QI(v_A); rB=rayleigh_QI(v_B); rC=rayleigh_QI(v_C)
print(f"Mode A (isotropic staggered (-1)^|x|): Rayleigh = {rA:.8f}")
print(f"  H_norm = {rA/(48*beta):.8f}, expected 0.000000 (null space)")
print(f"Mode B (directional staggered (-1)^|x| * delta_mu=0): Rayleigh = {rB:.8f}")
print(f"  H_norm = {rB/(48*beta):.8f}, expected ~4.000000 (from prior computation)")
print(f"Mode C (GOAL.md staggered (-1)^(|x|+mu)): Rayleigh = {rC:.8f}")
print(f"  H_norm = {rC/(48*beta):.8f}")
print()

# Is mode C an eigenvector?
v_C_link=np.zeros(n_links)
for l in range(n_links):
    x=idx_to_site(l//d); mu=l%d
    v_C_link[l]=(-1)**(sum(x)+mu)
v_C_link/=np.linalg.norm(v_C_link)
Kv_C=K_curl@v_C_link
lam_C=float(v_C_link@Kv_C)
res_C=np.linalg.norm(Kv_C-lam_C*v_C_link)/(abs(lam_C)+1e-30)
print(f"Mode C as eigenvector of K_curl: eigenvalue={lam_C:.6f}, residual={res_C:.2e}")
print(f"  As eigenvalue of H (beta/N * lam_C): {bN*lam_C:.6f} (H_norm={bN*lam_C/(48*beta):.8f})")
print()

# Additional modes: (-1)^(|x|+mu) only for mu=0
v_C0=np.zeros(n_dof)
for l in range(n_links):
    x=idx_to_site(l//d); mu=l%d
    if mu==0:
        v_C0[l*n_gen+0]=(-1)**(sum(x)+0)  # mu=0 so (-1)^(|x|+0) = (-1)^|x|
v_C0/=np.linalg.norm(v_C0)
rC0=rayleigh_QI(v_C0)
print(f"Mode C0 (GOAL mode restricted to mu=0): Rayleigh = {rC0:.8f}")
print(f"  (This equals Mode B since (-1)^(|x|+0) = (-1)^|x|)")
print()

# Try mode: (-1)^(|x|+mu) for each direction separately
print("Per-direction (-1)^(|x|+mu) modes:")
for mu0 in range(d):
    v_mu=np.zeros(n_dof)
    for l in range(n_links):
        x=idx_to_site(l//d); mu=l%d
        if mu==mu0:
            v_mu[l*n_gen+0]=(-1)**(sum(x)+mu0)
    if np.linalg.norm(v_mu)>0:
        v_mu/=np.linalg.norm(v_mu)
        r_mu=rayleigh_QI(v_mu)
        print(f"  mu={mu0}: Rayleigh = {r_mu:.8f}, H_norm = {r_mu/(48*beta):.8f}")

print()

# ================================================================
# PART 2: B_P bound with v_max for 5 configurations
# ================================================================
print("="*60)
print("PART 2: B_P bound with v_max at specific configurations")
print("="*60)

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

def power_iter(H, n_iter=150, v0=None):
    n=H.shape[0]
    w=v0 if v0 is not None else np.random.randn(n)
    w/=np.linalg.norm(w)
    lam=0.0
    for i in range(n_iter):
        Hw=H@w; lam_new=float(w@Hw)
        w=Hw/np.linalg.norm(Hw)
        if i>20 and abs(lam_new-lam)<1e-9*(abs(lam_new)+1): lam=lam_new; break
        lam=lam_new
    return lam, w

def compute_BP_sum(Q, v_flat):
    """Compute sum_P |B_P(Q,v)|^2 using parallel transport."""
    total=0.0
    for plaq in plaquettes:
        G=[I2.copy()]
        for k in range(4):
            l,s=plaq[k]
            Wk=Q[l] if s==+1 else su2d(Q[l])
            G.append(G[-1]@Wk)
        B_P=np.zeros((2,2),dtype=complex)
        for k in range(4):
            l,s=plaq[k]
            v_l=sum(float(v_flat[l*n_gen+a])*tau[a] for a in range(n_gen))
            B_P+=s*(G[k]@v_l@su2d(G[k]))
        total+=-2.0*np.real(np.trace(B_P@B_P))
    return total

# Configurations
configs={}
Q_I=np.zeros((n_links,2,2),dtype=complex)
for l in range(n_links): Q_I[l]=I2.copy()
configs['Q=I']=Q_I

np.random.seed(7)
Q_eps=np.zeros((n_links,2,2),dtype=complex)
for l in range(n_links): Q_eps[l]=Q_I[l]@su2_exp(0.1*np.random.randn(3))
configs['near-id eps=0.1']=Q_eps

# Gibbs-like: use a warm start
np.random.seed(13)
Q_g=np.zeros((n_links,2,2),dtype=complex)
for l in range(n_links): Q_g[l]=Q_I[l]@su2_exp(0.5*np.random.randn(3))
configs['warm start eps=0.5']=Q_g

np.random.seed(21)
Q_r1=np.zeros((n_links,2,2),dtype=complex)
for l in range(n_links): Q_r1[l]=random_su2()
configs['random Haar 1']=Q_r1

np.random.seed(29)
Q_r2=np.zeros((n_links,2,2),dtype=complex)
for l in range(n_links): Q_r2[l]=random_su2()
configs['random Haar 2']=Q_r2

bp_vmax_results=[]
for name, Q in configs.items():
    t0=time.time()
    print(f"\nConfig: {name}")
    H=compute_hessian(Q)
    t1=time.time()
    # Use v_stag_dir as starting vector for power iter at Q=I, random otherwise
    lam,v_max=power_iter(H,n_iter=200)
    t2=time.time()
    hnorm=lam/(48*beta)
    print(f"  lambda_max = {lam:.6f}, H_norm = {hnorm:.8f}, build={t1-t0:.1f}s, iter={t2-t1:.1f}s")
    
    # B_P sum with v_max
    BP_sum=compute_BP_sum(Q,v_max)
    BP_ratio=BP_sum/np.sum(v_max**2)
    print(f"  BP_sum/|v|^2 = {BP_ratio:.6f}, bound 4d=16")
    print(f"  BP bound satisfied: {BP_ratio <= 16+1e-4}")
    
    # Also B_P sum with random vector for comparison
    v_rand=np.random.randn(n_dof); v_rand/=np.linalg.norm(v_rand)
    BP_rand=compute_BP_sum(Q,v_rand)
    print(f"  BP_sum/|v|^2 for random v: {BP_rand:.6f}")
    
    bp_vmax_results.append({
        'config': name, 'H_norm': float(hnorm), 'lambda_max': float(lam),
        'BP_ratio_vmax': float(BP_ratio), 'BP_ratio_random': float(BP_rand),
        'BP_bound_satisfied': bool(BP_ratio <= 16+1e-4)
    })

print("\n"+"="*60)
print("SUMMARY: B_P bound with v_max")
print("="*60)
for r in bp_vmax_results:
    flag="✓" if r['BP_bound_satisfied'] else "VIOLATED"
    print(f"  {r['config']:25s}: H_norm={r['H_norm']:.6f}, BP(v_max)={r['BP_ratio_vmax']:.4f} {flag}")

with open('/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/yang-mills/strategies/strategy-003/explorations/exploration-004/code/staggered_bp_vmax_results.json','w') as f:
    json.dump({'staggered_modes': {'rA':float(rA),'rB':float(rB),'rC':float(rC),'rC0':float(rC0),'lam_K_C':float(lam_C)},
               'bp_vmax': bp_vmax_results}, f, indent=2)
print("\nSaved to staggered_bp_vmax_results.json")
print("DONE staggered_and_bp_vmax.py")

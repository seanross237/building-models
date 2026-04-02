"""
pp_bound_corrected.py - Per-plaquette bound test with CORRECTED B_P formula.

From first principles (Convention 2: Q_k → exp(s_k ε τ_a) Q_k):
  B_P(Q,v) = Σ_{k,a} v_{k,a} × s_k × Lp[k] × τ_a × W_k × Rs[k]

At Q=I: B_P(I,v) = Σ_{k,a} v_{k,a} s_k τ_a
         |B_P|² = Σ_a (Σ_k s_k v_k)² [correct coboundary]

The per-plaquette bound to test: H_P(Q,v) ≤ (bN/2)|B_P(Q,v)|²

Previous code had wrong formula for sk=+1: used Lp[k+1]@tau@Rs[k] = Lp[k]W_k tau Rs[k]
Correct: s_k × Lp[k] @ tau[a] @ W[k] @ Rs[k]
"""
import numpy as np, json, os

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
    th=np.sqrt(cs); return np.cos(th/2)*I2+(np.sin(th/2)/(th/2))*A

plaquettes=[]
for xi in range(n_sites):
    x=idx_to_site(xi)
    for mu in range(d):
        for nu in range(mu+1,d):
            xm=add_dir(x,mu); xn=add_dir(x,nu)
            l0=link_idx(site_to_idx(x),mu); l1=link_idx(site_to_idx(xm),nu)
            l2=link_idx(site_to_idx(xn),mu); l3=link_idx(site_to_idx(x),nu)
            plaquettes.append([(l0,+1),(l1,+1),(l2,-1),(l3,-1)])

def compute_T_P(Q, plaq, v):
    """v^T H_P v for one plaquette."""
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

def compute_BP_sq_corrected(Q, plaq, v):
    """
    CORRECTED B_P: B_P(Q,v) = Σ_{k,a} v_{k,a} × s_k × Lp[k] × τ_a × W_k × Rs[k]
    |B_P|² = -2 Re Tr(B_P²) [anti-Hermitian norm, = Σ_a (Σ_k s_k v_k)² at Q=I]
    """
    W=[Q[l] if s==+1 else su2d(Q[l]) for (l,s) in plaq]
    lids=[l for (l,s) in plaq]; sgns=[s for (l,s) in plaq]
    Lp=[I2.copy()]
    for k in range(4): Lp.append(Lp[-1]@W[k])
    Rs=[None]*4; Rs[3]=I2.copy()
    for k in range(2,-1,-1): Rs[k]=W[k+1]@Rs[k+1]

    BP=np.zeros((2,2),dtype=complex)
    for k in range(4):
        lk=lids[k]; sk=sgns[k]
        for a in range(n_gen):
            # CORRECT: s_k × Lp[k] × tau_a × W_k × Rs[k]
            dU = sk * (Lp[k] @ tau[a] @ W[k] @ Rs[k])
            BP += v[lk*n_gen+a] * dU

    BP_sq = -2.0 * float(np.real(np.trace(BP @ BP)))
    return BP_sq

# Verify at Q=I: check |B_P|² = Σ_a (Σ_k s_k v_k)²
print("="*60)
print("VERIFICATION at Q=I")
print("="*60)
Q_I = np.array([I2.copy() for _ in range(n_links)])
np.random.seed(42)
v_test = np.random.randn(n_dof); v_test /= np.linalg.norm(v_test)

# Compute coboundary B_P directly
for pi, plaq in enumerate(plaquettes[:5]):
    lids=[l for (l,s) in plaq]; sgns=[s for (l,s) in plaq]
    # Coboundary |B_P|² = Σ_a (Σ_k s_k v_{k,a})²
    bpsq_cob = sum((sum(sgns[k]*v_test[lids[k]*n_gen+a] for k in range(4)))**2 for a in range(n_gen))
    bpsq_formula = compute_BP_sq_corrected(Q_I, plaq, v_test)
    hp = compute_T_P(Q_I, plaq, v_test)
    ratio = hp / (bN/2 * bpsq_formula) if abs(bpsq_formula) > 1e-12 else float('nan')
    print(f"  Plaq {pi}: |B_P|²_cob={bpsq_cob:.6f}, |B_P|²_formula={bpsq_formula:.6f}, "
          f"H_P={hp:.6f}, ratio={ratio:.6f}")
print()

# Now test per-plaquette bound for multiple configs
print("="*60)
print("PER-PLAQUETTE BOUND H_P ≤ (bN/2)|B_P|² FOR MULTIPLE Q")
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

configs = [("Q=I", Q_I.copy())]
np.random.seed(10)
Q_p01 = np.array([Q_I[l] @ su2_exp(0.1*np.random.randn(3)) for l in range(n_links)])
configs.append(("near-id eps=0.1", Q_p01))
np.random.seed(10)
Q_p05 = np.array([Q_I[l] @ su2_exp(0.5*np.random.randn(3)) for l in range(n_links)])
configs.append(("near-id eps=0.5", Q_p05))
np.random.seed(20)
Q_r1 = np.array([random_su2() for _ in range(n_links)])
configs.append(("random Haar 1", Q_r1))
np.random.seed(30)
Q_r2 = np.array([random_su2() for _ in range(n_links)])
configs.append(("random Haar 2", Q_r2))

results = []
for label, Q in configs:
    print(f"\n{label}:")
    H = compute_hessian(Q)
    evals, evecs = np.linalg.eigh(H)
    lam_max = evals[-1]; v_max = evecs[:,-1]
    H_norm = lam_max / (48*beta)
    print(f"  λ_max={lam_max:.4f}, H_norm={H_norm:.6f}")

    # Check per-plaquette bound with v_max
    max_ratio = -1e9; min_ratio = 1e9
    n_pos_bp = 0; n_neg_bp = 0; n_zero_bp = 0
    max_ratio_pos = -1e9  # only where |B_P|² > 0

    for plaq in plaquettes:
        HP = compute_T_P(Q, plaq, v_max)
        BPsq = compute_BP_sq_corrected(Q, plaq, v_max)
        bound = bN/2 * BPsq

        if BPsq > 1e-10:
            ratio = HP / bound
            max_ratio = max(max_ratio, ratio)
            min_ratio = min(min_ratio, ratio)
            max_ratio_pos = max(max_ratio_pos, ratio)
            n_pos_bp += 1
        elif BPsq < -1e-10:
            n_neg_bp += 1
        else:
            n_zero_bp += 1

    # Also test with 5 random unit vectors
    max_ratio_rand = -1e9
    np.random.seed(0)
    for _ in range(5):
        v_rand = np.random.randn(n_dof); v_rand /= np.linalg.norm(v_rand)
        for plaq in plaquettes:
            HP = compute_T_P(Q, plaq, v_rand)
            BPsq = compute_BP_sq_corrected(Q, plaq, v_rand)
            if BPsq > 1e-10:
                ratio = HP / (bN/2 * BPsq)
                max_ratio_rand = max(max_ratio_rand, ratio)

    violated = max_ratio_pos > 1.0 + 1e-4
    print(f"  |B_P|² > 0: {n_pos_bp}, < 0: {n_neg_bp}, ≈ 0: {n_zero_bp}")
    print(f"  Max ratio (|B_P|²>0, v_max): {max_ratio_pos:.6f}")
    print(f"  Max ratio (random v): {max_ratio_rand:.6f}")
    print(f"  Violated? {'YES *** VIOLATION ***' if violated else 'NO'}")

    results.append({
        "config": label, "H_norm": float(H_norm), "lambda_max": float(lam_max),
        "n_pos_bp": n_pos_bp, "n_neg_bp": n_neg_bp, "n_zero_bp": n_zero_bp,
        "max_ratio_pos_vmax": float(max_ratio_pos),
        "max_ratio_rand": float(max_ratio_rand),
        "violated": bool(violated)
    })

print()
print("="*60)
print("SUMMARY")
print("="*60)
for r in results:
    flag = " *** VIOLATION ***" if r['violated'] else ""
    print(f"  {r['config']}: max ratio = {r['max_ratio_pos_vmax']:.6f}{flag}")

OUTDIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(OUTDIR, "pp_bound_corrected_results.json"), "w") as f:
    json.dump(results, f, indent=2)
print(f"\nSaved to pp_bound_corrected_results.json")
print("DONE")

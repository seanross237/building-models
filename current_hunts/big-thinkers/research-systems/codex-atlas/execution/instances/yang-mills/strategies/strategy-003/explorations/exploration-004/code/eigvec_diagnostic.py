"""
eigvec_diagnostic.py - Find the actual K_curl and H maximum eigenvectors at Q=I,
test per-plaquette bound H_P ≤ (bN/2)|B_P|², and update staggered mode analysis.
"""
import numpy as np, json

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

# Build K_curl
K_curl=np.zeros((n_links,n_links))
for plaq in plaquettes:
    for (li,si) in plaq:
        for (lj,sj) in plaq:
            K_curl[li,lj]+=si*sj

print("="*60)
print("PART 1: K_curl Rayleigh quotients for candidate modes")
print("="*60)

# Mode A: isotropic staggered (-1)^|x|, all links
vA=np.zeros(n_links)
for l in range(n_links):
    x=idx_to_site(l//d); vA[l]=(-1)**sum(x)
vA/=np.linalg.norm(vA)
rA=float(vA@K_curl@vA)
print(f"Mode A: isotropic (-1)^|x|  → K_curl quotient = {rA:.4f}")

# Mode B: directional mu=0 only, f=(1,0,0,0)
vB=np.zeros(n_links)
for l in range(n_links):
    x=idx_to_site(l//d); mu=l%d
    if mu==0: vB[l]=(-1)**sum(x)
vB/=np.linalg.norm(vB)
rB=float(vB@K_curl@vB)
print(f"Mode B: directional mu=0 only (-1)^|x| δ_{{μ,0}}  → K_curl quotient = {rB:.4f}")
print(f"  (H quotient = bN/2 × {rB:.4f} = {bN/2*rB:.4f})")

# Mode C: (-1)^(|x|+mu), Σf=0
vC=np.zeros(n_links)
for l in range(n_links):
    x=idx_to_site(l//d); mu=l%d; vC[l]=(-1)**(sum(x)+mu)
vC/=np.linalg.norm(vC)
rC=float(vC@K_curl@vC)
print(f"Mode C: (-1)^(|x|+mu) f=(-1)^mu  → K_curl quotient = {rC:.4f}")
print(f"  (H quotient = bN/2 × {rC:.4f} = {bN/2*rC:.4f})")

# Mode D: zero-sum f=(1,-1,0,0)/sqrt(2)
vD=np.zeros(n_links)
for l in range(n_links):
    x=idx_to_site(l//d); mu=l%d
    if mu==0: vD[l]=(-1)**sum(x)/np.sqrt(2)
    elif mu==1: vD[l]=-(-1)**sum(x)/np.sqrt(2)
vD/=np.linalg.norm(vD)
rD=float(vD@K_curl@vD)
print(f"Mode D: zero-sum f=(1,-1,0,0)/√2  → K_curl quotient = {rD:.4f}")
print(f"  (H quotient = bN/2 × {rD:.4f} = {bN/2*rD:.4f})")

print()
print("="*60)
print("PART 2: K_curl exact maximum eigenvectors (top eigenvalues)")
print("="*60)
evals_K, evecs_K = np.linalg.eigh(K_curl)
idx_desc = np.argsort(evals_K)[::-1]
evals_K = evals_K[idx_desc]; evecs_K = evecs_K[:, idx_desc]
print(f"Top 5 K_curl eigenvalues: {evals_K[:5]}")
print(f"λ_max(K_curl) = {evals_K[0]:.6f}")
print(f"Multiplicity of λ_max: {np.sum(evals_K > evals_K[0]-0.01)}")

# Analyze maximum eigenvectors structure
print("\nMaximum eigenvector structure (top 3):")
for ev_idx in range(min(3, int(np.sum(evals_K > evals_K[0]-0.01)))):
    ev = evecs_K[:, ev_idx]
    # Compute per-direction averages
    per_mu = []
    for mu in range(d):
        links_mu = [l for l in range(n_links) if l%d == mu]
        per_mu.append(np.sum(ev[links_mu]**2))
    print(f"  Eigvec {ev_idx+1}: per-dir energy = {per_mu} (sum={sum(per_mu):.4f})")
    # Check if it looks like (-1)^|x| f(mu)
    correlations = []
    for mu in range(d):
        links_mu = np.array([l for l in range(n_links) if l%d == mu])
        if len(links_mu) > 0:
            stag = np.array([(-1)**sum(idx_to_site(l//d)) for l in links_mu])
            pattern = ev[links_mu]
            corr = abs(np.dot(pattern, stag)) / (np.linalg.norm(pattern)*np.linalg.norm(stag))
            correlations.append(corr)
    print(f"    Correlation with (-1)^|x| per direction: {[f'{c:.3f}' for c in correlations]}")

print()
print("="*60)
print("PART 3: Per-plaquette bound H_P ≤ (bN/2)|B_P|² test")
print("="*60)
print("At Q=I: checking equality H_P = (bN/2)|B_P|² analytically")

# Build full Hessian at Q=I to get max eigenvector v_max
def compute_hessian_QI():
    H=np.zeros((n_dof,n_dof))
    for plaq in plaquettes:
        lids=[l for (l,s) in plaq]; sgns=[s for (l,s) in plaq]
        dv=bN/2  # (bN/4)*Re Tr(I) = (bN/4)*2 = bN/2
        for k in range(4):
            lk=lids[k]
            for a in range(n_gen): H[lk*n_gen+a,lk*n_gen+a]+=dv
        for k in range(4):
            lk=lids[k]; sk=sgns[k]
            for m in range(k+1,4):
                lm=lids[m]; sm=sgns[m]
                # val = sk*sm*Re Tr(tau_a tau_b) = sk*sm*(-delta_ab/2)
                # H[ii,jj] += -bN * val = bN * sk*sm/2 * delta_ab
                for a in range(n_gen):
                    ii=lk*n_gen+a; jj=lm*n_gen+a
                    H[ii,jj]+=bN*sk*sm/2; H[jj,ii]+=bN*sk*sm/2
    return H

print("Building Hessian at Q=I (3072x3072)...", flush=True)
H_QI = compute_hessian_QI()
print(f"λ_max(H at Q=I) from full eigvalsh...", end=" ", flush=True)
evals_H = np.linalg.eigvalsh(H_QI)
print(f"{evals_H[-1]:.6f} (expected 4.0)")
print(f"Top 5 H eigenvalues: {evals_H[-5:][::-1]}")

# Verify H = (bN/2) K_curl ⊗ I_3
H_check = np.zeros((n_dof, n_dof))
for a in range(n_gen):
    for la in range(n_links):
        for lb in range(n_links):
            H_check[la*n_gen+a, lb*n_gen+a] = bN/2 * K_curl[la,lb]
diff = np.max(np.abs(H_QI - H_check))
print(f"\nMax |H_QI - (bN/2)*K_curl⊗I₃| = {diff:.2e} (should be ~0)")

print()
print("="*60)
print("PART 4: Per-plaquette test with general Q")
print("="*60)

def compute_T_P(Q, plaq, v):
    """H_P(Q,v) = v^T H_P v for one plaquette."""
    W=[Q[l] if s==+1 else su2d(Q[l]) for (l,s) in plaq]
    lids=[l for (l,s) in plaq]
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
        lk=lids[k]; sk=int([s for (l,s) in plaq][k])
        for m in range(k+1,4):
            lm=lids[m]; sm=int([s for (l,s) in plaq][m])
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

def compute_BP_sq(Q, plaq, v):
    """
    B_P(Q,v) = Σ_{k,a} v_{k,a} × dU_P/dv_{k,a}
    s_k=+1: dU/dv_{k,a} = Lp[k] W_k tau_a Rs[k] (right mult)
    s_k=-1: dU/dv_{k,a} = -Lp[k] tau_a W_k Rs[k] (left mult, negative)
    |B_P|² = -2 Re Tr(B_P²) (using |A|²=-2Tr(A²) convention for anti-Hermitian)
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
            if sk==+1:
                # dU/dv_{k,a} = Lp[k] W_k tau_a Rs[k] = Lp[k+1] tau_a Rs[k]
                dU = Lp[k+1] @ tau[a] @ Rs[k]
            else:
                # dU/dv_{k,a} = -Lp[k] tau_a W_k Rs[k]
                dU = -Lp[k] @ tau[a] @ W[k] @ Rs[k]
            BP += v[lk*n_gen+a] * dU

    # |B_P|² = -2 Re Tr(B_P²)
    BP_sq = -2.0 * float(np.real(np.trace(BP @ BP)))
    return BP_sq

# Test at Q=I: verify H_P = (bN/2)|B_P|² (should be equality)
Q_I = np.array([I2.copy() for _ in range(n_links)])
np.random.seed(42)
v_test = np.random.randn(n_dof); v_test /= np.linalg.norm(v_test)

ratios_QI = []
for pi, plaq in enumerate(plaquettes[:20]):  # First 20 plaquettes
    HP = compute_T_P(Q_I, plaq, v_test)
    BPsq = compute_BP_sq(Q_I, plaq, v_test)
    bound = bN/2 * BPsq
    if abs(BPsq) > 1e-10:
        ratio = HP / bound if abs(bound) > 1e-12 else float('nan')
        ratios_QI.append(ratio)

print(f"At Q=I (random v): H_P / ((bN/2)|B_P|²) for 20 plaquettes:")
print(f"  Min={min(ratios_QI):.6f}, Max={max(ratios_QI):.6f}, Mean={np.mean(ratios_QI):.6f}")
print(f"  (Expected: all = 1.0 at Q=I)")

# Full test: 10 configs, max eigenvector v_max
print("\nTesting H_P ≤ (bN/2)|B_P|² for multiple Q configs...")
configs = []
for l in range(n_links): Q_I[l] = I2.copy()
configs.append(("Q=I", Q_I.copy()))

np.random.seed(10)
Q_p = np.array([Q_I[l] @ su2_exp(0.1*np.random.randn(3)) for l in range(n_links)])
configs.append(("near-id eps=0.1", Q_p))

np.random.seed(20)
Q_r1 = np.array([random_su2() for _ in range(n_links)])
configs.append(("random Haar 1", Q_r1))

np.random.seed(30)
Q_r2 = np.array([random_su2() for _ in range(n_links)])
configs.append(("random Haar 2", Q_r2))

results_pp = []
for label, Q in configs:
    # Get v via power iteration on this config's Hessian
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

    print(f"  {label}: building Hessian...", end=" ", flush=True)
    H = compute_hessian(Q)
    evals, evecs = np.linalg.eigh(H)
    lam_max = evals[-1]; v_max = evecs[:,-1]
    H_norm = lam_max / (48*beta)
    print(f"λ_max={lam_max:.4f}, H_norm={H_norm:.6f}")

    # Per-plaquette bound test with v_max
    max_ratio = -1e9; min_ratio = 1e9; n_nonzero = 0
    for plaq in plaquettes:
        HP = compute_T_P(Q, plaq, v_max)
        BPsq = compute_BP_sq(Q, plaq, v_max)
        if abs(BPsq) > 1e-10:
            bound = bN/2 * BPsq
            ratio = HP / bound
            max_ratio = max(max_ratio, ratio)
            min_ratio = min(min_ratio, ratio)
            n_nonzero += 1

    # Also test with 3 random unit vectors
    max_ratio_rand = -1e9
    for _ in range(3):
        v_rand = np.random.randn(n_dof); v_rand /= np.linalg.norm(v_rand)
        for plaq in plaquettes:
            HP = compute_T_P(Q, plaq, v_rand)
            BPsq = compute_BP_sq(Q, plaq, v_rand)
            if abs(BPsq) > 1e-10:
                bound = bN/2 * BPsq
                ratio = HP / bound
                max_ratio_rand = max(max_ratio_rand, ratio)

    violated = max_ratio > 1.0 + 1e-4
    print(f"    Per-plaquette ratios (v_max): min={min_ratio:.4f}, max={max_ratio:.4f}, n={n_nonzero}")
    print(f"    Per-plaquette max ratio (random v): {max_ratio_rand:.4f}")
    print(f"    Bound H_P ≤ (bN/2)|B_P|² violated? {'YES *** VIOLATION ***' if violated else 'NO'}")
    results_pp.append({
        "config": label,
        "H_norm": float(H_norm),
        "lambda_max": float(lam_max),
        "pp_ratio_max_vmax": float(max_ratio),
        "pp_ratio_min_vmax": float(min_ratio),
        "pp_ratio_max_rand": float(max_ratio_rand),
        "violated": bool(violated)
    })

print()
print("="*60)
print("SUMMARY")
print("="*60)
any_viol = any(r['violated'] for r in results_pp)
print(f"Per-plaquette bound H_P ≤ (bN/2)|B_P|² violated for ANY config: {any_viol}")
for r in results_pp:
    flag = " *** VIOLATION ***" if r['violated'] else ""
    print(f"  {r['config']}: max ratio = {r['pp_ratio_max_vmax']:.4f}{flag}")

import os
OUTDIR = os.path.dirname(os.path.abspath(__file__))
out = {
    "K_curl_rayleigh_quotients": {
        "mode_A_isotropic": rA, "mode_B_directional_mu0": rB,
        "mode_C_alternating_mu": rC, "mode_D_zero_sum": rD,
        "lambda_max_K_curl": float(evals_K[0])
    },
    "H_equals_bN_over_2_Kcurl": float(diff),
    "per_plaquette_bound": results_pp
}
with open(os.path.join(OUTDIR, "eigvec_diagnostic_results.json"), "w") as f:
    json.dump(out, f, indent=2)
print(f"\nSaved to eigvec_diagnostic_results.json")
print("DONE")

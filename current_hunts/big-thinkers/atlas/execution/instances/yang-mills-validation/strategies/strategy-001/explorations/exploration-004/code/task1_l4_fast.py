"""
Task 1 FAST: L=4, d=4 — dense H build (0.13s) + eigsh warm start (0.57s).
Sanity check + 20 configurations including 5 adversarial with 30 gradient steps.
"""
import sys, os, json, time
import numpy as np
import scipy.linalg as la
import scipy.sparse.linalg as spla
from itertools import product as iproduct

np.random.seed(42)

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

def normalize_su2_arr(U):
    out=np.empty_like(U)
    for i in range(len(U)):
        d=np.linalg.det(U[i]); out[i]=U[i]/(np.sqrt(d) if abs(d)>1e-12 else 1)
    return out

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
    by_link=[[] for _ in range(n_links)]
    for p in plaq_list:
        for pos,(lk,_) in enumerate(p): by_link[lk].append(p)
    return plaq_list, by_link, n_links

def build_H(U, plaq_list, beta, N, n_links, n_gen):
    n_dof=n_links*n_gen; H=np.zeros((n_dof,n_dof)); pf=beta/(2*N)
    for plaq in plaq_list:
        ei=[plaq[k][0] for k in range(4)]; sg=[plaq[k][1] for k in range(4)]
        Us=[U[ei[k]] for k in range(4)]
        P2=Us[0].copy(); P3=Us[0]@Us[1]@Us[2].conj().T; P4=P3@Us[3].conj().T
        Rs=[adjoint_rep(P) for P in [np.eye(N,dtype=complex),P2,P3,P4]]
        for i in range(4):
            for j in range(4):
                H[ei[i]*n_gen:(ei[i]+1)*n_gen,ei[j]*n_gen:(ei[j]+1)*n_gen]+=pf*sg[i]*sg[j]*Rs[i].T@Rs[j]
    return H

def lmax_and_vec(H, v0=None, tol=1e-9):
    """Efficient: eigsh on prebuilt H with warm start."""
    n=H.shape[0]
    A=spla.LinearOperator((n,n),matvec=lambda v: H@v,dtype=float)
    try:
        kw={'tol':tol,'maxiter':1000}
        if v0 is not None: kw['v0']=v0
        vals,vecs=spla.eigsh(A,k=1,which='LM',**kw)
        return float(vals[0]),vecs[:,0]
    except:
        evals,evecs=la.eigh(H)
        idx=np.argmax(evals); return evals[idx],evecs[:,idx]

def lmax_accurate(H):
    """Most accurate lmax via full eigvalsh."""
    return float(np.max(la.eigvalsh(H)))

def plaq_rq(vm, U, plaq, pf, N):
    ei=[plaq[k][0] for k in range(4)]; sg=[plaq[k][1] for k in range(4)]
    Us=[U[ei[k]] for k in range(4)]
    P2=Us[0].copy(); P3=Us[0]@Us[1]@Us[2].conj().T; P4=P3@Us[3].conj().T
    Rs=[adjoint_rep(P) for P in [np.eye(N,dtype=complex),P2,P3,P4]]
    t=0.0
    for i in range(4):
        for j in range(4): t+=float(vm[ei[i]]@(pf*sg[i]*sg[j]*Rs[i].T@Rs[j])@vm[ei[j]])
    return t

def compute_grad(U, v, by_link, plaq_list, beta, N, n_links, n_gen, eps=5e-4):
    pf=beta/(2*N); vm=v.reshape(n_links,n_gen); grad=np.zeros((n_links,n_gen))
    for e in range(n_links):
        plaqs=by_link[e]
        if not plaqs: continue
        for a in range(n_gen):
            Up=U.copy(); Up[e]=su2_exp(eps*tau[a])@U[e]
            Um=U.copy(); Um[e]=su2_exp(-eps*tau[a])@U[e]
            rp=sum(plaq_rq(vm,Up,p,pf,N) for p in plaqs)
            rm=sum(plaq_rq(vm,Um,p,pf,N) for p in plaqs)
            grad[e,a]=(rp-rm)/(2*eps)
    return grad

def wilson_action(U,plaq_list,beta,N):
    S=0.0
    for plaq in plaq_list:
        ei=[plaq[k][0] for k in range(4)]
        Up=U[ei[0]]@U[ei[1]]@U[ei[2]].conj().T@U[ei[3]].conj().T
        S+=np.real(np.trace(Up))
    return -beta/N*S

def gibbs_sample(U,plaq_list,beta,N,n_links,n_steps=2000):
    U=U.copy(); S=wilson_action(U,plaq_list,beta,N); acc=0
    for _ in range(n_steps):
        e=np.random.randint(n_links); Unew=random_su2(); Utmp=U.copy(); Utmp[e]=Unew
        Snew=wilson_action(Utmp,plaq_list,beta,N)
        if np.random.rand()<np.exp(-(Snew-S)): U[e]=Unew; S=Snew; acc+=1
    return U,acc/n_steps

# ============================================================
# SETUP
# ============================================================
L,d,N,beta=4,4,2,1.0
plaq_list,by_link,n_links=build_lattice(L,d)
n_gen=N**2-1; n_dof=n_links*n_gen; n_plaq=len(plaq_list)
H_NORM_BOUND=1/12

print(f"L={L}, d={d}, N={N}, beta={beta}")
print(f"n_links={n_links}, n_dof={n_dof}, n_plaq={n_plaq}")
print()

results=[]

# ============================================================
# SANITY CHECK: Q=I
# ============================================================
print("="*60); print("SANITY CHECK: Q=I"); print("="*60)
U_I=np.array([np.eye(2,dtype=complex)]*n_links)
t0=time.time()
H_I=build_H(U_I,plaq_list,beta,N,n_links,n_gen)
t_build=time.time()-t0
lmax_I,v_I=lmax_and_vec(H_I)
t_eig=time.time()-t0-t_build
hn_I=lmax_I/(48*beta)
print(f"  H build: {t_build:.2f}s, eigsh: {t_eig:.2f}s")
print(f"  lambda_max = {lmax_I:.8f}  (expected {4*beta:.8f})")
print(f"  H_norm     = {hn_I:.8f}  (expected {H_NORM_BOUND:.8f})")
print(f"  Difference = {abs(lmax_I-4*beta):.2e}")
assert abs(lmax_I-4*beta)<1e-3, f"SANITY FAILED: {lmax_I}"
print("  *** SANITY CHECK PASSED ***")
results.append({'type':'identity','lmax':lmax_I,'hnorm':hn_I})
print()

# ============================================================
# 5 HAAR RANDOM
# ============================================================
print("="*60); print("5 HAAR RANDOM"); print("="*60)
for trial in range(5):
    U=np.array([random_su2() for _ in range(n_links)])
    H=build_H(U,plaq_list,beta,N,n_links,n_gen)
    lm,_=lmax_and_vec(H)
    hn=lm/(48*beta)
    results.append({'type':'haar','trial':trial,'lmax':lm,'hnorm':hn})
    print(f"  Haar {trial}: lmax={lm:.6f}, H_norm={hn:.6f}")
print()

# ============================================================
# 5 GIBBS AT beta=0.1
# ============================================================
print("="*60); print("5 GIBBS (beta=0.1)"); print("="*60)
for trial in range(5):
    U=np.array([random_su2() for _ in range(n_links)])
    U,acc=gibbs_sample(U,plaq_list,0.1,N,n_links,n_steps=2000)
    H=build_H(U,plaq_list,beta,N,n_links,n_gen)
    lm,_=lmax_and_vec(H)
    hn=lm/(48*beta)
    results.append({'type':'gibbs','trial':trial,'lmax':lm,'hnorm':hn,'acc':acc})
    print(f"  Gibbs {trial}: lmax={lm:.6f}, H_norm={hn:.6f}, acc={acc:.2f}")
print()

# ============================================================
# 5 NEAR-IDENTITY (eps=0.1)
# ============================================================
print("="*60); print("5 NEAR-IDENTITY (eps=0.1)"); print("="*60)
for trial in range(5):
    U=np.array([su2_exp(0.1*sum(np.random.randn()*tau[a] for a in range(3)))
                for _ in range(n_links)])
    H=build_H(U,plaq_list,beta,N,n_links,n_gen)
    lm,_=lmax_and_vec(H)
    hn=lm/(48*beta)
    results.append({'type':'near_id','trial':trial,'lmax':lm,'hnorm':hn})
    print(f"  Near-I {trial}: lmax={lm:.6f}, H_norm={hn:.6f}")
print()

# ============================================================
# 5 ADVERSARIAL GRADIENT ASCENT (30 steps)
# ============================================================
print("="*60); print("5 ADVERSARIAL GRADIENT ASCENT (30 steps)"); print("="*60)

adv_starts=[
    ('random', lambda: np.array([random_su2() for _ in range(n_links)])),
    ('aligned_tau0', lambda: np.array([su2_exp(0.5*tau[0])]*n_links)),
    ('aligned_tau1', lambda: np.array([su2_exp(0.8*tau[1])]*n_links)),
    ('alternating_01', lambda: np.array([su2_exp(0.6*tau[0]) if i%2==0 else su2_exp(0.6*tau[1])
                                          for i in range(n_links)])),
    ('fixed_axis', lambda: np.array([su2_exp(np.pi/4*sum(
        np.array([1,1,1])[a]/np.sqrt(3)*tau[a] for a in range(3)))]*n_links)),
]

for trial,(name,init_fn) in enumerate(adv_starts):
    print(f"\n  Adv {trial} ({name}):")
    np.random.seed(trial*100+42)
    U=init_fn()
    best_hn=0.0; v_prev=None
    n_steps=30; step_size=0.005; t0_trial=time.time()

    for step in range(n_steps):
        H=build_H(U,plaq_list,beta,N,n_links,n_gen)
        lm,v=lmax_and_vec(H,v0=v_prev)
        v/=np.linalg.norm(v); v_prev=v.copy()
        hn=lm/(48*beta)
        if hn>best_hn: best_hn=hn

        grad=compute_grad(U,v,by_link,plaq_list,beta,N,n_links,n_gen)
        gm=grad.reshape(n_links,n_gen)
        for e in range(n_links):
            ge=gm[e]; ng=np.linalg.norm(ge)
            if ng<1e-10: continue
            U[e]=su2_exp(step_size/ng*sum(ge[a]*tau[a] for a in range(3)))@U[e]
        U=normalize_su2_arr(U)

        if step%10==0:
            print(f"    step {step}: H_norm={hn:.6f} (best={best_hn:.6f}) [{time.time()-t0_trial:.0f}s]")

    # Final eval — use accurate eigvalsh to avoid ARPACK tolerance artifacts
    H_f=build_H(U,plaq_list,beta,N,n_links,n_gen)
    lm_f=lmax_accurate(H_f)
    hn_f=lm_f/(48*beta)
    print(f"    FINAL: lmax={lm_f:.8f}, H_norm={hn_f:.8f}, best={best_hn:.6f}  [{time.time()-t0_trial:.0f}s]")
    results.append({'type':'adversarial','trial':trial,'name':name,
                    'lmax':lm_f,'hnorm':hn_f,'best_hnorm':best_hn})
    # Only flag if genuinely large (>0.001 above bound) — smaller could be eigsh artifact
    if hn_f>H_NORM_BOUND+0.001:
        print(f"  *** GENUINE VIOLATION: H_norm={hn_f:.8f} >> {H_NORM_BOUND:.8f} ***")
        sys.exit(2)
print()

# ============================================================
# SUMMARY
# ============================================================
print("="*60); print("TASK 1 (L=4) SUMMARY"); print("="*60)
all_hn=[r['hnorm'] for r in results]
max_hn=max(all_hn); max_r=results[all_hn.index(max_hn)]
print(f"\n  {'Type':<12} {'Trial':<8} {'lmax':>12} {'H_norm':>10} {'Status'}")
print(f"  {'-'*55}")
for r in results:
    st='VIOLATION!' if r['hnorm']>H_NORM_BOUND+1e-6 else 'ok'
    print(f"  {r['type']:<12} {str(r.get('trial','--')):<8} {r['lmax']:>12.6f} {r['hnorm']:>10.6f} {st}")
print(f"\n  Max H_norm:  {max_hn:.8f}  (type: {max_r['type']})")
print(f"  Bound 1/12:  {H_NORM_BOUND:.8f}")
print(f"  Margin:      {H_NORM_BOUND-max_hn:.8f}")
print(f"  ALL WITHIN:  {all(r['hnorm']<=H_NORM_BOUND+1e-6 for r in results)}")

with open(os.path.join(os.path.dirname(__file__),'task1_results.json'),'w') as f:
    json.dump({'L':L,'d':d,'beta':beta,'max_hnorm':max_hn,'results':results},f,indent=2)
print("  Saved task1_results.json")

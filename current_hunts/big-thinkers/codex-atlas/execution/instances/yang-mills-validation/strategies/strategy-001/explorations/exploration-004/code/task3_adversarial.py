"""
Task 3: Adversarial Gradient Ascent on lambda_max.
Run at L=2 (fast, 192 DOFs) for 500 steps from structured starts.
Verify best config on L=4.
"""
import sys, os, json, time
import numpy as np
import scipy.linalg as la
import scipy.sparse.linalg as spla
from itertools import product as iproduct

np.random.seed(77)

sigma=np.zeros((3,2,2),dtype=complex)
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
    by_link=[[] for _ in range(n_links)]
    for p in plaq_list:
        for pos,(lk,_) in enumerate(p): by_link[lk].append(p)
    return plaq_list,by_link,n_links

def build_H(U,plaq_list,beta,N,n_dof,n_links,n_gen):
    H=np.zeros((n_dof,n_dof)); pf=beta/(2*N)
    for plaq in plaq_list:
        ei=[plaq[k][0] for k in range(4)]; sg=[plaq[k][1] for k in range(4)]
        Us=[U[ei[k]] for k in range(4)]
        P1=np.eye(N,dtype=complex); P2=Us[0].copy()
        P3=Us[0]@Us[1]@Us[2].conj().T; P4=P3@Us[3].conj().T
        Rs=[adjoint_rep(P) for P in [P1,P2,P3,P4]]
        for i in range(4):
            for j in range(4):
                H[ei[i]*n_gen:(ei[i]+1)*n_gen,ei[j]*n_gen:(ei[j]+1)*n_gen]+=pf*sg[i]*sg[j]*Rs[i].T@Rs[j]
    return H

def lmax_and_vec(U,plaq_list,beta,N,n_links,n_gen,use_dense=True):
    n_dof=n_links*n_gen
    if use_dense:
        H=build_H(U,plaq_list,beta,N,n_dof,n_links,n_gen)
        evals,evecs=la.eigh(H)
        idx=np.argmax(evals)
        return evals[idx],evecs[:,idx]
    else:
        def mv(v):
            pf=beta/(2*N); r=np.zeros(n_dof); rm=r.reshape(n_links,n_gen); vm=v.reshape(n_links,n_gen)
            for plaq in plaq_list:
                ei=[plaq[k][0] for k in range(4)]; sg=[plaq[k][1] for k in range(4)]
                Us=[U[ei[k]] for k in range(4)]
                P1=np.eye(N,dtype=complex); P2=Us[0].copy()
                P3=Us[0]@Us[1]@Us[2].conj().T; P4=P3@Us[3].conj().T
                Rs=[adjoint_rep(P) for P in [P1,P2,P3,P4]]
                for i in range(4):
                    rm[ei[i]]+=pf*sg[i]*sum(sg[j]*Rs[i].T@(Rs[j]@vm[ei[j]]) for j in range(4))
            return r
        A=spla.LinearOperator((n_dof,n_dof),matvec=mv,dtype=float)
        vals,vecs=spla.eigsh(A,k=1,which='LM',tol=1e-8)
        return float(vals[0]),vecs[:,0]

def plaq_rq(vm,U,plaq,pf):
    ei=[plaq[k][0] for k in range(4)]; sg=[plaq[k][1] for k in range(4)]
    Us=[U[ei[k]] for k in range(4)]
    P1=np.eye(2,dtype=complex); P2=Us[0].copy()
    P3=Us[0]@Us[1]@Us[2].conj().T; P4=P3@Us[3].conj().T
    Rs=[adjoint_rep(P) for P in [P1,P2,P3,P4]]
    t=0.0
    for i in range(4):
        for j in range(4):
            t+=float(vm[ei[i]]@(pf*sg[i]*sg[j]*Rs[i].T@Rs[j])@vm[ei[j]])
    return t

def compute_grad(U,v,by_link,plaq_list,beta,N,n_links,n_gen,eps=5e-4):
    pf=beta/(2*N); vm=v.reshape(n_links,n_gen); grad=np.zeros((n_links,n_gen))
    for e in range(n_links):
        plaqs=by_link[e]
        if not plaqs: continue
        for a in range(n_gen):
            Up=U.copy(); Up[e]=su2_exp(eps*tau[a])@U[e]
            Um=U.copy(); Um[e]=su2_exp(-eps*tau[a])@U[e]
            rp=sum(plaq_rq(vm,Up,p,pf) for p in plaqs)
            rm2=sum(plaq_rq(vm,Um,p,pf) for p in plaqs)
            grad[e,a]=(rp-rm2)/(2*eps)
    return grad

def gradient_ascent(U_init, plaq_list, by_link, beta, N, n_links, n_gen, n_steps=500,
                    step_size=0.005, use_dense=True, label="", verbose=True):
    U=U_init.copy(); best_hn=0.0; history=[]
    pf=beta/(2*N)
    for step in range(n_steps):
        lmax,v=lmax_and_vec(U,plaq_list,beta,N,n_links,n_gen,use_dense)
        v/=np.linalg.norm(v)
        hn=lmax/(48*beta)
        if hn>best_hn: best_hn=hn; best_U=U.copy()
        history.append(hn)

        grad=compute_grad(U,v,by_link,plaq_list,beta,N,n_links,n_gen)
        gm=grad.reshape(n_links,n_gen)
        for e in range(n_links):
            ge=gm[e]; ng=np.linalg.norm(ge)
            if ng<1e-10: continue
            U[e]=su2_exp(step_size/ng*sum(ge[a]*tau[a] for a in range(3)))@U[e]
        U=normalize_su2_arr(U)

        if verbose and step%100==0:
            print(f"    [{label}] step {step}: H_norm={hn:.6f} (best={best_hn:.6f})")

    lmax_f,_=lmax_and_vec(U,plaq_list,beta,N,n_links,n_gen,use_dense)
    return lmax_f/(48*beta), best_hn, best_U, history

# ============================================================
# L=2 SETUP
# ============================================================
L2,d,N,beta=2,4,2,1.0
plaq2,by2,nl2=build_lattice(L2,d)
ng2=N**2-1; nd2=nl2*ng2
print(f"L=2 lattice: n_links={nl2}, n_dof={nd2}, n_plaq={len(plaq2)}")

# Sanity check at L=2
U_I=np.array([np.eye(2,dtype=complex)]*nl2)
lm,_=lmax_and_vec(U_I,plaq2,beta,N,nl2,ng2)
assert abs(lm-4*beta)<1e-4, f"L=2 sanity FAIL: {lm}"
print(f"L=2 sanity: lmax={lm:.6f} ✓")
print()

results=[]

# ============================================================
# STRUCTURED STARTS — 500 STEPS EACH
# ============================================================
print("="*60); print("ADVERSARIAL GRADIENT ASCENT (L=2, 500 steps)"); print("="*60)

adv_configs=[
    # (label, init_fn)
    ('random_1', lambda: np.array([random_su2() for _ in range(nl2)])),
    ('random_2', lambda: np.array([random_su2() for _ in range(nl2)])),
    ('aligned_tau0_0.5', lambda: np.array([su2_exp(0.5*tau[0])]*nl2)),
    ('aligned_tau2_1.0', lambda: np.array([su2_exp(1.0*tau[2])]*nl2)),
    ('alternating_01', lambda: np.array([su2_exp(0.7*tau[0]) if i%2==0 else su2_exp(0.7*tau[1])
                                          for i in range(nl2)])),
    ('alternating_02', lambda: np.array([su2_exp(0.7*tau[0]) if i%2==0 else su2_exp(0.7*tau[2])
                                          for i in range(nl2)])),
    ('fixed_axis_pi4', lambda: np.array([su2_exp(np.pi/4*sum(np.array([1,1,1])[a]/np.sqrt(3)*tau[a]
                                                              for a in range(3)))]*nl2)),
    ('near_minus_I', lambda: np.array([su2_exp(np.pi*tau[2]+0.1*sum(np.random.randn()*tau[a]
                                                                      for a in range(3)))
                                        for _ in range(nl2)])),
]

for label,init_fn in adv_configs:
    print(f"\n  === {label} ===")
    np.random.seed(hash(label)%10000)
    U0=init_fn()
    t0=time.time()
    hn_f,best_hn,best_U,hist=gradient_ascent(
        U0,plaq2,by2,beta,N,nl2,ng2,
        n_steps=500,step_size=0.005,use_dense=True,label=label
    )
    elapsed=time.time()-t0
    print(f"  Final H_norm={hn_f:.6f}, Best H_norm={best_hn:.6f}, Time={elapsed:.1f}s")
    print(f"  History: max={max(hist):.6f}, final={hist[-1]:.6f}")
    results.append({'label':label,'hn_final':hn_f,'hn_best':best_hn,'time':elapsed,
                    'hist_max':max(hist),'hist_final':hist[-1]})

# ============================================================
# VERIFY BEST CONFIG ON L=4
# ============================================================
print("\n"+"="*60)
print("VERIFY BEST CONFIG ON L=4")
print("="*60)

best_overall=max(results,key=lambda r:r['hn_best'])
print(f"  Best L=2 config: {best_overall['label']} with H_norm={best_overall['hn_best']:.6f}")

# Build L=4 lattice and test a few structured starts
L4,d,N,beta=4,4,2,1.0
plaq4,by4,nl4=build_lattice(L4,d)
ng4=N**2-1; nd4=nl4*ng4

print(f"\n  L=4 lattice: n_links={nl4}, n_dof={nd4}")

# Run short gradient ascent at L=4 from 3 structured starts
l4_configs=[
    ('aligned_tau0_0.5', np.array([su2_exp(0.5*tau[0])]*nl4)),
    ('alternating_01', np.array([su2_exp(0.7*tau[0]) if i%2==0 else su2_exp(0.7*tau[1])
                                  for i in range(nl4)])),
    ('random_L4', np.array([random_su2() for _ in range(nl4)])),
]

l4_results=[]
for label,U0 in l4_configs:
    print(f"\n  L=4 {label}:")
    t0=time.time()
    hn_f,best_hn,_,hist=gradient_ascent(
        U0,plaq4,by4,beta,N,nl4,ng4,
        n_steps=50,step_size=0.005,use_dense=False,label=f"L4_{label}",verbose=True
    )
    print(f"  Final H_norm={hn_f:.6f}, Best={best_hn:.6f}, Time={time.time()-t0:.1f}s")
    l4_results.append({'label':label,'hn_final':hn_f,'hn_best':best_hn})

# ============================================================
# SUMMARY
# ============================================================
print("\n"+"="*60); print("TASK 3 ADVERSARIAL SUMMARY"); print("="*60)
all_bests=[r['hn_best'] for r in results]
global_max=max(all_bests)
best_label=results[all_bests.index(global_max)]['label']
print(f"  L=2 configurations:")
for r in results:
    print(f"    {r['label']:<25} best={r['hn_best']:.6f}  final={r['hn_final']:.6f}")
print(f"\n  Global max H_norm (L=2): {global_max:.6f} (at {best_label})")
print(f"  Bound 1/12:              {1/12:.6f}")
print(f"  Margin:                  {1/12 - global_max:.6f}")
print(f"\n  L=4 adversarial results:")
for r in l4_results:
    print(f"    {r['label']:<25} best={r['hn_best']:.6f}  final={r['hn_final']:.6f}")

all_data={'L2_results':results,'L4_results':l4_results,'global_max_hnorm':global_max}
with open(os.path.join(os.path.dirname(__file__),'task3_results.json'),'w') as f:
    json.dump(all_data,f,indent=2)
print("  Saved task3_results.json")

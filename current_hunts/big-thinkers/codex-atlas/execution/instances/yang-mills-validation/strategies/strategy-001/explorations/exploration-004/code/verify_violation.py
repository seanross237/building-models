"""
Verify the potential violation at adv_2 (aligned_tau1 start).
Check if lmax truly exceeds 4*beta or if this is numerical artifact.
"""
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

L,d,N,beta=4,4,2,1.0
n_sites=L**d; n_links=d*n_sites; n_gen=N**2-1; n_dof=n_links*n_gen
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

def build_H(U):
    H=np.zeros((n_dof,n_dof)); pf=beta/(2*N)
    for plaq in plaq_list:
        ei=[plaq[k][0] for k in range(4)]; sg=[plaq[k][1] for k in range(4)]
        Us=[U[ei[k]] for k in range(4)]
        P2=Us[0].copy(); P3=Us[0]@Us[1]@Us[2].conj().T; P4=P3@Us[3].conj().T
        Rs=[adjoint_rep(P) for P in [np.eye(N,dtype=complex),P2,P3,P4]]
        for i in range(4):
            for j in range(4):
                H[ei[i]*n_gen:(ei[i]+1)*n_gen,ei[j]*n_gen:(ei[j]+1)*n_gen]+=pf*sg[i]*sg[j]*Rs[i].T@Rs[j]
    return H

def plaq_rq(vm,U,plaq,pf):
    ei=[plaq[k][0] for k in range(4)]; sg=[plaq[k][1] for k in range(4)]
    Us=[U[ei[k]] for k in range(4)]
    P2=Us[0].copy(); P3=Us[0]@Us[1]@Us[2].conj().T; P4=P3@Us[3].conj().T
    Rs=[adjoint_rep(P) for P in [np.eye(N,dtype=complex),P2,P3,P4]]
    t=0.0
    for i in range(4):
        for j in range(4): t+=float(vm[ei[i]]@(pf*sg[i]*sg[j]*Rs[i].T@Rs[j])@vm[ei[j]])
    return t

def compute_grad(U,v,eps=5e-4):
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

def lmax_and_vec_dense(H):
    A=spla.LinearOperator(H.shape,matvec=lambda v:H@v,dtype=float)
    vals,vecs=spla.eigsh(A,k=1,which='LM',tol=1e-10)
    return float(vals[0]),vecs[:,0]

def check_su2(U):
    """Check all matrices are in SU(2)."""
    max_det_err=max(abs(np.linalg.det(U[i])-1) for i in range(len(U)))
    max_unit_err=max(np.linalg.norm(U[i]@U[i].conj().T-np.eye(2)) for i in range(len(U)))
    return max_det_err, max_unit_err

print("="*60)
print("REPRODUCING VIOLATION: aligned_tau1 start at L=4")
print("="*60)
print()

# Reproduce the gradient ascent
U=np.array([su2_exp(0.8*tau[1])]*n_links)

# Check initial config
print("Initial config:")
det_err,unit_err=check_su2(U)
print(f"  Max det error: {det_err:.2e}, max unitarity error: {unit_err:.2e}")
H=build_H(U)
lm_init=float(np.max(la.eigvalsh(H)))
hn_init=lm_init/(48*beta)
print(f"  lmax={lm_init:.8f}, H_norm={hn_init:.8f} (expected 4.0 and 1/12)")

# Find top few eigenvalues (check degeneracy)
top_evals=np.sort(la.eigvalsh(H))[::-1][:20]
print(f"  Top 20 eigenvalues: {top_evals}")
n_max_evals=np.sum(np.abs(top_evals-top_evals[0])<1e-6)
print(f"  Degeneracy of lambda_max: {n_max_evals}")
print()

# Run 30 gradient steps and track carefully
n_steps=30; step_size=0.005; v_prev=None

history_lmax=[]
history_det_err=[]
history_unit_err=[]

for step in range(n_steps):
    H=build_H(U)
    A=spla.LinearOperator(H.shape,matvec=lambda v:H@v,dtype=float)
    kw={'tol':1e-9,'maxiter':1000}
    if v_prev is not None: kw['v0']=v_prev
    vals,vecs=spla.eigsh(A,k=1,which='LM',**kw)
    lm=float(vals[0]); v=vecs[:,0]; v/=np.linalg.norm(v); v_prev=v.copy()
    hn=lm/(48*beta)
    history_lmax.append(lm)

    det_err,unit_err=check_su2(U)
    history_det_err.append(det_err)
    history_unit_err.append(unit_err)

    grad=compute_grad(U,v)
    gm=grad.reshape(n_links,n_gen)
    for e in range(n_links):
        ge=gm[e]; ng=np.linalg.norm(ge)
        if ng<1e-10: continue
        U[e]=su2_exp(step_size/ng*sum(ge[a]*tau[a] for a in range(3)))@U[e]
    U=normalize_su2_arr(U)

    if step%5==0:
        print(f"  Step {step}: lmax={lm:.8f}, H_norm={hn:.8f}, det_err={det_err:.2e}, unit_err={unit_err:.2e}")

print()

# Final state check
H_f=build_H(U)
lm_f=float(np.max(la.eigvalsh(H_f)))
hn_f=lm_f/(48*beta)
det_err_f,unit_err_f=check_su2(U)
print(f"Final state:")
print(f"  lmax={lm_f:.8f}, H_norm={hn_f:.8f}")
print(f"  det_err={det_err_f:.2e}, unit_err={unit_err_f:.2e}")
print()

# ============================================================
# KEY QUESTION: Is the violation genuine?
# ============================================================
print("="*60)
print("VIOLATION ANALYSIS")
print("="*60)
print()

threshold=4*beta  # = 4.0
max_lmax=max(history_lmax)
step_max=history_lmax.index(max_lmax)
print(f"  Max lmax in trajectory: {max_lmax:.8f} at step {step_max}")
print(f"  Threshold (4*beta):     {threshold:.8f}")
print(f"  Excess:                 {max_lmax-threshold:.2e}")
print()

if max_lmax > threshold + 1e-4:
    print("  FINDING: lmax GENUINELY exceeds 4*beta (> 0.0001 excess)")
    print("  This could be a real violation of Conjecture 1!")
elif max_lmax > threshold + 1e-6:
    print("  FINDING: lmax BARELY exceeds 4*beta (1e-6 to 1e-4 excess)")
    print("  Could be numerical artifact — investigate further")
else:
    print("  FINDING: lmax is at or below 4*beta (within 1e-6)")
    print("  The earlier 'violation' was numerical noise")

# Check at maximum step
print()
print(f"  Max det error over trajectory: {max(history_det_err):.2e}")
print(f"  Max unit error over trajectory: {max(history_unit_err):.2e}")

# Extra check: what is the exact lmax at the step with maximum value?
print()
print("  Cross-checking with scipy.linalg.eigh (slower but more accurate):")
H_f=build_H(U)
all_evals=la.eigvalsh(H_f)
top5=np.sort(all_evals)[::-1][:5]
print(f"  Top 5 eigenvalues (eigvalsh): {top5}")
hn_top=top5[0]/(48*beta)
print(f"  lmax={top5[0]:.10f}, H_norm={hn_top:.10f}")
print(f"  Excess over 1/12: {hn_top - 1/12:.2e}")

print()
print("  FD check: what does lmax do near the final config?")
# Verify lmax by a few FD steps
eps_fd=1e-3
H_f=build_H(U)
lm_ref=float(np.max(la.eigvalsh(H_f)))
print(f"  Reference lmax at final U: {lm_ref:.8f}")
# Also check with a slightly perturbed U
for trial in range(3):
    U_pert=U.copy()
    for e in range(n_links):
        U_pert[e]=su2_exp(eps_fd*sum(np.random.randn()*tau[a] for a in range(3)))@U[e]
    U_pert=normalize_su2_arr(U_pert)
    H_p=build_H(U_pert)
    lm_p=float(np.max(la.eigvalsh(H_p)))
    print(f"  Randomly perturbed lmax: {lm_p:.8f} {'> bound!' if lm_p>4*beta+1e-6 else '<=bound'}")

"""
Task 4: Center Element Configurations.
Test U_all = exp(θ τ_a) for various θ and axes, plus center-adjacent elements.
"""
import sys, os, json, time
import numpy as np
import scipy.linalg as la
from itertools import product as iproduct

np.random.seed(42)

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
    t=np.sqrt(t2); return np.cos(t/2)*np.eye(2,dtype=complex)+(2/t)*np.sin(t/2)*M

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
    return plaq_list,n_links

def build_H(U,plaq_list,beta,N,n_links,n_gen):
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

def lmax(U,plaq_list,beta,N,n_links,n_gen):
    H=build_H(U,plaq_list,beta,N,n_links,n_gen)
    return float(np.max(la.eigvalsh(H)))

# Use L=2 for speed (results are L-independent for flat/uniform configs)
L,d,N,beta=2,4,2,1.0
plaq_list,n_links=build_lattice(L,d)
n_gen=N**2-1; H_NORM_BOUND=1/12
print(f"L={L} lattice for center configs: n_links={n_links}")

results=[]

# ============================================================
# THETA SWEEP: U_all = exp(θ τ_1)
# ============================================================
print("\n"+"="*60)
print("SWEEP: U_all = exp(θ τ_1)")
print("="*60)
thetas=[0.0, 0.1, 0.3, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, np.pi]
for theta in thetas:
    g=su2_exp(theta*tau[0])
    U=np.array([g]*n_links)
    # Verify plaquette
    plaq=plaq_list[0]; ei=[plaq[k][0] for k in range(4)]
    Up=U[ei[0]]@U[ei[1]]@U[ei[2]].conj().T@U[ei[3]].conj().T
    reTr=np.real(np.trace(Up))
    lm=lmax(U,plaq_list,beta,N,n_links,n_gen)
    hn=lm/(48*beta)
    print(f"  θ={theta:.3f}: U=exp({theta:.3f}τ₁), Re Tr(U_plaq)={reTr:.4f}, lmax={lm:.6f}, H_norm={hn:.6f}")
    results.append({'theta':theta,'axis':0,'lmax':lm,'hnorm':hn,'reTr_plaq':reTr})

# ============================================================
# GOAL-SPECIFIED: exp((π/4)τ₁) and exp(πτ₁) = iσ₁
# ============================================================
print("\n"+"="*60)
print("GOAL-SPECIFIED CENTER CONFIGS")
print("="*60)
center_configs=[
    ('exp(π/4 τ₁)', su2_exp(np.pi/4*tau[0])),
    ('exp(π/2 τ₁)', su2_exp(np.pi/2*tau[0])),
    ('exp(π τ₁) = iσ₁', su2_exp(np.pi*tau[0])),
    ('iσ₁', np.array([[0,1j],[1j,0]],dtype=complex)),
    ('iσ₂', np.array([[0,1],[-1,0]],dtype=complex)),
    ('iσ₃ (from E003)', np.array([[1j,0],[0,-1j]],dtype=complex)),
    ('-I (center)', -np.eye(2,dtype=complex)),
    ('+I (identity)', np.eye(2,dtype=complex)),
]
for name,g in center_configs:
    # Check it's in SU(2)
    det=np.linalg.det(g)
    U=np.array([g]*n_links)
    # Verify plaquette trivial for uniform config
    plaq=plaq_list[0]; ei=[plaq[k][0] for k in range(4)]
    Up=U[ei[0]]@U[ei[1]]@U[ei[2]].conj().T@U[ei[3]].conj().T
    reTr=np.real(np.trace(Up))
    lm=lmax(U,plaq_list,beta,N,n_links,n_gen)
    hn=lm/(48*beta)
    print(f"  {name:<22}: det={det:.4f}, Re Tr(U_plaq)={reTr:.4f}, lmax={lm:.6f}, H_norm={hn:.6f}")
    results.append({'name':name,'lmax':lm,'hnorm':hn,'reTr_plaq':reTr,'det':np.real(det)})

# ============================================================
# MIXED PLAQUETTE CONFIGS: some links at exp(θτ₁), others at -exp(θτ₁)
# ============================================================
print("\n"+"="*60)
print("MIXED CONFIGS: +/- uniform")
print("="*60)
for theta in [np.pi/4, np.pi/2, np.pi]:
    g_p=su2_exp(theta*tau[0]); g_m=-g_p  # g_m ∈ SU(2) since det=1
    U=np.array([g_p if i%2==0 else g_m for i in range(n_links)])
    lm=lmax(U,plaq_list,beta,N,n_links,n_gen)
    hn=lm/(48*beta)
    print(f"  θ={theta:.4f} mixed +/-: lmax={lm:.6f}, H_norm={hn:.6f}")
    results.append({'name':f'mixed_pm_theta{theta:.3f}','lmax':lm,'hnorm':hn})

# ============================================================
# 2D CENTER TWIST: Z2 twisted boundary conditions
# ============================================================
print("\n"+"="*60)
print("Z2 TWIST CONFIGURATION")
print("="*60)
# Set all links in mu=0 direction to -I, all others to I
U=np.array([np.eye(2,dtype=complex)]*n_links)
for e in range(n_links):
    # Mu=0 links have index (site_idx * d + 0) % d == 0
    if e % d == 0:
        U[e] = -np.eye(2,dtype=complex)
lm=lmax(U,plaq_list,beta,N,n_links,n_gen)
hn=lm/(48*beta)
print(f"  Z2 twist (μ=0 links = -I, others = I): lmax={lm:.6f}, H_norm={hn:.6f}")
results.append({'name':'Z2_twist_mu0','lmax':lm,'hnorm':hn})

# ============================================================
# THETA SWEEP: check if max is near a specific theta
# ============================================================
print("\n"+"="*60)
print("FINE THETA SWEEP AROUND MAX H_NORM")
print("="*60)
all_hnorms=[r['hnorm'] for r in results if 'theta' in r]
if all_hnorms:
    max_hn_theta=max(all_hnorms)
    max_theta=[r for r in results if 'theta' in r and r['hnorm']==max_hn_theta][0]['theta']
    print(f"  Max H_norm in theta sweep: {max_hn_theta:.6f} at θ={max_theta:.3f}")
    # Fine sweep around max_theta
    if max_theta > 0:
        fine_thetas=np.linspace(max(0,max_theta-0.3), min(np.pi,max_theta+0.3), 15)
        for theta in fine_thetas:
            g=su2_exp(theta*tau[0])
            U=np.array([g]*n_links)
            lm=lmax(U,plaq_list,beta,N,n_links,n_gen)
            hn=lm/(48*beta)
            print(f"  fine θ={theta:.4f}: H_norm={hn:.6f}")
            results.append({'theta_fine':theta,'lmax':lm,'hnorm':hn})

# ============================================================
# SUMMARY
# ============================================================
print("\n"+"="*60); print("TASK 4 SUMMARY"); print("="*60)
max_hn=max(r['hnorm'] for r in results)
print(f"  Max H_norm: {max_hn:.8f}")
print(f"  Bound 1/12: {H_NORM_BOUND:.8f}")
print(f"  Margin:     {H_NORM_BOUND-max_hn:.8f}")
print(f"  ALL OK:     {all(r['hnorm']<=H_NORM_BOUND+1e-6 for r in results)}")

with open(os.path.join(os.path.dirname(__file__),'task4_results.json'),'w') as f:
    json.dump({'L':L,'d':d,'max_hnorm':max_hn,'results':results},f,indent=2)
print("  Saved task4_results.json")

"""
fast_gradient_ascent.py — Efficient gradient ascent for H_norm maximization.
L=4, d=4, SU(2). Uses numerical gradient via partial Hessian quadratic form.

Key speed-up: instead of rebuilding the full 3072x3072 Hessian,
compute v^T H_P v for individual plaquettes using numpy vectorization.
Gradient: d(v^T H v)/d(eps^c_l) ≈ sum_{P∋l} [vT_HP_v(Q_pert) - vT_HP_v(Q)] / eps

This is O(n_links * n_gen * 6 plaquettes * fast_eval) per gradient step.
"""
import numpy as np
import json
import time
import sys

# ===== Setup (same as hessian_l4.py) =====
L=4; d=4; N_SU=2; beta=1.0
n_sites=L**d; n_links=n_sites*d; n_gen=3; n_dof=n_links*n_gen
HNORM_CONJ=1.0/12; LAMBDA_NORM=48.0*beta; beta_N=beta/N_SU

sigma=np.zeros((3,2,2),dtype=complex)
sigma[0]=[[0,1],[1,0]]; sigma[1]=[[0,-1j],[1j,0]]; sigma[2]=[[1,0],[0,-1]]
tau=1j*sigma/2; I2=np.eye(2,dtype=complex)

def site_to_idx(x):
    idx=0
    for i in range(d): idx=idx*L+x[i]
    return idx
def idx_to_site(idx):
    x=[]
    for i in range(d): x.append(idx%L); idx//=L
    return tuple(reversed(x))
def link_idx(si,mu): return si*d+mu
def add_dir(site,mu):
    x=list(site); x[mu]=(x[mu]+1)%L; return tuple(x)

plaquettes=[]
for x_idx in range(n_sites):
    x=idx_to_site(x_idx)
    for mu in range(d):
        for nu in range(mu+1,d):
            x_mu=add_dir(x,mu); x_nu=add_dir(x,nu)
            l0=link_idx(site_to_idx(x),mu); l1=link_idx(site_to_idx(x_mu),nu)
            l2=link_idx(site_to_idx(x_nu),mu); l3=link_idx(site_to_idx(x),nu)
            plaquettes.append([(l0,+1),(l1,+1),(l2,-1),(l3,-1)])
n_plaq=len(plaquettes)

link_to_plaqs=[[] for _ in range(n_links)]
for p_idx,plaq in enumerate(plaquettes):
    for pos,(l,s) in enumerate(plaq):
        link_to_plaqs[l].append((p_idx,pos))

def random_su2():
    q=np.random.randn(4); q/=np.linalg.norm(q)
    return q[0]*I2+1j*(q[1]*sigma[0]+q[2]*sigma[1]+q[3]*sigma[2])
def su2_dagger(U): return U.conj().T
def su2_exp(c):
    A=c[0]*tau[0]+c[1]*tau[1]+c[2]*tau[2]
    cs=float(np.real(c[0]**2+c[1]**2+c[2]**2))
    if cs<1e-30: return I2+A
    th=np.sqrt(cs)
    return np.cos(th/2)*I2+(np.sin(th/2)/(th/2))*A

def plaq_product(Q,plaq):
    r=I2.copy()
    for l,s in plaq: r=r@(Q[l] if s==+1 else su2_dagger(Q[l]))
    return r

def config_identity():
    Q=np.zeros((n_links,2,2),dtype=complex)
    for l in range(n_links): Q[l]=I2.copy()
    return Q
def config_random():
    Q=np.zeros((n_links,2,2),dtype=complex)
    for l in range(n_links): Q[l]=random_su2()
    return Q
def config_perturbed(eps):
    Q=np.zeros((n_links,2,2),dtype=complex)
    for l in range(n_links): Q[l]=su2_exp(eps*np.random.randn(3))
    return Q

# ===== Fast plaquette quadratic form =====
def vT_HP_v(Q, v, p_idx):
    """
    Compute v^T H_P v for plaquette p_idx.
    Uses numpy einsum for the 3x3 trace matrix.
    """
    plaq=plaquettes[p_idx]
    link_ids=[l for l,s in plaq]
    signs=[s for l,s in plaq]
    W=np.array([Q[l] if s==+1 else su2_dagger(Q[l]) for l,s in plaq])
    
    # Prefix products (5 matrices: L[0]=I, L[k+1]=L[k]@W[k])
    L=np.zeros((5,2,2),dtype=complex); L[0]=I2
    for k in range(4): L[k+1]=L[k]@W[k]
    # Suffix products (4 matrices: R[3]=I, R[k]=W[k+1]@R[k+1])
    R=np.zeros((4,2,2),dtype=complex); R[3]=I2
    for k in range(2,-1,-1): R[k]=W[k+1]@R[k+1]
    
    retr=np.real(np.trace(L[4]))
    
    # V[k,a] = v component for link k, generator a
    V=np.array([[v[link_ids[k]*n_gen+a] for a in range(n_gen)] for k in range(4)])
    
    # Diagonal: (beta_N/4)*retr * sum_{k,a} V[k,a]^2
    result=(beta_N/4)*retr*np.sum(V**2)
    
    # Off-diagonal: k < m
    for k in range(4):
        sk=signs[k]
        # Middle products M[k,m] for all m>k
        M=I2.copy()  # M[k,k+1] = I (no factors between k and k+1)
        # We need M_{km} = W[k+1]...W[m-1]
        # For m=k+1: M=I; m=k+2: M=W[k+1]; m=k+3: M=W[k+1]@W[k+2]
        for m in range(k+1,4):
            sm=signs[m]
            if m>k+1: M=M@W[m-1]  # Accumulate: M_{km} = M_{k,m-1} @ W[m-1]
            # But M here is M_{k,m} = W[k+1]...W[m-1]
            # Actually we want: M_km = W[k+1]...W[m-1]
            # For m=k+1: M_km = I (already set)
            # For m=k+2: M_km = W[k+1]
            # For m=k+3: M_km = W[k+1]@W[k+2]
            
            # Precompute LAM[a] = L[k] @ Ak[a] @ M_km  (shape: 3 x 2 x 2)
            LAM=np.zeros((n_gen,2,2),dtype=complex)
            for a in range(n_gen):
                Ak=(W[k]@tau[a]) if sk==+1 else (-tau[a]@W[k])
                LAM[a]=L[k]@Ak@M
            # Precompute AR[b] = Am[b] @ R[m]  (shape: 3 x 2 x 2)
            AR=np.zeros((n_gen,2,2),dtype=complex)
            for b in range(n_gen):
                Am=(W[m]@tau[b]) if sm==+1 else (-tau[b]@W[m])
                AR[b]=Am@R[m]
            # Trace matrix: Tr[a,b] = Re Tr(LAM[a] @ AR[b])
            # LAM: (3,2,2), AR: (3,2,2)
            # LAM[a]@AR[b] = einsum('aij,bjk->abik', LAM, AR)... then trace
            # Faster: Tr(A@B) = sum_{ij} A_{ij} B_{ji}
            Tr_mat=np.real(np.einsum('aij,bji->ab', LAM, AR))
            # Contribution: -2*beta_N * V[k] @ Tr_mat @ V[m]
            result += -2*beta_N * np.dot(V[k], Tr_mat @ V[m])
    
    return result

# Fix the M_km accumulation issue above:
def vT_HP_v_correct(Q, v, p_idx):
    """Correct version with proper M_km."""
    plaq=plaquettes[p_idx]
    link_ids=[l for l,s in plaq]
    signs=[s for l,s in plaq]
    W=np.array([Q[l] if s==+1 else su2_dagger(Q[l]) for l,s in plaq])
    L=np.zeros((5,2,2),dtype=complex); L[0]=I2
    for k in range(4): L[k+1]=L[k]@W[k]
    R=np.zeros((4,2,2),dtype=complex); R[3]=I2
    for k in range(2,-1,-1): R[k]=W[k+1]@R[k+1]
    retr=np.real(np.trace(L[4]))
    V=np.array([[v[link_ids[k]*n_gen+a] for a in range(n_gen)] for k in range(4)])
    result=(beta_N/4)*retr*np.sum(V**2)
    for k in range(4):
        sk=signs[k]
        for m in range(k+1,4):
            sm=signs[m]
            # M_km = W[k+1] @ ... @ W[m-1]
            M_km=I2.copy()
            for j in range(k+1,m): M_km=M_km@W[j]
            LAM=np.zeros((n_gen,2,2),dtype=complex)
            for a in range(n_gen):
                Ak=(W[k]@tau[a]) if sk==+1 else (-tau[a]@W[k])
                LAM[a]=L[k]@Ak@M_km
            AR=np.zeros((n_gen,2,2),dtype=complex)
            for b in range(n_gen):
                Am=(W[m]@tau[b]) if sm==+1 else (-tau[b]@W[m])
                AR[b]=Am@R[m]
            Tr_mat=np.real(np.einsum('aij,bji->ab', LAM, AR))
            result += -2*beta_N * np.dot(V[k], Tr_mat @ V[m])
    return result

# ===== Full Hessian for power iteration =====
def compute_hessian(Q):
    H=np.zeros((n_dof,n_dof))
    for plaq in plaquettes:
        W=np.zeros((4,2,2),dtype=complex); link_ids=np.zeros(4,dtype=int); signs=np.zeros(4,dtype=int)
        for k,(l,s) in enumerate(plaq):
            link_ids[k]=l; signs[k]=s; W[k]=Q[l] if s==+1 else su2_dagger(Q[l])
        L=np.zeros((5,2,2),dtype=complex); L[0]=I2
        for k in range(4): L[k+1]=L[k]@W[k]
        R=np.zeros((4,2,2),dtype=complex); R[3]=I2
        for k in range(2,-1,-1): R[k]=W[k+1]@R[k+1]
        dv=(beta_N/4)*np.real(np.trace(L[4]))
        for k in range(4):
            lk=link_ids[k]
            for a in range(n_gen): H[lk*n_gen+a,lk*n_gen+a]+=dv
        for k in range(4):
            lk=link_ids[k]; sk=signs[k]
            for m in range(k+1,4):
                lm=link_ids[m]; sm=signs[m]
                M=I2.copy()
                for j in range(k+1,m): M=M@W[j]
                for a in range(n_gen):
                    Ak=(W[k]@tau[a]) if sk==+1 else (-tau[a]@W[k])
                    LAM=L[k]@Ak@M
                    for b in range(n_gen):
                        Am=(W[m]@tau[b]) if sm==+1 else (-tau[b]@W[m])
                        val=np.real(np.trace(LAM@Am@R[m]))
                        H[lk*n_gen+a,lm*n_gen+b]+=-beta_N*val
                        H[lm*n_gen+b,lk*n_gen+a]+=-beta_N*val
    return H

def power_iteration(H, n_iter=150):
    w=np.random.randn(n_dof); w/=np.linalg.norm(w)
    for _ in range(n_iter):
        Hw=H@w; lam=float(w@Hw); w=Hw/np.linalg.norm(Hw)
    Hw=H@w; lam=float(w@Hw)
    res=np.linalg.norm(Hw-lam*w)/(abs(lam)+1e-30)
    return lam, w, res

# ===== Numerical gradient via partial Hessian quadratic forms =====
EPS_GRAD = 5e-4  # step size for numerical gradient

def compute_fast_gradient(Q, v_max):
    """
    Compute gradient of lambda_max(H(Q)) w.r.t. each link,
    using numerical differentiation of v^T H v via partial plaquette evaluation.
    
    d(lambda_max)/d(eps^c_l) ≈ sum_{P∋l} [vT_HP_v(Q_pert) - vT_HP_v(Q)] / eps
    """
    # Pre-compute baseline plaquette quadratic forms
    baseline = np.array([vT_HP_v_correct(Q, v_max, p) for p in range(n_plaq)])
    
    grad = np.zeros((n_links, n_gen))
    
    for l in range(n_links):
        Q_pert = Q.copy()
        for c in range(n_gen):
            # Perturb link l by eps in direction tau_c
            pert_c = np.zeros(3); pert_c[c] = EPS_GRAD
            Q_pert[l] = Q[l] @ su2_exp(pert_c)
            
            # Recompute v^T H_P v for the 6 plaquettes containing l
            delta_f = 0.0
            for (p_idx, pos) in link_to_plaqs[l]:
                f_new = vT_HP_v_correct(Q_pert, v_max, p_idx)
                delta_f += f_new - baseline[p_idx]
            
            grad[l, c] = delta_f / EPS_GRAD
            
            # Reset
            Q_pert[l] = Q[l]
    
    return grad

# ===== Main gradient ascent =====
print(f"L={L}, d={d}, SU(2): fast gradient ascent")
print(f"n_links={n_links}, n_dof={n_dof}, n_plaq={n_plaq}")
print()

# Quick timing test
np.random.seed(77)
Q_test = config_random()
H_test = compute_hessian(Q_test)
lam_test, v_test, _ = power_iteration(H_test)

print("Timing: vT_HP_v for one plaquette...")
t0=time.time()
for p in range(10): vT_HP_v_correct(Q_test, v_test, p)
t1=time.time()
print(f"  Per plaquette: {(t1-t0)/10*1000:.2f}ms")

print("Timing: gradient computation (1 step)...")
t2=time.time()
g_test = compute_fast_gradient(Q_test, v_test)
t3=time.time()
print(f"  Gradient time: {t3-t2:.2f}s")
print(f"  Gradient norm: {np.linalg.norm(g_test):.4f}")
print()

# Estimate total time
hess_time = 1.8
pi_time = 0.7
grad_time = t3 - t2
N_STEPS = 30
N_CONFIGS = 5
total_est = N_CONFIGS * N_STEPS * (hess_time + pi_time + grad_time)
print(f"Estimated total time: {N_CONFIGS} configs x {N_STEPS} steps x {hess_time+pi_time+grad_time:.1f}s = {total_est:.0f}s")
print()

# Starting configs
np.random.seed(234)
starting_configs = [
    ("random_1", config_random()),
    ("random_2", config_random()),
    ("perturbed_0.5", config_perturbed(0.5)),
    ("perturbed_0.1", config_perturbed(0.1)),
    ("identity", config_identity()),
]

STEP_SIZES = [0.02 * (0.97**i) for i in range(N_STEPS)]

all_results = []
global_max_hnorm = 0.0

for run_name, Q0 in starting_configs:
    print(f"\n{'='*55}")
    print(f"Gradient ascent run: {run_name}")
    print(f"{'='*55}")
    
    Q = Q0.copy()
    
    # Initial state
    H = compute_hessian(Q)
    lam, v_max, res = power_iteration(H)
    hnorm = lam / LAMBDA_NORM
    print(f"  Step 0: lam={lam:.6f}, H_norm={hnorm:.8f}, res={res:.2e}")
    
    if hnorm > HNORM_CONJ:
        print(f"  *** COUNTEREXAMPLE AT START: H_norm={hnorm:.6f} > 1/12 ***")
    
    traj = [{"step":0,"lam":float(lam),"hnorm":float(hnorm),"grad_norm":0.0}]
    max_hnorm = hnorm
    max_at_step = 0
    
    for step in range(N_STEPS):
        alpha = STEP_SIZES[step]
        
        # Compute gradient
        t_g0 = time.time()
        grad = compute_fast_gradient(Q, v_max)
        t_g1 = time.time()
        grad_norm = float(np.linalg.norm(grad))
        
        # Take Riemannian gradient ascent step
        Q_new = Q.copy()
        for l in range(n_links):
            Q_new[l] = Q[l] @ su2_exp(alpha * grad[l])
        Q = Q_new
        
        # Recompute Hessian and eigenvector
        H = compute_hessian(Q)
        lam, v_max, res = power_iteration(H)
        hnorm = lam / LAMBDA_NORM
        
        if hnorm > max_hnorm:
            max_hnorm = hnorm
            max_at_step = step + 1
        if hnorm > global_max_hnorm:
            global_max_hnorm = hnorm
        
        traj.append({"step":step+1,"lam":float(lam),"hnorm":float(hnorm),"grad_norm":grad_norm})
        
        if step % 5 == 0 or step < 5:
            print(f"  Step {step+1:3d}: alpha={alpha:.4f}, lam={lam:.6f}, "
                  f"H_norm={hnorm:.8f}, grad_norm={grad_norm:.4f}, "
                  f"grad_t={t_g1-t_g0:.1f}s")
        
        if hnorm > HNORM_CONJ:
            print(f"  *** COUNTEREXAMPLE at step {step+1}: H_norm={hnorm:.8f} > 1/12 ***")
    
    print(f"\n  Final: lam={lam:.6f}, H_norm={hnorm:.8f}")
    print(f"  Max H_norm: {max_hnorm:.8f} (at step {max_at_step})")
    print(f"  Counterexample: {max_hnorm > HNORM_CONJ}")
    
    all_results.append({
        "run_name": run_name,
        "initial_hnorm": float(traj[0]["hnorm"]),
        "final_hnorm": float(hnorm),
        "max_hnorm": float(max_hnorm),
        "max_at_step": max_at_step,
        "counterexample": bool(max_hnorm > HNORM_CONJ),
        "n_steps": N_STEPS,
        "trajectory": traj,
    })

print("\n" + "="*60)
print("GRADIENT ASCENT SUMMARY")
print("="*60)
for r in all_results:
    print(f"  {r['run_name']:25s}: max_H_norm={r['max_hnorm']:.8f}, final={r['final_hnorm']:.8f}, CE={r['counterexample']}")

any_ce = any(r["counterexample"] for r in all_results)
print(f"\nGlobal max H_norm: {global_max_hnorm:.8f} (bound: {HNORM_CONJ:.8f})")
print(f"Any counterexample: {any_ce}")
print(f"Conjecture H_norm <= 1/12: {'VIOLATED' if any_ce else 'HOLDS'}")

out = {
    "L": L, "d": d, "beta": beta,
    "n_steps": N_STEPS,
    "eps_grad": EPS_GRAD,
    "runs": all_results,
    "global_max_hnorm": float(global_max_hnorm),
    "any_counterexample": bool(any_ce),
    "conjecture_holds": not any_ce,
}
out_path = ("/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/"
            "instances/yang-mills/strategies/strategy-003/explorations/exploration-004/"
            "code/fast_gradient_results.json")
with open(out_path, "w") as f:
    json.dump(out, f, indent=2)
print(f"\nResults saved to {out_path}")
print("fast_gradient_ascent.py DONE")

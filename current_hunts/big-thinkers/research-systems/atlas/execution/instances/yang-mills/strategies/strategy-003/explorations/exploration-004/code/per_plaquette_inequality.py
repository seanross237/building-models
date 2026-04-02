"""
per_plaquette_inequality.py

Test: H_P(Q, v) <= (beta/(2N)) * |B_P(Q, v)|^2 for each plaquette P.

This is the KEY open inequality needed to complete the proof chain.

For each configuration Q and each test vector v:
  - Compute H_P(v) = v^T H_P v for each plaquette P
  - Compute BP_sq = |B_P(Q, v)|^2
  - Check: H_P(v) <= (beta/(2N)) * BP_sq?
  - Compute ratio: H_P(v) / [(beta/(2N)) * BP_sq] when BP_sq > 0

If ratio ever exceeds 1, the conjecture is violated.
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

plaquettes=[]
for xi in range(n_sites):
    x=idx_to_site(xi)
    for mu in range(d):
        for nu in range(mu+1,d):
            xm=add_dir(x,mu); xn=add_dir(x,nu)
            l0=site_to_idx(x)*d+mu; l1=site_to_idx(xm)*d+nu
            l2=site_to_idx(xn)*d+mu; l3=site_to_idx(x)*d+nu
            plaquettes.append([(l0,+1),(l1,+1),(l2,-1),(l3,-1)])

def compute_HP(Q, plaq, v):
    """Compute v^T H_P v for one plaquette."""
    W=[Q[l] if s==+1 else su2d(Q[l]) for (l,s) in plaq]
    lids=[l for (l,s) in plaq]; sgns=[s for (l,s) in plaq]
    Lp=[I2.copy()]
    for k in range(4): Lp.append(Lp[-1]@W[k])
    UP=Lp[4]; rtr=np.real(np.trace(UP))
    Rs=[None]*4; Rs[3]=I2.copy()
    for k in range(2,-1,-1): Rs[k]=W[k+1]@Rs[k+1]
    result=0.0
    dv=(bN/4)*rtr
    for k in range(4):
        for a in range(n_gen): result+=dv*v[lids[k]*n_gen+a]**2
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

def compute_BP_sq(Q, plaq, v_flat):
    """Compute |B_P(Q,v)|^2 using parallel transport."""
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
    return -2.0*np.real(np.trace(B_P@B_P))

print("Per-plaquette inequality test: H_P(v) <= (beta/2N) * |B_P|^2")
print(f"Coefficient: beta/(2N) = {bN/2}")
print()

# Test configurations
configs = {}
Q_I=np.zeros((n_links,2,2),dtype=complex)
for l in range(n_links): Q_I[l]=I2.copy()
configs['Q=I'] = Q_I

np.random.seed(7)
Q_eps=np.zeros((n_links,2,2),dtype=complex)
for l in range(n_links): Q_eps[l]=Q_I[l]@su2_exp(0.1*np.random.randn(3))
configs['near-id eps=0.1'] = Q_eps

np.random.seed(13)
Q_g=np.zeros((n_links,2,2),dtype=complex)
for l in range(n_links): Q_g[l]=Q_I[l]@su2_exp(0.5*np.random.randn(3))
configs['warm start eps=0.5'] = Q_g

np.random.seed(21)
Q_r1=np.zeros((n_links,2,2),dtype=complex)
for l in range(n_links): Q_r1[l]=random_su2()
configs['random Haar'] = Q_r1

# For each config, test with multiple v vectors
n_v_per_config = 5
np.random.seed(42)
results = []

for config_name, Q in configs.items():
    print(f"Config: {config_name}")
    
    # Test vectors: v_max (from Mode C for Q=I), random vectors, and a few more
    test_vectors = {}
    
    # Mode C at Q=I
    v_C = np.zeros(n_dof)
    for l in range(n_links):
        x=idx_to_site(l//d); mu=l%d
        v_C[l*n_gen+0] = (-1)**(sum(x)+mu)
    v_C /= np.linalg.norm(v_C)
    test_vectors['Mode_C'] = v_C
    
    # Random unit vectors
    for i in range(4):
        v = np.random.randn(n_dof); v /= np.linalg.norm(v)
        test_vectors[f'random_{i}'] = v
    
    for v_name, v in test_vectors.items():
        max_ratio = 0.0
        n_violated = 0
        n_plaq_tested = 0
        sum_HP = 0.0
        sum_bBP = 0.0
        
        for pi, plaq in enumerate(plaquettes):
            HP = compute_HP(Q, plaq, v)
            BP_sq = compute_BP_sq(Q, plaq, v)
            bBP = (bN/2) * BP_sq
            
            n_plaq_tested += 1
            sum_HP += HP
            sum_bBP += bBP
            
            if BP_sq > 1e-10:
                ratio = HP / bBP
                if ratio > max_ratio: max_ratio = ratio
                if ratio > 1 + 1e-6: n_violated += 1
        
        viol_str = "VIOLATED!" if n_violated > 0 else "✓"
        print(f"  v={v_name:12s}: max ratio={max_ratio:.6f}, violations={n_violated}/{n_plaq_tested}, "
              f"sum_HP={sum_HP:.6f}, sum_bBP={sum_bBP:.6f} {viol_str}")
        results.append({
            'config': config_name, 'v': v_name, 'max_ratio': float(max_ratio),
            'n_violated': int(n_violated), 'n_plaq': n_plaq_tested,
            'sum_HP': float(sum_HP), 'sum_bBP': float(sum_bBP)
        })
    print()

print("="*60)
all_max_ratio = max(r['max_ratio'] for r in results)
all_violated = sum(r['n_violated'] for r in results)
print(f"OVERALL: max ratio = {all_max_ratio:.6f} (bound = 1.0)")
print(f"OVERALL: total violations = {all_violated}")
print(f"Inequality H_P <= (beta/2N)|B_P|^2 holds: {all_violated == 0}")

with open('/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/yang-mills/strategies/strategy-003/explorations/exploration-004/code/per_plaquette_results.json','w') as f:
    json.dump({'max_ratio': all_max_ratio, 'total_violations': all_violated, 'results': results}, f, indent=2)
print("Saved to per_plaquette_results.json")
print("DONE")

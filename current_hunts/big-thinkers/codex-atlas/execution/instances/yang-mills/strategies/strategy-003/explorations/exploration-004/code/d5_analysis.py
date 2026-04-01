"""
d5_analysis.py — d=5 anomaly investigation.

At d=5, E009 found lambda_max at Q=I is 5*beta (not 4*beta as for d=4).
This script finds the maximum eigenvector, compares with staggered mode,
and computes H_norm_max(d=5).

L=2, d=5, SU(2): 2^5=32 sites, 160 links, 3*160=480 DOFs.
"""
import numpy as np

d5=5; L5=2; N_SU=2; beta=1.0
n_sites5=L5**d5; n_links5=n_sites5*d5; n_gen=3; n_dof5=n_links5*n_gen
beta_N=beta/N_SU

sigma=np.zeros((3,2,2),dtype=complex)
sigma[0]=[[0,1],[1,0]]; sigma[1]=[[0,-1j],[1j,0]]; sigma[2]=[[1,0],[0,-1]]
tau=1j*sigma/2; I2=np.eye(2,dtype=complex)

def site_to_idx5(x):
    idx=0
    for i in range(d5): idx=idx*L5+x[i]
    return idx
def idx_to_site5(idx):
    x=[]
    for i in range(d5): x.append(idx%L5); idx//=L5
    return tuple(reversed(x))
def link_idx5(si,mu): return si*d5+mu
def add_dir5(site,mu):
    x=list(site); x[mu]=(x[mu]+1)%L5; return tuple(x)

plaq5=[]
for x_idx in range(n_sites5):
    x=idx_to_site5(x_idx)
    for mu in range(d5):
        for nu in range(mu+1,d5):
            xm=add_dir5(x,mu); xn=add_dir5(x,nu)
            l0=link_idx5(site_to_idx5(x),mu); l1=link_idx5(site_to_idx5(xm),nu)
            l2=link_idx5(site_to_idx5(xn),mu); l3=link_idx5(site_to_idx5(x),nu)
            plaq5.append([(l0,+1),(l1,+1),(l2,-1),(l3,-1)])
n_plaq5=len(plaq5)
print(f"d=5: n_sites={n_sites5}, n_links={n_links5}, n_dof={n_dof5}, n_plaq={n_plaq5}")

# Build Hessian at Q=I for d=5 (using the simple K⊗I_3 structure)
# At Q=I: H[li a, lj b] = delta_{ab} * K[li,lj]
# K[li,lj] = sum_{plaq containing both li,lj} (beta/2)*sign_li*sign_lj
# K[li,li] = 2*(d-1) * (beta/2) = (d-1)*beta  [per generator]
# For d=5: each link in 2*4=8 plaquettes. K[l,l] = 8 * (beta/2) = 4*beta.

K5=np.zeros((n_links5,n_links5))
for plaq in plaq5:
    for li,si in plaq:
        for lj,sj in plaq:
            K5[li,lj]+=(beta/2)*si*sj

# Full Hessian = K⊗I_3 (at Q=I)
H5=np.zeros((n_dof5,n_dof5))
for i in range(n_links5):
    for j in range(n_links5):
        for a in range(n_gen):
            H5[i*n_gen+a,j*n_gen+a]=K5[i,j]

# Diagonalize
evals5,evecs5=np.linalg.eigh(H5)
print(f"\nd=5 at Q=I:")
print(f"  lambda_max = {evals5.max():.6f} = {evals5.max()/beta:.4f}*beta")
print(f"  Expected 4*beta = {4*beta:.4f}")
print(f"  Expected 5*beta = {5*beta:.4f}")
print(f"  H_norm = lambda_max/(48*beta) = {evals5.max()/(48*beta):.8f}")
print(f"  1/12 = {1/12:.8f}")

# List unique eigenvalues
unique_e5=[]
for e in np.sort(evals5)[::-1]:
    if not unique_e5 or abs(e-unique_e5[-1][0])>1e-6:
        unique_e5.append((e,0))
    unique_e5[-1]=(unique_e5[-1][0], unique_e5[-1][1]+1)
print(f"\n  Top eigenvalues:")
for e,cnt in unique_e5[:8]:
    print(f"    {e:.6f} = {e/beta:.4f}*beta (multiplicity {cnt})")

# Maximum eigenvector at d=5
max_idx5=np.argmax(evals5)
v_max5=evecs5[:,max_idx5]
print(f"\n  Max eigenvector (first 12 components):")
for i in range(min(12,n_dof5)):
    print(f"    DOF {i} (link {i//n_gen}, gen {i%n_gen}): {v_max5[i]:.6f}")

# Check staggered mode for d=5
v_stag5=np.zeros(n_dof5)
for x_idx in range(n_sites5):
    x=idx_to_site5(x_idx)
    parity=sum(x)%2
    sign=(-1)**parity
    for mu in range(d5):
        l=link_idx5(x_idx,mu)
        v_stag5[l*n_gen+0]=sign
v_stag5/=np.linalg.norm(v_stag5)

Hv5=H5@v_stag5
lam_stag5=float(v_stag5@Hv5)
res_stag5=np.linalg.norm(Hv5-lam_stag5*v_stag5)/(abs(lam_stag5)+1e-30)
print(f"\n  Staggered mode (d=5): lambda = {lam_stag5:.6f} = {lam_stag5/beta:.4f}*beta")
print(f"  Is it the max eigenvector? {abs(lam_stag5-evals5.max())<0.01}")
print(f"  Staggered residual: {res_stag5:.2e}")

# What IS the max eigenvector structure?
# Look at non-staggered projections
print(f"\n  Analysis of max eigenvector:")
print(f"  Max evec norm: {np.linalg.norm(v_max5):.6f}")
# Project onto staggered mode
proj=np.dot(v_max5, v_stag5)**2
print(f"  Projection onto staggered mode: {proj:.6f}")

# Try to identify the pattern
# For d=5 L=2: each link labeled by (x, mu) with x in {0,1}^5
# Let's look at the pattern
print(f"\n  Max eigenvector pattern (non-zero entries):")
# The max evec might be a specific mode
for mu in range(d5):
    v_mu=np.zeros(n_dof5)
    for x_idx in range(n_sites5):
        x=idx_to_site5(x_idx)
        parity=sum(x)%2
        sign=(-1)**parity
        l=link_idx5(x_idx,mu)
        v_mu[l*n_gen+0]=sign
    v_mu/=np.linalg.norm(v_mu)
    proj_mu=np.dot(v_max5,v_mu)**2
    print(f"    mu={mu} staggered (gen=0): projection = {proj_mu:.6f}")

# Try link-direction modes: v = delta_{mu, mu0} * staggered
for mu0 in range(d5):
    v_test=np.zeros(n_dof5)
    for x_idx in range(n_sites5):
        x=idx_to_site5(x_idx)
        parity=sum(x)%2
        sign=(-1)**parity
        l=link_idx5(x_idx,mu0)
        v_test[l*n_gen+0]=sign
    if np.linalg.norm(v_test)>0:
        v_test/=np.linalg.norm(v_test)
        proj=np.dot(v_max5,v_test)**2
        Hv=H5@v_test
        lam_t=float(v_test@Hv)
        print(f"    Link-mu={mu0} staggered: Rayleigh={lam_t:.4f}={lam_t/beta:.4f}b, proj_on_max={proj:.4f}")

# For d=5, the maximum eigenvalue at Q=I:
# K[l,l] = 2*(d5-1)*(beta/2) = (d5-1)*beta = 4*beta
# K[l,l'] for l,l' in same plaquette = (beta/2)*si*sj
# The eigenvalue structure changes with d because cross-plaquette connections change.
# At d=4: max eigenvalue = 4*beta. At d=5: max = 5*beta (?) 
# This is the "anomaly": d=4 might be a coincidence, but d=5 breaks it.

# Compute H_norm for d=5
print(f"\n  d=5 H_norm comparison:")
print(f"  H_norm = lambda_max/(48*beta) = {evals5.max()/(48*beta):.6f}")
print(f"  1/12 = {1/12:.6f} (d=4 bound)")
print(f"  5/64 = {5/64:.6f} (E009 finding)")
print(f"  3/40 = {3/40:.6f} (E008 formula)")

# d=5 specific: how many plaquettes per link?
n_plaq_per_link5 = 2*(d5-1)
print(f"\n  For d={d5}: each link in {n_plaq_per_link5} plaquettes")
print(f"  K[l,l] = {n_plaq_per_link5}*(beta/2) = {n_plaq_per_link5*0.5}*beta")
print(f"  This is the diagonal of K, but the eigenvalue 5*beta > 4*beta suggests")
print(f"  the off-diagonal contributions INCREASE K's max eigenvalue beyond its diagonal")
print(f"  (For d=4: K_diag = 6*(1/2) = 3*beta, K_max = 4*beta > 3*beta)")
print(f"  (For d=5: K_diag = 8*(1/2) = 4*beta, K_max = {evals5.max():.4f}*beta)")

print("\nd5_analysis.py DONE")

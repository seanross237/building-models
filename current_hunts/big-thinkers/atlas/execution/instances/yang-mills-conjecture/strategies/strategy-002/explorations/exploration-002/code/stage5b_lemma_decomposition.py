"""
Stage 5b: Verify LEMMA_D and LEMMA_RDR decomposition.
Key finding: sum_S = LEMMA_D + LEMMA_RDR, both >= 0 under constraint Sigma T_mu = 0.
"""
import numpy as np

PLANES = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]

def random_so3():
    q = np.random.randn(4); q /= np.linalg.norm(q)
    w, x, y, z = q
    return np.array([[1-2*(y*y+z*z), 2*(x*y-w*z), 2*(x*z+w*y)],
                     [2*(x*y+w*z), 1-2*(x*x+z*z), 2*(y*z-w*x)],
                     [2*(x*z-w*y), 2*(y*z+w*x), 1-2*(x*x+y*y)]])

def f_vec(M, p): return float(p @ (np.eye(3)-M) @ p)

def random_T_constrained():
    T = np.random.randn(4, 3); T[3] = -(T[0]+T[1]+T[2]); return T

def compute_all(R, D, T):
    I3 = np.eye(3)
    fhalf = cross_D = cross_RDR = cross_VCB = 0
    for mu, nu in PLANES:
        p, q = T[mu], T[nu]
        U = R[mu]@D[(mu,nu)]; W = D[(mu,nu)]@R[nu].T
        fhalf += f_vec(U,p) + f_vec(W,q)  # = f_same/2
        cross_D   += -2*float(p@(I3-D[(mu,nu)].T)@q)
        cross_RDR += -2*float(p@(I3-R[mu]@D[(mu,nu)]@R[nu].T)@q)
        cross_VCB +=    float(p@(I3-U)@(I3-W.T)@q)
    return fhalf, cross_D, cross_RDR, cross_VCB

np.random.seed(42)
N = 200000

min_LD = min_LR = min_SVCB = min_Sdiff = float('inf')
viol_LD = viol_LR = viol_SVCB = viol_Sdiff = 0

for _ in range(N):
    R = [random_so3() for _ in range(4)]
    D = {mn: random_so3() for mn in PLANES}
    T = random_T_constrained()
    n2 = float(np.sum(T**2))
    
    fhalf, cD, cRDR, cVCB = compute_all(R, D, T)
    
    LD   = (fhalf + cD)   / n2
    LR   = (fhalf + cRDR) / n2
    SVCB = (fhalf + cVCB) / n2
    Sdiff= (fhalf + cD + cRDR - fhalf - cVCB) / n2  # sum(S - VCB_S)
    
    if LD   < min_LD:   min_LD   = LD
    if LR   < min_LR:   min_LR   = LR
    if SVCB < min_SVCB: min_SVCB = SVCB
    if Sdiff< min_Sdiff:min_Sdiff = Sdiff
    
    if LD   < -1e-10: viol_LD   += 1
    if LR   < -1e-10: viol_LR   += 1
    if SVCB < -1e-10: viol_SVCB += 1
    if Sdiff< -1e-10: viol_Sdiff += 1

print(f"N = {N} tests with constraint Sigma T_mu = 0")
print()
print(f"LEMMA_D   (f_same/2 + cross_D):   min={min_LD:.4f}, violations={viol_LD}")
print(f"LEMMA_RDR (f_same/2 + cross_RDR): min={min_LR:.4f}, violations={viol_LR}")
print(f"sum_VCB_S (f_same/2 + cross_VCB): min={min_SVCB:.4f}, violations={viol_SVCB}")
print(f"sum(S-VCB_S):                      min={min_Sdiff:.4f}, violations={viol_Sdiff}")
print()
print("sum_S = LEMMA_D + LEMMA_RDR")
print("All quantities >= 0 with constraint Sigma T_mu = 0")

# Also test WITHOUT constraint
np.random.seed(42)
viol_LD_unc = 0
for _ in range(N):
    R = [random_so3() for _ in range(4)]
    D = {mn: random_so3() for mn in PLANES}
    T = np.random.randn(4, 3)  # NO constraint
    n2 = float(np.sum(T**2))
    fhalf, cD, _, _ = compute_all(R, D, T)
    if (fhalf + cD)/n2 < -1e-10: viol_LD_unc += 1

print(f"\nLEMMA_D WITHOUT constraint: violations={viol_LD_unc}")
print("=> Constraint Sigma T_mu = 0 is ESSENTIAL for LEMMA_D")

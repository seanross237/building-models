"""Quick adversarial search for Combined Bound Lemma violation (100 trials)."""
import numpy as np

np.random.seed(54321)

def random_so3():
    q = np.random.randn(4); q /= np.linalg.norm(q)
    w,x,y,z = q
    return np.array([[1-2*(y*y+z*z),2*(x*y-w*z),2*(x*z+w*y)],
                     [2*(x*y+w*z),1-2*(x*x+z*z),2*(y*z-w*x)],
                     [2*(x*z-w*y),2*(y*z+w*x),1-2*(x*x+y*y)]])

def so3_exp(omega):
    angle = np.linalg.norm(omega)
    if angle < 1e-14: return np.eye(3)
    ax = omega/angle
    K = np.array([[0,-ax[2],ax[1]],[ax[2],0,-ax[0]],[-ax[1],ax[0],0]])
    return np.eye(3) + np.sin(angle)*K + (1-np.cos(angle))*(K@K)

def f(R, n): return 1.0 - n @ R @ n

def combined_bound(params):
    A = so3_exp(params[0:3])
    B = so3_exp(params[3:6])
    D = so3_exp(params[6:9])
    theta, phi = params[9], params[10]
    n = np.array([np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)])
    return (f(A,n) + f(B,n) + f(A@D,n) + f(D@B.T,n) - f(D,n) - f(A@D@B.T,n))

def grad(params, eps=1e-7):
    g = np.zeros(11)
    val0 = combined_bound(params)
    for i in range(11):
        p = params.copy(); p[i] += eps
        g[i] = (combined_bound(p) - val0) / eps
    return g

min_val = float('inf')
for trial in range(200):
    params = np.random.randn(11) * np.pi
    lr = 0.02
    for step in range(3000):
        val = combined_bound(params)
        if val < min_val:
            min_val = val
        g = grad(params)
        params -= lr * g
        lr *= 0.9995
    if trial % 50 == 0:
        print(f"Trial {trial}: min so far = {min_val:.15e}")

print(f"\nFinal min over 200 trials: {min_val:.15e}")
print(f"Combined Bound Lemma holds: {min_val >= -1e-10}")

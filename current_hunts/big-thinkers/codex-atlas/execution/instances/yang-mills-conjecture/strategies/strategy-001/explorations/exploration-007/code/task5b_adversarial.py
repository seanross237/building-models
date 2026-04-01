"""
Task 5b: Adversarial search for Combined Bound Lemma violation.
Uses gradient descent without scipy.
"""

import numpy as np

np.random.seed(54321)

def random_so3():
    q = np.random.randn(4)
    q /= np.linalg.norm(q)
    w, x, y, z = q
    return np.array([
        [1-2*(y*y+z*z), 2*(x*y-w*z), 2*(x*z+w*y)],
        [2*(x*y+w*z), 1-2*(x*x+z*z), 2*(y*z-w*x)],
        [2*(x*z-w*y), 2*(y*z+w*x), 1-2*(x*x+y*y)]
    ])

def axis_angle_to_R(omega):
    angle = np.linalg.norm(omega)
    if angle < 1e-14:
        return np.eye(3)
    axis = omega / angle
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(angle)*K + (1-np.cos(angle))*(K@K)

def f(R, n):
    return 1.0 - n @ R @ n

def combined_bound(omega_A, omega_B, omega_D, theta, phi):
    A = axis_angle_to_R(omega_A)
    B = axis_angle_to_R(omega_B)
    D = axis_angle_to_R(omega_D)
    n = np.array([np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)])

    return (f(A,n) + f(B,n) + f(A@D,n) + f(D@B.T,n)
          - f(D,n) - f(A@D@B.T,n))

def numerical_gradient(params, eps=1e-7):
    grad = np.zeros_like(params)
    for i in range(len(params)):
        p_plus = params.copy(); p_plus[i] += eps
        p_minus = params.copy(); p_minus[i] -= eps
        val_plus = combined_bound(p_plus[:3], p_plus[3:6], p_plus[6:9], p_plus[9], p_plus[10])
        val_minus = combined_bound(p_minus[:3], p_minus[3:6], p_minus[6:9], p_minus[9], p_minus[10])
        grad[i] = (val_plus - val_minus) / (2*eps)
    return grad

print("=" * 70)
print("ADVERSARIAL SEARCH: Trying to minimize the Combined Bound Lemma")
print("=" * 70)

min_val = float('inf')
min_params = None

for trial in range(1000):
    # Random starting point
    params = np.random.randn(11) * np.pi

    # Gradient descent
    lr = 0.01
    for step in range(2000):
        val = combined_bound(params[:3], params[3:6], params[6:9], params[9], params[10])
        if val < min_val:
            min_val = val
            min_params = params.copy()
        grad = numerical_gradient(params)
        params -= lr * grad
        lr *= 0.999  # decay

    if trial % 100 == 0:
        print(f"  Trial {trial}: current min = {min_val:.15e}")

print(f"\nFinal min over 1000 adversarial trials: {min_val:.15e}")
print(f"Combined Bound Lemma HOLDS: {min_val >= -1e-10}")

if min_val < -1e-10:
    print("\n*** VIOLATION FOUND! ***")
    print(f"Parameters: {min_params}")
else:
    print("\nNo violation found. The lemma appears correct.")

# ============================================================
# Additional: Try to find cases where the bound is TIGHT (= 0)
# ============================================================

print("\n" + "=" * 70)
print("TIGHTNESS: When does the Combined Bound = 0?")
print("=" * 70)

# From the proof: LHS = (sqrt(f(A))-sqrt(f(B)))^2 + |cross|^2 terms...
# Actually LHS = n^T(I-A)D(I-B^T)n + f(A) + f(B)
# = 0 requires both f(A)=f(B)=0, which means A*n=n and B*n=n.
# Then cross = n^T(I-A)D(I-B^T)n = 0 too.
# So the bound is tight iff A and B both fix n.

# Verify: A = rotation around n by angle alpha, B = rotation around n by angle beta
for _ in range(10):
    n = np.random.randn(3); n /= np.linalg.norm(n)
    # Build rotations that fix n: rotate around n-axis
    alpha = np.random.rand() * 2 * np.pi
    beta = np.random.rand() * 2 * np.pi

    # Rotation around n by angle theta:
    K = np.array([[0, -n[2], n[1]], [n[2], 0, -n[0]], [-n[1], n[0], 0]])
    A = np.eye(3) + np.sin(alpha)*K + (1-np.cos(alpha))*(K@K)
    B = np.eye(3) + np.sin(beta)*K + (1-np.cos(beta))*(K@K)
    D = random_so3()

    val = (f(A,n) + f(B,n) + f(A@D,n) + f(D@B.T,n)
         - f(D,n) - f(A@D@B.T,n))

    print(f"  A,B fix n: bound = {val:.15f} (f(A)={f(A,n):.2e}, f(B)={f(B,n):.2e})")

# Now try A fixes n, B doesn't (or vice versa):
for _ in range(5):
    n = np.random.randn(3); n /= np.linalg.norm(n)
    alpha = np.random.rand() * 2 * np.pi
    K = np.array([[0, -n[2], n[1]], [n[2], 0, -n[0]], [-n[1], n[0], 0]])
    A = np.eye(3) + np.sin(alpha)*K + (1-np.cos(alpha))*(K@K)
    B = random_so3()
    D = random_so3()

    val = (f(A,n) + f(B,n) + f(A@D,n) + f(D@B.T,n)
         - f(D,n) - f(A@D@B.T,n))
    print(f"  A fixes n, B random: bound = {val:.6f} (f(A)={f(A,n):.2e}, f(B)={f(B,n):.6f})")

# Also check: A=B case (combined bound should be >= 0 even here)
print("\n  A=B case:")
for _ in range(10):
    A = random_so3()
    D = random_so3()
    n = np.random.randn(3); n /= np.linalg.norm(n)

    val = (f(A,n) + f(A,n) + f(A@D,n) + f(D@A.T,n)
         - f(D,n) - f(A@D@A.T,n))
    print(f"    bound = {val:.10f}")

print("\nDone.")

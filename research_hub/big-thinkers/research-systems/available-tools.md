# Available Tools for Computation

Shared reference for all systems running science missions. This describes what's installed and usable on this machine.

## Python (3.9.12, via Anaconda)

**Core math stack (always available):**
- `numpy` 2.0.2 — linear algebra, FFT, eigenvalue problems, random number generation. The workhorse.
- `scipy` 1.7.3 — optimization, sparse matrices, special functions, integration, spatial algorithms. Has a numpy version warning but works for most uses.
- `sympy` 1.10.1 — symbolic algebra, calculus, equation solving, group theory.
- `mpmath` 1.2.1 — arbitrary precision floating point. Useful when double precision isn't enough.
- `networkx` 2.7.1 — graph algorithms.

**Broken (numpy 2.x incompatibility with Anaconda 3.9):**
- `matplotlib` — crashes on import. Workaround: save data to JSON, or `pip install --force-reinstall matplotlib` in a venv.
- `pandas` — crashes on import. Same issue.
- `numba` — crashes on import. Same issue.

**Not installed but pip-installable:**
- `jax`, `torch`, `tensorflow` — GPU/autodiff frameworks. `pip install jax jaxlib` or `pip install torch`.
- `cvxpy` — convex optimization / SDP. `pip install cvxpy`.
- `dedalus` — spectral PDE solver (good for fluid dynamics). `pip install dedalus`.
- `fenics` / `firedrake` — finite element PDE solvers. More complex install.
- Any other PyPI package — `pip install <package>` works.

**General pattern:** Explorers in past missions have written bespoke simulation code using raw numpy rather than relying on domain-specific packages. This works well — Monte Carlo lattice gauge simulations, Hessian eigenvalue computations, spectral methods all implemented from scratch with numpy + scipy.linalg. Installing specialized packages is fine but not required.

## Computer Algebra Systems

- **SageMath 10.8** — full CAS with number theory, algebraic geometry, combinatorics, group theory. Run via `sage` or `sage -python script.py`. Includes its own Python environment with GAP, PARI/GP, Singular, etc.

## Theorem Provers

- **Lean 4** — via elan. Mathlib available. Useful for formalizing proofs but algebraic geometry and PDE libraries are limited.

## Shell Tools

- Standard Unix tools (curl, wget, etc.) for fetching papers, data.
- `pip3` for installing Python packages on the fly.
- Web search and web fetch available through Claude's built-in tools.

## Modal (Cloud Compute)

For computations that are too big or too slow to run locally, use **Modal** to run them on cloud hardware. Modal is authenticated and ready to use.

**When to use Modal instead of running locally:**
- Grid sizes above N=128 (e.g., N=256³ NS simulations)
- Monte Carlo sweeps with L≥16 or >5000 sweeps
- Any computation you estimate will take >10 minutes locally
- When you need more RAM than available locally
- When you need a GPU (JAX, large FFTs)

**How to use it:**

Write your computation script as normal Python. The only difference: read inputs from `ARGS` dict and store outputs in `RESULTS` dict. Then run it via the client.

```python
# Example: run a script on Modal from your exploration code
import sys
sys.path.insert(0, "/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/modal")
from run_remote import remote, remote_heavy, remote_gpu

result = remote('''
import numpy as np
from numpy.fft import fftn, ifftn

N = ARGS["N"]
field = np.random.randn(N, N, N)
spectrum = np.abs(fftn(field))**2
RESULTS["total_energy"] = float(np.sum(spectrum))
print(f"Energy for N={N}: {np.sum(spectrum):.6e}")
''', args={"N": 256})

print(result["stdout"])     # printed output from the remote script
print(result["results"])    # {"total_energy": ...}
if result["error"]:
    print(result["error"])  # traceback if it crashed
```

**Three tiers available:**

| Function | Hardware | Timeout | Use for |
|---|---|---|---|
| `remote(script, args)` | 1 CPU, 4 GB | 1 hour | Standard computations |
| `remote_heavy(script, args)` | 4 CPU, 16 GB | 2 hours | Big grids, long sweeps |
| `remote_gpu(script, args)` | T4 GPU, 8 GB | 1 hour | JAX/GPU-accelerated code |

**You can also run a local .py file remotely:**
```python
result = remote_file("code/ns_solver.py", args={"N": 256, "Re": 5000}, heavy=True)
```

**Or from the command line:**
```bash
python /Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/modal/run_remote.py code/my_script.py --heavy --args '{"N": 256}'
```

**Available packages on Modal:** numpy, scipy, sympy, mpmath, networkx, matplotlib. GPU tier also has JAX with CUDA.

**Important notes:**
- The remote environment is a fresh container — no local files are available. Embed all code and data in the script string or pass via `ARGS`.
- Results must be JSON-serializable (use `.tolist()` on numpy arrays).
- First call may have a ~10s cold start. Subsequent calls within ~5 minutes are fast.

## Tips for Explorers

1. **Write code immediately.** Don't spend 10 minutes reasoning about what a computation "should" give — run it.
2. **numpy is enough for most things.** Eigenvalue problems: `np.linalg.eigh`. FFTs: `np.fft`. Random matrices: `np.random`. Linear systems: `scipy.linalg.solve`.
3. **Save code to files before running.** Don't run long computations inline — write to `code/script.py` and execute.
4. **Print intermediate results.** Don't wait for a 5-minute computation to finish before seeing any output.
5. **pip install freely.** If a package would save significant implementation time, install it. But don't spend 20 minutes debugging package installs when you could write 50 lines of numpy.
6. **Use Modal for heavy computation.** If your grid is large, your sweep is long, or you're hitting the 10-minute timeout — run it on Modal instead. See the Modal section above.

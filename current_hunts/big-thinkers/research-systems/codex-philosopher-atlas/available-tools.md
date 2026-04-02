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
- Web search is available to Codex-launched research roles through the wrapper's
  top-level `--search` flag.

## Tips for Explorers

1. **Write code immediately.** Don't spend 10 minutes reasoning about what a computation "should" give — run it.
2. **numpy is enough for most things.** Eigenvalue problems: `np.linalg.eigh`. FFTs: `np.fft`. Random matrices: `np.random`. Linear systems: `scipy.linalg.solve`.
3. **Save code to files before running.** Don't run long computations inline — write to `code/script.py` and execute.
4. **Print intermediate results.** Don't wait for a 5-minute computation to finish before seeing any output.
5. **pip install freely.** If a package would save significant implementation time, install it. But don't spend 20 minutes debugging package installs when you could write 50 lines of numpy.

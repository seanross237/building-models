`harmonic_shell_model.py` implements the minimal exterior-shell model used in `REPORT.md`.

It does three things:

1. encodes the uniform shell on `|y| = 2` whose Newtonian potential is exactly constant on `B_1`,
2. computes the local pairing with the explicit cutoff `psi(x,t) = (1 - |x|^2)^2_+`,
3. checks numerically at sample points that the shell potential is constant inside `B_1` and prints the induced energy-scale family `U(A)` for `u_A = A e_1`.

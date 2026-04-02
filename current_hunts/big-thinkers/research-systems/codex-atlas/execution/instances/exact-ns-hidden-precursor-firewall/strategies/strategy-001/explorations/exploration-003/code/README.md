# Exploration 003 Code

`time_local_balance_demo.py` is a reproducible algebraic demonstration of the
time-local structure used in `REPORT.md`.

It does not construct an exact Navier-Stokes solution. It only shows that the
localized witness-gain balance can keep the late gain fixed while the earlier
precursor mass `P_flux^-` tends to zero, because the exact identity controls
the late gain by terms supported on the late activation window.

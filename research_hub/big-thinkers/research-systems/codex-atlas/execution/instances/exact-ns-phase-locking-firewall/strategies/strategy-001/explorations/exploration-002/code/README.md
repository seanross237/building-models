Primary reproducible artifact:

```bash
python3 code/minimal_c_support_audit.py
```

This prints:

- the exact five-wavevector two-triad cluster used in the report,
- the internal helical ledger and receiver equations,
- the forced single-triad value `C_l = +/-1`,
- the exact cancellation family `C_l = tan^2(eps/2)`,
- and the external emissions showing the support is not dynamically isolated.

Saved output:

```bash
python3 code/minimal_c_support_audit.py > code/minimal_c_support_audit_output.txt
```

Supplementary artifact:

```bash
python3 code/minimal_cluster_cancellation_demo.py
```

This older demo prints a simpler same-target two-input cancellation example.

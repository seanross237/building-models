#!/usr/bin/env python3
"""
Thin client for running scientific computation on Modal.

Usage from any agent script or inline Python:

    from run_remote import remote, remote_heavy, remote_gpu

    # Run a script string remotely
    result = remote('''
    import numpy as np
    A = np.random.randn(ARGS["N"], ARGS["N"])
    eigenvalues = np.linalg.eigvalsh(A + A.T)
    RESULTS["eigenvalues"] = eigenvalues.tolist()
    print(f"Computed {len(eigenvalues)} eigenvalues")
    ''', args={"N": 1000})

    print(result["stdout"])           # "Computed 1000 eigenvalues"
    print(result["results"]["eigenvalues"][:5])  # first 5 eigenvalues

    # Or run a .py file remotely
    result = remote_file("code/ns_solver.py", args={"N": 128, "Re": 5000})

Conventions for scripts:
    - Read input parameters from the `ARGS` dict (injected into globals)
    - Store output data in the `RESULTS` dict (injected into globals)
    - Use print() for progress/logging — captured in result["stdout"]
    - If the script errors, result["error"] contains the traceback
"""

from __future__ import annotations

import os
import sys
import modal

# Resolve the app relative to this file so it works from any cwd
_APP_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")


def _get_fn(fn_name: str):
    """Look up a Modal function by name."""
    return modal.Function.from_name("research-compute", fn_name)


def remote(script: str, args: dict | None = None) -> dict:
    """Run a script on Modal (standard CPU, 4 GB RAM, 1h timeout)."""
    fn = _get_fn("run_script")
    return fn.remote(script=script, args=args)


def remote_heavy(script: str, args: dict | None = None) -> dict:
    """Run a script on Modal (4 CPUs, 16 GB RAM, 2h timeout)."""
    fn = _get_fn("run_script_heavy")
    return fn.remote(script=script, args=args)


def remote_gpu(script: str, args: dict | None = None) -> dict:
    """Run a script on Modal (T4 GPU, 8 GB RAM, 1h timeout)."""
    fn = _get_fn("run_script_gpu")
    return fn.remote(script=script, args=args)


def remote_file(filepath: str, args: dict | None = None, heavy: bool = False, gpu: bool = False) -> dict:
    """Read a local .py file and run it on Modal."""
    with open(filepath, "r") as f:
        script = f.read()
    if gpu:
        return remote_gpu(script, args)
    if heavy:
        return remote_heavy(script, args)
    return remote(script, args)


# ---------------------------------------------------------------------------
# CLI convenience: python run_remote.py <script.py> [--heavy] [--gpu]
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Run a Python script on Modal")
    parser.add_argument("script", help="Path to .py file")
    parser.add_argument("--heavy", action="store_true", help="Use heavy tier (4 CPU, 16 GB)")
    parser.add_argument("--gpu", action="store_true", help="Use GPU tier (T4)")
    parser.add_argument("--args", type=str, default="{}", help="JSON string of args")
    parsed = parser.parse_args()

    args = json.loads(parsed.args)
    result = remote_file(parsed.script, args=args, heavy=parsed.heavy, gpu=parsed.gpu)

    if result["error"]:
        print("=== ERROR ===", file=sys.stderr)
        print(result["error"], file=sys.stderr)
    if result["stdout"]:
        print(result["stdout"])
    if result["results"]:
        print("=== RESULTS ===")
        print(json.dumps(result["results"], indent=2, default=str))

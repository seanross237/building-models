"""
Modal compute app for research systems.

Provides remote execution of scientific Python code on cloud hardware.
Agents send scripts (as strings) and get back stdout + any saved result files.
"""

from __future__ import annotations

import modal

app = modal.App("research-compute")

# ---------------------------------------------------------------------------
# Images
# ---------------------------------------------------------------------------

science_image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "numpy",
        "scipy",
        "sympy",
        "mpmath",
        "networkx",
        "matplotlib",
    )
)

science_image_gpu = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "numpy",
        "scipy",
        "sympy",
        "mpmath",
        "networkx",
        "matplotlib",
        "jax[cuda12]",
    )
)


# ---------------------------------------------------------------------------
# General-purpose remote executor (CPU)
# ---------------------------------------------------------------------------

@app.function(
    image=science_image,
    timeout=3600,       # 1 hour max
    memory=4096,        # 4 GB RAM
)
def run_script(script: str, args: dict | None = None) -> dict:
    """
    Execute an arbitrary Python script on Modal and return results.

    Parameters
    ----------
    script : str
        Python source code to execute.
    args : dict, optional
        Passed into the script's global namespace as `ARGS`.

    Returns
    -------
    dict with keys:
        stdout  : str   — captured print output
        results : dict   — anything the script stores in the `RESULTS` dict
        error   : str | None — traceback if the script raised
    """
    import io
    import sys
    import traceback

    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf

    namespace = {"ARGS": args or {}, "RESULTS": {}}

    error = None
    try:
        exec(compile(script, "<remote-script>", "exec"), namespace)
    except Exception:
        error = traceback.format_exc()
    finally:
        sys.stdout = old_stdout

    return {
        "stdout": buf.getvalue(),
        "results": namespace.get("RESULTS", {}),
        "error": error,
    }


# ---------------------------------------------------------------------------
# General-purpose remote executor (GPU)
# ---------------------------------------------------------------------------

@app.function(
    image=science_image_gpu,
    gpu="T4",
    timeout=3600,
    memory=8192,
)
def run_script_gpu(script: str, args: dict | None = None) -> dict:
    """Same as run_script but with a T4 GPU available."""
    import io
    import sys
    import traceback

    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf

    namespace = {"ARGS": args or {}, "RESULTS": {}}

    error = None
    try:
        exec(compile(script, "<remote-script>", "exec"), namespace)
    except Exception:
        error = traceback.format_exc()
    finally:
        sys.stdout = old_stdout

    return {
        "stdout": buf.getvalue(),
        "results": namespace.get("RESULTS", {}),
        "error": error,
    }


# ---------------------------------------------------------------------------
# Heavy CPU variant — for big NS grids, long Monte Carlo sweeps
# ---------------------------------------------------------------------------

@app.function(
    image=science_image,
    timeout=7200,       # 2 hours max
    memory=16384,       # 16 GB RAM
    cpu=4,
)
def run_script_heavy(script: str, args: dict | None = None) -> dict:
    """Same as run_script but with 4 CPUs, 16 GB RAM, 2-hour timeout."""
    import io
    import sys
    import traceback

    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf

    namespace = {"ARGS": args or {}, "RESULTS": {}}

    error = None
    try:
        exec(compile(script, "<remote-script>", "exec"), namespace)
    except Exception:
        error = traceback.format_exc()
    finally:
        sys.stdout = old_stdout

    return {
        "stdout": buf.getvalue(),
        "results": namespace.get("RESULTS", {}),
        "error": error,
    }

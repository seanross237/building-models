# Section 1, Step 1 — Scaffolding notes

## What you built

- Folder skeleton under `buddy-eywa/` for `eywa-system/`, `data-system/`, `convenience-docs/`, `sticky-notes/`, and `design-docs/`, each with `.gitkeep` markers.
- Empty-but-importable `buddy_eywa_runtime` package at `eywa-system/runtime/buddy_eywa_runtime/__init__.py` with a docstring and `__version__ = "0.0.1"`.
- Minimal hatchling-based `pyproject.toml` at the project root that maps the non-standard package path to `buddy_eywa_runtime` for editable installs.

## Judgment calls

- **Build backend: hatchling.** Super-eywa has no `pyproject.toml`, `setup.py`, or `setup.cfg` at all — no convention to match. Picked hatchling because it is the modern PEP 517 default, has first-class support for non-standard package layouts via `tool.hatch.build.targets.wheel.sources`, and keeps the config to ~15 lines. Setuptools would also have worked but needs more boilerplate to remap a hyphenated parent path.
- **Python version: `>=3.9`.** Super-eywa has no declared minimum, but all observed tracebacks point at `/Users/seanross/opt/anaconda3/lib/python3.9/...`, so 3.9 is the de facto floor. Used `>=3.9` rather than pinning exactly so future builders can move forward without editing this file.
- **Package version `0.0.1`.** Spec said so; mirrored it in `__init__.py` so the two never drift.
- **`.gitkeep` over placeholder READMEs.** Spec explicitly forbids "TODO filler" content files, and `.gitkeep` is the conventional zero-content marker. No info loss because every empty dir is named meaningfully.
- **Path remap in pyproject.** The package lives at `eywa-system/runtime/buddy_eywa_runtime/` (hyphenated parents make it non-importable as a namespace), so I configured both `[tool.hatch.build.targets.wheel] packages` and `[tool.hatch.build.targets.wheel.sources]` so that `pip install -e .` exposes it as the top-level import `buddy_eywa_runtime`.
- **No `dependencies`, no `[project.optional-dependencies]`, no `[project.scripts]`, no `[tool.*]` linting config.** Spec said empty deps; I also held off on tool config (ruff, black, mypy) because there's nothing yet to lint and adding it would be speculative.
- **No `__author__`, `license`, `readme`, or `urls` in pyproject.** Kept the metadata block to the bare minimum the spec asked for. These are easy to add later when Sean cares.

## Uncertainties / things to revisit

- **Hatchling vs Sean's preferences.** Sean may already use poetry/uv/pdm in other home-base projects; I didn't audit them. If a different backend is the home-base norm, swapping is a 10-line edit.
- **Python floor `>=3.9`.** Inferred from tracebacks, not from a config file. If Sean is on a newer interpreter for new work, bump to `>=3.11` or `>=3.12` to unlock match statements, better typing, etc.
- **Package path remap.** The double declaration of `packages` and `sources` is the cleanest hatchling pattern I know for this layout, but I did not actually run `pip install -e .` (per spec). Worth a smoke test before Section 2 starts depending on imports.
- **`design-docs/` exists empty.** Step 6 is supposed to move the root `01-vision.md`..`09-...md` into it; the empty dir + `.gitkeep` is fine for now but will need the `.gitkeep` removed when real files arrive.
- **`convenience-docs/lil-plans/archive/` is the only nested convenience-docs path created.** Spec only listed that one. If buddy-eywa later wants `lil-plans/active/` or similar siblings, they'll be added then.

## Blockers

None. All deliverables in scope completed.

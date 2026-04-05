# Exploration 001: Background-Only Cosmology Screen

## Mission Context

This is the first concrete screen for the unfinished-spacetime idea. The question is not whether the ontology is beautiful. The question is whether a late-time deformation of dark-energy behavior survives basic public-data checks.

## Goal

Build the smallest reproducible background-only pipeline that can compare:

- `LCDM`
- constant-`w`
- CPL
- smooth-step `w(z)`

on simple BAO and SN summary data.

## Required Outputs

1. A runnable Python script for coarse model comparison.
2. A dataset manifest template showing what files are expected.
3. A self-check mode using synthetic data.
4. A `REPORT.md` entry once real data is plugged in.

## Constraints

- Start with BAO + SN only.
- Keep `r_d` fixed in the first pass.
- Treat `Planck` and `ACT` as the next-stage robustness anchors, not as hidden assumptions in this first script.
- Be explicit about the SN intercept nuisance and what is or is not being fit.

## Success Criteria

- The script runs on a toy dataset.
- The pipeline can score all four model families.
- The code is honest about what is missing for a full paper-grade cosmology analysis.

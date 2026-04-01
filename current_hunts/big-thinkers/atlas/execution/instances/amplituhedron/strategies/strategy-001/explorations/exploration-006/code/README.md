# EFT-Hedron Positivity Bounds — Code

## Overview

This directory contains the implementation of EFT-hedron positivity constraints for
2→2 scalar scattering and photon-photon scattering.

## Files

| File | Description |
|------|-------------|
| `partial_waves.py` | Spectral density models (BW, power-law, multi-resonance), Wilson coefficient computation via dispersion relations |
| `forward_bounds.py` | Forward limit positivity bounds: g_{n,0} >= 0 for all UV-complete models |
| `hankel_bounds.py` | Hankel matrix PSD bounds, analytic formula verification, saturation properties |
| `photon_scattering.py` | Photon-photon scattering bounds, Euler-Heisenberg QED verification |
| `eft_hedron_main.py` | **Main script**: runs all stages and prints a clean summary |

## Quick Start

```bash
python3 eft_hedron_main.py     # full pipeline
python3 partial_waves.py       # spectral density demo
python3 forward_bounds.py      # forward bounds only
python3 hankel_bounds.py       # Hankel bounds only
python3 photon_scattering.py   # photon bounds only
```

## Dependencies

- Python 3.x
- numpy
- scipy (integrate, special)

## Key Results

- All UV-complete spectral densities give g_{n,0} >= 0 (n=2..8) [COMPUTED]
- Single resonance saturates 2x2 Hankel: det ≈ 0 [COMPUTED]
- Two resonances give strict inequality [COMPUTED]
- Analytic formula det(H_2) = (16pi)^2 A B (M1^2-M2^2)^2 / (M1 M2)^10 [VERIFIED]
- QED Euler-Heisenberg satisfies all photon bounds; c2/c1 = 7/4 [COMPUTED]

## Physical Setup

The EFT expansion M(s,t) = sum g_{p,q} s^p t^q is valid for s << M (UV cutoff mass M).
The spectral density Im M(s,0) = s sigma_tot(s) >= 0 by the optical theorem.
The Wilson coefficients g_{n,0} = (1/pi) int Im M(s',0) / s'^{n+1} ds' are moments
of the positive measure, giving all the positivity constraints.

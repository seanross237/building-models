#!/usr/bin/env python3

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
from matplotlib import pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
PROCESSED_ROOT = ROOT / "data" / "processed"
PLOT_ROOT = ROOT / "plots"
NOTE_ROOT = ROOT / "notes"

SUMMARY_PATH = PROCESSED_ROOT / "bullet_cluster_shadow_summary.json"
REPORT_PATH = NOTE_ROOT / "bullet_cluster_shadow_report.md"
PLOT_PATH = PLOT_ROOT / "bullet_cluster_shadow_tradeoffs.png"


@dataclass
class BulletConstraints:
    global_star_fraction: float = 0.10
    global_gas_fraction: float = 0.90
    local_plasma_to_bcg_baryon_ratio: float = 2.0
    mass_gas_offset_sigma: float = 8.0
    projected_subcluster_separation_mpc: float = 0.72


@dataclass
class SourceLinks:
    clowe_2006: str = "https://arxiv.org/abs/astro-ph/0608407"
    clowe_2007: str = "https://arxiv.org/abs/astro-ph/0611496"
    bradac_2006: str = "https://arxiv.org/abs/astro-ph/0608408"
    markevitch_2002: str = "https://arxiv.org/abs/astro-ph/0110468"
    clowe_2006_pdf_snippet: str = "https://www.physics.rutgers.edu/~saurabh/690/Clowe-etal-2006.pdf"
    gas_rich_btfr: str = "https://arxiv.org/abs/1102.3913"


def required_phase_weight_ratio(star_fraction: float, gas_fraction: float) -> float:
    return gas_fraction / star_fraction


def effective_star_fraction(raw_star_fraction: float, eta_star_over_gas: float) -> float:
    numerator = raw_star_fraction * eta_star_over_gas
    denominator = numerator + (1.0 - raw_star_fraction)
    return numerator / denominator


def beta_required(weight_ratio: float, density_contrast: float) -> float:
    return math.log(weight_ratio) / math.log(density_contrast)


def coarse_grained_gas_to_bcg_ratio(local_mass_ratio: float, beta: np.ndarray) -> np.ndarray:
    return local_mass_ratio ** (1.0 + beta)


def make_plot(
    local_mass_ratio: float,
    global_eta_required: float,
    local_eta_required: float,
) -> dict[str, list[float] | float]:
    beta_grid = np.linspace(0.0, 4.0, 400)
    gas_to_bcg = coarse_grained_gas_to_bcg_ratio(local_mass_ratio, beta_grid)

    eta_grid = np.logspace(0.0, 2.2, 400)
    raw_star_fractions = [0.10, 0.20, 0.50]

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    axes[0].plot(beta_grid, gas_to_bcg, color="#9c1c31", lw=2.5)
    axes[0].axhline(1.0, color="#222222", ls="--", lw=1)
    axes[0].set_xlabel("Density exponent beta")
    axes[0].set_ylabel("Predicted gas / BCG effective source")
    axes[0].set_title("Coarse-grained monotone law")
    axes[0].set_ylim(0.0, max(18.0, float(gas_to_bcg.max()) * 1.03))
    axes[0].text(
        0.15,
        0.89,
        "Bullet local baryon ratio = 2:1 gas over BCG",
        transform=axes[0].transAxes,
        fontsize=9,
    )

    colors = ["#264653", "#2a9d8f", "#e9c46a"]
    for raw_star_fraction, color in zip(raw_star_fractions, colors, strict=True):
        eff = [effective_star_fraction(raw_star_fraction, eta) for eta in eta_grid]
        gas_fraction = 1.0 - raw_star_fraction
        label = f"raw stars={raw_star_fraction:.0%}, gas={gas_fraction:.0%}"
        axes[1].plot(eta_grid, eff, color=color, lw=2.5, label=label)
    axes[1].axvline(global_eta_required, color="#9c1c31", ls="--", lw=1.5)
    axes[1].axvline(local_eta_required, color="#8d99ae", ls=":", lw=1.5)
    axes[1].text(global_eta_required * 1.05, 0.13, "Bullet global eta=9", color="#9c1c31", fontsize=9)
    axes[1].text(local_eta_required * 1.05, 0.06, "local eta=2", color="#8d99ae", fontsize=9)
    axes[1].set_xscale("log")
    axes[1].set_xlabel("Star / gas shielding weight ratio eta")
    axes[1].set_ylabel("Effective stellar fraction")
    axes[1].set_ylim(0.0, 1.0)
    axes[1].set_title("If Bullet forces stars to out-weight gas")
    axes[1].legend(frameon=False, fontsize=8, loc="lower right")

    fig.tight_layout()
    fig.savefig(PLOT_PATH, dpi=180, bbox_inches="tight")
    plt.close(fig)

    return {
        "beta_grid": beta_grid.tolist(),
        "coarse_grained_gas_to_bcg_ratio": gas_to_bcg.tolist(),
        "eta_grid": eta_grid.tolist(),
    }


def build_summary() -> dict[str, object]:
    constraints = BulletConstraints()
    sources = SourceLinks()

    global_eta_required = required_phase_weight_ratio(
        constraints.global_star_fraction,
        constraints.global_gas_fraction,
    )
    local_eta_required = constraints.local_plasma_to_bcg_baryon_ratio

    gas_rich_examples = {}
    for raw_star_fraction in (0.10, 0.20, 0.50):
        key = f"{int(raw_star_fraction * 100)}pct_stars"
        gas_rich_examples[key] = {
            "raw_star_fraction": raw_star_fraction,
            "effective_star_fraction_eta_1": effective_star_fraction(raw_star_fraction, 1.0),
            "effective_star_fraction_eta_2": effective_star_fraction(raw_star_fraction, 2.0),
            "effective_star_fraction_eta_9": effective_star_fraction(raw_star_fraction, 9.0),
            "effective_star_fraction_eta_30": effective_star_fraction(raw_star_fraction, 30.0),
        }

    microscopic_density_contrasts = {
        "1e20": 1e20,
        "1e24": 1e24,
        "1e30": 1e30,
    }
    beta_requirements = {
        key: {
            "beta_for_eta_2": beta_required(local_eta_required, value),
            "beta_for_eta_9": beta_required(global_eta_required, value),
            "beta_for_eta_10": beta_required(10.0, value),
        }
        for key, value in microscopic_density_contrasts.items()
    }

    plot_data = make_plot(
        constraints.local_plasma_to_bcg_baryon_ratio,
        global_eta_required,
        local_eta_required,
    )

    coarse_model_no_go = {
        "model": "rho_sh = rho_b * (rho_bar_lambda / rho0)^beta, beta >= 0",
        "peak_source_scaling": "S_lambda ~ M_lambda^(1+beta) / V_lambda^beta",
        "bullet_local_ratio": constraints.local_plasma_to_bcg_baryon_ratio,
        "predicted_gas_to_bcg_ratio_beta_0": constraints.local_plasma_to_bcg_baryon_ratio ** 1.0,
        "predicted_gas_to_bcg_ratio_beta_1": constraints.local_plasma_to_bcg_baryon_ratio ** 2.0,
        "predicted_gas_to_bcg_ratio_beta_2": constraints.local_plasma_to_bcg_baryon_ratio ** 3.0,
        "verdict": "impossible_to_move_peak_from_gas_to_bcg",
    }

    phase_weighted_model = {
        "model": "rho_sh = eta_phase * rho_b, with eta_star / eta_gas = eta",
        "eta_required_global_from_90_10_split": global_eta_required,
        "eta_required_local_from_2_to_1_plasma_excess": local_eta_required,
        "gas_rich_examples": gas_rich_examples,
        "verdict": "can_save_bullet_only_by_making_stars_dominate_gas_elsewhere",
    }

    return {
        "sources": asdict(sources),
        "bullet_constraints": asdict(constraints),
        "candidate_law": {
            "coarse_grained_density": "rho_bar_lambda(x) = integral G_lambda(x-x') rho_b(x') d^3x'",
            "effective_shielding_source": "rho_sh(x) = rho_b(x) * (rho_bar_lambda/ rho0)^beta * eta_phase",
            "projected_lensing_proxy": "Sigma_sh(x_perp) = integral rho_sh(x_perp, z) dz",
        },
        "coarse_grained_monotone_result": coarse_model_no_go,
        "phase_weighted_result": phase_weighted_model,
        "microscopic_density_power_law_requirements": beta_requirements,
        "plot_data": plot_data,
        "bottom_line": {
            "coarse_grained_universal_law": "ruled_out_by_local_bullet_ordering",
            "microscopic_density_weighting": "requires_star_over_gas_weight_ratio_of_at_least_9",
            "overall": "minimal_shadow_models_fail_or_become_pathological",
        },
    }


def write_report(summary: dict[str, object]) -> None:
    constraints = summary["bullet_constraints"]
    coarse = summary["coarse_grained_monotone_result"]
    phase = summary["phase_weighted_result"]
    beta_requirements = summary["microscopic_density_power_law_requirements"]
    sources = summary["sources"]

    report = f"""# Bullet Cluster Shadow Test

## Goal

Write down the simplest explicit shielding law that matches the "gravity as expansion shadow"
intuition, then see whether that law can put the Bullet Cluster lensing peaks on the galaxies
instead of on the hot gas.

## Observational inputs

- Clowe et al. 2007 summarize the Bullet Cluster lensing result as lensing aligned with the
  galaxies, which are roughly `10%` of the observed baryons, rather than the X-ray plasma, which
  is roughly `90%`: <{sources["clowe_2007"]}>
- Clowe et al. 2006 report an `8 sigma` offset between the total-mass and baryonic-gas centroids:
  <{sources["clowe_2006"]}>
- The same 2006 paper states that, in the subcluster, the total visible mass at the plasma peak is
  greater by a factor of about `2` than at the BCG, yet the lensing peak sits near the BCG:
  <{sources["clowe_2006_pdf_snippet"]}>

These two facts are the core constraint:

1. **Global**: stars must out-weight gas enough to overcome a `90/10` gas/star split.
2. **Local**: at the relevant subcluster peak, the theory must invert a `2:1` baryonic ordering so
   that the BCG beats the plasma peak.

## Candidate shielding law

Use a projected shielding source instead of bare baryonic column density:

```text
rho_bar_lambda(x) = integral G_lambda(x-x') rho_b(x') d^3x'
rho_sh(x) = rho_b(x) * (rho_bar_lambda(x) / rho0)^beta * eta_phase
Sigma_sh(x_perp) = integral rho_sh(x_perp, z) dz
```

Interpretation:

- `G_lambda` is a smoothing kernel that sets the geometric shielding scale.
- `beta >= 0` measures how strongly denser regions shield more effectively per unit baryonic mass.
- `eta_phase` is an optional phase factor that can distinguish stars from hot gas.

This is the smallest family I know how to write that still encodes your premise:
mass blocks expansion, denser matter may block it more, and the result can be geometry-dependent.

## Family 1: coarse-grained monotone shielding

Set `eta_phase = 1`, so the only enhancement comes from cluster-scale density:

```text
rho_sh = rho_b * (rho_bar_lambda / rho0)^beta
```

Inside one smoothing kernel of volume `V_lambda`, the effective source scales like

```text
S_lambda ~ M_lambda * (M_lambda / V_lambda)^beta
         ~ M_lambda^(1+beta) / V_lambda^beta
```

So if the plasma peak already contains more baryonic mass than the BCG on the same smoothing scale,
then any monotone `beta >= 0` makes the plasma peak at least as strong and usually stronger.

With the Bullet local ratio `M_plasma / M_BCG ~= {constraints["local_plasma_to_bcg_baryon_ratio"]:.1f}`:

- `beta = 0` gives `S_plasma / S_BCG = {coarse["predicted_gas_to_bcg_ratio_beta_0"]:.1f}`
- `beta = 1` gives `S_plasma / S_BCG = {coarse["predicted_gas_to_bcg_ratio_beta_1"]:.1f}`
- `beta = 2` gives `S_plasma / S_BCG = {coarse["predicted_gas_to_bcg_ratio_beta_2"]:.1f}`

That means **no coarse-grained monotone shielding law can move the peak from the plasma to the
BCG** once the plasma already wins on the relevant baryonic smoothing scale.

## Family 2: microscopic phase weighting

To rescue the Bullet Cluster, you have to let stars count more than hot gas per unit baryonic mass:

```text
rho_sh = eta_phase * rho_b
eta = eta_star / eta_gas
```

Bullet then requires at least:

- `eta > {phase["eta_required_global_from_90_10_split"]:.1f}` from the global `90/10` gas/star split
- `eta > {phase["eta_required_local_from_2_to_1_plasma_excess"]:.1f}` from the local `2:1` plasma excess

The global requirement is the real killer. If `eta ~= 9`, then a galaxy that is `90%` gas and `10%`
stars stops behaving like a gas-dominated system at all. Its effective stellar fraction becomes
`50%`.

This matters because gas-rich galaxies are one of the standard clean MOND-style tests:
<{sources["gas_rich_btfr"]}>

So a universal phase-weighted rule that rescues Bullet pushes directly against the gas-rich-galaxy
motivation behind the whole MOND-like phenomenology.

## If the phase weighting comes from microscopic density

Suppose the phase factor itself comes from a weak density law:

```text
eta = (rho_star / rho_gas)^beta
```

For plausible microscopic density contrasts:

- `rho_star / rho_gas ~ 1e20` needs only `beta = {beta_requirements["1e20"]["beta_for_eta_9"]:.3f}` to reach `eta = 9`
- `rho_star / rho_gas ~ 1e24` needs only `beta = {beta_requirements["1e24"]["beta_for_eta_9"]:.3f}` to reach `eta = 9`
- `rho_star / rho_gas ~ 1e30` needs only `beta = {beta_requirements["1e30"]["beta_for_eta_9"]:.3f}` to reach `eta = 9`

So the microscopic-density escape hatch is too efficient. Even an extremely weak density dependence
already makes stars dominate over gas by the amount Bullet needs.

## What this means

The Bullet Cluster does not yet prove that every imaginable "expansion shadow" model is impossible.
But it **does** kill the two obvious minimal families:

1. **Cluster-scale monotone shielding** fails immediately because the plasma peak already beats the
   BCG in visible baryons locally.
2. **Microscopic phase-weighted shielding** can rescue Bullet only by making stars dominate over
   gas so strongly that gas-rich galaxy phenomenology becomes hard to preserve.

## Bottom line

My best current read is:

- The simplest explicit shielding law is now written down.
- The natural coarse-grained version is ruled out by Bullet.
- The natural microscopic rescue becomes pathological almost immediately.

That leaves the theory in a bad place. To keep going, you would need a **third ingredient** beyond
"denser matter shields more":

- a non-universal shock/temperature dependence,
- a history-dependent merger effect,
- or a second field that changes how shielding gravitates.

At that point, the theory is no longer a simple expansion-shadow mechanism. It becomes a tuned
cluster-specific model.
"""
    REPORT_PATH.write_text(report)


def main() -> None:
    PROCESSED_ROOT.mkdir(parents=True, exist_ok=True)
    PLOT_ROOT.mkdir(parents=True, exist_ok=True)
    NOTE_ROOT.mkdir(parents=True, exist_ok=True)

    summary = build_summary()
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2))
    write_report(summary)


if __name__ == "__main__":
    main()

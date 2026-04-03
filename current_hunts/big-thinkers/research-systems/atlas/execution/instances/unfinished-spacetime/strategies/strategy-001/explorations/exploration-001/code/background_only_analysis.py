#!/usr/bin/env python3
"""Background-only screening for late-time dark-energy deformations.

This script is intentionally small and transparent. It is designed to answer:

1. Can we score LCDM, constant-w, CPL, and a smooth-step w(z) model
   on simple BAO and SN summary data?
2. Does the pipeline behave sensibly on synthetic data before real data
   is plugged in?

It is not a replacement for Cobaya/CLASS or official Planck/ACT likelihoods.
Those belong in the next stage if this screen survives.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

import numpy as np

C_LIGHT_KM_S = 299792.458


@dataclass(frozen=True)
class SNPoint:
    z: float
    mu: float
    sigma: float


@dataclass(frozen=True)
class BAOPoint:
    z: float
    observable: str
    value: float
    sigma: float


@dataclass(frozen=True)
class BackgroundCache:
    z_grid: np.ndarray
    e_grid: np.ndarray
    d_c_grid: np.ndarray


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--models",
        nargs="+",
        default=["lcdm", "wcdm", "cpl", "step"],
        choices=["lcdm", "wcdm", "cpl", "step"],
        help="Model ladder to evaluate.",
    )
    parser.add_argument("--sn-csv", type=Path, help="SN summary CSV path.")
    parser.add_argument("--bao-csv", type=Path, help="BAO summary CSV path.")
    parser.add_argument(
        "--bao-cov",
        type=Path,
        help="Optional full BAO covariance matrix aligned to --bao-csv row order.",
    )
    parser.add_argument(
        "--rd-mpc",
        type=float,
        default=147.09,
        help="Fixed sound horizon in Mpc for the first-pass BAO screen.",
    )
    parser.add_argument(
        "--step-delta-z",
        type=float,
        default=0.15,
        help="Fixed logistic step width for the step model.",
    )
    parser.add_argument(
        "--grid-config",
        type=Path,
        help="Optional JSON override for coarse parameter grids.",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        help="Optional JSON file for best-fit summaries.",
    )
    parser.add_argument(
        "--self-check",
        action="store_true",
        help="Run against a tiny synthetic dataset instead of real inputs.",
    )
    return parser.parse_args()


def default_grid() -> Dict[str, List[float]]:
    return {
        "Omega_m": [0.26, 0.30, 0.34],
        "H0": [68.0, 70.0, 72.0],
        "w0": [-1.15, -1.0, -0.85],
        "wa": [-0.8, 0.0, 0.8],
        "A": [0.0, 0.15, 0.3],
        "z_t": [0.3, 0.6, 0.9],
    }


def load_grid_config(path: Path | None) -> Dict[str, List[float]]:
    grid = default_grid()
    if path is None:
        return grid
    with path.open() as fh:
        user_grid = json.load(fh)
    for key, values in user_grid.items():
        grid[key] = list(values)
    return grid


def load_sn_csv(path: Path) -> List[SNPoint]:
    rows: List[SNPoint] = []
    with path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        required = {"z", "mu", "sigma"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"{path} missing required SN columns {sorted(required)}")
        for row in reader:
            rows.append(SNPoint(z=float(row["z"]), mu=float(row["mu"]), sigma=float(row["sigma"])))
    if not rows:
        raise ValueError(f"{path} contains no SN rows")
    return rows


def load_bao_csv(path: Path) -> List[BAOPoint]:
    rows: List[BAOPoint] = []
    with path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        required = {"z", "observable", "value", "sigma"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"{path} missing required BAO columns {sorted(required)}")
        for row in reader:
            rows.append(
                BAOPoint(
                    z=float(row["z"]),
                    observable=row["observable"].strip(),
                    value=float(row["value"]),
                    sigma=float(row["sigma"]),
                )
            )
    if not rows:
        raise ValueError(f"{path} contains no BAO rows")
    return rows


def load_covariance_matrix(path: Path, expected_size: int) -> np.ndarray:
    matrix = np.loadtxt(path, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError(f"{path} is not a square covariance matrix")
    if matrix.shape[0] != expected_size:
        raise ValueError(
            f"{path} dimension {matrix.shape[0]} does not match BAO vector length {expected_size}"
        )
    return matrix


def w_of_z(model: str, z: float, params: Dict[str, float], delta_z: float) -> float:
    if model == "lcdm":
        return -1.0
    if model == "wcdm":
        return params["w0"]
    if model == "cpl":
        a = 1.0 / (1.0 + z)
        return params["w0"] + params["wa"] * (1.0 - a)
    if model == "step":
        return -1.0 + params["A"] / (1.0 + math.exp((z - params["z_t"]) / delta_z))
    raise ValueError(f"Unknown model {model}")


def w_of_z_array(model: str, z: np.ndarray, params: Dict[str, float], delta_z: float) -> np.ndarray:
    if model == "lcdm":
        return np.full_like(z, -1.0, dtype=float)
    if model == "wcdm":
        return np.full_like(z, params["w0"], dtype=float)
    if model == "cpl":
        a = 1.0 / (1.0 + z)
        return params["w0"] + params["wa"] * (1.0 - a)
    if model == "step":
        return -1.0 + params["A"] / (1.0 + np.exp((z - params["z_t"]) / delta_z))
    raise ValueError(f"Unknown model {model}")


def de_density_ratio(model: str, z: float, params: Dict[str, float], delta_z: float) -> float:
    if z <= 0.0:
        return 1.0
    if model == "lcdm":
        return 1.0
    if model == "wcdm":
        return (1.0 + z) ** (3.0 * (1.0 + params["w0"]))
    if model == "cpl":
        return (1.0 + z) ** (3.0 * (1.0 + params["w0"] + params["wa"])) * math.exp(
            -3.0 * params["wa"] * z / (1.0 + z)
        )
    grid = np.linspace(0.0, z, 150)
    integrand = np.array(
        [(1.0 + w_of_z(model, zi, params, delta_z)) / (1.0 + zi) for zi in grid],
        dtype=float,
    )
    return math.exp(3.0 * np.trapezoid(integrand, grid))


def de_density_ratio_array(
    model: str,
    z_grid: np.ndarray,
    params: Dict[str, float],
    delta_z: float,
) -> np.ndarray:
    if model == "lcdm":
        return np.ones_like(z_grid, dtype=float)
    if model == "wcdm":
        return (1.0 + z_grid) ** (3.0 * (1.0 + params["w0"]))
    if model == "cpl":
        return (1.0 + z_grid) ** (3.0 * (1.0 + params["w0"] + params["wa"])) * np.exp(
            -3.0 * params["wa"] * z_grid / (1.0 + z_grid)
        )
    w_grid = w_of_z_array(model, z_grid, params, delta_z)
    integrand = (1.0 + w_grid) / (1.0 + z_grid)
    integral = np.zeros_like(z_grid, dtype=float)
    if len(z_grid) > 1:
        dz = np.diff(z_grid)
        trapezoids = 0.5 * (integrand[1:] + integrand[:-1]) * dz
        integral[1:] = np.cumsum(trapezoids)
    return np.exp(3.0 * integral)


def e_z(model: str, z: float, params: Dict[str, float], delta_z: float) -> float:
    omega_m = params["Omega_m"]
    omega_de = 1.0 - omega_m
    return math.sqrt(omega_m * (1.0 + z) ** 3 + omega_de * de_density_ratio(model, z, params, delta_z))


def build_background_cache(
    model: str,
    params: Dict[str, float],
    delta_z: float,
    z_values: Sequence[float],
) -> BackgroundCache:
    z_grid = np.unique(np.concatenate((np.array([0.0], dtype=float), np.asarray(z_values, dtype=float))))
    omega_m = params["Omega_m"]
    omega_de = 1.0 - omega_m
    de_ratio = de_density_ratio_array(model, z_grid, params, delta_z)
    e_grid = np.sqrt(omega_m * (1.0 + z_grid) ** 3 + omega_de * de_ratio)
    d_c_grid = np.zeros_like(z_grid, dtype=float)
    if len(z_grid) > 1:
        dz = np.diff(z_grid)
        inv_e = 1.0 / e_grid
        trapezoids = 0.5 * (inv_e[1:] + inv_e[:-1]) * dz
        d_c_grid[1:] = (C_LIGHT_KM_S / params["H0"]) * np.cumsum(trapezoids)
    return BackgroundCache(z_grid=z_grid, e_grid=e_grid, d_c_grid=d_c_grid)


def comoving_distance_mpc(model: str, z: float, params: Dict[str, float], delta_z: float) -> float:
    if z <= 0.0:
        return 0.0
    grid = np.linspace(0.0, z, 300)
    integrand = np.array([1.0 / e_z(model, zi, params, delta_z) for zi in grid], dtype=float)
    return (C_LIGHT_KM_S / params["H0"]) * np.trapezoid(integrand, grid)


def luminosity_distance_mpc(model: str, z: float, params: Dict[str, float], delta_z: float) -> float:
    return (1.0 + z) * comoving_distance_mpc(model, z, params, delta_z)


def distance_modulus(model: str, z: float, params: Dict[str, float], delta_z: float) -> float:
    d_l = luminosity_distance_mpc(model, z, params, delta_z)
    return 5.0 * math.log10(d_l) + 25.0


def bao_prediction(
    point: BAOPoint,
    model: str,
    params: Dict[str, float],
    delta_z: float,
    rd_mpc: float,
) -> float:
    d_m = comoving_distance_mpc(model, point.z, params, delta_z)
    d_h = C_LIGHT_KM_S / (params["H0"] * e_z(model, point.z, params, delta_z))
    if point.observable == "DM_over_rd":
        return d_m / rd_mpc
    if point.observable == "DH_over_rd":
        return d_h / rd_mpc
    if point.observable == "DV_over_rd":
        d_v = (point.z * d_m * d_m * d_h) ** (1.0 / 3.0)
        return d_v / rd_mpc
    raise ValueError(f"Unsupported BAO observable {point.observable}")


def fit_sn_offset(sn_points: Sequence[SNPoint], mu_model: np.ndarray) -> float:
    weights = np.array([1.0 / (p.sigma * p.sigma) for p in sn_points], dtype=float)
    mu_obs = np.array([p.mu for p in sn_points], dtype=float)
    return float(np.sum(weights * (mu_obs - mu_model)) / np.sum(weights))


def sn_mu_from_cache(sn_points: Sequence[SNPoint], cache: BackgroundCache) -> np.ndarray:
    z = np.array([p.z for p in sn_points], dtype=float)
    indices = np.searchsorted(cache.z_grid, z)
    d_l = (1.0 + z) * cache.d_c_grid[indices]
    return 5.0 * np.log10(d_l) + 25.0


def chi2_sn(
    sn_points: Sequence[SNPoint],
    model: str,
    params: Dict[str, float],
    delta_z: float,
) -> Dict[str, float]:
    mu_model = np.array([distance_modulus(model, p.z, params, delta_z) for p in sn_points], dtype=float)
    offset = fit_sn_offset(sn_points, mu_model)
    mu_obs = np.array([p.mu for p in sn_points], dtype=float)
    sigma = np.array([p.sigma for p in sn_points], dtype=float)
    residual = (mu_obs - (mu_model + offset)) / sigma
    return {"chi2": float(np.sum(residual * residual)), "mu_offset": offset}


def chi2_sn_from_cache(sn_points: Sequence[SNPoint], cache: BackgroundCache) -> Dict[str, float]:
    mu_model = sn_mu_from_cache(sn_points, cache)
    offset = fit_sn_offset(sn_points, mu_model)
    mu_obs = np.array([p.mu for p in sn_points], dtype=float)
    sigma = np.array([p.sigma for p in sn_points], dtype=float)
    residual = (mu_obs - (mu_model + offset)) / sigma
    return {"chi2": float(np.sum(residual * residual)), "mu_offset": offset}


def chi2_bao(
    bao_points: Sequence[BAOPoint],
    model: str,
    params: Dict[str, float],
    delta_z: float,
    rd_mpc: float,
) -> float:
    total = 0.0
    for point in bao_points:
        pred = bao_prediction(point, model, params, delta_z, rd_mpc)
        total += ((point.value - pred) / point.sigma) ** 2
    return total


def chi2_bao_from_cache(
    bao_points: Sequence[BAOPoint],
    cache: BackgroundCache,
    params: Dict[str, float],
    rd_mpc: float,
    precision: np.ndarray | None = None,
) -> float:
    residuals = []
    for point in bao_points:
        index = int(np.searchsorted(cache.z_grid, point.z))
        d_m = float(cache.d_c_grid[index])
        d_h = C_LIGHT_KM_S / (params["H0"] * float(cache.e_grid[index]))
        if point.observable == "DM_over_rd":
            pred = d_m / rd_mpc
        elif point.observable == "DH_over_rd":
            pred = d_h / rd_mpc
        elif point.observable == "DV_over_rd":
            pred = (point.z * d_m * d_m * d_h) ** (1.0 / 3.0) / rd_mpc
        else:
            raise ValueError(f"Unsupported BAO observable {point.observable}")
        residuals.append(point.value - pred)
    residual = np.array(residuals, dtype=float)
    if precision is not None:
        return float(residual @ precision @ residual)
    sigma = np.array([point.sigma for point in bao_points], dtype=float)
    scaled = residual / sigma
    return float(np.sum(scaled * scaled))


def parameter_grid(model: str, grid: Dict[str, List[float]]) -> Iterable[Dict[str, float]]:
    if model == "lcdm":
        keys = ["Omega_m", "H0"]
    elif model == "wcdm":
        keys = ["Omega_m", "H0", "w0"]
    elif model == "cpl":
        keys = ["Omega_m", "H0", "w0", "wa"]
    elif model == "step":
        keys = ["Omega_m", "H0", "A", "z_t"]
    else:
        raise ValueError(f"Unknown model {model}")
    for values in itertools.product(*(grid[key] for key in keys)):
        yield dict(zip(keys, values))


def parameter_count(model: str) -> int:
    return {
        "lcdm": 2,
        "wcdm": 3,
        "cpl": 4,
        "step": 4,
    }[model]


def model_summary(
    model: str,
    sn_points: Sequence[SNPoint],
    bao_points: Sequence[BAOPoint],
    grid: Dict[str, List[float]],
    delta_z: float,
    rd_mpc: float,
    bao_precision: np.ndarray | None = None,
) -> Dict[str, object]:
    best: Dict[str, object] | None = None
    z_values = [p.z for p in sn_points] + [p.z for p in bao_points]
    for params in parameter_grid(model, grid):
        cache = build_background_cache(model, params, delta_z, z_values)
        sn_fit = chi2_sn_from_cache(sn_points, cache) if sn_points else {"chi2": 0.0, "mu_offset": 0.0}
        bao_fit = (
            chi2_bao_from_cache(bao_points, cache, params, rd_mpc, precision=bao_precision)
            if bao_points
            else 0.0
        )
        total = float(sn_fit["chi2"]) + float(bao_fit)
        if best is None or total < float(best["chi2_total"]):
            best = {
                "model": model,
                "params": params,
                "chi2_sn": float(sn_fit["chi2"]),
                "chi2_bao": float(bao_fit),
                "chi2_total": total,
                "mu_offset": float(sn_fit["mu_offset"]),
            }
    assert best is not None
    n_points = len(sn_points) + len(bao_points)
    k = parameter_count(model) + (1 if sn_points else 0)
    best["aic"] = float(best["chi2_total"]) + 2.0 * k
    best["bic"] = float(best["chi2_total"]) + k * math.log(max(n_points, 1))
    return best


def generate_synthetic_data() -> tuple[List[SNPoint], List[BAOPoint]]:
    params = {"Omega_m": 0.30, "H0": 70.0}
    sn_z = [0.03, 0.08, 0.15, 0.35, 0.6, 1.0]
    sn_points = [
        SNPoint(z=z, mu=distance_modulus("lcdm", z, params, 0.15) - 19.25, sigma=0.12)
        for z in sn_z
    ]
    bao_points = [
        BAOPoint(z=0.35, observable="DM_over_rd", value=bao_prediction(BAOPoint(0.35, "DM_over_rd", 0.0, 1.0), "lcdm", params, 0.15, 147.09), sigma=0.8),
        BAOPoint(z=0.35, observable="DH_over_rd", value=bao_prediction(BAOPoint(0.35, "DH_over_rd", 0.0, 1.0), "lcdm", params, 0.15, 147.09), sigma=0.4),
        BAOPoint(z=0.8, observable="DM_over_rd", value=bao_prediction(BAOPoint(0.8, "DM_over_rd", 0.0, 1.0), "lcdm", params, 0.15, 147.09), sigma=1.0),
    ]
    return sn_points, bao_points


def print_results(results: Sequence[Dict[str, object]]) -> None:
    print("Model comparison")
    print("=" * 72)
    for item in sorted(results, key=lambda x: float(x["chi2_total"])):
        params_str = ", ".join(f"{k}={v}" for k, v in item["params"].items())
        print(
            f"{item['model']:>5}  "
            f"chi2={item['chi2_total']:.3f}  "
            f"AIC={item['aic']:.3f}  "
            f"BIC={item['bic']:.3f}  "
            f"params: {params_str}"
        )


def main() -> None:
    args = parse_args()
    grid = load_grid_config(args.grid_config)

    if args.self_check:
        sn_points, bao_points = generate_synthetic_data()
    else:
        sn_points = load_sn_csv(args.sn_csv) if args.sn_csv else []
        bao_points = load_bao_csv(args.bao_csv) if args.bao_csv else []
        if not sn_points and not bao_points:
            raise SystemExit("Provide --self-check or at least one of --sn-csv / --bao-csv")
    bao_precision = None
    if args.bao_cov:
        if not bao_points:
            raise SystemExit("--bao-cov requires --bao-csv")
        bao_cov = load_covariance_matrix(args.bao_cov, len(bao_points))
        bao_precision = np.linalg.inv(bao_cov)

    results = [
        model_summary(
            model=model,
            sn_points=sn_points,
            bao_points=bao_points,
            grid=grid,
            delta_z=args.step_delta_z,
            rd_mpc=args.rd_mpc,
            bao_precision=bao_precision,
        )
        for model in args.models
    ]

    print_results(results)

    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        with args.output_json.open("w") as fh:
            json.dump(results, fh, indent=2)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Iterable

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output"
PLOTS_DIR = ROOT / "plots"
MC_SAMPLES = 10_000
MC_SEED = 20260402
HIT_THRESHOLDS = (0.01, 0.001, 0.0001)


@dataclass(frozen=True)
class Parameter:
    key: str
    label: str
    value: float
    uncertainty: float | None
    uncertainty_text: str | None
    unit: str
    category: str
    source_url: str
    note: str = ""


@dataclass(frozen=True)
class Target:
    label: str
    value: float


@dataclass
class RelationHit:
    family: str
    relation: str
    value: float
    target_label: str
    target_value: float
    relative_error: float
    note: str = ""

    @property
    def percent_error(self) -> float:
        return 100.0 * self.relative_error


def ensure_dirs() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)


def angle_deg_from_sin(sine_value: float) -> float:
    return math.degrees(math.asin(sine_value))


def angle_deg_from_sin2(sine_squared: float) -> float:
    return math.degrees(math.asin(math.sqrt(sine_squared)))


def sym_uncertainty_from_inverse(x_inv: float, dx_inv: float) -> float:
    return dx_inv / (x_inv * x_inv)


def build_parameters() -> list[Parameter]:
    leptons_url = "https://pdg.lbl.gov/2025/tables/rpp2025-sum-leptons.pdf"
    quarks_url = "https://pdg.lbl.gov/2025/tables/rpp2025-sum-quarks.pdf"
    gauge_url = "https://pdg.lbl.gov/2025/tables/rpp2025-sum-gauge-higgs-bosons.pdf"
    ckm_url = "https://pdg.lbl.gov/2025/reviews/rpp2025-rev-ckm-matrix.pdf"
    sm_url = "https://pdg.lbl.gov/2025/reviews/rpp2025-rev-standard-model.pdf"
    qcd_url = "https://pdg.lbl.gov/2025/reviews/rpp2025-rev-qcd.pdf"

    ckm_s12 = 0.22501
    ckm_s23 = 0.04183
    ckm_s13 = 0.003732
    ckm_theta12 = angle_deg_from_sin(ckm_s12)
    ckm_theta23 = angle_deg_from_sin(ckm_s23)
    ckm_theta13 = angle_deg_from_sin(ckm_s13)

    pmns_s12_sq = 0.307
    pmns_s23_sq = 0.534
    pmns_s13_sq = 0.0216
    pmns_theta12 = angle_deg_from_sin2(pmns_s12_sq)
    pmns_theta23 = angle_deg_from_sin2(pmns_s23_sq)
    pmns_theta13 = angle_deg_from_sin2(pmns_s13_sq)

    alpha_em_inv = 127.930
    alpha_em_inv_unc = 0.008
    alpha_em = 1.0 / alpha_em_inv
    alpha_em_unc = sym_uncertainty_from_inverse(alpha_em_inv, alpha_em_inv_unc)

    g_f = 1.1663785e-5
    g_f_unc = 6.0e-12
    v = (math.sqrt(2.0) * g_f) ** -0.5
    v_unc = 0.5 * v * (g_f_unc / g_f)

    return [
        Parameter("m_e", "m_e", 0.00051099895, 1.5e-13, "1.5e-13", "GeV", "mass", leptons_url),
        Parameter("m_mu", "m_mu", 0.1056583755, 2.3e-9, "2.3e-9", "GeV", "mass", leptons_url),
        Parameter("m_tau", "m_tau", 1.77693, 9.0e-5, "9e-5", "GeV", "mass", leptons_url),
        Parameter("m_u", "m_u", 0.00216, 7.0e-5, "7e-5 (CL=90%)", "GeV", "mass", quarks_url),
        Parameter("m_d", "m_d", 0.00470, 7.0e-5, "7e-5 (CL=90%)", "GeV", "mass", quarks_url),
        Parameter("m_s", "m_s", 0.0935, 8.0e-4, "8e-4 (CL=90%)", "GeV", "mass", quarks_url),
        Parameter("m_c", "m_c", 1.2730, 0.0046, "0.0046 (CL=90%)", "GeV", "mass", quarks_url),
        Parameter("m_b", "m_b", 4.183, 0.007, "0.007 (CL=90%)", "GeV", "mass", quarks_url),
        Parameter("m_t", "m_t", 172.56, 0.31, "0.31", "GeV", "mass", quarks_url, note="Direct-measurement mass entry."),
        Parameter("dm2_21", "Delta m^2_21", 7.50e-5, 0.19e-5, "0.19e-5", "eV^2", "delta_m2", leptons_url, note="Normal ordering."),
        Parameter("dm2_32_abs", "|Delta m^2_32|", 2.451e-3, 0.026e-3, "0.026e-3", "eV^2", "delta_m2", leptons_url, note="Normal ordering absolute value."),
        Parameter("theta12_ckm_deg", "theta_12^CKM", ckm_theta12, None, "derived from sin theta_12 = 0.22501 +/- 0.00068", "deg", "angle", ckm_url),
        Parameter("theta23_ckm_deg", "theta_23^CKM", ckm_theta23, None, "derived from sin theta_23 = 0.04183 +0.00079/-0.00069", "deg", "angle", ckm_url),
        Parameter("theta13_ckm_deg", "theta_13^CKM", ckm_theta13, None, "derived from sin theta_13 = 0.003732 +0.000090/-0.000085", "deg", "angle", ckm_url),
        Parameter("theta12_pmns_deg", "theta_12^PMNS", pmns_theta12, None, "derived from sin^2 theta_12 = 0.307 +/- 0.012", "deg", "angle", leptons_url),
        Parameter("theta23_pmns_deg", "theta_23^PMNS", pmns_theta23, None, "derived from sin^2 theta_23 = 0.534 +0.015/-0.019", "deg", "angle", leptons_url, note="Prompt value 49.0 deg is not the 2025 PDG central value."),
        Parameter("theta13_pmns_deg", "theta_13^PMNS", pmns_theta13, None, "derived from sin^2 theta_13 = 0.0216 +/- 0.0006", "deg", "angle", leptons_url),
        Parameter("alpha_em_MZ", "alpha_em(M_Z)", alpha_em, alpha_em_unc, f"{alpha_em_unc:.2e}", "dimensionless", "coupling", sm_url, note="Using PDG MS-like alpha^(5)(M_Z)^-1 = 127.930 +/- 0.008; prompt rounded to 1/127.95."),
        Parameter("alpha_s_MZ", "alpha_s(M_Z)", 0.1180, 0.0009, "0.0009", "dimensionless", "coupling", qcd_url),
        Parameter("sin2_thetaW", "sin^2 theta_W", 0.23122, 0.00006, "0.00006", "dimensionless", "coupling", sm_url, note="PDG effective weak mixing-angle table entry."),
        Parameter("M_W", "M_W", 80.3692, 0.0133, "0.0133", "GeV", "mass", gauge_url),
        Parameter("M_Z", "M_Z", 91.1880, 0.0020, "0.0020", "GeV", "mass", gauge_url),
        Parameter("M_H", "M_H", 125.20, 0.11, "0.11", "GeV", "mass", gauge_url),
        Parameter("G_F", "G_F", g_f, g_f_unc, "6e-12", "GeV^-2", "constant", sm_url),
        Parameter("v", "v", v, v_unc, f"{v_unc:.2e}", "GeV", "mass", sm_url, note="Derived from G_F via v = (sqrt(2) G_F)^(-1/2); not an independent parameter."),
    ]


def build_target_map() -> tuple[list[Target], list[Target], list[Target]]:
    def add_target(store: dict[float, str], label: str, value: float, min_value: float | None = None, max_value: float | None = None) -> None:
        if min_value is not None and value < min_value:
            return
        if max_value is not None and value > max_value:
            return
        key = round(float(value), 15)
        if key not in store:
            store[key] = label

    koide_store: dict[float, str] = {}
    simple_store: dict[float, str] = {}
    ratio_store: dict[float, str] = {}

    for numerator in range(1, 14):
        for denominator in range(1, 14):
            frac = Fraction(numerator, denominator)
            label = f"{frac.numerator}/{frac.denominator}" if frac.denominator != 1 else str(frac.numerator)
            value = float(frac)
            add_target(simple_store, label, value, min_value=1.0 / 13.0, max_value=13.0)
            add_target(ratio_store, label, value, min_value=1.0, max_value=200.0)
            add_target(koide_store, label, value, min_value=1.0 / 3.0, max_value=1.0)

    extras = {
        "pi": math.pi,
        "e": math.e,
        "sqrt(2)": math.sqrt(2.0),
        "sqrt(3)": math.sqrt(3.0),
        "sqrt(5)": math.sqrt(5.0),
        "sqrt(pi)": math.sqrt(math.pi),
        "sqrt(e)": math.sqrt(math.e),
    }
    for label, value in extras.items():
        add_target(simple_store, label, value, min_value=1.0 / 13.0, max_value=13.0)
        add_target(ratio_store, label, value, min_value=1.0, max_value=200.0)

    scalar_factors = [Fraction(1, 2), Fraction(2, 3), Fraction(3, 2), Fraction(2, 1), Fraction(3, 1), Fraction(4, 1), Fraction(5, 1), Fraction(6, 1), Fraction(8, 1), Fraction(10, 1)]
    for frac in scalar_factors:
        scale = float(frac)
        scale_label = f"{frac.numerator}/{frac.denominator}" if frac.denominator != 1 else str(frac.numerator)
        for base_label, base_value in extras.items():
            add_target(simple_store, f"{scale_label}*{base_label}", scale * base_value, min_value=1.0 / 13.0, max_value=13.0)
            add_target(ratio_store, f"{scale_label}*{base_label}", scale * base_value, min_value=1.0, max_value=200.0)

    for integer in range(1, 201):
        add_target(ratio_store, str(integer), float(integer), min_value=1.0, max_value=200.0)

    for base in (2, 3, 5, 10):
        value = float(base)
        exponent = 1
        while value <= 1.0e6:
            add_target(ratio_store, f"{base}^{exponent}", value, min_value=1.0, max_value=1.0e6)
            exponent += 1
            value *= base

    def freeze(store: dict[float, str]) -> list[Target]:
        return [Target(label=store[key], value=key) for key in sorted(store)]

    return freeze(koide_store), freeze(simple_store), freeze(ratio_store)


def build_parameter_lookup(parameters: Iterable[Parameter]) -> dict[str, Parameter]:
    return {parameter.key: parameter for parameter in parameters}


def best_target(values: np.ndarray, targets: list[Target]) -> tuple[np.ndarray, np.ndarray]:
    target_values = np.array([target.value for target in targets], dtype=float)
    rel_errors = np.abs(values[:, None] - target_values[None, :]) / target_values[None, :]
    best_indices = np.argmin(rel_errors, axis=1)
    best_errors = rel_errors[np.arange(values.size), best_indices]
    return best_indices, best_errors


def koide_triplet_values(source_values: np.ndarray, triples: np.ndarray) -> np.ndarray:
    subset = source_values[triples]
    return subset.sum(axis=1) / np.square(np.sqrt(subset).sum(axis=1))


def format_float(value: float) -> str:
    if value == 0:
        return "0"
    if abs(value) >= 1.0e4 or abs(value) < 1.0e-4:
        return f"{value:.6e}"
    return f"{value:.12g}"


def prompt_koide_value() -> tuple[float, float]:
    masses = np.array([0.000510999, 0.105658, 1.77686], dtype=float)
    value = float(masses.sum() / np.square(np.sqrt(masses).sum()))
    rel_error = abs(value - (2.0 / 3.0)) / (2.0 / 3.0)
    return value, rel_error


def current_koide_value(parameters: dict[str, Parameter]) -> tuple[float, float]:
    masses = np.array([parameters["m_e"].value, parameters["m_mu"].value, parameters["m_tau"].value], dtype=float)
    value = float(masses.sum() / np.square(np.sqrt(masses).sum()))
    rel_error = abs(value - (2.0 / 3.0)) / (2.0 / 3.0)
    return value, rel_error


def build_systematic_model(parameters: dict[str, Parameter]) -> dict[str, object]:
    core_keys = [
        "m_e",
        "m_mu",
        "m_tau",
        "m_u",
        "m_d",
        "m_s",
        "m_c",
        "m_b",
        "m_t",
        "dm2_21",
        "dm2_32_abs",
        "theta12_ckm_deg",
        "theta23_ckm_deg",
        "theta13_ckm_deg",
        "theta12_pmns_deg",
        "theta23_pmns_deg",
        "theta13_pmns_deg",
        "alpha_em_MZ",
        "alpha_s_MZ",
        "sin2_thetaW",
        "M_W",
        "M_Z",
        "M_H",
        "G_F",
        "v",
    ]
    mass_keys = [
        "m_e",
        "m_mu",
        "m_tau",
        "m_u",
        "m_d",
        "m_s",
        "m_c",
        "m_b",
        "m_t",
        "M_W",
        "M_Z",
        "M_H",
        "v",
    ]
    ratio_groups = {
        "mass_ratios": mass_keys,
        "angle_ratios_deg": [
            "theta12_ckm_deg",
            "theta23_ckm_deg",
            "theta13_ckm_deg",
            "theta12_pmns_deg",
            "theta23_pmns_deg",
            "theta13_pmns_deg",
        ],
        "coupling_ratios": ["alpha_em_MZ", "alpha_s_MZ", "sin2_thetaW"],
        "delta_m2_ratios": ["dm2_21", "dm2_32_abs"],
    }
    sum_rule_subsets = {
        "charged_leptons": ["m_e", "m_mu", "m_tau"],
        "up_type_quarks": ["m_u", "m_c", "m_t"],
        "down_type_quarks": ["m_d", "m_s", "m_b"],
        "gauge_higgs": ["M_W", "M_Z", "M_H"],
        "all_quarks": ["m_u", "m_d", "m_s", "m_c", "m_b", "m_t"],
        "all_fermion_masses": ["m_e", "m_mu", "m_tau", "m_u", "m_d", "m_s", "m_c", "m_b", "m_t"],
        "all_masses": mass_keys,
    }
    exponents = (-1.0, -0.5, 0.0, 0.5, 1.0, 2.0)

    return {
        "core_keys": core_keys,
        "mass_keys": mass_keys,
        "raw_triples": np.array(list(combinations(range(len(core_keys)), 3)), dtype=int),
        "mass_triples": np.array(list(combinations(range(len(mass_keys)), 3)), dtype=int),
        "ratio_groups": ratio_groups,
        "sum_rule_subsets": sum_rule_subsets,
        "exponents": exponents,
        "pmns_sin2": np.array([0.307, 0.534, 0.0216], dtype=float),
        "ckm_sin2": np.array([0.22501**2, 0.04183**2, 0.003732**2], dtype=float),
    }


def parameter_vector(parameters: dict[str, Parameter] | dict[str, float], keys: list[str]) -> np.ndarray:
    sample_value = next(iter(parameters.values()))
    if isinstance(sample_value, Parameter):
        return np.array([parameters[key].value for key in keys], dtype=float)  # type: ignore[index]
    return np.array([parameters[key] for key in keys], dtype=float)  # type: ignore[index]


def summarize_thresholds(errors: np.ndarray) -> dict[str, int]:
    return {
        "lt_1pct": int(np.count_nonzero(errors < 0.01)),
        "lt_0p1pct": int(np.count_nonzero(errors < 0.001)),
        "lt_0p01pct": int(np.count_nonzero(errors < 0.0001)),
    }


def systematic_search(
    parameters: dict[str, Parameter] | dict[str, float],
    model: dict[str, object],
    koide_targets: list[Target],
    simple_targets: list[Target],
    ratio_targets: list[Target],
    collect_hits: bool,
) -> tuple[list[RelationHit], dict[str, object]]:
    hits: list[RelationHit] = []
    trial_count = 0
    threshold_counts = {"lt_1pct": 0, "lt_0p1pct": 0, "lt_0p01pct": 0}
    family_min_errors: dict[str, float] = {}

    core_keys: list[str] = model["core_keys"]  # type: ignore[assignment]
    mass_keys: list[str] = model["mass_keys"]  # type: ignore[assignment]
    raw_triples: np.ndarray = model["raw_triples"]  # type: ignore[assignment]
    mass_triples: np.ndarray = model["mass_triples"]  # type: ignore[assignment]
    ratio_groups: dict[str, list[str]] = model["ratio_groups"]  # type: ignore[assignment]
    sum_rule_subsets: dict[str, list[str]] = model["sum_rule_subsets"]  # type: ignore[assignment]
    exponents: tuple[float, ...] = model["exponents"]  # type: ignore[assignment]

    core_values = parameter_vector(parameters, core_keys)
    mass_values = parameter_vector(parameters, mass_keys)

    def absorb_errors(name: str, errors: np.ndarray) -> None:
        nonlocal trial_count
        trial_count += int(errors.size)
        family_min_errors[name] = float(errors.min(initial=np.inf))
        summary = summarize_thresholds(errors)
        for key, count in summary.items():
            threshold_counts[key] += count

    def maybe_append(hit: RelationHit) -> None:
        if collect_hits and hit.relative_error < 0.01:
            hits.append(hit)

    raw_q = koide_triplet_values(core_values, raw_triples)
    raw_best_idx, raw_errors = best_target(raw_q, koide_targets)
    absorb_errors("koide_raw_all", raw_errors)
    if collect_hits:
        for index in np.where(raw_errors < 0.01)[0]:
            triple = raw_triples[index]
            target = koide_targets[int(raw_best_idx[index])]
            relation = f"Q({core_keys[int(triple[0])]}, {core_keys[int(triple[1])]}, {core_keys[int(triple[2])]})"
            maybe_append(RelationHit("koide_raw_all", relation, float(raw_q[index]), target.label, target.value, float(raw_errors[index]), note="Raw prompt-unit triple scan."))

    mass_q = koide_triplet_values(mass_values, mass_triples)
    mass_best_idx, mass_errors = best_target(mass_q, koide_targets)
    absorb_errors("koide_mass_only", mass_errors)
    if collect_hits:
        for index in np.where(mass_errors < 0.01)[0]:
            triple = mass_triples[index]
            target = koide_targets[int(mass_best_idx[index])]
            relation = f"Q({mass_keys[int(triple[0])]}, {mass_keys[int(triple[1])]}, {mass_keys[int(triple[2])]})"
            maybe_append(RelationHit("koide_mass_only", relation, float(mass_q[index]), target.label, target.value, float(mass_errors[index])))

    for family_name, keys in ratio_groups.items():
        values = parameter_vector(parameters, keys)
        pair_indices = list(combinations(range(len(keys)), 2))
        ratios = np.array([max(values[i], values[j]) / min(values[i], values[j]) for i, j in pair_indices], dtype=float)
        best_idx, errors = best_target(ratios, ratio_targets)
        absorb_errors(family_name, errors)
        if collect_hits:
            for index in np.where(errors < 0.01)[0]:
                i, j = pair_indices[index]
                if values[i] >= values[j]:
                    numerator_key, denominator_key = keys[i], keys[j]
                else:
                    numerator_key, denominator_key = keys[j], keys[i]
                target = ratio_targets[int(best_idx[index])]
                relation = f"{numerator_key}/{denominator_key}"
                maybe_append(RelationHit(family_name, relation, float(ratios[index]), target.label, target.value, float(errors[index])))

    sum_rule_values: list[float] = []
    sum_rule_meta: list[tuple[str, float, float, float]] = []
    for subset_name, keys in sum_rule_subsets.items():
        values = parameter_vector(parameters, keys)
        powered_sums = {exponent: float(np.power(values, exponent).sum()) for exponent in exponents}
        for p in exponents:
            numerator = powered_sums[p]
            for q in exponents:
                denominator_base = powered_sums[q]
                for r in exponents:
                    if len(keys) == 3 and p == 1.0 and q == 0.5 and r == 2.0:
                        continue
                    if p == q and r == 1.0:
                        continue
                    if p == 0.0 and r == 0.0:
                        continue
                    if p == 0.0 and q == 0.0:
                        continue
                    sum_rule_values.append(float(numerator / (denominator_base**r)))
                    if collect_hits:
                        sum_rule_meta.append((subset_name, p, q, r))
    sum_rule_array = np.array(sum_rule_values, dtype=float)
    sum_rule_best_idx, sum_rule_errors = best_target(sum_rule_array, simple_targets)
    absorb_errors("sum_rules", sum_rule_errors)
    if collect_hits:
        for index in np.where(sum_rule_errors < 0.01)[0]:
            subset_name, p, q, r = sum_rule_meta[index]
            target = simple_targets[int(sum_rule_best_idx[index])]
            relation = f"S[p={p:g}, q={q:g}, r={r:g}]({subset_name})"
            hits.append(RelationHit("sum_rules", relation, float(sum_rule_array[index]), target.label, target.value, float(sum_rule_errors[index])))

    mixing_values = np.array(
        [
            float(model["ckm_sin2"].sum() / np.square(np.sqrt(model["ckm_sin2"]).sum())),  # type: ignore[index]
            float(model["pmns_sin2"].sum() / np.square(np.sqrt(model["pmns_sin2"]).sum())),  # type: ignore[index]
        ],
        dtype=float,
    )
    mixing_best_idx, mixing_errors = best_target(mixing_values, koide_targets)
    absorb_errors("mixing_sin2_koide", mixing_errors)
    if collect_hits:
        labels = ("Q(sin^2 theta_CKM)", "Q(sin^2 theta_PMNS)")
        for index in np.where(mixing_errors < 0.01)[0]:
            target = koide_targets[int(mixing_best_idx[index])]
            maybe_append(RelationHit("mixing_sin2_koide", labels[index], float(mixing_values[index]), target.label, target.value, float(mixing_errors[index])))

    summary = {
        "trial_count": trial_count,
        "threshold_counts": threshold_counts,
        "family_min_errors": family_min_errors,
        "global_min_error": min(family_min_errors.values()),
    }
    hits.sort(key=lambda hit: hit.relative_error)
    return hits, summary


def fake_parameter_sample(parameters: dict[str, Parameter], rng: np.random.Generator) -> dict[str, float]:
    sampled: dict[str, float] = {}
    for key, parameter in parameters.items():
        if parameter.unit == "deg":
            low = max(0.05, parameter.value / 10.0)
            high = min(89.9, parameter.value * 10.0)
            sampled_value = float(np.exp(rng.uniform(math.log(low), math.log(high))))
        elif parameter.unit == "dimensionless":
            low = max(1.0e-6, parameter.value / 10.0)
            high = min(0.999, parameter.value * 10.0)
            sampled_value = float(np.exp(rng.uniform(math.log(low), math.log(high))))
        else:
            low = max(1.0e-30, parameter.value / 10.0)
            high = parameter.value * 10.0
            sampled_value = float(np.exp(rng.uniform(math.log(low), math.log(high))))
        sampled[key] = sampled_value
    return sampled


def run_monte_carlo(
    parameters: dict[str, Parameter],
    model: dict[str, object],
    koide_targets: list[Target],
    simple_targets: list[Target],
    ratio_targets: list[Target],
) -> dict[str, object]:
    rng = np.random.default_rng(MC_SEED)
    min_errors = np.empty(MC_SAMPLES, dtype=float)
    hits_1pct = np.empty(MC_SAMPLES, dtype=int)
    hits_0p1pct = np.empty(MC_SAMPLES, dtype=int)
    hits_0p01pct = np.empty(MC_SAMPLES, dtype=int)

    for index in range(MC_SAMPLES):
        fake_params = fake_parameter_sample(parameters, rng)
        _, summary = systematic_search(fake_params, model, koide_targets, simple_targets, ratio_targets, collect_hits=False)
        min_errors[index] = float(summary["global_min_error"])
        hits_1pct[index] = int(summary["threshold_counts"]["lt_1pct"])
        hits_0p1pct[index] = int(summary["threshold_counts"]["lt_0p1pct"])
        hits_0p01pct[index] = int(summary["threshold_counts"]["lt_0p01pct"])

    return {
        "seed": MC_SEED,
        "samples": MC_SAMPLES,
        "min_errors": min_errors.tolist(),
        "hits_1pct": hits_1pct.tolist(),
        "hits_0p1pct": hits_0p1pct.tolist(),
        "hits_0p01pct": hits_0p01pct.tolist(),
        "summary": {
            "min_error_mean": float(min_errors.mean()),
            "min_error_median": float(np.median(min_errors)),
            "hits_1pct_mean": float(hits_1pct.mean()),
            "hits_0p1pct_mean": float(hits_0p1pct.mean()),
            "hits_0p01pct_mean": float(hits_0p01pct.mean()),
        },
    }


def known_relations(parameters: dict[str, Parameter], koide_targets: list[Target], ratio_targets: list[Target]) -> list[RelationHit]:
    def koide(xs: list[float]) -> float:
        return sum(xs) / (sum(math.sqrt(x) for x in xs) ** 2)

    results: list[RelationHit] = []
    q_prompt, err_prompt = prompt_koide_value()
    results.append(RelationHit("known", "Koide(prompt lepton masses)", q_prompt, "2/3", 2.0 / 3.0, err_prompt, note="Using the rounded masses from the task prompt."))

    q_current, err_current = current_koide_value(parameters)
    results.append(RelationHit("known", "Koide(PDG 2025 charged leptons)", q_current, "2/3", 2.0 / 3.0, err_current))

    q_up = koide([parameters["m_u"].value, parameters["m_c"].value, parameters["m_t"].value])
    err_up = abs(q_up - 2.0 / 3.0) / (2.0 / 3.0)
    results.append(RelationHit("known", "Q_up vs 2/3", q_up, "2/3", 2.0 / 3.0, err_up))

    q_down = koide([parameters["m_d"].value, parameters["m_s"].value, parameters["m_b"].value])
    err_down = abs(q_down - 2.0 / 3.0) / (2.0 / 3.0)
    results.append(RelationHit("known", "Q_down vs 2/3", q_down, "2/3", 2.0 / 3.0, err_down))

    mb_over_tau = parameters["m_b"].value / parameters["m_tau"].value
    best_index, errors = best_target(np.array([mb_over_tau], dtype=float), ratio_targets)
    best = ratio_targets[int(best_index[0])]
    results.append(RelationHit("known", "m_b/m_tau", mb_over_tau, best.label, best.value, float(errors[0]), note="Best match inside the predeclared simple-constant bank."))

    sin_theta_c = 0.22501
    cabibbo_rhs = math.sqrt(parameters["m_d"].value / parameters["m_s"].value)
    cabibbo_error = abs(sin_theta_c - cabibbo_rhs) / sin_theta_c
    results.append(RelationHit("known", "sin(theta_C) vs sqrt(m_d/m_s)", cabibbo_rhs, f"sin(theta_C)={sin_theta_c:.5f}", sin_theta_c, cabibbo_error))

    sin2_theta_w = parameters["sin2_thetaW"].value
    target = Fraction(3, 13)
    target_value = float(target)
    results.append(RelationHit("known", "sin^2(theta_W)", sin2_theta_w, "3/13", target_value, abs(sin2_theta_w - target_value) / target_value))

    q_ckm_sin2 = koide([0.22501**2, 0.04183**2, 0.003732**2])
    q_pmns_sin2 = koide([0.307, 0.534, 0.0216])
    results.append(RelationHit("known", "Q(sin^2 theta_CKM)", q_ckm_sin2, "best simple rational from systematic scan", float("nan"), float("nan")))
    results.append(RelationHit("known", "Q(sin^2 theta_PMNS)", q_pmns_sin2, "best simple rational from systematic scan", float("nan"), float("nan")))

    return results


def add_global_p_values(hits: list[RelationHit], monte_carlo: dict[str, object]) -> list[dict[str, object]]:
    min_errors = np.array(monte_carlo["min_errors"], dtype=float)
    rows: list[dict[str, object]] = []
    for hit in hits:
        p_global = float((np.count_nonzero(min_errors <= hit.relative_error) + 1) / (min_errors.size + 1))
        rows.append(
            {
                "family": hit.family,
                "relation": hit.relation,
                "value": hit.value,
                "target_label": hit.target_label,
                "target_value": hit.target_value,
                "relative_error": hit.relative_error,
                "percent_error": hit.percent_error,
                "global_p_value": p_global,
                "note": hit.note,
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def plot_monte_carlo(real_summary: dict[str, object], monte_carlo: dict[str, object]) -> None:
    min_errors = np.array(monte_carlo["min_errors"], dtype=float)
    hits_0p1 = np.array(monte_carlo["hits_0p1pct"], dtype=int)
    hits_0p01 = np.array(monte_carlo["hits_0p01pct"], dtype=int)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    axes[0].hist(min_errors * 100.0, bins=40, color="#4472c4", alpha=0.85)
    axes[0].axvline(float(real_summary["global_min_error"]) * 100.0, color="#c00000", linewidth=2)
    axes[0].set_xlabel("Best relative error in full search (%)")
    axes[0].set_ylabel("Monte Carlo count")
    axes[0].set_title("Best hit precision under the null")

    bins = np.arange(0, max(hits_0p1.max(), hits_0p01.max(), int(real_summary["threshold_counts"]["lt_0p1pct"])) + 3) - 0.5
    axes[1].hist(hits_0p1, bins=bins, alpha=0.75, label="hits < 0.1%", color="#70ad47")
    axes[1].hist(hits_0p01, bins=bins, alpha=0.75, label="hits < 0.01%", color="#ffc000")
    axes[1].axvline(int(real_summary["threshold_counts"]["lt_0p1pct"]), color="#1f4e79", linewidth=2, linestyle="--")
    axes[1].axvline(int(real_summary["threshold_counts"]["lt_0p01pct"]), color="#bf9000", linewidth=2, linestyle="--")
    axes[1].set_xlabel("Hit count")
    axes[1].set_ylabel("Monte Carlo count")
    axes[1].set_title("Multiplicity of precise relations")
    axes[1].legend(frameon=False)

    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "monte_carlo_null_distributions.png", dpi=180)
    plt.close(fig)


def make_report(
    parameters: dict[str, Parameter],
    systematic_rows: list[dict[str, object]],
    known_rows: list[dict[str, object]],
    real_summary: dict[str, object],
    monte_carlo: dict[str, object],
) -> str:
    prompt_value, prompt_rel_error = prompt_koide_value()
    current_value, current_rel_error = current_koide_value(parameters)

    top_rows: list[dict[str, object]] = []
    seen_preview_keys: set[tuple[str, str, float]] = set()
    for row in systematic_rows:
        preview_key = (str(row["relation"]), str(row["target_label"]), round(float(row["value"]), 12))
        if preview_key in seen_preview_keys:
            continue
        seen_preview_keys.add(preview_key)
        top_rows.append(row)
        if len(top_rows) >= 20:
            break
    lines = [
        "# Koide-like Search Report",
        "",
        "## Scope",
        "",
        "This run used PDG 2025 updated central values where available. A few prompt values have shifted since older PDG/NuFIT snapshots, most visibly M_W, M_H, and theta_23^PMNS.",
        "",
        "The systematic search was fixed in advance to avoid post-hoc cherry-picking:",
        "",
        "- Koide-type Q on all raw positive parameter triples in the prompt units.",
        "- Koide-type Q on all GeV mass triples.",
        "- Same-unit pair ratios matched to a fixed low-complexity constant bank.",
        "- Generalized sum rules on predeclared family mass subsets for p, q, r in {-1, -1/2, 0, 1/2, 1, 2}.",
        "- Koide-type Q on CKM and PMNS sin^2-angle triples.",
        "",
        f"Total systematic composite trials: {real_summary['trial_count']}.",
        "",
        "## Charged-lepton Koide",
        "",
        f"- Prompt masses reproduce Q = {prompt_value:.9f}, with relative error {100.0 * prompt_rel_error:.6f}%.",
        f"- PDG 2025 lepton masses give Q = {current_value:.9f}, with relative error {100.0 * current_rel_error:.6f}%.",
        "",
        "## Best systematic hits below 1%",
        "",
        "| Family | Relation | Value | Target | Error (%) | Global p |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in top_rows:
        lines.append(
            f"| {row['family']} | `{row['relation']}` | {float(row['value']):.9g} | {row['target_label']} | {float(row['percent_error']):.6f} | {float(row['global_p_value']):.4f} |"
        )
    lines.extend(
        [
            "",
            "Full hit table: `output/systematic_hits_lt_1pct.csv`.",
            "",
            "## Known checks",
            "",
            "| Relation | Value | Target | Error (%) |",
            "| --- | ---: | ---: | ---: |",
        ]
    )
    for row in known_rows:
        error_text = "n/a" if math.isnan(float(row["percent_error"])) else f"{float(row['percent_error']):.6f}"
        lines.append(f"| `{row['relation']}` | {float(row['value']):.9g} | {row['target_label']} | {error_text} |")

    real_hits_0p1 = int(real_summary["threshold_counts"]["lt_0p1pct"])
    real_hits_0p01 = int(real_summary["threshold_counts"]["lt_0p01pct"])
    mc_hits_0p1 = np.array(monte_carlo["hits_0p1pct"], dtype=int)
    mc_hits_0p01 = np.array(monte_carlo["hits_0p01pct"], dtype=int)
    mc_min_errors = np.array(monte_carlo["min_errors"], dtype=float)

    p_best = float((np.count_nonzero(mc_min_errors <= float(real_summary["global_min_error"])) + 1) / (mc_min_errors.size + 1))
    p_hits_0p1 = float((np.count_nonzero(mc_hits_0p1 >= real_hits_0p1) + 1) / (mc_hits_0p1.size + 1))
    p_hits_0p01 = float((np.count_nonzero(mc_hits_0p01 >= real_hits_0p01) + 1) / (mc_hits_0p01.size + 1))

    lines.extend(
        [
            "",
            "## Monte Carlo null",
            "",
            "Null model: each parameter was independently randomized log-uniformly within one order of magnitude around its real value, with physical clipping for angles and dimensionless couplings. The full systematic search was rerun on each fake set.",
            "",
            f"- Monte Carlo samples: {monte_carlo['samples']}.",
            f"- Real best systematic error: {100.0 * float(real_summary['global_min_error']):.6f}%.",
            f"- Mean null best error: {100.0 * float(monte_carlo['summary']['min_error_mean']):.6f}%.",
            f"- Real hits below 0.1%: {real_hits_0p1}; null mean: {float(monte_carlo['summary']['hits_0p1pct_mean']):.3f}; tail probability P(null >= real): {p_hits_0p1:.4f}.",
            f"- Real hits below 0.01%: {real_hits_0p01}; null mean: {float(monte_carlo['summary']['hits_0p01pct_mean']):.3f}; tail probability P(null >= real): {p_hits_0p01:.4f}.",
            f"- Global look-elsewhere p-value for the single best hit: {p_best:.4f}.",
            "",
            "## Assessment",
            "",
        ]
    )

    if p_best < 0.05 or p_hits_0p01 < 0.05:
        lines.append("The real SM set does beat the chosen null on at least one metric, but the interpretation should remain cautious because the raw-unit mixed-parameter scan is representation-dependent and not rooted in a field-theoretic invariant.")
    else:
        lines.append("This first-pass search does not show convincing excess structure over the null once the look-elsewhere effect is accounted for. Charged-lepton Koide remains the standout curiosity, but the broader parameter set does not produce a clear overabundance of ultra-precise simple relations.")

    lines.extend(
        [
            "",
            "The biggest caveat is unit dependence: any scan that mixes masses, angles in degrees, couplings, and G_F as bare numbers is inherently representation-sensitive. The mass-only and dimensionless-family checks are more meaningful than the mixed raw-unit triples.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    ensure_dirs()
    parameter_list = build_parameters()
    parameters = build_parameter_lookup(parameter_list)
    koide_targets, simple_targets, ratio_targets = build_target_map()
    model = build_systematic_model(parameters)

    systematic_hits, real_summary = systematic_search(parameters, model, koide_targets, simple_targets, ratio_targets, collect_hits=True)
    monte_carlo = run_monte_carlo(parameters, model, koide_targets, simple_targets, ratio_targets)
    systematic_rows = add_global_p_values(systematic_hits, monte_carlo)

    known_hits = known_relations(parameters, koide_targets, ratio_targets)
    known_rows = []
    for hit in known_hits:
        known_rows.append(
            {
                "family": hit.family,
                "relation": hit.relation,
                "value": hit.value,
                "target_label": hit.target_label,
                "target_value": hit.target_value,
                "relative_error": hit.relative_error,
                "percent_error": hit.percent_error,
                "note": hit.note,
            }
        )

    write_csv(OUTPUT_DIR / "systematic_hits_lt_1pct.csv", systematic_rows)
    write_csv(OUTPUT_DIR / "known_relations.csv", known_rows)
    plot_monte_carlo(real_summary, monte_carlo)

    report_text = make_report(parameters, systematic_rows, known_rows, real_summary, monte_carlo)
    (OUTPUT_DIR / "report.md").write_text(report_text, encoding="utf-8")
    (OUTPUT_DIR / "sm_parameters.json").write_text(json.dumps([asdict(parameter) for parameter in parameter_list], indent=2), encoding="utf-8")
    (OUTPUT_DIR / "systematic_summary.json").write_text(json.dumps(real_summary, indent=2), encoding="utf-8")
    (OUTPUT_DIR / "monte_carlo_summary.json").write_text(json.dumps(monte_carlo["summary"], indent=2), encoding="utf-8")
    (OUTPUT_DIR / "monte_carlo_raw.json").write_text(json.dumps(monte_carlo, indent=2), encoding="utf-8")

    print(report_text)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
import time
from dataclasses import dataclass
from itertools import combinations, product
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "output"
PLOTS_DIR = ROOT / "plots"

N_MONTE_CARLO = 10_000
RNG_SEED = 20260402


@dataclass(frozen=True)
class ParameterRecord:
    key: str
    label: str
    value: float
    unit: str
    uncertainty: str
    source_url: str
    source_note: str
    include_in_generic_search: bool = True


PROMPT_PARAMETERS: list[ParameterRecord] = [
    ParameterRecord(
        key="m_e",
        label="electron mass",
        value=0.000510999,
        unit="GeV",
        uncertainty="1.6e-13 GeV",
        source_url="https://pdg.lbl.gov/2025/reviews/rpp2025-rev-phys-constants.pdf",
        source_note="PDG 2025 physical constants table lists m_e = 0.51099895069(16) MeV.",
    ),
    ParameterRecord(
        key="m_mu",
        label="muon mass",
        value=0.105658,
        unit="GeV",
        uncertainty="2.3e-9 GeV",
        source_url="https://pdg.lbl.gov/2025/tables/contents_tables.html",
        source_note="PDG 2025 leptons summary table; nominal analysis value follows the prompt truncation.",
    ),
    ParameterRecord(
        key="m_tau",
        label="tau mass",
        value=1.77686,
        unit="GeV",
        uncertainty="9.0e-5 GeV",
        source_url="https://pdg.lbl.gov/2025/tables/contents_tables.html",
        source_note="PDG 2025 leptons summary table gives the current tau mass near 1.77693 GeV; analysis uses the prompt central value 1.77686 GeV for consistency with the requested Koide check.",
    ),
    ParameterRecord(
        key="m_u",
        label="up quark mass",
        value=0.00216,
        unit="GeV",
        uncertainty="+4.9e-4/-2.6e-4 GeV",
        source_url="https://pdg.lbl.gov/2025/reviews/rpp2024-rev-standard-model.pdf",
        source_note="PDG electroweak review: m_u = 2.16^{+0.49}_{-0.26} MeV at 2 GeV in MS-bar.",
    ),
    ParameterRecord(
        key="m_d",
        label="down quark mass",
        value=0.00467,
        unit="GeV",
        uncertainty="+4.8e-4/-1.7e-4 GeV",
        source_url="https://pdg.lbl.gov/2025/reviews/rpp2024-rev-standard-model.pdf",
        source_note="PDG electroweak review: m_d = 4.67^{+0.48}_{-0.17} MeV at 2 GeV in MS-bar.",
    ),
    ParameterRecord(
        key="m_s",
        label="strange quark mass",
        value=0.0934,
        unit="GeV",
        uncertainty="+8.6e-3/-3.4e-3 GeV",
        source_url="https://pdg.lbl.gov/2025/reviews/rpp2024-rev-standard-model.pdf",
        source_note="PDG electroweak review: m_s = 93.4^{+8.6}_{-3.4} MeV at 2 GeV in MS-bar.",
    ),
    ParameterRecord(
        key="m_c",
        label="charm quark mass",
        value=1.27,
        unit="GeV",
        uncertainty="8.0e-3 GeV plus alpha_s dependence",
        source_url="https://pdg.lbl.gov/2025/reviews/rpp2024-rev-standard-model.pdf",
        source_note="PDG electroweak review uses m_c(m_c) = 1.274 +- 0.008 GeV with mild alpha_s dependence.",
    ),
    ParameterRecord(
        key="m_b",
        label="bottom quark mass",
        value=4.18,
        unit="GeV",
        uncertainty="8.0e-3 GeV plus alpha_s dependence",
        source_url="https://pdg.lbl.gov/2025/reviews/rpp2024-rev-standard-model.pdf",
        source_note="PDG electroweak review uses m_b(m_b) = 4.180 +- 0.008 GeV with mild alpha_s dependence.",
    ),
    ParameterRecord(
        key="m_t",
        label="top quark mass",
        value=172.57,
        unit="GeV",
        uncertainty="0.31 GeV",
        source_url="https://pdg.lbl.gov/2025/tables/contents_tables.html",
        source_note="PDG 2025 quark summary table; nominal value follows the prompt.",
    ),
    ParameterRecord(
        key="dm21",
        label="Delta m^2_21",
        value=7.53e-5,
        unit="eV^2",
        uncertainty="1.8e-6 eV^2",
        source_url="https://pdg.lbl.gov/encoder_listings/s067.pdf",
        source_note="PDG neutrino listing snippet includes Delta m^2_21 = (7.53 +- 0.18) x 10^-5 eV^2.",
        include_in_generic_search=False,
    ),
    ParameterRecord(
        key="dm32_abs",
        label="|Delta m^2_32|",
        value=2.453e-3,
        unit="eV^2",
        uncertainty="about 3.0e-5 eV^2",
        source_url="https://pdg.lbl.gov/2025/reviews/rpp2024-rev-neutrino-mixing.pdf",
        source_note="PDG 2024 neutrino review gives nearby central values that depend on ordering and global-fit column; analysis uses the prompt central value 2.453 x 10^-3 eV^2.",
        include_in_generic_search=False,
    ),
    ParameterRecord(
        key="theta12_ckm_deg",
        label="CKM theta_12",
        value=13.04,
        unit="deg",
        uncertainty="0.04 deg",
        source_url="https://pdg.lbl.gov/2025/reviews/rpp2025-rev-ckm-matrix.pdf",
        source_note="PDG CKM review gives sin(theta_12) = 0.22501 +- 0.00068; the prompt angle is the corresponding central value in degrees.",
        include_in_generic_search=False,
    ),
    ParameterRecord(
        key="theta23_ckm_deg",
        label="CKM theta_23",
        value=2.38,
        unit="deg",
        uncertainty="+0.05/-0.04 deg",
        source_url="https://pdg.lbl.gov/2025/reviews/rpp2025-rev-ckm-matrix.pdf",
        source_note="PDG CKM review gives sin(theta_23) = 0.04183^{+0.00079}_{-0.00069}; the prompt angle is the corresponding central value in degrees.",
        include_in_generic_search=False,
    ),
    ParameterRecord(
        key="theta13_ckm_deg",
        label="CKM theta_13",
        value=0.201,
        unit="deg",
        uncertainty="+0.005/-0.005 deg",
        source_url="https://pdg.lbl.gov/2025/reviews/rpp2025-rev-ckm-matrix.pdf",
        source_note="PDG CKM review gives sin(theta_13) = 0.003732^{+0.000090}_{-0.000085}; the prompt angle is the corresponding central value in degrees.",
        include_in_generic_search=False,
    ),
    ParameterRecord(
        key="theta12_pmns_deg",
        label="PMNS theta_12",
        value=33.41,
        unit="deg",
        uncertainty="+0.75/-0.72 deg",
        source_url="https://pdg.lbl.gov/2025/reviews/rpp2024-rev-neutrino-mixing.pdf",
        source_note="PDG neutrino review Table 14.7 gives theta_12 near 33.41 deg in multiple global-fit columns.",
        include_in_generic_search=False,
    ),
    ParameterRecord(
        key="theta23_pmns_deg",
        label="PMNS theta_23",
        value=49.0,
        unit="deg",
        uncertainty="about +1.0/-1.2 deg",
        source_url="https://pdg.lbl.gov/2025/reviews/rpp2024-rev-neutrino-mixing.pdf",
        source_note="PDG neutrino review Table 14.7 gives theta_23 values that depend on ordering and fit treatment; the prompt nominal value 49.0 deg is used here.",
        include_in_generic_search=False,
    ),
    ParameterRecord(
        key="theta13_pmns_deg",
        label="PMNS theta_13",
        value=8.54,
        unit="deg",
        uncertainty="+0.11/-0.12 deg",
        source_url="https://pdg.lbl.gov/2025/reviews/rpp2024-rev-neutrino-mixing.pdf",
        source_note="PDG neutrino review Table 14.7 gives theta_13 near 8.54 deg; analysis uses the prompt central value.",
        include_in_generic_search=False,
    ),
    ParameterRecord(
        key="alpha_em",
        label="alpha_em(M_Z)",
        value=1.0 / 127.95,
        unit="dimensionless",
        uncertainty="about 6e-7",
        source_url="https://pdg.lbl.gov/2025/reviews/rpp2024-rev-standard-model.pdf",
        source_note="PDG electroweak review gives alpha_hat^(5)(M_Z)^-1 = 127.930 +- 0.008; the analysis uses the prompt nominal 1/127.95.",
    ),
    ParameterRecord(
        key="alpha_s",
        label="alpha_s(M_Z)",
        value=0.1180,
        unit="dimensionless",
        uncertainty="0.0009",
        source_url="https://pdg.lbl.gov/2025/reviews/rpp2025-rev-phys-constants.pdf",
        source_note="PDG 2025 physical constants table lists alpha_s(m_Z) = 0.1180(9).",
    ),
    ParameterRecord(
        key="sin2_theta_w",
        label="sin^2 theta_W",
        value=0.23122,
        unit="dimensionless",
        uncertainty="0.00006",
        source_url="https://pdg.lbl.gov/2025/reviews/rpp2025-rev-phys-constants.pdf",
        source_note="PDG 2025 physical constants table lists sin^2 theta_hat(M_Z) = 0.23122(6).",
    ),
    ParameterRecord(
        key="M_W",
        label="W boson mass",
        value=80.377,
        unit="GeV",
        uncertainty="0.013 GeV",
        source_url="https://pdg.lbl.gov/2025/reviews/rpp2025-rev-phys-constants.pdf",
        source_note="PDG 2025 physical constants table lists m_W = 80.3692(133) GeV; the prompt nominal value 80.377 GeV is used for the search dataset.",
    ),
    ParameterRecord(
        key="M_Z",
        label="Z boson mass",
        value=91.1876,
        unit="GeV",
        uncertainty="0.0020 GeV",
        source_url="https://pdg.lbl.gov/2025/reviews/rpp2025-rev-phys-constants.pdf",
        source_note="PDG 2025 physical constants table lists m_Z = 91.1880(20) GeV; the prompt nominal value 91.1876 GeV is used for the search dataset.",
    ),
    ParameterRecord(
        key="M_H",
        label="Higgs boson mass",
        value=125.25,
        unit="GeV",
        uncertainty="0.09 GeV",
        source_url="https://pdg.lbl.gov/2025/reviews/rpp2024-rev-standard-model.pdf",
        source_note="PDG electroweak review quotes an LHC average near 125.10 +- 0.09 GeV; the prompt nominal value 125.25 GeV is used for the search dataset.",
    ),
    ParameterRecord(
        key="G_F",
        label="Fermi constant",
        value=1.1664e-5,
        unit="GeV^-2",
        uncertainty="6e-12 GeV^-2",
        source_url="https://pdg.lbl.gov/2025/reviews/rpp2025-rev-phys-constants.pdf",
        source_note="PDG 2025 physical constants table lists G_F = 1.1663785(6) x 10^-5 GeV^-2; kept in the parameter table but excluded from the generic relation search because it is dimensionful and directly tied to v.",
        include_in_generic_search=False,
    ),
    ParameterRecord(
        key="v",
        label="Higgs vev",
        value=246.22,
        unit="GeV",
        uncertainty="derived tree-level scale from G_F",
        source_url="https://pdg.lbl.gov/2025/reviews/rpp2024-rev-standard-model.pdf",
        source_note="PDG electroweak review states v = 246.22 GeV after symmetry breaking.",
    ),
]


PARAMS = {record.key: record for record in PROMPT_PARAMETERS}

MASS_KEYS = [
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

ANGLE_KEYS_DEG = [
    "theta12_ckm_deg",
    "theta23_ckm_deg",
    "theta13_ckm_deg",
    "theta12_pmns_deg",
    "theta23_pmns_deg",
    "theta13_pmns_deg",
]

EXPONENTS = (-1.0, -0.5, 0.0, 0.5, 1.0, 2.0)

SUM_RULE_SUBSETS = {
    "charged_leptons": ["m_e", "m_mu", "m_tau"],
    "up_quarks": ["m_u", "m_c", "m_t"],
    "down_quarks": ["m_d", "m_s", "m_b"],
    "all_quarks": ["m_u", "m_d", "m_s", "m_c", "m_b", "m_t"],
    "charged_fermions": ["m_e", "m_mu", "m_tau", "m_u", "m_d", "m_s", "m_c", "m_b", "m_t"],
    "ew_bosons": ["M_W", "M_Z", "M_H"],
    "ew_scales": ["M_W", "M_Z", "M_H", "v"],
    "all_mass_scales": MASS_KEYS,
}

MASS_RATIO_EXPRESSIONS = [
    ("sqrt(m_d/m_s)", lambda p: math.sqrt(p["m_d"] / p["m_s"])),
    ("sqrt(m_u/m_c)", lambda p: math.sqrt(p["m_u"] / p["m_c"])),
    ("sqrt(m_s/m_b)", lambda p: math.sqrt(p["m_s"] / p["m_b"])),
    ("sqrt(m_e/m_mu)", lambda p: math.sqrt(p["m_e"] / p["m_mu"])),
    ("sqrt(m_mu/m_tau)", lambda p: math.sqrt(p["m_mu"] / p["m_tau"])),
    ("sqrt(dm21/dm32_abs)", lambda p: math.sqrt(p["dm21"] / p["dm32_abs"])),
    ("(dm21/dm32_abs)^(1/4)", lambda p: (p["dm21"] / p["dm32_abs"]) ** 0.25),
]


def deg_to_sin(angle_deg: float) -> float:
    return math.sin(math.radians(angle_deg))


def build_named_values() -> dict[str, float]:
    values = {record.key: record.value for record in PROMPT_PARAMETERS}
    values["ckm_s12"] = deg_to_sin(values["theta12_ckm_deg"])
    values["ckm_s23"] = deg_to_sin(values["theta23_ckm_deg"])
    values["ckm_s13"] = deg_to_sin(values["theta13_ckm_deg"])
    values["pmns_s12"] = deg_to_sin(values["theta12_pmns_deg"])
    values["pmns_s23"] = deg_to_sin(values["theta23_pmns_deg"])
    values["pmns_s13"] = deg_to_sin(values["theta13_pmns_deg"])
    values["ckm_s12_sq"] = values["ckm_s12"] ** 2
    values["ckm_s23_sq"] = values["ckm_s23"] ** 2
    values["ckm_s13_sq"] = values["ckm_s13"] ** 2
    values["pmns_s12_sq"] = values["pmns_s12"] ** 2
    values["pmns_s23_sq"] = values["pmns_s23"] ** 2
    values["pmns_s13_sq"] = values["pmns_s13"] ** 2
    values["sqrt_dm21"] = math.sqrt(values["dm21"])
    values["sqrt_dm32_abs"] = math.sqrt(values["dm32_abs"])
    return values


def add_target(store: dict[float, tuple[str, float]], value: float, label: str) -> None:
    if not math.isfinite(value) or value <= 0:
        return
    key = round(value, 12)
    current = store.get(key)
    if current is None or len(label) < len(current[0]):
        store[key] = (label, value)


def build_koide_targets() -> list[dict[str, float | str]]:
    store: dict[float, tuple[str, float]] = {}
    for numerator in range(1, 13):
        for denominator in range(1, 13):
            value = numerator / denominator
            if value < (1.0 / 3.0) or value > 1.0:
                continue
            add_target(store, value, f"{numerator}/{denominator}")
    targets = [{"label": label, "value": value} for label, value in store.values()]
    return sorted(targets, key=lambda item: item["value"])


def build_simple_targets() -> list[dict[str, float | str]]:
    store: dict[float, tuple[str, float]] = {}

    for numerator in range(1, 13):
        for denominator in range(1, 13):
            frac = numerator / denominator
            add_target(store, frac, f"{numerator}/{denominator}")
            add_target(store, math.sqrt(frac), f"sqrt({numerator}/{denominator})")

    for numerator in range(1, 7):
        for denominator in range(1, 7):
            frac = numerator / denominator
            add_target(store, math.pi * frac, f"{numerator}pi/{denominator}")
            add_target(store, math.e * frac, f"{numerator}e/{denominator}")

    for exponent in range(-5, 9):
        add_target(store, 2.0**exponent, f"2^{exponent}")
    for exponent in range(-3, 6):
        add_target(store, 3.0**exponent, f"3^{exponent}")
    for exponent in range(-4, 5):
        add_target(store, 10.0**exponent, f"10^{exponent}")

    targets = [{"label": label, "value": value} for label, value in store.values()]
    return sorted(targets, key=lambda item: item["value"])


KOIDE_TARGETS = build_koide_targets()
SIMPLE_TARGETS = build_simple_targets()
KOIDE_TARGET_VALUES = np.array([item["value"] for item in KOIDE_TARGETS], dtype=float)
SIMPLE_TARGET_VALUES = np.array([item["value"] for item in SIMPLE_TARGETS], dtype=float)

MASS_TRIPLES = list(combinations(MASS_KEYS, 3))
DIMENSIONLESS_KEYS = [
    "alpha_em",
    "alpha_s",
    "sin2_theta_w",
    "ckm_s12",
    "ckm_s23",
    "ckm_s13",
    "pmns_s12",
    "pmns_s23",
    "pmns_s13",
]
DIMENSIONLESS_TRIPLES = list(combinations(DIMENSIONLESS_KEYS, 3))
MASS_PAIRS = list(combinations(MASS_KEYS, 2))
DIMENSIONLESS_PAIRS = list(combinations(DIMENSIONLESS_KEYS, 2))

SUM_RULE_CANDIDATES: list[tuple[str, tuple[str, ...], float, float, float]] = []
for subset_name, subset_keys in SUM_RULE_SUBSETS.items():
    for p, q, r in product(EXPONENTS, repeat=3):
        if (p == 0.0 and q == 0.0) or (p == q and r == 1.0) or (p == 0.0 and r == 0.0):
            continue
        if len(subset_keys) == 3 and (p, q, r) == (1.0, 0.5, 2.0):
            # This is exactly the Koide form already counted in the dedicated Koide search.
            continue
        SUM_RULE_CANDIDATES.append((subset_name, tuple(subset_keys), p, q, r))

ANGLE_TO_SINE_KEYS = [
    ("CKM s12", "ckm_s12"),
    ("CKM s23", "ckm_s23"),
    ("CKM s13", "ckm_s13"),
    ("PMNS s12", "pmns_s12"),
    ("PMNS s23", "pmns_s23"),
    ("PMNS s13", "pmns_s13"),
]


def nearest_targets(values: np.ndarray, target_values: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    rel_errors = np.abs(values[:, None] - target_values[None, :]) / np.abs(target_values[None, :])
    best_idx = np.argmin(rel_errors, axis=1)
    best_error = rel_errors[np.arange(values.shape[0]), best_idx]
    return best_idx, best_error


def koide_value(a: float, b: float, c: float) -> float:
    return (a + b + c) / (math.sqrt(a) + math.sqrt(b) + math.sqrt(c)) ** 2


def empirical_pvalue(mc_best_errors: np.ndarray, threshold: float) -> float:
    exceed = int(np.count_nonzero(mc_best_errors <= threshold))
    return (exceed + 1) / (mc_best_errors.size + 1)


def decade_bounds(value: float) -> tuple[float, float]:
    exponent = math.floor(math.log10(value))
    lo = 10.0**exponent
    hi = 10.0 ** (exponent + 1)
    return lo, hi


def draw_fake_values(rng: np.random.Generator, template_values: dict[str, float]) -> dict[str, float]:
    fake = {}
    for key, value in template_values.items():
        if key.endswith("_sq"):
            continue
        if key in {"ckm_s12", "ckm_s23", "ckm_s13", "pmns_s12", "pmns_s23", "pmns_s13", "sqrt_dm21", "sqrt_dm32_abs"}:
            continue
        if value <= 0:
            fake[key] = value
            continue
        lo, hi = decade_bounds(value)
        fake[key] = 10.0 ** rng.uniform(math.log10(lo), math.log10(hi))

    for key in ("ckm_s12", "ckm_s23", "ckm_s13", "pmns_s12", "pmns_s23", "pmns_s13"):
        lo, hi = decade_bounds(template_values[key])
        fake[key] = 10.0 ** rng.uniform(math.log10(lo), math.log10(hi))

    fake["theta12_ckm_deg"] = math.degrees(math.asin(min(1.0, fake["ckm_s12"])))
    fake["theta23_ckm_deg"] = math.degrees(math.asin(min(1.0, fake["ckm_s23"])))
    fake["theta13_ckm_deg"] = math.degrees(math.asin(min(1.0, fake["ckm_s13"])))
    fake["theta12_pmns_deg"] = math.degrees(math.asin(min(1.0, fake["pmns_s12"])))
    fake["theta23_pmns_deg"] = math.degrees(math.asin(min(1.0, fake["pmns_s23"])))
    fake["theta13_pmns_deg"] = math.degrees(math.asin(min(1.0, fake["pmns_s13"])))
    fake["ckm_s12_sq"] = fake["ckm_s12"] ** 2
    fake["ckm_s23_sq"] = fake["ckm_s23"] ** 2
    fake["ckm_s13_sq"] = fake["ckm_s13"] ** 2
    fake["pmns_s12_sq"] = fake["pmns_s12"] ** 2
    fake["pmns_s23_sq"] = fake["pmns_s23"] ** 2
    fake["pmns_s13_sq"] = fake["pmns_s13"] ** 2
    fake["sqrt_dm21"] = math.sqrt(fake["dm21"])
    fake["sqrt_dm32_abs"] = math.sqrt(fake["dm32_abs"])
    return fake


def family_error_arrays(values: dict[str, float]) -> dict[str, np.ndarray]:
    arrays: dict[str, np.ndarray] = {}

    mass_koide = np.array([koide_value(values[a], values[b], values[c]) for a, b, c in MASS_TRIPLES], dtype=float)
    arrays["koide_mass"] = nearest_targets(mass_koide, KOIDE_TARGET_VALUES)[1]

    dim_koide = np.array([koide_value(values[a], values[b], values[c]) for a, b, c in DIMENSIONLESS_TRIPLES], dtype=float)
    arrays["koide_dimless"] = nearest_targets(dim_koide, KOIDE_TARGET_VALUES)[1]

    mass_ratios = np.array([max(values[a], values[b]) / min(values[a], values[b]) for a, b in MASS_PAIRS], dtype=float)
    arrays["ratio_mass"] = nearest_targets(mass_ratios, SIMPLE_TARGET_VALUES)[1]

    dim_ratios = np.array([max(values[a], values[b]) / min(values[a], values[b]) for a, b in DIMENSIONLESS_PAIRS], dtype=float)
    arrays["ratio_dimless"] = nearest_targets(dim_ratios, SIMPLE_TARGET_VALUES)[1]

    sum_rule_values: list[float] = []
    for _, subset_keys, p, q, r in SUM_RULE_CANDIDATES:
        subset = [values[key] for key in subset_keys]
        s_p = sum(x**p for x in subset)
        s_q = sum(x**q for x in subset)
        sum_rule_values.append(s_p / (s_q**r))
    arrays["sum_rule"] = nearest_targets(np.array(sum_rule_values, dtype=float), KOIDE_TARGET_VALUES)[1]

    mixing_koide_values = np.array(
        [
            koide_value(values["ckm_s12_sq"], values["ckm_s23_sq"], values["ckm_s13_sq"]),
            koide_value(values["pmns_s12_sq"], values["pmns_s23_sq"], values["pmns_s13_sq"]),
        ],
        dtype=float,
    )
    arrays["mixing_koide_sin2"] = nearest_targets(mixing_koide_values, KOIDE_TARGET_VALUES)[1]

    angle_mass_errors = []
    for _, angle_key in ANGLE_TO_SINE_KEYS:
        angle_value = values[angle_key]
        for _, expr in MASS_RATIO_EXPRESSIONS:
            reference = expr(values)
            angle_mass_errors.append(abs((angle_value / reference) - 1.0))
    arrays["angle_mass"] = np.array(angle_mass_errors, dtype=float)

    arrays["weinberg"] = np.array([abs(values["sin2_theta_w"] / (3.0 / 13.0) - 1.0)], dtype=float)
    return arrays


def candidate_trial_count() -> dict[str, int]:
    return {
        "koide_mass": len(MASS_TRIPLES),
        "koide_dimless": len(DIMENSIONLESS_TRIPLES),
        "ratio_mass": len(MASS_PAIRS),
        "ratio_dimless": len(DIMENSIONLESS_PAIRS),
        "sum_rule": len(SUM_RULE_CANDIDATES),
        "mixing_koide_sin2": 2,
        "angle_mass": len(ANGLE_TO_SINE_KEYS) * len(MASS_RATIO_EXPRESSIONS),
        "weinberg": 1,
    }


def summarize_known_relations(values: dict[str, float]) -> dict[str, float]:
    koide_lepton = koide_value(values["m_e"], values["m_mu"], values["m_tau"])
    two_thirds = 2.0 / 3.0
    return {
        "koide_leptons": koide_lepton,
        "koide_leptons_error_pct": abs(koide_lepton - two_thirds) / two_thirds * 100.0,
        "koide_up": koide_value(values["m_u"], values["m_c"], values["m_t"]),
        "koide_down": koide_value(values["m_d"], values["m_s"], values["m_b"]),
        "mb_over_mtau": values["m_b"] / values["m_tau"],
        "cabibbo_vs_sqrt_md_ms_ratio": values["ckm_s12"] / math.sqrt(values["m_d"] / values["m_s"]),
        "cabibbo_vs_sqrt_md_ms_error_pct": abs(values["ckm_s12"] / math.sqrt(values["m_d"] / values["m_s"]) - 1.0) * 100.0,
        "weinberg_over_3_over_13": values["sin2_theta_w"] / (3.0 / 13.0),
        "weinberg_vs_3_over_13_error_pct": abs(values["sin2_theta_w"] / (3.0 / 13.0) - 1.0) * 100.0,
    }


def make_parameter_table(values: dict[str, float]) -> list[dict[str, str | float]]:
    table = []
    for record in PROMPT_PARAMETERS:
        table.append(
            {
                "key": record.key,
                "label": record.label,
                "value": record.value,
                "unit": record.unit,
                "uncertainty": record.uncertainty,
                "source_url": record.source_url,
                "source_note": record.source_note,
                "include_in_generic_search": record.include_in_generic_search,
            }
        )
    derived = [
        ("ckm_s12", "sin(theta12_CKM)", values["ckm_s12"]),
        ("ckm_s23", "sin(theta23_CKM)", values["ckm_s23"]),
        ("ckm_s13", "sin(theta13_CKM)", values["ckm_s13"]),
        ("pmns_s12", "sin(theta12_PMNS)", values["pmns_s12"]),
        ("pmns_s23", "sin(theta23_PMNS)", values["pmns_s23"]),
        ("pmns_s13", "sin(theta13_PMNS)", values["pmns_s13"]),
        ("sqrt_dm21", "sqrt(Delta m^2_21)", values["sqrt_dm21"]),
        ("sqrt_dm32_abs", "sqrt(|Delta m^2_32|)", values["sqrt_dm32_abs"]),
    ]
    for key, label, value in derived:
        table.append(
            {
                "key": key,
                "label": label,
                "value": value,
                "unit": "derived",
                "uncertainty": "",
                "source_url": "",
                "source_note": "Derived from the prompt nominal inputs.",
                "include_in_generic_search": True,
            }
        )
    return table


def full_results(values: dict[str, float]) -> list[dict[str, str | float | bool]]:
    results: list[dict[str, str | float | bool]] = []

    mass_koide_values = np.array([koide_value(values[a], values[b], values[c]) for a, b, c in MASS_TRIPLES], dtype=float)
    best_idx, best_err = nearest_targets(mass_koide_values, KOIDE_TARGET_VALUES)
    for i, (a, b, c) in enumerate(MASS_TRIPLES):
        target = KOIDE_TARGETS[int(best_idx[i])]
        results.append(
            {
                "family": "koide_mass",
                "relation": f"Q({a}, {b}, {c})",
                "value": mass_koide_values[i],
                "target_label": target["label"],
                "target_value": float(target["value"]),
                "error_frac": float(best_err[i]),
                "error_pct": float(best_err[i] * 100.0),
                "unit_sensitive": False,
            }
        )

    dim_koide_values = np.array([koide_value(values[a], values[b], values[c]) for a, b, c in DIMENSIONLESS_TRIPLES], dtype=float)
    best_idx, best_err = nearest_targets(dim_koide_values, KOIDE_TARGET_VALUES)
    for i, (a, b, c) in enumerate(DIMENSIONLESS_TRIPLES):
        target = KOIDE_TARGETS[int(best_idx[i])]
        results.append(
            {
                "family": "koide_dimless",
                "relation": f"Q({a}, {b}, {c})",
                "value": dim_koide_values[i],
                "target_label": target["label"],
                "target_value": float(target["value"]),
                "error_frac": float(best_err[i]),
                "error_pct": float(best_err[i] * 100.0),
                "unit_sensitive": False,
            }
        )

    mass_ratio_values = np.array([max(values[a], values[b]) / min(values[a], values[b]) for a, b in MASS_PAIRS], dtype=float)
    best_idx, best_err = nearest_targets(mass_ratio_values, SIMPLE_TARGET_VALUES)
    for i, (a, b) in enumerate(MASS_PAIRS):
        target = SIMPLE_TARGETS[int(best_idx[i])]
        ordered = (a, b) if values[a] >= values[b] else (b, a)
        results.append(
            {
                "family": "ratio_mass",
                "relation": f"{ordered[0]}/{ordered[1]}",
                "value": mass_ratio_values[i],
                "target_label": target["label"],
                "target_value": float(target["value"]),
                "error_frac": float(best_err[i]),
                "error_pct": float(best_err[i] * 100.0),
                "unit_sensitive": False,
            }
        )

    dim_ratio_values = np.array([max(values[a], values[b]) / min(values[a], values[b]) for a, b in DIMENSIONLESS_PAIRS], dtype=float)
    best_idx, best_err = nearest_targets(dim_ratio_values, SIMPLE_TARGET_VALUES)
    for i, (a, b) in enumerate(DIMENSIONLESS_PAIRS):
        target = SIMPLE_TARGETS[int(best_idx[i])]
        ordered = (a, b) if values[a] >= values[b] else (b, a)
        results.append(
            {
                "family": "ratio_dimless",
                "relation": f"{ordered[0]}/{ordered[1]}",
                "value": dim_ratio_values[i],
                "target_label": target["label"],
                "target_value": float(target["value"]),
                "error_frac": float(best_err[i]),
                "error_pct": float(best_err[i] * 100.0),
                "unit_sensitive": False,
            }
        )

    sum_rule_values: list[float] = []
    for _, subset_keys, p, q, r in SUM_RULE_CANDIDATES:
        subset = [values[key] for key in subset_keys]
        s_p = sum(x**p for x in subset)
        s_q = sum(x**q for x in subset)
        sum_rule_values.append(s_p / (s_q**r))
    sum_rule_array = np.array(sum_rule_values, dtype=float)
    best_idx, best_err = nearest_targets(sum_rule_array, KOIDE_TARGET_VALUES)
    for i, (subset_name, subset_keys, p, q, r) in enumerate(SUM_RULE_CANDIDATES):
        target = KOIDE_TARGETS[int(best_idx[i])]
        results.append(
            {
                "family": "sum_rule",
                "relation": f"S({subset_name}; p={p}, q={q}, r={r})",
                "value": sum_rule_array[i],
                "target_label": target["label"],
                "target_value": float(target["value"]),
                "error_frac": float(best_err[i]),
                "error_pct": float(best_err[i] * 100.0),
                "unit_sensitive": True,
            }
        )

    mixing_koide_triplets = [
        ("CKM sin^2 triple", ("ckm_s12_sq", "ckm_s23_sq", "ckm_s13_sq")),
        ("PMNS sin^2 triple", ("pmns_s12_sq", "pmns_s23_sq", "pmns_s13_sq")),
    ]
    mixing_values = np.array([koide_value(values[a], values[b], values[c]) for _, (a, b, c) in mixing_koide_triplets], dtype=float)
    best_idx, best_err = nearest_targets(mixing_values, KOIDE_TARGET_VALUES)
    for i, (label, _) in enumerate(mixing_koide_triplets):
        target = KOIDE_TARGETS[int(best_idx[i])]
        results.append(
            {
                "family": "mixing_koide_sin2",
                "relation": label,
                "value": mixing_values[i],
                "target_label": target["label"],
                "target_value": float(target["value"]),
                "error_frac": float(best_err[i]),
                "error_pct": float(best_err[i] * 100.0),
                "unit_sensitive": False,
            }
        )

    for angle_label, angle_key in ANGLE_TO_SINE_KEYS:
        for expr_label, expr in MASS_RATIO_EXPRESSIONS:
            reference = expr(values)
            ratio = values[angle_key] / reference
            err = abs(ratio - 1.0)
            results.append(
                {
                    "family": "angle_mass",
                    "relation": f"{angle_label} / {expr_label}",
                    "value": ratio,
                    "target_label": "1",
                    "target_value": 1.0,
                    "error_frac": float(err),
                    "error_pct": float(err * 100.0),
                    "unit_sensitive": False,
                }
            )

    ratio = values["sin2_theta_w"] / (3.0 / 13.0)
    results.append(
        {
            "family": "weinberg",
            "relation": "sin^2(theta_W) / (3/13)",
            "value": ratio,
            "target_label": "1",
            "target_value": 1.0,
            "error_frac": float(abs(ratio - 1.0)),
            "error_pct": float(abs(ratio - 1.0) * 100.0),
            "unit_sensitive": False,
        }
    )

    return results


def save_csv(path: Path, rows: Iterable[dict[str, object]]) -> None:
    rows = list(rows)
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def save_json(path: Path, payload: object) -> None:
    with path.open("w") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def monte_carlo(values: dict[str, float], n_trials: int) -> dict[str, object]:
    rng = np.random.default_rng(RNG_SEED)
    family_names = list(candidate_trial_count().keys())
    family_best_errors = {name: np.empty(N_MONTE_CARLO, dtype=float) for name in family_names}
    best_overall = np.empty(N_MONTE_CARLO, dtype=float)
    best_core = np.empty(N_MONTE_CARLO, dtype=float)
    hit_counts_1pct = np.empty(N_MONTE_CARLO, dtype=int)
    hit_counts_0p1pct = np.empty(N_MONTE_CARLO, dtype=int)
    hit_counts_0p01pct = np.empty(N_MONTE_CARLO, dtype=int)
    core_hit_counts_0p1pct = np.empty(N_MONTE_CARLO, dtype=int)

    start = time.time()
    for i in range(N_MONTE_CARLO):
        fake = draw_fake_values(rng, values)
        arrays = family_error_arrays(fake)
        combined = np.concatenate([arrays[name] for name in family_names])
        core = np.concatenate([arrays[name] for name in family_names if name != "sum_rule"])

        best_overall[i] = float(np.min(combined))
        best_core[i] = float(np.min(core))
        hit_counts_1pct[i] = int(np.count_nonzero(combined <= 0.01))
        hit_counts_0p1pct[i] = int(np.count_nonzero(combined <= 0.001))
        hit_counts_0p01pct[i] = int(np.count_nonzero(combined <= 0.0001))
        core_hit_counts_0p1pct[i] = int(np.count_nonzero(core <= 0.001))

        for name in family_names:
            family_best_errors[name][i] = float(np.min(arrays[name]))

        if (i + 1) % 1000 == 0:
            elapsed = time.time() - start
            print(f"Monte Carlo {i + 1}/{N_MONTE_CARLO} in {elapsed:.1f}s")

    return {
        "family_best_errors": {name: values.tolist() for name, values in family_best_errors.items()},
        "best_overall": best_overall.tolist(),
        "best_core": best_core.tolist(),
        "hit_counts_1pct": hit_counts_1pct.tolist(),
        "hit_counts_0p1pct": hit_counts_0p1pct.tolist(),
        "hit_counts_0p01pct": hit_counts_0p01pct.tolist(),
        "core_hit_counts_0p1pct": core_hit_counts_0p1pct.tolist(),
        "n_mc": N_MONTE_CARLO,
        "seed": RNG_SEED,
        "n_candidate_trials": n_trials,
    }


def add_pvalues(results: list[dict[str, str | float | bool]], mc: dict[str, object]) -> list[dict[str, str | float | bool]]:
    family_best = {name: np.array(values, dtype=float) for name, values in mc["family_best_errors"].items()}
    best_overall = np.array(mc["best_overall"], dtype=float)
    enriched = []
    for row in results:
        family = str(row["family"])
        error_frac = float(row["error_frac"])
        row = dict(row)
        row["p_any_same_family"] = empirical_pvalue(family_best[family], error_frac)
        row["p_any_global"] = empirical_pvalue(best_overall, error_frac)
        enriched.append(row)
    return enriched


def make_summary_markdown(
    values: dict[str, float],
    results: list[dict[str, str | float | bool]],
    known: dict[str, float],
    mc: dict[str, object],
    trial_counts: dict[str, int],
) -> str:
    total_trials = sum(trial_counts.values())
    best_overall = np.array(mc["best_overall"], dtype=float)
    best_core = np.array(mc["best_core"], dtype=float)
    hit_counts_0p1pct = np.array(mc["hit_counts_0p1pct"], dtype=int)
    hit_counts_0p01pct = np.array(mc["hit_counts_0p01pct"], dtype=int)
    core_hit_counts_0p1pct = np.array(mc["core_hit_counts_0p1pct"], dtype=int)

    hits_under_1pct = [row for row in results if float(row["error_frac"]) <= 0.01]
    hits_under_0p1pct = [row for row in results if float(row["error_frac"]) <= 0.001]
    hits_under_0p01pct = [row for row in results if float(row["error_frac"]) <= 0.0001]
    core_hits_under_0p1pct = [row for row in results if float(row["error_frac"]) <= 0.001 and not bool(row["unit_sensitive"])]

    lines = []
    lines.append("# Koide-like Search in Standard Model Parameters")
    lines.append("")
    lines.append("## Input Convention")
    lines.append("")
    lines.append("The search uses the prompt's nominal PDG-like central values to keep the requested Koide reproduction exact.")
    lines.append("Uncertainties and source links are attached from PDG 2024/2025 pages, with source notes calling out where the 2025 update has slightly shifted a central value.")
    lines.append("")
    lines.append("## Original Koide Check")
    lines.append("")
    lines.append(f"- Q_leptons = {known['koide_leptons']:.12f}")
    lines.append(f"- Target 2/3 = {2.0 / 3.0:.12f}")
    lines.append(f"- Relative deviation = {known['koide_leptons_error_pct']:.6f}%")
    lines.append("")
    lines.append("## Search Definition")
    lines.append("")
    lines.append(f"- Total candidate trials N_trials = {total_trials}")
    for family, count in trial_counts.items():
        lines.append(f"- {family}: {count}")
    lines.append("- Simple-target libraries were fixed before the Monte Carlo search. Each candidate is scored against its nearest target in that fixed library.")
    lines.append("- The `sum_rule` family is unit-sensitive and should be treated as exploratory numerology, not as a physically robust invariant.")
    lines.append("")
    lines.append("## Known Relations")
    lines.append("")
    lines.append(f"- Koide charged leptons: Q = {known['koide_leptons']:.12f}, error = {known['koide_leptons_error_pct']:.6f}%")
    lines.append(f"- Up-type quarks: Q_up = {known['koide_up']:.12f}")
    lines.append(f"- Down-type quarks: Q_down = {known['koide_down']:.12f}")
    lines.append(f"- m_b / m_tau = {known['mb_over_mtau']:.6f}")
    lines.append(f"- sin(theta_C) / sqrt(m_d / m_s) = {known['cabibbo_vs_sqrt_md_ms_ratio']:.6f}, error = {known['cabibbo_vs_sqrt_md_ms_error_pct']:.4f}%")
    lines.append(f"- sin^2(theta_W) / (3/13) = {known['weinberg_over_3_over_13']:.6f}, error = {known['weinberg_vs_3_over_13_error_pct']:.4f}%")
    lines.append("")
    lines.append("## Hits Better Than 1%")
    lines.append("")
    lines.append(f"- Total hits under 1%: {len(hits_under_1pct)}")
    lines.append(f"- Total hits under 0.1%: {len(hits_under_0p1pct)}")
    lines.append(f"- Total hits under 0.01%: {len(hits_under_0p01pct)}")
    lines.append(f"- Core non-sum-rule hits under 0.1%: {len(core_hits_under_0p1pct)}")
    lines.append("")
    lines.append("| Family | Relation | Value | Target | Error % | p_any_global |")
    lines.append("|---|---|---:|---:|---:|---:|")
    for row in hits_under_1pct[:30]:
        lines.append(
            f"| {row['family']} | {row['relation']} | {float(row['value']):.10g} | {row['target_label']} | {float(row['error_pct']):.6f} | {float(row['p_any_global']):.4f} |"
        )
    lines.append("")
    lines.append("## Monte Carlo Null")
    lines.append("")
    lines.append("- Fake parameter sets were generated by replacing each positive observable with an independent log-uniform draw inside the decade that contains the observed value, using the same units and the same search definitions.")
    lines.append(f"- Real best global error = {min(float(row['error_frac']) for row in results) * 100.0:.6f}%")
    lines.append(f"- MC median best global error = {np.median(best_overall) * 100.0:.6f}%")
    lines.append(f"- Real core best error (excluding sum rules) = {min(float(row['error_frac']) for row in results if not bool(row['unit_sensitive'])) * 100.0:.6f}%")
    lines.append(f"- MC median core best error = {np.median(best_core) * 100.0:.6f}%")
    lines.append(f"- Real count <= 0.1% = {len(hits_under_0p1pct)} vs MC mean {hit_counts_0p1pct.mean():.2f}, median {np.median(hit_counts_0p1pct):.2f}")
    lines.append(f"- Real count <= 0.01% = {len(hits_under_0p01pct)} vs MC mean {hit_counts_0p01pct.mean():.2f}, median {np.median(hit_counts_0p01pct):.2f}")
    lines.append(f"- Real core count <= 0.1% = {len(core_hits_under_0p1pct)} vs MC mean {core_hit_counts_0p1pct.mean():.2f}, median {np.median(core_hit_counts_0p1pct):.2f}")
    lines.append("")

    core_p = (np.count_nonzero(core_hit_counts_0p1pct >= len(core_hits_under_0p1pct)) + 1) / (core_hit_counts_0p1pct.size + 1)
    overall_p = (np.count_nonzero(hit_counts_0p1pct >= len(hits_under_0p1pct)) + 1) / (hit_counts_0p1pct.size + 1)
    koide_global_p = min(float(row["p_any_global"]) for row in results if row["relation"] == "Q(m_e, m_mu, m_tau)")

    lines.append("## Assessment")
    lines.append("")
    if core_p < 0.05:
        verdict = "The real SM shows an excess of sub-0.1% non-trivial hits over the null, so there is some evidence of structure beyond an isolated coincidence."
    else:
        verdict = "Outside the original Koide relation, the real SM does not show a clear excess of sub-0.1% non-trivial hits over the null. The first-pass evidence favors Koide being isolated."
    lines.append(f"- {verdict}")
    lines.append(f"- Global Monte Carlo tail for the real <= 0.1% hit count: p = {overall_p:.4f}")
    lines.append(f"- Core non-sum-rule Monte Carlo tail for the real <= 0.1% hit count: p = {core_p:.4f}")
    lines.append(f"- Empirical global look-elsewhere probability for the charged-lepton Koide precision within this search: p = {koide_global_p:.6f}")
    lines.append("- Interpret the `sum_rule` family with caution: its formulas are highly flexible and partly unit-convention sensitive, so its hits should not drive the physics conclusion.")
    lines.append("")
    return "\n".join(lines)


def plot_histograms(mc: dict[str, object], results: list[dict[str, str | float | bool]]) -> None:
    hit_counts_0p1pct = np.array(mc["hit_counts_0p1pct"], dtype=int)
    hit_counts_0p01pct = np.array(mc["hit_counts_0p01pct"], dtype=int)
    best_overall = np.array(mc["best_overall"], dtype=float) * 100.0

    real_0p1 = sum(float(row["error_frac"]) <= 0.001 for row in results)
    real_0p01 = sum(float(row["error_frac"]) <= 0.0001 for row in results)
    real_best = min(float(row["error_frac"]) for row in results) * 100.0

    plt.figure(figsize=(8, 5))
    bins = np.arange(0, max(hit_counts_0p1pct.max(), real_0p1) + 2) - 0.5
    plt.hist(hit_counts_0p1pct, bins=bins, color="#4c78a8", alpha=0.85)
    plt.axvline(real_0p1, color="#d62728", linewidth=2, label=f"real SM = {real_0p1}")
    plt.xlabel("Number of hits with error <= 0.1%")
    plt.ylabel("Monte Carlo count")
    plt.title("Null Distribution of Sub-0.1% Hits")
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "mc_hits_0p1pct_hist.png", dpi=200)
    plt.close()

    plt.figure(figsize=(8, 5))
    bins = np.arange(0, max(hit_counts_0p01pct.max(), real_0p01) + 2) - 0.5
    plt.hist(hit_counts_0p01pct, bins=bins, color="#72b7b2", alpha=0.85)
    plt.axvline(real_0p01, color="#d62728", linewidth=2, label=f"real SM = {real_0p01}")
    plt.xlabel("Number of hits with error <= 0.01%")
    plt.ylabel("Monte Carlo count")
    plt.title("Null Distribution of Koide-Precision Hits")
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "mc_hits_0p01pct_hist.png", dpi=200)
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.hist(best_overall, bins=60, color="#f58518", alpha=0.85)
    plt.axvline(real_best, color="#d62728", linewidth=2, label=f"real SM = {real_best:.4g}%")
    plt.xlabel("Best relation error in one fake SM set [%]")
    plt.ylabel("Monte Carlo count")
    plt.title("Best-Relation Precision Under the Null")
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "mc_best_error_hist.png", dpi=200)
    plt.close()


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    values = build_named_values()
    parameter_table = make_parameter_table(values)
    save_csv(DATA_DIR / "parameter_table.csv", parameter_table)
    save_json(DATA_DIR / "parameter_table.json", parameter_table)

    known = summarize_known_relations(values)
    save_json(OUTPUT_DIR / "known_relations.json", known)

    raw_results = full_results(values)
    trial_counts = candidate_trial_count()
    mc = monte_carlo(values, sum(trial_counts.values()))
    enriched_results = add_pvalues(raw_results, mc)
    enriched_results.sort(key=lambda row: float(row["error_frac"]))

    save_csv(OUTPUT_DIR / "all_candidate_results.csv", enriched_results)
    save_csv(OUTPUT_DIR / "hits_under_1pct.csv", [row for row in enriched_results if float(row["error_frac"]) <= 0.01])
    save_csv(OUTPUT_DIR / "hits_under_0p1pct.csv", [row for row in enriched_results if float(row["error_frac"]) <= 0.001])
    save_json(OUTPUT_DIR / "monte_carlo_summary.json", mc)

    summary = make_summary_markdown(values, enriched_results, known, mc, trial_counts)
    (OUTPUT_DIR / "summary.md").write_text(summary)

    plot_histograms(mc, enriched_results)

    print(summary)


if __name__ == "__main__":
    main()

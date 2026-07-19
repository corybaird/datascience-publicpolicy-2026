"""Transform API observations into a transparent country-level ESG dataset."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

import data


REPO_ROOT = Path(__file__).resolve().parents[4]
PROCESSED_PATH = (
    REPO_ROOT / "data" / "final_project" / "huang-shuo" / "esg_investing_cross_section.csv"
)

ESG_INPUTS = [
    "renewable_share",
    "co2_intensity",
    "life_expectancy",
    "female_lfp",
    "male_lfp",
    "rule_of_law",
    "regulatory_quality",
    "control_corruption",
]
CONTROLS = ["gdp_per_capita_ppp", "trade_openness", "population"]


def _relative_score(series: pd.Series, higher_is_better: bool = True) -> pd.Series:
    """Convert a variable to a robust 0-100 percentile score within the sample."""
    oriented = series if higher_is_better else -series
    return 100 * oriented.rank(method="average", pct=True)


def _zscore(series: pd.Series) -> pd.Series:
    return (series - series.mean()) / series.std(ddof=0)


def _country_averages(raw: pd.DataFrame) -> pd.DataFrame:
    keys = ["iso3", "country", "region", "income_group"]
    wide = raw.pivot_table(
        index=keys + ["year"], columns="indicator", values="value", aggfunc="first"
    ).reset_index()

    variables = list(data.INDICATORS)
    means = wide.groupby(keys, observed=True)[variables].mean()
    counts = wide.groupby(keys, observed=True)[variables].count().add_suffix("_n")
    return means.join(counts).reset_index()


def run(raw: pd.DataFrame | None = None) -> pd.DataFrame:
    """Clean, screen, score, and save the medium-run country cross section.

    The 2018-2022 averages damp one-year noise.  A country needs at least three
    annual observations for every ESG input and macro control, at least two for
    market capitalization/GDP, and a population of one million.  These rules
    are set before looking at the regression coefficients.
    """
    if raw is None:
        raw = data.run(force_refresh=False)

    country = _country_averages(raw)
    flow: list[tuple[str, int]] = [("API economies after removing aggregates", len(country))]

    required_counts = [f"{name}_n" for name in ESG_INPUTS + CONTROLS]
    country = country[country[required_counts].ge(3).all(axis=1)].copy()
    flow.append(("At least 3 years for ESG inputs and controls", len(country)))

    country = country[country["market_cap_gdp_n"].ge(2)].copy()
    flow.append(("At least 2 years for equity-market depth", len(country)))

    country = country[
        country[ESG_INPUTS + CONTROLS + ["market_cap_gdp"]].notna().all(axis=1)
    ].copy()
    country = country[(country["population"] >= 1_000_000) & (country["market_cap_gdp"] > 0)]
    flow.append(("Complete cases, population >= 1m, positive market depth", len(country)))

    # A smaller absolute male-female participation gap is treated as better.
    country["gender_lfp_gap"] = (country["male_lfp"] - country["female_lfp"]).abs()

    country["renewable_score"] = _relative_score(country["renewable_share"], True)
    country["carbon_score"] = _relative_score(country["co2_intensity"], False)
    country["life_score"] = _relative_score(country["life_expectancy"], True)
    country["gender_score"] = _relative_score(country["gender_lfp_gap"], False)
    country["rule_score"] = _relative_score(country["rule_of_law"], True)
    country["regulation_score"] = _relative_score(country["regulatory_quality"], True)
    country["corruption_score"] = _relative_score(country["control_corruption"], True)

    country["e_score"] = country[["renewable_score", "carbon_score"]].mean(axis=1)
    country["s_score"] = country[["life_score", "gender_score"]].mean(axis=1)
    country["g_score"] = country[
        ["rule_score", "regulation_score", "corruption_score"]
    ].mean(axis=1)
    country["esg_score"] = country[["e_score", "s_score", "g_score"]].mean(axis=1)

    lower, upper = country["market_cap_gdp"].quantile([0.02, 0.98])
    country["market_cap_gdp_w"] = country["market_cap_gdp"].clip(lower, upper)
    country["log_market_depth"] = np.log1p(country["market_cap_gdp_w"])
    country["log_gdp_pc"] = np.log(country["gdp_per_capita_ppp"])
    country["log_population"] = np.log(country["population"])
    country["market_cap_billions"] = country["market_cap_usd"] / 1_000_000_000

    for pillar in ["e_score", "s_score", "g_score", "esg_score"]:
        country[pillar.replace("_score", "_z")] = _zscore(country[pillar])
    country["trade_z"] = _zscore(country["trade_openness"])

    country["esg_rank"] = country["esg_score"].rank(ascending=False, method="min").astype(int)
    country = country.sort_values("esg_score", ascending=False).reset_index(drop=True)
    # Keep attrs JSON-like so downstream pandas operations can compare metadata.
    country.attrs["sample_flow"] = [
        {"screen": screen, "countries": countries} for screen, countries in flow
    ]
    country.attrs["winsor_limits"] = (float(lower), float(upper))

    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    country.to_csv(PROCESSED_PATH, index=False)
    return country


if __name__ == "__main__":
    clean = run()
    print(pd.DataFrame(clean.attrs["sample_flow"]).to_string(index=False))
    print(f"\nSaved {len(clean):,} countries to {PROCESSED_PATH}")

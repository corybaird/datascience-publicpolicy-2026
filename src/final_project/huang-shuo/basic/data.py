"""Download the ESG-investing dataset from official World Bank APIs.

Every observation used by the project is retrieved programmatically.  The
World Development Indicators (WDI) and Worldwide Governance Indicators (WGI)
share the World Bank API, but are distinct source databases.  The API URL used
for every series is retained in the raw data as a provenance field.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd


START_YEAR = 2018
END_YEAR = 2022
API_ROOT = "https://api.worldbank.org/v2"
REPO_ROOT = Path(__file__).resolve().parents[4]
DATA_DIR = REPO_ROOT / "data" / "final_project" / "huang-shuo"
RAW_PATH = DATA_DIR / "world_bank_esg_raw.csv"

# variable: (World Bank indicator code, source database, optional source id)
INDICATORS: dict[str, tuple[str, str, int | None]] = {
    "market_cap_gdp": ("CM.MKT.LCAP.GD.ZS", "WDI", None),
    "market_cap_usd": ("CM.MKT.LCAP.CD", "WDI", None),
    "renewable_share": ("EG.FEC.RNEW.ZS", "WDI", None),
    "co2_intensity": ("EN.GHG.CO2.RT.GDP.PP.KD", "WDI", None),
    "life_expectancy": ("SP.DYN.LE00.IN", "WDI", None),
    "female_lfp": ("SL.TLF.CACT.FE.ZS", "WDI", None),
    "male_lfp": ("SL.TLF.CACT.MA.ZS", "WDI", None),
    "rule_of_law": ("GOV_WGI_RL.SC", "WGI 2025 revision", 3),
    "regulatory_quality": ("GOV_WGI_RQ.SC", "WGI 2025 revision", 3),
    "control_corruption": ("GOV_WGI_CC.SC", "WGI 2025 revision", 3),
    "gdp_per_capita_ppp": ("NY.GDP.PCAP.PP.KD", "WDI", None),
    "trade_openness": ("NE.TRD.GNFS.ZS", "WDI", None),
    "population": ("SP.POP.TOTL", "WDI", None),
}


def _get_json(url: str, attempts: int = 3, timeout: int = 45) -> Any:
    """Read JSON with a clear user agent and short exponential retries."""
    request = Request(url, headers={"User-Agent": "UTokyo-ESG-research/1.0"})
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            with urlopen(request, timeout=timeout) as response:
                return json.load(response)
        except Exception as exc:  # network errors differ across platforms
            last_error = exc
            if attempt < attempts - 1:
                time.sleep(2**attempt)
    raise RuntimeError(f"World Bank API request failed after {attempts} attempts: {url}") from last_error


def _country_metadata() -> pd.DataFrame:
    params = urlencode({"format": "json", "per_page": 400})
    payload = _get_json(f"{API_ROOT}/country?{params}")
    rows = payload[1]
    metadata = pd.DataFrame(
        {
            "iso3": row["id"],
            "country": row["name"],
            "region": row["region"]["value"],
            "income_group": row["incomeLevel"]["value"],
        }
        for row in rows
        if row["region"]["value"] != "Aggregates"
    )
    return metadata.drop_duplicates("iso3")


def _indicator_url(indicator_code: str, source_id: int | None) -> str:
    params: dict[str, str | int] = {
        "date": f"{START_YEAR}:{END_YEAR}",
        "format": "json",
        "per_page": 20_000,
    }
    if source_id is not None:
        params["source"] = source_id
    return f"{API_ROOT}/country/all/indicator/{indicator_code}?{urlencode(params)}"


def _download_indicator(
    variable: str,
    indicator_code: str,
    source_database: str,
    source_id: int | None,
) -> pd.DataFrame:
    url = _indicator_url(indicator_code, source_id)
    payload = _get_json(url)
    if not isinstance(payload, list) or len(payload) < 2 or payload[1] is None:
        raise ValueError(f"No observations returned for {indicator_code}: {url}")

    frame = pd.DataFrame(
        {
            "iso3": row.get("countryiso3code"),
            "year": int(row["date"]),
            "indicator": variable,
            "value": row.get("value"),
            "indicator_code": indicator_code,
            "source_database": source_database,
            "api_url": url,
        }
        for row in payload[1]
    )
    frame["value"] = pd.to_numeric(frame["value"], errors="coerce")
    return frame


def run(force_refresh: bool = True) -> pd.DataFrame:
    """Download and return a tidy country-year-indicator data frame."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if RAW_PATH.exists() and not force_refresh:
        return pd.read_csv(RAW_PATH)

    metadata = _country_metadata()
    downloads = [
        _download_indicator(variable, code, database, source_id)
        for variable, (code, database, source_id) in INDICATORS.items()
    ]
    raw = pd.concat(downloads, ignore_index=True)
    raw = raw.merge(metadata, on="iso3", how="inner", validate="many_to_one")
    raw = raw[
        [
            "iso3",
            "country",
            "region",
            "income_group",
            "year",
            "indicator",
            "value",
            "indicator_code",
            "source_database",
            "api_url",
        ]
    ].sort_values(["indicator", "iso3", "year"])
    raw.to_csv(RAW_PATH, index=False)
    return raw.reset_index(drop=True)


def download_audit(raw: pd.DataFrame) -> pd.DataFrame:
    """Summarize API coverage for a compact notebook audit table."""
    nonmissing = raw.dropna(subset=["value"])
    return (
        nonmissing.groupby(
            ["source_database", "indicator", "indicator_code"], as_index=False
        )
        .agg(
            observations=("value", "size"),
            countries=("iso3", "nunique"),
            first_year=("year", "min"),
            last_year=("year", "max"),
        )
        .sort_values(["source_database", "indicator"])
        .reset_index(drop=True)
    )


if __name__ == "__main__":
    downloaded = run(force_refresh=True)
    print(download_audit(downloaded).to_string(index=False))
    print(f"\nSaved {len(downloaded):,} rows to {RAW_PATH}")

import requests
import pandas as pd
import time
from pathlib import Path

BORROWER_COUNTRIES = [
    "PAK", "AGO", "LKA", "ETH", "KEN", "KHM",
    "LAO", "ZMB", "MMR", "BGD", "NGA", "MNG",
]
LENDER = "CHN"
CHINA_COUNTERPART_CODE = "730"
IDS_INDICATOR = "DT.DOD.BLAT.CD"
WEO_INDICATOR = "NGDP_RPCH"


def load_weo_growth():
    url = f"https://www.imf.org/external/datamapper/api/v2/{WEO_INDICATOR}"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()["values"][WEO_INDICATOR]

    rows = []
    for code in BORROWER_COUNTRIES + [LENDER]:
        if code not in data:
            continue
        for year, value in data[code].items():
            rows.append({"country": code, "year": int(year), "gdp_growth": value})
    return pd.DataFrame(rows)


def load_china_debt():
    frames = []
    for country in BORROWER_COUNTRIES:
        url = (
            f"https://api.worldbank.org/v2/sources/6/country/{country}"
            f"/series/{IDS_INDICATOR}/counterpart-area/{CHINA_COUNTERPART_CODE}/time/all"
        )
        try:
            resp = requests.get(url, params={"format": "json", "per_page": 200}, timeout=30)
            resp.raise_for_status()
            payload = resp.json()

            source = payload.get("source", {}) if isinstance(payload, dict) else {}
            if isinstance(source, list):
                source = source[0] if source else {}
            entries = source.get("data", []) if isinstance(source, dict) else []

            if not entries:
                print(f"[INFO] {country}: no data: {str(payload)[:200]}）")

            for e in entries:
                year, value = None, e.get("value")
                for v in e.get("variable", []):
                    if v.get("concept") == "Time":
                        year = int(v["id"].replace("YR", ""))
                frames.append({"country": country, "year": year, "china_debt_usd": value})
        except Exception as exc:
            print(f"[WARN] {country}: {type(exc).__name__}: {exc}")
        time.sleep(0.3)
    return pd.DataFrame(frames)


def run():
    project_root = Path(__file__).resolve().parents[4]
    dest_dir = project_root / "data/final_project/ryu-hasegawa"
    dest_dir.mkdir(parents=True, exist_ok=True)

    growth_df = load_weo_growth()
    debt_df = load_china_debt()

    growth_file = dest_dir / "weo_growth_raw.csv"
    debt_file = dest_dir / "china_debt_raw.csv"
    growth_df.to_csv(growth_file, index=False)
    debt_df.to_csv(debt_file, index=False)

    print(f"Data acquired and saved to {growth_file.relative_to(project_root)} "
          f"and {debt_file.relative_to(project_root)}")
    return growth_df, debt_df


if __name__ == "__main__":
    run()

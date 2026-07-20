import pandas as pd
import requests
from pathlib import Path

def load_manifesto_data():
    project_root = Path(__file__).resolve().parents[4]
    source_path = project_root / "data/examples/week_7/manifesto_english_speaking.parquet"
    if not source_path.exists():
        raise FileNotFoundError(f"Source manifesto data not found at {source_path}")
    df = pd.read_parquet(source_path).reset_index()
    df["year"] = pd.to_datetime(df["date"]).dt.year
    country_to_iso3 = {
        "Australia": "AUS",
        "Canada": "CAN",
        "Ireland": "IRL",
        "South Africa": "ZAF",
        "United Kingdom": "GBR",
        "United States": "USA",
    }
    df["country"] = df["countryname"].map(country_to_iso3)
    return df[["country", "countryname", "year", "partyname", "text"]]

def load_voice_accountability():
    countries = ["AUS", "CAN", "IRL", "ZAF", "GBR", "USA"]
    url = (
        f"https://api.worldbank.org/v2/country/{';'.join(countries)}/indicator/GOV_WGI_VA.EST"
        "?format=json&per_page=1000&date=1996:2022"
    )
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    rows = response.json()[1]
    df = pd.DataFrame([
        {"country": row["countryiso3code"], "year": int(row["date"]), "voice_accountability": row["value"]}
        for row in rows
    ])
    return df

def run():
    project_root = Path(__file__).resolve().parents[4]
    dest_dir = project_root / "data/final_project/rushan-ajizu"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_file = dest_dir / "manifesto_voice_accountability.csv"

    df_manifesto = load_manifesto_data()
    df_wgi = load_voice_accountability()
    df_merged = pd.merge(df_manifesto, df_wgi, on=["country", "year"], how="left")
    df_merged.to_csv(dest_file, index=False)
    print(f"Data acquired and saved to {dest_file.relative_to(project_root)}")
    return df_merged

if __name__ == "__main__":
    run()

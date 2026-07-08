import pandas as pd
from pathlib import Path

def load_jst_data():
    project_root = Path(__file__).resolve().parents[4]
    source_path = project_root / "data/final_project/cory-baird/jst_panel.parquet"
    if not source_path.exists():
        raise FileNotFoundError(f"Source JST data not found at {source_path}")
    df = pd.read_parquet(source_path)
    cols = ["date", "country", "country_name", "rgdpmad", "debtgdp"]
    df_subset = df[cols].copy()
    df_subset["year"] = df_subset["date"]
    df_filtered = df_subset[(df_subset["year"] >= 1960) & (df_subset["country"].isin(["USA", "GBR", "DEU", "FRA", "JPN", "CAN", "ITA"]))]
    return df_filtered

def load_weo_revenue():
    project_root = Path(__file__).resolve().parents[4]
    source_path = project_root / "data/final_project/cory-baird/imf_weo_countries.parquet"
    if not source_path.exists():
        raise FileNotFoundError(f"Source WEO data not found at {source_path}")
    df = pd.read_parquet(source_path)
    df_filtered = df[(df["weo_subject_code"] == "GGR_NGDP") & (df["iso"].isin(["USA", "GBR", "DEU", "FRA", "JPN", "CAN", "ITA"]))]
    df_subset = df_filtered[["iso", "year", "value"]].copy()
    df_subset = df_subset.rename(columns={"iso": "country", "value": "gov_revenue_gdp"})
    return df_subset

def run():
    project_root = Path(__file__).resolve().parents[4]
    dest_dir = project_root / "data/final_project/cory-baird"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_file = dest_dir / "macro_growth_debt.csv"
    
    df_jst = load_jst_data()
    df_weo = load_weo_revenue()
    df_merged = pd.merge(df_jst, df_weo, on=["country", "year"], how="left")
    df_merged.to_csv(dest_file, index=False)
    print(f"Data acquired and saved to {dest_file.relative_to(project_root)}")
    return df_merged

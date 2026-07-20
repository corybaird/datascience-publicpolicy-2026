import pandas as pd
from pathlib import Path

EXPOSURE_SCORE_MAP = {
    "Not Exposed": 0,
    "Minimal Exposure": 1,
    "Exposed: Gradient 1": 2,
    "Exposed: Gradient 2": 3,
    "Exposed: Gradient 3": 4,
    "Exposed: Gradient 4": 5,
}

def process_exposure(df):
    df = df.copy()
    df["exposure_score"] = df["potential25"].map(EXPOSURE_SCORE_MAP)
    df["isco08_code"] = df["isco08_2d"].str.split(" - ").str[0].astype(int)
    df["isco08_label"] = df["isco08_2d"].str.split(" - ").str[1]
    return (
        df.groupby(["isco08_code", "isco08_label"])
        .agg(exposure_score=("exposure_score", "mean"), n_tasks=("exposure_score", "size"))
        .reset_index()
    )

def process_employment(df):
    df = df.copy()
    df["isco08_code"] = df["classif1.label"].str.extract(r"2 digit level:\s*(\d+)\s*-").astype(int)
    df["year"] = df["time"].astype(int)

    latest_year = df["year"].max()
    df_latest = df[df["year"] == latest_year]

    employment_wide = df_latest.pivot_table(
        index="isco08_code", columns="sex.label", values="obs_value", aggfunc="sum"
    ).reset_index()
    employment_wide = employment_wide.rename(columns={"Female": "employment_female", "Male": "employment_male"})
    employment_wide["year"] = latest_year
    return employment_wide

def run():
    project_root = Path(__file__).resolve().parents[4]
    data_dir = project_root / "data/final_project/sheena-pham"
    exposure_file = data_dir / "ai_exposure_raw.csv"
    employment_file = data_dir / "employment_raw.csv"
    if not exposure_file.exists() or not employment_file.exists():
        raise FileNotFoundError(f"Raw data not found in {data_dir}. Run download stage first.")

    df_exposure_raw = pd.read_csv(exposure_file)
    df_employment_raw = pd.read_csv(employment_file)

    df_exposure = process_exposure(df_exposure_raw)
    df_employment = process_employment(df_employment_raw)

    df = pd.merge(df_exposure, df_employment, on="isco08_code", how="inner")
    df["employment_total"] = df["employment_female"] + df["employment_male"]
    df["female_share"] = df["employment_female"] / df["employment_total"]
    df["is_clerical"] = df["isco08_code"] // 10 == 4

    df_clean = df.dropna(subset=["exposure_score", "female_share"]).copy()
    df_clean = df_clean.sort_values("exposure_score", ascending=False).reset_index(drop=True)

    dest_file = data_dir / "processed_gender_ai_exposure.csv"
    df_clean.to_csv(dest_file, index=False)
    print(f"Data processed and saved to {dest_file.relative_to(project_root)} with shape {df_clean.shape}")
    return df_clean

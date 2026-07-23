import pandas as pd
from pathlib import Path

def clean_low_bw(df_low_bw):
    df_subset = df_low_bw[["REF_AREA", "TIME_PERIOD", "OBS_VALUE"]].copy()
    df_subset = df_subset.rename(columns={"REF_AREA": "country_code", "TIME_PERIOD": "year", "OBS_VALUE": "lowb_pct"})
    return df_subset

def clean_parental_leave(df_parental_leave):
    measure_map = {
        "Total length of paid paternity and parental leave reserved for fathers": "leave_fathers",
        "Total length of paid maternity and parental leave available to mothers": "leave_mothers",
    }
    df_filtered = df_parental_leave[df_parental_leave["Measure"].isin(measure_map)].assign(Measure=lambda d: d["Measure"].map(measure_map))
    df_pivot = df_filtered.pivot_table(index=["REF_AREA", "TIME_PERIOD"], columns="Measure", values="OBS_VALUE").reset_index()
    df_pivot.columns.name = None
    df_pivot = df_pivot.rename(columns={"REF_AREA": "country_code", "TIME_PERIOD": "year"})
    return df_pivot

def run():
    project_root = Path(__file__).resolve().parents[4]
    source_dir = project_root / "data/final_project/ruoran-wang"
    dest_file = source_dir / "low_bw_parental_leave_clean.csv"

    df_low_bw = pd.read_csv(source_dir / "low_bw_raw.csv")
    df_parental_leave = pd.read_csv(source_dir / "parental_leave_raw.csv")

    df_low_bw_clean = clean_low_bw(df_low_bw)
    df_parental_leave_clean = clean_parental_leave(df_parental_leave)
    df_merged = df_low_bw_clean.merge(df_parental_leave_clean, on=["country_code", "year"], how="inner")

    df_merged.to_csv(dest_file, index=False)
    print(f"Data processed and saved to {dest_file.relative_to(project_root)} with shape {df_merged.shape}")
    return df_merged

if __name__ == "__main__":
    run()

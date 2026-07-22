import pandas as pd
from pathlib import Path

def load_gpr_data():
    project_root = Path(__file__).resolve().parents[4]
    source_path = project_root / "data/final_project/katsuhiro-kita/data_gpr_export.xls"
    if not source_path.exists():
        raise FileNotFoundError(f"Source GPR data not found at {source_path}")
    df = pd.read_excel(source_path)
    df_subset = df[["month", "GPR", "GPRT", "GPRA"]].rename(columns={"month": "date", "GPR": "gpr_index", "GPRT": "gpr_threat", "GPRA": "gpr_act"})
    return df_subset

def load_ebp_data():
    project_root = Path(__file__).resolve().parents[4]
    source_path = project_root / "data/final_project/katsuhiro-kita/ebp_csv.csv"
    if not source_path.exists():
        raise FileNotFoundError(f"Source EBP data not found at {source_path}")
    df = pd.read_csv(source_path)
    return df

def run():
    project_root = Path(__file__).resolve().parents[4]
    dest_dir = project_root / "data/final_project/katsuhiro-kita"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_file = dest_dir / "gpr_market_stress.csv"

    df_gpr = load_gpr_data()
    df_ebp = load_ebp_data()
    df_gpr["date"] = pd.to_datetime(df_gpr["date"])
    df_ebp["date"] = pd.to_datetime(df_ebp["date"])
    df_merged = pd.merge(df_gpr, df_ebp, on="date", how="inner")
    df_merged = df_merged.dropna(subset=["gpr_index", "gz_spread"])
    df_merged.to_csv(dest_file, index=False)
    print(f"Data acquired and saved to {dest_file.relative_to(project_root)}")
    return df_merged

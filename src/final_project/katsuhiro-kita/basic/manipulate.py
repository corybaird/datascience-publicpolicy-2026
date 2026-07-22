import pandas as pd
from pathlib import Path

def run():
    project_root = Path(__file__).resolve().parents[4]
    data_file = project_root / "data/final_project/katsuhiro-kita/gpr_market_stress.csv"
    if not data_file.exists():
        raise FileNotFoundError(f"{data_file} not found. Run download stage first.")

    df = pd.read_csv(data_file)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    # Lagged GPR terms let us test whether past geopolitical risk predicts current stress,
    # rather than just moving together with it at the same point in time
    df["gpr_index_lag1"] = df["gpr_index"].shift(1)
    df["gpr_index_lag2"] = df["gpr_index"].shift(2)
    df["gpr_index_lag3"] = df["gpr_index"].shift(3)
    df["gz_spread_lag1"] = df["gz_spread"].shift(1)

    df_clean = df.dropna(subset=["gpr_index_lag1", "gpr_index_lag2", "gpr_index_lag3", "gz_spread_lag1"]).copy()

    dest_dir = project_root / "data/final_project/katsuhiro-kita"
    dest_file = dest_dir / "processed_gpr_market_stress.csv"
    df_clean.to_csv(dest_file, index=False)
    print(f"Data processed and saved to {dest_file.relative_to(project_root)} with shape {df_clean.shape}")
    return df_clean

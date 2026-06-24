import pandas as pd
from pathlib import Path

def run():
    project_root = Path(__file__).resolve().parents[4]
    data_file = project_root / "data/final_project/cory-baird/macro_growth_debt.csv"
    if not data_file.exists():
        raise FileNotFoundError(f"{data_file} not found. Run download stage first.")
        
    df = pd.read_csv(data_file)
    
    # Calculate growth and changes
    df["gdp_growth"] = df.groupby("country")["rgdpmad"].pct_change() * 100
    df["debt_change"] = df.groupby("country")["debtgdp"].diff()
    df["debt_change_lag1"] = df.groupby("country")["debt_change"].shift(1)
    df["gdp_growth_lag1"] = df.groupby("country")["gdp_growth"].shift(1)
    
    # Clean rows with missing data
    df_clean = df.dropna(subset=["gdp_growth", "debt_change_lag1", "gdp_growth_lag1", "gov_revenue_gdp"]).copy()
    
    # Save processed data
    dest_dir = project_root / "data/final_project/cory-baird"
    dest_file = dest_dir / "processed_macro_data.csv"
    df_clean.to_csv(dest_file, index=False)
    print(f"Data processed and saved to {dest_file.relative_to(project_root)} with shape {df_clean.shape}")
    return df_clean

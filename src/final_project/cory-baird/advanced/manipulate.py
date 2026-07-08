import pandas as pd
import yaml
from pathlib import Path

class DataManipulation:
    def __init__(self, config_path="references/configs/final_project/cory-baird/project_settings.yaml"):
        project_root = Path(__file__).resolve().parents[4]
        path_obj = Path(config_path)
        if not path_obj.is_absolute():
            self.config_path = project_root / path_obj
        else:
            self.config_path = path_obj

        if self.config_path.exists():
            with open(self.config_path) as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = {}

    def run(self):
        project_root = Path(__file__).resolve().parents[4]
        data_file = project_root / "data/final_project/cory-baird/macro_growth_debt.csv"
        if not data_file.exists():
            raise FileNotFoundError(f"{data_file} not found. Run download stage first.")
            
        df = pd.read_csv(data_file)
        
        # Calculate real GDP growth (economic growth) per country
        df["gdp_growth"] = df.groupby("country")["rgdpmad"].pct_change() * 100
        
        # Calculate change in government debt to GDP ratio per country
        df["debt_change"] = df.groupby("country")["debtgdp"].diff()
        
        # Calculate lags
        df["debt_change_lag1"] = df.groupby("country")["debt_change"].shift(1)
        df["gdp_growth_lag1"] = df.groupby("country")["gdp_growth"].shift(1)
        
        # Drop rows with missing values created by lags, diffs, and merged datasets (revenue data starts in 1980)
        df_clean = df.dropna(subset=["gdp_growth", "debt_change_lag1", "gdp_growth_lag1", "gov_revenue_gdp"]).copy()
        
        # Save processed data
        dest_dir = project_root / "data/final_project/cory-baird"
        dest_file = dest_dir / "processed_macro_data.csv"
        df_clean.to_csv(dest_file, index=False)
        print(f"Data processed and saved to {dest_file.relative_to(project_root)} with shape {df_clean.shape}")
        return df_clean

if __name__ == "__main__":
    dm = DataManipulation()
    dm.run()

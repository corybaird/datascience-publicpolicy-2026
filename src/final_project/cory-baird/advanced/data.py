import pandas as pd
import yaml
import sys
from pathlib import Path

# Add the dictionary folder to sys.path to enable clean imports
dict_dir = (Path(__file__).resolve().parents[4] / "references/dictionaries/final_project/cory-baird").resolve()
if str(dict_dir) not in sys.path:
    sys.path.insert(0, str(dict_dir))

from country_mapping import COUNTRY_NAMES

class DataAcquisition:
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

    def load_jst_data(self):
        project_root = Path(__file__).resolve().parents[4]
        source_path = project_root.parent / "macroeconomics-data/data/panel/annual/jst_panel.parquet"
        if not source_path.exists():
            raise FileNotFoundError(f"Source JST data not found at {source_path}")
        df = pd.read_parquet(source_path)
        cols = ["date", "country", "country_name", "rgdpmad", "debtgdp"]
        df_subset = df[cols].copy()
        df_subset["year"] = df_subset["date"]
        df_filtered = df_subset[(df_subset["year"] >= 1960) & (df_subset["country"].isin(["USA", "GBR", "DEU", "FRA", "JPN", "CAN", "ITA"]))]
        return df_filtered

    def load_weo_revenue(self):
        project_root = Path(__file__).resolve().parents[4]
        source_path = project_root.parent / "macroeconomics-data/data/raw/annual/economic/imf_weo_countries.parquet"
        if not source_path.exists():
            raise FileNotFoundError(f"Source WEO data not found at {source_path}")
        df = pd.read_parquet(source_path)
        df_filtered = df[(df["weo_subject_code"] == "GGR_NGDP") & (df["iso"].isin(["USA", "GBR", "DEU", "FRA", "JPN", "CAN", "ITA"]))]
        df_subset = df_filtered[["iso", "year", "value"]].copy()
        df_subset = df_subset.rename(columns={"iso": "country", "value": "gov_revenue_gdp"})
        return df_subset

    def load_country_mapping(self):
        return COUNTRY_NAMES

    def run(self):
        project_root = Path(__file__).resolve().parents[4]
        dest_dir = project_root / "data/final_project/cory-baird"
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_file = dest_dir / "macro_growth_debt.csv"
        
        try:
            # 1. Load primary dataset
            df_jst = self.load_jst_data()
            
            # 2. Load secondary dataset
            df_weo = self.load_weo_revenue()
            
            # 3. Load country mapping metadata
            mapping = self.load_country_mapping()
            
            # Map full names using the dictionary to verify integration
            df_jst["country_name_mapped"] = df_jst["country"].map(mapping).fillna(df_jst["country_name"])
            df_jst = df_jst.drop(columns=["country_name"]).rename(columns={"country_name_mapped": "country_name"})
            
            # 4. Merge datasets
            df_merged = pd.merge(df_jst, df_weo, on=["country", "year"], how="left")
            
            # Save raw dataset
            df_merged.to_csv(dest_file, index=False)
            print(f"Data acquired and saved to {dest_file.relative_to(project_root)}")
            return df_merged
        except Exception as e:
            if dest_file.exists():
                print(f"Acquisition failed but loading cached data: {e}")
                return pd.read_csv(dest_file)
            else:
                raise e

if __name__ == "__main__":
    da = DataAcquisition()
    da.run()

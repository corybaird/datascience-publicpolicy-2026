import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import yaml
import sys
from pathlib import Path

# Add the dictionary folder to sys.path to enable clean imports
dict_dir = (Path(__file__).resolve().parents[4] / "references/dictionaries/final_project/cory-baird").resolve()
if str(dict_dir) not in sys.path:
    sys.path.insert(0, str(dict_dir))

from country_mapping import COUNTRY_NAMES

class DataVisualization:
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
        data_file = project_root / "data/final_project/cory-baird/processed_macro_data.csv"
        if not data_file.exists():
            raise FileNotFoundError(f"{data_file} not found. Run manipulate stage first.")
            
        df = pd.read_csv(data_file)
        
        # Map country codes to full country names for visualization
        df["Country Name"] = df["country"].map(COUNTRY_NAMES).fillna(df["country"])
        
        dest_dir = project_root / "reports/final_project/cory-baird"
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_file = dest_dir / "debt_growth_scatter.png"
        
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x="debt_change_lag1", y="gdp_growth", hue="Country Name", alpha=0.6)
        sns.regplot(data=df, x="debt_change_lag1", y="gdp_growth", scatter=False, line_kws={"color": "red", "linewidth": 2})
        
        plt.title("Economic Growth vs. Lagged Government Debt Changes (G7 Countries)")
        plt.xlabel("Lagged Change in Government Debt to GDP Ratio (t-1)")
        plt.ylabel("Real GDP per Capita Growth (t)")
        plt.tight_layout()
        plt.savefig(dest_file)
        plt.close()
        print(f"Scatter plot saved to {dest_file.relative_to(project_root)}")
        return dest_file.relative_to(project_root)

if __name__ == "__main__":
    dv = DataVisualization()
    dv.run()

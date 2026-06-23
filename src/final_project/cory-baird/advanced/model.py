import pandas as pd
import yaml
from pathlib import Path
from stats_transformer.models.regression.panel import PanelRegressionModel

class EconometricModeling:
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
        
        # Load parameters from configuration
        target = self.config.get("target_variable", "gdp_growth")
        independent_vars = self.config.get("independent_variables", ["debt_change_lag1", "gdp_growth_lag1", "gov_revenue_gdp"])
        entity_col = self.config.get("entity_column", "country")
        date_col = self.config.get("date_column", "year")
        
        # Initialize and fit the PanelOLS model via stats-transformer
        model = PanelRegressionModel(
            target=target,
            independent_variables=independent_vars,
            entity_column=entity_col,
            time_column=date_col
        )
        
        model.load_data(df)
        model.build_model()
        
        print("=== Regression Results Summary ===")
        print(model.get_summary())
        return model.get_summary()

if __name__ == "__main__":
    em = EconometricModeling()
    em.run()

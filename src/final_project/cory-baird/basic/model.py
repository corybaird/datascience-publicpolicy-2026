import pandas as pd
from pathlib import Path
from stats_transformer.models.regression.panel import PanelRegressionModel

def run():
    project_root = Path(__file__).resolve().parents[4]
    data_file = project_root / "data/final_project/cory-baird/processed_macro_data.csv"
    if not data_file.exists():
        raise FileNotFoundError(f"{data_file} not found. Run manipulate stage first.")
        
    df = pd.read_csv(data_file)
    
    # Initialize and fit the PanelOLS model
    model = PanelRegressionModel(
        target="gdp_growth",
        independent_variables=["debt_change_lag1", "gdp_growth_lag1", "gov_revenue_gdp"],
        entity_column="country",
        time_column="year"
    )
    model.load_data(df)
    model.build_model()
    
    print("=== Regression Results Summary ===")
    print(model.get_summary())
    return model.get_summary()

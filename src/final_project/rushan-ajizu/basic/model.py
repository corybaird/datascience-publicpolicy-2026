import pandas as pd
from pathlib import Path
from stats_transformer.models.regression.panel import PanelRegressionModel

def run():
    project_root = Path(__file__).resolve().parents[4]
    data_file = project_root / "data/final_project/rushan-ajizu/processed_religion_democracy.csv"
    if not data_file.exists():
        raise FileNotFoundError(f"{data_file} not found. Run manipulate stage first.")

    df = pd.read_csv(data_file)

    model = PanelRegressionModel(
        target="religious_rhetoric_rate",
        independent_variables=["voice_accountability"],
        entity_column="country",
        time_column="year",
        entity_effects=True,
    )
    model.load_data(df)
    model.build_model()

    print("=== Regression Results Summary ===")
    print(model.get_summary())
    return model.get_summary()

if __name__ == "__main__":
    run()

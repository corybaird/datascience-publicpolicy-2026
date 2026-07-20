import pandas as pd
import statsmodels.formula.api as smf
from pathlib import Path

def run():
    project_root = Path(__file__).resolve().parents[4]
    data_file = project_root / "data/final_project/sheena-pham/processed_gender_ai_exposure.csv"
    if not data_file.exists():
        raise FileNotFoundError(f"{data_file} not found. Run manipulate stage first.")

    df = pd.read_csv(data_file)

    # Cross-sectional OLS across ISCO-08 2-digit sub-major occupation groups (Australia).
    model = smf.ols("exposure_score ~ female_share", data=df).fit()

    print("=== Regression Results Summary ===")
    print(model.summary())
    return model.summary()

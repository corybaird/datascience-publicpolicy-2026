import pandas as pd
import statsmodels.api as sm
from pathlib import Path

def run():
    project_root = Path(__file__).resolve().parents[4]
    data_file = project_root / "data/final_project/Ling-Syuan/processed_education_fertility.csv"
    if not data_file.exists():
        raise FileNotFoundError(f"{data_file} not found. Run manipulate stage first.")

    df = pd.read_csv(data_file)

    df_reg = df[df["educational_attainment_level"] == "Tertiary education"].dropna(
        subset=["per cent", "fertility_rate"]
    ).copy()
    df_reg = df_reg.rename(columns={"per cent": "tertiary"})

    X = sm.add_constant(df_reg["tertiary"])
    y = df_reg["fertility_rate"]
    fit_model = sm.OLS(y, X).fit()

    print("=== Regression Results Summary ===")
    print(fit_model.summary())
    return fit_model.summary()

import pandas as pd
import statsmodels.api as sm
from pathlib import Path


class EconometricModeling:
    def run(self):
        project_root = Path(__file__).resolve().parents[4]
        data_file = project_root / "data/final_project/qicheng-lee/clean/state_cross_section.csv"
        if not data_file.exists():
            raise FileNotFoundError(f"{data_file} not found. Run manipulate stage first.")

        df = pd.read_csv(data_file)

        X = sm.add_constant(df[["share_foreign", "log_inventor_count"]])
        y = df["log_patents"]

        fitted = sm.OLS(y, X).fit(cov_type="HC1")  # heteroskedasticity-robust SEs

        print("=== Regression Results Summary ===")
        print(fitted.summary())
        return fitted.summary()


if __name__ == "__main__":
    em = EconometricModeling()
    em.run()
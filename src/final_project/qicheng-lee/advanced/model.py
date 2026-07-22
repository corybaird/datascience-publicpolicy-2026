import pandas as pd
import statsmodels.api as sm

from paths import PROJECT_ROOT


class EconometricModeling:
    def run(self):
        project_root = PROJECT_ROOT
        data_file = project_root / "data/final_project/qicheng-lee/clean/state_cross_section.csv"
        if not data_file.exists():
            raise FileNotFoundError(f"{data_file} not found. Run manipulate stage first.")

        df = pd.read_csv(data_file)
        y = df["log_patents"]

        # Model 1: bivariate, no control for state size. Shows the naive/raw
        # association implied by the Figure 2 scatter's fitted line.
        X_bivariate = sm.add_constant(df[["share_foreign"]])
        fitted_bivariate = sm.OLS(y, X_bivariate).fit(cov_type="HC1")

        # Model 2: controls for the size of each state's inventor pool. This is
        # the primary specification - see whether share_foreign's coefficient
        # survives once state size is accounted for.
        X_controlled = sm.add_constant(df[["share_foreign", "log_inventor_count"]])
        fitted_controlled = sm.OLS(y, X_controlled).fit(cov_type="HC1")

        print("=== Model 1: Without Inventor Count Control ===")
        print(fitted_bivariate.summary())
        print("\n=== Model 2: With Inventor Count Control (Primary Specification) ===")
        print(fitted_controlled.summary())

        return {"bivariate": fitted_bivariate.summary(), "controlled": fitted_controlled.summary()}


if __name__ == "__main__":
    em = EconometricModeling()
    em.run()
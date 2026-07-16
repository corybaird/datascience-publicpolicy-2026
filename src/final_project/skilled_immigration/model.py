from pathlib import Path

import pandas as pd
import statsmodels.api as sm

import data
import manipulate


def run(project_root: Path | None = None):
    root = project_root or data.find_project_root()
    annual = manipulate.run(root)["annual"]

    dependent = annual["n_speeches"]
    independent = sm.add_constant(annual[["year_centered"]])
    result = sm.OLS(dependent, independent).fit()

    output_dir = root / "data" / "final_project" / data.PROJECT_NAME / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "ols_summary.txt").write_text(
        result.summary().as_text(), encoding="utf-8"
    )

    confidence = result.conf_int()
    coefficients = pd.DataFrame(
        {
            "term": result.params.index,
            "coefficient": result.params.values,
            "std_error": result.bse.values,
            "p_value": result.pvalues.values,
            "ci_lower": confidence[0].values,
            "ci_upper": confidence[1].values,
        }
    )
    coefficients.to_csv(output_dir / "ols_coefficients.csv", index=False)
    return result


if __name__ == "__main__":
    print(run().summary())

from pathlib import Path

import pandas as pd
import statsmodels.api as sm

from manipulate import DataManipulation
from settings import load_settings


class EconometricModeling:
    def __init__(self, config_path: str | Path, project_root: Path | None = None):
        self.config, self.project_root = load_settings(config_path, project_root)
        self.manipulator = DataManipulation(config_path, self.project_root)
        self.processed_dir = self.project_root / self.config["paths"]["processed_dir"]

    def run(self):
        annual = self.manipulator.run()["annual"]
        dependent_name = self.config["model"]["dependent"]
        independent_name = self.config["model"]["independent"]
        y = annual[dependent_name]
        x = sm.add_constant(annual[[independent_name]])
        result = sm.OLS(y, x).fit()
        self._save(result)
        return result

    def _save(self, result) -> None:
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        (self.processed_dir / "advanced_ols_summary.txt").write_text(result.summary().as_text(), encoding="utf-8")
        confidence = result.conf_int()
        coefficients = pd.DataFrame({
            "term": result.params.index,
            "coefficient": result.params.values,
            "std_error": result.bse.values,
            "p_value": result.pvalues.values,
            "ci_lower": confidence[0].values,
            "ci_upper": confidence[1].values,
        })
        coefficients.to_csv(self.processed_dir / "advanced_ols_coefficients.csv", index=False)

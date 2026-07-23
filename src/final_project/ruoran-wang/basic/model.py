import pandas as pd
from pathlib import Path
from stats_transformer.models.regression.regression import RegressionModel
from stats_transformer.models.regression.panel import PanelRegressionModel

def run_pooled_ols(df, leave_var):
    model = RegressionModel(target="lowb_pct", independent_variables=[leave_var])
    model.load_data(df)
    model.build_model()
    return model.model

def run_panel_fe(df, leave_var, entity_effects, time_effects):
    model = PanelRegressionModel(
        target="lowb_pct",
        independent_variables=[leave_var],
        entity_column="country_code",
        time_column="year",
        entity_effects=entity_effects,
        time_effects=time_effects,
    )
    model.load_data(df)
    model.build_model()
    return model.model

def extract_coef_row(fitted, leave_var, label):
    std_err = fitted.bse if hasattr(fitted, "bse") else fitted.std_errors
    return {
        "Regression": label,
        "Variable": leave_var,
        "Coefficient": fitted.params[leave_var],
        "Std. Error": std_err[leave_var],
        "P-value": fitted.pvalues[leave_var],
    }

def run():
    project_root = Path(__file__).resolve().parents[4]
    data_file = project_root / "data/final_project/ruoran-wang/low_bw_parental_leave_clean.csv"
    if not data_file.exists():
        raise FileNotFoundError(f"{data_file} not found. Run manipulate stage first.")

    df = pd.read_csv(data_file)
    leave_vars = ["leave_fathers", "leave_mothers"]
    specs = [
        ("Pooled OLS", lambda lv: run_pooled_ols(df, lv)),
        ("Country FE", lambda lv: run_panel_fe(df, lv, entity_effects=True, time_effects=False)),
        ("Year FE", lambda lv: run_panel_fe(df, lv, entity_effects=False, time_effects=True)),
    ]

    rows = []
    for label, fit_fn in specs:
        for leave_var in leave_vars:
            fitted = fit_fn(leave_var)
            rows.append(extract_coef_row(fitted, leave_var, label))

    return pd.DataFrame(rows)

if __name__ == "__main__":
    run()

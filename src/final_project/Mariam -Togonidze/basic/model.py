"""
Model building and analysis module for final project.
"""
import os
import pandas as pd
import statsmodels.api as sm

def run():
    processed_path = os.path.join("data", "final_project", "Mariam -Togonidze", "processed_macro_data.csv")
    df = pd.read_csv(processed_path)

    # Define variables
    Y = df["gdp_growth"]
    X = df[["debt_change_lag1", "gov_revenue_gdp"]]
    X_const = sm.add_constant(X)

    # OLS Regression
    model = sm.OLS(Y, X_const).fit()
    print(model.summary())
    return model

if __name__ == "__main__":
    run()

"""
Data manipulation and feature engineering module for final project.
"""
import os
import pandas as pd
import data

def run():
    raw_path = os.path.join("data", "final_project", "Mariam -Togonidze", "macro_growth_debt.csv")
    processed_path = os.path.join("data", "final_project", "Mariam -Togonidze", "processed_macro_data.csv")
    
    # Load raw data
    if not os.path.exists(raw_path):
        df = data.run()
    else:
        df = pd.read_csv(raw_path)

    # Sort data cleanly
    df = df.sort_values(by=["country", "date"])
    
    # Calculate simple growth and change metrics
    df["gdp_growth"] = df.groupby("country")["rgdpmad"].pct_change() * 100
    df["debt_change"] = df.groupby("country")["debtgdp"].diff()
    df["debt_change_lag1"] = df.groupby("country")["debt_change"].shift(1)
    
    # Drop rows with missing values created by lagging/differencing
    df_clean = df.dropna().copy()
    
    # Save cleaned file
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    df_clean.to_csv(processed_path, index=False)
    
    print(f"Data processed and saved to {processed_path} with shape {df_clean.shape}")
    return df_clean

if __name__ == "__main__":
    run()

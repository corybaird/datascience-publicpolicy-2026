"""
Visualization and graphing module for final project.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt

def run():
    processed_path = os.path.join("data", "final_project", "Mariam -Togonidze", "processed_macro_data.csv")
    df = pd.read_csv(processed_path)

    # Graph 1: Simple Bar Chart of Government Revenue
    plt.figure(figsize=(8, 4))
    avg_rev = df.groupby("country_name")["gov_revenue_gdp"].mean()
    plt.bar(avg_rev.index, avg_rev.values, color="navy", alpha=0.8)
    plt.title("Average Government Revenue (% of GDP) by Country", fontsize=12)
    plt.xlabel("Country", fontsize=10)
    plt.ylabel("Revenue / GDP (%)", fontsize=10)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()

    # Graph 2: Simple Scatter Plot of Lagged Debt Change vs GDP Growth
    plt.figure(figsize=(8, 4))
    plt.scatter(df["debt_change_lag1"], df["gdp_growth"], color="teal", alpha=0.7)
    plt.title("Lagged Debt Change vs GDP Growth Rate", fontsize=12)
    plt.xlabel("Lagged Change in Debt-to-GDP Ratio", fontsize=10)
    plt.ylabel("Real GDP Growth Rate (%)", fontsize=10)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run()
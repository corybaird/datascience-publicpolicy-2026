import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path

def run():
    project_root = Path(__file__).resolve().parents[4]
    data_file = project_root / "data/final_project/cory-baird/processed_macro_data.csv"
    if not data_file.exists():
        raise FileNotFoundError(f"{data_file} not found. Run manipulate stage first.")
        
    df = pd.read_csv(data_file)
    
    dest_dir = project_root / "reports/final_project/cory-baird"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_file = dest_dir / "debt_growth_scatter.png"
    
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="debt_change_lag1", y="gdp_growth", hue="country_name", alpha=0.6)
    sns.regplot(data=df, x="debt_change_lag1", y="gdp_growth", scatter=False, line_kws={"color": "red", "linewidth": 2})
    
    plt.title("Economic Growth vs. Lagged Government Debt Changes (G7 Countries)")
    plt.xlabel("Lagged Change in Government Debt to GDP Ratio (t-1)")
    plt.ylabel("Real GDP per Capita Growth (t)")
    plt.tight_layout()
    plt.savefig(dest_file)
    plt.close()
    print(f"Scatter plot saved to {dest_file.relative_to(project_root)}")
    return dest_file.relative_to(project_root)

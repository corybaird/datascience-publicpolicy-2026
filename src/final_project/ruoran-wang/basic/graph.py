import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

def run():
    project_root = Path(__file__).resolve().parents[4]
    data_file = project_root / "data/final_project/ruoran-wang/low_bw_parental_leave_clean.csv"
    if not data_file.exists():
        raise FileNotFoundError(f"{data_file} not found. Run manipulate stage first.")

    df = pd.read_csv(data_file)
    country_avg = df.groupby("country_code")[["lowb_pct", "leave_fathers", "leave_mothers"]].mean().reset_index()

    dest_dir = project_root / "reports/final_project/ruoran-wang"
    dest_dir.mkdir(parents=True, exist_ok=True)

    fathers_dest = dest_dir / "low_bw_vs_leave_fathers_scatter.png"
    plt.figure(figsize=(8, 5))
    plt.scatter(country_avg["lowb_pct"], country_avg["leave_fathers"], color="#55A868", alpha=0.8, edgecolors="white", linewidth=0.5, s=80)
    plt.title("Average Paid Leave for Fathers vs. Average Low Birthweight Rate by Country")
    plt.xlabel("Average Low Birthweight (% of live births)")
    plt.ylabel("Average Paid Leave for Fathers (weeks)")
    plt.grid(linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(fathers_dest)
    plt.close()
    print(f"Scatter plot saved to {fathers_dest.relative_to(project_root)}")

    mothers_dest = dest_dir / "low_bw_vs_leave_mothers_scatter.png"
    plt.figure(figsize=(8, 5))
    plt.scatter(country_avg["lowb_pct"], country_avg["leave_mothers"], color="#C44E52", alpha=0.8, edgecolors="white", linewidth=0.5, s=80)
    plt.title("Average Paid Leave for Mothers vs. Average Low Birthweight Rate by Country")
    plt.xlabel("Average Low Birthweight (% of live births)")
    plt.ylabel("Average Paid Leave for Mothers (weeks)")
    plt.grid(linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(mothers_dest)
    plt.close()
    print(f"Scatter plot saved to {mothers_dest.relative_to(project_root)}")

    return fathers_dest.relative_to(project_root), mothers_dest.relative_to(project_root)

if __name__ == "__main__":
    run()

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path


class DataVisualization:
    def run(self):
        project_root = Path(__file__).resolve().parents[4]
        data_file = project_root / "data/final_project/qicheng-lee/state_cross_section.csv"
        if not data_file.exists():
            raise FileNotFoundError(f"{data_file} not found. Run manipulate stage first.")

        df = pd.read_csv(data_file)
        dest_dir = project_root / "reports/final_project/qicheng-lee"
        dest_dir.mkdir(parents=True, exist_ok=True)

        top = df.sort_values("share_foreign", ascending=False)
        plt.figure(figsize=(10, 12))
        sns.barplot(data=top, y="state", x="share_foreign", color="steelblue")
        plt.title("Name-Inferred Foreign-Origin Inventor Share by State (2025)")
        plt.xlabel("Share of Foreign-Origin-Coded Inventor Names")
        plt.ylabel("State")
        plt.tight_layout()
        fig1 = dest_dir / "foreign_share_by_state.png"
        plt.savefig(fig1)
        plt.close()

        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x="share_foreign", y="log_patents", size="inventor_count", legend=False, alpha=0.7)
        sns.regplot(data=df, x="share_foreign", y="log_patents", scatter=False, line_kws={"color": "red"})
        plt.title("State Patent Output vs. Foreign-Origin Inventor Share (2025)")
        plt.xlabel("Share of Foreign-Origin-Coded Inventor Names")
        plt.ylabel("log(Patent Count)")
        plt.tight_layout()
        fig2 = dest_dir / "patents_vs_foreign_share.png"
        plt.savefig(fig2)
        plt.close()

        print(f"Figures saved to {dest_dir.relative_to(project_root)}")
        return [fig1, fig2]


if __name__ == "__main__":
    dv = DataVisualization()
    dv.run()
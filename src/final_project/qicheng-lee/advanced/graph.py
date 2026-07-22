import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from paths import PROJECT_ROOT


class DataVisualization:
    def run(self):
        project_root = PROJECT_ROOT
        clean_dir = project_root / "data/final_project/qicheng-lee/clean"
        data_file = clean_dir / "state_cross_section.csv"
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

        # Descriptive-only: full name-inferred nationality composition of the
        # inventor pool, nationwide. Not used in the regression (that stays on
        # the aggregate share_foreign) - this exists so the write-up can show
        # which groups are actually largest in the data rather than asserting it.
        figs = [fig1, fig2]
        breakdown_file = clean_dir / "nationality_breakdown.csv"
        if breakdown_file.exists():
            breakdown = pd.read_csv(breakdown_file).sort_values("inventor_count", ascending=False)
            plt.figure(figsize=(10, 8))
            sns.barplot(data=breakdown, y="nationality_name", x="share", color="steelblue")
            plt.title("Name-Inferred Nationality Composition of US Patent Inventors (2025)")
            plt.xlabel("Share of Classified Inventors (Descriptive Only)")
            plt.ylabel("Name-Inferred Nationality")
            plt.tight_layout()
            fig3 = dest_dir / "nationality_breakdown.png"
            plt.savefig(fig3)
            plt.close()
            figs.append(fig3)

        print(f"Figures saved to {dest_dir.relative_to(project_root)}")
        return figs


if __name__ == "__main__":
    dv = DataVisualization()
    dv.run()
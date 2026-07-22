import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path

def plot_fertility_by_education(df, dest_dir, project_root):
    """Plot 1: Bar chart of mean educational attainment across fertility groups."""
    desired_order = [
        "Below upper secondary education",
        "Upper secondary or post-secondary non-tertiary education",
        "Tertiary education"
    ]

    df_groupby_analysis = df.groupby(
        ["fertility_group", "educational_attainment_level"], observed=False
    )["per cent"].agg(
        mean="mean",
        median="median",
        min="min",
        max="max"
    ).dropna().round(3)
    df_groupby_analysis = df_groupby_analysis.reindex(desired_order, level=1)

    new_labels = ["Hyper-Low Fertility\n(<=1.3)", "Sub-Replacement\n(1.3-2.1)", "Replacement & Above\n(>2.1)"]

    df_plot = df_groupby_analysis["mean"].unstack().reindex(columns=desired_order)
    df_plot.index = new_labels
    df_plot = df_plot.reset_index().rename(columns={"index": "fertility_group"})

    df_melted = df_plot.melt(
        id_vars="fertility_group",
        var_name="Educational Attainment",
        value_name="Percentage"
    )

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(11, 6))

    pink_palette = ["#E44A78", "#F791BA", "#FCCDE2"]

    sns.barplot(
        data=df_melted,
        x="fertility_group",
        y="Percentage",
        hue="Educational Attainment",
        palette=pink_palette
    )

    plt.title("Educational Attainment across Different Fertility Groups", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Fertility Groups", fontsize=12, labelpad=10)
    plt.ylabel("Percentage(%)", fontsize=12, labelpad=10)
    plt.legend(title="Educational Attainment", bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
    plt.tight_layout()

    dest_file = dest_dir / "fertility_education_bar.png"
    plt.savefig(dest_file)
    plt.close()
    print(f"Bar chart saved to {dest_file.relative_to(project_root)}")
    return dest_file.relative_to(project_root)

def plot_tertiary_scatter(df, dest_dir, project_root):
    """Plot 2: Scatter plot of tertiary education attainment vs. fertility rate."""
    df_scatter_data = df[df["educational_attainment_level"] == "Tertiary education"].copy()

    pink_palette = ["#E44A78", "#F791BA", "#FCCDE2"]

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6))

    sns.scatterplot(
        data=df_scatter_data,
        x="per cent",
        y="fertility_rate",
        hue="fertility_group",
        palette=pink_palette,
        s=100,
        alpha=0.8
    )

    plt.title("The Relationship Between Higher Education and Fertility Rates", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Tertiary Education Attainment Rate (%)", fontsize=12, labelpad=10)
    plt.ylabel("Fertility Rate (Births per Woman)", fontsize=12, labelpad=10)
    plt.legend(title="Fertility Status", bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()

    dest_file = dest_dir / "tertiary_fertility_scatter.png"
    plt.savefig(dest_file)
    plt.close()
    print(f"Scatter plot saved to {dest_file.relative_to(project_root)}")
    return dest_file.relative_to(project_root)

def run():
    project_root = Path(__file__).resolve().parents[4]
    data_file = project_root / "data/final_project/Ling-Syuan/processed_education_fertility.csv"
    if not data_file.exists():
        raise FileNotFoundError(f"{data_file} not found. Run manipulate stage first.")

    df = pd.read_csv(data_file)

    dest_dir = project_root / "reports/final_project/Ling-Syuan"
    dest_dir.mkdir(parents=True, exist_ok=True)

    bar_path = plot_fertility_by_education(df, dest_dir, project_root)
    scatter_path = plot_tertiary_scatter(df, dest_dir, project_root)

    return bar_path, scatter_path

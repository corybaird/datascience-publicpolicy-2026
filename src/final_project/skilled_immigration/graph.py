from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import data
import manipulate


def run(project_root: Path | None = None) -> list[Path]:
    root = project_root or data.find_project_root()
    frames = manipulate.run(root)
    output_dir = root / "notebooks" / "hw" / "final_project" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)

    annual = frames["annual"]
    figure_paths: list[Path] = []

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(annual["year"], annual["n_speeches"], marker="o", linewidth=2)
    ax.set_title("Japanese Diet Speeches on Immigration-Related Topics, 2012–2024")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of speeches")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    path = output_dir / "annual_speech_volume.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    figure_paths.append(path)

    stance = frames["stance"]
    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(stance["stance"].astype(str), stance["share_pct"])
    ax.set_title("Overall Stance Distribution")
    ax.set_xlabel("Stance label")
    ax.set_ylabel("Share of classified speeches (%)")
    ax.set_ylim(0, max(stance["share_pct"]) * 1.18)
    for bar, value in zip(bars, stance["share_pct"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            f"{value:.1f}%",
            ha="center",
        )
    fig.tight_layout()
    path = output_dir / "stance_distribution.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    figure_paths.append(path)

    concentration = frames["concentration"].set_index("level")
    comparison = concentration.loc[["national_anti_speakers", "prefecture_median"]]
    fig, ax = plt.subplots(figsize=(8, 5))
    x = range(len(comparison))
    width = 0.35
    ax.bar(
        [i - width / 2 for i in x],
        comparison["top1_share_pct"],
        width,
        label="Top 1",
    )
    ax.bar(
        [i + width / 2 for i in x],
        comparison["top3_share_pct"],
        width,
        label="Top 3",
    )
    ax.set_xticks(list(x), ["National", "Median prefecture"])
    ax.set_title("Concentration of Anti-Immigration Speech")
    ax.set_ylabel("Share of anti-immigration speeches (%)")
    ax.legend()
    fig.tight_layout()
    path = output_dir / "speaker_concentration.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    figure_paths.append(path)

    return figure_paths


if __name__ == "__main__":
    for figure in run():
        print(figure)

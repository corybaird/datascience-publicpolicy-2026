from pathlib import Path

import matplotlib.pyplot as plt

from manipulate import DataManipulation
from settings import load_settings


class DataVisualization:
    def __init__(self, config_path: str | Path, project_root: Path | None = None):
        self.config, self.project_root = load_settings(config_path, project_root)
        self.manipulator = DataManipulation(config_path, self.project_root)
        self.figures_dir = self.project_root / self.config["paths"]["figures_dir"]
        self.dpi = int(self.config["visualization"]["dpi"])
        self.format = str(self.config["visualization"]["format"])

    def run(self) -> list[Path]:
        frames = self.manipulator.run()
        self.figures_dir.mkdir(parents=True, exist_ok=True)
        return [
            self._plot_attention(frames["annual"]),
            self._plot_stance(frames["stance"]),
            self._plot_concentration(frames["concentration"]),
        ]

    def _plot_attention(self, annual) -> Path:
        fig, ax = plt.subplots(figsize=(10, 5.5))
        ax.plot(annual["year"], annual["n_speeches"], marker="o", linewidth=2, label="Annual count")
        ax.plot(annual["year"], annual["rolling_mean"], linestyle="--", linewidth=2, label="3-year rolling mean")
        ax.set_title("Parliamentary Attention to Immigration-Related Topics")
        ax.set_xlabel("Year")
        ax.set_ylabel("Number of speeches")
        ax.grid(alpha=0.25)
        ax.legend()
        fig.tight_layout()
        path = self.figures_dir / f"advanced_attention_trend.{self.format}"
        fig.savefig(path, dpi=self.dpi)
        plt.close(fig)
        return path

    def _plot_stance(self, stance) -> Path:
        fig, ax = plt.subplots(figsize=(7.5, 5))
        bars = ax.bar(stance["stance"].astype(str), stance["share_pct"])
        ax.set_title("Stance Distribution in Classified Diet Speeches")
        ax.set_xlabel("Stance")
        ax.set_ylabel("Share of speeches (%)")
        ax.set_ylim(0, stance["share_pct"].max() * 1.18)
        for bar, value in zip(bars, stance["share_pct"]):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, f"{value:.1f}%", ha="center")
        fig.tight_layout()
        path = self.figures_dir / f"advanced_stance_distribution.{self.format}"
        fig.savefig(path, dpi=self.dpi)
        plt.close(fig)
        return path

    def _plot_concentration(self, concentration) -> Path:
        indexed = concentration.set_index("level")
        comparison = indexed.loc[["national_anti_speakers", "prefecture_median"]]
        labels = ["National", "Median prefecture"]
        x = list(range(len(comparison)))
        width = 0.34
        fig, ax = plt.subplots(figsize=(8.5, 5))
        ax.bar([value - width / 2 for value in x], comparison["top1_share_pct"], width, label="Top 1 speaker")
        ax.bar([value + width / 2 for value in x], comparison["top3_share_pct"], width, label="Top 3 speakers")
        ax.set_xticks(x, labels)
        ax.set_title("Concentration of Anti-Immigration Speech")
        ax.set_ylabel("Share of anti-immigration speeches (%)")
        ax.legend()
        fig.tight_layout()
        path = self.figures_dir / f"advanced_speaker_concentration.{self.format}"
        fig.savefig(path, dpi=self.dpi)
        plt.close(fig)
        return path

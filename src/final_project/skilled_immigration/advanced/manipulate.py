from pathlib import Path

import pandas as pd

from data import DataAcquisition
from settings import load_settings


class DataManipulation:
    def __init__(self, config_path: str | Path, project_root: Path | None = None):
        self.config, self.project_root = load_settings(config_path, project_root)
        self.acquisition = DataAcquisition(config_path, self.project_root)
        self.processed_dir = self.project_root / self.config["paths"]["processed_dir"]

    def run(self) -> dict[str, pd.DataFrame]:
        frames = self.acquisition.run()
        annual = self._clean_annual(frames["annual"])
        stance = self._clean_stance(frames["stance"])
        concentration = self._clean_concentration(frames["concentration"])
        correlation = self._clean_correlation(frames["correlation"])

        cleaned = {
            "annual": annual,
            "stance": stance,
            "concentration": concentration,
            "correlation": correlation,
        }
        self._save(cleaned)
        return cleaned

    def _clean_annual(self, frame: pd.DataFrame) -> pd.DataFrame:
        annual = frame.copy()
        annual["year"] = pd.to_numeric(annual["year"], errors="raise").astype(int)
        annual["n_speeches"] = pd.to_numeric(annual["n_speeches"], errors="raise").astype(int)
        annual = annual.drop_duplicates("year").sort_values("year").reset_index(drop=True)
        annual["year_centered"] = annual["year"] - annual["year"].min()
        window = int(self.config["visualization"]["rolling_window"])
        annual["rolling_mean"] = annual["n_speeches"].rolling(window, min_periods=1).mean()
        annual["year_over_year_change"] = annual["n_speeches"].pct_change() * 100
        return annual

    @staticmethod
    def _clean_stance(frame: pd.DataFrame) -> pd.DataFrame:
        stance = frame.copy()
        stance["n_speeches"] = pd.to_numeric(stance["n_speeches"], errors="raise").astype(int)
        stance["share_pct"] = 100 * stance["n_speeches"] / stance["n_speeches"].sum()
        order = ["pro", "neutral", "anti"]
        stance["stance"] = pd.Categorical(stance["stance"], categories=order, ordered=True)
        return stance.sort_values("stance").reset_index(drop=True)

    @staticmethod
    def _clean_concentration(frame: pd.DataFrame) -> pd.DataFrame:
        concentration = frame.copy()
        columns = ["n_speakers_or_prefectures", "top1_share_pct", "top3_share_pct", "gini"]
        concentration[columns] = concentration[columns].apply(pd.to_numeric, errors="raise")
        return concentration

    @staticmethod
    def _clean_correlation(frame: pd.DataFrame) -> pd.DataFrame:
        correlation = frame.copy()
        columns = ["n_prefectures", "pearson_r", "p_value"]
        correlation[columns] = correlation[columns].apply(pd.to_numeric, errors="raise")
        return correlation

    def _save(self, frames: dict[str, pd.DataFrame]) -> None:
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        for name, frame in frames.items():
            frame.to_csv(self.processed_dir / f"advanced_{name}.csv", index=False)

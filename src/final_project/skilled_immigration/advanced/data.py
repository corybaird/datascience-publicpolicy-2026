from pathlib import Path

import pandas as pd

from settings import load_settings


class DataAcquisition:
    def __init__(self, config_path: str | Path, project_root: Path | None = None):
        self.config, self.project_root = load_settings(config_path, project_root)
        self.raw_dir = self.project_root / self.config["paths"]["raw_dir"]

    def run(self) -> dict[str, pd.DataFrame]:
        files = self.config["files"]
        missing = [filename for filename in files.values() if not (self.raw_dir / filename).exists()]
        if missing:
            raise FileNotFoundError(f"Missing committed aggregate snapshots: {missing}")

        frames = {
            name: pd.read_csv(self.raw_dir / filename)
            for name, filename in files.items()
        }
        self._validate(frames)
        return frames

    @staticmethod
    def _validate(frames: dict[str, pd.DataFrame]) -> None:
        required = {"annual", "stance", "concentration", "correlation"}
        if set(frames) != required:
            raise ValueError(f"Expected datasets {required}, received {set(frames)}")
        if len(frames["annual"]) < 10:
            raise ValueError("Annual dataset must contain at least ten years.")
        if set(frames["stance"]["stance"]) != {"pro", "neutral", "anti"}:
            raise ValueError("Stance data must contain pro, neutral, and anti labels.")

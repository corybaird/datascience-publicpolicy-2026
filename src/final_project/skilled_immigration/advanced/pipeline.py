from pathlib import Path

from data import DataAcquisition
from graph import DataVisualization
from manipulate import DataManipulation
from model import EconometricModeling
from settings import find_project_root


class SkilledImmigrationPipeline:
    def __init__(self, config_path: str | Path, project_root: Path | None = None):
        self.project_root = project_root or find_project_root()
        self.config_path = config_path

    def run(self) -> dict[str, object]:
        raw = DataAcquisition(self.config_path, self.project_root).run()
        clean = DataManipulation(self.config_path, self.project_root).run()
        figures = DataVisualization(self.config_path, self.project_root).run()
        regression = EconometricModeling(self.config_path, self.project_root).run()
        return {"raw": raw, "clean": clean, "figures": figures, "regression": regression}


if __name__ == "__main__":
    root = find_project_root()
    config = root / "references/configs/final_project/skilled_immigration/project_settings.yaml"
    outputs = SkilledImmigrationPipeline(config, root).run()
    print("Advanced pipeline complete")
    print(f"Figures: {len(outputs['figures'])}")
    print(f"Regression observations: {int(outputs['regression'].nobs)}")

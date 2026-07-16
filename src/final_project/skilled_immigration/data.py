from pathlib import Path

import pandas as pd


PROJECT_NAME = "skilled_immigration"
REQUIRED_FILES = {
    "annual": "annual_speech_counts.csv",
    "stance": "stance_summary.csv",
    "concentration": "concentration_summary.csv",
    "correlation": "geographic_correlation.csv",
}


def find_project_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "pyproject.toml").exists() or (
            (candidate / "src").exists() and (candidate / "notebooks").exists()
        ):
            return candidate
    raise FileNotFoundError("Could not locate the repository root.")


def run(project_root: Path | None = None) -> dict[str, pd.DataFrame]:
    root = project_root or find_project_root()
    raw_dir = root / "data" / "final_project" / PROJECT_NAME / "raw"

    missing = [name for name in REQUIRED_FILES.values() if not (raw_dir / name).exists()]
    if missing:
        raise FileNotFoundError(f"Missing committed project snapshots: {missing}")

    frames = {
        key: pd.read_csv(raw_dir / filename)
        for key, filename in REQUIRED_FILES.items()
    }

    if len(frames["annual"]) < 10:
        raise ValueError("Annual speech dataset should contain at least ten years.")
    if set(frames["stance"]["stance"]) != {"pro", "neutral", "anti"}:
        raise ValueError("Stance summary must contain pro, neutral, and anti labels.")

    return frames


if __name__ == "__main__":
    loaded = run()
    for name, frame in loaded.items():
        print(f"{name}: {frame.shape}")

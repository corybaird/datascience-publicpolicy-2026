from pathlib import Path

import data
import graph
import manipulate
import model


def run(project_root: Path | None = None) -> dict[str, object]:
    root = project_root or data.find_project_root()
    raw = data.run(root)
    clean = manipulate.run(root)
    figures = graph.run(root)
    regression = model.run(root)
    return {
        "raw": raw,
        "clean": clean,
        "figures": figures,
        "regression": regression,
    }


if __name__ == "__main__":
    outputs = run()
    print("Pipeline complete")
    print(f"Figures: {len(outputs['figures'])}")
    print(f"Regression observations: {int(outputs['regression'].nobs)}")

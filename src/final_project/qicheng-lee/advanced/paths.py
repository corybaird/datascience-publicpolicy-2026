from pathlib import Path

# This file lives at src/final_project/qicheng-lee/advanced/paths.py, four levels
# below the repo root. Every other script in this package imports PROJECT_ROOT
# from here rather than recomputing parents[4] itself, so the depth assumption
# only needs to be correct (and updated) in one place.
PROJECT_ROOT = Path(__file__).resolve().parents[4]

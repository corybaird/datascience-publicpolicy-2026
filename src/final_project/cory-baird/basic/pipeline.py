import sys
from pathlib import Path

# Add the basic folder to sys.path to enable clean imports
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

import data
import manipulate
import graph
import model

def run():
    print("=== Starting Basic Pipeline ===")
    data.run()
    manipulate.run()
    graph.run()
    summary = model.run()
    print("=== Basic Pipeline execution complete ===")
    return summary

if __name__ == "__main__":
    run()

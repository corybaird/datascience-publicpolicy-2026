"""
Pipeline orchestration for basic final project
"""
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
    print("=== Starting Basic Pipeline for Mariam Togonidze ===")
    print("\n1. Loading data...")
    data.run()
    print("\n2. Manipulating data...")
    manipulate.run()
    print("\n3. Generating graphs...")
    graph.run()
    print("\n4. Running model...")
    model.run()
    print("\n=== Basic Pipeline execution complete ===")

if __name__ == "__main__":
    run()

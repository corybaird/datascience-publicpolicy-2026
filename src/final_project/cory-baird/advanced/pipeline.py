import sys
from pathlib import Path

class PipelineDebtAnalysis:
    def __init__(self, config_path="references/configs/final_project/cory-baird/project_settings.yaml"):
        self.config_path = config_path
        
        # Add the student folder to sys.path to enable clean imports
        current_dir = Path(__file__).resolve().parent
        if str(current_dir) not in sys.path:
            sys.path.insert(0, str(current_dir))

    def run_acquisition(self):
        import data
        print("Stage 1: Downloading & Acquiring Data...")
        fetcher = data.DataAcquisition(config_path=self.config_path)
        return fetcher.run()

    def run_manipulation(self):
        import manipulate
        print("Stage 2: Cleaning & Preprocessing Data...")
        manipulator = manipulate.DataManipulation(config_path=self.config_path)
        return manipulator.run()

    def run_visualization(self):
        import graph
        print("Stage 3: Generating Visualizations...")
        visualizer = graph.DataVisualization(config_path=self.config_path)
        return visualizer.run()

    def run_modeling(self):
        import model
        print("Stage 4: Fitting Econometric Models...")
        modeler = model.EconometricModeling(config_path=self.config_path)
        return modeler.run()

    def run(self):
        print("=== Starting PipelineDebtAnalysis ===")
        self.run_acquisition()
        self.run_manipulation()
        self.run_visualization()
        summary = self.run_modeling()
        print("=== PipelineDebtAnalysis execution complete ===")
        return summary

if __name__ == "__main__":
    pipeline = PipelineDebtAnalysis()
    pipeline.run()

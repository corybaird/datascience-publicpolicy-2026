import os
import numpy as np
import pandas as pd

from matrix_reg import MatrixRegression
from viz import RegressionVisualizer

# Pipeline that ties data loading, matrix preparation, model fitting,
# and visualization together.  The run() method is the sole entry point.

class RegressionPipeline:
    def __init__(self):
        self.model = MatrixRegression()
        self.viz = RegressionVisualizer()
        self.data = None
        self.X = None
        self.y = None

        # Resolve project root once so paths work from any working directory
        lib_dir = os.path.dirname(os.path.abspath(__file__))
        self._project_root = os.path.dirname(os.path.dirname(os.path.dirname(lib_dir)))

    def load_data(self):
        # Load the world happiness parquet dataset
        data_path = os.path.join(self._project_root, "data", "examples", "week_5", "world_happiness.parquet")
        self.data = pd.read_parquet(data_path)
        return self.data

    def prepare_matrices(self):
        # Extract predictor and target, dropping rows with missing values
        clean = self.data[['explained_by:_log_gdp_per_capita', 'ladder_score']].dropna()
        self.X = clean['explained_by:_log_gdp_per_capita'].values
        self.y = clean['ladder_score'].values

    def run(self):
        # Run the full pipeline: load -> prepare -> fit -> output -> plot
        self.load_data()
        self.prepare_matrices()
        self.model.fit(self.X, self.y)

        # Build the full beta vector [intercept, slope] for prediction / plotting
        beta = np.array([self.model.intercept] + list(self.model.coefficients))

        print("=== OLS Regression Results ===")
        print(f"Intercept (B0): {self.model.intercept:.4f}")
        print(f"Slope     (B1): {self.model.coefficients[0]:.4f}")

        # Generate predicted values to compute R-squared manually
        n_obs = self.X.shape[0]
        X_design = np.hstack((np.ones((n_obs, 1)), self.X.reshape(-1, 1)))
        y_pred = X_design @ beta
        ss_res = np.sum((self.y - y_pred.flatten()) ** 2)
        ss_tot = np.sum((self.y - np.mean(self.y)) ** 2)
        r_squared = 1 - ss_res / ss_tot
        print(f"R-squared:      {r_squared:.4f}")

        # Save the regression plot under reports/viz/
        viz_dir = os.path.join(self._project_root, "reports", "viz")
        os.makedirs(viz_dir, exist_ok=True)
        save_path = os.path.join(viz_dir, "regression_pipeline.png")
        self.viz.plot_regression(
            self.X, self.y, beta,
            title='World Happiness: Log GDP per capita vs Ladder Score',
            save_path=save_path
        )
        print("\nPlot saved to reports/viz/regression_pipeline.png")

        return beta

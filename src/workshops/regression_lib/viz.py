import matplotlib.pyplot as plt
import numpy as np

# Visualization helper for scattering data points and drawing the fitted regression line

class RegressionVisualizer:
    def plot_regression(self, X, y, beta, title, save_path):
        # Scatter the original data
        plt.figure(figsize=(8, 5))
        plt.scatter(X, y, alpha=0.5, edgecolor='black', label='Observed data')

        # Build sorted X for a smooth regression line
        X_sorted = np.sort(X)
        X_design = np.hstack((np.ones((len(X_sorted), 1)), X_sorted.reshape(-1, 1)))
        y_pred = X_design @ beta

        # Plot the fitted line
        plt.plot(X_sorted, y_pred, color='red', linewidth=2, label='Fitted line')

        plt.xlabel('X')
        plt.ylabel('y')
        plt.title(title)
        plt.legend()
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()

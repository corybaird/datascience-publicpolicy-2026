import numpy as np

from base import BaseRegression

# OLS regression solved via the matrix normal equation:
# beta = (X^T X)^{-1} X^T Y

class MatrixRegression(BaseRegression):
    def fit(self, X, y):
        # Build design matrix with intercept column (ones)
        n_obs = X.shape[0]
        X_matrix = np.hstack((np.ones((n_obs, 1)), X.reshape(-1, 1)))
        Y_vector = y.reshape(-1, 1)

        # Solve for coefficients: beta = (X^T X)^{-1} X^T Y
        beta_matrix = np.linalg.inv(X_matrix.T @ X_matrix) @ (X_matrix.T @ Y_vector)

        # Extract intercept (first element) and slope coefficients (remaining)
        self.intercept = beta_matrix[0, 0]
        self.coefficients = beta_matrix[1:, 0]

# Advanced Assignment: Custom NumPy OLS Regression Library

## Objective
Build a custom OLS regression library using matrix algebra in NumPy. You will practice object-oriented inheritance, code modularization, and visualization by splitting your code across multiple Python files under `src/workshops/regression_lib/`.

## Mathematical Background
OLS coefficients are solved via the matrix equation:
$$\beta = (X^T X)^{-1} X^T Y$$
Where $X$ is the design matrix (including a column of ones for the intercept) and $Y$ is the target vector.

## Coding Standards
- **Exclude Docstrings:** Use standard `#` comments for all code explanations.
- **Exclude Type Hints:** Do not use type annotations or type checks.
- **Formatting:** Keep all function and method signatures on a single line.
- **Sole Entry Point:** Ensure that your pipeline exposes a `run()` method as the sole entry point to run the regression pipeline.

## Library Structure
Create the following files inside `src/workshops/regression_lib/`:

### 1. `base.py`
Define an abstract base class `BaseRegression` containing:
- `__init__`: Set instance variables for `coefficients` and `intercept` to `None`.
- `fit(self, X, y)`: Define an empty placeholder method.

### 2. `matrix_reg.py`
Define the class `MatrixRegression` inheriting from `BaseRegression` and implement the `fit(self, X, y)` method using matrix algebra:
```python
# Convert variables to numpy matrices
n_obs = len(df_merged)
X_matrix = np.hstack((np.ones((n_obs, 1)), df_merged['gdp_per_capita'].values.reshape(-1, 1)))
Y_vector = df_merged['ladder_score'].values.reshape(-1, 1)

# Solve coefficients using matrix multiplication
beta_matrix = np.linalg.inv(X_matrix.T @ X_matrix) @ (X_matrix.T @ Y_vector)
```
Store the intercept ($\beta_0$) and slope ($\beta_1$) in the class instance variables.

### 3. `viz.py`
Define `RegressionVisualizer` containing a `plot_regression(self, X, y, beta, title, save_path)` method. This method should plot the data points as a scatter plot, draw the predicted regression line, and save the figure.

### 4. `pipeline.py`
Define a `RegressionPipeline` class that imports `MatrixRegression` and `RegressionVisualizer` to run the entire flow:
- `load_data(self)`: Load the parquet or CSV dataset.
- `prepare_matrices(self)`: Extract the design matrix $X$ and target vector $y$.
- `run(self)`: Run the pipeline and output the calculated intercept and slope coefficients.

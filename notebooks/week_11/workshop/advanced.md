# Advanced Assignment: Object-Oriented Regression Interpreter

## Objective
Convert a procedural regression interpretation flow into a reusable, object-oriented Class in a Python file. You will organize this class according to proper project structures and run a sample pipeline.

## Guidelines & Setup
- **File Location:** Create your class in `src/workshops/regression_interpreter.py` (relative to the project root).
- **Sole Entry Point:** Expose a `run()` method as the sole orchestrator to run the regression pipeline.
- **Coding Standards:**
  - Never use docstrings (use standard `#` comments for explanation).
  - Never use type checking or type annotations.
  - Keep all function and method arguments on a single line.

## Class Specification
Your `RegressionInterpreter` class should support the following structure and methods:

### 1. Initialization
Store variables such as data path, target column, feature column, and functional forms.

### 2. Data Loading
Define a method `load_data` to load the dataset from the CSV file.

### 3. Regression Fitting
Define a method `fit_ols` to add a constant to the independent variable and fit the model using `statsmodels.api.OLS`.

### 4. Interpretation
Define a method `interpret` that accepts the fitted model and prints interpretations based on the combination of functional forms (Level-Level, Log-Log, Level-Log, Log-Level, and Percent-Change cases).

### 5. Execution Orchestration
Define a public method `run` to execute the data load, regression fit, and interpretation print.

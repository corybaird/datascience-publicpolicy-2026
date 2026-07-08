# Abstract base class for regression models
# This provides the interface that all regression implementations must follow

class BaseRegression:
    def __init__(self):
        # Store model parameters, initialized to None before fitting
        self.coefficients = None
        self.intercept = None

    def fit(self, X, y):
        # Placeholder: subclasses must override this method
        pass


def interpret_regression(model, x_col, y_type, x_type, y_name, x_name):
    """Interprets a fitted statsmodels OLS result."""
    coefficient_val = model.params.loc[x_col]
    r_squared_val   = model.rsquared
    p_value_val     = model.pvalues.loc[x_col]
    
    print(f"\n=== Regression Interpretation: {y_name} vs. {x_name} ===")
    print(f"Specification: {y_type.upper()} to {x_type.upper()}")
    print(f"Coefficient: {coefficient_val:.6f}")
    
    if y_type == 'log' and x_type == 'log':
        print(f"Interpretation: A 1% increase in {x_name} is associated with a {coefficient_val:.4f}% change in {y_name}.")
    elif y_type == 'level' and x_type == 'log':
        change_y = coefficient_val / 100
        print(f"Interpretation: A 1% increase in {x_name} is associated with a {change_y:.4f} unit change in {y_name}.")
    elif y_type == 'log' and x_type == 'level':
        percentage_y = coefficient_val * 100
        print(f"Interpretation: A 1 unit increase in {x_name} is associated with a {percentage_y:.4f}% change in {y_name}.")
    elif y_type == 'level' and x_type == 'level':
        print(f"Interpretation: A 1 unit increase in {x_name} is associated with a {coefficient_val:.6f} unit change in {y_name}.")
    
    print(f"R squared (Fit quality): {r_squared_val:.4f}")
    print(f"p value (Statistical significance): {p_value_val:.4f}")
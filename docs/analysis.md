# Analytical Methodology & Model Design Guide

This guide details the statistical approaches, modeling designs, and validation metrics used in this project. Both human researchers and agentic tools must follow these methodologies.

---

## 1. Regression & Modeling Specifications

When constructing statistical models or regressions:
- **Model Formulations**: Define equations explicitly before writing code.
- **Controls & Variables**: Document independent, dependent, and control variables to prevent omitted variable bias.
- **Standard Errors**: Specify cluster or robust standard error estimators when dealing with panel or grouped data.

---

## 2. Validation & Performance Metrics

To ensure reproducibility and analytical rigour:
- **Baseline Models**: Always compare custom models against simple baseline benchmarks (e.g., mean forecasts, simple linear models).
- **Out-of-sample Testing**: Where possible, use cross-validation or rolling-window backtests.
- **Metrics**: Standardize metrics (e.g., RMSE, MAE, R-squared, p-values) to keep reports comparable.

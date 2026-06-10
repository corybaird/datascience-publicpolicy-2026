# Codebase Architecture & Data Design Guide

This guide details the modular system design, code conventions, parameter configurations, and data architecture of the **datascience-publicpolicy-2026** project.

---

## 1. Modular Code Architecture (`src/`)

To prevent messy notebooks, code logic must be moved to modular packages within the `src/` directory.

### Actual Source Directory Layout

- **`src/data/`**: Data loading, scraping, and ETL utilities.
  - `data_import.py`: Module for importing raw data.
  - `data_manipulate.py`: Module for data cleaning and transformations.
  - `data_merge.py`: Module for merging datasets.
- **`src/model/`**: Statistical modeling and regression code.
  - `regression.py`: Regression specifications and validation code.
- **`src/grading/`**: Homework grader scripts.
  - `hw_grader.py`: General homework assessment module.
  - `grader_hw_2.py`: Specific grader for Homework 2.
- **`src/temp/`**: Directory for scratchpads or temporary experimental scripts.

### Core Architecture Rules
- **No type checking**: Do not use `isinstance`, `typing`, or runtime validation in code modules.
- **Single Line Arguments**: Function and method signatures must define all arguments on a single line.
- **No docstrings**: Do not write docstrings (`""" """`). Rely on comments and clean naming instead.
- **Class Entry Point**: Executable pipeline classes must expose a `run()` method. Do not define a `main()` function.

---

## 2. Data Directory & Cookie Cutter Structure

We enforce a separation of data stages to ensure reproducibility and prevent data corruption.

### Actual Data Directory Layout
- **`data/raw/`**: Immutable original dataset dumps. Never edit manually.
  - `imf_reports/`: Contains raw International Monetary Fund reporting data.
- **`data/examples/`**: Reference datasets used during classes and tutorials.
- **`data/hw/`**: Source data for individual homework assignments.
- **`data/temp/`**: Gitignored scratch space for debugging and testing.

### Standardized Cookie Cutter targets (for pipelines)
- **`data/processed/`**: Cleaned, structured datasets ready for modeling.
- **`data/pipeline/`**: Intermediate DVC stage outputs (e.g., parquet or json files).

### Ingestion & Storage Standards
- **File Formats**: Cleaned datasets should be saved in **Parquet** format for column storage efficiency, or **CSV** when human-readability is required.
- **Dynamic Paths**: Paths must be constructed using `pathlib.Path` relative to the project root. Absolute paths are strictly forbidden.

---

## 3. Configuration & Parameter Management

### YAML Configurations
- All runtime configurations must reside in `references/configs/` as YAML files.
- Configurations must be loaded dynamically using `yaml.safe_load()`.

### Dictionary Management
- **Never hard-code dictionaries with more than 3 keys** inside code.
- Dictionaries exceeding 3 keys must be moved to `references/dictionaries/DICTIONARY_NAME.py` containing only constants and simple assignments.
- Example: `references/dictionaries/iso2_to_countryname.py` containing the `ISO2_TO_COUNTRYNAME` constant.

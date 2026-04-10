# Week 2 Notebooks Overview

This directory contains three core Jupyter notebooks designed to transition students smoothly from basic file handling to automated data retrieval, while demystifying the underlying Python syntax. The flow employs a "data-first" approach, getting students to their "aha!" moment quickly before breaking down the exact mechanics.

*   `1-notebook-code-basics.ipynb` **(Working with Files and Pandas)**
    *   **Focus:** Getting oriented and loading local data.
    *   **Key Concepts:** File paths, assigning variables, bringing in the `pandas` library, and loading local CSV sequences.
    *   **Goal:** Students learn how to locate themselves using the command line (`os.getcwd()`) and successfully import their first dataframe to get immediate visual feedback using `df.head()`, `df.tail()`, and `df.info()`.

*   `2-reading-data.ipynb` **(Data from the Web and APIs)**
    *   **Focus:** Scaling up and pulling data dynamically.
    *   **Key Concepts:** Reading CSVs from GitHub URLs, interacting with APIs (World Bank), and a "just-in-time" introduction to custom functions (`def`) and lists.
    *   **Goal:** Demystifying where data comes from on the web. Students bypass manual downloads by fetching information programmatically, leveraging a custom-built function to pass list objects to the World Bank API.

*   `3-python-fundamentals.ipynb` **(Looking Under the Hood: The Grammar of Python)**
    *   **Focus:** Deconstructing the code used in previous notebooks.
    *   **Key Concepts:** Deep dive into data types (strings, integers, floats) and structure mapping (dictionaries).
    *   **Goal:** Returning to the fundamentals of syntax now that students have achieved results. This notebook connects the dots, thoroughly explaining *why* the objects they used in Notebooks 1 and 2 behaved the way they did.

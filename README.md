# qPCR Analyzer

## Overview

This project implements a Python tool for analyzing RT-qPCR experiment results exported as CSV files. Many qPCR instruments output data with one row per well, including sample name, target (gene), and Cq (Ct) value. In typical experiments, each biological sample is measured in technical duplicates (for example, `KC_sample1_1` and `KC_sample1_2`).

The goal of this project is to automate common analysis steps:

* Load qPCR data from a CSV file
* Filter results for a specific target gene
* Detect and combine technical duplicates
* Compute summary statistics per sample:

  * Mean Cq
  * Standard deviation
  * Number of replicates
* Display results in a table
* Visualize mean Cq values using a bar plot with error bars

This project demonstrates modular Python design, data analysis, visualization, and automated testing.

---

## Project Structure

```
MyProjectFolder/
│
├── ProjectNotebook.ipynb        # Project description and demonstration
├── requirements.txt             # List of external dependencies
│
├── my_module/
│   ├── __init__.py
│   └── functions.py             # Core analysis functions
│
├── scripts/
│   └── qpcr_cli.py              # Command-line interface
│
└── tests/
    └── test_functions.py        # Pytest unit tests
```

---

## Core Functionality

The main analysis workflow:

1. Load CSV file
2. Filter rows by target gene
3. Remove replicate suffix (`_1`, `_2`, etc.) from sample names
4. Group by base sample
5. Compute:

   * mean Cq
   * standard deviation
   * replicate count
6. Optionally generate a bar plot with error bars

---

## How to Run the Project

### 1. In the Jupyter Notebook (recommended)

Open:

```
ProjectNotebook.ipynb
```

Example usage:

```python
from my_module.functions import summarize_target_from_file

summary = summarize_target_from_file("20251103_1.csv", "Actb")
summary
```

To plot:

```python
from scripts.qpcr_cli import plot_cq_summary
plot_cq_summary(summary, "Actb")
```

---

### 2. Run the Command-Line Interface

From the project folder:

```bash
python scripts/qpcr_cli.py
```

The program will prompt for:

* CSV filename
* Target gene

It will then display results and optionally save a CSV or show a plot.

---

## Running Tests (Required)

This project includes unit tests using **pytest**.

From the project directory:

```bash
pytest
```

or inside a notebook:

```python
!pytest -q
```

The tests verify:

* Sample name cleaning
* Duplicate handling
* Mean and replicate calculations
* Target filtering

---

## Dependencies

All required packages are included in the standard Anaconda distribution used on DataHub.

`requirements.txt`:

```
pandas
matplotlib
pytest
```

---

## Design Approach

This project follows a modular design:

* Core logic is implemented in reusable functions (`my_module/functions.py`)
* User interaction is separated into a script (`qpcr_cli.py`)
* Analysis and demonstration are presented in a Jupyter notebook
* Unit tests ensure correctness of key functions

The implementation uses:

* DataFrames for structured data handling
* String processing to detect duplicate samples
* Grouping and aggregation for statistical summaries
* Matplotlib for visualization
* Pytest for automated testing

---

## Project Motivation

RT-qPCR experiments commonly include technical duplicates and multiple targets. Manual averaging and organization of Cq values can be time-consuming and error-prone. This tool provides a simple automated workflow for summarizing and visualizing qPCR results.

---

## Author

Rina Matsuo

 

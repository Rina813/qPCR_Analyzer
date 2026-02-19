"""
qPCR Analyzer core functions.

This module provides functions to:
- load qPCR CSV files
- filter by Target (gene)
- merge technical duplicates (e.g., KC_sample1_1 and KC_sample1_2)
- compute mean Cq, standard deviation, and replicate count per sample

Assumptions:
- The CSV has columns: 'Target', 'Sample', 'Cq' (case-sensitive).
- Technical duplicates are indicated by a trailing suffix like '_1', '_2', etc.
"""

from __future__ import annotations

import re
from typing import Optional

import pandas as pd


def load_qpcr_csv(filename: str) -> pd.DataFrame:
    """
    Load a qPCR CSV file into a pandas DataFrame.

    Parameters
    ----------
    filename : str
        Path to the CSV file.

    Returns
    -------
    pandas.DataFrame
        Loaded DataFrame.
    """
    return pd.read_csv(filename)


def filter_by_target(df: pd.DataFrame, target_name: str) -> pd.DataFrame:
    """
    Filter rows to keep only a single target (gene).

    Parameters
    ----------
    df : pandas.DataFrame
        qPCR data including a 'Target' column.
    target_name : str
        Target gene name to keep.

    Returns
    -------
    pandas.DataFrame
        Subset of df where Target == target_name.
    """
    return df[df["Target"] == target_name].copy()


def clean_sample_name(sample_name: str) -> str:
    """
    Remove replicate suffix from sample name.

    Examples
    --------
    'KC_sample1_1' -> 'KC_sample1'
    'KC_sample1_2' -> 'KC_sample1'
    'Control'      -> 'Control'

    Parameters
    ----------
    sample_name : str

    Returns
    -------
    str
        Base sample name.
    """
    return re.sub(r"_\d+$", "", sample_name)


def add_base_sample_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a 'base_sample' column by stripping replicate suffixes from 'Sample'.

    Parameters
    ----------
    df : pandas.DataFrame
        Must contain a 'Sample' column.

    Returns
    -------
    pandas.DataFrame
        Copy of df with added 'base_sample' column.
    """
    df_out = df.copy()
    df_out["base_sample"] = df_out["Sample"].apply(clean_sample_name)
    return df_out


def summarize_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize technical duplicates by base sample using Cq values.

    Parameters
    ----------
    df : pandas.DataFrame
        Must contain 'base_sample' and 'Cq'.

    Returns
    -------
    pandas.DataFrame
        Columns:
        - base_sample
        - mean_cq
        - std_cq
        - n_reps
    """
    if "base_sample" not in df.columns:
        raise KeyError("Missing required column: 'base_sample'")
    if "Cq" not in df.columns:
        raise KeyError("Missing required column: 'Cq'")

    summary = (
        df.groupby("base_sample")["Cq"]
        .agg(mean_cq="mean", std_cq="std", n_reps="count")
        .reset_index()
    )
    return summary


def summarize_target_from_file(filename: str, target_name: str) -> pd.DataFrame:
    """
    Load a qPCR CSV and return duplicate-summarized Cq stats for a given Target.

    Parameters
    ----------
    filename : str
        CSV filepath.
    target_name : str
        Target to analyze (exact match in 'Target' column).

    Returns
    -------
    pandas.DataFrame
        Summary table for that target, or empty DataFrame if none found.
    """
    df = load_qpcr_csv(filename)

    # Validate required columns early for clearer errors
    for col in ("Target", "Sample", "Cq"):
        if col not in df.columns:
            raise KeyError(f"Missing required column: '{col}'")

    df_target = filter_by_target(df, target_name)
    if df_target.empty:
        return pd.DataFrame()

    df_target = add_base_sample_column(df_target)
    return summarize_duplicates(df_target)

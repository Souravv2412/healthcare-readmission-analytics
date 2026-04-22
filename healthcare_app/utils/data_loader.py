# utils/data_loader.py
"""
Data loading utilities. Looks for the cleaned dataset in several locations
to be compatible with the user's existing project structure.
"""

import os
from pathlib import Path


CANDIDATE_PATHS = [
    "data/processed/cleaned_data.csv",
    "../Dataset/cleaned/cleaned_data.csv",
    "../data/processed/cleaned_data.csv",
    "Dataset/cleaned/cleaned_data.csv",
]


def find_cleaned_data():
    """Return the path to cleaned_data.csv or None if not found."""
    base = Path(__file__).parent.parent
    for rel in CANDIDATE_PATHS:
        p = base / rel
        if p.exists():
            return str(p)
    return None


def dataset_available():
    return find_cleaned_data() is not None
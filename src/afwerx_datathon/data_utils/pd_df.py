"""Utility methods for manipulating pandas DataFrames."""

# builtins
from typing import Dict

# 3d party/FOSS
import numpy as np
import pandas as pd

DEFAULT_INDEX = pd.Index(["pilot", "session", "run"])


def query(data: pd.DataFrame, query: Dict) -> pd.DataFrame:
    """Get unique rows from a df with a query."""
    valid_rows = np.ones(len(data), dtype=bool)
    for col, value in query.items():
        valid_rows &= data[col] == value
    return data[valid_rows]


def sort(data: pd.DataFrame, idx: pd.Index = DEFAULT_INDEX) -> pd.DataFrame:
    """Sort by index.

    Defaults to a "run_sort" [pilot, session, run]
    """
    return data.sort_values(idx)


def remove_nonfeatures(
    features_data: pd.DataFrame,
    nonfeatures: pd.Index = DEFAULT_INDEX,
) -> pd.DataFrame:
    """Remove nonfeatures data from features dataframe.

    Default nonfeatures: [pilot, session, run].
    """

    for nonfeature in nonfeatures:
        del features_data[nonfeature]

    return features_data

"""Wavelet preprocessing methods."""

# builtins
from copy import deepcopy
import pathlib
from typing import Dict

# 3d party/FOSS
import numpy as np
import numpy.typing as npt
import pandas as pd
import pywt
import scipy.stats as sp_stats
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# this
from afwerx_datathon.io.datasets import load_labels, remove_undesirables
from afwerx_datathon.io.parquet import ParquetReader
from afwerx_datathon.io.path import DEV_DATA
from afwerx_datathon.io.types import DataType, ExperimentType


def calc_stats(data: npt.ArrayLike) -> Dict:
    """Calculate a standard set of stats on an input array."""
    results = {
        "mean": np.mean(data),
        "std": np.std(data),
        "skew": sp_stats.skew(data),
        "kurt": sp_stats.kurtosis(data),
    }
    return results


def query_df(data: pd.DataFrame, query: Dict) -> pd.DataFrame:
    """Get unique rows from a df with a query."""
    valid_rows = np.ones(len(data), dtype=bool)
    for col, value in query.items():
        valid_rows &= data[col] == value
    return data[valid_rows]


def calc_features(data: Dict, **kwargs) -> pd.DataFrame:
    """Calculate features for the data."""
    skip_types = [DataType.labels]
    skip_cols = ["pilot", "session", "run", "time_s"]
    df = data[DataType.perf]
    runs = df[["pilot", "session", "run"]].drop_duplicates().to_dict("records")

    results = []
    for run in runs:
        features = deepcopy(run)
        for thaipe, df in data.items():
            if thaipe in skip_types:
                continue
            run_df = query_df(df, run)
            for col in run_df.columns:
                if col in skip_cols:
                    continue
                coeffs = pywt.wavedec(
                    run_df[col], wavelet="bior2.8", level=4, **kwargs
                )
                for ix, coeff in enumerate(coeffs):
                    stats = calc_stats(coeff)
                    for key, stat in stats.items():
                        name = f"{thaipe.value}_{col}_wl-coef-{ix}_{key}"
                        features[name] = stat
        results.append(features)
    return pd.DataFrame(results)


def run_sort(data: pd.DataFrame) -> pd.DataFrame:
    """Sort by run-index."""
    return data.sort_values(["pilot", "session", "run"])


def add_labels(
    feature_data: pd.DataFrame,
    label_data: pd.DataFrame,
    label_key: str,
) -> pd.DataFrame:
    """Add label data to the features data."""
    label_data_sorted = run_sort(label_data)
    feature_data_sorted = run_sort(feature_data)
    feature_data_sorted["labels"] = label_data_sorted[label_key]
    return feature_data


def remove_nonfeatures(features_data: pd.DataFrame) -> pd.DataFrame:
    """Remove nonfeatures data from features dataframe."""

    del features_data["pilot"]
    del features_data["session"]
    del features_data["run"]
    return features_data


def save_features(
    features_data: pd.DataFrame,
    path: pathlib.Path = DEV_DATA,
    expr_type: ExperimentType = ExperimentType.ils,
) -> None:
    """Write features data to disk."""

    fname = path / f"task-{expr_type.value}" / "wavelet_features.parquet"
    features_data.to_parquet(fname)


def load_features(
    path: pathlib.Path = DEV_DATA,
    expr_type: ExperimentType = ExperimentType.ils,
) -> pd.DataFrame:
    """Load features data from disk."""
    fname = path / f"task-{expr_type.value}" / "wavelet_features.parquet"
    reader = ParquetReader(fname)
    return reader.read_all()


def load_clean_labels(
    path: pathlib.Path = DEV_DATA,
    expr_type: ExperimentType = ExperimentType.ils,
) -> pd.DataFrame:
    """Load labels data from disk."""

    return remove_undesirables(load_labels(path, expr_type))["labels"]


def rf_workflow(features: pd.DataFrame, labels: pd.DataFrame) -> None:
    """Example workflow for RF analysis."""

    sorted_features = run_sort(features)
    sorted_labels = run_sort(labels)
    run_ix = pd.Index(["pilot", "session", "run"])
    aligned = (
        sorted_features[run_ix].values == sorted_labels[run_ix].values
    ).all()
    if not aligned:
        raise ValueError("Labels and features rows are not aligned!")
    labs = sorted_labels["Difficulty"]
    labs = labs.astype({"Difficulty": "category"})
    feats = remove_nonfeatures(sorted_features)
    feats_train, feats_test, labs_train, labs_test = train_test_split(
        feats, labs, test_size=0.25
    )
    rf = RandomForestClassifier(n_estimators=500)
    rf.fit(feats_train, labs_train)
    labs_pred = rf.predict(feats_test)
    score = accuracy_score(labs_test, labs_pred)
    print(f"Accuracy: {score}")

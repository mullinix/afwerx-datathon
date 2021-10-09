"""Wavelet preprocessing methods."""

# builtins
from copy import deepcopy
from typing import Any, Dict

# 3d party/FOSS
import pandas as pd
import pywt

# this
from afwerx_datathon.data_utils import pd_df
from afwerx_datathon.io.types import DataType
from afwerx_datathon.signal.metrics import calc_stats


def calc_features(data: Dict, **kwargs: Any) -> pd.DataFrame:
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
            run_df = pd_df.query(df, run)
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

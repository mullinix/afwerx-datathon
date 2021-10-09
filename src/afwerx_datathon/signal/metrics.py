"""Methods for signal metrics calculation."""

# builtins
from typing import Dict

# 3d party/FOSS
import numpy as np
import numpy.typing as npt
import scipy.stats as sp_stats


def calc_stats(data: npt.ArrayLike) -> Dict:
    """Calculate a standard set of stats on an input array."""
    q = np.array([5, 25, 50, 75, 95])
    # ignore the fact that numpy hasn't properly typed this method
    qtiles = np.quantile(data, q / 100.0)  # type: ignore
    qs = {f"q{qq:d}": qtiles[ix] for ix, qq in enumerate(q)}
    qs["median"] = qs.pop("q50")
    results = {
        "mean": np.mean(data),
        "std": np.std(data),
        "skew": sp_stats.skew(data),
        "kurt": sp_stats.kurtosis(data),
    }
    results.update(qs)
    return results

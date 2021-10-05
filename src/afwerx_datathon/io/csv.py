"""CSV File IO methods."""

# builtins
import pathlib
from typing import Any

# 3d party/FOSS
import pandas as pd

# this
from afwerx_datathon.io.types import PathLike, DataType
from afwerx_datathon.io.factory import ReaderFactory


class CSVReader(ReaderFactory):
    """CSV reader concretion."""

    def __init__(
        self, run_path: PathLike, data_type: DataType, **kwargs: Any
    ) -> None:
        """Initialize reader."""

        self.path = pathlib.Path(run_path)
        self.data_type = data_type
        self.kwargs = kwargs

    def read(self, key: Any) -> Any:
        """Downselect data based on a key.
        
        Note: This isn't a "lazy-reader" -- this reads all _then_ down selects.
        """

        return self.read_all()[key]

    def read_all(self) -> pd.DataFrame:
        """Read all data from file."""

        data = []
        for f in self.path.glob(f"*{self.data_type.value}*.csv"):
            data.append(pd.read_csv(f, **self.kwargs))

        return pd.concat(data, ignore_index=True)
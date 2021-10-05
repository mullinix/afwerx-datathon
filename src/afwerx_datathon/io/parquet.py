"""CSV File IO methods."""

# builtins
from typing import Any

# 3d party/FOSS
import pandas as pd

# this
from afwerx_datathon.io.factory import ReaderFactory


class ParquetReader(ReaderFactory):
    """Parquet reader concretion."""

    def read(self, key: Any) -> Any:
        """Downselect data based on a key.
        
        Note: This isn't a "lazy-reader" -- this reads all _then_ down selects.
        """

        return self.read_all()[key]

    def read_all(self) -> pd.DataFrame:
        """Read all data from file."""

        data = pd.read_parquet(self.path)
        data = data.astype({
            "run": "category",
            "session": "category",
            "pilot": "category",
        })
        return data
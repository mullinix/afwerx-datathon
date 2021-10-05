"""Types for data IO."""

# builtins
from enum import Enum
import pathlib
from typing import Any, List, Union

class REnum(Enum):
    """Build on the Enum class."""

    @classmethod
    def __getitem__(cls, key: str) -> Any:
        """Lookup/generator for class."""

        return cls._member_map_[key]

    @classmethod
    def keys(cls) -> List[str]:
        """Get member names as a list."""

        return cls._member_names_


class ExperimentType(REnum):
    """Enumeration for experiments."""
    ils = "ils"
    rest = "rest"


class DataType(REnum):
    """Enumeration for data."""
    emg = "lslshimmeremg"
    eda = "lslshimmereda"
    ecg = "lslshimmerrespecg"
    acc = "lslshimmertorsoacc"
    htc = "lslhtcviveeye"
    xp11 = "lslxp11xpcplt"
    ocu = "ocuevts"
    perf = "perfmetric"


PathLike = Union[str, pathlib.Path]

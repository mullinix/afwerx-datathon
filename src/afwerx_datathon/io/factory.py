"""Factory methods for IO."""

# builtins
import abc
import pathlib
from typing import Any

# this
from src.afwerx_datathon.io.types import PathLike


class ReaderFactory(abc.ABC):
    """Factory method for reading data."""

    def __init__(self, path: PathLike) -> None:
        """Initialize reader."""

        self.path = pathlib.Path(path)

    def __getitem__(self, key: Any) -> Any:
        """Syntactic sugar on the read method."""

        return self.read(key)

    @abc.abstractmethod
    def read(self, key: Any) -> Any:
        """Implement a lazy reader if possible."""

        raise NotImplementedError

    @abc.abstractmethod
    def read_all(self) -> Any:
        """Implement a method to read all data."""

        raise NotImplementedError


class WriterFactory(abc.ABC):
    """Factory method for writing data."""

    def __init__(self, path: PathLike) -> None:
        """Initialize writer."""

        self.path = pathlib.Path(path)

    @abc.abstractmethod
    def update(self, key: Any, data: Any) -> Any:
        """Implement a method to update data based on a key."""

        raise NotImplementedError

    @abc.abstractmethod
    def dump(self, data: Any) -> Any:
        """Implement a method to write all data to disk."""

        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, key: Any) -> Any:
        """Implement a method to delete data located at key in the file."""

        raise NotImplementedError

"""Methods for traversing data paths."""

# builtins
import abc
import pathlib
from typing import List

# this
from afwerx_datathon.io.types import ExperimentType, PathLike

DATA_DIR = pathlib.Path("/data")
DEV_DATA = DATA_DIR / "developmentSet"
EVAL_DATA = DATA_DIR / "evaluationSet"


def get_pilots(
    source: PathLike, expr_type: ExperimentType
) -> List[pathlib.Path]:
    """Get paths to pilot data."""
    path = pathlib.Path(source) / f"task-{expr_type.value}"
    return list(path.glob("sub-cp*"))


def get_sessions(pilot_path: PathLike) -> List[pathlib.Path]:
    """Get listing of folder sessions for a pilot."""
    path = pathlib.Path(pilot_path)
    return list(path.glob("ses-*"))


def get_runs(session_path: PathLike) -> List[pathlib.Path]:
    """Get listing of runs during a session."""
    path = pathlib.Path(session_path)
    return list(path.glob("run-*"))


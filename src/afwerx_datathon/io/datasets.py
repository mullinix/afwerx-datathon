"""Methods to build dataset files."""

# builtins
import pathlib
from typing import Dict

# 3d party/FOSS
import pandas as pd

# this
from afwerx_datathon.io.csv import CSVReader
from afwerx_datathon.io.parquet import ParquetReader
from afwerx_datathon.io.path import DEV_DATA, get_pilots, get_runs, get_sessions
from afwerx_datathon.io.types import DataType, ExperimentType, PathLike


def build_all() -> Dict:
    """Method to build monolithic dataframes."""

    expr_type = ExperimentType.ils
    output = {}
    for dt_name in DataType.keys():
        data_type = DataType[dt_name]
        data = []

        for pilot_path in get_pilots(DEV_DATA, expr_type):
            pilot = pilot_path.name
            for session_path in get_sessions(pilot_path):
                session = session_path.name
                for run_path in get_runs(session_path):
                    run = run_path.name
                    try:
                        reader = CSVReader(run_path, data_type)
                        df_ = reader.read_all()
                        df_["pilot"] = pilot
                        df_["session"] = session
                        df_["run"] = run
                        data.append(df_)

                    except Exception:
                        msg = "Could not load data for "
                        msg += f"{pilot}/{session}/{run}\n"
                        msg += f"data type: {data_type.value}."
                        print(msg)
                        pass
        try:
            df = pd.concat(data, ignore_index=True)
            output[data_type] = df
        except Exception:
            print(f"Could not create monolith DF for {data_type.value}.")
            pass
    return output


def save_monolithic_data(data: Dict, location: PathLike = DEV_DATA) -> None:
    """Save monolithic data to parquet."""

    for data_type, df in data.items():
        out_file = pathlib.Path(location) / f"{data_type.value}.parquet"
        df.to_parquet(out_file)


def load_all(location: PathLike = DEV_DATA) -> Dict:
    """Method to load all monolithic datasets."""
    location = pathlib.Path(location)
    data = {}
    for dt_name in DataType.keys():
        data_type = DataType[dt_name]
        path = location / f"{data_type.value}.parquet"
        reader = ParquetReader(path)
        data[data_type] = reader.read_all()

    return data

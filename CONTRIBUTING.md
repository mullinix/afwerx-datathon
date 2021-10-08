# Contributing

Thank you for taking the time to contribute to afwerx-datathon. This guide will
assist you in setting up a development environment, understanding the project
tooling, and learning the coding guidelines.

## Setup

### Requirements

- `python3.7` or `python3.8`
- Python package `poetry`

### Establishing environment

- Run the following commands to setup an environment.
- Note: The `DATA_DIR` environment variable should point to
  `dataChallenge_release/data`.

```shell
git clone git@github.com:mullinix/afwerx-datathon.git
cd afwerx-datathon
poetry install
poetry shell
export DATA_DIR=/path/to/data
```

## Examples

### Load "dev" CSV data from "ils" experiments into monolithic dataframes

```python
from afwerx_datathon.io import datasets
data = datasets.build_all()
datasets.save_monolithic_data(data)
```

### Load monolithic data, remove known "bad" data, get "ECG" data

```python
from afwerx_datathon.io import datasets
from afwerx_datathon.io.types import DataType
data = datasets.load_all()
data = datasets.remove_undesirables(data)
data[DataType.ecg]
```

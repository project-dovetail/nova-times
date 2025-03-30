from typing import TypedDict

import numpy as np
from astropy.table import Table

DataStats = TypedDict(
    "DataStats",
    {
        "num_obs": int,
        "num_observers": int,
        "min_jd": float,
        "max_jd": float,
        "min_mag": float,
        "max_mag": float,
        "mean_mag": float,
        "median_mag": float,
    },
)


def describe_dataset(dataset: Table) -> DataStats:
    results = DataStats(
        num_obs=len(dataset),
        num_observers=len(set(dataset["Observer Code"])),
        min_jd=min(dataset["JD"]),
        max_jd=max(dataset["JD"]),
        min_mag=min(dataset["Magnitude"]),
        max_mag=max(dataset["Magnitude"]),
        mean_mag=np.round(np.mean(dataset["Magnitude"]), decimals=4),
        median_mag=np.median(dataset["Magnitude"]),
    )
    return results

from typing import TypedDict

import numpy as np
from astropy.table import Table


TimingData = TypedDict(
    "TimingData",
    {
        "band": str,
        "maximum_jd": float,
        "maximum_mag": float,
    },
)


def measure_time(dataset: Table) -> TimingData:
    mask = dataset.groups.keys["Band"] == "V"
    singleband_data = dataset.groups[mask]
    maximum_mag = min(singleband_data["Magnitude"])
    maximum_indx = np.argmin(singleband_data["Magnitude"])
    maximum_jd = singleband_data["JD"][maximum_indx]
    results = TimingData(
        band="V",
        maximum_jd=maximum_jd,
        maximum_mag=maximum_mag,
    )
    return results

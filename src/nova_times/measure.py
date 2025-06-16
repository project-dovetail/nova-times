from typing import Optional, TypedDict

import numpy as np
from astropy.table import Table

from nova_times.exceptions import MissingDataError

TimingData = TypedDict(
    "TimingData",
    {
        "band": str,
        "maximum_jd": float,
        "maximum_mag": float,
        "t2_mag": float,
        "t2_jd": float,
    },
)


def measure_time(dataset: Table, band: Optional[str] = None) -> TimingData:
    MINIMUM_NUM_DATA = 10
    if band is None:
        band = "V"
    mask = dataset.groups.keys["Band"] == band
    singleband_data = dataset.groups[mask]
    if len(singleband_data) < MINIMUM_NUM_DATA:
        raise MissingDataError(
            f"{len(singleband_data)} points in band {band}, {MINIMUM_NUM_DATA} required"
        )
    magnitudes = singleband_data["Magnitude"]
    jds = singleband_data["JD"]

    # maximum
    maximum_mag = min(magnitudes)
    maximum_indx = np.argmin(magnitudes)
    maximum_jd = jds[maximum_indx]

    # T2
    t2_mag_calc = maximum_mag + 2
    t2_indx = np.argmin(np.abs(magnitudes - t2_mag_calc))
    t2_mag = magnitudes[t2_indx]
    t2_jd = jds[t2_indx]

    results = TimingData(
        band=band,
        maximum_jd=maximum_jd,
        maximum_mag=maximum_mag,
        t2_mag=t2_mag,
        t2_jd=t2_jd,
    )
    return results

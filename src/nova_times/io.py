import pandas as pd
from astropy.io import ascii
from astropy.table import Table


def read_csv(filename: str) -> Table:
    data = ascii.read(filename).to_pandas()

    # clean up
    data["Magnitude"] = pd.to_numeric(data["Magnitude"], errors="coerce")

    return Table.from_pandas(data).group_by("Band")

from astropy.io import ascii
from astropy.table import Table


def read_csv(filename: str) -> Table:
    data = ascii.read(filename).group_by("Observer Code")
    return data

import numpy as np

from astropy.table import Table

from nova_times.io import read_csv


class TestReadCSV:

    def test_valid_datafile(self):
        result = read_csv("tests/data/aavso_000-BPZ-067.csv")
        assert isinstance(result, Table)

    def test_magnitudes_are_numbers(self):
        result = read_csv("tests/data/aavso_000-BPZ-067.csv")
        assert result["Magnitude"].dtype == np.float64

    def test_grouped_by_band(self):
        result = read_csv("tests/data/aavso_000-BPZ-067.csv")
        assert len(result.groups.keys) == 9

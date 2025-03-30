from astropy.table import Table

from nova_times.io import read_csv


class TestReadCSV:

    def test_valid_datafile(self):
        result = read_csv("tests/data/aavso_000-BPZ-067.csv")
        assert isinstance(result, Table)

    def test_grouped_by_observer(self):
        result = read_csv("tests/data/aavso_000-BPZ-067.csv")
        assert len(result.groups.keys) == 4

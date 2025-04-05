import pytest

from nova_times.describe import describe_dataset
from nova_times.io import read_csv


@pytest.fixture
def test_dataset():
    return read_csv("tests/data/aavso_000-BPZ-067.csv")


class TestDescribeDataset:

    def test_num_obs(self, test_dataset):
        result = describe_dataset(test_dataset)
        assert result["num_obs"] == 723

    def test_num_observers(self, test_dataset):
        result = describe_dataset(test_dataset)
        assert result["num_observers"] == 21

    def test_num_bands(self, test_dataset):
        result = describe_dataset(test_dataset)
        assert result["num_bands"] == 9

    def test_min_jd(self, test_dataset):
        result = describe_dataset(test_dataset)
        assert result["min_jd"] == 2460563.075515

    def test_max_jd(self, test_dataset):
        result = describe_dataset(test_dataset)
        assert result["max_jd"] == 2460762.825035

    def test_min_mag(self, test_dataset):
        result = describe_dataset(test_dataset)
        assert result["min_mag"] == 7.957

    def test_max_mag(self, test_dataset):
        result = describe_dataset(test_dataset)
        assert result["max_mag"] == 16.44

    def test_mean_mag(self, test_dataset):
        result = describe_dataset(test_dataset)
        assert result["mean_mag"] == pytest.approx(11.228, rel=0.001)

    def test_median_mag(self, test_dataset):
        result = describe_dataset(test_dataset)
        assert result["median_mag"] == pytest.approx(10.8465, rel=0.001)

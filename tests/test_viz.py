from unittest.mock import MagicMock

import pytest

from nova_times.io import read_csv
from nova_times.viz import viz_dataset


@pytest.fixture
def test_dataset():
    return read_csv("tests/data/aavso_000-BPZ-067.csv")


class TestVizDataset:

    def test_calls_scatter_for_all_bands(self, test_dataset):
        ax = MagicMock()

        viz_dataset(ax, test_dataset)
        assert ax.scatter.call_count == 9

    def test_can_plot_single_band(self, test_dataset):
        ax = MagicMock()

        viz_dataset(ax, test_dataset, "B")
        ax.scatter.assert_called_once()

from unittest.mock import patch

import pytest
from click.testing import CliRunner

from nova_times.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_cli(runner):
    result = runner.invoke(cli)
    assert result.exit_code == 0
    assert "Usage: nova-times" in result.output


def test_cli_help(runner):
    result = runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert "Usage: nova-times" in result.output


def test_cli_describe_requires_filename(runner):
    result = runner.invoke(cli, "describe")
    assert result.exit_code == 2


def test_cli_describe_w_invalid_filename(runner):
    result = runner.invoke(cli, ["describe", "bad_filename"])
    assert result.exit_code == 1
    assert "Error: Could not open file 'bad_filename'" in result.output


@patch("nova_times.cli.describe_dataset")
@patch("nova_times.cli.read_csv")
def test_cli_describe_valid(mock_read_csv, mock_describe_dataset, runner):
    mock_describe_dataset.return_value = {"num_obs": 123}
    result = runner.invoke(cli, ["describe", "good_filename"])
    assert result.exit_code == 0
    assert "num_obs: 123" in result.output
    mock_describe_dataset.assert_called_with(mock_read_csv.return_value)

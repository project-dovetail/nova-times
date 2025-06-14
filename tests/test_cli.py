import json
from unittest.mock import patch

import pytest
from click import FileError
from click.testing import CliRunner

from nova_times.cli import cli, read_file


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


@patch("nova_times.cli.read_csv")
def test_read_file(mock_read_csv):
    read_file("good_filename")
    mock_read_csv.assert_called_with("good_filename")


def test_read_invalid_file():
    with pytest.raises(FileError):
        read_file("bad_filename")


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
    mock_data = {"num_obs": 123, "num_bands": 3}
    mock_describe_dataset.return_value = mock_data
    result = runner.invoke(cli, ["describe", "good_filename"])
    assert result.exit_code == 0
    assert json.loads(result.output) == mock_data
    mock_read_csv.assert_called_with("good_filename")
    mock_describe_dataset.assert_called_with(mock_read_csv.return_value)


@patch("nova_times.cli.viz_dataset")
@patch("nova_times.cli.read_csv")
def test_cli_viz(mock_read_csv, mock_viz_dataset, tmp_path, runner):
    output_filename = tmp_path / "test_output_viz.pdf"
    result = runner.invoke(cli, ["viz", "good_filename", str(output_filename)])
    mock_read_csv.assert_called_with("good_filename")
    assert mock_read_csv.return_value in mock_viz_dataset.call_args[0]
    assert result.exit_code == 0
    assert output_filename in tmp_path.iterdir()
    assert len(list(tmp_path.iterdir())) == 1


@patch("nova_times.cli.viz_dataset")
@patch("nova_times.cli.read_csv")
def test_cli_viz_band(mock_read_csv, mock_viz_dataset, tmp_path, runner):
    output_filename = tmp_path / "test_output_viz.pdf"
    result = runner.invoke(
        cli, ["viz", "good_filename", str(output_filename), "--band", "band1"]
    )
    mock_read_csv.assert_called_with("good_filename")
    assert mock_read_csv.return_value in mock_viz_dataset.call_args[0]
    assert "band1" in mock_viz_dataset.call_args[0]
    assert result.exit_code == 0
    assert output_filename in tmp_path.iterdir()
    assert len(list(tmp_path.iterdir())) == 1


@patch("nova_times.cli.measure_time")
@patch("nova_times.cli.read_csv")
def test_cli_measure_default(mock_read_csv, mock_measure_time, runner):
    mock_measure_time.return_value = {"a": 1}
    result = runner.invoke(cli, ["measure", "good_filename"])
    mock_read_csv.assert_called_with("good_filename")
    assert mock_read_csv.return_value in mock_measure_time.call_args[0]
    assert result.exit_code == 0


@patch("nova_times.cli.measure_time")
@patch("nova_times.cli.read_csv")
def test_cli_measure_band(mock_read_csv, mock_measure_time, runner):
    mock_measure_time.return_value = {"a": 1}
    result = runner.invoke(cli, ["measure", "good_filename", "--band", "band1"])
    mock_read_csv.assert_called_with("good_filename")
    assert "band" in mock_measure_time.call_args[1]
    assert mock_measure_time.call_args[1]["band"] == "band1"
    assert mock_read_csv.return_value in mock_measure_time.call_args[0]
    assert result.exit_code == 0

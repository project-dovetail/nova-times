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


def test_cli_describe(runner):
    result = runner.invoke(cli, "describe")
    assert result.exit_code == 0
    assert "Describe" in result.output

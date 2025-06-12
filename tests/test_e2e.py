from click.testing import CliRunner

from nova_times.cli import cli


def test_e2e_describe():
    runner = CliRunner()
    result = runner.invoke(cli, ["describe", "tests/data/aavso_000-BPZ-067.csv"])
    assert result.exit_code == 0
    assert '"num_obs": 723' in result.output

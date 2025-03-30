import click

from nova_times.describe import describe_dataset
from nova_times.io import read_csv


@click.group("nova-times")
def cli() -> None:
    pass


@click.command()
@click.argument("filename", required=True)
def describe(filename: str) -> None:
    try:
        data_table = read_csv(filename)
    except FileNotFoundError as err:
        raise click.FileError(filename, hint=str(err))

    description = describe_dataset(data_table)

    for key, value in description.items():
        print(f"{key}: {value}")
    return


cli.add_command(describe)

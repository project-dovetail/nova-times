from typing import Optional

import click
import matplotlib.pyplot as plt

from nova_times.describe import describe_dataset
from nova_times.viz import viz_dataset
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


@click.command()
@click.argument("filename", required=True)
@click.argument("output_filename", required=True)
@click.option("-b", "--band", "band")
def viz(filename: str, output_filename: str, band: Optional[str] = None) -> None:
    try:
        data_table = read_csv(filename)
    except FileNotFoundError as err:
        raise click.FileError(filename, hint=str(err))

    fig, ax = plt.subplots()

    viz_dataset(ax, data_table, band)

    plt.savefig(output_filename)


cli.add_command(describe)
cli.add_command(viz)

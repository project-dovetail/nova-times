import json
from typing import Optional

import click
import matplotlib.pyplot as plt
from astropy.table import Table


from nova_times.describe import describe_dataset
from nova_times.measure import measure_time
from nova_times.measure import measure_tN
from nova_times.viz import viz_dataset
from nova_times.io import read_csv


@click.group("nova-times")
def cli() -> None:
    pass


def read_file(filename: str) -> Table:
    try:
        data_table = read_csv(filename)
    except FileNotFoundError as err:
        raise click.FileError(filename, hint=str(err))
    return data_table


@click.command()
@click.argument("filename", required=True)
def describe(filename: str) -> None:
    data_table = read_file(filename)

    description = describe_dataset(data_table)

    for key, value in description.items():
        print(f"{key}: {value}")
    return


@click.command()
@click.argument("filename", required=True)
@click.argument("output_filename", required=True)
@click.option("-b", "--band", "band")
def viz(filename: str, output_filename: str, band: Optional[str] = None) -> None:
    data_table = read_file(filename)

    fig, ax = plt.subplots()

    viz_dataset(ax, data_table, band)

    plt.savefig(output_filename)


@click.command()
@click.argument("filename", required=True)
# @click.argument("output_filename", required=True)
# @click.option("-b", "--band", "band")
def measure_times(filename: str) -> None:
    data_table = read_file(filename)

    timing_data = measure_time(data_table)

    print(json.dumps(timing_data, indent=4))

@click.command()
@click.argument("filename", required=True)
# @click.argument("output_filename", required=True)
# @click.option("-b", "--band", "band")
def measure_tNs(filename: str) -> None:
    data_table = read_file(filename)

    timing_data = measure_tN(data_table)

    print(json.dumps(timing_data, indent=4))    


cli.add_command(describe)
cli.add_command(viz)
cli.add_command(measure_times)
cli.add_command(measure_tNs)


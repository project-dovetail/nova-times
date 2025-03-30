import click


@click.group("nova-times")
def cli() -> None:
    pass


@click.command()
def describe() -> None:
    print("Nova Times CLI - Describe")
    return


cli.add_command(describe)

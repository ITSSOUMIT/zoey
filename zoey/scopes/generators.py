from pathlib import Path
import click


@click.command()
def site():
    click.echo('Generating an optimized build...')
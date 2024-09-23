from pathlib import Path
import click


@click.command()
def generate():
    click.echo('Generating an optimized build...')
    src_dir = Path('src')
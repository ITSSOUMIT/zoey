from pathlib import Path
import click
import shutil
import os


def clear_public_directory():
    public_directory = Path('public')
    if public_directory.exists():
        shutil.rmtree(public_directory)
        public_directory.mkdir()
    else:
        public_directory.mkdir()


def traverse_and_convert():
    src_directory = Path('src')
    public_directory = Path('public')
    for root, dirs, files in os.walk(src_directory):
        for file in files:
            src_file = Path(root) / file
            public_file = public_directory / src_file.relative_to(src_directory)
            public_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src_file, public_file)


@click.command()
def site():
    public_directory = Path('public')
    click.echo(click.style('Generating an optimized build...', fg='yellow'))
    click.echo(click.style('Emptying the public directory...', fg='red'))
    clear_public_directory()
    click.echo(click.style('Converting source files to HTML...', fg='yellow'))
    traverse_and_convert()
    click.echo(click.style(f'Your site is generated successfully inside {public_directory} directory', fg='green'))
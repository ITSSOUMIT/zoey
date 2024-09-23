from pathlib import Path
import click
import shutil
import pkg_resources


def all_groups():
    src_dir = Path('src')
    groups = [group.name for group in src_dir.iterdir() if group.is_dir()]
    groups.remove('assets')
    return groups


@click.command()
def groups():
    click.echo("Groups:")
    for group in all_groups():
        click.echo(f"- {group}")


@click.command()
@click.argument('name')
def group(name):
    if name == 'assets':
        click.echo("Error: 'assets' is a reserved word and cannot be used as a group name.")
        return
    src_dir = Path('src')
    src_dir.mkdir(exist_ok=True)
    group_dir = src_dir / name
    group_dir.mkdir(exist_ok=True)
    template_path = pkg_resources.resource_filename("zoey", "templates/page_base/single_page.md")
    page_path = group_dir / "index.md"
    shutil.copy(template_path, page_path)
    click.echo(f"Created new group: {name}")

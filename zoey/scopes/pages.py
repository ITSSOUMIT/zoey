from pathlib import Path
from .groups import all_groups
import click
import shutil
import pkg_resources


def create_page(name, template):
    src_dir = Path('src')
    src_dir.mkdir(exist_ok=True)
    template_path = pkg_resources.resource_filename("zoey", f"templates/page_base/{template}")
    page_path = src_dir / f"{name}.md"
    shutil.copy(template_path, page_path)
    return page_path


@click.command()
@click.argument('name')
@click.option('--group', default=None, help='Optional group name.')
def page(name, group):
    template_path = pkg_resources.resource_filename("zoey", "templates/page_base/single_page.md")
    if group is not None and group not in all_groups():
        click.echo(f"Error: group '{group}' does not exist.")
        return
    page_path = Path('src') / f"{name}.md" if group is None else Path('src') / group / f"{name}.md"
    shutil.copy(template_path, page_path)
    message = f'Created new page: {name}' if group is None else f'Created new page: {name} in group: {group}'
    message += f' at path: {page_path}'
    click.echo(message)
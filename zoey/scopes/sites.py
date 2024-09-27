from pathlib import Path
import click
import shutil
import pkg_resources


@click.command()
@click.argument('name')
def site(name):
    try:
        template_path = Path(pkg_resources.resource_filename('zoey', 'templates/project_base'))
        project_path = Path(name)
        shutil.copytree(template_path, project_path)
        for pycache_dir in project_path.glob('**/__pycache__'):
            shutil.rmtree(pycache_dir)
        click.echo(f"Created new project: {name}")
    except Exception as e:
        click.echo(f"Error creating project: {str(e)}")
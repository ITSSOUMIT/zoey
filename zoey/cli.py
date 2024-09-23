from .scopes.projects import project
from .scopes.pages import page
from .scopes.groups import group, groups
from .scopes.business import generate
import click


# zoey
@click.group()
def main():
    pass

main.add_command(generate)
main.add_command(groups)


# zoey new [command]
@main.group()
def new():
    pass

new.add_command(project)
new.add_command(page)
new.add_command(group)


# zoey
if __name__ == '__main__':
    main()
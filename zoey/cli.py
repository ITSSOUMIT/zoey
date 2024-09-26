from .scopes.sites import site
from .scopes.pages import page
from .scopes.groups import group, groups
from .scopes.generators import site as generate_site
import click


# zoey
@click.group()
def main():
    pass

main.add_command(groups)


# zoey new [command]
@main.group()
def new():
    pass

new.add_command(site)
new.add_command(page)
new.add_command(group)


# zoey generate [command]
@main.group()
def generate():
    pass

generate.add_command(generate_site)


# zoey
if __name__ == '__main__':
    main()
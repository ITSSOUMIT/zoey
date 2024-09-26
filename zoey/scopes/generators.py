from pathlib import Path
from datetime import datetime
import click
import shutil
import os
import re
import markdown
import importlib.util


def clear_public_directory():
    public_directory = Path('public')
    if public_directory.exists():
        shutil.rmtree(public_directory)
        public_directory.mkdir()
    else:
        public_directory.mkdir()


def update_css_colors():
    config_path = Path('config.py')
    spec = importlib.util.spec_from_file_location("config", config_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    color_code = getattr(config, 'color_code', {})
    red = color_code.get('red', 0)
    green = color_code.get('green', 0)
    blue = color_code.get('blue', 0)
    css_path = Path('src/assets/style.css')
    with css_path.open('r') as file:
        css_content = file.read()
    css_content = re.sub(
        r'--c-azure:\s*rgb\((\d+),\s*(\d+),\s*(\d+)\);',
        f'--c-azure: rgb({red}, {green}, {blue});',
        css_content
    )
    css_content = re.sub(
        r'--c-azure-light:\s*rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\);',
        f'--c-azure-light: rgba({red}, {green}, {blue}, 0.56);',
        css_content
    )
    with css_path.open('w') as file:
        file.write(css_content)


def extract_metadata_content(markdown_content):
    metadata_pattern = r'^""""(.*?)""""'
    match = re.match(metadata_pattern, markdown_content, re.DOTALL)
    if match:
        metadata_block = match.group(1).strip()
        content = re.sub(metadata_pattern, '', markdown_content, flags=re.DOTALL).strip()
        metadata = {}
        for line in metadata_block.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                if key.strip().lower() == 'tags':
                    metadata['tags'] = [tag.strip() for tag in value.split(',')]
                else:
                    metadata[key.strip().lower()] = value.strip()
        return metadata, content
    else:
        return {}, markdown_content
    

def get_relative_path(file_path, target):
    return os.path.relpath(target, os.path.dirname(file_path)).replace('\\', '/')


def convert_markdown_to_html(src_file, public_file):
    with open(src_file, 'r') as file:
        markdown_content = file.read()
    metadata, content = extract_metadata_content(markdown_content)
    html_content = markdown.markdown(content)
    title = metadata.get('title', 'Untitled')
    tags = metadata.get('tags', [])
    tags_html = ""
    if tags:
        tags_html = """
<div id="tags">
  Tags: 
  """ + ' '.join([f"<span>{tag}</span>" for tag in tags]) + """
</div>
"""
    relative_css_path = get_relative_path(public_file, os.path.join('public', 'assets', 'style.css'))
    relative_home_path = get_relative_path(public_file, os.path.join('public', 'index.html'))
    
    with open(public_file, 'w') as file:
        file.write(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" crossorigin="anonymous">
    <link rel="stylesheet" href="{relative_css_path}">
</head>
<body class='page-home'>
<header id="header">
<nav>
  <div>
    <a id="nav-home" href="{relative_home_path}" class='active'><svg id="nav-home-dot" width="12" height="12" xmlns="http://www.w3.org/2000/svg"><circle cx="6" cy="6" r="6" /></svg></a>
  </div>
</nav>
</header>
<section id="main">
<div id="content">
{html_content}
</div>
{tags_html}
</section>
</body>
</html>
        """)


def create_index_file(folder_path, public_folder_path):
    index_content = f"<ul id='links'>"
    for item in folder_path.iterdir():
        if item.is_file() and item.suffix.lower() == '.md':
            last_modified = datetime.fromtimestamp(item.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            link_name = item.stem
            link_path = item.with_suffix('.html').name
            index_content += f"<li><a href='{link_path}'>{link_name}</a><span class='date'>{last_modified}</span></li>\n"
    index_content += "</ul>"

    index_file_path = public_folder_path / f"{folder_path.name}-index.html"
    relative_css_path = get_relative_path(index_file_path, os.path.join('public', 'assets', 'style.css'))
    relative_home_path = get_relative_path(index_file_path, os.path.join('public', 'index.html'))
    with open(index_file_path, 'w') as file:
        file.write(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Index of {folder_path.name}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" crossorigin="anonymous">
    <link rel="stylesheet" href="{relative_css_path}">
</head>
<body class='page-home'>
<header id="header">
<nav>
  <div>
    <a id="nav-home" href="{relative_home_path}" class='active'><svg id="nav-home-dot" width="12" height="12" xmlns="http://www.w3.org/2000/svg"><circle cx="6" cy="6" r="6" /></svg></a>
  </div>
</nav>
</header>
<section id="main">
<div id="content">
{index_content}
</div>
</section>
</body>
</html>
        """)


def traverse_and_convert():
    src_directory = Path('src')
    public_directory = Path('public')
    for root, dirs, files in os.walk(src_directory):
        current_path = Path(root)
        public_path = public_directory / current_path.relative_to(src_directory)
        public_path.mkdir(parents=True, exist_ok=True)
        if current_path.name != 'assets' and current_path != src_directory:
            create_index_file(current_path, public_path)
        for file in files:
            src_file = current_path / file
            if src_file.suffix.lower() == '.md':
                public_file = public_path / src_file.with_suffix('.html').name
                convert_markdown_to_html(src_file, public_file)
            else:
                public_file = public_path / file
                shutil.copy(src_file, public_file)


@click.command()
def site():
    public_directory = Path('public')
    click.echo(click.style('Generating an optimized build...', fg='blue'))
    click.echo(click.style('Emptying the public directory...', fg='red'))
    clear_public_directory()
    click.echo(click.style('Installing the color palette...', fg='blue'))
    update_css_colors()
    click.echo(click.style('Converting source files to HTML...', fg='blue'))
    traverse_and_convert()
    click.echo(click.style(f'Your site is generated successfully inside {public_directory} directory', fg='green'))
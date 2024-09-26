from pathlib import Path
import click
import shutil
import os
import re
import markdown


def clear_public_directory():
    public_directory = Path('public')
    if public_directory.exists():
        shutil.rmtree(public_directory)
        public_directory.mkdir()
    else:
        public_directory.mkdir()


def get_relative_css_path(html_file_path):
    html_dir = os.path.dirname(html_file_path)
    relative_path = os.path.relpath(os.path.join('public', 'assets/style.css'), html_dir)
    return relative_path.replace('\\', '/')


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
                metadata[key.strip().lower()] = value.strip()
        return metadata, content
    else:
        return {}, markdown_content


def convert_markdown_to_html(src_file, public_file):
    with open(src_file, 'r') as file:
        markdown_content = file.read()
    metadata, content = extract_metadata_content(markdown_content)
    html_content = markdown.markdown(content)
    title = metadata.get('title', 'Untitled')
    relative_css_path = get_relative_css_path(public_file)
    with open(public_file, 'w') as file:
        file.write(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" crossorigin="anonymous" >
    <link rel="stylesheet" href="{relative_css_path}">
</head>
<body>
<section id="main">
{html_content}
</section>
</body>
</html>
        """)


def traverse_and_convert():
    src_directory = Path('src')
    public_directory = Path('public')
    for root, dirs, files in os.walk(src_directory):
        for file in files:
            src_file = Path(root) / file
            if src_file.suffix.lower() == '.md':
                public_file = public_directory / src_file.relative_to(src_directory).with_suffix('.html')
                public_file.parent.mkdir(parents=True, exist_ok=True)
                convert_markdown_to_html(src_file, public_file)
            else:
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
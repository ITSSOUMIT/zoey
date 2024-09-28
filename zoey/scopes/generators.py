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


def site_color_mode():
    config_path = Path('config.py')
    spec = importlib.util.spec_from_file_location("config", config_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    return getattr(config, 'color_mode', 'light')


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


def generate_header_links(current_file_path):
    src_directory = Path('src')
    links_html = ""

    for item in src_directory.iterdir():
        if item.name == 'assets':
            continue
        if item.is_file() and item.suffix.lower() == '.md' and item.name != 'index.md':
            # Generate link for the markdown file
            public_other_file = Path('public') / item.with_suffix('.html').name
            link_text = item.stem
            relative_link = get_relative_path(current_file_path, public_other_file)
            links_html += f"<a href='{relative_link}'>/{link_text}</a> "

        elif item.is_dir():
            # Generate link for the folder's index.html
            public_folder_index_file = Path('public') / item.name /f"{item.name}-index.html"
            relative_folder_link = get_relative_path(current_file_path, public_folder_index_file)
            links_html += f"<a href='{relative_folder_link}'>/{item.name}</a> "

    return links_html


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
    src_directory = Path('src')
    links_html = generate_header_links(public_file)
    relative_css_path = get_relative_path(public_file, os.path.join('public', 'assets', 'style.css')) if site_color_mode() == 'light' else get_relative_path(public_file, os.path.join('public', 'assets', 'style-dark.css'))
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
    {links_html}
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

    src_directory = Path('src')
    index_file_path = public_folder_path / f"{folder_path.name}-index.html"
    links_html = generate_header_links(index_file_path)
    relative_css_path = get_relative_path(index_file_path, os.path.join('public', 'assets', 'style.css')) if site_color_mode() == 'light' else get_relative_path(index_file_path, os.path.join('public', 'assets', 'style-dark.css'))
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
    {links_html}
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


def insert_footer():
    config_path = Path('config.py')
    spec = importlib.util.spec_from_file_location("config", config_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)

    # Extract footer information from the config
    footer_text = getattr(config, 'footer_text', '')
    social_mail = getattr(config, 'social_mail', '')
    social_linkedin = getattr(config, 'social_linkedin', '')
    social_github = getattr(config, 'social_github', '')
    social_instagram = getattr(config, 'social_instagram', '')
    social_twitter = getattr(config, 'social_twitter', '')
    social_facebook = getattr(config, 'social_facebook', '')

    # Social media icons
    social_icons = {
        'mail': ('fa-solid fa-envelope', social_mail),
        'linkedin': ('fa-brands fa-linkedin', social_linkedin),
        'github': ('fa-brands fa-github', social_github),
        'instagram': ('fa-brands fa-instagram', social_instagram),
        'twitter': ('fa-brands fa-twitter', social_twitter),
        'facebook': ('fa-brands fa-facebook', social_facebook),
    }

    # Create footer-left based on available social links
    footer_left = ''
    for social, class_link in social_icons.items():
        if class_link[1]:
            footer_left += f'<a href="{class_link[1]}" target="_blank"><i class="{class_link[0]}" style="color: #777;"></i></a>\n'

    # Construct footer-right only if footer_text is not empty
    footer_right = f'<div class="footer-right">{footer_text}</div>' if footer_text else ''
    footer_content = f"""
<footer>
  <div class="footer-left">
    {footer_left.strip()}
  </div>
  {footer_right}
</footer>
    """
    public_directory = Path('public')
    for html_file in public_directory.glob('**/*.html'):
        with open(html_file, 'r') as file:
            content = file.read()

        # Skip files that don't need a footer (optional, depending on your structure)
        if '</body>' not in content:
            continue

        # Insert footer before the closing </body> tag
        new_content = re.sub(r'(</body>)', f'{footer_content}\\1', content)
        with open(html_file, 'w') as file:
            file.write(new_content)


def is_zoey_workspace():
    return Path('src').exists() and Path('config.py').exists()


@click.command()
def site():
    if not is_zoey_workspace():
        click.echo(click.style('The current directory is not a Zoey workspace', fg='red'))
        return
    public_directory = Path('public')
    click.echo(click.style('Generating an optimized build...', fg='blue'))
    click.echo(click.style('Emptying the public directory...', fg='red'))
    clear_public_directory()
    click.echo(click.style('Installing the color palette...', fg='blue'))
    update_css_colors()
    click.echo(click.style('Converting source files to HTML...', fg='blue'))
    traverse_and_convert()
    insert_footer()
    click.echo(click.style(f'Your site is generated successfully inside {public_directory} directory', fg='green'))
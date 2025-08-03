from markdown import markdown_to_html_node
from markdown import extract_markdown_title
from os.path import join, abspath, isfile, dirname
from os import makedirs

def generate_page(from_path, template_path, dest_path, base_path, content_dir):
    if not isfile(abspath(from_path)):
        raise Exception("Provided mardown filepath is not a file.")
    if not isfile(abspath(template_path)):
        raise Exception("Provided template filepath is not a file.")
    if dest_path == "":
        raise Exception("No destination path provided.")
    if not from_path.endswith(".md"):
        raise Exception(f"{from_path} is not a markdown file.")

    markdown = ""
    with open(abspath(from_path), 'r') as source_file:
        markdown = source_file.read()
    if len(markdown) == 0:
        raise Exception("Markdown file is empty.")

    # Parse Markdown into HTML
    title = extract_markdown_title(markdown)
    html_node = markdown_to_html_node(markdown)
    html_str = html_node.to_html()

    with open(abspath(template_path), 'r') as template_file:
        template = template_file.read()

    # Insert html content into template.
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_str)
    # Update links and images to point to base path.
    template = template.replace('href="/', f'href="{base_path}')
    template = template.replace('src="/', f'src="{base_path}')

    # Create output file path.
    html_file = from_path[len(content_dir):-2] + 'html'
    output_file_path = abspath(dest_path) + html_file
    print(f'output_file_path = {output_file_path}')

    # Create subdirectories based on output file path hierarchy.
    makedirs(dirname(output_file_path), mode=0o777, exist_ok=True)
    with open(abspath(output_file_path), 'w') as output_file:
        output_file.write(template)

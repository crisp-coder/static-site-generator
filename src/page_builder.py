from markdown import markdown_to_html_node
from markdown import extract_markdown_title
from os.path import abspath, exists, isfile, isdir, dirname
from os import makedirs

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')

    if not isfile(abspath(from_path)):
        raise Exception("Provided mardown filepath is not a file.")
    if not isfile(abspath(template_path)):
        raise Exception("Provided template filepath is not a file.")
    if dest_path != "":
        makedirs(dirname(abspath(dest_path)), mode=0o777, exist_ok=True)

    markdown = ""
    with open(abspath(from_path), 'r') as source_file:
        markdown = source_file.read()

    #print(f'{markdown}')
    if markdown == "":
        raise Exception("Markdown file is empty.")

    # Parse Markdown into HTML
    title = extract_markdown_title(markdown)
    html_node = markdown_to_html_node(markdown)
    html_str = html_node.to_html()
    #print(f'{html_str}')

    with open(abspath(template_path), 'r') as template_file:
        template = template_file.read()

    #print(f'{template}')
    # Insert html content into Template.
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_str)

    #print(f'{template}')
    # Write out produced html file.
    with open(abspath(dest_path), 'w') as output_file:
        output_file.write(template)
    print(f'wrote template to {abspath(dest_path)}')
    print(f'Done')

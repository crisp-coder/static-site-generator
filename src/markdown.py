import re

from blocktype import *
from textnode import *
from htmlnode import *
from parentnode import *

def text_to_text_nodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_text_node_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_text_node_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_text_node_delimiter(nodes, "`", TextType.CODE)
    nodes = split_text_node_image(nodes)
    nodes = split_text_node_link(nodes)
    return nodes

def extract_markdown_title(text):
    matches = re.findall(r"^#\s.*", text, flags=re.MULTILINE)

    if len(matches) > 1:
        raise Exception("Only one H1 heading can be the title.")

    if len(matches) == 0:
        raise Exception("No title found.")

    if len(matches[0]) < 3:
        raise Exception("Markdown Heading 1 block is empty.")

    title = matches[0][2:]
    return title

def extract_markdown_links(text):
    links = []
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    for m in matches:
        links.append((m[0], m[1]))
    return links

def extract_markdown_images(text):
    images = []
    matches = re.findall(r'!\[([^\[\]]*)\]\(([^\(\)]*)\)', text)
    for m in matches:
        images.append((m[0], m[1]))
    return images

def split_text_node_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # Skip splitting if node is not a text node.
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_links(node.text)
        # If no matches, skip splitting the node.
        if len(matches) == 0:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        # Split text on each match.
        for link_match in matches:
            # link_match is a tuple (title, url)
            title = link_match[0]
            url = link_match[1]
            delimiter = f'[{title}]({url})'
            text_split = remaining_text.split(delimiter, 1)
            pre_text = text_split[0]

            # Skip adding text node if no text before match.
            if pre_text != "":
                new_nodes.append(TextNode(pre_text, TextType.TEXT))
            # Always add link node if match found
            new_nodes.append(TextNode(title, TextType.LINK, url))

            if len(text_split) > 1:
                remaining_text = text_split[1]
            else:
                break
        # Append remaining text as a text node.
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def split_text_node_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # Skip splitting if node is not a text node.
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_images(node.text)
        # If no matches, skip splitting the node.
        if len(matches) == 0:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        # Split text on each match.
        for img_match in matches:
            # img_match is a tuple (title, url)
            alt_text = img_match[0]
            url = img_match[1]
            delimiter = f'![{alt_text}]({url})'
            text_split = remaining_text.split(delimiter, 1)
            pre_text = text_split[0]

            # Skip adding text node if no text before match.
            if pre_text != "":
                new_nodes.append(TextNode(pre_text, TextType.TEXT))
            # Always add link node if match found
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

            if len(text_split) > 1:
                remaining_text = text_split[1]
            else:
                break

        # Append remaining text as a text node.
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def split_text_node_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        # Skip splitting if node is not a text node.
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Split the node into multiple nodes and add them in the old node's place
        if delimiter in node.text:
            new_text_list = node.text.split(delimiter)
            if len(new_text_list) % 2 != 1:
                raise Exception(f"Unmatched delimiter {delimiter}")

            # Track text type because some of the new nodes will still be text,
            # and some will have changed.
            next_text_type = TextType.TEXT
            for split_text in new_text_list:
                # Skip empty nodes
                if split_text != "":
                    new_node = TextNode(split_text, next_text_type, node.url)
                    new_nodes.append(new_node)

                # swap text types each iteration of loop.
                if next_text_type  == TextType.TEXT:
                    next_text_type  = text_type
                elif next_text_type  == text_type:
                    next_text_type  = TextType.TEXT

        # We still need to keep the node if no delimiter is found.
        else:
            new_nodes.append(node)
    return new_nodes

def markdown_to_blocks(markdown):
    text_blocks = markdown.split("\n\n")
    blocks = []
    for item in text_blocks:
        if item != "":
            blocks.append(item.strip())
    return blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_blocktype(block)
        node = ()
        match block_type:
            case BlockType.PARAGRAPH:
                node = paragraph_to_html_node(block)
            case BlockType.HEADING:
                node = heading_to_html_node(block)
            case BlockType.QUOTE:
                node = quote_to_html_node(block)
            case BlockType.CODE:
                node = code_to_html_node(block)
            case BlockType.UNORDERED_LIST:
                node = ul_to_html_node(block)
            case BlockType.ORDERED_LIST:
                node = ol_to_html_node(block)
            case _:
                raise Exception("Invalid BlockType")
        # Keep list of children to add to root node
        children.append(node)
    return ParentNode('div', children)

def text_nodes_to_children(text_nodes):
    children = []
    for child in text_nodes:
        children.append(text_node_to_html_node(child))
    return children

def paragraph_to_html_node(block):
    text = block.replace("\n", " ")
    text = text.strip()
    text_nodes = text_to_text_nodes(text)
    html_nodes = text_nodes_to_children(text_nodes)
    return ParentNode('p', html_nodes)

def heading_to_html_node(block):
    text = block.replace("\n", " ")
    count = 0
    for i in range(0, len(text)):
        if text[i] == '#':
            count += 1
        elif text[i] == ' ':
            break
        else:
            raise Exception("Heading block missing space after #")
    if count > 6:
        raise Exception("Heading block has too many #")

    text = block.lstrip('#')
    text = text.lstrip(' ')
    text_nodes = text_to_text_nodes(text)
    html_nodes = text_nodes_to_children(text_nodes)
    return ParentNode("h" + str(count), html_nodes)

def quote_to_html_node(block):
    text = block.replace("\n", "")
    text = text.replace(">", "")
    text = text.strip()
    text_nodes = text_to_text_nodes(text)
    html_nodes = text_nodes_to_children(text_nodes)
    return ParentNode('blockquote', html_nodes)

def code_to_html_node(block):
    text = block.lstrip("```")
    text = text.rstrip("```")
    text = text.lstrip()
    textnode = TextNode(text, TextType.CODE)
    html_node = text_node_to_html_node(textnode)
    return ParentNode('pre', [html_node])

def ul_to_html_node(block):
    text = block.replace("\n", "")
    items = text.split("- ")
    children = []
    for item in items:
        item.strip()
        if item == "":
            continue
        text_nodes = text_to_text_nodes(item)
        html_nodes = text_nodes_to_children(text_nodes)
        children.append(ParentNode('li', html_nodes))
    return ParentNode('ul', children)

def ol_to_html_node(block):
    text = block.replace("\n", " ")
    items = re.split(r'\d+\.\s', text)
    children = []
    for item in items:
        item = item.strip()
        if item == "":
            continue
        text_nodes = text_to_text_nodes(item)
        html_nodes = text_nodes_to_children(text_nodes)
        children.append(ParentNode('li', html_nodes))
    return ParentNode('ol', children)



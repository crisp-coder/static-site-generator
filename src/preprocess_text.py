import re

from textnode import TextType, TextNode
from leafnode import LeafNode

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    return nodes

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

def split_nodes_links(old_nodes):
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
            delim = f'[{title}]({url})'
            text_split = remaining_text.split(delim, 1)
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

def split_nodes_images(old_nodes):
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
            delim = f'![{alt_text}]({url})'
            text_split = remaining_text.split(delim, 1)
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

def text_node_to_html_node(text_node):
    match(text_node.text_type):
        case TextType.TEXT:
            return LeafNode(value=text_node.text)
        case TextType.BOLD:
            return LeafNode(
                "b",
                value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(
                "i",
                value=text_node.text)
        case TextType.CODE:
            return LeafNode(
                "code",
                value=text_node.text)
        case TextType.LINK:
            return LeafNode(
                "a",
                value=text_node.text,
                props={"href": f'"{text_node.url}"'})
        case TextType.IMAGE:
            return LeafNode(
                "img",
                value=text_node.text,
                props={"src":f'"{text_node.url}", "alt":"{text_node.text}"'})
        case _:
            raise Exception("Unmatched text type.")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
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



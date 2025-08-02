import re

from textnode import TextType
from leafnode import LeafNode

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



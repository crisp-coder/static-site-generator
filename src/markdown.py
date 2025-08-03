import re

from blocktype import *
from textnode import *
from htmlnode import *
from parentnode import *
from preprocess_text import *

def text_nodes_to_children(text_nodes):
    children = []
    for child in text_nodes:
        children.append(text_node_to_html_node(child))
    return children

def paragraph_to_html_node(block):
    text = block.replace("\n", " ")
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
    text_nodes = text_to_text_nodes(text)
    html_nodes = text_nodes_to_children(text_nodes)
    return ParentNode("h" + str(count), html_nodes)

def quote_to_html_node(block):
    text = block.replace("\n", " ")
    text = text.lstrip(">")
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
    text = block.replace("\n", " ")
    items = text.split("- ")
    children = []
    for item in items:
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


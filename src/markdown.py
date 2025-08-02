from blocktype import *
from textnode import *
from htmlnode import *
from parentnode import *
from preprocess_text import *

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_blocktype(block)
        node = ()
        match block_type:
            case BlockType.PARAGRAPH:
                text = block.replace("\n", " ")
                text_nodes = text_to_textnodes(text)
                html_nodes = text_nodes_to_children(text_nodes)
                node = ParentNode('p', html_nodes)
            case BlockType.HEADING:
                text = block.lstrip("#")
                text_nodes = text_to_text_nodes(text)
                html_nodes = text_nodes_to_children(text_nodes)
                node = ParentNode('h1', html_nodes)
            case BlockType.QUOTE:
                text = block.lstrip(">")
                text_nodes = text_to_text_nodes(text)
                html_nodes = text_nodes_to_children(text_nodes)
                node = ParentNode('blockquote', html_nodes)
            case BlockType.CODE:
                text = block.lstrip("```")
                text = text.rstrip("```")
                text = text.lstrip()
                textnode = TextNode(text, TextType.CODE)
                html_node = text_node_to_html_node(textnode)
                node = ParentNode('pre', [html_node])
            case BlockType.UNORDERED_LIST:
                node = ul_to_html_node(block)
            case BlockType.ORDERED_LIST:
                node = ol_to_html_node(block)
            case _:
                raise Exception("Invalid BlockType")
        # Keep list of children to add to root node
        children.append(node)
    final = ParentNode('div', children)
    #print(f'final=\n{final}')
    return final

# Convert all text nodes to appropriate html tag nodes
def text_nodes_to_children(text_nodes):
    children = []
    for child in text_nodes:
        children.append(text_node_to_html_node(child))
    return children

def ul_to_html_node(text):
    items = text.split("- ")
    children = []
    for item in items:
        text_nodes = text_to_text_nodes(item)
        html_nodes = text_nodes_to_children(text_nodes)
        children.append(ParentNode('li', html_nodes))

    return ParentNode('ul', children)

def ol_to_html_node(text):
    children = []
    for item in items:
        text_nodes = text_to_text_nodes(item)
        html_nodes = text_nodes_to_children(text_nodes)
        children.append(ParentNode('li', html_nodes))
    return ParentNode('ol', children)


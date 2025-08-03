from enum import Enum

from leafnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url

    def __eq__(self, other):
        return self.text == other.text \
        and self.text_type == other.text_type \
        and self.url == other.url

    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'

def text_node_to_html_node(text_node):
    output = ""
    match(text_node.text_type):
        case TextType.TEXT:
            output = LeafNode(value=text_node.text)
        case TextType.BOLD:
            output = LeafNode(
                tag="b",
                value=text_node.text)
        case TextType.ITALIC:
            output = LeafNode(
                tag="i",
                value=text_node.text)
        case TextType.CODE:
            output = LeafNode(
                tag="code",
                value=text_node.text)
        case TextType.LINK:
            output = LeafNode(
                tag="a",
                value=text_node.text,
                props={"href": f'{text_node.url}'})
        case TextType.IMAGE:
            output = LeafNode(
                tag="img",
                value=text_node.text,
                props={"src":f'{text_node.url}', "alt":f'{text_node.text}'})
        case _:
            raise Exception("Unmatched text type.")

    return output


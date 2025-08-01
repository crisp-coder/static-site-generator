from src.textnode import *
from src.htmlnode import *
from src.leafnode import *
from src.parentnode import *

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


def main():
    print("hello world")
    text_node = TextNode("This is some anchor text", "link", "https://github.com")
    node2 = text_node_to_html_node(text_node)
    print(node2)

if __name__ == "__main__":
    main()

import unittest

from src.htmlnode import HTMLNode
from src.leafnode import LeafNode
from src.textnode import TextNode, TextType

from src.main import text_node_to_html_node

class TestMain(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


if __name__ == "__main__":
    unittest.main()

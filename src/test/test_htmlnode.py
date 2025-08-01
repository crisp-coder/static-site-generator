import unittest

from src.htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node1, node2)

    def test_repr(self):
        html_str = "HTMLNode(tag=p, value=alaska, children=[], props={})"
        node = HTMLNode(tag='p', value='alaska')
        self.assertEqual(node.__repr__(), html_str)

    def test_props_to_html(self):
        node = HTMLNode(
            tag='p',
            value='alaska',
            children=[],
            props={"href": "https://test.com", "name": "NodeOne"})

        self.assertEqual(node.props_to_html(), ' href=\"https://test.com\" name=\"NodeOne\"')

if __name__ == "__main__":
    unittest.main()


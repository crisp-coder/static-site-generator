import unittest

from src.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node3 = TextNode("This is a text node", TextType.TEXT)
        node4 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node3, node4)

        node5 = TextNode("This is a text node", TextType.LINK, "https://github.com")
        node6 = TextNode("This is a text node", TextType.LINK, "https://github.com")
        self.assertEqual(node5, node6)

    def test_not_eq(self):
        node = TextNode("Larger than life.", TextType.TEXT)
        node2 = TextNode("Larger than life.", TextType.BOLD)
        self.assertFalse(node == node2)

        node3 = TextNode("Larger than life.", TextType.BOLD)
        self.assertFalse(node == node3)

        node4 = TextNode("Larger than life.", TextType.LINK, "https://help.com")
        node5 = TextNode("Larger than life.", TextType.LINK)
        node6 = TextNode("Larger than life.", TextType.LINK, "https://")
        self.assertFalse(node4 == node5)
        self.assertFalse(node4 == node6)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT)
        TextNode_STR = "TextNode(This is a text node, text, None)"
        self.assertEqual(node.__repr__(), TextNode_STR)

if __name__ == "__main__":
    unittest.main()


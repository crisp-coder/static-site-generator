import unittest

from textnode import TextNode, TextType
from splitnodes import split_nodes_delimiter

class TestSplitNodes(unittest.TestCase):
    def test_text_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ])

        node2 = TextNode("Here is a `block` of `code` that I wrote.", TextType.TEXT)
        new_nodes2 = split_nodes_delimiter([node2], '`', TextType.CODE)
        self.assertEqual(
            new_nodes2,
            [
                TextNode("Here is a ", TextType.TEXT),
                TextNode("block", TextType.CODE),
                TextNode(" of ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" that I wrote.", TextType.TEXT),
            ])


        node3 = TextNode("`Here` is a `block` of `code` that I wrote.````", TextType.TEXT)
        new_nodes3 = split_nodes_delimiter([node3], '`', TextType.CODE)
        self.assertEqual(
            new_nodes3,
            [
                TextNode("Here", TextType.CODE),
                TextNode(" is a ", TextType.TEXT),
                TextNode("block", TextType.CODE),
                TextNode(" of ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" that I wrote.", TextType.TEXT),
            ])

    def test_text_text(self):
        node = TextNode("This is text with a code block word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a code block word", TextType.TEXT)
            ])

        # Note that we still split in this case, we just keep the type of new nodes as text.
        node2 = TextNode("Here is a `block` of `code` that I wrote.", TextType.TEXT)
        new_nodes2 = split_nodes_delimiter([node2], '`', TextType.TEXT)
        self.assertEqual(
            new_nodes2,
            [
                TextNode("Here is a ", TextType.TEXT),
                TextNode("block", TextType.TEXT),
                TextNode(" of ", TextType.TEXT),
                TextNode("code", TextType.TEXT),
                TextNode(" that I wrote.", TextType.TEXT),
            ])

        node3 = TextNode("`Here` is a `block` of `code` that I wrote.````", TextType.TEXT)
        new_nodes3 = split_nodes_delimiter([node3], '#', TextType.CODE)
        self.assertEqual(
            new_nodes3,
            [
                TextNode("`Here` is a `block` of `code` that I wrote.````", TextType.TEXT)
            ])

    def test_text_italic(self):
        node = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("italic block", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ])

        node2 = TextNode("Here is a _block_ of _code_ that I wrote.", TextType.TEXT)
        new_nodes2 = split_nodes_delimiter([node2], '_', TextType.ITALIC)
        self.assertEqual(
            new_nodes2,
            [
                TextNode("Here is a ", TextType.TEXT),
                TextNode("block", TextType.ITALIC),
                TextNode(" of ", TextType.TEXT),
                TextNode("code", TextType.ITALIC),
                TextNode(" that I wrote.", TextType.TEXT),
            ])


        node3 = TextNode("_Here_ is a _block_ of _code_ that I wrote.____", TextType.TEXT)
        new_nodes3 = split_nodes_delimiter([node3], '_', TextType.ITALIC)
        self.assertEqual(
            new_nodes3,
            [
                TextNode("Here", TextType.ITALIC),
                TextNode(" is a ", TextType.TEXT),
                TextNode("block", TextType.ITALIC),
                TextNode(" of ", TextType.TEXT),
                TextNode("code", TextType.ITALIC),
                TextNode(" that I wrote.", TextType.TEXT),
            ])





if __name__ == "__main__":
    unittest.main()


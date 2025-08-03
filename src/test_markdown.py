import unittest

from textnode import TextNode, TextType
from markdown import *

class TestMarkdown(unittest.TestCase):
    def test_text_to_text_nodes(self):
        text = 'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        nodes = text_to_text_nodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )

    def test_extract_markdown_title(self):
        text="""
# This is the GOOD title
## This is an h2
### This is an h3

This is a paragraph.

- this is a ul
"""
        title = extract_markdown_title(text)
        self.assertEqual(title, "This is the GOOD title")

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            extract_markdown_links(text),
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev")
            ]
        )

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
            ]
        )

    def test_split_node_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_text_node_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ])

    def test_split_text_node_image(self):
        node = TextNode(
            "This is text with an image ![my image alt text](https://myimage.com/img.jpg) and ![img2alttext](https://myimage22.com/img2.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_text_node_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("my image alt text", TextType.IMAGE, "https://myimage.com/img.jpg"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "img2alttext", TextType.IMAGE, "https://myimage22.com/img2.jpg"
                ),
            ])

    def test_split_node_delimiter_empty(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_text_node_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [node])

    def test_split_text_node_delimiter_many_nodes(self):
        self.maxDiff = None
        nodes = []
        embedded_str = ""
        for i in range(10):
            if i % 3 == 0:
                embedded_str = "`code block`"
            elif i % 3 == 1:
                embedded_str = "**bold text**"
            elif i % 3 == 2:
                embedded_str = "_italic text_"


            nodes.append(
                TextNode(
                    f"This is node {i} and it has a {embedded_str} inside it.",
                    TextType.TEXT
                )
            )

        new_nodes1 = split_text_node_delimiter(nodes, "`", TextType.CODE)
        new_nodes2 = split_text_node_delimiter(new_nodes1, "_", TextType.ITALIC)
        new_nodes3 = split_text_node_delimiter(new_nodes2, "**", TextType.BOLD)

        self.assertEqual(
            new_nodes3,
            [
                TextNode("This is node 0 and it has a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" inside it.", TextType.TEXT),
                TextNode("This is node 1 and it has a ", TextType.TEXT),
                TextNode("bold text", TextType.BOLD),
                TextNode(" inside it.", TextType.TEXT),
                TextNode("This is node 2 and it has a ", TextType.TEXT),
                TextNode("italic text", TextType.ITALIC),
                TextNode(" inside it.", TextType.TEXT),
                TextNode("This is node 3 and it has a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" inside it.", TextType.TEXT),
                TextNode("This is node 4 and it has a ", TextType.TEXT),
                TextNode("bold text", TextType.BOLD),
                TextNode(" inside it.", TextType.TEXT),
                TextNode("This is node 5 and it has a ", TextType.TEXT),
                TextNode("italic text", TextType.ITALIC),
                TextNode(" inside it.", TextType.TEXT),
                TextNode("This is node 6 and it has a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" inside it.", TextType.TEXT),
                TextNode("This is node 7 and it has a ", TextType.TEXT),
                TextNode("bold text", TextType.BOLD),
                TextNode(" inside it.", TextType.TEXT),
                TextNode("This is node 8 and it has a ", TextType.TEXT),
                TextNode("italic text", TextType.ITALIC),
                TextNode(" inside it.", TextType.TEXT),
                TextNode("This is node 9 and it has a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" inside it.", TextType.TEXT),
            ]
        )

    def test_split_text_node_delimiter_text_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_text_node_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ])

        node2 = TextNode("Here is a `block` of `code` that I wrote.", TextType.TEXT)
        new_nodes2 = split_text_node_delimiter([node2], '`', TextType.CODE)
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
        new_nodes3 = split_text_node_delimiter([node3], '`', TextType.CODE)
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

    def test_split_text_node_delimiter_text_text(self):
        node = TextNode("This is text with a code block word", TextType.TEXT)
        new_nodes = split_text_node_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a code block word", TextType.TEXT)
            ])

        # Note that we still split in this case, we just keep the type of new nodes as text.
        node2 = TextNode("Here is a `block` of `code` that I wrote.", TextType.TEXT)
        new_nodes2 = split_text_node_delimiter([node2], '`', TextType.TEXT)
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
        new_nodes3 = split_text_node_delimiter([node3], '#', TextType.CODE)
        self.assertEqual(
            new_nodes3,
            [
                TextNode("`Here` is a `block` of `code` that I wrote.````", TextType.TEXT)
            ])

    def test_split_text_node_delimiter_text_italic(self):
        node = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        new_nodes = split_text_node_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("italic block", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ])

        node2 = TextNode("Here is a _block_ of _code_ that I wrote.", TextType.TEXT)
        new_nodes2 = split_text_node_delimiter([node2], '_', TextType.ITALIC)
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
        new_nodes3 = split_text_node_delimiter([node3], '_', TextType.ITALIC)
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

    def test_ordered_list(self):
        md = """
1. This is the first item.
2. Second item.
3. Third item
has a second line.
4. Fourth item has number 255 in it.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is the first item.</li><li>Second item.</li><li>Third item has a second line.</li><li>Fourth item has number 255 in it.</li></ol></div>",
        )


    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()

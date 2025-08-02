import unittest

from blocktype import BlockType, block_to_blocktype, markdown_to_blocks

class TestBlockType(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown_str = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(markdown_str)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_heading_block(self):
        markdown = """
# This is a heading 1

## This is a heading 2

### This is a heading 3

#### This is a heading 4

##### This is a heading 5

###### This is a heading 6
"""
        blocks = markdown_to_blocks(markdown)
        for b in blocks:
            self.assertEqual(BlockType.HEADING, block_to_blocktype(b))

    def test_code_block(self):
        markdown = """
``` This is a code block ```
"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(BlockType.CODE, block_to_blocktype(blocks[0]))

    def test_quote_block(self):
        markdown = """
> This is a quote block.
La Di Da. Aloha Broha.

> This is a second quote block.
"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(BlockType.QUOTE, block_to_blocktype(blocks[0]))

    def test_unordered_list(self):
        pass

    def test_ordered_list(self):
        pass

    def test_paragraph(self):
        pass

if __name__ == "__main__":
    unittest.main()

